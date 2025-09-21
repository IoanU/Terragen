cmake_minimum_required(VERSION 3.15)
project(terragen_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
  message(STATUS "pybind11 not found via config; using FetchContent")
  include(FetchContent)
  FetchContent_Declare(pybind11 GIT_REPOSITORY https://github.com/pybind/pybind11.git GIT_TAG v2.12.0)
  FetchContent_MakeAvailable(pybind11)
endif()

pybind11_add_module(terragen_core
  cpp/bindings.cpp
  cpp/perlin.cpp
  cpp/diamond_square.cpp
  cpp/fbm.cpp
  cpp/erosion.cpp
)

install(TARGETS terragen_core
        LIBRARY DESTINATION terragen
        RUNTIME DESTINATION terragen
        ARCHIVE DESTINATION terragen)

# For `pip install .` via scikit-build-core, leave as is
