from gobigger.envs import create_env
from cooperative_agent.agent import AIAgent as AI

env = create_env('st_t2p2')
obs = env.reset()

agent1 = AI(team_name=0, player_names=[0,1])
agent2 = AI(team_name=1, player_names=[2,3])

for i in range(1000):
    actions1 = agent1.get_actions(obs)
    actions2 = agent2.get_actions(obs)
    actions1.update(actions2)
    obs, rew, done, info = env.step(actions1)
    print('[{}] leaderboard={}'.format(i, obs[0]['leaderboard']))
    if done:
        print('finish game!')
        break
env.close()