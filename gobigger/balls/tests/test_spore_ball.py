import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import SporeBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestSporesBall:

    def test_move(self):
        name = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        size = SporeBall.default_config().spore_radius_init ** 2
        direction = Vector2(1, 0)
        spore_ball = SporeBall(name, position, border=border, size=size, vel=None, acc=None, direction=direction)
        logging.debug('direction={}, position={}, vel={}, acc={}'
            .format(spore_ball.direction, spore_ball.position, spore_ball.vel, spore_ball.acc))
        for i in range(10):
            spore_ball.move(duration=0.05)
            logging.debug('[{}] direction={}, position={}, vel={}, acc={}'
                .format(i, spore_ball.direction, spore_ball.position, spore_ball.vel, spore_ball.acc))
        assert True

    def test_eat(self):
        name = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        size = SporeBall.default_config().spore_radius_init ** 2
        direction = Vector2(1, 0)
        spore_ball = SporeBall(name, position, border=border, size=size, vel=None, acc=None, direction=direction)
        spore_ball.eat(ball=None)