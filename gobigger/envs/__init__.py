from .gobigger_env import GoBiggerEnv
from .gobigger_sp_env import GoBiggerSPEnv

def create_env(env_name):
    '''
    env_name choice in ['standard']
    '''
    if env_name == 'standard':
        return GoBiggerEnv()

