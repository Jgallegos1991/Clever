# Makefile — Clever (offline-first, Jay-only)
# Usage:
#   make setup          # create venv + install deps (base + full if present)
#   make run            # start Flask on http://localhost:5000
#   make fmt            # format python with black
#   make lint           # lint python with flake8
#   make test           # run pytest if tests/ exists
#   make ingest         # trigger a local ingestion POST
#   make freeze         # write requirements-lock.txt
#   make clean-venv     # remove .venv

.PHONY: default venv install setup setup-full run fmt lint test ingest freeze clean-venv help

PY ?= python3
VENV ?= .venv
PIP  = $(PY) -m pip
ACTIVATE = . $(VENV)/bin/activate

FLASK_APP ?= app.py
FLASK_ENV ?= development
HOST ?= 0.0.0.0
PORT ?= 5000

default: run

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(ACTIVATE) && $(PIP) install -U pip wheel
	@test -f requirements-base.txt && ( $(ACTIVATE) && $(PIP) install -r requirements-base.txt ) || true
	@test -f requirements.txt      && ( $(ACTIVATE) && $(PIP) install -r requirements.txt )      || true

setup: install
	@echo "✅ Env ready. DB will initialize on first app start at $$PWD/clever.db (offline runtime)."

# Alias kept for muscle memory
setup-full: install

run:
	$(ACTIVATE) && FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run --host=$(HOST) --port=$(PORT)

fmt:
	$(ACTIVATE) && black .

lint:
	$(ACTIVATE) && flake8 .

test:
	@test -d tests && ( $(ACTIVATE) && pytest -q ) || echo "No tests/ directory; skipping."

ingest:
	@echo "POST /ingest"
	@curl -s -X POST http://127.0.0.1:$(PORT)/ingest \
		-H "Content-Type: application/json" \
		-d '{"action":"scan"}' || true

freeze:
	$(ACTIVATE) && $(PIP) freeze > requirements-lock.txt && echo "📦 Wrote requirements-lock.txt"

clean-venv:
	rm -rf $(VENV)

help:
	@echo "Targets: setup, run, fmt, lint, test, ingest, freeze, clean-venv"
