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


struct DefaultCloneBall {
    float acc_max = 100.0f;
    float vel_max = 25.0f;
    float radius_min = 3.0f;
    float radius_max = 300.0f;
    float radius_init = 3.0f;
    int part_num_max = 16;
    int on_thorns_part_num = 10;
    float on_thorns_part_radius_max = 20.0f;
    float split_radius_min = 10.0f;
    float eject_radius_min = 10.0f;
    float recombine_age = 20.0f;
    float split_vel_init = 30.0f;
    float split_vel_zero_time = 1.0f;
    float stop_zero_time = 1.0f;
    float size_decay_rate = 0.00005f;
    float given_acc_weight = 10.0f;
};


class CloneBall : public BaseBall {
public:
    CloneBall() {}
    CloneBall(const string &name, const string &team_name, const string &owner,
              Vector2 position, Border* border, float size,
              Vector2 vel, Vector2 acc, Vector2 vel_last, Vector2 acc_last, Vector2 last_given_acc,
              bool stop_flag, const DefaultCloneBall &default_clone_ball, 
              const DefaultSporeBall &default_spore_ball) : 
        BaseBall(name, position, border, size, default_clone_ball.radius_min, default_clone_ball.radius_max) {
        this->default_clone_ball = default_clone_ball;
        this->default_spore_ball = default_spore_ball;
        this->acc_max = default_clone_ball.acc_max;
        this->vel_max = default_clone_ball.vel_max;
        this->radius_init = default_clone_ball.radius_init;
        this->part_num_max = default_clone_ball.part_num_max;
        this->on_thorns_part_num = default_clone_ball.on_thorns_part_num;
        this->on_thorns_part_radius_max = default_clone_ball.on_thorns_part_radius_max;
        this->split_radius_min = default_clone_ball.split_radius_min;
        this->eject_radius_min = default_clone_ball.eject_radius_min;
        this->recombine_age = default_clone_ball.recombine_age;
        this->split_vel_init = default_clone_ball.split_vel_init;
        this->split_vel_zero_time = default_clone_ball.split_vel_zero_time;
        this->stop_zero_time = default_clone_ball.stop_zero_time;
        this->size_decay_rate = default_clone_ball.size_decay_rate;
        this->given_acc_weight = default_clone_ball.given_acc_weight;
        this->vel = vel;
        this->acc = acc;
        this->team_name = team_name;
        this->vel_last = vel_last;
        this->acc_last = acc_last;
        this->last_given_acc = last_given_acc;
        this->stop_flag = stop_flag;
        this->owner = owner;
        this->ball_type = 4; // spore ball type id 4
        this->split_acc_init = this->split_vel_init / this->split_vel_zero_time;
        this->age = 0;
        if (this->vel_last.length() > 0) {
            this->cooling_last = true;
        } else {
            this->cooling_last = false;
        }
        this->direction = (this->vel + this->vel_last + Vector2(0.00001, 0.00001)).normalize();
        this->vel_max_ball =0.0f;
        this->check_border();
    }
    Vector2 format_vector(Vector2 v, float norm_max) {
        if (v.length() < norm_max) {
            return v;
        } else {
            return v.normalize() * norm_max;
        }
    }
    float cal_vel_max(float radius) {
        return this->vel_max * 20 / (radius + 10);
    }
    void move(Vector2 &given_acc_center, float duration) {
        Vector2 given_acc = this->last_given_acc;
        this->move(given_acc, given_acc_center, duration);
    }
    void move(Vector2 &given_acc, Vector2 &given_acc_center, float duration) {
        this->age += duration;
        if (given_acc.length() != 0.0f) {
            given_acc = given_acc.normalize() * 10;
            this->last_given_acc = given_acc;
        } else {
            given_acc = this->last_given_acc;
        }
        if (this->stop_flag) {
            if (this->stop_time < this->stop_zero_time) {
                this->vel = this->vel + this->acc_stop * duration;
                this->vel_last = this->vel_last + this->acc_last * duration;
                this->stop_time += duration;
                if (this->stop_time >= this->stop_zero_time) {
                    this->vel = Vector2(0.0f, 0.0f);
                    this->acc_stop = Vector2(0.0f, 0.0f);
                    this->vel_last = Vector2(0.0f, 0.0f);
                    this->acc_last = Vector2(0.0f, 0.0f);
                }
                this->position = this->position + (this->vel + this->vel_last) * duration;
            } else {
                if (given_acc_center.length() == 0.0f) {
                    return;
                } else {
                    this->acc = this->format_vector(given_acc * this->acc_max, this->acc_max);
                    this->vel_max_ball = this->cal_vel_max(this->radius);
                    this->vel = this->format_vector(this->vel * 0.95 + 
                        (this->acc + this->format_vector(this->acc + given_acc_center/sqrt(this->radius), this->acc_max)) * duration, 
                        this->vel_max_ball);
                    this->position = this->position + this->vel * duration;
                }
            }
        } else {
            this->acc_stop = Vector2(0.0f, 0.0f);
            this->acc = this->format_vector(given_acc * this->acc_max, this->acc_max);
            this->vel_max_ball = this->cal_vel_max(this->radius);
            this->vel = this->format_vector(this->vel + 
                (this->acc + this->format_vector(this->acc + given_acc_center/sqrt(this->radius), this->acc_max)) * duration,
                this->vel_max_ball);
            if (this->cooling_last) {
                this->vel_last = this->vel_last + this->acc_last * duration;
                if (this->age >= this->split_vel_zero_time) {
                    this->vel_last = Vector2(0.0f, 0.0f);
                    this->acc_last = Vector2(0.0f, 0.0f);
                    this->cooling_last = false;
                }
            }
            this->position = this->position + (this->vel + this->vel_last) * duration;
        }
        if (this->vel.length() > 0 || this->vel_last.length() > 0) {
            this->direction = (this->vel + this->vel_last).normalize();
        }
        this->check_border();
    }
    void eat_normal(BaseBall* ball) {
        if (ball->ball_type == 1 || ball->ball_type == 3 || ball->ball_type == 4) {
            this->set_size(this->size + ball->size);
            if (this->radius > this->radius_max) {
                this->radius = this->radius_max;
            }
        }
        this->check_border();
    }
    vector<CloneBall> eat_thorns(ThornsBall* ball, int clone_num) {
        vector<CloneBall> ret;
        if (ball->ball_type == 2) { // thornsball
            this->set_size(this->size + ball->size);
            if (clone_num < this->part_num_max) {
                int split_num = min(this->part_num_max - clone_num, this->on_thorns_part_num);
                // on thorns
                float around_radius = min(sqrt(this->size / (split_num + 1)), this->on_thorns_part_radius_max);
                float around_size = around_radius * around_radius;
                float middle_size = this->size - around_size * split_num;
                this->set_size(middle_size);
                for (int i = 0; i < split_num; i++) {
                    float angle = 2 * M_PI * (i + 1) / split_num;
                    float unit_x = cos(angle);
                    float unit_y = sin(angle);
                    Vector2 around_vel = Vector2(this->split_vel_init * unit_x, this->split_vel_init * unit_y);
                    Vector2 around_acc = Vector2(this->split_acc_init * unit_x, this->split_acc_init * unit_y) * (-1);
                    Vector2 around_last_given_acc = Vector2(this->last_given_acc.x, this->last_given_acc.y);
                    Vector2 tmp_position = Vector2((this->radius + around_radius) * unit_x,
                                                   (this->radius + around_radius) * unit_y);
                    Vector2 around_position = this->position + tmp_position;
                    CloneBall around_ball = CloneBall(
                        generate_uuid(), this->team_name, this->owner, around_position,
                        this->border, around_size, this->vel, this->acc, 
                        around_vel, around_acc, around_last_given_acc, this->stop_flag,
                        this->default_clone_ball, this->default_spore_ball
                    );
                    ret.push_back(around_ball);
                }
            }
        }
        return ret;
    }
    bool is_ejectable() {
        return this->radius >= this->eject_radius_min;
    }
    void eject(Vector2 direction, vector<SporeBall>& sporeballs) {
        if (direction.length() == 0.0f) {
            direction = this->direction;
        }
        float spore_radius = this->default_spore_ball.radius_min;
        float spore_size = spore_radius * spore_radius;
        this->set_size(this->size - spore_size);
        Vector2 direction_unit = direction.normalize();
        Vector2 tmp_position = this->position + direction_unit * (this->radius + spore_radius);
        SporeBall ball = SporeBall(generate_uuid(), tmp_position, this->border, spore_size,
                                   direction_unit, default_spore_ball);
        sporeballs.push_back(ball);
    }
    bool is_splitable(int clone_num) {
        return this->radius >= this->split_radius_min && clone_num < this->part_num_max;
    }
    CloneBall split(Vector2 direction) {
        if (direction.length() == 0.0f) {
            direction = this->direction;
        }
        float split_size = this->size / 2;
        this->set_size(split_size);
        direction = direction.normalize();
        Vector2 position_split = this->position + direction * this->radius * 2;
        Vector2 vel_split = direction * this->split_vel_init;
        Vector2 acc_split = direction * this->split_acc_init * (-1);
        Vector2 last_given_acc_split = Vector2(this->last_given_acc.x, this->last_given_acc.y);
        CloneBall ball = CloneBall(
            generate_uuid(), this->team_name, this->owner, position_split,
            this->border, split_size, this->vel, this->acc, 
            vel_split, acc_split, last_given_acc_split, this->stop_flag,
            this->default_clone_ball, this->default_spore_ball
        );
        return ball;
    }
    void rigid_collision(CloneBall &ball) {
        if (this->name == ball.name) {
            return;
        }
        Vector2 p = ball.position - this->position;
        float d = p.length();
        float f = min(this->radius + ball.radius - d, (this->radius + ball.radius - d) / (d+0.00001f));
        this->position = this->position - p * f * (ball.size / (this->size + ball.size));
        ball.position = ball.position + p * f * (this->size / (this->size + ball.size));
        this->check_border();
        ball.check_border();
    }   
    void stop(Vector2 direction) {
        if (direction.length() == 0.0f) {
            direction = Vector2(0.000001f, 0.000001f);
        }
        this->stop_flag = true;
        this->stop_time = 0;
        this->acc_stop = (this->vel + this->vel_last) * (-1) / this->stop_zero_time;
        this->acc = Vector2(0.0f, 0.0f);
        this->direction = direction;
        this->last_given_acc = Vector2(0.0f, 0.0f);
    }
    bool judge_rigid(CloneBall &ball) {
        return (this->age < this->recombine_age || ball.age < ball.recombine_age);
    }
    void check_border() {
        if ((this->position.x < this->border->minx + this->radius) ||
            (this->position.x > this->border->maxx - this->radius)) {
            this->position.x = max(this->position.x, this->border->minx + this->radius);
            this->position.x = min(this->position.x, this->border->maxx - this->radius);
            this->vel.x = 0;
            this->acc.x = 0;
            this->acc_last.x = 0;
        }
        if ((this->position.y < this->border->miny + this->radius) ||
            (this->position.y > this->border->maxy - this->radius)) {
            this->position.y = max(this->position.y, this->border->miny + this->radius);
            this->position.y = min(this->position.y, this->border->maxy - this->radius);
            this->vel.y = 0;
            this->acc.y = 0;
            this->acc_last.y = 0;
        }
    }
    void size_decay() {
        this->set_size(this->size * (1 - this->size_decay_rate));
    }
    void echo() {
        cout << "position=(" << this->position.x << ", " << this->position.y << "), "
             << "radius=" << this->radius << ", "
             << "owner=" << this->owner << ", "
             << "team_name=" << this->team_name << ", "
             << "vel=(" << this->vel.x << ", " << this->vel.y << "), "
             << "acc=(" << this->acc.x << ", " << this->acc.y << "), "
             << "vel_last=(" << this->vel_last.x << ", " << this->vel_last.y << "), "
             << "acc_last=(" << this->acc_last.x << ", " << this->acc_last.y << "), "
             << endl;
    }
    string get_team_name() {
        return this->team_name;
    }
    string get_owner() {
        return this->owner;
    }
    string get_name() {
        return this->name;
    }
    Vector2 get_vel() {
        return this->vel;
    }
    Vector2 get_acc() {
        return this->acc;
    }
    Vector2 get_vel_last() {
        return this->vel_last;
    }
    Vector2 get_acc_last() {
        return this->acc_last;
    }
    Vector2 get_last_given_acc() {
        return this->last_given_acc;
    }
    bool get_moving() {
        return this->moving;
    }
    DefaultCloneBall default_clone_ball;
    DefaultSporeBall default_spore_ball;
    float acc_max;
    float vel_max;
    float radius_init;
    int part_num_max;
    int on_thorns_part_num;
    float on_thorns_part_radius_max;
    float split_radius_min;
    float eject_radius_min;
    float recombine_age;
    float split_vel_init;
    float split_vel_zero_time;
    float stop_zero_time;
    float size_decay_rate;
    float given_acc_weight;
    Vector2 vel_last;
    Vector2 acc_last;
    bool stop_flag;
    float age;
    float split_acc_init;
    bool cooling_last;
    Vector2 direction;
    Vector2 acc_stop;
    float vel_max_ball;
    float stop_time;
    bool moving;
    Vector2 last_given_acc;
    string team_name;
    string owner;
    Vector2 vel;
    Vector2 acc;
};

