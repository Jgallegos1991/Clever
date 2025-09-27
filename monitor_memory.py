#!/usr/bin/env python3
"""
Continuous memory monitoring for Clever revolutionary optimization.
"""

def check_memory():
    """Check current memory status."""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        memory = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                value = ''.join(filter(str.isdigit, value))
                if value:
                    memory[key.strip()] = int(value) * 1024
        
        available_mb = memory.get('MemAvailable', 0) / (1024 * 1024)
        total_mb = memory.get('MemTotal', 0) / (1024 * 1024)
        
        return available_mb, total_mb
        
    except Exception as _e:
        print(f"Memory check failed: {e}")
        return 800, 2700

def monitor_clever_memory():
    """Monitor Clever's memory usage continuously."""
    print("🔄 Starting Clever memory monitoring...")
    
    try:
        while True:
            available, total = check_memory()
            usage_percent = ((total - available) / total) * 100
            
            print(f"Memory: {available:.0f}MB available ({usage_percent:.1f}% used)")
            
            # Alert if memory gets critically low
            if available < total * 0.1:  # Less than 10% available
                print("🚨 CRITICAL: Memory pressure detected!")
                subprocess.run(['python3', 'revolutionary_memory_strategy.py'], 
                             capture_output=True)
            
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n👋 Memory monitoring stopped")

if __name__ == "__main__":
    monitor_clever_memory()
