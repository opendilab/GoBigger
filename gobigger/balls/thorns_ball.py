import logging
from easydict import EasyDict
import math
from pygame.math import Vector2

from gobigger.utils import format_vector, add_size, Border, deep_merge_dicts
from .base_ball import BaseBall
from .spore_ball import SporeBall


class ThornsBall(BaseBall):
    """
    Overview:
        - characteristic:
        * Can't move actively
        * Can eat spores. When eating spores, it will inherit the momentum of the spores and move a certain distance.
        * Can only be eaten by balls heavier than him. After eating, it will split the host into multiple smaller units.
        * Nothing happens when a ball lighter than him passes by
    """
    @staticmethod
    def default_config():
        cfg = BaseBall.default_config()
        cfg.update(dict(
            radius_min=3, # Minimum radius, greater than the player's maximum number of clones multiplied by the player's minimum weight
            radius_max=5, # Maximum radius
            eat_spore_vel_init=4, # Initialization speed after eating spores
            eat_spore_vel_zero_frame=10, # Time to zero speed after eating spores(s)
        ))
        return EasyDict(cfg)

    def __init__(self, ball_id, position, radius, border, **kwargs):
        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = ThornsBall.default_config()
        cfg = deep_merge_dicts(cfg, kwargs)
        super(ThornsBall, self).__init__(ball_id, position, radius=radius, border=border, **cfg)
        self.radius_min = cfg.radius_min
        self.radius_max = cfg.radius_max
        self.eat_spore_vel_init = cfg.eat_spore_vel_init
        self.eat_spore_vel_zero_frame = cfg.eat_spore_vel_zero_frame
        self.move_frame = 0
        self.vel = Vector2(0, 0)
        self.vel_piece = Vector2(0, 0)
        self.moving = False
        self.check_border()

    def move(self, direction=None, duration=0.05, **kwargs):
        assert duration > 0
        if self.moving:
            self.position = self.position + self.vel * duration
            self.move_frame += 1
            if self.move_frame < self.eat_spore_vel_zero_frame:
                self.vel = self.vel - self.vel_piece
            else:
                self.vel = Vector2(0, 0)
                self.vel_piece = Vector2(0, 0)
                self.moving = False
        self.check_border()
        return True

    def eat(self, ball):
        if isinstance(ball, SporeBall):
            self.set_size(add_size(self.size, ball.size))
            if self.radius > self.radius_max:
                self.radius = self.radius_max
            if ball.vel.length() > 0:
                self.vel = self.eat_spore_vel_init * ball.vel.normalize()
                self.vel_piece = self.vel / self.eat_spore_vel_zero_frame
                self.move_time = 0
                self.moving = True
        else:
            logging.debug('ThornsBall can not eat {}'.format(type(ball)))
        return True

    def set_size(self, size: float) -> None:
        self.size = size
        self.radius = self.size_to_radius(self.size)
        if self.radius > self.radius_max:
            self.radius = self.radius_max
        elif self.radius < self.radius_min:
            self.radius = self.radius_min
        self.size = self.radius_to_size(self.radius)
