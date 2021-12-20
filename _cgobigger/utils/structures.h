#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <map>
#include <ctime>
#include <algorithm>
#include <random>
#include <chrono>

using namespace std;


class Vector2 {
public:
    Vector2() : x(0.0f), y(0.0f) {}
    Vector2(float x, float y) : x(x), y(y) {}
    float getX() { return this->x; }
    void setX(float x) { this->x = x; }
    float geY() { return this->y; }
    void setY(float y) { this->y = y; }
    float distance(Vector2 &v) {
        return sqrt(pow(this->x - v.x, 2) + pow(this->y - v.y, 2));
    }
    Vector2 operator+(const Vector2& v) {
        Vector2 vv;
        vv.setX(this->x + v.x);
        vv.setY(this->y + v.y);
        return vv;
    }
    Vector2 operator-(const Vector2& v) {
        Vector2 vv;
        vv.setX(this->x - v.x);
        vv.setY(this->y - v.y);
        return vv;
    }
    Vector2 operator*(float v) {
        Vector2 vv;
        vv.setX(this->x * v);
        vv.setY(this->y * v);
        return vv;
    }
    Vector2 operator/(float v) {
        Vector2 vv;
        vv.setX(this->x / v);
        vv.setY(this->y / v);
        return vv;
    }
    float length() {
        return sqrt(pow(this->x, 2) + pow(this->y, 2));
    }
    Vector2 normalize() {
        Vector2 v;
        float norm = this->length();
        v.setX(this->x / norm);
        v.setY(this->y / norm);
        return v;
    }
    void echo() {
        cout << "Vector2(x=" << this->x << ", y=" << this->y << ")" << endl;
    }
    float x;
    float y;
};


class Border {
public:
    Border() : minx(0.0f), miny(0.0f), maxx(0.0f), maxy(0.0f), width(0.0f), height(0.0f) {
        this->seed = time(0);
        e.seed(this->seed);
    }
    Border(float minx, float miny, float maxx, float maxy) : 
        minx(minx), miny(miny), maxx(maxx), maxy(maxy) { 
        this->width = maxx - minx;
        this->height = maxy - miny;
        this->seed = time(0);
        e.seed(this->seed);
    }
    Border(float minx, float miny, float maxx, float maxy, time_t seed) : 
        minx(minx), miny(miny), maxx(maxx), maxy(maxy), seed(seed) { 
        this->width = maxx - minx;
        this->height = maxy - miny;
        e.seed(this->seed);
    }
    float getMinx() { return this->minx; }
    float getMiny() { return this->maxx; }
    float getMaxx() { return this->miny; }
    float getMaxy() { return this->maxy; }
    bool contains(Vector2 position) {
        if ((position.x > this->minx) && (position.x < this->maxx) 
            && (position.y > this->miny) && (position.y < this->maxy)) {
            return true;
        } else {
            return false;
        }
    }
    Vector2 sample() {
        float x = e() * 1.0f / e.max() * this->width + this->minx;
        float y = e() * 1.0f / e.max() * this->height + this->miny;
        Vector2 position = Vector2(x, y);
        return position;
    }
    float sample(float min_v, float max_v) {
        return e() * 1.0f / e.max() * (max_v - min_v) + min_v;
    }
    void echo() {
        cout << "Border(minx=" << this->minx << ", maxx=" << this->maxx
             << ", miny=" << this->miny << ", maxy=" << this->maxy << ")" << endl;
    }
    void set_seed(time_t seed) {
        this->seed = seed;
        e.seed(this->seed);
    }
    float minx;
    float miny;
    float maxx;
    float maxy;
    float width;
    float height;
    time_t seed;
    static default_random_engine e;
};

default_random_engine Border::e = default_random_engine();

