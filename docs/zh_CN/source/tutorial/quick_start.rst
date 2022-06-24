快速开始
##############

通过代码与游戏环境进行交互
==================================

在安装完成之后，可以用以下代码快速实现与游戏环境进行交互：

.. code-block:: python

    import random
    from gobigger.envs import GoBiggerEnv

    env = GoBiggerEnv(dict(
        team_num=2,
        player_num_per_team=2,
    ))
    obs = env.reset()
    team_infos = env.get_team_infos()
    for i in range(1000):
        actions = {0: [random.uniform(-1, 1), random.uniform(-1, 1), -1],
                   1: [random.uniform(-1, 1), random.uniform(-1, 1), -1],
                   2: [random.uniform(-1, 1), random.uniform(-1, 1), -1],
                   3: [random.uniform(-1, 1), random.uniform(-1, 1), -1]}
        obs, rew, done, info = env.step(actions)
        print('[{}] leaderboard={}'.format(i, obs[0]['leaderboard']))
        if done:
            print('finish game!')
            break
    env.close()

在上述代码中，首先构建了 ``GoBiggerEnv`` 作为环境，然后通过 ``env.step()`` 完成游戏每一步的进行，并获取到对应的 ``observation``，``reward``，``done``，``info`` 等信息。执行之后，将会得到类似下面的输出，给出了每一帧排行榜信息。

.. code-block::

    [0] leaderboard={0: 4.6, 1: 4.6}
    [1] leaderboard={0: 4.6, 1: 4.6}
    [2] leaderboard={0: 4.6, 1: 4.6}
    [3] leaderboard={0: 4.6, 1: 4.6}
    [4] leaderboard={0: 4.6, 1: 4.6}
    [5] leaderboard={0: 4.6, 1: 4.6}
    [6] leaderboard={0: 4.6, 1: 4.6}
    [7] leaderboard={0: 4.6, 1: 4.6}
    [8] leaderboard={0: 4.6, 1: 4.6}
    [9] leaderboard={0: 4.6, 1: 4.6}
    [10] leaderboard={0: 4.6, 1: 4.6}
    ...


自定义游戏环境
============================

默认情况下，``Server`` 类使用了默认的配置来启动游戏环境。用户也可以选择通过修改配置 cfg 来自定义游戏环境。以下举了几个简单的例子。

修改游戏中的队伍数量和玩家数量
------------------------------------

如果用户想要在游戏中存在 6 个队伍，每个队伍中含有 2 名玩家，那么可以修改 ``team_num`` 和 ``player_num_per_team`` 并将其作为 ``Server`` 的参数。

.. code-block:: python

    from gobigger.server import Server

    server = Server(dict(
        team_num=6, 
        player_num_per_team=2
    ))

修改游戏时长
------------------------------------

如果用户想要将游戏时长设置为 20 分钟（1200秒），可以修改 ``match_time``。

.. code-block:: python

    from gobigger.server import Server

    server = Server(dict(
        match_time=1200
    ))

修改游戏地图大小
------------------------------------

如果用户想要拥有一个更大的地图，可以修改 ``map_width`` 和 ``map_height``。

.. code-block:: python

    from gobigger.server import Server
    
    server = Server(dict(
        map_width=1000,
        map_height=1000,
    ))


