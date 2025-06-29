#!/bin/bash

# Run script for Kobayashi directional solidification project
# Usage:
#   ./run.sh python    # to run Python version
#   ./run.sh cpp       # to run C++ version


# Check argument
if [ "$1" == "python" ]; then
    echo "🔁 Running Python version..."
    python python/src/main.py

elif [ "$1" == "cpp" ]; then
    echo "🔁 Running C++ version..."
    cd cpp
    make                # or your preferred build system
    ./kobayashi_sim

else
    echo "Invalid argument."
    echo "Usage: ./run.sh [python|cpp]"
    exit 1
fi

