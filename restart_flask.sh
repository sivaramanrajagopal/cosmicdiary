#!/bin/bash
# Script to kill and restart Flask API server

echo "🛑 Stopping Flask API server..."

# Find and kill process on port 8000
FLASK_PID=$(lsof -ti:8000 2>/dev/null)

if [ -z "$FLASK_PID" ]; then
    echo "   ℹ️  No Flask process found on port 8000"
else
    echo "   Found process: $FLASK_PID"
    kill $FLASK_PID 2>/dev/null
    sleep 2
    
    # Force kill if still running
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "   Force killing..."
        kill -9 $FLASK_PID 2>/dev/null
        sleep 1
    fi
    
    echo "   ✅ Flask server stopped"
fi

echo ""
echo "🚀 Starting Flask API server..."
echo "   (Press CTRL+C to stop)"
echo ""

cd "$(dirname "$0")"
python3 api_server.py

