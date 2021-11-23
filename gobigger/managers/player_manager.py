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

    def __init__(self, cfg, border, team_num, player_num_per_team, spore_manager_settings):
        super(PlayerManager, self).__init__(cfg, border)
        self.players = {}
        self.team_num = team_num
        self.player_num_per_team = player_num_per_team
        self.player_num = self.team_num * self.player_num_per_team
        self.spore_manager_settings = spore_manager_settings
        self.spore_settings = self.spore_manager_settings.ball_settings

    def init_balls(self, custom_init=None):
        if custom_init is None:
            for i in range(self.team_num):
                team_name = str(i)
                for j in range(self.player_num_per_team):
                    player_name = str(i * self.player_num_per_team + j)
                    player = HumanPlayer(cfg=self.cfg.ball_settings, team_name=team_name, name=player_name, border=self.border, spore_settings=self.spore_settings)
                    player.respawn(position=self.border.sample())
                    self.players[player_name] = player
        else:
            init_dict = {}
            for i in range(self.team_num):
                team_name = str(i)
                init_dict[team_name] = {}
                for j in range(self.player_num_per_team):
                    player_name = str(i * self.player_num_per_team + j)
                    player = HumanPlayer(cfg=self.cfg.ball_settings, team_name=team_name, name=player_name, border=self.border, spore_settings=self.spore_settings)
                    self.players[player_name] = player
                    init_dict[team_name][player_name] = False
            for ball_cfg in custom_init:
                # [position.x, position.y, radius, player_name, team_name, 
                #  vel.x, vel.y, acc.x, acc.y, vel_last.x,
                #  vel_last.y, acc_last.x, acc_last.y, direction.x, direction.y,
                #  last_given_acc.x, last_given_acc.y, age, cooling_last, stop_flag,
                #  stop_time, acc_stop.x, acc_stop.y]
                position = Vector2(*ball_cfg[0:2])
                radius = ball_cfg[2]
                player_name = ball_cfg[3]
                team_name = ball_cfg[4]
                ball = CloneBall(team_name=team_name, name=uuid.uuid1(), position=position, border=self.border, 
                                 size=radius**2, vel=Vector2(0,0), acc=Vector2(0,0),
                                 vel_last=Vector2(0,0), acc_last=Vector2(0,0), last_given_acc=Vector2(0,0),
                                 stop_flag=True, owner=player_name, spore_settings=self.spore_settings)
                ball.vel = Vector2(*ball_cfg[5:7])
                ball.acc = Vector2(*ball_cfg[7:9])
                ball.vel_last = Vector2(*ball_cfg[9:11])
                ball.acc_last = Vector2(*ball_cfg[11:13])
                ball.direction = Vector2(*ball_cfg[13:15])
                ball.last_given_acc = Vector2(*ball_cfg[15:17])
                ball.age = ball_cfg[17]
                ball.cooling_last = ball_cfg[18]
                ball.stop_flag = ball_cfg[19]
                ball.stop_time = ball_cfg[20]
                ball.acc_stop = Vector2(*ball_cfg[21:23])
                self.players[player_name].add_balls(ball)
                init_dict[team_name][player_name] = True
            for team_name, team in init_dict.items():
                for player_name, player_init_flag in team.items():
                    if not player_init_flag:
                        self.players[player_name].respawn(position=self.border.sample())
            
    def get_balls(self):
        balls = []
        for player_name, player in self.players.items():
            balls.extend(player.get_balls())
        return balls

    def get_players(self):
        return list(self.players.values())

    def get_player_by_name(self, name):
        assert name in self.players
        return self.players[name]
    
    def add_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.players[ball.owner].add_balls(ball)
        elif isinstance(balls, CloneBall):
            self.players[balls.owner].add_balls(balls)
        return True

    def remove_balls(self, balls):
        if isinstance(balls, list):
            for ball in balls:
                self.players[ball.owner].remove_balls(ball)
        elif isinstance(balls, CloneBall):
            self.players[balls.owner].remove_balls(balls)

    def step(self):
        for player_name, player in self.players.items():
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
        return self.players[ball.owner].get_clone_num()

    def get_player_names(self):
        '''
        Overview:
            get all names of players
        '''
        return [player.name for player in self.get_players()]

    def get_team_names(self):
        '''
        Overview:
            get all names of players by teams with team names
        '''
        ret = {}
        for player in self.get_players():
            if player.team_name not in ret:
                ret[player.team_name] = []
            ret[player.team_name].append(player.name)
        return ret

    def get_player_names_with_team(self):
        '''
        Overview:
            get all names of players by teams
        '''
        ret = {}
        for player in self.get_players():
            if player.team_name not in ret:
                ret[player.team_name] = []
            ret[player.team_name].append(player.name)
        return list(ret.values())

    def get_teams_size(self):
        team_name_size = {}
        for player in self.get_players():
            if player.team_name not in team_name_size:
                team_name_size[player.team_name] = player.get_total_size()
            else:
                team_name_size[player.team_name] += player.get_total_size()
        return team_name_size

    def reset(self):
        '''
        Overview:
            reset manager
        '''
        self.refresh_time_count = 0
        self.players = {}
        return True
