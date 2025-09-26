#!/usr/bin/env python3
"""
tailscale_config.py - Tailscale Configuration for Remote Clever Access

Why: Enables secure remote access to Clever's digital brain extension from any device
     on Jay's Tailscale network, maintaining privacy and cognitive partnership continuity
     across locations and devices.

Where: Configures Flask app for Tailscale network access, integrates with app.py
       for remote cognitive partnership sessions while preserving digital sovereignty.

How: Configures Flask to bind to Tailscale IP, sets up secure access controls,
     and provides connection utilities for seamless remote interaction with Clever.

File Usage:
    - Primary callers: app.py for network configuration, startup scripts
    - Configuration: Tailscale IP detection and Flask binding configuration
    - Remote access: Enables cross-device cognitive partnership sessions
    - Security: Maintains digital sovereignty while enabling remote access

Connects to:
    - app.py: Flask application configuration for Tailscale network binding
    - config.py: Network and security configuration integration
    - debug_config.py: Remote session logging and monitoring
"""

import subprocess
import sys
from pathlib import Path

def get_tailscale_ip():
    """
    Get this device's Tailscale IP address.
    
    Why: Needed to bind Flask app to Tailscale network for remote access
    Where: Called during app startup to configure network binding
    How: Parses tailscale status output to extract IPv4 address only
    
    Returns:
        str: Tailscale IPv4 address or None if not available
    """
    try:
        result = subprocess.run(['tailscale', 'ip'], capture_output=True, text=True)
        if result.returncode == 0:
            # Get only the IPv4 address (first line, ignore IPv6)
            ips = result.stdout.strip().split('\n')
            for ip in ips:
                if '.' in ip and not ':' in ip:  # IPv4 format
                    return ip.strip()
            return ips[0].strip() if ips else None
    except FileNotFoundError:
        print("Tailscale not found - install with: curl -fsSL https://tailscale.com/install.sh | sh")
    except Exception as e:
        print(f"Error getting Tailscale IP: {e}")
    return None

def get_tailscale_status():
    """
    Get full Tailscale network status and connected devices.
    
    Why: Provides visibility into available devices for remote Clever access
    Where: Used for network diagnostics and device discovery
    How: Executes tailscale status command and parses output
    
    Returns:
        dict: Status information including connected devices and network state
    """
    try:
        result = subprocess.run(['tailscale', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            devices = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        devices.append({
                            'ip': parts[0],
                            'hostname': parts[1],
                            'user': parts[2],
                            'os': parts[3],
                            'status': parts[4] if len(parts) > 4 else 'online'
                        })
            
            return {
                'connected': True,
                'devices': devices,
                'network_ready': True
            }
    except Exception as e:
        print(f"Error getting Tailscale status: {e}")
    
    return {
        'connected': False,
        'devices': [],
        'network_ready': False
    }

def create_remote_access_info():
    """
    Create information file for remote access to Clever.
    
    Why: Provides easy reference for accessing Clever remotely from other devices
    Where: Creates info file in Clever directory for quick reference
    How: Generates connection details and usage instructions
    """
    tailscale_ip = get_tailscale_ip()
    status = get_tailscale_status()
    
    if not tailscale_ip:
        return False
    
    info_content = f"""# Clever Remote Access via Tailscale

## 🧠 Access Your Digital Brain Extension Remotely

### Primary Access URL:
**http://{tailscale_ip}:5000**

### From Your Other Devices:
- **Chromebook**: Open browser → http://{tailscale_ip}:5000
- **Samsung Phone**: Browser → http://{tailscale_ip}:5000  
- **Any Tailscale Device**: http://{tailscale_ip}:5000

### API Endpoints for Advanced Usage:
- **Chat**: POST http://{tailscale_ip}:5000/api/chat
- **Document Analysis**: POST http://{tailscale_ip}:5000/api/query_documents
- **Cognitive Sovereignty**: GET http://{tailscale_ip}:5000/api/cognitive_sovereignty/status

### Connected Devices in Your Network:
"""
    
    for device in status.get('devices', []):
        info_content += f"- **{device['hostname']}**: {device['ip']} ({device['os']}) - {device['status']}\n"
    
    info_content += f"""

### Security Notes:
- ✅ **Private Network**: Only accessible within your Tailscale network
- ✅ **Encrypted**: All traffic encrypted via WireGuard
- ✅ **No External Access**: Complete digital sovereignty maintained
- ✅ **Gmail Account**: Authenticated via lapirfta@gmail.com

### Quick Commands:
```bash
# Check Clever is running
curl http://{tailscale_ip}:5000

# Quick chat test  
curl -X POST http://{tailscale_ip}:5000/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{{"message": "Hello Clever!"}}' 

# Check cognitive sovereignty status
curl http://{tailscale_ip}:5000/api/cognitive_sovereignty/status
```

### Mobile Bookmarks:
Create these bookmarks on your phone/tablet for instant Clever access:
- **Clever Home**: http://{tailscale_ip}:5000
- **Clever Chat**: http://{tailscale_ip}:5000 (same interface)

---
*Generated: {Path(__file__).stat().st_mtime}*
*Tailscale IP: {tailscale_ip}*
*Network Status: {'Connected' if status['connected'] else 'Disconnected'}*
"""
    
    info_file = Path(__file__).parent / "REMOTE_ACCESS_INFO.md"
    info_file.write_text(info_content)
    
    print(f"✅ Remote access info created: {info_file}")
    print(f"🌐 Clever accessible at: http://{tailscale_ip}:5000")
    
    return True

def configure_flask_for_tailscale():
    """
    Configure Flask app to bind to Tailscale IP for remote access.
    
    Why: Enables Flask to accept connections from other devices on Tailscale network
    Where: Modifies Flask startup configuration in app.py or via environment
    How: Sets host binding to Tailscale IP address
    
    Returns:
        dict: Configuration settings for Flask remote access
    """
    tailscale_ip = get_tailscale_ip()
    
    if not tailscale_ip:
        return {
            'success': False,
            'error': 'Tailscale IP not available'
        }
    
    return {
        'success': True,
        'host': tailscale_ip,
        'port': 5000,
        'debug': False,  # Security: disable debug in remote access
        'threaded': True,
        'tailscale_ip': tailscale_ip,
        'bind_all': True  # Allow connections from any Tailscale device
    }

if __name__ == "__main__":
    print("🌐 Clever Tailscale Configuration")
    print("=" * 50)
    
    # Check Tailscale status
    tailscale_ip = get_tailscale_ip()
    if tailscale_ip:
        print(f"✅ Tailscale IP: {tailscale_ip}")
    else:
        print("❌ Tailscale not connected")
        sys.exit(1)
    
    # Get network status
    status = get_tailscale_status()
    print(f"🔗 Network Status: {'Connected' if status['connected'] else 'Disconnected'}")
    print(f"📱 Connected Devices: {len(status.get('devices', []))}")
    
    # Create access info
    if create_remote_access_info():
        print("\n🎉 Clever is ready for remote access!")
        print(f"🔗 Access URL: http://{tailscale_ip}:5000")
    else:
        print("\n❌ Failed to create remote access configuration")
        sys.exit(1)