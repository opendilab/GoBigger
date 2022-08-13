import time
import pygame
import logging
import pickle
import lz4.frame

from gobigger.render import PBRender, TkSelect
from gobigger.envs import GoBiggerEnv, create_env
from gobigger.agents import BotAgent

logging.basicConfig(level=logging.DEBUG)


def read_pb(pb_path):
    with open(pb_path, 'rb') as f:
        pb_data = pickle.load(f)
    pb_data = pickle.loads(lz4.frame.decompress(pb_data))
    return pb_data


def play():
    select = TkSelect()
    if not hasattr(select, 'pb_path'):
        return
    pb_path = select.pb_path
    pb_data = read_pb(pb_path)
    clock = pygame.time.Clock()
    fps_set = 20
    pb_render = PBRender(pb_data=pb_data)
    while True:
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
        if mouse_pos is not None:
            pb_render.on_pressed(mouse_pos)
        pb_render.show()
        clock.tick(fps_set)


if __name__ == '__main__':
    play()
