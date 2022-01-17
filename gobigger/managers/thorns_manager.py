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


class ThornsManager(BaseManager):

    def __init__(self, cfg, border, random_generator=None):
        super(ThornsManager, self).__init__(cfg, border)
        self.thorns_refresh_time = self.cfg.refresh_time
        self.refresh_time_count = 0
        if random_generator is not None:
            self._random = random_generator
        else:
            self._random = random.Random()

    def get_balls(self):
        return list(self.balls.values())
    
    def add_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.balls[ball.name] = ball
        elif isinstance(balls, ThornsBall):
            self.balls[balls.name] = balls
        return True

    def refresh(self):
        todo_num = min(self.cfg.refresh_num, self.cfg.num_max - len(self.balls))
        for _ in range(todo_num):
            self.add_balls(self.spawn_ball())

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                ball.remove()
                del self.balls[ball.name]
        elif isinstance(balls, ThornsBall):
            balls.remove()
            del self.balls[balls.name]

    def spawn_ball(self, position=None, size=None):
        if position is None:
            position = self.border.sample()
        if size is None:
            size = self._random.uniform(self.ball_settings.radius_min, self.ball_settings.radius_max)**2
        name = uuid.uuid1()
        return ThornsBall(name=name, position=position, border=self.border, size=size, **self.ball_settings)

    def init_balls(self, custom_init=None):
        # [position.x, position.y, radius, vel.x, vel.y, acc.x, acc.y, 
        #  move_time, moving]
        if custom_init is None:
            for _ in range(self.cfg.num_init):
                ball = self.spawn_ball()
                self.balls[ball.name] = ball
        else:
            for ball_cfg in custom_init:
                ball = self.spawn_ball(position=Vector2(*ball_cfg[:2]), size=ball_cfg[2]**2)
                if len(ball_cfg) > 3:
                    ball.vel = Vector2(*ball_cfg[3:5])
                    ball.acc = Vector2(*ball_cfg[5:7])
                    ball.move_time = ball_cfg[7]
                    ball.moving = ball_cfg[8]
                self.balls[ball.name] = ball

    def step(self, duration):
        self.refresh_time_count += duration
        if self.refresh_time_count > self.thorns_refresh_time:
            self.refresh()
            self.refresh_time_count = 0

    def reset(self):
        self.refresh_time_count = 0
        self.balls = {}
        return True
