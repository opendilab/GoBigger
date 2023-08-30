import os
from typing import Dict, Any
import numpy as np
import torch
import torch.nn as nn
from ..tools.util import read_config, deep_merge_dicts
from ..tools.encoder import Encoder
from ..tools.head import PolicyHead, ValueHead

default_config = read_config(os.path.join(os.path.dirname(__file__), 'default_model_config.yaml'))

class Model(nn.Module):
    def __init__(self, cfg={}, **kwargs):
        super(Model, self).__init__()
        self.whole_cfg = deep_merge_dicts(default_config, cfg)
        self.encoder = Encoder(self.whole_cfg)
        self.policy_head = PolicyHead(self.whole_cfg)
        self.value_head = ValueHead(self.whole_cfg)
        self.only_update_value = False
        self.ortho_init = self.whole_cfg.model.get('ortho_init', True)
        self.player_num = self.whole_cfg.env.player_num_per_team
        self.team_num = self.whole_cfg.env.team_num

    def forward(self, obs, temperature=0):
        obs = flatten_data(obs,start_dim=0,end_dim=1) # [env_num*team_num, 2]
        embedding = self.encoder(obs)
        logit = self.policy_head(embedding)
        if temperature == 0:
            action = logit.argmax(dim=-1)
        else:
            logit = logit.div(temperature)
            dist = torch.distributions.Categorical(logits=logit)
            action = dist.sample()
        return {'action': action, 'logit': logit}

    def compute_value(self, obs, ):
        obs = flatten_data(obs,start_dim=0,end_dim=1)
        embedding = self.encoder(obs)
        batch_size = embedding.shape[0] // self.team_num // self.player_num
        team_embedding = embedding.reshape(batch_size*self.team_num, self.player_num, -1)
        team_embedding = self.transform_ctde(team_embedding,device=team_embedding.device)
        value = self.value_head(team_embedding) # [bs, player_num, 1]
        return {'value': value.reshape(-1)}

    def compute_logp_action(self, obs, **kwargs, ):
        obs = flatten_data(obs,start_dim=0,end_dim=1)
        embedding = self.encoder(obs)
        batch_size = embedding.shape[0] // self.team_num // self.player_num
        logit = self.policy_head(embedding)
        dist = torch.distributions.Categorical(logits=logit)
        action = dist.sample()
        action_log_probs = dist.log_prob(action)
        log_action_probs = action_log_probs
        team_embedding = embedding.reshape(batch_size*self.team_num, self.player_num, -1)
        team_embedding = self.transform_ctde(team_embedding,device=team_embedding.device)
        value = self.value_head(team_embedding)
        return {'action': action,
                'action_logp': log_action_probs,
                'logit': logit,
                'value': value.reshape(-1),
                }

    def rl_train(self, inputs: dict, **kwargs) -> Dict[str, Any]:
        r"""
        Overview:
            Forward and backward function of learn mode.
        Arguments:
            - inputs (:obj:`dict`): Dict type data
        ArgumentsKeys:
            - obs shape     :math:`(T+1, B)`, where T is timestep, B is batch size
            - action_logp: behaviour logits, :math:`(T, B,action_size)`
            - action: behaviour actions, :math:`(T, B)`
            - reward: shape math:`(T, B)`
            - done:shape math:`(T, B)`
        Returns:
            - metric_dict (:obj:`Dict[str, Any]`):
              Including current total_loss, policy_gradient_loss, critic_loss and entropy_loss
        """

        obs = inputs['obs']        
        # flat obs
        obs = flatten_data(obs,start_dim=0,end_dim=1)
        embedding = self.encoder(obs, )
        batch_size = embedding.shape[0] // self.player_num
        logits = self.policy_head(embedding)
        critic_input = embedding.reshape(batch_size, self.player_num, -1)
        critic_input = self.transform_ctde(critic_input, device=critic_input.device)
        if self.only_update_value:
            critic_input = detach_grad(critic_input)
        values = self.value_head(critic_input)
        outputs = {
            'value': values.squeeze(-1).reshape(-1),
            'logit': logits,
            'action': inputs['action'].reshape(-1),
            'action_logp': inputs['action_logp'].reshape(-1),
            # 'reward': inputs['reward'],
            # 'done': inputs['done'],
            'old_value': inputs['old_value'].reshape(-1),
            'advantage': inputs['advantage'].reshape(-1),
            'return': inputs['return'].reshape(-1),
        }
        return outputs
    
    def transform_ctde(self, array, device):
        # player = A,B  array AB and BA
        ret = []
        for i in range(self.player_num):
            index = [i for i in range(self.player_num)]
            index.pop(i)
            other_array = torch.index_select(array, dim=1, index=torch.LongTensor(index).to(device))
            self_array = array[:,i,:].unsqueeze(dim=1)
            ret.append(torch.cat((self_array, other_array), dim=1).flatten(start_dim=1,end_dim=2).unsqueeze(1))
        ret = torch.cat(ret, dim=1)
        return ret

def flatten_data(data,start_dim=0,end_dim=1):
    if isinstance(data, dict):
        return {k: flatten_data(v,start_dim=start_dim, end_dim=end_dim) for k, v in data.items()}
    elif isinstance(data, torch.Tensor):
        return torch.flatten(data, start_dim=start_dim, end_dim=end_dim)