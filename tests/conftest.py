"""
conftest.py - Pytest configuration for Clever's cognitive partnership system tests

Why: Ensure local project modules (e.g., persona.py) are importable during tests
without requiring installation as a package. Pytest sometimes adjusts sys.path
based on invocation context; we explicitly prepend repo root. Essential for
testing Clever's cognitive partnership system components in isolation.

Where: Automatically discovered by pytest in tests/ directory. Core testing
infrastructure for Clever's digital brain extension system validation.

How: Inserts absolute repository root into sys.path at position 0 early in
test execution to ensure proper module resolution and import paths.

File Usage:
    - Test configuration: Primary pytest configuration for Clever's test suite
    - Module resolution: Ensures proper import paths for all Clever components
    - Test infrastructure: Foundation for all automated testing in cognitive partnership system
    - Development workflow: Critical for continuous integration and test automation
    - Quality assurance: Enables comprehensive testing of system components
    - CI/CD integration: Supports automated testing in build and deployment pipelines
    - Debugging support: Facilitates test debugging and development workflows
    - Regression testing: Enables comprehensive validation of system changes

Connects to:
    - All test files: Provides import configuration for entire test suite
    - persona.py: Personality engine testing with proper module imports
    - nlp_processor.py: Natural language processing component testing
    - memory_engine.py: Memory system testing and validation
    - evolution_engine.py: Learning system testing and cognitive enhancement validation
    - app.py: Main application testing and integration validation
    - database.py: Data persistence layer testing and validation
    - introspection.py: Runtime system testing and debugging validation
    - pytest.ini: Pytest configuration file complementing this setup
    - Makefile: Test execution commands using this configuration
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    # Why: Prepend root for direct module imports (single-file modules not in a package)
    sys.path.insert(0, str(ROOT))