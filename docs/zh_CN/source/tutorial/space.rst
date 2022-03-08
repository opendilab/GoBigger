游戏空间设计
##############


动作空间
======================

由于玩家操控的每个球只能进行移动，吐孢子，分裂，停止，因此 GoBigger 的动作空间是比较简单的：

.. code-block:: python

    action = [x, y, action_type]

* x, y: 是单位圆中的一个点 ``(x, y)``，用来代表玩家对球的加速度的操控. 
    * GoBigger 会对加速度进行归一化，保证其的模长不会超过 1。
    * 如果用户不提供加速度变化，可以提供 (None, None) 表示不对移动进行改变。

* action_type: Int
    * -1 代表无动作，意味着继续维持上一帧的速度
    * 0 代表在给定方向上吐孢子。如果方向无指定，则在移动方向上执行。并修改移动方向为给定方向。
    * 1 代表在给定方向上进行分裂。如果方向无指定，则在移动方向上执行。并修改移动方向为给定方向。
    * 2 代表停止运动并将所有的分身球聚集起来
    * 3 代表在给定方向上吐孢子。如果方向无指定，则在移动方向上执行。不修改移动方向。
    * 4 代表在给定方向上进行分裂。如果方向无指定，则在移动方向上执行。不修改移动方向。

我们希望玩家可以更灵活的使用分身球的各个技能，并希望运动方向不会对技能的选择有所限制。因此，我们允许玩家在使用技能时指定的方向和运动的方向可以不同。例如，当玩家的分身球正在往右运动时，如果想要往下吐孢子，只需要指定 ``action_type=3`` 并同时指定 ``(x, y)``，分身球即可一边往右继续移动，一边往下吐孢子。下面给出了一个简单的例子。同样，在玩家使用分裂技能的时候也可以通过指定 ``action_type=3`` 来使得动作方向与运动方向不一致。

.. only:: html

    .. figure:: images/eject_and_move.gif
      :width: 300
      :align: center


向环境提交动作
--------------

对于多个玩家的情况，需要指定每个动作与玩家的对应关系。因此，可以遵循如下代码来提交动作：

.. code-block:: python

    player_names = server.get_player_names() # get all names in server
    actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] for player_name in player_names)}
    server.step(actions)


状态空间
======================

每当 ``server.obs()`` 被调用时，用户可以获取到分身球视野下的游戏状态。

.. code-block:: python

    global_state, player_state = server.obs()

``global_state`` 具体如下：

.. code-block:: python

    {
        'border': [map_width, map_height], # the map size
        'total_time': match_time, # the duration of a game
        'last_time': last_time,   # the length of time a game has been played
        'leaderboard': {
            team_name: team_size
        } # the team with its size in this game
    }

``player_state`` 具体如下：

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

``player_state`` 中的 ``overlap`` 代表的是当前玩家视野中出现的球的结构化信息。``overlap`` 是一个简单的字典，每个键值对代表了视野中的一种球的信息。``overlap`` 中包含了食物球，荆棘球，孢子球，分身球的结构化信息（位置和半径，如果是分身球则包含所属玩家名称和队伍名称）。具体来说，例如我们发现 ``food`` 字段的内容为 ``[[3.0, 4.0, 2], ..]`` （简单起见这里只展示了列表中的第一个元素），那么其中的含义是玩家的视野中，坐标 ``(3.0, 4.0)`` 位置存在一个半径为 ``2`` 的食物球。

请注意，每一种球的信息列表的长度是不确定的。例如，在当前帧视野中一共有20个食物球，那么当前 ``food`` 对应的列表长度为20。在下一帧，视野内的食物球如果变为25，则对应的列表长度将会变成25。 此外，如果某个球只有一部分出现在玩家视野中，GoBigger也会在 ``overlap`` 中给出该球的圆心和半径信息。

GoBigger 定义 ``player_state`` 中的 ``feature_layers`` 为当前玩家所能获得的 2D 空间信息。``feature_layers`` 由多个 channel 组成，每个 channel 给出了视野内某一种球的所有信息。比如，在某场比赛中，有 4 支队伍，每支队伍由 3 名玩家组成。因此，我们在游戏中获得的 ``feature_layers`` 将会是一个长度为 15 的 list。其中的每个元素含义如下：

* channel 0: 视野内玩家0的分身球所处位置。例如玩家0的某个分身球出现在了视野内左上角，那么左上角对应的位置会被置为1，其余部分为0。

* channel 1: 视野内玩家1的分身球所处位置。

* channel 2: 视野内玩家2的分身球所处位置。

* channel 3: 视野内玩家3的分身球所处位置。

* channel 4: 视野内玩家4的分身球所处位置。

* channel 5: 视野内玩家5的分身球所处位置。

* channel 6: 视野内玩家6的分身球所处位置。

* channel 7: 视野内玩家7的分身球所处位置。

* channel 8: 视野内玩家8的分身球所处位置。

* channel 9: 视野内玩家9的分身球所处位置。

* channel 10: 视野内玩家10的分身球所处位置。

* channel 11: 视野内玩家11的分身球所处位置。

* channel 12: 视野内食物球所处位置。

* channel 13: 视野内孢子球所处位置。

* channel 14: 视野内荆棘球所处位置。


状态空间 - 自定义
============================================

除了上述的状态空间以外，GoBigger 还支持不同种类的状态空间。用户可以在 server 的输入 cfg 中通过修改 ``obs_settings`` 来实现。

.. code-block:: python

    server = Server(cfg=dict(
        ...
        obs_settings=dict(
            with_spatial=True,
            with_speed=False,
            with_all_vision=False,
            cheat=False,
        ),
    ))

下面我们介绍 ``obs_settings`` 中各个值的作用。

携带 Spatial 信息
------------------

实际上，在游戏环境返回给用户的状态信息中，``feature_layers`` and ``overlap`` 二者包含的信息内容是一致的，只不过给出的形式不同。因此，我们可以通过设置在获取状态中不包含 ``feature_layers`` 来减少 ``server.obs()`` 的时间消耗。可以通过指定 ``with_spatial=False`` 来指定。

携带速度信息
------------------

我们可以对同一个球通过计算帧间相对位置来获取到该球的运动速度信息。为了减轻用户的负担，GoBigger 提供了 ``with_speed=True`` 来帮助用户直接在 observation 中获取到所有球的速度信息。一旦指定了 ``with_speed=True``，用户获取到的 ``overlap`` 中将会在对应元素中添加 ``speed`` 信息，来表示该球的运动速度。速度是矢量，因此会存在 ``speed.x`` 和 ``speed.y``。例如，添加了速度信息之后的 ``player_state`` 将如下所示。 请注意列表中不同元素的顺序。

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

    ``overlap`` 中只有 ``spore``，``thorn``，以及 ``clone`` 会含有速度信息。

获取全局视野
------------------

局部视野的存在可能会使得训练变得复杂。因此，GoBigger 提供了全局视野接口。通过指定 ``with_all_vision=True`` 来获取全局视野的信息。注意，在此模式下，由于不同玩家的视野是相同的，为了减少信息传输压力，我们只会在第一个玩家的信息字典中给出对应的全局视野信息。例如，假设一局游戏中有 2 个队伍，每个队伍中有 2 人，那么获取到的 ``player_state`` 将会如下：

.. code-block:: python

    {
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

请注意，除了 ``'0'`` 号玩家以外，其他玩家的信息中对应的 ``feature_layers`` 和 ``overlap`` 将会置为 ``None``。

获取全局视野+玩家局部视野
------------------------------------

在许多场景下，使用一些作弊信息（例如去掉战争迷雾）能够有效帮助算法收敛。因此，我们在获取全局视野的基础上，增加了同时获取全局视野和玩家局部视野的模式。通过指定 ``cheat=True`` 来获取。注意，在此模式下，``with_all_vision`` 的设置将会失效，因为会固定返回全局视野信息。例如，假设一局游戏中有 2 个队伍，每个队伍中有 1 人，那么获取到的 ``player_state`` 将会如下：

.. code-block:: python

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

请注意，全局视野信息放在了 ``all`` 字段下，其中的 ``team_name`` 被设置为空。其余玩家信息保持不变。
