import numpy as np
import numexpr as ne
from easydict import EasyDict


class PlayerStatesUtil:

    def __init__(self, obs_settings):
        self.obs_settings = obs_settings

    def get_player_states(self, food_balls, thorns_balls, spore_balls, players):
        player_states = {}
        food_balls = np.array([[ball.position.x, ball.position.y] for ball in food_balls])
        for player in players:
            rectangle = self.get_rectangle_by_player(player)
            overlap, raw_balls = self.get_overlap(rectangle, food_balls, thorns_balls, spore_balls, players)
            player_score, can_feed, can_split = self.get_score_and_action(overlap, player.team_id)
            player_states[player.player_id] = {
                'rectangle': rectangle,
                'overlap': overlap,
                'team_name': player.team_id,
                'raw_balls': raw_balls,
                'score': player_score,
                'can_feed': can_feed, 
                'can_split': can_split,
            }
        return player_states

    def get_rectangle_by_player(self, player):
        centroid = player.cal_centroid()
        xs_max = 0
        ys_max = 0
        for ball in player.get_balls():
            direction_center = centroid - ball.position
            if abs(direction_center.x) + ball.radius > xs_max:
                xs_max = abs(direction_center.x) + ball.radius
            if abs(direction_center.y) + ball.radius > ys_max:
                ys_max = abs(direction_center.y) + ball.radius
        xs_max = max(xs_max, self.obs_settings.partial.vision_x_min)
        ys_max = max(ys_max, self.obs_settings.partial.vision_y_min)
        scale_up_len =  max(xs_max, ys_max)
        left_top_x = centroid.x - scale_up_len * self.obs_settings.partial.scale_up_ratio
        left_top_y = centroid.y - scale_up_len * self.obs_settings.partial.scale_up_ratio
        right_bottom_x = left_top_x + scale_up_len * self.obs_settings.partial.scale_up_ratio * 2
        right_bottom_y = left_top_y + scale_up_len * self.obs_settings.partial.scale_up_ratio * 2
        rectangle = (left_top_x, left_top_y, right_bottom_x, right_bottom_y)
        return rectangle

    def get_overlap(self, rectangle, food_balls, thorns_balls, spore_balls, players):
        ret = {}
        food_count = 0
        thorns_count = 0
        spore_count = 0
        clone_count = 0

        assert len(players) > 0, 'len(players) = {} can not be 0'.format(len(players))

        food = len(food_balls) * [3 * [None]]     # without speed
        thorns = len(thorns_balls) * [3 * [None]] # without speed 
        spore = len(spore_balls) * [3 * [None]]   # without speed 
        clone = len(players) * players[0].ball_settings.part_num_max * [5 * [None]]   # without speed 

        food_radius = 0.5
        fr0 = rectangle[0] - food_radius
        fr1 = rectangle[1] - food_radius
        fr2 = rectangle[2] + food_radius
        fr3 = rectangle[3] + food_radius
        food_balls_x = food_balls[:,0]
        food_balls_y = food_balls[:,1]
        food_result = ne.evaluate('(food_balls_x>fr0) & (food_balls_x<fr2) & (food_balls_y>fr1) & (food_balls_y<fr3)')
        x = food_balls_x[food_result==True]
        y = food_balls_y[food_result==True]
        r_col = np.ones_like(x) * food_radius
        res = np.stack((x, y, r_col), axis=-1)
        ret['food'] = res.tolist()
        # p = food_balls[food_result==True]
        # r_col = np.ones([p.shape[0]]) * food_radius
        # res = np.c_[p, r_col]
        # ret['food'] = res.tolist()

        # thorns overlap
        for ball in thorns_balls:
            if ball.judge_in_rectangle(rectangle):
                thorns[thorns_count] = [ball.position.x, ball.position.y, ball.radius]
                thorns_count += 1
        thorns = thorns[:thorns_count]
        ret['thorns'] = thorns
        # spore overlap
        for ball in spore_balls:
            if ball.judge_in_rectangle(rectangle):
                spore[spore_count] = [ball.position.x, ball.position.y, ball.radius, ball.owner]
                spore_count += 1
        spore = spore[:spore_count]
        ret['spore'] = spore
        # clone overlap
        for player in players:
            for ball in player.get_balls():
                if ball.judge_in_rectangle(rectangle):
                    clone[clone_count] = [ball.position.x, ball.position.y, ball.radius, 
                                          ball.vel.x, ball.vel.y, ball.direction.x, ball.direction.y, 
                                          player.player_id, player.team_id]
                    clone_count += 1
        clone = clone[:clone_count]
        ret['clone'] = clone
        raw_balls = self.get_raw_balls(ret['clone'], ret['food'], ret['thorns'], ret['spore'])
        return ret, raw_balls
    
    def radius_to_score(self, radius):
        # radius = sqrt(score / 100 *0.042 + 0.15)
        return (np.power(radius,2) - 0.15) / 0.042 * 100
    
    def score_to_radius(self, score):
        radius = np.sqrt(score / 100 * 0.042 + 0.15)
        return radius

    def get_msg_ball(self, balls, ball_type):
        # message MsgBall {
        #                     int32  Type    // 球类型 (1球 2粮食 3刺 4孢子)
        #                     uint64 Own     // 球所有者(玩家球为玩家id,粮食刺为0)
        #                     uint32 Score   // 球大小
        #                     int32  X       // 球位置x
        #                     int32  Y       // 球位置y
        #                     int32 XSpeed   // 当前速度x
        #                     int32 YSpeed   // 当前速度y
        #                     int32 XDrct    // 当前方向x
        #                     int32 YDrct    // 当前方向y
        #                 }
        ball_type_map = {'clone':1, 'food':2, 'thorn':3, 'spore':4}
        raw_balls = []
        for bl in balls:
            ball = EasyDict()
            ball.Type = ball_type_map[ball_type]
            ball.Own = bl[-2] if ball_type == 'clone' else 0
            ball.score = self.radius_to_score(bl[2])
            ball.X = bl[0] * 100
            ball.Y = bl[1] * 100
            ball.NX = (bl[0] + 0.05*bl[3])*100 if ball_type == 'clone' else bl[0]
            ball.NY = (bl[1] + 0.05*bl[4])*100 if ball_type == 'clone' else bl[1]
            ball.XSpeed = bl[3] if ball_type == 'clone' else 0
            ball.YSpeed = bl[4] if ball_type == 'clone' else 0
            ball.XDrct = bl[5]  if ball_type == 'clone' else 0
            ball.YDrct = bl[6]  if ball_type == 'clone' else 0
            raw_balls.append(ball)
        return raw_balls

    def get_raw_balls(self, clone, food, thorns, spore):
        raw_balls = []
        raw_balls += self.get_msg_ball(clone, 'clone')
        raw_balls += self.get_msg_ball(food, 'food')
        raw_balls += self.get_msg_ball(spore, 'spore')
        raw_balls += self.get_msg_ball(thorns, 'thorn')
        return raw_balls
    
    def get_score_and_action(self, overlap, team_num):
        clone = np.array(overlap['clone'])
        own_balls = clone[np.where(clone[:,-1]==team_num)]
        size = own_balls[:,2]
        player_score = self.radius_to_score(size).sum().item()
        # can action
        size = sorted(size)
        can_feed = size[-1]>(1.6*0.755)    # min feed size
        can_split = (size[-1]>(1.5*0.755)) and (len(own_balls)<16)   # min split size
        return player_score, can_feed, can_split


class PlayerStatesSPUtil(PlayerStatesUtil):

    def get_overlap(self, rectangle, food_balls, thorns_balls, spore_balls, players):
        ret = {}
        food_count = 0
        thorns_count = 0
        spore_count = 0
        clone_count = 0

        assert len(players) > 0, 'len(players) = {} can not be 0'.format(len(players))

        food = len(food_balls) * [3 * [None]]     # without speed
        thorns = len(thorns_balls) * [3 * [None]] # without speed 
        spore = len(spore_balls) * [3 * [None]]   # without speed 
        clone = len(players) * players[0].ball_settings.part_num_max * [5 * [None]]   # without speed 

        food_radius = 0.5
        fr0 = rectangle[0] - food_radius
        fr1 = rectangle[1] - food_radius
        fr2 = rectangle[2] + food_radius
        fr3 = rectangle[3] + food_radius
        food_balls_x = food_balls[:,0]
        food_balls_y = food_balls[:,1]
        food_result = ne.evaluate('(food_balls_x>fr0) & (food_balls_x<fr2) & (food_balls_y>fr1) & (food_balls_y<fr3)')
        x = food_balls_x[food_result==True]
        y = food_balls_y[food_result==True]
        r_col = np.ones_like(x) * food_radius
        res = np.stack((x, y, r_col), axis=-1)
        ret['food'] = res.tolist()
        # p = food_balls[food_result==True]
        # r_col = np.ones([p.shape[0]]) * food_radius
        # res = np.c_[p, r_col]
        # ret['food'] = res.tolist()

        # thorns overlap
        for ball in thorns_balls:
            if ball.judge_in_rectangle(rectangle):
                thorns[thorns_count] = [ball.position.x, ball.position.y, ball.radius]
                thorns_count += 1
        thorns = thorns[:thorns_count]
        ret['thorns'] = thorns
        # spore overlap
        for ball in spore_balls:
            if ball.judge_in_rectangle(rectangle):
                spore[spore_count] = [ball.position.x, ball.position.y, ball.radius, ball.owner]
                spore_count += 1
        spore = spore[:spore_count]
        ret['spore'] = spore
        # clone overlap
        for player in players:
            for ball in player.get_balls():
                if ball.judge_in_rectangle(rectangle):
                    clone[clone_count] = [ball.position.x, ball.position.y, ball.radius, 
                                          ball.vel.x, ball.vel.y, ball.direction.x, ball.direction.y, 
                                          player.player_id, player.team_id, ball.ball_id]
                    clone_count += 1
        clone = clone[:clone_count]
        ret['clone'] = clone
        return ret
