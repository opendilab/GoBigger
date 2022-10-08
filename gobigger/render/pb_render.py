import os
from typing import Callable, List
import pygame
import tkinter
import tkinter.filedialog as filedialog
from pygame.math import Vector2
import copy

from .base_render import BaseRender
from gobigger.utils import FOOD_COLOR, THORNS_COLOR, SPORE_COLOR, PLAYER_COLORS, BACKGROUND, \
                           BLACK, RED, WHITE, GRAY, YELLOW
from gobigger.utils import to_aliased_circle, to_arrow


class TkSelect():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Load PlayBack File")
        w_w = self.window.winfo_screenwidth()
        w_h = self.window.winfo_screenheight()
        tk_w = 350
        tk_h = 200
        self.window.geometry(f'{tk_w}x{tk_h}+{int((w_w-tk_w)/2)}+{int((w_h-tk_h)/2)}')
        btn = tkinter.Button(self.window, text="Load PlayBack File",
                     pady=10, command=self.on_load_clicked)
        btn.pack()
        self.window.mainloop()

    def on_load_clicked(self):
        my_filetypes = [('playback files', '.pb')]
        self.pb_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                    title="Please select a playback file:",
                                                    filetypes=my_filetypes)
        self.window.destroy()


class Button(object):
    def __init__(self, x, y, text, half_w=8, half_h=8):
        self.text = text
        self.x = x
        self.y = y
        self.half_w = half_w
        self.half_h = half_h
        self.left = x - half_w
        self.top = y - half_h
        self.right = x + half_w
        self.bottom = y + half_h
        self.font = pygame.font.SysFont('arial', 11, True)

    def display(self, screen, text=None):
        if text is None:
            text = self.text
        txt = self.font.render(text, True, BLACK)
        bg_rect = pygame.Rect(self.left, self.top, self.half_w*2, self.half_h*2)
        pygame.draw.rect(screen, WHITE, bg_rect)
        screen.blit(txt, txt.get_rect(center=(self.x, self.y)))

    def check_click(self, position):
        x_match = position[0] > self.left and position[0] < self.right
        y_match = position[1] > self.top and position[1] < self.bottom
        if x_match and y_match:
            return True
        else:
            return False


class PlayButton(Button):
    def __init__(self, x, y, text, half_w=8, half_h=8):
        super(PlayButton, self).__init__(x, y, text, half_w=half_w, half_h=half_h)
        self.text_choices = ['>', '||']
        self.play = True if text == '||' else False

    def on_pressed(self):
        self.play = not self.play
        self.text = self.text_choices[int(self.play)]
        return self.play


class SpeedButton(Button):
    def __init__(self, x, y, text, half_w=8, half_h=8):
        super(SpeedButton, self).__init__(x, y, text, half_w=half_w, half_h=half_h)
        self.speed_choices = ['x1', 'x2', 'x4', 'x8']
        self.speed = 1
        self.speed_index = 0

    def on_pressed(self):
        self.speed_index = (self.speed_index + 1) % len(self.speed_choices)
        self.text = self.speed_choices[self.speed_index]
        self.speed = int(self.text[-1])
        return self.speed


class Scrollbar(object):
    def __init__(self, x, y, length, width=8):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.top = self.y - width/2
        self.bottom = self.y + width/2
        self.rate = 0

    def on_pressed(self, position):
        self.rate = 1.0*(position[0]-self.x)/self.length
        return self.rate

    def check_click(self, position):
        if position[0] > self.x and position[0] < self.x+self.length \
            and position[1] > self.top and position[1] < self.bottom:
            return True
        else:
            return False

    def display(self, screen, rate=None):
        if rate is None:
            rate = self.rate
        pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x+self.length, self.y), width=3)
        pygame.draw.line(screen, YELLOW, (self.x+self.length*rate, self.top), (self.x+self.length*rate, self.bottom), width=4)


class PBRender(BaseRender):

    def __init__(self, game_screen_width=512, game_screen_height=512, info_width=60, info_height=20,
                 padding=20, map_width=128, map_height=128, pb_data=None, player_num_per_team=1):
        super(PBRender, self).__init__(game_screen_width=game_screen_width, 
                                       game_screen_height=game_screen_height, 
                                       info_width=info_width, info_height=info_height,
                                       with_show=True)
        self.padding = padding
        self.pb_data = pb_data
        assert pb_data is not None
        self.map_width = self.pb_data['cfg']['map_width']
        self.map_height = self.pb_data['cfg']['map_height']
        self.player_num_per_team = self.pb_data['cfg']['player_num_per_team']
        self.speed_button = SpeedButton(20, game_screen_height+info_height/2, 'x1')
        self.play_button = PlayButton(40, game_screen_height+info_height/2, '||')
        self.scrollbar = Scrollbar(60, game_screen_height+info_height/2, game_screen_width-80)
        self.if_play = True
        self.speed = 1
        self.frame_now = 1
        self.frame_target = self.frame_now + self.speed
        self.overlap = copy.deepcopy(self.pb_data[self.frame_now][0])
        self.leaderboard = self.pb_data[self.frame_now][2]
        self.frame_total = len(self.pb_data)
        self.rate = self.frame_now / self.frame_total

    def set_data(self):
        if self.if_play:
            if self.frame_target == self.frame_now:
                return
            if self.frame_target < self.frame_now:
                self.frame_now = 1
                self.overlap = copy.deepcopy(self.pb_data[self.frame_now][0])
                self.leaderboard = self.pb_data[self.frame_now][2]
            for i in range(self.frame_now+1, self.frame_target+1):
                if i in self.pb_data:
                    diff_balls_modify, diff_balls_remove, self.leaderboard = self.pb_data[i]
                    for index, balls in enumerate(diff_balls_modify[:-1]):
                        for ball_id, ball in balls.items():
                            self.overlap[index][ball_id] = ball
                    self.overlap[-1] = diff_balls_modify[-1]
                    for index, ball_ids in enumerate(diff_balls_remove):
                        for ball_id in ball_ids:
                            self.overlap[index].pop(ball_id, None)
        self.frame_now = self.frame_target

    def render_all_balls_colorful(self, scale_ratio_w=1, scale_ratio_h=1):
        # add line
        pygame.draw.line(self.screen, RED, (self.padding, self.padding), (self.game_screen_width-self.padding, self.padding), width=1)
        pygame.draw.line(self.screen, RED, (self.padding, self.padding), (self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(self.screen, RED, (self.padding, self.game_screen_width-self.padding), 
                         (self.game_screen_width-self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(self.screen, RED, (self.game_screen_width-self.padding, self.padding), 
                         (self.game_screen_width-self.padding, self.game_screen_width-self.padding), width=1)
        pygame.draw.line(self.screen, BLACK, (self.game_screen_width, 0), 
                         (self.game_screen_width, self.game_screen_width+self.padding), width=1)
        for ball_id, ball in self.overlap[0].items():
            x = ball[0] * scale_ratio_w + self.padding
            y = ball[1] * scale_ratio_h + self.padding
            r = ball[2] * scale_ratio_w
            pygame.draw.circle(self.screen, FOOD_COLOR, Vector2(x, y), r)
        for ball_id, ball in self.overlap[1].items():
            x = ball[0] * scale_ratio_w + self.padding
            y = ball[1] * scale_ratio_h + self.padding
            r = ball[2] * scale_ratio_w
            pygame.draw.polygon(self.screen, THORNS_COLOR, to_aliased_circle(Vector2(x, y), r))
            # pygame.draw.circle(self.screen, THORNS_COLOR, Vector2(x, y), r)
        for ball_id, ball in self.overlap[2].items():
            x = ball[0] * scale_ratio_w + self.padding
            y = ball[1] * scale_ratio_h + self.padding
            r = ball[2] * scale_ratio_w
            pygame.draw.circle(self.screen, SPORE_COLOR, Vector2(x, y), r)
        for ball_id, ball in self.overlap[3].items():
            x = ball[0] * scale_ratio_w + self.padding
            y = ball[1] * scale_ratio_h + self.padding
            r = ball[2] * scale_ratio_w
            direction = Vector2(ball[3], ball[4])
            player_id = int(ball[5])
            team_id = int(ball[6])
            pygame.draw.circle(self.screen, PLAYER_COLORS[team_id][0], Vector2(x, y), r)
            point_list = to_arrow(Vector2(x, y), r, direction)
            pygame.draw.polygon(self.screen, PLAYER_COLORS[team_id][0], point_list)
            font_size = int(r/1.6)
            font = pygame.font.SysFont('arial', max(font_size, 6), True)
            txt = font.render('{}'.format(chr(player_id%self.player_num_per_team+65)), True, WHITE)
            txt_rect = txt.get_rect(center=(x, y))
            self.screen.blit(txt, txt_rect)

    def render_rect_balls_colorful(self, scale_ratio_w=1, scale_ratio_h=1, start_x=0, start_y=0):
        # add line
        pygame.draw.line(self.screen, BLACK, ((self.map_width-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h),
                         ((self.map_width-start_x) * scale_ratio_w, (self.map_height-start_y) * scale_ratio_h), width=1)
        pygame.draw.line(self.screen, BLACK, ((0-start_x) * scale_ratio_w, (self.map_height-start_y) * scale_ratio_h),
                         ((self.map_width-start_x) * scale_ratio_w, (self.map_height-start_y) * scale_ratio_h), width=1)
        pygame.draw.line(self.screen, BLACK, ((0-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h),
                         ((0-start_x) * scale_ratio_w, (self.map_height-start_y) * scale_ratio_h), width=1)
        pygame.draw.line(self.screen, BLACK, ((0-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h),
                         ((self.map_width-start_x) * scale_ratio_w, (0-start_y) * scale_ratio_h), width=1)
        # render all balls
        for ball_id, ball in self.overlap[0].items():
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            pygame.draw.circle(self.screen, FOOD_COLOR, Vector2(x, y), r)
        for ball_id, ball in self.overlap[1].items():
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            pygame.draw.polygon(self.screen, THORNS_COLOR, to_aliased_circle(Vector2(x, y), r))
            # pygame.draw.circle(self.screen, THORNS_COLOR, Vector2(x, y), r)
        for ball_id, ball in self.overlap[2].items():
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            pygame.draw.circle(self.screen, SPORE_COLOR, Vector2(x, y), r)
        for ball_id, ball in self.overlap[3].items():
            x = (ball[0] - start_x) * scale_ratio_w
            y = (ball[1] - start_y) * scale_ratio_h
            r = ball[2] * scale_ratio_w
            direction = Vector2(ball[3], ball[4])
            player_id = int(ball[5])
            team_id = int(ball[6])
            pygame.draw.circle(self.screen, PLAYER_COLORS[team_id][0], Vector2(x, y), r)
            point_list = to_arrow(Vector2(x, y), r, direction)
            pygame.draw.polygon(self.screen, PLAYER_COLORS[team_id][0], point_list)
            font_size = int(r/1.6)
            font = pygame.font.SysFont('arial', max(font_size, 6), True)
            txt = font.render('{}'.format(chr(player_id%self.player_num_per_team+65)), True, WHITE)
            txt_rect = txt.get_rect(center=(x, y))
            self.screen.blit(txt, txt_rect)

    def render_leaderboard_colorful(self, leaderboard):
        start = 10
        team_score = sorted(leaderboard.items(), key=lambda d: d[1], reverse=True)
        for index, (team_id, score) in enumerate(team_score):
            start += 20
            font = pygame.font.SysFont('arial', 8, True)
            fps_txt = font.render('{} : {:.2f}'.format(team_id, score), True, PLAYER_COLORS[int(team_id)][0])
            self.screen.blit(fps_txt, (self.game_screen_width+5, start))
            # start += 20
            # font = pygame.font.SysFont('arial', 7, True)
            # for player_id, player_score in team_name_score[team_id].items():
            #     fps_txt = font.render('{} : {:.2f}'.format(chr(player_id%self.player_num_per_team+65), player_score), True, 
            #                           PLAYER_COLORS[team_id][0])
            #     self.screen.blit(fps_txt, (self.game_screen_width+5, start))
            #     start += 20

    def fill(self, rectangle=None):
        self.screen.fill(BACKGROUND)

        if rectangle is not None:
            left, top, right, bottom = rectangle
            width_real, height_real, hw_ratio = right-left, bottom-top, (right-left)/(bottom-top)
            scale_ratio_w = self.game_screen_width / width_real
            scale_ratio_h = self.game_screen_width / height_real
            start_x = left
            start_y = top
            self.render_rect_balls_colorful(scale_ratio_w=scale_ratio_w, scale_ratio_h=scale_ratio_h,
                                            start_x=start_x, start_y=start_y)
        else:
            scale_ratio_w = (self.game_screen_width-self.padding*2) / self.map_width
            scale_ratio_h = (self.game_screen_height-self.padding*2) / self.map_height
            start_x = 0
            start_y = 0
            self.render_all_balls_colorful(scale_ratio_w=scale_ratio_w, scale_ratio_h=scale_ratio_h)

        # for debug
        font = pygame.font.SysFont('Menlo', 15, True)

        assert len(self.leaderboard) > 0, 'leaderboard could not be None'
        self.render_leaderboard_colorful(self.leaderboard)

        self.speed_button.display(self.screen)
        self.play_button.display(self.screen)
        self.scrollbar.display(self.screen, self.rate)

    def show(self):
        self.fill()
        pygame.display.update()
        self.set_data()
        if self.if_play:
            self.frame_target = min(self.frame_now + self.speed, self.frame_total)
        self.rate = self.frame_now / self.frame_total

    def close(self):
        pygame.quit()

    def on_pressed(self, position):
        if self.play_button.check_click(position):
            self.if_play = self.play_button.on_pressed()
        elif self.speed_button.check_click(position):
            self.speed = self.speed_button.on_pressed()
        elif self.scrollbar.check_click(position):
            self.rate = self.scrollbar.on_pressed(position)
            self.frame_target = int(self.rate * self.frame_total)
