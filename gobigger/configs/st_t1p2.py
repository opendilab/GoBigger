from easydict import EasyDict
from gobigger.utils import deep_merge_dicts
from .server_default_config import server_default_config

cfg_ori = EasyDict(server_default_config)
st_t1p2 = EasyDict(dict(
    team_num=1,
    player_num_per_team=2,
    map_width=48,
    map_height=48,
    frame_limit=60*3*20,
    manager_settings=dict(
        food_manager=dict(
            num_init=130,
            num_min=130,
            num_max=150,
        ),
        thorns_manager=dict(
            num_init=2,
            num_min=2,
            num_max=3,
        ),
        player_manager=dict(
            ball_settings=dict(
                score_init=1000,
            ),
        ),
    ),
))
st_t1p2 = deep_merge_dicts(cfg_ori, st_t1p2)
