#!/bin/bash

# Run script for Kobayashi directional solidification project
# Usage:
#   ./run.sh python    # to run Python version
#   ./run.sh cpp       # to run C++ version


# Check argument
if [ "$1" == "python" ]; then
    echo "🔁 Running Python version..."
    python python/pyKobayashiIso/main.py

elif [ "$1" == "pythontest" ]; then
    echo "🔁 Running Python tests..."
    cd python/pyKobayashiIso
    python -m unittest discover -s tests

elif [ "$1" == "cpp" ]; then
    echo "🔁 Running C++ version..."
    cd cpp
    mkdir -p build
    mkdir -p data
    cd build
    cmake ..
    make                
    ./CPPKobayashiIso

elif [ "$1" == "cpptest" ]; then
    echo "🔁 Running C++ test..."
    cd cpp
    mkdir -p build
    cd build
    cmake ..
    make                
    ./test_CPP


elif ["$1" == "help"]; then
    echo ""
    echo "Usage:"
    echo "  ./run.sh python      # Run Python version"
    echo "  ./run.sh pythontest  # Run Python tests"
    echo "  ./run.sh cpp         # Run C++ version"
    echo "  ./run.sh cpptest     # Run C++ unit tests"
    echo "  ./run.sh --help      # Show this help message"
    echo ""]

else
    echo "Invalid argument."
    echo "Usage: ./run.sh [python|cpp|pythontest|cpptest|help]"
    exit 1
fi

