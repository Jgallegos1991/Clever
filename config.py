import os

# Get the absolute path of the directory where this file is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --------------------------
# Paths
# --------------------------
# Using BASE_DIR for project path as it's more robust for different environments.
PROJECT_PATH = BASE_DIR  # Assuming BASE_DIR is the project root

BACKUP_DIR = os.path.join(PROJECT_PATH, "backups")
MEMORY_DB_PATH = os.path.join(PROJECT_PATH, "clever_memory.db")
SYNC_DIR = os.path.join(PROJECT_PATH, "Clever_Sync")

# --- Database Configuration ---
# Changed DATABASE_NAME to point to the new database file as per your analysis.
# Keeping DATABASE_NAME for consistency with existing code if it references it,
# but MEMORY_DB_PATH is now the primary definition based on proposed structure.
DATABASE_NAME = MEMORY_DB_PATH

# --- File Upload Configuration ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'md', 'pdf'}  # Added PDF based on mind map

# --- AI Model Configuration ---
# This allows us to easily swap models in the future
SPACY_MODEL = "en_core_web_sm"

# --------------------------
# UI Options
# --------------------------
UI_PIXELS_ENABLED = True
UI_DEFAULT_COLOR = "#FFFFFF"
UI_DEFAULT_EXPRESSION = "idle"

# --------------------------
# Operational Modes
# --------------------------
MODES = ["deep_dive", "quick_hit", "creative", "support"]
DEFAULT_MODE = "quick_hit"

# --------------------------
# Offline Flags
# --------------------------
OFFLINE_ONLY = True
ALLOW_REMOTE_SYNC = False  # Only enable if using rclone workarounds

# --------------------------
# Backup Options
# --------------------------
KEEP_LATEST_BACKUPS = 1
BACKUP_ZIP_FORMAT = "backup_%Y-%m-%d_%H-%M-%S.zip"
