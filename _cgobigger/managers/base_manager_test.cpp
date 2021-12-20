#include <string>
#include "base_manager.h"
#include "food_manager.h"
#include "spore_manager.h"
#include "thorns_manager.h"
#include "player_manager.h"
#include "balls/baseball.h"
#include "balls/cloneball.h"
#include "utils/structures.h"
#include "utils/utils.h"

using namespace std;


void test_food_manager() {
    DefaultFoodManager default_food_manager;
    default_food_manager.num_init = 10;
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    FoodManager food_manager = FoodManager(default_food_manager, &border);
    vector<BaseBall*> balls;
    food_manager.init_balls();
    food_manager.get_balls(balls);
    cout << balls.size() << endl;
    for (int i = 0; i < 10; i++) {
        balls[i]->echo();
    }
    for (int i = 0; i < 5; i++) {
        food_manager.remove_ball(balls[i]->name);
    }
    balls.clear();
    food_manager.get_balls(balls);
    cout << "======= after remove =========" << endl;
    for (int i = 0; i < balls.size(); i++) {
        balls[i]->echo();
    }
    balls.clear();
    for (int i = 0; i < 5; i++) {
        food_manager.step(1.0f);
        food_manager.get_balls(balls);
        cout << "==============" << balls.size() << ", " << food_manager.refresh_time_count << endl;
        for (int i = 0; i < 5; i++) {
            int index = (int)balls.size()-i-1;
            balls[index]->echo();
        }
        balls.clear();
    }
};

void test_spore_manager() {
    DefaultSporeManager default_spore_manager;
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    SporeManager spore_manager = SporeManager(default_spore_manager, &border);
    spore_manager.init_balls();
};

void test_thorns_manager() {
    DefaultThornsManager default_thorns_manager;
    default_thorns_manager.num_init = 10;
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    ThornsManager thorns_manager = ThornsManager(default_thorns_manager, &border);
    vector<BaseBall*> balls;
    thorns_manager.init_balls();
    thorns_manager.get_balls(balls);
    cout << balls.size() << endl;
    for (int i = 0; i < 10; i++) {
        balls[i]->echo();
    }
    for (int i = 0; i < 5; i++) {
        thorns_manager.remove_ball(balls[i]->name);
    }
    balls.clear();
    thorns_manager.get_balls(balls);
    cout << "======= after remove =========" << endl;
    for (int i = 0; i < balls.size(); i++) {
        balls[i]->echo();
    }
    balls.clear();
    for (int i = 0; i < 5; i++) {
        thorns_manager.step(1.0f);
        thorns_manager.get_balls(balls);
        cout << "==============" << balls.size() << ", " << thorns_manager.refresh_time_count << endl;
        for (int i = 0; i < 5; i++) {
            int index = (int)balls.size()-i-1;
            balls[index]->echo();
        }
        balls.clear();
    }
};

void test_humanplayer() {
    string team_name = "0";
    string name = "1";
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    DefaultCloneBall default_clone_ball;
    DefaultSporeBall default_spore_ball;
    HumanPlayer player = HumanPlayer(team_name, name, &border, default_clone_ball, default_spore_ball);
    Vector2 position = border.sample();
    player.respawn();
    cout << "==================== respawn ====================" << endl;
    vector<BaseBall*> cloneballs;
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
    cout << "==================== move ====================" << endl;
    Vector2 move_direction = Vector2(1.0f, 0.0f);
    player.move(move_direction, 0.05);
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
    player.move(move_direction, 0.05);
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
    player.move(move_direction, 0.05);
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
    player.move(move_direction, 0.05);
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
    cout << "==================== split false ====================" << endl;
    Vector2 split_direction = Vector2(0.0f, 1.0f);
    player.split(split_direction);
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
    cout << "==================== split true ====================" << endl;
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->set_size(1000.0f);
        item->echo();
    }
    player.split(split_direction);
    cloneballs.clear();
    player.get_balls(cloneballs);
    for (auto item : cloneballs) {
        item->echo();
    }
}

void cout_player_manager(PlayerManager &player_manager) {
    int team_num = 4;
    int player_num_per_team = 3;
    vector<string>* team_names = player_manager.get_team_names();
    vector<string>* player_names = player_manager.get_player_names();
    vector<float>* sizes = player_manager.get_sizes();
    for (int i = 0; i < team_num; i++) {
        cout << (*team_names)[i] << " (";
        for (int j = 0; j < player_num_per_team; j++) {
            cout << (*player_names)[i*player_num_per_team + j] << "=" << 
                    (*sizes)[i*player_num_per_team + j] << ", ";
        }
        cout << ")" << endl;
    }
}

void test_player_manager() {
    DefaultPlayerManager default_player_manager;
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    int team_num = 4;
    int player_num_per_team = 3;
    DefaultSporeManager default_spore_manager;
    time_t seed = time(0);
    PlayerManager player_manager = PlayerManager(default_player_manager, &border, team_num,
                                                 player_num_per_team, default_spore_manager);
    cout << "============ init_balls ============" << endl;
    player_manager.init_balls();
    cout << "============ print leaderboard ============" << endl;
    cout_player_manager(player_manager);
    cout << "============ get_balls ============" << endl;
    vector<BaseBall*> balls;
    player_manager.get_balls(balls);
    for (int i = 0; i < balls.size(); i++) {
        balls[i]->echo();
    }
};

void test_random() {
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f, time(0));
    for (int i = 0; i < 10; i++) {
        cout << &border;
        border.sample().echo();
    }
};

class Test1 {
public:
    Test1(Border &border) {
        this->border = border;
    }
    void init() {
        for (int i = 0; i < 10; i++) {
            this->border.sample().echo();
        }
    }
    void echo() {
        cout << &(this->border) << " ";
        Vector2 position = this->border.sample();
        position.echo();
    }
    Border border;
};

void test_random2() {
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    Test1 test1 = Test1(border);
    test1.init();
};

void test_player_manager2() {
    DefaultPlayerManager default_player_manager;
    Border border = Border(0.0f, 0.0f, 1000.0f, 1000.0f);
    int team_num = 4;
    int player_num_per_team = 3;
    DefaultSporeManager default_spore_manager;
    time_t seed = time(0);
    PlayerManager player_manager1 = PlayerManager(default_player_manager, &border, team_num,
                                                 player_num_per_team, default_spore_manager);
    PlayerManager player_manager2 = PlayerManager(default_player_manager, &border, team_num,
                                                 player_num_per_team, default_spore_manager);
    cout << "============ init_balls 1 ============" << endl;
    player_manager1.init_balls();
    cout << "============ get_balls 1 ============" << endl;
    vector<BaseBall*> balls1;
    player_manager1.get_balls(balls1);
    for (int i = 0; i < balls1.size(); i++) {
        balls1[i]->echo();
    }

    cout << "============ init_balls 2 ============" << endl;
    player_manager2.init_balls();
    cout << "============ get_balls 2 ============" << endl;
    vector<BaseBall*> balls2;
    player_manager2.get_balls(balls2);
    for (int i = 0; i < balls2.size(); i++) {
        balls2[i]->echo();
    }
};


int main(int argc, char* argv[]) {
    // test_food_manager();
    // test_random();
    // cout << "============== random1 finish ==============" << endl;
    // test_random2();
    // cout << "============== random2 finish ==============" << endl;
    // test_spore_manager();
    // test_thorns_manager();
    // test_humanplayer();
    // test_player_manager();
    test_player_manager2();
    // test_border();
    return 0;
};

