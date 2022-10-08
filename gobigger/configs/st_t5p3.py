from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t5p3 = EasyDict(dict(
    team_num=5,
    player_num_per_team=3,
    map_width=128,
    map_height=128,
    frame_limit=60*12*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=900,
            num_min=900,
            num_max=1000,
        ),
        thorns_manager=dict(
            num_init=10,
            num_min=12,
            num_max=12,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=1000,
            ),
        ),
    ),
))
st_t5p3 = deep_merge_dicts(cfg_ori, st_t5p3)
