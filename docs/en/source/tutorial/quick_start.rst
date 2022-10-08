Quick Start
##############

Launch a game environment
==================================

After installation, you can launch your game environment easily according the following code:

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

You will see output as following. It shows the frame number and the leaderboard per frame.

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


Customize your config
============================

Users can also choose to customize the game environment by modifying the configuration cfg and through the ``gobigger.envs.create_env_custom`` method we provide. The ``gobigger.envs.create_env_custom`` method accepts two parameters, the first parameter is ``type``, the optional value is ``st`` or ``sp``, which represent the standard game mode, and the independent action game mode. See the introduction of the two modes for details. Below we give a few simple examples based on the standard game mode.

Add more players in a game
------------------------------------

For example, you may want to allow 6 teams and 2 players per team in your game, and then please modify ``team_num`` and ``player_num_per_team`` in config.

.. code-block:: python

    from gobigger.envs import create_env_custom

    env = create_env_custom(type='st', cfg=dict(
        team_num=6, 
        player_num_per_team=2
    ))

Extend the game time
------------------------------------
If you want to extend the game time to 20 minutes (24000 frames), you can use the following codes.

.. code-block:: python

    from gobigger.envs import create_env_custom

    env = create_env_custom(type='st', cfg=dict(
        frame_limit=24000
    ))

Change the size of the map
------------------------------------

If you want to have a larger map, you can change ``map_width`` and ``map_height`` in config.

.. code-block:: python

    from gobigger.envs import create_env_custom
    
    env = create_env_custom(type='st', cfg=dict(
        map_width=1000,
        map_height=1000,
    ))


