import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
from easydict import EasyDict

from gobigger.balls import BaseBall, SporeBall
from gobigger.players import HumanPlayer
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestEnvRender:

    def test_init(self):
        render = EnvRender()
        assert True

    def test_fill_all(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender()
        food_balls = [BaseBall('0', border.sample(), border=border, radius=1)]
        thorns_balls = [BaseBall('0', border.sample(), border=border, radius=1)]
        spore_balls = [BaseBall('0', border.sample(), border=border, radius=1)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                               team_id=0, player_id=0, border=border, 
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        screen_data_all = render.get_screen(food_balls, thorns_balls, spore_balls, players, 1)
        assert len(screen_data_all.shape) == 3
