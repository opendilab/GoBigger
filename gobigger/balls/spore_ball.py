import logging
from easydict import EasyDict
from pygame.math import Vector2
import math

from gobigger.utils import format_vector, add_size, Border, deep_merge_dicts
from .base_ball import BaseBall


class SporeBall(BaseBall):
    """
    Overview:
        Spores spit out by the player ball
        - characteristic:
        * Can't move actively
        * can not eat
        * Can be eaten by CloneBall and ThornsBall
        * There is an initial velocity at birth, and it decays to 0 within a period of time
    """
    @staticmethod
    def default_config():
        cfg = BaseBall.default_config()
        cfg.update(dict(
            radius_min=3, # Minimum radius(Fixed)
            radius_max=3, # Maximum radius(Fixed)
            vel_init=50, # initial value if velocity(Fixed)
            vel_zero_time=0.1, # The time it takes for the speed to decay to zero(S)
            spore_radius_init=20, # initial radius(Fixed)
        ))
        return EasyDict(cfg)

    def __init__(self, name, position, border, size=1, vel=None, acc=None, direction=Vector2(0,0), owner=-1, **kwargs):
        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = SporeBall.default_config()
        cfg = deep_merge_dicts(cfg, kwargs)
        super(SporeBall, self).__init__(name, position, border, size=size, vel=vel, acc=acc, **cfg)
        self.vel_init = cfg.vel_init
        self.vel_zero_time = cfg.vel_zero_time
        self.spore_radius_init = cfg.spore_radius_init
        # normal kwargs
        self.direction = direction.normalize()
        self.vel = self.vel_init * self.direction
        self.acc = - (self.vel_init / self.vel_zero_time) * self.direction
        self.owner = owner
        self.move_time = 0
        # reset size
        if math.sqrt(self.size) != self.spore_radius_init:
            self.set_size(self.spore_radius_init**2)
        self.moving = True
        self.check_border()

    def move(self, direction=None, duration=0.05):
        assert direction is None
        assert duration > 0
        self.position = self.position + self.vel * duration
        self.move_time += duration
        if self.move_time < self.vel_zero_time:
            self.vel += self.acc * duration
        else:
            self.vel = Vector2(0, 0)
            self.acc = Vector2(0, 0)
            self.moving = False
        self.check_border()
        return True

    def eat(self, ball):
        logging.debug('SporeBall can not eat others')
        return
