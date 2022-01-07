import os
import time
import pickle
import logging

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
    replay_path = os.path.join(replay_dir, str(seed)+'.replay')
    f = open(replay_path, 'w')
    f.write(str(seed) + '\n')
    for i in range(100000):
        obs = server.obs()
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        data_simple['actions'].append(actions)
        # logging.info('{} {} {} {} {}'.format(seed, i, server.get_last_time(), actions, obs[0]['leaderboard']))
        f.write('{} {}\n'.format(i, actions))
        f.flush()
        finish_flag = server.step(actions=actions)
        if finish_flag:
            logging.info('Game Over, {}'.format(obs[0]['leaderboard']))
            break
    server.close()


# def relaunch(replay_path):


if __name__ == '__main__':
    replay_dir = 'replays'
    if not os.path.isdir(replay_dir):
        os.mkdir(replay_dir)
    while True:
        launch(replay_dir)


