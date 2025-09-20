"""
Runtime Introspection Utilities for Clever

Why: Provide a real-time window into what the system is rendering, which routes
are active, and the associated Why/Where/How reasoning metadata extracted from
docstrings. This converts the enforced documentation standard into actionable
observability for debugging UI/template issues, latency problems, or missing
persona integration.
Where: Imported by `app.py` to wrap template rendering and serve an
`/api/runtime_introspect` endpoint. Also consumed implicitly by any frontend
runtime overlay requesting JSON state.
How: Maintains in-memory registries for recent template renders, endpoint
metadata derived from Flask routes, parsed Why/Where/How sections, last error
captured by a global error handler, and lightweight git version discovery.

Connects to:
    - app.py: Provides decorators and helper functions used in route handlers
    - templates/index.html: Source of main render events tracked
    - static/js/main.js: Frontend can poll runtime introspection for overlay
"""
from __future__ import annotations
import inspect
import re
import threading
import time
from collections import deque
from typing import Any, Callable, Deque, Dict, List, Optional

# Regular expression to extract Why/Where/How sections from docstrings (case-insensitive)
_SECTION_RE = re.compile(r"^(why|where|how)\s*:\s*(.*)$", re.IGNORECASE)

# Thread-safe registries
_render_events: Deque[Dict[str, Any]] = deque(maxlen=50)
_registry_lock = threading.Lock()
_last_error: Optional[Dict[str, Any]] = None

# Cache for parsed docstring metadata keyed by object id
_doc_meta_cache: Dict[int, Dict[str, str]] = {}


def extract_doc_meta(obj: Any) -> Dict[str, str]:
    """Extract Why / Where / How sections from a callable or object docstring.

    Why: Converts enforced documentation tokens into structured data for live
    introspection, aiding debugging and transparency.
    Where: Used by runtime introspection endpoint to surface reasoning for
    routes and core functions.
    How: Parses the object's __doc__ line-by-line, capturing case-insensitive
    section headers (Why/Where/How) and aggregating multiline content until the
    next section or end of docstring. Results cached for efficiency.

    Args:
        obj: Any Python object (function/class/module) with a docstring.

    Returns:
        Dictionary containing 'why', 'where', 'how' keys (empty string if
        absent).
    """
    oid = id(obj)
    if oid in _doc_meta_cache:
        return _doc_meta_cache[oid]
    raw = inspect.getdoc(obj) or ""
    lines = [l.rstrip() for l in raw.splitlines()]
    current_key = None
    sections: Dict[str, List[str]] = {"why": [], "where": [], "how": []}
    for line in lines:
        m = _SECTION_RE.match(line.strip())
        if m:
            current_key = m.group(1).lower()
            sections[current_key].append(m.group(2).strip())
        else:
            if current_key and line.strip():
                sections[current_key].append(line.strip())
    meta = {k: " ".join(v).strip() for k, v in sections.items()}
    _doc_meta_cache[oid] = meta
    return meta


def record_render(template: str, route: str, duration_ms: float, context_size: int) -> None:
    """Record a template render event.

    Why: Build a rolling history of recent renders to pinpoint UI issues and
    confirm which template actually served a request.
    Where: Called by wrapper around Flask's render_template inside app.py.
    How: Appends a structured event dictionary to a deque with a thread lock.

    Args:
        template: Name of the template rendered.
        route: Flask route rule or request path.
        duration_ms: Duration of render call.
        context_size: Approximate size (len of keys) of the context mapping.
    """
    with _registry_lock:
        _render_events.append({
            "template": template,
            "route": route,
            "duration_ms": round(duration_ms, 3),
            "ts": time.time(),
            "context_size": context_size,
        })


def get_recent_renders() -> List[Dict[str, Any]]:
    """Return a list of recent render events (newest last)."""
    with _registry_lock:
        return list(_render_events)


def set_last_error(info: Dict[str, Any]) -> None:
    """Store the last captured error for introspection."""
    global _last_error
    with _registry_lock:
        _last_error = info


def get_last_error() -> Optional[Dict[str, Any]]:
    """Return last captured error dictionary or None."""
    with _registry_lock:
        return _last_error


def build_endpoints_snapshot(app) -> List[Dict[str, Any]]:
    """Collect metadata for all Flask endpoints (rules + Why/Where/How).

    Why: Provide a routing map with reasoning context to help trace request
    handling and quickly identify undocumented or divergent endpoints.
    Where: Executed within `/api/runtime_introspect` handler.
    How: Iterates over `app.url_map.iter_rules()`, inspects view functions,
    extracts doc meta, and structures a lightweight list.
    """
    snapshot = []
    for rule in app.url_map.iter_rules():
        endpoint = app.view_functions.get(rule.endpoint)
        if not endpoint:
            continue
        meta = extract_doc_meta(endpoint)
        snapshot.append({
            "rule": str(rule),
            "methods": sorted(m for m in rule.methods if m not in {"HEAD", "OPTIONS"}),
            "func": getattr(endpoint, "__name__", "<unknown>"),
            "module": getattr(endpoint, "__module__", "<unknown>"),
            "why": meta.get("why", ""),
            "where": meta.get("where", ""),
            "how": meta.get("how", ""),
        })
    snapshot.sort(key=lambda r: r["rule"])
    return snapshot


def detect_git_version() -> Optional[str]:
    """Attempt to read a short git commit hash (best-effort, offline safe)."""
    try:
        import subprocess  # Local import to avoid cost if not used
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return None


_GIT_HASH = detect_git_version()


def runtime_state(app, persona_engine=None) -> Dict[str, Any]:
    """Assemble full runtime introspection state.

    Why: Single aggregation point turning raw registries + persona context into
    a JSON-serializable snapshot for debugging overlays.
    Where: Returned by `/api/runtime_introspect` endpoint in `app.py`.
    How: Pulls recent renders, last error, endpoint metadata, persona mode, and
    version hash into one dictionary.
    """
    renders = get_recent_renders()
    last_render = renders[-1] if renders else None
    persona_mode = None
    if persona_engine is not None:
        # Attempt to read an internal current mode attribute if present
        persona_mode = getattr(persona_engine, "_last_mode", None) or getattr(persona_engine, "default_mode", None)
    return {
        "last_render": last_render,
        "recent_renders": renders,
        "endpoints": build_endpoints_snapshot(app),
        "persona_mode": persona_mode,
        "last_error": get_last_error(),
        "version": {"git": _GIT_HASH},
        "generated_ts": time.time(),
    }


def traced_render(app, template: str, route: str, render_func: Callable, **context):
    """Wrapper that records template render timing and delegates to Flask renderer.

    Why: Central interception point to know exactly which template produced the
    response for a route, enabling UI debugging tied to Why/Where/How metadata.
    Where: Used by `app.py` home route instead of calling `render_template` directly.
    How: Measures monotonic time around the render call, then records the event
    with context size for lightweight insight (no full serialization to avoid
    sensitive data exposure or overhead).
    """
    start = time.perf_counter()
    rv = render_func(template, **context)
    duration_ms = (time.perf_counter() - start) * 1000.0
    record_render(template, route=route, duration_ms=duration_ms, context_size=len(context))
    return rv


def register_error_handler(app):
    """Install a global error handler capturing exceptions for introspection."""
    @app.errorhandler(Exception)
    def _capture_error(e):  # type: ignore
        set_last_error({
            "type": type(e).__name__,
            "message": str(e),
            "ts": time.time(),
        })
        # Re-raise after capturing so default Flask debug still applies when debug=True
        raise e

    return app
