"""
Simple Debug Configuration for Clever AI

Why: Provides basic debugging and logging without complex dependencies
Where: Used by app.py and other modules for status messages
How: Simple class-based debugger with print-based logging

Connects to:
    - app.py: Main application logging
    - system_validator.py: Validation logging
"""
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional


class SimpleDebugger:
    """
    Simple debugger for Clever AI
    
    Why: Provides basic logging without external dependencies
    Where: Used throughout application for status tracking
    How: Print-based logging with timestamps and component tags
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize simple debugger
        
        Why: Set up basic logging configuration
        Where: Called once during app initialization
        How: Configure session ID and basic settings
        """
        self.session_id = session_id or f"clever_{int(time.time())}"
        self.debug_level = os.environ.get('CLEVER_DEBUG_LEVEL', 'INFO')
        self.error_count = 0
        
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
        Log error message
        
        Why: Track errors for debugging and monitoring
        Where: Used in exception handling throughout application
        How: Print error with timestamp and increment counter
        """
        self.error_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{component}] ERROR: {message}")
        if extra:
            print(f"  Extra: {extra}")
    
    def warning(self, component: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{component}] WARNING: {message}")
        if extra:
            print(f"  Extra: {extra}")
    
    def track_performance(self, component: str, operation: str, duration: float):
        """
        Track performance metrics
        
        Why: Monitor operation timing for optimization
        Where: Used in performance-critical operations
        How: Log timing information with component context
        """
        self.info(component, f"Performance: {operation} took {duration:.3f}s")
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """
        Get current debug session summary
        
        Why: Provide overview of debugging session status
        Where: Used by monitoring and health check systems
        How: Return dictionary with key metrics
        """
        return {
            'session_id': self.session_id,
            'debug_level': self.debug_level,
            'error_count': self.error_count,
            'timestamp': datetime.now().isoformat()
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