import math
import logging
import random
import uuid
import numpy as np
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2

from .base_manager import BaseManager
from gobigger.utils import format_vector, Border
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class FoodManager(BaseManager):

    def __init__(self, cfg, border, random_generator=None):
        super(FoodManager, self).__init__(cfg, border)
        self.refresh_frame_freq = self.cfg.refresh_frame_freq
        self.refresh_frame_count = 0
        if random_generator is not None:
            self._random = random_generator
        else:
            self._random = random.Random()

    def get_balls(self):
        return list(self.balls.values())
    
    def add_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.balls[ball.ball_id] = ball
        elif isinstance(balls, FoodBall):
            self.balls[balls.ball_id] = balls
        return True

    def refresh(self):
        left_num = self.cfg.num_max - len(self.balls)
        todo_num = min(math.ceil(self.cfg.refresh_percent * left_num), left_num)
        for _ in range(todo_num):
            self.add_balls(self.spawn_ball())

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                ball.remove()
                try:
                    del self.balls[ball.ball_id]
                except:
                    pass
        elif isinstance(balls, FoodBall):
            balls.remove()
            try:
                del self.balls[balls.ball_id]
            except:
                pass

    def spawn_ball(self, position=None, score=None):
        if position is None:
            position = self.border.sample()
        if score is None:
            score = self._random.uniform(self.ball_settings.score_min, self.ball_settings.score_max)
        ball_id = uuid.uuid1()
        return FoodBall(ball_id=ball_id, position=position, border=self.border, score=score, **self.ball_settings)

    def init_balls(self, custom_init=None):
        if custom_init is None or len(custom_init) == 0:
            for _ in range(self.cfg.num_init):
                ball = self.spawn_ball()
                self.balls[ball.ball_id] = ball
        else:
            for ball_cfg in custom_init:
                ball = self.spawn_ball(position=Vector2(*ball_cfg[:2]), score=ball_cfg[2])
                self.balls[ball.ball_id] = ball

    def step(self, duration):
        self.refresh_frame_count += 1
        if self.refresh_frame_count >= self.refresh_frame_freq:
            self.refresh()
            self.refresh_frame_count = 0

    def reset(self):
        self.refresh_frame_count = 0
        self.balls = {}
        return True
