#!/bin/bash

# Neptou Backend Startup Script with IP Detection
# This script starts the server and shows your local IP for iPhone access

echo "🚀 Starting Neptou Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Get local IP address
LOCAL_IP=$(python3 get_local_ip.py 2>/dev/null | grep "Your local IP address is:" | awk '{print $6}')

if [ -z "$LOCAL_IP" ]; then
    # Fallback method
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Warning: venv not found. Using system Python."
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env file with ANTHROPIC_API_KEY"
    exit 1
fi

# Check if API key is set
if ! grep -q "ANTHROPIC_API_KEY=" .env || grep -q "ANTHROPIC_API_KEY=your_" .env; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY not set in .env file!"
    echo "   Please add your API key to .env file"
    exit 1
fi

echo "✅ Environment ready!"
echo ""
echo "🌐 Server Information:"
echo "   Local URL: http://127.0.0.1:8000 (for simulator)"
if [ ! -z "$LOCAL_IP" ]; then
    echo "   Network URL: http://$LOCAL_IP:8000 (for iPhone)"
    echo ""
    echo "📱 To connect from iPhone:"
    echo "   1. Make sure iPhone and laptop are on the same WiFi"
    echo "   2. Use this IP in your app: $LOCAL_IP"
else
    echo "   Network URL: Could not detect local IP"
    echo "   Run: python3 get_local_ip.py to find your IP"
fi
echo ""
echo "   Press CTRL+C to stop"
echo ""

# Run the server
python3 main.py
