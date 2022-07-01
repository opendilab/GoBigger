import logging
import pytest
import uuid
from pygame.math import Vector2

from gobigger.managers import PlayerSPManager
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.players import HumanSPPlayer
from gobigger.balls import CloneBall

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.unittest
class TestPlayerManager:

    def get_manager(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = PlayerSPManager(cfg=cfg.manager_settings.player_manager, border=border,
                                         team_num=cfg.team_num, player_num_per_team=cfg.player_num_per_team, 
                                         spore_manager_settings=cfg.manager_settings.spore_manager)
        return player_manager

    def test_init(self):
        player_manager = self.get_manager()
        assert True

    def test_init_bals(self):
        cfg = Server.default_config()
        player_manager = self.get_manager()
        player_manager.init_balls()
        assert len(player_manager.players) == cfg.team_num * cfg.player_num_per_team

    def test_get_bals(self):
        player_manager = self.get_manager()
        player_manager.init_balls()
        balls = player_manager.get_balls()
        assert isinstance(balls, list)

    def test_get_players(self):
        cfg = Server.default_config()
        player_manager = self.get_manager()
        player_manager.init_balls()
        players = player_manager.get_players()
        assert len(players) == cfg.team_num * cfg.player_num_per_team

    def test_get_player_by_name(self):
        player_manager = self.get_manager()
        player_manager.init_balls()
        players = player_manager.get_players()
        player = player_manager.get_player_by_name(players[0].player_id)
        assert isinstance(player, HumanSPPlayer)

    def test_add_balls(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        players = player_manager.get_players()
        player_id = players[0].player_id
        num_old = len(player_manager.get_balls())
        ball = CloneBall(player_manager.sequence_generator.get(), border.sample(), border=border, radius=4, team_id=players[0].team_id, player_id=player_id, sequence_generator=player_manager.sequence_generator)
        player_manager.add_balls(ball)
        num_new = len(player_manager.get_balls())
        assert num_new - num_old == 1
        ball1 = CloneBall(player_manager.sequence_generator.get(), border.sample(), border=border, radius=4, team_id=players[0].team_id, player_id=player_id, sequence_generator=player_manager.sequence_generator)
        ball2 = CloneBall(player_manager.sequence_generator.get(), border.sample(), border=border, radius=4, team_id=players[0].team_id, player_id=player_id, sequence_generator=player_manager.sequence_generator)
        balls = [ball1, ball2]
        player_manager.add_balls(balls)

    def test_remove_balls(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        players = player_manager.get_players()
        player_id = players[0].player_id
        ball = CloneBall(player_manager.sequence_generator.get(), border.sample(), border=border, radius=4, team_id=players[0].team_id, player_id=player_id, sequence_generator=player_manager.sequence_generator)
        player_manager.add_balls(ball)
        num_old = len(player_manager.get_balls())
        player_manager.remove_balls(ball)
        num_new = len(player_manager.get_balls())
        assert num_new - num_old == -1
        ball1 = CloneBall(player_manager.sequence_generator.get(), border.sample(), border=border, radius=4, team_id=players[0].team_id, player_id=player_id, sequence_generator=player_manager.sequence_generator)
        ball2 = CloneBall(player_manager.sequence_generator.get(), border.sample(), border=border, radius=4, team_id=players[0].team_id, player_id=player_id, sequence_generator=player_manager.sequence_generator)
        balls = [ball1, ball2]
        player_manager.remove_balls(balls)

    def test_step(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        balls = player_manager.get_balls()
        player_manager.remove_balls(balls[0])
        num_old = len(player_manager.get_balls())
        player_manager.step()
        num_new = len(player_manager.get_balls())
        assert num_new - num_old == 1

    def test_adjust(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        player_manager.adjust()

    def test_get_clone_num(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        balls = player_manager.get_balls()
        assert player_manager.get_clone_num(balls[0]) == 1
        player_manager.remove_balls(balls[0])
        assert player_manager.get_clone_num(balls[0]) == 0

    def test_get_player_names(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        player_names = player_manager.get_player_names()
        assert len(player_names) == cfg.team_num * cfg.player_num_per_team

    def test_get_team_names(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        team_names = player_manager.get_team_names()
        assert len(team_names) == cfg.team_num
    
    def test_get_player_names_with_team(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        player_names_with_team = player_manager.get_player_names_with_team()
        assert len(player_names_with_team) == cfg.team_num
        assert len(player_names_with_team[0]) == cfg.player_num_per_team

    def test_reset(self):
        cfg = Server.default_config()
        border = Border(0, 0, cfg.map_width, cfg.map_height)
        player_manager = self.get_manager()
        player_manager.init_balls()
        player_names_with_team = player_manager.get_player_names_with_team()
        assert len(player_names_with_team) == cfg.team_num
        assert len(player_names_with_team[0]) == cfg.player_num_per_team
        player_manager.reset()
        assert len(player_manager.players) == 0
