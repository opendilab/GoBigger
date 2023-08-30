import torch.nn as nn

from .network.nn_module import fc_block
from .network.res_block import ResFCBlock


class PolicyHead(nn.Module):
    def __init__(self, cfg):
        super(PolicyHead, self).__init__()
        self.whole_cfg = cfg
        self.cfg = self.whole_cfg.model.policy

        self.embedding_dim = self.cfg.embedding_dim
        self.project_cfg = self.cfg.project
        self.project = fc_block(in_channels=self.project_cfg.input_dim,
                                out_channels=self.embedding_dim,
                                activation= self.project_cfg.activation,
                                norm_type=self.project_cfg.norm_type)

        self.resnet_cfg = self.cfg.resnet
        blocks = [ResFCBlock(in_channels=self.embedding_dim,
                             activation=self.resnet_cfg.activation,
                             norm_type=self.resnet_cfg.norm_type)
                  for _ in range(self.resnet_cfg.res_num)]
        self.resnet = nn.Sequential(*blocks)

        self.direction_num = self.whole_cfg.agent.features.get('direction_num', 12)
        self.action_num = 2 * self.direction_num + 3
        self.output_layer = fc_block(in_channels=self.embedding_dim,
                                  out_channels=self.action_num,
                                  norm_type=None,
                                  activation=None)

    def forward(self, x, temperature=1):
        x = self.project(x)
        x = self.resnet(x)
        logit = self.output_layer(x)
        logit /= temperature
        return logit


class ValueHead(nn.Module):
    def __init__(self, cfg):
        super(ValueHead, self).__init__()
        self.whole_cfg = cfg
        self.cfg = self.whole_cfg.model.value

        self.embedding_dim = self.cfg.embedding_dim
        self.project_cfg = self.cfg.project
        self.project = fc_block(in_channels=self.project_cfg.input_dim,
                                out_channels=self.embedding_dim,
                                activation= self.project_cfg.activation,
                                norm_type=self.project_cfg.norm_type)

        self.resnet_cfg = self.cfg.resnet
        blocks = [ResFCBlock(in_channels=self.embedding_dim,
                             activation=self.resnet_cfg.activation,
                             norm_type=self.resnet_cfg.norm_type)
                  for _ in range(self.resnet_cfg.res_num)]
        self.resnet = nn.Sequential(*blocks)

        self.output_layer = fc_block(in_channels=self.embedding_dim,
                                  out_channels=1,
                                  norm_type=None,
                                  activation=None)
    def forward(self, x):
        x = self.project(x)
        x = self.resnet(x)
        x = self.output_layer(x)
        x = x.squeeze(1)
        return x