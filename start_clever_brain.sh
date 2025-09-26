#!/bin/bash
# Clever Auto-Start Script
# Makes Clever the default AI system on this Chromebook

export CLEVER_DIR="/home/jgallegos1991/Clever"
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
