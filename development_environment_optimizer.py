import time
#!/usr/bin/env python3
"""
development_environment_optimizer.py - Chromebook Development Environment Memory Optimizer

Why: Optimizes the entire development ecosystem (Clever + VS Code + Pylance + GitHub Copilot)
     for Chromebook memory constraints, ensuring smooth development experience while maintaining
     Clever's cognitive capabilities and your AI assistant performance.

Where: Integrates with Clever's memory optimization, VS Code settings, and system monitoring
       to create a harmonious development environment that respects hardware limitations.

How: Monitors system memory pressure and dynamically adjusts settings for all components:
     - VS Code memory limits and feature optimization
     - Pylance type checking and analysis settings  
     - GitHub Copilot suggestion frequency
     - Clever's processing modes and cache sizes
     - File watching and indexing limits

File Usage:
    - Primary callers: Clever's cognitive sovereignty engine, VS Code workspace settings
    - System integration: Memory monitoring, process management, configuration updates
    - Configuration targets: VS Code settings.json, Pylance config, Clever parameters
    - Performance monitoring: Real-time memory tracking and pressure detection
    - Automatic optimization: Dynamic adjustment based on memory availability

Connects to:
    - memory_optimized_code_intelligence.py: Clever's memory-conscious processing
    - cognitive_sovereignty.py: System awareness and adaptive behavior
    - .vscode/settings.json: VS Code memory and performance configuration
    - VS Code extensions: Pylance, GitHub Copilot memory optimization
    - system monitoring: Real-time memory pressure detection and response
"""

import psutil
from dataclasses import dataclass

@dataclass
class MemoryProfile:
    """System memory profile for optimization decisions."""
    total_mb: float
    available_mb: float
    used_percent: float
    pressure_level: str  # 'low', 'medium', 'high', 'critical'
    vscode_memory_mb: float
    pylance_memory_mb: float
    clever_memory_mb: float

@dataclass
class OptimizationSettings:
    """Optimized settings for development environment."""
    vscode_memory_limit_mb: int
    pylance_type_checking: str  # 'o', 'basic', 'strict'
    copilot_suggestions: bool
    clever_processing_mode: str  # 'minimal', 'conservative', 'standard'
    file_watching_enabled: bool
    intellisense_max_files: int
    cache_limits: Dict[str, int]

class DevelopmentEnvironmentOptimizer:
    """
    Comprehensive memory optimizer for Chromebook development environment.
    
    Manages memory usage across all development tools to maintain performance
    while respecting hardware constraints.
    """
    
    def __init__(self, workspace_path: str = "/home/jgallegos1991/Clever"):
        """
        Initialize development environment optimizer.
        
        Why: Sets up comprehensive memory monitoring and optimization for entire dev stack
        Where: Called during system startup or when memory pressure is detected
        How: Initializes monitoring systems and baseline configurations
        
        Args:
            workspace_path: Path to Clever workspace for configuration
        """
        self.workspace_path = Path(workspace_path)
        self.vscode_settings_path = self.workspace_path / ".vscode" / "settings.json"
        self.baseline_memory = self._get_memory_baseline()
        
        # Optimization profiles for different memory situations
        self.optimization_profiles = {
            'critical': OptimizationSettings(
                vscode_memory_limit_mb=200,
                pylance_type_checking='o',
                copilot_suggestions=False,
                clever_processing_mode='minimal',
                file_watching_enabled=False,
                intellisense_max_files=50,
                cache_limits={'analysis': 5, 'completions': 10, 'symbols': 100}
            ),
            'high': OptimizationSettings(
                vscode_memory_limit_mb=300,
                pylance_type_checking='basic',
                copilot_suggestions=True,
                clever_processing_mode='conservative',
                file_watching_enabled=True,
                intellisense_max_files=100,
                cache_limits={'analysis': 10, 'completions': 20, 'symbols': 200}
            ),
            'medium': OptimizationSettings(
                vscode_memory_limit_mb=500,
                pylance_type_checking='basic',
                copilot_suggestions=True,
                clever_processing_mode='standard',
                file_watching_enabled=True,
                intellisense_max_files=200,
                cache_limits={'analysis': 20, 'completions': 50, 'symbols': 500}
            ),
            'low': OptimizationSettings(
                vscode_memory_limit_mb=800,
                pylance_type_checking='strict',
                copilot_suggestions=True,
                clever_processing_mode='standard',
                file_watching_enabled=True,
                intellisense_max_files=500,
                cache_limits={'analysis': 50, 'completions': 100, 'symbols': 1000}
            )
        }
    
    def get_current_memory_profile(self) -> MemoryProfile:
        """
        Get current system memory profile for optimization decisions.
        
        Why: Provides real-time memory analysis for dynamic optimization
        Where: Called continuously to monitor memory pressure
        How: Uses psutil to analyze system and process memory usage
        
        Returns:
            MemoryProfile with current memory state and pressure level
        """
        memory = psutil.virtual_memory()
        
        # Get VS Code and related process memory usage
        vscode_memory = 0
        pylance_memory = 0
        clever_memory = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
            try:
                if proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    
                    if 'code' in proc.info['name'] or '/usr/share/code/code' in cmdline:
                        vscode_memory += memory_mb
                    elif 'pylance' in cmdline or 'ms-python.vscode-pylance' in cmdline:
                        pylance_memory += memory_mb
                    elif 'flask' in cmdline and 'Clever' in cmdline:
                        clever_memory += memory_mb
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Determine pressure level
        available_mb = memory.available / (1024 * 1024)
        if available_mb < 200:
            pressure_level = 'critical'
        elif available_mb < 400:
            pressure_level = 'high'
        elif available_mb < 800:
            pressure_level = 'medium'
        else:
            pressure_level = 'low'
        
        return MemoryProfile(
            total_mb=memory.total / (1024 * 1024),
            available_mb=available_mb,
            used_percent=memory.percent,
            pressure_level=pressure_level,
            vscode_memory_mb=vscode_memory,
            pylance_memory_mb=pylance_memory,
            clever_memory_mb=clever_memory
        )
    
    def optimize_vscode_settings(self, profile: MemoryProfile) -> Dict[str, Any]:
        """
        Optimize VS Code settings based on memory profile.
        
        Why: Adjusts VS Code memory usage and features based on available resources
        Where: Called when memory pressure changes to adapt VS Code behavior
        How: Generates optimized VS Code settings.json configuration
        
        Args:
            profile: Current memory profile
            
        Returns:
            Dict with optimized VS Code settings
        """
        settings = self.optimization_profiles[profile.pressure_level]
        
        vscode_config = {
            # Memory and performance optimization
            "files.watcherExclude": {
                "**/.git/objects/**": True,
                "**/.git/subtree-cache/**": True,
                "**/node_modules/*/**": True,
                "**/.hg/store/**": True,
                "**/__pycache__/**": True,
                "**/.venv/**": True if profile.pressure_level in ['critical', 'high'] else False,
                "**/logs/**": True,
                "**/backup*/**": True
            },
            
            # Python/Pylance optimization
            "python.analysis.typeCheckingMode": settings.pylance_type_checking,
            "python.analysis.autoImportCompletions": profile.pressure_level not in ['critical'],
            "python.analysis.indexing": profile.pressure_level not in ['critical', 'high'],
            "python.analysis.packageIndexDepths": [
                {"name": "", "depth": 1 if profile.pressure_level == 'critical' else 2}
            ],
            
            # IntelliSense optimization  
            "python.analysis.memory.keepLibraryAst": profile.pressure_level == 'low',
            "python.analysis.diagnosticMode": "workspace" if profile.pressure_level == 'low' else "openFilesOnly",
            
            # GitHub Copilot optimization
            "github.copilot.enable": {
                "*": settings.copilot_suggestions,
                "yaml": False,
                "plaintext": False,
                "markdown": profile.pressure_level == 'low'
            },
            
            # Editor optimization
            "editor.minimap.enabled": profile.pressure_level not in ['critical', 'high'],
            "editor.suggest.maxVisibleSuggestions": 5 if profile.pressure_level == 'critical' else 10,
            "editor.hover.enabled": profile.pressure_level != 'critical',
            "editor.parameterHints.enabled": profile.pressure_level not in ['critical'],
            
            # File handling optimization
            "files.maxMemoryForLargeFilesMB": 16 if profile.pressure_level == 'critical' else 32,
            "search.maxResults": 100 if profile.pressure_level == 'critical' else 1000,
            
            # Extension optimization
            "extensions.autoCheckUpdates": False,
            "extensions.autoUpdate": False,
            
            # Terminal optimization
            "terminal.integrated.enablePersistentSessions": profile.pressure_level == 'low',
            "terminal.integrated.rightClickBehavior": "nothing" if profile.pressure_level == 'critical' else "default",
            
            # Workbench optimization
            "workbench.editor.limit.enabled": True,
            "workbench.editor.limit.value": 3 if profile.pressure_level == 'critical' else 8,
            "workbench.settings.enableNaturalLanguageSearch": False,
            
            # Clever-specific optimizations
            "clever.memoryOptimization": {
                "enabled": True,
                "processingMode": settings.clever_processing_mode,
                "cacheLimits": settings.cache_limits,
                "pressureLevel": profile.pressure_level
            }
        }
        
        return vscode_config
    
    def apply_optimizations(self, profile: Optional[MemoryProfile] = None) -> Dict[str, Any]:
        """
        Apply memory optimizations to the entire development environment.
        
        Why: Implements system-wide memory optimizations for smooth development
        Where: Called when memory pressure is detected or periodically
        How: Updates configurations for all development tools
        
        Args:
            profile: Memory profile, will detect current if not provided
            
        Returns:
            Dict with optimization results and applied settings
        """
        if profile is None:
            profile = self.get_current_memory_profile()
        
        # Apply VS Code optimizations
        vscode_settings = self.optimize_vscode_settings(profile)
        
        # Ensure .vscode directory exists
        vscode_dir = self.workspace_path / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        # Update VS Code settings
        existing_settings = {}
        if self.vscode_settings_path.exists():
            try:
                existing_settings = json.loads(self.vscode_settings_path.read_text())
            except json.JSONDecodeError:
                existing_settings = {}
        
        # Merge optimizations with existing settings
        merged_settings = {**existing_settings, **vscode_settings}
        
        # Write optimized settings
        self.vscode_settings_path.write_text(
            json.dumps(merged_settings, indent=2)
        )
        
        # Apply Clever memory optimizations
        clever_optimizations = self._optimize_clever_memory(profile)
        
        return {
            'success': True,
            'memory_profile': {
                'pressure_level': profile.pressure_level,
                'available_mb': profile.available_mb,
                'used_percent': profile.used_percent,
                'vscode_memory_mb': profile.vscode_memory_mb,
                'pylance_memory_mb': profile.pylance_memory_mb,
                'clever_memory_mb': profile.clever_memory_mb
            },
            'optimizations_applied': {
                'vscode_settings_updated': True,
                'clever_memory_optimized': clever_optimizations,
                'pressure_response': self.optimization_profiles[profile.pressure_level].__dict__
            },
            'recommendations': self._generate_user_recommendations(profile)
        }
    
    def _optimize_clever_memory(self, profile: MemoryProfile) -> Dict[str, Any]:
        """
        Optimize Clever's memory usage based on system pressure.
        
        Why: Ensures Clever adapts her processing to available system resources
        Where: Called as part of system-wide memory optimization
        How: Adjusts Clever's internal memory limits and processing modes
        
        Args:
            profile: Current memory profile
            
        Returns:
            Dict with Clever optimization results
        """
        try:
            # Import Clever's memory optimization system
            from memory_optimized_code_intelligence import get_memory_optimized_code_intelligence
            
            code_intel = get_memory_optimized_code_intelligence()
            
            # Clear caches if memory pressure is high
            if profile.pressure_level in ['critical', 'high']:
                code_intel.clear_cache()
            
            # Update system constraints based on current profile
            code_intel.system_constraints.update({
                'memory_pressure_level': profile.pressure_level,
                'available_memory_mb': profile.available_mb,
                'processing_strategy': 'minimal' if profile.pressure_level == 'critical' else 'conservative',
                'batch_size': 1 if profile.pressure_level == 'critical' else 2,
                'cache_limit': 3 if profile.pressure_level == 'critical' else 10
            })
            
            return {
                'cache_cleared': profile.pressure_level in ['critical', 'high'],
                'processing_mode': code_intel.system_constraints['processing_strategy'],
                'memory_constraints_updated': True
            }
            
        except ImportError:
            return {'error': 'Clever memory optimization not available'}
    
    def _generate_user_recommendations(self, profile: MemoryProfile) -> List[str]:
        """Generate user-friendly recommendations based on memory profile."""
        recommendations = []
        
        if profile.pressure_level == 'critical':
            recommendations.extend([
                "🚨 Critical memory pressure detected - some features disabled",
                "💡 Close unused browser tabs and applications",
                "⚡ Restart VS Code if performance degrades",
                "🧠 Clever is in minimal processing mode"
            ])
        elif profile.pressure_level == 'high':
            recommendations.extend([
                "⚠️ High memory usage - performance optimizations active", 
                "🔧 VS Code features reduced for better performance",
                "🧠 Clever using conservative processing mode",
                "💾 Consider closing large files if not needed"
            ])
        elif profile.pressure_level == 'medium':
            recommendations.extend([
                "✅ Memory usage manageable with optimizations",
                "🚀 Most features available with performance tuning",
                "🧠 Clever operating in standard mode with limits"
            ])
        else:
            recommendations.extend([
                "🎉 Low memory pressure - full features available",
                "🚀 Optimal performance configuration active",
                "🧠 Clever operating at full capability"
            ])
        
        return recommendations
    
    def _get_memory_baseline(self) -> Dict[str, float]:
        """Get baseline memory measurements for comparison."""
        memory = psutil.virtual_memory()
        return {
            'total_mb': memory.total / (1024 * 1024),
            'baseline_timestamp': time.time()
        }
    
    def start_monitoring(self, check_interval: int = 30) -> None:
        """
        Start continuous memory monitoring and optimization.
        
        Why: Provides proactive memory management for development environment
        Where: Called to start background monitoring process
        How: Periodically checks memory and applies optimizations as needed
        
        Args:
            check_interval: Seconds between memory checks
        """
        print(f"🔍 Starting development environment memory monitoring (every {check_interval}s)")
        
        last_pressure_level = None
        
        while True:
            try:
                profile = self.get_current_memory_profile()
                
                # Apply optimizations if pressure level changed
                if profile.pressure_level != last_pressure_level:
                    print(f"📊 Memory pressure: {profile.pressure_level} ({profile.available_mb:.0f}MB available)")
                    
                    optimizations = self.apply_optimizations(profile)
                    
                    if optimizations['success']:
                        print(f"⚙️ Applied {profile.pressure_level} pressure optimizations")
                        for rec in optimizations['recommendations'][:2]:  # Show first 2 recommendations
                            print(f"   {rec}")
                    
                    last_pressure_level = profile.pressure_level
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n👋 Memory monitoring stopped")
                break
            except Exception:
                print(f"❌ Monitoring error: {e}")
                time.sleep(check_interval)

# Singleton instance
_dev_env_optimizer = None

def get_development_environment_optimizer():
    """
    Get the global development environment optimizer instance.
    
    Why: Provides singleton access to memory optimization across the system
    Where: Called by Clever's cognitive sovereignty and monitoring systems  
    How: Creates and caches single optimizer instance
    
    Returns:
        DevelopmentEnvironmentOptimizer: Global optimizer instance
    """
    global _dev_env_optimizer
    
    if _dev_env_optimizer is None:
        _dev_env_optimizer = DevelopmentEnvironmentOptimizer()
    
    return _dev_env_optimizer

if __name__ == "__main__":
    # CLI interface for manual optimization
    
    optimizer = get_development_environment_optimizer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        optimizer.start_monitoring()
    else:
        print("🔧 Applying development environment optimizations...")
        result = optimizer.apply_optimizations()
        
        if result['success']:
            profile = result['memory_profile']
            print(f"✅ Optimizations applied for {profile['pressure_level']} memory pressure")
            print(f"💾 Available memory: {profile['available_mb']:.0f}MB")
            print(f"📊 Memory usage: {profile['used_percent']:.1f}%")
            print(f"🔧 VS Code: {profile['vscode_memory_mb']:.0f}MB")
            print(f"🐍 Pylance: {profile['pylance_memory_mb']:.0f}MB") 
            print(f"🧠 Clever: {profile['clever_memory_mb']:.0f}MB")
            
            print("\n💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"   {rec}")
        else:
            print("❌ Optimization failed")
            sys.exit(1)