import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import numpy as np
import cv2
import argparse
import time

from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender
from gobigger.agents import BotAgent
from gobigger.envs import GoBiggerEnv, GoBiggerSPEnv

logging.basicConfig(level=logging.DEBUG)


def play_partial_against_bot():
    env = GoBiggerEnv(dict(
        team_num=3, 
        player_num_per_team=1,
    ), step_mul=1)
    obs = env.reset()
    done = False
    render = RealtimePartialRender()
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    my_player_id = 0
    bot_agents = []
    for player in env.server.player_manager.get_players():
        if player.player_id != my_player_id:
            bot_agents.append(BotAgent(player.player_id))
    for i in range(100000):
        actions = None
        x, y = None, None
        action_type = 0
        # ================ control by keyboard ===============
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0]-render.game_screen_width/2) / (render.game_screen_width/4)
        y = (mouse_pos[1]-render.game_screen_height/2) / (render.game_screen_height/4)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # eject
                    x, y = None, None                    
                    action_type = 1
                elif event.key == pygame.K_w: # split
                    x, y = None, None                    
                    action_type = 2
                elif event.key == pygame.K_e: # cheating, adding weight
                    action_type = 0
                    env.server.player_manager.get_players()[0].get_balls()[0].set_score(100000)
        actions = {my_player_id: [x, y, action_type]}
        actions.update({agent.name: agent.step(obs[1][agent.name]) for agent in bot_agents})
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            render.fill(obs[0], obs[1][0], player_num_per_team=1, fps=fps_real)
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


def play_all_against_bot():
    env = GoBiggerEnv(dict(
        team_num=3, 
        player_num_per_team=1,
    ), step_mul=1)
    obs = env.reset()
    done = False
    render = RealtimeRender()
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    my_player_id = 0
    bot_agents = []
    for player in env.server.player_manager.get_players():
        if player.player_id != my_player_id:
            bot_agents.append(BotAgent(player.player_id))
    for i in range(100000):
        actions = None
        x, y = None, None
        action_type = 0
        # ================ control by keyboard ===============
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0]-render.game_screen_width/2) / (render.game_screen_width/4)
        y = (mouse_pos[1]-render.game_screen_height/2) / (render.game_screen_height/4)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # eject
                    x, y = None, None                    
                    action_type = 1
                elif event.key == pygame.K_w: # split
                    x, y = None, None                    
                    action_type = 2
                elif event.key == pygame.K_e: # cheating, adding weight
                    action_type = 0
                    env.server.player_manager.get_players()[0].get_balls()[0].set_score(100000)
        actions = {my_player_id: [x, y, action_type]}
        actions.update({agent.name: agent.step(obs[1][agent.name]) for agent in bot_agents})
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real)
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


def play_partial_sp_against_bot():
    env = GoBiggerSPEnv(dict(
        team_num=1, 
        player_num_per_team=1,
    ), step_mul=1)
    obs = env.reset()
    done = False
    render = RealtimePartialRender()
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    for i in range(100000):
        clone_balls = obs[1][0]['overlap']['clone']
        ball_ids = [ball[-1] for ball in clone_balls]
        actions = None
        x, y = None, None
        action_type = 0
        # ================ control by keyboard ===============
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0]-render.game_screen_width/2) / (render.game_screen_width/4)
        y = (mouse_pos[1]-render.game_screen_height/2) / (render.game_screen_height/4)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # eject
                    x, y = None, None                    
                    action_type = 1
                elif event.key == pygame.K_w: # split
                    x, y = None, None                    
                    action_type = 2
                elif event.key == pygame.K_e: # cheating, adding weight
                    action_type = 0
                    env.server.player_manager.get_players()[0].get_balls()[0].set_score(100000)
        actions = {player.player_id: {ball_id: [x, y, action_type] for ball_id in ball_ids} for player in env.server.player_manager.get_players()}
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            # import pdb; pdb.set_trace()
            render.fill(obs[0], obs[1][0], player_num_per_team=1, fps=fps_real)
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['st', 'sp'], default='st')
    parser.add_argument('--vision-type', type=str, choices=['full', 'partial'], default='partial')
    args = parser.parse_args()

    if args.mode == 'st':
        if args.vision_type == 'partial':
            play_partial_against_bot()
        elif args.vision_type == 'full':
            play_all_against_bot()
    elif args.mode == 'sp':
        if args.vision_type == 'partial':
            play_partial_sp_against_bot()
    else:
        print('Not Support')
