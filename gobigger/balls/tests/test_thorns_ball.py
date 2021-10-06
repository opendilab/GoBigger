import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import ThornsBall, SporeBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestThornsBall:

    def test_init(self):
        name = uuid.uuid1()
        border = Border(0, 0, 100, 100)
        position = Vector2(10, 10)
        size = 1600
        thorns_ball = ThornsBall(name, position, border = border, size=size)
        assert True

    def test_eat_move(self):
        name = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        thorns_position = Vector2(100, 100)
        thorns_size = ThornsBall.default_config().radius_min ** 2
        thorns_ball = ThornsBall(name, thorns_position, border=border, size=thorns_size)

        name = uuid.uuid1()
        spore_position = Vector2(100, 100)
        spore_size = SporeBall.default_config().spore_radius_init ** 2
        direction = Vector2(1, 0)
        spore_ball = SporeBall(name, spore_position, border=border, size=spore_size, direction=direction)

        logging.debug('=========================== before eat =============================')
        logging.debug('[thorns] position={}, size={}, vel={}, move_time={}'
            .format(thorns_ball.position, thorns_ball.size, thorns_ball.vel, thorns_ball.move_time))
        logging.debug('[spore]  position={}, size={}, vel={}'
            .format(spore_ball.position, spore_ball.size, spore_ball.vel))
        thorns_ball.eat(spore_ball)
        logging.debug('=========================== after eat  =============================')
        logging.debug('[thorns] position={}, size={}, vel={}, move_time={}'
            .format(thorns_ball.position, thorns_ball.size, thorns_ball.vel, thorns_ball.move_time))
        logging.debug('[spore]  position={}, size={}, vel={}'
            .format(spore_ball.position, spore_ball.size, spore_ball.vel))

        for i in range(10):
            thorns_ball.move(duration=0.05)
            logging.debug('=========================== after move {} ============================='.format(i))
            logging.debug('[thorns] position={}, size={}, vel={}, move_time={}'
                .format(thorns_ball.position, thorns_ball.size, thorns_ball.vel, thorns_ball.move_time))

        assert True

    def test_judge_in_rectangle(self):
        border = Border(0, 0, 800, 800)
        position = Vector2(400, 400)
        owner = None
        name = uuid.uuid1()
        base_ball = ThornsBall(name, position, border, size=100)
        rectangle = [300, 300, 500, 500]
        logging.debug(base_ball.judge_in_rectangle(rectangle))
        assert True

