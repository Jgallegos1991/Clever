# Application (`app.py`) Overview

"""
Why: Establish a concise operational map of the Flask entrypoint so contributors know insertion points (sanitization, routes, introspection) without reverse-engineering source.
Where: Mirrors logic in `app.py`, complements `docs/architecture.md`, references persona + sanitizer + evolution engine.
How: Summarizes routes, middleware, lifecycle, and defensive invariants.
"""

## Core Responsibilities
| Responsibility | Description |
|----------------|-------------|
| Route handling | Serves index + chat + health + introspection |
| Offline guard | Enforces local-only network usage |
| Persona mediation | Generates raw response then sanitizes |
| Introspection aggregation | Exposes runtime graph/state JSON |
| Evolution logging | (If enabled) logs interaction metadata |

## Key Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Serve minimal UI template |
| `/chat` | POST | Accept user text → persona → sanitize → JSON |
| `/api/runtime_introspect` | GET | Runtime state (graphs, coverage, diagnostics excerpt) |
| `/health` | GET | Basic liveness probe |

## Sanitization Flow
```
user text -> PersonaEngine.generate() -> raw text
   -> _sanitize_persona_text() -> response['response']
   -> client appendMessage() final scrub
```
- Defense-in-depth ensures leakage does not surface.

## Middleware / Headers
- Security headers optionally applied (CSP, object-src none)
- Offline guard blocks outbound calls globally early in startup

## Error Handling Philosophy
- Fail fast on missing config invariants (single DB, offline guard)
- Log + continue for non-critical introspection assembly failures

## Integration Points
| Component | Interaction |
|-----------|------------|
| persona.py | Response generation (mode, mood, variation) |
| evolution_engine.py | Logging interactions (optional) |
| introspection.py | Provides `runtime_state()` data structure |
| database.py | Underlying persistence (sentiment, memory) |

## Adding a New Route (Pattern)
1. Define function with Why/Where/How docstring
2. Validate inputs early
3. Avoid external network dependencies
4. Return JSON with minimal envelope
5. Update this doc + add test if logic non-trivial

## Common Pitfalls
- Adding verbose debug prints (prefer structured logging via debug_config)
- Returning unsanitized persona output
- Expanding chat JSON schema without updating frontend handling

## Extension Roadmap
- Add `/api/metrics` exporting lightweight perf counters
- Chat streaming (chunked) while preserving sanitizer pipeline

---
*Canonical Source*: `docs/app_overview.md`