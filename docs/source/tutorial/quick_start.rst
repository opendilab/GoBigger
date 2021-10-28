Quick Start
##############

Launch a game environment
==================================

After installation, you can launch your game environment easily according the following code:

.. code-block:: python

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


