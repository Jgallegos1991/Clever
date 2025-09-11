#!/bin/bash
# Start ngrok tunnel for Clever AI

echo "🚀 Starting ngrok tunnel for Clever AI..."

if ! command -v ngrok >/dev/null 2>&1; then
    echo "❌ ngrok not installed. Run: make fix-phone-access"
    exit 1
fi

# Check if auth token is set
if ! ngrok config check >/dev/null 2>&1; then
    echo "⚠️  ngrok auth token not set"
    echo "1. Get free account: https://ngrok.com/signup"
    echo "2. Get auth token from dashboard"  
    echo "3. Run: ngrok config add-authtoken YOUR_TOKEN"
    exit 1
fi

echo "🌐 Starting tunnel on port 5000..."
echo "📱 Use the https://xyz.ngrok.io URL on your phone"
echo "⏹️  Press Ctrl+C to stop"

ngrok http 5000
