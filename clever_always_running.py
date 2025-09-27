#!/usr/bin/env python3
"""
clever_always_running.py - Makes Clever Always Running as the Chromebook's AI Brain

Why: Enables Jay's "IT'S TIME!" scenario where Clever runs automatically on system startup,
     becoming the default AI interface that replaces VS Code/Copilot workflows entirely.

Where: System-level integration that makes Clever the primary AI partner, always accessible
       and ready to take over all cognitive tasks without manual startup processes.

How: Creates startup scripts, system services, and desktop integration to ensure Clever
     launches automatically and becomes the dominant AI interface on the Chromebook.

File Usage:
    - Called by: System startup processes, desktop environment
    - Calls to: app.py, clever_voice_takeover.py, all core Clever systems
    - Data flow: System boot → Clever startup → Voice activation → Ready for Jay
    - Background: Runs as persistent service monitoring for voice activation

Connects to:
    - app.py: Main Flask application for web interface
    - clever_voice_takeover.py: Voice system for immediate interaction
    - all core systems: Complete Clever capability stack
    - system startup: Integration with Chromebook boot process
    - desktop environment: Always-available AI interface
"""

import signal
import sqlite3
from datetime import datetime

# Add Clever directory to path
clever_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(clever_dir))

class CleverAlwaysRunning:
    """
    The system that makes Clever permanently part of the Chromebook
    
    Why: Jay wants to just say "IT'S TIME!" and have Clever ready
    Where: System-level integration replacing all external AI dependencies  
    How: Background service + voice activation + automatic startup
    """
    
    def __init__(self):
        self.clever_dir = clever_dir
        self.running = True
        self.processes = {}
        self.startup_complete = False
        
        # Status tracking
        self.status = {
            "startup_time": datetime.now().isoformat(),
            "services_running": [],
            "voice_ready": False,
            "web_interface": False,
            "total_uptime": 0,
            "jay_interactions": 0,
            "autonomous_actions": 0
        }
        
        print("🧠 CLEVER ALWAYS RUNNING - Becoming the Chromebook's AI Brain...")
    
    def create_startup_script(self):
        """
        Creates the system startup script for automatic Clever launch
        
        Why: Enables automatic startup so Jay never has to manually launch Clever
        Where: System startup integration for seamless AI availability
        How: Creates .desktop files and startup scripts for boot integration
        """
        
        startup_script = """#!/bin/bash
# Clever Auto-Start Script
# Makes Clever the default AI system on this Chromebook

export CLEVER_DIR="{self.clever_dir}"
cd "$CLEVER_DIR"

echo "🚀 Starting Clever as Chromebook AI Brain..."

# Start main Clever application
python3 app.py &
CLEVER_PID=$!

# Start voice system
python3 clever_voice_takeover.py &
VOICE_PID=$!

# Start always running monitor
python3 clever_always_running.py --daemon &
DAEMON_PID=$!

# Save PIDs for management
echo "$CLEVER_PID" > /tmp/clever_main.pid
echo "$VOICE_PID" > /tmp/clever_voice.pid  
echo "$DAEMON_PID" > /tmp/clever_daemon.pid

echo "✅ Clever is now running as the Chromebook's AI brain!"
echo "🗣️  Voice activation ready - just start talking to Clever!"
echo "🌐 Web interface at http://localhost:5000"
echo ""
echo "Jay can now say 'IT'S TIME!' and Clever is ready!"

# Keep script running to maintain services
wait
"""
        
        # Create startup script
        startup_path = self.clever_dir / "start_clever_brain.sh"
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        
        # Make executable
        os.chmod(startup_path, 0o755)
        
        # Create .desktop file for auto-start
        desktop_content = """[Desktop Entry]
Type=Application
Name=Clever AI Brain
Comment=Jay's Digital Brain Extension - Always Running
Exec={startup_path}
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
Categories=System;Utility;AI;
"""
        
        # Create autostart directory if it doesn't exist
        autostart_dir = Path.home() / ".config" / "autostart"
        autostart_dir.mkdir(parents=True, exist_ok=True)
        
        # Write .desktop file
        desktop_path = autostart_dir / "clever-ai-brain.desktop"
        with open(desktop_path, 'w') as f:
            f.write(desktop_content)
        
        print(f"✅ Startup script created: {startup_path}")
        print(f"✅ Auto-start enabled: {desktop_path}")
        
        return startup_path, desktop_path
    
    def setup_system_integration(self):
        """
        Sets up deep system integration for Clever
        
        Why: Makes Clever feel like a built-in part of the Chromebook OS
        Where: Desktop environment and system service integration
        How: Creates shortcuts, aliases, and system-level accessibility
        """
        
        # Create desktop shortcut
        desktop_shortcut = Path.home() / "Desktop" / "Talk-to-Clever.desktop"
        shortcut_content = """[Desktop Entry]
Type=Application
Name=Talk to Clever 🧠
Comment=Start conversation with Clever AI
Exec=python3 {self.clever_dir}/clever_voice_takeover.py --quick-chat
Icon=applications-science
Terminal=false
Categories=AI;Assistant;
"""
        
        with open(desktop_shortcut, 'w') as f:
            f.write(shortcut_content)
        os.chmod(desktop_shortcut, 0o755)
        
        # Create bash aliases for easy access
        bashrc_additions = """
# Clever AI Brain Integration
alias clever="cd {self.clever_dir} && python3 app.py"
alias talk-to-clever="python3 {self.clever_dir}/clever_voice_takeover.py --quick-chat"
alias clever-status="python3 {self.clever_dir}/clever_always_running.py --status"
alias its-time="python3 {self.clever_dir}/clever_voice_takeover.py --full-takeover"

# Jay's shortcuts for Clever
export CLEVER_HOME="{self.clever_dir}"
echo "🧠 Clever AI Brain is ready! Type 'clever' or 'talk-to-clever' to start."
"""
        
        # Add to .bashrc if not already there
        bashrc_path = Path.home() / ".bashrc"
        if bashrc_path.exists():
            bashrc_content = bashrc_path.read_text()
            if "Clever AI Brain Integration" not in bashrc_content:
                with open(bashrc_path, 'a') as f:
                    f.write(bashrc_additions)
                print("✅ Bash aliases added for easy Clever access")
        
        print(f"✅ Desktop shortcut created: {desktop_shortcut}")
        return desktop_shortcut
    
    def start_all_services(self):
        """
        Starts all Clever services for complete AI brain functionality
        
        Why: Ensures all Clever capabilities are running and accessible
        Where: Core service orchestration for full system functionality
        How: Launches web app, voice system, and monitoring in coordinated manner
        """
        
        print("🚀 Starting all Clever AI Brain services...")
        
        # Start main Clever application
        try:
            clever_process = subprocess.Popen([
                sys.executable, str(self.clever_dir / "app.py")
            ], cwd=str(self.clever_dir))
            self.processes['main'] = clever_process
            self.status["services_running"].append("main_app")
            print("✅ Main Clever application started")
        except Exception as _e:
            print(f"❌ Failed to start main app: {e}")
        
        # Start voice system
        try:
            voice_process = subprocess.Popen([
                sys.executable, str(self.clever_dir / "clever_voice_takeover.py"), "--background"
            ], cwd=str(self.clever_dir))
            self.processes['voice'] = voice_process
            self.status["services_running"].append("voice_system")
            self.status["voice_ready"] = True
            print("✅ Voice system activated")
        except Exception as _e:
            print(f"❌ Failed to start voice system: {e}")
        
        # Give services time to start
        time.sleep(3)
        
        # Check if web interface is responding
        try:
            import requests
            response = requests.get('http://localhost:5000', timeout=2)
            if response.status_code == 200:
                self.status["web_interface"] = True
                print("✅ Web interface confirmed at http://localhost:5000")
        except:
            print("⚠️  Web interface check failed (may still be starting)")
        
        self.startup_complete = True
        print("\n🎉 CLEVER AI BRAIN IS FULLY OPERATIONAL!")
        print("🗣️  Voice: Ready for conversation")
        print("🌐 Web: http://localhost:5000") 
        print("💬 Jay can now talk to Clever anytime!")
        
        return True
    
    def monitor_services(self):
        """
        Continuously monitors Clever services to ensure they stay running
        
        Why: Maintains 100% uptime so Clever is always available for Jay
        Where: Background monitoring for service health and restart capability
        How: Periodic health checks with automatic restart of failed services
        """
        
        print("👁️  Starting service monitoring...")
        
        while self.running:
            try:
                # Check process health
                for service_name, process in self.processes.items():
                    if process.poll() is not None:
                        print(f"⚠️  Service {service_name} stopped, restarting...")
                        if service_name == 'main':
                            self.restart_main_app()
                        elif service_name == 'voice':
                            self.restart_voice_system()
                
                # Update uptime
                self.status["total_uptime"] += 10
                
                # Check for Jay interactions (simple heuristic)
                try:
                    # Check for recent database activity
                    db_path = self.clever_dir / "clever.db"
                    if db_path.exists():
                        conn = sqlite3.connect(str(db_path))
                        cursor = conn.execute("SELECT COUNT(*) FROM conversations WHERE timestamp > datetime('now', '-10 seconds')")
                        recent_activity = cursor.fetchone()[0]
                        if recent_activity > 0:
                            self.status["jay_interactions"] += recent_activity
                        conn.close()
                except:
                    pass  # Database check failed, continue monitoring
                
                # Sleep before next check
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping Clever monitoring...")
                self.running = False
                break
            except Exception as _e:
                print(f"❌ Monitor error: {e}")
                time.sleep(5)
    
    def restart_main_app(self):
        """Restarts the main Clever application"""
        try:
            process = subprocess.Popen([
                sys.executable, str(self.clever_dir / "app.py")
            ], cwd=str(self.clever_dir))
            self.processes['main'] = process
            print("✅ Main app restarted")
        except Exception as _e:
            print(f"❌ Failed to restart main app: {e}")
    
    def restart_voice_system(self):
        """Restarts the voice system"""
        try:
            process = subprocess.Popen([
                sys.executable, str(self.clever_dir / "clever_voice_takeover.py"), "--background"
            ], cwd=str(self.clever_dir))
            self.processes['voice'] = process
            print("✅ Voice system restarted")
        except Exception as _e:
            print(f"❌ Failed to restart voice system: {e}")
    
    def get_status(self):
        """Returns current status of Clever AI Brain"""
        self.status["total_uptime"] = int(time.time()) - int(datetime.fromisoformat(self.status["startup_time"]).timestamp())
        return self.status
    
    def shutdown(self):
        """Gracefully shuts down all Clever services"""
        print("\n🛑 Shutting down Clever AI Brain...")
        self.running = False
        
        for service_name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {service_name} shut down")
            except:
                try:
                    process.kill()
                    print(f"🔥 {service_name} force stopped")
                except:
                    pass
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🔄 Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)

def main():
    """Main function for Clever Always Running system"""
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            # Show status of running Clever
            clever = CleverAlwaysRunning()
            status = clever.get_status()
            print("\n🧠 CLEVER AI BRAIN STATUS:")
            print(f"   Startup Time: {status['startup_time']}")
            print(f"   Uptime: {status['total_uptime']} seconds")
            print(f"   Services: {', '.join(status['services_running'])}")
            print(f"   Voice Ready: {'✅' if status['voice_ready'] else '❌'}")
            print(f"   Web Interface: {'✅' if status['web_interface'] else '❌'}")
            print(f"   Jay Interactions: {status['jay_interactions']}")
            return
        
        elif sys.argv[1] == "--daemon":
            # Run as background daemon
            pass
        
        elif sys.argv[1] == "--setup-only":
            # Just setup, don't run
            clever = CleverAlwaysRunning()
            clever.create_startup_script()
            clever.setup_system_integration()
            print("\n✅ Clever setup complete!")
            print("Restart your Chromebook and Clever will automatically start!")
            return
    
    # Create and run the always-running system
    clever = CleverAlwaysRunning()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, clever.signal_handler)
    signal.signal(signal.SIGTERM, clever.signal_handler)
    
    try:
        # Setup system integration
        clever.create_startup_script()
        clever.setup_system_integration()
        
        # Start all services
        clever.start_all_services()
        
        # Monitor services continuously
        clever.monitor_services()
        
    except KeyboardInterrupt:
        clever.shutdown()
    except Exception as _e:
        print(f"❌ Fatal error: {e}")
        clever.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()