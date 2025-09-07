#!/usr/bin/env bash
# Clever AI - Tailscale Setup for Jay
# Sets up secure remote access to Clever AI via Tailscale

set -euo pipefail

echo "🔧 Setting up Tailscale for Clever AI (Jay's Setup)"
echo "📧 Email: lapirfta@gmail.com"
echo "=" * 50

# Check if we're in a devcontainer/codespace
if [ -n "${CODESPACES:-}" ] || [ -n "${DEVCONTAINER:-}" ]; then
    echo "🐳 Detected containerized environment"
    CONTAINER_MODE=true
else
    echo "💻 Detected local environment"
    CONTAINER_MODE=false
fi

# Install Tailscale if not present
if ! command -v tailscale >/dev/null 2>&1; then
    echo "📥 Installing Tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
    echo "✅ Tailscale installed"
else
    echo "✅ Tailscale already installed"
fi

# Configuration
STATE_DIR="/workspaces/projects/.devcontainer/.tailscale"
STATE_FILE="${STATE_DIR}/tailscaled.state"
HOST_LABEL="clever-ai-jay"

# Create state directory
mkdir -p "${STATE_DIR}"

# Stop any existing tailscaled process
echo "🔄 Restarting Tailscale daemon..."
sudo pkill tailscaled >/dev/null 2>&1 || true
sleep 2

# Start tailscaled in userspace mode for containers
if [ "$CONTAINER_MODE" = true ]; then
    echo "🚀 Starting Tailscale in container mode..."
    sudo nohup tailscaled \
        --tun=userspace-networking \
        --state="${STATE_FILE}" \
        >/tmp/tailscaled.log 2>&1 &
else
    echo "🚀 Starting Tailscale in local mode..."
    sudo nohup tailscaled \
        --state="${STATE_FILE}" \
        >/tmp/tailscaled.log 2>&1 &
fi

# Grant control to current user
sudo tailscale set --operator="${USER}" || true
sleep 3

# Authentication setup
echo ""
echo "🔐 Setting up Tailscale authentication..."

if [ ! -s "${STATE_FILE}" ]; then
    echo "🆕 First-time setup detected"
    
    if [ -z "${TAILSCALE_AUTHKEY:-}" ]; then
        echo ""
        echo "⚠️  TAILSCALE_AUTHKEY not found in environment"
        echo ""
        echo "📋 To complete setup:"
        echo "1. Go to: https://login.tailscale.com/admin/settings/keys"
        echo "2. Sign in with: lapirfta@gmail.com"
        echo "3. Generate a new auth key (ephemeral + preauth recommended)"
        echo "4. Set it as environment variable:"
        echo "   export TAILSCALE_AUTHKEY='tskey-auth-xxxxx'"
        echo "5. Re-run this script"
        echo ""
        exit 1
    fi
    
    echo "🔑 Using provided auth key..."
    tailscale up \
        --ssh \
        --accept-dns=false \
        --hostname="${HOST_LABEL}" \
        --authkey="${TAILSCALE_AUTHKEY}" \
        || {
            echo "❌ Failed to authenticate. Check your auth key."
            exit 1
        }
else
    echo "🔄 Using existing authentication..."
    tailscale up \
        --ssh \
        --accept-dns=false \
        --hostname="${HOST_LABEL}" \
        || {
            echo "⚠️  Re-authentication may be needed"
        }
fi

# Check status
echo ""
echo "📊 Tailscale Status:"
tailscale status || {
    echo "❌ Tailscale status check failed"
    exit 1
}

# Get Tailscale IP
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "IP not available")
echo ""
echo "🎉 Tailscale Setup Complete!"
echo "=" * 30
echo "🏷️  Hostname: ${HOST_LABEL}"
echo "🌐 Tailscale IP: ${TAILSCALE_IP}"
echo "📧 Account: lapirfta@gmail.com"
echo ""
echo "🚀 Clever AI will be accessible at:"
echo "   http://${TAILSCALE_IP}:5000"
echo "   (from any device in your Tailscale network)"
echo ""
echo "🔧 Next steps:"
echo "1. Start Clever: make run"
echo "2. Access remotely via Tailscale IP"
echo "3. Enjoy secure, private AI access!"
