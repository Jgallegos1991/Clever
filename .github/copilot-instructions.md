# Clever AI: Coding Agent Instructions

## Unbreakable Rules
1. **Strictly Offline:** Never add code that makes external network calls at runtime. All libraries and models must be local. Enforce with `utils.offline_guard.enable()`.
2. **Single-User Only:** The system is for "Jordan" (Jay). No user accounts, logins, or multi-tenancy. Personalize via `user_config.py`. The persona is a witty, empathetic female AI named "Clever".

## Architecture Overview
- **Framework:** Python 3.12 + Flask (`app.py`)
- **Database:** SQLite (`clever.db`, `clever_memory.db`) via `DatabaseManager` in `database.py`
- **Modular Monolith:** Key modules:
  - `app.py`: Flask routes, main logic
  - `persona.py`: PersonaEngine, response modes
  - `evolution_engine.py`: Self-learning, memory, growth metrics
  - `nlp_processor.py`: Local NLP (spaCy, VADER, TextBlob)
  - `debug_config.py`: Debugging, monitoring
- **Frontend:** `templates/index.html` (dark, particle UI), `static/css/style.css`, `static/js/main.js` (entry), engines under `static/js/`, performance modules

## Developer Workflows
- **Setup:**
  - `make setup` (base, offline)
  - `make setup-full` (full, downloads spaCy model)
  - `make run` (start Flask server)
  - `make file-inventory` (auto-generate file inventory)
- **Testing:**
  - `make test` (pytest, see `pytest.ini`)
  - `test-offline.sh` (validates offline operation)
- **Debugging:**
  - Use `debug_config.py` for logging, performance, error recovery

## Project Conventions
- **Config:** Always import user info from `user_config.py`
- **Database:** Use `DatabaseManager` with thread safety (`_lock`)
- **Error Handling:** Use debug system (`get_debugger`, `performance_monitor`)
- **File Sync:**
  - Sync dirs: `Clever_Sync/`, `synaptic_hub_sync/`
  - Ingestion: `pdf_ingestor.py` (PDFs), `file_ingestor.py` (text)
  - Watch: `sync_watcher.py` (uses watchdog)

## Integration Points
- **PersonaEngine:** Use established response modes (Auto, Creative, Deep Dive, Support, Quick Hit). Return `PersonaResponse` with `text`, `mode`, `sentiment`, `proactive_suggestions`.
- **Evolution Engine:** Always call `evolution_engine.log_interaction()` after user interactions.
- **Frontend:** Particle UI, frosted glass, neon accents. JS engines in `static/js/engines/`.
- **Health Monitoring:** `health_monitor.py` for system status.

## Source of Truth
- **File Inventory:** See `file-inventory.md` for file types, counts, and structure.
- **Documentation:** See `docs/` for architecture, API, UI, deployment.

## Example Patterns

**Thread-safe DB:**

```python
from database import DatabaseManager
db = DatabaseManager(config.DB_PATH)
# Always use with _lock for thread safety
```

**Debug Logging:**

```python
from debug_config import get_debugger
debugger = get_debugger()
debugger.info('module', 'Operation completed')
```

**Persona Response:**

```python
from persona import PersonaEngine
response = PersonaEngine().respond("Hello", mode="Auto")
```

---

*Update this file as the architecture evolves. For unclear or missing sections, ask Jay for clarification or review the latest `README.md` and `file-inventory.md`.*

## Request lifecycle (server-side)
- `app.py` wires debug systems, loads `user_config`, enforces offline via `utils.offline_guard.enable()`, initializes DB/NLP/persona with graceful fallbacks.
- Typical flow: request → optional NLP (`UnifiedNLPProcessor`) → persona generate → DB/evolution logging → response.

### Add a new Flask route (pattern)
```python
from flask import request, jsonify
from debug_config import get_debugger
from evolution_engine import get_evolution_engine

debugger = get_debugger()
evo = get_evolution_engine()

@app.route('/api/analyze', methods=['POST'])
def analyze():
  data = request.get_json(force=True)
  text = (data or {}).get('text', '')
  if not text:
    return jsonify({"error": "text required"}), 400
  # persona + evolution telemetry
  resp = clever_persona.generate(text, mode=data.get('mode', 'Auto'))
  evo.log_interaction({"user_input": text, "active_mode": resp.mode})
  debugger.info('api.analyze', 'analyzed text')
  return jsonify({"reply": resp.text, "mode": resp.mode, "sentiment": resp.sentiment})
```

### Enforce offline guard early
```python
from utils import offline_guard
offline_guard.enable()  # Allow loopback only; blocks external network
```

### Log interactions to evolution engine
```python
from evolution_engine import get_evolution_engine
evo = get_evolution_engine()
evo.log_interaction({"user_input": text, "active_mode": mode, "action_taken": "respond"})
```

### Database usage with thread safety
```python
from database import DatabaseManager
import config

db = DatabaseManager(config.DB_PATH)
with db._connect() as con:  # internal helper; prefer high-level methods when available
  con.execute('INSERT INTO utterances (role, text, mode, ts) VALUES (?,?,?,?)', ('user', text, mode, time.time()))
```

### File ingestion pipeline (outline)
- Watch dirs: `Clever_Sync/`, `synaptic_hub_sync/` via `sync_watcher.py` (watchdog).
- Ingest: `pdf_ingestor.py` for PDFs, `file_ingestor.py` for text → store in `sources` via `DatabaseManager.add_or_update_source()` with `content_hash`, `size`, `modified_ts`.

```python
from database import DatabaseManager
from pathlib import Path
import hashlib, time

def ingest_text(db: DatabaseManager, path: Path):
  content = path.read_text(errors='ignore')
  h = hashlib.sha256(content.encode('utf-8')).hexdigest()
  db.add_or_update_source(
    filename=path.name,
    path=str(path),
    content=content,
    content_hash=h,
    size=path.stat().st_size,
    modified_ts=path.stat().st_mtime,
  )
```

### Performance monitoring wrapper
```python
from debug_config import performance_monitor

@performance_monitor('app.generate_reply')
def generate_reply(text: str):
  return clever_persona.generate(text)
```

### Minimal pytest example
```python
def test_persona_auto_mode_smoke():
  from persona import PersonaEngine
  p = PersonaEngine()
  resp = p.generate("hello", mode="Auto")
  assert resp.text and resp.mode == "Auto"
```

### Frontend pattern (particles + core app)
- Main UI at `templates/index.html`; JS entry `static/js/core/app.js` controls particle engines under `static/js/engines/` and performance modules under `static/js/performance/`.
