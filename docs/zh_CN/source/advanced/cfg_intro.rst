游戏配置介绍
##############


总览
======================

为了让玩家更进一步了解游戏机制的实现，我们开放了部分参数供玩家进行调整。我们希望玩家可以通过修改对应的参数，来实现各种不同的环境。同时，也可以设计自己的代理环境，用于对算法的快速验证。

GoBigger 将可配置参数统一放在 ``gobigger/server/server_default_config.py``

配置细节
======================

下面将会对可配置参数进行详细介绍。

* ``team_num``: 游戏中的队伍数量，默认为4
* ``player_num_per_team``: 每支队伍中的玩家数量，默认为3 
* ``map_width``: 地图宽度。默认为1000
* ``map_height``: 地图高度，默认为1000
* ``match_time``: 单局游戏时长，默认为10分钟
* ``state_tick_per_second``: 每秒的状态帧数。每个状态帧都会对所有球的状态进行更新。默认为40
* ``action_tick_per_second``: 每秒的动作帧数。每个动作帧都会接收动作并在游戏中实现。默认为5
* ``collision_detection_type``: 碰撞检测算法的种类。默认是'precision'
* ``save_video``: 是否保存视频。默认为False
* ``save_quality``: 保存的视频质量。默认为'high'，可以是'low'
* ``save_path``: 保存视频路径。默认为空
* ``manager_settings``
    * ``food_manager``
        * ``num_init``: 地图中初始化的食物球数量，默认为2000
        * ``num_min``: 地图中食物球数量的最小值，默认为2000
        * ``num_max``: 地图中食物球数量的最大值，默认为2500
        * ``refresh_time``: 地图中刷新食物球的时间间隔（单位为秒），默认为2
        * ``refresh_num``: 每次刷新食物球的数量，默认为30
        * ``ball_settings``:
            * ``radius_min``: 食物球的最小半径，默认为2
            * ``radius_max``: 食物球的最大半径，默认为2
    * ``thorns_manager``
        * ``num_init``: 地图中初始化的荆棘球数量，默认为15
        * ``num_min``: 地图中荆棘球数量的最小值，默认为15
        * ``num_max``: 地图中荆棘球数量的最大值，默认为20
        * ``refresh_time``: 地图中刷新荆棘球的时间间隔（单位为秒），默认为2
        * ``refresh_num``: 每次刷新食物球的数量，默认为2
        * ``ball_settings``
            * ``radius_min``: 荆棘球的最小半径，默认为12
            * ``radius_max``: 荆棘球的最大半径，默认为20
            * ``vel_max``: 荆棘球的速度上限，默认为100
            * ``eat_spore_vel_init``: 荆棘球吃掉孢子球后的初始化速度模值大小，默认为10
            * ``eat_spore_vel_zero_time``: 荆棘球吃掉孢子球后速度归零所需时间（单位为秒），默认为1
    * ``player_manager``
        * ``ball_settings``
            * ``acc_max``: 分身球的加速度上限，默认为100
            * ``vel_max``: 分身球的速度上限，默认为25
            * ``radius_min``: 分身球的半径最小值，默认为3
            * ``radius_max``: 分身球的半径最大值，默认为300
            * ``radius_init``: 分身球的半径初始化值，默认为3
            * ``part_num_max``: 分身球的最大分裂数量，默认为16
            * ``on_thorns_part_num``: 分身球吃掉荆棘球之后的最大分裂数量，默认为10
            * ``on_thorns_part_radius_max``: 分身球吃掉荆棘球后得到的新的分身球的最大半径，默认为20
            * ``split_radius_min``: 分身球达到此半径时才能解锁分裂技能，默认为10
            * ``eject_radius_min``: 分身球达到此半径时才能解锁吐孢子技能，默认为10
            * ``recombine_age``: 分身球分裂之后能够融合的时间间隔（单位为秒），默认为20
            * ``split_vel_init``: 分身球分裂之后得到的新球的初始化速度，默认为30
            * ``split_vel_zero_time``: 分身球分裂之后得到的新球速度归零时间（单位为秒），默认为1
            * ``stop_zero_time``: 分身球使用停止技能后速度归零时间（单位为秒），默认为1
            * ``size_decay_rate``: 分身球每个状态帧体积衰减的比例，默认为0.00005
            * ``given_acc_weight``: 未启用
    * ``spore_manager``: 
        * ``ball_settings``: 
            * ``radius_min``: 孢子球的最小半径，默认为3
            * ``radius_max``: 孢子球的最大半径，默认为3
            * ``vel_init``: 孢子球的初始化速度，默认为250
            * ``vel_zero_time``: 孢子球速度归零时间（单位为秒），默认为0.3
            * ``spore_radius_init``: 未启用
* ``custom_init``: 自定义开局
    * ``food``: 自定义的食物球列表，需提供位置和半径，默认为空
    * ``thorns``: 自定义的荆棘球列表，需提供位置和半径，默认为空
    * ``spore``: 自定义的孢子球列表，需提供位置和半径，默认为空
    * ``clone``: 自定义的分身球列表，需提供位置、半径、玩家名称和队伍名称，默认为空
* ``obs_settings``: 自定义obs
    * ``with_spatial``: 是否携带spatial信息，默认为True
    * ``with_speed``: 食肉携带速度信息，默认为False
    * ``with_all_vision``: 是否全局视野，默认为False
