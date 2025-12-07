#!/bin/bash

# Neptou Backend Startup Script

echo "🚀 Starting Neptou Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

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
echo "🌐 Starting server on http://0.0.0.0:8000"
echo "   Press CTRL+C to stop"
echo ""

# Run the server
python3 main.py

