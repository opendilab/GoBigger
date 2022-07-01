import importlib

from .gobigger_env import GoBiggerEnv
from .gobigger_sp_env import GoBiggerSPEnv
from gobigger.configs import *

def create_env_st(cfg):
    return GoBiggerEnv(cfg)

def create_env_sp(cfg):
    return GoBiggerSPEnv(cfg)

def create_env(env_name):
    '''
    env_name choice in ['st_v0', 'sp_v0']
    '''
    if env_name.startswith('st'):
        cfg = importlib.import_module('gobigger.configs.{}'.format(env_name))
        return create_env_st(cfg)
    elif env_name.startswith('sp'):
        cfg = importlib.import_module('gobigger.configs.{}'.format(env_name))
        return create_env_sp(cfg)
    else:
        raise NotImplementedError

def create_env_custom(type, cfg=None):
    if type == 'st':
        create_env_st(cfg)
    elif type == 'sp':
        create_env_sp(cfg)
    else:
        raise NotImplementedError
