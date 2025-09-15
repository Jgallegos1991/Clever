# Configuration Management
**Last updated:** 2025-09-04

This document is the canonical reference for Clever AI’s configuration. Clever runs as an **offline-first Flask + SQLite + spaCy** assistant with no cloud dependencies or telemetry.

---

## Overview

- **App:** Flask (`app.py`)
- **Storage:** Local SQLite (`clever_memory.db`)
- **NLP:** Local spaCy model (`en_core_web_sm`)
- **Privacy:** Offline-only by default (`OFFLINE_ONLY=True`)
- **Sync:** Remote sync disabled (`ALLOW_REMOTE_SYNC=False`)

---

## Path & File Configuration (`config.py`)

```python
import os

# Base paths
BASE_DIR      = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH  = BASE_DIR

# Critical system paths
BACKUP_DIR        = os.path.join(PROJECT_PATH, "backups")
MEMORY_DB_PATH    = os.path.join(PROJECT_PATH, "clever_memory.db")
DATABASE_NAME     = MEMORY_DB_PATH
SYNC_DIR          = os.path.join(PROJECT_PATH, "Clever_Sync")
UPLOAD_FOLDER     = os.path.join(BASE_DIR, "uploads")

# File upload restrictions
ALLOWED_EXTENSIONS = {"txt", "md", "pdf"}
