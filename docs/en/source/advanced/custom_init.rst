Custom opening
##############


Overview
======================

We consider that the game will mainly be divided into two situations: early development and late attack. Therefore, in order to make it easier for agents to learn for different scenarios, we provide the function of customizing the opening. Through this function, the user can freely set the scene when the game starts, including the number, position and size of the various balls in the scene. We hope this will allow users to pay more attention to the design of some agent tasks.


How to customize
======================

The user can customize the opening game scene by setting the initialization ``config`` passed to the ``server``. The relevant details of the ``custom_init`` field can be used to set the relevant details of the food ball, thorns ball, spore ball and the player's clone ball. The following is a simple configuration example:

.. code-block:: python

    custom_init=dict(
        food=[{'position': [100, 100],'radius': 2}],
        thorns=[{'position': [200, 200],'radius': 15}],
        spore=[{'position': [300, 300],'radius': 3}],
        clone=[{'position': [400, 400],'radius': 12,'player': '0','team': '0'}],
    ),

As shown above, for the food ball, thorns ball, and spore ball, we have opened the position and radius setting interface. For the player's clone ball, in addition to the position and radius, the user also needs to specify the name of the player and team to which the ball belongs. Note that the naming of player names and team names needs to conform to game habits. For example, in a game consisting of 4 teams and 3 players in each team, if you want to customize the opening design, the name of the player should be selected. The value range is the str type from 0 to 11, and the value range of the team name is the str type from 0 to 3. If the relevant player is not set, it will be randomly born on the map with the smallest radius.

In addition, after setting the opening, the game will continue to iterate according to the parameters in the configuration table. For example, if the player sets only 100 food balls at the beginning (far lower than the initial number of food balls set in the configuration table), then the number of food balls will increase according to the rules after the start.


Overloaded game
======================

We sometimes encounter the following situations:

* When you play a beautiful game, you may want to continue to explore other solutions from the middle of the game

* When your agent does something wrong in a certain game, you may want to go back to a certain point in the game to let the agent explore more directions

At this time, you can use the interface we provide to reload the game to achieve the above goals! In the initialization ``config`` passed in to ``server``, there are several character breaks that need to be set:

.. code-block:: python

    save_bin=False, # Whether to save the information of the game
    load_bin=False, # Whether to load the information of a game at the start of the game
    load_bin_path='', # The file path to load the information of a game at the start of the game
    load_bin_frame_num ='all', # can be int (representing the action frame number to load), or 'all' (representing loading all frames)

As shown above. To use the function of reloading the game, we need to set ``save_bin`` to ``True`` in the first game, so that the information of the first game will be saved under the ``save_path`` provided by the user, with ``.pkl`` is the file suffix. So after the end of this round, we can assume that we got the information file named ``/path/to/d11355d8-4c4e-11ec-8503-b49691521104.pkl``. Suppose we want to load the first 300 action frames of the first game in the second game, then we can make the following settings:

.. code-block:: python

    load_bin=True,
    load_bin_path='/path/to/d11355d8-4c4e-11ec-8503-b49691521104.pkl',
    load_bin_frame_num = 300,

Then when the user calls ``server.reset()``, we will load the first 300 frames in the file information of the first round and stop the game at the end of the 300 frames. At this point, the user can continue to ``step`` or ``obs`` on this basis.
