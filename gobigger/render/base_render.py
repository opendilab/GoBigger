import os
import pygame
import platform


class BaseRender:

    def __init__(self, width, height, padding=(0,0), cell_size=10, only_render=False):
        pygame.init()
        if platform.system() == 'Linux': # If the current system is linux, window is not used
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.width = width
        self.height = height
        self.padding = padding
        self.width_full = self.width + self.padding[0] * 2
        self.height_full = self.height + self.padding[1] * 2
        self.cell_size = cell_size
        self.FPS = 60 # Set the frame rate (the number of screen refreshes per second)
        self.fpsClock = pygame.time.Clock() 
        if not only_render:
            self.screen = pygame.display.set_mode((self.width_full, self.height_full),  0, 32)
            pygame.display.set_caption("GoBigger - Opendilab Challenge")

    def fill(self, server):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
