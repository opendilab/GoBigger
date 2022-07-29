import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.managers import FoodManager
from gobigger.utils import Border
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestFoodManager:

    def get_manager(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        food_manager = FoodManager(cfg=cfg.manager_settings.food_manager, border=border)
        return food_manager

    def test_init(self):
        food_manager = self.get_manager()
        assert True

    def test_get_balls(self):
        food_manager = self.get_manager()
        food_manager.init_balls()
        balls = food_manager.get_balls()
        assert len(balls) == food_manager.cfg.num_init
        for i in range(10):
            logging.debug(balls[i])
        assert True

    def test_remove_balls(self):
        food_manager = self.get_manager()
        food_manager.init_balls()
        balls = food_manager.get_balls()
        assert len(balls) == food_manager.cfg.num_init
        food_manager.remove_balls(balls[:100])
        logging.debug('[FoodManager.remove_balls] init num: {}, now num {}'
            .format(food_manager.cfg.num_init, len(food_manager.get_balls())))
        assert True

    def test_step(self):
        food_manager = self.get_manager()
        food_manager.init_balls()
        balls = food_manager.get_balls()
        assert len(balls) == food_manager.cfg.num_init
        food_manager.remove_balls(balls[:100])
        logging.debug('[FoodManager.remove_balls] init num: {}, now num {}'
            .format(food_manager.cfg.num_init, len(food_manager.get_balls())))
        refresh_frame_freq = food_manager.cfg.refresh_frame_freq
        logging.debug('=================== test step ===================')
        for i in range(10):
            food_manager.step(duration=None)
            logging.debug('[FoodManager.step] {} food num = {}'.format(i, len(food_manager.get_balls())))

    def test_reset(self):
        food_manager = self.get_manager()
        food_manager.init_balls()
        balls = food_manager.get_balls()
        assert len(balls) == food_manager.cfg.num_init
        food_manager.reset()
        balls = food_manager.get_balls()
        assert len(balls) == 0

    def test_add_balls(self):
        to_add_list = []
        food_manager = self.get_manager()
        for _ in range(2):
            to_add_list.append(food_manager.spawn_ball())
        assert food_manager.add_balls(to_add_list)

    def test_init_balls_custom(self):
        custom_init = [[100, 100, 2]]
        food_manager = self.get_manager()
        food_manager.init_balls(custom_init)
    