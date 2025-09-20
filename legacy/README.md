Legacy Modules Archive
======================

Why: These files contained merge artifacts, duplicated definitions, or syntax issues.
They are preserved here for reference while the active codebase uses simplified or
refactored replacements to maintain a clean, runnable state.

Modules archived:
- clever_conversation_engine.py (duplicate methods, structural corruption)
- knowledge_base_full.py (mixed schemas, indentation errors)
- utils_watcher_full.py (duplicate docstrings, conflict markers)
- test_suite_full.py (invalid Python syntax in DB tests)
- fixer_legacy.py (retained original for audit; active version simplified or pending refactor)
- run_tests_legacy.py (superseded by pytest usage)

All legacy files are excluded from lint and not imported at runtime.
