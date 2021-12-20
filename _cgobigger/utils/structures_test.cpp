#include <string>
#include "structures.h"
#include "collision_detection.h"
#include "managers/food_manager.h"
#include "managers/player_manager.h"


void test_vector2() {
    Vector2 v1 = Vector2(1.0f, 2.0f);
    Vector2 v2 = Vector2(2.0f, 9.0f);
    Vector2 v3 = v1 + v2;
    Vector2 v4 = v1 - v2;
    Vector2 v5 = v1 * 2;
    Vector2 v6 = v1 / 2;
    Vector2 v7 = v1 + v2 * 2;
    v3.echo();
    v4.echo();
    v5.echo();
    v6.echo();
    v7.echo();
    Vector2 v8 = Vector2(0.0f, 0.0f);
    float x = v8.length();
    if (x == 0.0f) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
};


void test_border() {
    Border border1 = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    cout << "============== test_border ================" << endl;
    Vector2 position1 = border1.sample();
    cout << &border1 << " ";
    position1.echo();

    Border border2 = border1;
    Vector2 position2 = border2.sample();
    cout << &border2 << " ";
    position2.echo();

    Border border3 = border1;
    Vector2 position3 = border3.sample();
    cout << &border3 << " ";
    position3.echo();

    Border border4 = border1;
    Vector2 position4 = border4.sample();
    cout << &border4 << " ";
    position4.echo();

    Border border5 = border1;
    Vector2 position5 = border5.sample();
    cout << &border5 << " ";
    position5.echo();

    cout << "============ same =============" << endl;
    Vector2 position6 = border1.sample();
    position6.echo();
    Vector2 position7 = border1.sample();
    position7.echo();
    Vector2 position8 = border1.sample();
    position8.echo();
};

class Test1 {
public:
    Test1() {}
    Test1(string name, Border &border) {
        this->name = name;
        this->border = border;
    }
    void echo() {
        cout << &(this->border) << " ";
        Vector2 position = this->border.sample();
        position.echo();
    }
    string name;
    Border border;
};

class Test2 {
public:
    Test2(Border &border) {
        this->border = border;
    }
    void init_balls() {
        for (int i = 0; i < 3; i++) {
            string name = to_string(i);
            Test1 test1_tmp = Test1(name, this->border);
            test1_tmp.border.sample().echo();
            cout << &(test1_tmp) << endl;
            this->a.insert(make_pair(name, test1_tmp));
        }
    }
    void echo() {
        map<string, Test1>::iterator iter;
        iter = this->a.begin();
        while (iter != this->a.end()) {
            cout << &(iter->second) << endl;
            iter->second.echo();
            iter++;
        }
    }
    Border border;
    map<string, Test1> a;
};

// void test_border_2() {
//     Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
//     Test1 test1 = Test1(border);
//     Test1 test2 = Test1(border);
//     Test1 test3 = Test1(border);
//     cout << &(test1.border) << endl;
//     cout << &(test2.border) << endl;
//     cout << &(test3.border) << endl;
//     test1.border.sample().echo();
//     test2.border.sample().echo();
//     test3.border.sample().echo();
// };

void test_border_3() {
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Test2 test = Test2(border);
    cout << "======== init_balls =========" << endl;
    test.init_balls();
    cout << "======== echo =========" << endl;
    test.echo();
};

void test_collision_detection() {
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    PrecisionCollisionDetection p = PrecisionCollisionDetection(&border, 50);
    vector<BaseBall*> query;
    vector<BaseBall*> gallery;
    DefaultFoodManager default_food_manager;
    FoodManager food_manager = FoodManager(default_food_manager, &border);
    food_manager.init_balls();
    food_manager.get_balls(gallery);

    DefaultPlayerManager default_player_manager;
    default_player_manager.default_clone_ball.radius_init = 20.0f;
    int team_num = 4;
    int player_num_per_team = 3;
    DefaultSporeManager default_spore_manager;
    time_t seed = time(0);
    PlayerManager player_manager = PlayerManager(default_player_manager, &border, team_num,
                                                 player_num_per_team, default_spore_manager);
    player_manager.init_balls();
    player_manager.get_balls(query);

    vector<vector<BaseBall*>>* result = p.solve(query, gallery);
    for (int i = 0; i < (*result).size(); i++) {
        cout << "query : ";
        query[i]->echo();
        for (int j = 0; j < (*result)[i].size(); j++) {
            cout << "    ";
            (*result)[i][j]->echo();
        }
        cout << endl;
    }
}

int main(int argc, char* argv[]) {
    // test_vector2();
    // test_border();
    // test_border_2();
    // test_border_3();
    test_collision_detection();
};
