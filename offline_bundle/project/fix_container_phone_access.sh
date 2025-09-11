#!/bin/bash
# Container-Friendly Tailscale Alternative for Clever AI
# Works around container limitations with multiple access methods

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Fixing Tailscale access issues in container environment...${NC}"

# Check container environment
CONTAINER_TYPE=""
if [ -f /.dockerenv ]; then
    CONTAINER_TYPE="Docker"
elif [ -n "${CODESPACES}" ]; then
    CONTAINER_TYPE="GitHub Codespaces"
elif [ -n "${DEVCONTAINER}" ]; then
    CONTAINER_TYPE="Dev Container"
else
    CONTAINER_TYPE="Unknown/Host"
fi

echo -e "${BLUE}📦 Environment: $CONTAINER_TYPE${NC}"

# Solution 1: Port forwarding for immediate access
echo -e "${BLUE}🚀 Solution 1: Port Forwarding (Works Now)${NC}"
echo -e "${GREEN}✅ Your Clever is running on: http://127.0.0.1:5000${NC}"

# Check if we're in a cloud environment
if [ -n "${CODESPACES}" ]; then
    # GitHub Codespaces
    CODESPACE_NAME="${CODESPACE_NAME:-unknown}"
    echo -e "${GREEN}🌐 GitHub Codespaces detected${NC}"
    echo -e "${YELLOW}📱 Access from your phone:${NC}"
    echo -e "   1. Go to your Codespace in GitHub"
    echo -e "   2. Click 'Ports' tab"
    echo -e "   3. Make port 5000 public"
    echo -e "   4. Use the generated URL on your phone"
elif [ -n "${GITPOD_WORKSPACE_URL}" ]; then
    # Gitpod
    GITPOD_URL="${GITPOD_WORKSPACE_URL/https:\/\//https://5000-}"
    echo -e "${GREEN}🌐 Gitpod detected${NC}"
    echo -e "${YELLOW}📱 Access from your phone: ${GITPOD_URL}${NC}"
else
    # Local development or other container
    echo -e "${YELLOW}💡 For phone access, you need to expose port 5000${NC}"
    echo -e "   Method 1: Use your computer's local IP"
    echo -e "   Method 2: Set up ngrok (temporary tunnel)"
    echo -e "   Method 3: Use SSH tunnel to host machine"
fi

# Solution 2: ngrok tunnel (works anywhere)
echo -e "\n${BLUE}🚀 Solution 2: ngrok Tunnel (Universal)${NC}"
if command -v ngrok >/dev/null 2>&1; then
    echo -e "${GREEN}✅ ngrok found${NC}"
    echo -e "${YELLOW}Run: ngrok http 5000${NC}"
    echo -e "Then use the https://xyz.ngrok.io URL"
else
    echo -e "${YELLOW}📥 Installing ngrok...${NC}"
    
    # Install ngrok
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install -y ngrok
    
    echo -e "${GREEN}✅ ngrok installed${NC}"
    echo -e "${BLUE}💡 To use ngrok:${NC}"
    echo -e "   1. Get free account: https://ngrok.com/signup"
    echo -e "   2. Get auth token from dashboard"
    echo -e "   3. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo -e "   4. Run: ngrok http 5000"
    echo -e "   5. Use the https://xyz.ngrok.io URL on your phone"
fi

# Solution 3: Tailscale on host (if possible)
echo -e "\n${BLUE}🚀 Solution 3: Host Tailscale Integration${NC}"
echo -e "${YELLOW}⚠️  Container limitations prevent direct Tailscale use${NC}"
echo -e "${BLUE}💡 Alternative approaches:${NC}"
echo -e "   1. Install Tailscale on your HOST machine"
echo -e "   2. Forward port 5000 from container to host"
echo -e "   3. Access via host's Tailscale IP"

# Create helper scripts
cat > start_ngrok.sh << 'EOF'
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
EOF

chmod +x start_ngrok.sh

# Create quick phone access script
cat > phone_access.sh << 'EOF'
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
EOF

chmod +x phone_access.sh

# Create comprehensive fix script
cat > fix_phone_access_complete.sh << 'EOF'
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
EOF

chmod +x fix_phone_access_complete.sh

# Update user config for external access
if [ -f user_config.py ]; then
    if ! grep -q "CLEVER_HOST.*0.0.0.0" user_config.py; then
        echo "" >> user_config.py
        echo "# Container phone access fix" >> user_config.py
        echo "CLEVER_HOST = \"0.0.0.0\"  # Allow external connections" >> user_config.py
        echo "CLEVER_EXTERNAL_ACCESS = True" >> user_config.py
    fi
fi

echo -e "\n${GREEN}🎉 Phone access fix complete!${NC}"
echo ""
echo -e "${BLUE}📱 Quick access methods:${NC}"
echo -e "   ${YELLOW}./phone_access.sh${NC}     - Show all options"
echo -e "   ${YELLOW}./start_ngrok.sh${NC}      - Start ngrok tunnel"
echo -e "   ${YELLOW}make fix-phone-access${NC} - Complete setup"
echo ""
echo -e "${GREEN}💡 Recommended: Use ngrok for reliable phone access from anywhere${NC}"
