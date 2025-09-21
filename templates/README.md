# Templates Directory (Minimized)

Why:
  Consolidated to a single authoritative `index.html` to reduce maintenance,
  eliminate drift across experimental variants (`index_clean`, `magical_ui`,
  etc.) and ensure tests target one stable DOM contract.
Where:
  Referenced by `app.py` home route and UI acceptance + tooltip tests. All
  former variants have been removed; their patterns are preserved in git
  history if future design exploration is needed.
How:
  Only the following files remain:

* `index.html`: Canonical UI (chat + particles + required placeholders)
* `README.md`: This rationale file for reasoning/introspection graph

Removed legacy templates on YYYY-MM-DD (see commit) to prevent accidental
reintroduction of divergent element IDs that break tests or inflate bundle.

Connects to:
* tests/test_ui_brief_acceptance.py: Asserts presence of key IDs/classes
* tests/test_ui_tooltips.py: Scans all .html files (now only index.html)
* system_validator.py: May enforce required asset references

If a new experimental layout is needed, create it under `legacy_ui/` or a
feature branch so production `index.html` stays stable.
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
