What is GoBigger?
####################

Overview
===============

GoBigger is an `Agar <https://agar.io/>`_ like game, which is one of the most popular game all over the world. In GoBigger, users control their owned balls to collect weight in a 2-d map with border. There are many other balls in the map, such as food-balls, thorns-balls, spore-balls and other players' balls. With the limited time, user are ranked by the weight they collect. In order to improve the antagonism of the game, users are allowed to eat other others' balls to get more weight. So in a game, users need to grow by eating food-balls and thorns-balls, and escape from the larger balls, and eat smaller balls to gather more weight quickly.

.. only:: html

    .. figure:: images/overview.gif
      :width: 600
      :align: center

      Players are controling player-balls in a game.

For a more detailed exposition rules of the game, we will firstly introduce the balls in GoBigger.

Balls
===============
* Food-balls

    Food-balls are the neutral resources in the game. They will stay on where they are borned util someone comes and eats them. If a player-ball eat a food-ball, the food-ball's size will be parsed to the player-ball. There is a maximum number of food-balls in the map. Once the number of available food-balls is not enough, the game will generate new food-balls in random positions every certain time. 

    .. only:: html

        .. figure:: images/eat_food.gif
          :width: 300
          :align: center

          A player-balls eat a food-ball.


* Thorns-balls

    Thorns-balls are also the neutral resources in the game. Different with food-balls, they have larger size and less quantity. If a player-ball eat a thorns-ball, the thorns-ball's size will be parsed to the player-ball. But at the same time, the player-ball will explode and will be splited into several pieces. In GoBigger, the pieces always have the same size, and they will appear evenly around the original player-ball. So be careful! If there are other player-balls larger than yours, you should pay more attention to decide whether to eat the thorns-balls.

    Another feature of the thorns-balls is that they can be moved by player-balls through ejecting spore-balls. If a player-ball eject spore-balls to a thorns-ball, the thorns-ball will eat the spore-balls and grow larger. Besides, it will move on the moving direction of the spore-balls. That means if a player-ball wants to force a larger player-ball to explode, it can eject spore-balls to the thorns-ball and move it to the larger player-ball.

    .. only:: html

        .. figure:: images/on_thorns.gif
          :width: 300
          :align: center

          A player-balls eat a thorns-ball and explode.

* Spore-balls

    Spore-balls are ejected by the player-balls. They will stay on the map and can be eaten by any other player-balls. Spore-balls can not move or eat others.

    .. only:: html

        .. figure:: images/eject.gif
          :width: 300
          :align: center

          A player-balls eject some spore-balls.

* Player-balls

    Player-balls are the balls you can control in the game. You can change its moving direction at any time if you want. In addition, it can eat other balls smaller than itself by covering others' center. Once a player-ball eat other balls, its size will raise and it radius will increase accordingly. A player-ball has there skills:

    .. only:: html

        .. figure:: images/eat_player.gif
          :width: 300
          :align: center

          A player-balls eat other player-balls.

    * Eject

        Ejecting a spore-ball can help a player-ball decrease its size and make it move faster. When a player-ball ejects, the new spore-ball must appear on the player-ball's moving direction with a high speed and quickly slow down. 

        .. only:: html

            .. figure:: images/eject_to_thorns.gif
              :width: 300
              :align: center

              A player-ball eject to a thorns-ball and move it.

    * Split

        Spliting helps a player-ball to split itself in two pieces. The two pieces has the same size. Remember that all pieces will be merged in certain time. If you want to move faster, you can split and turn your balls into smaller size in order to get higher speed limit.

        .. only:: html

            .. figure:: images/split.gif
              :width: 300
              :align: center

              A player-ball splits into two player-balls.

    * Stop

        Stopping is a useful skill when a player wants all his player-balls to gather together. When you have numbers of cloned pieces, you can stop all your balls and soonly find them gather in a slow speed. If you have only one player-ball, you can call stop skill and make your player-ball still in place.

        .. only:: html

            .. figure:: images/split_merge.gif
              :width: 300
              :align: center

              A player stop and finally merge all balls together.

Rules of Game
===============

There are a few rules to be aware of as following.

1. Player-balls have a decay on size to ensure that they will not grow too large. For example, we set ``size_decay=0.00001`` in our default setting, which means that a player-ball's size will drop 0.001% in a state frame. Normaly we will have 40 state frames in a second, that means a player-ball's size will drop 0.04% in a second. If your player-ball's size is too large, you must eat more others to remain your size.

2. If a player's all balls are eat, it will respawn in somewhere randomly and immediately.

3. The player's vision will depends on its balls' positions. We calculate the centroid of a player, and get the smallest external square of all balls. After that, we expand this square as the final vision. To guarantee each player's vision, we also provide them with the basic vision even if all their balls gather together. For example, if the balls of a player are dispersed enough, a larger vision will be applied for this player. 

4. Each ball has its own speed limit based on its size. In order to ensure the balance of the game, we let larger balls move slow and smaller balls move fast.


High-level Operations
==============================

.. only:: html

    .. figure:: images/merge_quickly.gif
      :width: 320
      :align: center

      Eject towards the center.

.. only:: html

    .. figure:: images/split_eat_all.gif
      :width: 320
      :align: center

      Surround others by splitting.

.. only:: html

    .. figure:: images/fast_eat.gif
      :width: 320
      :align: center

      Eat food balls quickly.

.. only:: html

    .. figure:: images/eject_merger.gif
      :width: 422
      :align: center

      Concentrate size.



