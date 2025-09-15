"""
<<<<<<< HEAD
Central configuration for Clever AI

Why: Provides centralized configuration management with environment variable
support, user-specific settings, and default values to enable consistent
configuration across all components while supporting customization.
Where: Imported by all modules requiring configuration settings including
database paths, server settings, sync directories, and operational parameters.
How: Implements configuration hierarchy with environment variables, user config
overrides, and sensible defaults with .env file support for development.

Connects to:
    - user_config.py: User-specific configuration overrides and personalization
    - database.py: Uses DB_PATH for centralized database configuration
    - sync modules: Uses SYNC_DIR and SYNAPTIC_HUB_DIR for file operations
    - app.py: Server configuration including host, port, and debug settings
    - All modules: Centralized configuration source for system-wide settings
=======
Central configuration for Clever AI Assistant.

Why: Provides centralized configuration management for all Clever components, 
     ensuring consistent settings across the application while maintaining 
     offline-first and single-user design principles.

Where: Used by all Python modules that need configuration settings, including
       database paths, server settings, and feature flags.

How: Import this module and access configuration constants directly. 
     Environment variables can override defaults. All paths and settings
     are resolved once at startup for consistency.
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
"""
import os
from pathlib import Path

<<<<<<< HEAD
# Import user-specific configuration - required for full operation
from user_config import *
=======
# Import user-specific configuration (required - no fallbacks per architecture standards)
from user_config import USER_NAME, USER_EMAIL, TAILSCALE_ENABLED, CLEVER_EXTERNAL_ACCESS
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b

# Base directories
ROOT_DIR = Path(__file__).resolve().parent

<<<<<<< HEAD
def _load_dotenv(path: Path):
    """
    Minimal environment file loader for offline operation
    
    Why: Provides environment configuration loading without external dependencies
    to maintain offline-first operation while supporting development configuration
    through .env files with proper error handling.
    Where: Called during configuration initialization to load development
    settings from .env file if present without breaking offline requirements.
    How: Implements simple .env parsing with error handling and environment
    variable setting using only standard library for offline compatibility.
    
    Args:
        path: Path to .env file to load
        
    Connects to:
        - .env file: Development environment configuration
        - os.environ: System environment variable integration
    """
    if not path.exists():
        return
    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip(); v = v.strip().strip('"').strip("'")
            os.environ.setdefault(k, v)
    except Exception:
        pass
=======
def _load_dotenv(path: Path) -> None:
	"""
	Load environment variables from .env file for configuration overrides.
	
	Why: Allows environment-specific configuration without modifying code,
	     supporting different deployment scenarios while staying offline-first.
	
	Where: Called once during module initialization to load .env settings.
	
	How: Reads key=value pairs from .env file and sets them as environment
	     variables if not already set, with basic parsing for quotes.
	"""
	if not path.exists():
		return
	
	for line in path.read_text().splitlines():
		line = line.strip()
		if not line or line.startswith('#'):
			continue
		if '=' not in line:
			continue
		k, v = line.split('=', 1)
		k = k.strip(); v = v.strip().strip('"').strip("'")
		os.environ.setdefault(k, v)
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b

_load_dotenv(ROOT_DIR / ".env")

# Directories to sync/ingest from
<<<<<<< HEAD
# Why: Restrict file system operations to designated ingestion directories
# Where: Used by sync modules and ingestors for file monitoring and processing
=======
# Restrict file system operations to your two ingestion roots
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
from pathlib import Path
SYNC_DIR = str(Path("Clever_Sync").resolve())
SYNAPTIC_HUB_DIR = str(Path("synaptic_hub_sync").resolve())

<<<<<<< HEAD
# SQLite database file path - SINGLE DATABASE ARCHITECTURE
# Why: Centralized database path for single database enforcement across all components
# Where: Used by DatabaseManager and all modules requiring database access
=======
# SQLite database file path
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
DB_PATH = os.environ.get("CLEVER_DB_PATH", str(ROOT_DIR / "clever.db"))

# Server config
APP_HOST = getattr(globals(), 'CLEVER_HOST', "0.0.0.0") if CLEVER_EXTERNAL_ACCESS else "127.0.0.1"
APP_PORT = getattr(globals(), 'CLEVER_PORT', 5000)
DEBUG = getattr(globals(), 'DEBUG_MODE', False)

# rclone settings (optional)
RCLONE_REMOTE = os.environ.get("RCLONE_REMOTE", "")
# By default, target the CLEVER_AI folder on the remote
RCLONE_SRC = os.environ.get("RCLONE_SRC", "CLEVER_AI")
RCLONE_DST = os.environ.get("RCLONE_DST", "CLEVER_AI")
RCLONE_EXTRA = os.environ.get("RCLONE_EXTRA", "--fast-list --checkers 8 --transfers 8 --copy-links")

# Feature flags
# Disable all cloud sync so Clever stays offline-only
ENABLE_RCLONE = False
AUTO_RCLONE_SCHEDULE = os.environ.get("AUTO_RCLONE_SCHEDULE", "false").lower() in {"1", "true", "yes", "on"}
RCLONE_INTERVAL_MINUTES = int(os.environ.get("RCLONE_INTERVAL_MINUTES", "60"))

<<<<<<< HEAD
# Allowed filesystem roots for local operations (comma-separated paths)
def _split_paths(val: str) -> list[str]:
=======
def _split_paths(val: str) -> list[str]:
	"""
	Split comma-separated path string into list of cleaned paths.
	
	Why: Provides consistent parsing of path lists from environment variables
	     or configuration strings, ensuring proper path handling.
	
	Where: Used internally for processing ALLOWED_ROOTS and similar path configs.
	
	How: Splits on comma, strips whitespace, and filters out empty strings
	     to return clean list of path strings.
	"""
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
	return [p.strip() for p in val.split(',') if p.strip()]

HOME_DIR = str(Path.home())
DEFAULT_EXTRA = [HOME_DIR, "/mnt/chromeos/MyFiles", "/mnt/chromeos/GoogleDrive/MyDrive"]
_defaults = [str(ROOT_DIR), str(SYNC_DIR), str(SYNAPTIC_HUB_DIR), *DEFAULT_EXTRA]
ALLOWED_ROOTS = {SYNC_DIR, SYNAPTIC_HUB_DIR}

# Auto-ingest cooldown (minutes) when grounding is weak
AUTO_INGEST_COOLDOWN_MINUTES = int(os.environ.get("AUTO_INGEST_COOLDOWN_MINUTES", "20"))
