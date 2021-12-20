import logging
from pygame.math import Vector2
import pygame
import argparse
import time

from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender
from gobigger.agents import BotAgent

logging.basicConfig(level=logging.DEBUG)


def play_control_by_keyboard():
    server = Server(dict(
        team_num=1,
        player_num_per_team=1,
        match_time=60*10,
        map_width=600,
        map_height=600,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.reset()
    render = RealtimeRender(server.map_width, server.map_height)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for i in range(100000):
        clock.tick(1000)
        x, y = 0.0, 0.0
        action_type = -1
        actions = {player: [x, y, action_type] for player in server.get_player_names()}
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x, y = 0, -1
                    action_type = -1
                elif event.key == pygame.K_DOWN:
                    x, y = 0, 1
                    action_type = -1
                elif event.key == pygame.K_LEFT:
                    x, y = -1, 0
                    action_type = -1
                elif event.key == pygame.K_RIGHT:
                    x, y = 1, 0
                    action_type = -1
                elif event.key == pygame.K_q: # Spores
                    x, y = 0.0, 0.0
                    action_type = 0
                elif event.key == pygame.K_w: # Splite
                    x, y = 0.0, 0.0
                    action_type = 1
                elif event.key == pygame.K_e: # Stop moving
                    x, y = 0.0, 0.0
                    action_type = 2
                elif event.key == pygame.K_r: # Cheating, adding weight
                    x, y = 0.0, 0.0
                    action_type = -1
                actions = {player: [x, y, action_type] for player in server.get_player_names()}
        if server.get_last_time() < server.match_time:
            print(actions)
            server.step_state_tick(actions=actions)
            if actions is not None and x is not None and y is not None:
                render.fill(server.obs(), direction=Vector2(x, y), fps=fps_real, last_time=server.get_last_time())
            else:
                render.fill(server.obs(), direction=None, fps=fps_real, last_time=server.get_last_time())
            render.show()
            if i % server.state_tick_per_second == 0:
                t2 = time.time()
                fps_real = server.state_tick_per_second/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


def play_control_by_keyboard_multi_player():
    server = Server(dict(
        team_num=2,
        player_num_per_team=1,
        match_time=60*10,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.reset()
    render = RealtimeRender(server.map_width, server.map_height)
    player_names = [player.name for player in server.player_manager.get_players()]
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for i in range(100000):
        actions = None
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                x1, y1, x2, y2 = None, None, None, None
                action_type1 = -1
                action_type2 = -1
                if event.key == pygame.K_UP:
                    x1, y1 = 0, -1
                if event.key == pygame.K_DOWN:
                    x1, y1 = 0, 1
                if event.key == pygame.K_LEFT:
                    x1, y1 = -1, 0
                if event.key == pygame.K_RIGHT:
                    x1, y1 = 1, 0
                if event.key == pygame.K_LEFTBRACKET: # Spores
                    action_type1 = 0
                if event.key == pygame.K_RIGHTBRACKET: # Splite
                    action_type1 = 1
                if event.key == pygame.K_BACKSLASH: # Stop moving
                    action_type1 = 2
                if event.key == pygame.K_w:
                    x2, y2 = 0, -1
                if event.key == pygame.K_s:
                    x2, y2 = 0, 1
                if event.key == pygame.K_a:
                    x2, y2 = -1, 0
                if event.key == pygame.K_d:
                    x2, y2 = 1, 0
                if event.key == pygame.K_1: # Spores
                    action_type2 = 0
                if event.key == pygame.K_2: # Splite
                    action_type2 = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type2 = 2
                actions = {
                    player_names[0]: [x1, y1, action_type1],
                    player_names[1]: [x2, y2, action_type2],
                }
        if server.last_time < server.match_time:
            server.step_state_tick(actions=actions)
            if actions is not None and x1 is not None and y1 is not None:
                render.fill(server, direction=Vector2(x1, y1), fps=fps_real, last_time=server.last_time)
            else:
                render.fill(server, direction=None, fps=fps_real, last_time=server.last_time)
            render.show()
            if i % server.state_tick_per_second == 0:
                t2 = time.time()
                fps_real = server.state_tick_per_second/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


def play_control_by_keyboard_partial():
    '''
    Keyboard control + partly visible
    '''
    server = Server(dict(
        team_num=1,
        player_num_per_team=1,
        match_time=60*10,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.reset()
    render = RealtimePartialRender(server.map_width, server.map_height)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for i in range(100000):
        actions = None
        x, y = None, None
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x, y = 0, -1
                    action_type = -1
                elif event.key == pygame.K_DOWN:
                    x, y = 0, 1
                    action_type = -1
                elif event.key == pygame.K_LEFT:
                    x, y = -1, 0
                    action_type = -1
                elif event.key == pygame.K_RIGHT:
                    x, y = 1, 0
                    action_type = -1
                elif event.key == pygame.K_q: # Spore
                    x, y = None, None
                    action_type = 0
                elif event.key == pygame.K_w: # Splite
                    x, y = None, None
                    action_type = 1
                elif event.key == pygame.K_e: # stop moving
                    x, y = None, None
                    action_type = 2
                elif event.key == pygame.K_r: # cheating
                    x, y = None, None
                    action_type = -1
                    server.player_manager.get_players()[0].get_balls()[0].set_size(144)
                actions = {player.name: [x, y, action_type] for player in server.player_manager.get_players()}

        if server.last_time < server.match_time:
            server.step_state_tick(actions=actions)
            if actions is not None and x is not None and y is not None:
                render.fill(server, direction=Vector2(x, y), fps=fps_real, last_time=server.last_time)
            else:
                render.fill(server, direction=None, fps=fps_real, last_time=server.last_time)
            render.show()
            if i % server.state_tick_per_second == 0:
                t2 = time.time()
                fps_real = server.state_tick_per_second/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


def play_control_by_keyboard_vs_bot(team_num=2):
    server = Server(dict(
        map_width=600,
        map_height=600,
        team_num=team_num,
        player_num_per_team=1,
        match_time=60*10,
        save_video=False,
        state_tick_per_second=20, # frame
        action_tick_per_second=5, # frame
    ))
    server.reset()
    render = RealtimeRender(server.map_width, server.map_height)
    server.set_render(render)
    human_team_name = '0'
    human_team_player_name = []
    bot_agents = []
    for player_name in server.get_player_names():
        if player_name != human_team_name:
            bot_agents.append(BotAgent(player_name, level=3))
        else:
            human_team_player_name.append(player_name)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = server.state_tick_per_second
    for i in range(100000):
        _, obs, obs_raw = server.obs(with_raw=True)
        x, y = 0.0, 0.0
        action_type = -1
        actions_bot = {bot_agent.name: bot_agent.step(obs[bot_agent.name]) for bot_agent in bot_agents}
        actions = {player: [x, y, action_type] for player in server.get_player_names()}
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x, y = 0, -1
                    action_type = -1
                elif event.key == pygame.K_DOWN:
                    x, y = 0, 1
                    action_type = -1
                elif event.key == pygame.K_LEFT:
                    x, y = -1, 0
                    action_type = -1
                elif event.key == pygame.K_RIGHT:
                    x, y = 1, 0
                    action_type = -1
                elif event.key == pygame.K_q: # Spores
                    x, y = 0.0, 0.0
                    action_type = 0
                elif event.key == pygame.K_w: # Splite
                    x, y = 0.0, 0.0
                    action_type = 1
                elif event.key == pygame.K_e: # Stop moving
                    x, y = 0.0, 0.0
                    action_type = 2
                elif event.key == pygame.K_r: # Cheating, adding weight
                    x, y = 0.0, 0.0
                    action_type = -1
                actions = {player_name: [x, y, action_type] for player_name in human_team_player_name}
        if server.get_last_time() < server.match_time:
            actions.update(actions_bot)
            server.step_state_tick(actions=server.format_actions(actions))
            food_balls, thorns_balls, spore_balls, clone_balls, _ = server.transform_obs_to_balls_and_rects(obs_raw)
            if actions is not None and x is not None and y is not None:
                render.fill(food_balls, thorns_balls, spore_balls, clone_balls,
                            direction=Vector2(x, y), fps=fps_real, last_time=server.get_last_time())
            else:
                render.fill(food_balls, thorns_balls, spore_balls, clone_balls,
                            direction=None, fps=fps_real, last_time=server.get_last_time())
            render.show()
            if i % server.state_tick_per_second == 0:
                t2 = time.time()
                fps_real = server.state_tick_per_second/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--player-num', type=int, choices=[1,2], default=1)
    parser.add_argument('--vision-type', type=str, choices=['full', 'partial'], default='full')
    parser.add_argument('--vs-bot', action='store_true', help='vs bot')
    parser.add_argument('--team-num', type=int, default=2)
    args = parser.parse_args()

    if args.vs_bot:
        play_control_by_keyboard_vs_bot(team_num=args.team_num)
    elif args.player_num == 1 and args.vision_type == 'full':
        play_control_by_keyboard()
    elif args.player_num == 1 and args.vision_type == 'partial':
        play_control_by_keyboard_partial()
    elif args.player_num == 2 and args.vision_type == 'full':
        play_control_by_keyboard_multi_player()
    else:
        logging.error('Not supoort when player_num = {} and vision_type = {}'.format(args.player_num, args.vision_type))
