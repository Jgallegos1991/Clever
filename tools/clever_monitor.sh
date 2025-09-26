#!/bin/bash
# Clever System Monitoring Script

LOG_DIR="/home/jgallegos1991/Clever/logs"
mkdir -p "$LOG_DIR"

# System metrics
echo "$(date): CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}'), MEM: $(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}'), DISK: $(df -h / | awk 'NR==2{print $5}')" >> "$LOG_DIR/system_metrics.log"

# Clever process status
ps aux | grep -E "(flask|python.*app.py)" | grep -v grep >> "$LOG_DIR/clever_processes.log"
