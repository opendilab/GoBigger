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
        self.step_time_all = 0
        self.obs_time_all = 0
        self.step_mul = step_mul
    
    def step(self, actions):
        t1 = time.time()
        for i in range(self.step_mul):
            if i==0:
                done = self.server.step(actions=actions)
            else:
                done = self.server.step(actions=None)
        t2 = time.time()
        obs = self.server.obs()
        t3 = time.time()
        self.step_time_all += t2 - t1
        self.obs_time_all += t3 - t2
        global_state, player_states = obs
        total_score = [global_state['leaderboard'][i] \
                        for i in range(len(global_state['leaderboard']))]
        assert len(self.last_total_score) == len(total_score)
        reward = [total_score[i] - self.last_total_score[i] for i in range(len(total_score))]
        self.last_total_score = total_score
        info = [t2-t1, self.step_time_all/global_state['last_frame_count'], 
                t3-t2, self.obs_time_all/global_state['last_frame_count'],]
        return obs, reward, done, info

    def reset(self):
        self.init_server()
        self.server.reset()
        obs = self.server.obs()
        global_state, player_states = obs
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
