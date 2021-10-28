Real-time Interaction with game
##########################################

GoBigger allow users to play game on their personal computer in real-time. Serveral modes are supported for users to explore this game.


Single Player
--------------------

If you want to play real-time game on your PC on your own, you can launch a game with the following code:

.. code-block:: bash

    python -m gobigger.bin.play --player-num 1 --vision-type full

In this mode, up arrow & down arrow & left arrow & rigth arrow allows your balls move, ``Q`` means eject spore on your moving direction, ``W`` means split your balls, and ``E`` means stop all your balls and gather them together.


Double Players
--------------------

If you want to play real-time game on your PC with your friends, you can launch a game with the following code:

.. code-block:: bash

    python -m gobigger.bin.play --player-num 2 --vision-type full

In this mode, player1 use up arrow & down arrow & left arrow & rigth arrow allows the balls move, ``[`` means eject spore on your moving direction, ``]`` means split your balls, and ``\\`` means stop all your balls and gather them together. player2 use ``W`` & ``S`` & ``A`` & ``D`` allows the balls move, ``1`` means eject spore on your moving direction, ``2`` means split your balls, and ``3`` means stop all your balls and gather them together.


Single Players with partial vision
----------------------------------------

If you want to play real-time game on your PC with only partial vision, you can launch a game with the following code:

.. code-block:: bash

    python -m gobigger.bin.play --player-num 1 --vision-type partial

Your vision depends on all your balls' positions and their size.

