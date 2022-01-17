import logging
import pytest

from gobigger.hyper import StraightMergeHyperAction, QuarterMergeHyperAction, EighthMergeHyperAction
from gobigger.server import Server
from gobigger.render import EnvRender

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestHyperActions:

    def test_straight_merge(self):
        server = Server(dict(
            team_num=1,
            player_num_per_team=2,
            map_width=600,
            map_height=600,
            match_time=10 * 1,
            state_tick_per_second=20,  # frame
            action_tick_per_second=5,  # frame
        ))
        server.start()
        render = EnvRender(server.map_width, server.map_height)
        server.set_render(render)
        server.player_manager.get_players()[0].get_balls()[0].set_size(420)
        server.player_manager.get_players()[1].get_balls()[0].set_size(100)
        player_name1 = server.player_manager.get_players()[0].name
        player_name2 = server.player_manager.get_players()[1].name
        sm_action = StraightMergeHyperAction(player_name1, player_name2)

        for _ in range(4):
            obs = server.obs()
            sm_action.update(obs[1][player_name1], obs[1][player_name2])
            actions = sm_action.get()
            server.step(actions=actions)

    def test_quarter_merge(self):
        server = Server(dict(
            team_num=1,
            player_num_per_team=2,
            map_width=600,
            map_height=600,
            match_time=10 * 1,
            state_tick_per_second=20,  # frame
            action_tick_per_second=5,  # frame
        ))
        server.start()
        render = EnvRender(server.map_width, server.map_height)
        server.set_render(render)
        server.player_manager.get_players()[0].get_balls()[0].set_size(420)
        server.player_manager.get_players()[1].get_balls()[0].set_size(100)
        player_name1 = server.player_manager.get_players()[0].name
        player_name2 = server.player_manager.get_players()[1].name
        qm_action = QuarterMergeHyperAction(player_name1, player_name2)

        for _ in range(4):
            obs = server.obs()
            qm_action.update(obs[1][player_name1], obs[1][player_name2])
            actions = qm_action.get()
            server.step(actions=actions)

    def test_eighth_merge(self):
        server = Server(dict(
            team_num=1,
            player_num_per_team=2,
            map_width=600,
            map_height=600,
            match_time=10 * 1,
            state_tick_per_second=20,  # frame
            action_tick_per_second=5,  # frame
        ))
        server.start()
        render = EnvRender(server.map_width, server.map_height)
        server.set_render(render)
        server.player_manager.get_players()[0].get_balls()[0].set_size(420)
        server.player_manager.get_players()[1].get_balls()[0].set_size(100)
        player_name1 = server.player_manager.get_players()[0].name
        player_name2 = server.player_manager.get_players()[1].name
        em_action = EighthMergeHyperAction(player_name1, player_name2)

        for _ in range(4):
            obs = server.obs()
            em_action.update(obs[1][player_name1], obs[1][player_name2])
            actions = em_action.get()
            server.step(actions=actions)
