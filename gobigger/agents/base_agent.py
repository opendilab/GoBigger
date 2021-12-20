import os
import random
import logging


class BaseAgent:
    '''
    Overview:
        The base class of all agents
    '''
    def __init__(self):
        pass

    def step(self, obs):
        raise NotImplementedError

