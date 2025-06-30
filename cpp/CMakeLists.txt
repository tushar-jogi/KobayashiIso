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

# === HDF5 ===
find_package(OpenCV REQUIRED)
include_directories($Open_CV_INCLUDE_DIRS)

# === Executable and sources ===
add_executable(CPPKobayashi
    src/main.cpp
    src/build_matrices.cpp
    src/solve.cpp
    src/initialize.cpp
    src/boundary_conditions.cpp
    src/utils.cpp
    src/write.cpp
    src/read.cpp
)

# === Linking libraries ===
target_link_libraries(CPPKobayashi petsc yaml-cpp hdf5_cpp hdf5 ${OpenCV_LIBS})

