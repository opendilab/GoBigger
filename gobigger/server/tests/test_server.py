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
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestServer:

    def test_init(self):
        server = Server()
        assert True

    def test_spawn_balls(self):
        server = Server()
        server.reset()

    def test_step_control_random(self):
        server = Server()
        server.reset()
        fps_set = 20
        clock = pygame.time.Clock()
        render = RealtimePartialRender()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                        for player_name in server.get_player_names()}
            done = server.step(actions=actions)
            obs = server.obs()
            render.fill(obs[0], obs[1][0], player_num_per_team=1, fps=10)
            render.show()
            clock.tick(fps_set)
        server.close()

    def test_obs(self):
        server = Server()
        server.reset()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                        for player_name in server.get_player_names()}
            done = server.step(actions=actions)
            obs = server.obs()
            logging.debug(obs[0])

    def test_obs_multi_player(self):
        server = Server(dict(
            team_num=1, 
            player_num_per_team=2, 
        ))
        server.reset()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                        for player_name in server.get_player_names()}
            done = server.step(actions=actions)
            obs = server.obs()
            logging.debug(obs[0])

    def test_multiprocessing(self):
        '''
        Overview:
            Test the server in a multi-process environment
        '''
        server_num = 2
        servers = []
        for i in range(server_num):
            server = Server(dict(
                team_num=1,
                player_num_per_team=1, 
                match_time=60*1,
            ))
            server.reset()
            servers.append(server)

        def run(server_index):
            for i in range(server_num):
                actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                            for player_name in servers[server_index].get_player_names()}
                done = servers[server_index].step(actions=actions)
                global_state, players_obs, info = servers[server_index].obs()
                logging.debug('{} {} {}'.format(server_index, i, global_state))
            logging.debug('{} start close'.format(server_index))
            logging.debug('{} finish'.format(server_index))

        ps = []
        for i in range(server_num):
            p = mp.Process(target=run, args=(i,), daemon=True)
            ps.append(p)

        for p in ps:
            p.start()

        for p in ps:
            p.join()

