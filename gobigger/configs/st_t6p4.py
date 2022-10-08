from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t6p4 = EasyDict(dict(
    team_num=6,
    player_num_per_team=4,
    map_width=144,
    map_height=144,
    frame_limit=60*12*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=1000,
            num_min=1000,
            num_max=1100,
        ),
        thorns_manager=dict(
            num_init=11,
            num_min=13,
            num_max=13,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=1000,
            ),
        ),
    ),
))
st_t6p4 = deep_merge_dicts(cfg_ori, st_t6p4)
