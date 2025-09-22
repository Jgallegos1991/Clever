"""
Test Suite for Sanitizer Functions

Why: To ensure that the text sanitization functions, which are critical for
     cleaning AI-generated output before it's presented to the user, are
     working correctly. This prevents internal metadata or undesirable
     artifacts from leaking into the final response.
Where: This test module is part of the project's test suite and is executed
       during automated testing (e.g., via `make test`). It specifically
       targets the `_sanitize_persona_text` function.
How: It defines a series of test cases with sample raw text containing various
     meta-markers and asserts that the sanitized output does not contain
     these markers, while still retaining the core conversational content.

Connects to:
    - app.py:
        - Imports and tests the `_sanitize_persona_text` function.
"""

import re
from app import _sanitize_persona_text

def test_sanitizer_removes_meta_markers():
    raw = (
        "Noted— you're reflecting on hey— balanced starting point. "
        "Time-of-day: afternoon; focal lens: essence. Vector: 1.15 complexity index. "
        "Earlier we touched on 'clev' which resonates here."
    )
    cleaned = _sanitize_persona_text(raw)
    banned = ["Time-of-day", "focal lens", "Vector:", "complexity index", "essence:"]
    for b in banned:
        assert b.lower() not in cleaned.lower()
    # Should still retain core conversational opening
    assert "balanced starting point" in cleaned
