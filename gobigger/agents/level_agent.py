
from .bot_agent import BotAgent
from pygame.math import Vector2
import random

level_para = {
    1 : 30,  # all weight = 19000
    2 : 20,  # all weight = 25000
    3 : 15,  # all weight = 32000
    4 : 10,  # all weight = 40000
    5 : 5,   # all weight = 60000
    6 : 1,   # all weight = 75000
}

class LevelBotAgent(BotAgent):

    def __init__(self,name,level) -> None:
        super(LevelBotAgent,self).__init__(name)
        self.name = name
        self.noise_ratio = level_para[level]
    
    def add_noise_to_direction(self, direction):
        noise_ratio = self.noise_ratio
        print(noise_ratio)
        direction = direction + Vector2(((random.random() * 2 - 1)*noise_ratio)*direction.x, ((random.random() * 2 - 1)*noise_ratio)*direction.y)
        return direction
    





