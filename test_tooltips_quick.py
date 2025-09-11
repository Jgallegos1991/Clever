#!/usr/bin/env python3
"""
Quick UI Tooltip Test Runner
Runs only the tooltip-related tests for fast validation
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run UI tooltip tests quickly"""
    print("🔍 Quick UI Tooltip Test")
    print("=" * 30)
    
    try:
        # Run built-in tooltip tests
        from tests.test_ui_functionality import run_ui_tooltip_tests
        results = run_ui_tooltip_tests()
        
        print(f"Status: {results['status'].upper()}")
        print(f"Tests: {results['passed']}/{results['total']} passed")
        
        if results['status'] == 'passed':
            print("✅ All tooltip tests passed!")
            
            # Show summary
            for test_name, test_result in results['tests'].items():
                if test_result['status'] == 'passed':
                    details = test_result['details']
                    if 'total_buttons' in details:
                        print(f"   ✅ {details['total_buttons']} buttons checked")
                    elif 'patterns_found' in details:
                        print(f"   ✅ {len(details['patterns_found'])} button patterns validated")
                    elif 'files_checked' in details:
                        print(f"   ✅ {details['files_checked']} template files validated")
            
            print("\n🎯 Summary:")
            print("   • All buttons have descriptive tooltips")
            print("   • Consistent tooltip patterns across templates")
            print("   • Proper accessibility attributes")
            print("   • Valid HTML structure")
            
            return True
        else:
            print("❌ Some tooltip tests failed:")
            for test_name, test_result in results['tests'].items():
                if test_result['status'] == 'failed':
                    print(f"   ❌ {test_name}")
                    details = test_result['details']
                    if 'missing_tooltips' in details and details['missing_tooltips']:
                        print(f"      Missing tooltips: {len(details['missing_tooltips'])}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tooltip tests: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
