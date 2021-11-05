import random
from easydict import EasyDict
import uuid
import logging
import cv2
import os
import time
import numpy as np
import copy

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from pygame.math import Vector2

from gobigger.utils import Border, create_collision_detection, deep_merge_dicts
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall
from gobigger.managers import FoodManager, SporeManager, ThornsManager, PlayerManager
from .server_default_config import server_default_config


class Server:
    '''
    Overview:
        Server is responsible for the management of the entire game environment, including the status of all balls in the environment, and the status update after the action is entered
        The main logic when updating is as follows:
        0 tick -> input action -> update the state of the player's ball -> update the state of all balls after the current state continues for 1 tick
            -> detect collision and eating (update status) -> 0 tick end/1 tick start
        The details are as follows:
        1. Generate all balls (food, thorns, players)
        2. Single step
            1. Modify the current state of all players' balls according to the action (including acceleration, instantaneous state after splitting/spitting)
            2. Continue a tick for the current state of all balls, that is, update the acceleration/velocity/position of each ball after a tick, and at the same time the ball that is in the moving state in this tick
            3. Adjust all balls in each player (rigid body collision + ball-ball fusion)
            4. For each ball moved in this tick (already sorted by priority):
                1. We will know which balls he collided with (there will be repetitions)
                2. Category discussion
                    1. One of the balls is the player ball
                        1. Another is another player's ball, the bigger one eats the smaller one
                        2. The other side is your own clone, in fact, you don’t need to deal with it if you have already dealt with it before.
                        3. Another is food/spores, player ball eat it
                        4. Another is the thornball
                            1. Do not touch the center of the circle, continue
                            2. Hit the center of the circle
                                1. player ball is older than thornball
                                    1. number of player's avatar reaches the upper limit, thornball will be eaten
                                    2. number of player's avatar doesn't reache the upper limit, player ball eat thornball and blow up
                                2. player ball is younger than thornball, nothing happened
                    2. One of the balls is a thornball
                        1. Another is the player ball
                            1. hit the center of a circle
                                1. player ball is older than thornball
                                    1. number of player's avatar reaches the upper limit, thornball will be eaten
                                    2. number of player's avatar doesn't reache the upper limit, player ball eat thornball and blow up
                                2. player ball is younger than thornball, nothing happened
                            2. Do not touch the center of the circle, continue,
                        2. The another is the spore, thornball eat it and add a speed and acceleration
                    3. One of the balls is Spore
                        1. Another is the player ball, Spore was eaten
                        2. Another is the thorn ball, Spore was eaten
        3. After each tick, check if you want to update food, thorns, and player rebirth
    '''

    @staticmethod
    def default_config():
        cfg = copy.deepcopy(server_default_config)
        return EasyDict(cfg)

    def __init__(self, cfg=None):
        self.cfg = Server.default_config()
        if isinstance(cfg, dict):
            cfg = EasyDict(cfg)
            self.cfg = deep_merge_dicts(self.cfg, cfg)
        logging.debug(self.cfg)
        self.team_num = self.cfg.team_num
        self.player_num_per_team = self.cfg.player_num_per_team
        self.map_width = self.cfg.map_width
        self.map_height = self.cfg.map_height
        self.match_time = self.cfg.match_time
        self.state_tick_per_second = self.cfg.state_tick_per_second
        self.action_tick_per_second = self.cfg.action_tick_per_second
        # other kwargs
        self.state_tick_duration = 1 / self.state_tick_per_second
        self.action_tick_duration = 1 / self.action_tick_per_second
        self.state_tick_per_action_tick = self.state_tick_per_second // self.action_tick_per_second

        self.custom_init = self.cfg.custom_init
        self.save_video = self.cfg.save_video
        self.save_path = self.cfg.save_path
        self.obs_settings = self.cfg.obs_settings
        
        self.border = Border(0, 0, self.map_width, self.map_height)
        self.last_time = 0
        self.screens_all = []
        self.screens_partial = {}

        self.food_manager = FoodManager(self.cfg.manager_settings.food_manager, border=self.border)
        self.thorns_manager = ThornsManager(self.cfg.manager_settings.thorns_manager, border=self.border)
        self.spore_manager = SporeManager(self.cfg.manager_settings.spore_manager, border=self.border)
        self.player_manager  = PlayerManager(self.cfg.manager_settings.player_manager, border=self.border,
                                             team_num=self.team_num, player_num_per_team=self.player_num_per_team, 
                                             spore_manager_settings=self.cfg.manager_settings.spore_manager)

        self.collision_detection_type = self.cfg.collision_detection_type
        self.collision_detection = create_collision_detection(self.collision_detection_type, border=self.border)

    def spawn_balls(self):
        '''
        Overview:
            Initialize all balls. If self.custom_init is set, initialize all balls based on it.
        '''
        # check custom_init
        custom_init_food = self.custom_init.food if self.custom_init.food else None
        custom_init_thorns = self.custom_init.thorns if self.custom_init.thorns else None
        custom_init_spore = self.custom_init.spore if self.custom_init.spore else None
        custom_init_clone = self.custom_init.clone if self.custom_init.clone else None
        # init
        self.food_manager.init_balls(custom_init=custom_init_food) # init food
        self.thorns_manager.init_balls(custom_init=custom_init_thorns) # init thorns
        self.spore_manager.init_balls(custom_init=custom_init_spore) # init spore
        self.player_manager.init_balls(custom_init=custom_init_clone) # init player

    def step_state_tick(self, actions=None):
        moving_balls = [] # Record all balls in motion
        total_balls = [] # Record all balls
        # Update all player balls according to action
        if actions is not None:
            '''
            In a single action: 
              If sporulation and splitting operations occur at the same time, sporulation will be given priority
              If move and stop move occur at the same time in action, perform stop move operation
            '''
            for player in self.player_manager.get_players():
                direction_x, direction_y, action_type = actions[player.name]
                if direction_x is None or direction_y is None:
                    direction = None
                else:
                    direction = Vector2(direction_x, direction_y).normalize()
                if action_type == 0 or action_type == 3: # eject
                    tmp_spore_balls = player.eject(direction=direction)
                    for tmp_spore_ball in tmp_spore_balls:
                        if tmp_spore_ball:
                            self.spore_manager.add_balls(tmp_spore_ball) 
                if action_type == 1 or action_type == 4: # split 
                    self.player_manager.add_balls(player.split(direction=direction))
                if action_type == 2: # stop moving
                    player.stop()
                elif action_type == 3 or action_type == 4: # move on old direction
                    player.move(duration=self.state_tick_duration)
                    moving_balls.extend(player.get_balls())
                else: # move on new direction
                    player.move(direction=direction, duration=self.state_tick_duration)
                    moving_balls.extend(player.get_balls())
        else:
            for player in self.player_manager.get_players():
                player.move(duration=self.state_tick_duration)
                moving_balls.extend(player.get_balls())
                total_balls.extend(player.get_balls())
        moving_balls = sorted(moving_balls, reverse=True) # Sort by size
        # Update the status of other balls after moving, and record the balls with status updates
        for thorns_ball in self.thorns_manager.get_balls():
            if thorns_ball.moving:
                thorns_ball.move(duration=self.state_tick_duration)
            moving_balls.append(thorns_ball)
        for spore_ball in self.spore_manager.get_balls():
            if spore_ball.moving:
                spore_ball.move(duration=self.state_tick_duration)
        # Adjust the position of all player balls
        self.player_manager.adjust()
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
        self.food_manager.step(duration=self.state_tick_duration)
        self.spore_manager.step(duration=self.state_tick_duration)
        self.thorns_manager.step(duration=self.state_tick_duration)
        self.player_manager.step()
        self.last_time += self.state_tick_duration

    def deal_with_collision(self, moving_ball, target_ball):
        if not moving_ball.is_remove and not target_ball.is_remove: # Ensure that the two balls are present
            if isinstance(moving_ball, CloneBall): 
                if isinstance(target_ball, CloneBall):
                    if moving_ball.team_name != target_ball.team_name:
                        if moving_ball.size > target_ball.size:
                            moving_ball.eat(target_ball)
                            self.player_manager.remove_balls(target_ball)
                        else:
                            target_ball.eat(moving_ball)
                            self.player_manager.remove_balls(moving_ball)
                    elif moving_ball.owner != target_ball.owner:
                        if moving_ball.size > target_ball.size:
                            if self.player_manager.get_clone_num(target_ball) > 1:
                                moving_ball.eat(target_ball)
                                self.player_manager.remove_balls(target_ball)
                        else:
                            if self.player_manager.get_clone_num(moving_ball) > 1:
                                target_ball.eat(moving_ball)
                                self.player_manager.remove_balls(moving_ball)
                elif isinstance(target_ball, FoodBall):
                    moving_ball.eat(target_ball)
                    self.food_manager.remove_balls(target_ball)
                elif isinstance(target_ball, SporeBall):
                    moving_ball.eat(target_ball)
                    self.spore_manager.remove_balls(target_ball)
                elif isinstance(target_ball, ThornsBall):
                    if moving_ball.size > target_ball.size:
                        ret = moving_ball.eat(target_ball, clone_num=self.player_manager.get_clone_num(moving_ball))
                        self.thorns_manager.remove_balls(target_ball)
                        if isinstance(ret, list): 
                            self.player_manager.add_balls(ret) 
            elif isinstance(moving_ball, ThornsBall):
                if isinstance(target_ball, CloneBall):
                    if moving_ball.size < target_ball.size: 
                        ret = target_ball.eat(moving_ball, clone_num=self.player_manager.get_clone_num(target_ball))
                        self.thorns_manager.remove_balls(moving_ball)
                        if isinstance(ret, list): 
                            self.player_manager.add_balls(ret) 
                elif isinstance(target_ball, SporeBall): 
                    moving_ball.eat(target_ball)
                    self.spore_manager.remove_balls(target_ball)
            elif isinstance(moving_ball, SporeBall):
                if isinstance(target_ball, CloneBall) or isinstance(target_ball, ThornsBall): 
                    target_ball.eat(moving_ball)
                    self.spore_manager.remove_balls(moving_ball)
        else:
            return

    def start(self):
        self.spawn_balls()
        self._end_flag = False

    def stop(self):
        self._end_flag = True

    def reset(self):
        self.last_time = 0
        self.screens_all = []
        self.screens_partial = {}
        self.food_manager.reset()
        self.thorns_manager.reset()
        self.spore_manager.reset()
        self.player_manager.reset()
        self.start()

    def record_frame_for_video(self):
        if self.save_video:
            screen_data_all, screen_data_players = self.render.get_tick_all_colorful(
                food_balls=self.food_manager.get_balls(),
                thorns_balls=self.thorns_manager.get_balls(),
                spore_balls=self.spore_manager.get_balls(),
                players=self.player_manager.get_players(),
                player_num_per_team=self.player_num_per_team,
                team_name_size=self.player_manager.get_teams_size())
            self.screens_all.append(screen_data_all)
            for player_name, screen_data_player in screen_data_players.items():
                if player_name not in self.screens_partial:
                    self.screens_partial[player_name] = []
                self.screens_partial[player_name].append(screen_data_player)

    def step(self, actions=None, **kwargs):
        if self.last_time >= self.match_time:
            if self.save_video:
                self.save_mp4(save_path=self.save_path)
            self.stop()
            return True
        if not self._end_flag:
            for i in range(self.state_tick_per_action_tick):
                if i == 0:
                    self.step_state_tick(actions)
                    self.record_frame_for_video()
                else:
                    self.step_state_tick()
                    self.record_frame_for_video()
        return False

    def set_render(self, render):
        self.render = render
        self.render.set_obs_settings(self.obs_settings)

    def obs(self, obs_type='all'):
        assert obs_type in ['all', 'single']
        assert hasattr(self, 'render')
        team_name_size = self.player_manager.get_teams_size()
        global_state = {
            'border': [self.map_width, self.map_height],
            'total_time': self.match_time,
            'last_time': self.last_time,
            'leaderboard': {
                str(i): team_name_size[str(i)] for i in range(self.team_num)
            }
        }
        _, screen_data_players = self.render.update_all(food_balls=self.food_manager.get_balls(),
                                                        thorns_balls=self.thorns_manager.get_balls(),
                                                        spore_balls=self.spore_manager.get_balls(),
                                                        players=self.player_manager.get_players())
        return global_state, screen_data_players

    def save_mp4(self, save_path=''):
        # self.video_id = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        self.video_id = str(uuid.uuid1())
        fps = self.state_tick_per_second
        # save all
        video_file = os.path.join(save_path, '{}-all.mp4'.format(self.video_id))
        out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (self.screens_all[0].shape[1], self.screens_all[0].shape[0]))
        for screen in self.screens_all:
            out.write(screen)
        out.release()
        cv2.destroyAllWindows()
        # save partial
        for player_name, screens in self.screens_partial.items():
            video_file = os.path.join(save_path, '{}-{:02d}.mp4'.format(self.video_id, int(player_name)))
            out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, screens[0].shape[:2])
            for screen in screens:
                out.write(screen)
            out.release()
            cv2.destroyAllWindows()

    def get_player_names(self):
        return self.player_manager.get_player_names()

    def get_team_names(self):
        return self.player_manager.get_team_names()

    def get_player_names_with_team(self):
        return self.player_manager.get_player_names_with_team()

    def close(self):
        self.stop()
        if hasattr(self, 'render'):
            self.render.close()

    def seed(self, seed):
        self._seed = seed
        np.random.seed(self._seed)
        random.seed(self._seed)
