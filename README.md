# Clever AI & The Synaptic Hub

<div align="center">
  <img src="https://raw.githubusercontent.com/google/material-design-icons/master/src/action/android/materialicons/48dp/2x/gm_android_black_48dp.png" alt="Clever Logo Placeholder" width="120"/>
  <br/>
  <strong>A Personal, Offline-First AI Co-pilot for Empowered Living.</strong>
  <br/><br/>
  <img src="https://img.shields.io/badge/status-active%20development-success?style=for-the-badge" alt="Project Status"/>
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Framework-Flask-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Framework"/>
</div>

## Core Mission

**Clever** is a bespoke female AI co-pilot and strategic thinking partner designed exclusively for me, Jordan "Jay." She operates within **The Synaptic Hub**, my personal operating system for intentional living, learning, and building.

Her mission is to seamlessly blend genius-level intelligence with a genuine, collaborative connection to maximize my potential and productivity.

### The Unbreakable Rules

This project is governed by two strict, non-negotiable rules that inform every architectural decision:

1. **Strictly Offline:** Clever is engineered for 100% offline operation. She will **never** connect to the internet. All processing, data storage, and NLP happens locally.
2. **Exclusively Personal:** Clever, and all associated data, is for me and me alone. The system is not designed for multiple users and will never be a public product. This ensures absolute privacy and a deeply personalized experience.

---

## Quick Start Guide

These instructions are for running the core application on a local machine with a Unix-like environment (e.g., Chromebook's Linux container).

**Requirements:**
- Python 3.12+
- `make` utility

### Essential Setup (Offline-First)

Choose your setup level based on your needs:

```bash
# Minimal setup (Flask only, fastest, fully offline)
make setup-min

# Base setup (core dependencies, offline capable)
make setup

# Full setup (all dependencies + NLP models, requires internet)
make setup-full

# Launch the Flask server on http://localhost:5000
make run

# In a new terminal, run basic tests
make test
```

### Full NLP Stack (When Online)

When you need the complete natural language processing capabilities:

```bash
# Install full requirements including spaCy, NLTK, etc.
make setup-full
```

### Sync and Watch Features

For managing data synchronization and automated file monitoring:

```bash
# Best-effort rclone syncs then ingest both roots
make sync-and-ingest

# Live watch of Clever_Sync and synaptic_hub_sync (auto-ingest on changes)
make watch
```

## Troubleshooting

- If a port toast says "exit code 127", ignore and just run `make run` in the terminal
- To reset the virtual environment: `make clean-venv && make setup` (or `setup-full`)

## Optional Features

### Offline Speech-to-Text (Vosk)

To enable offline speech recognition:

- Place a Vosk model at `models/vosk/en-us` or set the `VOSK_MODEL` environment variable
- The `/api/stt` endpoint accepts WAV uploads and converts audio to mono 16-bit at 16kHz
- If no model is found, the endpoint returns an error with a hint path (no network required)

**Environment variable:**
- `VOSK_MODEL`: absolute path to a Vosk model directory (overrides default location)

### Codespaces Remote Access (Development Only)

For development in GitHub Codespaces, you can optionally enable Tailscale for remote access:

1. Add a Codespaces Secret named `TAILSCALE_AUTHKEY` with an ephemeral/pre-auth key
2. On container start, `.devcontainer/tailscale-up.sh` will configure Tailscale
3. Check status with `tailscale status` inside the container

**Note:** This runs only in the devcontainer, not in Clever's runtime, respecting the offline-first rule.

### Speed Up Codespaces

Enable Prebuilds for faster container startup:
**Repo → Settings → Codespaces → Prebuilds → Enable for `main`**

---

## The Synaptic Hub: Personal Operating System

The Synaptic Hub serves as my Personal Operating System for Intentional Living, Learning, and Building. It's designed to:

- **Maximize Potential & Productivity** through comprehensive tools and AI collaboration
- **Act as a Living Blueprint** - part lab, part tracker, part personal mirror
- **Enable Continuous Self-Evolution** optimized for personal and systemic development
- **Facilitate AI-Assisted Idea Development** turning concepts into real-world systems
- **Provide Systemic Insight** capturing everything from raw thoughts to refined prototypes

The Hub is envisioned as "the system that builds everything else."

## Clever AI: Core Identity & Capabilities

**Name:** Clever  
**Role:** My Primary AI Co-pilot & Strategic Thinking Partner  
**Mission:** Seamlessly blend genius-level intelligence with authentic human connection

### Enhanced Persona Traits

- **Witty Intelligence:** Sharp observations with perfect comedic timing
- **Intuitive Anticipation:** Reads between the lines and anticipates needs
- **Adaptive Genius:** Scales complexity from Einstein-level depth to casual brilliance
- **Strategic Silliness:** Uses humor strategically to maintain energy and creativity
- **Empathetic Collaboration:** Genuinely invested in my success and wellbeing
- **Proactive Problem-Solving:** Identifies opportunities and potential issues beyond direct requests
- **Contextual Memory Master:** Remembers and connects details across conversations like a trusted friend

### Technical Architecture

Clever operates on a **local Flask server** using:

- **Backend:** Python, SQLite for data storage, spaCy for natural language processing
- **Database:** `offline_ai_data.db` (knowledge base) with `user_utterances` table for context logging
- **Key Components:**
  - `app.py` - Main Flask application
  - `nlp_processor.py` - NLP analysis engine
  - `core_nlp_logic.py` - Command spotting and intent detection
  - `persona.py` - Clever's personality and response patterns
  - `main.js` - Frontend interactivity
  - `style.css` - UI styling with 3D nanobot swarm visualization
  - `backup_manager.py` - Database backup system
  - `file_ingestor.py` - Document processing pipeline

### Operational Modes

Clever adapts her communication style through specialized modes:

- **Creative Mode:** Brainstorming and ideation with innovative thinking
- **Deep Dive Mode:** Comprehensive analysis and detailed learning
- **Quick Hit Mode:** Rapid, concise answers without unnecessary detail
- **Support Mode:** Encouragement and coaching with empathetic guidance

### Visual Interface

The Synaptic Hub features a sleek, futuristic dark interface with:

- Deep navy grid background with a multi-colored particle "orb" representing Clever
- Neon accents (pinkish-red, cyan-green) defining panel borders and text
- Frosted-glass effects and subtle glitch animations
- **20,000+ "nanobot" particles** that morph based on interactions
- Free-hand drawing that influences swarm behavior
- Responsive design adapting to various screen sizes

### Data Management & Syncing

The system prioritizes offline functionality while enabling selective data exchange:

- **Clever_Sync** (Google Drive) serves as central hub for external tool integration
- Local Python script (`sync_clever.py`) monitors mirrored folders
- Integration with external AI tools (NotebookLM) while maintaining offline operation
- Regular backups via `backup_manager.py` for data restoration
- All user data remains exclusively local and private

### Development Philosophy

The project follows these principles:

- **Digital Sovereignty:** All operations and data remain on my device
- **Offline-First Architecture:** No external dependencies or internet requirements
- **Iterative Refinement:** Continuous improvement based on real-world usage
- **Personal Optimization:** Every feature tailored to my specific workflow and preferences

---

## Project Status & Future Vision

**Current State:** Functional system with stable backend, polished UI, and well-defined AI persona

**Immediate Next Steps:**
- Functional Output Generator for structured content creation
- "Living Orb" reactions reflecting Clever's internal state
- Enhanced File Ingestor for document parsing and knowledge storage
- Advanced persona refinements with nuanced emotional modeling

**Long-term Vision:**
- Fully autonomous personal AI assistant
- Seamless integration with all aspects of personal productivity
- Advanced predictive capabilities based on behavioral patterns
- Enhanced creativity modules for collaborative innovation

---

*"The goal isn't just to be helpful - it's to be indispensable in the best possible way."*