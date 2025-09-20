"""Tests for file search intent handling in PersonaEngine.

Why: Ensure newly added capability (file location) functions correctly so
persona responses remain aligned with actionable behavior.
Where: Executed in CI test stage; guards regression in intent parse or
utility search logic.
How: Invoke PersonaEngine with representative queries and assert that
expected known repository files appear in the response payload.

Connects to:
  - persona.py:_maybe_handle_file_search
  - utils/file_search.py: search_files & search_by_extension
"""
from __future__ import annotations

from persona import PersonaEngine


def _response_lines(text: str):
    return [l.strip() for l in text.splitlines() if l.strip()]


def test_file_search_simple_python():
    p = PersonaEngine()
    resp = p.generate("find .py files about persona")
    lines = _response_lines(resp.text)
    # Expect persona.py to be referenced
    assert any('persona.py' in l for l in lines), f"persona.py not referenced in: {lines[:10]}"


def test_file_search_markdown_architecture():
    p = PersonaEngine()
    resp = p.generate("locate markdown files about architecture")
    lines = _response_lines(resp.text)
    # architecture.md should exist
    assert any('architecture.md' in l for l in lines), f"architecture.md not found in output: {lines[:10]}"


def test_file_search_no_results():
    p = PersonaEngine()
    resp = p.generate("find files with totallynonexistentpatternzzz")
    assert "didn't find" in resp.text.lower()
