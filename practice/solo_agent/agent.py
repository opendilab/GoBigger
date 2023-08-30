import torch
from practice.tools.util import default_collate_with_dim
from practice.tools.features import Features
from practice.solo_agent.model import Model
from copy import deepcopy
from easydict import EasyDict
import torch

class AIAgent:

    def __init__(self, team_name, player_names):
        cfg = EasyDict({
            'env': {
                'name': 'gobigger',
                'player_num_per_team': 1,
                'team_num': 2,
            },
            'agent': {
                'player_id': None,
                'game_player_id': None,
                'features': {}
            },
            'checkpoint_path': 'PATH/MODEL_NAME.pth.tar',
        })
        self.agents = {}
        for player_name in player_names:
            cfg_cp = deepcopy(cfg)
            cfg_cp.agent.player_id = player_name
            cfg_cp.agent.game_player_id = player_name
            agent = Agent(cfg_cp)
            agent.reset()
            agent.model.load_state_dict(torch.load(cfg.checkpoint_path, map_location='cpu')['model'], strict=False)
            self.agents[player_name] = agent

    def get_actions(self, obs):
        global_state, player_states = obs
        actions = {}
        for player_name, agent in self.agents.items():
            action = agent.step([global_state, {player_name: player_states[player_name]}])
            actions.update(action)
        return actions

class Agent:

    def __init__(self, cfg=None, ):
        self.whole_cfg = cfg
        self.cfg = self.whole_cfg.agent
        # setup model
        self.use_action_mask = self.whole_cfg.agent.get('use_action_mask', False)
        self.player_num = self.whole_cfg.env.player_num_per_team
        self.team_num = self.whole_cfg.env.team_num
        self.game_player_id = self.whole_cfg.agent.game_player_id
        self.game_team_id = self.game_player_id // self.player_num
        self.features = Features(self.whole_cfg)
        self.device = 'cpu'
        self.model = Model(self.whole_cfg)
    
    def transform_action(self, agent_outputs, env_status, eval_vsbot=False):
        env_num = len(env_status)
        actions_list = agent_outputs['action'].cpu().numpy().tolist()
        actions = {}
        for env_id in range(env_num):
            actions[env_id] = {}
            game_player_num = self.player_num if eval_vsbot else self.player_num * self.team_num
            for game_player_id in range(game_player_num):
                action_idx = actions_list[env_id * (game_player_num) + game_player_id]
                env_status[env_id].last_action_types[game_player_id] = action_idx
                actions[env_id][game_player_id] = self.features.transform_action(action_idx)
        return actions

    ########## only for submission####################    
    def reset(self):
        self.last_action_type = {}
        for player_id in range(self.player_num*self.game_team_id, self.player_num*(self.game_team_id+1)):
            self.last_action_type[player_id] = self.features.direction_num * 2
    
    def step(self, obs):
        """
        Overview:
            Agent.step() in submission
        Arguments:
            - obs
        Returns:
            - action
        """
        # preprocess obs
        env_team_obs = []
        for player_id in range(self.player_num*self.game_team_id, self.player_num*(self.game_team_id+1)):
            game_player_obs = self.features.transform_obs(obs, game_player_id=player_id,
                                            last_action_type=self.last_action_type[player_id])
            env_team_obs.append(game_player_obs)
        env_team_obs = stack(env_team_obs)
        obs = default_collate_with_dim([env_team_obs], device=self.device)
        
        # policy
        self.model_input = obs
        with torch.no_grad():
            model_output = self.model(self.model_input)['action'].cpu().detach().numpy()
            
        actions = []
        for i in range(len(model_output)):
            actions.append(self.features.transform_action(model_output[i]))
        ret = {}
        for player_id, act in zip(range(self.player_num*self.game_team_id, self.player_num*(self.game_team_id+1)), actions):
            ret[player_id] = act
        for player_id, act in zip(range(self.player_num*self.game_team_id, self.player_num*(self.game_team_id+1)), model_output):
            self.last_action_type[player_id] = act.item() # TODO
        return ret
    ####################################################

def stack(data):
    result = {}
    for k1 in data[0].keys():
        result[k1] = {}
        if isinstance(data[0][k1], dict):
            for k2 in data[0][k1].keys():
                result[k1][k2] = torch.stack([o[k1][k2] for o in data])
        else:
            result[k1] = torch.stack([o[k1] for o in data])
    return result