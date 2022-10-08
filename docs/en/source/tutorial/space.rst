Space
#######################

Standard game mode
*********************

Standard game mode refers to the same game as agar, where the player can only provide one action per frame, and then all player balls will perform that one action.


Action Space
=======================

Since each ball controlled by the player can only move, sporulate, split, and stop, the action space of GoBigger is relatively simple:

.. code-block:: python

    action = [x, y, action_type]

* ``x, y``: is a point in the unit circle. ``(x, y)`` represents the player's manipulation of the ball's acceleration.
    * GoBigger will normalize ``(x, y)`` to ensure that its modulus does not exceed ``1``.
    * If the user does not provide acceleration changes, ``(None, None)`` can be provided to indicate no changes to the movement.

* ``action_type``: Int
    * ``0``: means only move, actually every time ``env.step`` is called.
    * ``1``: Represents ejecting in the given direction. If the direction is not specified (ie ``(None, None)``), it is executed in the direction of movement.
    * ``2``: represents splitting in the given direction. If the direction is not specified (ie ``(None, None)``), it is executed in the direction of movement.

We hope that players can use the various skills of the clone ball more flexibly, and hope that the movement direction will not limit the choice of skills. Therefore, we allow the player to specify different directions and directions of movement when using the skill. For example, when the player's clone ball is moving to the right, if you want to spore down, you only need to specify ``action_type=1`` and specify ``(x, y)`` at the same time, and the clone ball can go to the side. Continue to move right, while spitting down spores. A simple example is given below.

.. only:: html

    .. figure:: images/eject_and_move.gif
      :width: 300
      :align: center

In addition, some useful actions can be achieved by the clever combination of ``x``, ``y`` and ``action_type``. For example, setting ``x`` and ``y`` to both ``None`` when sporulating spores can achieve cross sporulation. E.g:

.. only:: html

    .. figure:: images/eject_cross.gif
      :width: 300
      :align: center


Submit actions to the environment
------------------------------------------

In the case of multiple players, it is necessary to specify the correspondence between each action and the player. The submitted actions should be a dictionary, and each ``key-value-pair`` should be a player's ``id`` and the action he needs to do in this frame. Therefore, the action can be submitted as follows:

.. code-block:: python

     team_infos = env.get_team_infos()
     actions = {}
     for team_id, player_ids in team_infos.items():
         actions.update({player_id: [random.uniform(-1, 1), random.uniform(-1, 1), -1] for player_id in player_ids)})
     obs = env.step(actions)


Observation Space
=======================

After each step of the game, the user can get the game state under the vision of the clone ball.

.. code-block:: python

     obs, reward, done, info = env.step()
     global_state, player_states = obs

``global_state`` contains some global information, as follows:

.. code-block:: python

     {
         'border': [map_width, map_height], # map size
         'total_frame': total_frame, # The total number of frames in the whole game
         'last_frame_count': last_frame_count, # The current number of frames that have passed
         'leaderboard': { team_name: team_size } # Current leaderboard information, including the score of each team. The team's score is the sum of the players' scores in the team
     }

``player_states`` contains the information that each player can get, according to ``player_id``, as follows:


.. code-block:: python

    {
        player_id: {
            'rectangle': [left_top_x, left_top_y, right_bottom_x, right_bottom_y], # The position of the view box in the global view
            'overlap': {
                'food': [[position.x, position.y, radius, score], ...], # Food ball information in the field of view, which are position xy, radius, score
                'thorns': [[position.x, position.y, radius, score, vel.x, vel.y], ...], # The information of the thorns ball in the field of view, namely position xy, radius, score, current speed xy
                'spore': [[position.x, position.y, radius, score, vel.x, vel.y, owner], ...], # The spore ball information in the field of view, which are the position xy, radius, score, Current speed xy, from player's id
                'clone': [[[position.x, position.y, radius, score, vel.x, vel.y, direction.x, direction.y,
                            player_id, team_id], ...], # Player ball information in the field of view, namely position xy, radius, score, current speed xy, current direction xy, belonging player id, belonging team id
            },
            'team_name': team_name, # The current player's team id
            'score': player_score, # current player's score
            'can_eject': bool, # Whether the current player can perform the spore action
            'can_split': bool, # Whether the current player can perform the split action
        },
        ...
    }


The ``overlap`` in ``player_states`` represents the structured information about the ball currently in the player's field of view. ``overlap`` is a simple dictionary, each key-value pair represents information about a ball in view. ``overlap`` contains structured information about food balls, thorn balls, spore balls, and clone balls. Specifically, for example, we found that the content of the ``food`` field is ``[[3.0, 4.0, 2, 2], ...]`` (only the first element in the list is shown here for simplicity) , then the meaning is that in the player's field of vision, there is a food ball with a radius of ``2`` at the coordinates ``(3.0, 4.0)``, and the score of this food ball is ``2``.

Note that the length of the information list for each type of ball is indeterminate. For example, if there are ``20`` food balls in the current frame view, the length of the list corresponding to the current ``food`` is ``20``. In the next frame, if the food ball in the field of view becomes ``25``, the corresponding list length will become ``25``. Additionally, if only a portion of a ball is in the player's field of view, GoBigger will also give information about the center and radius of the ball in ``overlap``.


Reward
=======================

After each ``step`` of the game, the user can get the game's default reward.

.. code-block:: python

    _, reward, _, _ = env.step()

The default reward in the game is very simple, it is the difference between the total score of the player's current frame and the total score of the previous frame. Users can design more complex rewards based on the player's obseravtion.


Other Information
=======================

GoBigger provides statistics and puts this information in ``info``. After each ``step`` of the game, the user can get it.

.. code-block:: python

    _, _, _, info = env.step()

Specifically, ``info`` is a dictionary, and in the context of ``st_t2p2``, the following information can be obtained:

.. code-block::python

    info = {
        'eats': { # Each player id and his corresponding information
            0: {
                'food': 382, # How many food balls were eaten in the whole game
                'thorns': 2, # How many thorn balls were eaten in the whole game
                'spore': 0, # How many spore balls were eaten in the whole game
                'clone_self': 38, # How many self-player balls were eaten in the whole game
                'clone_team': 4, # How many teammates' player balls were eaten in the whole game
                'clone_other': 27, # How many opponent player balls were eaten in the whole game
                'eaten': 3, # How many player balls were eaten by other opponents in the whole game
            },
            1: {...}, 
            2: {...}, 
            3: {...},
        },
    }


Independent Action Game Mode
**************************************


The independent action game mode means that the player needs to provide action to all of his player balls every frame. Each player ball of the player can perform actions independently.


Action Space
=======================

The minimum action unit is the same as the standard game mode, except that when doing ``env.step(actions)``, the format of ``actions`` should be as follows:

.. code-block:: python

    actions = {
        player_id: {
            ball_id: [x, y, action_type],
            ...
        },
        ...
    }

The ``ball_id`` here can be determined from the ``obs`` obtained in each frame. Each ``ball_id`` will uniquely correspond to one of the player's clone balls.


Observation Space
=======================

Most of it is the same as the standard game mode, the only difference is that the clone ball part will add ``ball_id`` information. This information can be used to tell the player where the ``ball_id`` can be taken from when providing ``actions``.

``player_states`` is as follows:

.. code-block:: python

    {
        player_id: {
            ...
            'overlap': {
                ...
                'clone': [[[position.x, position.y, radius, score, vel.x, vel.y, direction.x, direction.y,
                            player_id, team_id, ball_id], ...], # The player's ball information in the field of view, namely position xy, radius, current speed xy, current direction xy, player id, team id, ball id
            },
            ...
        }
    }

