Space
##############


Action Space
======================

In fact, a ball can only move, eject, split, and stop in our game, thus the action space is simple:

.. code-block:: python

    action = [x, y, action_type]

* x, y: A point ``(x, y)`` in the unit circle. 
    * We will normalize this point to ensure that its length will not more than 1. 

* action_type: Int
    * -1 means no actions
    * 0 means eject spore on given direction, and move on given direction
    * 1 means split into several balls, and move on given direction
    * 2 means stop and gather all your balls together
    * 3 means eject but not change direction
    * 4 means split but not change direction

It is important for a ball to do some actions on other direction without changing moving direction. That is why we add action_type 3 and 4 in our action space. A simple demo is as following. The ball can eject and change direction at the same time with ``action_type=0``, and it can also eject on other direction and not change its moving direction with ``action_type=3``.

.. only:: html

    .. figure:: images/eject_and_move.gif
      :width: 300
      :align: center

If you have several players in your game, remember that server needs to know the relationship between the actions and the players. So you need to send actions in the following way:

.. code-block:: python

    player_names = server.get_player_names() # get all names in server
    actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] for player_name in player_names)}
    server.step(actions)


Observation Space
======================

Each time ``server.obs()`` is called, you will get your balls' observation. 

.. code-block:: python

    global_state, player_state = server.obs()

``global_state`` in details:

.. code-block:: python

    {
        'border': [map_width, map_height], # the map size
        'total_time': match_time, # the duration of a game
        'last_time': last_time,   # the length of time a game has been played
        'leaderboard': {
            team_name: team_size
        } # the team with its size in this game
    }

``player_state`` in details:

.. code-block:: python

    {
        player_name: {
            'feature_layers': list(numpy.ndarray), # features of player
            'rectangle': [left_top_x, left_top_y, right_bottom_x, right_bottom_y], # the vision's position in the map
            'overlap': {
                'food': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
                'thorns': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
                'spore': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
                'clone': [{'position': position, 'radius': radius, 'player': player_name, 'team': team_name}, ...], # the length of food is not sure
            }, # all balls' info in vision
            'team_name': team_name, # the team which this player belongs to 
        }
    }


We define that ``feature_layers`` in ``player_state`` represents the feature of this player. ``feature_layers`` has several channels, and each channel gives the info of food balls, or spore balls, or thorns balls, or player balls in its vision. For example, in a game we have 4 teams and 3 players for each team, then we get ``feature_layers`` as a list, and the length of this list should be 15. Here we show the meanning of each channel in the list:

* channel 0: the position of player 0 in vision. If no player 0 in vision, all items will be zero.

* channel 1: the position of player 1 in vision. 

* channel 2: the position of player 2 in vision. 

* channel 3: the position of player 3 in vision. 

* channel 4: the position of player 4 in vision. 

* channel 5: the position of player 5 in vision. 

* channel 6: the position of player 6 in vision. 

* channel 7: the position of player 7 in vision. 

* channel 8: the position of player 8 in vision. 

* channel 9: the position of player 9 in vision. 

* channel 10: the position of player 10 in vision. 

* channel 11: the position of player 11 in vision. 

* channel 12: the position of all food balls in vision. 

* channel 13: the position of all spore balls in vision. 

* channel 14: the position of all thorns balls in vision.


.. note::

    ``overlap`` in ``player_state`` only includes balls in the player's owned vision. What's more, if a ball only show part of itself in the player's vision, we will return all this ball's info, such as radius and position, to be part of ``overlap``.


Observation Space - Without Feature Layers
============================================

In fact, when we get ``feature_layers`` and ``overlap`` in observation, it is clear that they contains similar info but different in the form of expression. That means, we can only get ``overlap`` and drop ``feature_layers`` in our observation, which will bring us less computation because it reduces the amount of rendering calculations. You can add ``use_spatial=False`` when your render inits as following:

.. code-block:: python

    server = Server()
    render = EnvRender(server.map_width, server.map_height, use_spatial=False) # drop feature_layers
    server.set_render(render)
    server.start()

.. note::

    If you use ``use_spatial=False`` in your render, you will be unable to get the saved video because there will be no rendering in your environment simulation. 
