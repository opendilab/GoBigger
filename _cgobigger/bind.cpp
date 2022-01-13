#pragma once

#include <stdio.h>
#include <algorithm>
#include <chrono>
#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>
#include "server/server.h"

#define STRINGIFY(x)
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace std;

PYBIND11_MODULE(_cgobigger, m) {
    py::class_<DefaultObsSetting>(m, "DefaultObsSetting")
        .def(py::init<>())
        .def_readwrite("with_spatial", &DefaultObsSetting::with_spatial)
        .def_readwrite("with_speed", &DefaultObsSetting::with_speed)
        .def_readwrite("with_all_vision", &DefaultObsSetting::with_all_vision);
    py::class_<DefaultServer>(m, "DefaultServer")
        .def(py::init<>())
        .def_readwrite("team_num", &DefaultServer::team_num)
        .def_readwrite("player_num_per_team", &DefaultServer::player_num_per_team)
        .def_readwrite("map_width", &DefaultServer::map_width)
        .def_readwrite("map_height", &DefaultServer::map_height)
        .def_readwrite("match_time", &DefaultServer::match_time)
        .def_readwrite("state_tick_per_second", &DefaultServer::state_tick_per_second)
        .def_readwrite("action_tick_per_second", &DefaultServer::action_tick_per_second)
        .def_readwrite("load_bin_frame_num", &DefaultServer::load_bin_frame_num)
        .def_readwrite("jump_to_frame_file", &DefaultServer::jump_to_frame_file)
        .def_readwrite("seed", &DefaultServer::seed)
        .def_readwrite("default_food_manager", &DefaultServer::default_food_manager)
        .def_readwrite("default_thorns_manager", &DefaultServer::default_thorns_manager)
        .def_readwrite("default_spore_manager", &DefaultServer::default_spore_manager)
        .def_readwrite("default_player_manager", &DefaultServer::default_player_manager)
        .def_readwrite("default_obs_setting", &DefaultServer::default_obs_setting);
    py::class_<OutputBall>(m, "OutputBall")
        .def(py::init<float, float, float, int>())
        .def_readwrite("position_x", &OutputBall::position_x)
        .def_readwrite("position_y", &OutputBall::position_y)
        .def_readwrite("radius", &OutputBall::radius)
        .def_readwrite("speed_x", &OutputBall::speed_x)
        .def_readwrite("speed_y", &OutputBall::speed_y)
        .def_readwrite("ball_type", &OutputBall::ball_type)
        .def_readwrite("owner", &OutputBall::owner)
        .def_readwrite("team_name", &OutputBall::team_name);
    py::class_<Server>(m, "Server")
        .def(py::init<DefaultServer &>())
        .def("step", &Server::step)
        .def("step_state_tick", &Server::step_state_tick)
        .def("start", &Server::start)
        .def("reset", &Server::reset)
        .def("close", &Server::close)
        .def("get_player_names", &Server::get_player_names)
        .def("get_team_names", &Server::get_team_names)
        .def("save_frame_info", &Server::save_frame_info)
        .def("obs_partial_array", &Server::obs_partial_array)
        .def("obs_full_array", &Server::obs_full_array)
        .def_readwrite("last_time", &Server::last_time);
}

