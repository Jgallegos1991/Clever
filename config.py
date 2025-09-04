"""
Central configuration for Clever.

Edit these defaults as needed or override via environment variables.
"""
import os
from pathlib import Path

# Base directories
ROOT_DIR = Path(__file__).resolve().parent

# Minimal .env loader (offline, no extra deps)
def _load_dotenv(path: Path):
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

_load_dotenv(ROOT_DIR / ".env")

# Directories to sync/ingest from
# Restrict file system operations to your two ingestion roots
from pathlib import Path
SYNC_DIR = str(Path("Clever_Sync").resolve())
SYNAPTIC_HUB_DIR = str(Path("synaptic_hub_sync").resolve())

# SQLite database file path
DB_PATH = os.environ.get("CLEVER_DB_PATH", str(ROOT_DIR / "clever.db"))

# Server config
APP_HOST = "0.0.0.0"
APP_PORT = 5000
DEBUG = False

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

# Allowed filesystem roots for local operations (comma-separated paths)
def _split_paths(val: str) -> list[str]:
	return [p.strip() for p in val.split(',') if p.strip()]

HOME_DIR = str(Path.home())
DEFAULT_EXTRA = [HOME_DIR, "/mnt/chromeos/MyFiles", "/mnt/chromeos/GoogleDrive/MyDrive"]
_defaults = [str(ROOT_DIR), str(SYNC_DIR), str(SYNAPTIC_HUB_DIR), *DEFAULT_EXTRA]
ALLOWED_ROOTS = {SYNC_DIR, SYNAPTIC_HUB_DIR}

# Auto-ingest cooldown (minutes) when grounding is weak
AUTO_INGEST_COOLDOWN_MINUTES = int(os.environ.get("AUTO_INGEST_COOLDOWN_MINUTES", "20"))
