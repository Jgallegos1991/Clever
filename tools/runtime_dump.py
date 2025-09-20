"""Runtime snapshot dump utility.

Why: Provide a quick offline CLI method to visualize the same reasoning
"arrows" (Why/Where/How + recent renders) available via the debug overlay
without needing a browser session.
Where: Invoked manually: `python -m tools.runtime_dump` from project root.
How: Imports the Flask app, triggers a render of `'/'` if none recorded, then
prints JSON snapshot from `runtime_state` to stdout.

Connects to:
    - app.py: Imports app + persona engine
    - introspection.py: runtime_state aggregator
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
