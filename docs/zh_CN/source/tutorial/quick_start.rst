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
        else:
            print('finish game!')
            break
    server.close()

在上述代码中，首先构建了 ``Server`` 类作为游戏引擎，并构建 ``EnvRender`` 类作为渲染引擎，由二者协调游戏的进行。然后，通过 ``server.step()`` 完成游戏每一步的进行，通过 ``server.obs()`` 获取游戏环境的当前状态。

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


