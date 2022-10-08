import os
import sys
import gym
import time

from gobigger.server import ServerSP
from gobigger.render import EnvRender
from .gobigger_env import GoBiggerEnv


class GoBiggerSPEnv(GoBiggerEnv):

    def init_server(self):
        self.server = ServerSP(cfg=self.server_cfg)
