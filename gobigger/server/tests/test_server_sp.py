import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
import numpy as np
import cv2
import multiprocessing as mp

from gobigger.utils import Border
from gobigger.server import ServerSP
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestServerSP:

    def test_init(self):
        server = ServerSP()
        assert True

    def test_spawn_balls(self):
        server = ServerSP()
        server.reset()

    def test_step_control_random(self):
        server = ServerSP()
        server.reset()
        obs = server.obs()
        fps_set = 20
        clock = pygame.time.Clock()
        render = RealtimePartialRender()
        for i in range(10):
            actions = {player_name: {ball[-1]: [random.uniform(-1, 1), random.uniform(-1, 1), -1]\
                        for ball in obs[1][0]['overlap']['clone']} \
                        for player_name in server.get_player_names()}
            done = server.step(actions=actions)
            obs = server.obs()
            render.fill(obs[0], obs[1][0], player_num_per_team=1, fps=10)
            render.show()
            clock.tick(fps_set)
        server.close()

    def test_obs(self):
        server = ServerSP()
        server.reset()
        obs = server.obs()
        for i in range(10):
            actions = {player_name: {ball[-1]: [random.uniform(-1, 1), random.uniform(-1, 1), -1]\
                        for ball in obs[1][0]['overlap']['clone']} \
                        for player_name in server.get_player_names()}
            done = server.step(actions=actions)
            obs = server.obs()
            logging.debug(obs[0])

    def test_obs_multi_player(self):
        server = ServerSP(dict(
            team_num=1, 
            player_num_per_team=2, 
        ))
        server.reset()
        obs = server.obs()
        for i in range(10):
            actions = {player_name: {ball[-1]: [random.uniform(-1, 1), random.uniform(-1, 1), -1]\
                        for ball in obs[1][0]['overlap']['clone']} \
                        for player_name in server.get_player_names()}
            done = server.step(actions=actions)
            obs = server.obs()
            logging.debug(obs[0])
