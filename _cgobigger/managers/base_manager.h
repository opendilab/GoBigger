#pragma once

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include "balls/baseball.h"
#include "utils/structures.h"

using namespace std;


class BaseManager {
public:
    BaseManager() {}
    BaseManager(Border* border) {
        this->border = border;
    }
    Border* border;
};
