#!/usr/bin/env python3
"""
start_clever_remote.py - Remote Access Startup Script for Clever

Why: Provides convenient remote startup of Clever with Tailscale network configuration
     for seamless digital brain extension access across Jay's devices.

Where: Standalone startup script that configures and launches Clever for remote access
       via Tailscale network while maintaining digital sovereignty.

How: Configures Tailscale networking, starts Flask with proper binding, and provides
     connection information for accessing Clever from remote devices.
"""

# Add Clever directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tailscale_config import get_tailscale_ip, get_tailscale_status, configure_flask_for_tailscale

def start_clever_remote():
    """Start Clever with Tailscale remote access configuration."""
    
    print("🧠 Starting Clever Digital Brain Extension")
    print("🌐 Configuring Tailscale Remote Access")
    print("=" * 60)
    
    # Check Tailscale connectivity
    tailscale_ip = get_tailscale_ip()
    if not tailscale_ip:
        print("❌ Tailscale not connected!")
        print("Run: sudo tailscale up")
        return False
    
    print(f"✅ Tailscale IP: {tailscale_ip}")
    
    # Get network status  
    status = get_tailscale_status()
    print(f"📱 Connected Devices: {len(status.get('devices', []))}")
    
    for device in status.get('devices', []):
        status_icon = "🟢" if device['status'] != 'offline' else "🔴"
        print(f"   {status_icon} {device['hostname']} ({device['os']})")
    
    print()
    print("🚀 Starting Clever Flask Server...")
    print(f"🔗 Remote Access: http://{tailscale_ip}:5000")
    print("📱 Bookmark this URL on your other devices!")
    print()
    print("Press Ctrl+C to stop server")
    print("=" * 60)
    
    # Import and start the main app
    try:
        from app import app
        
        # Configure for remote access
        flask_config = configure_flask_for_tailscale()
        if not flask_config['success']:
            print(f"❌ Flask configuration error: {flask_config.get('error')}")
            return False
            
        # Start Flask with Tailscale configuration
        app.run(
            host='0.0.0.0',  # Accept connections from all Tailscale devices
            port=5000,
            debug=False,     # Security: disable debug for remote access
            threaded=True    # Handle multiple remote connections
        )
        
    except KeyboardInterrupt:
        print("\n👋 Clever shutting down gracefully...")
        return True
    except Exception:
        print(f"❌ Error starting Clever: {e}")
        return False

if __name__ == "__main__":
    success = start_clever_remote()
    sys.exit(0 if success else 1)