#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <map>
#include <algorithm>
#include "base_manager.h"
#include "balls/sporeball.h"
#include "utils/structures.h"
#include "utils/utils.h"
#include "utils/collision_detection.h"

using namespace std;


struct DefaultSporeManager {
    DefaultSporeBall default_spore_ball;
};

class SporeManager : public BaseManager {
public:
    SporeManager() : BaseManager() {}
    SporeManager(const DefaultSporeManager &default_spore_manager, Border* border) : BaseManager(border) {
        this->default_spore_manager = default_spore_manager;
        this->border = border;
    }
    void get_balls(vector<BaseBall*>& sporeballs) {
        map<string, SporeBall>::iterator iter = this->balls.begin();
        while (iter != balls.end()) {
            sporeballs.push_back(&(iter->second));
            iter++;
        }
    }
    void get_units(vector<Unit*>& units) {
        map<string, SporeBall>::iterator iter = this->balls.begin();
        while (iter != this->balls.end()) {
            Unit unit = Unit(iter->second.name,
                             iter->second.position.x,
                             iter->second.position.y,
                             iter->second.radius,
                             3);
            units.push_back(&unit);
            iter++;
        }
    }
    void add_balls(vector<SporeBall> &sporeballs) {
        for (auto ball : sporeballs) {
            this->balls.insert(make_pair(ball.name, ball));
        }
    }
    void spawn_ball_full(Vector2 &position, float size, Vector2 &direction, Vector2 &vel,
                         Vector2 &acc, float move_time, bool moving) {
        string name = generate_uuid();
        SporeBall ball = SporeBall(name, position, this->border, size,
                                 this->default_spore_manager.default_spore_ball);
        ball.direction = direction;
        ball.vel = vel;
        ball.acc = acc;
        ball.move_time = move_time;
        ball.moving = moving;
        this->balls.insert(make_pair(ball.name, ball));
    }
    void spawn_ball_custom(Vector2 &position, float size) {
        string name = generate_uuid();
        SporeBall ball = SporeBall(name, position, this->border, size,
                                 this->default_spore_manager.default_spore_ball);
        this->balls.insert(make_pair(ball.name, ball));
    }
    void init_balls() { }
    void init_balls_custom(vector<vector<float>> &custom_init) {
        for (auto item: custom_init) {
            Vector2 position_tmp = Vector2(item[0], item[1]);
            float radius_tmp = item[2];
            Vector2 direction_tmp = Vector2(item[3], item[4]);
            Vector2 vel_tmp = Vector2(item[5], item[6]);
            Vector2 acc_tmp = Vector2(item[7], item[8]);
            float move_time_tmp = item[9];
            bool moving_tmp = item[10];
            this->spawn_ball_full(position_tmp, pow(radius_tmp, 2), direction_tmp, vel_tmp,
                                    acc_tmp, move_time_tmp, moving_tmp);
        }
    }
    void remove_ball(string &name) {
        this->balls.erase(name);
    }
    void step(float duration) { }
    void reset() {
        this->balls.clear();
    }
    vector<vector<float>> get_frame_info() {
        vector<vector<float>> frame_info(this->balls.size(), vector<float>(11, 0.0f));
        map<string, SporeBall>::iterator iter = this->balls.begin();
        int index = 0;
        while (iter != this->balls.end()) {
            frame_info[index][0] = iter->second.position.x;
            frame_info[index][1] = iter->second.position.y;
            frame_info[index][2] = iter->second.radius;
            frame_info[index][3] = iter->second.direction.x;
            frame_info[index][4] = iter->second.direction.y;
            frame_info[index][5] = iter->second.vel.x;
            frame_info[index][6] = iter->second.vel.y;
            frame_info[index][7] = iter->second.acc.x;
            frame_info[index][8] = iter->second.acc.y;
            frame_info[index][9] = iter->second.move_time;
            frame_info[index][10] = iter->second.moving ? 1.0f : 0.0f;
            iter++;
            index++;
        }
        return frame_info;
    }
    DefaultSporeManager default_spore_manager;
    map<string, SporeBall> balls;
};
