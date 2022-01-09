import os
import time
import pickle
import logging
from uuid import uuid1

from gobigger.agents import BotAgent
from gobigger.server import Server
from gobigger.render import EnvRender

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_AUDIODRIVER'] = 'dsp'

logging.basicConfig(level=logging.INFO)


def launch(replay_dir='replays'):
    seed = int(time.time())
    server = Server(dict(seed=seed))
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.reset()
    bot_agents = []
    for player_name in server.get_player_names():
        bot_agents.append(BotAgent(player_name, level=3))
    logging.info(seed)
    data_simple = {'seed': seed, 'actions': []}
    for i in range(100000):
        obs = server.obs()
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        data_simple['actions'].append(actions)
        # logging.info('{} {} {} {} {}'.format(seed, i, server.get_last_time(), actions, obs[0]['leaderboard']))
        finish_flag = server.step(actions=actions)
        if finish_flag:
            logging.info('Game Over, {}'.format(obs[0]['leaderboard']))
            break
    server.close()


def relaunch(replay_path):
    data_hard = {
        'observations': [],
        'actions': []
    }
    lines = open(replay_path, 'r').readlines()
    seed = int(lines[0].strip())
    actions_all = [eval(line.strip().split(' ', 1)[-1]) for line in lines[1:]]
    server = Server(dict(seed=seed))
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.reset()
    for i in range(500):
        obs = server.obs()
        actions = actions_all[i]
        logging.info('{} {} {}'.format(i, server.get_last_time(), obs[0]['leaderboard']))
        data_hard['observations'].append(obs)
        data_hard['actions'].append(actions)
        finish_flag = server.step(actions=actions)
        if finish_flag:
            logging.info('Game Over, {}'.format(obs[0]['leaderboard']))
            break
    server.close()
    file_name = str(uuid1()) + "-" + str(seed)
    data_path = os.path.join('replays', file_name+'.data2')
    with open(data_path, "wb") as f:
        pickle.dump(data_hard, f)


if __name__ == '__main__':
    replay_dir = 'replays'
    if not os.path.isdir(replay_dir):
        os.mkdir(replay_dir)
    while True:
        launch(replay_dir)

    # relaunch(replay_path='replays/1641535363.replay')

