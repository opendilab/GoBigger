import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.players import HumanPlayer
from gobigger.balls import ThornsBall, SporeBall, CloneBall, FoodBall
from gobigger.utils import Border
from gobigger.server import Server

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.unittest
class TestHumanPlayer:

    def get_player(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_name = uuid.uuid1()
        return HumanPlayer(cfg=cfg.manager_settings.player_manager.ball_settings, 
                           team_name='0', name=player_name, border=border, 
                           spore_settings=cfg.manager_settings.spore_manager.ball_settings)

    def test_init(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player = self.get_player()
        player.respawn(position=border.sample())
        balls = player.get_balls()
        logging.debug('=================== test_init ===================')
        for index, ball in enumerate(balls):
            logging.debug('{} {}'.format(index, ball))

    def test_move(self):
        logging.debug('\n=================== test_move ===================')
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player = self.get_player()
        player.respawn(position=border.sample())
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        direction = Vector2(10, 0)
        player.move(direction=direction, duration=0.05)
        logging.debug('=================== after move ===================')
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        player.stop()
        for i in range(20):
            player.move()

    def test_split_move(self):
        logging.debug('\n=================== test_split_move ===================')
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player = self.get_player()
        player.respawn(position=border.sample())
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        food_ball = FoodBall(name=uuid.uuid1(), position=border.sample(), border=border, size=1600)
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        logging.debug('=================== after eat ===================')
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        player.split()
        logging.debug('=================== after split ===================')
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        direction = Vector2(100, 0)
        for i in range(20):
            logging.debug('=================== after move {} ==================='.format(i))
            player.move(direction=direction, duration=0.05)
            for index, ball in enumerate(player.get_balls()):
                logging.debug('{} {}'.format(index, ball))
        player.split()
        player.stop()
        player.move()

    def test_adjust(self):
        logging.debug('\n=================== test_adjust ===================')
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player = self.get_player()
        player.respawn(position=Vector2(990, 990))
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        player.adjust()
        logging.debug('=================== after adjust ===================')
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        food_ball = FoodBall(name=uuid.uuid1(), position=border.sample(), border=border, size=1600)
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        player.get_balls()[0].eat(food_ball, clone_num=len(player.get_balls()))
        logging.debug('=================== after eat ===================')
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        player.split()
        logging.debug('=================== after split ===================')
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        for i in range(10):
            player.adjust()
            logging.debug('=================== after adjust {} ==================='.format(i))
            for index, ball in enumerate(player.get_balls()):
                logging.debug('{} {}'.format(index, ball))

    def test_eject(self):
        logging.debug('\n=================== test_eject ===================')
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player = self.get_player()
        player.respawn(position=border.sample())
        for index, ball in enumerate(player.get_balls()):
            logging.debug('{} {}'.format(index, ball))
        assert isinstance(player.eject(), list)
