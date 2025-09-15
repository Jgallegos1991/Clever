# Clever Static Assets Organization

This directory contains all frontend assets for Clever, organized for maintainability and clarity.


## 📁 Directory Structure (Cleaned)

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
- Version numbers in HTML template prevent caching issues during development
- All paths are absolute from `/static/` for consistency

## 📝 File Naming Convention

- `*-simple.js`: Simplified/optimized versions
- `*-quick.js`: Fast-loading variants  
- `*-dashboard.js`: UI/monitoring components
- `*.backup`: Backup copies
- `*.corrupted`: Files that had issues (preserved for debugging)
