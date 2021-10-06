import logging
from easydict import EasyDict

from gobigger.utils import format_vector, add_size, Border
from .base_ball import BaseBall


class FoodBall(BaseBall):
    """
    Overview:
        - characteristic:
        * Can't move, can only be eaten, randomly generated
    """
    @staticmethod
    def default_config():
        cfg = BaseBall.default_config()
        cfg.update(dict())
        return EasyDict(cfg)

    def __init__(self, name, position, border, size=1, vel=None, acc=None, **kwargs):
        super(FoodBall, self).__init__(name, position, border, size=size, vel=vel, acc=acc, **kwargs)
        self.check_border()

    def move(self, direction, duration):
        logging.debug('FoodBall can not move')
        return

    def eat(self, ball):
        logging.debug('FoodBall can not eat others')
        return
