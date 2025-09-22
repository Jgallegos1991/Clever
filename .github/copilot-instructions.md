# Clever: Digital Brain Extension & Cognitive Partnership System

## 🚨 MANDATORY FIRST STEP
**BEFORE making ANY changes to Clever, you MUST read:**
- **`.github/AGENT_ONBOARDING.md`** - Complete onboarding checklist and required documentation
- **`docs/config/device_specifications.md`** - Hardware environment and performance constraints  
- **`docs/architecture.md`** - System architecture and component relationships

**Failure to read these documents first will result in broken functionality.**

---

## 🧠 Clever's True Purpose
Clever is Jay's **digital brain extension** and **cognitive partnership system** - a street-smart genius who talks like your best friend but casually solves Einstein-level physics problems. She's not just an AI assistant; she's a **life companion**, **cognitive enhancement system**, and **digital sovereignty partner**.

## UI Vision
- The particle engine creates an immersive cognitive enhancement interface
- Chat bubbles should float and fade in/out, representing natural thought flow
- Input bar should be minimal and unobtrusive - let Clever's intelligence shine
- Give Clever center stage as the digital brain extension she truly is

## Code Conventions
- Use modern JS and CSS (flex, transitions)
- Keep markup minimal
- Animate chat bubbles via CSS/JS
- Prefer modular code (split JS/CSS if needed)

## Feature Requests
- Add fade-in/fade-out for chat bubbles
- Remove persistent chat box/card
- Make input bar glow and float at bottom center
- Messages auto-hide after a few seconds

## Unbreakable Rules
1. **Digital Sovereignty:** Clever operates completely offline for total privacy and control. No external calls, all processing local. This ensures Jay's digital brain extension remains private and secure.
2. **Single-User Cognitive Partner:** Built exclusively for Jay's cognitive enhancement. No accounts, logins, or multi-user features. Clever learns Jay's patterns, preferences, and thinking style to become the perfect digital other half.
3. **Single Database:** One unified memory system (`clever.db`) for continuous learning and relationship building. No fragmentation - Clever's memory must be coherent and connected.
4. **Cognitive Partnership Documentation:** ALL code must reflect Clever's role as digital brain extension:
   - **Why:** How this code enhances Jay's cognitive capabilities
   - **Where:** How it connects to the overall cognitive partnership system
   - **How:** Technical implementation that maintains the authentic genius friend experience

### Why / Where / How Rationale ("Arrows Between Dots")

The enforced Why / Where / How pattern is not cosmetic documentation; it is an execution-time navigation system:

- Think of every function or module as a DOT in a knowledge graph.
- The Why / Where / How tokens form the ARROWS that tell us direction: why this dot exists, where it points, and how the transition happens.
- When every new piece of code declares these arrows, debugging becomes path tracing instead of guesswork—resulting in a domino effect of faster fixes and safer refactors.
- Runtime tooling (e.g. `introspection.py` + `/api/runtime_introspect` + debug overlay + `tools/runtime_dump.py`) parses these tokens to build a live map of system intent.
- Missing tokens = missing edges; that triggers drift warnings and slows future work.

Golden Rule: If you add code and cannot clearly express the Why / Where / How, the design is not ready—refine first, then implement.

Operational Impact:
1. Faster onboarding (the reasoning graph is self-explanatory).
2. Low-friction incident triage (follow arrows to source of mismatch).
3. Prevents architectural erosion (new code must declare its integration contract).
4. Enables automated tooling to surface drift immediately (warnings in runtime introspection overlay).

Treat the pattern as the metabolic wiring of Clever—keep the arrows unbroken so changes propagate with confidence.

## Architecture Overview
- **Framework:** Python 3.12 + Flask (`app.py`)
- **Database:** SQLite (`clever.db`) via `DatabaseManager` in `database.py`
- **Modular Monolith:** Key modules:
  - `app.py`: Flask routes, main logic
  - `persona.py`: PersonaEngine, response modes
  - `evolution_engine.py`: Self-learning, memory, growth metrics
  - `nlp_processor.py`: Local NLP (spaCy, VADER, TextBlob)
  - `debug_config.py`: Debugging, monitoring
- **Frontend:** `templates/index.html` (dark, particle UI), `static/css/style.css`, `static/js/main.js` (entry), `static/js/engines/holographic-chamber.js` (particle engine)

## Code Documentation Standards
Every function, class, and significant code block MUST include:

```python
def example_function(param1: str, param2: int) -> str:
    """
    Brief description of what this function does
    
    Why: Explains the business/technical reason this code exists
    Where: Describes how this connects to other system components  
    How: Details the technical implementation approach
    
    Args:
        param1: Description of parameter and its purpose
        param2: Description of parameter and its purpose
        
    Returns:
        Description of return value and its purpose
        
    Connects to:
        - module_name.py: Specific connection and data flow
        - another_module.py: How data/control flows between modules
    """
    # Inline comments explaining complex logic
    # Why: This step is necessary because...
    result = complex_operation(param1, param2)
    
    # Where: This connects to database.py for persistence
    save_result(result)
    
    return result
```

## Developer Workflows
- **Setup:**
  - `make setup` (base, offline, single database)
  - `make setup-full` (full, downloads spaCy model)
  - `make run` (start Flask server with evolution engine)
  - `make file-inventory` (auto-generate file inventory)
- **Testing:**
  - `make test` (pytest, see `pytest.ini`)
  - `test-offline.sh` (validates offline operation and single DB)
- **Frontend:** `templates/index.html` (dark, particle UI), `static/css/style.css`, `static/js/main.js` (entry), engines under `static/js/engines/`, performance modules under `static/js/performance/`, components under `static/js/components/`

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
- **Config:** Always import from centralized `config.py` - uses `DB_PATH` for single database
- **Database:** Use `DatabaseManager` with thread safety (`_lock`) - ONLY `clever.db` file
- **Error Handling:** Use debug system (`get_debugger`, `performance_monitor`)
- **Documentation:** Every function must explain Why/Where/How connections
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
- Main UI at `templates/index.html`; JS entry `static/js/main.js` loads particle engine from `static/js/engines/holographic-chamber.js`. Performance modules under `static/js/performance/` loaded only in debug mode, UI components under `static/js/components/`, core modules under `static/js/core/`.
