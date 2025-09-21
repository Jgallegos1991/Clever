"""Legacy ad-hoc test runner (archived).

Why: Originally orchestrated a bespoke sequence of assertions before the project
standardized on pytest. Retained only to show historical testing approach.
Where: Archived under `legacy/`; no longer imported. Modern testing occurs via
`tests/` directory and `make test` / CI workflow.
How: Reduced to documentation-only placeholder to avoid drift and accidental usage;
original imperative logic is recoverable from Git history if ever needed.

Connects to:
	- tests/ (pytest suite): Current authoritative test suite
	- Makefile (test target): Replacement execution path
"""
