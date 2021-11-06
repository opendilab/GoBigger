import os
import random
import logging
import copy
import queue
from pygame.math import Vector2
from .bot_agent import BotAgent
from .base_agent import BaseAgent


class LowAgent(BotAgent):
    def __init__(self,name) -> None:
        super(LowAgent,self).__init__(name)
        self.name = name
        self.actions_queue = queue.Queue()
        self.last_clone_num = 1
        self.last_total_size = 0

    def step(self,obs):
        if self.actions_queue.qsize() > 0:
            return self.actions_queue.get()
        overlap = obs['overlap']
        overlap = self.preprocess(overlap)
        food_balls = overlap['food']
        thorns_balls = overlap['thorns']
        spore_balls = overlap['spore']
        clone_balls = overlap['clone']

        my_clone_balls, others_clone_balls = self.process_clone_balls(clone_balls)
        min_distance, min_food_ball = self.process_food_balls(food_balls, my_clone_balls[0])
        direction = (min_food_ball['position'] - my_clone_balls[0]['position']).normalize()
        action_type = -1
        self.actions_queue.put([direction.x, direction.y, action_type])
        action_ret = self.actions_queue.get()
        return action_ret

class MidAgent(BotAgent):
    def __init__(self,name) -> None:
        super(MidAgent,self).__init__(name)
        self.name = name
        self.actions_queue = queue.Queue()
        self.last_clone_num = 1
        self.last_total_size = 0

    def step(self,obs):
        if self.actions_queue.qsize() > 0:
            return self.actions_queue.get()
        overlap = obs['overlap']
        overlap = self.preprocess(overlap)
        food_balls = overlap['food']
        thorns_balls = overlap['thorns']
        spore_balls = overlap['spore']
        clone_balls = overlap['clone']

        my_clone_balls, others_clone_balls = self.process_clone_balls(clone_balls)
        min_distance, min_thorns_ball = self.process_thorns_balls(thorns_balls, my_clone_balls[0])
        if min_thorns_ball is not None:
            direction = (min_thorns_ball['position'] - my_clone_balls[0]['position']).normalize()
        else:
            direction = (Vector2(0, 0) - my_clone_balls[0]['position']).normalize()
        action_type = -1
        self.actions_queue.put([direction.x, direction.y, action_type])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        self.actions_queue.put([None, None, -1])
        action_ret = self.actions_queue.get()
        return action_ret