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

.PHONY: default venv install setup setup-full setup-min run fmt lint test ingest freeze clean-venv watch sync-and-ingest help

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

# Minimal setup for offline-only operation (Flask only)
setup-min: venv
	$(ACTIVATE) && $(PIP) install -U pip wheel
	$(ACTIVATE) && $(PIP) install -r requirements-min.txt
	@echo "✅ Minimal env ready. Only Flask installed for offline-only testing."

# Base setup with core dependencies (offline capable)
setup: install
	@echo "✅ Env ready. DB will initialize on first app start at $$PWD/clever.db (offline runtime)."

# Full setup with all dependencies including NLP models (requires internet)
setup-full: install
	@test -f requirements.txt && ( $(ACTIVATE) && $(PIP) install -r requirements.txt ) || true
	@echo "📥 Downloading spaCy model (requires internet)..."
	@$(ACTIVATE) && python -m spacy download en_core_web_sm || echo "⚠️  spaCy model download failed - offline NLP may be limited"
	@echo "✅ Full env ready with NLP capabilities."

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

# Watch sync directories for changes and auto-ingest
watch:
	@echo "👀 Starting sync directory watcher..."
	$(ACTIVATE) && python sync_watcher.py

# Best-effort rclone syncs then ingest both roots
sync-and-ingest:
	@echo "🔄 Running sync tools and ingesting content..."
	$(ACTIVATE) && python sync_tools.py || echo "⚠️  sync_tools.py not found or failed"

freeze:
	$(ACTIVATE) && $(PIP) freeze > requirements-lock.txt && echo "📦 Wrote requirements-lock.txt"

clean-venv:
	rm -rf $(VENV)

help:
	@echo "Clever AI Development Commands:"
	@echo "  setup-min        Install minimal dependencies (Flask only, offline)"
	@echo "  setup            Install base dependencies (offline capable)"
	@echo "  setup-full       Install all dependencies + NLP models (requires internet)"
	@echo "  run              Start Flask development server"
	@echo "  test             Run pytest test suite"
	@echo "  watch            Monitor sync directories for changes"
	@echo "  sync-and-ingest  Run sync tools and ingest content"
	@echo "  ingest           Trigger manual ingestion via API"
	@echo "  fmt              Format code with black"
	@echo "  lint             Lint code with flake8"
	@echo "  freeze           Generate requirements-lock.txt"
	@echo "  clean-venv       Remove virtual environment"
