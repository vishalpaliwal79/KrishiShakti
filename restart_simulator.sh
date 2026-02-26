#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Restarting Simulator with New Ranges                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Stop old simulator processes
echo "🛑 Stopping old simulator processes..."
pkill -f "simulator.py"
sleep 2

# Check if stopped
if pgrep -f "simulator.py" > /dev/null; then
    echo "⚠️  Some processes still running, force killing..."
    pkill -9 -f "simulator.py"
    sleep 1
fi

echo "✅ Old processes stopped"
echo ""

# Start new simulator
echo "🚀 Starting simulator with new ranges..."
echo ""
echo "📋 New Sensor Ranges:"
echo "   • MQ-135 (Air Quality): 18-20 ppm"
echo "   • PMS5003 (PM2.5/PM10): 10-12 µg/m³"
echo "   • DHT22 (Temperature): 28-30°C"
echo "   • FC-28 (Water Level): 10-12%"
echo "   • TDS (Water Quality): 100-150 ppm"
echo ""
echo "⏱️  Update Frequency: Every 7-8 seconds"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Start simulator in background
nohup python simulator.py > simulator.log 2>&1 &

sleep 2

# Check if started
if pgrep -f "simulator.py" > /dev/null; then
    echo ""
    echo "✅ Simulator started successfully!"
    echo "📊 Check dashboard: http://localhost:5001/dashboard.html"
    echo "📝 View logs: tail -f simulator.log"
    echo ""
else
    echo ""
    echo "❌ Failed to start simulator"
    echo "Try manually: python simulator.py"
    echo ""
fi
