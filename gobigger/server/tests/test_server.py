import logging
import pytest
import pygame
import random
import multiprocessing as mp

from gobigger.server import Server
from gobigger.render import RealtimeRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestServer:

    def test_init(self):
        server = Server()
        assert True

    def test_step_control_random(self):
        server = Server()
        server.reset()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                       for player_name in server.get_player_names()}
            server.step(actions=actions)
        server.close()

    def test_obs(self):
        server = Server()
        server.reset()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                       for player_name in server.get_player_names()}
            if not server.step(actions):
                global_state, players_obs = server.obs()
            else:
                logging.debug('finish!')
                break
            logging.debug(global_state)

    def test_obs_multi_player(self):
        server = Server(dict(
            team_num=1,
            player_num_per_team=2,
        ))
        server.reset()
        for i in range(10):
            actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                       for player_name in server.get_player_names()}
            if not server.step(actions):
                global_state, players_obs = server.obs()
            else:
                logging.debug('finish!')
                break
            logging.debug(global_state)

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

