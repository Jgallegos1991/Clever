# Clever Static Assets Organization

<!--
Why: Organizes frontend assets for Clever's holographic UI and particle system
Where: Serves CSS, JavaScript, and assets to Flask app for browser rendering
How: Structured directory layout with engines, components, and performance modules

Connects to:
    - templates/index.html: HTML template that loads these CSS and JS assets
    - app.py: Flask static file serving for CSS, JS, and asset delivery
    - static/js/engines/holographic-chamber.js: Main particle engine for UI
    - static/css/style.css: Primary stylesheet for dark theme and particle UI
    - docs/config/device_specifications.md: Asset optimization for hardware limits
    - tests/test_ui_brief_acceptance.py: Validates proper asset linking
-->

This directory contains all frontend assets for Clever, organized for maintainability and clarity.


## 📁 Directory Structure (Cleaned)
## 📁 Directory Structure

```
static/
├── css/
│   ├── style.css            # Main stylesheet
│   ├── landing.css          # Magical UI and particle styles
│   └── test_basic.css       # Diagnostic template stylesheet
├── js/
│   ├── holographic-chamber.js      # Particle system engine
│   ├── main.js                    # Main application logic
│   ├── magic-orchestrator.js      # Particle state orchestrator
│   └── performance/
│       └── performance-dashboard.js # Performance monitor (debug mode)
├── assets/                  # Images and other assets
│   └── *.png                # Screenshots and images
└── README.md                # This file
│   └── style.css                    # Main stylesheet
├── js/
│   ├── core/                        # Core application files
│   │   ├── app.js                   # Main application logic
│   │   └── sw.js                    # Service worker
│   ├── engines/                     # Particle/visual engines
│   │   ├── einstein-engine.js       # Advanced particle physics
│   │   ├── quantum-scene.js         # Complex quantum simulation
│   │   └── quantum-scene-simple.js  # Simplified particle system (active)
│   ├── performance/                 # Performance monitoring & optimization
│   │   ├── clever-performance-quick.js
│   │   ├── performance-dashboard.js
│   │   ├── performance-enhancer.js
│   │   └── performance-quick.js
│   ├── unused/                      # Legacy/unused files
│   │   ├── orb.js
│   │   ├── scene*.js               # Various legacy scene implementations
│   │   ├── sources.js
│   │   └── test-particles.js
│   └── archive/                     # Backup files
│       ├── scene.js.backup
│       ├── scene.js.corrupted
│       └── scene.js.fixed
├── assets/                          # Images and other assets
│   └── *.png                       # Screenshots and images
└── README.md                        # This file
```

## 🚀 Active Components


### Currently Used Files:
- **CSS**: `css/style.css`, `css/landing.css`, `css/test_basic.css`
- **Core**: `js/main.js` - Main application logic and chat interface
- **Engine**: `js/holographic-chamber.js` - Particle system (morphing formations)
- **Orchestrator**: `js/magic-orchestrator.js` - Particle state orchestrator
- **Performance**: `js/performance/performance-dashboard.js` - Performance monitoring (debug mode)


### Key Features:
- **Magical Particle System**: Beautiful, responsive particle animations
- **Manifestation UI**: Cards and panels emerge from the particle field
- **Microcopy Overlay**: Inspiring phrases animate in the status overlay
- **Chat Interface**: Real-time communication with Clever
- **Performance Monitoring**: Built-in performance tracking
- **Responsive Design**: Works on all device sizes


## 🔧 Development Notes

- File organization follows modern web development best practices
- All legacy/unused files have been removed for clarity
### Currently Used Files:
- **CSS**: `css/style.css` - All styling for Clever's interface
- **Core**: `js/core/app.js` - Main application logic and chat interface
- **Engine**: `js/engines/quantum-scene-simple.js` - Active particle system
- **Performance**: `js/performance/performance-dashboard.js` - Performance monitoring
- **Service Worker**: `js/core/sw.js` - Offline functionality

### Key Features:
- **Quantum Particle System**: Beautiful, responsive particle animations
- **Chat Interface**: Real-time communication with Clever
- **Performance Monitoring**: Built-in performance tracking
- **Offline Support**: Service worker for offline functionality
- **Responsive Design**: Works on all device sizes

## 🔧 Development Notes

- File organization follows modern web development best practices
- Legacy files preserved in `unused/` and `archive/` directories
- Version numbers in HTML template prevent caching issues during development
- All paths are absolute from `/static/` for consistency

## 📝 File Naming Convention

- `*-simple.js`: Simplified/optimized versions
- `*-quick.js`: Fast-loading variants  
- `*-dashboard.js`: UI/monitoring components
- `*.backup`: Backup copies
- `*.corrupted`: Files that had issues (preserved for debugging)
