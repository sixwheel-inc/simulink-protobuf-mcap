cmake_minimum_required(VERSION 3.21)
project(example-bindings)

# need this to make the .lib along with the .dll
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# need this for LSP / intellisense
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# example-bindings lib
add_library(example-bindings SHARED
                "example-bindings.cpp"
                "proto-to-busses.cpp")

target_include_directories(example-bindings PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Add headers that will be used by example-bindings
set_target_properties(example-bindings PROPERTIES PUBLIC_HEADER "example-bindings.h")
                
set_property(TARGET example-bindings PROPERTY CXX_STANDARD 17)

# TODO do this until I figure out how to avoid the warnings from 3rd Parties
target_compile_options(example-bindings PRIVATE -Wno-everything)

# protobuf
find_package(protobuf CONFIG REQUIRED)
target_link_libraries(example-bindings PUBLIC protobuf::libprotoc protobuf::libprotobuf protobuf::libprotobuf-lite)
# copied the .protos from 
file(GLOB PROTO_FILES proto/*.proto)
add_library(example-schema OBJECT ${PROTO_FILES})
target_link_libraries(example-schema PUBLIC protobuf::libprotobuf)
set(PROTO_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
target_include_directories(example-schema PUBLIC "$<BUILD_INTERFACE:${PROTO_BINARY_DIR}>")
protobuf_generate(
    TARGET example-schema
    IMPORT_DIRS "${CMAKE_CURRENT_LIST_DIR}/proto"
    PROTOC_OUT_DIR "${PROTO_BINARY_DIR}")
target_link_libraries(example-bindings PUBLIC example-schema)

# mcap needs lz4 and libzstd
find_package(lz4 CONFIG REQUIRED)
target_link_libraries(example-bindings PUBLIC lz4::lz4)
find_package(zstd CONFIG REQUIRED)
target_link_libraries(example-bindings PUBLIC zstd::libzstd)

# copied the header only mcap lib from git:foxglove/mcap
add_library(mcap INTERFACE)
target_include_directories(mcap SYSTEM INTERFACE mcap/)

install(TARGETS example-bindings 
        LIBRARY DESTINATION libs
        PUBLIC_HEADER DESTINATION includes)

