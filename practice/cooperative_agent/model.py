import os
import torch
import torch.nn as nn
from ..tools.util import read_config, deep_merge_dicts
from ..tools.encoder import Encoder
from ..tools.head import PolicyHead, ValueHead

default_config = read_config(os.path.join(os.path.dirname(__file__), 'default_model_config.yaml'))

class Model(nn.Module):
    def __init__(self, cfg={}, use_value_network=False):
        super(Model, self).__init__()
        self.whole_cfg = deep_merge_dicts(default_config, cfg)
        self.model_cfg = self.whole_cfg.model
        self.use_value_network = use_value_network
        self.encoder = Encoder(self.whole_cfg)
        self.policy_head = PolicyHead(self.whole_cfg)
        self.temperature = self.whole_cfg.agent.get('temperature', 1)

    # used in rl_eval actor
    def compute_action(self, obs, ):
        action_mask = obs.pop('action_mask',None)
        embedding = self.encoder(obs, )
        logit = self.policy_head(embedding, temperature=self.temperature)
        if action_mask is not None:
            logit.masked_fill_(mask=action_mask,value=-1e9)
        dist = torch.distributions.Categorical(logits=logit)
        action = dist.sample()
        return {'action': action, 'logit': logit}