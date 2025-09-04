# Configuration Management

## Configuration Architecture

### Primary Configuration (`config.py`)

**Purpose:** Centralized system configuration and environment management  
**Location:** `/home/runner/work/projects/projects/config.py`  
**Type:** Python module with global constants and paths

### Core Configuration Sections

#### Path Configuration
```python
# Base directory resolution
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR

# Critical system paths
BACKUP_DIR = os.path.join(PROJECT_PATH, "backups")
MEMORY_DB_PATH = os.path.join(PROJECT_PATH, "clever_memory.db") 
SYNC_DIR = os.path.join(PROJECT_PATH, "Clever_Sync")
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
```

**Path Management Features:**
- **Absolute Path Resolution:** Robust cross-platform compatibility
- **Dynamic Path Creation:** Automatic directory creation when needed
- **Environment-Aware Paths:** Different paths for development/production
- **Security Validation:** Path traversal prevention

#### Database Configuration
```python
# Database settings
DATABASE_NAME = MEMORY_DB_PATH  # Primary database reference
MEMORY_DB_PATH = os.path.join(PROJECT_PATH, "clever_memory.db")

# Connection pooling (future enhancement)
DB_CONNECTION_POOL_SIZE = 5
DB_TIMEOUT = 30
DB_RETRY_ATTEMPTS = 3
```

**Database Features:**
- **SQLite Optimization:** WAL mode for better concurrency
- **Connection Management:** Single connection per request pattern
- **Backup Integration:** Automatic backup path configuration
- **Transaction Settings:** Configurable isolation levels

#### File Processing Configuration
```python
# File upload restrictions
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'md', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

# File processing settings
FILE_PROCESSING_TIMEOUT = 300  # 5 minutes
TEMP_FILE_RETENTION = 24 * 3600  # 24 hours
```

**Security Features:**
- **Extension Validation:** Whitelist-based file type checking
- **Size Limits:** Configurable maximum file sizes
- **Path Security:** Secure filename generation
- **Temporary File Management:** Automatic cleanup procedures

#### AI Model Configuration
```python
# NLP Model settings
SPACY_MODEL = "en_core_web_sm"
MODEL_CACHE_SIZE = 100  # Cached analysis results
NLP_PROCESSING_TIMEOUT = 60  # seconds

# AI behavior settings
DEFAULT_MODE = "quick_hit"
MODES = ["deep_dive", "quick_hit", "creative", "support"]
RESPONSE_CONFIDENCE_THRESHOLD = 0.7
```

**AI Configuration Features:**
- **Model Management:** Version-specific model loading
- **Performance Tuning:** Timeout and cache configurations
- **Behavior Controls:** Operational mode settings
- **Quality Thresholds:** Confidence scoring parameters

### UI Configuration

#### Visual Settings
```python
# UI behavior controls
UI_PIXELS_ENABLED = True
UI_DEFAULT_COLOR = "#FFFFFF"
UI_DEFAULT_EXPRESSION = "idle"

# Performance settings for different hardware
UI_PERFORMANCE_MODE = "auto"  # auto, high, medium, low
PARTICLE_COUNT_MAX = 1000
ANIMATION_FRAME_RATE = 60
```

**UI Features:**
- **Performance Scaling:** Adaptive quality based on hardware
- **Visual Preferences:** Customizable color schemes and effects
- **Accessibility Options:** High contrast and reduced motion modes
- **Device-Specific Settings:** Optimizations for different platforms

#### Frontend Asset Configuration
```javascript
// Static asset configuration
const FRONTEND_CONFIG = {
    api: {
        baseURL: '/',
        timeout: 30000,
        retryAttempts: 3
    },
    ui: {
        theme: 'dark',
        particleCount: 1000,
        animationSpeed: 1.0,
        glitchEffects: true
    },
    performance: {
        targetFPS: 60,
        adaptiveQuality: true,
        memoryLimit: '100MB'
    }
};
```

### Operational Configuration

#### Offline-First Settings
```python
# Offline operation flags
OFFLINE_ONLY = True
ALLOW_REMOTE_SYNC = False  # Only enable for rclone workarounds
NETWORK_TIMEOUT = 5  # seconds for any network operations
FALLBACK_MODE = True  # Enable graceful degradation
```

**Privacy & Security:**
- **Network Isolation:** Strict offline-only operation
- **Data Locality:** All processing and storage local
- **Sync Controls:** Optional external synchronization
- **Fallback Mechanisms:** Graceful degradation when features unavailable

#### Backup & Maintenance
```python
# Backup configuration
KEEP_LATEST_BACKUPS = 7  # Keep 7 most recent backups
BACKUP_ZIP_FORMAT = "backup_%Y-%m-%d_%H-%M-%S.zip"
BACKUP_COMPRESSION_LEVEL = 6  # Balance speed vs size

# Maintenance schedules
AUTO_VACUUM_INTERVAL = 7  # days
CLEANUP_TEMP_FILES_INTERVAL = 24  # hours
LOG_ROTATION_SIZE = 10 * 1024 * 1024  # 10MB
```

### Environment-Specific Configuration

#### Development Configuration
```python
# Development settings
DEBUG_MODE = True
VERBOSE_LOGGING = True
HOT_RELOAD = True
DISABLE_CACHE = True

# Development database
DEV_DATABASE = "clever_memory_dev.db"
TEST_DATABASE = "clever_memory_test.db"
```

#### Production Configuration
```python
# Production settings
DEBUG_MODE = False
VERBOSE_LOGGING = False
ENABLE_COMPRESSION = True
CACHE_STATIC_ASSETS = True

# Production optimizations
PRELOAD_NLP_MODEL = True
ENABLE_QUERY_OPTIMIZATION = True
USE_CONNECTION_POOLING = True
```

### Configuration Management Utilities

#### Configuration Validation
```python
def validate_configuration():
    """Validate all configuration settings on startup"""
    # Check file paths exist and are writable
    # Verify database accessibility
    # Validate NLP model availability
    # Check required directories
    # Validate file permissions
```

#### Dynamic Configuration Updates
```python
class ConfigManager:
    def __init__(self):
        self.config_cache = {}
        self.observers = []
    
    def update_config(self, key, value):
        """Update configuration value with validation"""
        # Validate new value
        # Update configuration
        # Notify observers
        # Persist change if needed
    
    def reload_config(self):
        """Reload configuration from sources"""
        # Re-read config files
        # Validate settings
        # Update runtime configuration
```

### Configuration Sources

#### File-Based Configuration
- **`config.py`** - Primary Python configuration
- **`requirements.txt`** - Dependency specifications
- **`Makefile`** - Build and development commands
- **`.env`** - Environment variables (if used)

#### Database Configuration
- **`system_config` table** - Dynamic runtime settings
- **User preferences** - Stored in context_memory
- **Session settings** - Temporary configuration overrides

#### Environment Variables
```bash
# Optional environment overrides
export CLEVER_DEBUG=true
export CLEVER_DB_PATH="/custom/path/clever.db"
export CLEVER_BACKUP_DIR="/custom/backup/path"
export CLEVER_LOG_LEVEL="DEBUG"
```

## TODO Items

### Configuration Management
- [ ] Implement configuration validation on startup
- [ ] Create configuration migration system for updates
- [ ] Add environment-specific configuration files
- [ ] Implement hot-reload for development configuration
- [ ] Create configuration backup and restore procedures

### Security & Validation
- [ ] Add configuration encryption for sensitive settings
- [ ] Implement configuration integrity checking
- [ ] Create secure configuration storage
- [ ] Add configuration access logging
- [ ] Implement configuration change approval workflow

### Performance & Optimization
- [ ] Create performance-based configuration profiles
- [ ] Implement automatic configuration tuning
- [ ] Add configuration impact analysis
- [ ] Create configuration performance monitoring
- [ ] Implement lazy loading for expensive configurations

### User Experience
- [ ] Create web-based configuration interface
- [ ] Implement configuration export/import functionality
- [ ] Add configuration change history tracking
- [ ] Create configuration reset to defaults
- [ ] Implement configuration wizard for first-time setup

### Integration & Testing
- [ ] Create configuration testing framework
- [ ] Implement configuration compatibility checking
- [ ] Add configuration documentation generation
- [ ] Create configuration change validation
- [ ] Implement configuration rollback mechanisms

---

**Last Updated:** September 4, 2025  
**Changelog:** Initial configuration documentation - comprehensive system configuration guide