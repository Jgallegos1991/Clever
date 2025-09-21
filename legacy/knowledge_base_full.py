"""Legacy full knowledge_base with schema corruption.

Why: The previous version mixed two different initialization flows and contained
indentation errors plus partial SQL statements. Archiving prior to rewrite.
Where: Moved to `legacy/` to isolate unstable logic from the active `knowledge_base.py`
implementation and prevent accidental import by production code paths.
How: File content intentionally minimized; original logic removed after capture in
version control history. Retained docstring documents rationale and directs future
audits to the modern module instead of restoring flawed code.

Connects to:
	- knowledge_base.py: Current stable implementation
	- evolution_engine.py: Consumes transformed knowledge entries (modern path only)
"""
