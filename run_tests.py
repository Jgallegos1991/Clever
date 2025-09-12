#!/usr/bin/env python3
"""
Clever AI Test Runner

Why: Provides a unified entry point for running all test suites, including UI
tooltip tests, to ensure system reliability and feature coverage.
Where: Connects to tests/test_ui_functionality.py and other test modules.
How: Imports test modules, runs specific test functions, aggregates and prints
results for developer review.

Connects to:
    - tests/test_ui_functionality.py: Runs UI tooltip tests
    - Other test modules as imported
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tooltip_tests():
    """Run UI tooltip tests specifically"""
    print("🔍 Running UI Tooltip Tests...")
    
    try:
        from tests.test_ui_functionality import run_ui_tooltip_tests
        results = run_ui_tooltip_tests()
        
        print(f"📊 Tooltip Tests: {results['status'].upper()}")
        print(f"   Tests: {results['passed']}/{results['total']} passed")
        
        # Show detailed results
        for test_name, test_result in results['tests'].items():
            status_icon = "✅" if test_result['status'] == 'passed' else "❌" if test_result['status'] == 'failed' else "⚠️"
            print(f"   {status_icon} {test_name}: {test_result['status']}")
            
            if test_result['status'] == 'failed' and 'details' in test_result:
                details = test_result['details']
                if 'missing_tooltips' in details and details['missing_tooltips']:
                    print(f"      Missing tooltips: {len(details['missing_tooltips'])}")
                    for missing in details['missing_tooltips'][:3]:  # Show first 3
                        print(f"        - {missing['file']}: {missing['button_id']}")
                if 'inconsistencies' in details and details['inconsistencies']:
                    print(f"      Inconsistencies: {len(details['inconsistencies'])}")
                if 'accessibility_issues' in details and details['accessibility_issues']:
                    print(f"      Accessibility issues: {len(details['accessibility_issues'])}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error running tooltip tests: {e}")
        return {'status': 'error', 'error': str(e)}

def run_main_test_suite():
    """Run the main Clever test suite"""
    print("🚀 Running Main Test Suite...")
    
    try:
        from test_suite import get_test_suite
        test_suite = get_test_suite()
        results = test_suite.run_all_tests()
        
        print(f"📊 Main Suite: {results['overall_status'].upper()}")
        print(f"   Tests: {results['passed_tests']}/{results['total_tests']} passed")
        print(f"   Success Rate: {results['success_rate']:.1f}%")
        print(f"   Duration: {results['duration_seconds']:.2f}s")
        
        # Show category results
        for category, result in results['categories'].items():
            status_icon = "✅" if result['status'] == 'passed' else "❌" if result['status'] == 'failed' else "⚠️"
            print(f"   {status_icon} {category}: {result.get('passed', 0)}/{result.get('total', 0)} passed")
        
        return results
        
    except Exception as e:
        print(f"❌ Error running main test suite: {e}")
        return {'status': 'error', 'error': str(e)}

def run_pytest_tests():
    """Run pytest tests if available"""
    print("🧪 Checking for pytest tests...")
    
    try:
        import subprocess
        result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Pytest tests passed")
            print(result.stdout.split('\n')[-3:-1])  # Show summary lines
        else:
            print("❌ Pytest tests failed")
            print(result.stderr if result.stderr else result.stdout)
            
        return {
            'status': 'passed' if result.returncode == 0 else 'failed',
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print("⏰ Pytest tests timed out")
        return {'status': 'timeout'}
    except FileNotFoundError:
        print("⚠️  pytest not available, skipping")
        return {'status': 'skipped', 'reason': 'pytest not found'}
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return {'status': 'error', 'error': str(e)}

def create_test_report(tooltip_results, main_results, pytest_results):
    """Create a comprehensive test report"""
    timestamp = datetime.now().isoformat()
    
    report = {
        'timestamp': timestamp,
        'summary': {
            'tooltip_tests': tooltip_results.get('status', 'unknown'),
            'main_suite': main_results.get('overall_status', 'unknown'),
            'pytest': pytest_results.get('status', 'unknown')
        },
        'details': {
            'tooltip_tests': tooltip_results,
            'main_suite': main_results,
            'pytest': pytest_results
        }
    }
    
    # Save report
    report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Test report saved: {report_filename}")
    except Exception as e:
        print(f"⚠️  Could not save report: {e}")
    
    return report

def main():
    """Main test runner"""
    print("=" * 60)
    print("🧪 CLEVER AI COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Run all test categories
    tooltip_results = run_tooltip_tests()
    print()
    
    main_results = run_main_test_suite()
    print()
    
    pytest_results = run_pytest_tests()
    print()
    
    # Create comprehensive report
    print("📊 GENERATING TEST REPORT")
    print("=" * 30)
    
    report = create_test_report(tooltip_results, main_results, pytest_results)
    
    # Overall summary
    all_passed = (
        tooltip_results.get('status') == 'passed' and
        main_results.get('overall_status') == 'passed' and
        pytest_results.get('status') in ['passed', 'skipped']
    )
    
    print(f"🎯 OVERALL STATUS: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()
