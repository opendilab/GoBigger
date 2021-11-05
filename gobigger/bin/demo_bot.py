import logging
import pytest
import uuid
from pygame.math import Vector2
import time
import random
import numpy as np
import cv2
import pygame

from gobigger.agents import BotAgent, LowAgent, MidAgent
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


def demo_bot():
    server = Server(dict(
        team_num=4, 
        player_num_per_team=3, 
        map_width=1000, 
        map_height=1000, 
        match_time=60*10, 
        state_tick_per_second=20, # frame
        action_tick_per_second=5, 
        collision_detection_type='precision',
        save_video=True,
        save_path='',
        manager_settings=dict(
            # food setting
            food_manager=dict(
                num_init=2000, # initial number
                num_min=2000, # Minimum number
                num_max=2500, # Maximum number
                refresh_time=2, # Time interval (seconds) for refreshing food in the map
                refresh_num=30, # The number of refreshed foods in the map each time
                ball_settings=dict( # The specific parameter description can be viewed in the ball module
                    radius_min=2, 
                    radius_max=2,
                ),
            ),
            # thorns setting
            thorns_manager=dict(
                num_init=15, # initial number
                num_min=15, # Minimum number
                num_max=20, # Maximum number
                refresh_time=2, # Time interval (seconds) for refreshing thorns in the map
                refresh_num=2, # The number of refreshed  thorns in the map each time
                ball_settings=dict( # The specific parameter description can be viewed in the ball module
                    radius_min=12, 
                    radius_max=20, 
                    vel_max=100,
                    eat_spore_vel_init=10, 
                    eat_spore_vel_zero_time=1,
                )
            ),
            # player setting
            player_manager=dict(
                ball_settings=dict(  # The specific parameter description can be viewed in the ball module
                    acc_max=100, 
                    vel_max=25,
                    radius_min=3, 
                    radius_max=100, 
                    radius_init=3, 
                    part_num_max=16, 
                    on_thorns_part_num=10, 
                    on_thorns_part_radius_max=20,
                    split_radius_min=10, 
                    eject_radius_min=10, 
                    recombine_age=20,
                    split_vel_init=30,
                    split_vel_zero_time=1, 
                    stop_zero_time=1,
                    size_decay_rate=0.00005, 
                    given_acc_weight=10,
                )
            ),
            # spore setting
            spore_manager=dict(
                ball_settings=dict( # The specific parameter description can be viewed in the ball module
                    radius_min=3, 
                    radius_max=3, 
                    vel_init=250,
                    vel_zero_time=0.3, 
                    spore_radius_init=20, 
                )
            )
        ),
        custom_init=dict(
            food=[],
            thorns=[],
            spore=[],
            clone=[],
        ),
    ))
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.start()
    bot_agents = []
    for player in server.player_manager.get_players():
        #bot_agents.append(LowAgent(player.name))
        #bot_agents.append(MidAgent(player.name))
        bot_agents.append(BotAgent(player.name, level=1))
    time_obs = 0
    time_step = 0
    time_fill_all = 0
    time_get_rectangle = 0
    time_get_clip = 0
    time_cvt = 0
    time_overlap = 0
    for i in range(100000):
        t1 = time.time()
        obs = server.obs()
        t2 = time.time()
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        t3 = time.time()
        finish_flag = server.step(actions=actions)
        t4 = time.time()
        tmp_obs = t2-t1
        tmp_step = t4-t3
        time_obs +=  tmp_obs
        time_step += tmp_step
        logging.debug('{} {:.4f} obs: {:.3f} / {:.3f}, step: {:.3f} / {:.3f}'\
            .format(i, server.last_time, tmp_obs, time_obs/(i+1), tmp_step, time_step/(i+1)))

        if finish_flag:
            logging.debug('Game Over')
            break
    server.close()


if __name__ == '__main__':
    demo_bot()
