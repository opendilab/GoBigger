Quick Start
##############

Launch a game environment
==================================

After installation, you can launch your game environment easily according the following code:

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

You will see output as following. It shows the frame number and the leaderboard per frame.

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

We also build a simple env following ``gym.Env``. For more details, you can refer to ``gobigger/envs/gobigger_env.py``.


Customize your config
============================

Class ``Server`` use default config to generate a game environment. To customize your environment, you can change the parameters and parse them to ``Server``.

Add more players in a game
------------------------------------

For example, you may want to allow 6 teams and 2 players per team in your game, and then please add ``team_num`` and ``player_num_per_team`` in config and parse it to ``Server``.

.. code-block:: python

    from gobigger.server import Server

    server = Server(dict(
        team_num=6, 
        player_num_per_team=2
    ))

Extend the game time
------------------------------------
If you want to extend the game time to 20 minutes (1200 seconds), you can use the following codes.

.. code-block:: python

    from gobigger.server import Server

    server = Server(dict(
        match_time=1200
    ))

Change the size of the map
------------------------------------

If you want to have a larger map, you can change ``map_width`` and ``map_height`` in config.

.. code-block:: python

    from gobigger.server import Server
    
    server = Server(dict(
        map_width=1000,
        map_height=1000,
    ))


