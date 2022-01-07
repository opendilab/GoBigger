import logging

from gobigger.agents import BotAgent
from gobigger.server import Server
from gobigger.render import EnvRender

logging.basicConfig(level=logging.DEBUG)


def launch():
    server = Server()
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.reset()
    bot_agents = []
    for player_name in server.get_player_names():
        bot_agents.append(BotAgent(player_name, level=3))
    for i in range(100000):
        obs = server.obs()
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        finish_flag = server.step(actions=actions)
        if finish_flag:
            logging.debug('Game Over, {}'.format(obs[0]['leaderboard']))
            break
    server.close()


if __name__ == '__main__':
    while True:
        launch()
