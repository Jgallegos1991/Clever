#!/bin/bash
# Quick setup script for both ngrok and Tailscale
# For Jay's Clever AI remote access

set -e

echo "🌐 Setting up BOTH remote access options for Clever AI"
echo "=" * 60

# Check if tokens are provided
if [ -z "${NGROK_TOKEN:-}" ]; then
    echo "⚠️  NGROK_TOKEN not set"
    echo "Run: export NGROK_TOKEN='your_ngrok_token'"
fi

if [ -z "${TAILSCALE_AUTHKEY:-}" ]; then
    echo "⚠️  TAILSCALE_AUTHKEY not set" 
    echo "Run: export TAILSCALE_AUTHKEY='your_tailscale_key'"
fi

echo ""

# Setup ngrok if token provided
if [ -n "${NGROK_TOKEN:-}" ]; then
    echo "🚀 Configuring ngrok..."
    ngrok config add-authtoken "${NGROK_TOKEN}"
    echo "✅ ngrok configured"
else
    echo "⏭️  Skipping ngrok setup (no token)"
fi

# Setup Tailscale if auth key provided  
if [ -n "${TAILSCALE_AUTHKEY:-}" ]; then
    echo "🔐 Setting up Tailscale..."
    ./setup_tailscale.sh
    echo "✅ Tailscale configured"
else
    echo "⏭️  Skipping Tailscale setup (no auth key)"
fi

echo ""
echo "🎉 Remote access setup complete!"
echo ""
echo "📱 Access options:"
echo "🔸 Local: http://127.0.0.1:5000"
if [ -n "${NGROK_TOKEN:-}" ]; then
    echo "🔸 ngrok: Run './start_ngrok.sh' for public URL"
fi
if [ -n "${TAILSCALE_AUTHKEY:-}" ]; then
    echo "🔸 Tailscale: Use your Tailscale IP (secure network)"
fi
