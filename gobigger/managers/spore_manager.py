import math
import logging
import random
import uuid
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2

from .base_manager import BaseManager
from gobigger.utils import format_vector, Border
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class SporeManager(BaseManager):

    def __init__(self, cfg, border):
        super(SporeManager, self).__init__(cfg, border)

    def get_balls(self):
        return list(self.balls.values())
    
    def add_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.balls[ball.name] = ball
        elif isinstance(balls, SporeBall):
            self.balls[balls.name] = balls
        return True

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                ball.remove()
                del self.balls[ball.name]
        elif isinstance(balls, SporeBall):
            balls.remove()
            del self.balls[balls.name]

    def spawn_ball(self, position=None, size=None):
        if position is None:
            position = self.border.sample()
        if size is None:
            size = random.uniform(self.ball_settings.radius_min, self.ball_settings.radius_max)**2
        name = uuid.uuid1()
        return SporeBall(name=name, position=position, border=self.border, direction=Vector2(1,0), vel_init=0)
    
    def init_balls(self, custom_init=None):
        if custom_init is not None:
            for ball_cfg in custom_init:
                ball = self.spawn_ball(position=Vector2(*ball_cfg['position']), size=ball_cfg['radius']**2)
                self.balls[ball.name] = ball

    def step(self, duration):
        return

    def reset(self):
        self.balls = {}
        return True
