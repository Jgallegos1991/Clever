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

import os
import sys  # keep for exit, but requests removed
import time
import logging
import sys
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
    """Handles file system events in sync directories"""
    
    def __init__(self):
    """
    File system event handler for automatic ingestion of sync directory changes.
    
    Why: Enables real-time processing of files added to sync directories,
         ensuring Clever AI's knowledge base stays current with external changes.
    Where: Used by the sync watcher system to monitor Clever_Sync and 
           synaptic_hub_sync directories for file system events.
    How: Inherits from FileSystemEventHandler, debounces events to prevent
         rapid-fire ingestion, and directly uses FileIngestor for processing.
    """
    
    def __init__(self):
        """
        Initialize the sync event handler with debouncing and direct ingestion.
        
        Why: Sets up debouncing to prevent excessive ingestion calls and
             establishes direct connection to FileIngestor for efficient processing.
        Where: Called when SyncEventHandler is instantiated by the sync watcher.
        How: Configures debounce timing, imports FileIngestor, and initializes
             with the configured sync directory from config.SYNC_DIR.
        """
        self.last_trigger = 0
        self.debounce_seconds = 2  # Prevent rapid-fire ingestion
        # Direct ingestion via FileIngestor
        from file_ingestor import FileIngestor
        import config
        self.ingestor = FileIngestor(base_dir=config.SYNC_DIR)
        
    def on_any_event(self, event):
        """React to any file system event"""
        """
        Process any file system event with intelligent filtering and debouncing.
        
        Why: Automatically detects file changes in sync directories to maintain
             up-to-date knowledge base without manual intervention.
        Where: Called by the watchdog Observer when any file system event occurs
               in monitored directories.
        How: Filters out directories and temporary files, applies debouncing to
             prevent rapid-fire triggers, then initiates ingestion for valid files.
        """
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
    """Main function to set up watchers and start monitoring"""
    
    # Get configuration from environment
    clever_sync_dir = os.getenv('CLEVER_SYNC_DIR', './Clever_Sync')
    synaptic_hub_sync_dir = os.getenv('SYNAPTIC_HUB_SYNC_DIR', './synaptic_hub_sync')
    flask_url = os.getenv('FLASK_URL', 'http://localhost:5000')
            raise  # Re-raise instead of swallowing the exception

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
