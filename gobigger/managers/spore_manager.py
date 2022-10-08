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


class SporeManager(BaseManager):

    def __init__(self, cfg, border, random_generator=None, sequence_generator=None):
        super(SporeManager, self).__init__(cfg, border)
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
        elif isinstance(balls, SporeBall):
            self.balls[balls.ball_id] = balls
        return True

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                ball.remove()
                try:
                    del self.balls[ball.ball_id]
                except:
                    pass
        elif isinstance(balls, SporeBall):
            balls.remove()
            try:
                del self.balls[balls.ball_id]
            except:
                pass

    def spawn_ball(self, position=None):
        if position is None:
            position = self.border.sample()
        name = uuid.uuid1()
        return SporeBall(name=name, position=position, border=self.border, score=self.ball_settings.score_init,
                         direction=Vector2(1,0))
    
    def init_balls(self, custom_init=None):
        # [position.x, position.y, score, direction.x, direction.y, vel.x, vel.y, acc.x, acc.y, 
        #  move_time, moving]
        if custom_init is not None:
            for ball_cfg in custom_init:
                ball = self.spawn_ball(position=Vector2(*ball_cfg[:2]))
                if len(ball_cfg) > 2:
                    ball.direction = Vector2(*ball_cfg[2:4])
                    ball.vel = Vector2(*ball_cfg[4:6])
                    ball.move_frame = ball_cfg[6]
                    ball.moving = ball_cfg[7]
                    ball.owner = ball_cfg[8]
                self.balls[ball.name] = ball

    def step(self, duration):
        return

    def reset(self):
        self.balls = {}
        return True
