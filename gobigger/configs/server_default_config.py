server_default_config = dict(
    team_num=4, # the number of team in a game
    player_num_per_team=3, # the number of players in a team in a game
    map_width=256, # map width
    map_height=256, # map height
    frame_limit=60*10*20, # the number of frames in a game
    fps=20, # the number of frame in each second
    collision_detection_type='precision', # type of collision detection 
    match_ratio=1.0, # match_ratio will be multiple to manager to control ball num
    eat_ratio=pow(1.2, 1/3), # ball A could eat ball B only when the radius A > eat_ratio * radius B
    playback_settings=dict(
        save_video=False,
        save_fps=10,
        save_resolution=552,
        save_all=True,
        save_partial=False,
        save_dir='.',
        save_name_prefix='testvideo',
    ),
    opening_settings=dict(
        opening_type='none', # ['none', 'handcraft', 'from_frame']
        handcraft=dict(
            food=[], # only position and radius
            thorns=[], # only position and radius
            spore=[], # only position and radius
            clone=[], # only position and radius and player and team
        ),
        from_frame=dict(
            frame_path='',
        ),
    ),
    manager_settings=dict(
        # food setting
        food_manager=dict(
            num_init=2000, # initial number
            num_min=2000, # Minimum number
            num_max=2500, # Maximum number
            refresh_frame_freq=8, # Time interval (seconds) for refreshing food in the map
            refresh_percent=0.01, # The number of refreshed foods in the map each time
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                radius_min=0.5,
                radius_max=0.5,
            ),
        ),
        # thorns setting
        thorns_manager=dict(
            num_init=16, # initial number
            num_min=16, # Minimum number
            num_max=24, # Maximum number
            refresh_frame_freq=40, # Time interval (seconds) for refreshing thorns in the map
            refresh_percent=0.4, # The number of refreshed  thorns in the map each time
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                radius_min=2.4, 
                radius_max=3.0, 
                eat_spore_vel_init=10, 
                eat_spore_vel_zero_frame=20,
            ),
        ),
        # player setting
        player_manager=dict(
            ball_settings=dict(  # The specific parameter description can be viewed in the ball module
                acc_weight=30,
                vel_max=100,
                radius_init=1,
                part_num_max=16,
                on_thorns_part_num=10,
                on_thorns_part_radius_max=3,
                split_radius_min=1.6,
                eject_radius_min=1.5,
                recombine_frame=320,
                split_vel_init=40,
                split_vel_zero_frame=20,
                size_decay_radius_min=4, 
                size_decay_rate_per_frame=0.00005, # * sqrt(radius)
                center_acc_weight=10,
            ),
        ),
        # spore setting
        spore_manager=dict(
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                radius_init=1,
                vel_init=50,
                vel_zero_frame=10,
            ),
        )   
    ),
    obs_settings=dict(
        obs_type='partial', # ['partial', 'all']
        partial=dict(
            type='square', # ['circle', 'square']
            vision_x_min=10,
            vision_y_min=10,
            scale_up_ratio=1.8,
        )
    ),
)
