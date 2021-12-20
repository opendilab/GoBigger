#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include "baseball.h"
#include "sporeball.h"
#include "utils/structures.h"
#include "utils/utils.h"

using namespace std;


struct DefaultThornsBall {
    float radius_min = 12.0f;
    float radius_max = 20.0f;
    float eat_spore_vel_init = 10.0f;
    float eat_spore_vel_zero_time = 1.0f;
};


class ThornsBall : public BaseBall {
public:
    ThornsBall() {}
    ThornsBall(const string &name, Vector2 &position, Border* border, float size,
               Vector2 &vel, Vector2 &acc, const DefaultThornsBall &default_thorns_ball) : 
        BaseBall(name, position, border, size, default_thorns_ball.radius_min, default_thorns_ball.radius_max) {
        this->eat_spore_vel_init = default_thorns_ball.eat_spore_vel_init;
        this->eat_spore_vel_zero_time = default_thorns_ball.eat_spore_vel_zero_time;
        this->acc_default = this->eat_spore_vel_init / this->eat_spore_vel_zero_time;
        this->move_time = 0.0f;
        this->moving = false;
        this->vel = vel;
        this->acc = acc;
        this->ball_type = 2; // thorns ball type id 2
        this->check_border();
    }
    ThornsBall(Vector2 &position, Border* border, float size,
               const DefaultThornsBall &default_thorns_ball) : 
        BaseBall(position, border, size, default_thorns_ball.radius_min, default_thorns_ball.radius_max) {
        this->eat_spore_vel_init = default_thorns_ball.eat_spore_vel_init;
        this->eat_spore_vel_zero_time = default_thorns_ball.eat_spore_vel_zero_time;
        this->acc_default = this->eat_spore_vel_init / this->eat_spore_vel_zero_time;
        this->move_time = 0.0f;
        this->moving = false;
        this->ball_type = 2; // thorns ball type id 2
        this->check_border();
    }
    ThornsBall(Border* border, float size, const DefaultThornsBall &default_thorns_ball) :
        BaseBall(border, size, default_thorns_ball.radius_min, default_thorns_ball.radius_max) {
        this->eat_spore_vel_init = default_thorns_ball.eat_spore_vel_init;
        this->eat_spore_vel_zero_time = default_thorns_ball.eat_spore_vel_zero_time;
        this->acc_default = this->eat_spore_vel_init / this->eat_spore_vel_zero_time;
        this->move_time = 0.0f;
        this->moving = false;
        this->ball_type = 2; // thorns ball type id 2
        this->check_border();
    }
    void move(float duration) {
        if (this->moving) {
            this->position = this->position + this->vel * duration;
            this->move_time += duration;
            if (this->move_time < this->eat_spore_vel_zero_time) {
                this->vel = this->vel + this->acc * duration;
            } else {
                this->vel = Vector2(0.0f, 0.0f);
                this->acc = Vector2(0.0f, 0.0f);
                this->moving = false;
            }
            this->check_border();
        }
    }
    void eat(SporeBall* ball) {
        if (ball->ball_type == 3) {
            this->set_size(this->size + ball->size);
            if (this->radius > this->radius_max) {
                this->radius = this->radius_max;
            }
            if (ball->vel.length() > 0) {
                this->vel = ball->vel.normalize() * this->eat_spore_vel_init;
                this->acc = ball->vel.normalize() * this->acc_default * (-1);
                this->move_time = 0.0f;
                this->moving = true;
            }
        } else {
            cout << "ThornsBall can not eat " << typeid(this).name() << endl;
        }
        this->check_border();
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
    float eat_spore_vel_init;
    float eat_spore_vel_zero_time;
    float acc_default;
    float move_time;
    bool moving;
};

