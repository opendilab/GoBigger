import os
import uuid
import cv2

import numpy as np
import copy
from easydict import EasyDict
import logging

from _cgobigger import Server as CServer
from _cgobigger import OutputBall, DefaultServer

from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config


def transfer_cfg_to_cserver_config(cfg):
    default_server = DefaultServer()
    default_server.team_num = cfg.team_num
    default_server.player_num_per_team = cfg.player_num_per_team
    default_server.map_width = cfg.map_width
    default_server.map_height = cfg.map_height
    default_server.match_time = cfg.match_time
    default_server.state_tick_per_second = cfg.state_tick_per_second
    default_server.action_tick_per_second = cfg.action_tick_per_second
    if 'seed' in cfg and cfg.seed:
        default_server.seed = cfg.seed
    return default_server


class Server:

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
        default_server = DefaultServer()
        default_server.team_num = self.cfg.team_num
        default_server.player_num_per_team = self.cfg.player_num_per_team
        default_server.map_width = self.cfg.map_width
        default_server.map_height = self.cfg.map_height
        default_server.match_time = self.cfg.match_time
        default_server.state_tick_per_second = self.cfg.state_tick_per_second
        default_server.action_tick_per_second = self.cfg.action_tick_per_second
        if 'seed' in self.cfg and self.cfg.seed:
            default_server.seed = self.cfg.seed
        self.server = CServer(default_server)
        self.team_num = self.cfg.team_num
        self.player_num_per_team = self.cfg.player_num_per_team
        self.map_width = self.cfg.map_width
        self.map_height = self.cfg.map_height
        self.match_time = self.cfg.match_time
        self.state_tick_per_second = self.cfg.state_tick_per_second
        self.action_tick_per_second = self.cfg.action_tick_per_second
        self.save_video = self.cfg.save_video
        self.save_quality = self.cfg.save_quality
        self.save_path = self.cfg.save_path
        self.jump_to_frame_file = self.cfg.jump_to_frame_file
        self.state_tick_per_action_tick = self.state_tick_per_second // self.action_tick_per_second

        self.screens_all = []
        self.screens_partial = {}

        self.null_actions = self.get_null_actions()

    def format_actions(self, actions):
        actions_format = {}
        for player_name, action in actions.items():
            if action[0] is None or action[1] is None:
                actions_format[player_name] = [0.0, 0.0, -1]
            else:
                actions_format[player_name] = action
        return actions_format

    def get_null_actions(self):
        actions = {}
        for i in range(self.team_num):
            for j in range(self.player_num_per_team):
                actions[str(i*self.player_num_per_team+j)] = [0.0, 0.0, -1]
        return actions

    def step(self, actions, save_frame_full_path='', **kwargs):
        self.save_frame_info(save_frame_full_path)
        actions = self.format_actions(actions)
        if self.get_last_time() >= self.match_time:
            if self.save_video:
                self.save_mp4(save_path=self.save_path)
            return True
        for i in range(self.state_tick_per_action_tick):
            if i == 0:
                self.step_state_tick(actions)
            else:
                self.step_state_tick(self.null_actions)
        return False

    def step_state_tick(self, actions):
        self.server.step_state_tick(actions)

    def get_global_state(self, obs_raw):
        player_sizes = obs_raw[self.player_num_per_team * self.team_num * 4 + 4:
                               self.player_num_per_team * self.team_num * 5 + 4, 5]
        team_name_size = {str(i): 0 for i in range(self.team_num)}
        for i, player_size in enumerate(player_sizes):
            team_name_size[str(i//self.player_num_per_team)] += player_size
        global_state = {
            'border': [self.map_width, self.map_height],
            'total_time': self.match_time,
            'last_time': self.get_last_time(),
            'leaderboard': {
                str(i): team_name_size[str(i)] for i in range(self.team_num)
            }
        }
        return global_state

    def get_player_states(self, obs_raw):
        row_num, col_num = obs_raw.shape
        ball_obs_raw = obs_raw[:, :5]
        food_end, thorns_end, spore_end, clone_end = obs_raw[:4, 5]
        player_states = {str(i): {'overlap': {}, 'team_name': str(i//self.player_num_per_team),
                                  'rectangle': [int(obs_raw[i*4+4][5]), int(obs_raw[i*4+5][5]),
                                                int(obs_raw[i*4+6][5]), int(obs_raw[i*4+7][5])]}
                         for i in range(self.player_num_per_team * self.team_num)}
        last_end = 0
        for key_name, end in zip(['food', 'thorns', 'spore', 'clone'],
                                 [int(food_end), int(thorns_end), int(spore_end), int(clone_end)]):
            target_ball_obs_raw = ball_obs_raw[last_end:end, :5]
            for i in range(6, col_num):
                obs_player = np.compress((obs_raw[last_end:end, i]>0), target_ball_obs_raw, axis=0)
                player_states[str(i-6)]['overlap'].update({key_name: obs_player})
            last_end = end
        return player_states

    def obs(self, with_raw=False):
        """
        Get the raw obs from CServer
        :param with_raw: use in render, to get raw obs to render all balls.
        :return:
            global_state: a dict, including border, total time, last time, leaderboard
            player_states: a dict, including all players' states
            obs_raw: return when with_raw is True, including raw info of the obs
        """
        obs_raw = self.server.obs_partial_array()
        global_state = self.get_global_state(obs_raw)
        player_states = self.get_player_states(obs_raw)
        self.record_frame_for_video(obs_raw)
        if not with_raw:
            return global_state, player_states
        else:
            return global_state, player_states, obs_raw

    def start(self):
        self.server.start()

    def reset(self):
        self.server.reset(self.jump_to_frame_file)

    def set_render(self, render):
        self.render = render

    def transform_obs_to_balls_and_rects(self, obs):
        food_end, thorns_end, spore_end, clone_end = obs[:4, 5]
        food_balls = obs[:int(food_end), :5]
        thorns_balls = obs[int(food_end):int(thorns_end), :5]
        spore_balls = obs[int(thorns_end):int(spore_end), :5]
        clone_balls = obs[int(spore_end):int(clone_end), :5]
        rects = {str(i): [int(obs[i*4+4][5]), int(obs[i*4+5][5]), int(obs[i*4+6][5]), int(obs[i*4+7][5])]
                 for i in range(self.player_num_per_team * self.team_num)}
        return food_balls, thorns_balls, spore_balls, clone_balls, rects

    def record_frame_for_video(self, obs_raw):
        if self.save_video:
            food_balls, thorns_balls, spore_balls, clone_balls, rects = self.transform_obs_to_balls_and_rects(obs_raw)
            screen_data_all, screen_data_players = self.render.get_tick_all_colorful(
                food_balls=food_balls,
                thorns_balls=thorns_balls,
                spore_balls=spore_balls,
                clone_balls=clone_balls,
                player_num_per_team=self.player_num_per_team,
                team_num=self.team_num,
                rectangle_dict=rects)
            self.screens_all.append(screen_data_all)
            for player_name, screen_data_player in screen_data_players.items():
                if player_name not in self.screens_partial:
                    self.screens_partial[player_name] = []
                self.screens_partial[player_name].append(screen_data_player)

    def save_mp4(self, save_path=''):
        # self.video_id = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        self.video_id = str(uuid.uuid1())
        fps = self.state_tick_per_second if self.save_quality == 'high' else self.action_tick_per_second
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

    def save_frame_info(self, save_frame_full_path=''):
        if save_frame_full_path != '':
            self.server.save_frame_info(save_frame_full_path)

    def load_frame_info(self, jump_to_frame_file):
        if jump_to_frame_file:
            self.server.load_frame_info(jump_to_frame_file)

    def get_player_names(self):
        return self.server.get_player_names()

    def get_player_names_with_team(self):
        ret = []
        for i in range(self.team_num):
            ret.append([])
            for j in range(self.player_num_per_team):
                ret[-1].append(str(i*self.player_num_per_team+j))
        return retß

    def get_team_names(self):
        return self.server.get_team_names()

    def get_last_time(self):
        return self.server.last_time

    def close(self):
        self.server.close()
