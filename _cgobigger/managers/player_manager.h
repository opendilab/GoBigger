#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <math.h>
#include <map>
#include <algorithm>
#include "balls/baseball.h"
#include "balls/foodball.h"
#include "balls/sporeball.h"
#include "balls/cloneball.h"
#include "spore_manager.h"
#include "utils/structures.h"
#include "utils/utils.h"
#include "utils/collision_detection.h"

using namespace std;


class HumanPlayer {
public:
    HumanPlayer() {}
    HumanPlayer(string &team_name, string &name, Border* border,
                DefaultCloneBall &default_clone_ball,
                DefaultSporeBall &default_spore_ball) {
        this->team_name = team_name;
        this->name = name;
        this->border = border;
        this->default_clone_ball = default_clone_ball;
        this->default_spore_ball = default_spore_ball;
        this->stop_flag = false;
    }
    int get_clone_num() {
        return this->balls.size();
    }
    void get_balls(vector<BaseBall*>& cloneballs) {
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            cloneballs.push_back(&(this->iter->second));
            this->iter++;
        }
    }
    void get_units(vector<Unit*>& units) {
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            Unit unit = Unit(this->iter->second.name,
                             this->iter->second.position.x,
                             this->iter->second.position.y,
                             this->iter->second.radius,
                             4);
            units.push_back(&unit);
            this->iter++;
        }
    }
    void size_decay() {
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            this->iter->second.size_decay();
            this->iter++;
        }
    }
    Vector2 cal_centroid() {
        float x = 0.0f;
        float y = 0.0f;
        float total_size = 0.0f;
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            x += this->iter->second.size * this->iter->second.position.x;
            y += this->iter->second.size * this->iter->second.position.y;
            total_size += this->iter->second.size;
            this->iter++;
        }
        Vector2 v = Vector2(x, y) / total_size;
        return v;
    }
    void remove_ball(string &ball_name) {
        auto iter = this->balls.find(ball_name);
        if (iter != this->balls.end()) {
            iter->second.remove();
        }
        this->balls.erase(ball_name);
    }
    float get_total_size() {
        float total_size = 0.0f;
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            total_size += this->iter->second.size;
            this->iter++;
        }
        return total_size;
    }
    void get_sort() {
        this->sort_balls.clear();
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            this->sort_balls.push_back(make_pair(this->iter->second.size, this->iter->second.name));
            this->iter++;
        }
        sort(this->sort_balls.begin(), this->sort_balls.end());
    }
    void respawn() {
        string ball_name = generate_uuid();
        Vector2 ball_position = this->border->sample();
        float ball_size = pow(this->default_clone_ball.radius_init, 2);
        Vector2 ball_vel = Vector2(0.0f, 0.0f);
        Vector2 ball_acc = Vector2(0.0f, 0.0f);
        Vector2 ball_last_vel = Vector2(0.0f, 0.0f);
        Vector2 ball_last_acc = Vector2(0.0f, 0.0f);
        Vector2 ball_last_given_acc = Vector2(0.0f, 0.0f);
        CloneBall ball = CloneBall(generate_uuid(), this->team_name, this->name, ball_position,
                                   this->border, ball_size, ball_vel, ball_acc, 
                                   ball_last_vel, ball_last_acc, ball_last_given_acc, false,
                                   this->default_clone_ball, this->default_spore_ball);
        Vector2 stop_tmp = Vector2(0.0f, 0.0f);
        ball.stop(stop_tmp);
        this->balls.clear();
        this->balls.insert(make_pair(ball.name, ball));
    }
    void adjust() {
        vector<string> to_remove_names;
        this->iter = this->balls.begin();
        this->iter2 = this->balls.begin();
        this->iter2++;
        while (this->iter2 != this->balls.end()) {
            if (!(this->iter->second.is_remove)) {
                while (this->iter2 != this->balls.end()) {
                    if (!(this->iter->second.is_remove) && !(this->iter2->second.is_remove)) {
                        float dis = this->iter->second.get_dis(&this->iter2->second);
                        if (dis < (this->iter->second.radius + this->iter2->second.radius)) {
                            if (this->iter->second.judge_rigid(this->iter2->second)) {
                                this->iter->second.rigid_collision(this->iter2->second);
                            } else {
                                if ((dis < this->iter->second.radius) || (dis < this->iter2->second.radius)) {
                                    if (this->iter->second.size > this->iter2->second.size) {
                                        this->iter->second.eat_normal(&(this->iter2->second));
                                        this->iter2->second.remove();
                                        to_remove_names.push_back(this->iter2->second.name);
                                    } else {
                                        this->iter2->second.eat_normal(&(this->iter->second));
                                        this->iter->second.remove();
                                        to_remove_names.push_back(this->iter->second.name);
                                    }
                                }
                            }
                        }
                    }
                    this->iter2++;
                }
                this->iter2 = this->iter;
                this->iter2++;
            }
            this->iter++;
            this->iter2 = this->iter;
            this->iter2++;
        }
        for (auto name : to_remove_names) {
            this->remove_ball(name);
        }
    }
    void stop() {
        if (this->stop_flag) {
            return;
        } else {
            this->stop_flag = true;
            Vector2 centroid = this->cal_centroid();
            Vector2 direction_center;
            this->iter = this->balls.begin();
            while (this->iter != this->balls.end()) {
                direction_center = centroid - this->iter->second.position;
                if (direction_center.length() == 0.0f) {
                    direction_center = Vector2(0.000001f, 0.000001f);
                }
                this->iter->second.stop(direction_center);
                this->iter++;
            }
        }
    }
    void split(Vector2 &direction) {
        this->get_sort();
        for (auto item : this->sort_balls) {
            if (this->balls[item.second].is_splitable(this->get_clone_num())) {
                CloneBall ball_tmp = this->balls[item.second].split(direction);
                this->balls[ball_tmp.name] = ball_tmp;
            }
        }
    }
    void eject(Vector2 &direction, vector<SporeBall>& sporeballs) {
        this->iter = this->balls.begin();
        while (this->iter != this->balls.end()) {
            if (this->iter->second.is_ejectable()) {
                this->iter->second.eject(direction, sporeballs);
            }
            this->iter++;
        }
    }
    void move(Vector2 &direction, float duration) {
        if (direction.length() != 0.0f) {
            this->stop_flag = false;
            this->iter = this->balls.begin();
            while (this->iter != this->balls.end()) {
                this->iter->second.stop_flag = false;
                this->iter++;
            }
        }
        if (this->stop_flag) {
            if (this->get_clone_num() == 1) {
                Vector2 given_acc_center = Vector2(0.0f, 0.0f);
                this->iter = this->balls.begin();
                while (this->iter != this->balls.end()) {
                    this->iter->second.move(given_acc_center, duration);
                    this->iter++;
                }
            } else {
                Vector2 centroid = this->cal_centroid();
                this->iter = this->balls.begin();
                while (this->iter != this->balls.end()) {
                    Vector2 given_acc_center = centroid - this->iter->second.position;
                    if (given_acc_center.length() == 0) {
                        given_acc_center = Vector2(0.000001f, 0.000001f);
                    } else if (given_acc_center.length() > 1) {
                        given_acc_center = given_acc_center.normalize();
                    }
                    given_acc_center = given_acc_center * 20;
                    this->iter->second.move(direction, given_acc_center, duration);
                    this->iter++;
                }
            }
        } else {
            if (this->get_clone_num() == 1) {
                this->iter = this->balls.begin();
                while (this->iter != this->balls.end()) {
                    Vector2 given_acc_center = Vector2(0.0f, 0.0f);
                    this->iter->second.move(direction, given_acc_center, duration);
                    this->iter++;
                }
            } else {
                Vector2 centroid = this->cal_centroid();
                this->iter = this->balls.begin();
                while (this->iter != this->balls.end()) {
                    Vector2 given_acc_center = centroid - this->iter->second.position;
                    if (given_acc_center.length() == 0.0f) {
                        given_acc_center = Vector2(0.000001f, 0.000001f);
                    } else if (given_acc_center.length() > 1.0f) {
                        given_acc_center = given_acc_center.normalize();
                    }
                    given_acc_center = given_acc_center * 20;
                    this->iter->second.move(direction, given_acc_center, duration);
                    this->iter++;
                }
            }
        }
        this->size_decay();
    }
    vector<float> get_rectangle(float width_full, float height_full, float scale_up_ratio,
                                float vision_x_min, float vision_y_min) {
        Vector2 centroid = this->cal_centroid();
        float xs_max = 0.0f;
        float ys_max = 0.0f;
        vector<BaseBall*> balls;
        this->get_balls(balls);
        for (auto ball : balls) {
            Vector2 direction_center = centroid - ball->position;
            if (abs(direction_center.x) + ball->radius > xs_max) {
                xs_max = abs(direction_center.x) + ball->radius;
            }
            if (abs(direction_center.y) + ball->radius > ys_max) {
                ys_max = abs(direction_center.y) + ball->radius;
            }
        }
        xs_max = max(xs_max, vision_x_min);
        ys_max = max(ys_max, vision_y_min);
        float scale_up_len = max(xs_max, ys_max);
        float left_top_x = min(max(centroid.x - scale_up_len * scale_up_ratio, 0.0f),
                               max(width_full - scale_up_len * scale_up_ratio * 2.0f, 0.0f));
        float left_top_y = min(max(centroid.y - scale_up_len * scale_up_ratio, 0.0f),
                               max(height_full - scale_up_len * scale_up_ratio * 2.0f, 0.0f));
        float right_bottom_x = min(left_top_x + scale_up_len * scale_up_ratio * 2.0f, width_full);
        float right_bottom_y = min(left_top_y + scale_up_len * scale_up_ratio * 2.0f, height_full);
        vector<float> rectangle {left_top_x, left_top_y, right_bottom_x, right_bottom_y};
        return rectangle;
    }
    void echo() {
        cout << this->name << " " << &(this->border) << " ";
        this->border->sample().echo();
    }
    string team_name;
    string name;
    Border* border;
    DefaultCloneBall default_clone_ball;
    DefaultSporeBall default_spore_ball;
    map<string, CloneBall> balls;
    map<string, CloneBall>::iterator iter;
    map<string, CloneBall>::iterator iter2;
    vector<pair<float, string>> sort_balls;
    bool stop_flag;
};


struct DefaultPlayerManager {
    DefaultCloneBall default_clone_ball;
};


class PlayerManager : public BaseManager {
public:
    PlayerManager() : BaseManager() {}
    PlayerManager(const DefaultPlayerManager &default_player_manager, Border* border, int team_num,
                  int player_num_per_team, const DefaultSporeManager &default_spore_manager) :
                  BaseManager(border) {
        this->default_player_manager = default_player_manager;
        this->team_num = team_num;
        this->player_num_per_team = player_num_per_team;
        this->default_spore_ball = default_spore_manager.default_spore_ball;
        this->border = border;
    }
    void init_balls() {
        for (int i = 0; i < this->team_num; i++) {
            string team_name = to_string(i);
            this->team_names.push_back(team_name);
            for (int j = 0; j < this->player_num_per_team; j++) {
                string player_name = to_string(i * this->player_num_per_team + j);
                this->player_names.push_back(player_name);
                HumanPlayer player = HumanPlayer(team_name, player_name, this->border,
                                                 this->default_player_manager.default_clone_ball,
                                                 this->default_spore_ball);
                player.respawn();
                this->players.insert(make_pair(player_name, player));
            }
        }
    }
    void init_balls_custom(vector<vector<float>> &custom_init) {
        for (int i = 0; i < this->team_num; i++) {
            string team_name = to_string(i);
            this->team_names.push_back(team_name);
            for (int j = 0; j < this->player_num_per_team; j++) {
                string player_name = to_string(i * this->player_num_per_team + j);
                this->player_names.push_back(player_name);
                HumanPlayer player = HumanPlayer(team_name, player_name, this->border,
                                                 this->default_player_manager.default_clone_ball,
                                                 this->default_spore_ball);
                this->players.insert(make_pair(player_name, player));
            }
        }
        for (auto item: custom_init) {
            Vector2 position_tmp = Vector2(item[0], item[1]);
            float radius_tmp = item[2];
            float size_tmp = pow(radius_tmp, 2);
            string player_name_tmp = to_string((int)item[3]);
            string team_name_tmp = to_string((int)item[4]);
            Vector2 vel_tmp = Vector2(item[5], item[6]);
            Vector2 acc_tmp = Vector2(item[7], item[8]);
            Vector2 vel_last_tmp = Vector2(item[9], item[10]);
            Vector2 acc_last_tmp = Vector2(item[11], item[12]);
            Vector2 direction_tmp = Vector2(item[13], item[14]);
            Vector2 last_given_acc_tmp = Vector2(item[15], item[16]);
            float age_tmp = item[17];
            bool cooling_last_tmp =item[18]>0 ? true : false;
            bool stop_flag_tmp =item[19]>0 ? true : false;
            float stop_time_tmp = item[20];
            Vector2 acc_stop_tmp = Vector2(item[21], item[22]);
            CloneBall ball = CloneBall(generate_uuid(), team_name_tmp, player_name_tmp, position_tmp,
                                       this->border, size_tmp, vel_tmp, acc_tmp,
                                       vel_last_tmp, acc_last_tmp, last_given_acc_tmp, stop_flag_tmp,
                                       this->default_player_manager.default_clone_ball,
                                       this->default_spore_ball);
            ball.direction = direction_tmp;
            ball.age = age_tmp;
            ball.cooling_last = cooling_last_tmp;
            ball.stop_time = stop_time_tmp;
            ball.acc_stop = acc_stop_tmp;
            this->players[player_name_tmp].balls.insert(make_pair(ball.name, ball));
        }
    }
    void get_balls(vector<BaseBall*>& cloneballs) {
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            this->iter->second.get_balls(cloneballs);
            this->iter++;
        }
    }
    void get_units(vector<Unit*>& units) {
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            this->iter->second.get_units(units);
            this->iter++;
        }
    }
    void get_players(vector<HumanPlayer*>& human_players) {
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            human_players.push_back(&(this->iter->second));
            this->iter++;
        }
    }
    void add_balls(vector<CloneBall>& to_add_balls) {
        for (int i = 0; i < to_add_balls.size(); i++) {
            this->players[to_add_balls[i].owner].balls
                .insert(make_pair(to_add_balls[i].name, to_add_balls[i]));
        }
    }
    void remove_ball(string &player_name, string &ball_name) {
        this->players[player_name].balls.erase(ball_name);
    }
    void step() {
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            map<string, CloneBall>::iterator iter_ball = this->iter->second.balls.begin();
//            cout << "clone " << this->iter->second.name << " from " << this->iter->second.balls.size();
            while (iter_ball != this->iter->second.balls.end()) {
                if (iter_ball->second.is_remove) {
                    iter_ball = this->iter->second.balls.erase(iter_ball);
                } else {
                    iter_ball++;
                }
            }
//            cout << " to " << this->iter->second.balls.size() << endl;
            if (this->iter->second.get_clone_num() == 0) {
                this->iter->second.respawn();
            }
            this->iter++;
        }
    }
    void adjust() {
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            this->iter->second.adjust();
            this->iter++;
        }
    }
    int get_clone_num(string &player_name) {
        return this->players[player_name].get_clone_num();
    }
    vector<string>* get_team_names() {
        return &(this->team_names);
    }
    vector<string>* get_player_names() {
        return &(this->player_names);
    }
    vector<float>* get_sizes() {
        this->sizes.clear();
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            this->sizes.push_back(this->iter->second.get_total_size());
            this->iter++;
        }
        return &(this->sizes);
    }
    map<string, float>* get_sizes_dict() {
        this->sizes_dict.clear();
        this->iter = this->players.begin();
        while (this->iter != this->players.end()) {
            this->sizes_dict.insert(make_pair(this->iter->second.name, this->iter->second.get_total_size()));
            this->iter++;
        }
        return &(this->sizes_dict);
    }
    void reset() {
        this->players.clear();
        this->team_names.clear();
        this->player_names.clear();
    }
    vector<vector<float>> get_frame_info() {
        vector<BaseBall*> cloneballs;
        this->get_balls(cloneballs);
        vector<vector<float>> frame_info(cloneballs.size(), vector<float>(23, 0.0f));
        this->iter = this->players.begin();
        int index = 0;
        while (this->iter != this->players.end()) {
            map<string, CloneBall>::iterator ball_iter = this->iter->second.balls.begin();
            while (ball_iter != this->iter->second.balls.end()) {
                frame_info[index][0] = ball_iter->second.position.x;
                frame_info[index][1] = ball_iter->second.position.y;
                frame_info[index][2] = ball_iter->second.radius;
                frame_info[index][3] = (float)(stoi(ball_iter->second.owner));
                frame_info[index][4] = (float)(stoi(ball_iter->second.team_name));
                frame_info[index][5] = ball_iter->second.vel.x;
                frame_info[index][6] = ball_iter->second.vel.y;
                frame_info[index][7] = ball_iter->second.acc.x;
                frame_info[index][8] = ball_iter->second.acc.y;
                frame_info[index][9] = ball_iter->second.vel_last.x;
                frame_info[index][10] = ball_iter->second.vel_last.y;
                frame_info[index][11] = ball_iter->second.acc_last.x;
                frame_info[index][12] = ball_iter->second.acc_last.y;
                frame_info[index][13] = ball_iter->second.direction.x;
                frame_info[index][14] = ball_iter->second.direction.y;
                frame_info[index][15] = ball_iter->second.last_given_acc.x;
                frame_info[index][16] = ball_iter->second.last_given_acc.y;
                frame_info[index][17] = ball_iter->second.age;
                frame_info[index][18] = ball_iter->second.cooling_last ? 1.0f : 0.0f;
                frame_info[index][19] = ball_iter->second.stop_flag ? 1.0f : 0.0f;
                frame_info[index][20] = ball_iter->second.stop_time;
                frame_info[index][21] = ball_iter->second.acc_stop.x;
                frame_info[index][22] = ball_iter->second.acc_stop.y;
                ball_iter++;
                index++;
            }
            this->iter++;
        }
        return frame_info;
    }
    DefaultPlayerManager default_player_manager;
    int team_num;
    int player_num_per_team;
    DefaultSporeBall default_spore_ball;
    map<string, HumanPlayer> players;
    map<string, HumanPlayer>::iterator iter;
    vector<string> team_names;
    vector<string> player_names;
    vector<float> sizes;
    map<string, float> sizes_dict;
};
