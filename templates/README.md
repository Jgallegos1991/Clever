# Clever Templates

Why:
  Establish a single authoritative UI surface and reduce confusion from legacy / experimental template variants.
Where:
  Resides in the `templates/` directory to document each remaining file's purpose and deprecation status.
How:
  Lists active vs. legacy templates, clarifies which IDs/classes are contractually required by tests and JS, and sets guidelines for future UI changes.

## Canonical Template

- **`index.html`** (authoritative)
  - Must expose:
    - `#particles` (canvas background)
    - `.grid-overlay` (ripple / acceptance tests)
    - `#chat-log` (chat stream container)
    - Bottom-centered input ( `.entrybar`, `#chat-input`, `#send-btn` )
  - Owned by: frontend/particle system + `static/js/main.js`
  - Ephemeral chat bubbles auto-fade (mutation observer inline script)

## Legacy / Reference Templates

Retained temporarily for design reference; not wired in `app.py`:

| File                | Status      | Notes |
|---------------------|-------------|-------|
| `index_classic.html`| legacy      | Older layout before particle simplification |
| `index_clean.html`  | legacy      | Minimal styling experiment |
| `index_working.html`| legacy      | Interim debug template |
| `index_backup.html` | backup      | Safety copy prior to consolidation |
| `magical_ui.html`   | experimental| High-concept visual prototype |
| `projects.html`     | legacy/unused | Placeholder for possible multi-view design |
| `generate_output.html` | tooling  | Likely generated artifact/utility output |

## Decommissioned / Removed

- `index_new.html`: Superseded by `index.html`; removed to avoid ID mismatches.

## Required ID / Class Contracts

| Selector      | Purpose                                  | JS/Test Dependency |
|---------------|-------------------------------------------|--------------------|
| `#particles`  | Particle canvas                          | `main.js`, tests    |
| `.grid-overlay` | Visual ripple anchor                   | tests, ripple logic |
| `#chat-log`   | Message container for bubbles            | `appendMessage()`   |
| `#chat-input` | User message input                       | send handler        |
| `#send-btn`   | Send action trigger                      | click handler       |

## Adding a New Template Variant

1. Justify the need (performance experiment? layout overhaul?).
2. Keep it isolated; do NOT change home route until accepted.
3. Replicate required ID/class contracts (table above).
4. Update this README with status: `experimental`.
5. After adoption, deprecate older template (mark here) and remove after one release.

## Future Enhancements

- History retention toggle (persist bubbles longer when user opts in).
- SVG-based particle layer fallback for very low-power environments.
- Accessibility audit (focus order, ARIA roles for dynamic bubbles).

## Connects to

- `app.py` (home route rendering `index.html`)
- `static/js/main.js` (message lifecycle + particle triggers)
- Tests under `tests/test_ui_*` verifying structural contracts
