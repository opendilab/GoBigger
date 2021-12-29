import os
import sys
import time
import pygame
from pygame.math import Vector2
import random
import queue
import math
from easydict import EasyDict

from gobigger.server import Server
from gobigger.render import EnvRender, RealtimeRender


class HyperAction:
    def __init__(self):
        raise NotImplementedError
    def update(self, obs):
        raise NotImplementedError
    def get(self):
        raise NotImplementedError


class StraightMergeHyperAction(HyperAction):

    #########################################################
    #                        直线中合                        #
    #########################################################

    def __init__(self, player_name1, player_name2):
        self.player_name1 = player_name1
        self.player_name2 = player_name2
        self.state = "reach" # in ['reach', 'merge']
        self.need_stop = 0

    def update(self, obs1, obs2):
        self.balls1 = self.get_balls_from_obs_by_name(self.player_name1, obs1)
        self.balls2 = self.get_balls_from_obs_by_name(self.player_name2, obs2)

    def get(self):
        if self.state == 'reach':
            tmp = self.straight_merge_reach()
            if tmp is not None:
                return tmp
        if self.state == 'action':
            return self.straight_merge_action()

    def get_balls_from_obs_by_name(self, player_name, obs):
        balls = []
        overlap = obs['overlap']
        for item in overlap['clone']:
            if str(int(item[3])) == player_name:
                ball = EasyDict()
                ball.position = Vector2(float(item[0]), float(item[1]))
                ball.radius = float(item[2])
                ball.player = str(int(item[3]))
                ball.team = str(int(item[4]))
                balls.append(ball)
        return balls

    def straight_merge_reach(self):
        """
        移动到相近位置（相切）
        """
        ball1 = self.balls1[0]
        ball2 = self.balls2[0]
        if len(self.balls1) == 1 and len(self.balls2) == 1 and \
            (ball1.position - ball2.position).length() <= 1.5 * (ball1.radius + ball2.radius):
            self.state = 'action'
            return None
        if len(self.balls1) != 1:
            action1 = [None, None, 2]
        else:
            direction1 = ball2.position - ball1.position
            action1 = [direction1.x, direction1.y, -1]
        if len(self.balls2) != 1:
            action2 = [None, None, 2]
        else:
            direction2 = ball1.position - ball2.position
            action2 = [direction2.x, direction2.y, -1]
        actions = {
            str(ball1.player): action1,
            str(ball2.player): action2,
        }
        return actions

    def straight_merge_action(self):
        """
        直线中合
        balls1是较大的球，balls2是较小的球
        条件：1. 同队友都只有一个球。
        """
        ret = {}
        ball1 = self.balls1[0]
        ball2 = self.balls2[0]
        if self.need_stop > 0:
            self.need_stop -= 1
            return {
                ball1.player: [None, None, 2],
                ball2.player: [None, None, 2],
            }
        size1 = ball1.radius ** 2
        size2 = ball2.radius ** 2
        split_size_min = 100
        if len(self.balls1) == 1:
            tmp = ball2.position - ball1.position
            direction = [tmp.x, tmp.y]
        else:
            direction = [None, None]
        if size1 > split_size_min:
            ret[ball1.player] = [*direction, 1] # split
            ret[ball2.player] = [None, None, 2] # stop
            self.need_stop = 5
        else:
            ret = None
        return ret


class QuarterMergeHyperAction(HyperAction):

    #########################################################
    #                        四分中合                        #
    #########################################################

    def __init__(self, player_name1, player_name2):
        self.player_name1 = player_name1
        self.player_name2 = player_name2
        self.state = "reach" # in ['reach', 'merge']
        self.need_stop = 0
        self.split_count = 0

    def update(self, obs1, obs2):
        self.balls1 = self.get_balls_from_obs_by_name(self.player_name1, obs1)
        self.balls2 = self.get_balls_from_obs_by_name(self.player_name2, obs2)

    def get(self):
        if self.state == 'reach':
            tmp = self.quarter_merge_reach()
            if tmp is not None:
                return tmp
        if self.state == 'action':
            return self.quarter_merge_action()

    def get_balls_from_obs_by_name(self, player_name, obs):
        balls = []
        overlap = obs['overlap']
        for item in overlap['clone']:
            if str(int(item[3])) == player_name:
                ball = EasyDict()
                ball.position = Vector2(float(item[0]), float(item[1]))
                ball.radius = float(item[2])
                ball.player = str(int(item[3]))
                ball.team = str(int(item[4]))
                balls.append(ball)
        return balls

    def quarter_merge_reach(self):
        """
        移动到相近位置（相切）
        """
        ball1 = self.balls1[0]
        ball2 = self.balls2[0]
        if len(self.balls1) == 1 and len(self.balls2) == 1 and \
            (ball1.position - ball2.position).length() <= 1.5 * (ball1.radius + ball2.radius):
            self.state = 'action'
            return None
        if len(self.balls1) != 1:
            action1 = [None, None, 2]
        else:
            direction1 = ball2.position - ball1.position
            action1 = [direction1.x, direction1.y, -1]
        if len(self.balls2) != 1:
            action2 = [None, None, 2]
        else:
            direction2 = ball1.position - ball2.position
            action2 = [direction2.x, direction2.y, -1]
        actions = {
            str(ball1.player): action1,
            str(ball2.player): action2,
        }
        return actions

    def quarter_merge_action(self):
        """
        直线中合
        balls1是较大的球，balls2是较小的球
        条件：1. 同队友都只有一个球。
        """
        def cal_centroid(balls):
            '''
            Overview:
                Calculate the centroid
            '''
            x = 0
            y = 0
            total_size = 0
            for ball in balls:
                x += ball.radius ** 2 * ball.position.x
                y += ball.radius ** 2 * ball.position.y
                total_size += ball.radius ** 2
            return Vector2(x, y) / total_size

        ret = {}
        ball1 = self.balls1[0]
        ball2 = self.balls2[0]
        if self.need_stop > 0:
            self.need_stop -= 1
            return {
                ball1.player: [None, None, 2],
                ball2.player: [None, None, 2],
            }
        size1 = ball1.radius ** 2
        size2 = ball2.radius ** 2
        split_size_min = 100
        centroid = cal_centroid(self.balls1)
        if len(self.balls1) == 1 or self.split_count == 0:
            tmp = ball2.position - ball1.position
            tmp = Vector2(tmp.x * math.cos(math.pi/4) - tmp.y * math.sin(math.pi/4),
                          tmp.x * math.sin(math.pi/4) + tmp.y * math.cos(math.pi/4))
            direction = [tmp.x, tmp.y]
            self.split_count += 1
        elif self.split_count == 1:
            tmp = ball2.position - centroid
            direction = [tmp.x, tmp.y]
            self.split_count += 1
        else:
            direction = [None, None]
            self.split_count += 1
        if size1 > split_size_min:
            ret[ball1.player] = [*direction, 1] # split
            tmp = centroid - ball2.position
            ret[ball2.player] = [tmp.x, tmp.y, 2] # stop
            self.need_stop = 5
        else:
            ret = None
        return ret


class EighthMergeHyperAction(HyperAction):

    #########################################################
    #                        四分中合                        #
    #########################################################

    def __init__(self, player_name1, player_name2):
        self.player_name1 = player_name1
        self.player_name2 = player_name2
        self.state = "reach" # in ['reach', 'merge']
        self.need_stop = 0
        self.split_count = 0

    def update(self, obs1, obs2):
        self.balls1 = self.get_balls_from_obs_by_name(self.player_name1, obs1)
        self.balls2 = self.get_balls_from_obs_by_name(self.player_name2, obs2)

    def get(self):
        if self.state == 'reach':
            tmp = self.quarter_merge_reach()
            if tmp is not None:
                return tmp
        if self.state == 'action':
            return self.quarter_merge_action()

    def get_balls_from_obs_by_name(self, player_name, obs):
        balls = []
        overlap = obs['overlap']
        for item in overlap['clone']:
            if str(int(item[3])) == player_name:
                ball = EasyDict()
                ball.position = Vector2(float(item[0]), float(item[1]))
                ball.radius = float(item[2])
                ball.player = str(int(item[3]))
                ball.team = str(int(item[4]))
                balls.append(ball)
        return balls

    def quarter_merge_reach(self):
        """
        移动到相近位置（相切）
        """
        ball1 = self.balls1[0]
        ball2 = self.balls2[0]
        if len(self.balls1) == 1 and len(self.balls2) == 1 and \
            (ball1.position - ball2.position).length() <= 1.5 * (ball1.radius + ball2.radius):
            self.state = 'action'
            return None
        if len(self.balls1) != 1:
            action1 = [None, None, 2]
        else:
            direction1 = ball2.position - ball1.position
            action1 = [direction1.x, direction1.y, -1]
        if len(self.balls2) != 1:
            action2 = [None, None, 2]
        else:
            direction2 = ball1.position - ball2.position
            action2 = [direction2.x, direction2.y, -1]
        actions = {
            str(ball1.player): action1,
            str(ball2.player): action2,
        }
        return actions

    def quarter_merge_action(self):
        """
        直线中合
        balls1是较大的球，balls2是较小的球
        条件：1. 同队友都只有一个球。
        """
        def cal_centroid(balls):
            '''
            Overview:
                Calculate the centroid
            '''
            x = 0
            y = 0
            total_size = 0
            for ball in balls:
                x += ball.radius ** 2 * ball.position.x
                y += ball.radius ** 2 * ball.position.y
                total_size += ball.radius ** 2
            return Vector2(x, y) / total_size

        ret = {}
        ball1 = self.balls1[0]
        ball2 = self.balls2[0]
        if self.need_stop > 0:
            self.need_stop -= 1
            return {
                ball1.player: [None, None, 2],
                ball2.player: [None, None, 2],
            }
        size1 = ball1.radius ** 2
        size2 = ball2.radius ** 2
        split_size_min = 100
        centroid = cal_centroid(self.balls1)
        if len(self.balls1) == 1 or self.split_count == 0:
            tmp = ball2.position - ball1.position
            tmp = Vector2(tmp.x * math.cos(math.pi/4) - tmp.y * math.sin(math.pi/4),
                          tmp.x * math.sin(math.pi/4) + tmp.y * math.cos(math.pi/4))
            direction = [tmp.x, tmp.y]
            self.split_count += 1
        elif self.split_count == 1:
            tmp = ball2.position - centroid
            direction = [tmp.x, tmp.y]
            self.split_count += 1
        else:
            direction = [None, None]
            self.split_count += 1
        if size1 > split_size_min:
            ret[ball1.player] = [*direction, 1] # split
            tmp = centroid - ball2.position
            ret[ball2.player] = [tmp.x, tmp.y, 2] # stop
            self.need_stop = 5
        else:
            tmp = ball2.position - centroid
            ret = {
                ball1.player: [tmp.x, tmp.y, -1],
                ball2.player: [None, None, 2],
            }
        return ret


