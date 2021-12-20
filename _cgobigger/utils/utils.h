#pragma once

#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/uuid/uuid_generators.hpp>

string generate_uuid(){
    boost::uuids::uuid a_uuid = boost::uuids::random_generator()();
    string uuid_string = boost::uuids::to_string(a_uuid);
    return uuid_string;
}