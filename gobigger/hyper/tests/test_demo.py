import pygame
import time
import logging

from gobigger.hyper import StraightMergeHyperAction, QuarterMergeHyperAction, EighthMergeHyperAction
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender


def demo_straight_merge():
    server = Server(dict(
        team_num=1, 
        player_num_per_team=2,
        map_width=600,
        map_height=600,
        match_time=60*1,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.start()
    render = RealtimeRender(server.map_width, server.map_height)
    server.set_render(render)
    server.player_manager.get_players()[0].get_balls()[0].set_size(420)
    server.player_manager.get_players()[1].get_balls()[0].set_size(100)
    player_name1 = server.player_manager.get_players()[0].name
    player_name2 = server.player_manager.get_players()[1].name
    sm_action = StraightMergeHyperAction(player_name1, player_name2)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for _ in range(100000):
        obs = server.obs()
        sm_action.update(obs[1][player_name1], obs[1][player_name2])
        action = sm_action.get()
        if server.last_time < server.match_time:
            for i in range(server.state_tick_per_action_tick):
                if i == 0:
                    server.step_state_tick(actions=action)
                else:
                    server.step_state_tick()
                render.fill(server, direction=None, fps=fps_real, last_time=server.last_time,
                            player_num_per_team=server.player_num_per_team)
                render.show()
                if i % server.state_tick_per_second == 0:
                    t2 = time.time()
                    fps_real = server.state_tick_per_second/(t2-t1)
                    t1 = time.time()
                clock.tick(fps_set)
        else:
            logging.debug('Game Over')
            break
    render.close()


def demo_quarter_merge():
    server = Server(dict(
        team_num=1, 
        player_num_per_team=2,
        map_width=600,
        map_height=600,
        match_time=60*1,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.start()
    render = RealtimeRender(server.map_width, server.map_height)
    server.set_render(render)
    server.player_manager.get_players()[0].get_balls()[0].set_size(420)
    server.player_manager.get_players()[1].get_balls()[0].set_size(100)
    player_name1 = server.player_manager.get_players()[0].name
    player_name2 = server.player_manager.get_players()[1].name
    sm_action = QuarterMergeHyperAction(player_name1, player_name2)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for _ in range(100000):
        obs = server.obs()
        sm_action.update(obs[1][player_name1], obs[1][player_name2])
        action = sm_action.get()
        print(action)
        if server.last_time < server.match_time:
            for i in range(server.state_tick_per_action_tick):
                if i == 0:
                    server.step_state_tick(actions=action)
                else:
                    server.step_state_tick()
                render.fill(server, direction=None, fps=fps_real, last_time=server.last_time,
                            player_num_per_team=server.player_num_per_team)
                render.show()
                if i % server.state_tick_per_second == 0:
                    t2 = time.time()
                    fps_real = server.state_tick_per_second/(t2-t1)
                    t1 = time.time()
                clock.tick(fps_set)
        else:
            logging.debug('Game Over')
            break
    render.close()


def demo_eighth_merge():
    server = Server(dict(
        team_num=1, 
        player_num_per_team=2,
        map_width=600,
        map_height=600,
        match_time=60*1,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.start()
    render = RealtimeRender(server.map_width, server.map_height)
    server.set_render(render)
    server.player_manager.get_players()[0].get_balls()[0].set_size(820)
    server.player_manager.get_players()[1].get_balls()[0].set_size(100)
    player_name1 = server.player_manager.get_players()[0].name
    player_name2 = server.player_manager.get_players()[1].name
    sm_action = EighthMergeHyperAction(player_name1, player_name2)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for _ in range(100000):
        obs = server.obs()
        sm_action.update(obs[1][player_name1], obs[1][player_name2])
        action = sm_action.get()
        print(action)
        if server.last_time < server.match_time:
            for i in range(server.state_tick_per_action_tick):
                if i == 0:
                    server.step_state_tick(actions=action)
                else:
                    server.step_state_tick()
                render.fill(server, direction=None, fps=fps_real, last_time=server.last_time,
                            player_num_per_team=server.player_num_per_team)
                render.show()
                if i % server.state_tick_per_second == 0:
                    t2 = time.time()
                    fps_real = server.state_tick_per_second/(t2-t1)
                    t1 = time.time()
                clock.tick(fps_set)
        else:
            logging.debug('Game Over')
            break
    render.close()


if __name__ == '__main__':
    # demo_straight_merge()
    # demo_quarter_merge()
    demo_eighth_merge()

