"""
runtime_dump.py - Runtime snapshot dump utility for Clever's cognitive partnership system

Why: Provide a quick offline CLI method to visualize the same reasoning
"arrows" (Why/Where/How + recent renders) available via the debug overlay
without needing a browser session. Essential for debugging Clever's cognitive
partnership system and understanding system state during development.

Where: Invoked manually: `python -m tools.runtime_dump` from project root.
Part of Clever's development toolkit for system introspection and debugging.

How: Imports the Flask app, triggers a render of `'/'` if none recorded, then
prints JSON snapshot from `runtime_state` to stdout for analysis.

File Usage:
    - CLI debugging: Primary tool for offline system state analysis and debugging
    - Development workflow: Used during development to understand system behavior
    - Troubleshooting: Consulted when debugging template rendering or system issues
    - Performance analysis: Used to analyze system performance and render metrics
    - Documentation validation: Helps verify Why/Where/How pattern compliance
    - System monitoring: Provides snapshot capabilities for system health analysis
    - Integration testing: Used to validate system state during automated testing
    - Error diagnosis: Helps identify system issues through runtime state inspection

Connects to:
    - app.py: Main Flask application and persona engine integration
    - introspection.py: Runtime state aggregation and system introspection
    - tools/: Development utilities ecosystem for system analysis
    - debug_config.py: System debugging and performance monitoring integration
    - persona.py: Personality engine state analysis and cognitive partnership insights
    - evolution_engine.py: Learning system state and interaction analysis
    - templates/index.html: Template rendering analysis and performance tracking
    - static/js/main.js: Frontend state correlation and debugging support
    - config.py: Configuration system integration for runtime analysis
"""
from __future__ import annotations
import json

from app import app, clever_persona  # type: ignore
from introspection import runtime_state, get_recent_renders


def ensure_initial_render():
    """Trigger a home render if no renders recorded yet.

    Why: runtime_state is more useful with at least one render event present.
    Where: Called only when executed via CLI before dumping snapshot.
    How: Uses test_request_context + calling the home route function.
    """
    if get_recent_renders():
        return
    with app.test_request_context('/'):
        app.view_functions['home']()  # call home handler directly


def main():
    ensure_initial_render()
    snapshot = runtime_state(app, persona_engine=clever_persona)
    print(json.dumps(snapshot, indent=2, sort_keys=True))


if __name__ == '__main__':  # pragma: no cover - manual tool entry
    main()
