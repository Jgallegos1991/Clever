#!/bin/bash
# Tailscale Container Setup for Clever AI
# Fixes networking issues in container environments

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🌐 Setting up Tailscale for Clever AI in container...${NC}"

# Check if we're in a container
if [ -f /.dockerenv ] || [ -n "${CODESPACES}" ] || [ -n "${DEVCONTAINER}" ]; then
    echo -e "${YELLOW}📦 Container environment detected${NC}"
    IN_CONTAINER=true
else
    IN_CONTAINER=false
fi

# Check current Tailscale status
if command -v tailscale >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Tailscale binary found${NC}"
    
    # Try to check status
    if sudo tailscale status >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Tailscale is running and connected${NC}"
        sudo tailscale status
        exit 0
    else
        echo -e "${YELLOW}⚠️  Tailscale installed but not running${NC}"
    fi
else
    echo -e "${RED}❌ Tailscale not found${NC}"
    echo -e "${BLUE}📥 Installing Tailscale...${NC}"
    
    # Install Tailscale
    curl -fsSL https://tailscale.com/install.sh | sh
fi

# Container-specific Tailscale setup
if [ "$IN_CONTAINER" = true ]; then
    echo -e "${BLUE}🐳 Configuring Tailscale for container environment...${NC}"
    
    # Check if we have the auth key
    if [ -z "$TAILSCALE_AUTHKEY" ]; then
        echo -e "${RED}❌ TAILSCALE_AUTHKEY environment variable not set${NC}"
        echo -e "${BLUE}🔑 To get your auth key:${NC}"
        echo -e "   1. Go to: ${YELLOW}https://login.tailscale.com/admin/settings/keys${NC}"
        echo -e "   2. Sign in with: ${YELLOW}lapirfta@gmail.com${NC}"
        echo -e "   3. Generate a new auth key with these settings:"
        echo -e "      ✅ Reusable: YES"
        echo -e "      ✅ Ephemeral: YES (for containers)"
        echo -e "      ✅ Preauthorized: YES"
        echo -e "   4. Copy the key and run:"
        echo -e "      ${YELLOW}export TAILSCALE_AUTHKEY='tskey-auth-YOUR-KEY-HERE'${NC}"
        echo -e "      ${YELLOW}./fix_tailscale.sh${NC}"
        echo ""
        
        # Create a placeholder for the key
        echo -e "${BLUE}💡 Creating example environment file...${NC}"
        cat > .env.tailscale << 'EOF'
# Add your Tailscale auth key here
# Get it from: https://login.tailscale.com/admin/settings/keys
# TAILSCALE_AUTHKEY=tskey-auth-YOUR-KEY-HERE
EOF
        echo -e "${GREEN}✅ Created .env.tailscale - add your auth key there${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🚀 Starting Tailscale in container mode...${NC}"
    
    # Start tailscaled in userspace mode (works in containers)
    sudo tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock --tun=userspace-networking &
    TAILSCALED_PID=$!
    
    # Wait for daemon to start
    sleep 3
    
    # Authenticate with Tailscale
    echo -e "${BLUE}🔐 Authenticating with Tailscale...${NC}"
    sudo tailscale up --authkey="$TAILSCALE_AUTHKEY" --hostname="clever-ai-jay" --accept-routes
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Tailscale connected successfully!${NC}"
        echo -e "${BLUE}📊 Connection status:${NC}"
        sudo tailscale status
        
        # Get the Tailscale IP
        TAILSCALE_IP=$(sudo tailscale ip -4)
        echo -e "${GREEN}🌐 Your Tailscale IP: ${YELLOW}$TAILSCALE_IP${NC}"
        echo -e "${GREEN}🔗 Clever AI will be accessible at: ${YELLOW}http://$TAILSCALE_IP:5000${NC}"
        
        # Update user config with Tailscale IP
        cat >> user_config.py << EOF

# Tailscale Configuration (Auto-generated)
TAILSCALE_IP = "$TAILSCALE_IP"
TAILSCALE_URL = "http://$TAILSCALE_IP:5000"
TAILSCALE_CONNECTED = True
EOF
        
        echo -e "${GREEN}✅ Updated user_config.py with Tailscale settings${NC}"
        
    else
        echo -e "${RED}❌ Failed to connect to Tailscale${NC}"
        kill $TAILSCALED_PID 2>/dev/null || true
        exit 1
    fi
    
else
    # Host system setup
    echo -e "${BLUE}🖥️  Setting up Tailscale on host system...${NC}"
    
    # Start tailscaled service
    if sudo systemctl is-active --quiet tailscaled; then
        echo -e "${GREEN}✅ Tailscale service already running${NC}"
    else
        echo -e "${BLUE}🚀 Starting Tailscale service...${NC}"
        sudo systemctl enable --now tailscaled
    fi
    
    # Connect to Tailscale
    if [ -n "$TAILSCALE_AUTHKEY" ]; then
        sudo tailscale up --authkey="$TAILSCALE_AUTHKEY" --hostname="clever-ai-jay"
    else
        echo -e "${BLUE}🔗 Connecting to Tailscale (will open browser)...${NC}"
        sudo tailscale up --hostname="clever-ai-jay"
    fi
fi

echo -e "${GREEN}✅ Tailscale setup complete!${NC}"
echo ""
echo -e "${BLUE}📱 To access from your phone:${NC}"
echo -e "   1. Install Tailscale app on your phone"
echo -e "   2. Sign in with: ${YELLOW}lapirfta@gmail.com${NC}"
echo -e "   3. Open: ${YELLOW}http://clever-ai-jay:5000${NC}"
echo -e "   4. Or use IP: ${YELLOW}$(sudo tailscale ip -4 2>/dev/null || echo 'IP not available'):5000${NC}"
echo ""
echo -e "${GREEN}🎉 Your Clever AI is now accessible from anywhere on your Tailscale network!${NC}"
