# Copilot Diagnostics & Alignment Report

Date: 2025-09-21

## Why / Where / How Summary
Why: Provide a living diagnostic snapshot showing how current code and workflows align with `.github/copilot-instructions.md` (unbreakable rules, UI vision, documentation contract) so future contributors can quickly detect drift.
Where: Lives under `docs/` and can be referenced by CI, onboarding, or runtime introspection tooling (future enhancement: expose excerpt via `/api/runtime_introspect`).
How: Consolidates checks (manual for now) across Offline enforcement, Single DB, Single User, Documentation pattern, Frontend UI rules, and Feature requests completion status.

---
## Unbreakable Rules Compliance
1. Strictly Offline: `app.py` calls `offline_guard.enable()` at top (line near imports). No external network fetch code added in recent changes (frontend only calls local `/chat`, `/api/chat`, `/api/ping`, `/api/telemetry`).
2. Single-User Only: `user_config.py` defines personalization; no auth or account creation endpoints exist. Chat endpoints do not accept a user identifier parameter.
3. Single Database: Only `config.DB_PATH` (`clever.db`) referenced. No alternative file names or fallback creation observed.
4. Mandatory Documentation: New/modified sections (telemetry routes in `app.py`, lifecycle logic in `main.js`, CSS fade classes, `index.html` inline hide narrowing) include Why/Where/How comments. Older legacy files may still need retrofitting (see Drift Risks).

---
## UI Vision Alignment
| Vision Element | Current Status | Notes |
| -------------- | -------------- | ----- |
| Stage (particle engine) primary | Active via `holographic-chamber.js`; canvas fixed full screen | Fallback to legacy particle start in `main.js` if chamber init fails |
| Chat bubbles float + fade | Implemented: `.message.manifesting/manifested/fading` transitions + JS lifecycle | Auto-hide ~14s, pin & pause supported |
| Minimal input bar | `.entrybar` fixed bottom center translucent glow | Could add subtle focus glow animation (future) |
| Remove persistent chat card | No large static panel; ephemeral bubbles | Legacy panel elements hidden / minimized |
| Messages auto-hide | Implemented with centralized `scheduleMessageAutoHide` | Pinned messages exempt |

---
## Feature Request Completion Matrix
| Feature | Implemented | File(s) | Follow-up Potential |
|--------|-------------|---------|---------------------|
| Fade-in/out messages | Yes | `static/js/main.js`, `static/css/style.css` | Fine-tune durations per performance tests |
| Remove persistent chat box | Yes | `templates/index.html` | Clean legacy placeholders later |
| Floating minimal input | Yes | `index.html` inline `.entrybar` | Add accessibility label improvements |
| Auto-hide messages | Yes | JS lifecycle constants | Add user setting for retention |
| Pin / Pause behavior | Added (extra) | `main.js` + CSS | Tooltip + keyboard A11y |
| Toast notifications | Added (extra) | `main.js`, CSS | Severity theming expansion |
| Telemetry endpoints | Added (extra) | `app.py` | Optional overlay panel |

---
## Backend Route Snapshot (Relevant to Copilot Instructions)
| Route | Purpose | Why/Where/How Present | Notes |
|-------|---------|-----------------------|-------|
| `/chat` & `/api/chat` | Core conversation | Yes (docstring) | Returns legacy-compatible schema |
| `/api/ping` | Latency & readiness | Yes | Very lightweight |
| `/api/telemetry` | Operational metrics | Yes | In-memory only |
| `/api/runtime_introspect` | Debug overlay data | Yes | Supports reasoning graph concept |

---
## Documentation Pattern Audit (Spot Sample)
Sampled Files: `app.py`, `templates/index.html`, `static/js/main.js`, `static/css/style.css`
- app.py: New telemetry + ping routes: Why/Where/How docstrings present.
- index.html: Inline comment block clarifying narrowed hidden selectors (Why/Where/How inline). Additional note for selfcheck chip.
- main.js: appendMessage & scheduleMessageAutoHide functions include multi-line Why/Where/How comments.
- style.css: `.message.fading` block includes Why/Where/How comment.
Remaining Work: Some older modules (e.g., `memory_engine.py`, `sync_watcher.py`) may lack full pattern; schedule phased retrofit.

---
## Drift Risks & TODOs
| Area | Risk | Mitigation |
|------|------|------------|
| Legacy templates present | Future edits may reintroduce hidden chat log | Remove deprecated templates after confirmation |
| Missing Why/Where/How in legacy engines | Inconsistent reasoning map | Add retrofit ticket & incremental patches |
| No automated offline guard test | Silent regression risk | Add pytest ensuring external socket attempts fail |
| Telemetry non-persistent | Lost metrics on restart | Acceptable (design); document intentionally ephemeral |
| Vulnerability TODO in requirements | Security lag | Investigate & bump minimal versions, update changelog |

---
## Recommended Next Enhancements
1. Telemetry Overlay: Small floating panel toggled by `?debug=telemetry` showing `total_chats`, `avg_latency_ms`, last latency.
2. Accessibility Pass: ARIA labels for pin buttons; add keyboard shortcut (e.g., Alt+P toggles pin on focused bubble).
3. Configurable Retention: Add a simple settings constant (e.g., `MESSAGE_LIFECYCLE.AUTO_HIDE_MS` adjustable via query param or localStorage toggle).
4. Vulnerability Remediation: Implement minimal safe dependency upgrade with changelog entry and CI guard.
5. Why/Where/How Retrofit Script: CLI tool scanning for functions lacking the triad to generate a report.

---
## Quick Verification Checklist
- [x] Offline guard enabled at startup
- [x] Only one DB path referenced (`clever.db`)
- [x] No multi-user constructs (accounts/sessions) added
- [x] Chat bubbles appear & auto-hide (pin to persist)
- [x] New routes documented with Why/Where/How
- [x] Index template no longer hides `#chat-log`
- [x] Selfcheck status chip available for status messaging

---
## How to Regenerate / Update
Manual for now: After any UI or architectural change, update this file with:
- Added/changed routes
- New UI lifecycle behaviors
- Any breach or exception to unbreakable rules (must justify or roll back)
Future Idea: Add a `make diagnostics` target that compiles static checks + this markdown.

---
## Integration Pointers
Potential future integration: `/api/runtime_introspect` can embed a hash or excerpt from this diagnostics file for overlay display—ensuring runtime awareness of declared rules vs. observed state.

---
## Meta
Authored by automated assistance per project instructions. Treat as living document; prune sections as automation matures.
