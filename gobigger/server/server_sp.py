import copy
from easydict import EasyDict
from pygame.math import Vector2
import logging

from gobigger.utils import Border, create_collision_detection, deep_merge_dicts, PlayerStatesSPUtil
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall
from gobigger.managers import FoodManager, SporeManager, ThornsManager, PlayerManager, PlayerSPManager
from gobigger.configs import server_sp_default_config
from .server import Server


class ServerSP(Server):

    @staticmethod
    def default_config():
        cfg = copy.deepcopy(server_sp_default_config)
        return EasyDict(cfg)

    def __init__(self, cfg=None, seed=None):
        self.cfg = ServerSP.default_config()
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
        self.food_manager = FoodManager(self.manager_settings.food_manager, border=self.border, 
                                        random_generator=self._random)
        self.thorns_manager = ThornsManager(self.manager_settings.thorns_manager, border=self.border, 
                                            random_generator=self._random)
        self.spore_manager = SporeManager(self.manager_settings.spore_manager, border=self.border, 
                                          random_generator=self._random)
        self.player_manager  = PlayerSPManager(self.manager_settings.player_manager, border=self.border,
                                               team_num=self.team_num, player_num_per_team=self.player_num_per_team, 
                                               spore_manager_settings=self.cfg.manager_settings.spore_manager,
                                               random_generator=self._random)
        self.init_obs()
        self.collision_detection = create_collision_detection(self.collision_detection_type, border=self.border)

    def init_obs(self):
        self.eats = {player_id: {'food': 0, 'thorns': 0, 'spore': 0, 'clone_self': 0, 'clone_team': 0, 'clone_other': 0, 'eaten': 0} \
                     for player_id in self.player_manager.get_player_names()}
        self.player_states_util = PlayerStatesSPUtil(self.obs_settings)

    def step_one_frame(self, actions=None):
        moving_balls = [] # Record all balls in motion
        total_balls = [] # Record all balls
        # Update all player balls according to action
        if actions is not None and isinstance(actions, dict):
            for player in self.player_manager.get_players():
                if player.player_id in actions:
                    for ball_id, action in actions[player.player_id].items():
                        direction_x, direction_y, action_type = action
                        if direction_x is None or direction_y is None:
                            direction = None
                        else:
                            direction = Vector2(direction_x, direction_y)
                            if direction.length() > 1:
                                direction = direction.normalize()
                        if action_type == 1: # eject
                            tmp_spore_balls = player.eject(ball_id, direction=direction)
                            for tmp_spore_ball in tmp_spore_balls:
                                if tmp_spore_ball:
                                    self.spore_manager.add_balls(tmp_spore_ball)
                        elif action_type == 2: # split
                            self.player_manager.add_balls(player.split(ball_id, direction=direction))
                        player.move(ball_id, direction=direction, duration=self.frame_duration)
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
            moving_balls.append(thorns_ball)
        for spore_ball in self.spore_manager.get_balls():
            if spore_ball.moving:
                spore_ball.move(duration=self.frame_duration)
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
        self.food_manager.step(duration=self.frame_duration)
        self.spore_manager.step(duration=self.frame_duration)
        self.thorns_manager.step(duration=self.frame_duration)
        self.player_manager.step()
        self.last_frame_count += 1
