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
    * -1 代表无动作
    * 0 代表在移动方向上吐孢子
    * 1 代表分裂
    * 2 代表停止运动并将所有的分身球聚集起来

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
                'food': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
                'thorns': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
                'spore': [{'position': position, 'radius': radius}, ...], # the length of food is not sure
                'clone': [{'position': position, 'radius': radius, 'player': player_name, 'team': team_name}, ...], # the length of food is not sure
            }, # all balls' info in vision
            'team_name': team_name, # the team which this player belongs to 
        }
    }

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


.. note::

    ``player_state`` 中的 ``overlap`` 代表的是当前玩家视野中出现的球的结构化信息。此外，如果某个球只有一部分出现在玩家视野中，GoBigger也会在 ``overlap`` 中给出该球的圆心和半径信息。

状态空间 - 不含 feature_layers
============================================

实际上，在游戏环境返回给用户的状态信息中，``feature_layers`` and ``overlap`` 二者包含的信息内容是一致的，只不过给出的形式不同。因此，我们可以通过设置在获取状态中不包含 ``feature_layers`` 来减少 ``server.obs()`` 的时间消耗。可以通过在初始化 ``EnvRender`` 时添加 ``use_spatial=False`` 来指定。

.. code-block:: python

    server = Server()
    render = EnvRender(server.map_width, server.map_height, use_spatial=False) # drop feature_layers
    server.set_render(render)
    server.start()

.. note::

    如果在渲染引擎中添加了 ``use_spatial=False``，用户将无法进行保存 demo 的操作，因为相关的渲染动作会被取消。
