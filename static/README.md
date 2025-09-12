# Clever Static Assets Organization

This directory contains all frontend assets for Clever, organized for maintainability and clarity.

## 📁 Directory Structure

```
static/
├── css/
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
- **CSS**: `css/style.css` - All styling for Clever's interface  
- **Core**: `js/main.js` - Main application logic and chat interface
- **Engine**: `js/holographic-chamber.js` - ACTIVE particle system (morphing formations)
- **Performance**: `js/performance/performance-dashboard.js` - Performance monitoring (debug mode)
- **Service Worker**: `js/core/sw.js` - Offline functionality (NOT currently loaded)

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
