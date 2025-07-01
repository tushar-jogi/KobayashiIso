cmake_minimum_required(VERSION 3.10)
project(KobayashiIso)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

set(CONDA_PREFIX $ENV{CONDA_PREFIX})

# === PETSc ===
set(PETSC_DIR $ENV{PETSC_DIR})
set(PETSC_ARCH $ENV{PETSC_ARCH})

set(PETSC_INCLUDE_DIR ${PETSC_DIR}/include ${PETSC_DIR}/${PETSC_ARCH}/include)
set(PETSC_LIB_DIR ${PETSC_DIR}/${PETSC_ARCH}/lib)

include_directories(${PETSC_INCLUDE_DIR} include)
link_directories(${PETSC_LIB_DIR})

# === yaml-cpp ===
set(yaml-cpp_DIR "${CONDA_PREFIX}/lib/cmake/yaml-cpp")
find_package(yaml-cpp REQUIRED)
include_directories(${YAML_CPP_INCLUDE_DIR})

# === HDF5 ===
set(HDF5_INCLUDE_DIR "${CONDA_PREFIX}/include")
set(HDF5_LIB_DIR "${CONDA_PREFIX}/lib")
include_directories(${HDF5_INCLUDE_DIR})
link_directories(${HDF5_LIB_DIR})

# === OpenCV ===
#find_package(OpenCV REQUIRED)
#include_directories(${OpenCV_INCLUDE_DIRS})

# === Define library from src files ===
add_library(kobayashi_core
    src/build_matrices.cpp
    src/solve.cpp
    src/initialize.cpp
    src/boundary_conditions.cpp
    src/utils.cpp
    src/write.cpp
    src/read.cpp
)

#target_link_libraries(kobayashi_core petsc yaml-cpp hdf5_cpp hdf5 ${OpenCV_LIBS})
target_link_libraries(kobayashi_core petsc yaml-cpp hdf5_cpp hdf5)

# === Executable ===
add_executable(CPPKobayashi src/main.cpp)
target_link_libraries(CPPKobayashi kobayashi_core)

# === Tests ===
enable_testing()
add_subdirectory(tests)
