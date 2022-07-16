import math
import logging
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2
from functools import total_ordering

from gobigger.utils import format_vector, Border, deep_merge_dicts


@total_ordering
class BaseBall(ABC):
    '''
    Overview:
        Base class of all balls
    '''
    @staticmethod
    def default_config():
        '''
        Overview:
            Default config
        '''
        cfg = dict()
        return EasyDict(cfg)

    def __init__(self, ball_id, position, radius, border, **kwargs):
        '''
        Parameters:
             vel <Vector2> : the direction of the ball's speed 
             acc <Vector2> : the direction of the ball's acceleration
        '''
        self.ball_id = ball_id
        self.position = position

        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = BaseBall.default_config()
        cfg = deep_merge_dicts(cfg, kwargs)
        self.radius = radius
        self.border = border
        self.size = self.radius_to_size(self.radius)
        self.is_remove = False
        self.quad_node = None

    def set_size(self, size: float) -> None:
        self.size = size
        self.radius = self.size_to_radius(self.size)
    
    def radius_to_size(self, radius):
        return (math.pow(radius,2) - 0.15) / 0.042 * 100
    
    def size_to_radius(self, score):
        return math.sqrt(score / 100 * 0.042 + 0.15)

    def move(self, direction, duration):
        """
        Overview:
            Realize the movement of the ball, pass in the direction and time parameters, and return the new position
        Parameters:
            direction <Vector2>: A point in the unit circle
            duration <float>: time
        Returns:
            position <Vector2>: position after moving 
        """
        raise NotImplementedError

    def eat(self, ball):
        """
        Overview:
            Describe the rules of eating and being eaten
        Parameters:
            ball <BaseBall>: Eaten ball
        """
        raise NotImplementedError

    def remove(self):
        """
        Overview:
            Things to do when being removed from the map
        """
        self.is_remove = True

    def check_border(self):
        """
        Overview:
            Check to see if the position of the ball exceeds the bounds of the map. 
            If it exceeds, the speed and acceleration in the corresponding direction will be zeroed, and the position will be edged
        """
        if self.position.x < self.border.minx or self.position.x > self.border.maxx:
            self.position.x = max(self.position.x, self.border.minx)
            self.position.x = min(self.position.x, self.border.maxx)
        if self.position.y < self.border.miny or self.position.y > self.border.maxy:
            self.position.y = max(self.position.y, self.border.miny)
            self.position.y = min(self.position.y, self.border.maxy)

    def get_dis(self, ball):
        '''
        Overview:
            Get the distance between the centers of the two balls
        Parameters:
            ball <BaseBall>: another ball
        '''
        return (self.position - ball.position).length()

    def judge_cover(self, ball):
        '''
        Overview:
            Determine whether the center of the two balls is covered
        Parameters:
            ball <BaseBall>: another ball
        Returns:
            is_covered <bool>: covered or not
        '''
        if ball.ball_id == self.ball_id:
            return False
        dis = self.get_dis(ball)
        if self.radius > dis or ball.radius > dis:
            return True
        else:
            return False

    def judge_in_rectangle(self, rectangle):
        '''
        Overview:
            Determine if the ball and rectangle intersect
        Parameters:
            rectangle <List>: left_top_x, left_top_y, right_bottom_x, right_bottom_y
        Returns:
            <bool> : intersect or not
        '''
        dx = rectangle[0] - self.position.x if rectangle[0] > self.position.x \
                else self.position.x - rectangle[2] if self.position.x > rectangle[2] else 0
        dy = rectangle[1] - self.position.y if rectangle[1] > self.position.y \
                else self.position.y - rectangle[3] if self.position.y > rectangle[3] else 0
        return dx**2 + dy**2 <= self.radius**2

    def __repr__(self) -> str:
        return 'position={}, size={:.3f}, radius={:.3f}'.format(self.position, self.size, self.radius)

    def __eq__(self, other):
        return self.size == other.size

    def __le__(self, other):
        return self.size < other.size

    def __gt__(self, other):
        return self.size > other.size
