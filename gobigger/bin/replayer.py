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


def test_pbutil():
    env = create_env('st_t2p2', dict(
        playback_settings=dict(
            playback_type='by_frame',
            by_frame=dict(
                save_frame=True,
            )
        ),
    ))
    obs = env.reset()
    bot_agents = []
    team_infos = env.get_team_infos()
    print(team_infos)
    for team_id, player_ids in team_infos:
        for player_id in player_ids:
            bot_agents.append(BotAgent(player_id, level=2))
    time_step_all = 0
    for i in range(100000):
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        t1 = time.time()
        obs, reward, done, info = env.step(actions=actions)
        t2 = time.time()
        time_step_all += t2-t1
        logging.debug('{} {:.4f} envstep {:.3f} / {:.3f}, leaderboard={}'\
            .format(i, obs[0]['last_frame_count'], t2-t1, time_step_all/(i+1), obs[0]['leaderboard']))
        if done:
            logging.debug('Game Over')
            break
    env.close()

if __name__ == '__main__':
    play()
    # test_pbutil()
