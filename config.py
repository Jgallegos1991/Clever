"""
Central configuration for Clever AI Assistant.

Why: Provides centralized configuration management for all Clever components, 
     ensuring consistent settings across the application while maintaining 
     offline-first and single-user design principles.

Where: Used by all Python modules that need configuration settings, including
       database paths, server settings, and feature flags.

How: Import this module and access configuration constants directly. 
     Environment variables can override defaults. All paths and settings
     are resolved once at startup for consistency.
"""
import os
from pathlib import Path

# Import user-specific configuration (required - no fallbacks per architecture standards)
from user_config import USER_NAME, USER_EMAIL, TAILSCALE_ENABLED, CLEVER_EXTERNAL_ACCESS

# Base directories
ROOT_DIR = Path(__file__).resolve().parent

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

_load_dotenv(ROOT_DIR / ".env")

# Directories to sync/ingest from
# Restrict file system operations to your two ingestion roots
from pathlib import Path
SYNC_DIR = str(Path("Clever_Sync").resolve())
SYNAPTIC_HUB_DIR = str(Path("synaptic_hub_sync").resolve())

# SQLite database file path
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

def _split_paths(val: str) -> list[str]:
	"""
	Split comma-separated path string into list of cleaned paths.
	
	Why: Provides consistent parsing of path lists from environment variables
	     or configuration strings, ensuring proper path handling.
	
	Where: Used internally for processing ALLOWED_ROOTS and similar path configs.
	
	How: Splits on comma, strips whitespace, and filters out empty strings
	     to return clean list of path strings.
	"""
	return [p.strip() for p in val.split(',') if p.strip()]

HOME_DIR = str(Path.home())
DEFAULT_EXTRA = [HOME_DIR, "/mnt/chromeos/MyFiles", "/mnt/chromeos/GoogleDrive/MyDrive"]
_defaults = [str(ROOT_DIR), str(SYNC_DIR), str(SYNAPTIC_HUB_DIR), *DEFAULT_EXTRA]
ALLOWED_ROOTS = {SYNC_DIR, SYNAPTIC_HUB_DIR}

# Auto-ingest cooldown (minutes) when grounding is weak
AUTO_INGEST_COOLDOWN_MINUTES = int(os.environ.get("AUTO_INGEST_COOLDOWN_MINUTES", "20"))
