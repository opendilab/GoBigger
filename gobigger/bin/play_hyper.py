import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import numpy as np
import cv2
import argparse
import time
import importlib

from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender
from gobigger.agents import BotAgent

logging.basicConfig(level=logging.DEBUG)


def play_by_config(config_name):
    config_module = importlib.import_module('gobigger.hyper.configs.config_{}'.format(config_name))
    config = config_module.server_default_config
    server = Server(config)
    server.reset()
    render = RealtimeRender(server.map_width, server.map_height)
    server.set_render(render)
    human_team_name = '0'
    human_team_player_name = []
    bot_agents = []
    for player in server.player_manager.get_players():
        if player.team_name != human_team_name:
            bot_agents.append(BotAgent(player.name))
        else:
            human_team_player_name.append(player.name)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for i in range(100000):
        obs = server.obs()
        # actions_bot = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        actions_bot = {bot_agent.name: [None, None, -1] for bot_agent in bot_agents}
        actions = {player_name: [None, None, -1] for player_name in human_team_player_name}
        x, y = None, None
        action_type = -1
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                x1, y1, x2, y2 = None, None, None, None
                action_type1 = -1
                action_type2 = -1
                if event.key == pygame.K_UP:
                    x1, y1 = 0, -1
                if event.key == pygame.K_DOWN:
                    x1, y1 = 0, 1
                if event.key == pygame.K_LEFT:
                    x1, y1 = -1, 0
                if event.key == pygame.K_RIGHT:
                    x1, y1 = 1, 0
                if event.key == pygame.K_LEFTBRACKET: # Spores
                    action_type1 = 0
                if event.key == pygame.K_RIGHTBRACKET: # Splite
                    action_type1 = 1
                if event.key == pygame.K_BACKSLASH: # Stop moving
                    action_type1 = 2
                if event.key == pygame.K_w:
                    x2, y2 = 0, -1
                if event.key == pygame.K_s:
                    x2, y2 = 0, 1
                if event.key == pygame.K_a:
                    x2, y2 = -1, 0
                if event.key == pygame.K_d:
                    x2, y2 = 1, 0
                if event.key == pygame.K_1: # Spores
                    action_type2 = 0
                if event.key == pygame.K_2: # Splite
                    action_type2 = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type2 = 2
                actions = {
                    human_team_player_name[0]: [x1, y1, action_type1],
                    human_team_player_name[1]: [x2, y2, action_type2],
                }
        if server.last_time < server.match_time:
            actions.update(actions_bot)
            print(actions)
            server.step_state_tick(actions=actions)
            if actions is not None and x is not None and y is not None:
                render.fill(server, direction=Vector2(x, y), fps=fps_real, last_time=server.last_time)
            else:
                render.fill(server, direction=None, fps=fps_real, last_time=server.last_time)
            render.show()
            if i % server.state_tick_per_second == 0:
                t2 = time.time()
                fps_real = server.state_tick_per_second/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='2f2s')
    args = parser.parse_args()

    play_by_config(args.config)
    