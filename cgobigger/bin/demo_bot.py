import logging
import time
import datetime

from cgobigger.agents import BotAgent
from cgobigger.server import Server
from cgobigger.render import EnvRender

logging.basicConfig(level=logging.DEBUG)


def demo_bot():
    server = Server(dict(
        team_num=4,
        player_num_per_team=3,
        map_width=1000,
        map_height=1000,
        match_time=60*10,
        state_tick_per_second=10, # frame
        action_tick_per_second=5,
        collision_detection_type='precision',
        save_video=True,
        save_quality='low', # ['high', 'low']
        save_path='',
    ))
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.reset()
    bot_agents = []
    for player_name in server.get_player_names():
        bot_agents.append(BotAgent(player_name, level=3))
    time_obs = 0
    time_step = 0
    for i in range(100000):
        t0 = datetime.datetime.now()
        obs = server.obs()
        t1 = datetime.datetime.now()
        # actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        actions = {bot_agent.name: [0.0, 0.0, -1] for bot_agent in bot_agents}
        t2 = datetime.datetime.now()
        finish_flag = server.step(actions=actions)
        t3 = datetime.datetime.now()
        tmp_obs = (t1-t0).total_seconds()
        tmp_step = (t3-t2).total_seconds()
        time_obs += tmp_obs
        time_step += tmp_step
        logging.debug('{} {:.4f} obs: {:.6f} / {:.6f}, step: {:.6f} / {:.6f}' \
                      .format(i, server.get_last_time(), tmp_obs, time_obs/(i+1),
                              tmp_step, time_step/(i+1)))
        if finish_flag:
            logging.debug('Game Over')
            break
    server.close()


if __name__ == '__main__':
    demo_bot()
