# Configuration & Environment Reference

"""
Why: Centralize runtime invariants (offline guard, single DB, user personalization) to prevent drift and accidental multi-environment divergence.
Where: Reflects logic in `config.py`, `user_config.py`, `app.py` (offline enforcement), and diagnostics tooling (`make diagnostics`).
How: Enumerates settings, mandates non-negotiables, and provides extension pattern for safe additions.
"""

## Core Invariants
| Invariant | Description | Enforcement |
|-----------|-------------|-------------|
| Offline-only runtime | No external network calls permitted | `utils.offline_guard.enable()` in `app.py` |
| Single database file | Exactly one SQLite file at `config.DB_PATH` | `config.DB_PATH` constant + diagnostics check |
| Single user (Jay) | No auth layers, persona tuned to Jay | `user_config.py` consumption |
| Sanitized persona output | No meta reasoning leakage | `_sanitize_persona_text` + tests |

## Key Files
| File | Purpose |
|------|---------|
| `config.py` | Base paths, DB path, flags |
| `user_config.py` | User personalization (name, traits placeholders) |
| `app.py` | Applies offline guard, initializes engines |
| `database.py` | Thread-safe DB manager using `DB_PATH` |

## `config.py` Highlights
```python
PROJECT_ROOT = BASE_DIR
DB_PATH = os.path.join(PROJECT_ROOT, 'clever.db')
OFFLINE_ONLY = True
```
- Do NOT introduce environment-variable indirection for `DB_PATH` unless adding migration logic & diagnostics update.

## Extending Configuration (Pattern)
1. Add constant in `config.py`
2. Document here under "Extension Parameters"
3. Reference in code with clear Why/Where/How docstring
4. Add diagnostics rule if safety-critical

## Extension Parameters (Reserved Examples)
| Name | Purpose | Status |
|------|---------|--------|
| `SANITIZER_STRICT_MODE` | Toggle extra regex patterns | Planned |
| `MEMORY_WINDOW_TURNS` | Bound short-term context size | Planned |
| `UI_MAX_VISIBLE_BUBBLES` | Cap concurrent chat DOM nodes | Planned |

## User Personalization
`user_config.py` inputs (name, preferences roadmap) must NOT break single-user assumption. Multi-user separation is out of scope.

## Environment Variables (Minimal)
Environment variable proliferation intentionally avoided. Add only if necessary for deployment abstractions, and mirror value in this document.

## Diagnostics Hooks
`make diagnostics` should fail if:
- `offline_guard.enable()` missing
- Multiple `clever.db` references or variant filenames appear

## Anti-Patterns
- Multiple DB paths or dynamic DB switching
- Adding remote fetch logic for models or assets at runtime
- Embedding secrets in config (keep local, not tracked)

## Roadmap
- Introduce config schema validator (lightweight) to flag unauthorized keys
- Add dynamic runtime dump of active config to introspection (read-only)

---
*Canonical Source*: `docs/configuration.md`