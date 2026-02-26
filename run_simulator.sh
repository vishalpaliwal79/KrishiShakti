#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Starting Sensor Data Simulator                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Start simulator
python simulator.py
