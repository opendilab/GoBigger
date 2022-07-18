import uuid
from pygame.math import Vector2
import logging

from .base_player import BasePlayer
from gobigger.balls import FoodBall, ThornsBall, CloneBall, SporeBall


class HumanPlayer(BasePlayer):

    def __init__(self, cfg, team_id, player_id, border, spore_settings):
        self.team_id = team_id
        self.player_id = player_id
        self.border = border
        self.balls = {}
        self.ball_settings = cfg
        self.spore_settings = spore_settings

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
                self.balls[ball.ball_id] = ball
        elif isinstance(balls, CloneBall):
            self.balls[balls.ball_id] = balls
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
        if self.get_clone_num() == 0:
            return True
        if self.get_clone_num() == 1:
            for ball in self.balls.values():
                ball.move(given_acc=direction, duration=duration)
        elif self.get_clone_num() >= 2:
            centroid = self.cal_centroid()
            for ball in self.balls.values():
                given_acc_center = centroid - ball.position
                ball.move(given_acc=direction, given_acc_center=given_acc_center, duration=duration)
        self.score_decay()

    def score_decay(self):
        '''
        Overview: 
            The player’s balls' scor will decay over time
        '''
        for ball in self.balls.values():
            ball.score_decay()
        return True

    def eject(self, direction=None):
        '''
        Overview:
            All clones controlled by the player perform the spore-spitting action
        Return:
            <list>: list of new spores
        '''
        ret = []
        ball_ids = list(self.balls.keys())
        for ball_id in ball_ids:
            if ball_id in self.balls:
                ball = self.balls[ball_id]
                ret.append(ball.eject(direction=direction))
        return ret

    def get_keys_sort_by_balls(self):
        '''
        Overview:
            Sort by ball score from largest to smallest
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
            if k in self.balls:
                ret = self.balls[k].split(self.get_clone_num(), direction=direction)
                if ret and isinstance(ret, CloneBall):
                    self.add_balls(ret)
        return True

    def eat(self, ball):
        raise NotImplementedError

    def remove_balls(self, ball):
        ball.remove()
        if ball.ball_id in self.balls:
            try:
                del self.balls[ball.ball_id]
            except:
                pass
        return True

    def respawn(self, position):
        ball_id = uuid.uuid1()
        ball = CloneBall(ball_id=ball_id, position=position, border=self.border, 
                         score=self.ball_settings.score_init,
                         team_id=self.team_id, player_id=self.player_id, 
                         spore_settings=self.spore_settings, **self.ball_settings)
        direction = Vector2(1, 0)
        # ball.stop()
        self.balls = {}
        self.balls[ball.ball_id] = ball   
        return True

    def cal_centroid(self):
        '''
        Overview:
            Calculate the centroid
        '''
        x = 0
        y = 0
        total_score = 0
        for ball in self.get_balls():
            x += ball.score * ball.position.x
            y += ball.score * ball.position.y
            total_score += ball.score
        return Vector2(x, y) / total_score

    def adjust(self):
        '''
        Overview:
            Adjust all the balls controlled by the player, including two parts
            1. Possible Rigid Body Collision
            2. Possible ball-ball fusion
        '''
        eats = 0
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
                                    eats += 1
                                    if balls[i].score > balls[j].score: # without eat_ratio
                                        balls[i].eat(balls[j])
                                        balls[j].remove()
                                        to_remove_balls.append(balls[j])
                                    else:
                                        balls[j].eat(balls[i])
                                        balls[i].remove()
                                        to_remove_balls.append(balls[i])
        for ball in to_remove_balls: 
            self.remove_balls(ball)
        return eats

    def get_total_score(self):
        '''
            Overview: 
                Get the total score of all balls of the current player
        '''
        total_score = 0
        for ball in self.get_balls():
            total_score += ball.score
        return total_score

    def get_info(self):
        total_score = 0
        can_eject = False
        can_split = False
        for ball in self.get_balls():
            total_score += ball.score
            if ball.score > self.ball_settings.eject_score_min:
                can_eject = True
            if self.get_clone_num() < self.ball_settings.part_num_max \
                and ball.score > self.ball_settings.split_score_min:
                can_split = True
        return total_score, can_split, can_eject
