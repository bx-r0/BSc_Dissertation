cmake_minimum_required(VERSION 3.8)
project(Dissertation_Project)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        ClientServer/PacketCapture/PacketCapture.cpp
        )

add_executable(Dissertation_Project ${SOURCE_FILES})