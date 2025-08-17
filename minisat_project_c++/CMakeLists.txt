cmake_minimum_required(VERSION 3.29)
project(minisat_project)

set(CMAKE_CXX_STANDARD 20)

add_subdirectory(minisat)

add_executable(minisat_project main.cpp)

target_link_libraries(minisat_project PRIVATE MiniSat::libminisat)

target_include_directories(minisat_project PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/minisat)