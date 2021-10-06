import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.envs import GoBiggerEnv

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestGoBiggerEnv:

    def test_env(self):
        env = GoBiggerEnv()
        env.seed(1000)
        global_state, screen_data_players = env.reset()
        assert len(screen_data_players) == env.server.team_num * env.server.player_num_per_team
        obs, reward, done, info = env.step(actions=None)
        global_state, screen_data_players = obs
        assert len(screen_data_players) == env.server.team_num * env.server.player_num_per_team
        env.close()
        assert True
