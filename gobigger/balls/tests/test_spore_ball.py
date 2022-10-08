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
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        direction = Vector2(1, 0)
        spore_ball = SporeBall(ball_id, position, border=border, score=2, direction=direction)
        logging.debug('direction={}, position={}, vel={}, move_frame={}'
            .format(spore_ball.direction, spore_ball.position, spore_ball.vel, spore_ball.move_frame))
        for i in range(10):
            spore_ball.move(duration=0.05)
            logging.debug('[{}] direction={}, position={}, vel={}, move_frame={}'
                .format(i, spore_ball.direction, spore_ball.position, spore_ball.vel, spore_ball.move_frame))
        assert True

    def test_eat(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        direction = Vector2(1, 0)
        spore_ball = SporeBall(ball_id, position, border=border, score=2, direction=direction)
        spore_ball.eat(ball=None)