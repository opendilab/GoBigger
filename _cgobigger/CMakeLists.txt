cmake_minimum_required(VERSION 3.20)
project(test)

set(CMAKE_CXX_STANDARD 11)
include_directories(.)
include_directories(/usr/local/opt/boost@1.74/include)
include_directories(/Users/zm/anaconda2/envs/torch041-py36/include/)
#include_directories(/Users/zm/anaconda2/envs/torch041-py36/lib/python3.6/site-packages/pybind11/include)
include_directories(/Users/zm/anaconda2/envs/torch041-py36/include/python3.6m)
include_directories(/opt/homebrew/Cellar/boost/1.76.0/include/)

link_directories(/usr/local/opt/boost@1.74/lib/)
link_directories(/Users/zm/anaconda2/envs/torch041-py36/lib)
link_directories(/opt/homebrew/Cellar/boost/1.76.0/lib)

link_libraries(python)

add_executable(test server/server_test.cpp)
