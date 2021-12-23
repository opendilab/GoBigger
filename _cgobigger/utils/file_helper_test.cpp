#include "file_helper.h"


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


int main(int argc, char* argv[]) {
//    test_save_frame();
    test_read_frame();
    return 0;

}