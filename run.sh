#!/bin/bash
PYTHON=/storage/Desktop/sem2/t5env/bin/python

# Kill anything on port 5000
PID=$(lsof -ti:5000 2>/dev/null)
if [ -n "$PID" ]; then
    echo "Killing process on port 5000 (PID $PID)..."
    kill -9 $PID
    sleep 1
fi

echo "Starting Blynk bridge..."
$PYTHON blynk_bridge.py > blynk_bridge.log 2>&1 &
sleep 2

echo "Starting KrishiShakti..."
$PYTHON app.py
