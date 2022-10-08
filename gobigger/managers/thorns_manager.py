import math
import logging
import random
import uuid
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2

from .base_manager import BaseManager
from gobigger.utils import format_vector, Border, SequenceGenerator
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class ThornsManager(BaseManager):

    def __init__(self, cfg, border, random_generator=None, sequence_generator=None):
        super(ThornsManager, self).__init__(cfg, border)
        self.refresh_frame_freq = self.cfg.refresh_frame_freq
        self.refresh_frame_count = 0
        if random_generator is not None:
            self._random = random_generator
        else:
            self._random = random.Random()
        if sequence_generator is not None:
            self.sequence_generator = sequence_generator
        else:
            self.sequence_generator = SequenceGenerator()

    def get_balls(self):
        return list(self.balls.values())
    
    def add_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.balls[ball.ball_id] = ball
        elif isinstance(balls, ThornsBall):
            self.balls[balls.ball_id] = balls
        return True

    def refresh(self):
        left_num = self.cfg.num_max - len(self.balls)
        todo_num = min(math.ceil(self.cfg.refresh_percent * left_num), left_num)
        new_balls = {}
        for _ in range(todo_num):
            ball = self.spawn_ball()
            self.add_balls(ball)
            new_balls[ball.ball_id] = ball.save()
        return new_balls

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                ball.remove()
                try:
                    del self.balls[ball.ball_id]
                except:
                    pass
        elif isinstance(balls, ThornsBall):
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
        ball_id = self.sequence_generator.get()
        return ThornsBall(ball_id=ball_id, position=position, border=self.border, score=score, **self.ball_settings)

    def init_balls(self, custom_init=None):
        # [position.x, position.y, score, vel.x, vel.y, acc.x, acc.y, 
        #  move_time, moving]
        if custom_init is None or len(custom_init) == 0:
            for _ in range(self.cfg.num_init):
                ball = self.spawn_ball()
                self.balls[ball.ball_id] = ball
        else:
            for ball_cfg in custom_init:
                ball = self.spawn_ball(position=Vector2(*ball_cfg[:2]), score=ball_cfg[2])
                if len(ball_cfg) > 3:
                    ball.vel = Vector2(*ball_cfg[3:5])
                    ball.move_frame = Vector2(*ball_cfg[5])
                    ball.moving = ball_cfg[6]
                self.balls[ball.ball_id] = ball

    def step(self, duration):
        self.refresh_frame_count += 1
        new_balls = {}
        if self.refresh_frame_count > self.refresh_frame_freq:
            new_balls = self.refresh()
            self.refresh_frame_count = 0
        return new_balls

    def reset(self):
        self.refresh_frame_count = 0
        self.balls = {}
        return True
