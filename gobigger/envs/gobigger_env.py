import os
import sys
import gym

from gobigger.server import Server
from gobigger.render import EnvRender


class GoBiggerEnv(gym.Env):

    def __init__(self, server_cfg=None):
        self.server_cfg = server_cfg
        self.server = Server(cfg=server_cfg)
        self.server.set_render(render=EnvRender(self.server.map_width, self.server.map_height))

    def step(self, actions):
        done = self.server.step(actions=actions)
        obs = self.server.obs()
        global_state, screen_data_players = obs
        total_size = [global_state['leaderboard'][str(i)] \
                        for i in range(len(global_state['leaderboard']))]
        assert len(self.last_total_size) == len(total_size)
        reward = [total_size[i] - self.last_total_size[i] for i in range(len(total_size))]
        self.last_total_size = total_size
        info = {}
        return obs, reward, done, info

    def reset(self):
        self.server.reset()
        obs = self.server.obs()
        global_state, screen_data_players = obs
        self.last_total_size = [global_state['leaderboard'][str(i)] \
                                for i in range(len(global_state['leaderboard']))]
        return obs

    def close(self):
        self.server.close()

    def seed(self, seed):
        self.server.seed(seed)
