import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.managers import BaseManager
from gobigger.utils import Border
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestBaseManager:

    def test_init(self):
        cfg = Server.default_config()
        border = Border(0, 0, 100, 100)
        base_manager = BaseManager(cfg=cfg.manager_settings.food_manager, border=border)
        assert True

    def test_others(self):
        cfg = Server.default_config()
        border = Border(0, 0, 100, 100)
        base_manager = BaseManager(cfg=cfg.manager_settings.food_manager, border=border)
        base_manager.get_balls()
        with pytest.raises(Exception) as e:
            base_manager.add_balls([])
        with pytest.raises(Exception) as e:
            base_manager.refresh()
        with pytest.raises(Exception) as e:
            base_manager.remove_balls()
        with pytest.raises(Exception) as e:
            base_manager.spawn_ball()
        with pytest.raises(Exception) as e:
            base_manager.init_balls()
        with pytest.raises(Exception) as e:
            base_manager.step()
        with pytest.raises(Exception) as e:
            base_manager.obs()
        with pytest.raises(Exception) as e:
            base_manager.reset()
            

