# Copilot Operating Rules (Jay's Clever)

- Identity: You are assisting **Jay** only. First person refers to Jay.
- Non-negotiables:
  1) **Clever never connects to the internet.** Any networked code must be opt-in and isolated from Clever runtime.
  2) Clever is **offline-first** (Flask + SQLite + local assets + spaCy).
  3) UI mood: **3D, softer neon, 20k+ "nanobot" pixels**, morphs on events, free-hand draw. Subtle, not blown out.

- Codebase highlights (anchor for @workspace):
  - Backend: `app.py`, `database.py`, `core_nlp_logic.py`, `nlp_processor.py`, `file_ingestor.py`, `backup_manager.py`, `config.py`, `sync_watcher.py`
  - Frontend: `index.html`/`projects.html`, `style.css`, `main.js`, `nanobot_swarm.js`, `ui.js`, `orb_renderer.js`, `nebula_renderer.js`
  - Data: `conversations.json` (private, never paste content), `clever_memory.db` (local)
  - Build: `Makefile` (setup-min/setup/setup-full), `requirements-min.txt`, `requirements-base.txt`, `requirements.txt`
  - Constraints: zero external CDNs; fonts/assets local. All JS/CSS must be local.

- Development workflow:
  - `make setup-min` - Flask only (fastest, offline)
  - `make setup` - Base dependencies (offline capable)
  - `make setup-full` - Full NLP stack (requires internet)
  - `make watch` - Auto-ingest file changes from sync directories
  - `make test` - Run pytest test suite

- Visual behaviors to preserve:
  - Free-hand draw attracts the swarm path.
  - Morph keywords: sphere, ring, torus, panel, and `write <TEXT>`.
  - Idle self-evolution every ~10s.
  - Brightness stays soft (alpha ≤ 0.25), 20k particles default.

- Testing expectations:
  - Python: pytest-style unit tests; no network; use temp sqlite; seed data isolated.
  - Frontend: DOM-only tests where feasible (no external services).
  - All new scripts should include basic unit tests (see `test_sync_watcher.py` as example).

- Output style:
  - Show diffs or full file replacements (smallest safe patch).
  - Keep responses concise; include "how to run" notes when adding new files.
  - Reference the improved documentation in `README.copilot.md` for architecture decisions.
