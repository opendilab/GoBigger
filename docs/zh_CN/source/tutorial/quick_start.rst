快速开始
##############

通过代码与游戏环境进行交互
==================================

在安装完成之后，可以用以下代码快速实现与游戏环境进行交互：

.. code-block:: python

import random
from gobigger.envs import create_env

env = create_env('st_t2p2')
obs = env.reset()
for i in range(1000):
    actions = {0: [random.uniform(-1, 1), random.uniform(-1, 1), 0],
               1: [random.uniform(-1, 1), random.uniform(-1, 1), 0],
               2: [random.uniform(-1, 1), random.uniform(-1, 1), 0],
               3: [random.uniform(-1, 1), random.uniform(-1, 1), 0]}
    obs, rew, done, info = env.step(actions)
    print('[{}] leaderboard={}'.format(i, obs[0]['leaderboard']))
    if done:
        print('finish game!')
        break
env.close()

在上述代码中，首先构建了环境，然后通过 ``env.step()`` 完成游戏每一步的进行，并获取到对应的 ``observation``，``reward``，``done``，``info`` 等信息。执行之后，将会得到类似下面的输出，给出了每一帧排行榜信息。

.. code-block::

    [0] leaderboard={0: 3000, 1: 3100.0}
    [1] leaderboard={0: 3000, 1: 3100.0}
    [2] leaderboard={0: 3000, 1: 3100.0}
    [3] leaderboard={0: 3000, 1: 3100.0}
    [4] leaderboard={0: 3000, 1: 3100.0}
    [5] leaderboard={0: 3000, 1: 3100.0}
    [6] leaderboard={0: 3000, 1: 3100.0}
    [7] leaderboard={0: 3000, 1: 3100.0}
    [8] leaderboard={0: 3000, 1: 3100.0}
    [9] leaderboard={0: 3000, 1: 3100.0}
    [10] leaderboard={0: 3000, 1: 3100.0}
    ...


自定义游戏环境
============================

用户也可以选择通过修改配置 cfg，并通过我们提供的 ``gobigger.envs.create_env_custom`` 方法来自定义游戏环境。``gobigger.envs.create_env_custom`` 方法接收两个参数，第一个参数是 ``type``，可选值为 ``st`` 或 ``sp``，分别代表标准比赛模式，和独立动作比赛模式。关于两种模式的介绍具体可以看。以下我们基于标准比赛模式举几个简单的例子。

修改游戏中的队伍数量和玩家数量
------------------------------------

如果用户想要在游戏中存在 6 个队伍，每个队伍中含有 2 名玩家，那么可以修改 ``team_num`` 和 ``player_num_per_team``。

.. code-block:: python

    from gobigger.envs import create_env_custom

    env = create_env_custom(type='st', cfg=dict(
        team_num=6, 
        player_num_per_team=2
    ))

修改游戏时长
------------------------------------

游戏内默认每秒20帧。如果用户想要将游戏时长设置为 20 分钟，即 24000 帧，可以修改 ``frame_limit``。

.. code-block:: python

    from gobigger.envs import create_env_custom

    env = create_env_custom(type='st', cfg=dict(
        frame_limit=24000
    ))

修改游戏地图大小
------------------------------------

如果用户想要拥有一个更大的地图，可以修改 ``map_width`` 和 ``map_height``。注意更大的地图可能会导致 ``step`` 速度变慢。

.. code-block:: python

    from gobigger.envs import create_env_custom
    
    env = create_env_custom(type='st', cfg=dict(
        map_width=1000,
        map_height=1000,
    ))


