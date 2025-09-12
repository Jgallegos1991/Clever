"""
Debug Configuration - Comprehensive debugging and logging system for Clever AI

# Project Coding Instructions:
# See .github/copilot-instructions.md for architecture, documentation, and workflow rules.
# All code must follow these standards.

Why: Provides centralized debugging, logging, and performance monitoring
capabilities to enable effective troubleshooting, performance analysis,
and system health monitoring across all Clever components.
Where: Used by all modules for logging, debugging, and performance tracking
with centralized configuration and structured output management.
How: Implements comprehensive logging system with session tracking, performance
monitoring, error reporting, and debug flag management for system observability.

Connects to:
    - app.py: Main application debugging and performance monitoring
    - evolution_engine.py: Learning process debugging and metrics
    - nlp_processor.py: NLP processing performance and error tracking
    - database.py: Database operation monitoring and error reporting
    - All modules: Centralized logging and debugging infrastructure
"""

import os
import sys
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
import json
from functools import wraps


class CleverDebugger:
    """
    Enhanced debugging system for Clever AI with comprehensive monitoring

    Why: Provides centralized debugging infrastructure to enable effective
    troubleshooting, performance analysis, and system health monitoring
    across all Clever components with structured logging and metrics.
    Where: Instantiated once and used throughout the application for consistent
    logging, performance tracking, and error reporting across all modules.
    How: Implements structured logging with session tracking, performance
    monitoring, debug flags, and comprehensive error reporting capabilities.
    """

    def __init__(self, debug_level: str = "INFO"):
        """
        Initialize the debugging system

        Why: Sets up comprehensive debugging infrastructure with logging,
        performance tracking, and error monitoring to enable effective
        system observability and troubleshooting capabilities.
        Where: Called once during application startup to establish debugging
        infrastructure used throughout the application lifecycle.
        How: Creates logging directory, configures logging system, initializes
        debug flags and performance tracking with session identification.

        Args:
            debug_level: Logging level for debug output control

        Connects to:
            - File system: Creates logs directory for debug output
            - All modules: Provides debugging infrastructure
        """
        self.debug_level = debug_level
        self.debug_dir = "./logs"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ensure debug directory exists
        os.makedirs(self.debug_dir, exist_ok=True)

        # Setup logging
        self.setup_logging()

        # Debug flags
        self.debug_flags = {
            "evolution_engine": True,
            "nlp_processing": True,
            "persona_responses": True,
            "file_ingestion": True,
            "knowledge_base": True,
            "ui_interactions": True,
            "performance_metrics": True,
        }

        # Performance tracking
        self.performance_metrics = {}
        self.error_count = 0
        self.warning_count = 0

    def setup_logging(self):
        """
        Setup comprehensive logging system

        Why: Creates structured logging infrastructure with file output and
        console output to enable effective debugging and system monitoring
        with proper log rotation and formatting.
        Where: Called during debugger initialization to establish logging
        infrastructure used throughout the application for debug output.
        How: Configures Python logging with file handlers, formatters,
        and log levels for comprehensive debug information capture.

        Connects to:
            - File system: Creates log files for persistent debug storage
            - Console: Provides real-time debug output during development
        """

        # Main application logger
        self.logger = logging.getLogger("clever_ai")
        self.logger.setLevel(getattr(logging, self.debug_level.upper()))

        # Clear existing handlers
        self.logger.handlers = []

        # Console handler with color coding
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for all logs
        file_handler = logging.FileHandler(
            os.path.join(self.debug_dir, f"clever_debug_{self.session_id}.log")
        )
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Error-only handler
        error_handler = logging.FileHandler(
            os.path.join(
                self.debug_dir, f"clever_errors_{self.session_id}.log"
            )
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)

        # Performance metrics handler
        self.perf_logger = logging.getLogger("clever_performance")
        perf_handler = logging.FileHandler(
            os.path.join(
                self.debug_dir, f"clever_performance_{self.session_id}.log"
            )
        )
        perf_formatter = logging.Formatter("%(asctime)s | %(message)s")
        perf_handler.setFormatter(perf_formatter)
        self.perf_logger.addHandler(perf_handler)
        self.perf_logger.setLevel(logging.INFO)

        self.logger.info("🐛 Clever AI Debug System Initialized")
        self.logger.info(f"Session ID: {self.session_id}")
        self.logger.info(f"Debug Level: {self.debug_level}")

    def debug(self, component: str, message: str, data: Optional[Dict] = None):
        """Log debug message for specific component"""
        if self.debug_flags.get(component, False):
            log_msg = f"[{component.upper()}] {message}"
            if data:
                log_msg += f" | Data: {json.dumps(data, default=str)[:200]}"
            self.logger.debug(log_msg)

    def info(self, component: str, message: str, data: Optional[Dict] = None):
        """Log info message"""
        log_msg = f"[{component.upper()}] {message}"
        if data:
            log_msg += f" | {json.dumps(data, default=str)[:200]}"
        self.logger.info(log_msg)

    def warning(
        self, component: str, message: str, data: Optional[Dict] = None
    ):
        """Log warning message"""
        self.warning_count += 1
        log_msg = f"[{component.upper()}] {message}"
        if data:
            log_msg += f" | {json.dumps(data, default=str)[:200]}"
        self.logger.warning(log_msg)

    def error(
        self,
        component: str,
        message: str,
        error: Optional[Exception] = None,
        data: Optional[Dict] = None,
    ):
        """Log error with full traceback"""
        self.error_count += 1
        log_msg = f"[{component.upper()}] {message}"

        if data:
            log_msg += f" | Data: {json.dumps(data, default=str)[:200]}"

        if error:
            log_msg += f" | Error: {str(error)}"
            self.logger.error(log_msg)
            self.logger.error(f"Traceback: {traceback.format_exc()}")
        else:
            self.logger.error(log_msg)

    def track_performance(
        self,
        component: str,
        operation: str,
        duration: float,
        metadata: Optional[Dict] = None,
    ):
        """Track performance metrics"""
        metric_key = f"{component}_{operation}"

        if metric_key not in self.performance_metrics:
            self.performance_metrics[metric_key] = {
                "total_calls": 0,
                "total_time": 0.0,
                "avg_time": 0.0,
                "min_time": float("inf"),
                "max_time": 0.0,
            }

        metrics = self.performance_metrics[metric_key]
        metrics["total_calls"] += 1
        metrics["total_time"] += duration
        metrics["avg_time"] = metrics["total_time"] / metrics["total_calls"]
        metrics["min_time"] = min(metrics["min_time"], duration)
        metrics["max_time"] = max(metrics["max_time"], duration)

        # Log performance
        perf_msg = f"{component}.{operation} | {duration:.4f}s | avg: {metrics['avg_time']:.4f}s"
        if metadata:
            perf_msg += f" | {json.dumps(metadata, default=str)[:100]}"

        self.perf_logger.info(perf_msg)

    def get_debug_summary(self) -> Dict[str, Any]:
        """Get current debug session summary"""
        return {
            "session_id": self.session_id,
            "debug_level": self.debug_level,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "performance_metrics": self.performance_metrics,
            "debug_flags": self.debug_flags,
            "log_files": {
                "main": f"clever_debug_{self.session_id}.log",
                "errors": f"clever_errors_{self.session_id}.log",
                "performance": f"clever_performance_{self.session_id}.log",
            },
        }

    def export_debug_report(self) -> str:
        """Export comprehensive debug report"""
        report_path = os.path.join(
            self.debug_dir, f"debug_report_{self.session_id}.json"
        )

        report = {
            "timestamp": datetime.now().isoformat(),
            "session_info": self.get_debug_summary(),
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": os.getcwd(),
            },
        }

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)

        self.info("debug_system", f"Debug report exported to {report_path}")
        return report_path


# Global debugger instance
_debugger = None


def get_debugger() -> CleverDebugger:
    """Get global debugger instance"""
    global _debugger
    if _debugger is None:
        debug_level = os.environ.get("CLEVER_DEBUG_LEVEL", "INFO")
        _debugger = CleverDebugger(debug_level)
    return _debugger


def debug_method(component: str):
    """Decorator for debugging method calls"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            debugger = get_debugger()
            start_time = datetime.now()

            try:
                # Log method entry
                debugger.debug(
                    component,
                    f"Entering {func.__name__}",
                    {"args_count": len(args), "kwargs": list(kwargs.keys())},
                )

                # Execute function
                result = func(*args, **kwargs)

                # Calculate duration
                duration = (datetime.now() - start_time).total_seconds()

                # Log success
                debugger.debug(
                    component,
                    f"Completed {func.__name__}",
                    {
                        "duration": f"{duration:.4f}s",
                        "result_type": type(result).__name__,
                    },
                )

                # Track performance
                debugger.track_performance(component, func.__name__, duration)

                return result

            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()

                # Log error
                debugger.error(
                    component,
                    f"Error in {func.__name__}",
                    e,
                    {
                        "duration": f"{duration:.4f}s",
                        "args_count": len(args),
                        "kwargs": list(kwargs.keys()),
                    },
                )

                raise

        return wrapper

    return decorator


def performance_monitor(component: str):
    """Decorator for monitoring function performance"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            debugger = get_debugger()
            start_time = datetime.now()

            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()

                # Track performance
                debugger.track_performance(
                    component,
                    func.__name__,
                    duration,
                    {"success": True, "result_type": type(result).__name__},
                )

                return result

            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()

                # Track failed performance
                debugger.track_performance(
                    component,
                    func.__name__,
                    duration,
                    {"success": False, "error": str(e)},
                )

                raise

        return wrapper

    return decorator


def debug_context(component: str, operation: str):
    """Context manager for debugging operations"""

    class DebugContext:
        def __init__(self):
            self.debugger = get_debugger()
            self.start_time = None

        def __enter__(self):
            self.start_time = datetime.now()
            self.debugger.debug(component, f"Starting {operation}")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            duration = (datetime.now() - self.start_time).total_seconds()

            if exc_type is None:
                self.debugger.debug(
                    component,
                    f"Completed {operation}",
                    {"duration": f"{duration:.4f}s"},
                )
                self.debugger.track_performance(component, operation, duration)
            else:
                self.debugger.error(
                    component,
                    f"Error in {operation}",
                    exc_val,
                    {"duration": f"{duration:.4f}s"},
                )

    return DebugContext()


# Convenience functions
def debug_log(component: str, message: str, data: Optional[Dict] = None):
    """Quick debug logging"""
    get_debugger().debug(component, message, data)


def info_log(component: str, message: str, data: Optional[Dict] = None):
    """Quick info logging"""
    get_debugger().info(component, message, data)


def error_log(
    component: str,
    message: str,
    error: Optional[Exception] = None,
    data: Optional[Dict] = None,
):
    """Quick error logging"""
    get_debugger().error(component, message, error, data)


def warning_log(component: str, message: str, data: Optional[Dict] = None):
    """Quick warning logging"""
    get_debugger().warning(component, message, data)
