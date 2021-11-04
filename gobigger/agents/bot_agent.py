import os
import random
import logging
import copy
import queue
from pygame.math import Vector2

from .base_agent import BaseAgent


level_para = {
    1 : 30,  # all weight = 19000
    2 : 20,  # all weight = 25000
    3 : 15,  # all weight = 32000
    4 : 10,  # all weight = 40000
    5 : 5,   # all weight = 60000
    6 : 1,   # all weight = 75000
}


class BotAgent(BaseAgent):
    '''
    Overview:
        A simple script bot
    '''
    def __init__(self, name=None, level=1):
        self.name = name
        self.actions_queue = queue.Queue()
        self.last_clone_num = 1
        self.last_total_size = 0
        self.noise_ratio = level_para[level]

    def step(self, obs):
        if self.actions_queue.qsize() > 0:
            return self.actions_queue.get()
        overlap = obs['overlap']
        overlap = self.preprocess(overlap)
        food_balls = overlap['food']
        thorns_balls = overlap['thorns']
        spore_balls = overlap['spore']
        clone_balls = overlap['clone']

        my_clone_balls, others_clone_balls = self.process_clone_balls(clone_balls)

        if len(my_clone_balls) >= 9 and my_clone_balls[4]['radius'] > 14:
            self.actions_queue.put([None, None, 2])
            self.actions_queue.put([None, None, -1])
            self.actions_queue.put([None, None, -1])
            self.actions_queue.put([None, None, -1])
            self.actions_queue.put([None, None, -1])
            self.actions_queue.put([None, None, -1])
            self.actions_queue.put([None, None, -1])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            self.actions_queue.put([None, None, 0])
            action_ret = self.actions_queue.get()
            return action_ret

        if len(others_clone_balls) > 0:
            if my_clone_balls[-1] > others_clone_balls[0]:
                direction = (others_clone_balls[-1]['position'] - my_clone_balls[-1]['position']).normalize()
            else:
                direction = (my_clone_balls[0]['position'] - others_clone_balls[0]['position']).normalize()
            action_type = -1
        else:
            min_distance, min_thorns_ball = self.process_thorns_balls(thorns_balls, my_clone_balls[0])
            if min_thorns_ball is not None:
                direction = (min_thorns_ball['position'] - my_clone_balls[0]['position']).normalize()
            else:
                min_distance, min_food_ball = self.process_food_balls(food_balls, my_clone_balls[0])
                if min_food_ball is not None:
                    direction = (min_food_ball['position'] - my_clone_balls[0]['position']).normalize()
                else:
                    direction = (Vector2(0, 0) - my_clone_balls[0]['position']).normalize()
            action_random = random.random()
            if action_random < 0.02:
                action_type = 1
            if action_random < 0.04 and action_random > 0.02:
                action_type = 2
            else:
                action_type = -1
        direction = self.add_noise_to_direction(direction)
        self.actions_queue.put([direction.x, direction.y, action_type])
        action_ret = self.actions_queue.get()
        return action_ret

    def process_clone_balls(self, clone_balls):
        my_clone_balls = []
        others_clone_balls = []
        for clone_ball in clone_balls:
            if clone_ball['player'] == self.name:
                my_clone_balls.append(copy.deepcopy(clone_ball))
        my_clone_balls.sort(key=lambda a: a['radius'], reverse=True)

        for clone_ball in clone_balls:
            if clone_ball['player'] != self.name:
                others_clone_balls.append(copy.deepcopy(clone_ball))
        others_clone_balls.sort(key=lambda a: a['radius'], reverse=True)
        return my_clone_balls, others_clone_balls

    def process_thorns_balls(self, thorns_balls, my_max_clone_ball):
        min_distance = 10000
        min_thorns_ball = None
        for thorns_ball in thorns_balls:
            if thorns_ball['radius'] < my_max_clone_ball['radius']:
                distance = (thorns_ball['position'] - my_max_clone_ball['position']).length()
                if distance < min_distance:
                    min_distance = distance
                    min_thorns_ball = copy.deepcopy(thorns_ball)
        return min_distance, min_thorns_ball

    def process_food_balls(self, food_balls, my_max_clone_ball):
        min_distance = 10000
        min_food_ball = None
        for food_ball in food_balls:
            distance = (food_ball['position'] - my_max_clone_ball['position']).length()
            if distance < min_distance:
                min_distance = distance
                min_food_ball = copy.deepcopy(food_ball)
        return min_distance, min_food_ball

    def preprocess(self, overlap):
        new_overlap = {}
        for k, v in overlap.items():
            new_overlap[k] = []
            for index, vv in enumerate(v):
                new_overlap[k].append(vv)
                new_overlap[k][index]['position'] = Vector2(*vv['position'])
        return new_overlap
    
    def add_noise_to_direction(self, direction):
        noise_ratio = self.noise_ratio
        direction = direction + Vector2(((random.random() * 2 - 1)*noise_ratio)*direction.x, ((random.random() * 2 - 1)*noise_ratio)*direction.y)
        return direction
