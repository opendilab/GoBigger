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


struct DefaultSporeBall {
    float radius_min = 3.0f;
    float radius_max = 3.0f;
    float vel_init = 250.0f;
    float vel_zero_time = 0.3f;
    float spore_radius_init = 20.0f;
};


class SporeBall : public BaseBall {
public:
    SporeBall() {}
    SporeBall(const string &name, Vector2 position, Border* border, float size,
              Vector2 direction, const DefaultSporeBall &default_spore_ball) :
        BaseBall(name, position, border, size, default_spore_ball.radius_min, default_spore_ball.radius_max) {
        this->vel_init = default_spore_ball.vel_init;
        this->vel_zero_time = default_spore_ball.vel_zero_time;
        this->spore_radius_init = default_spore_ball.spore_radius_init;
        this->direction = direction.normalize();
        this->vel = this->direction * this->vel_init;
        this->acc = this->direction * (this->vel_init / this->vel_zero_time) * (-1);
        this->move_time = 0;
        // reset size
        this->set_size(pow(this->spore_radius_init, 2));
        this->moving = true;
        this->ball_type = 3; // spore ball type id 3
        this->check_border();
    }
    SporeBall(const string &name, Vector2 position, Border* border, float size,
              const DefaultSporeBall &default_spore_ball) : 
        BaseBall(name, position, border, size, default_spore_ball.radius_min, default_spore_ball.radius_max) {
        this->vel_init = default_spore_ball.vel_init;
        this->vel_zero_time = default_spore_ball.vel_zero_time;
        this->spore_radius_init = default_spore_ball.spore_radius_init;
        this->direction = direction.normalize();
        this->vel = this->direction * this->vel_init;
        this->acc = this->direction * (this->vel_init / this->vel_zero_time) * (-1);
        this->move_time = 0;
        // reset size
        this->set_size(pow(this->spore_radius_init, 2));
        this->moving = true;
        this->ball_type = 3; // spore ball type id 3
        this->check_border();
    }
    void move(float duration) {
        this->position = this->position + this->vel * duration;
        this->move_time += duration;
        if (this->move_time < this->vel_zero_time) {
            this->vel = this->vel + this->acc * duration;
        } else {
            this->vel = Vector2();
            this->acc = Vector2();
            this->moving = false;
        }
        this->check_border();
    }
    void eat(BaseBall &ball) {
        cout << "SporeBall can not eat others" << endl;
    }
    void check_border() {
        if ((this->position.x < this->border->minx + this->radius) ||
            (this->position.x > this->border->maxx - this->radius)) {
            this->position.x = max(this->position.x, this->border->minx + this->radius);
            this->position.x = min(this->position.x, this->border->maxx - this->radius);
            this->vel.x = 0;
            this->acc.x = 0;
        }
        if ((this->position.y < this->border->miny + this->radius) ||
            (this->position.y > this->border->maxy - this->radius)) {
            this->position.y = max(this->position.y, this->border->miny + this->radius);
            this->position.y = min(this->position.y, this->border->maxy - this->radius);
            this->vel.y = 0;
            this->acc.y = 0;
        }
    }
    string get_name() {
        return this->name;
    }
    bool get_moving() {
        return this->moving;
    }
    Vector2 vel;
    Vector2 acc;
    float vel_init;
    float vel_zero_time;
    float spore_radius_init;
    float move_time;
    Vector2 direction;
    bool moving;
};

