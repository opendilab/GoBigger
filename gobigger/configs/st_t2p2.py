from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t2p2 = EasyDict(dict(
    team_num=2,
    player_num_per_team=2,
    map_width=64,
    map_height=64,
    frame_limit=60*3*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=260,
            num_min=260,
            num_max=300,
        ),
        thorns_manager=dict(
            num_init=3,
            num_min=3,
            num_max=4,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=13000,
            ),
        ),
    ),
))
st_t2p2 = deep_merge_dicts(cfg_ori, st_t2p2)
