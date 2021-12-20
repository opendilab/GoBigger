#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <stdio.h>
#include <math.h>
#include <map>
#include <algorithm>
#include <chrono>
#include "balls/baseball.h"
#include "utils/structures.h"

using namespace std;


struct Unit {
    string name;
    float x;
    float y;
    float radius;
    int ball_type;
    Unit(string name, float x, float y, float radius, int ball_type) :
        name(name), x(x), y(y), radius(radius), ball_type(ball_type) {}
};


class PrecisionCollisionDetection {
public:
    PrecisionCollisionDetection() {}
    PrecisionCollisionDetection(Border* border, int precision) :
            border(border), precision(precision) {}

    int get_row(double x) {
        return min(max(0, (int)((x - this->border->minx) / this->border->height + this->precision)), this->precision);
    }
//    bool judge_cover(Unit* unit1, Unit* unit2) {
//        if (unit1->name == unit2->name) {
//            return false;
//        }
//        float dis = sqrt(pow(unit1->x - unit2->x, 2) + pow(unit1->y - unit1->y, 2));
//        if ((unit1->radius > dis) || (unit2->radius > dis)) {
//            return true;
//        } else {
//            return false;
//        }
//    }
    vector<vector<BaseBall*>>* solve(vector<BaseBall*>& query, vector<BaseBall*>& gallery) {
//        chrono::steady_clock::time_point begin = chrono::steady_clock::now();

        vector<pair<double, int> > vec[this->precision + 1];
        static vector<vector<BaseBall*>> results;
        results.clear();

        for (int i = 0; i < gallery.size(); i++) {
            int row_id = get_row(gallery[i]->position.x);
            vec[row_id].push_back(make_pair(gallery[i]->position.y, i));
        }

        for (int i = 0; i <= this->precision; i++)
            sort(vec[i].begin(), vec[i].end());

        for (int index = 0; index < query.size(); index++) {
            results.push_back({});
            double left = query[index]->position.y - query[index]->radius;
            double right = query[index]->position.y + query[index]->radius;
            int top = get_row(query[index]->position.x - query[index]->radius);
            int bottom = get_row(query[index]->position.x + query[index]->radius);

            for (int i = top; i < bottom + 1; i++) {
                if (vec[i].size() > 0) {
                    int l = vec[i].size();
                    int start_pos = 0;
                    for (int j = 15; j > 0; j--) {
                        int t = pow(2, j);
                        if ((start_pos+t < l) && (vec[i][start_pos+t].first < left))
                            start_pos += t;
                    }
                    for (int j = start_pos; j < l; j++) {
                        if (vec[i][j].first > right)
                            break;
                        if (query[index]->judge_cover(gallery[vec[i][j].second])) {
                            results[index].push_back(gallery[vec[i][j].second]);
                        }
                    }
                }
            }
        }

//        chrono::steady_clock::time_point end = chrono::steady_clock::now();
//        cout << "cost = " << chrono::duration_cast<chrono::microseconds>(end - begin).count() << " us" << endl;
        return &results;
    }
    Border* border;
    int precision;
};