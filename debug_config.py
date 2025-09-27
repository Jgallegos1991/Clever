import os
import time
"""
Simple Debug Configuration for Clever AI

Why: Provides basic debugging and logging without complex dependencies
Where: Used by app.py and other modules for status messages
How: Simple class-based debugger with print-based logging

Connects to:
    - app.py: `get_debugger()` is used for logging throughout the main application.
    - persona.py: `get_debugger()` is used for logging engine state and performance.
    - memory_engine.py: `get_debugger()` is used for logging memory operations.
    - system_validator.py: `get_debugger()` is used to log the results of validation checks.
    - health_monitor.py: `get_debugger()` is used for logging health status, and `performance_monitor` is used to track the duration of health checks.
    - introspection.py: The `performance_monitor` decorator is used to wrap functions to gather performance data.
    - intelligent_analyzer.py: `get_performance_stats()` and `get_component_health()` are called to provide data for analysis.
"""
from collections import defaultdict, deque
from datetime import datetime
from typing import Dict, Any, Optional

class SimpleDebugger:
    """
    Enhanced debugger for Clever AI with performance analytics
    
    Why: Provides debugging, logging, and performance monitoring that feeds
    into the intelligent analysis system for better insights
    Where: Used throughout application for status tracking and performance analysis
    How: Print-based logging with timestamps, performance tracking, and data collection
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize enhanced debugger with performance tracking
        
        Why: Set up logging and performance monitoring for intelligent analysis
        Where: Called once during app initialization
        How: Configure session ID, performance registries, and analytics
        """
        self.session_id = session_id or f"clever_{int(time.time())}"
        self.debug_level = os.environ.get('CLEVER_DEBUG_LEVEL', 'INFO')
        self.error_count = 0
        
        # Enhanced: Performance tracking for intelligent analysis
        self.performance_data = defaultdict(list)  # function -> [durations]
        self.error_patterns = deque(maxlen=100)    # recent errors for pattern analysis
        self.component_health = {}                 # component -> health metrics
        
    def info(self, component: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        Log info message
        
        Why: Provide status information during operation
        Where: Used throughout application for status updates
        How: Print formatted message with timestamp
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{component}] INFO: {message}")
        if extra:
            print(f"  Extra: {extra}")
            
    def debug(self, component: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message if debug level permits"""
        if self.debug_level == 'DEBUG':
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{component}] DEBUG: {message}")
            if extra:
                print(f"  Extra: {extra}")
    
    def error(self, component: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        Enhanced error logging with pattern tracking
        
        Why: Track errors for debugging and feed into intelligent analysis
        Where: Used in exception handling throughout application
        How: Print error, increment counter, and store for pattern analysis
        """
        self.error_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{component}] ERROR: {message}")
        if extra:
            print(f"  Extra: {extra}")
        
        # Enhanced: Store error for pattern analysis
        self.error_patterns.append({
            'component': component,
            'message': message,
            'timestamp': time.time(),
            'extra': extra
        })
    
    def warning(self, component: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{component}] WARNING: {message}")
        if extra:
            print(f"  Extra: {extra}")
    
    def track_performance(self, component: str, operation: str, duration: float):
        """
        Enhanced performance tracking for intelligent analysis
        
        Why: Monitor operation timing and feed data to intelligent analyzer
        Where: Used in performance-critical operations throughout the app
        How: Log timing and store data for pattern analysis and recommendations
        """
        self.info(component, f"Performance: {operation} took {duration:.3f}s")
        
        # Enhanced: Store performance data for intelligent analysis
        key = f"{component}.{operation}"
        self.performance_data[key].append(duration)
        
        # Keep only recent measurements (last 100) to prevent memory growth
        if len(self.performance_data[key]) > 100:
            self.performance_data[key] = self.performance_data[key][-100:]
        
        # Update component health metrics
        self._update_component_health(component, duration)
    
    def _update_component_health(self, component: str, duration: float):
        """
        Update component health metrics for intelligent analysis
        
        Why: Track component performance trends for health assessment
        Where: Called by track_performance to maintain health data
        How: Calculate and store health metrics based on performance data
        """
        if component not in self.component_health:
            self.component_health[component] = {
                'total_calls': 0,
                'total_duration': 0.0,
                'avg_duration': 0.0,
                'max_duration': 0.0,
                'health_score': 100.0,
                'last_updated': time.time()
            }
        
        health = self.component_health[component]
        health['total_calls'] += 1
        health['total_duration'] += duration
        health['avg_duration'] = health['total_duration'] / health['total_calls']
        health['max_duration'] = max(health['max_duration'], duration)
        health['last_updated'] = time.time()
        
        # Simple health score: penalize slow operations
        if duration > 1.0:  # >1s is considered slow
            health['health_score'] = max(0, health['health_score'] - 5)
        elif duration < 0.1:  # <100ms is good
            health['health_score'] = min(100, health['health_score'] + 1)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for intelligent analysis
        
        Why: Provide performance data to intelligent analyzer for insights
        Where: Called by intelligent_analyzer to correlate performance issues
        How: Return structured performance data with statistics
        """
        stats = {}
        for key, durations in self.performance_data.items():
            if durations:
                import statistics
                stats[key] = {
                    'count': len(durations),
                    'avg': statistics.mean(durations),
                    'max': max(durations),
                    'min': min(durations),
                    'recent': durations[-10:],  # last 10 measurements
                    'std_dev': statistics.stdev(durations) if len(durations) > 1 else 0
                }
        return stats
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """
        Enhanced debug session summary with performance insights
        
        Why: Provide comprehensive overview including performance and health data
        Where: Used by monitoring, health checks, and intelligent analysis
        How: Return dictionary with metrics, performance stats, and component health
        """
        return {
            'session_id': self.session_id,
            'debug_level': self.debug_level,
            'error_count': self.error_count,
            'timestamp': datetime.now().isoformat(),
            'performance_functions_tracked': len(self.performance_data),
            'component_health': self.component_health,
            'error_patterns_count': len(self.error_patterns),
            'total_performance_measurements': sum(len(d) for d in self.performance_data.values())
        }

# Simple performance monitor decorator
def performance_monitor(component: str):
    """
    Decorator for performance monitoring
    
    Why: Track execution time of critical functions
    Where: Applied to functions that need timing analysis
    How: Wrapper that measures and logs execution duration
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                debugger = get_debugger()
                debugger.track_performance(component, func.__name__, duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                debugger = get_debugger()
                debugger.error(component, f"Error in {func.__name__}: {str(e)}")
                debugger.track_performance(component, f"{func.__name__}_error", duration)
                raise
        return wrapper
    return decorator

# Global debugger instance
_debugger = None

# Global performance monitoring registry
class PerformanceRegistry:
    """
    Global registry for performance monitoring data
    
    Why: Centralize performance data collection for intelligent analysis
    Where: Accessed by intelligent_analyzer and debug tools
    How: Singleton pattern with thread-safe data collection
    """
    
    def __init__(self):
        self._stats = {}
        self._lock = None  # Will be set when needed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all performance statistics."""
        debugger = get_debugger()
        return debugger.get_performance_stats()
    
    def get_component_health(self) -> Dict[str, Any]:
        """Get component health metrics."""
        debugger = get_debugger()
        return debugger.component_health

# Global registry instance
performance_monitor_registry = PerformanceRegistry()

def get_debugger() -> SimpleDebugger:
    """
    Get global debugger instance
    
    Why: Provide singleton access to debugger across application
    Where: Used by all modules needing debugging capabilities
    How: Create or return existing debugger instance
    
    Connects to:
        - app.py: Main application debugging
        - All modules: Universal debugging access
    """
    global _debugger
    if _debugger is None:
        _debugger = SimpleDebugger()
    return _debugger

def reset_debugger():
    """
    Reset global debugger instance
    
    Why: Allow clean state for testing and reinitialization
    Where: Used in test cases and system restarts
    How: Clear global debugger variable
    """
    global _debugger
    _debugger = None