#!/usr/bin/env python3
"""
vscode_memory_optimizer.py - VS Code Memory Configuration for Chromebook

Why: Optimizes VS Code and Pylance settings specifically for Chromebook memory constraints.
     Prevents extension crashes and maintains stable development environment for Clever.

Where: Integrates with Clever's development environment and emergency memory stabilizer.
       Applied automatically when memory pressure is detected.

How: Updates VS Code configuration files with memory-optimized settings, limits Pylance
     memory usage, and provides different optimization profiles based on available memory.

File Usage:
    - Called by: emergency_memory_stabilizer.py during memory pressure events
    - Calls to: VS Code configuration files, system memory monitoring
    - Data flow: Memory status → optimization profile → VS Code settings update
    - Configuration: Uses VS Code user settings.json and workspace settings

Connects to:
    - emergency_memory_stabilizer.py: Automatic optimization during memory pressure
    - development_environment_optimizer.py: Comprehensive development tool optimization
    - config.py: System configuration and paths
    - database.py: Logging optimization events for Clever's learning
"""

import json
import os
from pathlib import Path
import subprocess
import time

class VSCodeMemoryOptimizer:
    """
    Specialized VS Code memory optimization for Chromebook development.
    
    Provides different optimization levels based on memory pressure.
    """
    
    def __init__(self):
        self.settings_path = Path.home() / '.config/Code/User/settings.json'
        self.workspace_settings_path = Path('/home/jgallegos1991/Clever/.vscode/settings.json')
        
    def get_memory_mb(self):
        """Get available memory in MB."""
        try:
            result = subprocess.run(['free', '-m'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            mem_line = lines[1].split()
            return int(mem_line[6]) if len(mem_line) > 6 else int(mem_line[3])
        except Exception:
            return 300
    
    def create_emergency_profile(self):
        """Emergency settings for critical memory situations (<300MB)."""
        return {
            # Core memory management
            "python.analysis.memory.keepLibraryAst": False,
            "python.analysis.memory.keepLibraryLocalVariables": False,
            
            # Disable heavy analysis features
            "python.analysis.indexing": False,
            "python.analysis.autoImportCompletions": False,
            "python.analysis.completeFunctionParens": False,
            "python.analysis.autoSearchPaths": False,
            
            # Minimal diagnostics
            "python.analysis.diagnosticMode": "workspace",
            "python.analysis.diagnosticSeverityOverrides": {
                "reportUnusedVariable": "none",
                "reportUnusedFunction": "none", 
                "reportUnusedClass": "none",
                "reportUnusedImport": "none",
                "reportMissingImports": "none",
                "reportOptionalSubscript": "none",
                "reportOptionalMemberAccess": "none",
                "reportGeneralTypeIssues": "none"
            },
            
            # Limit package analysis
            "python.analysis.packageIndexDepths": [{
                "name": "",
                "depth": 1,
                "includeAllSymbols": False
            }],
            
            # Extension affinity (keep Python extensions on same process)
            "extensions.experimental.affinity": {
                "ms-python.python": 1,
                "ms-python.vscode-pylance": 1
            },
            
            # UI optimizations
            "workbench.reduceMotion": "on",
            "editor.minimap.enabled": False,
            "breadcrumbs.enabled": False,
            "editor.hover.delay": 2000,
            "editor.quickSuggestionsDelay": 1000,
            "editor.suggest.showSnippets": False,
            "editor.suggest.showWords": False,
            "editor.wordBasedSuggestions": "off",
            
            # File watching limits
            "files.watcherExclude": {
                "**/.git/**": True,
                "**/node_modules/**": True,
                "**/.venv/**": True,
                "**/venv/**": True,
                "**/__pycache__/**": True,
                "**/logs/**": True,
                "**/static/**": True,
                "**/templates/**": True
            },
            
            # Search limits
            "search.exclude": {
                "**/.git": True,
                "**/node_modules": True,
                "**/.venv": True,
                "**/venv": True,
                "**/__pycache__": True,
                "**/logs": True
            },
            
            # Terminal optimizations
            "terminal.integrated.gpuAcceleration": "off",
            "terminal.integrated.rendererType": "dom",
            
            # Git optimizations
            "git.enabled": True,
            "git.autoRepositoryDetection": "openEditors"
        }
    
    def create_conservative_profile(self):
        """Conservative settings for low memory (300-500MB)."""
        emergency = self.create_emergency_profile()
        
        # Add back some features for better usability
        conservative = emergency.copy()
        conservative.update({
            "python.analysis.autoImportCompletions": True,
            "python.analysis.completeFunctionParens": True,
            "editor.minimap.enabled": True,
            "breadcrumbs.enabled": True,
            "editor.hover.delay": 1000,
            "editor.quickSuggestionsDelay": 500,
            
            # Limited diagnostics
            "python.analysis.diagnosticSeverityOverrides": {
                "reportUnusedVariable": "warning",
                "reportUnusedImport": "information",
                "reportMissingImports": "warning"
            }
        })
        
        return conservative
    
    def create_balanced_profile(self):
        """Balanced settings for moderate memory (>500MB)."""
        return {
            # Memory management (still conservative)
            "python.analysis.memory.keepLibraryAst": False,
            "python.analysis.memory.keepLibraryLocalVariables": True,
            
            # Standard analysis
            "python.analysis.indexing": True,
            "python.analysis.autoImportCompletions": True,
            "python.analysis.completeFunctionParens": True,
            "python.analysis.autoSearchPaths": True,
            
            # Package analysis with limits
            "python.analysis.packageIndexDepths": [{
                "name": "",
                "depth": 2,
                "includeAllSymbols": False
            }],
            
            # Extension affinity
            "extensions.experimental.affinity": {
                "ms-python.python": 1,
                "ms-python.vscode-pylance": 1
            },
            
            # UI optimizations (less aggressive)
            "editor.minimap.enabled": True,
            "breadcrumbs.enabled": True,
            "editor.hover.delay": 500,
            "editor.quickSuggestionsDelay": 300,
            
            # File watching (still limited)
            "files.watcherExclude": {
                "**/.git/**": True,
                "**/node_modules/**": True,
                "**/.venv/**": True,
                "**/venv/**": True,
                "**/__pycache__/**": True
            }
        }
    
    def apply_settings(self, settings_dict, target='user'):
        """Apply settings to VS Code configuration."""
        try:
            if target == 'user':
                settings_path = self.settings_path
            else:
                settings_path = self.workspace_settings_path
                
            # Create directory if needed
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing settings
            existing_settings = {}
            if settings_path.exists():
                try:
                    existing_settings = json.loads(settings_path.read_text())
                except Exception:
                    pass
            
            # Merge settings
            existing_settings.update(settings_dict)
            
            # Write back
            settings_path.write_text(json.dumps(existing_settings, indent=2))
            
            return True
            
        except Exception as e:
            print(f"Failed to apply {target} settings: {e}")
            return False
    
    def optimize_for_current_memory(self):
        """Apply appropriate optimization profile based on current memory."""
        available_mb = self.get_memory_mb()
        
        print(f"🔧 VS Code optimization for {available_mb}MB available memory")
        
        if available_mb < 300:
            print("🚨 Applying EMERGENCY optimization profile")
            profile = self.create_emergency_profile()
            optimization_level = "emergency"
            
        elif available_mb < 500:
            print("⚠️ Applying CONSERVATIVE optimization profile")
            profile = self.create_conservative_profile()
            optimization_level = "conservative"
            
        else:
            print("✅ Applying BALANCED optimization profile")
            profile = self.create_balanced_profile()
            optimization_level = "balanced"
        
        # Apply to both user and workspace settings
        user_success = self.apply_settings(profile, 'user')
        workspace_success = self.apply_settings(profile, 'workspace')
        
        if user_success and workspace_success:
            print(f"✅ Applied {optimization_level} profile to VS Code settings")
            return True
        else:
            print(f"❌ Failed to apply {optimization_level} profile")
            return False
    
    def create_clever_specific_settings(self):
        """Create Clever-specific workspace optimizations."""
        clever_settings = {
            # Clever project specific optimizations
            "python.defaultInterpreterPath": "/usr/bin/python3",
            
            # File associations for Clever
            "files.associations": {
                "*.py": "python",
                "Makefile": "makefile",
                "requirements*.txt": "pip-requirements"
            },
            
            # Clever-specific excludes
            "files.exclude": {
                "**/__pycache__": True,
                "**/logs": True,
                "**/*.pyc": True,
                "**/clever.db": False,  # Keep database visible
                "**/static/js/engines/*.min.js": True
            },
            
            # Search settings for Clever codebase
            "search.exclude": {
                "**/__pycache__": True,
                "**/logs": True,
                "**/static/css/*.min.css": True,
                "**/static/js/*.min.js": True
            },
            
            # Python specific for Clever
            "python.analysis.extraPaths": [
                "./",
                "./utils",
                "./tools"
            ],
            
            # Terminal settings for Clever development
            "terminal.integrated.cwd": "/home/jgallegos1991/Clever",
            "terminal.integrated.defaultProfile.linux": "bash"
        }
        
        return clever_settings
    
    def optimize_clever_workspace(self):
        """Apply Clever-specific optimizations."""
        print("🧠 Optimizing VS Code for Clever development...")
        
        # Get memory-appropriate profile
        available_mb = self.get_memory_mb()
        
        if available_mb < 300:
            base_profile = self.create_emergency_profile()
        elif available_mb < 500:
            base_profile = self.create_conservative_profile()
        else:
            base_profile = self.create_balanced_profile()
        
        # Add Clever-specific settings
        clever_settings = self.create_clever_specific_settings()
        base_profile.update(clever_settings)
        
        # Apply to workspace
        success = self.apply_settings(base_profile, 'workspace')
        
        if success:
            print("✅ Clever workspace optimized for memory constraints")
            return True
        else:
            print("❌ Failed to optimize Clever workspace")
            return False
    
    def get_status(self):
        """Get current VS Code optimization status."""
        available_mb = self.get_memory_mb()
        
        user_settings_exist = self.settings_path.exists()
        workspace_settings_exist = self.workspace_settings_path.exists()
        
        return {
            'available_memory_mb': available_mb,
            'user_settings_configured': user_settings_exist,
            'workspace_settings_configured': workspace_settings_exist,
            'recommended_profile': (
                'emergency' if available_mb < 300 else
                'conservative' if available_mb < 500 else
                'balanced'
            )
        }

def main():
    """Main optimization entry point."""
    print("🔧 VS CODE MEMORY OPTIMIZER")
    print("=" * 40)
    
    optimizer = VSCodeMemoryOptimizer()
    
    # Show current status
    status = optimizer.get_status()
    print(f"Available Memory: {status['available_memory_mb']}MB")
    print(f"Recommended Profile: {status['recommended_profile']}")
    
    # Apply optimizations
    print("\n1. Optimizing VS Code settings...")
    optimizer.optimize_for_current_memory()
    
    print("\n2. Optimizing Clever workspace...")
    optimizer.optimize_clever_workspace()
    
    print("\n✅ VS Code optimization complete!")
    print("📝 Restart VS Code to apply all settings.")

if __name__ == "__main__":
    main()