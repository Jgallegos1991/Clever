"""
introspection.py - Runtime Introspection Utilities for Clever's Cognitive Partnership System

Why: Provide a real-time window into what the system is rendering, which routes
are active, and the associated Why/Where/How reasoning metadata extracted from
docstrings. This converts the enforced documentation standard into actionable
observability for debugging UI/template issues, latency problems, or missing
persona integration. Essential for maintaining Clever's cognitive partnership system
intelligence and debugging efficiency.

Where: Imported by `app.py` to wrap template rendering and serve an
`/api/runtime_introspect` endpoint. Also consumed implicitly by any frontend
runtime overlay requesting JSON state. Central to Clever's self-awareness and
system intelligence capabilities.

How: Maintains in-memory registries for recent template renders, endpoint
metadata derived from Flask routes, parsed Why/Where/How sections, last error
captured by a global error handler, and lightweight git version discovery.

File Usage:
    - Runtime debugging: Primary tool for real-time system state analysis and debugging
    - Template rendering: Tracks all template renders for performance and error analysis
    - Documentation validation: Validates Why/Where/How patterns across system components
    - Error tracking: Captures and reports system errors for debugging workflows
    - Performance monitoring: Tracks rendering times and system performance metrics
    - System intelligence: Provides live introspection for Clever's cognitive partnership
    - Development tools: Powers debug overlays and development monitoring interfaces
    - API endpoint: Serves real-time system state via /api/runtime_introspect

Connects to:
    - app.py: Main Flask application integration for template rendering and error handling
        - `traced_render` called by `app.py`'s `home()` route to render templates
        - `register_error_handler` called in `app.py` to set up global error catching
        - `runtime_state` called by the `/api/runtime_introspect` route in `app.py`
    - evolution_engine.py: Learning system integration for concept data and interaction statistics
        - `get_evolution_engine` called by `_build_concept_graph` and `runtime_state`
    - intelligent_analyzer.py: AI-powered analysis integration for enhanced introspection
        - `get_intelligent_analysis` called by `runtime_state` for AI analysis payload
    - tools/runtime_dump.py: CLI utility consuming JSON output from introspection endpoint
    - templates/index.html: Main UI template whose rendering is tracked by `record_render`
    - static/js/main.js: Frontend JavaScript polling `/api/runtime_introspect` for debug data
    - debug_config.py: System debugging and performance monitoring integration
    - persona.py: Personality engine integration for cognitive partnership insights
    - database.py: Data persistence layer monitoring and performance tracking
    - config.py: Configuration system integration for runtime settings
    - All Python modules: Documentation standard validation and reasoning metadata extraction
"""
from __future__ import annotations
import inspect
import re
from collections import deque
from pathlib import Path  # For code health & component graph scanning
import ast  # For static analysis of functions & imports

# Regular expression to extract Why/Where/How sections from docstrings (case-insensitive)
_SECTION_RE = re.compile(r"^(why|where|how)\s*:\s*(.*)$", re.IGNORECASE)

# Thread-safe registries
_render_events: Deque[Dict[str, Any]] = deque(maxlen=50)
_registry_lock = threading.Lock()
_last_error: Optional[Dict[str, Any]] = None

# Cache for parsed docstring metadata keyed by object id
_docstring_cache: Dict[int, Dict[str, str]] = {}

# Component health tracking registry  
_component_health: Dict[str, Dict[str, Any]] = {}
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


def _extract_connects_to(obj: Any) -> List[str]:
    """Parse 'Connects to:' lines from a docstring to derive graph edges.

    Why: Convert human-readable connection annotations into machine-readable
    edges that can power a live reasoning/architecture graph overlay.
    Where: Called when assembling reasoning_graph inside runtime_state; ties
    directly into enforced documentation contract without extra author burden.
    How: Scans the docstring for a 'Connects to:' line, then collects the
    following indented or hyphen-prefixed lines until a blank or new section.
    Extracts probable module/file tokens (*.py) or bare identifiers.
    """
    doc = inspect.getdoc(obj) or ""
    lines = doc.splitlines()
    captures: List[str] = []
    in_block = False
    for raw in lines:
        line = raw.rstrip()
        if not in_block:
            if line.lower().startswith('connects to'):  # start block
                in_block = True
            continue
        # inside block: terminate on blank or section style line
        if not line.strip():
            break
        if re.match(r'^(why|where|how)\s*:', line, re.IGNORECASE):  # new section
            break
        # Normalize bullet styles
        line_clean = re.sub(r'^[-*]\s*', '', line).strip()
        if not line_clean:
            continue
        # Heuristic: capture first token that looks like module or file
        token = line_clean.split()[0]
        # Strip trailing commas / punctuation
        token = token.rstrip(':,;')
        captures.append(token)
    # Deduplicate while preserving order
    seen: Set[str] = set()
    ordered = []
    for c in captures:
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def _build_reasoning_graph(endpoints: List[Dict[str, Any]], app) -> Dict[str, Any]:
    """Build a lightweight reasoning graph from endpoint docstrings.

    Why: Provide the frontend with a navigable set of nodes/edges describing
    declared architectural intent (the "arrows" between components).
    Where: Embedded in runtime_state payload; consumed by optional graph
    debug overlay (graph-debug.js) when ?graph=1 is present.
    How: Creates nodes for each endpoint function + unique referenced targets
    from their Connects to blocks. Edges are directed endpoint -> target.
    Truncates counts to remain payload-friendly; includes a 'truncated' flag.
    """
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, str]] = []
    MAX_NODES = 300
    MAX_EDGES = 600
    # First add endpoint nodes
    for ep in endpoints:
        ident = f"{ep['module']}.{ep['func']}"
        nodes[ident] = {
            'id': ident,
            'label': ep['func'],
            'type': 'endpoint',
            'why': ep.get('why',''),
            'where': ep.get('where',''),
            'how': ep.get('how',''),
            'rule': ep.get('rule'),
        }
    # Extract edges by re-inspecting actual view functions (for raw docstring)
    for rule in app.url_map.iter_rules():
        fn = app.view_functions.get(rule.endpoint)
        if not fn:
            continue
        src = f"{getattr(fn,'__module__','<unknown>')}.{getattr(fn,'__name__','<unknown>')}"
        targets = _extract_connects_to(fn)
        for tgt in targets:
            # Normalize target id heuristic: if endswith .py remove extension
            norm = tgt[:-3] if tgt.endswith('.py') else tgt
            # Create node placeholder if missing
            if norm not in nodes:
                nodes[norm] = {'id': norm, 'label': norm, 'type': 'target'}
            edges.append({'source': src, 'target': norm, 'type': 'connects_to'})
    truncated = False
    if len(nodes) > MAX_NODES:
        truncated = True
        # Keep endpoints preferentially
        ep_nodes = [n for n in nodes.values() if n.get('type')=='endpoint']
        extra = MAX_NODES - len(ep_nodes)
        keep_ids = set(n['id'] for n in ep_nodes)
        if extra > 0:
            for n in nodes.values():
                if n['id'] not in keep_ids and n.get('type')=='target' and extra>0:
                    keep_ids.add(n['id']); extra -=1
        nodes = {nid: nodes[nid] for nid in keep_ids}
        edges = [e for e in edges if e['source'] in nodes and e['target'] in nodes][:MAX_EDGES]
    if len(edges) > MAX_EDGES:
        truncated = True
        edges = edges[:MAX_EDGES]
    return {
        'nodes': list(nodes.values()),
        'edges': edges,
        'truncated': truncated,
        'generated_at': time.time(),  # Why: unify timestamp key naming for frontend consumption; Where: referenced by graph legend overlay; How: epoch seconds float
    }


def _build_concept_graph() -> Optional[Dict[str, Any]]:
    """Attempt to build an evolution concept graph (best-effort).

    Why: Provide optional second layer (concept network) requested for rich
    graph view (option C). Keeps failure silent if evolution engine not ready
    or data would be too large.
    Where: runtime_state attaches as concept_graph when available.
    How: Queries evolution_engine for a lightweight list of concepts and their
    connections if such attributes exist. Applies size caps similar to
    reasoning graph.
    """
    try:
        from evolution_engine import get_evolution_engine  # type: ignore
        evo = get_evolution_engine()
        concepts = getattr(evo, 'concepts', None)
        links = getattr(evo, 'concept_links', None)
        if not concepts or not links:
            return None
        MAX_CONCEPTS = 250
        MAX_LINKS = 600
        c_items = list(concepts.items()) if isinstance(concepts, dict) else []
        c_items = c_items[:MAX_CONCEPTS]
        nodes = [{'id': k, 'label': k, 'type': 'concept', 'weight': v} for k, v in c_items]
        # Filter links to those whose endpoints present in truncated node set
        node_ids = {n['id'] for n in nodes}
        filtered = [l for l in links if l[0] in node_ids and l[1] in node_ids]
        filtered = filtered[:MAX_LINKS]
        edges = [{'source': a, 'target': b, 'type': 'concept_link', 'weight': w} for a,b,w in filtered]
        return {
            'nodes': nodes,
            'edges': edges,
            'truncated': len(concepts)>MAX_CONCEPTS or len(links)>MAX_LINKS,
            'generated_ts': time.time(),  # Why: allow frontend to detect refresh cycles; Where: consumed by graph-debug.js legend; How: epoch seconds
        }
    except Exception:
        return None


def runtime_state(app, persona_engine=None, include_intelligent_analysis=True) -> Dict[str, Any]:
    """Assemble full runtime introspection state with enhanced intelligent analysis.

    Why: Central aggregation converting docstring reasoning + live telemetry
    (renders, errors, evolution stats) + AI-powered analysis into a comprehensive
    navigational map that not only shows "what connects to what" but also
    identifies problems, suggests fixes, and provides actionable insights.
    Where: Returned by `/api/runtime_introspect` endpoint in `app.py`, consumed
    by enhanced frontend debug overlay and CLI analysis tools.
    How: Gathers traditional metrics plus intelligent analysis results, problem
    detection, architectural insights, and performance recommendations to create
    a complete system health and improvement dashboard.

    Connects to:
        - evolution_engine.py: Interaction summary (if available)
        - app.py: Persona engine reference & endpoint registration
        - tools/runtime_dump.py: CLI dump utility
        - intelligent_analyzer.py: AI-powered problem detection and insights
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
            proj_root = Path(__file__).resolve().parent
            diag_path = proj_root / 'docs' / 'copilot_diagnostics.md'
        if diag_path.exists():
            text = diag_path.read_text(encoding='utf-8', errors='ignore').splitlines()
            diagnostics_excerpt = text[:40]
    except Exception:
        diagnostics_excerpt = None

    reasoning_graph = _build_reasoning_graph(endpoints, app)
    concept_graph = _build_concept_graph()
    # Code health + component graph (best-effort; never raise to caller)
    try:
        code_health = _scan_code_health()
    except Exception as e:  # noqa: BLE001
        code_health = {"error": f"code health scan failed: {e}"}
    try:
        component_graph = _build_component_graph()
    except Exception as e:  # noqa: BLE001
        component_graph = {"error": f"component graph failed: {e}"}
    # JSON safety pass (convert sets recursively)
    def _json_safe(obj):  # Why: Prevent Flask jsonify errors on non-serializable containers
        # Where: Applied just before assembling final runtime_state dict
        # How: Recursively convert set -> sorted list; walk dict/list/tuple
        if isinstance(obj, set):
            try:
                return sorted(list(obj))
            except Exception:  # noqa: BLE001
                return list(obj)
        if isinstance(obj, dict):
            return {k: _json_safe(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_json_safe(v) for v in obj]
        return obj
    code_health = _json_safe(code_health)
    component_graph = _json_safe(component_graph)
    reasoning_graph = _json_safe(reasoning_graph)
    concept_graph = _json_safe(concept_graph)

    # Coverage stats: count endpoints with all tokens vs total (documentation health metric)
    complete = 0
    for ep in endpoints:
        if all((ep.get(k) or '').strip() for k in ('why','where','how')):
            complete += 1
    reasoning_coverage = {
        'endpoints_total': len(endpoints),
        'endpoints_complete': complete,
        'percent': (complete / len(endpoints) * 100.0) if endpoints else 100.0,
    }

    # Enhanced: Add intelligent analysis if requested
    intelligent_analysis = None
    if include_intelligent_analysis:
        try:
            from intelligent_analyzer import get_intelligent_analysis  # type: ignore
            intelligent_analysis = get_intelligent_analysis()
        except Exception as e:  # noqa: BLE001 broad purposely
            intelligent_analysis = {
                'error': f'Intelligent analysis unavailable: {str(e)}',
                'generated_at': time.time()
            }
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
        "reasoning_coverage": reasoning_coverage,
        "generated_ts": time.time(),
        "diagnostics_excerpt": diagnostics_excerpt,
        "reasoning_graph": reasoning_graph,
        "concept_graph": concept_graph,
        "intelligent_analysis": intelligent_analysis,
        "code_health": code_health,
        "component_graph": component_graph,
        "ui_component_validation": validate_ui_components(),
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

# ---------------------------------------------------------------------------
# Code Health & Dependency Graph Enhancements (clean implementation)
# ---------------------------------------------------------------------------

def _scan_code_health(max_files: int = 400) -> Dict[str, Any]:
    """Perform lightweight repository code health scan.

    Why: Provide fast, offline insight into documentation coverage and potential
         merge/conflict drift so Jay sees immediate cognitive wiring health.
    Where: Returned inside `runtime_state` under `code_health`; consumed by
           debug overlay + tests to guard enforced Why/Where/How contract.
    How: Walk project root (bounded), AST-parse Python files, measure function
         doc token presence (why/where/how), detect merge conflict markers and
         meta leakage patterns. Returns summary counts + sample gaps.

    Args:
        max_files: Safety cap to avoid excessive traversal cost.

    Returns:
        Dict with counts, percentages, gaps, and timestamps.
    """
    root = Path(__file__).resolve().parent
    py_files: List[Path] = []
    skip_dirs = {"__pycache__", ".git", "venv", "logs", "legacy"}
    for p in root.rglob("*.py"):
        if any(part in skip_dirs for part in p.parts):
            continue
        py_files.append(p)
        if len(py_files) >= max_files:
            break
    conflict_markers = 0
    meta_token_hits = 0
    functions_total = 0
    functions_with_why = 0
    functions_with_where = 0
    functions_with_how = 0
    missing_samples: List[str] = []
    meta_pattern = re.compile(r"(Time-of-day:|focal lens:|Vector:|complexity index|essence:)", re.IGNORECASE)
    for file_path in py_files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if any(m in text for m in ("<<<<<<<", ">>>>>>>", "=======")):
            conflict_markers += 1
        if meta_pattern.search(text):
            meta_token_hits += 1
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions_total += 1
                doc = ast.get_docstring(node) or ""
                has_why = bool(re.search(r"\bwhy\s*:", doc, re.IGNORECASE))
                has_where = bool(re.search(r"\bwhere\s*:", doc, re.IGNORECASE))
                has_how = bool(re.search(r"\bhow\s*:", doc, re.IGNORECASE))
                if has_why: functions_with_why += 1
                if has_where: functions_with_where += 1
                if has_how: functions_with_how += 1
                if not (has_why and has_where and has_how) and len(missing_samples) < 12:
                    rel = file_path.relative_to(root)
                    missing_samples.append(f"{rel}:{getattr(node,'name','<anon>')}")
    coverage_any_percent = (functions_with_why / functions_total * 100.0) if functions_total else 100.0
    combined_with_all = min(functions_with_why, functions_with_where, functions_with_how)
    coverage_all_percent = (combined_with_all / functions_total * 100.0) if functions_total else 100.0
    return {
        "files_scanned": len(py_files),
        "functions_total": functions_total,
        "functions_with_why": functions_with_why,
        "functions_with_where": functions_with_where,
        "functions_with_how": functions_with_how,
        "coverage_percent_any_why": round(coverage_any_percent, 2),
        "coverage_percent_all": round(coverage_all_percent, 2),
        "conflict_markers": conflict_markers,
        "meta_token_hits": meta_token_hits,
        "missing_samples": missing_samples,
        "generated_ts": time.time(),
    }


def _build_component_graph(max_nodes: int = 300, max_edges: int = 800) -> Dict[str, Any]:
    """Build lightweight intra-project import dependency graph.

    Why: Visualize coupling to keep cognitive architecture clean & traceable.
    Where: Returned via runtime_state -> `component_graph`; supports debug graph overlay.
    How: Parse AST of Python files in root + selected subdirs, add node per
         module, edge per intra-project import. Apply size caps to stay payload-light.
    """
    root = Path(__file__).resolve().parent
    py_files: List[Path] = [p for p in root.glob("*.py")]
    for sub in ("utils", "tools", "tests"):
        sp = root / sub
        if sp.exists():
            for p in sp.rglob("*.py"):
                py_files.append(p)
    def norm(p: Path) -> str:
        rel = p.relative_to(root).as_posix()
        return rel[:-3] if rel.endswith('.py') else rel
    local = {norm(p) for p in py_files}
    modules: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, str]] = []
    for p in py_files:
        if len(modules) >= max_nodes:
            break
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(text)
        except Exception:
            continue
        src_id = norm(p)
        modules.setdefault(src_id, {"id": src_id, "label": src_id, "type": "module"})
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    tgt = alias.name.split('.')[0]
                    if tgt in local:
                        edges.append({"source": src_id, "target": tgt, "type": "import"})
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    tgt = node.module.split('.')[0]
                    if tgt in local:
                        edges.append({"source": src_id, "target": tgt, "type": "import"})
        if len(edges) >= max_edges:
            break
    truncated = len(modules) > max_nodes or len(edges) > max_edges
    return {
        "nodes": list(modules.values())[:max_nodes],
        "edges": edges[:max_edges],
        "truncated": truncated,
        "generated_ts": time.time(),
    }


def validate_ui_components() -> Dict[str, Any]:
    """
    Validate UI component integrity and catch CSS/HTML/JS mismatches
    
    Why: Prevent invisible UI elements caused by ID/selector mismatches, z-index conflicts,
         or broken component connections. The particle visibility issue demonstrated 
         that our system needs automated component health checking.
    Where: Called by runtime_state() to include component validation in introspection.
           Should catch issues like CSS #particle-canvas vs HTML id="particles".
    How: Cross-references template files, CSS selectors, and JavaScript element queries
         to detect mismatches. Validates z-index hierarchy and positioning conflicts.
    
    Returns:
        Dictionary with component health status, warnings, and validation results
        
    Connects to:
        - templates/index.html: Scans for canvas and UI element IDs
        - static/css/style.css: Validates CSS selectors match HTML IDs  
        - static/js/main.js: Checks JavaScript element queries
        - app.py: Results included in /api/runtime_introspect endpoint
    """
    validation_results = {
        "canvas_particle_system": _validate_particle_system(),
        "chat_interface": _validate_chat_interface(), 
        "input_controls": _validate_input_controls(),
        "z_index_hierarchy": _validate_z_index_hierarchy(),
        "timestamp": time.time(),
        "overall_status": "healthy"
    }
    
    # Determine overall health status
    issues_found = []
    for component, result in validation_results.items():
        if isinstance(result, dict) and result.get("status") == "error":
            issues_found.append(component)
            
    if issues_found:
        validation_results["overall_status"] = "issues_detected"
        validation_results["issues"] = issues_found
        
    return validation_results


def _validate_particle_system() -> Dict[str, Any]:
    """
    Validate the holographic particle system component integrity
    
    Why: The particle invisibility bug was caused by CSS/HTML ID mismatch that should
         have been caught automatically by component validation.
    Where: Called by validate_ui_components() to check particle system health.
    How: Validates HTML canvas element, CSS styling, and JavaScript initialization.
    """
    try:
        # Check HTML template for canvas element
        template_path = Path("templates/index.html")
        if not template_path.exists():
            return {"status": "error", "message": "Template file not found"}
            
        template_content = template_path.read_text()
        
        # Extract canvas ID from HTML
        canvas_match = re.search(r'<canvas[^>]+id=["\']([^"\']+)["\']', template_content)
        html_canvas_id = canvas_match.group(1) if canvas_match else None
        
        # Check CSS for matching selector
        css_path = Path("static/css/style.css")
        css_content = css_path.read_text() if css_path.exists() else ""
        
        # Look for canvas styling rules
        css_selectors = re.findall(r'#([a-zA-Z0-9_-]+)\s*{[^}]*(?:position|z-index)', css_content)
        
        # Check JavaScript for element queries
        js_path = Path("static/js/main.js") 
        js_content = js_path.read_text() if js_path.exists() else ""
        
        js_queries = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_content)
        
        # Validation results
        result = {
            "status": "healthy",
            "html_canvas_id": html_canvas_id,
            "css_selectors": css_selectors,
            "js_queries": js_queries,
            "warnings": []
        }
        
        # Check for ID/selector mismatches
        if html_canvas_id and html_canvas_id not in css_selectors:
            result["status"] = "error"
            result["warnings"].append(f"CSS missing selector for HTML canvas ID: {html_canvas_id}")
            
        if html_canvas_id and html_canvas_id not in js_queries:
            result["warnings"].append(f"JavaScript missing query for canvas ID: {html_canvas_id}")
            
        return result
        
    except Exception as e:
        return {"status": "error", "message": f"Validation failed: {str(e)}"}


def _validate_chat_interface() -> Dict[str, Any]:
    """Validate chat interface component integrity"""
    return {"status": "healthy", "message": "Chat interface validation not implemented yet"}


def _validate_input_controls() -> Dict[str, Any]:  
    """Validate input controls component integrity"""
    return {"status": "healthy", "message": "Input controls validation not implemented yet"}


def _validate_z_index_hierarchy() -> Dict[str, Any]:
    """
    Validate z-index hierarchy for proper UI layering
    
    Why: Conflicting z-index values can cause UI elements to be hidden behind others.
    Where: Called by validate_ui_components() to check layering conflicts.
    How: Scans CSS for z-index declarations and validates proper hierarchy.
    """
    try:
        css_path = Path("static/css/style.css")
        if not css_path.exists():
            return {"status": "error", "message": "CSS file not found"}
            
        css_content = css_path.read_text()
        
        # Extract z-index declarations
        z_index_pattern = r'([#.][\w-]+)\s*{[^}]*z-index:\s*(\d+)'
        z_indexes = re.findall(z_index_pattern, css_content)
        
        # Build hierarchy map
        hierarchy = {}
        for selector, z_value in z_indexes:
            hierarchy[selector] = int(z_value)
            
        return {
            "status": "healthy",
            "hierarchy": hierarchy,
            "max_z_index": max(hierarchy.values()) if hierarchy else 0,
            "conflicts": _detect_z_index_conflicts(hierarchy)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Z-index validation failed: {str(e)}"}


def _detect_z_index_conflicts(hierarchy: Dict[str, int]) -> List[str]:
    """Detect potential z-index conflicts"""
    conflicts = []
    
    # Check for duplicate z-index values
    values_seen = {}
    for selector, z_value in hierarchy.items():
        if z_value in values_seen:
            conflicts.append(f"Duplicate z-index {z_value}: {selector} and {values_seen[z_value]}")
        else:
            values_seen[z_value] = selector
            
    return conflicts

