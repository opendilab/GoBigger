Derived Environments and Action Spaces
################

Overview
=======================

On the basis of the GoBigger environment, considering the complexity of large-scale environment training and
algorithm verification for specific tasks, we provide some small environments under specific conditions,
as well as advanced serialization actions to facilitate training and algorithm design.


small environment
=======================

We provide the initialization method of the small environment by providing config.


* The clone fits the ball, the clone holds the ball (2f2s)

    There are only two teams in this small environment, and there are two players in each team.
There will also be food summed thorn balls in the same scale in the map. In this map, the blue A ball
only needs to split to the right, while the blue B ball needs to eat the small ball split by the blue A ball
and move down, and eat the yellow A by splitting (or moving). ball.

    .. only:: html

        .. figure:: images/2f2s.png
          :width: 300
          :align: center


* Measured increase (2f2s_v2)

    This small environment is the v2 version of 2f2s. In this map, the blue A ball only needs to split
to the right, while the blue B ball remains stationary to eat the yellow A ball.

    .. only:: html

        .. figure:: images/2f2s_v2.png
          :width: 300
          :align: center


* Measured increase (2f2s_v3)

    This small environment is the v3 version of 2f2s. In this map, the blue A ball needs to split between
the yellow ball and the blue B ball and spore the center, while the blue B ball moves down to eat the yellow A ball.

    .. only:: html

        .. figure:: images/2f2s_v3.png
          :width: 300
          :align: center


Advanced Serialization Actions
=======================

Please check ``gobigger/hyper/tests`` to get more details on serialization actions.


* Straight line

    .. only:: html

        .. figure:: images/straight_merge.gif
          :width: 362
          :align: center


* Four point ball

    .. only:: html

        .. figure:: images/quarter_merge.gif
          :width: 362
          :align: center


* Eights

    .. only:: html

        .. figure:: images/eighth_merge.gif
          :width: 338
          :align: center
