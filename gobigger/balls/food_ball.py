import logging
from easydict import EasyDict

from gobigger.utils import format_vector, add_score, Border, deep_merge_dicts
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
        cfg.update(dict(
            score_min=0.5,
            score_max=0.5,
        ))
        return EasyDict(cfg)

    def __init__(self, ball_id, position, score, border, **kwargs):
        super(FoodBall, self).__init__(ball_id, position, score=score, border=border, **kwargs)
        self.check_border()
        
    def move(self, direction, duration):
        logging.debug('FoodBall can not move')
        return

    def eat(self, ball):
        logging.debug('FoodBall can not eat others')
        return
