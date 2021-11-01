import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.players import BasePlayer
from gobigger.balls import ThornsBall, SporeBall, CloneBall, FoodBall
from gobigger.utils import Border
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestBasePlayer:

    def test_all(self):
        base_player = BasePlayer(name='test')
        with pytest.raises(Exception) as e:
            base_player.move(direction=None)
        with pytest.raises(Exception) as e:
            base_player.eject()
        with pytest.raises(Exception) as e:
            base_player.eat(ball=None)
        with pytest.raises(Exception) as e:
            base_player.stop()
        with pytest.raises(Exception) as e:
            base_player.respawn()
