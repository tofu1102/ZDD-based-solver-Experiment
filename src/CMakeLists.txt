# How to build
#
# mkdir build
# cd build
# cmake ..
# make
#

cmake_policy(SET CMP0048 NEW)
project(reconf-graphillion)

cmake_minimum_required(VERSION 3.17)

if(NOT "${CMAKE_CXX_STANDARD}")
  set(CMAKE_CXX_STANDARD 17)
endif()
set(CMAKE_CXX_EXTENSIONS OFF)

include_directories(../src)
include_directories(./SAPPOROBDD)

# ctest -VV

enable_testing()

set(test_dir "./test")
set(lib "./SAPPOROBDD")
set(graphillion_src "./graphillion")

add_subdirectory(${test_dir}/googletest)
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
message("gtest_SOURCE_DIR: ${gtest_SOURCE_DIR}")
include(GoogleTest)

add_executable(reconf_test ${test_dir}/reconf_test.cc ${lib}/bddc.c ${lib}/BDD.cc ${lib}/ZBDD.cc ${graphillion_src}/reconf.cc)
target_link_libraries(reconf_test gtest_main)
gtest_discover_tests(reconf_test)
