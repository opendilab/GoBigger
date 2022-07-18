import os
import sys
import gym
import time

from gobigger.server import Server
from gobigger.render import EnvRender
import copy


class GoBiggerEnv(gym.Env):

    def __init__(self, server_cfg=None, step_mul=1):
        self.server_cfg = server_cfg
        self.step_mul = step_mul
    
    def step(self, actions):
        for i in range(self.step_mul):
            if i==0:
                done = self.server.step(actions=actions)
            else:
                done = self.server.step(actions=None)
        obs_raw = self.server.obs()
        global_state, player_states, info = obs_raw
        obs = [global_state, player_states]
        total_score = [global_state['leaderboard'][i] \
                        for i in range(len(global_state['leaderboard']))]
        assert len(self.last_total_score) == len(total_score)
        reward = [total_score[i] - self.last_total_score[i] for i in range(len(total_score))]
        self.last_total_score = total_score
        return obs, reward, done, info

    def reset(self):
        self.init_server()
        self.server.reset()
        obs_raw = self.server.obs()
        global_state, player_states, info = obs_raw
        obs = [global_state, player_states]
        self.last_total_score = [global_state['leaderboard'][i] \
                                for i in range(len(global_state['leaderboard']))]
        return obs

    def close(self):
        self.server.close()

    def seed(self, seed):
        self.server.seed(seed)

    def get_team_infos(self):
        assert hasattr(self, 'server'), "Please call `reset()` first"
        return self.server.get_team_infos()

    def init_server(self):
        self.server = Server(cfg=self.server_cfg)
