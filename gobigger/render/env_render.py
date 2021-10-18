import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
import numpy as np
import cv2
import time

from .base_render import BaseRender
from gobigger.utils import Colors, BLACK, YELLOW, GREEN
from gobigger.utils import PLAYER_COLORS, FOOD_COLOR, THORNS_COLOR, SPORE_COLOR
from gobigger.utils import precision_algorithm, Border, to_aliased_circle


class EnvRender(BaseRender):
    '''
    Overview:
        No need to use a new window, giving a global view and the view that each player can see
    '''
    def __init__(self, width, height, background=(255,255,255), padding=(0,0), cell_size=10, 
                 scale_up_ratio=1.5, vision_x_min=100, vision_y_min=100, only_render=True, use_spatial=True):
        super(EnvRender, self).__init__(width, height, background=background, padding=padding, 
                                        cell_size=cell_size, only_render=only_render)
        self.scale_up_ratio = scale_up_ratio
        self.vision_x_min = vision_x_min
        self.vision_y_min = vision_y_min
        self.use_spatial = use_spatial

    def fill_all(self, screen, food_balls, thorns_balls, spore_balls, players):
        font = pygame.font.SysFont('Menlo', 12, True)
        # render all balls
        for ball in food_balls:
            pygame.draw.circle(screen, FOOD_COLOR, ball.position, ball.radius)
        for ball in thorns_balls:
            pygame.draw.polygon(screen, THORNS_COLOR, to_aliased_circle(ball.position, ball.radius))
        for ball in spore_balls:
            pygame.draw.circle(screen, SPORE_COLOR, ball.position, ball.radius)
        for index, player in enumerate(players):
            for ball in player.get_balls():
                pygame.draw.circle(screen, PLAYER_COLORS[int(ball.owner)], ball.position, ball.radius)
        screen_data = pygame.surfarray.array3d(screen)
        return screen_data

    def get_clip_screen(self, screen_data, rectangle):
        if len(screen_data.shape) == 3:
            screen_data_clip = screen_data[rectangle[0]:rectangle[2], 
                                           rectangle[1]:rectangle[3], :]
        else:
            screen_data_clip = screen_data[rectangle[0]:rectangle[2], 
                                           rectangle[1]:rectangle[3]]
        return screen_data_clip

    def get_rectangle_by_player(self, player):
        '''
        Multiples of the circumscribed matrix of the centroid
        '''
        centroid = player.cal_centroid()
        xs_max = 0
        ys_max = 0
        for ball in player.get_balls():
            direction_center = centroid - ball.position
            if abs(direction_center.x) + ball.radius > xs_max:
                xs_max = abs(direction_center.x) + ball.radius
            if abs(direction_center.y) + ball.radius > ys_max:
                ys_max = abs(direction_center.y) + ball.radius
        xs_max = max(xs_max, self.vision_x_min)
        ys_max = max(ys_max, self.vision_y_min)
        scale_up_len =  max(xs_max, ys_max)
        left_top_x = min(max(int(centroid.x - scale_up_len * self.scale_up_ratio), 0), 
                         max(int(self.width_full - scale_up_len * self.scale_up_ratio * 2), 0))
        left_top_y = min(max(int(centroid.y - scale_up_len * self.scale_up_ratio), 0),
                         max(int(self.height_full - scale_up_len * self.scale_up_ratio * 2), 0))
        right_bottom_x = min(int(left_top_x + scale_up_len * self.scale_up_ratio * 2), self.width_full)
        right_bottom_y = min(int(left_top_y + scale_up_len * self.scale_up_ratio * 2), self.height_full)
        rectangle = (left_top_x, left_top_y, right_bottom_x, right_bottom_y)
        return rectangle

    def get_overlap(self, rectangle, food_balls, thorns_balls, spore_balls, player):
        def food_generator(rectangle, food_balls):
            for ball in food_balls:
                if ball.judge_in_rectangle(rectangle):
                    yield({'position': tuple(ball.position), 'radius': ball.radius})

        def thorns_generator(rectangle, thorns_balls):
            for ball in thorns_balls:
                if ball.judge_in_rectangle(rectangle):
                    yield({'position': tuple(ball.position), 'radius': ball.radius})

        def spore_generator(rectangle, spore_balls):
            for ball in spore_balls:
                if ball.judge_in_rectangle(rectangle):
                    yield({'position': tuple(ball.position), 'radius': ball.radius})
        
        def player_generator(rectangle, player):
            for ball in player.get_balls():
                if ball.judge_in_rectangle(rectangle):
                    yield({'position': tuple(ball.position), 'radius': ball.radius, 
                                        'player': player.name, 'team': player.team_name})

        return  {'food': food_generator(rectangle, food_balls), 'thorns': thorns_generator(rectangle, thorns_balls), 
                'spore': spore_generator(rectangle, spore_balls), 'clone': player_generator(rectangle, player)}

    def update_all(self, food_balls, thorns_balls, spore_balls, players):
        screen_data_all = None
        feature_layers = None
        if self.use_spatial:
            screen_all = pygame.Surface((self.width, self.height))
            screen_all.fill(self.background)
            screen_data_all = self.fill_all(screen_all, food_balls, thorns_balls, spore_balls, players)
        screen_data_players = {}

      #  food_balls = precision_algorithm(Border(0, 0, 1000, 1000), food_balls)

        for player in players:
            rectangle = self.get_rectangle_by_player(player)
            if self.use_spatial:
                screen_data_player = self.get_clip_screen(screen_data_all, rectangle=rectangle)
                screen_data_player = cv2.cvtColor(screen_data_player, cv2.COLOR_RGB2BGR)
                screen_data_player = np.fliplr(screen_data_player)
                screen_data_player = np.rot90(screen_data_player)
                feature_layers = self.transfer_rgb_to_features(screen_data_player, player_num=len(players))
            overlap = self.get_overlap(rectangle, food_balls, thorns_balls, spore_balls, player)

            # overlap = self.get_overlap(rectangle, food_balls.solve(rectangle[0], rectangle[1],rectangle[2], rectangle[3), thorns_balls, spore_balls, player)

            screen_data_players[player.name] = {
                'feature_layers': feature_layers,
                'rectangle': rectangle,
                'overlap': overlap,
                'team_name': player.team_name,
            }
        return screen_data_all, screen_data_players

    def get_tick_all_colorful(self, food_balls, thorns_balls, spore_balls, players, partial_size=300, player_num_per_team=3):
        screen_all = pygame.Surface((self.width, self.height))
        screen_all.fill(self.background)
        # render all balls
        for ball in food_balls:
            pygame.draw.circle(screen_all, BLACK, ball.position, ball.radius)
        for ball in thorns_balls:
            pygame.draw.polygon(screen_all, GREEN, to_aliased_circle(ball.position, ball.radius))
        for ball in spore_balls:
            pygame.draw.circle(screen_all, YELLOW, ball.position, ball.radius)
        
        for index, player in enumerate(players):
            for ball in player.get_balls():
                # pygame.draw.circle(screen_all, Colors[int(ball.team_name)][int(ball.owner)%player_num_per_team], ball.position, ball.radius)
                pygame.draw.circle(screen_all, Colors[int(ball.team_name)][0], ball.position, ball.radius)
                font = pygame.font.SysFont('Menlo', max(int(ball.radius/1.5+2), 6), True)
                screen_all.blit(font.render(ball.owner, int(ball.radius/1.5+2), (255,255,255)), ball.position-Vector2(int(ball.radius/1.5+2), int(ball.radius/1.5+2))/2)
                
        screen_data_all = pygame.surfarray.array3d(screen_all)
        screen_data_players = {}
        for player in players:
            rectangle = self.get_rectangle_by_player(player)
            screen_data_player = self.get_clip_screen(screen_data_all, rectangle=rectangle)
            screen_data_player = np.resize(np.rot90(np.fliplr(cv2.cvtColor(screen_data_player, cv2.COLOR_RGB2BGR))), (partial_size, partial_size, 3))
            screen_data_players[player.name] = screen_data_player
        screen_data_all = np.rot90(np.fliplr(cv2.cvtColor(screen_data_all, cv2.COLOR_RGB2BGR)))
        return screen_data_all, screen_data_players

    def transfer_rgb_to_features(self, rgb, player_num=12):
        '''
        Overview:
            12 player + food + spore + thorns
        '''
        features = []
        h, w = rgb.shape[0:2]
        tmp_rgb = rgb[:,:,0]
        assert len(tmp_rgb.shape) == 2
        for i in range(player_num):
            features.append((tmp_rgb==PLAYER_COLORS[i][0]).astype(int))
        features.append((tmp_rgb==FOOD_COLOR[0]).astype(int))
        features.append((tmp_rgb==SPORE_COLOR[0]).astype(int))
        features.append((tmp_rgb==THORNS_COLOR[0]).astype(int))
        return features

    def show(self):
        raise NotImplementedError

    def close(self):
        pygame.quit()
