import math
import torch


class Features:
    def __init__(self, cfg):
        self.cfg = cfg
        self.player_num_per_team = self.cfg.env.player_num_per_team
        self.team_num = self.cfg.env.team_num
        self.max_player_num = self.player_num_per_team
        self.max_team_num = self.team_num
        self.max_ball_num = self.cfg.agent.features.get('max_ball_num', 80)
        self.max_food_num = self.cfg.agent.features.get('max_food_num', 256)
        self.max_spore_num = self.cfg.agent.features.get('max_spore_num', 64)
        self.direction_num = self.cfg.agent.features.get('direction_num', 12)
        self.spatial_x = 64
        self.spatial_y = 64
        self.step_mul = self.cfg.env.get('step_mul', 5)
        self.second_per_frame = self.cfg.agent.features.get('second_per_frame', 0.05)
        self.action_num = self.direction_num * 2 + 3
        self.setup_action()
        self._init_fake_data()

    def get_augmentation_map(self):
        augmentation_mapping = {}
        for aug_type in ['ud', 'lr', 'lrud']:
            augmentation_mapping[aug_type] = {action: self.augmentation_action(action, aug_type=aug_type) for action in
                                              range(self.action_num)}
        return augmentation_mapping

    def setup_action(self):
        theta = math.pi * 2 / self.direction_num
        self.x_y_action_List = [[0.3 * math.cos(theta * i), 0.3 * math.sin(theta * i), 0] for i in
                                range(self.direction_num)] + \
                               [[math.cos(theta * i), math.sin(theta * i), 0] for i in
                                range(self.direction_num)] + \
                               [[0, 0, 0], [0, 0, 1], [0, 0, 2]]

    def _init_fake_data(self):
        self.SCALAR_INFO = {
            'view_x': (torch.long, ()),
            'view_y': (torch.long, ()),  # view center (x, y) from left bottom
            'view_width': (torch.long, ()),
            # 'view_height': (torch.long, ()),
            'score': (torch.long, ()),  # log
            'team_score': (torch.long, ()),
            'rank': (torch.long, ()),
            'time': (torch.long, ()),
            'last_action_type': (torch.long, ())
        }
        self.TEAM_INFO = {
            'alliance': (torch.long, (self.max_player_num,)),
            'view_x': (torch.long, (self.max_player_num,)),
            'view_y': (torch.long, (self.max_player_num,)),  # view center (x, y) from left bottom
            # 'view_width': (torch.long, (self.max_player_num * self.max_team_num,)),
            # 'view_height': (torch.long, (self.max_player_num * self.max_team_num,)),
            # 'score': (torch.long, (self.max_player_num * self.max_team_num,)),  # log
            # 'team_score': (torch.long, (self.max_player_num * self.max_team_num,)),
            # 'team_rank': (torch.long, (self.max_player_num * self.max_team_num,)),
            'player_num': (torch.long, ()),

        }
        self.BALL_INFO = {
            'alliance': (torch.long, (self.max_ball_num,)),  # 0 neutral, 1 self, 2 teammate, 3 enemy,
            'score': (torch.long, (self.max_ball_num,)),  # log own score + 1
            'radius': (torch.float, (self.max_ball_num,)),  # log (ratio to own score + 1)
            'rank': (torch.long, (self.max_ball_num,)),  # onehot 0 neural, 1-10 for team rank
            'x': (torch.long, (self.max_ball_num,)),  # binary relative coordinate to view center
            'y': (torch.long, (self.max_ball_num,)),  # binary relative coordinate to view center
            'next_x': (torch.long, (self.max_ball_num,)),  # binary relative coordinate to view center
            'next_y': (torch.long, (self.max_ball_num,)),  # binary relative coordinate to view center
            'ball_num': (torch.long, ())
        }

        self.SPATIAL_INFO = {
            'food_x': (torch.long, (self.max_food_num,)),  # relative coordinate to view center
            'food_y': (torch.long, (self.max_food_num,)),  # relative coordinate to view center
            'spore_x': (torch.long, (self.max_spore_num,)),  # relative coordinate to view center
            'spore_y': (torch.long, (self.max_spore_num,)),  # relative coordinate to view center
            'ball_x': (torch.long, (self.max_ball_num,)),  # relative coordinate to view center
            'ball_y': (torch.long, (self.max_ball_num,)),  # relative coordinate to view center
            'food_num': (torch.long, ()),
            'spore_num': (torch.long, ())
        }
        self.REWARD_INFO = {
            'score': (torch.float, ()),
            'spore': (torch.float, ()),
            'mate_spore': (torch.float, ()),
            'team_spore': (torch.float, ()),
            'clone': (torch.float, ()),
            'team_clone': (torch.float, ()),
            'opponent': (torch.float, ()),
            'team_opponent': (torch.float, ()),
            'max_dist': (torch.float, ()),
            'min_dist': (torch.float, ()),
        }

        self.ACTION_INFO = {
            'action': (torch.long, ()),
            'logit': (torch.float, (self.action_num,)),  # self.direction_num * 2, feed -3, split -2, stop -1,
            'action_logp': (torch.long, ()),
        }

    def get_rl_step_data(self, last=False):
        data = {}
        scalar_info = {k: torch.ones(size=v[1], dtype=v[0]) for k, v in self.SCALAR_INFO.items()}
        team_info = {k: torch.ones(size=v[1], dtype=v[0]) for k, v in self.TEAM_INFO.items()}
        ball_info = {k: torch.ones(size=v[1], dtype=v[0]) for k, v in self.BALL_INFO.items()}
        spatial_info = {k: torch.ones(size=v[1], dtype=v[0]) for k, v in self.SPATIAL_INFO.items()}
        action_mask = torch.zeros(size=(self.action_num,), dtype=torch.bool)

        data['obs'] = {'scalar_info': scalar_info, 'team_info': team_info, 'ball_info': ball_info,
                       'spatial_info': spatial_info, 'action_mask': action_mask}
        if not last:
            data['action'] = torch.zeros(size=(), dtype=torch.long)
            data['action_logp'] = torch.zeros(size=(), dtype=torch.float)
            data['reward'] = {k: torch.zeros(size=v[1], dtype=v[0]) for k, v in self.REWARD_INFO.items()}
            data['done'] = torch.zeros(size=(), dtype=torch.bool)
            data['model_last_iter'] = torch.zeros(size=(), dtype=torch.float)
        return data

    def get_player2team(self, ):
        player2team = {}
        for player_id in range(self.player_num_per_team * self.team_num):
            player2team[player_id] = player_id // self.player_num_per_team
        return player2team

    def transform_obs(self, obs, game_player_id=1, padding=True, last_action_type=None, ):
        global_state, player_observations = obs
        player2team = self.get_player2team()
        own_player_id = game_player_id
        leaderboard = global_state['leaderboard']
        team2rank = {key: rank for rank, key in enumerate(sorted(leaderboard, key=leaderboard.get, reverse=True), )}

        own_player_obs = player_observations[own_player_id]
        own_team_id = player2team[own_player_id]

        # ===========
        # scalar info
        # ===========
        scene_size = global_state['border'][0]
        own_left_top_x, own_left_top_y, own_right_bottom_x, own_right_bottom_y = own_player_obs['rectangle']
        own_view_center = [(own_left_top_x + own_right_bottom_x - scene_size) / 2,
                           (own_left_top_y + own_right_bottom_y - scene_size) / 2]
        own_view_width = float(own_right_bottom_x - own_left_top_x)
        # own_view_height = float(own_right_bottom_y - own_left_top_y)

        own_score = own_player_obs['score'] / 100
        own_team_score = global_state['leaderboard'][own_team_id] / 100
        own_rank = team2rank[own_team_id]

        scalar_info = {
            'view_x': torch.tensor(own_view_center[0]).round().long(),
            'view_y': torch.tensor(own_view_center[1]).round().long(),
            'view_width': torch.tensor(own_view_width).round().long(),
            'score': torch.log(torch.tensor(own_score) / 10).round().long().clamp_(max=9),
            'team_score': torch.log(torch.tensor(own_team_score / 10)).round().long().clamp_(max=9),
            'time': torch.tensor(global_state['last_time']//20, dtype=torch.long),
            'rank': torch.tensor(own_rank, dtype=torch.long),
            'last_action_type': torch.tensor(last_action_type, dtype=torch.long)
        }
        # ===========
        # team_info
        # ===========

        all_players = []
        scene_size = global_state['border'][0]

        for game_player_id in player_observations.keys():
            game_team_id = player2team[game_player_id]
            game_player_left_top_x, game_player_left_top_y, game_player_right_bottom_x, game_player_right_bottom_y = \
                player_observations[game_player_id]['rectangle']
            if game_player_id == own_player_id:
                alliance = 0
            elif game_team_id == own_team_id:
                alliance = 1
            else:
                alliance = 2
            if alliance != 2:
                game_player_view_x = (game_player_right_bottom_x + game_player_left_top_x - scene_size) / 2
                game_player_view_y = (game_player_right_bottom_y + game_player_left_top_y - scene_size) / 2

                # game_player_view_width = game_player_right_bottom_x - game_player_left_top_x
                # game_player_view_height = game_player_right_bottom_y -  game_player_left_top_y
                #
                # game_player_score = math.log((player_observations[game_player_id]['score'] + 1) / 1000)
                # game_player_team_score = math.log((global_state['leaderboard'][game_team_id] + 1) / 1000)
                # game_player_rank = team2rank[game_team_id]

                all_players.append([alliance,
                                    game_player_view_x,
                                    game_player_view_y,
                                    # game_player_view_width,
                                    # game_player_view_height,
                                    # game_player_score,
                                    # game_player_team_score,
                                    # game_player_rank,
                                    ])
        all_players = torch.as_tensor(all_players)
        player_padding_num = self.max_player_num - len(all_players)
        player_num = len(all_players)
        all_players = torch.nn.functional.pad(all_players, (0, 0, 0, player_padding_num), 'constant', 0)
        team_info = {
            'alliance': all_players[:, 0].long(),
            'view_x': all_players[:, 1].round().long(),
            'view_y': all_players[:, 2].round().long(),
            # 'view_width': all_players[:,3].round().long(),
            # 'view_height': all_players[:,4].round().long(),
            # 'score': all_players[:,5].round().long().clamp_(max=10,min=0),
            # 'team_score': all_players[:,6].round().long().clamp_(max=10,min=0),
            # 'team_rank': all_players[:,7].long(),
            'player_num': torch.tensor(player_num, dtype=torch.long),
        }

        # ===========
        # ball info
        # ===========
        ball_type_map = {'clone': 1, 'food': 2, 'thorns': 3, 'spore': 4}
        clone = own_player_obs['overlap']['clone']
        thorns = own_player_obs['overlap']['thorns']
        food = own_player_obs['overlap']['food']
        spore = own_player_obs['overlap']['spore']

        neutral_team_id = self.team_num
        neutral_player_id = self.team_num * self.player_num_per_team
        neutral_team_rank = self.team_num

        clone = [[ball_type_map['clone'], bl[3], bl[-2], bl[-1], team2rank[bl[-1]], bl[0], bl[1],
                  *self.next_position(bl[0], bl[1], bl[4], bl[5])] for bl in clone]
        thorns = [[ball_type_map['thorns'], bl[3], neutral_player_id, neutral_team_id, neutral_team_rank, bl[0], bl[1],
                   *self.next_position(bl[0], bl[1], bl[4], bl[5])] for bl in thorns]
        food = [
            [ball_type_map['food'], bl[3], neutral_player_id, neutral_team_id, neutral_team_rank, bl[0], bl[1], bl[0],
             bl[1]] for bl in food]

        spore = [
            [ball_type_map['spore'], bl[3], bl[-1], player2team[bl[-1]], team2rank[player2team[bl[-1]]], bl[0],
             bl[1],
             *self.next_position(bl[0], bl[1], bl[4], bl[5])] for bl in spore]

        all_balls = clone + thorns + food + spore

        for b in all_balls:
            if b[2] == own_player_id and b[0] == 1:
                if b[5] < own_left_top_x or b[5] > own_right_bottom_x or \
                        b[6] < own_left_top_y or b[6] > own_right_bottom_y:
                    b[5] = int((own_left_top_x + own_right_bottom_x) / 2)
                    b[6] = int((own_left_top_y + own_right_bottom_y) / 2)
                    b[7], b[8] = b[5], b[6]
        all_balls = torch.as_tensor(all_balls, dtype=torch.float)

        origin_x = own_left_top_x
        origin_y = own_left_top_y

        all_balls[:, -4] = ((all_balls[:, -4] - origin_x) / own_view_width * self.spatial_x)
        all_balls[:, -3] = ((all_balls[:, -3] - origin_y) / own_view_width * self.spatial_y)
        all_balls[:, -2] = ((all_balls[:, -2] - origin_x) / own_view_width * self.spatial_x)
        all_balls[:, -1] = ((all_balls[:, -1] - origin_y) / own_view_width * self.spatial_y)

        # ball
        ball_indices = torch.logical_and(all_balls[:, 0] != 2,
                                         all_balls[:, 0] != 4)  # include player balls and thorn balls
        balls = all_balls[ball_indices]

        balls_num = len(balls)

        # consider position of thorns ball
        if balls_num > self.max_ball_num:  # filter small balls
            own_indices = balls[:, 3] == own_player_id
            teammate_indices = (balls[:, 4] == own_team_id) & ~own_indices
            enemy_indices = balls[:, 4] != own_team_id

            own_balls = balls[own_indices]
            teammate_balls = balls[teammate_indices]
            enemy_balls = balls[enemy_indices]

            if own_balls.shape[0] + teammate_balls.shape[0] >= self.max_ball_num:
                remain_ball_num = self.max_ball_num - own_balls.shape[0]
                teammate_ball_score = teammate_balls[:, 1]
                teammate_high_score_indices = teammate_ball_score.sort(descending=True)[1][:remain_ball_num]
                teammate_remain_balls = teammate_balls[teammate_high_score_indices]
                balls = torch.cat([own_balls, teammate_remain_balls])
            else:
                remain_ball_num = self.max_ball_num - own_balls.shape[0] - teammate_balls.shape[0]
                enemy_ball_score = enemy_balls[:, 1]
                enemy_high_score_ball_indices = enemy_ball_score.sort(descending=True)[1][:remain_ball_num]
                remain_enemy_balls = enemy_balls[enemy_high_score_ball_indices]

                balls = torch.cat([own_balls, teammate_balls, remain_enemy_balls])
        balls_num = len(balls)
        ball_padding_num = self.max_ball_num - len(balls)
        if padding or ball_padding_num < 0:
            balls = torch.nn.functional.pad(balls, (0, 0, 0, ball_padding_num), 'constant', 0)
            alliance = torch.zeros(self.max_ball_num)
            balls_num = min(self.max_ball_num, balls_num)
        else:
            alliance = torch.zeros(balls_num)
        alliance[balls[:, 3] == own_team_id] = 2
        alliance[balls[:, 2] == own_player_id] = 1
        alliance[balls[:, 3] != own_team_id] = 3
        alliance[balls[:, 0] == 3] = 0

        ## score&radius
        scale_score = balls[:, 1] / 100
        radius = (torch.sqrt(scale_score * 0.042 + 0.15) / own_view_width).clamp_(max=1)
        score = ((torch.sqrt(scale_score * 0.042 + 0.15) / own_view_width).clamp_(max=1) * 50).round().long().clamp_(
            max=49)

        ## rank:
        ball_rank = balls[:, 4]

        ## coordinate
        x = balls[:, -4] - self.spatial_x // 2
        y = balls[:, -3] - self.spatial_y // 2
        next_x = balls[:, -2] - self.spatial_x // 2
        next_y = balls[:, -1] - self.spatial_y // 2

        ball_info = {
            'alliance': alliance.long(),
            'score': score.long(),
            'radius': radius,
            'rank': ball_rank.long(),
            'x': x.round().long(),
            'y': y.round().long(),
            'next_x': next_x.round().long(),
            'next_y': next_y.round().long(),
            'ball_num': torch.tensor(balls_num, dtype=torch.long)
        }

        # ============
        # spatial info
        # ============
        # ball coordinate for scatter connection
        ball_x = balls[:, -4]
        ball_y = balls[:, -3]

        food_indices = all_balls[:, 0] == 2
        food_x = all_balls[food_indices, -4]
        food_y = all_balls[food_indices, -3]
        food_num = len(food_x)
        food_padding_num = self.max_food_num - len(food_x)
        if padding or food_padding_num < 0:
            food_x = torch.nn.functional.pad(food_x, (0, food_padding_num), 'constant', 0)
            food_y = torch.nn.functional.pad(food_y, (0, food_padding_num), 'constant', 0)
        food_num = min(food_num, self.max_food_num)

        spore_indices = all_balls[:, 0] == 4
        spore_x = all_balls[spore_indices, -4]
        spore_y = all_balls[spore_indices, -3]
        spore_num = len(spore_x)
        spore_padding_num = self.max_spore_num - len(spore_x)
        if padding or spore_padding_num < 0:
            spore_x = torch.nn.functional.pad(spore_x, (0, spore_padding_num), 'constant', 0)
            spore_y = torch.nn.functional.pad(spore_y, (0, spore_padding_num), 'constant', 0)
        spore_num = min(spore_num, self.max_spore_num)

        spatial_info = {
            'food_x': food_x.round().clamp_(min=0, max=self.spatial_x - 1).long(),
            'food_y': food_y.round().clamp_(min=0, max=self.spatial_y - 1).long(),
            'spore_x': spore_x.round().clamp_(min=0, max=self.spatial_x - 1).long(),
            'spore_y': spore_y.round().clamp_(min=0, max=self.spatial_y - 1).long(),
            'ball_x': ball_x.round().clamp_(min=0, max=self.spatial_x - 1).long(),
            'ball_y': ball_y.round().clamp_(min=0, max=self.spatial_y - 1).long(),
            'food_num': torch.tensor(food_num, dtype=torch.long),
            'spore_num': torch.tensor(spore_num, dtype=torch.long)
        }

        output_obs = {
            'scalar_info': scalar_info,
            'team_info': team_info,
            'ball_info': ball_info,
            'spatial_info': spatial_info,
        }
        return output_obs

    def generate_action_mask(self, can_eject, can_split, ):
        action_mask = torch.zeros(size=(self.action_num,), dtype=torch.bool)
        if not can_eject:
            action_mask[self.direction_num * 2 + 1] = True
        if not can_split:
            action_mask[self.direction_num * 2 + 2] = True
        return action_mask

    def transform_action(self, action_idx):
        return self.x_y_action_List[int(action_idx)]

    def next_position(self, x, y, vel_x, vel_y):
        next_x = x + self.second_per_frame * vel_x * self.step_mul
        next_y = y + self.second_per_frame * vel_y * self.step_mul
        return next_x, next_y
