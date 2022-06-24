import random
import math
import logging
import uuid
from abc import ABC, abstractmethod
from easydict import EasyDict
from pygame.math import Vector2

from .base_manager import BaseManager
from gobigger.utils import format_vector, Border
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall
from gobigger.players import HumanPlayer


class PlayerManager(BaseManager):

    def __init__(self, cfg, border, team_num, player_num_per_team, spore_manager_settings, random_generator=None):
        super(PlayerManager, self).__init__(cfg, border)
        self.players = {}
        self.team_num = team_num
        self.player_num_per_team = player_num_per_team
        self.player_num = self.team_num * self.player_num_per_team
        self.spore_manager_settings = spore_manager_settings
        self.spore_settings = self.spore_manager_settings.ball_settings
        if random_generator is not None:
            self._random = random_generator
        else:
            self._random = random.Random()

    def init_balls(self, custom_init=None):
        if custom_init is None or len(custom_init) == 0:
            for i in range(self.team_num):
                team_id = i
                for j in range(self.player_num_per_team):
                    player_id = i * self.player_num_per_team + j
                    player = HumanPlayer(cfg=self.cfg.ball_settings, team_id=team_id, player_id=player_id, 
                                         border=self.border, spore_settings=self.spore_settings)
                    player.respawn(position=self.border.sample())
                    self.players[player_id] = player
        else:
            init_dict = {}
            for i in range(self.team_num):
                team_id = i
                init_dict[team_id] = {}
                for j in range(self.player_num_per_team):
                    player_id = i * self.player_num_per_team + j
                    player = HumanPlayer(cfg=self.cfg.ball_settings, team_id=team_id, player_id=player_id, 
                                         border=self.border, spore_settings=self.spore_settings)
                    self.players[player_id] = player
                    init_dict[team_id][player_id] = False
            for ball_cfg in custom_init:
                # [position.x, position.y, radius, player_name, team_name, 
                #  vel.x, vel.y, acc.x, acc.y, vel_last.x,
                #  vel_last.y, acc_last.x, acc_last.y, direction.x, direction.y,
                #  last_given_acc.x, last_given_acc.y, age, cooling_last, stop_flag,
                #  stop_time, acc_stop.x, acc_stop.y]
                position = Vector2(*ball_cfg[0:2])
                radius = ball_cfg[2]
                player_id = ball_cfg[3]
                team_id = ball_cfg[4]
                ball = CloneBall(ball_id=uuid.uuid1(), position=position, border=self.border, radius=radius, 
                                 team_id=team_id, player_id=player_id, 
                                 spore_settings=self.spore_settings, **self.cfg.ball_settings)
                if len(ball_cfg) > 5:
                    ball.vel_given = Vector2(*ball_cfg[5:7])
                    ball.acc_given = Vector2(*ball_cfg[7:9])
                    ball.vel_split = Vector2(*ball_cfg[9:11])
                    ball.split_frame = Vector2(*ball_cfg[12])
                    ball.frame_since_last_split = ball_cfg[13]
                self.players[player_id].add_balls(ball)
                init_dict[team_id][player_id] = True
            for team_id, team in init_dict.items():
                for player_id, player_init_flag in team.items():
                    if not player_init_flag:
                        self.players[player_id].respawn(position=self.border.sample())
            
    def get_balls(self):
        balls = []
        for player_id, player in self.players.items():
            balls.extend(player.get_balls())
        return balls

    def get_players(self):
        return list(self.players.values())

    def get_player_by_name(self, player_id):
        assert player_id in self.players
        return self.players[player_id]
    
    def add_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.players[ball.player_id].add_balls(ball)
        elif isinstance(balls, CloneBall):
            self.players[balls.player_id].add_balls(balls)
        return True

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.players[ball.player_id].remove_balls(ball)
        elif isinstance(balls, CloneBall):
            self.players[balls.player_id].remove_balls(balls)

    def step(self):
        for player_id, player in self.players.items():
            if player.get_clone_num() == 0:
                player.respawn(position=self.border.sample())

    def adjust(self):
        '''
        Overview:
            Adjust all balls in all players
        '''
        for player in self.get_players():
            player.adjust()
        return True

    def get_clone_num(self, ball):
        return self.players[ball.player_id].get_clone_num()

    def get_player_names(self):
        '''
        Overview:
            get all names of players
        '''
        return [player.player_id for player in self.get_players()]

    def get_team_names(self):
        '''
        Overview:
            get all names of players by teams with team names
        '''
        ret = {}
        for player in self.get_players():
            if player.team_id not in ret:
                ret[player.team_id] = []
            ret[player.team_id].append(player.player_id)
        return ret

    def get_player_names_with_team(self):
        '''
        Overview:
            get all names of players by teams
        '''
        ret = {}
        for player in self.get_players():
            if player.team_id not in ret:
                ret[player.team_id] = []
            ret[player.team_id].append(player.player_id)
        return list(ret.values())

    def get_team_infos(self):
        team_player_ids = {}
        for player in self.get_players():
            if player.team_id not in team_player_ids:
                team_player_ids[player.team_id] = []
            team_player_ids[player.team_id].append(player.player_id)
        return sorted(team_player_ids.items())

    def get_teams_size(self):
        team_name_size = {}
        for player in self.get_players():
            if player.team_id not in team_name_size:
                team_name_size[player.team_id] = player.get_total_size()
            else:
                team_name_size[player.team_id] += player.get_total_size()
        return team_name_size

    def reset(self):
        '''
        Overview:
            reset manager
        '''
        self.players = {}
        return True
