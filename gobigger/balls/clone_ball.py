import math
import logging
import uuid
import copy
from easydict import EasyDict
from pygame.math import Vector2

from gobigger.utils import format_vector, add_size, Border, deep_merge_dicts
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
            acc_max=50, # Maximum acceleration
            vel_max=25, # Maximum velocity
            radius_min=2, # Minimum radius
            radius_max=100, # Maximum radius
            radius_init=2, # The initial radius of the player's ball
            part_num_max=16, # Maximum number of avatars
            on_thorns_part_num=10, # Maximum number of splits when encountering thorns
            on_thorns_part_radius_max=5, # Maximum radius of split part when encountering thorns
            split_radius_min=30, # The lower limit of the radius of the splittable ball
            eject_radius_min=30, # The lower limit of the radius of the ball that can spores
            recombine_age=30, # Time for the split ball to rejoin (s)
            split_vel_init=50, # The initial velocity of the split ball
            split_vel_zero_time=0.1, # The time it takes for the speed of the split ball to decay to zero (s)
            stop_zero_time=0.1, # The time to zero the speed after using the stop function
            size_decay_rate=0.0001, # The size proportion of each state frame attenuation
            given_acc_weight=10, # The ratio of actual acceleration to input acceleration
        ))
        return EasyDict(cfg)

    def __init__(self, team_name, name, position, border, size=None, vel=None, acc=None, 
                 vel_last=None, acc_last=None, last_given_acc=None, stop_flag=False, 
                 owner=None, spore_settings=SporeBall.default_config(), **kwargs):
        # init other kwargs
        kwargs = EasyDict(kwargs)
        cfg = CloneBall.default_config()
        cfg = deep_merge_dicts(cfg, kwargs)
        super(CloneBall, self).__init__(name, position, border, size=size, vel=vel, acc=acc, **cfg)
        self.vel_max = cfg.vel_max
        self.acc_max = cfg.acc_max
        self.radius_min = cfg.radius_min
        self.radius_max = cfg.radius_max
        self.radius_init = cfg.radius_init
        self.part_num_max = cfg.part_num_max
        self.on_thorns_part_num = cfg.on_thorns_part_num
        self.on_thorns_part_radius_max = cfg.on_thorns_part_radius_max
        self.split_radius_min = cfg.split_radius_min
        self.eject_radius_min = cfg.eject_radius_min
        self.recombine_age = cfg.recombine_age
        self.split_vel_init = cfg.split_vel_init
        self.split_vel_zero_time = cfg.split_vel_zero_time
        self.stop_zero_time = cfg.stop_zero_time
        self.size_decay_rate = cfg.size_decay_rate
        self.given_acc_weight = cfg.given_acc_weight
        self.spore_settings = spore_settings
        self.cfg = cfg
        # normal kwargs
        self.team_name = team_name
        self.owner = owner
        self.split_acc_init = self.split_vel_init / self.split_vel_zero_time # Initialized deceleration scalar after split
        self.age = 0 # The time of the current ball from the last split

        self.vel_last = Vector2(0, 0) if vel_last is None else vel_last
        self.acc_last = Vector2(0, 0) if acc_last is None else acc_last 

        if self.vel_last.length() > 0:
            self.cooling_last = True
        else:
            self.cooling_last = False
        if not hasattr(self, 'direction'):
            if (self.vel + self.vel_last).length() != 0:
                self.direction = copy.deepcopy((self.vel + self.vel_last).normalize())
            else:
                self.direction = Vector2(0.000001, 0.000001).normalize()

        self.check_border()
        self.stop_flag = stop_flag
        self.last_given_acc = Vector2(0, 0) if last_given_acc is None else last_given_acc

        if not hasattr(self, 'stop_time'):
            self.stop_time = 0
        if not hasattr(self, 'acc_stop'):
            self.acc_stop = Vector2(0, 0)

    def cal_vel_max(self, radius):
        return self.vel_max*20/(radius+10)

    def move(self, given_acc=None, given_acc_center=None, duration=0.05):
        """
        Overview:
            Realize the movement of the ball, pass in the direction and time parameters
        """
        self.age += duration
        if given_acc is not None:
            given_acc = given_acc if given_acc.length() < 1 else given_acc.normalize()
            given_acc *= 10
            self.last_given_acc = given_acc
        else:
            given_acc = self.last_given_acc
        if self.stop_flag: # Stop function used
            if not hasattr(self, 'stop_time'):
                self.stop_time = 0
                self.acc_stop = Vector2(0, 0)
            if self.stop_time < self.stop_zero_time: # Deceleration state
                self.vel = self.vel + self.acc_stop * duration # Acceleration is already in the opposite direction of speed
                self.vel_last += self.acc_last * duration
                self.stop_time += duration
                if self.stop_time >= self.stop_zero_time: # If the stop time is exceeded, set the speed and acceleration to 0 directly
                    self.vel = Vector2(0, 0)
                    self.acc_stop = Vector2(0, 0)
                    self.vel_last = Vector2(0, 0)
                    self.acc_last = Vector2(0, 0)
                self.position = self.position + (self.vel + self.vel_last) * duration
            else: # Exceed the stop time, move closer to the center
                if given_acc_center is None: # Single ball
                    return
                else: # Multiple balls
                    self.acc = format_vector(given_acc*self.acc_max, self.acc_max)
                    acc_tmp = format_vector(self.acc + given_acc_center/math.sqrt(self.radius), self.acc_max) # The acceleration towards the center of mass is handled separately
                    self.vel_max_ball = self.cal_vel_max(self.radius)
                    self.vel = format_vector(self.vel * 0.95 + (self.acc + acc_tmp) * duration, self.vel_max_ball) # vel is multiplied by a number to prevent circling phenomenon
                    self.position = self.position + self.vel * duration
        else: # normal status
            self.acc_stop = Vector2(0, 0)
            if given_acc_center is None:
                given_acc_center = Vector2(0, 0)
            self.acc = format_vector(given_acc*self.acc_max, self.acc_max)
            acc_tmp = format_vector(self.acc + given_acc_center/math.sqrt(self.radius), self.acc_max) # The acceleration towards the center of mass is handled separately
            self.vel_max_ball = self.cal_vel_max(self.radius)
            self.vel = format_vector(self.vel + (self.acc + acc_tmp) * duration, self.vel_max_ball)
            if self.cooling_last:
                self.vel_last += self.acc_last * duration
                if self.age >= self.split_vel_zero_time:
                    self.vel_last = Vector2(0, 0)
                    self.acc_last = Vector2(0, 0)
                    self.cooling_last = False
            self.position = self.position + (self.vel + self.vel_last) * duration

        if (self.vel + self.vel_last).length() != 0:
            self.direction = copy.deepcopy((self.vel + self.vel_last).normalize())
        else:
            self.direction = Vector2(0.000001, 0.000001).normalize()
        self.check_border()

    def eat(self, ball, clone_num=None):
        """
        Parameters:
            clone_num <int>: The total number of balls for the current player
        """
        if isinstance(ball, SporeBall) or isinstance(ball, FoodBall) or isinstance(ball, CloneBall):
            self.set_size(add_size(self.size, ball.size))
            if self.radius > self.radius_max:
                self.radius = self.radius_max
        elif isinstance(ball, ThornsBall):
            assert clone_num is not None
            self.set_size(add_size(self.size, ball.size))
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
            Split after encountering thorns, calculate the size, position, speed, acceleration of each ball after splitting
        Parameters:
            split_num <int>: Number of splits added
        Returns:
            Return a list that contains the newly added balls after the split, the distribution of the split balls is a circle and the center of the circle has a ball
        '''
        # middle ball
        around_radius = min(math.sqrt(self.size / (split_num + 1)), self.on_thorns_part_radius_max)
        around_size = around_radius * around_radius
        middle_size = self.size - around_size * split_num
        self.set_size(middle_size) 
        middle_position = Vector2(self.position.x, self.position.y)
        around_positions = []
        around_vels = []
        around_accs = []
        for i in range(split_num):
            angle = 2*math.pi*(i+1)/split_num
            unit_x = math.cos(angle)
            unit_y = math.sin(angle)
            vel = Vector2(self.split_vel_init*unit_x, self.split_vel_init*unit_y)
            acc = - Vector2(self.split_acc_init*unit_x, self.split_acc_init*unit_y)
            around_position = self.position + Vector2((self.radius+around_radius)*unit_x, (self.radius+around_radius)*unit_y)
            around_vels.append(vel)
            around_accs.append(acc)
            around_positions.append(around_position)
        balls = []
        for p, v, a in zip(around_positions, around_vels, around_accs):
            around_ball = CloneBall(team_name=self.team_name, name=uuid.uuid1(), position=p, border=self.border, 
                                    size=around_size, vel=copy.deepcopy(self.vel), acc=copy.deepcopy(self.acc),
                                    vel_last=v, acc_last=a, last_given_acc=copy.deepcopy(self.last_given_acc), 
                                    stop_flag=self.stop_flag, owner=self.owner, spore_settings=self.spore_settings, 
                                    **self.cfg)
            balls.append(around_ball)
        return balls

    def eject(self, direction=None) -> list:
        '''
        Overview:
            When spit out spores, the spores spit out must be in the moving direction of the ball, and the position is tangent to the original ball after spitting out
        Returns:
            Return a list containing the spores spit out
        '''
        if direction is None:
            direction = copy.deepcopy(self.direction)
        if self.radius >= self.eject_radius_min:
            spore_radius = self.spore_settings.radius_min
            self.set_size(self.size - spore_radius**2)
            direction_unit = direction.normalize()
            position = self.position + direction_unit * (self.radius + spore_radius)
            return SporeBall(name=uuid.uuid1(), position=position, border=self.border, direction=direction_unit, owner=self.owner, **self.spore_settings)
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
        if direction is None:
            direction = copy.deepcopy(self.direction)
        if self.radius >= self.split_radius_min and clone_num < self.part_num_max:
            split_size = self.size / 2
            self.set_size(split_size)
            clone_num += 1
            direction_unit = direction.normalize()
            position = self.position + direction_unit * (self.radius * 2)
            vel_split = self.split_vel_init * direction_unit
            acc_split = - self.split_acc_init * direction_unit
            return CloneBall(team_name=self.team_name, name=uuid.uuid1(), position=position, border=self.border, 
                             size=split_size, vel=copy.deepcopy(self.vel), acc=copy.deepcopy(self.acc),
                             vel_last=vel_split, acc_last=acc_split, last_given_acc=copy.deepcopy(self.last_given_acc),
                             stop_flag=self.stop_flag, owner=self.owner, spore_settings=self.spore_settings, **self.cfg)
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
        if ball.name == self.name:
            return True
        assert isinstance(ball, CloneBall), 'ball is not CloneBall but {}'.format(type(ball))
        assert self.owner == ball.owner
        assert self.age < self.recombine_age or ball.age < ball.recombine_age
        p = ball.position - self.position
        d = p.length()
        if self.radius + ball.radius > d:
            f = min(self.radius + ball.radius - d, (self.radius + ball.radius - d) / (d+0.00001))
            self.position = self.position - f * p * (ball.size / (self.size + ball.size))
            ball.position = ball.position + f * p * (self.size / (self.size + ball.size))
        else:
            print('WARNINGS: self.radius ({}) + ball.radius ({}) <= d ({})'.format(self.radius, ball.radius, d))
        self.check_border()
        ball.check_border()
        return True

    def stop(self, direction=None):
        '''
        Overview:
            Stop in place, the speed and acceleration become 0, and the direction points to the center of gravity of the shape surrounded by the centers of all spheres
            Acceleration is set to the opposite direction of speed
            stop_zero_time = 0.2
            stop_flag = True
            Judge stop_flag at the next move
            1. True: The direction must be the center of the circle, the acceleration and the upper limit of the speed are reduced
            2. False: Normal movement
        Parameters:
            direction <Vector2>: The direction of the speed after the stop
        Returns:
            state <bool>:  the operation is successful or not
        '''
        self.stop_flag = True
        self.stop_time = 0
        self.acc_stop = - 1 / self.stop_zero_time * (self.vel + self.vel_last)
        self.acc = Vector2(0, 0)
        self.direction = direction if direction is not None else Vector2(0.000001, 0.000001)
        self.last_given_acc = Vector2(0, 0)
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
        return self.age < self.recombine_age or ball.age < ball.recombine_age

    def check_border(self):
        """
        Overview:
            Check if the position of the ball is beyond the bounds of the map
        """
        if self.position.x < self.border.minx or self.position.x > self.border.maxx:
            self.position.x = max(self.position.x, self.border.minx)
            self.position.x = min(self.position.x, self.border.maxx)
            self.vel.x = 0
            self.acc.x = 0
            self.acc_last.x = 0 

        if self.position.y < self.border.miny or self.position.y > self.border.maxy:
            self.position.y = max(self.position.y, self.border.miny)
            self.position.y = min(self.position.y, self.border.maxy)
            self.vel.y = 0
            self.acc.y = 0
            self.acc_last.y = 0 

    def size_decay(self):
        '''
        Overview: 
            Control the size of the ball to decay over time
        '''
        self.set_size(self.size * (1-self.size_decay_rate))
        return True


    def __repr__(self) -> str:
        return '{}, vel_last={}, acc_last={}, age={:.3f}, owner={}, direction={}, team_name={}'\
                .format(super().__repr__(), self.vel_last, self.acc_last, self.age, self.owner, self.direction, self.team_name)
