from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t3p2 = EasyDict(dict(
    team_num=3,
    player_num_per_team=2,
    map_width=88,
    map_height=88,
    frame_limit=60*3*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=500,
            num_min=500,
            num_max=560,
        ),
        thorns_manager=dict(
            num_init=5,
            num_min=5,
            num_max=6,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=13000,
            ),
        ),
    ),
))
st_t3p2 = deep_merge_dicts(cfg_ori, st_t3p2)
