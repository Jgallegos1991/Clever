# 🌐 Clever AI + Tailscale Setup Guide

## Quick Setup for Jay (lapirfta@gmail.com)

### Step 1: Get Tailscale Auth Key

1. Go to: https://login.tailscale.com/admin/settings/keys
2. Sign in with: **lapirfta@gmail.com** 
3. Click "Generate auth key"
4. Set options:
   - ✅ **Ephemeral** (recommended for dev environments)
   - ✅ **Preauthorized** (auto-approve this device)
   - Optional: Set expiry (90 days recommended)
5. Copy the key (starts with `tskey-auth-`)

### Step 2: Set Environment Variable

```bash
# In your terminal, set the auth key:
export TAILSCALE_AUTHKEY='tskey-auth-xxxxxxxxxx'

# Or add to your shell profile for persistence:
echo 'export TAILSCALE_AUTHKEY="tskey-auth-xxxxxxxxxx"' >> ~/.bashrc
```

### Step 3: Run Setup

```bash
# Run the Tailscale setup script
make tailscale-setup

# Or manually:
./setup_tailscale.sh
```

### Step 4: Start Clever with Tailscale

```bash
# Start Clever AI
make run
```

You'll see output like:
```
🌟 Synaptic Hub Neural Interface Ready!
👤 User: Jay (lapirfta@gmail.com)
🔗 Local: http://127.0.0.1:5000
🌐 Tailscale: http://100.64.x.x:5000
🔒 Secure remote access via Tailscale network
```

## Access Methods

### Local Access
- **URL:** http://127.0.0.1:5000
- **Use:** When working on the same machine

### Remote Access (Tailscale)
- **URL:** http://100.64.x.x:5000 (your Tailscale IP)
- **Use:** From any device in your Tailscale network
- **Security:** Encrypted tunnel, no public internet exposure

## Managing Tailscale

```bash
# Check status
make tailscale-status

# Manual commands
tailscale status          # Show connection status
tailscale ip -4          # Show your Tailscale IP
tailscale up             # Connect/reconnect
tailscale down           # Disconnect
```

## Security Features

✅ **Private Network:** Only devices in your Tailscale network can access  
✅ **Encrypted:** All traffic encrypted end-to-end  
✅ **No Public Exposure:** Clever never exposed to public internet  
✅ **Offline-First Maintained:** No cloud AI dependencies  
✅ **Personal Network:** Your devices only (lapirfta@gmail.com account)  

## Troubleshooting

### Auth Key Issues
```bash
# Check if auth key is set
echo $TAILSCALE_AUTHKEY

# Generate new key if expired
# Go to: https://login.tailscale.com/admin/settings/keys
```

### Connection Issues
```bash
# Restart Tailscale
sudo pkill tailscaled
./setup_tailscale.sh

# Check logs
tail -f /tmp/tailscaled.log
```

### Access Issues
```bash
# Verify Clever is listening on all interfaces
netstat -tlnp | grep :5000

# Check firewall (if applicable)
sudo ufw status
```

## What This Enables

🏠 **Work from anywhere** - Access Clever from any device in your network  
📱 **Mobile access** - Use Clever from phone/tablet via Tailscale app  
💻 **Multi-device** - Seamlessly switch between devices  
🔒 **Zero-trust security** - Private network with enterprise-grade encryption  
🌍 **Global access** - Works anywhere you have internet  

**Your personal AI is now accessible securely from anywhere in the world!** 🌟
