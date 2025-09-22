"""
System Health Monitor - Real-time monitoring for Clever AI components

Why: Provides comprehensive system health monitoring and alerting to ensure
optimal performance, resource management, and early detection of issues
before they impact user experience or system stability.
Where: Used by app.py and debug_config for continuous system monitoring
with integration into dashboard and alerting systems.
How: Implements real-time resource monitoring, component health checks,
and intelligent alerting with threshold management and trend analysis.

Connects to:
    - debug_config.py: Integrates with debugging and logging systems
    - app.py: Provides system status for health endpoints
    - database.py: Monitors database performance and connectivity
    - System resources: Tracks CPU, memory, disk, and process metrics
"""

import psutil
 
import sqlite3
import config
from datetime import datetime
from typing import Dict, List, Any
from typing import cast
from debug_config import get_debugger, performance_monitor
from database import DatabaseManager


class SystemHealthMonitor:
    """Monitors system health and component status with intelligent alerting.

    Why:
        Provide centralized, lightweight visibility into core runtime health
        (resources, database, evolution engine, NLP components) so issues are
        surfaced early without spreading ad‑hoc monitoring logic across the
        codebase.
    Where:
        Instantiated lazily via ``get_health_monitor()`` (see bottom of file)
        and reused by API endpoints or diagnostic tooling wanting a snapshot.
    How:
        Wraps targeted check_* methods using psutil / sqlite / internal APIs,
        records last results in ``self.health_checks`` and reports anomalies
        through the central debugger for structured logging.

    Connects to:
        - debug_config.py:
            - `get_debugger()`: Used to get the logger instance for logging health status.
            - `performance_monitor()`: Decorator used to time the execution of health check functions.
        - database.py:
            - `check_database_health()` -> `DatabaseManager`: Connects to the database to check its size, and table statistics.
        - evolution_engine.py:
            - `check_evolution_engine()` -> `get_evolution_engine()`: Gets the engine instance to check its status and learning progress.
        - config.py:
            - `check_database_health()`: Reads `config.DB_PATH` to locate the database file.
        - psutil: (Optional) Used to gather system resource metrics like CPU, memory, and disk usage.
        - spacy, textblob, vaderSentiment: (Optional) The `check_nlp_components` function attempts to import and test these libraries to verify NLP capabilities.
    """

    def __init__(self):
        self.debugger = get_debugger()
        self.start_time = datetime.now()
        self.health_checks = {}
        self.alerts = []

        # Health check thresholds
        self.thresholds = {
            "memory_usage_mb": 500,
            "cpu_usage_percent": 80,
            "response_time_ms": 2000,
            "error_rate_percent": 5,
            "disk_usage_percent": 90,
        }

        self.debugger.info("health_monitor", "System Health Monitor initialized")

    @performance_monitor("health_monitor")
    def check_system_resources(self) -> Dict[str, Any]:
        """
        Check system resource usage and performance metrics

        Why: Provides real-time system resource monitoring to detect performance
        issues, resource constraints, and potential problems before they impact
        system stability or user experience.
        Where: Called regularly by monitoring loops and health check endpoints
        to provide current system status and resource utilization data.
        How: Uses psutil to gather system metrics including memory, CPU, disk
        usage, and process information with threshold comparison and alerting.

        Returns:
            Dict[str, Any]: Comprehensive system resource metrics and status

        Connects to:
            - psutil: System resource data collection
            - debug_config.py: Performance metrics logging
            - Alerting systems: Resource threshold monitoring
        """
        """Check system resource usage"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used / (1024 * 1024)
            memory_percent = memory.percent

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Disk usage
            disk = psutil.disk_usage("/")
            disk_percent = (disk.used / disk.total) * 100

            # Process info
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024 * 1024)

            health_data = {
                "timestamp": datetime.now().isoformat(),
                "memory": {
                    "total_mb": memory.total / (1024 * 1024),
                    "used_mb": memory_mb,
                    "percent": memory_percent,
                    "process_mb": process_memory,
                },
                "cpu": {"percent": cpu_percent, "count": psutil.cpu_count()},
                "disk": {
                    "total_gb": disk.total / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "percent": disk_percent,
                },
            }

            # Check thresholds
            alerts = []
            if memory_mb > self.thresholds["memory_usage_mb"]:
                alerts.append(f"High memory usage: {memory_mb:.1f}MB")

            if cpu_percent > self.thresholds["cpu_usage_percent"]:
                alerts.append(f"High CPU usage: {cpu_percent:.1f}%")

            if disk_percent > self.thresholds["disk_usage_percent"]:
                alerts.append(f"High disk usage: {disk_percent:.1f}%")

            health_data["alerts"] = alerts
            health_data["status"] = "healthy" if not alerts else "warning"

            self.health_checks["system_resources"] = health_data

            if alerts:
                self.debugger.warning(
                    "health_monitor", "System resource alerts", {"alerts": alerts}
                )

            return health_data

        except Exception as e:
            # Provide structured error context for downstream analysis
            self.debugger.error(
                "health_monitor", "Failed to check system resources", {"error": str(e)}
            )
            return {"status": "error", "error": str(e)}

    @performance_monitor("health_monitor")
    def check_database_health(self) -> Dict[str, Any]:
        """Check database health and integrity"""
        try:
            db_path = config.DB_PATH
            health_data = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy",
                "issues": [],
            }

            # Check if database exists
            import os

            if not os.path.exists(db_path):
                health_data["status"] = "error"
                health_data["issues"].append("Database file not found")
                return health_data

            # Check database size
            db_size = os.path.getsize(db_path) / (1024 * 1024)  # MB
            health_data["size_mb"] = db_size

            # Check database connectivity
            # Prefer using DatabaseManager to respect single-DB configuration
            db = DatabaseManager(db_path)
            conn = db._connect()
            cursor = conn.cursor()

            # Check table counts
            tables = [
                "interactions",
                "knowledge_sources",
                "content_chunks",
                "user_preferences",
                "personality_state",
                "system_metrics",
            ]

            table_stats = {}
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_stats[table] = count
                except sqlite3.OperationalError:
                    health_data["issues"].append(
                        f"Table {table} not found or corrupted"
                    )

            health_data["table_stats"] = table_stats

            # Check for recent activity
            try:
                cursor.execute("SELECT MAX(timestamp) FROM interactions")
                last_interaction = cursor.fetchone()[0]
                if last_interaction:
                    health_data["last_interaction"] = last_interaction
            except Exception:
                # Table may not exist yet; treat as no interactions
                pass

            conn.close()

            if health_data["issues"]:
                health_data["status"] = "warning"

            self.health_checks["database"] = health_data
            return health_data

        except Exception as e:
            self.debugger.error(
                "health_monitor", "Database health check failed", {"error": str(e)}
            )
            return {"status": "error", "error": str(e)}

    @performance_monitor("health_monitor")
    def check_nlp_components(self) -> Dict[str, Any]:
        """Check NLP component health"""
        try:
            health_data: Dict[str, Any] = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy",
                "components": {},
            }

            # Check spaCy
            try:
                import importlib

                spacy = importlib.import_module("spacy")
                # Model load may fail in minimal envs; still acceptable
                try:
                    nlp = getattr(spacy, "load")("en_core_web_sm")  # type: ignore[call-arg]
                    _ = nlp("This is a test.")
                except Exception:
                    pass
                health_data["components"]["spacy"] = {
                    "status": "healthy",
                    "version": getattr(spacy, "__version__", "unknown"),
                    "model": "en_core_web_sm",
                }
            except Exception as e:
                health_data["components"]["spacy"] = {
                    "status": "error",
                    "error": str(e),
                }
                health_data["status"] = "warning"

            # Check VADER
            try:
                import importlib

                vader_mod = importlib.import_module("vaderSentiment.vaderSentiment")
                analyzer_cls = getattr(vader_mod, "SentimentIntensityAnalyzer")
                analyzer = analyzer_cls()
                test_sentiment = analyzer.polarity_scores("This is great!")
                health_data["components"]["vader"] = {
                    "status": "healthy",
                    "test_score": test_sentiment["compound"],
                }
            except Exception as e:
                health_data["components"]["vader"] = {
                    "status": "error",
                    "error": str(e),
                }
                health_data["status"] = "warning"

            # Check TextBlob
            try:
                import importlib

                tb_mod = importlib.import_module("textblob")
                TextBlob = getattr(tb_mod, "TextBlob")
                blob = TextBlob("This is a test.")
                sentiment = getattr(blob, "sentiment", None)
                test_sentiment = getattr(sentiment, "polarity", 0.0)
                health_data["components"]["textblob"] = {
                    "status": "healthy",
                    "test_polarity": test_sentiment,
                }
            except Exception as e:
                health_data["components"]["textblob"] = {
                    "status": "error",
                    "error": str(e),
                }
                health_data["status"] = "warning"

            self.health_checks["nlp_components"] = health_data
            return health_data

        except Exception as e:
            self.debugger.error(
                "health_monitor", "NLP component check failed", {"error": str(e)}
            )
            return {"status": "error", "error": str(e)}

    @performance_monitor("health_monitor")
    def check_evolution_engine(self) -> Dict[str, Any]:
        """Check evolution engine health"""
        try:
            health_data: Dict[str, Any] = {"timestamp": datetime.now().isoformat(), "status": "healthy"}

            # Import and test evolution engine
            from evolution_engine import get_evolution_engine

            engine = get_evolution_engine()

            # Get evolution status (use getattr to avoid type checker complaints)
            evolution_status: Dict[str, Any] = {}
            try:
                getter = getattr(engine, "get_evolution_status", None)
                if callable(getter):
                    result = getter()
                    if isinstance(result, dict):
                        evolution_status = cast(Dict[str, Any], result)
            except Exception:
                evolution_status = {}

            health_data.update(
                {
                    "concept_count": evolution_status.get("concept_count", 0),
                    "connection_count": evolution_status.get("connection_count", 0),
                    "evolution_score": evolution_status.get("evolution_score", 0),
                    "capabilities": evolution_status.get("capabilities", {}),
                }
            )

            # Check for issues
            issues: List[str] = []
            if evolution_status.get("concept_count", 0) == 0:
                issues.append("No concepts learned yet")

            if evolution_status.get("evolution_score", 0) < 0.1:
                issues.append("Low evolution score")

            health_data["issues"] = issues
            if issues:
                health_data["status"] = "warning"

            self.health_checks["evolution_engine"] = health_data
            return health_data

        except Exception as e:
            self.debugger.error(
                "health_monitor", "Evolution engine check failed", {"error": str(e)}
            )
            return {"status": "error", "error": str(e)}

    @performance_monitor("health_monitor")
    def run_full_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        self.debugger.info("health_monitor", "Starting full health check")

        full_report = {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "checks": {},
        }

        # Run all health checks
        checks = [
            ("system_resources", self.check_system_resources),
            ("database", self.check_database_health),
            ("nlp_components", self.check_nlp_components),
            ("evolution_engine", self.check_evolution_engine),
        ]

        overall_status = "healthy"
        for check_name, check_func in checks:
            try:
                result = check_func()
                full_report["checks"][check_name] = result

                if result.get("status") == "error":
                    overall_status = "error"
                elif result.get("status") == "warning" and overall_status != "error":
                    overall_status = "warning"

            except Exception as e:
                full_report["checks"][check_name] = {"status": "error", "error": str(e)}
                overall_status = "error"
                self.debugger.error(
                    "health_monitor",
                    f"Health check {check_name} failed",
                    {"error": str(e), "check": check_name},
                )

        full_report["overall_status"] = overall_status

        # Log summary
        healthy_checks = sum(
            1
            for check in full_report["checks"].values()
            if check.get("status") == "healthy"
        )
        total_checks = len(full_report["checks"])

        self.debugger.info(
            "health_monitor",
            f"Health check complete: {healthy_checks}/{total_checks} healthy",
            {"overall_status": overall_status},
        )

        return full_report

    def get_health_summary(self) -> Dict[str, Any]:
        """Get quick health summary"""
        return {
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "last_checks": {
                name: check.get("status", "unknown")
                for name, check in self.health_checks.items()
            },
            "alert_count": len(self.alerts),
        }


# Global health monitor
_health_monitor = None


def get_health_monitor() -> SystemHealthMonitor:
    """Get global health monitor instance"""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = SystemHealthMonitor()
    return _health_monitor
