#pragma once

#include <iostream>
#include <fstream>
#include <sstream>
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

map<string, vector<vector<float>>> read_frame(string &file_name) {
    ifstream file(file_name);
    string line;
    map<string, vector<vector<float>>> balls;
    while (getline(file, line)) {
        stringstream linestream(line);
        string data;
        int ball_type;
        vector<float> ball;
        linestream >> ball_type;
        switch (ball_type) {
            case 1: // food
                float position_x;
                float position_y;
                float radius;
                linestream >> position_x >> position_y >> radius;
                ball = {position_x, position_y, radius};
                balls["food"].push_back(ball);
                break;
            case 2: // thorns
                float vel_x;
                float vel_y;
                float acc_x;
                float acc_y;
                float move_time;
                float moving; // 1.0 true, 0.0 false
                linestream >> position_x >> position_y >> radius >> vel_x >> vel_y
                           >> acc_x >> acc_y >> move_time >> moving;
                ball = {position_x, position_y, radius, vel_x,
                        vel_y, acc_x, acc_y, move_time, moving};
                balls["thorns"].push_back(ball);
                break;
            case 3: // spore
                float direction_x;
                float direction_y;
                linestream >> position_x >> position_y >> radius
                           >> direction_x >> direction_y
                           >> vel_x >> vel_y
                           >> acc_x >> acc_y >> move_time >> moving;
                ball = {position_x, position_y, radius, direction_x, direction_y,
                        vel_x, vel_y, acc_x, acc_y, move_time, moving};
                balls["spore"].push_back(ball);
                break;
            case 4: // clone
                float owner;
                float team_name;
                float vel_last_x;
                float vel_last_y;
                float acc_last_x;
                float acc_last_y;
                float last_given_acc_x;
                float last_given_acc_y;
                float age;
                float cooling_last;
                float stop_flag;
                float stop_time;
                float acc_stop_x;
                float acc_stop_y;
                linestream >> position_x >> position_y >> radius >> owner >> team_name
                           >> vel_x >> vel_y >> acc_x >> acc_y
                           >> vel_last_x >> vel_last_y >> acc_last_x >> acc_last_y
                           >> direction_x >> direction_y >> last_given_acc_x >> last_given_acc_y
                           >> age >> cooling_last >> stop_flag >> stop_time
                           >> acc_stop_x >> acc_stop_y;
                ball = {position_x, position_y, radius, owner, team_name, vel_x, vel_y,
                        acc_x, acc_y, vel_last_x, vel_last_y, acc_last_x, acc_last_y,
                        direction_x, direction_y, last_given_acc_x, last_given_acc_y,
                        age, cooling_last, stop_flag, stop_time, acc_stop_x,acc_stop_y};
                balls["clone"].push_back(ball);
                break;
        }
    }
    return balls;
}


void save_frame(map<string, vector<vector<float>>> balls, string &file_name) {
    ofstream output(file_name);
    map<string, vector<vector<float>>>::iterator iter = balls.begin();
    while (iter != balls.end()) {
        for (int i = 0; i < iter->second.size(); i++) {
            if (iter->first == "food") {
                output << 1 << " ";
            } else if (iter->first == "thorns") {
                output << 2 << " ";
            } else if (iter->first == "spore") {
                output << 3 << " ";
            } else if (iter->first == "clone") {
                output << 4 << " ";
            }
            for (int j = 0; j < iter->second[i].size(); j++) {
                output << iter->second[i][j] << " ";
            }
            output << endl;
        }
        iter++;
    }
    output.close();
}
