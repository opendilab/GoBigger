import math
import logging
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2

from gobigger.utils import format_vector, Border
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class BaseManager(ABC):
    '''
    Overview:
        Base class for all ball managers
    '''
    def __init__(self, cfg, border):
        self.cfg = cfg
        self.border = border
        self.balls = {}
        self.ball_settings = self.cfg.ball_settings

    def get_balls(self):
        '''
        Overview:
            Get all balls currently managed
        '''
        return self.balls.values()
    
    def add_balls(self, balls):
        '''
        Overview:
            Add one (or more) balls
        '''
        raise NotImplementedError

    def refresh(self):
        '''
        Overview:
            Refresh. Used to refresh the balls in management. Such as replenishing eaten food balls
        '''
        raise NotImplementedError

    def remove_balls(self, balls):
        '''
        Overview:
            Remove managed balls
        '''
        raise NotImplementedError

    def spawn_ball(self):
        raise NotImplementedError

    def init_balls(self):
        raise NotImplementedError

    def step(self, duration):
        '''
        Overview:
            Perform a status update under the control of the server
        '''
        raise NotImplementedError

    def obs(self):
        '''
        Overview:
            Return data available for observation
        '''
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
