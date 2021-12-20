#include <string>
#include <map>
#include <vector>
#include "baseball.h"
#include "foodball.h"
#include "sporeball.h"
#include "thornsball.h"
#include "cloneball.h"
#include "utils/structures.h"
#include "utils/utils.h"

using namespace std;


void test_baseball() {
    string ball_name = "baseball1";
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    float radius_min = 3.0f;
    float radius_max = 100.0f;
    BaseBall base_ball = BaseBall(ball_name, position, &border, size, vel, acc,
                                  radius_min, radius_max);
    base_ball.echo();
};

void test_foodball() {
    string ball_name = generate_uuid();
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    DefaultFoodBall default_food_ball;
    default_food_ball.radius_min = 2.0f;
    default_food_ball.radius_max = 2.0f;
    FoodBall food_ball = FoodBall(ball_name, position, border, size, vel, acc,
                                  default_food_ball);
    cout << food_ball.radius_min << endl;
    food_ball.echo();
}

void test_sporeball() {
    string ball_name = generate_uuid();
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    Vector2 direction = Vector2(1.0f, 0.0f);
    DefaultSporeBall default_spore_ball;
    default_spore_ball.radius_min = 3.0f;
    default_spore_ball.radius_max = 3.0f;
    default_spore_ball.vel_init = 250;
    default_spore_ball.vel_zero_time = 0.3f;
    default_spore_ball.spore_radius_init = 20.0f;
    SporeBall spore_ball = SporeBall(ball_name, position, border, size, vel, acc,
                                     direction, default_spore_ball);
    spore_ball.echo();
}

void test_thornsball() {
    string ball_name = generate_uuid();
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 225.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    DefaultThornsBall default_thorns_ball;
    default_thorns_ball.radius_min = 15.0f;
    default_thorns_ball.radius_max = 20.0f;
    default_thorns_ball.eat_spore_vel_init = 10;
    default_thorns_ball.eat_spore_vel_zero_time = 1.0f;
    ThornsBall thorns_ball = ThornsBall(ball_name, position, border, size, vel, acc,
                                       default_thorns_ball);
    thorns_ball.echo();
}

template<typename T>
void test(vector<T> *balls){
    for (int i = 0; i < balls->size(); i++) {
        (*balls)[i].echo();
        cout << (*balls)[i].name << endl;
    }
    for (int i = 0; i < 10; i++) {
        string ball_name = generate_uuid();
        Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
        Vector2 position = border.sample();
        float size = 4.0f;
        Vector2 vel = Vector2(0.0f, 0.0f);
        Vector2 acc = Vector2(0.0f, 0.0f);
        DefaultFoodBall default_food_ball;
        default_food_ball.radius_min = 2.0f;
        default_food_ball.radius_max = 2.0f;
        FoodBall food_ball = FoodBall(ball_name, position, border, size, vel, acc,
                                      default_food_ball);
        balls->push_back(food_ball);
    }
}

void test_parse_vector() {
    vector<BaseBall> balls;
    test(&balls);
    for (int i = 0; i < balls.size(); i++) {
        balls[i].echo();
        cout << balls[i].name << endl;
    }
}

void test_different_balls() {
    vector<BaseBall> balls;
    for (int i = 0; i < 10; i++) {
        string ball_name = generate_uuid();
        Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
        Vector2 position = border.sample();
        float size = 4.0f;
        Vector2 vel = Vector2(0.0f, 0.0f);
        Vector2 acc = Vector2(0.0f, 0.0f);
        DefaultFoodBall default_food_ball;
        default_food_ball.radius_min = 2.0f;
        default_food_ball.radius_max = 2.0f;
        FoodBall food_ball = FoodBall(ball_name, position, border, size, vel, acc,
                                      default_food_ball);
        balls.push_back(food_ball);
    }
    for (int i = 0; i < 10; i++) {
        string ball_name = generate_uuid();
        Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
        Vector2 position = border.sample();
        float size = 4.0f;
        Vector2 vel = Vector2(0.0f, 0.0f);
        Vector2 acc = Vector2(0.0f, 0.0f);
        Vector2 direction = Vector2(1.0f, 0.0f);
        DefaultSporeBall default_spore_ball;
        default_spore_ball.radius_min = 3.0f;
        default_spore_ball.radius_max = 3.0f;
        default_spore_ball.vel_init = 250;
        default_spore_ball.vel_zero_time = 0.3f;
        default_spore_ball.spore_radius_init = 20.0f;
        SporeBall spore_ball = SporeBall(ball_name, position, border, size, vel, acc,
                                         direction, default_spore_ball);
        balls.push_back(spore_ball);
    }
    cout << balls.size() << endl;
    test(&balls);
}

void test_cloneball() {
    string ball_name = generate_uuid();
    string team_name = "0";
    string owner = "0";
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    Vector2 vel_last = Vector2(0.0f, 0.0f);
    Vector2 acc_last = Vector2(0.0f, 0.0f);
    bool stop_flag = false;
    DefaultSporeBall default_spore_ball;
    default_spore_ball.radius_min = 3.0f;
    default_spore_ball.radius_max = 3.0f;
    default_spore_ball.vel_init = 250;
    default_spore_ball.vel_zero_time = 0.3f;
    default_spore_ball.spore_radius_init = 20.0f;
    DefaultCloneBall default_clone_ball;
    CloneBall clone_ball = CloneBall(ball_name, team_name, owner, position, border,
                                     size, vel, acc, vel_last, acc_last,
                                     stop_flag, default_clone_ball, default_spore_ball);
    clone_ball.echo();
}

vector<BaseBall*> test_get() {
    vector<BaseBall*> balls;
    string ball_name = generate_uuid();
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    DefaultFoodBall default_food_ball;
    default_food_ball.radius_min = 2.0f;
    default_food_ball.radius_max = 2.0f;
    FoodBall food_ball = FoodBall(ball_name, position, border, size, vel, acc,
                                  default_food_ball);
    balls.push_back(&food_ball);
    return balls;
}

void test_get_base() {
    vector<BaseBall*> balls = test_get();
    for (int i = 0; i < balls.size(); i++) {
        balls[i]->echo();
    }
}

void test_get2(vector<BaseBall*>& balls) {
    string ball_name = generate_uuid();
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    DefaultFoodBall default_food_ball;
    default_food_ball.radius_min = 2.0f;
    default_food_ball.radius_max = 2.0f;
    FoodBall food_ball = FoodBall(ball_name, position, border, size, vel, acc,
                                  default_food_ball);
    balls.push_back(&(food_ball));
}

void test_get_base2() {
    vector<BaseBall*> balls;
    test_get2(balls);
    for (int i = 0; i < balls.size(); i++) {
        balls[i]->echo();
        cout << balls[i]->ball_type << endl;
    }
}

void test_get_base3() {
    vector<BaseBall*> balls;
    string ball_name = generate_uuid();
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    DefaultFoodBall default_food_ball;
    default_food_ball.radius_min = 2.0f;
    default_food_ball.radius_max = 2.0f;
    FoodBall food_ball = FoodBall(ball_name, position, border, size, vel, acc,
                                  default_food_ball);
    cout << &food_ball << endl;
    map<string, FoodBall> bs;
    auto p = bs.insert(make_pair(ball_name, food_ball));
    map<string, FoodBall>::iterator iter;
    iter = bs.begin();
    while (iter != bs.end()) {
        cout << iter->first << " : " << iter->second.name << endl;
        balls.push_back(&(iter->second));
        iter++;
    }
    // balls.push_back(&food_ball);
    // cout << bs[food_ball.name].name << endl;
    // balls.push_back(&(bs[food_ball.name]));
    for (int i = 0; i < balls.size(); i++) {
        balls[i]->echo();
        cout << balls[i]->ball_type << endl;
    }
}

void test_operator() {
    string ball_name = "baseball1";
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    float radius_min = 3.0f;
    float radius_max = 100.0f;
    BaseBall ball1 = BaseBall(ball_name, position, border, size, vel, acc,
                                   radius_min, radius_max);
    BaseBall ball2 = BaseBall(ball_name, position, border, size, vel, acc,
                                   radius_min, radius_max);
    ball1.size = 100.0f;
    cout << ball1.size << " " << ball2.size << endl;
    if (ball1 < ball2) {
        cout << "ball1 < ball2" << endl;
    } else {
        cout << "ball1 > ball2" << endl;
    }
}

bool cmp_by_value(const pair<string, BaseBall>& lhs, const pair<string, BaseBall>& rhs) {
  return lhs.second.size < rhs.second.size;
}

template<typename A, typename B>
std::pair<float, string> flip_pair(const std::pair<string, float> &p)
{
    return std::pair<float,string>(p.second, p.first);
}

void test_operator_in_map() {
    string ball_name1 = "baseball1";
    string ball_name2 = "baseball2";
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Vector2 position = border.sample();
    float size = 4.0f;
    Vector2 vel = Vector2(0.0f, 0.0f);
    Vector2 acc = Vector2(0.0f, 0.0f);
    float radius_min = 3.0f;
    float radius_max = 100.0f;
    BaseBall ball1 = BaseBall(ball_name1, position, border, size, vel, acc,
                                   radius_min, radius_max);
    BaseBall ball2 = BaseBall(ball_name2, position, border, size, vel, acc,
                                   radius_min, radius_max);
    ball2.size = 100.0f;
    map<string, BaseBall> m;
    m.insert(make_pair(ball1.name, ball1));
    m.insert(make_pair(ball2.name, ball2));
    vector<pair<float, string>> vv;
    map<string, BaseBall>::iterator iter = m.begin();
    while (iter != m.end()) {
        vv.push_back(make_pair(iter->second.size, iter->second.name));
        iter++;
    }
    sort(vv.begin(), vv.end());
    cout << "vv size = " << vv.size() << endl;
    for (int i = 0; i < vv.size(); ++i) {
        cout << i << " " << vv[i].first << " " << vv[i].second << endl;
        m[vv[i].second].echo();
    }
}


int main(int argc, char* argv[]) {
    // test_baseball();
    // test_foodball();
    // test_sporeball();
    // test_thornsball();
    // test_parse_vector();
    // test_different_balls();
    // test_cloneball();
    // test_get_base();
    // test_get_base2();
    // test_get_base3();
    // test_operator();
    test_operator_in_map();
};
