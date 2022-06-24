import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.managers import SporeManager
from gobigger.balls import SporeBall
from gobigger.utils import Border
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestSporeManager:

    def get_manager(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        spore_manager = SporeManager(cfg=cfg.manager_settings.spore_manager, border=border)
        return spore_manager

    def get_spore_ball(self):
        ball_id = uuid.uuid1()
        border = Border(0, 0, 1000, 1000)
        position = Vector2(100, 100)
        radius = SporeBall.default_config().radius_init
        direction = Vector2(1, 0)
        return SporeBall(ball_id, position, border=border, radius=radius, direction=direction)

    def test_init(self):
        spore_manager = self.get_manager()
        assert True

    def test_get_balls(self):
        spore_manager = self.get_manager()
        for i in range(10):
            spore_manager.add_balls(self.get_spore_ball())
        spore_manager.add_balls([self.get_spore_ball(), self.get_spore_ball()])
        balls = spore_manager.get_balls()
        for i in range(10):
            logging.debug(balls[i])
        assert True

    def test_remove_balls(self):
        spore_manager = self.get_manager()
        for i in range(10):
            spore_manager.add_balls(self.get_spore_ball())
        balls = spore_manager.get_balls()
        original_len = len(balls)
        spore_manager.remove_balls(balls[:5])
        logging.debug('[SporeManager.remove_balls] init num: {}, now num {}'
            .format(original_len, len(spore_manager.get_balls())))
        assert True

    def test_reset(self):
        spore_manager = self.get_manager()
        for i in range(10):
            spore_manager.add_balls(self.get_spore_ball())
        balls = spore_manager.get_balls()
        spore_manager.reset()
        assert len(spore_manager.balls) == 0
