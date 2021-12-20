#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include "baseball.h"
#include "utils/structures.h"
#include "utils/utils.h"

using namespace std;


struct DefaultFoodBall {
    float radius_min = 2.0f;
    float radius_max = 2.0f;
};


class FoodBall : public BaseBall {
public:
    FoodBall() {}
    FoodBall(const string &name, Vector2 position, Border* border, float size,
             Vector2 &vel, Vector2 &acc, const DefaultFoodBall default_food_ball) : 
        BaseBall(name, position, border, size, default_food_ball.radius_min, default_food_ball.radius_max) {
        this->ball_type = 1; // food ball type id 1
        this->check_border();
    }
    FoodBall(Border* border, float size, const DefaultFoodBall default_food_ball) :
        BaseBall(border, size, default_food_ball.radius_min, default_food_ball.radius_max) {
        this->ball_type = 1; // food ball type id 1
        this->check_border();
    }
    FoodBall(Vector2 position, Border* border, float size, const DefaultFoodBall default_food_ball) :
        BaseBall(border, size, default_food_ball.radius_min, default_food_ball.radius_max) {
        this->ball_type = 1; // food ball type id 1
        this->check_border();
    }
    void check_border() {
        if ((this->position.x < this->border->minx + this->radius) ||
            (this->position.x > this->border->maxx - this->radius)) {
            this->position.x = max(this->position.x, this->border->minx + this->radius);
            this->position.x = min(this->position.x, this->border->maxx - this->radius);
        }
        if ((this->position.y < this->border->miny + this->radius) ||
            (this->position.y > this->border->maxy - this->radius)) {
            this->position.y = max(this->position.y, this->border->miny + this->radius);
            this->position.y = min(this->position.y, this->border->maxy - this->radius);
        }
    }
    string get_name() {
        return this->name;
    }
    bool get_moving() {
        return this->moving;
    }
};

