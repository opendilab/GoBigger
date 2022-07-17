import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import BaseBall, ThornsBall, SporeBall, CloneBall, FoodBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestCloneBall:

    def get_clone(self, score=None):
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        team_id = uuid.uuid1()
        ball_id = uuid.uuid1()
        score = CloneBall.default_config().score_init if score is None else score
        player_id = uuid.uuid1()
        return CloneBall(ball_id, position, border=border, score=score, team_id=team_id, player_id=player_id)

    def get_thorns(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        thorns_position = Vector2(100, 100)
        thorns_score = ThornsBall.default_config().score_min
        return ThornsBall(ball_id, thorns_position, border=border, score=thorns_score)

    def get_food(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(200, 200)
        return FoodBall(ball_id, position, border=border, score=5)

    def test_init(self):
        clone_ball = self.get_clone()
        assert True

    def test_eat_food(self):
        clone_ball = self.get_clone()
        food_ball = self.get_food()
        clone_score = clone_ball.score
        food_score = food_ball.score
        clone_ball.eat(food_ball, clone_num=1)
        logging.debug('clone_score={}, food_score={}, now_score={}, now_score={}'
            .format(clone_score, food_score, clone_ball.score, clone_ball.score))
        assert True

    def test_eat_thorns(self):
        clone_ball = self.get_clone()
        thorns_ball = self.get_thorns()
        clone_score = clone_ball.score
        thorns_score = thorns_ball.score

        logging.debug('clone_ball={}'.format(clone_ball))
        logging.debug('===================== first eat =====================')
        rets = clone_ball.eat(thorns_ball, clone_num=1)
        logging.debug('[original] {} eat thorns_score={}'.format(clone_ball, thorns_score))
        for i, ret in enumerate(rets):
            logging.debug('[{}] {}'.format(i, ret))
        clone_num =  1 + len(rets)
        logging.debug('===================== second eat =====================')
        rets = clone_ball.eat(thorns_ball, clone_num=clone_num)
        logging.debug('[original] {} eat thorns_score={}'.format(clone_ball, thorns_score))
        for i, ret in enumerate(rets):
            logging.debug('[{}] {}'.format(i, ret))

    def test_move(self):
        border = Border(0, 0, 1000, 1000)
        clone_ball = self.get_clone(score=16)
        direction = Vector2(1,0) * 1000
        logging.debug('===================== before move =====================')
        logging.debug('position={}, vel={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.vel_max))
        for i in range(10):
            clone_ball.move(given_acc=direction, given_acc_center=Vector2(0,0), duration=0.05)
            logging.debug('===================== after move =====================')
            logging.debug('position={}, vel={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.vel_max))
        for i in range(20):
            clone_ball.move(given_acc=None, given_acc_center=None, duration=0.05)
            logging.debug('===================== move after stop =====================')
            logging.debug('position={}, vel={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.vel_max))
        clone_ball.split(1)
        for i in range(20):
            clone_ball.move(given_acc=None, given_acc_center=None, duration=0.05)
            logging.debug('===================== move after stop =====================')
            logging.debug('position={}, vel={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.vel_max))

    def test_eject(self):
        logging.debug('===================== test eject =====================')
        eject_score_min = CloneBall.default_config().eject_score_min
        clone_ball = self.get_clone(score=eject_score_min)
        rets = clone_ball.eject()
        logging.debug('clone_ball: {}, eject_score_min={}'.format(clone_ball, eject_score_min))
        if clone_ball.score < eject_score_min:
            assert rets
        else:
            logging.debug('spore_ball: {}'.format(rets))
        assert not clone_ball.eject()
    
    def test_split(self):
        logging.debug('===================== test split =====================')
        split_score_min = CloneBall.default_config().split_score_min
        clone_ball = self.get_clone(score=split_score_min)
        logging.debug('clone_ball: {}, split_score_min={}'.format(clone_ball, split_score_min))
        rets = clone_ball.split(1)
        logging.debug('===================== after split =====================')
        logging.debug('[original] {}'.format(clone_ball))
        logging.debug('[new     ] {}'.format(rets))
        clone_ball = self.get_clone()
        assert not clone_ball.split(1)

    def test_rigid_collision(self):
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        player_id = uuid.uuid1()
        ball_id1 = uuid.uuid1()
        ball_id2 = uuid.uuid1()
        team_id = uuid.uuid1()
        clone_ball_1 = CloneBall(ball_id1, position=Vector2(100, 100), border=border, score=5, team_id=team_id, player_id=player_id)
        clone_ball_2 = CloneBall(ball_id2, position=Vector2(100, 110), border=border, score=6, team_id=team_id, player_id=player_id)
        logging.debug('===================== test rigid_collision =====================')
        logging.debug('clone_ball_1: {}'.format(clone_ball_1))
        logging.debug('clone_ball_2: {}'.format(clone_ball_2))
        clone_ball_1.rigid_collision(clone_ball_2)
        logging.debug('===================== after rigid_collision =====================')
        logging.debug('clone_ball_1: {}'.format(clone_ball_1))
        logging.debug('clone_ball_2: {}'.format(clone_ball_2))

    def test_move_wo_stop_flag(self):
        clone_ball = self.get_clone()
        clone_ball.move(given_acc=None, given_acc_center=None, duration=0.05)
        clone_ball.move(given_acc=None, given_acc_center=Vector2(1,0), duration=0.05)
        clone_ball.move(given_acc=None, given_acc_center=None, duration=0.05)

    def test_eat_baseball(self):
        border = Border(0, 0, 100, 100)
        position = Vector2(10, 10)
        ball_id = uuid.uuid1()
        base_ball = BaseBall(ball_id, position, border=border, score=1)
        clone_ball = self.get_clone()
        clone_ball.eat(base_ball)

    def test_rigid_collision_self(self):
        clone_ball = self.get_clone()
        assert clone_ball.rigid_collision(clone_ball)

