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
        server.start()
        render = RealtimeRender(server.map_width, server.map_height)
        render.fill(server)
        render.show()
        render.close()

    def test_step_control_random(self):
        server = Server()
        server.start()
        fps_set = 20
        clock = pygame.time.Clock()
        render = RealtimeRender(server.map_width, server.map_height)
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                        for player_name in server.get_player_names()}
            server.step(actions=actions)
            render.fill(server)
            render.show()
            clock.tick(fps_set)
        render.close()
        server.close()

    def test_obs(self):
        server = Server()
        server.start()
        render = EnvRender(server.map_width, server.map_height)
        server.set_render(render)
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                        for player_name in server.get_player_names()}
            if not server.step(actions):
                global_state, players_obs = server.obs()
            else:
                logging.debug('finish!')
                break
            logging.debug(global_state)

        render.close()

    def test_obs_multi_player(self):
        server = Server(dict(
            team_num=1, 
            player_num_per_team=2, 
        ))
        render = EnvRender(server.map_width, server.map_height)
        server.set_render(render)
        server.start()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                        for player_name in server.get_player_names()}
            if not server.step(actions):
                global_state, players_obs = server.obs()
            else:
                logging.debug('finish!')
                break
            logging.debug(global_state)
        render.close()

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
            render = EnvRender(server.map_width, server.map_height)
            server.set_render(render)
            server.start()
            servers.append(server)

        def run(server_index):
            for i in range(server_num):
                actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                            for player_name in servers[server_index].get_player_names()}
                if not servers[server_index].step(actions):
                    global_state, players_obs = servers[server_index].obs()
                else:
                    logging.debug('finish!')
                    break
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

