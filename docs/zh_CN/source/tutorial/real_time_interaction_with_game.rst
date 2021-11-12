实时游玩
##########################################

GoBigger 允许用户在个人电脑中实时游玩。同时也提供了多种游戏模式供用户选择。

.. note::

    如果你还在使用 GoBigger v0.1.0 版本，建议升级以获得更好的体验。可以使用 ``pip install --upgrade gobigger`` 来快速获得最新版本的 GoBigger。

单人游玩
--------------------

如果用户想要体验游戏的具体内容，可以选择单人游玩模式。可以通过以下代码启动游戏：

.. code-block:: bash

    python -m gobigger.bin.play --player-num 1 --vision-type full

在本模式中，键盘的上下左右箭头可以用来操控玩家控制的球，三个技能分别是``Q``，``W``，``E``。``Q`` 技能是在移动方向上吐孢子，``W`` 技能是将用户的球进行分裂，``E`` 技能是将用户的球停止并集中。

双人游玩
--------------------

如果你想和朋友一起游玩的话，可以使用以下代码启动双人游戏环境：

.. code-block:: bash

    python -m gobigger.bin.play --player-num 2 --vision-type full

在本模式中，玩家一依然使用上下左右箭头来进行移动控制，并使用 ``[``，``]``，``\\`` 分别对应吐孢子，分裂，以及停止技能。玩家二使用 ``W`` & ``S`` & ``A`` & ``D`` 来进行移动控制，使用 ``1``，``2``，``3`` 来实现吐孢子，分裂，以及停止技能。


部分视野下的单人游玩
----------------------------------------

上述的两种游玩方式都是在全局视野下的。为了让用户能够体验到 AI 所能够获得的 obs，GoBigger提供了部分视野下的单人游玩模式。该模式下，玩家只能看到周围一定范围内的视野。可以通过以下代码来启动游戏：

.. code-block:: bash

    python -m gobigger.bin.play --player-num 1 --vision-type partial

玩家的视野由球的相对位置决定。尝试分散玩家的球，这样可以获得更大的视野。


与bot对抗的单人游玩
----------------------------------------

如果你想和bot进行对抗，可以通过以下代码来启动游戏：

.. code-block:: bash

    python -m gobigger.bin.play --vs-bot

你也可以往游戏里添加更多的bot，通过指定 ``--team-num`` 来实现这一功能。

.. code-block:: bash

    python -m gobigger.bin.play --vs-bot --team-num 4