#include <string>
#include <queue>
#include "server.h"
#include "balls/thornsball.h"
#include "balls/cloneball.h"


void test_server() {
    DefaultServer default_server;
    Server server = Server(default_server);
    string j = "";
    server.reset(j);
    map<string, vector<float>> actions;
    default_random_engine e = default_random_engine();
    e.seed(time(0));
    for (int i = 0; i < 1000; i++) {
        for (auto player_name: server.get_player_names()) {
            vector<float> action;
            float x = e() * 1.0f / e.max() * 2 - 1;
            float y = e() * 1.0f / e.max() * 2 - 1;
            int action_type = -1;
            action.push_back(x);
            action.push_back(y);
            action.push_back(action_type);
            actions.insert(make_pair(player_name, action));
        }
        chrono::steady_clock::time_point begin = chrono::steady_clock::now();
        server.step(actions);
        chrono::steady_clock::time_point end = chrono::steady_clock::now();
        cout << "cost = " << chrono::duration_cast<chrono::microseconds>(end - begin).count() << " us" << endl;
    }
}

void test_server_obs() {
    DefaultServer default_server;
    default_server.team_num = 1;
    default_server.player_num_per_team = 1;
    default_server.default_food_manager.num_init = 100;
    default_server.default_thorns_manager.num_init = 100;
    default_server.default_thorns_manager.default_thorns_ball.radius_min = 4;
    default_server.default_thorns_manager.default_thorns_ball.radius_max = 5;
    default_server.seed = 1638783661;
    Server server = Server(default_server);
    string j = "";
    server.reset(j);
    default_random_engine e = default_random_engine();
//    time_t my_seed = time(0);
    time_t my_seed = 1638786904;
    e.seed(my_seed);
    cout << my_seed << endl;
    for (int i = 0; i < 10000; i++ ) {
        if (i == 142) {
            cout << i << endl;
        }
        vector<BaseBall*> v;
        server.player_manager.get_balls(v);
        for (auto ball : v) {
            cout << i << " "
                 << "name=" << ball->get_name() << ", "
                 << "position=(" << ball->position.x << ", " << ball->position.y << "), "
                 << "radius=" << ball->radius << ", "
                 << "owner=" << ball->get_owner() << ", "
                 << "team_name=" << ball->get_team_name() << ", "
                 << "vel=(" << ball->get_vel().x << ", " << ball->get_vel().y << "), "
                 << "acc=(" << ball->get_acc().x << ", " << ball->get_acc().y << "), "
                 << "vel_last=(" << ball->get_vel_last().x << ", " << ball->get_vel_last().y << "), "
                 << "acc_last=(" << ball->get_acc_last().x << ", " << ball->get_acc_last().y << "), "
                 << "last_given_acc=(" << ball->get_last_given_acc().x << ", " << ball->get_last_given_acc().y << "), "
                 << endl;
        }
        map<string, vector<float>> actions;
        vector<float> action;
        action.push_back(e() * 1.0f / e.max() * 2 - 1);
        action.push_back(e() * 1.0f / e.max() * 2 - 1);
        action.push_back(-1);
        actions["0"] = action;
        if (i >= 142) {
            actions.clear();
            action.clear();
            action.push_back(0.0f);
            action.push_back(0.0f);
            action.push_back(-1);
            actions["0"] = action;
        }
        server.step(actions);
//        map<string, map<string, vector<vector<float>>>> obs = server.obs_default();
//        auto result = server.obs_partial_array();
    }
}

void test_eat_thornsball() {
    string ball_name = generate_uuid();
    string team_name = "0";
    string owner = "0";
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
//    Vector2 position = border.sample();
    Vector2 position = Vector2(500.0f, 500.0f);
    float size = 800.0f;
    Vector2 vel = Vector2(-30.0f, 0.0f);
    Vector2 acc = Vector2(-10.0f, 0.0f);
    Vector2 vel_last = Vector2(0.0f, 0.0f);
    Vector2 acc_last = Vector2(0.0f, 0.0f);
    Vector2 last_given_acc = Vector2(0.0f, 0.0f);
    bool stop_flag = false;
    DefaultSporeBall default_spore_ball;
    DefaultCloneBall default_clone_ball;
    CloneBall clone_ball = CloneBall(ball_name, team_name, owner, position, &border,
                                     size, vel, acc, vel_last, acc_last, last_given_acc,
                                     stop_flag, default_clone_ball, default_spore_ball);
    clone_ball.echo();

    string ball_name2 = generate_uuid();
    Vector2 position2 = border.sample();
    float size2 = 300.0f;
    Vector2 vel2 = Vector2(0.0f, 0.0f);
    Vector2 acc2 = Vector2(0.0f, 0.0f);
    DefaultThornsBall default_thorns_ball;
    ThornsBall thorns_ball = ThornsBall(ball_name2, position2, &border, size2, vel2, acc2,
                                        default_thorns_ball);
    cout << "start eat" << endl;
    vector<CloneBall> ret = clone_ball.eat_thorns(&thorns_ball, 1);
    clone_ball.echo();

    cout << "after eat_thorns ... " << endl;
    for (auto ball : ret) {
        ball.echo();
    }
}

void test_out() {
    DefaultServer default_server;
    default_server.team_num = 1;
    default_server.player_num_per_team = 1;
    Server server = Server(default_server);
    string j = "";
    server.reset(j);
    default_random_engine e = default_random_engine();
    e.seed(time(0));
    for (int i = 0; i < 10; i++ ) {
        vector<BaseBall*> v;
        server.player_manager.get_balls(v);
        for (auto ball : v) {
            cout << "position=(" << ball->position.x << ", " << ball->position.y << "), "
                 << "radius=" << ball->radius << ", "
                 << "owner=" << ball->owner << ", "
                 << "team_name=" << ball->get_team_name() << ", "
                 << "vel=(" << ball->get_vel().x << ", " << ball->get_vel().y << "), "
                 << "acc=(" << ball->get_acc().x << ", " << ball->get_acc().y << "), "
                 << endl;
        }
        map<string, vector<float>> actions;
        vector<float> action;
        action.push_back(0.0);
        action.push_back(-1);
        action.push_back(-1);
        actions["0"] = action;
        actions["0"] = action;
        server.step(actions);
    }
}

bool compare_func (BaseBall* a, BaseBall* b) {
    return (a->radius < b->radius);
}

class BotAgent {
public:
    BotAgent() {}
    BotAgent(string &name) : name(name) {}
    vector<float> step(vector<BaseBall*> &obs_food_balls,
                       vector<BaseBall*> &obs_thorns_balls,
                       vector<BaseBall*> &obs_spore_balls,
                       vector<BaseBall*> &obs_clone_balls) {
        vector<BaseBall*> my_clone_balls;
        vector<BaseBall*> other_clone_balls;
        for (auto ball : obs_clone_balls) {
            if (ball->get_owner() == this->name) {
                my_clone_balls.push_back(ball);
            } else {
                other_clone_balls.push_back(ball);
            }
        }
        sort(my_clone_balls.begin(), my_clone_balls.end(), compare_func);
        sort(other_clone_balls.begin(), other_clone_balls.end(), compare_func);

        if (my_clone_balls.size() >= 9 && my_clone_balls[4]->radius > 14.0f) {
            this->actions_queue.push({0.0f, 0.0f, 2.0f});
            this->actions_queue.push({0.0f, 0.0f, -1.0f});
            this->actions_queue.push({0.0f, 0.0f, -1.0f});
            this->actions_queue.push({0.0f, 0.0f, -1.0f});
            this->actions_queue.push({0.0f, 0.0f, -1.0f});
            this->actions_queue.push({0.0f, 0.0f, -1.0f});
            this->actions_queue.push({0.0f, 0.0f, -1.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            this->actions_queue.push({0.0f, 0.0f, 0.0f});
            vector<float> ret = this->actions_queue.front();
            this->actions_queue.pop();
            return ret;
        }
        Vector2 direction;
        float action_type = -1.0f;
        if (other_clone_balls.size() > 0 && my_clone_balls[0]->radius < other_clone_balls[0]->radius) {
            direction = my_clone_balls[0]->position - other_clone_balls[0]->position;
            direction = direction.normalize();
        } else {
            float min_thorns_distance = 10000.0f;
            bool min_thorns_ball_flag = false;
            BaseBall* min_thorns_ball;
            vector<BaseBall*> other_thorns_balls;
            for (auto ball : obs_thorns_balls) {
                if (ball->radius < my_clone_balls[0]->radius) {
                    float distance_tmp = (ball->position - my_clone_balls[0]->position).length();
                    if (distance_tmp < min_thorns_distance) {
                        min_thorns_distance = distance_tmp;
                        min_thorns_ball = ball;
                        min_thorns_ball_flag = true;
                    }
                }
            }
            if (min_thorns_ball_flag) {
                direction = (min_thorns_ball->position - my_clone_balls[0]->position).normalize();
            } else {
                float min_food_distance = 10000.0f;
                bool min_food_ball_flag = false;
                BaseBall* min_food_ball;
                for (auto ball : obs_food_balls) {
                    if (ball->radius < my_clone_balls[0]->radius) {
                        float distance_tmp = (ball->position - my_clone_balls[0]->position).length();
                        if (distance_tmp < min_food_distance) {
                            min_food_distance = distance_tmp;
                            min_food_ball = ball;
                            min_food_ball_flag = true;
                        }
                    }
                }
                if (min_food_ball_flag) {
                    direction = (min_food_ball->position - my_clone_balls[0]->position).normalize();
                } else {
                    direction = my_clone_balls[0]->position.normalize() * (-1.0f);
                }
            }
            float action_random = this->e() * 1.0f;
            if (action_random < 0.02f) {
                action_type = 1.0f;
            } else if (action_random < 0.04f && action_random > 0.02f) {
                action_type = 2.0f;
            }
        }
        direction = Vector2(((e() * 2.0f - 1.0f) * 0.1f) * direction.x,
                            ((e() * 2.0f - 1.0f) * 0.1f) * direction.y);
        this->actions_queue.push({direction.x, direction.y, action_type});
        vector<float> ret = this->actions_queue.front();
        this->actions_queue.pop();
        return ret;
    }
    queue<vector<float>> actions_queue;
    string name;
    default_random_engine e;

};


void test_server_new() {
    DefaultServer default_server;
//    default_server.team_num = 1;
//    default_server.player_num_per_team = 1;
//    default_server.seed = 1638783661;
    Server server = Server(default_server);
    string j = "";
    server.reset(j);
    vector<string> player_names = server.get_player_names();
    map<string, BotAgent> agents;
    for (auto player_name : player_names) {
        agents.insert(make_pair(player_name, BotAgent(player_name)));
    }
    default_random_engine e = default_random_engine();
    e.seed(time(0));
    for (int i = 0; i < 100000; i++ ) {
//        cout << i << endl;
        vector<BaseBall*> obs_food_balls;
        vector<BaseBall*> obs_thorns_balls;
        vector<BaseBall*> obs_spore_balls;
        vector<BaseBall*> obs_clone_balls;
        server.food_manager.get_balls(obs_food_balls);
        server.thorns_manager.get_balls(obs_thorns_balls);
        server.spore_manager.get_balls(obs_spore_balls);
        server.player_manager.get_balls(obs_clone_balls);

        vector<HumanPlayer*> players;
        server.player_manager.get_players(players);
        map<string, vector<float>> actions;
        for (auto player : players) {
            vector<BaseBall*> obs_food_balls_tmp;
            vector<BaseBall*> obs_thorns_balls_tmp;
            vector<BaseBall*> obs_spore_balls_tmp;
            vector<BaseBall*> obs_clone_balls_tmp;

            vector<float> rectangle = player->get_rectangle(server.map_width, server.map_height,
                                                            server.default_obs_setting.scale_up_ratio,
                                                            server.default_obs_setting.vision_x_min,
                                                            server.default_obs_setting.vision_y_min);
            float fr0 = rectangle[0] - server.default_food_manager.default_food_ball.radius_min;
            float fr1 = rectangle[1] - server.default_food_manager.default_food_ball.radius_min;
            float fr2 = rectangle[2] + server.default_food_manager.default_food_ball.radius_min;
            float fr3 = rectangle[3] + server.default_food_manager.default_food_ball.radius_min;
            for (auto ball: obs_food_balls) {
                if (ball->position.x > fr0 && ball->position.x < fr2
                    && ball->position.y > fr1 && ball->position.y < fr3) {
                    obs_food_balls_tmp.push_back(ball);
                }
            }
            for (auto ball: obs_thorns_balls) {
                if (ball->judge_in_rectangle(rectangle)) {
                    obs_thorns_balls_tmp.push_back(ball);
                }
            }
            for (auto ball: obs_spore_balls) {
                if (ball->judge_in_rectangle(rectangle)) {
                    obs_spore_balls_tmp.push_back(ball);
                }
            }
            for (auto ball: obs_clone_balls) {
                if (ball->judge_in_rectangle(rectangle)) {
                    obs_clone_balls_tmp.push_back(ball);
                }
            }
            vector<float> action = agents[player->name].step(obs_food_balls_tmp,
                                               obs_thorns_balls_tmp,
                                               obs_spore_balls_tmp,
                                               obs_clone_balls_tmp);
            actions.insert(make_pair(player->name, action));
        }
        if (server.step(actions)) {

            for (auto player : players) {
                cout << player->team_name << " "
                     << player->name << " "
                     << player->get_total_size() << " ";
            }
            cout << endl;
            break;
        }
    }
}


int main(int argc, char* argv[]) {
//    test_server();
//    test_server_obs();
//    test_eat_thornsball();
//    test_out();
//    test_time1();
    int count = 0;
    cout << "start" << endl;
    while (true) {
        count++;
        cout << count << " ";
        test_server_new();
    }
    return 0;
}

