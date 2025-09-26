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

.PHONY: default venv install setup setup-full setup-min run fmt lint test ingest ingest-pdfs freeze clean-venv watch watch-pdfs sync-and-ingest tailscale-setup tailscale-status help docstrings memory-status memory-optimize memory-monitor memory-emergency

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
	# Run diagnostics drift check before executing full test suite
	$(ACTIVATE) && $(PY) tools/diagnostics_check.py
	$(ACTIVATE) && pytest

# Enforce Why/Where/How docstring presence across codebase
docstrings:
	$(ACTIVATE) && $(PY) tools/docstring_enforcer.py --fail-on-missing --min-coverage 0.90 || (echo "❌ Docstring enforcement failed" && exit 1)

# Auto-generate file inventory
file-inventory:
	$(ACTIVATE) && python tools/generate_file_inventory.py
	@test -d tests && ( $(ACTIVATE) && pytest -q ) || echo "No tests/ directory; skipping."

ingest:
	@echo "POST /ingest"
	@curl -s -X POST http://127.0.0.1:$(PORT)/ingest \
		-H "Content-Type: application/json" \
		-d '{"action":"scan"}' || true

# Enhanced PDF ingestion
ingest-pdfs:
	@echo "📚 Processing PDFs and documents..."
	$(ACTIVATE) && python pdf_ingestor.py

# Ingest knowledge from Clever_Learn directory
ingest-knowledge:
	@echo "🧠 Ingesting knowledge files from Clever_Learn..."
	$(ACTIVATE) && python ingest_knowledge.py --verbose

# Watch sync directories for changes and auto-ingest  
watch:
	@echo "👀 Starting sync directory watcher..."
	$(ACTIVATE) && python sync_watcher.py

# Enhanced file watcher with PDF support
watch-pdfs:
	@echo "👁️  Starting enhanced file watcher with PDF support..."
	$(ACTIVATE) && python pdf_ingestor.py watch

# Best-effort rclone syncs then ingest both roots
sync-and-ingest:
	@echo "🔄 Running sync tools and ingesting content..."
	$(ACTIVATE) && python sync_tools.py || echo "⚠️  sync_tools.py not found or failed"

# Tailscale setup and management
tailscale-setup:
	@echo "🔧 Setting up Tailscale for Jay (lapirfta@gmail.com)..."
	./setup_tailscale.sh

tailscale-fix:
	@echo "🔧 Fixing Tailscale connection issues..."
	./fix_tailscale.sh

tailscale-status:
	@echo "📊 Tailscale Status:"
	@tailscale status || echo "❌ Tailscale not running"
	@echo ""
	@echo "🌐 Tailscale IP:"
	@tailscale ip -4 2>/dev/null || echo "❌ No Tailscale IP"

# Google Drive PDF sync
setup-gdrive:
	@echo "📁 Setting up Google Drive PDF sync..."
	./setup_gdrive_sync.sh

setup-rclone:
	@echo "🚀 Setting up rclone Google Drive integration..."
	./setup_rclone_gdrive.sh

sync-pdfs:
	@echo "🔄 Syncing PDFs from Google Drive..."
	./sync_pdfs.sh || echo "❌ PDF sync failed - run 'make setup-gdrive' first"

rclone-sync:
	@echo "🔄 Syncing from Google Drive via rclone..."
	./rclone_sync_clever.sh || echo "❌ rclone sync failed - run 'make setup-rclone' first"

watch-gdrive:
	@echo "👁️  Starting Google Drive PDF monitoring..."
	./watch_gdrive_pdfs.sh || echo "❌ PDF watcher failed - run 'make setup-gdrive' first"

rclone-watch:
	@echo "👁️  Starting rclone Google Drive monitoring..."
	./watch_rclone_sync.sh || echo "❌ rclone watcher failed - run 'make setup-rclone' first"

rclone-test:
	@echo "🧪 Testing rclone connection..."
	@rclone listremotes && echo "✅ rclone available" || echo "❌ rclone not configured"

# Phone access fixes for container environments
fix-phone-access:
	@echo "🔧 Fixing phone access in container environment..."
	./fix_container_phone_access.sh

start-ngrok:
	@echo "🚀 Starting ngrok tunnel for phone access..."
	./start_ngrok.sh || echo "❌ Run 'make fix-phone-access' first"

phone-help:
	@echo "📱 Getting phone access options..."
	./phone_access.sh || echo "❌ Run 'make fix-phone-access' first"

freeze:
	$(ACTIVATE) && $(PIP) freeze > requirements-lock.txt && echo "📦 Wrote requirements-lock.txt"

clean-venv:
	rm -rf $(VENV)

# Remove root-level screenshot and image assets
clean-images:
	@echo "🗑️ Removing root-level screenshot assets..."
	@git rm -f *.png || true
	@echo "✅ Root image assets removed from git"

help:
	@echo "Clever AI Development Commands:"
	@echo ""
	@echo "🏗️  Setup Commands:"
	@echo "  setup-min        Install minimal dependencies (Flask only, offline)"
	@echo "  setup            Install base dependencies (offline capable)"
	@echo "  setup-full       Install all dependencies + NLP models (requires internet)"
	@echo ""
	@echo "🚀 Core Commands:"
	@echo "  run              Start Flask development server"
	@echo "  test             Run pytest test suite"
	@echo "  fmt              Format code with black"
	@echo "  lint             Lint code with flake8"
	@echo "  validate         Validate documentation and architecture standards"
	@echo ""
	@echo "📚 Content Processing:"
	@echo "  ingest           Trigger manual ingestion via API"
	@echo "  ingest-pdfs      Process PDFs and documents in Clever_Learn/"
	@echo "  watch            Monitor sync directories for changes"
	@echo "  watch-pdfs       Enhanced file watcher with PDF support"
	@echo "  sync-and-ingest  Run sync tools and ingest content"
	@echo ""
	@echo "☁️  Google Drive Integration:"
	@echo "  setup-gdrive     Set up local Google Drive PDF sync"
	@echo "  setup-rclone     Set up rclone Google Drive integration"
	@echo "  sync-pdfs        Sync PDFs from Google Drive (local method)"
	@echo "  rclone-sync      Sync from Google Drive via rclone"
	@echo "  watch-gdrive     Monitor Google Drive continuously (local method)"
	@echo "  rclone-watch     Monitor Google Drive via rclone"
	@echo "  rclone-test      Test rclone connection"
	@echo ""
	@echo "🌐 Remote Access:"
	@echo "  tailscale-setup  Configure Tailscale for secure remote access"
	@echo "  tailscale-fix    Fix Tailscale connection issues"
	@echo "  tailscale-status Check Tailscale connection status"
	@echo "  fix-phone-access Fix phone access in container environments"
	@echo "  start-ngrok      Start ngrok tunnel for phone access"
	@echo ""
evolution-status:
	@echo "🧠 Checking Clever's Evolution Status..."
	@$(ACTIVATE) && $(PY) -c "from evolution_engine import get_evolution_engine; import json; engine = get_evolution_engine(); status = engine.get_evolution_status(); print(f'🌟 Evolution Score: {status[\"evolution_score\"]:.1%}'); print(f'🔗 Concepts: {status[\"concept_count\"]}'); print(f'⚡ Connections: {status[\"connection_count\"]}'); print(f'📊 Network Density: {status[\"network_density\"]:.1%}'); print('🚀 Top Capabilities:'); [print(f'  {cap.replace(\"_\", \" \").title()}: {level:.1%}') for cap, level in sorted(status.get('capabilities', {}).items(), key=lambda x: x[1], reverse=True)[:5]]; print('📈 Recent Evolution Events:'); [print(f'  {event[1]}') for event in status.get('recent_events', [])[:3]]"

trigger-evolution:
	@echo "✨ Triggering Evolution Cascade..."
	@$(ACTIVATE) && $(PY) -c "from evolution_engine import get_evolution_engine; engine = get_evolution_engine(); clusters = engine.trigger_evolution_cascade(); print(f'🌟 Evolution cascade completed!'); print(f'🔮 Discovered {len(clusters)} knowledge clusters'); [print(f'  Cluster {i+1}: {cluster[\"size\"]} concepts') for i, cluster in enumerate(clusters[:3])]"

evolution-learn:
	@echo "📚 Triggering Learning from Sync Folder..."
	@$(ACTIVATE) && $(PY) -c "from file_ingestor import FileIngestor; from evolution_engine import get_evolution_engine; print('🔍 Scanning for new knowledge...'); ingestor = FileIngestor('./Clever_Sync'); ingestor.ingest_all_files(); print('🧠 Processing evolution learning...'); engine = get_evolution_engine(); status = engine.get_evolution_status(); print(f'✨ Learning complete! Evolution: {status[\"evolution_score\"]:.1%}')"

	@echo "🔧 Maintenance:"
	@echo "  freeze           Generate requirements-lock.txt"
	@echo "  clean-venv       Remove virtual environment"
	@echo "  freeze           Generate requirements-lock.txt"
	@echo "  clean-venv       Remove virtual environment"
	@echo ""
	@echo "🧠 Evolution Commands:"
	@echo "  evolution-status Check Clever's current intelligence level"
	@echo "  trigger-evolution Force evolution cascade"
	@echo "  evolution-learn  Learn from all sync folder content"

# Diagnostics alignment (Why/Where/How + offline + single DB)
.PHONY: diagnostics audit-why
diagnostics:
	$(ACTIVATE) && $(PY) tools/diagnostics_check.py

audit-why:
	$(ACTIVATE) && $(PY) tools/why_where_how_audit.py

# Remove unreferenced legacy UI assets and templates
.PHONY: clean-ui
clean-ui:
	@echo "🧹 Cleaning legacy UI assets..."
	$(ACTIVATE) && $(PY) tools/clean_ui_assets.py
	@echo "✅ UI cleanup complete"

# Build an offline bundle with all Python wheels and sources
.PHONY: bundle-offline
bundle-offline:
	@echo "📦 Building offline bundle..."
	@chmod +x tools/offline_bundle.sh
	@tools/offline_bundle.sh
	@echo "✅ Offline bundle ready: clever_offline_bundle.tgz"

# Memory Management Commands for Chromebook Development
memory-status:
	@echo "🧠 Checking Clever memory status..."
	@$(ACTIVATE) && python3 clever_memory_manager.py status

memory-optimize:
	@echo "🔧 Optimizing Clever memory usage..."
	@$(ACTIVATE) && python3 clever_memory_manager.py optimize

memory-monitor:
	@echo "🔍 Starting continuous memory monitoring..."
	@echo "Press Ctrl+C to stop monitoring"
	@$(ACTIVATE) && python3 clever_memory_manager.py monitor

memory-emergency:
	@echo "🚨 EMERGENCY: Applying aggressive memory optimization..."
	@$(ACTIVATE) && python3 clever_memory_manager.py emergency
