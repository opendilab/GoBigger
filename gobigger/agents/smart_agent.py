import os
import random
import logging
import copy
import queue
from typing import List
from pygame.math import Vector2

from .base_agent import BaseAgent
import math

class SmartAgent(BaseAgent):
    '''
    Overview:
        A simple script bot
    '''
    def __init__(self, name=None):
        self.name = name
        self.actions_queue = queue.Queue()
        self.last_clone_num = 1
        self.last_total_size = 0
    

    def step(self,obs):

        '''
        1、clone ball 超过6个聚合
        2、eat
            1、比荆棘大，不管多少cloneball先聚合再吃荆棘
            2、比荆棘小
                    1、吃食物
        '''

        if self.actions_queue.qsize() > 0:
            return self.actions_queue.get()

        overlap = obs['overlap']
        overlap = self.preprocess(overlap)
        food_balls = overlap['food']
        thorns_balls = overlap['thorns']
        spore_balls = overlap['spore']
        clone_balls = overlap['clone']

        action_flag = False
        
        my_clone_balls, others_clone_balls = self.process_clone_balls(clone_balls)

        if len(my_clone_balls)>3:
            direction =  my_clone_balls[-1]['position']-my_clone_balls[0]['position']
            self.actions_queue.put([direction.x, direction.y, 2])
            #self.actions_queue.put([None, None, 0])
            action_flag = True
        
        ###
        if not action_flag:
            min_distance, min_thorns_ball = self.process_thorns_balls(thorns_balls, my_clone_balls[0])
            if min_thorns_ball:
                my_clone_balls, others_clone_balls = self.process_clone_balls(clone_balls)
                all_my_clone_balls_size = 0
                for i in range(len(my_clone_balls)):
                    all_my_clone_balls_size += my_clone_balls[i]['radius']*my_clone_balls[i]['radius']
                
                min_thorns_ball_size = min_thorns_ball['radius']*min_thorns_ball['radius']
                if all_my_clone_balls_size > min_thorns_ball_size:
                    direction = (min_thorns_ball['position'] - my_clone_balls[0]['position']).normalize()
                    self.actions_queue.put([direction.x, direction.y, 2])
                    # 延迟动作 使得可以吃荆棘
                    self.actions_queue.put([direction.x, direction.y, -1])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    action_flag = True
                else:
                    direction = (my_clone_balls[0]['position']-min_thorns_ball['position']).normalize()
                    min_distance, min_food_ball = self.process_food_balls(food_balls, my_clone_balls[0])
                    if min_food_ball:
                        direction = (min_food_ball['position'] - my_clone_balls[0]['position']).normalize()
                    else:
                        direction = Vector2(random.randint(-100,100),random.randint(-100,100))
                        if direction.x == 0: direction.x += 5
                        if direction.y == 0: direction.y += 5
                        direction = direction.normalize()
            else:
                min_distance, min_food_ball = self.process_food_balls(food_balls, my_clone_balls[0])
                if min_food_ball:
                    direction = (min_food_ball['position'] - my_clone_balls[0]['position']).normalize()
                    # quick eat， 分身+中吐
                    self.actions_queue.put([direction.x, direction.y, 1])
                    self.actions_queue.put([direction.x, direction.y, 1])
                    self.actions_queue.put([direction.x, direction.y, 2])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    self.actions_queue.put([direction.x, direction.y, -1])
                    #self.actions_queue.put([None, None, 0])
                    action_flag = True
                else:
                    direction = Vector2(random.randint(-100,100),random.randint(-100,100))
                    if direction.x == 0: direction.x += 5
                    if direction.y == 0: direction.y += 5
                    direction = direction.normalize()
        else:
            # action random
            # action_random = random.random()
            # if action_random < 0.02:
            #     action_type = 1
            # else:
            #     action_type = -1
            action_type = -1
            # direction random
            direction = Vector2(random.randint(-100,100),random.randint(-100,100))
            if direction.x == 0: direction.x += 5
            if direction.y == 0: direction.y += 5
            direction = direction.normalize()
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
    
    def add_noise_to_direction(self, direction, noise_ratio=0.1):
        direction = direction + Vector2(((random.random() * 2 - 1)*noise_ratio)*direction.x, ((random.random() * 2 - 1)*noise_ratio)*direction.y)
        return direction