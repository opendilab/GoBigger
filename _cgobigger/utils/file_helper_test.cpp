#include "file_helper.h"
#include <random>


void test_save_frame() {
    cout << "start" << endl;
    map<string, vector<vector<float>>> balls;
    string file_name = "/Users/zm/Desktop/st/1988/GoBigger-cpp/_cgobigger/utils/frame.txt";
    cout << "start define food" << endl;
    vector<vector<float>> food_balls(10, vector<float>(3, 1.0f));
    balls["food"] = food_balls;
    cout << "start define thorns" << endl;
    vector<vector<float>> thorns_balls(10, vector<float>(9, 1.0f));
    balls["thorns"] = thorns_balls;
    cout << "start define spore" << endl;
    vector<vector<float>> spore_balls(10, vector<float>(11, 1.0f));
    balls["spore"] = spore_balls;
    cout << "start define clone" << endl;
    vector<vector<float>> clone_balls(10, vector<float>(23, 1.0f));
    balls["clone"] = clone_balls;
    cout << "start save frame" << endl;
    save_frame(balls, file_name);
    cout << "finish" << endl;
}


void test_read_frame() {
    string file_name = "/Users/zm/Desktop/st/1988/GoBigger-cpp/_cgobigger/utils/frame.txt";
    map<string, vector<vector<float>>> balls = read_frame(file_name);
    map<string, vector<vector<float>>>::iterator iter = balls.begin();
    while (iter != balls.end()) {
        for (int i = 0; i < iter->second.size(); i++) {
            cout << "key = " << iter->first << endl;
            for (int j = 0; j < iter->second[i].size(); j++) {
                cout << iter->second[i][j] << " ";
            }
            cout << endl;
        }
        iter++;
    }
}


void test_random() {
    ofstream output("/Users/zm/Desktop/st/1988/GoBigger-cpp/replays/2.txt");
    default_random_engine e1 = default_random_engine();
    e1.seed(1641535363);
    float width = 1000.0f;
    float height = 1000.0f;
    for (int i = 0; i < 1000000; i++) {
        float x = e1() * 1.0f / e1.max() * width + 0.0f;
        output << x << endl;
    }
    output.close();
}


int main(int argc, char* argv[]) {
//    test_save_frame();
//    test_read_frame();
    test_random();
    return 0;

}