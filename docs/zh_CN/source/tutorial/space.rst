游戏空间设计
##############

标准比赛模式
**********************

标准比赛模式指的是和agar之类的游戏相同，玩家每帧只能提供一个动作，然后所有的玩家球都会执行这一个动作。

动作空间
======================

由于玩家操控的每个球只能进行移动，吐孢子，分裂，停止，因此 GoBigger 的动作空间是比较简单的：

.. code-block:: python

    action = [x, y, action_type]

* x, y: 是单位圆中的一个点 ``(x, y)``，用来代表玩家对球的加速度的操控. 
    * GoBigger 会对加速度进行归一化，保证其的模长不会超过 1。
    * 如果用户不提供加速度变化，可以提供 (None, None) 表示不对移动进行改变。

* action_type: Int
    * 0: move，实际上每次step都会进行move。
    * 1: 代表在给定方向上吐孢子。如果方向无指定，则在移动方向上执行。
    * 2: 代表在给定方向上进行分裂。如果方向无指定，则在移动方向上执行。

我们希望玩家可以更灵活的使用分身球的各个技能，并希望运动方向不会对技能的选择有所限制。因此，我们允许玩家在使用技能时指定的方向和运动的方向可以不同。例如，当玩家的分身球正在往右运动时，如果想要往下吐孢子，只需要指定 ``action_type=1`` 并同时指定 ``(x, y)``，分身球即可一边往右继续移动，一边往下吐孢子。下面给出了一个简单的例子。

.. only:: html

    .. figure:: images/eject_and_move.gif
      :width: 300
      :align: center

另外，通过x，y，与 action_type 的巧妙配合可以实现一些有用的操作。例如，在吐孢子的时候设置 x,y 均为 None，可以实现交叉吐孢子。例如：

.. only:: html

    .. figure:: images/eject_cross.gif
      :width: 300
      :align: center


向环境提交动作
--------------

对于多个玩家的情况，需要指定每个动作与玩家的对应关系。提交的动作应当是一个字典，每个 key-value-pair 应当是某个玩家在这一帧需要做的动作。因此，可以遵循如下代码来提交动作：

.. code-block:: python

    team_infos = env.get_team_infos()
    actions = {}
    for team_id, player_ids in team_infos.items():
        actions.update({player_id: [random.uniform(-1, 1), random.uniform(-1, 1), -1] for player_id in player_ids)})
    obs = env.step(actions)


状态空间
======================

在游戏的每次 step 之后，用户可以获取到分身球视野下的游戏状态。

.. code-block:: python

    obs, _, _, _ = env.step()
    global_state, player_states = obs

``global_state`` 包含一些全局信息，具体如下：

.. code-block:: python

    {
        'border': [map_width, map_height], # 地图大小
        'total_frame': total_frame, # 整局游戏的总帧数
        'last_frame_count': last_frame_count,   # 当前已经过去了的帧数
        'leaderboard': { team_name: team_size } # 当前的排行榜信息，包含每个队伍的分数。队伍的分数是队内玩家分数之和
    }

``player_states`` 包含了每个玩家所能获得的信息，根据 ``player_id`` 来区分，具体如下：

.. code-block:: python

    {
        player_id: {
            'rectangle': [left_top_x, left_top_y, right_bottom_x, right_bottom_y], # 视野框在全局视野中的位置
            'overlap': {
                'food': [[position.x, position.y, radius, score], ...],   # 视野内食物球信息，分别是位置xy，半径，分数
                'thorns': [[position.x, position.y, radius, score, vel.x, vel.y], ...], # 视野内荆棘球信息，分别是位置xy，半径，分数，当前速度xy
                'spore': [[position.x, position.y, radius, score, vel.x, vel.y, owner], ...],  # 视野内孢子球信息，分别是位置xy，半径，分数，当前速度xy，来自玩家的id
                'clone': [[[position.x, position.y, radius, score, vel.x, vel.y, direction.x, direction.y, 
                            player_id, team_id], ...], # 视野内玩家球信息，分别是位置xy，半径，分数，当前速度xy，当前方向xy，所属玩家id，所属队伍id
            }, 
            'team_name': team_name, # 当前玩家所属队伍id
            'score': player_score, # 当前玩家的得分
            'can_eject': bool, # 当前玩家能否执行吐孢子
            'can_split': bool, # 当前玩家能否执行分裂
        },
        ...
    }

``player_states`` 中的 ``overlap`` 代表的是当前玩家视野中出现的球的结构化信息。``overlap`` 是一个简单的字典，每个键值对代表了视野中的一种球的信息。``overlap`` 中包含了食物球，荆棘球，孢子球，分身球的结构化信息（位置和半径，如果是分身球则包含所属玩家名称和队伍名称）。具体来说，例如我们发现 ``food`` 字段的内容为 ``[[3.0, 4.0, 2, 2], ..]`` （简单起见这里只展示了列表中的第一个元素），那么其中的含义是玩家的视野中，坐标 ``(3.0, 4.0)`` 位置存在一个半径为 ``2`` 的食物球，同时这个食物球的分数是 ``2``。

请注意，每一种球的信息列表的长度是不确定的。例如，在当前帧视野中一共有20个食物球，那么当前 ``food`` 对应的列表长度为20。在下一帧，视野内的食物球如果变为25，则对应的列表长度将会变成25。 此外，如果某个球只有一部分出现在玩家视野中，GoBigger也会在 ``overlap`` 中给出该球的圆心和半径信息。


独立动作比赛模式
**********************

独立动作比赛模式指的是玩家每帧需要对他的所有玩家球提供动作。玩家的每个玩家球都可以独立执行动作。

动作空间
======================

最小动作单元和标准比赛模式是一样的，只是在进行 ``env.step(actions)`` 的时候，actions 的格式应该如下：

.. code-block:: python

    actions = {
        player_id: {
            ball_id: [x, y, action_type],
            ...
        },
        ...
    }

这里面的 ball_id 可以从每一帧拿到的 obs 来确定。每个 ball_id 会唯一对应到玩家的一个分身球。

状态空间
======================

大部分和标准比赛模式是一样的，唯一不同在于 clone 球部分会增加 ball_id 的信息。这个信息可以用来告诉玩家在提供 actions 的时候 ball_id 可以从这里拿。

``player_states`` 具体如下：

.. code-block:: python

    {
        player_id: {
            ...
            'overlap': {
                ...
                'clone': [[[position.x, position.y, radius, score, vel.x, vel.y, direction.x, direction.y, 
                            player_id, team_id, ball_id], ...], # 视野内玩家球信息，分别是位置xy，半径，当前速度xy，当前方向xy，所属玩家id，所属队伍id，球的id
            }, 
            ...
        }
    }
