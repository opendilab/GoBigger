import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.envs import GoBiggerSPEnv

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestGoBiggerEnv:

    def test_env(self):
        env = GoBiggerSPEnv()
        obs = env.reset()
        env.seed(1000)
        obs, reward, done, info = env.step(actions=None)
        global_state, player_states = obs
        assert len(player_states) == env.server.team_num * env.server.player_num_per_team
        env.close()
        assert True
