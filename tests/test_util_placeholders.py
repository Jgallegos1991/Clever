"""Tests for placeholder utility modules summarize_repo and self_fix.

Why:
    Ensure placeholder utilities maintain stable return contracts so downstream
    experimental integrations or UI components can rely on them without fear of
    silent shape changes.
Where:
    Runs in the standard pytest suite (tests/). Validates tools layer utilities
    that are currently stubs but documented and intended for future expansion.
How:
    Imports summarize() and plan_self_fixes() and asserts minimal structural
    invariants (types, required keys). Keeps assertions intentionally lenient to
    avoid over-constraining future evolution while still catching regressions.

Connects to:
    - tools/summarize_repo.py: summarize() API contract
    - utils/self_fix.py: plan_self_fixes() return shape
"""
from __future__ import annotations

from tools.summarize_repo import summarize
from utils.self_fix import plan_self_fixes


def test_summarize_min_shape():
    data = summarize()
    assert isinstance(data, dict)
    assert "root" in data and isinstance(data["root"], str)
    assert "top_level_count" in data and isinstance(data["top_level_count"], int)


def test_plan_self_fixes_shape():
    fixes = plan_self_fixes()
    assert isinstance(fixes, list)
    assert fixes, "Expected at least one planned fix placeholder"
    for fx in fixes:
        assert isinstance(fx, dict)
        assert {"action", "reason", "risk"}.issubset(fx.keys())
