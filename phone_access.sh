#!/bin/bash
# Quick phone access helper for Clever AI

echo "📱 Clever AI Phone Access Helper"
echo "================================"
echo ""

# Check if Clever is running
if ! curl -s http://127.0.0.1:5000/health >/dev/null 2>&1; then
    echo "❌ Clever not running. Start with: make run"
    exit 1
fi

echo "✅ Clever is running locally"
echo ""

# Show available options
echo "🚀 Phone Access Options:"
echo ""
echo "1. 📡 ngrok tunnel (works anywhere)"
echo "   ./start_ngrok.sh"
echo ""
echo "2. 🏠 Local network (same WiFi)"
echo "   Find your computer's IP and use: http://YOUR-IP:5000"
echo ""
echo "3. ☁️  Cloud environment"
if [ -n "${CODESPACES}" ]; then
    echo "   GitHub Codespaces: Make port 5000 public in Ports tab"
elif [ -n "${GITPOD_WORKSPACE_URL}" ]; then
    GITPOD_URL="${GITPOD_WORKSPACE_URL/https:\/\//https://5000-}"
    echo "   Gitpod URL: $GITPOD_URL"
else
    echo "   Forward container port 5000 to host"
fi
echo ""

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "unknown")
if [ "$LOCAL_IP" != "unknown" ]; then
    echo "🏠 Possible local network URL: http://$LOCAL_IP:5000"
    echo "   (Try this if you're on the same WiFi network)"
fi

echo ""
echo "💡 Recommended: Use ngrok for reliable access from anywhere"
