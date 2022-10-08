GoBigger Engine Design
###########################

Overview
===============

This section mainly explains the engine design of GoBigger, including detailed motion logic for various balls. If readers want to develop a new environment based on GoBigger, or want to learn more about the development details of GoBigger, they can read this section carefully. For the convenience of explanation, we will introduce the logic of each ball, and the interaction with other balls. If you are not familiar with the basic ball units in GoBigger, it is recommended to check the previous section (What is GoBigger) first. Note that the following descriptions are based on the settings of ``st_t4p3``.


What all balls have in common
==================================

1. In GoBigger, you can see that different balls have different sizes. We define that each ball has a certain ``score``, and the corresponding ``radius`` can be calculated from the score.

.. code-block:: python

    import math

    def score_to_radius(score):
        return math. sqrt(score / 100 * 0.042 + 0.15)

2. Food balls are immovable, but thorn balls, spore balls, and clone balls all contain speed attributes, which means they can all move.
3. If there is a relationship between two balls that can be eaten and eaten (such as between clone balls, between clone balls and all other balls, between thorn balls and spore balls), then when the centers of the two balls overlap, it will be determined whether phagocytosis can occur by the scores of the balls. We stipulate that phagocytosis can only occur when the score of the large ball exceeds ``1.3`` times that of the small ball.
4. The center of all balls will not exceed the map boundary during the movement.
5. Our default in-game ``FPS`` is ``20``. That is, the game state is updated ``20`` times in a second. Also, by default each call to ``env.step`` will advance the environment two frames, the user-provided action will be done in the first frame, and then the second frame will be given an empty action.


Food Ball
===============

1. Food balls are neutral resources in the game. In the ``st_t4p3`` configuration, the number of food balls on the map at the start of the game will be ``800``, and the maximum number is ``900``. Every ``8`` frames, ``(maximum quantity - current quantity) * 0.01`` food balls will be replenished, and the number of food balls will not exceed the upper limit.
2. The initial score for the food ball is ``100``. That is, if a clone eats a food ball, the clone's score will increase by ``100``.


Thorn Ball
===============
1. Thorn balls are also neutral resource in the game. In the ``st_t4p3`` configuration, the number of thorn balls on the map at the beginning of the game will be ``9``, and the maximum number is ``12``. Every ``120`` frames, round up ``(maximum quantity - current quantity) * 0.2`` thorn balls will be added in the map, and the number of thorn balls will not exceed the upper limit.
2. The initial score of the ball of thorns will be randomly selected from the range of ``10000`` to ``15000``.
3. When the player ejects the spore ball to the thorn ball, if the spore ball is covered by the center of the thorn ball, the thorn ball will eat the spore ball, and at the same time generate an initial velocity of ``10`` in the direction of the spore ball's movement, and the velocity decays uniformly to ``0`` over ``20`` frames.


Spore Ball
===============
1. The size of the spore ball is fixed and the score is fixed at ``1400``.
2. When the spore ball is spit out, the speed is fixed at ``30``, and the speed is uniformly attenuated to ``0`` in the ``20`` frame.


Clone Ball
===============
The size of the clone ball increases as it continues to eat the ball. The initial score for the clone ball is ``1000``. A single player can have a maximum of ``16`` clone balls. The ``eject`` skill can only be used when the score of each clone ball exceeds ``3200``, and the ``split`` skill can only be used when the score exceeds ``3600``.


Speed
---------------
The speed of the clone ball is a combination of three parts of the vector: the player's action, the centripetal force caused by the presence of multiple balls, and the gradually decaying speed caused by splitting or eating the thorn ball. The acceleration caused by player actions and centripetal force is multiplied by the length of each frame as the speed change amount at each frame.

1. Player Action: As defined by the action space, the player can provide any point ``(x,y)`` within a unit circle to change the speed of the clone ball. Specifically, GoBigger will first normalize this point to the inside of the unit circle (or to the circle if it is outside, otherwise leave it alone), and then multiply it by the weight ``30`` to give the acceleration.
2. Centripetal force: When the player has multiple clone balls, a centripetal force will be generated inside the multiple balls, which points to the center of mass. In fact, the centripetal force will not be used directly, it will be divided by the radius as the true centripetal force, and multiplied by the weight ``10`` to be the acceleration.
3. Gradually attenuated speed after splitting or eating the thorn ball: The new clone ball split by eating the thorn ball will have a new initial speed after the split. The modulo length of this velocity is related to the radius after splitting, specifically ``(260 - 20 * radius) / 7``, and the direction is away from the center of the circle. The velocity decays evenly to ``0`` over ``14`` frames. If the Clone Ball is obtained through the split skill, the formula for calculating the modulo length of this initial velocity is ``(95 + 19 * radius) / 7``.
4. The speed brought by player operation and centripetal force will be limited by the upper speed limit. The upper speed limit is related to the radius of the ball, and adjusts the upper speed limit by using the larger of the player action and centripetal force as the ``ratio``. The specific formula is ``(2.35 + 5.66 / radius) * ratio``.


Eating a thorn ball
---------------------------
1. Each time the Clone Ball eats the Thorns Ball, it will split up to a maximum of ``10`` new Clone Balls. For example, if a player currently has only two clone balls, and one of the clone balls eats a thorn ball, he will split new ``10`` clone balls, so the player has a total of `` 12`` Clone Balls; if a player currently has ``10`` Clone Balls, and one of them eats a Thorny Ball, he will split a new ``6`` Clone Ball, so this At that time the player has a total of ``16`` clone balls.
2. The maximum score of the new ball split by the Clone Ball is ``5000``. For example, the current score of the clone ball is ``23000``, he eats a thorn ball with a score of ``10000``, then his score will become ``33000``. At the same time, this avatar will split into new ``10`` avatars. According to the even distribution, the score of each avatar is ``3000``.
3. After eating the ball of thorns and splitting, the positions of the new balls are evenly distributed around, and there will always be new ball clones in the horizontal position to the right of the original ball.


Split
---------------
1. The new split ball will be in the direction specified by the player. If there is no specified direction, it will appear in the direction of movement of the original ball.
2. The split skill will divide the score of the original ball equally between the two split balls.
3. The split ball will also have the speed of the original one.
4. Whether after splitting or eating the thorn ball, the player's clone ball (including triggering the split and eating the thorn ball, as well as the newly added clone ball after these two operations) will enter a cooldown period with a length of ``20``. Clone balls in the cooldown period cannot trigger the operation of merging with their own clone balls. Additionally, after the Clone Ball completes a merge, it will re-enter the cooldown phase.


Eject
---------------
1. The spore balls generated after the sporulation operation is performed by the clone ball will appear in the direction specified by the player. If there is no specified direction, it will appear in the movement direction of the clone ball.
2. Each time the clone ball spit out a spore ball, it is equivalent to dividing ``1400`` from its own score and assigning it to a new spore ball.
