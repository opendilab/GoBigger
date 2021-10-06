import logging
import pytest
import uuid
from pygame.math import Vector2
import time
import random
import numpy as np
import cv2
import pygame

from gobigger.agents import BaseAgent
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestBaseAgent:

    def test_init(self):
        base_agent = BaseAgent()
        assert True

    def test_step(self):
        base_agent = BaseAgent()
        with pytest.raises(Exception) as e:
            base_agent.step()
            

