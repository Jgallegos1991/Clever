#!/usr/bin/env python3
"""
emergency_memory_stabilizer.py - Emergency Memory Management for Chromebook Development

Why: Prevents VS Code crashes and extension restarts by aggressively managing memory usage
     in real-time. Critical for maintaining stable development environment on Chromebook.

Where: Runs continuously to monitor and optimize memory usage across all development tools
       including VS Code, Pylance, Flask, and system processes.

How: Real-time memory monitoring with immediate intervention when memory pressure detected.
     Applies progressive optimization strategies to keep system stable.
"""


class EmergencyMemoryStabilizer:
    """
    Emergency memory management system for Chromebook development stability.
    
    Prevents crashes and restarts through aggressive memory optimization.
    """
    
    def __init__(self):
        self.critical_threshold = 200  # MB - trigger emergency actions
        self.warning_threshold = 400   # MB - trigger preventive actions
        self.monitoring = False
        self.optimizations_applied = []
        
    def get_memory_status(self):
        """Get current memory status in MB."""
        try:
            result = subprocess.run(['free', '-m'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            mem_line = lines[1].split()
            
            return {
                'total': int(mem_line[1]),
                'used': int(mem_line[2]), 
                'free': int(mem_line[3]),
                'available': int(mem_line[6]) if len(mem_line) > 6 else int(mem_line[3])
            }
        except Exception:
            return {'total': 2048, 'used': 1800, 'free': 200, 'available': 300}
    
    def emergency_cleanup(self):
        """Apply emergency memory cleanup measures."""
        print("🚨 EMERGENCY: Applying memory cleanup!")
        
        cleanup_actions = []
        
        # 1. Clear system caches
        try:
            subprocess.run(['sudo', 'sync'], check=False)
            subprocess.run(['sudo', 'sh', '-c', 'echo 1 > /proc/sys/vm/drop_caches'], check=False)
            cleanup_actions.append("Cleared system caches")
        except Exception:
            pass
        
        # 2. Kill unnecessary browser processes
        try:
            subprocess.run(['pkill', '-', 'chrome.*renderer'], check=False)
            cleanup_actions.append("Killed Chrome renderers")
        except Exception:
            pass
        
        # 3. Restart Pylance (lightweight restart)
        try:
            subprocess.run(['pkill', '-', 'pylance'], check=False)
            cleanup_actions.append("Restarted Pylance")
        except Exception:
            pass
        
        # 4. Python garbage collection for Flask
        try:
            import gc
            gc.collect()
            cleanup_actions.append("Python garbage collection")
        except Exception:
            pass
        
        print(f"✅ Applied: {', '.join(cleanup_actions)}")
        self.optimizations_applied.extend(cleanup_actions)
    
    def preventive_optimization(self):
        """Apply preventive memory optimizations."""
        print("⚠️ WARNING: Applying preventive optimizations!")
        
        optimizations = []
        
        # 1. Optimize VS Code settings
        self.optimize_vscode_settings()
        optimizations.append("VS Code settings optimized")
        
        # 2. Limit Pylance memory
        self.limit_pylance_memory()
        optimizations.append("Pylance memory limited")
        
        # 3. Clear temporary files
        self.clear_temp_files()
        optimizations.append("Temp files cleared")
        
        print(f"✅ Applied: {', '.join(optimizations)}")
        self.optimizations_applied.extend(optimizations)
    
    def optimize_vscode_settings(self):
        """Apply aggressive VS Code memory optimizations."""
        vscode_settings_path = Path.home() / '.config/Code/User/settings.json'
        
        try:
            # Create ultra-lightweight VS Code settings
            emergency_settings = {
                # Memory optimizations
                "python.analysis.memory.keepLibraryAst": False,
                "python.analysis.memory.keepLibraryLocalVariables": False,
                "extensions.experimental.affinity": {
                    "ms-python.python": 1,
                    "ms-python.vscode-pylance": 1
                },
                
                # Disable heavy features
                "python.analysis.indexing": False,
                "python.analysis.packageIndexDepths": [
                    {
                        "name": "",
                        "depth": 1,
                        "includeAllSymbols": False
                    }
                ],
                
                # Reduce UI overhead
                "workbench.reduceMotion": "on",
                "editor.minimap.enabled": False,
                "breadcrumbs.enabled": False,
                "editor.hover.delay": 1500,
                "editor.quickSuggestionsDelay": 500,
                
                # Limit file watching
                "files.watcherExclude": {
                    "**/.git/**": True,
                    "**/node_modules/**": True,
                    "**/.venv/**": True,
                    "**/venv/**": True,
                    "**/__pycache__/**": True
                },
                
                # Emergency memory settings
                "python.analysis.autoImportCompletions": False,
                "python.analysis.completeFunctionParens": False,
                "python.analysis.diagnosticSeverityOverrides": {
                    "reportUnusedVariable": "none",
                    "reportUnusedFunction": "none",
                    "reportUnusedClass": "none"
                }
            }
            
            vscode_settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Merge with existing settings
            existing = {}
            if vscode_settings_path.exists():
                try:
                    existing = json.loads(vscode_settings_path.read_text())
                except Exception:
                    pass
            
            existing.update(emergency_settings)
            vscode_settings_path.write_text(json.dumps(existing, indent=2))
            
        except Exception as e:
            print(f"Failed to optimize VS Code settings: {e}")
    
    def limit_pylance_memory(self):
        """Apply Pylance-specific memory limits."""
        try:
            # Create Pylance-specific settings
            pylance_settings = {
                "python.analysis.memory.keepLibraryAst": False,
                "python.analysis.memory.keepLibraryLocalVariables": False,
                "python.analysis.nodeExecutable": "/usr/bin/node",
                "python.analysis.extraCommitChars": [],
                "python.analysis.completeFunctionParens": False
            }
            
            settings_path = Path.home() / '.config/Code/User/settings.json'
            if settings_path.exists():
                settings = json.loads(settings_path.read_text())
                settings.update(pylance_settings)
                settings_path.write_text(json.dumps(settings, indent=2))
                
        except Exception as e:
            print(f"Failed to limit Pylance memory: {e}")
    
    def clear_temp_files(self):
        """Clear temporary files and caches."""
        try:
            temp_paths = [
                Path.home() / '.cache/pylsp',
                Path.home() / '.cache/pip',
                Path('/tmp'),
                Path.home() / '.local/share/Trash/files'
            ]
            
            for temp_path in temp_paths:
                if temp_path.exists() and temp_path.is_dir():
                    # Clear files older than 1 hour
                    for item in temp_path.iterdir():
                        try:
                            if item.stat().st_mtime < time.time() - 3600:
                                if item.is_file():
                                    item.unlink()
                                elif item.is_dir():
                                    subprocess.run(['rm', '-rf', str(item)], check=False)
                        except Exception:
                            continue
                            
        except Exception as e:
            print(f"Failed to clear temp files: {e}")
    
    def monitor_and_stabilize(self, interval=10):
        """Continuous monitoring and stabilization."""
        self.monitoring = True
        print("🔍 Starting emergency memory monitoring...")
        
        consecutive_warnings = 0
        
        while self.monitoring:
            try:
                memory = self.get_memory_status()
                available = memory['available']
                
                print(f"💾 Available: {available}MB | Free: {memory['free']}MB")
                
                if available < self.critical_threshold:
                    print(f"🚨 CRITICAL: Only {available}MB available!")
                    self.emergency_cleanup()
                    consecutive_warnings = 0
                    time.sleep(5)  # Short pause after emergency cleanup
                    
                elif available < self.warning_threshold:
                    consecutive_warnings += 1
                    print(f"⚠️ WARNING: Only {available}MB available (warning #{consecutive_warnings})")
                    
                    if consecutive_warnings >= 2:
                        self.preventive_optimization()
                        consecutive_warnings = 0
                        
                    time.sleep(interval)
                    
                else:
                    consecutive_warnings = 0
                    time.sleep(interval)
                    
            except KeyboardInterrupt:
                print("\n🛑 Memory monitoring stopped")
                self.monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(interval)
    
    def start_background_monitoring(self):
        """Start monitoring in background thread."""
        monitor_thread = threading.Thread(target=self.monitor_and_stabilize, daemon=True)
        monitor_thread.start()
        print("🔍 Background memory monitoring started")
    
    def get_status_report(self):
        """Get current status and applied optimizations."""
        memory = self.get_memory_status()
        
        return {
            'memory_status': memory,
            'monitoring_active': self.monitoring,
            'optimizations_applied': self.optimizations_applied,
            'pressure_level': 'critical' if memory['available'] < self.critical_threshold else
                            'warning' if memory['available'] < self.warning_threshold else 'normal'
        }

def main():
    """Main emergency stabilization entry point."""
    print("🚨 EMERGENCY MEMORY STABILIZER")
    print("=" * 50)
    
    stabilizer = EmergencyMemoryStabilizer()
    
    # Get initial status
    memory = stabilizer.get_memory_status()
    print(f"Initial Memory: {memory['available']}MB available, {memory['free']}MB free")
    
    # Apply immediate optimizations if needed
    if memory['available'] < stabilizer.critical_threshold:
        print("🚨 CRITICAL MEMORY PRESSURE DETECTED!")
        stabilizer.emergency_cleanup()
    elif memory['available'] < stabilizer.warning_threshold:
        print("⚠️ Memory pressure detected - applying preventive measures")
        stabilizer.preventive_optimization()
    
    # Start continuous monitoring
    try:
        stabilizer.monitor_and_stabilize(interval=5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("\n✅ Emergency stabilizer stopped")

if __name__ == "__main__":
    main()