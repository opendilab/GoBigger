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
    * -1 means no actions. It will remain speed in the last frame.
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

Send actions
--------------

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
                'food': [[position.x, position.y, radius], ...], 
                'thorns': [[position.x, position.y, radius], ...],
                'spore': [[position.x, position.y, radius], ...],
                'clone': [[[position.x, position.y, radius, player_name, team_name], ...], 
            }, # all balls' info in vision
            'team_name': team_name, # the team which this player belongs to 
        }
    }

The ``overlap`` in ``player_state`` represents the structured information of the ball appearing in the current player's field of vision. ``overlap`` is a simple dictionary, each key-value pair represents the information of a kind of ball in the field of view. ``overlap`` contains the structured information of food ball, thorn ball, spore ball, clone ball (only position and radius, if it is a clone ball, it contains the player name and team name). Specifically, for example, we found that the content of the ``food`` field is ``[[3.0, 4.0, 2], ..]`` (for simplicity, only the first element in the list is shown here), then the meaning is that there is a food ball with a radius of ``2`` at the coordinate ``(3.0, 4.0)`` in the player's field of vision.

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



Observation Space - Customize
============================================

In addition to the observation space mentioned above, GoBigger also supports different kinds of observation space. Users can modify ``obs_settings`` in the input cfg of the server.

.. code-block:: python

    server = Server(cfg=dict(
        ...
        obs_settings=dict(
            with_spatial=True,
            with_speed=False,
            with_all_vision=False,
            cheat=False,
            with_spore_owner=False,
        ),
    ))

Now we introduce the role of each value in ``obs_settings``.

With Spatial Info
-------------------

In fact, when we get ``feature_layers`` and ``overlap`` in observation, it is clear that they contains similar info but different in the form of expression. That means, we can only get ``overlap`` and drop ``feature_layers`` in our observation, which will bring us less computation because it reduces the amount of rendering calculations. You can add ``with_spatial=False`` when your server initializes.

With Spore Owner Info
------------------------

We add owner for spores to let users know where spores come from. You can add ``with_spore_owner=True`` in ``obs_settings`` when your server initializes. We add owner in each spore's cell.

For example, a spore cell will be like:

.. code-block:: python

    [position.x, position.y, radius, owner]

Or if you set ``with_speed=True``, it will be like:
    
.. code-block:: python

    [position.x, position.y, radius, vel.x, vel.y, owner]    

With Speed Info
-------------------

We can get the speed information of the ball by calculating the relative position between frames for the same ball. In order to reduce the user's burden, GoBigger provides ``with_speed=True`` to help users directly get the speed information of all balls in observation. Once ``with_speed=True`` is specified, the ``overlap`` obtained by the user will add ``speed`` info to the corresponding element to indicate the speed of the ball. For example, the ``player_state`` will look like the following. Please pay attention to the order of different elements in the list.

.. code-block:: python

    {
        player_name: {
            'feature_layers': list(numpy.ndarray), # features of player
            'rectangle': [left_top_x, left_top_y, right_bottom_x, right_bottom_y], # the vision's position in the map
            'overlap': {
                'food': [[position.x, position.y, radius], ...], 
                'thorns': [[position.x, position.y, radius, speed.x, speed.y], ...],
                'spore': [[position.x, position.y, radius, speed.x, speed.y], ...],
                'clone': [[[position.x, position.y, radius, speed.x, speed.y, player_name, team_name], ...],     
            }, # all balls' info in vision
            'team_name': team_name, # the team which this player belongs to 
        }
    }

.. note::

    Only ``spore``, ``thorn``, and ``clone`` in ``overlap`` will contain speed information.

Get a full vision
------------------

The existence of a partial field of view may complicate training. Therefore, GoBigger provides a full vision interface. Get the information of the full vision by specifying ``with_all_vision=True``. Note that in this mode, since the field of view of different players is the same, in order to reduce the pressure of information transmission, we will only give the corresponding global field of view information in the information dictionary of the first player. For example, if there are 2 teams in a game, and there are 2 players in each team, the ``player_state`` obtained will be as follows:

.. code-block:: python

    {
        '0': {
            'feature_layers': list(numpy.ndarray),
            'rectangle': None,
            'overlap': {
                'food': [[position.x, position.y, radius], ...], 
                'thorns': [[position.x, position.y, radius], ...],
                'spore': [[position.x, position.y, radius], ...],
                'clone': [[[position.x, position.y, radius, player_name, team_name], ...],   
            }, 
            'team_name': team_name, 
        },
        '1': {
            'feature_layers': None,
            'rectangle': None,
            'overlap': None,
            'team_name': team_name,
        },
        '2': {
            'feature_layers': None,
            'rectangle': None,
            'overlap': None,
            'team_name': team_name,
        },
        '3': {
            'feature_layers': None,
            'rectangle': None,
            'overlap': None,
            'team_name': team_name,
        },
    }

Please note that the corresponding ``feature_layers`` and ``overlap`` in the information of other players will be set to ``None`` except for the player with the number ``'0'``.

Get global vision + player's local vision
-------------------------------------------------

In many scenarios, using some cheat information (such as removing the fog of war) can effectively help the algorithm converge. Therefore, on the basis of obtaining the global vision, we have added a mode of obtaining the global vision and the player's local vision at the same time. Get it by specifying ``cheat=True``. Note that in this mode, the setting of ``with_all_vision`` will have no effect, because the global vision information will always be returned. For example, assuming there are 2 teams in a game with 1 player in each team, the ``player_state`` obtained will be as follows:

.. code-block::python

    {
        'all': {
            'feature_layers': list(numpy.ndarray),
            'rectangle': None,
            'overlap': {
                'food': [{'position': position, 'radius': radius}, ...],
                'thorns': [{'position': position, 'radius': radius}, ...],
                'spore': [{'position': position, 'radius': radius}, ...],
                'clone': [{'position': position, 'radius': radius, 'player': player_name, 'team': team_name}, ...],
            },
            'team_name': '',
        }
        '0': {
            'feature_layers': list(numpy.ndarray),
            'rectangle': None,
            'overlap': {
                'food': [{'position': position, 'radius': radius}, ...],
                'thorns': [{'position': position, 'radius': radius}, ...],
                'spore': [{'position': position, 'radius': radius}, ...],
                'clone': [{'position': position, 'radius': radius, 'player': player_name, 'team': team_name}, ...],
            },
            'team_name': team_name,
        },
        '1': {
            'feature_layers': list(numpy.ndarray),
            'rectangle': None,
            'overlap': {
                'food': [{'position': position, 'radius': radius}, ...],
                'thorns': [{'position': position, 'radius': radius}, ...],
                'spore': [{'position': position, 'radius': radius}, ...],
                'clone': [{'position': position, 'radius': radius, 'player': player_name, 'team': team_name}, ...],
            },
            'team_name': team_name,
        },
    }

Note that the global view information is placed under the ``all`` field, where the ``team_name`` is set to empty. The rest of the player information remains the same.
