"""Pytest configuration for Clever tests.

Why: Ensure local project modules (e.g., persona.py) are importable during tests
without requiring installation as a package. Pytest sometimes adjusts sys.path
based on invocation context; we explicitly prepend repo root.
Where: Automatically discovered by pytest in tests/ directory.
How: Inserts absolute repository root into sys.path at position 0 early.

Connects to:
    - persona.py, nlp_processor.py, memory_engine.py: imported directly in tests
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    # Why: Prepend root for direct module imports (single-file modules not in a package)
    sys.path.insert(0, str(ROOT))