import pygame
import numpy as np
import cv2
from pygame.math import Vector2

from .base_render import BaseRender
from cgobigger.utils import FOOD_COLOR, THORNS_COLOR, SPORE_COLOR, PLAYER_COLORS, BACKGROUND, BLACK, WHITE
from cgobigger.utils import FOOD_COLOR_GRAYSCALE, THORNS_COLOR_GRAYSCALE, SPORE_COLOR_GRAYSCALE, PLAYER_COLORS_GRAYSCALE, BACKGROUND_GRAYSCALE
from cgobigger.utils import to_aliased_circle


class EnvRender(BaseRender):
    '''
    Overview:
        No need to use a new window, giving a global view and the view that each player can see
    '''
    def __init__(self, width, height, padding=(0,0), cell_size=10,
                 scale_up_ratio=1.5, vision_x_min=100, vision_y_min=100, only_render=True):
        super(EnvRender, self).__init__(width, height, padding=padding,
                                        cell_size=cell_size, only_render=only_render)
        self.scale_up_ratio = scale_up_ratio
        self.vision_x_min = vision_x_min
        self.vision_y_min = vision_y_min

    def set_obs_settings(self, obs_settings):
        self.with_spatial = obs_settings.get('with_spatial', False)
        self.with_speed = obs_settings.get('with_speed', False)
        self.with_all_vision = obs_settings.get('with_all_vision', False)

    def get_clip_screen(self, screen_data, rectangle):
        if len(screen_data.shape) == 3:
            screen_data_clip = screen_data[rectangle[0]:rectangle[2],
                               rectangle[1]:rectangle[3], :]
        elif len(screen_data.shape) == 2:
            screen_data_clip = screen_data[rectangle[0]:rectangle[2],
                               rectangle[1]:rectangle[3]]
        else:
            raise NotImplementedError
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

    def render_all_balls_colorful(self, screen, food_balls, thorns_balls, spore_balls, clone_balls,
                                  player_num_per_team):
        # render all balls
        for ball in food_balls:
            pygame.draw.circle(screen, FOOD_COLOR, Vector2(ball[0], ball[1]), ball[2])
        for ball in thorns_balls:
            pygame.draw.polygon(screen, THORNS_COLOR, to_aliased_circle(Vector2(ball[0], ball[1]), ball[2]))
        for ball in spore_balls:
            pygame.draw.circle(screen, SPORE_COLOR, Vector2(ball[0], ball[1]), ball[2])
        player_name_size = {}
        for ball in clone_balls:
            player_name = int(ball[3])
            team_name = int(ball[4])
            pygame.draw.circle(screen, PLAYER_COLORS[int(team_name)][0], Vector2(ball[0], ball[1]), ball[2])
            font_size = int(ball[2]/1.6)
            font = pygame.font.SysFont('arial', max(font_size, 8), True)
            txt = font.render('{}'.format(chr(int(player_name)%player_num_per_team+65)), True, WHITE)
            txt_rect = txt.get_rect(center=(ball[0], ball[1]))
            screen.blit(txt, txt_rect)
            if str(player_name) not in player_name_size:
                player_name_size[str(player_name)] = 0
            player_name_size[str(player_name)] += ball[2] ** 2
        return screen, player_name_size

    def render_leaderboard_colorful(self, screen, player_name_size, player_num_per_team, team_num):
        team_name_size = {}
        for i in range(team_num):
            team_name_size[str(i)] = 0
            for j in range(player_num_per_team):
                team_name_size[str(i)] += player_name_size[str(i*player_num_per_team+j)]
        team_name_size = sorted(team_name_size.items(), key=lambda d: d[1], reverse=True)
        start = 10
        for index, (team_name, size) in enumerate(team_name_size):
            start += 20
            font = pygame.font.SysFont('arial', 16, True)
            fps_txt = font.render('{} : {:.3f}'.format(team_name, size), True, PLAYER_COLORS[int(team_name)][0])
            screen.blit(fps_txt, (self.width+20, start))
            start += 20
            font = pygame.font.SysFont('arial', 14, True)
            for j in range(player_num_per_team):
                player_name = str(int(team_name)*player_num_per_team+j)
                player_size = player_name_size[player_name]
                fps_txt = font.render('  {} : {:.3f}'.format(chr(int(player_name)%player_num_per_team+65), player_size), True, PLAYER_COLORS[int(team_name)][0])
                screen.blit(fps_txt, (self.width+20, start))
                start += 20
        return screen

    def get_tick_all_colorful(self, food_balls, thorns_balls, spore_balls, clone_balls, rectangle_dict, team_num=4,
                              player_num_per_team=3, partial_size=300, bar_width=150):
        screen_all = pygame.Surface((self.width+bar_width, self.height))
        screen_all.fill(BACKGROUND)
        pygame.draw.line(screen_all, BLACK, (self.width+1, 0), (self.width+1, self.height), width=3)
        screen_all, player_name_size = self.render_all_balls_colorful(screen_all, food_balls, thorns_balls, spore_balls, clone_balls,
                                                                      player_num_per_team=player_num_per_team)
        screen_all = self.render_leaderboard_colorful(screen_all, player_name_size,
                                                      player_num_per_team=player_num_per_team,
                                                      team_num=team_num)
        screen_data_all = pygame.surfarray.array3d(screen_all)
        screen_data_players = {}

        for player_name, rectangle in rectangle_dict.items():
            screen_data_player = self.get_clip_screen(screen_data_all, rectangle=rectangle)
            screen_data_player = cv2.resize(np.rot90(np.fliplr(cv2.cvtColor(screen_data_player, cv2.COLOR_RGB2BGR))), (partial_size, partial_size))
            screen_data_players[player_name] = screen_data_player
        screen_data_all = np.rot90(np.fliplr(cv2.cvtColor(screen_data_all, cv2.COLOR_RGB2BGR)))
        return screen_data_all, screen_data_players

    def show(self):
        raise NotImplementedError

    def close(self):
        pygame.quit()
