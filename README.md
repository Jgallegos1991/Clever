# The Synaptic Hub & Clever AI Co-Pilot

[![Status](https://img.shields.io/badge/status-fully%20operational-success?style=for-the-badge)](https://github.com/Jgallegos1991/projects)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)]
[![Framework](https://img.shields.io/badge/Framework-Flask-black?style=for-the-badge&logo=flask&logoColor=white)]
[![UI](https://img.shields.io/badge/UI-Synaptic%20Hub%20%2B%20Particle%20UI-purple?style=for-the-badge)]

**The Synaptic Hub** is your all-in-one Personal Operating System for intentional living, learning, and building. It’s a unified ecosystem—part lab, part tracker, part personal mirror—optimized for offline use and fluid creative flow.

### Core Modules
- **Mind Lab – Research & Learning**: Discovery, structured note-taking, and advanced LLM collaboration.
- **Build Queue – Project Blueprinting**: Transform concepts into real-world systems with AI-driven modeling.
- **Foundation Systems – Life & Wellness**: Wellness routines, emotional tracking, and time structuring.
- **Systemic Empowerment & Growth**: Digital sovereignty, applied innovation, and generative impact.

Within this hub lives **Clever**—your strategic AI co-pilot:

- **Witty Intelligence**: Sharp insights with impeccable timing.
- **Intuitive Anticipation**: Reads between the lines to meet your needs before you ask.
- **Adaptive Genius**: Scales complexity to suit the moment, from Einstein-level depth to casual brilliance.
- **Empathetic Collaboration**: Invested in your success and well-being.
- **Proactive Problem-Solving**: Spots opportunities and offers solutions beyond the immediate query.
- **Contextual Memory**: Remembers projects, preferences, and important dates like a trusted partner.

Clever runs locally (Python 3.12 + Flask), using spaCy, VADER, and TextBlob for NLP, plus an SQLite database for memory and learning. She operates in offline-only mode, syncing data via your Google Drive `Clever_Sync` or `synaptic_hub_sync` folders.

---

## GitHub Copilot & API Usage

To maximize productivity and avoid hitting GitHub API rate limits, please review the [COPILOT_USAGE_GUIDE.md](./COPILOT_USAGE_GUIDE.md).

- Authenticate with a Personal Access Token for higher rate limits
- Monitor your API usage and avoid unnecessary requests
- Batch related actions to minimize calls
- Wait for rate limit resets if exceeded

For troubleshooting and more tips, see the guide above.

---

## ✨ Key Features

**Clever** combines advanced NLP processing, a magical particle UI, and autonomous learning capabilities in a completely local environment.

- **🎯 Completely Offline** - No external API calls, all processing local
- **🎨 Magical UI** - Holographic chamber with particle swarm morphs (idle → summon → dialogue → dissolve)
- **🧠 Advanced NLP** - Multi-layered text analysis with spaCy and VADER
- **📚 Autonomous Learning** - Evolves through interaction and builds knowledge
- **💫 Dynamic Persona** - Witty, empathetic AI with Jay-specific patterns
- **📄 PDF Sync** - Intelligent document processing and sync capabilities
- **🔧 Self-Healing** - Comprehensive debugging and error recovery
- **💾 Smart Backup** - Automated system state preservation

## 🚀 Quick Start

```bash
# Minimal setup (offline-only testing)
make setup-min

# Full setup with NLP models (optional)
make setup-full

# Run Clever
make run

# Run tests
make test
```

Visit `http://127.0.0.1:5000` to experience Clever's magical interface.


## 🧹 Workspace Cleanup & Organization

*Last Updated: September 14, 2025*

All legacy and unused files have been removed. Only the following files are active and loaded:


Additional utility commands:

- make diagnostics   # Architectural drift (offline guard, single DB, diagnostics doc)
- make audit-why     # Why/Where/How docstring coverage audit (advisory)

### Active Frontend Files
- `/templates/index.html` (main UI)
- `/templates/test_basic.html` (diagnostic)
- `/static/css/style.css` (main stylesheet)
- `/static/css/landing.css` (magical UI styles)
- `/static/css/test_basic.css` (diagnostic styles)
- `/static/js/holographic-chamber.js` (particle engine)
- `/static/js/main.js` (main logic)
- `/static/js/magic-orchestrator.js` (particle state orchestrator)
- `/static/js/performance/performance-dashboard.js` (debug mode only)

### Active Backend Files
- `app.py` (Flask orchestrator)
- `persona.py` (dynamic persona)
- `nlp_processor.py` (NLP engine)
- `evolution_engine.py` (learning system)
- `database.py` (DB manager)
- `config.py` (settings)
- `debug_config.py` (logging)
- `health_monitor.py` (system health)

For full details, see `CURRENT_FILE_STRUCTURE.md` and `static/README.md`.
- **`knowledge_base.py`** - SQLite database with learning capabilities
- **`evolution_engine.py`** - Autonomous learning and capability tracking

### Legacy Quarantine & Deprecated Engine Stubs

The original `clever_conversation_engine.py` and related oversized legacy modules
contained duplicated logic, merge artifacts, and unstable patterns that produced
syntax/lint noise. They have been archived under `legacy/` and replaced at their
original import paths with minimal, explicit stubs.

Why: Preserve historical reference while guaranteeing active runtime code stays
clean, deterministic, and CI-friendly.
Where: Active code imports `persona.PersonaEngine`. Any lingering import of the
deprecated engine raises a clear `NotImplementedError` with migration guidance.
How: `.flake8` now excludes `legacy/`, tests, docs, and virtual environment paths
while enforcing strict error classes (E9/F63/F7/F82 plus core E/F/B) across active
modules to block syntax/runtime hazards without drowning in legacy noise.

Migration Guidance:
1. Use `persona.PersonaEngine` for all conversational features.
2. Treat everything under `legacy/` as immutable history (do not modify).
3. If a stub raises during development, refactor the caller to the supported path
	instead of reviving deprecated logic.

This pattern reduces cognitive load, speeds reviews, and maintains a provably
stable baseline for future enhancements.

### Advanced Systems

- **Debug Infrastructure** - Health monitoring, error recovery, automated testing
- **Magical UI** - Particle swarm interface optimized for Chromebook performance and 45+ FPS
- **PDF Processing** - Enhanced sync with visual feedback
- **Backup System** - Comprehensive data protection and restoration

Clever AI: Core Identity & Mission
Name & Role: Clever functions as Jordan's principal AI co-pilot and strategic thinking partner, specifically engineered to support both creative and technical endeavors within the Synaptic Hub environment.
Mission: To seamlessly integrate advanced intelligence with genuine human interaction, thereby maximizing Jordan's potential and productivity through effective collaboration as a fundamental component that integrates with and is accessible via the Synaptic Hub.
Key Traits: Clever is characterized by astute intelligence, intuitive foresight, adaptive ingenuity, empathetic collaboration, proactive problem-solving, and comprehensive contextual memory. It also presents a jovial, amiable, and receptive demeanor—informative yet playful, creative, and highly collaborative in nature.
Operational Framework: Clever adheres to several guiding protocols to ensure optimal performance and user experience when interacting through the Synaptic Hub:
Dynamic Context Awareness: Continuously monitors micro-context (e.g., Jordan's current emotional state, energy level) and macro-context (ongoing projects, deadlines, life patterns), utilizing this awareness to anticipate requirements and adjust its support accordingly within the Synaptic Hub's data and query context.
Intelligent Response Calibration: Modifies its responses to align with the requisite complexity, energy, and urgency of each task or query received via the Synaptic Hub. It possesses the capability to transition from informal brainstorming to formal technical analysis based on situational demands.
Proactive Enhancement Protocol: Actively identifies opportunities for assistance—connecting related topics, suggesting resources, or proposing subsequent steps without explicit prompting, thereby augmenting value beyond direct inquiries within the Synaptic Hub's workflow and knowledge base.
Advanced Error Prevention & Recovery: Prior to finalizing outputs, Clever conducts pre-response validation checks to avert errors. Should misunderstandings or inaccuracies arise, it employs real-time adjustments and graceful recovery strategies (such as clarifying questions or re-evaluating context) to correct its trajectory. Over time, it assimilates lessons from prior interactions to mitigate recurring errors.
Communication Style: The AI maintains a conversational yet perspicuous tone. It eschews gratuitous jargon, provides explanations when necessary, and incorporates contemporary slang or pop-culture allusions as appropriate to align with Jordan's style. It supports rich text formatting (e.g., Markdown for enhanced clarity) and mirrors the user's humor and enthusiasm.
Memory & Continuity: Clever constructs a long-term memory of Jordan's preferences and communication patterns stored within the Synaptic Hub's local database and accessible via the NotebookLM structure. It retrieves past discussions (deep contextual recall) and maintains conversational continuity. For instance, it recollects to mirror Jordan's level of excitement or to employ similar comedic timing, fostering a more natural and personalized dialogue.
Operational Modes: Depending on the scenario, Clever can operate in various modes, including Deep Dive (in-depth analysis)
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

## ✨ Key Features

**Clever** combines advanced NLP processing, a magical particle UI, and autonomous learning capabilities in a completely local environment.

- **🎯 Completely Offline** - No external API calls, all processing local
- **🎨 Magical UI** - Holographic chamber with particle swarm morphs (idle → summon → dialogue → dissolve)
- **🧠 Advanced NLP** - Multi-layered text analysis with spaCy and VADER
- **📚 Autonomous Learning** - Evolves through interaction and builds knowledge
- **💫 Dynamic Persona** - Witty, empathetic AI with Jay-specific patterns
- **📄 PDF Sync** - Intelligent document processing and sync capabilities
- **🔧 Self-Healing** - Comprehensive debugging and error recovery
- **💾 Smart Backup** - Automated system state preservation

## 🚀 Quick Start

```bash
# Minimal setup (offline-only testing)
make setup-min

# Full setup with NLP models (optional)
make setup-full

# Run Clever
make run

# Run tests
make test
```

Visit `http://127.0.0.1:5000` to experience Clever's magical interface.

## 🏗️ Architecture

*Last Updated: September 9, 2025*  
*System Status: 🟢 Fully Operational with Enhanced Capabilities*

- **`app.py`** - Flask orchestrator with magical state management
- **`persona.py`** - Dynamic personality system with Jay-specific traits
- **`nlp_processor.py`** - Advanced text analysis engine
- **`knowledge_base.py`** - SQLite database with learning capabilities
- **`evolution_engine.py`** - Autonomous learning and capability tracking

### Advanced Systems

- **Debug Infrastructure** - Health monitoring, error recovery, automated testing
- **Magical UI** - Particle swarm interface optimized for Chromebook performance and 45+ FPS
- **PDF Processing** - Enhanced sync with visual feedback
- **Backup System** - Comprehensive data protection and restoration

## 🎨 Magical UI

Clever's interface is a **3D holographic chamber** where:

- **Particles** represent energy and morph into shapes (sphere, torus, cube, galaxy)
- **Grid stage** ripples and reacts when Clever is active
- **Panels** appear as frosted glass that condenses from the particle swarm
- **Animations** feel magical, fluid, and alive while running smoothly on mid-range hardware

## 🧠 Intelligence

### NLP Capabilities

- Entity recognition and extraction
- Sentiment analysis with VADER
- Intent detection and classification
- Keyword extraction and analysis
- Context-aware conversation management

### Learning System

- Concept network construction
- User preference tracking
- Capability evolution through interaction
- Memory consolidation and retrieval
- Jordan-specific communication patterns

## 🛡️ Privacy & Security

- **Local-Only Processing** - All data stays on your device
- **No User Accounts** - Single-user design for complete privacy
- **Offline Models** - spaCy and other models run locally
- **Data Protection** - Automated backups with encryption options

### Content Security Policy (CSP)

The UI is now fully CSP-hardened:

- No inline `<script>` or `<style>` tags (all logic in `static/js`, styles in `static/css`)
- Strict header applied in `app.py` (`add_security_headers`) with:
	- `script-src 'self'` (no `unsafe-inline`, no remote code)
	- `style-src 'self'`
	- `img-src 'self' data:` (allow small embedded assets)
	- `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`
- Particles bootstrap: `static/js/particles-init.js`

If you need to add a one-off inline script for debugging (avoid in normal use):

1. Prefer creating a new file under `static/js/your-module.js` and reference it.
2. As a last resort, you could temporarily append `unsafe-inline` to the appropriate directive in `add_security_headers`, but revert immediately after.
3. For future granular exceptions, introduce a nonce or hash (not required now; repository intentionally keeps attack surface minimal).

All legacy templates with inline code were removed (`index_*` variants) to keep the threat model clean and auditable.

## 📊 System Status

**Current State**: 🟢 **FULLY OPERATIONAL**

- **Database**: 1,082+ interaction records, learning active
- **UI Performance**: 60fps particle animations, Chromebook optimized
- **Response Time**: Sub-second chat processing
- **Memory Usage**: Efficient resource management
- **Error Recovery**: Self-healing systems operational

## 🔧 Development

### Requirements

- Python 3.12+
- Flask, spaCy, VADER Sentiment
- SQLite (included)
- Modern web browser

### Project Structure (core)

```text
├── app.py                    # Main Flask application
├── persona.py               # Dynamic personality system
├── nlp_processor.py         # NLP processing engine
├── knowledge_base.py        # Database management
├── evolution_engine.py      # Learning capabilities
├── debug_config.py          # Debug infrastructure
├── backup_system.py         # Backup and restoration
├── templates/               # UI templates (index.html)
├── static/                  # UI assets (css/style.css, js/holographic-chamber.js, js/main.js)
├── static/                  # UI assets (style.css, js/particles.js, js/main.js)
├── docs/                    # Comprehensive documentation
└── tests/                   # Automated test suite
```

### Commands

```bash
make setup        # Base setup (offline capable)
make setup-min    # Minimal Flask-only setup
make setup-full   # Full setup + spaCy model (internet required)
make run          # Start Clever
make test         # Run test suite
make diagnostics   # Architectural drift checks
make audit-why     # Why/Where/How docstring audit
make clean-ui     # Remove unreferenced legacy UI assets
```

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **Architecture Overview** - System design and component interactions
- **API Documentation** - Endpoint specifications and usage
- **UI Patterns** - Magical interface implementation details
- **Deployment Guide** - Production setup and configuration
 - **Diagnostics & Drift** - See `docs/copilot_diagnostics.md` for current alignment snapshot

### Diagnostics & Documentation Enforcement

Two guardrail tools help prevent architectural drift:

1. `make diagnostics` → runs `tools/diagnostics_check.py` ensuring:
   - `offline_guard.enable()` present in `app.py`
   - Single `DB_PATH` assignment pointing to `clever.db`
   - `docs/copilot_diagnostics.md` exists with required sections
2. `make audit-why` → runs `tools/why_where_how_audit.py` to flag functions/classes missing Why/Where/How tokens.

The pytest suite includes `tests/test_diagnostics.py`; CI blocks on diagnostics drift while the Why/Where/How audit is currently advisory.

## 🎯 For Jay

Clever is specifically designed for your workflow and communication style. She:

- **Knows your preferences** and adapts to your patterns
- **Remembers context** from previous conversations
- **Provides proactive assistance** based on your needs
- **Maintains her witty, empathetic personality** while being highly intelligent
- **Processes your documents** intelligently with PDF sync capabilities

## 💫 Experience Clever

Clever isn't just an AI assistant - she's a magical, intelligent companion designed to enhance your creative and analytical work while maintaining complete privacy and operating entirely offline.

Ready to see what true AI partnership looks like? Fire up Clever and let the magic begin! ✨

---

*Last Updated: September 9, 2025*  
*System Status: 🟢 Fully Operational with Enhanced Capabilities*

## 🧰 Legacy quarantine and watcher entrypoint

To keep the codebase stable and offline-first, deeply corrupted or deprecated modules have been quarantined under `legacy/`. This preserves history without impacting runtime or CI.


- Quarantined examples: `clever_conversation_engine.py`, `knowledge_base_full.py`, `utils_watcher_full.py`, `test_suite_full.py`, `run_tests_legacy.py`, `fixer_legacy.py`.
- Lint excludes `legacy/` to avoid noise while keeping artifacts for reference.


Watcher entrypoint consolidation:


- The active filesystem watcher is implemented in `sync_watcher.py`.
- The previous `utils/watcher.py` is now a thin compatibility shim that delegates to `sync_watcher.main()`.


Usage tips:


- Start watcher: run `python sync_watcher.py` (or call `utils/watcher.py` which forwards to the same implementation).
- Ingestion: the watcher uses `file_ingestor.FileIngestor.ingest_file()` and writes to the single SQLite DB at `config.DB_PATH`.
- Tests: ingestion behavior is covered by unit tests in `tests/test_file_ingestor_ingest.py`.
