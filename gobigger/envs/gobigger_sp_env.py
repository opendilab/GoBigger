import os
import sys
import gym
import time

from gobigger.server import ServerSP
from gobigger.render import EnvRender
from .gobigger_env import GoBiggerEnv


class GoBiggerSPEnv(GoBiggerEnv):

    def reset(self):
        self.server = ServerSP(cfg=self.server_cfg)
        self.server.reset()
        obs = self.server.obs()
        global_state, player_states = obs
        self.last_total_size = [global_state['leaderboard'][i] \
                                for i in range(len(global_state['leaderboard']))]
        return obs
