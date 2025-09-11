# File Inventory

This document provides an overview of all files in the project repository.

## Summary Statistics

- **Total Files**: 6,328
- **Total Lines of Code**: 3,302,702
- **Languages/File Types**: 74

## Top Languages by File Count

| Language | Files | Lines of Code |
|----------|-------|---------------|
| python | 3,897 | 1,211,613 |
| marisa | 799 | 21,216 |
| other | 471 | 117,865 |
| pyi | 285 | 44,976 |
| txt | 115 | 225,318 |
| so | 90 | 1,347,780 |
| pyx | 68 | 25,095 |
| pxd | 63 | 5,843 |
| f90 | 61 | 1,296 |
| doctest | 59 | 20,071 |
| typed | 54 | 65 |
| h | 39 | 13,042 |
| csv | 33 | 44,651 |
| js | 28 | 6,771 |
| npy | 25 | 119 |
| f | 24 | 508 |
| markdown | 16 | 1,105 |
| json | 15 | 88,008 |
| gz | 15 | 106 |
| c | 14 | 14,723 |

## Directory Structure Overview

| Directory | Files | Total LOC |
|-----------|-------|-----------|
| .venv | 6,248 | 3,261,628 |
| static | 35 | 14,841 |
| . | 20 | 3,069 |
| docs | 7 | 20,319 |
| utils | 5 | 225 |
| .vscode | 3 | 75 |
| logs | 2 | 238 |
| .github | 2 | 51 |
| Clever_Sync | 2 | 4 |
| .devcontainer | 1 | 23 |
| templates | 1 | 35 |
| uploads | 1 | 2,159 |
| tools | 1 | 35 |

## Core Project Files

Files in the root directory and main project folders:

| File | Language | LOC | Purpose |
|------|----------|-----|---------|
| `.devcontainer/devcontainer.json` | json | 23 | - |
| `.env.sample` | sample | 12 | - |
| `.github/instructions/CLEVER_UI_INSTRUCTIONS.md.instructions.md` | markdown | 12 | - |
| `.github/prompts/COPILOT_UI_BRIEF.md.prompt.md` | markdown | 39 | - |
| `.gitignore` | other | 43 | - |
| `.vscode/extensions.json` | json | 18 | - |
| `.vscode/settings.json` | json | 25 | - |
| `.vscode/tasks.json` | json | 32 | - |
| `CLEVER_FRAMEWORK_DEMO.md` | markdown | 215 | - |
| `Clever_Sync/sample_note.txt` | txt | 2 | - |
| `Clever_Sync/sample_note_3.txt` | txt | 2 | - |
| `MAGICAL_UI_IMPLEMENTATION.md` | markdown | 82 | - |
| `Makefile` | other | 66 | - |
| `PROJECT_STRUCTURE.md` | markdown | 85 | - |
| `README.md` | markdown | 32 | - |
| `app.py` | python | 1,175 | - |
| `clever.db` | db | 177 | - |
| `config.py` | python | 69 | Central configuration for Clever. |
| `database.py` | python | 378 | - |
| `docs/screenshots/Screenshot 2025-08-25 11.23.31 AM.png` | png | 3,309 | - |
| `docs/screenshots/Screenshot 2025-08-30 11.36.34 PM.png` | png | 2,317 | - |
| `docs/screenshots/Screenshot 2025-08-30 11.41.08 PM.png` | png | 2,102 | - |
| `docs/screenshots/Screenshot 2025-08-30 11.58.33 PM.png` | png | 3,827 | - |
| `docs/screenshots/Screenshot 2025-08-30 8.47.43 PM.png` | png | 2,223 | - |
| `docs/screenshots/Screenshot 2025-08-30 8.53.42 PM.png` | png | 2,035 | - |
| `docs/screenshots/Screenshot 2025-08-31 12.44.27 AM.png` | png | 4,506 | - |
| `file_ingestor.py` | python | 97 | - |
| `fixer.py` | python | 81 | - |
| `jsconfig.json` | json | 19 | - |
| `logs/app.log` | log | 147 | - |
| `logs/server.log` | log | 91 | - |
| `nlp_processor.py` | python | 199 | - |
| `persona.py` | python | 177 | - |
| `requirements-base.txt` | txt | 2 | - |
| `requirements.txt` | txt | 60 | - |
| `static/README.md` | markdown | 68 | - |
| `static/assets/Screenshot 2025-08-31 12.20.00 AM.png` | png | 4,164 | - |
| `static/clever-performance-quick.js` | js | 54 | - |
| `static/css/style.css` | css | 622 | - |
| `static/einstein-engine.js` | js | 278 | - |
| `static/js/archive/scene.js.backup` | backup | 820 | - |
| `static/js/archive/scene.js.corrupted` | corrupted | 820 | - |
| `static/js/archive/scene.js.fixed` | fixed | 806 | - |
| `static/js/core/app.js` | js | 358 | - |
| `static/js/core/app.js.corrupted` | corrupted | 333 | - |
| `static/js/core/sw.js` | js | 19 | - |
| `static/js/engines/einstein-engine.js` | js | 278 | - |
| `static/js/engines/quantum-scene-simple.js` | js | 263 | - |
| `static/js/engines/quantum-scene.js` | js | 567 | - |
| `static/js/performance/clever-performance-quick.js` | js | 54 | - |
| `static/js/performance/performance-dashboard.js` | js | 134 | - |
| `static/js/performance/performance-enhancer.js` | js | 306 | - |
| `static/js/performance/performance-quick.js` | js | 135 | - |
| `static/js/unused/orb.js` | js | 2 | - |
| `static/js/unused/scene.js` | js | 812 | - |
| `static/js/unused/scene_3d.js` | js | 331 | - |
| `static/js/unused/scene_complex.js` | js | 1 | - |
| `static/js/unused/sources.js` | js | 51 | - |
| `static/js/unused/test-particles.js` | js | 74 | - |
| `static/performance-dashboard.js` | js | 134 | - |
| `static/performance-enhancer.js` | js | 306 | - |
| `static/performance-quick.js` | js | 135 | - |
| `static/quantum-scene-simple.js` | js | 238 | - |
| `static/quantum-scene.js` | js | 567 | - |
| `static/scene.js` | js | 812 | - |
| `static/scene.js.fixed` | fixed | 806 | - |
| `static/scene_3d.js` | js | 331 | - |
| `static/scene_complex.js` | js | 1 | - |
| `static/style.css` | css | 87 | - |
| `static/test-particles.js` | js | 74 | - |
| `sync_tools.py` | python | 47 | - |
| `templates/index.html` | html | 35 | - |
| `test-offline.sh` | sh | 53 | - |
| `tools/summarize_repo.py` | python | 35 | - |
| `uploads/Screenshot 2025-08-31 12.38.26 AM.png` | png | 2,159 | - |
| `utils/backup_manager.py` | python | 44 | - |
| `utils/cli.py` | python | 66 | - |
| `utils/scheduler.py` | python | 42 | - |
| `utils/self_fix.py` | python | 1 | - |
| `utils/watcher.py` | python | 72 | - |

## Detailed Breakdown by Language

### 0 Files

- **Count**: 2
- **Total LOC**: 9,363

### 1 Files

- **Count**: 1
- **Total LOC**: 315

### 12 Files

- **Count**: 2
- **Total LOC**: 21

### APACHE Files

- **Count**: 5
- **Total LOC**: 890

### BSD Files

- **Count**: 5
- **Total LOC**: 120

### A Files

- **Count**: 2
- **Total LOC**: 561

### BACKUP Files

- **Count**: 1
- **Total LOC**: 820

**Notable files:**

- `static/js/archive/scene.js.backup` (820 LOC)

### BIN Files

- **Count**: 2
- **Total LOC**: 219

### BUILD Files

- **Count**: 3
- **Total LOC**: 158

### BZ2 Files

- **Count**: 5
- **Total LOC**: 61

### C Files

- **Count**: 14
- **Total LOC**: 14,723

### CC Files

- **Count**: 1
- **Total LOC**: 59

### CFG Files

- **Count**: 8
- **Total LOC**: 622

### CORRUPTED Files

- **Count**: 2
- **Total LOC**: 1,153

**Notable files:**

- `static/js/archive/scene.js.corrupted` (820 LOC)
- `static/js/core/app.js.corrupted` (333 LOC)

### CPP Files

- **Count**: 4
- **Total LOC**: 41,242

### CSH Files

- **Count**: 1
- **Total LOC**: 28

### CSS Files

- **Count**: 3
- **Total LOC**: 860

**Notable files:**

- `static/css/style.css` (622 LOC)
- `static/style.css` (87 LOC)

### CSV Files

- **Count**: 33
- **Total LOC**: 44,651

### CU Files

- **Count**: 2
- **Total LOC**: 848

### DB Files

- **Count**: 1
- **Total LOC**: 177

**Notable files:**

- `clever.db` (177 LOC)

### DOCTEST Files

- **Count**: 59
- **Total LOC**: 20,071

### EGG Files

- **Count**: 1
- **Total LOC**: 5

### EXE Files

- **Count**: 14
- **Total LOC**: 4,892

### F Files

- **Count**: 24
- **Total LOC**: 508

### F90 Files

- **Count**: 61
- **Total LOC**: 1,296

### F95 Files

- **Count**: 1
- **Total LOC**: 6

### FISH Files

- **Count**: 1
- **Total LOC**: 70

### FITS Files

- **Count**: 1
- **Total LOC**: 1

### FIXED Files

- **Count**: 2
- **Total LOC**: 1,612

**Notable files:**

- `static/scene.js.fixed` (806 LOC)
- `static/js/archive/scene.js.fixed` (806 LOC)

### GZ Files

- **Count**: 15
- **Total LOC**: 106

### GZIP Files

- **Count**: 5
- **Total LOC**: 48

### H Files

- **Count**: 39
- **Total LOC**: 13,042

### HH Files

- **Count**: 2
- **Total LOC**: 495

### HTML Files

- **Count**: 3
- **Total LOC**: 44

**Notable files:**

- `templates/index.html` (35 LOC)

### INC Files

- **Count**: 1
- **Total LOC**: 2

### INI Files

- **Count**: 5
- **Total LOC**: 64

### IPYNB Files

- **Count**: 1
- **Total LOC**: 43

### JINJA Files

- **Count**: 1
- **Total LOC**: 652

### JS Files

- **Count**: 28
- **Total LOC**: 6,771

**Notable files:**

- `static/scene.js` (812 LOC)
- `static/js/unused/scene.js` (812 LOC)
- `static/quantum-scene.js` (567 LOC)
- `static/js/engines/quantum-scene.js` (567 LOC)
- `static/js/core/app.js` (358 LOC)
- `static/scene_3d.js` (331 LOC)
- `static/js/unused/scene_3d.js` (331 LOC)
- `static/performance-enhancer.js` (306 LOC)
- `static/js/performance/performance-enhancer.js` (306 LOC)
- `static/einstein-engine.js` (278 LOC)

### JSON Files

- **Count**: 15
- **Total LOC**: 88,008

**Notable files:**

- `.vscode/tasks.json` (32 LOC)
- `.vscode/settings.json` (25 LOC)
- `.devcontainer/devcontainer.json` (23 LOC)
- `jsconfig.json` (19 LOC)
- `.vscode/extensions.json` (18 LOC)

### LOG Files

- **Count**: 2
- **Total LOC**: 238

**Notable files:**

- `logs/app.log` (147 LOC)
- `logs/server.log` (91 LOC)

### LZMA Files

- **Count**: 5
- **Total LOC**: 35

### MARISA Files

- **Count**: 799
- **Total LOC**: 21,216

### MARKDOWN Files

- **Count**: 16
- **Total LOC**: 1,105

**Notable files:**

- `CLEVER_FRAMEWORK_DEMO.md` (215 LOC)
- `PROJECT_STRUCTURE.md` (85 LOC)
- `MAGICAL_UI_IMPLEMENTATION.md` (82 LOC)
- `static/README.md` (68 LOC)
- `.github/prompts/COPILOT_UI_BRIEF.md.prompt.md` (39 LOC)
- `README.md` (32 LOC)
- `.github/instructions/CLEVER_UI_INSTRUCTIONS.md.instructions.md` (12 LOC)

### MARKDOWN-IT Files

- **Count**: 1
- **Total LOC**: 23

### NPY Files

- **Count**: 25
- **Total LOC**: 119

### NPZ Files

- **Count**: 2
- **Total LOC**: 22

### OTHER Files

- **Count**: 471
- **Total LOC**: 117,865

**Notable files:**

- `Makefile` (66 LOC)
- `.gitignore` (43 LOC)

### PC Files

- **Count**: 1
- **Total LOC**: 8

### PEM Files

- **Count**: 2
- **Total LOC**: 9,518

### PKL Files

- **Count**: 11
- **Total LOC**: 200

### PNG Files

- **Count**: 12
- **Total LOC**: 26,660

**Notable files:**

- `docs/screenshots/Screenshot 2025-08-31 12.44.27 AM.png` (4,506 LOC)
- `static/assets/Screenshot 2025-08-31 12.20.00 AM.png` (4,164 LOC)
- `docs/screenshots/Screenshot 2025-08-30 11.58.33 PM.png` (3,827 LOC)
- `docs/screenshots/Screenshot 2025-08-25 11.23.31 AM.png` (3,309 LOC)
- `docs/screenshots/Screenshot 2025-08-30 11.36.34 PM.png` (2,317 LOC)
- `docs/screenshots/Screenshot 2025-08-30 8.47.43 PM.png` (2,223 LOC)
- `uploads/Screenshot 2025-08-31 12.38.26 AM.png` (2,159 LOC)
- `docs/screenshots/Screenshot 2025-08-30 11.41.08 PM.png` (2,102 LOC)
- `docs/screenshots/Screenshot 2025-08-30 8.53.42 PM.png` (2,035 LOC)

### PS1 Files

- **Count**: 1
- **Total LOC**: 248

### PTH Files

- **Count**: 1
- **Total LOC**: 2

### PXD Files

- **Count**: 63
- **Total LOC**: 5,843

### PYF Files

- **Count**: 7
- **Total LOC**: 83

### PYI Files

- **Count**: 285
- **Total LOC**: 44,976

### PYTHON Files

- **Count**: 3,897
- **Total LOC**: 1,211,613

**Notable files:**

- `app.py` (1,175 LOC)
- `database.py` (378 LOC)
- `nlp_processor.py` (199 LOC)
- `persona.py` (177 LOC)
- `file_ingestor.py` (97 LOC)
- `fixer.py` (81 LOC)
- `utils/watcher.py` (72 LOC)
- `config.py` (69 LOC) - Central configuration for Clever.
- `utils/cli.py` (66 LOC)
- `sync_tools.py` (47 LOC)

### PYX Files

- **Count**: 68
- **Total LOC**: 25,095

### RST Files

- **Count**: 2
- **Total LOC**: 245

### SAMPLE Files

- **Count**: 1
- **Total LOC**: 12

**Notable files:**

- `.env.sample` (12 LOC)

### SH Files

- **Count**: 2
- **Total LOC**: 73

**Notable files:**

- `test-offline.sh` (53 LOC)

### SO Files

- **Count**: 90
- **Total LOC**: 1,347,780

### TEMPLATE Files

- **Count**: 1
- **Total LOC**: 56

### TMPL Files

- **Count**: 2
- **Total LOC**: 11

### TOML Files

- **Count**: 1
- **Total LOC**: 68

### TXT Files

- **Count**: 115
- **Total LOC**: 225,318

**Notable files:**

- `requirements.txt` (60 LOC)
- `requirements-base.txt` (2 LOC)
- `Clever_Sync/sample_note_3.txt` (2 LOC)
- `Clever_Sync/sample_note.txt` (2 LOC)

### TYPED Files

- **Count**: 54
- **Total LOC**: 65

### XML Files

- **Count**: 4
- **Total LOC**: 9,182

### XZ Files

- **Count**: 5
- **Total LOC**: 42

### YAML Files

- **Count**: 1
- **Total LOC**: 49

### YML Files

- **Count**: 1
- **Total LOC**: 283

### Z Files

- **Count**: 3
- **Total LOC**: 3

### ZIP Files

- **Count**: 1
- **Total LOC**: 19

---

*This file inventory was generated automatically from the repository analysis.*