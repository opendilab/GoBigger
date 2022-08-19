import random
from easydict import EasyDict
import uuid
import logging
import cv2
import os
import sys
import time
import numpy as np
import copy
import pickle
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from pygame.math import Vector2

from gobigger.utils import Border, create_collision_detection, deep_merge_dicts, PlayerStatesUtil, SequenceGenerator
from gobigger.playbacks import create_pb
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall
from gobigger.managers import FoodManager, SporeManager, ThornsManager, PlayerManager
from gobigger.configs import server_default_config


class Server:

    @staticmethod
    def default_config():
        cfg = copy.deepcopy(server_default_config)
        return EasyDict(cfg)

    def __init__(self, cfg=None, seed=None):
        self.cfg = Server.default_config()
        if isinstance(cfg, dict):
            cfg = EasyDict(cfg)
            self.cfg = deep_merge_dicts(self.cfg, cfg)
        self.update_match_ratio() # update match ratio
        logging.debug(self.cfg)
        self.team_num = self.cfg.team_num
        self.player_num_per_team = self.cfg.player_num_per_team
        self.map_width = self.cfg.map_width
        self.map_height = self.cfg.map_height
        self.frame_limit = self.cfg.frame_limit
        self.fps = self.cfg.fps
        self.frame_duration = 1 / self.fps
        self.collision_detection_type = self.cfg.collision_detection_type
        self.eat_ratio = self.cfg.eat_ratio

        self.playback_settings = self.cfg.playback_settings
        self.opening_settings = self.cfg.opening_settings
        self.manager_settings = self.cfg.manager_settings
        self.obs_settings = self.cfg.obs_settings

        self.seed(seed)
        self.border = Border(0, 0, self.map_width, self.map_height, self._random)
        self.last_frame_count = 0

        self.init_playback()
        self.init_opening()
        self.sequence_generator = SequenceGenerator()
        self.food_manager = FoodManager(self.manager_settings.food_manager, border=self.border, 
                                        random_generator=self._random, sequence_generator=self.sequence_generator)
        self.thorns_manager = ThornsManager(self.manager_settings.thorns_manager, border=self.border, 
                                            random_generator=self._random, sequence_generator=self.sequence_generator)
        self.spore_manager = SporeManager(self.manager_settings.spore_manager, border=self.border, 
                                          random_generator=self._random, sequence_generator=self.sequence_generator)
        self.player_manager  = PlayerManager(self.manager_settings.player_manager, border=self.border,
                                             team_num=self.team_num, player_num_per_team=self.player_num_per_team, 
                                             spore_manager_settings=self.cfg.manager_settings.spore_manager,
                                             random_generator=self._random, sequence_generator=self.sequence_generator)
        self.init_obs()
        self.collision_detection = create_collision_detection(self.collision_detection_type, border=self.border)

    def update_match_ratio(self):
        # map size
        self.cfg.map_width = int(self.cfg.map_width * math.sqrt(self.cfg.match_ratio))
        self.cfg.map_height = int(self.cfg.map_height * math.sqrt(self.cfg.match_ratio))
        # food
        self.cfg.manager_settings.food_manager.num_init = int(self.cfg.manager_settings.food_manager.num_init * self.cfg.match_ratio)
        self.cfg.manager_settings.food_manager.num_min = int(self.cfg.manager_settings.food_manager.num_min * self.cfg.match_ratio)
        self.cfg.manager_settings.food_manager.num_max = int(self.cfg.manager_settings.food_manager.num_max * self.cfg.match_ratio)
        # thorns
        self.cfg.manager_settings.thorns_manager.num_init = int(self.cfg.manager_settings.thorns_manager.num_init * self.cfg.match_ratio)
        self.cfg.manager_settings.thorns_manager.num_min = int(self.cfg.manager_settings.thorns_manager.num_min * self.cfg.match_ratio)
        self.cfg.manager_settings.thorns_manager.num_max = int(self.cfg.manager_settings.thorns_manager.num_max * self.cfg.match_ratio)

    def init_playback(self):
        self.diff_balls_remove = [[], [], [], []]
        self.diff_balls_modify = [{}, {}, {}, {}]
        self.playback_type = self.playback_settings.playback_type
        self.save_video = self.playback_settings.by_video.save_video
        self.save_frame = self.playback_settings.by_frame.save_frame
        self.playback_util = create_pb(self.playback_settings, fps=self.fps, map_width=self.map_width,
                                       map_height=self.map_height)

    def init_opening(self):
        self.custom_init_food = []
        self.custom_init_thorns = []
        self.custom_init_spore = []
        self.custom_init_clone = []
        opening_type = self.opening_settings.opening_type
        if opening_type == 'none':
            pass
        elif opening_type == 'handcraft':
            self.custom_init_food = self.opening_settings.handcraft.food
            self.custom_init_thorns = self.opening_settings.handcraft.thorns
            self.custom_init_spore = self.opening_settings.handcraft.spore
            self.custom_init_clone = self.opening_settings.handcraft.clone
        elif opening_type == 'from_frame':
            if self.frame_path and os.path.isfile(self.frame_path):
                with open(self.frame_path, 'rb') as f:
                    data = pickle.load(f)
                self.custom_init_food = data['food']
                self.custom_init_thorns = data['thorns']
                self.custom_init_spore = data['spore']
                self.custom_init_clone = data['clone']

    def init_obs(self):
        self.eats = {player_id: {'food': 0, 'thorns': 0, 'spore': 0, 'clone_self': 0, 'clone_team': 0, 'clone_other': 0, 'eaten': 0} \
                     for player_id in self.player_manager.get_player_names()}
        self.player_states_util = PlayerStatesUtil(self.obs_settings)

    def spawn_balls(self):
        '''
        Overview:
            Initialize all balls. If self.custom_init is set, initialize all balls based on it.
        '''
        self.food_manager.init_balls(custom_init=self.custom_init_food) # init food
        self.thorns_manager.init_balls(custom_init=self.custom_init_thorns) # init thorns
        self.spore_manager.init_balls(custom_init=self.custom_init_spore) # init spore
        self.player_manager.init_balls(custom_init=self.custom_init_clone) # init player
        if self.save_frame:
            for ball in self.food_manager.get_balls():
                self.diff_balls_modify[0][ball.ball_id] = ball.save()
            for ball in self.thorns_manager.get_balls():
                self.diff_balls_modify[1][ball.ball_id] = ball.save()
            for ball in self.spore_manager.get_balls():
                self.diff_balls_modify[2][ball.ball_id] = ball.save()
            for ball in self.player_manager.get_balls():
                self.diff_balls_modify[3][ball.ball_id] = ball.save()

    def step_one_frame(self, actions=None):
        moving_balls = [] # Record all balls in motion
        total_balls = [] # Record all balls
        # Update all player balls according to action
        if actions is not None and isinstance(actions, dict):
            for player in self.player_manager.get_players():
                if player.player_id in actions:
                    direction_x, direction_y, action_type = actions[player.player_id]
                    if direction_x is None or direction_y is None:
                        direction = None
                    else:
                        direction = Vector2(direction_x, direction_y)
                        if direction.length() > 1:
                            direction = direction.normalize()
                    if action_type == 1: # eject
                        tmp_spore_balls = player.eject(direction=direction)
                        for tmp_spore_ball in tmp_spore_balls:
                            if tmp_spore_ball:
                                self.spore_manager.add_balls(tmp_spore_ball)
                                if self.save_frame:
                                    self.diff_balls_modify[2][tmp_spore_ball.ball_id] = tmp_spore_ball.save()
                    elif action_type == 2: # split
                        self.player_manager.add_balls(player.split(direction=direction))
                    player.move(direction=direction, duration=self.frame_duration)
                    moving_balls.extend(player.get_balls())
                else:
                    player.move(duration=self.frame_duration)
                    moving_balls.extend(player.get_balls())
        else:
            for player in self.player_manager.get_players():
                player.move(duration=self.frame_duration)
                moving_balls.extend(player.get_balls())

        moving_balls = sorted(moving_balls, reverse=True) # Sort by size
        # Update the status of other balls after moving, and record the balls with status updates
        for thorns_ball in self.thorns_manager.get_balls():
            if thorns_ball.moving:
                thorns_ball.move(duration=self.frame_duration)
                if self.save_frame:
                    self.diff_balls_modify[1][thorns_ball.ball_id] = thorns_ball.save()
            moving_balls.append(thorns_ball)
        for spore_ball in self.spore_manager.get_balls():
            if spore_ball.moving:
                spore_ball.move(duration=self.frame_duration)
                if self.save_frame:
                    self.diff_balls_modify[2][spore_ball.ball_id] = spore_ball.save()
        # Adjust the position of all player balls
        eats = self.player_manager.adjust()
        for player_id, clone_self_num in eats.items():
            self.eats[player_id]['clone_self'] += clone_self_num
        # Collision detection
        total_balls.extend(self.player_manager.get_balls())
        total_balls.extend(self.thorns_manager.get_balls())
        total_balls.extend(self.spore_manager.get_balls())
        total_balls.extend(self.food_manager.get_balls())
        collisions_dict = self.collision_detection.solve(moving_balls, total_balls)
        # Process each ball in moving_balls
        for index, moving_ball in enumerate(moving_balls):
            if not moving_ball.is_remove and index in collisions_dict:
                for target_ball in collisions_dict[index]:
                    self.deal_with_collision(moving_ball, target_ball)
        # After each tick, check if there is a need to update food, thorns, and player rebirth
        new_food_balls = self.food_manager.step(duration=self.frame_duration)
        new_thorns_balls = self.thorns_manager.step(duration=self.frame_duration)
        self.spore_manager.step(duration=self.frame_duration)
        self.player_manager.step()
        self.last_frame_count += 1
        if self.save_frame:
            self.diff_balls_modify[0].update(new_food_balls)
            self.diff_balls_modify[1].update(new_thorns_balls)
            for ball in self.player_manager.get_balls():
                self.diff_balls_modify[3][ball.ball_id] = ball.save()

    def deal_with_collision(self, moving_ball, target_ball):
        if not moving_ball.is_remove and not target_ball.is_remove: # Ensure that the two balls are present
            if isinstance(moving_ball, CloneBall):
                if isinstance(target_ball, CloneBall):
                    if moving_ball.team_id != target_ball.team_id:
                        if moving_ball.score > target_ball.score and self.can_eat(moving_ball.score, target_ball.score):
                            moving_ball.eat(target_ball)
                            self.eats[moving_ball.player_id]['clone_other'] += 1
                            self.eats[target_ball.player_id]['eaten'] += 1
                            self.player_manager.remove_balls(target_ball)
                        elif self.can_eat(target_ball.score, moving_ball.score):
                            target_ball.eat(moving_ball)
                            self.eats[target_ball.player_id]['clone_other'] += 1
                            self.eats[moving_ball.player_id]['eaten'] += 1
                            self.player_manager.remove_balls(moving_ball)
                    elif moving_ball.player_id != target_ball.player_id:
                        if moving_ball.score > target_ball.score and self.can_eat(moving_ball.score, target_ball.score):
                            if self.player_manager.get_clone_num(target_ball) > 1:
                                moving_ball.eat(target_ball)
                                self.eats[moving_ball.player_id]['clone_team'] += 1
                                self.eats[target_ball.player_id]['eaten'] += 1
                                self.player_manager.remove_balls(target_ball)
                        elif self.can_eat(target_ball.score, moving_ball.score):
                            if self.player_manager.get_clone_num(moving_ball) > 1:
                                target_ball.eat(moving_ball)
                                self.eats[target_ball.player_id]['clone_team'] += 1
                                self.eats[moving_ball.player_id]['eaten'] += 1
                                self.player_manager.remove_balls(moving_ball)
                elif isinstance(target_ball, FoodBall):
                    moving_ball.eat(target_ball)
                    self.eats[moving_ball.player_id]['food'] += 1
                    if self.save_frame:
                        self.diff_balls_remove[0].append(target_ball.ball_id)
                    self.food_manager.remove_balls(target_ball)
                elif isinstance(target_ball, SporeBall):
                    moving_ball.eat(target_ball)
                    self.eats[moving_ball.player_id]['spore'] += 1
                    if self.save_frame:
                        self.diff_balls_remove[2].append(target_ball.ball_id)
                    self.spore_manager.remove_balls(target_ball)
                elif isinstance(target_ball, ThornsBall):
                    if moving_ball.score > target_ball.score and self.can_eat(moving_ball.score, target_ball.score):
                        ret = moving_ball.eat(target_ball, clone_num=self.player_manager.get_clone_num(moving_ball))
                        self.eats[moving_ball.player_id]['thorns'] += 1
                        if self.save_frame:
                            self.diff_balls_remove[1].append(target_ball.ball_id)
                        self.thorns_manager.remove_balls(target_ball)
                        if isinstance(ret, list): 
                            self.player_manager.add_balls(ret) 
            elif isinstance(moving_ball, ThornsBall):
                if isinstance(target_ball, CloneBall):
                    if moving_ball.score < target_ball.score and self.can_eat(target_ball.score, moving_ball.score): 
                        ret = target_ball.eat(moving_ball, clone_num=self.player_manager.get_clone_num(target_ball))
                        self.eats[target_ball.player_id]['thorns'] += 1
                        if self.save_frame:
                            self.diff_balls_remove[1].append(moving_ball.ball_id)
                        self.thorns_manager.remove_balls(moving_ball)
                        if isinstance(ret, list): 
                            self.player_manager.add_balls(ret) 
                elif isinstance(target_ball, SporeBall): 
                    moving_ball.eat(target_ball)
                    if self.save_frame:
                        self.diff_balls_remove[2].append(target_ball.ball_id)
                    self.spore_manager.remove_balls(target_ball)
            elif isinstance(moving_ball, SporeBall):
                if isinstance(target_ball, CloneBall) or isinstance(target_ball, ThornsBall): 
                    target_ball.eat(moving_ball)
                    if isinstance(target_ball, CloneBall):
                        self.eats[target_ball.player_id]['spore'] += 1
                    if self.save_frame:
                        self.diff_balls_remove[2].append(moving_ball.ball_id)
                        if isinstance(target_ball, ThornsBall):
                            self.diff_balls_modify[1][target_ball.ball_id] = target_ball.save()
                    self.spore_manager.remove_balls(moving_ball)
        else:
            return

    def can_eat(self, score1, score2):
        if score1 > self.eat_ratio * score2:
            return True
        else:
            return False

    def reset(self):
        self.last_frame_count = 0
        self.init_playback()
        self.init_opening()
        self.food_manager.reset()
        self.thorns_manager.reset()
        self.spore_manager.reset()
        self.player_manager.reset()
        self.spawn_balls()
        self.init_obs()
        self._end_flag = False

    def step(self, actions=None, save_frame_full_path='', **kwargs):
        if not self._end_flag:
            self.step_one_frame(actions)
            if self.playback_util.need_save(self.last_frame_count):
                if self.save_video:
                    self.playback_util.save_step(food_balls=self.food_manager.get_balls(),
                                                 thorns_balls=self.thorns_manager.get_balls(),
                                                 spore_balls=self.spore_manager.get_balls(),
                                                 players=self.player_manager.get_players(),
                                                 player_num_per_team=self.player_num_per_team)
                elif self.save_frame:
                    self.playback_util.save_step(diff_balls_remove=self.diff_balls_remove,
                                                 diff_balls_modify=self.diff_balls_modify,
                                                 leaderboard=self.leaderboard,
                                                 last_frame_count=self.last_frame_count)
                    self.diff_balls_remove = [[], [], [], []]
                    self.diff_balls_modify = [{}, {}, {}, {}]
        if self.last_frame_count >= self.frame_limit:
            if not self._end_flag:
                self.playback_util.save_final(self.cfg)
            self._end_flag = True
        return self._end_flag

    def obs(self, obs_type='all'):
        assert obs_type in ['all', 'single']
        global_state = self.get_global_state()
        player_states = self.player_states_util.get_player_states(food_balls=self.food_manager.get_balls(),
                                                                  thorns_balls=self.thorns_manager.get_balls(),
                                                                  spore_balls=self.spore_manager.get_balls(),
                                                                  players=self.player_manager.get_players())
        self.leaderboard = global_state['leaderboard']
        return global_state, player_states, {'eats': self.eats}

    def get_global_state(self):
        team_name_score = self.player_manager.get_teams_score()
        global_state = {
            'border': [self.map_width, self.map_height],
            'total_frame': self.frame_limit,
            'last_frame_count': self.last_frame_count,
            'last_time':self.last_frame_count,
            'leaderboard': {
                i: team_name_score[i] for i in range(self.team_num)
            }
        }
        return global_state

    def get_player_names(self):
        return self.player_manager.get_player_names()

    def get_team_names(self):
        return self.player_manager.get_team_names()

    def get_player_names_with_team(self):
        return self.player_manager.get_player_names_with_team()

    def get_team_infos(self):
        return self.player_manager.get_team_infos()

    def close(self):
        if hasattr(self, 'render'):
            self.render.close()

    def seed(self, seed=None):
        if seed is None:
            self._seed = random.randrange(sys.maxsize)
        else:
            self._seed = seed
        self._random = random.Random(self._seed)
