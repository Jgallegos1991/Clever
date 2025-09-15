# CURRENT ACTIVE FILE STRUCTURE

## ⚠️ CRITICAL: Files Actually Loaded by Browser

This document lists ONLY the files that are actually loaded and used by the application.
**DO NOT EDIT FILES NOT LISTED HERE** - they will have no effect!

## 🎯 Active Frontend Files (Browser Loads These)

### Template

- **`/templates/index.html`** - Main HTML template (Flask renders this)
- **`/templates/test_basic.html`** - Diagnostic template (minimal CSP-safe test)

### CSS (Loaded in Order)

- **`/static/css/style.css`** - Main stylesheet
- **`/static/css/landing.css`** - Magical UI and particle styles
- **`/static/css/test_basic.css`** - Diagnostic template stylesheet

### JavaScript (Loaded in Order)

- **`/static/js/holographic-chamber.js`** - Particle system engine
- **`/static/js/main.js`** - Main application logic
- **`/static/js/magic-orchestrator.js`** - Particle state orchestrator

### Debug Mode Only

- **`/static/js/performance/performance-dashboard.js`** - Performance monitor (only when `?debug` in URL)

## 🚫 Files That Are NOT Loaded (All legacy/unused files have been removed)

## 🔧 Backend Files (Server-side)

### Core Application

- **`app.py`** - Flask server entry point
- **`config.py`** - Configuration settings
- **`database.py`** - Database management
- **`persona.py`** - AI persona engine
- **`evolution_engine.py`** - Learning system

### Supporting Modules

- **`nlp_processor.py`** - Natural language processing
- **`debug_config.py`** - Debugging and logging
- **`health_monitor.py`** - System health monitoring

## 🎯 How to Verify Active Files

1. **Check template**: Look at `/templates/index.html` for script/link tags
2. **Check browser**: Use dev tools → Sources tab to see loaded files
3. **Check this file**: Always up-to-date list of active files

## 📝 Update Instructions

When adding/removing files:

1. ✅ Update template if changing loaded files
2. ✅ Update this document
3. ✅ Update `/static/README.md`
4. ✅ Update main `README.md`
5. ✅ Update `.github/copilot-instructions.md`

**Last Updated**: September 14, 2025 - After full workspace cleanup and organization
