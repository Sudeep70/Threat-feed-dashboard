#!/bin/bash

echo "=============================================="
echo "🛡️  ThreatFeed Dashboard - Quick Setup"
echo "=============================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your API keys:"
    echo "   nano .env"
    echo ""
    echo "Get API keys from:"
    echo "   • AbuseIPDB: https://www.abuseipdb.com/api"
    echo "   • Telegram: @BotFather on Telegram"
    echo ""
    exit 0
fi

echo "✅ .env file found"
echo ""

# Run first collection
echo "🔍 Running first threat collection..."
echo ""
python3 main.py
echo ""

echo "=============================================="
echo "✅ Setup complete!"
echo "=============================================="
echo ""
echo "To start the dashboard, run:"
echo "   python3 app.py"
echo ""
echo "Then visit: http://localhost:5000"
echo ""
