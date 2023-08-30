import torch
from practice.tools.util import default_collate_with_dim
from practice.tools.features import Features
from practice.cooperative_agent.model import Model
from copy import deepcopy
from easydict import EasyDict
import torch

class AIAgent:

    def __init__(self, team_name, player_names):
        cfg = EasyDict({
            'team_name': team_name,
            'player_names': player_names,
            'env': {
                'name': 'gobigger',
                'player_num_per_team': 2,
                'team_num': 2,
                'step_mul': 8
            },
            'agent': {
                'player_id': None,
                'game_player_id': None,
                'features': {}
            },
            'checkpoint_path': 'PATH/MODEL_NAME.pth.tar'
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

    def __init__(self, cfg,):
        self.whole_cfg = cfg
        self.player_num = self.whole_cfg.env.player_num_per_team
        self.team_num = self.whole_cfg.env.team_num
        self.game_player_id = self.whole_cfg.agent.game_player_id  # start from 0
        self.game_team_id = self.game_player_id // self.player_num # start from 0
        self.player_id = self.whole_cfg.agent.player_id
        self.features = Features(self.whole_cfg)
        self.eval_padding = self.whole_cfg.agent.get('eval_padding', False)
        self.use_action_mask = self.whole_cfg.agent.get('use_action_mask', False)
        self.model = Model(self.whole_cfg)

    def reset(self):
        self.last_action_type = self.features.direction_num * 2

    def preprocess(self, obs):
        self.last_player_score = obs[1][self.game_player_id]['score']
        if self.use_action_mask:
            can_eject = obs[1][self.game_player_id]['can_eject']
            can_split = obs[1][self.game_player_id]['can_split']
            action_mask = self.features.generate_action_mask(can_eject=can_eject,can_split=can_split)
        else:
            action_mask = self.features.generate_action_mask(can_eject=True,can_split=True)
        obs = self.features.transform_obs(obs, game_player_id=self.game_player_id,
                                          last_action_type=self.last_action_type,padding=self.eval_padding)
        obs = default_collate_with_dim([obs])

        obs['action_mask'] = action_mask.unsqueeze(0)
        return obs

    def step(self, obs):
        self.raw_obs = obs
        obs = self.preprocess(obs)
        self.model_input = obs
        with torch.no_grad():
            self.model_output = self.model.compute_action(self.model_input)
        actions = self.postprocess(self.model_output['action'].detach().numpy())
        return actions

    def postprocess(self, model_actions):
        actions = {}
        actions[self.game_player_id] = self.features.transform_action(model_actions[0])
        self.last_action_type = model_actions[0].item()
        return actions
