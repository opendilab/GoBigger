快速开始
##############

通过代码与游戏环境进行交互
==================================

在安装完成之后，可以用以下代码快速实现与游戏环境进行交互：

.. code-block:: python

    import random
    from gobigger.server import Server
    from gobigger.render import EnvRender

    server = Server()
    render = EnvRender(server.map_width, server.map_height)
    server.set_render(render)
    server.start()
    player_names = server.get_player_names_with_team() 
    # get [[team1_player1, team1_player2], [team2_player1, team2_player2], ...]
    for i in range(10000):
        actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] \
                   for team in player_names for player_name in team}
        if not server.step(actions):
            global_state, screen_data_players = server.obs()
            print('[{}] leaderboard={}'.format(i, global_state['leaderboard']))
        else:
            print('finish game!')
            break
    server.close()

在上述代码中，首先构建了 ``Server`` 类作为游戏引擎，并构建 ``EnvRender`` 类作为渲染引擎，由二者协调游戏的进行。然后，通过 ``server.step()`` 完成游戏每一步的进行，通过 ``server.obs()`` 获取游戏环境的当前状态。执行之后，将会得到类似下面的输出，给出了每一帧排行榜信息。

.. code-block::

    [0] leaderboard={'0': 27, '1': 27, '2': 27, '3': 27}
    [1] leaderboard={'0': 27, '1': 27, '2': 27, '3': 27}
    [2] leaderboard={'0': 27, '1': 30.99935, '2': 30.99935, '3': 30.998700032499997}
    [3] leaderboard={'0': 27, '1': 34.99610032498374, '2': 34.99675032498374, '3': 30.9961004874675}
    [4] leaderboard={'0': 27, '1': 38.99025149484726, '2': 34.99155136485701, '3': 38.992201494805016}
    [5] leaderboard={'0': 30.998700032499997, '1': 42.982054039382575, '2': 34.98635344444432, '3': 38.98620350437408}
    [6] leaderboard={'0': 34.9961004874675, '1': 42.973458273284024, '2': 34.98115656353774, '3': 38.98020671345127}
    [7] leaderboard={'0': 34.99270152230301, '1': 46.964264256209255, '2': 38.974660754429394, '3': 38.974211121796685}
    [8] leaderboard={'0': 34.98930323688059, '1': 46.954872107798515, '2': 38.96686640687893, '3': 38.96821672917049}
    [9] leaderboard={'0': 38.98525563106426, '1': 46.94548183767656, '2': 38.95907361808107, '3': 38.96222353533294}
    ...

我们也遵循 ``gym.Env`` 的接口完成了一个简单的 ``Env`` 类，具体可以查看 ``gobigger/envs/gobigger_env.py``。


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


