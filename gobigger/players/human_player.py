import uuid
from pygame.math import Vector2
import logging

from .base_player import BasePlayer
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class HumanPlayer(BasePlayer):

    def __init__(self, cfg, team_name, name, border, spore_settings):
        self.team_name = team_name
        self.name = name
        self.border = border
        self.balls = {}
        self.ball_settings = cfg
        self.spore_settings = spore_settings
        self.stop_flag = False

    def get_clone_num(self):
        '''
        Overview:
            Get how many avatars the current player has
        '''
        return len(self.balls)

    def get_balls(self):
        '''
        Overview:
            Get all the balls of the current player
        '''
        return list(self.balls.values())

    def add_balls(self, balls):
        '''
        Overview:
            Add new avatars
        Parameters:
            balls <List[CloneBall] or CloneBall>: It can be a list or a single doppelganger
        '''
        if isinstance(balls, list):
            for ball in balls:
                self.balls[ball.name] = ball
        elif isinstance(balls, CloneBall):
            self.balls[balls.name] = balls
        return True

    def move(self, direction=None, duration=0.05):
        '''
        Overview:
            Move all balls controlled by the player
            The main logic is
             1. Processing stopped state
             2. If it is stopping, control all balls to move closer to the center of mass
        Parameters:
            direction <Vector2>: A point in the unit circle
            duration <float>: time
        Returns:
            position <Vector2>: position after moving 
        '''
        if direction is not None: 
            self.stop_flag = False # Exit stopped state
            for ball in self.balls.values():
                ball.stop_flag = False
        if self.get_clone_num() == 0:
            pass
        elif self.stop_flag: 
            if self.get_clone_num() == 1: 
                for ball in self.balls.values():
                    ball.move(given_acc=None, given_acc_center=None, duration=duration)
            else: #If there are multiple balls, control them to move to the center
                centroid = self.cal_centroid()
                for ball in self.balls.values():
                    given_acc_center = centroid - ball.position
                    if given_acc_center.length() == 0:
                        given_acc_center = Vector2(0.000001, 0.000001)
                    elif given_acc_center.length() > 1:
                        given_acc_center = given_acc_center.normalize()
                    given_acc_center *= 20
                    ball.move(given_acc=direction, given_acc_center=given_acc_center, duration=duration)
        else:
            if self.get_clone_num() == 1:
                for ball in self.balls.values():
                    ball.move(given_acc=direction, given_acc_center=Vector2(0,0), duration=duration)
            else:
                centroid = self.cal_centroid()
                for ball in self.balls.values():
                    given_acc_center = centroid - ball.position
                    if given_acc_center.length() == 0:
                        given_acc_center = Vector2(0.000001, 0.000001)
                    elif given_acc_center.length() > 1:
                        given_acc_center = given_acc_center.normalize()
                    given_acc_center *= 20
                    ball.move(given_acc=direction, given_acc_center=given_acc_center, duration=duration)
        self.size_decay()
        return True

    def size_decay(self):
        '''
        Overview: 
            The player’s balls' size will decay over time
        '''
        for ball in self.balls.values():
            ball.size_decay()
        return True

    def eject(self, direction=None):
        '''
        Overview:
            All clones controlled by the player perform the spore-spitting action
        Return:
            <list>: list of new spores
        '''
        ret = []
        for ball in self.balls.values():
            ret.append(ball.eject(direction=direction))
        return ret

    def get_keys_sort_by_balls(self):
        '''
        Overview:
            Sort by ball size from largest to smallest
        Return:
            <list>: list of names
        '''
        items = self.balls.items() 
        backitems=[[v[1],v[0]] for v in items] 
        backitems.sort(reverse=True) 
        return [ backitems[i][1] for i in range(0,len(backitems))] 

    def split(self, direction=None):
        '''
        Overview:
            All avatars controlled by the player perform splits, from large to small
        '''
        balls_keys = self.get_keys_sort_by_balls()
        for k in balls_keys:
            ret = self.balls[k].split(self.get_clone_num(), direction=direction)
            if ret and isinstance(ret, CloneBall):
                self.add_balls(ret)
        return True

    def eat(self, ball):
        raise NotImplementedError

    def stop(self):
        if self.stop_flag:
            return True
        self.stop_flag = True
        centroid = self.cal_centroid()
        for ball in self.balls.values():
            direction_center = centroid - ball.position
            if direction_center.length() == 0:
                direction_center = Vector2(0.000001, 0.000001)
            ball.stop(direction=direction_center)
        return True

    def remove_balls(self, ball):
        ball.remove()
        if ball.name in self.balls:
            try:
                del self.balls[ball.name]
            except:
                pass
        return True

    def respawn(self, position):
        ball_name = uuid.uuid1()
        ball = CloneBall(team_name=self.team_name, name=ball_name, position=position, border=self.border, owner=self.name, 
                         spore_settings=self.spore_settings, **self.ball_settings)
        direction = Vector2(1, 0)
        ball.stop()
        self.balls = {}
        self.balls[ball.name] = ball   
        return True

    def cal_centroid(self):
        '''
        Overview:
            Calculate the centroid
        '''
        x = 0
        y = 0
        total_size = 0
        for ball in self.get_balls():
            x += ball.size * ball.position.x
            y += ball.size * ball.position.y
            total_size += ball.size
        return Vector2(x, y) / total_size

    def adjust(self):
        '''
        Overview:
            Adjust all the balls controlled by the player, including two parts
            1. Possible Rigid Body Collision
            2. Possible ball-ball fusion
        '''
        balls = self.get_balls()
        balls = sorted(balls, reverse=True)
        balls_num = len(balls)
        to_remove_balls = []
        for i in range(balls_num-1):
            if not balls[i].is_remove:
                for j in range(i+1, balls_num):
                    if not balls[j].is_remove:
                        dis = balls[i].get_dis(balls[j])
                        if dis < balls[i].radius + balls[j].radius:
                            if balls[i].judge_rigid(balls[j]):
                                balls[i].rigid_collision(balls[j]) # Rigid body collision                       
                            else:
                                if dis < balls[i].radius or dis < balls[j].radius: 
                                    if balls[i].size > balls[j].size:
                                        balls[i].eat(balls[j])
                                        balls[j].remove()
                                        to_remove_balls.append(balls[j])
                                    else:
                                        balls[j].eat(balls[i])
                                        balls[i].remove()
                                        to_remove_balls.append(balls[i])
        for ball in to_remove_balls: 
            self.remove_balls(ball)

    def get_total_size(self):
        '''
            Overview: 
                Get the total size of all balls of the current player
        '''
        total_size = 0
        for ball in self.get_balls():
            total_size += ball.size
        return total_size






