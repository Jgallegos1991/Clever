# CURRENT ACTIVE FILE STRUCTURE

## ⚠️ CRITICAL: Files Actually Loaded by Browser

This document lists ONLY the files that are actually loaded and used by the application.
**DO NOT EDIT FILES NOT LISTED HERE** - they will have no effect!

## 🎯 Active Frontend Files (Browser Loads These)

### Template
- **`/templates/index.html`** - Main HTML template (Flask renders this)

### CSS (Loaded in Order)
- **`/static/css/style.css`** - ONLY stylesheet loaded

### JavaScript (Loaded in Order)  
- **`/static/js/holographic-chamber.js`** - Particle system engine
- **`/static/js/main.js`** - Main application logic

### Debug Mode Only
- **`/static/js/performance/performance-dashboard.js`** - Performance monitor (only when `?debug` in URL)

## 🚫 Files That Are NOT Loaded (Don't Edit These!)

- `/static/style.css` - Legacy file, NOT loaded by template
- `/static/js/core/app.js` - REMOVED, was duplicate of main.js  
- `/static/js/engines/*.js` - Particle engines not currently used
- `/static/js/particles.js` - Legacy file
- `/static/js/simple-test.js` - Debug tool only

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

**Last Updated**: September 12, 2025 - After fixing particle system loading issues