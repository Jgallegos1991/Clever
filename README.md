## How to run Clever locally (offline-first)

Requirements: Python 3.12. In Codespaces this repo already includes a devcontainer.

Offline-first setup installs only essential deps (Flask + file watcher):

```bash
# from repo root
make setup     # create .venv, minimal deps, init DB on first run
make run       # launch on http://localhost:5000
# in a new terminal:
make test      # quick smoke; may print 'no tests' which is OK
```

When you’re online and want the full NLP stack:

```bash
make setup-full  # installs full requirements.txt (spaCy, etc.)
```

Optional sync helpers (offline-safe):

```bash
make sync-and-ingest  # best-effort rclone syncs then ingest both roots
make watch            # live watch of Clever_Sync and synaptic_hub_sync
```

Troubleshooting:

- If a port toast says “exit code 127”, ignore and just run `make run` in the terminal.
- To reset the venv: `make clean-venv && make setup` (or `setup-full`).
