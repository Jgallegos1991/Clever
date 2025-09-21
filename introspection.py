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

# Threshold (ms) above which a render is flagged as slow. Chosen conservatively
# to surface potential server-side slowness before it becomes user-visible.
# This can be tuned; kept internal to avoid config sprawl. Typical fast render
# under light load should be < 25ms; we set 40ms as initial heuristic.
RENDER_SLOW_THRESHOLD_MS = 40.0


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
    slow = duration_ms >= RENDER_SLOW_THRESHOLD_MS
    with _registry_lock:
        _render_events.append({
            "template": template,
            "route": route,
            "duration_ms": round(duration_ms, 3),
            "slow": slow,
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


def _compute_warnings(endpoints: List[Dict[str, Any]]) -> List[str]:
    """Compute drift warnings for endpoints missing reasoning sections.

    Why: Proactively signal documentation drift (missing Why/Where/How) so the
    runtime overlay acts as early warning before CI enforcement or confusion.
    Where: Used inside runtime_state assembly prior to JSON response.
    How: Iterates endpoint metadata and emits human-readable notes when any
    section is blank; keeps list small for overlay readability.
    """
    warnings: List[str] = []
    for ep in endpoints:
        missing = [k for k in ("why", "where", "how") if not (ep.get(k) or '').strip()]
        if missing:
            warnings.append(f"Endpoint {ep.get('rule')} missing: {', '.join(missing)}")
    return warnings


def runtime_state(app, persona_engine=None) -> Dict[str, Any]:
    """Assemble full runtime introspection state.

    Why: Central aggregation converting docstring reasoning + live telemetry
    (renders, errors, evolution stats) into a navigational map—the "arrows"
    that show what connected to what, why, and how at the moment of inspection.
    Where: Returned by `/api/runtime_introspect` endpoint in `app.py`, consumed
    by optional frontend debug overlay and CLI snapshot tool.
    How: Gathers recent renders (with slow flag), endpoint reasoning metadata,
    persona mode, evolution interaction summary (best-effort), last error,
    version hash, computed drift warnings, and the render slow threshold for
    client display.

    Connects to:
        - evolution_engine.py: Interaction summary (if available)
        - app.py: Persona engine reference & endpoint registration
        - tools/runtime_dump.py: CLI dump utility
    """
    renders = get_recent_renders()
    last_render = renders[-1] if renders else None
    persona_mode = None
    if persona_engine is not None:
        # Attempt to read an internal current mode attribute if present
        persona_mode = getattr(persona_engine, "_last_mode", None) or getattr(persona_engine, "default_mode", None)
    endpoints = build_endpoints_snapshot(app)
    # Evolution summary (best-effort, never raises)
    evolution_summary: Optional[Dict[str, Any]] = None
    try:
        from evolution_engine import get_evolution_engine  # type: ignore
        evo = get_evolution_engine()
        evolution_summary = {
            "total_interactions": getattr(evo, 'total_interactions', None),
            "recent_interactions": len(getattr(evo, 'interactions', [])),
        }
    except Exception:
        evolution_summary = None
    warnings = _compute_warnings(endpoints)
    # Attempt to read a short excerpt of diagnostics document (non-fatal)
    diagnostics_excerpt = None
    try:
        from pathlib import Path  # local import to avoid overhead if stripped
        diag_path = Path(__file__).resolve().parent / 'docs' / 'copilot_diagnostics.md'
        if not diag_path.exists():
            # adjust if running from root (introspection.py at project root)
            proj_root = Path(__file__).resolve().parent
            diag_path = proj_root / 'docs' / 'copilot_diagnostics.md'
        if diag_path.exists():
            text = diag_path.read_text(encoding='utf-8', errors='ignore').splitlines()
            # Extract first 40 lines to keep payload small
            diagnostics_excerpt = text[:40]
    except Exception:
        diagnostics_excerpt = None

    return {
        "last_render": last_render,
        "recent_renders": renders,
        "endpoints": endpoints,
        "persona_mode": persona_mode,
        "evolution": evolution_summary,
        "last_error": get_last_error(),
        "version": {"git": _GIT_HASH},
        "render_threshold_ms": RENDER_SLOW_THRESHOLD_MS,
        "warnings": warnings,
        "generated_ts": time.time(),
        "diagnostics_excerpt": diagnostics_excerpt,
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
