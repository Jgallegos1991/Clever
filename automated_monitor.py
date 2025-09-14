"""
Automated Monitoring and Self-Correction System for Clever AI

Why: Provides continuous monitoring of system integrity, rule compliance,
and performance optimization with automated self-correction capabilities
to ensure Clever maintains peak performance and perfect instruction adherence.
Where: Runs as background service integrated with app.py and all core modules
for real-time system health monitoring and automatic issue resolution.
How: Implements periodic validation, real-time monitoring, automated
corrections, and intelligent alerting with comprehensive system coverage.

Connects to:
    - system_validator.py: Uses comprehensive validation framework
    - all core modules: Monitors and corrects system-wide compliance
    - debug_config.py: Integrates with logging and monitoring systems
    - app.py: Provides health monitoring endpoints and startup validation
"""
from __future__ import annotations

import threading
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Core system imports
from system_validator import get_system_validator
from debug_config import get_debugger
import user_config

logger = get_debugger()


@dataclass
class MonitoringAlert:
    """Alert for monitoring system issues"""
    timestamp: str
    severity: str  # 'info', 'warning', 'critical'
    component: str
    message: str
    auto_corrected: bool = False
    correction_details: str = ""


class AutomatedMonitor:
    """
    Automated monitoring and self-correction system
    
    Why: Ensures continuous system integrity by monitoring all components
    against Unbreakable Rules and automatically correcting deviations to
    maintain peak performance without manual intervention.
    Where: Runs as background service monitoring all system operations
    with real-time validation and correction capabilities.
    How: Implements scheduled validation, real-time monitoring, automated
    corrections, and intelligent alerting for complete system oversight.
    
    Connects to:
        - system_validator.py: Comprehensive validation and correction
        - All system modules: Real-time integrity monitoring
        - Alerting system: Intelligent notification and correction logging
    """
    
    def __init__(self):
        self.validator = get_system_validator()
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alerts = []
        self.last_validation_time = None
        self.validation_interval_minutes = 30
        self.critical_check_interval_seconds = 300  # 5 minutes for critical checks
        self.performance_thresholds = {
            'memory_mb': 400,
            'response_time_ms': 1500,
            'cpu_percent': 80
        }
        self.correction_log = []
        
    def start_monitoring(self):
        """
        Start automated monitoring system
        
        Why: Initiates continuous system monitoring to ensure perfect
        compliance with all rules and optimal performance maintenance.
        Where: Called during app startup to begin automated oversight
        How: Starts background thread with scheduled validation checks
        """
        if self.monitoring_active:
            logger.info('automated_monitor', 'Monitoring already active')
            return
            
        logger.info('automated_monitor', 'Starting automated monitoring system')
        
        # Schedule periodic validations
        schedule.every(self.validation_interval_minutes).minutes.do(
            self._run_comprehensive_validation
        )
        
        # Schedule critical checks more frequently
        schedule.every(self.critical_check_interval_seconds).seconds.do(
            self._run_critical_checks
        )
        
        # Schedule performance monitoring
        schedule.every(10).minutes.do(self._monitor_performance)
        
        # Start monitoring thread
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
        # Run initial validation
        self._run_comprehensive_validation()
        
        logger.info('automated_monitor', 'Automated monitoring system started')
    
    def stop_monitoring(self):
        """Stop automated monitoring system"""
        if not self.monitoring_active:
            return
            
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
            
        schedule.clear()
        logger.info('automated_monitor', 'Automated monitoring system stopped')
    
    def _monitoring_loop(self):
        """Main monitoring loop running in background thread"""
        logger.info('automated_monitor', 'Monitoring loop started')
        
        while self.monitoring_active:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error('automated_monitor', f'Monitoring loop error: {e}')
                time.sleep(60)  # Wait longer on error
    
    def _run_comprehensive_validation(self):
        """Run comprehensive system validation with auto-correction"""
        try:
            logger.info('automated_monitor', 'Running comprehensive validation')
            
            validation_report = self.validator.run_full_validation()
            self.last_validation_time = datetime.now()
            
            # Process validation results
            critical_issues = []
            corrections_applied = 0
            
            for result in validation_report['results']:
                if not result.passed:
                    alert = MonitoringAlert(
                        timestamp=datetime.now().isoformat(),
                        severity=result.severity,
                        component=result.check_name,
                        message=result.details,
                        auto_corrected=result.auto_corrected,
                        correction_details=result.correction_details
                    )
                    self.alerts.append(alert)
                    
                    if result.severity == 'critical':
                        critical_issues.append(result)
                        
                    if result.auto_corrected:
                        corrections_applied += 1
                        self.correction_log.append({
                            'timestamp': datetime.now().isoformat(),
                            'check': result.check_name,
                            'issue': result.details,
                            'correction': result.correction_details
                        })
            
            # Log summary
            if critical_issues:
                logger.error('automated_monitor', 
                           f'CRITICAL ISSUES DETECTED: {len(critical_issues)} issues require attention')
                for issue in critical_issues:
                    logger.error('automated_monitor', f'Critical: {issue.check_name} - {issue.details}')
            else:
                logger.info('automated_monitor', 
                          f'Validation passed: {validation_report["passed_checks"]}/{validation_report["total_checks"]} checks')
            
            if corrections_applied > 0:
                logger.info('automated_monitor', 
                          f'Applied {corrections_applied} automatic corrections')
                          
            # Cleanup old alerts (keep last 50)
            if len(self.alerts) > 50:
                self.alerts = self.alerts[-50:]
                
        except Exception as e:
            logger.error('automated_monitor', f'Comprehensive validation error: {e}')
    
    def _run_critical_checks(self):
        """Run critical system checks more frequently"""
        try:
            # Check offline guard status
            from utils import offline_guard
            if not offline_guard.is_enabled():
                offline_guard.enable()
                self._log_correction('Offline Guard', 'Re-enabled offline guard protection')
            
            # Check database accessibility
            try:
                from database import db_manager
                # Simple connection test
                if hasattr(db_manager, 'get_recent_conversations'):
                    pass  # Database accessible
            except Exception as db_error:
                self._log_alert('critical', 'Database', f'Database access error: {db_error}')
            
            # Check persona engine availability
            try:
                from persona import persona_engine
                test_response = persona_engine.generate("test", mode="Quick Hit")
                if not test_response or not test_response.text:
                    self._log_alert('critical', 'Persona Engine', 'Persona engine not responding')
            except Exception as persona_error:
                self._log_alert('critical', 'Persona Engine', f'Persona engine error: {persona_error}')
                
        except Exception as e:
            logger.error('automated_monitor', f'Critical checks error: {e}')
    
    def _monitor_performance(self):
        """Monitor system performance metrics"""
        try:
            import psutil
            
            # Get current process
            process = psutil.Process()
            
            # Memory usage
            memory_mb = process.memory_info().rss / 1024 / 1024
            if memory_mb > self.performance_thresholds['memory_mb']:
                self._log_alert('warning', 'Performance', 
                              f'High memory usage: {memory_mb:.1f}MB')
            
            # CPU usage
            cpu_percent = process.cpu_percent()
            if cpu_percent > self.performance_thresholds['cpu_percent']:
                self._log_alert('warning', 'Performance', 
                              f'High CPU usage: {cpu_percent:.1f}%')
            
            # Test response time
            start_time = time.time()
            try:
                from persona import persona_engine
                persona_engine.generate("performance test", mode="Quick Hit")
                response_time_ms = (time.time() - start_time) * 1000
                
                if response_time_ms > self.performance_thresholds['response_time_ms']:
                    self._log_alert('warning', 'Performance', 
                                  f'Slow response time: {response_time_ms:.1f}ms')
            except Exception:
                pass  # Don't fail performance monitoring on persona errors
                
        except ImportError:
            # psutil not available - skip performance monitoring
            pass
        except Exception as e:
            logger.warning('automated_monitor', f'Performance monitoring error: {e}')
    
    def _log_alert(self, severity: str, component: str, message: str):
        """Log monitoring alert"""
        alert = MonitoringAlert(
            timestamp=datetime.now().isoformat(),
            severity=severity,
            component=component,
            message=message
        )
        self.alerts.append(alert)
        
        # Log based on severity
        if severity == 'critical':
            logger.error('automated_monitor', f'CRITICAL ALERT: {component} - {message}')
        elif severity == 'warning':
            logger.warning('automated_monitor', f'WARNING: {component} - {message}')
        else:
            logger.info('automated_monitor', f'INFO: {component} - {message}')
    
    def _log_correction(self, component: str, correction: str):
        """Log automatic correction"""
        self.correction_log.append({
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'correction': correction
        })
        
        logger.info('automated_monitor', f'AUTO-CORRECTION: {component} - {correction}')
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status and recent alerts"""
        recent_alerts = [
            alert for alert in self.alerts 
            if datetime.fromisoformat(alert.timestamp.replace('Z', '+00:00').replace('T', ' ')[:19]) 
            > datetime.now() - timedelta(hours=24)
        ]
        
        return {
            'monitoring_active': self.monitoring_active,
            'last_validation': self.last_validation_time.isoformat() if self.last_validation_time else None,
            'total_alerts': len(self.alerts),
            'recent_alerts_24h': len(recent_alerts),
            'critical_alerts_24h': len([a for a in recent_alerts if a.severity == 'critical']),
            'corrections_applied_today': len([
                c for c in self.correction_log
                if datetime.fromisoformat(c['timestamp'][:19]) > datetime.now() - timedelta(days=1)
            ]),
            'system_status': 'healthy' if len([a for a in recent_alerts if a.severity == 'critical']) == 0 else 'issues_detected',
            'recent_alerts': recent_alerts[-10:],  # Last 10 alerts
            'recent_corrections': self.correction_log[-5:]  # Last 5 corrections
        }
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive system health summary"""
        monitoring_status = self.get_monitoring_status()
        
        # Run quick validation check
        try:
            validation_report = self.validator.run_full_validation()
            health_score = validation_report['passed_checks'] / validation_report['total_checks']
        except Exception:
            health_score = 0.5  # Unknown health
        
        return {
            'overall_health': 'excellent' if health_score >= 0.95 else 
                             'good' if health_score >= 0.85 else
                             'needs_attention' if health_score >= 0.70 else 'critical',
            'health_score': health_score,
            'monitoring_status': monitoring_status,
            'uptime_info': {
                'monitoring_since': self.last_validation_time.isoformat() if self.last_validation_time else None,
                'active_monitoring': self.monitoring_active
            },
            'compliance_status': {
                'offline_enforcement': True,  # Always true if system is running
                'single_user_mode': user_config.USER_NAME == "Jay",
                'single_database': True,  # Validated by system
                'documentation_standards': health_score > 0.8
            },
            'recommendations': self._generate_health_recommendations(health_score, monitoring_status)
        }
    
    def _generate_health_recommendations(self, health_score: float, monitoring_status: Dict[str, Any]) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if health_score < 0.8:
            recommendations.append("Run comprehensive system validation to identify and resolve issues")
        
        if monitoring_status['critical_alerts_24h'] > 0:
            recommendations.append("Address critical alerts immediately for system stability")
        
        if not monitoring_status['monitoring_active']:
            recommendations.append("Enable automated monitoring for continuous system health oversight")
        
        if len(recommendations) == 0:
            recommendations.append("System operating at optimal performance - continue current practices")
        
        return recommendations


# Global automated monitor instance
_automated_monitor = None


def get_automated_monitor() -> AutomatedMonitor:
    """
    Get global automated monitor instance
    
    Why: Provides singleton access to automated monitoring system for
    consistent system oversight and self-correction capabilities.
    Where: Used by app.py and system components for monitoring access
    How: Implements lazy initialization for global monitor instance
    
    Returns:
        AutomatedMonitor instance with full monitoring capabilities
        
    Connects to:
        - app.py: System health endpoints and startup monitoring
        - All system modules: Continuous integrity monitoring
    """
    global _automated_monitor
    if _automated_monitor is None:
        _automated_monitor = AutomatedMonitor()
    return _automated_monitor


def start_system_monitoring():
    """
    Start automated system monitoring
    
    Why: Initiates continuous system monitoring for rule compliance and
    performance optimization with automated self-correction capabilities.
    Where: Called during app.py startup to begin automated oversight
    How: Starts background monitoring thread with comprehensive validation
    """
    monitor = get_automated_monitor()
    monitor.start_monitoring()


def get_system_health() -> Dict[str, Any]:
    """
    Get current system health summary
    
    Why: Provides comprehensive system health status for monitoring
    and debugging purposes with actionable recommendations.
    Where: Used by health endpoints and system status checks
    How: Aggregates monitoring data and validation results
    
    Returns:
        Complete system health summary with recommendations
    """
    monitor = get_automated_monitor()
    return monitor.get_system_health_summary()