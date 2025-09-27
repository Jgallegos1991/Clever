"""
Minimal test suite shim (prefer pytest in tests/)

Why:
    The previous monolithic test suite had unstable optional dependencies and
    overlapping concerns. We now default to pytest tests under tests/ for
    detailed coverage. This module remains to preserve a stable API for
    run_tests.py and any legacy scripts.
Where:
    Used by run_tests.py to run a lightweight smoke check.
How:
    Provides CleverTestSuite with only core database/knowledge smoke tests.

Connects to:
    - run_tests.py: Main test runner interface
    - database.py: Database connectivity and integrity tests
    - debug_config.py: Logging and debugging capabilities
    - pytest tests/: Modern test suite with comprehensive coverage
"""

import sqlite3
from datetime import datetime
from typing import Dict, Any
from debug_config import get_debugger


class CleverTestSuite:
    """Lightweight, reliable smoke tests.
    
    Why: Keep CI green and fast while deeper tests run under pytest.
    Where: Used by run_tests.py and optional CI stages.
    How: Runs a small set of deterministic checks (DB + knowledge_base shim).
    """

    def __init__(self):
        self.debugger = get_debugger()
        self.test_results: Dict[str, Any] = {}
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.debugger.info('test_suite', 'Minimal Clever Test Suite initialized')

    def run_all_tests(self) -> Dict[str, Any]:
        """Run reduced core tests only."""
        self.start_time = datetime.now()
        self.debugger.info('test_suite', 'Starting minimal test suite')

        categories = [('database_tests', self.test_database_components)]

        overall_status = 'passed'
        total_tests = 0
        passed_tests = 0

        for name, func in categories:
            try:
                self.debugger.info('test_suite', f'Running {name}')
                res = func()
                self.test_results[name] = res
                total_tests += res.get('total', 0)
                passed_tests += res.get('passed', 0)
                if res.get('status') != 'passed':
                    overall_status = 'failed'
            except Exception as _e:
                self.debugger.error('test_suite', f'Category {name} failed', {'error': str(e)})
                self.test_results[name] = {'status': 'error', 'error': str(e), 'total': 0, 'passed': 0, 'failed': 1}
                overall_status = 'failed'

        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0.0
        return {
            'overall_status': overall_status,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / max(1, total_tests)) * 100,
            'duration_seconds': duration,
            'timestamp': (self.end_time or datetime.now()).isoformat(),
            'categories': self.test_results,
        }
    
    def test_database_components(self) -> Dict[str, Any]:
        """Test core database and knowledge_base shim functionality.
        
        Why: Ensure DB connectivity and basic interaction logging works.
        """
        tests: list[dict] = []
        # Connection test via DatabaseManager and raw sqlite3
        try:
            from config import DB_PATH
            from database import DatabaseManager
            with DatabaseManager(DB_PATH)._connect() as con:
                con.execute('SELECT 1')
            with sqlite3.connect('clever.db') as con2:
                con2.execute('SELECT 1')
            tests.append({'name': 'database_connection', 'status': 'passed'})
        except Exception as _e:
            tests.append({'name': 'database_connection', 'status': 'failed', 'error': str(e)})

        # Knowledge base shim: init + log + read
        try:
            from knowledge_base import init_db, log_interaction, get_recent_interactions
            assert init_db() is True
            log_interaction("Test message", "Test response")
            recent = get_recent_interactions(limit=1)
            ok = bool(recent and isinstance(recent, list))
            tests.append({'name': 'knowledge_base_basic', 'status': 'passed' if ok else 'failed'})
        except Exception as _e:
            tests.append({'name': 'knowledge_base_basic', 'status': 'failed', 'error': str(e)})

        passed = sum(1 for t in tests if t['status'] == 'passed')
        total = len(tests)
        return {
            'status': 'passed' if passed == total else 'failed',
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'tests': tests,
        }
    

_TEST_SUITE_SINGLETON: CleverTestSuite | None = None

def get_test_suite() -> CleverTestSuite:
    """Return a singleton CleverTestSuite instance."""
    global _TEST_SUITE_SINGLETON
    if _TEST_SUITE_SINGLETON is None:
        _TEST_SUITE_SINGLETON = CleverTestSuite()
    return _TEST_SUITE_SINGLETON

def run_quick_tests() -> Dict[str, Any]:
    """Run a quick subset of tests.

    Only includes the database/knowledge smoke test to avoid optional
    dependencies and keep this shim deterministic.
    """
    suite = get_test_suite()
    critical_tests = {'database': suite.test_database_components()}
    total_passed = sum(result['passed'] for result in critical_tests.values())
    total_tests = sum(result['total'] for result in critical_tests.values())

    return {
        'status': 'passed' if total_passed == total_tests else 'failed',
        'total_tests': total_tests,
        'passed_tests': total_passed,
        'success_rate': (total_passed / max(1, total_tests)) * 100,
        'results': critical_tests
    }
