import math
import logging
import uuid
import copy
import random
from easydict import EasyDict
from pygame.math import Vector2

from gobigger.utils import format_vector, add_score, Border, deep_merge_dicts
from .base_ball import BaseBall
from .food_ball import FoodBall
from .thorns_ball import ThornsBall
from .spore_ball import SporeBall


class CloneBall(BaseBall):
    """
    Overview:
        One of the balls that a single player can control
        - characteristic:
        * Can move
        * Can eat any other ball smaller than itself
        * Under the control of the player, the movement can be stopped immediately and contracted towards the center of mass of the player
        * Skill 1: Split each unit into two equally
        * Skill 2: Spit spores forward
        * There is a percentage of weight attenuation, and the radius will shrink as the weight attenuates
    """
    @staticmethod
    def default_config():

        cfg = BaseBall.default_config()
        cfg.update(dict(
            acc_weight=100, # Maximum acceleration
            vel_max=20, # Maximum velocity
            score_init=1, # The initial score of the player's ball
            part_num_max=16, # Maximum number of avatars
            on_thorns_part_num=10, # Maximum number of splits when encountering thorns
            on_thorns_part_score_max=3, # Maximum score of split part when encountering thorns
            split_score_min=2.5, # The lower limit of the score of the splittable ball
            eject_score_min=2.5, # The lower limit of the score of the ball that can spores
            recombine_frame=320, # Time for the split ball to rejoin 
            split_vel_zero_frame=40, # The time it takes for the speed of the split ball to decay to zero (s)
            score_decay_min=2600,
            score_decay_rate_per_frame=0.00005, # The score proportion of each state frame attenuation
            center_acc_weight=10, # The ratio of actual acceleration to input acceleration
        ))
        return EasyDict(cfg)

    def __init__(self, ball_id, position, score, border, team_id, player_id,
                 vel_given=Vector2(0,0), acc_given=Vector2(0,0), 
                 from_split=False, from_thorns=False, split_direction=Vector2(0,0),
                 spore_settings=SporeBall.default_config(), sequence_generator=None, **kwargs):
        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = CloneBall.default_config()
        cfg = deep_merge_dicts(cfg, kwargs)
        super(CloneBall, self).__init__(ball_id, position, score, border, **cfg)
        self.acc_weight = cfg.acc_weight
        self.vel_max = cfg.vel_max
        self.score_init = cfg.score_init
        self.part_num_max = cfg.part_num_max
        self.on_thorns_part_num = cfg.on_thorns_part_num
        self.on_thorns_part_score_max = cfg.on_thorns_part_score_max
        self.split_score_min = cfg.split_score_min
        self.eject_score_min = cfg.eject_score_min
        self.recombine_frame = cfg.recombine_frame
        self.split_vel_zero_frame = cfg.split_vel_zero_frame
        self.score_decay_min = cfg.score_decay_min
        self.score_decay_rate_per_frame = cfg.score_decay_rate_per_frame
        self.center_acc_weight = cfg.center_acc_weight
        self.spore_settings = spore_settings
        self.sequence_generator = sequence_generator
        self.cfg = cfg
        # normal kwargs
        self.team_id = team_id
        self.player_id = player_id
        self.vel_given = vel_given
        self.acc_given = acc_given

        if from_split:
            self.vel_split = self.cal_split_vel_init_from_split(self.radius) * split_direction
        elif from_thorns:
            self.vel_split = self.cal_split_vel_init_from_thorns(self.radius) * split_direction
        else:
            self.vel_split = Vector2(0, 0)
        self.vel_split_piece = self.vel_split / self.split_vel_zero_frame
        self.split_frame = 0
        self.frame_since_last_split = 0 # The time of the current ball from the last split

        self.vel = self.vel_given + self.vel_split

        self.update_direction()
        self.check_border()

    def update_direction(self):
        if self.vel.length() != 0:
            self.direction = copy.deepcopy(self.vel.normalize())
        else:
            self.direction = Vector2(random.random(), random.random()).normalize()

    def cal_vel_max(self, radius, ratio):
        # return self.vel_max*1/(radius+10) * ratio
        return (2.35 + 5.66 / radius) * ratio

    def cal_split_vel_init_from_split(self, radius):
        return (4.75 + 0.95 * radius) / (self.split_vel_zero_frame / 20) * 2

    def cal_split_vel_init_from_thorns(self, radius):
        return (13.0 - radius) / (self.split_vel_zero_frame / 20) * 2

    def move(self, given_acc=None, given_acc_center=None, duration=0.05):
        """
        Overview:
            Realize the movement of the ball, pass in the direction and time parameters
        """
        # update acc
        if given_acc is not None:
            if given_acc.length != 0:
                given_acc = given_acc if given_acc.length() < 1 else given_acc.normalize()
                self.acc_given = given_acc * self.acc_weight
        else:
            given_acc = self.acc_given / self.acc_weight
        if given_acc_center is not None:
            given_acc_center = given_acc_center / self.radius
            if given_acc_center.length() != 0 and given_acc_center.length() > 1:
                given_acc_center = given_acc_center.normalize()
            self.acc_given_center = given_acc_center * self.center_acc_weight
        else:
            given_acc_center = Vector2(0, 0)
            self.acc_given_center = Vector2(0, 0)
        self.acc_given_total = self.acc_given + self.acc_given_center
        vel_max_ratio_given = given_acc.length()
        vel_max_ratio_center = given_acc_center.length()
        vel_max_ratio = max(vel_max_ratio_given, vel_max_ratio_center)

        # update vel_split
        if self.split_frame < self.split_vel_zero_frame:
            self.vel_split -= self.vel_split_piece
            self.split_frame += 1
        else:
            self.vel_split = Vector2(0,0)
        # update vel_given
        self.vel_given = self.vel_given + self.acc_given_total * duration
        self.vel_max_ball = self.cal_vel_max(self.radius, ratio=vel_max_ratio)
        self.vel_given = format_vector(self.vel_given, self.vel_max_ball)
        # udpate vel
        self.vel = self.vel_given + self.vel_split
        # print(self.vel_split, self.split_frame, self.vel_split_piece)
        # update position
        self.position = self.position + self.vel * duration
        self.update_direction()
        self.frame_since_last_split += 1
        self.check_border()

    def eat(self, ball, clone_num=None):
        """
        Parameters:
            clone_num <int>: The total number of balls for the current player
        """
        if isinstance(ball, SporeBall) or isinstance(ball, FoodBall) or isinstance(ball, CloneBall):
            self.set_score(add_score(self.score, ball.score))
        elif isinstance(ball, ThornsBall):
            assert clone_num is not None
            self.set_score(add_score(self.score, ball.score))
            if clone_num < self.part_num_max:
                split_num = min(self.part_num_max - clone_num, self.on_thorns_part_num)
                return self.on_thorns(split_num=split_num)
        else:
            logging.debug('CloneBall can not eat {}'.format(type(ball)))
        self.check_border()
        return True

    def on_thorns(self, split_num) -> list:
        '''
        Overview:
            Split after encountering thorns, calculate the score, position, speed, acceleration of each ball after splitting
        Parameters:
            split_num <int>: Number of splits added
        Returns:
            Return a list that contains the newly added balls after the split, the distribution of the split balls is a circle and the center of the circle has a ball
        '''
        # middle ball
        around_score = min(self.score / (split_num + 1), self.on_thorns_part_score_max)
        around_radius = self.score_to_radius(around_score)
        middle_score = self.score - around_score * split_num
        self.set_score(middle_score) 
        around_positions = []
        around_split_directions = []
        for i in range(split_num):
            angle = 2*math.pi*(i+1) / split_num
            unit_x = math.cos(angle)
            unit_y = math.sin(angle)
            split_direction = Vector2(unit_x, unit_y)
            around_position = self.position + Vector2((self.radius+around_radius)*unit_x, (self.radius+around_radius)*unit_y)
            around_positions.append(around_position)
            around_split_directions.append(split_direction)
        balls = []
        for p, s in zip(around_positions, around_split_directions):
            ball_id = uuid.uuid1() if self.sequence_generator is None else self.sequence_generator.get()
            around_ball = CloneBall(ball_id=ball_id, position=p, score=around_score, border=self.border, 
                                    team_id=self.team_id, player_id=self.player_id, 
                                    vel_given=copy.deepcopy(self.vel_given), acc_given=copy.deepcopy(self.acc_given),
                                    from_split=False, from_thorns=True, split_direction=s, spore_settings=self.spore_settings, 
                                    sequence_generator=self.sequence_generator, **self.cfg)
            balls.append(around_ball)
        return balls

    def eject(self, direction=None) -> list:
        '''
        Overview:
            When spit out spores, the spores spit out must be in the moving direction of the ball, and the position is tangent to the original ball after spitting out
        Returns:
            Return a list containing the spores spit out
        '''
        if direction is None or direction.length() == 0:
            direction = self.direction
        else:
            direction = direction.normalize()
        if self.score >= self.eject_score_min:
            spore_score = self.spore_settings.score_init
            self.set_score(self.score - spore_score)
            spore_radius = self.score_to_radius(spore_score)
            position = self.position + direction * (self.radius + spore_radius)
            return SporeBall(ball_id=uuid.uuid1(), position=position, border=self.border, score=spore_score, 
                             direction=direction, owner=self.player_id, **self.spore_settings)
        else:
            return False

    def split(self, clone_num, direction=None) -> list:
        '''
        Overview:
            Active splitting, the two balls produced by splitting have the same volume, and their positions are tangent to the forward direction
        Parameters:
            clone_num <int>: The total number of balls for the current player
        Returns:
            The return value is the new ball after the split
        '''
        if direction is None or direction.length() == 0:
            direction = self.direction
        else:
            direction = direction.normalize()
        if self.score >= self.split_score_min and clone_num < self.part_num_max:
            split_score = self.score / 2
            self.set_score(split_score)
            clone_num += 1
            position = self.position + direction * (self.radius * 2)
            ball_id = uuid.uuid1() if self.sequence_generator is None else self.sequence_generator.get()
            return CloneBall(ball_id=ball_id, position=position, score=self.score, border=self.border, 
                             team_id=self.team_id, player_id=self.player_id,
                             vel_given=copy.deepcopy(self.vel_given), acc_given=copy.deepcopy(self.acc_given),
                             from_split=True, from_thorns=False, split_direction=direction, spore_settings=self.spore_settings, 
                             sequence_generator=self.sequence_generator, **self.cfg)
        else:
            return False

    def rigid_collision(self, ball):
        '''
        Overview:
            When two balls collide, We need to determine whether the two balls belong to the same player
            A. If not, do nothing until one party is eaten at the end
            B. If the two balls are the same owner, judge whether the age of the two is full or not meet the fusion condition, if they are satisfied, do nothing.
            C. If the two balls are the same owner, judge whether the age of the two is full or not meet the fusion condition, Then the two balls will collide with rigid bodies
            This function completes the C part: the rigid body collision part, the logic is as follows:
             1. To determine the degree of fusion of the two balls, use [the radius of both] and subtract [the distance between the two] as the magnitude of the force
             2. Calculate the coefficient according to the weight, the larger the weight, the smaller the coefficient will be
             3. Correct the position of the two according to the coefficient and force
        Parameters:
            ball <CloneBall>: another ball
        Returns:
            state <bool>: the operation is successful or not
        '''
        if ball.ball_id == self.ball_id:
            return True
        assert isinstance(ball, CloneBall), 'ball is not CloneBall but {}'.format(type(ball))
        assert self.player_id == ball.player_id
        assert self.frame_since_last_split < self.recombine_frame or ball.frame_since_last_split < ball.recombine_frame
        p = ball.position - self.position
        d = p.length()
        if self.radius + ball.radius > d:
            f = min(self.radius + ball.radius - d, (self.radius + ball.radius - d) / (d+1e-8))
            self.position = self.position - f * p * (ball.score / (self.score + ball.score))
            ball.position = ball.position + f * p * (self.score / (self.score + ball.score))
        else:
            print('WARNINGS: self.radius ({}) + ball.radius ({}) <= d ({})'.format(self.radius, ball.radius, d))
        self.check_border()
        ball.check_border()
        return True

    def judge_rigid(self, ball):
        '''
        Overview:
            Determine whether two balls will collide with a rigid body
        Parameters:
            ball <CloneBall>: another ball
        Returns:
            <bool>: collide or not
        '''
        return self.frame_since_last_split < self.recombine_frame or ball.frame_since_last_split < ball.recombine_frame

    def score_decay(self):
        '''
        Overview: 
            Control the score of the ball to decay over time
        '''
        if self.score > self.score_decay_min:
            self.set_score(self.score * (1-self.score_decay_rate_per_frame*math.sqrt(self.radius)))
        return True

    def flush_frame_since_last_split(self):
        self.frame_since_last_split = 0
        return True

    def __repr__(self) -> str:
        return '{}, vel_given={}, acc_given={}, frame_since_last_split={:.3f}, player_id={}, direction={}, team_id={}'\
                .format(super().__repr__(), self.vel_given, self.acc_given, self.frame_since_last_split, self.player_id, self.direction, self.team_id)

    def save(self):
        return [self.position.x, self.position.y, self.radius, self.direction.x, self.direction.y, self.player_id, self.team_id]
