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
from gobigger.render import RealtimeRender, RealtimePartialRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestRealtimePartialRender:

    def test_init(self):
        render = RealtimeRender()
        render = RealtimePartialRender()
        assert True
