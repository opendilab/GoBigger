#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <map>
#include <algorithm>
#include "base_manager.h"
#include "balls/foodball.h"
#include "utils/structures.h"
#include "utils/utils.h"
#include "utils/collision_detection.h"

using namespace std;


struct DefaultFoodManager {
    int num_init = 2000;
    int num_min = 2000;
    int num_max = 2500;
    float refresh_time = 2;
    int refresh_num = 30;
    DefaultFoodBall default_food_ball;
};

class FoodManager : public BaseManager {
public:
    FoodManager() : BaseManager() {}
    FoodManager(const DefaultFoodManager &default_food_manager, Border* border) : BaseManager(border) {
        this->default_food_manager = default_food_manager;
        this->num_init = this->default_food_manager.num_init;
        this->num_min = this->default_food_manager.num_min;
        this->num_max = this->default_food_manager.num_max;
        this->border = border;
        this->refresh_time = this->default_food_manager.refresh_time;
        this->refresh_num = this->default_food_manager.refresh_num;
        this->refresh_time_count = 0.0f;
    }
    void get_balls(vector<BaseBall*>& foodballs) {
        map<string, FoodBall>::iterator iter = this->balls.begin();
        while (iter != this->balls.end()) {
            foodballs.push_back(&(iter->second));
            iter++;
        }
    }
    void get_units(vector<Unit*>& units) {
        map<string, FoodBall>::iterator iter = this->balls.begin();
        while (iter != this->balls.end()) {
            Unit unit = Unit(iter->second.name,
                             iter->second.position.x,
                             iter->second.position.y,
                             iter->second.radius,
                             1);
            units.push_back(&unit);
            iter++;
        }
    }
    void spawn_ball_random() {
        FoodBall ball = FoodBall(this->border, 
                                 pow(this->default_food_manager.default_food_ball.radius_min, 2),
                                 this->default_food_manager.default_food_ball);
        this->balls.insert(make_pair(ball.name, ball));
    }
    void spawn_ball_custom(Vector2 &position, float size) {
        FoodBall ball = FoodBall(position, this->border, size,
                                 this->default_food_manager.default_food_ball);
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
    vector<vector<float>> get_frame_info() {
        vector<vector<float>> frame_info(this->balls.size(), vector<float>(3, 0.0f));
        map<string, FoodBall>::iterator iter = this->balls.begin();
        int index = 0;
        while (iter != this->balls.end()) {
            frame_info[index][0] = iter->second.position.x;
            frame_info[index][1] = iter->second.position.y;
            frame_info[index][2] = iter->second.radius;
            iter++;
            index++;
        }
        return frame_info;
    }
    int num_init;
    int num_min;
    int num_max;
    float refresh_time;
    int refresh_num;
    float refresh_time_count;
    DefaultFoodManager default_food_manager;
    map<string, FoodBall> balls;
};
