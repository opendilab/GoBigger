import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import numpy as np
import cv2
import time
import copy

from .base_render import BaseRender
from gobigger.utils import FOOD_COLOR, THORNS_COLOR, SPORE_COLOR, PLAYER_COLORS, BACKGROUND, BLACK, WHITE, RED
from gobigger.utils import to_aliased_circle, to_arrow


class EnvRender(BaseRender):
    '''
    Overview:
        No need to use a new window, giving a global view and the view that each player can see
    '''
    def __init__(self, game_screen_width=512, game_screen_height=512, info_width=60, info_height=0, with_show=False,
                 padding=20, map_width=256, map_height=256):
        super(EnvRender, self).__init__(game_screen_width=game_screen_width, 
                                        game_screen_height=game_screen_height, 
                                        info_width=info_width, info_height=info_height,
                                        with_show=with_show)
        self.scale_ratio_w = (self.game_screen_width-padding*2) / map_width
        self.scale_ratio_h = (self.game_screen_height-padding*2) / map_height
        self.padding = padding

    def get_screen(self, food_balls, thorns_balls, spore_balls, players, player_num_per_team):
        screen_all = pygame.Surface((self.total_screen_width, self.total_screen_height))
        screen_all = self.render_all_balls_colorful(screen_all, food_balls, thorns_balls, spore_balls, players, player_num_per_team)
        screen_all = self.render_leaderboard_colorful(screen_all, players, player_num_per_team)
        screen_data_all = pygame.surfarray.array3d(screen_all)
        screen_data_all = np.rot90(np.fliplr(cv2.cvtColor(screen_data_all, cv2.COLOR_RGB2BGR)))
        return screen_data_all

    def render_all_balls_colorful(self, screen, food_balls, thorns_balls, spore_balls, players, player_num_per_team):
        screen.fill(BACKGROUND)
        # add line
        pygame.draw.line(screen, RED, (self.padding, self.padding), (self.game_screen_width-self.padding, self.padding), width=1)
        pygame.draw.line(screen, RED, (self.padding, self.padding), (self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(screen, RED, (self.padding, self.game_screen_width-self.padding), 
                         (self.game_screen_width-self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(screen, RED, (self.game_screen_width-self.padding, self.padding), 
                         (self.game_screen_width-self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(screen, BLACK, (self.game_screen_width, 0), 
                         (self.game_screen_width, self.game_screen_width+self.padding), width=1)
        # render all balls
        for ball in food_balls:
            x = ball.position.x * self.scale_ratio_w + self.padding
            y = ball.position.y * self.scale_ratio_h + self.padding
            r = ball.radius * self.scale_ratio_w
            pygame.draw.circle(screen, FOOD_COLOR, Vector2(x, y), r)
        for ball in thorns_balls:
            x = ball.position.x * self.scale_ratio_w + self.padding
            y = ball.position.y * self.scale_ratio_h + self.padding
            r = ball.radius * self.scale_ratio_w
            pygame.draw.polygon(screen, THORNS_COLOR, to_aliased_circle(Vector2(x, y), r))
        for ball in spore_balls:
            x = ball.position.x * self.scale_ratio_w + self.padding
            y = ball.position.y * self.scale_ratio_h + self.padding
            r = ball.radius * self.scale_ratio_w
            pygame.draw.circle(screen, SPORE_COLOR, Vector2(x, y), r)
        for player in players:
            for ball in player.get_balls():
                x = ball.position.x * self.scale_ratio_w + self.padding
                y = ball.position.y * self.scale_ratio_h + self.padding
                r = ball.radius * self.scale_ratio_w
                pygame.draw.circle(screen, PLAYER_COLORS[int(ball.team_id)][0], Vector2(x, y), r)
                # pygame.draw.polygon(screen, PLAYER_COLORS[int(ball.team_id)][0], to_arrow(Vector2(x, y), r, ball.direction))
                font_size = int(r/1.6)
                font = pygame.font.SysFont('arial', max(font_size, 8), True)
                txt = font.render('{}'.format(chr(int(ball.player_id%player_num_per_team)+65)), True, WHITE)
                txt_rect = txt.get_rect(center=(x, y))
                screen.blit(txt, txt_rect)
        return screen

    def render_leaderboard_colorful(self, screen, players, player_num_per_team):
        team_name_size = {}
        team_size = {}
        for player in players:
            if player.team_id not in team_name_size:
                team_name_size[player.team_id] = {}
                team_size[player.team_id] = 0
            team_name_size[player.team_id][player.player_id] = player.get_total_size()
            team_size[player.team_id] += team_name_size[player.team_id][player.player_id]
        team_size = sorted(team_size.items(), key=lambda d: d[0], reverse=True)
        start = 10
        for index, (team_id, size) in enumerate(team_size):
            start += 20
            font = pygame.font.SysFont('arial', 10, True)
            fps_txt = font.render('{} : {:.3f}'.format(team_id, size), True, PLAYER_COLORS[int(team_id)][0])
            screen.blit(fps_txt, (self.game_screen_width+5, start))
            start += 20
            font = pygame.font.SysFont('arial', 9, True)
            for player_id, player_size in team_name_size[team_id].items():
                fps_txt = font.render('  {} : {:.3f}'.format(chr(player_id%player_num_per_team+65), player_size), True, 
                                      PLAYER_COLORS[team_id][0])
                screen.blit(fps_txt, (self.game_screen_width+5, start))
                start += 20
        return screen

    def show(self):
        raise NotImplementedError

    def close(self):
        pygame.quit()
