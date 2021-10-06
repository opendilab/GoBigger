import os
import random
import logging
import copy
import queue
from pygame.math import Vector2

from .base_agent import BaseAgent


class BotAgent(BaseAgent):
    '''
    Overview:
        A simple script bot
    '''
    def __init__(self, name=None):
        self.name = name
        self.actions_queue = queue.Queue()
        self.last_clone_num = 1
        self.last_total_size = 0

    def step(self, obs):
        if self.actions_queue.qsize() > 0:
            return self.actions_queue.get()

        overlap = obs['overlap']
        overlap = self.preprocess(overlap)

        food_balls = overlap['food']
        thorns_balls = overlap['thorns']
        spore_balls = overlap['spore']
        clone_balls = overlap['clone']

        max_radius, max_position, my_clone_balls, total_size = self.get_my_max_clone_ball(clone_balls)
        others_clone_balls, min_others_clone_ball, min_distance = self.get_others_clone_balls(clone_balls, max_position)

        if len(others_clone_balls) > 0:
            if max_radius > min_others_clone_ball['radius']:
                direction = (min_others_clone_ball['position'] - max_position).normalize()
                direction = self.add_noise_to_direction(direction)
                action_type = -1
                self.actions_queue.put([direction.x, direction.y, action_type])
            else:
                direction = ((min_others_clone_ball['position'] - max_position) * -1).normalize()
                direction = self.add_noise_to_direction(direction)
                action_type = -1
                self.actions_queue.put([direction.x, direction.y, action_type])
        elif len(thorns_balls) > 0:
            max_distance, max_thorns_ball = self.get_remote_thorns_ball(thorns_balls, max_position)
            if len(my_clone_balls) > 14 and max_radius > max_thorns_ball['radius']:
                direction = (max_thorns_ball['position'] - max_position).normalize()
                direction = self.add_noise_to_direction(direction)
                action_type = -1
                self.actions_queue.put([direction.x, direction.y, action_type])
            if max_radius > max_thorns_ball['radius'] and len(others_clone_balls) == 0:
                direction = (max_thorns_ball['position'] - max_position).normalize()
                direction = self.add_noise_to_direction(direction)
                action_type = -1
                self.actions_queue.put([direction.x, direction.y, action_type])
            else:
                min_distance, min_food_ball = self.get_close_food_ball(food_balls, max_position)
                direction = (min_food_ball['position'] - max_position).normalize()
                direction = self.add_noise_to_direction(direction)
                action_type = -1
                self.actions_queue.put([direction.x, direction.y, action_type])
        else:
            min_distance, min_food_ball = self.get_close_food_ball(food_balls, max_position)
            direction = (min_food_ball['position'] - max_position).normalize()
            direction = self.add_noise_to_direction(direction)
            action_type = -1
            self.actions_queue.put([direction.x, direction.y, action_type])
        if random.random() < 0.1:
            self.actions_queue.put([direction.x, direction.y, 1])
        if random.random() < 0.05:
            self.actions_queue.put([direction.x, direction.y, 2])
        self.last_clone_num = len(my_clone_balls)
        action_ret = self.actions_queue.get()
        return action_ret

    def preprocess(self, overlap):
        new_overlap = {}
        for k, v in overlap.items():
            new_overlap[k] = []
            for index, vv in enumerate(v):
                new_overlap[k].append(vv)
                new_overlap[k][index]['position'] = Vector2(*vv['position'])
        return new_overlap

    def get_my_max_clone_ball(self, clone_balls):
        '''
        Overview:
            Get the radius and corresponding position in the ball with the largest radius of the control
        '''
        max_radius = -1
        max_position = -1
        my_clone_balls = []
        total_size = 0
        for clone_ball in clone_balls:
            if clone_ball['player'] == self.name:
                my_clone_balls.append(copy.deepcopy(clone_ball))
                total_size += clone_ball['radius'] ** 2
                if clone_ball['radius'] > max_radius:
                    max_radius = clone_ball['radius']
                    max_position = clone_ball['position']
        return max_radius, max_position, my_clone_balls, total_size

    def get_my_clone_ball_num(self, clone_balls):
        count = 0
        for clone_ball in clone_balls:
            if clone_ball['player'] == self.name:
                count += 1
        return count

    def get_remote_thorns_ball(self, thorns_balls, max_position):
        max_distance = 0
        max_thorns_ball = None
        for thorns_ball in thorns_balls:
            distance = (thorns_ball['position'] - max_position).length()
            if distance > max_distance:
                max_distance = distance
                max_thorns_ball = copy.deepcopy(thorns_ball)
        return max_distance, max_thorns_ball

    def get_others_clone_balls(self, clone_balls, max_position):
        others_clone_balls = []
        min_distance = 10000
        min_others_clone_ball = None
        for clone_ball in clone_balls:
            if clone_ball['player'] != self.name:
                others_clone_balls.append(copy.deepcopy(clone_ball))
                distance = (clone_ball['position'] - max_position).length()
                if distance < min_distance:
                    min_distance = distance
                    min_others_clone_ball = copy.deepcopy(clone_ball)
        return others_clone_balls, min_others_clone_ball, min_distance

    def get_close_food_ball(self, food_balls, max_position):
        min_distance = 10000
        min_food_ball = None
        for food_ball in food_balls:
            distance = (food_ball['position'] - max_position).length()
            if distance < min_distance:
                min_distance = distance
                min_food_ball = copy.deepcopy(food_ball)
        if min_food_ball is None:
            min_food_ball = {'position': Vector2(0,0)}
        return min_distance, min_food_ball
    
    def add_noise_to_direction(self, direction, noise_ratio=0.1):
        direction = direction + Vector2(((random.random() * 2 - 1)*noise_ratio)*direction.x, ((random.random() * 2 - 1)*noise_ratio)*direction.y)
        return direction
