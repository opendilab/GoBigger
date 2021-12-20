#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <map>
#include <algorithm>
#include "base_manager.h"
#include "balls/sporeball.h"
#include "balls/thornsball.h"
#include "utils/structures.h"
#include "utils/utils.h"
#include "utils/collision_detection.h"

using namespace std;


struct DefaultThornsManager {
    int num_init = 15;
    int num_min = 15;
    int num_max = 20;
    float refresh_time = 2;
    int refresh_num = 2;
    DefaultThornsBall default_thorns_ball;
};

class ThornsManager : public BaseManager {
public:
    ThornsManager() : BaseManager() {}
    ThornsManager(const DefaultThornsManager &default_thorns_manager, Border* border) : BaseManager(border) {
        this->default_thorns_manager = default_thorns_manager;
        this->num_init = this->default_thorns_manager.num_init;
        this->num_min = this->default_thorns_manager.num_min;
        this->num_max = this->default_thorns_manager.num_max;
        this->refresh_time = this->default_thorns_manager.refresh_time;
        this->refresh_num = this->default_thorns_manager.refresh_num;
        this->border = border;
        this->refresh_time_count = 0.0f;
    }
    void get_balls(vector<BaseBall*>& thornsballs) {
        map<string, ThornsBall>::iterator iter = this->balls.begin();
        while (iter != this->balls.end()) {
            thornsballs.push_back(&(iter->second));
            iter++;
        }
    }
    void get_units(vector<Unit*>& units) {
        map<string, ThornsBall>::iterator iter = this->balls.begin();
        while (iter != this->balls.end()) {
            Unit unit = Unit(iter->second.name,
                             iter->second.position.x,
                             iter->second.position.y,
                             iter->second.radius,
                             2);
            units.push_back(&unit);
            iter++;
        }
    }
    void spawn_ball_random() {
        float radius_tmp = this->border->sample(
            this->default_thorns_manager.default_thorns_ball.radius_min,
            this->default_thorns_manager.default_thorns_ball.radius_max
        );
        ThornsBall ball = ThornsBall(this->border, pow(radius_tmp, 2),
                                     this->default_thorns_manager.default_thorns_ball);
        this->balls.insert(make_pair(ball.name, ball));
    }
    void spawn_ball_custom(Vector2 &position, float size) {
        ThornsBall ball = ThornsBall(position, this->border, size,
                                 this->default_thorns_manager.default_thorns_ball);
        this->balls.insert(make_pair(ball.name, ball));
    }
    void refresh() {
        int todo_num = min(this->refresh_num, this->num_max - (int)this->balls.size());
        for (int i = 0; i < todo_num; i++) {
            this->spawn_ball_random();
        }
    }
    void init_balls() {
        for (int i = 0; i < this->num_init; i++) {
            this->spawn_ball_random();
        }
    }
    void init_balls_custom(vector<vector<float>> &custom_init) {
        for (auto item: custom_init) {
            Vector2 position_tmp = Vector2(item[0], item[1]);
            float radius_tmp = item[2];
            this->spawn_ball_custom(position_tmp, pow(radius_tmp, 2));
        }
    }
    void remove_ball(string &name) {
        this->balls.erase(name);
    }
    void step(float duration) {
        this->refresh_time_count += duration;
        if (this->refresh_time_count >= this->refresh_time) {
            this->refresh();
            this->refresh_time_count = 0.0f;
        }
    }
    void reset() {
        this->refresh_time_count = 0.0f;
        this->balls.clear();
    }
    int num_init;
    int num_min;
    int num_max;
    float refresh_time;
    int refresh_num;
    float refresh_time_count;
    DefaultThornsManager default_thorns_manager;
    map<string, ThornsBall> balls;
};
