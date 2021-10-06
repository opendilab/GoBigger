import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random

from gobigger.balls import BaseBall
from gobigger.players import HumanPlayer
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimePartialRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestRealtimePartialRender:

    def test_init(self):
        render = RealtimePartialRender(width=1000, height=1000)
        assert render.scale_up_ratio == 1.5

    def test_fill(self):
        render = RealtimePartialRender(width=1000, height=1000)
        server = Server()
        server.start()
        render.fill(server)
        render.close()