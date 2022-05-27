Configuration
##########################################


Overview
======================

In order to allow players to further understand the realization of the game mechanism, we have opened some parameters for players to adjust. We hope that players can modify the corresponding parameters to achieve a variety of different environments. At the same time, you can also design your own agent environment to quickly verify the algorithm.

GoBigger puts configurable parameters in ``gobigger/server/server_default_config.py``

Configuration details
======================

The configurable parameters will be described in detail below.

* ``team_num``: The number of teams in the game, the default is 4
* ``player_num_per_team``: the number of players in each team, the default is 3
* ``map_width``: The width of the map. The default is 1000
* ``map_height``: The height of the map. The default is 1000
* ``match_time``: the duration of a single game, the default is 10 minutes
* ``state_tick_per_second``: The number of state frames per second. Each status frame will update the status of all balls. The default is 40
* ``action_tick_per_second``: The number of action frames per second. Each action frame receives the action and implements it in the game. The default is 5
* ``collision_detection_type``: the type of collision detection algorithm. The default is precision
* ``save_video``: Whether to save the video. The default is False
* ``save_quality``: The quality of the video. The default is 'high', could be 'low'
* ``save_path``: The path to save the video. The default is empty
* ``save_bin``: Do you need to save the action sequence
* ``load_bin``: whether to load the action sequence
* ``load_bin_path``: The path to load the action sequence file
* ``load_bin_frame_num``: Load the action sequence to the first few frames
* ``jump_to_frame_file``: The path of the frame information file that needs to be jumped
* ``match_ratio``: match_ratio will be multiple to manager to control ball num. The default is 1.0
* ``manager_settings``
    * ``food_manager``
        * ``num_init``: The number of food balls initialized in the map, the default is 2000
        * ``num_min``: The minimum number of food balls in the map, the default is 2000
        * ``num_max``: The maximum number of food balls in the map, the default is 2500
        * ``refresh_time``: The time interval for refreshing the food ball in the map (in seconds), the default is 2
        * ``refresh_num``: The number of food balls refreshed each time, the default is 30
        * ``ball_settings``:
            * ``radius_min``: the minimum radius of the food ball, the default is 2
            * ``radius_max``: the maximum radius of the food ball, the default is 2
    * ``thorns_manager``
        * ``num_init``: The number of thorns balls initialized in the map, the default is 15
        * ``num_min``: The minimum number of thorns balls in the map, the default is 15
        * ``num_max``: The maximum number of thorns balls in the map, the default is 20
        * ``refresh_time``: The time interval for refreshing the thornball in the map (in seconds), the default is 2
        * ``refresh_num``: The number of food balls refreshed each time, the default is 2
        * ``ball_settings``
            * ``radius_min``: the minimum radius of the thorns ball, the default is 12
            * ``radius_max``: the maximum radius of the thorns ball, the default is 20
            * ``vel_max``: The upper limit of the speed of the thorns ball, the default is 100
            * ``eat_spore_vel_init``: The initial velocity modulus size of the thorn ball after eating the spore ball, the default is 10
            * ``eat_spore_vel_zero_time``: The time required for the speed of the thorn ball to return to zero after eating the spore ball (in second), the default is 1
    * ``player_manager``
        * ``ball_settings``
            * ``acc_max``: the upper limit of the acceleration of the clone, the default is 100
            * ``vel_max``: The upper limit of the speed of the clone, the default is 25
            * ``radius_min``: The minimum radius of the clone, the default is 3
            * ``radius_max``: The maximum radius of the clone, the default is 300
            * ``radius_init``: the initial value of the radius of the clone, the default is 3
            * ``part_num_max``: The maximum number of splits of the clone, the default is 16
            * ``on_thorns_part_num``: the maximum number of splits after the thorns ball is eaten by the clone, the default is 10
            * ``on_thorns_part_radius_max``: the maximum radius of the new clone ball obtained after the clone ball eats the thorns ball, the default is 20
            * ``split_radius_min``: Splitting skills can only be unlocked when the clone reaches this radius, the default is 10
            * ``eject_radius_min``: The spore-spitting skill can only be unlocked when the clone reaches this radius, the default is 10
            * ``recombine_age``: The time interval (in seconds) that the clone ball can merge after splitting, the default is 20
            * ``split_vel_init``: The initial speed of the new ball obtained after the split ball is split, the default is 30
            * ``split_vel_zero_time``: The time for the speed of the new ball to zero after the clone ball is split (in seconds), the default is 1
            * ``stop_zero_time``: The time for the clone ball to return to zero speed after using the stop skill (in second), the default is 1
            * ``size_decay_rate``: The volume decay ratio of each state frame, the default is 0.00005
            * ``given_acc_weight``: not enabled
    * ``spore_manager``:
        * ``ball_settings``:
            * ``radius_min``: the minimum radius of the spore ball, the default is 3
            * ``radius_max``: the maximum radius of the spore ball, the default is 3
            * ``vel_init``: Initialization speed of the spore ball, the default is 250
            * ``vel_zero_time``: the time for the velocity of the spore ball to return to zero (in seconds), the default is 0.3
            * ``spore_radius_init``: not enabled
* ``custom_init``: Customized opening
    * ``food``: Customized food ball list, need to provide location and radius, default is empty
    * ``thorns``: Customized thorns balls list, need to provide location and radius, default is empty
    * ``spore``: Customized spore ball list, need to provide location and radius, default is empty
    * ``clone``: Customized clone ball list, need to provide position, radius, player name and team name, the default is empty
* ``obs_settings``: Customized observation
    * ``with_spatial``: Whether to carry spatial information, the default is True
    * ``with_speed``: Whether to carry speed information, the default is False
    * ``with_all_vision``: Whether or not the global vision, the default is False
