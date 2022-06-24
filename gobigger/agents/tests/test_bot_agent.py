import logging
import pytest
import uuid
from pygame.math import Vector2
import time
import random
import numpy as np
import cv2
import pygame

from gobigger.agents import BotAgent
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestBotAgent:

    def test_step(self):
        server = Server(dict(
            team_num=4, 
            player_num_per_team=3, 
            frame_limit=20, 
        ))
        server.reset()
        bot_agents = []
        for index, player in enumerate(server.player_manager.get_players()):
            bot_agents.append(BotAgent(player.player_id, level=index%3+1))
            logging.debug('players init: {}'.format(player.player_id))
        time_obs = 0
        time_step = 0
        time_fill_all = 0
        time_get_rectangle = 0
        time_get_clip = 0
        time_cvt = 0
        time_overlap = 0
        for i in range(100):
            t1 = time.time()
            obs = server.obs()
            t2 = time.time()
            if i % 4 == 0:
                actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
            else:
                actions = None
            t3 = time.time()
            finish_flag = server.step(actions=actions)
            t4 = time.time()
            tmp_obs = t2-t1
            tmp_step = t4-t3
            time_obs +=  tmp_obs
            time_step += tmp_step
            logging.debug('{} {} obs: {:.3f} / {:.3f}, step: {:.3f} / {:.3f}'\
                .format(i, server.last_frame_count, tmp_obs, time_obs/(i+1), tmp_step, time_step/(i+1)))

            if finish_flag:
                logging.debug('Game Over')
                break
        server.close()
