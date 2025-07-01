# Unit tests for KobayashiIso

# GTest is assumed to be installed via conda
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
link_directories(${GTEST_LIBRARY_DIRS})

add_executable(test_CPP test_utils.cpp)
target_link_libraries(test_CPP 
  kobayashi_core
  GTest::GTest
  GTest::Main
  )

add_test(NAME CPPTest COMMAND test_CPP)

