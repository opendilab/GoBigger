from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t1p1 = EasyDict(dict(
    team_num=1,
    player_num_per_team=1,
    map_width=32,
    map_height=32,
    frame_limit=60*3*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=65,
            num_min=65,
            num_max=75,
        ),
        thorns_manager=dict(
            num_init=1,
            num_min=1,
            num_max=2,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=1000,
            ),
        ),
    ),
))
st_t1p1 = deep_merge_dicts(cfg_ori, st_t1p1)
