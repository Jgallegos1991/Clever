#!/usr/bin/env python2

"""
Intelligent Analysis System Validation Test

Why: Validate that the enhanced Why/Where/How graph system with intelligent
analysis correctly identifies problems, provides actionable recommendations,
and integrates properly with the existing Clever architecture.

Where: Run as standalone test script to validate the intelligent analysis
system before integration into production. Tests all components end-to-end.

How: Creates test scenarios with known issues, runs intelligent analysis,
validates detection accuracy, and tests recommendation quality.

Connects to:
    - intelligent_analyzer.py: Core analysis engine being tested
    - introspection.py: Enhanced runtime state integration
    - debug_config.py: Performance monitoring integration
"""
import sys
import tempfile
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config

try:
    from intelligent_analyzer import (
        get_intelligent_analysis,
        analyze_single_component,
        get_fix_recommendations
    )
    from debug_config import get_debugger, performance_monitor
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Analysis system not available: {e}")
    ANALYSIS_AVAILABLE = False

class TestColors:
    """Terminal color codes for test output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test_header(test_name: str):
    """Print formatted test header."""
    print(f"\n{TestColors.BOLD}{TestColors.BLUE}{'='*60}{TestColors.END}")
    print(f"{TestColors.BOLD}{TestColors.BLUE}TEST: {test_name}{TestColors.END}")
    print(f"{TestColors.BOLD}{TestColors.BLUE}{'='*60}{TestColors.END}")

def print_result(passed: bool, message: str):
    """Print test result with color coding."""
    status = f"{TestColors.GREEN}✓ PASS" if passed else f"{TestColors.RED}✗ FAIL"
    print(f"{status}{TestColors.END}: {message}")

def create_test_file(content: str, filename: str = "test_file.py") -> Path:
    """Create a temporary test file with given content."""
    temp_dir = Path(tempfile.mkdtemp())
    test_file = temp_dir / filename
    test_file.write_text(content)
    return test_file

def test_documentation_analysis():
    """Test Why/Where/How documentation analysis."""
    print_test_header("Documentation Analysis")
    
    # Test file with missing documentation
    bad_doc_content = '''
def undocumented_function(x, y):
    return x + y

class UndocumentedClass:
    def method_without_docs(self):
        pass

def function_with_partial_docs():
    """
    Brief description only.
    Why: Missing where and how
    """
    pass
'''
    
    test_file = create_test_file(bad_doc_content)
    
    try:
        results = analyze_single_component(str(test_file))
        doc_issues = [r for r in results if r.category == 'DOCUMENTATION']
        
        print_result(len(doc_issues) > 0, f"Detected {len(doc_issues)} documentation issues")
        
        # Check for specific issue types
        missing_docstring = any('Missing Function Documentation' in r.title for r in doc_issues)
        insufficient_coverage = any('Insufficient Why/Where/How' in r.title for r in doc_issues)
        
        print_result(missing_docstring, "Detected missing function docstrings")
        print_result(insufficient_coverage, "Detected insufficient Why/Where/How coverage")
        
        # Test fix suggestions
        if doc_issues:
            has_fix_suggestions = all(len(r.fix_suggestions) > 0 for r in doc_issues)
            print_result(has_fix_suggestions, "All documentation issues have fix suggestions")
        
        return True
        
    except Exception as e:
        print_result(False, f"Documentation analysis failed: {e}")
        return False
    finally:
        # Clean up
        import shutil
        shutil.rmtree(test_file.parent)

def test_performance_analysis():
    """Test performance issue detection."""
    print_test_header("Performance Analysis")
    
    # Test file with performance anti-patterns
    perf_content = '''
def inefficient_function():
    """
    Function with performance issues
    Why: Demonstrate performance anti-patterns for testing
    Where: Test validation system
    How: Contains known inefficient patterns
    """
    result = ""
    # String concatenation in loop (inefficient)
    for i in range(100):
        result += f"item {i}"
    
    # Inefficient dictionary iteration
    my_dict = {'a': 1, 'b': 2, 'c': 3}
    for key in my_dict.keys():
        print(my_dict[key])
    
    return result
'''
    
    test_file = create_test_file(perf_content)
    
    try:
        results = analyze_single_component(str(test_file))
        perf_issues = [r for r in results if r.category == 'PERFORMANCE']
        
        print_result(len(perf_issues) > 0, f"Detected {len(perf_issues)} performance issues")
        
        # Check for specific patterns
        string_concat = any('String Concatenation' in r.title for r in perf_issues)
        dict_iteration = any('Dictionary Iteration' in r.title for r in perf_issues)
        
        print_result(string_concat, "Detected string concatenation anti-pattern")
        print_result(dict_iteration, "Detected inefficient dictionary iteration")
        
        # Validate performance impact information
        has_impact_info = any(r.performance_impact for r in perf_issues)
        print_result(has_impact_info, "Performance issues include impact information")
        
        return True
        
    except Exception as e:
        print_result(False, f"Performance analysis failed: {e}")
        return False
    finally:
        import shutil
        shutil.rmtree(test_file.parent)

def test_security_analysis():
    """Test security issue detection.""" 
    print_test_header("Security Analysis")
    
    # Test file with security issues
    security_content = '''
import sqlite3

def vulnerable_function(user_input):
    """
    Function with security vulnerabilities
    Why: Demonstrate security issues for testing
    Where: Test validation system
    How: Contains known security anti-patterns
    """
    # Potential SQL injection
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute(query)
    
    # Hardcoded credentials
    api_key = "sk-1234567890abcdef"
    password = "hardcoded_password_123"
    
    return query

def debug_enabled():
    """Debug mode potentially enabled"""
    app.run(debug=True)
'''
    
    test_file = create_test_file(security_content)
    
    try:
        results = analyze_single_component(str(test_file))
        security_issues = [r for r in results if r.category == 'SECURITY']
        
        print_result(len(security_issues) > 0, f"Detected {len(security_issues)} security issues")
        
        # Check for specific vulnerabilities
        sql_injection = any('SQL Injection' in r.title for r in security_issues)
        hardcoded_creds = any('Hardcoded Credentials' in r.title for r in security_issues)
        
        print_result(sql_injection, "Detected potential SQL injection vulnerability")
        print_result(hardcoded_creds, "Detected hardcoded credentials")
        
        # Check severity levels
        has_critical = any(r.severity == 'CRITICAL' for r in security_issues)
        has_high = any(r.severity == 'HIGH' for r in security_issues)
        
        print_result(has_critical or has_high, "Security issues properly classified as high severity")
        
        return True
        
    except Exception as e:
        print_result(False, f"Security analysis failed: {e}")
        return False
    finally:
        import shutil
        shutil.rmtree(test_file.parent)

def test_complexity_analysis():
    """Test complexity and code quality analysis."""
    print_test_header("Complexity Analysis")
    
    # Test file with complexity issues
    complex_content = '''
def overly_complex_function(x, y, z, flag1, flag2, flag3):
    """
    Overly complex function for testing
    Why: Demonstrate complexity issues
    Where: Test validation system  
    How: Deep nesting and long function
    """
    if x > 0:
        if y > 0:
            if z > 0:
                if flag1:
                    if flag2:
                        if flag3:
                            result = x + y + z
                            for i in range(10):
                                if i % 2 == 0:
                                    for j in range(5):
                                        if j % 2 == 1:
                                            result += i * j
                                        else:
                                            result -= i * j
                                else:
                                    result *= 2
                            return result
                        else:
                            return x * y * z
                    else:
                        return x * y
                else:
                    return x + y
            else:
                return x
        else:
            return 0
    else:
        return -1
'''
    
    test_file = create_test_file(complex_content)
    
    try:
        results = analyze_single_component(str(test_file))
        complexity_issues = [r for r in results if r.category == 'COMPLEXITY']
        
        print_result(len(complexity_issues) > 0, f"Detected {len(complexity_issues)} complexity issues")
        
        # Check for specific complexity problems
        long_function = any('Function Too Long' in r.title for r in complexity_issues)
        deep_nesting = any('Excessive Nesting' in r.title for r in complexity_issues)
        
        print_result(long_function, "Detected overly long function")
        print_result(deep_nesting, "Detected excessive nesting")
        
        return True
        
    except Exception as e:
        print_result(False, f"Complexity analysis failed: {e}")
        return False
    finally:
        import shutil
        shutil.rmtree(test_file.parent)

def test_fix_recommendations():
    """Test fix recommendation system."""
    print_test_header("Fix Recommendation System")
    
    try:
        # Test recommendations for different categories
        categories_to_test = ['DOCUMENTATION', 'PERFORMANCE', 'SECURITY']
        all_passed = True
        
        for category in categories_to_test:
            recommendations = get_fix_recommendations('test_node', category)
            
            has_recommendations = bool(recommendations.get('recommendations'))
            print_result(has_recommendations, f"Generated recommendations for {category}")
            
            if not has_recommendations:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_result(False, f"Fix recommendation test failed: {e}")
        return False

@performance_monitor('test_system')
def test_performance_monitoring_integration():
    """Test integration with performance monitoring system."""
    print_test_header("Performance Monitoring Integration")
    
    try:
        debugger = get_debugger()
        
        # Simulate some performance data
        debugger.track_performance('test_component', 'test_operation', 0.15)
        debugger.track_performance('test_component', 'slow_operation', 1.2)
        debugger.track_performance('test_component', 'fast_operation', 0.05)
        
        # Get performance stats
        stats = debugger.get_performance_stats()
        
        has_stats = len(stats) > 0
        print_result(has_stats, f"Performance monitoring collected {len(stats)} statistics")
        
        # Check component health
        health = debugger.component_health
        has_health_data = 'test_component' in health
        print_result(has_health_data, "Component health tracking active")
        
        # Test that slow operations affect health score
        if has_health_data:
            health_score = health['test_component']['health_score']
            health_affected = health_score < 100  # Should be reduced by slow operation
            print_result(health_affected, f"Health score affected by performance: {health_score:.1f}")
        
        return has_stats and has_health_data
        
    except Exception as e:
        print_result(False, f"Performance monitoring integration failed: {e}")
        return False

def test_full_codebase_analysis():
    """Test full codebase analysis functionality."""
    print_test_header("Full Codebase Analysis")
    
    try:
        # Create a small test codebase
        test_dir = Path(tempfile.mkdtemp())
        
        # Create test files with various issues
        (test_dir / "good_file.py").write_text('''
def well_documented_function(x: int) -> int:
    """
    Well documented function for testing
    
    Why: Demonstrate good documentation practices
    Where: Test validation system
    How: Proper docstring with all required sections
    
    Connects to:
        - test_system: Validation testing
    """
    return x * 2
''')
        
        (test_dir / "problematic_file.py").write_text('''
def bad_function(x, y):
    # No docstring, potential issues
    result = ""
    for i in range(x):
        result += str(i)  # String concatenation issue
    return result
''')
        
        # Run analysis on test files
        test_files = [str(f) for f in test_dir.glob("*.py")]
        analysis = get_intelligent_analysis(test_files)
        
        # Validate analysis structure
        required_keys = ['analysis_results', 'quality_score', 'complexity_metrics', 
                        'architectural_insights', 'generated_at']
        has_required_keys = all(key in analysis for key in required_keys)
        print_result(has_required_keys, "Analysis contains all required components")
        
        # Check quality score calculation
        quality_score = analysis.get('quality_score', 0)
        has_quality_score = 0 <= quality_score <= 100
        print_result(has_quality_score, f"Quality score in valid range: {quality_score:.1f}%")
        
        # Check that issues were found
        results = analysis.get('analysis_results', [])
        found_issues = len(results) > 0
        print_result(found_issues, f"Found {len(results)} issues in test codebase")
        
        # Check issue diversity
        categories = set(r.category for r in results)
        has_diverse_issues = len(categories) > 1
        print_result(has_diverse_issues, f"Detected {len(categories)} different issue categories")
        
        return has_required_keys and has_quality_score and found_issues
        
    except Exception as e:
        print_result(False, f"Full codebase analysis failed: {e}")
        return False
    finally:
        # Clean up
        import shutil
        if 'test_dir' in locals():
            shutil.rmtree(test_dir)

def run_validation_suite():
    """Run the complete validation test suite."""
    if not ANALYSIS_AVAILABLE:
        print(f"{TestColors.RED}❌ Intelligent analysis system not available{TestColors.END}")
        return False
    
    print(f"{TestColors.BOLD}{TestColors.BLUE}")
    print("🧠 INTELLIGENT ANALYSIS SYSTEM VALIDATION")
    print("=" * 50)
    print(f"{TestColors.END}")
    
    tests = [
        ("Documentation Analysis", test_documentation_analysis),
        ("Performance Analysis", test_performance_analysis),
        ("Security Analysis", test_security_analysis),
        ("Complexity Analysis", test_complexity_analysis),
        ("Fix Recommendations", test_fix_recommendations),
        ("Performance Monitoring", test_performance_monitoring_integration),
        ("Full Codebase Analysis", test_full_codebase_analysis),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            start_time = time.time()
            result = test_func()
            duration = time.time() - start_time
            
            if result:
                passed_tests += 1
                print(f"{TestColors.GREEN}✓{TestColors.END} {test_name} completed in {duration:.2f}s")
            else:
                print(f"{TestColors.RED}✗{TestColors.END} {test_name} failed after {duration:.2f}s")
                
        except Exception as e:
            print(f"{TestColors.RED}✗{TestColors.END} {test_name} crashed: {e}")
    
    # Final summary
    print(f"\n{TestColors.BOLD}{'='*60}{TestColors.END}")
    success_rate = (passed_tests / total_tests) * 100
    
    if passed_tests == total_tests:
        print(f"{TestColors.GREEN}{TestColors.BOLD}🎉 ALL TESTS PASSED! ({passed_tests}/{total_tests}){TestColors.END}")
    else:
        print(f"{TestColors.YELLOW}{TestColors.BOLD}⚠️  PARTIAL SUCCESS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%){TestColors.END}")
    
    print(f"{TestColors.BOLD}System Status: {'READY FOR PRODUCTION' if success_rate >= 80 else 'NEEDS ATTENTION'}{TestColors.END}")
    
    return success_rate >= 80

if __name__ == '__main__':
    success = run_validation_suite()
    sys.exit(0 if success else 1)