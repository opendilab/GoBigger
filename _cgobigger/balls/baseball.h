#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include "utils/structures.h"
#include "utils/utils.h"

using namespace std;


struct DefaultBase {
    float radius_min;
    float radius_max;
};


class BaseBall {
public:
    BaseBall() {}
    BaseBall(const string &name, Vector2 position, Border* border, float size,
             float radius_min, float radius_max) {
        this->name = name;
        this->position = position;
        this->border = border;
        this->size = size;
        this->radius_min = radius_min;
        this->radius_max = radius_max;
        this->is_remove = false;
        this->set_size(this->size);
        this->ball_type = 0;
    }
    BaseBall(Border* border, float size, float radius_min, float radius_max) {
        this->name = generate_uuid();
        this->border = border;
        this->position = border->sample();
        this->size = size;
        this->radius_min = radius_min;
        this->radius_max = radius_max;
        this->is_remove = false;
        this->set_size(this->size);
        this->ball_type = 0;
    }
    BaseBall(Vector2 position, Border* border, float size,
             float radius_min, float radius_max) {
        this->name = generate_uuid();
        this->position = position;
        this->border = border;
        this->size = size;
        this->radius_min = radius_min;
        this->radius_max = radius_max;
        this->is_remove = false;
        this->set_size(this->size);
        this->ball_type = 0;
    }
    void set_size(float size) {
        this->size = size;
        this->radius = sqrt(this->size);
        if (this->radius > this->radius_max) {
            this->radius = this->radius_max;
        } else if (this->radius < this->radius_min) {
            this->radius = this->radius_min;
        }
        this->size = this->radius * this->radius;
    }
    float get_dis(BaseBall* ball) {
        return this->position.distance(ball->position);
    }
    bool judge_cover(BaseBall* ball) {
        if (this->name == ball->name) {
            return false;
        }
        float dis = this->position.distance(ball->position);
        if ((this->radius > dis) || (ball->radius > dis)) {
            return true;
        } else {
            return false;
        }
    }
    bool judge_in_rectangle(vector<float> &rectangle) {
        float dx, dy;
        if (rectangle[0] > this->position.x) {
            dx = rectangle[0] - this->position.x;
        } else if (this->position.x > rectangle[2]) {
            dx = this->position.x - rectangle[2];
        } else {
            dx = 0.0f;
        }
        if (rectangle[1] > this->position.y) {
            dy = rectangle[1] - this->position.y;
        } else if (this->position.y > rectangle[3]) {
            dy = this->position.y - rectangle[3];
        } else {
            dy = 0.0f;
        }
        if (dx * dx + dy * dy <= this->radius * this->radius) {
            return true;
        } else {
            return false;
        }
    }
    void remove() {
        this->is_remove = true;
    }
    void echo() {
        cout << "name=" << this->name << ", "
             << "position=(" << this->position.x << ", " << this->position.y << "), "
             << "size=" << this->size << ", "
             << "radius=" << this->radius << endl;
    }
    bool operator <(const BaseBall &ball) {
        if (this->size < ball.size) {
            return true;
        } else {
            return false;
        }
    }
    bool operator >(const BaseBall &ball) {
        if (this->size > ball.size) {
            return true;
        } else {
            return false;
        }
    }
    bool operator ==(const BaseBall &ball) {
        if (this->size == ball.size) {
            return true;
        } else {
            return false;
        }
    }
    virtual void move(float duration) {}
    virtual void move(Vector2 &direction, float duration) {}
    virtual void move(Vector2 &given_acc, Vector2 &given_acc_center, float duration) {}
    virtual void eat(BaseBall*) {}
    virtual void eat_normal(BaseBall*) {}
    virtual void eat_thorns(BaseBall* ball, int clone_num, vector<BaseBall*> ret) {}
    virtual string get_team_name() {}
    virtual string get_owner() {}
    virtual string get_name() {}
    virtual Vector2 get_vel() {}
    virtual Vector2 get_acc() {}
    virtual Vector2 get_vel_last() {}
    virtual Vector2 get_acc_last() {}
    virtual Vector2 get_last_given_acc() {}
    virtual bool get_moving() {}
    string name;
    Vector2 position;
    Border* border;
    float size;
    float radius;
    float radius_min;
    float radius_max;
    bool is_remove;
    int ball_type;
    bool moving = false;
    string team_name;
    string owner;
};
