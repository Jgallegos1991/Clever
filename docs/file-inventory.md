# File Inventory

## Core Python Components

### Primary Application Files
- **`app.py`** - Main Flask application server and route definitions
- **`config.py`** - System configuration and environment settings
- **`database.py`** - SQLite database connection and management utilities
- **`persona.py`** - Clever's AI personality and response generation logic

### Natural Language Processing
- **`nlp_processor.py`** - spaCy NLP pipeline and text analysis engine
- **`core_nlp_logic.py`** - Command recognition and intent classification
- **`file_ingestor.py`** - Document parsing and knowledge extraction

### Data Management
- **`backup_manager.py`** - Database backup and restore functionality
- **`clever_memory.db`** - SQLite database containing conversation history and knowledge
- **`conversations.json`** - JSON backup of conversation data

### Frontend Assets

#### HTML Templates
- **`templates/index.html`** - Main application interface structure

#### JavaScript Components
- **`static/js/main.js`** - Primary frontend logic and API communication
- **`static/js/orb_engine.js`** - 3D particle system and "living orb" visualization
- **`static/js/three-bridge.js`** - Three.js integration and 3D scene management

#### Styling
- **`static/css/`** - Stylesheet directory for UI theming
- **`static/vendor/`** - Third-party libraries (Three.js, Tailwind CSS)

#### Assets
- **`static/img/`** - Image assets for UI
- **`static/manifest.webmanifest`** - Progressive Web App configuration

### Configuration & Build
- **`requirements.txt`** - Python dependencies specification
- **`Makefile`** - Build automation and development commands
- **`.gitignore`** - Git exclusion patterns
- **`.vscode/`** - Visual Studio Code workspace configuration

### Development & Scripts
- **`scripts/`** - Utility scripts for development and maintenance
- **`projects/`** - Additional project files and resources
- **`.github/`** - GitHub Actions workflows and repository configuration
- **`.devcontainer/`** - Development container configuration

## Data Files

### Database Files
- **`clever_memory.db`** (45KB) - Primary SQLite database
  - User utterances table
  - Conversation history
  - Context and memory storage

### Backup & Sync
- **`backups/`** - Database backup storage (configured)
- **`Clever_Sync/`** - Google Drive synchronization folder (configured)
- **`uploads/`** - File upload temporary storage (configured)

### Generated Assets
- **Image files**: AI-generated visual assets for documentation
- **JSON exports**: Conversation and configuration backups

## TODO Items

### File Organization
- [ ] Audit file permissions and security settings
- [ ] Document file size limits and cleanup procedures
- [ ] Create file naming conventions documentation
- [ ] Map temporary file handling and cleanup
- [ ] Document log file rotation and retention

### Component Mapping
- [ ] Create detailed component dependency graph
- [ ] Document import relationships between Python modules
- [ ] Map frontend asset loading and dependencies
- [ ] Document database file structure and indexes
- [ ] Create build artifact inventory

### Configuration Files
- [ ] Document all configuration files and their purposes
- [ ] Map environment variable usage
- [ ] Document development vs production configurations
- [ ] Create configuration validation procedures
- [ ] Document secret and sensitive data handling

### Asset Management
- [ ] Document static asset optimization and compression
- [ ] Create frontend build process documentation
- [ ] Map third-party library versions and update procedures
- [ ] Document CDN alternatives for offline operation
- [ ] Create asset integrity verification procedures

---

**Last Updated:** September 4, 2025  
**Changelog:** Initial file inventory - comprehensive mapping of all project components