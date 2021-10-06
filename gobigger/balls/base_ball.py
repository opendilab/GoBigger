import math
import logging
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2
from functools import total_ordering

from gobigger.utils import format_vector, Border


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
        cfg = dict(
            radius_min = 5, # Minimum radius
            radius_max = 10, # Maximum radius
        )
        return EasyDict(cfg)

    def __init__(self, name, position, border, size=None, vel=None, acc=None, color : int = 1, **kwargs):
        '''
        Parameters:
             border <border>: Circumscribed rectangle of the ball
             vel <Vector2> : the direction of the ball's speed 
             acc <Vector2> : the direction of the ball's acceleration
        '''
        self.name = name
        self.position = position
        self.border = border
        self.vel = Vector2(0, 0) if vel is None else vel 
        self.acc = Vector2(0, 0) if acc is None else acc 

        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = BaseBall.default_config()
        cfg.update(kwargs)
        self.color=color
        self.radius_min = cfg.radius_min
        self.radius_max = cfg.radius_max
        if size is None:
            size = self.radius_min ** 2
        self.set_size(size)
        self.is_remove = False
        self.quad_node = None

    def set_size(self, size: float) -> None:
        """
        Overview:
            Set radius according to weight
        Parameters:
            size <float>: weight
        """
        self.size = size
        self.radius = math.sqrt(self.size)
        if self.radius > self.radius_max:
            self.radius = self.radius_max
        elif self.radius < self.radius_min:
            self.radius = self.radius_min
        self.size = self.radius * self.radius

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
        if self.position.x < self.border.minx + self.radius or self.position.x > self.border.maxx - self.radius:
            self.position.x = max(self.position.x, self.border.minx + self.radius)
            self.position.x = min(self.position.x, self.border.maxx - self.radius)
            self.vel.x = 0
            self.acc.x = 0
        if self.position.y < self.border.miny + self.radius or self.position.y > self.border.maxy - self.radius:
            self.position.y = max(self.position.y, self.border.miny + self.radius)
            self.position.y = min(self.position.y, self.border.maxy - self.radius)
            self.vel.y = 0
            self.acc.y = 0

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
        if ball.name == self.name:
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
        return 'position={}, size={:.3f}, radius={:.3f}, vel={}, acc={}'.format(self.position, self.size, self.radius, self.vel, self.acc)

    def __eq__(self, other):
        return self.size == other.size

    def __le__(self, other):
        return self.size < other.size

    def __gt__(self, other):
        return self.size > other.size
