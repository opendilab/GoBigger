import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.balls import ThornsBall, SporeBall, CloneBall, FoodBall
from gobigger.utils import Border

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestCloneBall:

    def get_clone(self, size=None):
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        team_name = uuid.uuid1()
        name = uuid.uuid1()
        size = CloneBall.default_config().radius_init ** 2 if size is None else size
        owner = uuid.uuid1()
        return CloneBall(team_name, name, position, border=border, size=size, vel=None, acc=None, owner=owner, clone_num=1)

    def get_thorns(self):
        name = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        thorns_position = Vector2(100, 100)
        thorns_size = ThornsBall.default_config().radius_min ** 2
        return ThornsBall(name, thorns_position, border=border, size=thorns_size)

    def get_food(self):
        name = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(200, 200)
        return FoodBall(name, position, border=border, size=25, vel=None, acc=None)

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
        clone_ball = self.get_clone(size=256)
        direction = Vector2(1,0) * 1000
        logging.debug('===================== before move =====================')
        logging.debug('position={}, vel={}, acc={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.acc, clone_ball.vel_max))
        for i in range(10):
            clone_ball.move(given_acc=direction, given_acc_center=Vector2(0,0), duration=0.05)
            logging.debug('===================== after move =====================')
            logging.debug('position={}, vel={}, acc={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.acc, clone_ball.vel_max))
        clone_ball.stop(direction)
        for i in range(20):
            clone_ball.move(given_acc=None, given_acc_center=None, duration=0.05)
            logging.debug('===================== move after stop =====================')
            logging.debug('position={}, vel={}, acc={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.acc, clone_ball.vel_max))
        clone_ball.split(1)
        clone_ball.stop(direction)
        for i in range(20):
            clone_ball.move(given_acc=None, given_acc_center=None, duration=0.05)
            logging.debug('===================== move after stop =====================')
            logging.debug('position={}, vel={}, acc={}, vel_max={}'.format(clone_ball.position, clone_ball.vel, clone_ball.acc, clone_ball.vel_max))

    def test_eject(self):
        logging.debug('===================== test eject =====================')
        eject_radius_min = CloneBall.default_config().eject_radius_min
        clone_ball = self.get_clone(size=eject_radius_min**2)
        direction = Vector2(1,0) * 1000
        clone_ball.stop(direction)
        rets = clone_ball.eject()
        logging.debug('clone_ball: {}, eject_radius_min={}'.format(clone_ball, eject_radius_min))
        if clone_ball.size < eject_radius_min**2:
            assert rets
        else:
            logging.debug('spore_ball: {}'.format(rets))
        clone_ball = self.get_clone()
        assert not clone_ball.eject()
    
    def test_split(self):
        logging.debug('===================== test split =====================')
        split_radius_min = CloneBall.default_config().split_radius_min
        clone_ball = self.get_clone(size=split_radius_min**2)
        direction = Vector2(1,0) * 1000
        clone_ball.stop(direction)
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
        owner = uuid.uuid1()
        name1 = uuid.uuid1()
        name2 = uuid.uuid1()
        team_name = uuid.uuid1()
        clone_ball_1 = CloneBall(team_name, name1, position=Vector2(100, 100), border=border, size=25, vel=None, acc=None, owner=owner, clone_num=2)
        clone_ball_2 = CloneBall(team_name, name2, position=Vector2(100, 110), border=border, size=26, vel=None, acc=None, owner=owner, clone_num=2)
        logging.debug('===================== test rigid_collision =====================')
        logging.debug('clone_ball_1: {}'.format(clone_ball_1))
        logging.debug('clone_ball_2: {}'.format(clone_ball_2))
        clone_ball_1.rigid_collision(clone_ball_2)
        logging.debug('===================== after rigid_collision =====================')
        logging.debug('clone_ball_1: {}'.format(clone_ball_1))
        logging.debug('clone_ball_2: {}'.format(clone_ball_2))
        
