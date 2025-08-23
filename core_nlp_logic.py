# Compatibility wrapper for legacy code
def process_text(nlp_model, text):
    """Wrapper for process_text_input for backward compatibility."""
    return process_text_input(nlp_model, text)
import os
import spacy

# Ensure variables like BASE_DIR are defined before usage
if '__file__' not in globals():
    __file__ = os.path.abspath(os.getcwd())

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR

# --------------------------
# Paths
# --------------------------
# Using BASE_DIR for project path as it's more robust for different environments.
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

# Upgrade logic for future configuration changes
def upgrade_configurations():
    """Upgrade configurations to handle future changes."""
    # Example: Add new configuration keys if they don't exist
    global MODES, DEFAULT_MODE
    if "experimental" not in MODES:
        MODES.append("experimental")
    if DEFAULT_MODE not in MODES:
        DEFAULT_MODE = "quick_hit"  # Reset to default if invalid

# Finalize configurations and ensure upgrade logic is robust
def finalize_configurations():
    """Ensure all configurations are finalized and consistent."""
    global UI_PIXELS_ENABLED, ALLOW_REMOTE_SYNC
    # Correct the logic using these built-ins
    if not isinstance(UI_PIXELS_ENABLED, bool):
        UI_PIXELS_ENABLED = True  # Default to True if invalid

    if not isinstance(ALLOW_REMOTE_SYNC, bool):
        ALLOW_REMOTE_SYNC = False  # Default to False if invalid

# Call the upgrade function to ensure configurations are up-to-date
upgrade_configurations()
finalize_configurations()

# Initialize the spaCy NLP model
def initialize_nlp_model():
    """Load and return the spaCy NLP model."""
    try:
        nlp_model = spacy.load(SPACY_MODEL)
        return nlp_model
    except OSError as e:
        raise RuntimeError(f"OS error while loading spaCy model '{SPACY_MODEL}': {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while loading spaCy model '{SPACY_MODEL}': {e}")

# Process text input using the NLP model
def process_text_input(nlp_model, text):
    """Analyze text input and extract intents, sentiments, and keywords."""
    if not text or not isinstance(text, str):
        return {"intents": [], "sentiments": None, "keywords": []}

    doc = nlp_model(text)

    # Extract keywords (using named entities and noun chunks as an example)
    keywords = list(set(ent.text for ent in doc.ents) | set(chunk.text for chunk in doc.noun_chunks))

    # Placeholder for intents and sentiments (to be implemented with custom logic)
    intents = []
    sentiments = None

    return {
        "intents": intents,
        "sentiments": sentiments,
        "keywords": keywords
    }
