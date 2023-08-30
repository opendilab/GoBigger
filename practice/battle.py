import logging
import pygame
import argparse
import time

from gobigger.agents import BotAgent
from gobigger.envs import GoBiggerEnv
from gobigger.render import RealtimeRender

logging.basicConfig(level=logging.DEBUG)

cfg = dict(
        team_num=2,
        player_num_per_team=2,
        direction_num=12,
        step_mul=8,
        map_width=64,
        map_height=64,
        frame_limit=3600,
        action_space_size=27,
        use_action_mask=False,
        reward_div_value=0.1,
        reward_type='log_reward',
        contain_raw_obs=True,  # False on collect mode, True on eval vsbot mode, because bot need raw obs
        start_spirit_progress=0.2,
        end_spirit_progress=0.8,
        manager_settings=dict(
            food_manager=dict(
                num_init=260,
                num_min=260,
                num_max=300,
            ),
            thorns_manager=dict(
                num_init=3,
                num_min=3,
                num_max=4,
            ),
            player_manager=dict(ball_settings=dict(score_init=13000, ), ),
        ),
        playback_settings=dict(
            playback_type='by_frame',
            by_frame=dict(
                save_frame=False,  # when training should set as False
                save_dir='./',
                save_name_prefix='gobigger',
            ),
        ),
    )

def play_farm_single(step):
    cfg['player_num_per_team'] = 1
    cfg['team_num'] = 1
    cfg['frame_limit'] = step
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    my_player_id = 0
    bot_agents = []
    for player in env.server.player_manager.get_players():
        if player.player_id != my_player_id:
            bot_agents.append(BotAgent(player.player_id))
    for i in range(100000):
        actions = None
        x1, y1 = None, None
        action_type = 0
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                action_type = -1
                action_type = -1
                if event.key == pygame.K_UP:
                    x1, y1 = 0, -1
                if event.key == pygame.K_DOWN:
                    x1, y1 = 0, 1
                if event.key == pygame.K_LEFT:
                    x1, y1 = -1, 0
                if event.key == pygame.K_RIGHT:
                    x1, y1 = 1, 0
                if event.key == pygame.K_1: # Spores
                    action_type = 0
                if event.key == pygame.K_2: # Splite
                    action_type = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type = 2
        actions = {my_player_id: [x1, y1, action_type]}
        actions.update({agent.name: agent.step(obs[1][agent.name]) for agent in bot_agents})
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()

def play_vsbot_single(step):
    cfg['player_num_per_team'] = 1
    cfg['frame_limit'] = step
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    my_player_id = 0
    bot_agents = []
    for player in env.server.player_manager.get_players():
        if player.player_id != my_player_id:
            bot_agents.append(BotAgent(player.player_id))
    for i in range(100000):
        actions = None
        x1, y1 = None, None
        action_type = 0
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                action_type = -1
                action_type = -1
                if event.key == pygame.K_UP:
                    x1, y1 = 0, -1
                if event.key == pygame.K_DOWN:
                    x1, y1 = 0, 1
                if event.key == pygame.K_LEFT:
                    x1, y1 = -1, 0
                if event.key == pygame.K_RIGHT:
                    x1, y1 = 1, 0
                if event.key == pygame.K_1: # Spores
                    action_type = 0
                if event.key == pygame.K_2: # Splite
                    action_type = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type = 2
        actions = {my_player_id: [x1, y1, action_type]}
        actions.update({agent.name: agent.step(obs[1][agent.name]) for agent in bot_agents})
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()

def play_farm_team(step):
    cfg['player_num_per_team'] = 2
    cfg['team_num'] = 1
    cfg['frame_limit'] = step
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    
    for i in range(100000):
        action_type1 = None
        action_type2 = None
        x1, y1, x2, y2 = None, None, None, None
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_1: # Spores
                    action_type1 = 0
                if event.key == pygame.K_2: # Splite
                    action_type1 = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type1 = 2
                if event.key == pygame.K_w:
                    x2, y2 = 0, -1
                if event.key == pygame.K_s:
                    x2, y2 = 0, 1
                if event.key == pygame.K_a:
                    x2, y2 = -1, 0
                if event.key == pygame.K_d:
                    x2, y2 = 1, 0
                if event.key == pygame.K_j: # Spores
                    action_type2 = 0
                if event.key == pygame.K_k: # Splite
                    action_type2 = 1
                if event.key == pygame.K_l: # Stop moving
                    action_type2 = 2
        actions = {
            0: [x1, y1, action_type1],
            1: [x2, y2, action_type2],
        }
        # actions.update({agent.name: agent.step(obs[1][agent.name]) for agent in bot_agents})
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()

def play_vsbot_team(step):
    cfg['frame_limit'] = step
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    
    bot_agents = []
    for player in env.server.player_manager.get_players():
        if player.player_id != 0 and player.player_id != 1:
            bot_agents.append(BotAgent(player.player_id))
    for i in range(100000):
        action_type1 = None
        action_type2 = None
        x1, y1, x2, y2 = None, None, None, None
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_1: # Spores
                    action_type1 = 0
                if event.key == pygame.K_2: # Splite
                    action_type1 = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type1 = 2
                if event.key == pygame.K_w:
                    x2, y2 = 0, -1
                if event.key == pygame.K_s:
                    x2, y2 = 0, 1
                if event.key == pygame.K_a:
                    x2, y2 = -1, 0
                if event.key == pygame.K_d:
                    x2, y2 = 1, 0
                if event.key == pygame.K_j: # Spores
                    action_type2 = 0
                if event.key == pygame.K_k: # Splite
                    action_type2 = 1
                if event.key == pygame.K_l: # Stop moving
                    action_type2 = 2
        actions = {
            0: [x1, y1, action_type1],
            1: [x2, y2, action_type2],
        }
        actions.update({agent.name: agent.step(obs[1][agent.name]) for agent in bot_agents})
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()

def play_vsai_single(step):
    cfg['frame_limit'] = step
    cfg['player_num_per_team'] = 1
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    my_player_id = 0
    ai_player_id = 1
    from solo_agent.agent import AIAgent as AI
    ai = AI(team_name=1, player_names=[1])
    for i in range(100000):
        actions = None
        x1, y1 = None, None
        action_type = 0
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                action_type = -1
                action_type = -1
                if event.key == pygame.K_UP:
                    x1, y1 = 0, -1
                if event.key == pygame.K_DOWN:
                    x1, y1 = 0, 1
                if event.key == pygame.K_LEFT:
                    x1, y1 = -1, 0
                if event.key == pygame.K_RIGHT:
                    x1, y1 = 1, 0
                if event.key == pygame.K_1: # Spores
                    action_type = 0
                if event.key == pygame.K_2: # Splite
                    action_type = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type = 2
        ai_action = ai.get_actions(obs)
        actions = {my_player_id: [x1, y1, action_type]}
        actions.update(ai_action)
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()

def play_vsai_team(step):
    cfg['frame_limit'] = step
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    from cooperative_agent.agent import AIAgent as AI
    ai = AI(team_name=1, player_names=[2,3])
    for i in range(100000):
        action_type1 = None
        action_type2 = None
        x1, y1, x2, y2 = None, None, None, None
        # ================ control by keyboard ===============
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_1: # Spores
                    action_type1 = 0
                if event.key == pygame.K_2: # Splite
                    action_type1 = 1
                if event.key == pygame.K_3: # Stop moving
                    action_type1 = 2
                if event.key == pygame.K_w:
                    x2, y2 = 0, -1
                if event.key == pygame.K_s:
                    x2, y2 = 0, 1
                if event.key == pygame.K_a:
                    x2, y2 = -1, 0
                if event.key == pygame.K_d:
                    x2, y2 = 1, 0
                if event.key == pygame.K_j: # Spores
                    action_type2 = 0
                if event.key == pygame.K_k: # Splite
                    action_type2 = 1
                if event.key == pygame.K_l: # Stop moving
                    action_type2 = 2
        actions = {
            0: [x1, y1, action_type1],
            1: [x2, y2, action_type2],
        }
        ai_action = ai.get_actions(obs)
        actions.update(ai_action)
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()

def watch_vsai_only(step):
    cfg['frame_limit'] = step
    env = GoBiggerEnv(cfg)
    obs = env.reset()
    done = False
    render = RealtimeRender(map_width=64, map_height=64)
    fps_real = 0
    t1 = time.time()
    clock = pygame.time.Clock()
    fps_set = env.server.fps
    from cooperative_agent.agent import AIAgent as AI
    ai_0 = AI(team_name=0, player_names=[0,1])
    ai_1 = AI(team_name=1, player_names=[2,3])
    for i in range(100000):
        action_type1 = None
        action_type2 = None
        x1, y1, x2, y2 = None, None, None, None
        # ================ control by keyboard ===============
        actions = {
            0: [x1, y1, action_type1],
            1: [x2, y2, action_type2],
        }
        ai_action = ai_0.get_actions(obs)
        actions.update(ai_action)
        ai_action = ai_1.get_actions(obs)
        actions.update(ai_action)
        if not done:
            obs, reward, done, info = env.step(actions=actions)
            print(obs[0]['leaderboard'])
            # import pdb; pdb.set_trace()
            render.fill(food_balls=env.server.food_manager.get_balls(), 
                        thorns_balls=env.server.thorns_manager.get_balls(), 
                        spore_balls=env.server.spore_manager.get_balls(), 
                        players=env.server.player_manager.get_players(), 
                        player_num_per_team=env.server.player_num_per_team, 
                        fps=fps_real,
                        leaderboard=obs[0]['leaderboard'])
            render.show()
            if i % fps_set == 0:
                t2 = time.time()
                fps_real = fps_set/(t2-t1)
                t1 = time.time()
        else:
            logging.debug('Game Over')
            break
        clock.tick(fps_set)
    render.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['single', 'team', 'watch'], default='single')
    parser.add_argument('--map', type=str, choices=['farm', 'vsbot', 'vsai'], default='farm')
    parser.add_argument('--step', type=int, default=3600)

    args = parser.parse_args()
    
    if args.mode == 'single':
        if args.map == 'farm':
            play_farm_single(args.step)
        elif args.map == 'vsbot':
            play_vsbot_single(args.step)
        elif args.map == 'vsai':
            play_vsai_single(args.step)
    elif args.mode == 'team':
        if args.map == 'farm':
            play_farm_team(args.step)
        elif args.map == 'vsbot':
            play_vsbot_team(args.step)
        elif args.map == 'vsai':
            play_vsai_team(args.step)
    elif args.mode == 'watch':
        watch_vsai_only(args.step)
        
