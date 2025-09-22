# Frontend ↔ Backend Interaction Overview

"""
Why: Define the explicit contract across UI → Flask → Persona → Sanitizer → Response so future modifications remain coherent and offline-safe.
Where: Bridges `templates/index.html`, `static/js/main.js`, `persona.py`, `app.py`, `introspection.py`.
How: Documents request schema, response envelope, lifecycle, and security barriers.
"""

## End-to-End Flow
```
User Input -> fetch('/chat') POST JSON { message } -> Flask route
  -> PersonaEngine.generate() -> raw text
  -> _sanitize_persona_text() -> response JSON
  -> Frontend appendMessage() -> fade lifecycle
```

## Request Schema (`/chat`)
```json
{
  "message": "string"  // required, user input
}
```

## Response Schema (`/chat`)
```json
{
  "response": "string",          // sanitized persona reply
  "analysis": null | object,       // currently often null (reserved)
  "approach": null | string,       // reserved for future reasoning summary (humanized)
  "mood": null | string,           // placeholder persona mood
  "particle_intensity": number    // UI modulation hint (0-1 range typical)
}
```

## Frontend Responsibilities
| Stage | Responsibility |
|-------|----------------|
| Pre-submit | Trim input, ignore empty |
| Send | POST JSON, handle network errors silently (no external retry) |
| Receive | Append AI bubble (sanitized expectation) |
| Post | Schedule auto-hide, final scrub regex |

## Backend Responsibilities
| Stage | Responsibility |
|-------|----------------|
| Input | Parse JSON safely, default empty string guard |
| Persona | Generate mode + text (no meta tokens) |
| Sanitize | Remove banned markers via regex list |
| Respond | Minimal JSON envelope (no internal debug) |

## Security / Integrity Barriers
| Barrier | Purpose |
|---------|---------|
| Offline Guard | Block outbound HTTP(S) |
| Sanitizer | Strip reasoning scaffolds |
| Single DB Constraint | Prevent data fragmentation |
| CSP Headers | Block inline script injection |

## Performance Notes
- Chat endpoint should remain sub-100ms typical (excluding heavy NLP expansion)
- Avoid synchronous DB writes in latency-sensitive path unless necessary

## Introspection Link
`/api/runtime_introspect` provides:
- Reasoning coverage metrics (docstring Why/Where/How completeness)
- Runtime graphs (concept graph, reasoning graph)
- Diagnostics excerpt (drift / anomaly summary)

## Extension Points
| Area | Safe Extension Example |
|------|------------------------|
| Response | Add `suggestions: []` (must update UI + doc) |
| Persona | Add adaptive emoji gating (still sanitized) |
| UI | Particle intensity mapping to sentiment (no raw scores) |

## Anti-Patterns
- Embedding raw stack traces in JSON
- Adding un-sanitized internal analysis arrays
- Expanding payload without updating this doc + tests

---
*Canonical Source*: `docs/frontend_backend_overview.md`