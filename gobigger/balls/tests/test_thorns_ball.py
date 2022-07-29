import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import BaseBall, ThornsBall, SporeBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestThornsBall:

    def test_init(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 100, 100)
        position = Vector2(10, 10)
        thorns_ball = ThornsBall(ball_id, position, border=border, score=4)
        assert True

    def test_eat_move(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        thorns_position = Vector2(100, 100)
        thorns_score = ThornsBall.default_config().score_min
        thorns_ball = ThornsBall(ball_id, thorns_position, border=border, score=thorns_score)

        ball_id = uuid.uuid1()
        spore_position = Vector2(100, 100)
        spore_score = SporeBall.default_config().score_init
        direction = Vector2(1, 0)
        spore_ball = SporeBall(ball_id, spore_position, border=border, score=spore_score, direction=direction)

        logging.debug('=========================== before eat =============================')
        logging.debug('[thorns] position={}, score={}, vel={}, move_frame={}'
            .format(thorns_ball.position, thorns_ball.score, thorns_ball.vel, thorns_ball.move_frame))
        logging.debug('[spore]  position={}, score={}, vel={}'
            .format(spore_ball.position, spore_ball.score, spore_ball.vel))
        thorns_ball.eat(spore_ball)
        logging.debug('=========================== after eat  =============================')
        logging.debug('[thorns] position={}, score={}, vel={}, move_frame={}'
            .format(thorns_ball.position, thorns_ball.score, thorns_ball.vel, thorns_ball.move_frame))
        logging.debug('[spore]  position={}, score={}, vel={}'
            .format(spore_ball.position, spore_ball.score, spore_ball.vel))

        for i in range(10):
            thorns_ball.move(duration=0.05)
            logging.debug('=========================== after move {} ============================='.format(i))
            logging.debug('[thorns] position={}, score={}, vel={}, move_frame={}'
                .format(thorns_ball.position, thorns_ball.score, thorns_ball.vel, thorns_ball.move_frame))

        assert True

    def test_judge_in_rectangle(self):
        border = Border(0, 0, 800, 800)
        position = Vector2(400, 400)
        ball_id = uuid.uuid1()
        thorns_ball = ThornsBall(ball_id, position, border=border, score=10)
        rectangle = [300, 300, 500, 500]
        assert thorns_ball.judge_in_rectangle(rectangle)

    def test_eat_others(self):
        border = Border(0, 0, 800, 800)
        position = Vector2(400, 400)
        ball_id = uuid.uuid1()
        thorns_ball = ThornsBall(ball_id, position, border=border, score=10)
        position = Vector2(10, 10)
        ball_id = uuid.uuid1()
        base_ball = BaseBall(ball_id, position, border=border, score=1)
        thorns_ball.eat(base_ball)

        ball_id = uuid.uuid1()
        spore_position = Vector2(100, 100)
        spore_score = SporeBall.default_config().score_init
        direction = Vector2(1, 0)
        spore_ball = SporeBall(ball_id, spore_position, border=border, score=spore_score, direction=direction)
        thorns_ball.set_score(thorns_ball.score_max)
        thorns_ball.eat(spore_ball)
