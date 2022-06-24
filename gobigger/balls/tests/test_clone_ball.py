import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import BaseBall, ThornsBall, SporeBall, CloneBall, FoodBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestCloneBall:

    def get_clone(self, radius=None):
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        team_id = uuid.uuid1()
        ball_id = uuid.uuid1()
        radius = CloneBall.default_config().radius_init if radius is None else radius
        player_id = uuid.uuid1()
        return CloneBall(ball_id, position, border=border, radius=radius, team_id=team_id, player_id=player_id)

    def get_thorns(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        thorns_position = Vector2(100, 100)
        thorns_radius = ThornsBall.default_config().radius_min
        return ThornsBall(ball_id, thorns_position, border=border, radius=thorns_radius)

    def get_food(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(200, 200)
        return FoodBall(ball_id, position, border=border, radius=5)

    def test_init(self):
        clone_ball = self.get_clone()
        assert True

    def test_eat_food(self):
        clone_ball = self.get_clone()
        food_ball = self.get_food()
        clone_size = clone_ball.size
        food_size = food_ball.size
        clone_ball.eat(food_ball, clone_num=1)
        logging.debug('clone_size={}, food_size={}, now_size={}, now_radius={}'
            .format(clone_size, food_size, clone_ball.size, clone_ball.radius))
        assert True

    def test_eat_thorns(self):
        clone_ball = self.get_clone()
        thorns_ball = self.get_thorns()
        clone_size = clone_ball.size
        thorns_size = thorns_ball.size

        logging.debug('clone_ball={}'.format(clone_ball))
        logging.debug('===================== first eat =====================')
        rets = clone_ball.eat(thorns_ball, clone_num=1)
        logging.debug('[original] {} eat thorns_size={}'.format(clone_ball, thorns_size))
        for i, ret in enumerate(rets):
            logging.debug('[{}] {}'.format(i, ret))
        clone_num =  1 + len(rets)
        logging.debug('===================== second eat =====================')
        rets = clone_ball.eat(thorns_ball, clone_num=clone_num)
        logging.debug('[original] {} eat thorns_size={}'.format(clone_ball, thorns_size))
        for i, ret in enumerate(rets):
            logging.debug('[{}] {}'.format(i, ret))

    def test_move(self):
        border = Border(0, 0, 1000, 1000)
        clone_ball = self.get_clone(radius=16)
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
        eject_radius_min = CloneBall.default_config().eject_radius_min
        clone_ball = self.get_clone(radius=eject_radius_min)
        rets = clone_ball.eject()
        logging.debug('clone_ball: {}, eject_radius_min={}'.format(clone_ball, eject_radius_min))
        if clone_ball.radius < eject_radius_min:
            assert rets
        else:
            logging.debug('spore_ball: {}'.format(rets))
        assert not clone_ball.eject()
    
    def test_split(self):
        logging.debug('===================== test split =====================')
        split_radius_min = CloneBall.default_config().split_radius_min
        clone_ball = self.get_clone(radius=split_radius_min)
        logging.debug('clone_ball: {}, split_radius_min={}'.format(clone_ball, split_radius_min))
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
        clone_ball_1 = CloneBall(ball_id1, position=Vector2(100, 100), border=border, radius=5, team_id=team_id, player_id=player_id)
        clone_ball_2 = CloneBall(ball_id2, position=Vector2(100, 110), border=border, radius=6, team_id=team_id, player_id=player_id)
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
        base_ball = BaseBall(ball_id, position, border=border, radius=1)
        clone_ball = self.get_clone()
        clone_ball.eat(base_ball)

    def test_rigid_collision_self(self):
        clone_ball = self.get_clone()
        assert clone_ball.rigid_collision(clone_ball)

