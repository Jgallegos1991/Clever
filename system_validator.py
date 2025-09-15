"""
System Validator and Auto-Corrector for Clever AI

Why: Ensures continuous adherence to all Unbreakable Rules and instructions
by monitoring system state, detecting deviations, and automatically correcting
issues to maintain peak performance and perfect instruction compliance.
  
  
Where: Used by app.py, persona.py, and all core modules for continuous
validation and self-correction of system integrity and rule compliance.
How: Implements comprehensive validation checks, automated corrections,
and real-time monitoring to ensure Clever operates at maximum capability.

Connects to:
    - .github/copilot-instructions.md: Validates against all Unbreakable Rules
    - config.py: Ensures proper configuration alignment
    - user_config.py: Validates user-specific settings compliance
    - All modules: Monitors and corrects system-wide compliance
"""
from __future__ import annotations

from typing import Dict, List, Any
import socket
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import config
import user_config
from utils import offline_guard
from debug_config import get_debugger

logger = get_debugger()
  
  
@dataclass
class ValidationResult:
    """Container for validation check results"""
    check_name: str
    passed: bool
    details: str
    severity: str  # 'critical', 'warning', 'info'
    auto_corrected: bool = False
    correction_details: str = ""


class SystemValidator:
    """
    Comprehensive system validator ensuring perfect adherence to all rules.
    
  
  
    Why: Maintains system integrity by continuously validating against
    Unbreakable Rules and automatically correcting any deviations to ensure
    Clever operates at full potential without compromise.
    Where: Integrated into all core system operations for real-time validation
    and correction,
    ensuring consistent peak performance across all interactions.
    How: Implements validation matrix covering offline operation, single-user
    mode, database integrity, and documentation standards with auto-correction.
    
  
  
    Connects to:
        - offline_guard: Validates and enforces offline-only operation
        - config system: Ensures proper configuration compliance
        - database: Validates single database rule adherence
        - All modules: Provides system-wide integrity monitoring
    """
    
    def __init__(self):
        """Initialize validator with all rule checks."""
        self.validation_checks = [
            self._validate_offline_enforcement,
            self._validate_single_user_config,
            self._validate_single_database,
            self._validate_jay_personalization,
            self._validate_clever_persona,
            self._validate_file_structure_compliance,
            self._validate_nlp_capabilities,
            self._validate_evolution_engine_access,
            self._validate_documentation_standards,
            self._validate_performance_optimization
        ]

    def run_full_validation(self) -> Dict[str, Any]:
        """
        Run comprehensive system validation.
        
    Why: Provides complete system health check against all Unbreakable Rules.
    To ensure perfect compliance and identify any areas requiring correction.
    Where: Called during system startup and periodically for maintenance.
    How: Executes all validation checks, attempts auto-correction,
    reports results.
        
        Returns:
            Complete validation report with results and corrections.
        """
        logger.info(
            'system_validator',
            'Starting comprehensive system validation...'
        )
        results = []
        auto_corrections_applied = 0
        critical_issues = 0
        for check in self.validation_checks:
            try:
                result = check()
                results.append(result)
                if result.auto_corrected:
                    auto_corrections_applied += 1
                    logger.info(
                        'system_validator',
                        f'Auto-corrected: {result.check_name}'
                    )
                if result.severity == 'critical' and not result.passed:
                    critical_issues += 1
            except Exception as e:
                logger.error(
                    'system_validator',
                    f'Validation check failed: {check.__name__}: {e}'
                )
                results.append(
                    ValidationResult(
                        check_name=check.__name__,
                        passed=False,
                        details=f"Validation failed with error: {e}",
                        severity='critical'
                    )
                )
                critical_issues += 1
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': (
                'PASS' if critical_issues == 0 else 'CRITICAL_ISSUES'
            ),
            'total_checks': len(results),
            'passed_checks': sum(1 for r in results if r.passed),
            'critical_issues': critical_issues,
            'auto_corrections_applied': auto_corrections_applied,
            'results': results,
            'recommendations': self._generate_recommendations(results)
        }
        
        logger.info(
            'system_validator',
            f'Validation complete: {report["overall_status"]} - '
            f'{report["passed_checks"]}/{report["total_checks"]} passed'
        )
        return report
    
    def _validate_offline_enforcement(self) -> ValidationResult:
        """Validate Rule #1: Strictly Offline Operation"""
        try:
            # Check if offline guard is enabled
            if not offline_guard.is_enabled():
                offline_guard.enable()
                return ValidationResult(
                    check_name="Offline Enforcement",
                    passed=True,
                    details=(
                        "Offline guard was disabled, automatically enabled"
                    ),
                    severity='warning',
                    auto_corrected=True,
                    correction_details=(
                        "Called offline_guard.enable() to enforce offline "
                        "operation"
                    )
                )
            
            # Test that external connections are blocked
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(1)
                test_socket.connect(('8.8.8.8', 53))  # Should be blocked
                test_socket.close()
                
                return ValidationResult(
                    check_name="Offline Enforcement",
                    passed=False,
                    details=(
                        "External network connections not properly blocked"
                    ),
                    severity='critical'
                )
            except (PermissionError, OSError):
                # Expected - connections should be blocked
                pass
            
            return ValidationResult(
                check_name="Offline Enforcement",
                passed=True,
                details=(
                    "Offline operation properly enforced - external "
                    "connections blocked"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Offline Enforcement",
                passed=False,
                details=f"Failed to validate offline enforcement: {e}",
                severity='critical'
            )
    
    def _validate_single_user_config(self) -> ValidationResult:
        """Validate Rule #2: Single-User Only (Jay)"""
        try:
            # Check user configuration
            if (
                not hasattr(user_config, 'USER_NAME') or
                user_config.USER_NAME != "Jay"
            ):
                return ValidationResult(
                    check_name="Single User Config",
                    passed=False,
                    details=(
                        f"User name not configured as 'Jay': "
                        f"{getattr(user_config, 'USER_NAME', 'MISSING')}"
                    ),
                    severity='critical'
                )
            
            # Check external access is disabled
            if getattr(user_config, 'CLEVER_EXTERNAL_ACCESS', True):
                return ValidationResult(
                    check_name="Single User Config", 
                    passed=False,
                    details="External access not properly disabled",
                    severity='critical'
                )
            
            return ValidationResult(
                check_name="Single User Config",
                passed=True,
                details=(
                    f"System properly configured for single user: "
                    f"{user_config.USER_NAME}"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Single User Config",
                passed=False,
                details=f"Failed to validate user configuration: {e}",
                severity='critical'
            )
    
    def _validate_single_database(self) -> ValidationResult:
        """Validate Rule #3: Single Database (clever.db)"""
        try:
            db_files = list(Path('.').glob('*.db'))
            
            if len(db_files) != 1:
                return ValidationResult(
                    check_name="Single Database",
                    passed=False,
                    details=(
                        f"Found {len(db_files)} database files, "
                        f"should be exactly 1: {[f.name for f in db_files]}"
                    ),
                    severity='critical'
                )
            
            expected_db = Path(config.DB_PATH)
            if not expected_db.exists():
                return ValidationResult(
                    check_name="Single Database",
                    passed=False,
                    details=f"Database file {config.DB_PATH} does not exist",
                    severity='critical'
                )
            
            if db_files[0].name != expected_db.name:
                return ValidationResult(
                    check_name="Single Database",
                    passed=False,
                    details=(
                        f"Database file mismatch: found {db_files[0].name}, "
                        f"expected {expected_db.name}"
                    ),
                    severity='critical'
                )
            
            return ValidationResult(
                check_name="Single Database",
                passed=True,
                details=(
                    f"Single database properly configured: {expected_db.name}"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Single Database",
                passed=False,
                details=f"Failed to validate database configuration: {e}",
                severity='critical'
            )
    
    def _validate_jay_personalization(self) -> ValidationResult:
        """Validate system is properly personalized for Jay"""
        try:
            # Check user details
            checks = [
                ('USER_NAME', 'Jay'),
                ('USER_EMAIL', 'lapirfta@gmail.com'),
                ('USER_FULL_NAME', 'Jordan Gallegos')
            ]
            
            for attr, expected in checks:
                actual = getattr(user_config, attr, None)
                if actual != expected:
                    return ValidationResult(
                        check_name="Jay Personalization",
                        passed=False,
                        details=(
                            f"{attr} mismatch: expected '{expected}', "
                            f"got '{actual}'"
                        ),
                        severity='warning'
                    )
            
            return ValidationResult(
                check_name="Jay Personalization",
                passed=True,
                details=(
                    "System properly personalized for Jay with correct "
                    "user details"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Jay Personalization",
                passed=False,
                details=f"Failed to validate personalization: {e}",
                severity='warning'
            )
    
    def _validate_clever_persona(self) -> ValidationResult:
        """Validate Clever persona is properly configured"""
        try:
            from persona import persona_engine, PersonaEngine
            
            # Check persona engine exists and is configured
            if not isinstance(persona_engine, PersonaEngine):
                return ValidationResult(
                    check_name="Clever Persona",
                    passed=False,
                    details="Persona engine not properly initialized",
                    severity='critical'
                )
            
            # Test response generation
            test_response = persona_engine.generate(
                "Test message", mode="Auto"
            )
            
            if not test_response or not test_response.text:
                return ValidationResult(
                    check_name="Clever Persona",
                    passed=False,
                    details="Persona engine not generating responses",
                    severity='critical'
                )
            
            # Check all modes are available
            required_modes = [
                "Auto", "Creative", "Deep Dive", "Support", "Quick Hit"
            ]
            for mode in required_modes:
                if mode not in persona_engine.modes:
                    return ValidationResult(
                        check_name="Clever Persona",
                        passed=False,
                        details=f"Required persona mode missing: {mode}",
                        severity='warning'
                    )
            
            return ValidationResult(
                check_name="Clever Persona",
                passed=True,
                details=(
                    f"Clever persona fully functional with "
                    f"{len(persona_engine.modes)} modes available"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Clever Persona",
                passed=False,
                details=f"Failed to validate persona: {e}",
                severity='critical'
            )
    
    def _validate_file_structure_compliance(self) -> ValidationResult:
        """Validate file structure matches CURRENT_FILE_STRUCTURE.md"""
        try:
            # Check critical files exist
            required_files = [
                'templates/index.html',
                'static/css/style.css',
                'static/js/holographic-chamber.js',
                'static/js/main.js',
                'app.py',
                'persona.py',
                'database.py',
                'config.py'
            ]
            
            missing_files = []
            for file_path in required_files:
                if not Path(file_path).exists():
                    missing_files.append(file_path)
            
            if missing_files:
                return ValidationResult(
                    check_name="File Structure Compliance",
                    passed=False,
                    details=f"Missing required files: {missing_files}",
                    severity='critical'
                )
            
            # Check template loads correct scripts
            template_path = Path('templates/index.html')
            if template_path.exists():
                content = template_path.read_text()
                if (
                    'holographic-chamber.js' not in content or
                    'main.js' not in content
                ):
                    return ValidationResult(
                        check_name="File Structure Compliance",
                        passed=False,
                        details=(
                            "Template not loading correct JavaScript files"
                        ),
                        severity='warning'
                    )
            
            return ValidationResult(
                check_name="File Structure Compliance",
                passed=True,
                details="File structure properly aligned with specifications",
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="File Structure Compliance",
                passed=False,
                details=f"Failed to validate file structure: {e}",
                severity='warning'
            )
    
    def _validate_nlp_capabilities(self) -> ValidationResult:
        """Validate NLP processor has full capabilities"""
        try:
            from nlp_processor import nlp_processor
            
            # Test NLP processing
            test_text = (
                "This is a complex sentence with multiple entities and "
                "emotions for testing NLP capabilities."
            )
            result = nlp_processor.process(test_text)
            
            if (
                not result or
                not hasattr(result, 'keywords') or
                not hasattr(result, 'sentiment')
            ):
                return ValidationResult(
                    check_name="NLP Capabilities",
                    passed=False,
                    details="NLP processor not returning expected results",
                    severity='critical'
                )
            
            # Check keywords extraction
            if not result.keywords or len(result.keywords) == 0:
                return ValidationResult(
                    check_name="NLP Capabilities", 
                    passed=False,
                    details="Keywords extraction not working",
                    severity='warning'
                )
            
            # Check sentiment analysis
            if (
                result.sentiment is None or
                not isinstance(result.sentiment, (int, float))
            ):
                return ValidationResult(
                    check_name="NLP Capabilities",
                    passed=False,
                    details="Sentiment analysis not working",
                    severity='warning'
                )
            
            return ValidationResult(
                check_name="NLP Capabilities",
                passed=True,
                details=(
                    f"NLP processor fully functional - extracted "
                    f"{len(result.keywords)} keywords, "
                    f"sentiment: {result.sentiment}"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="NLP Capabilities",
                passed=False,
                details=f"Failed to validate NLP capabilities: {e}",
                severity='critical'
            )
    
    def _validate_evolution_engine_access(self) -> ValidationResult:
        """Validate evolution engine has full access and functionality"""
        try:
            from evolution_engine import get_evolution_engine
            
            evo_engine = get_evolution_engine()
            if not evo_engine:
                return ValidationResult(
                    check_name="Evolution Engine Access",
                    passed=False,
                    details="Evolution engine not accessible",
                    severity='critical'
                )
            
            # Test interaction logging
            test_interaction = {
                "user_input": "test validation message",
                "response": "test response",
                "mode": "Auto"
            }
            
            try:
                evo_engine.log_interaction(test_interaction)
            except Exception as e:
                return ValidationResult(
                    check_name="Evolution Engine Access",
                    passed=False,
                    details=(
                        f"Evolution engine interaction logging failed: {e}"
                    ),
                    severity='warning'
                )
            
            return ValidationResult(
                check_name="Evolution Engine Access",
                passed=True,
                details=(
                    "Evolution engine fully accessible with logging "
                    "capabilities"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Evolution Engine Access",
                passed=False,
                details=f"Failed to validate evolution engine: {e}",
                severity='critical'
            )
    
    def _validate_documentation_standards(self) -> ValidationResult:
        """Validate Rule #4: Mandatory Code Documentation"""
        try:
            # Check key files have proper documentation headers
            files_to_check = [
                'app.py', 'persona.py', 'database.py', 'evolution_engine.py'
            ]
            undocumented_files = []
            
            for file_path in files_to_check:
                path = Path(file_path)
                if path.exists():
                    content = path.read_text()
                    # Check for documentation patterns
                    if (
                        'Why:' not in content or
                        'Where:' not in content or
                        'How:' not in content
                    ):
                        undocumented_files.append(file_path)
            
            if undocumented_files:
                return ValidationResult(
                    check_name="Documentation Standards",
                    passed=False,
                    details=(
                        f"Files missing proper documentation: "
                        f"{undocumented_files}"
                    ),
                    severity='warning'
                )
            
            return ValidationResult(
                check_name="Documentation Standards",
                passed=True,
                details=(
                    "All key files have proper documentation standards"
                ),
                severity='info'
            )
            
        except Exception as e:
            return ValidationResult(
                check_name="Documentation Standards",
                passed=False,
                details=f"Failed to validate documentation: {e}",
                severity='warning'
            )
    
    def _validate_performance_optimization(self) -> ValidationResult:
        """Validate system performance and optimization"""
        try:
            import psutil
            import time
            
            # Check memory usage
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            # Check response time
            start_time = time.time()
            from persona import persona_engine
            persona_engine.generate(
                "Quick test", mode="Quick Hit"
            )
            response_time = time.time() - start_time
            
            issues = []
            if memory_mb > 500:  # Flag if using more than 500MB
                issues.append(f"High memory usage: {memory_mb:.1f}MB")
            
            if (
                response_time > 2.0
                # Flag if responses take more than 2 seconds
            ):
                issues.append(f"Slow response time: {response_time:.2f}s")
            
            if issues:
                return ValidationResult(
                    check_name="Performance Optimization",
                    passed=False,
                    details=(
                        f"Performance issues detected: {'; '.join(issues)}"
                    ),
                    severity='warning'
                )
            
            return ValidationResult(
                check_name="Performance Optimization",
                passed=True,
                details=(
                    f"Performance optimal - Memory: {memory_mb:.1f}MB, "
                    f"Response: {response_time:.3f}s"
                ),
                severity='info'
            )
            
        except ImportError:
            return ValidationResult(
                check_name="Performance Optimization",
                passed=True,
                details=(
                    "Performance monitoring unavailable (psutil not installed)"
                ),
                severity='info'
            )
        except Exception as e:
            return ValidationResult(
                check_name="Performance Optimization",
                passed=False,
                details=f"Failed to validate performance: {e}",
                severity='warning'
            )
    
    def _generate_recommendations(
        self, results: List[ValidationResult]
    ) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []
        
        failed_critical = [
            r for r in results if not r.passed and r.severity == 'critical'
        ]
        if failed_critical:
            recommendations.append(
                "CRITICAL: Address failed critical checks "
                "immediately for system stability"
            )
        
        auto_corrected = [r for r in results if r.auto_corrected]
        if auto_corrected:
            recommendations.append(
                "Review auto-corrections applied to ensure "
                "they meet requirements"
            )
        
        warnings = [
            r for r in results if not r.passed and r.severity == 'warning'
        ]
        if warnings:
            recommendations.append(
                "Address warning-level issues to optimize "
                "system performance"
            )
        
        if len([r for r in results if r.passed]) == len(results):
            recommendations.append(
                "System operating at peak performance - "
                "all validations passed!"
            )
        
        return recommendations

# Global validator instance
  
  
_system_validator = None

  
def get_system_validator() -> SystemValidator:
    """
    Get global system validator instance
    
    Why: Provides singleton access to system validator for consistent
    validation and monitoring across all system components.
    Where: Used by all modules requiring system validation capabilities
    How: Implements lazy initialization pattern for global validator access
    
    Returns:
        SystemValidator instance for system validation operations
        
    Connects to:
        - All system modules: Provides validation capabilities
        - Monitoring systems: Enables continuous system health checks
    """
    global _system_validator
    if _system_validator is None:
        _system_validator = SystemValidator()
    return _system_validator

  
def validate_system_startup() -> Dict[str, Any]:
    """
    Run system validation during startup
    
    Why: Ensures system integrity and rule compliance before operation begins
    Where: Called during app.py initialization for startup validation
    How: Executes comprehensive validation and reports critical issues
    
    Returns:
        Validation report with startup system health status
    """
    validator = get_system_validator()
    return validator.run_full_validation()

  
if __name__ == "__main__":
    # Run standalone validation
    validator = SystemValidator()
    report = validator.run_full_validation()
    
    print("=== CLEVER AI SYSTEM VALIDATION REPORT ===")
    print(f"Overall Status: {report['overall_status']}")
    print(f"Checks Passed: {report['passed_checks']}/{report['total_checks']}")
    print(f"Auto-corrections Applied: {report['auto_corrections_applied']}")
    
    for result in report['results']:
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"{status} {result.check_name}: {result.details}")
        
        if result.auto_corrected:
            print(f"    🔧 Auto-corrected: {result.correction_details}")
    
    print("\n=== RECOMMENDATIONS ===")
    for rec in report['recommendations']:
        print(f"💡 {rec}")
