#include <string>
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
        auto result = server.obs_partial_array();
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


int main(int argc, char* argv[]) {
//    test_server();
    test_server_obs();
//    test_eat_thornsball();
//    test_out();
//    test_time1();
    return 0;
}

