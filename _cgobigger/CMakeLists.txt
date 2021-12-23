cmake_minimum_required(VERSION 3.20)
project(test)

set(CMAKE_CXX_STANDARD 11)
include_directories(.)
include_directories(/usr/local/opt/boost@1.74/include)
include_directories(/Users/zm/anaconda2/envs/torch041-py36/include/)
#include_directories(/Users/zm/anaconda2/envs/torch041-py36/lib/python3.6/site-packages/pybind11/include)
include_directories(/Users/zm/anaconda2/envs/torch041-py36/include/python3.6m)

link_directories("/usr/local/opt/boost@1.74/lib/")

add_executable(test utils/file_helper_test.cpp)
