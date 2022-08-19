from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t3p2 = EasyDict(dict(
    team_num=3,
    player_num_per_team=2,
    map_width=80,
    map_height=80,
    frame_limit=60*3*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=300,
            num_min=300,
            num_max=360,
        ),
        thorns_manager=dict(
            num_init=4,
            num_min=4,
            num_max=5,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=13000,
            ),
        ),
    ),
))
st_t3p2 = deep_merge_dicts(cfg_ori, st_t3p2)
