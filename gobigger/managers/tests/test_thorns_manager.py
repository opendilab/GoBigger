import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.managers import ThornsManager
from gobigger.utils import Border
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestThornsManager:

    def get_manager(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        thorns_manager = ThornsManager(cfg=cfg.manager_settings.thorns_manager, border=border)
        return thorns_manager

    def test_init(self):
        thorns_manager = self.get_manager()
        assert True

    def test_get_balls(self):
        thorns_manager = self.get_manager()
        thorns_manager.init_balls()
        balls = thorns_manager.get_balls()
        assert len(balls) == thorns_manager.cfg.num_init
        for i in range(10):
            logging.debug(balls[i])
        assert True

    def test_remove_balls(self):
        thorns_manager = self.get_manager()
        thorns_manager.init_balls()
        balls = thorns_manager.get_balls()
        assert len(balls) == thorns_manager.cfg.num_init
        thorns_manager.remove_balls(balls[:20])
        logging.debug('[ThornsManager.remove_balls] init num: {}, now num {}'
            .format(thorns_manager.cfg.num_init, len(thorns_manager.get_balls())))
        assert True

    def test_step(self):
        thorns_manager = self.get_manager()
        thorns_manager.init_balls()
        balls = thorns_manager.get_balls()
        assert len(balls) == thorns_manager.cfg.num_init
        thorns_manager.remove_balls(balls[:20])
        logging.debug('[ThornsManager.remove_balls] init num: {}, now num {}'
            .format(thorns_manager.cfg.num_init, len(thorns_manager.get_balls())))
        thorns_refresh_time = thorns_manager.cfg.refresh_time
        logging.debug('=================== test step ===================')
        for i in range(20):
            thorns_manager.step(duration=thorns_refresh_time/2)
            logging.debug('[FoodManager.step] {} food num = {}'.format(i, len(thorns_manager.get_balls())))

    def test_reset(self):
        thorns_manager = self.get_manager()
        thorns_manager.init_balls()
        balls = thorns_manager.get_balls()
        assert len(balls) == thorns_manager.cfg.num_init
        thorns_manager.reset()
        assert len(thorns_manager.balls) == 0

    def test_add_remove_list(self):
        thorns_manager = self.get_manager()
        thorns_manager.init_balls()
        balls = thorns_manager.get_balls()
        thorns_manager.add_balls(balls)
        thorns_manager.remove_balls(balls)
