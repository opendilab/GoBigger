import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import BaseBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestBaseBall:

    def test_init(self):
        border = Border(0, 0, 100, 100)
        position = Vector2(10, 10)
        owner = None
        name = uuid.uuid1()
        base_ball = BaseBall(name, position, border=border, owner=owner, size=1, 
                 acc_max=5, vel_max=10, radius_min=5, radius_max=10)
        assert True

    def test_judge_in_rectangle(self):
        border = Border(0, 0, 800, 800)
        position = Vector2(400, 400)
        owner = None
        name = uuid.uuid1()
        base_ball = BaseBall(name, position, border, size=36)
        rectangle = [300, 300, 500, 500]
        logging.debug(base_ball.judge_in_rectangle(rectangle))
        assert True

    def test_move(self):
        border = Border(0, 0, 800, 800)
        position = Vector2(400, 400)
        name = uuid.uuid1()
        base_ball = BaseBall(name, position, border, size=36)
        with pytest.raises(Exception) as e:
            base_ball.move(direction=None, duration=None)

    def test_eat(self):
        border = Border(0, 0, 800, 800)
        position = Vector2(400, 400)
        name = uuid.uuid1()
        base_ball = BaseBall(name, position, border, size=36)
        with pytest.raises(Exception) as e:
            base_ball.eat(ball=None)

    def test_op_override(self):
        border = Border(0, 0, 800, 800)
        base_ball_1 = BaseBall(uuid.uuid1(), border.sample(), border, size=36)
        base_ball_2 = BaseBall(uuid.uuid1(), border.sample(), border, size=50)
        assert not base_ball_1 == base_ball_2
        assert base_ball_1 < base_ball_2
        assert not base_ball_1 > base_ball_2
