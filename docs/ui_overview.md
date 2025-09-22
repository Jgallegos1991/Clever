# UI Overview & Interaction Model

"""
Why: Provide a high-level operational map for the minimal chat + particle UI after decluttering (removal of ambient microcopy, chips, overlays) so future additions do not reintroduce noise.
Where: Informs `templates/index.html`, `static/js/main.js`, particle engine scripts, and sanitizer layers (server + client) plus accessibility live region.
How: Describes DOM contract, fade lifecycle, sanitization defense stack, and extension hooks for future UI modules.
"""

## Current Philosophy
Minimal presence. Clever surfaces only the essentials:
- Floating centered input pill
- Ephemeral fading chat bubbles (auto-hide)
- Particle background (holographic chamber)
- Screen reader live region for accessibility

## DOM Contract (Essential Elements)
| Element | ID/Class | Purpose |
|---------|----------|---------|
| Wrapper | `#chat-log` | Container for transient message bubbles |
| Input | `#floating-input input` | Text entry field |
| Particle Canvas | `#particles` (or chamber container) | Visual ambient system |
| Live Region | `#sr-live` | Accessibility announcements |

Remove anything else unless justified by persona spec or diagnostics.

## Message Lifecycle
1. User submits → bubble appended (role=user)
2. Server reply sanitized → bubble appended (role=ai)
3. Auto-hide timer scheduled (fade-out + removal)
4. DOM scrub ensures no latent meta tokens

## Sanitization Defense Stack
| Layer | Location | Purpose |
|-------|----------|---------|
| Generation Suppression | `persona.py` | Avoid injecting meta scaffold |
| Server Sanitizer | `_sanitize_persona_text` in `app.py` | Regex strip banned tokens |
| Client Final Scrub | `appendMessage()` in `static/js/main.js` | Belt-and-suspenders defense |

## Accessibility
- Live region updates with AI reply text only (post-sanitization)
- Avoids decorative particle announcements
- Future: keyboard shortcuts (planned)

## Styling Guidelines
- Keep CSS centralized (`static/css/style.css`)
- Avoid inline styles; preserve CSP cleanliness
- Subtle glow for input focus; no persistent frames or panels

## Extension Hooks
| Hook | Intent |
|------|--------|
| `scheduleMessageAutoHide` | Adjust fade timing adaptively |
| Particle State Sync | Change ambient mode (thinking, idle) |
| Bubble Template Fn | Support optional structured responses (future) |

## Anti-Patterns
- Persistent conversation history log cluttering stage
- Inline scripts or style tags (CSP violation risk)
- Animations exceeding device performance envelope
- Reintroduction of meta or debug overlays by default

## Roadmap
- Particle intensity modulation based on sentiment (without exposing raw score)
- Reduced-motion preference detection
- Optional compact mode (denser vertical spacing)

---
*Canonical Source*: `docs/ui_overview.md`