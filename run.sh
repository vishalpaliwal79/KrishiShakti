#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Starting KrishiShakti Flask Server                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Start Flask server
echo "🚀 Starting Flask server..."
echo ""
python app.py
