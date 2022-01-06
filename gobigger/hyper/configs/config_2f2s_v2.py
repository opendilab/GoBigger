# 侧涨
server_default_config = dict(
    team_num=2, 
    player_num_per_team=2, 
    map_width=300,
    map_height=300, 
    match_time=10,
    state_tick_per_second=10, # frame
    action_tick_per_second=5, # frame
    collision_detection_type='precision',
    save_video=False,
    save_quality='high', # ['high', 'low']
    save_path='',
    save_bin=False, # save bin to go-explore
    load_bin=False,
    load_bin_path='',
    load_bin_frame_num = 'all',
    jump_to_frame_file = '',
    manager_settings=dict(
        # food setting
        food_manager=dict(
            num_init=180, # initial number
            num_min=180, # Minimum number
            num_max=225, # Maximum number
            refresh_time=2, # Time interval (seconds) for refreshing food in the map
            refresh_num=0, # The number of refreshed foods in the map each time
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                radius_min=2,
                radius_max=2,
            ),
        ),
        # thorns setting
        thorns_manager=dict(
            num_init=1, # initial number
            num_min=1, # Minimum number
            num_max=2, # Maximum number
            refresh_time=6, # Time interval (seconds) for refreshing thorns in the map
            refresh_num=0, # The number of refreshed  thorns in the map each time
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                radius_min=12, 
                radius_max=20, 
                vel_max=100,
                eat_spore_vel_init=10, 
                eat_spore_vel_zero_time=1,
            )
        ),
        # player setting
        player_manager=dict(
            ball_settings=dict(  # The specific parameter description can be viewed in the ball module
                acc_max=100, 
                vel_max=25,
                radius_min=3, 
                radius_max=300, 
                radius_init=3, 
                part_num_max=16, 
                on_thorns_part_num=10, 
                on_thorns_part_radius_max=20,
                split_radius_min=10, 
                eject_radius_min=10, 
                recombine_age=20,
                split_vel_init=30,
                split_vel_zero_time=1, 
                stop_zero_time=1,
                size_decay_rate=0.00005, 
                given_acc_weight=10,
            )
        ),
        # spore setting
        spore_manager=dict(
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                radius_min=3, 
                radius_max=3, 
                vel_init=250,
                vel_zero_time=0.3, 
                spore_radius_init=20, 
            )
        )   
    ),
    custom_init=dict(
        food=[], # only position and radius
        thorns=[[300, 300, 16]], # only position and radius
        spore=[], # only position and radius
        clone=[[80, 100, 16, '0', '0'], [130, 100, 10, '1', '0'], 
               [130, 115, 12, '2', '1'], [300, 300, 3, '3', '1']],
    ),
    obs_settings=dict(
        with_spatial=True,
        with_speed=False,
        with_all_vision=False,
    ),
)
