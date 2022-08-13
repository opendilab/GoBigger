import logging
from easydict import EasyDict
from pygame.math import Vector2
import math

from gobigger.utils import format_vector, add_score, Border, deep_merge_dicts
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
            score_init=1.5,
            vel_init=50,
            vel_zero_frame=10,
        ))
        return EasyDict(cfg)

    def __init__(self, ball_id, position, border, score, direction=Vector2(0,0), owner=-1, **kwargs):
        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = SporeBall.default_config()
        cfg = deep_merge_dicts(cfg, kwargs)
        super(SporeBall, self).__init__(ball_id, position, score=score, border=border, **cfg)
        self.score_init = cfg.score_init
        self.vel_init = cfg.vel_init
        self.vel_zero_frame = cfg.vel_zero_frame
        # normal kwargs
        self.direction = direction.normalize()
        self.vel = self.vel_init * self.direction
        self.vel_piece = self.vel / self.vel_zero_frame
        self.owner = owner
        self.move_frame = 0
        # reset score
        if self.score != self.score_init:
            self.set_score(self.score_init)
        self.moving = True
        self.check_border()

    def move(self, direction=None, duration=0.05):
        assert direction is None
        assert duration > 0
        if self.moving:
            self.position = self.position + self.vel * duration
            self.move_frame += 1
            if self.move_frame < self.vel_zero_frame:
                self.vel -= self.vel_piece
            else:
                self.vel = Vector2(0, 0)
                self.vel_piece = Vector2(0, 0)
                self.moving = False
        self.check_border()
        return True

    def eat(self, ball):
        logging.debug('SporeBall can not eat others')
        return

    def save(self):
        return [self.position.x, self.position.y, self.radius]
