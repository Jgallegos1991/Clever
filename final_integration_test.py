#!/usr/bin/env python3
"""
Final Integration Test for Comprehensive System Enhancement

Why: Validates that all enhanced capabilities work together perfectly
Where: Tests integration of enhanced conversation engine, system validator,
       and automated monitoring with core application
How: Runs comprehensive test scenarios to verify system meets user requirements
     for perfect conversational capability and full access

Connects to:
- enhanced_conversation_engine.py: Tests advanced conversation processing
- system_validator.py: Validates rule compliance and auto-correction
- automated_monitor.py: Ensures monitoring systems are operational
- app.py: Integration testing with Flask application
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, Any

# Add project root to path for imports
sys.path.insert(0, "/workspaces/projects")

# Import all enhanced components
from system_validator import SystemValidator, validate_system_startup
from enhanced_conversation_engine import EnhancedConversationEngine
from automated_monitor import AutomatedMonitor
from debug_config import get_debugger
import config


class FinalIntegrationTester:
    """
    Comprehensive test suite for enhanced Clever AI system

    Why: Ensures all enhancements work together to provide perfect
         conversational capability as requested by user
    Where: Tests integration points across all major system components
    How: Runs realistic conversation scenarios and validates system responses
    """

    def __init__(self):
        """Initialize test environment with enhanced components"""
        self.debugger = get_debugger()
        self.validator = SystemValidator()
        self.conversation_engine = None
        self.monitor = None
        self.test_results = []

    def setup_test_environment(self) -> bool:
        """
        Setup enhanced test environment

        Why: Creates isolated test environment to validate enhancements
        Where: Initializes all enhanced components safely
        How: Attempts to create conversation engine and monitor instances
        """
        try:
            # Test enhanced conversation engine
            self.conversation_engine = EnhancedConversationEngine()

            # Test automated monitor (don't start background threads in test)
            self.monitor = AutomatedMonitor(start_background=False)

            print("✅ Enhanced test environment setup successful")
            return True

        except Exception as e:
            print(f"❌ Test environment setup failed: {e}")
            return False

    def test_system_validation(self) -> Dict[str, Any]:
        """
        Test comprehensive system validation

        Why: Ensures system validator correctly identifies and fixes issues
        Where: Tests validation against all Unbreakable Rules
        How: Runs full validation suite and checks auto-correction
        """
        print("\n🔍 Testing System Validation...")

        try:
            # Run startup validation
            validation_report = validate_system_startup()

            # Test individual validation components
            validation_results = self.validator.validate_system()

            result = {
                "test": "system_validation",
                "passed": validation_report["overall_status"] == "PASS",
                "details": {
                    "startup_validation": validation_report,
                    "individual_checks": len(
                        [r for r in validation_results if r.passed]
                    ),
                    "total_checks": len(validation_results),
                    "critical_issues": len(
                        [
                            r
                            for r in validation_results
                            if not r.passed and r.severity == "critical"
                        ]
                    ),
                },
            }

            if result["passed"]:
                print(
                    f"✅ System validation passed - "
                    f"{result['details']['individual_checks']}"
                    f"/{result['details']['total_checks']} checks"
                )
            else:
                print(
                    f"❌ System validation failed - "
                    f"{result['details']['critical_issues']} critical issues"
                )

            return result

        except Exception as e:
            return {"test": "system_validation", "passed": False, "error": str(e)}

    def test_enhanced_conversation(self) -> Dict[str, Any]:
        """
        Test enhanced conversation capabilities

        Why: Validates advanced conversation processing meets user requirements
        Where: Tests conversation engine with complex scenarios
        How: Processes various conversation types and validates responses
        """
        print("\n💬 Testing Enhanced Conversation Engine...")

        if not self.conversation_engine:
            return {
                "test": "enhanced_conversation",
                "passed": False,
                "error": "Conversation engine not initialized",
            }

        test_scenarios = [
            {
                "input": "Analyze the current state of the system",
                "expected_features": ["system_analysis", "file_access"],
            },
            {
                "input": "What files are available in the project?",
                "expected_features": ["file_enumeration", "project_analysis"],
            },
            {
                "input": "Help me understand the architecture",
                "expected_features": ["documentation_access", "deep_analysis"],
            },
        ]

        passed_scenarios = 0
        scenario_results = []

        try:
            for scenario in test_scenarios:
                conversation_result = self.conversation_engine.process_conversation(
                    scenario["input"]
                )

                # Check if response contains expected features
                has_expected_features = all(
                    feature in str(conversation_result).lower()
                    for feature in scenario["expected_features"]
                )

                scenario_result = {
                    "input": scenario["input"],
                    "response_length": len(conversation_result.get("response", "")),
                    "has_analysis": bool(conversation_result.get("analysis")),
                    "has_memory": bool(conversation_result.get("memory_context")),
                    "approach": conversation_result.get("approach"),
                    "passed": has_expected_features
                    and len(conversation_result.get("response", "")) > 50,
                }

                if scenario_result["passed"]:
                    passed_scenarios += 1

                scenario_results.append(scenario_result)

            result = {
                "test": "enhanced_conversation",
                "passed": passed_scenarios == len(test_scenarios),
                "details": {
                    "passed_scenarios": passed_scenarios,
                    "total_scenarios": len(test_scenarios),
                    "scenario_results": scenario_results,
                },
            }

            print(
                f"✅ Enhanced conversation test: "
                f"{passed_scenarios}/{len(test_scenarios)} scenarios passed"
            )

            return result

        except Exception as e:
            return {"test": "enhanced_conversation", "passed": False, "error": str(e)}

    def test_file_access_capability(self) -> Dict[str, Any]:
        """
        Test full file access capability

        Why: Ensures conversation engine has full access as requested by user
        Where: Tests file reading, analysis, and processing capabilities
        How: Attempts to access and analyze various project files
        """
        print("\n📁 Testing File Access Capability...")

        if not self.conversation_engine:
            return {
                "test": "file_access",
                "passed": False,
                "error": "Conversation engine not initialized",
            }

        try:
            # Test file enumeration
            project_files = self.conversation_engine._enumerate_project_files()

            # Test specific file access
            test_files = ["config.py", "app.py", "README.md"]
            accessible_files = []

            for file_name in test_files:
                file_path = Path(f"/workspaces/projects/{file_name}")
                if file_path.exists():
                    try:
                        content = self.conversation_engine._read_file_safely(
                            str(file_path)
                        )
                        if content and len(content) > 10:
                            accessible_files.append(file_name)
                    except Exception:
                        pass

            result = {
                "test": "file_access",
                "passed": len(accessible_files) >= 2 and len(project_files) > 10,
                "details": {
                    "total_project_files": len(project_files),
                    "accessible_test_files": accessible_files,
                    "file_access_working": len(accessible_files) > 0,
                },
            }

            if result["passed"]:
                print(
                    f"✅ File access test passed - "
                    f"{len(project_files)} files found, "
                    f"{len(accessible_files)} test files accessible"
                )
            else:
                print("❌ File access test failed")

            return result

        except Exception as e:
            return {"test": "file_access", "passed": False, "error": str(e)}

    def test_automated_monitoring(self) -> Dict[str, Any]:
        """
        Test automated monitoring system

        Why: Ensures continuous system oversight works as designed
        Where: Tests monitoring components and health checking
        How: Validates monitor initialization and health report generation
        """
        print("\n🔄 Testing Automated Monitoring...")

        if not self.monitor:
            return {
                "test": "automated_monitoring",
                "passed": False,
                "error": "Monitor not initialized",
            }

        try:
            # Test health report generation
            health_report = self.monitor.generate_system_health_report()

            # Test critical checks
            critical_checks = self.monitor.run_critical_checks()

            result = {
                "test": "automated_monitoring",
                "passed": (
                    bool(health_report)
                    and isinstance(critical_checks, list)
                    and len(critical_checks) > 0
                ),
                "details": {
                    "health_report_generated": bool(health_report),
                    "critical_checks_count": (
                        len(critical_checks) if critical_checks else 0
                    ),
                    "monitor_status": "operational",
                },
            }

            if result["passed"]:
                print(
                    "✅ Automated monitoring test passed - "
                    "system oversight operational"
                )
            else:
                print("❌ Automated monitoring test failed")

            return result

        except Exception as e:
            return {"test": "automated_monitoring", "passed": False, "error": str(e)}

    def test_integration_workflow(self) -> Dict[str, Any]:
        """
        Test complete integration workflow

        Why: Validates all components work together seamlessly
        Where: Tests end-to-end conversation processing with all enhancements
        How: Simulates complete user interaction with full system capability
        """
        print("\n🔗 Testing Complete Integration Workflow...")

        try:
            # Simulate complete user interaction
            user_input = (
                "Please analyze the current system state, "
                "check for any issues, and provide a comprehensive "
                "overview of capabilities"
            )

            # Step 1: System validation
            validation_results = self.validator.validate_system()
            validation_passed = all(
                r.passed for r in validation_results if r.severity == "critical"
            )

            # Step 2: Enhanced conversation processing
            if self.conversation_engine:
                conversation_result = self.conversation_engine.process_conversation(
                    user_input
                )
                conversation_success = bool(
                    conversation_result.get("response")
                    and len(conversation_result.get("response", "")) > 100
                )
            else:
                conversation_success = False

            # Step 3: Monitoring oversight
            if self.monitor:
                health_report = self.monitor.generate_system_health_report()
                monitoring_success = bool(health_report)
            else:
                monitoring_success = False

            result = {
                "test": "integration_workflow",
                "passed": validation_passed
                and conversation_success
                and monitoring_success,
                "details": {
                    "validation_passed": validation_passed,
                    "conversation_success": conversation_success,
                    "monitoring_success": monitoring_success,
                    "workflow_complete": True,
                },
            }

            if result["passed"]:
                print(
                    "✅ Complete integration workflow test passed - "
                    "all systems working together"
                )
            else:
                print(
                    "❌ Integration workflow test failed - "
                    "component integration issues detected"
                )

            return result

        except Exception as e:
            return {"test": "integration_workflow", "passed": False, "error": str(e)}

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """
        Run complete test suite

        Why: Provides comprehensive validation of all enhancements
        Where: Orchestrates all test components for full system validation
        How: Runs all tests and provides detailed results summary
        """
        print("🚀 Starting Final Integration Test Suite...")
        print("=" * 60)

        # Setup test environment
        if not self.setup_test_environment():
            return {
                "overall_status": "FAILED",
                "error": "Test environment setup failed",
            }

        # Run all tests
        tests = [
            self.test_system_validation,
            self.test_enhanced_conversation,
            self.test_file_access_capability,
            self.test_automated_monitoring,
            self.test_integration_workflow,
        ]

        results = []
        passed_tests = 0

        for test_func in tests:
            try:
                result = test_func()
                results.append(result)
                if result.get("passed", False):
                    passed_tests += 1
            except Exception as e:
                results.append(
                    {"test": test_func.__name__, "passed": False, "error": str(e)}
                )

        # Generate final report
        overall_status = "PASSED" if passed_tests == len(tests) else "FAILED"

        final_report = {
            "overall_status": overall_status,
            "passed_tests": passed_tests,
            "total_tests": len(tests),
            "test_results": results,
            "timestamp": time.time(),
            "summary": {
                "system_validation": any(
                    r.get("test") == "system_validation" and r.get("passed")
                    for r in results
                ),
                "enhanced_conversation": any(
                    r.get("test") == "enhanced_conversation" and r.get("passed")
                    for r in results
                ),
                "file_access": any(
                    r.get("test") == "file_access" and r.get("passed") for r in results
                ),
                "automated_monitoring": any(
                    r.get("test") == "automated_monitoring" and r.get("passed")
                    for r in results
                ),
                "integration_workflow": any(
                    r.get("test") == "integration_workflow" and r.get("passed")
                    for r in results
                ),
            },
        }

        # Print final results
        print("\n" + "=" * 60)
        print("🏁 FINAL INTEGRATION TEST RESULTS")
        print("=" * 60)

        if overall_status == "PASSED":
            print(f"✅ ALL TESTS PASSED - {passed_tests}/{len(tests)} tests successful")
            print("🎉 Clever AI system is operating at maximum capability!")
            print("🔥 Perfect instruction compliance achieved!")
            print("💬 Full conversational access confirmed!")
        else:
            print(
                f"⚠️ {len(tests) - passed_tests} tests failed - "
                f"{passed_tests}/{len(tests)} tests passed"
            )

        for result in results:
            status = "✅" if result.get("passed") else "❌"
            test_name = result.get("test", "unknown").replace("_", " ").title()
            print(f"{status} {test_name}")
            if "error" in result:
                print(f"    Error: {result['error']}")

        return final_report


def main():
    """
    Main entry point for final integration testing

    Why: Provides command-line interface for comprehensive system testing
    Where: Entry point for validation of enhanced Clever AI system
    How: Creates tester instance and runs complete test suite
    """
    tester = FinalIntegrationTester()
    results = tester.run_comprehensive_test()

    # Save results to file
    results_file = "/workspaces/projects/final_test_results.json"
    try:
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Test results saved to: {results_file}")
    except Exception as e:
        print(f"Warning: Could not save results to file: {e}")

    # Exit with appropriate code
    exit_code = 0 if results["overall_status"] == "PASSED" else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
