import os
import pygame
import platform


class BaseRender:

    def __init__(self, game_screen_width, game_screen_height, info_width=0, info_height=0, with_show=False):
        pygame.init()
        if platform.system() == 'Linux': # If the current system is linux, window is not used
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.game_screen_width = game_screen_width
        self.game_screen_height = game_screen_height
        self.total_screen_width = game_screen_width + info_width
        self.total_screen_height = game_screen_height + info_height
        # self.FPS = 60 # Set the frame rate (the number of screen refreshes per second)
        # self.fpsClock = pygame.time.Clock() 
        if with_show:
            self.screen = pygame.display.set_mode((self.total_screen_width, self.total_screen_height),  0, 32)
            pygame.display.set_caption("GoBigger - OpenDILab Environment")

    def fill(self, server):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
