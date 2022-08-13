from gobigger.utils import SequenceGenerator
from gobigger.players import HumanSPPlayer
from .player_manager import PlayerManager


class PlayerSPManager(PlayerManager):

    def __init__(self, cfg, border, team_num, player_num_per_team, spore_manager_settings, 
                 random_generator=None, sequence_generator=None):
        super(PlayerSPManager, self).__init__(cfg, border, team_num, player_num_per_team, spore_manager_settings, 
                                              random_generator=random_generator)
        if sequence_generator is not None:
            self.sequence_generator = sequence_generator
        else:
            self.sequence_generator = SequenceGenerator()

    def init_balls(self, custom_init=None):
        if custom_init is None or len(custom_init) == 0:
            for i in range(self.team_num):
                team_id = i
                for j in range(self.player_num_per_team):
                    player_id = i * self.player_num_per_team + j
                    player = HumanSPPlayer(cfg=self.cfg.ball_settings, team_id=team_id, player_id=player_id, 
                                           border=self.border, spore_settings=self.spore_settings,
                                           sequence_generator=self.sequence_generator)
                    player.respawn(position=self.border.sample())
                    self.players[player_id] = player
        else:
            raise NotImplementedError
