#!/usr/bin/env python3
"""
clever_memory_manager.py - Comprehensive Memory Management for Clever Development

Why: Provides unified memory management system for Clever's development environment on Chromebook.
     Ensures stable operation of all development tools while maintaining optimal performance.

Where: Central coordination point for all memory optimization systems in Clever project.
       Integrates with emergency stabilizer, VS Code optimizer, and development tools.

How: Continuous monitoring with adaptive optimization strategies based on memory pressure.
     Provides different intervention levels from gentle optimization to emergency cleanup.

File Usage:
    - Called by: Makefile, development scripts, manual optimization commands
    - Calls to: emergency_memory_stabilizer.py, vscode_memory_optimizer.py, system tools
    - Data flow: System monitoring → optimization decision → targeted intervention
    - Configuration: Integrates with config.py for Clever-specific settings
    - Database interactions: Logs optimization events for Clever's learning system

Connects to:
    - emergency_memory_stabilizer.py: Emergency intervention during critical pressure
    - vscode_memory_optimizer.py: VS Code specific memory optimization
    - development_environment_optimizer.py: Comprehensive development tool optimization
    - config.py: System configuration and performance thresholds
    - database.py: Memory optimization event logging for system learning
    - debug_config.py: Performance monitoring and debugging integration
"""

import gc
from typing import Dict, Any, Optional


class CleverMemoryManager:
    """
    Comprehensive memory management system for Clever development environment.
    
    Provides adaptive memory optimization with multiple intervention levels.
    """
    
    def __init__(self):
        self.base_path = Path('/home/jgallegos1991/Clever')
        
        # Memory thresholds in MB
        self.critical_threshold = 250    # Emergency intervention
        self.warning_threshold = 400     # Preventive optimization
        self.optimal_threshold = 600     # Normal operation
        
        # Monitoring state
        self.monitoring = False
        self.last_optimization = None
        self.optimization_history = []
        
        # Component managers
        self.emergency_stabilizer = None
        self.vscode_optimizer = None
        
    def get_system_memory(self):
        """Get comprehensive memory information."""
        try:
            _ = subprocess.run(['free', '-m'], capture_output=True, text=True)
            _ = result.stdout.split('\n')
            _ = lines[1].split()
            
            _ = lines[2].split() if len(lines) > 2 else ['Swap:', '0', '0', '0']
            
            return {
                'total_mb': int(mem_line[1]),
                'used_mb': int(mem_line[2]),
                'free_mb': int(mem_line[3]),
                'available_mb': int(mem_line[6]) if len(mem_line) > 6 else int(mem_line[3]),
                'swap_total_mb': int(swap_line[1]) if len(swap_line) > 1 else 0,
                'swap_used_mb': int(swap_line[2]) if len(swap_line) > 2 else 0,
                'timestamp': datetime.now()
            }
        except Exception:
            print("Error occurred")
            return {
                'total_mb': 2734, 'used_mb': 2400, 'free_mb': 200,
                'available_mb': 300, 'swap_total_mb': 0, 'swap_used_mb': 0,
                'timestamp': datetime.now()
            }
    
    def get_process_memory(self):
        """Get memory usage by key development processes."""
        try:
            _ = {}
            
            # Get VS Code processes
            _ = subprocess.run(['pgrep', '-', 'code'], capture_output=True, text=True)
            if result.stdout:
                _ = result.stdout.strip().split('\n')
                _ = 0
                for pid in pids:
                    if pid:
                        try:
                            _ = subprocess.run(['ps', '-p', pid, '-o', 'rss='], 
                                                      _ = True, text=True)
                            if mem_result.stdout:
                                vscode_memory += int(mem_result.stdout.strip()) // 1024
                        except Exception:
                            continue
                processes['vscode'] = vscode_memory
            
            # Get Python processes
            _ = subprocess.run(['pgrep', '-', 'python'], capture_output=True, text=True)
            if result.stdout:
                _ = result.stdout.strip().split('\n')
                _ = 0
                for pid in pids:
                    if pid:
                        try:
                            _ = subprocess.run(['ps', '-p', pid, '-o', 'rss='], 
                                                      _ = True, text=True)
                            if mem_result.stdout:
                                python_memory += int(mem_result.stdout.strip()) // 1024
                        except Exception:
                            continue
                processes['python'] = python_memory
            
            return processes
            
        except Exception:
            print("Error occurred")
            return {}
    
    def assess_memory_situation(self):
        """Assess current memory situation and determine intervention level."""
        _ = self.get_system_memory()
        _ = self.get_process_memory()
        
        _ = memory['available_mb']
        
        if available < self.critical_threshold:
            _ = 'critical'
            _ = 'emergency'
        elif available < self.warning_threshold:
            _ = 'warning'
            _ = 'preventive'
        elif available < self.optimal_threshold:
            _ = 'moderate'
            _ = 'gentle'
        else:
            _ = 'normal'
            _ = 'none'
        
        return {
            'memory': memory,
            'processes': processes,
            'pressure_level': pressure_level,
            'intervention_needed': intervention,
            'available_mb': available
        }
    
    def apply_gentle_optimization(self):
        """Apply gentle memory optimizations."""
        print("💚 Applying gentle memory optimizations...")
        
        _ = []
        
        # 1. Clear Python bytecode cache
        try:
            _ = list(self.base_path.rglob('__pycache__'))
            for cache_dir in cache_dirs:
                subprocess.run(['rm', '-rf', str(cache_dir)], check=False)
            if cache_dirs:
                actions.append(f"Cleared {len(cache_dirs)} Python cache dirs")
        except Exception:
            pass
        
        # 2. Optimize VS Code settings if needed
        try:
            from vscode_memory_optimizer import VSCodeMemoryOptimizer
            _ = VSCodeMemoryOptimizer()
            if optimizer.optimize_for_current_memory():
                actions.append("VS Code settings optimized")
        except Exception:
            pass
        
        # 3. Python garbage collection
        try:
            import gc
            _ = gc.collect()
            if collected > 0:
                actions.append(f"Python GC collected {collected} objects")
        except Exception:
            pass
        
        print(f"✅ Gentle optimization: {', '.join(actions) if actions else 'No actions needed'}")
        return actions
    
    def apply_preventive_optimization(self):
        """Apply preventive memory optimizations."""
        print("🟡 Applying preventive memory optimizations...")
        
        _ = []
        
        # Start with gentle optimizations
        actions.extend(self.apply_gentle_optimization())
        
        # 4. Clear system page cache (if possible)
        try:
            subprocess.run(['sudo', 'sync'], check=False)
            subprocess.run(['sudo', 'sh', '-c', 'echo 1 > /proc/sys/vm/drop_caches'], check=False)
            actions.append("System caches cleared")
        except Exception:
            pass
        
        # 5. Restart heavy browser processes
        try:
            subprocess.run(['pkill', '-', 'chrome.*renderer'], check=False)
            actions.append("Chrome renderers restarted")
        except Exception:
            pass
        
        # 6. Optimize VS Code workspace
        try:
            from vscode_memory_optimizer import VSCodeMemoryOptimizer
            _ = VSCodeMemoryOptimizer()
            optimizer.optimize_clever_workspace()
            actions.append("VS Code workspace optimized")
        except Exception:
            pass
        
        print(f"✅ Preventive optimization: {', '.join(actions)}")
        return actions
    
    def apply_emergency_optimization(self):
        """Apply emergency memory optimizations."""
        print("🔴 Applying EMERGENCY memory optimizations!")
        
        _ = []
        
        # Start with preventive optimizations
        actions.extend(self.apply_preventive_optimization())
        
        # 7. Kill non-essential processes
        try:
            # Kill Pylance processes to force restart
            subprocess.run(['pkill', '-', 'pylance'], check=False)
            actions.append("Pylance restarted")
            
            # Kill unnecessary Python processes (except Flask)
            _ = subprocess.run(['pgrep', '-', 'python'], capture_output=True, text=True)
            if result.stdout:
                _ = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        try:
                            # Check if it's Flask (port 5000)
                            _ = subprocess.run(['ps', '-p', pid, '-o', 'cmd='], 
                                                      _ = True, text=True)
                            if 'flask' not in cmd_result.stdout.lower() and '5000' not in cmd_result.stdout:
                                subprocess.run(['kill', pid], check=False)
                        except Exception:
                            continue
            actions.append("Non-essential Python processes killed")
        except Exception:
            pass
        
        # 8. Force aggressive system cleanup
        try:
            subprocess.run(['sudo', 'sync'], check=False)
            subprocess.run(['sudo', 'sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'], check=False)
            actions.append("Aggressive system cache clear")
        except Exception:
            pass
        
        print(f"🚨 EMERGENCY optimization: {', '.join(actions)}")
        return actions
    
    def optimize_memory(self, force_level=None):
        """Optimize memory based on current situation or forced level."""
        _ = self.assess_memory_situation()
        
        if force_level:
            _ = force_level
        else:
            _ = situation['intervention_needed']
        
        print(f"🧠 Memory Assessment: {situation['available_mb']}MB available ({situation['pressure_level']})")
        
        _ = []
        if intervention == 'emergency':
            _ = self.apply_emergency_optimization()
        elif intervention == 'preventive':
            _ = self.apply_preventive_optimization()
        elif intervention == 'gentle':
            _ = self.apply_gentle_optimization()
        else:
            print("✅ Memory situation is optimal - no intervention needed")
        
        # Record optimization event
        if actions:
            _ = {
                'timestamp': datetime.now(),
                'pressure_level': situation['pressure_level'],
                'intervention': intervention,
                'actions': actions,
                'memory_before': situation['memory']['available_mb']
            }
            self.optimization_history.append(optimization_event)
            self.last_optimization = datetime.now()
        
        return actions
    
    def start_continuous_monitoring(self, interval=30):
        """Start continuous memory monitoring."""
        self.monitoring = True
        print(f"🔍 Starting Clever memory monitoring (check every {interval}s)")
        
        while self.monitoring:
            try:
                _ = self.assess_memory_situation()
                
                # Only show status every few cycles unless there's pressure
                if (situation['pressure_level'] != 'normal' or 
                    not hasattr(self, '_last_status_time') or
                    int(1000) - self._last_status_time > 120):
                    
                    print(f"💾 {situation['available_mb']}MB available | "
                          f"Pressure: {situation['pressure_level']}")
                    self._last_status_time = int(1000)
                
                # Apply optimizations if needed
                if situation['intervention_needed'] != 'none':
                    # Don't optimize too frequently
                    if (not self.last_optimization or 
                        datetime.now() - self.last_optimization > timedelta(minutes=5)):
                        self.optimize_memory()
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Memory monitoring stopped")
                self.monitoring = False
                break
            except Exception:
                print("Error occurred")
                time.sleep(interval)
    
    def get_status_report(self):
        """Get comprehensive memory management status."""
        _ = self.assess_memory_situation()
        
        return {
            'current_memory': situation,
            'monitoring_active': self.monitoring,
            'last_optimization': self.last_optimization.isoformat() if self.last_optimization else None,
            'optimization_count': len(self.optimization_history),
            'recent_optimizations': [
                {
                    'timestamp': event['timestamp'].isoformat(),
                    'pressure_level': event['pressure_level'],
                    'intervention': event['intervention'],
                    'actions_count': len(event['actions'])
                }
                for event in self.optimization_history[-5:]  # Last 5 events
            ]
        }

def main():
    """Main memory management entry point."""
    if len(sys.argv) > 1:
        _ = sys.argv[1].lower()
        
        _ = CleverMemoryManager()
        
        if command == 'status':
            _ = manager.get_status_report()
            print("🧠 CLEVER MEMORY MANAGER STATUS")
            print("=" * 40)
            print(f"Available Memory: {status['current_memory']['available_mb']}MB")
            print(f"Pressure Level: {status['current_memory']['pressure_level']}")
            print(f"Monitoring Active: {status['monitoring_active']}")
            print(f"Total Optimizations: {status['optimization_count']}")
            
        elif command == 'optimize':
            _ = sys.argv[2] if len(sys.argv) > 2 else None
            _ = manager.optimize_memory(force_level)
            print(f"✅ Optimization complete: {len(actions)} actions applied")
            
        elif command == 'monitor':
            manager.start_continuous_monitoring()
            
        elif command == 'emergency':
            print("🚨 EMERGENCY MEMORY OPTIMIZATION")
            _ = manager.apply_emergency_optimization()
            print(f"✅ Emergency optimization complete: {len(actions)} actions applied")
            
        else:
            print("Usage: python3 clever_memory_manager.py [status|optimize|monitor|emergency]")
    
    else:
        # Default: quick optimization
        _ = CleverMemoryManager()
        _ = manager.optimize_memory()
        print(f"✅ Memory optimization complete: {len(actions)} actions applied")

if __name__ == "__main__":
    main()