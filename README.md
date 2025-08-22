## How to run Clever locally

Requirements: Python 3.12. In Codespaces this repo already includes a devcontainer.

```bash
# from repo root
make setup   # create .venv, install deps, init DB
make run     # launch on http://localhost:5000 (Codespaces will forward the port)
# in a new terminal:
make test    # quick smoke; may print 'no tests' which is OK
```

Troubleshooting:

If port toast says “exit code 127”, ignore it and run make run in the terminal.

To reset the venv: make clean-venv && make setup.
## How to run Clever locally

Requirements: Python 3.12. In Codespaces this repo already includes a devcontainer.

```bash
# from repo root
make setup   # create .venv, install deps, init DB
make run     # launch on http://localhost:5000 (Codespaces will forward the port)
# in a new terminal:
make test    # quick smoke; may print 'no tests' which is OK
```

Troubleshooting:

If port toast says “exit code 127”, ignore it and run make run in the terminal.

To reset the venv: make clean-venv && make setup.
>>>>>>> 79ac8fc (UI polish: input shortcuts, auto-fading panels, analysis bubbles; tasks.json; README run steps; favicon route.)
