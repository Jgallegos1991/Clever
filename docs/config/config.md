# Clever AI Configuration Audit
## Generated on 2025-09-04

### Overview
This document provides a comprehensive audit of all configuration settings for the Clever AI system, an offline-first Flask + SQLite + spaCy assistant for Jay.

---

## Environment Variables (.env keys)

### Primary Environment Variables
The application references environment variables through the `scripts/dev.sh` file:

| Variable | Purpose | Default Value | Source |
|----------|---------|---------------|---------|
| `HOST` | Flask server bind address | `0.0.0.0` | scripts/dev.sh, Makefile |
| `PORT` | Flask server port | `5000` | scripts/dev.sh, Makefile |
| `PYTHON` | Python interpreter path | Auto-detected | scripts/dev.sh |
| `VENV` | Virtual environment path | `.venv` | scripts/dev.sh |
| `APP` | Main application file | `app.py` | scripts/dev.sh |
| `ENV_FILE` | Environment file location | `.env` | scripts/dev.sh |

### How the App Locates Configuration
1. **Environment Variables**: Loaded via `scripts/dev.sh` using bash parameter expansion (`${VAR:-default}`)
2. **Static Configuration**: Defined in `config.py` using hardcoded values
3. **Runtime Detection**: Some paths use `os.path.abspath()` and `os.path.dirname()` for dynamic resolution

---

## Static Configuration (config.py)

### Paths Configuration
```python
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR
BACKUP_DIR = os.path.join(PROJECT_PATH, "backups")
MEMORY_DB_PATH = os.path.join(PROJECT_PATH, "clever_memory.db")
SYNC_DIR = os.path.join(PROJECT_PATH, "Clever_Sync")
DATABASE_NAME = MEMORY_DB_PATH
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
```

### File Upload Configuration
```python
ALLOWED_EXTENSIONS = {'txt', 'md', 'pdf'}
```

### AI Model Configuration
```python
SPACY_MODEL = "en_core_web_sm"  # Local spaCy model
```

### UI Configuration
```python
UI_PIXELS_ENABLED = True
UI_DEFAULT_COLOR = "#FFFFFF"
UI_DEFAULT_EXPRESSION = "idle"
```

### Operational Modes
```python
MODES = ["deep_dive", "quick_hit", "creative", "support"]
DEFAULT_MODE = "quick_hit"
```

### Offline Configuration
```python
OFFLINE_ONLY = True              # ✅ Enforces offline-first principle
ALLOW_REMOTE_SYNC = False        # ✅ Disables remote synchronization
```

### Backup Configuration
```python
KEEP_LATEST_BACKUPS = 1
BACKUP_ZIP_FORMAT = "backup_%Y-%m-%d_%H-%M-%S.zip"
```

---

## Runtime Profiles

### Development Profile
- **Activation**: `make run` or `scripts/dev.sh run`
- **Host**: `0.0.0.0` (accepts external connections)
- **Port**: `5000`
- **Debug Mode**: `debug=True` (hardcoded in app.py line 224)
- **Safe Mode**: Controlled by `SAFE_MODE = False` in app.py
- **Database**: SQLite local file (`clever_memory.db`)

### Production Profile
- **Current Status**: No distinct production profile configured
- **Recommendations**: 
  - Set `debug=False` for production
  - Consider environment-specific configuration loading
  - Implement proper logging levels

### Offline Profile
- **Default State**: Always offline-first
- **Network Restrictions**: 
  - `OFFLINE_ONLY = True`
  - `ALLOW_REMOTE_SYNC = False`
  - No external API calls detected in codebase

---

## Ports Configuration

### Primary Service Ports
| Service | Port | Configurable | Default |
|---------|------|--------------|---------|
| Flask App | 5000 | ✅ Yes (HOST/PORT env vars) | 5000 |
| Static Files | Same as Flask | ✅ Inherited | 5000 |
| Service Worker | Same as Flask | ✅ Inherited | 5000 |

### Port Configuration Sources
1. **Environment Variable**: `PORT=${PORT:-5000}`
2. **Makefile Override**: `PORT ?= 5000`
3. **Hardcoded Fallback**: `app.run(port=5000)` in app.py

---

## Logging Configuration

### Logging Levels
| Component | Level | Configuration |
|-----------|-------|---------------|
| Persona Module | `DEBUG` | `logging.basicConfig(level=logging.DEBUG)` |
| Flask App | N/A | Uses print statements for warnings |
| Database | N/A | Uses print statements for status |

### Logging Outputs
- **Persona**: Structured logging with timestamps (`%(asctime)s - %(levelname)s - %(message)s`)
- **Application**: Console output via `print()` statements
- **Conversations**: File logging to `conversations.json` (append mode)
- **Database Operations**: Console warnings for failed operations

### Log Locations
- **Console**: Standard output for application logs
- **File**: `conversations.json` for user interactions
- **Database**: `clever_memory.db` for persistent conversation storage

---

## Offline-First Compliance Audit

### ✅ Compliant Practices
1. **No External API Calls**: No http/https requests found in codebase
2. **Local Data Storage**: SQLite database (`clever_memory.db`)
3. **Local NLP Processing**: spaCy model (`en_core_web_sm`) runs locally
4. **Offline Flags**: `OFFLINE_ONLY = True`, `ALLOW_REMOTE_SYNC = False`
5. **Local File Processing**: File ingestion works with local uploads only
6. **Service Worker**: PWA service worker for offline functionality

### ⚠️ Areas of Concern
1. **spaCy Model Dependency**: Requires initial download of `en_core_web_sm` model
2. **Python Package Dependencies**: Initial `pip install` requires internet
3. **No Network Fallback Handling**: App assumes always-offline environment

### 🟢 Offline-First Violations: None Detected
The codebase maintains strict offline-first principles with no cloud dependencies or telemetry.

---

## Security Configuration

### Data Privacy
- **Local Only**: All data stored locally in SQLite
- **No Telemetry**: No external tracking or analytics
- **File Upload Restrictions**: Limited to `.txt`, `.md`, `.pdf` extensions
- **Conversation Logging**: Stored locally in `conversations.json` and database

### Network Security
- **Bind Address**: `0.0.0.0` allows external connections (development setting)
- **No Authentication**: No user authentication system implemented
- **Local Network Only**: Designed for trusted local network operation

---

## Configuration Recommendations

### Immediate
1. **Environment-Specific Debug**: Replace hardcoded `debug=True` with environment variable
2. **Production Profile**: Create distinct production configuration
3. **Logging Standardization**: Unify logging approach across all modules

### Future Considerations
1. **Configuration Validation**: Add startup validation for required settings
2. **Health Check Endpoints**: Expand `/health` endpoint with configuration status
3. **Graceful Degradation**: Better handling when optional features are unavailable

---

## Changelog
- **2025-09-04**: Initial configuration audit created
  - Documented all environment variables and static configuration
  - Identified runtime profiles and port configuration
  - Audited logging setup across all components
  - Verified offline-first compliance (no violations found)
  - Provided security and recommendation analysis