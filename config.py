"""
Central Configuration for Clever - Digital Brain Extension & Cognitive Partnership System

Why: Core configuration hub that enables Clever's digital sovereignty and cognitive
partnership capabilities. Ensures all components work together as a unified brain
extension system with complete local control and privacy.
Where: Foundation layer imported by all Clever modules - from conversation engine
to memory system to particle UI. Creates the consistent environment needed for 
authentic cognitive partnership.
How: Hierarchical configuration with environment variables, user personalization,
and secure defaults. Single database design ensures coherent memory system for
continuous relationship building with Jay.

Connects to:
    - user_config.py: Imports `user_config` to source user-specific settings like `CLEVER_HOST`, `CLEVER_PORT`, and `DEBUG_MODE`.
    - database.py: The `db_manager` instance is initialized using `config.DB_PATH`, making this the central point for defining the database location.
    - memory_engine.py: The `get_memory_engine()` factory function uses `config.DB_PATH` when creating the `DatabaseManager`.
    - app.py: Uses `APP_HOST`, `APP_PORT`, and `DEBUG` to configure the Flask server, ensuring it respects the local-only rule.
    - sync_watcher.py: Uses `SYNC_DIR` and `SYNAPTIC_HUB_DIR` to know which directories to monitor for file changes.
    - file_ingestor.py: The main `FileIngestor` is instantiated using `config.SYNC_DIR` to know where to look for files to ingest.
    - pdf_ingestor.py: The `EnhancedFileIngestor` uses `config.SYNC_DIR` as one of its default source directories.
    - system_validator.py: `_validate_single_database()` reads `config.DB_PATH` to verify the single database rule.
    - health_monitor.py: `check_database_health()` reads `config.DB_PATH` to locate and check the database file.
"""

import os
from pathlib import Path

# Import user configuration explicitly to avoid star-import issues (F403/F405)
import user_config as _user_config

# Base directories
ROOT_DIR = Path(__file__).resolve().parent


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
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            os.environ.setdefault(k, v)
    except Exception:
        pass


_load_dotenv(ROOT_DIR / ".env")

# Directories to sync/ingest from
SYNC_DIR = str(Path("Clever_Sync").resolve())
SYNAPTIC_HUB_DIR = str(Path("synaptic_hub_sync").resolve())

DB_PATH = os.environ.get("CLEVER_DB_PATH", str(ROOT_DIR / "clever.db"))

# Server config
APP_HOST = (
    getattr(_user_config, "CLEVER_HOST", "0.0.0.0")
    if getattr(_user_config, "CLEVER_EXTERNAL_ACCESS", False)
    else "127.0.0.1"
)
APP_PORT = getattr(_user_config, "CLEVER_PORT", 5000)
DEBUG = getattr(_user_config, "DEBUG_MODE", False)

# rclone settings (optional)
RCLONE_REMOTE = os.environ.get("RCLONE_REMOTE", "")
# By default, target the CLEVER_AI folder on the remote
RCLONE_SRC = os.environ.get("RCLONE_SRC", "CLEVER_AI")
RCLONE_DST = os.environ.get("RCLONE_DST", "CLEVER_AI")
RCLONE_EXTRA = os.environ.get(
    "RCLONE_EXTRA", "--fast-list --checkers 8 --transfers 8 --copy-links"
)

# Feature flags
# Disable all cloud sync so Clever stays offline-only
ENABLE_RCLONE = False
AUTO_RCLONE_SCHEDULE = os.environ.get("AUTO_RCLONE_SCHEDULE", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
RCLONE_INTERVAL_MINUTES = int(os.environ.get("RCLONE_INTERVAL_MINUTES", "60"))


def _split_paths(val: str) -> list[str]:
    """
    Split comma-separated path string into list of cleaned paths.
    Why: Provides consistent parsing of path lists from environment variables or configuration strings, ensuring proper path handling.
    Where: Used internally for processing ALLOWED_ROOTS and similar path configs.
    How: Splits on comma, strips whitespace, and filters out empty strings to return clean list of path strings.
    """
    return [p.strip() for p in val.split(",") if p.strip()]


HOME_DIR = str(Path.home())
DEFAULT_EXTRA = [HOME_DIR, "/mnt/chromeos/MyFiles", "/mnt/chromeos/GoogleDrive/MyDrive"]
_defaults = [str(ROOT_DIR), str(SYNC_DIR), str(SYNAPTIC_HUB_DIR), *DEFAULT_EXTRA]
ALLOWED_ROOTS = {SYNC_DIR, SYNAPTIC_HUB_DIR}

# Auto-ingest cooldown (minutes) when grounding is weak
AUTO_INGEST_COOLDOWN_MINUTES = int(os.environ.get("AUTO_INGEST_COOLDOWN_MINUTES", "20"))
