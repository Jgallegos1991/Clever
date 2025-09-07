#!/bin/bash
# Complete phone access fix for Clever AI

echo "🔧 Complete Phone Access Fix for Clever AI"
echo "=========================================="

# Install ngrok if not present
if ! command -v ngrok >/dev/null 2>&1; then
    echo "📥 Installing ngrok..."
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install -y ngrok
    echo "✅ ngrok installed"
fi

# Update config to bind to all interfaces
echo "🔧 Updating Clever to accept external connections..."
sed -i 's/APP_HOST = .*/APP_HOST = "0.0.0.0"/' config.py 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Get ngrok account: https://ngrok.com/signup"
echo "2. Set auth token: ngrok config add-authtoken YOUR_TOKEN"
echo "3. Start tunnel: ./start_ngrok.sh"
echo "4. Use the ngrok URL on your phone"
echo ""
echo "💡 Or run: ./phone_access.sh for all options"
