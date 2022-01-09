#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <map>
#include <set>
#include <algorithm>
#include <chrono>
#include "balls/foodball.h"
#include "balls/sporeball.h"
#include "balls/thornsball.h"
#include "balls/cloneball.h"
#include "managers/food_manager.h"
#include "managers/spore_manager.h"
#include "managers/thorns_manager.h"
#include "managers/player_manager.h"
#include "utils/structures.h"
#include "utils/utils.h"
#include "utils/collision_detection.h"
#include "utils/file_helper.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
using namespace std;


struct DefaultObsSetting {
    bool with_spatial = true;
    bool with_speed = false;
    bool with_all_vision = false;
    float scale_up_ratio = 1.5f;
    float vision_x_min = 100.0f;
    float vision_y_min = 100.0f;
};

struct DefaultServer {
    int team_num = 4;
    int player_num_per_team = 3;
    float map_width = 1000.0f;
    float map_height = 1000.0f;
    float match_time = 600.0f;
    int state_tick_per_second = 10;
    int action_tick_per_second = 5;
    int load_bin_frame_num = -1; // -1 means all
    string jump_to_frame_file = "";
    int seed = (int)(time(0));
    DefaultFoodManager default_food_manager;
    DefaultThornsManager default_thorns_manager;
    DefaultSporeManager default_spore_manager;
    DefaultPlayerManager default_player_manager;
    DefaultObsSetting default_obs_setting;
};

struct OutputBall {
    float position_x;
    float position_y;
    float radius;
    float speed_x;
    float speed_y;
    int ball_type;
    string owner;
    string team_name;
    OutputBall(float position_x, float position_y, float radius, int ball_type) :
        position_x(position_x), position_y(position_y), radius(radius), ball_type(ball_type) {}
    OutputBall(float position_x, float position_y, float radius, int ball_type, string owner, string team_name) :
            position_x(position_x), position_y(position_y), radius(radius), ball_type(ball_type),
            owner(owner), team_name(team_name) {}
};

class Server {
public:
    Server(DefaultServer &default_server) {
        this->default_server = default_server;
        this->team_num = default_server.team_num;
        this->player_num_per_team = default_server.player_num_per_team;
        this->map_width = default_server.map_width;
        this->map_height = default_server.map_height;
        this->match_time = default_server.match_time;
        this->state_tick_per_second = default_server.state_tick_per_second;
        this->action_tick_per_second = default_server.action_tick_per_second;
        this->seed = default_server.seed;
        // other kwargs
        this->state_tick_duration = 1.0f / this->state_tick_per_second;
        this->action_tick_duration = 1.0f / this->action_tick_per_second;
        this->state_tick_per_action_tick = this->state_tick_per_second / this->action_tick_per_second;

        this->jump_to_frame_file = this->default_server.jump_to_frame_file;
        this->default_food_manager = this->default_server.default_food_manager;
        this->default_thorns_manager = this->default_server.default_thorns_manager;
        this->default_spore_manager = this->default_server.default_spore_manager;
        this->default_player_manager = this->default_server.default_player_manager;
        this->default_obs_setting = this->default_server.default_obs_setting;

        // basic kwargs
        this->border = Border(0.0f, 0.0f, this->map_width, this->map_height, this->seed);
        this->last_time = 0.0f;

        // managers
        this->food_manager = FoodManager(this->default_food_manager, &(this->border));
        this->thorns_manager = ThornsManager(this->default_thorns_manager, &(this->border));
        this->spore_manager = SporeManager(this->default_spore_manager, &(this->border));
        this->player_manager = PlayerManager(this->default_player_manager, &(this->border),
                                             this->team_num, this->player_num_per_team,
                                             this->default_spore_manager);
        // detection tools
        this->collision_detection = PrecisionCollisionDetection(&(this->border), 50);
    }
    void spawn_balls() {
        this->food_manager.init_balls();
        this->thorns_manager.init_balls();
        this->spore_manager.init_balls();
        this->player_manager.init_balls();
    }
    void spawn_balls(string &jump_to_frame_file) {
        map<string, vector<vector<float>>> balls = read_frame(jump_to_frame_file);
        this->food_manager.init_balls_custom(balls["food"]);
        this->spore_manager.init_balls_custom(balls["spore"]);
        this->thorns_manager.init_balls_custom(balls["thorns"]);
        this->player_manager.init_balls_custom(balls["clone"]);
    }

    void step_state_tick(map<string, vector<float>> actions) {
        vector<BaseBall*> moving_balls;
        vector<BaseBall*> total_balls;
        vector<HumanPlayer*> players;
        this->player_manager.get_players(players);
        if (actions.size() > 0) {
            for (auto player : players) {
                vector<float> player_action = actions[player->name];
                float x = player_action[0];
                float y = player_action[1];
                int action_type = (int)round(player_action[2]);
                Vector2 direction = Vector2(0.0f, 0.0f);
                if (x != 0.0f || y != 0.0f) {
                    direction.x = x;
                    direction.y = y;
                }
                if (action_type == 0 || action_type == 3) { // eject
                    vector<SporeBall> sporeballs;
                    player->eject(direction, sporeballs);
                    this->spore_manager.add_balls(sporeballs);
                }
                if (action_type == 1 || action_type == 4) { // split
                    player->split(direction);
                }
                if (action_type == 2) {
                    player->stop();
                } else if (action_type == 3 || action_type == 4) {
                    direction = Vector2(0.0f, 0.0f);
                    player->move(direction, this->state_tick_duration);
                    player->get_balls(moving_balls);
                } else {
                    player->move(direction, this->state_tick_duration);
                    player->get_balls(moving_balls);
                }
            }
        } else {
            for (auto player : players) {
                Vector2 direction = Vector2(0.0f, 0.0f);
                player->move(direction, this->state_tick_duration);
                player->get_balls(moving_balls);
            }
        }
        vector<BaseBall*> thorns_balls;
        this->thorns_manager.get_balls(thorns_balls);
        for (auto thorns_ball : thorns_balls) {
            if (thorns_ball->get_moving()) {
                thorns_ball->move(this->state_tick_duration);
            }
        }
        this->thorns_manager.get_balls(moving_balls);
        vector<BaseBall*> spore_balls;
        this->spore_manager.get_balls(spore_balls);
        for (auto spore_ball : spore_balls) {
            if (spore_ball->get_moving()) {
                spore_ball->move(this->state_tick_duration);
            }
        }
        this->player_manager.adjust();
        this->player_manager.get_balls(total_balls);
        this->thorns_manager.get_balls(total_balls);
        this->spore_manager.get_balls(total_balls);
        this->food_manager.get_balls(total_balls);
        vector<vector<BaseBall*>>* collisions_dict = this->collision_detection.solve(moving_balls, total_balls);

        for (int i = 0; i < moving_balls.size(); i++) {
            if (((*collisions_dict)[i].size() > 0) && (!(moving_balls[i]->is_remove))) {
                for (auto target_ball : (*collisions_dict)[i]) {
                    if ((!(moving_balls[i]->is_remove)) && (!(target_ball->is_remove))) {
                        if (moving_balls[i]->ball_type == 4) { // cloneball
                            CloneBall* moving_ball_pt = &(this->player_manager.players[moving_balls[i]->get_owner()]
                                                     .balls[moving_balls[i]->get_name()]);
                            if (target_ball->ball_type == 4) { // cloneball
                                CloneBall* target_ball_pt = &(this->player_manager.players[target_ball->get_owner()]
                                        .balls[target_ball->get_name()]);
                                if (moving_ball_pt->team_name != target_ball_pt->team_name) {
                                    if (moving_ball_pt->size > target_ball_pt->size) {
                                        moving_ball_pt->eat_normal(target_ball_pt);
//                                        this->player_manager.remove_ball(target_ball_pt->owner, target_ball_pt->name);
                                        target_ball->is_remove = true;
                                    } else {
                                        target_ball_pt->eat_normal(moving_ball_pt);
//                                        this->player_manager.remove_ball(moving_ball_pt->owner, moving_ball_pt->name);
                                        moving_balls[i]->is_remove = true;
                                    }
                                } else if (moving_ball_pt->owner != target_ball_pt->owner) {
                                    if (moving_ball_pt->size > target_ball_pt->size) {
                                        if (this->player_manager.get_clone_num(target_ball_pt->owner) > 1) {
                                            moving_ball_pt->eat_normal(target_ball_pt);
//                                            this->player_manager.remove_ball(target_ball_pt->owner, target_ball_pt->name);
                                            target_ball->is_remove = true;
                                        }
                                    } else {
                                        if (this->player_manager.get_clone_num(moving_ball_pt->owner) > 1) {
                                            target_ball_pt->eat_normal(moving_ball_pt);
//                                            this->player_manager.remove_ball(moving_ball_pt->owner, moving_ball_pt->name);
                                            moving_balls[i]->is_remove = true;
                                        }
                                    }
                                }
                            } else if (target_ball->ball_type == 1) { // foodball
                                FoodBall* target_ball_pt = &(this->food_manager.balls[target_ball->get_name()]);
                                moving_ball_pt->eat_normal(target_ball_pt);
//                                this->food_manager.remove_ball(target_ball_pt->name);
                                target_ball->is_remove = true;
                            } else if (target_ball->ball_type == 3) { // sporeball
                                SporeBall* target_ball_pt = &(this->spore_manager.balls[target_ball->get_name()]);
                                moving_ball_pt->eat_normal(target_ball_pt);
//                                this->spore_manager.remove_ball(target_ball_pt->name);
                                target_ball->is_remove = true;
                            } else if (target_ball->ball_type == 2) { // thornsball
                                ThornsBall* target_ball_pt = &(this->thorns_manager.balls[target_ball->get_name()]);
                                if (moving_ball_pt->size > target_ball_pt->size) {
                                    vector<CloneBall> clone_balls_on_thorns = moving_ball_pt->eat_thorns(target_ball_pt,
                                                         this->player_manager.get_clone_num(moving_ball_pt->owner));
//                                    this->thorns_manager.remove_ball(target_ball_pt->name);
                                    target_ball->is_remove = true;
                                    this->player_manager.add_balls(clone_balls_on_thorns);
                                }
                            }
                        } else if (moving_balls[i]->ball_type == 2) { // thornsball
                            ThornsBall* moving_ball_pt = &(this->thorns_manager.balls[moving_balls[i]->get_name()]);
                            if (target_ball->ball_type == 4) {
                                CloneBall* target_ball_pt = &(this->player_manager.players[target_ball->get_owner()]
                                                            .balls[target_ball->get_name()]);
                                if (moving_ball_pt->size < target_ball_pt->size) {
                                    vector<CloneBall> clone_balls_on_thorns = target_ball_pt->eat_thorns(moving_ball_pt,
                                                this->player_manager.get_clone_num(target_ball_pt->owner));
//                                    this->thorns_manager.remove_ball(moving_ball_pt->name);
                                    moving_balls[i]->is_remove = true;
                                    this->player_manager.add_balls(clone_balls_on_thorns);
                                }
                            } else if (target_ball->ball_type == 3) { // sporeball
                                SporeBall* target_ball_pt = &(this->spore_manager.balls[target_ball->get_name()]);
                                moving_ball_pt->eat(target_ball_pt);
//                                this->spore_manager.remove_ball(target_ball_pt->name);
                                target_ball->is_remove = true;
                            }
                        } else if (moving_balls[i]->ball_type == 3) { // sporeball
                            SporeBall* moving_ball_pt = &(this->spore_manager.balls[moving_balls[i]->get_name()]);
                            if (target_ball->ball_type == 4) { // cloneball
                                CloneBall* target_ball_pt = &(this->player_manager.players[target_ball->owner]
                                                            .balls[target_ball->name]);
                                target_ball_pt->eat_normal(moving_ball_pt);
//                                this->spore_manager.remove_ball(moving_ball_pt->name);
                                moving_balls[i]->is_remove = true;
                            } else if (target_ball->ball_type == 2) { // thornsball
                                ThornsBall* target_ball_pt = &(this->thorns_manager.balls[target_ball->name]);
                                target_ball_pt->eat(moving_ball_pt);
//                                this->spore_manager.remove_ball(moving_ball_pt->name);
                                moving_balls[i]->is_remove = true;
                            }
                        }
                    }
                }
            }
        }
        this->food_manager.step(this->state_tick_duration);
        this->spore_manager.step(this->state_tick_duration);
        this->thorns_manager.step(this->state_tick_duration);
        this->player_manager.step();
        this->last_time += this->state_tick_duration;
        moving_balls.clear();
        total_balls.clear();
    }
    void start(string &jump_to_frame_file) {
        if (jump_to_frame_file.empty()) {
            this->spawn_balls();
        } else {
            this->spawn_balls(jump_to_frame_file);
        }
    }
    void reset(string &jump_to_frame_file) {
        this->last_time = 0.0f;
        this->food_manager.reset();
        this->thorns_manager.reset();
        this->spore_manager.reset();
        this->player_manager.reset();
        this->start(jump_to_frame_file);
    }
    void close() {}
    bool step(map<string, vector<float>> actions) {
        if (this->last_time >= this->match_time) {
            return true;
        } else {
            for (int i = 0; i < this->state_tick_per_action_tick; i++ ) {
                this->step_state_tick(actions);
                if (i == 0) {
                    actions.clear();
                }
            }
        }
        return false;
    }
    py::array_t<float> obs_partial_array() {
        vector<BaseBall*> balls;
        this->food_manager.get_balls(balls);
        int food_end = balls.size();
        this->thorns_manager.get_balls(balls);
        int thorns_end = balls.size();
        this->spore_manager.get_balls(balls);
        int spore_end = balls.size();
        this->player_manager.get_balls(balls);
        int clone_end = balls.size();

        int player_start_index = 6;
        py::array_t<float, py::array::c_style> arr({clone_end, player_start_index + this->team_num * this->player_num_per_team});
        auto ra = arr.mutable_unchecked();

        for (int i = 0; i < clone_end; i++) {
            ra(i, 0) = balls[i]->position.x;
            ra(i, 1) = balls[i]->position.y;
            ra(i, 2) = balls[i]->radius;
            if (balls[i]->ball_type == 4) {
                ra(i, 3) = stof(balls[i]->get_owner());
                ra(i, 4) = stof(balls[i]->get_team_name());
            } else {
                ra(i, 3) = 0.0f;
                ra(i, 4) = 0.0f;
            }
        }
        ra(0, 5) = food_end;
        ra(1, 5) = thorns_end;
        ra(2, 5) = spore_end;
        ra(3, 5) = clone_end;
        int rect_start_index = 4;
        int size_start_index = rect_start_index + 4 * this->player_num_per_team * this->team_num;
        vector<HumanPlayer*> players;
        this->player_manager.get_players(players);
        for (auto player : players) {
            vector<float> rectangle = player->get_rectangle(this->map_width, this->map_height,
                                                            this->default_obs_setting.scale_up_ratio,
                                                            this->default_obs_setting.vision_x_min,
                                                            this->default_obs_setting.vision_y_min);
            ra(rect_start_index, 5) = rectangle[0];
            ra(rect_start_index+1, 5) = rectangle[1];
            ra(rect_start_index+2, 5) = rectangle[2];
            ra(rect_start_index+3, 5) = rectangle[3];
            rect_start_index = rect_start_index + 4;
            ra(size_start_index + stoi(player->name), 5) = player->get_total_size();
            int player_index = stoi(player->name);
            float fr0 = rectangle[0] - this->default_food_manager.default_food_ball.radius_min;
            float fr1 = rectangle[1] - this->default_food_manager.default_food_ball.radius_min;
            float fr2 = rectangle[2] + this->default_food_manager.default_food_ball.radius_min;
            float fr3 = rectangle[3] + this->default_food_manager.default_food_ball.radius_min;
            for (int i = 0; i < food_end; i++) {
                if (balls[i]->position.x > fr0 && balls[i]->position.x < fr2
                    && balls[i]->position.y > fr1 && balls[i]->position.y < fr3) {
                    ra(i, player_index + player_start_index) = 1.0f;
                } else {
                    ra(i, player_index + player_start_index) = 0.0f;
                }
            }
            for (int i = food_end; i < thorns_end; i++) {
                if (balls[i]->judge_in_rectangle(rectangle)) {
                    ra(i, player_index + player_start_index) = 1.0f;
                } else {
                    ra(i, player_index + player_start_index) = 0.0f;
                }
            }
            for (int i = thorns_end; i < spore_end; i++) {
                if (balls[i]->judge_in_rectangle(rectangle)) {
                    ra(i, player_index + player_start_index) = 1.0f;
                } else {
                    ra(i, player_index + player_start_index) = 0.0f;
                }
            }
            for (int i = spore_end; i < clone_end; i++) {
                if (balls[i]->judge_in_rectangle(rectangle)) {
                    ra(i, player_index + player_start_index) = 1.0f;
                } else {
                    ra(i, player_index + player_start_index) = 0.0f;
                }
            }
        }
        return arr;
    }
    py::array obs_full_array() {
        vector<BaseBall*> balls;
        this->food_manager.get_balls(balls);
        this->thorns_manager.get_balls(balls);
        this->spore_manager.get_balls(balls);
        this->player_manager.get_balls(balls);
        vector<float> ret (balls.size()*5, 0);
        int i = 0;
        for (auto ball : balls) {
            ret[i*5] = ball->position.x;
            ret[i*5+1] = ball->position.y;
            ret[i*5+2] = ball->radius;
            if (ball->ball_type == 4) {
                ret[i*5+3] = stof(ball->get_owner());
                ret[i*5+4] = stof(ball->get_team_name());
            }
            i++;
        }
        return py::array(ret.size(), ret.data());
    }
    vector<string> get_player_names() {
        vector<string>* ret = this->player_manager.get_player_names();
        return *ret;
    }
    vector<string> get_team_names() {
        vector<string>* ret = this->player_manager.get_team_names();
        return *ret;
    }
    void save_frame_info(string &save_frame_full_path) {
        map<string, vector<vector<float>>> balls;
        vector<vector<float>> food_frame_info = this->food_manager.get_frame_info();
        vector<vector<float>> thorns_frame_info = this->thorns_manager.get_frame_info();
        vector<vector<float>> spore_frame_info = this->spore_manager.get_frame_info();
        vector<vector<float>> clone_frame_info = this->player_manager.get_frame_info();
        balls.insert(make_pair("food", food_frame_info));
        balls.insert(make_pair("thorns", thorns_frame_info));
        balls.insert(make_pair("spore", spore_frame_info));
        balls.insert(make_pair("clone", clone_frame_info));
        save_frame(balls, save_frame_full_path);
    }
    int team_num;
    int player_num_per_team;
    float map_width;
    float map_height;
    float match_time;
    int state_tick_per_second;
    int action_tick_per_second;
    int seed;
    string save_path;
    bool save_bin;
    bool load_bin;
    string load_bin_path;
    int load_bin_frame_num; // -1 means all
    string jump_to_frame_file;
    DefaultFoodManager default_food_manager;
    DefaultThornsManager default_thorns_manager;
    DefaultSporeManager default_spore_manager;
    DefaultPlayerManager default_player_manager;
    DefaultObsSetting default_obs_setting;
    float state_tick_duration;
    float action_tick_duration;
    int state_tick_per_action_tick;
    FoodManager food_manager;
    ThornsManager thorns_manager;
    SporeManager spore_manager;
    PlayerManager player_manager;
    PrecisionCollisionDetection collision_detection;
    DefaultServer default_server;
    float last_time;
    Border border;
};
