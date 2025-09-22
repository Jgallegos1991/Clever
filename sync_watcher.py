#!/usr/bin/env python3
"""
Clever Sync Watcher - Monitors sync directories for changes and triggers ingestion

This script watches the Clever_Sync and synaptic_hub_sync directories for file changes
and automatically triggers ingestion when new files are detected.

Usage:
    python sync_watcher.py

Environment Variables:
    CLEVER_SYNC_DIR: Path to Clever_Sync directory (default: ./Clever_Sync)
    SYNAPTIC_HUB_SYNC_DIR: Path to synaptic_hub_sync directory (default: ./synaptic_hub_sync)
    FLASK_URL: Flask server URL (default: http://localhost:5000)
"""

 
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SyncEventHandler(FileSystemEventHandler):
    """File system event handler for automatic ingestion of sync directory changes.
    
    Why: Enables real-time processing of files added to sync directories,
        ensuring Clever AI's knowledge base stays current with external changes.
    Where: Used by the sync watcher system to monitor Clever_Sync and 
         synaptic_hub_sync directories for file system events.
    How: Inherits from FileSystemEventHandler, debounces events to prevent
        rapid-fire ingestion, and directly uses FileIngestor for processing.

    Connects to:
        - file_ingestor.py:
            - `__init__()`: Creates an instance of `FileIngestor`.
            - `trigger_ingestion()`: Calls `self.ingestor.ingest_file()` to process the changed file.
        - config.py:
            - `main()`: Reads `config.SYNC_DIR` and `config.SYNAPTIC_HUB_DIR` to determine which directories to monitor.
            - `SyncEventHandler.__init__()`: The `FileIngestor` it creates is initialized with `config.SYNC_DIR`.
    """
    def __init__(self):
        """Initialize sync event handler with debouncing + FileIngestor.
        
        Why: Prevent repeated rapid ingestion and centralize ingestion logic.
        Where: Constructed in main() when watcher starts.
        How: Sets timestamp, debounce interval, and instantiates FileIngestor.
        """
        self.last_trigger = 0
        self.debounce_seconds = 2  # Prevent rapid-fire ingestion
        # Lazy import to avoid circulars during certain test contexts
        from file_ingestor import FileIngestor  # local import by design
        self.ingestor = FileIngestor(base_dir=config.SYNC_DIR)
        
    def on_any_event(self, event):
        """Process filesystem events with debouncing and filtering."""
        if event.is_directory:
            return
        # Debounce rapid events
        current_time = time.time()
        if current_time - self.last_trigger < self.debounce_seconds:
            return
        self.last_trigger = current_time
        # Skip temporary files and hidden files
        src = str(event.src_path)
        if any(pattern in src for pattern in ['.tmp', '.swp', '~', '.DS_Store']):
            return
        logger.info(f"File change detected: {src}")
        # Trigger direct ingestion
        self.trigger_ingestion(src)
        
    def trigger_ingestion(self, file_path):
        """Trigger ingestion endpoint on Flask server"""
        """
        Execute direct file ingestion with comprehensive error handling.
        
        Why: Processes detected file changes immediately to keep Clever AI's
             knowledge base synchronized with external file updates.
        Where: Called by on_any_event after successful event filtering and
               debouncing validation.
        How: Uses FileIngestor to process the file, logs ingestion status,
             and handles any processing errors gracefully with detailed logging.
        
        Args:
            file_path: Path to the file that triggered the ingestion event
        """
        try:
            status = self.ingestor.ingest_file(file_path)
            if status in ("inserted", "updated"):
                logger.info(f"Ingestion {status} for {file_path}")
            else:
                logger.info(f"No ingestion needed for {file_path} (status: {status})")
        except Exception as e:
            logger.error(f"Error during ingestion of {file_path}: {e}")

def main():
    """
    Initialize and run the sync directory monitoring system.
    
    Why: Provides continuous monitoring of sync directories to enable
         real-time knowledge base updates for Clever AI's offline-first architecture.
    Where: Entry point for the sync watcher service, typically run as a
           background process or daemon.
    How: Configures directory paths from environment, validates existence,
         sets up watchdog Observer with SyncEventHandler, and runs monitoring loop.
    """
    
    # Get configuration from config.py
    clever_sync_dir = config.SYNC_DIR
    synaptic_hub_sync_dir = config.SYNAPTIC_HUB_DIR
    
    # Convert to Path objects and check if they exist
    sync_dirs = []
    
    clever_path = Path(clever_sync_dir)
    if clever_path.exists():
        sync_dirs.append(clever_path)
        logger.info(f"Watching Clever_Sync: {clever_path.absolute()}")
    else:
        logger.warning(f"Clever_Sync directory not found: {clever_path.absolute()}")
        
    synaptic_path = Path(synaptic_hub_sync_dir)
    if synaptic_path.exists():
        sync_dirs.append(synaptic_path)
        logger.info(f"Watching synaptic_hub_sync: {synaptic_path.absolute()}")
    else:
        logger.warning(f"synaptic_hub_sync directory not found: {synaptic_path.absolute()}")
        
    if not sync_dirs:
        logger.error("No sync directories found. Creating Clever_Sync directory...")
        clever_path.mkdir(exist_ok=True)
        sync_dirs.append(clever_path)
        logger.info(f"Created and watching: {clever_path.absolute()}")
    
    # Set up event handler and observer
    # Initialize sync handler
    event_handler = SyncEventHandler()
    observer = Observer()
    
    # Start watching each directory
    for sync_dir in sync_dirs:
        observer.schedule(event_handler, str(sync_dir), recursive=True)
        
    # Start the observer
    observer.start()
    logger.info("Sync watcher started. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping sync watcher...")
        observer.stop()
        
    observer.join()
    logger.info("Sync watcher stopped.")

if __name__ == "__main__":
    main()
