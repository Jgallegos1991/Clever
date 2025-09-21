# Clever AI: Agent Onboarding & Required Reading

**⚠️ MANDATORY: Read ALL documents below BEFORE making any changes to Clever**

---

## 🚨 CRITICAL FIRST STEPS

**Every agent/copilot MUST:**
1. Read this entire document
2. Review all referenced documentation  
3. Understand the device specifications
4. Follow the unbreakable rules
5. Document Why/Where/How for all code changes

**Failure to follow these steps will result in broken functionality or architectural violations.**

---

## 📋 REQUIRED READING CHECKLIST

### Core Documentation (READ FIRST)
- [ ] **`README.md`** - Project overview, setup, and basic usage
- [ ] **`.github/copilot-instructions.md`** - Primary coding standards and patterns
- [ ] **`docs/architecture.md`** - System architecture and component relationships
- [ ] **`docs/config/device_specifications.md`** - Hardware environment and constraints
- [ ] **`file-inventory.md`** - Complete file structure and purposes

### Architectural Foundation
- [ ] **`config.py`** - Central configuration (DB_PATH, settings)
- [ ] **`database.py`** - DatabaseManager, thread safety patterns
- [ ] **`persona.py`** - PersonaEngine, response modes
- [ ] **`evolution_engine.py`** - Self-learning, memory, growth
- [ ] **`debug_config.py`** - Logging, monitoring, error handling

### Development Standards
- [ ] **`pytest.ini`** - Testing configuration and patterns
- [ ] **`Makefile`** - Build, setup, and run commands
- [ ] **`test-offline.sh`** - Offline validation requirements
- [ ] **`requirements.txt`** - Dependency management

### UI/UX Guidelines  
- [ ] **`docs/ui.md`** - UI patterns and design principles
- [ ] **`templates/index.html`** - Main UI structure
- [ ] **`static/css/style.css`** - Styling conventions
- [ ] **`static/js/holographic-chamber.js`** - Particle engine

---

## 🔒 UNBREAKABLE RULES

### 1. Strictly Offline Operation
- **Rule:** Never add code that makes external network calls at runtime
- **Enforcement:** All code must pass `utils.offline_guard.enable()`
- **Libraries:** Must be local, no cloud dependencies
- **Testing:** Run `test-offline.sh` before committing

### 2. Single-User System
- **Rule:** System is for "Jordan" (Jay) only
- **Implementation:** Use `user_config.py` for personalization
- **Persona:** Witty, empathetic female AI named "Clever"
- **No:** User accounts, logins, or multi-tenancy

### 3. Single Database
- **Rule:** Use ONLY `clever.db` via `config.DB_PATH`
- **Implementation:** Always use `DatabaseManager` from `database.py`
- **Thread Safety:** Use `DatabaseManager._lock` for concurrent access
- **No:** Multiple databases, fallbacks, or placeholder DBs

### 4. Mandatory Documentation
- **Rule:** ALL code must include Why/Where/How comments
- **Why:** Business/technical reason code exists
- **Where:** How it connects to other system components
- **How:** Technical implementation details
- **Enforcement:** Runtime introspection parses these tokens

---

## 🏗️ ARCHITECTURE PATTERNS

### Core Framework
```
Flask App (app.py) 
├── PersonaEngine (persona.py) - Response generation
├── EvolutionEngine (evolution_engine.py) - Learning/memory
├── DatabaseManager (database.py) - SQLite operations
├── UnifiedNLPProcessor (nlp_processor.py) - Local NLP
└── DebugConfig (debug_config.py) - Monitoring/logging
```

### Request Lifecycle
```
User Input → NLP Processing → Persona Generation → Evolution Logging → Response
     ↓              ↓                ↓                  ↓           ↓
app.py → nlp_processor.py → persona.py → evolution_engine.py → JSON Response
```

### Database Schema
- **utterances:** Conversation history
- **sources:** File ingestion and sync
- **memories:** Long-term learning data
- **evolution_metrics:** Growth tracking

---

## 🔧 DEVELOPMENT WORKFLOWS

### Before Making Changes
```bash
# 1. Setup environment
make setup

# 2. Understand current state
make file-inventory

# 3. Run tests
make test

# 4. Check offline compliance
./test-offline.sh
```

### Code Pattern Templates
```python
# Required documentation pattern
def example_function(param: str) -> str:
    """
    Brief description
    
    Why: Business reason this exists
    Where: Connection to other components
    How: Technical implementation approach
    
    Connects to:
        - database.py: Data persistence
        - persona.py: Response generation
    """
    pass

# Database usage pattern  
from database import DatabaseManager
import config

db = DatabaseManager(config.DB_PATH)
# Always use DatabaseManager methods, never direct SQL

# Persona response pattern
from persona import PersonaEngine
response = PersonaEngine().respond(text, mode="Auto")

# Evolution logging pattern
from evolution_engine import get_evolution_engine
evo = get_evolution_engine()
evo.log_interaction({"user_input": text, "mode": mode})
```

---

## 📱 DEVICE ENVIRONMENT

### Hardware Constraints (from device_specifications.md)
- **Platform:** Chrome OS Pirika (Google Chromebook)
- **CPU:** Intel Jasper Lake (low-power)
- **Memory:** Limited RAM, efficient caching required
- **Storage:** 107GB eMMC (94% used, 6.9GB free)
- **Network:** WiFi 802.11ac, offline-first design

### Performance Considerations
- **SQLite:** Optimized for eMMC sequential access
- **Flask:** Single-threaded model suitable for CPU
- **UI:** Hardware-accelerated Canvas2D particles
- **Memory:** Close unused Chrome tabs if performance degrades

---

## 🎯 UI/UX VISION

### Design Philosophy
- **Focus:** Particle engine (holographic chamber) is center stage
- **Chat:** Floating bubbles that fade in/out, not persistent boxes
- **Input:** Minimal, glowing bar at bottom center
- **Aesthetic:** Dark theme, frosted glass, neon accents

### Technical Implementation
- **Particles:** `static/js/holographic-chamber.js` (HolographicChamber class)
- **Animations:** CSS transitions, fade effects
- **Responsiveness:** 1366x768 base, scales to external monitors
- **Performance:** 60fps particle rendering on Chrome OS

---

## 🧪 TESTING REQUIREMENTS

### Before Every Commit
```bash
# Full test suite
make test

# Offline validation
./test-offline.sh

# UI functionality  
make run
# Visit http://localhost:5000 and test particle system
```

### Test Categories
- **Unit Tests:** Core functionality (`tests/`)
- **Integration:** Full system workflows
- **Offline:** Network isolation compliance
- **UI:** Particle system, chat bubbles, input bar
- **Performance:** Memory usage, database operations

---

## 🚨 COMMON PITFALLS

### What NOT to Do
❌ Add external API calls or cloud dependencies  
❌ Create multiple database files or connections
❌ Skip Why/Where/How documentation
❌ Modify core architecture without understanding connections
❌ Add user authentication or multi-tenancy
❌ Use direct SQL instead of DatabaseManager
❌ Break particle engine or UI animations
❌ Ignore device storage/memory constraints

### Red Flags to Watch For
🚩 Import statements with external URLs
🚩 Database file paths not using `config.DB_PATH`
🚩 Functions without Why/Where/How comments
🚩 Network requests in production code
🚩 Hard-coded file paths or configurations
🚩 UI changes that break particle system
🚩 Memory-intensive operations without limits

---

## 📞 TROUBLESHOOTING

### Common Issues
1. **UI Not Updating:** Check cache busting in Flask routes
2. **Particles Not Visible:** Verify z-index in CSS, canvas rendering
3. **Database Errors:** Ensure using DatabaseManager, check file permissions
4. **Memory Issues:** Monitor Chrome tab usage, close unnecessary tabs
5. **Offline Failures:** Check for network calls, external dependencies

### Debug Commands
```bash
# System resources
df -h && free -h

# Database status
sqlite3 clever.db ".tables"

# Server logs
tail -f logs/clever.log

# Network isolation test
./test-offline.sh
```

---

## 📋 QUICK REFERENCE

### File Hierarchy Priority
1. **Core:** `app.py`, `config.py`, `database.py`
2. **AI:** `persona.py`, `evolution_engine.py`, `nlp_processor.py`
3. **UI:** `templates/`, `static/`, `holographic-chamber.js`
4. **Config:** `user_config.py`, `debug_config.py`
5. **Utils:** `file_ingestor.py`, `sync_watcher.py`

### Key Directories
- **`docs/`** - All documentation and specifications
- **`static/js/`** - Frontend JavaScript (particle engines)
- **`templates/`** - Jinja2 HTML templates
- **`tests/`** - Test suites and validation
- **`utils/`** - Utility functions and helpers

---

## ✅ VERIFICATION CHECKLIST

Before submitting ANY changes to Clever:

- [ ] Read all required documentation
- [ ] Understand device constraints and environment
- [ ] Follow unbreakable rules (offline, single-user, single-DB)
- [ ] Add Why/Where/How documentation to all code
- [ ] Test offline operation (`test-offline.sh`)
- [ ] Verify UI particle system still works
- [ ] Run full test suite (`make test`)
- [ ] Check memory and storage impact
- [ ] Validate against architectural patterns
- [ ] Ensure thread-safe database operations

**Remember: Clever is a carefully architected system. Every component connects to every other component. Understanding these connections is essential for safe changes.**

---

*This document is the source of truth for all Clever development. Update it when architectural patterns change.*