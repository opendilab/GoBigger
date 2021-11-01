import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random

from gobigger.balls import BaseBall
from gobigger.players import HumanPlayer
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestEnvRender:

    def test_init(self):
        render = EnvRender(width=1000, height=1000)
        assert render.scale_up_ratio == 1.5

    def test_fill_all(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        screen_all = pygame.Surface((render.width, render.height))
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                               team_name='0', name='0', border=border, 
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        screen_data_all = render.fill_all(screen_all, food_balls, thorns_balls, spore_balls, players)
        assert len(screen_data_all.shape) == 3

    def test_get_clip_screen(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        screen_all = pygame.Surface((render.width, render.height))
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                               team_name='0', name='0', border=border, 
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        screen_data_all = render.fill_all(screen_all, food_balls, thorns_balls, spore_balls, players)
        rectangle = [100, 100, 200, 200]
        screen_data_clip = render.get_clip_screen(screen_data_all, rectangle)
        assert screen_data_clip.shape == (100, 100, 3)

    def test_get_rectangle_by_player(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        player = HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                             team_name='0', name='0', border=border, 
                             spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)
        player.respawn(position=border.sample())
        rectangle = render.get_rectangle_by_player(player)
        assert len(rectangle) == 4
        logging.debug(rectangle)

    def test_get_overlap(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        player = HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                             team_name='0', name='0', border=border, 
                             spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)
        overlap = render.get_overlap([100,100,200,200], food_balls, thorns_balls, spore_balls, player)
        assert overlap is not None
        logging.debug(overlap)

    def test_update_all(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                               team_name='0', name='0', border=border, 
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        players[0].respawn(position=border.sample())
        screen_data_all, screen_data_players = render.update_all(food_balls, thorns_balls, spore_balls, players)
        assert screen_data_all is not None
        logging.debug(screen_data_all)
        logging.debug(screen_data_players)

    def test_transfer_rgb_to_features(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        screen_all = pygame.Surface((render.width, render.height))
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                               team_name='0', name='0', border=border, 
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        screen_data_all = render.fill_all(screen_all, food_balls, thorns_balls, spore_balls, players)
        rectangle = [100, 100, 200, 200]
        screen_data_clip = render.get_clip_screen(screen_data_all, rectangle)
        assert screen_data_clip.shape == (100, 100, 3)
        feature_layers = render.transfer_rgb_to_features(screen_data_clip, player_num=len(players))

    def test_update_all_wo_spatial(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000, use_spatial=False)
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings, 
                               team_name='0', name='0', border=border, 
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        players[0].respawn(position=border.sample())
        screen_data_all, screen_data_players = render.update_all(food_balls, thorns_balls, spore_balls, players)
        assert screen_data_all is None

    def test_get_tick_all_colorful(self):
        border = Border(0, 0, 1000, 1000)
        render = EnvRender(width=1000, height=1000)
        food_balls = [BaseBall('0', border.sample(), border=border)]
        thorns_balls = [BaseBall('0', border.sample(), border=border)]
        spore_balls = [BaseBall('0', border.sample(), border=border)]
        players = [HumanPlayer(cfg=Server.default_config().manager_settings.player_manager.ball_settings,
                               team_name='0', name='0', border=border,  
                               spore_settings=Server.default_config().manager_settings.spore_manager.ball_settings)]
        players[0].respawn(border.sample())
        screen_data_all, screen_data_players = render.get_tick_all_colorful(
                            food_balls=food_balls,
                            thorns_balls=thorns_balls,
                            spore_balls=spore_balls,
                            players=players,
                            player_num_per_team=1,
                            team_name_size={'0': 100.1111})
