import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import cv2
import math

from .base_render import BaseRender
from .env_render import EnvRender
from gobigger.utils import FOOD_COLOR, THORNS_COLOR, SPORE_COLOR, PLAYER_COLORS, BACKGROUND, BLACK, RED, WHITE
from gobigger.utils import to_aliased_circle, to_arrow


class RealtimeRender(BaseRender):
    '''
    Overview:
        Used in real-time games, giving a global view
    '''
    def __init__(self, game_screen_width=800, game_screen_height=800, info_width=0, info_height=0, with_show=True,
                 padding=20, map_width=256, map_height=256):
        super(RealtimeRender, self).__init__(game_screen_width=game_screen_width, 
                                             game_screen_height=game_screen_height, 
                                             info_width=info_width, info_height=info_height,
                                             with_show=with_show)
        self.scale_ratio_w = (self.game_screen_width-padding*2) / map_width
        self.scale_ratio_h = (self.game_screen_height-padding*2) / map_height
        self.padding = padding

    def render_all_balls_colorful(self, food_balls, thorns_balls, spore_balls, players, player_num_per_team):
        # render all balls
        for ball in food_balls:
            x = ball.position.x * self.scale_ratio_w + self.padding
            y = ball.position.y * self.scale_ratio_h + self.padding
            r = ball.radius * self.scale_ratio_w
            pygame.draw.circle(self.screen, FOOD_COLOR, Vector2(x, y), r)
        for ball in thorns_balls:
            x = ball.position.x * self.scale_ratio_w + self.padding
            y = ball.position.y * self.scale_ratio_h + self.padding
            r = ball.radius * self.scale_ratio_w
            pygame.draw.polygon(self.screen, THORNS_COLOR, to_aliased_circle(Vector2(x, y), r))
        for ball in spore_balls:
            x = ball.position.x * self.scale_ratio_w + self.padding
            y = ball.position.y * self.scale_ratio_h + self.padding
            r = ball.radius * self.scale_ratio_w
            pygame.draw.circle(self.screen, SPORE_COLOR, Vector2(x, y), r)
        for player in players:
            for ball in player.get_balls():
                x = ball.position.x * self.scale_ratio_w + self.padding
                y = ball.position.y * self.scale_ratio_h + self.padding
                r = ball.radius * self.scale_ratio_w
                pygame.draw.circle(self.screen, PLAYER_COLORS[int(ball.team_id)][0], Vector2(x, y), r)
                pygame.draw.polygon(self.screen, PLAYER_COLORS[int(ball.team_id)][0], to_arrow(Vector2(x, y), r, ball.direction))
                font_size = int(r/1.6)
                font = pygame.font.SysFont('arial', max(font_size, 8), True)
                txt = font.render('{}'.format(chr(int(ball.player_id%player_num_per_team)+65)), True, WHITE)
                txt_rect = txt.get_rect(center=(x, y))
                self.screen.blit(txt, txt_rect)

    def fill(self, food_balls, thorns_balls, spore_balls, players, player_num_per_team=1, fps=20):
        self.screen.fill(BACKGROUND)
        self.render_all_balls_colorful(food_balls, thorns_balls, spore_balls, players, player_num_per_team)
        # add line
        pygame.draw.line(self.screen, RED, (self.padding, self.padding), (self.game_screen_width-self.padding, self.padding), width=1)
        pygame.draw.line(self.screen, RED, (self.padding, self.padding), (self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(self.screen, RED, (self.padding, self.game_screen_width-self.padding), 
                         (self.game_screen_width-self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(self.screen, RED, (self.game_screen_width-self.padding, self.padding), 
                         (self.game_screen_width-self.padding, self.game_screen_width-self.padding), width=1)
        # for debug
        # font = pygame.font.SysFont('Menlo', 15, True)

        # assert len(leaderboard) > 0, 'leaderboard could not be None'
        # leaderboard = sorted(leaderboard.items(), key=lambda d: d[1], reverse=True)
        # for index, (team_id, team_size) in enumerate(leaderboard):
        #     pos_txt = font.render('{}: {:.5f}'.format(team_id, team_size), 1, RED)
        #     self.screen.blit(pos_txt, (20, 10+10*(index*2+1)))

        # fps_txt = font.render('fps: ' + str(fps), 1, RED)
        # last_frame_txt = font.render('frame_count: {} / {}'.format(frame_count, int(frame_count/20)), 1, RED)
        # self.screen.blit(fps_txt, (20, self.total_screen_height - 30))
        # self.screen.blit(last_frame_txt, (20, self.total_screen_height - 50))
    
    def show(self):
        pygame.display.update()
        # self.fpsClock.tick(self.FPS)

    def close(self):
        pygame.quit()


class RealtimePartialRender(BaseRender):
    '''
    Overview:
        Used in real-time games to give the player a visible field of view. The corresponding player can be obtained by specifying the player name. The default is the first player
    '''
    def __init__(self, game_screen_width=512, game_screen_height=512, info_width=0, info_height=0, with_show=True):
        super(RealtimePartialRender, self).__init__(game_screen_width=game_screen_width, 
                                                    game_screen_height=game_screen_height, 
                                                    info_width=info_width, info_height=info_height,
                                                    with_show=with_show)

    def render_all_balls_colorful(self, overlap, player_num_per_team=1, scale_ratio_w=1, scale_ratio_h=1,
                                  start_x=0, start_y=0):
        # render all balls
        for ball in overlap['food']:
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            pygame.draw.circle(self.screen, FOOD_COLOR, Vector2(x, y), r)
        for ball in overlap['thorns']:
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            pygame.draw.polygon(self.screen, THORNS_COLOR, to_aliased_circle(Vector2(x, y), r))
            # pygame.draw.circle(self.screen, THORNS_COLOR, Vector2(x, y), r)
        for ball in overlap['spore']:
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            pygame.draw.circle(self.screen, SPORE_COLOR, Vector2(x, y), r)
        for ball in overlap['clone']:
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            direction = Vector2(ball[5], ball[6])
            pygame.draw.circle(self.screen, PLAYER_COLORS[int(ball[8])][0], Vector2(x, y), r)
            point_list = to_arrow(Vector2(x, y), r, direction)
            pygame.draw.polygon(self.screen, PLAYER_COLORS[int(ball[8])][0], point_list)
            font_size = int(r/1.6)
            font = pygame.font.SysFont('arial', max(font_size, 8), True)
            txt = font.render('{}'.format(chr(int(ball[7])%player_num_per_team+65)), True, WHITE)
            txt_rect = txt.get_rect(center=(x, y))
            self.screen.blit(txt, txt_rect)

    def fill(self, global_state, player_state, player_num_per_team=1, fps=20):
        self.screen.fill(BACKGROUND)
        rectangle = player_state['rectangle']
        overlap = player_state['overlap']
        leaderboard = global_state['leaderboard']
        frame_count = global_state['last_frame_count']
        map_width, map_height = global_state['border']

        left, top, right, bottom = rectangle
        width_real, height_real, hw_ratio = right-left, bottom-top, (right-left)/(bottom-top)
        scale_ratio_w = self.game_screen_width / width_real
        scale_ratio_h = self.game_screen_width / height_real
        start_x = left
        start_y = top

        self.render_all_balls_colorful(overlap, player_num_per_team=player_num_per_team, 
                                       scale_ratio_w=scale_ratio_w, scale_ratio_h=scale_ratio_h,
                                       start_x=start_x, start_y=start_y)
        # add line
        pygame.draw.line(self.screen, BLACK, ((map_width-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h),
                         ((map_width-start_x) * scale_ratio_w, (map_height-start_y) * scale_ratio_h), width=1)
        pygame.draw.line(self.screen, BLACK, ((0-start_x) * scale_ratio_w, (map_height-start_y) * scale_ratio_h),
                         ((map_width-start_x) * scale_ratio_w, (map_height-start_y) * scale_ratio_h), width=1)
        pygame.draw.line(self.screen, BLACK, ((0-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h),
                         ((0-start_x) * scale_ratio_w, (map_height-start_y) * scale_ratio_h), width=1)
        pygame.draw.line(self.screen, BLACK, ((0-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h),
                         ((map_width-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h), width=1)

        # for debug
        font = pygame.font.SysFont('Menlo', 15, True)

        assert len(leaderboard) > 0, 'leaderboard could not be None'
        leaderboard = sorted(leaderboard.items(), key=lambda d: d[1], reverse=True)
        for index, (team_id, team_size) in enumerate(leaderboard):
            pos_txt = font.render('{}: {:.5f}'.format(team_id, team_size), 1, RED)
            self.screen.blit(pos_txt, (20, 10+10*(index*2+1)))

        fps_txt = font.render('fps: ' + str(fps), 1, RED)
        last_frame_txt = font.render('frame_count: {} / {}'.format(frame_count, int(frame_count/20)), 1, RED)
        self.screen.blit(fps_txt, (20, self.total_screen_height - 30))
        self.screen.blit(last_frame_txt, (20, self.total_screen_height - 50))
    
    def show(self):
        pygame.display.update()
        # self.fpsClock.tick(self.FPS)

    def close(self):
        pygame.quit()
