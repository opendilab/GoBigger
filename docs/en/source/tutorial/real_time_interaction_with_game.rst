Real-time Interaction with game
##########################################

GoBigger allow users to play game on their personal computer in real-time. Serveral modes are supported for users to explore this game.

.. note::

    If your version of GoBigger is v0.1.x, please upgrade for a better experience. You can use ``pip install --upgrade gobigger`` to access the latest version of GoBigger.


Standard setting with partial view
--------------------------------------

If you want to play real-time game on your PC on your own, you can launch a game with the following code:

.. code-block:: bash

    python -m gobigger.bin.play --mode st --vision-type partial

In this mode, using mouse to control the your balls to move, ``Q`` means eject spore on your moving direction, ``W`` means split your balls, and ``E`` means stop all your balls and gather them together.


Standard setting with full view
--------------------------------------

If you want to play real-time game on your PC with your friends, you can launch a game with the following code:

.. code-block:: bash

    python -m gobigger.bin.play --mode st --vision-type full


Independent action setting with partial view
------------------------------------------------

In the independent action game mode, each ball of the player receives an action individually. But because it is more difficult to control, we still only receive an action based on the mouse and keyboard in this mode, and assign this action to all the player's balls. The game can be started with the following code:

.. code-block:: bash

    python -m gobigger.bin.play --mode sp --vision-type partial

