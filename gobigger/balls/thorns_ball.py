import logging
from easydict import EasyDict
from pygame.math import Vector2

from gobigger.utils import format_vector, add_size, Border
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
            radius_min=5, # Minimum radius, greater than the player's maximum number of clones multiplied by the player's minimum weight
            radius_max=10, # Maximum radius
            vel_max=100, # Maximum velocity
            eat_spore_vel_init=100, # Initialization speed after eating spores
            eat_spore_vel_zero_time=0.2, # Time to zero speed after eating spores(s)
        ))
        return EasyDict(cfg)

    def __init__(self, name, position, border, size=1, vel=None, acc=None, **kwargs):
        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = ThornsBall.default_config()
        cfg.update(kwargs)
        super(ThornsBall, self).__init__(name, position, border, size=size, vel=vel, acc=acc, **cfg)
        self.vel_max = cfg.vel_max
        self.radius_min = cfg.radius_min
        self.radius_max = cfg.radius_max
        self.eat_spore_vel_init = cfg.eat_spore_vel_init
        self.eat_spore_vel_zero_time = cfg.eat_spore_vel_zero_time
        self.acc_default = self.eat_spore_vel_init / self.eat_spore_vel_zero_time
        self.move_time = 0
        self.moving = False
        self.check_border()

    def move(self, direction=None, duration=0.05):
        assert direction is None
        assert duration > 0
        self.position = self.position + self.vel * duration
        self.move_time += duration
        if self.move_time < self.eat_spore_vel_zero_time:
            self.vel += self.acc * duration
        else:
            self.vel = Vector2(0, 0)
            self.acc = Vector2(0, 0)
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
                self.acc = - self.acc_default * ball.vel.normalize()
                self.move_time = 0
                self.moving = True
        else:
            logging.debug('ThornsBall can not eat {}'.format(type(ball)))
        return True
