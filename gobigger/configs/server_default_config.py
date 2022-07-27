server_default_config = dict(
    team_num=4, # the number of team in a game
    player_num_per_team=3, # the number of players in a team in a game
    map_width=128, # map width
    map_height=128, # map height
    frame_limit=60*12*20, # the number of frames in a game
    fps=20, # the number of frame in each second
    collision_detection_type='precision', # type of collision detection 
    match_ratio=1.0, # match_ratio will be multiple to manager to control ball num
    eat_ratio=1.3, # ball A could eat ball B only when the size_A > eat_ratio * size_B
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
            num_init=800, # initial number
            num_min=800, # Minimum number
            num_max=900, # Maximum number
            refresh_frame_freq=8, # Time interval (seconds) for refreshing food in the map
            refresh_percent=0.01, # The number of refreshed foods in the map each time
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                score_min=100, # radius=0.438,  # score = 100
                score_max=100,
            ),
        ),
        # thorns setting
        thorns_manager=dict(
            num_init=9, # initial number
            num_min=9, # Minimum number
            num_max=12, # Maximum number
            refresh_frame_freq=120, # Time interval (seconds) for refreshing thorns in the map
            refresh_percent=0.2, # The number of refreshed  thorns in the map each time
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                score_min=10000, # 2.086
                score_max=15000, # 2.540
                eat_spore_vel_init=10, 
                eat_spore_vel_zero_frame=20,
            ),
        ),
        # player setting
        player_manager=dict(
            ball_settings=dict(  # The specific parameter description can be viewed in the ball module
                acc_weight=30,
                vel_max=50,
                score_init=1000, # 0.755,
                part_num_max=16,
                on_thorns_part_num=10,
                on_thorns_part_score_max=5000,
                split_score_min=3600,  # radius = 1.289
                eject_score_min=3200,  # radius = 1.222
                recombine_frame=400,
                split_vel_zero_frame=14,
                score_decay_min=2600, 
                score_decay_rate_per_frame=0.00005, # * sqrt(radius)
                center_acc_weight=10,
            ),
        ),
        # spore setting
        spore_manager=dict(
            ball_settings=dict( # The specific parameter description can be viewed in the ball module
                score_init=1400, # 0.859
                vel_init=30,
                vel_zero_frame=20,
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
