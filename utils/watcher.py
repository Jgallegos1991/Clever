from __future__ import annotations

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
from file_ingestor import FileIngestor
from database import db_manager


class IngestEventHandler(FileSystemEventHandler):
    """
    File system event handler for automatic ingestion of changes in monitored directories.
    
    Why: Enables real-time knowledge base updates when files are modified,
         created, moved, or deleted in sync directories.
    Where: Used by watchdog Observer to monitor sync directories and maintain
           synchronized database state with file system changes.
    How: Inherits from FileSystemEventHandler, maintains per-directory FileIngestor
         instances, processes events by delegating to appropriate ingestor.
    """
    
    def __init__(self):
        """
        Initialize event handler with FileIngestor instances for each sync directory.
        
        Why: Sets up dedicated ingestors for efficient processing of changes
             in both SYNC_DIR and SYNAPTIC_HUB_DIR locations.
        Where: Called by run_watch when setting up file system monitoring.
        How: Creates mapping of directory paths to FileIngestor instances
             using configured sync directory paths from config module.
        """
        super().__init__()
        self.ingestors = {
            config.SYNC_DIR: FileIngestor(config.SYNC_DIR),
            config.SYNAPTIC_HUB_DIR: FileIngestor(config.SYNAPTIC_HUB_DIR),
        }

    def on_modified(self, event):
        """
        Handle file modification events by triggering ingestion for updated content.
        
        Why: Ensures knowledge base reflects latest file content when
             files are edited or updated in monitored directories.
        Where: Called by watchdog when file modification events occur
               in directories under observation.
        How: Filters out directory events, passes file path to
             _ingest_file for processing with appropriate FileIngestor.
        """
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_created(self, event):
        """
        Handle file creation events by ingesting newly created files.
        
        Why: Automatically adds new files to knowledge base when they
             appear in monitored sync directories.
        Where: Called by watchdog when new files are created in
               directories under observation.
        How: Filters out directory creation events, triggers ingestion
             for new files using _ingest_file method.
        """
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_moved(self, event):
        """
        Handle file move/rename events by updating database paths and content.
        
        Why: Maintains accurate file path references in knowledge base
             when files are moved or renamed within sync directories.
        Where: Called by watchdog when files are moved or renamed in
               monitored directory structures.
        How: Removes old path from database, ingests file at new location
             to update database with correct path and any content changes.
        """
        if event.is_directory:
            return
        # delete old, ingest new
        db_manager.delete_source_by_path(event.src_path)
        self._ingest_file(event.dest_path)

    def on_deleted(self, event):
        """
        Handle file deletion events by removing entries from knowledge base.
        
        Why: Keeps database synchronized with file system state by removing
             records for files that no longer exist.
        Where: Called by watchdog when files are deleted from
               monitored sync directories.
        How: Filters out directory deletions, uses database manager to
             remove source records matching the deleted file path.
        """
        if event.is_directory:
            return
        db_manager.delete_source_by_path(event.src_path)

    def _ingest_file(self, path: str):
        """
        Process file ingestion using appropriate FileIngestor based on path location.
        
        Why: Routes ingestion requests to correct FileIngestor instance
             based on which sync directory contains the changed file.
        Where: Internal helper method called by all event handlers to
               perform actual file processing and database updates.
        How: Iterates through configured ingestors, matches path prefixes
             to select appropriate instance, handles ingestion errors gracefully.
        
        Args:
            path: File system path of the file to ingest
        """
        # pick ingestor based on root
        for root, ingestor in self.ingestors.items():
            if path.startswith(root):
                ingestor.ingest_file(path)
                break


def run_watch():
    """
    Initialize and run file system monitoring for automatic ingestion.
    
    Why: Provides continuous monitoring of sync directories to maintain
         real-time synchronization between file system and knowledge base.
    Where: Main entry point for file watching service, typically run as
           background process for continuous operation.
    How: Creates Observer and IngestEventHandler, schedules monitoring for
         configured directories, handles graceful shutdown on interruption.
    """
    observer = Observer()
    handler = IngestEventHandler()
    for d in set([config.SYNC_DIR, config.SYNAPTIC_HUB_DIR]):
        if os.path.isdir(d):
            observer.schedule(handler, d, recursive=True)
    observer.start()
    print("Watching for changes...")
    while True:
        observer.join(1)
    observer.stop()
    observer.join()


if __name__ == "__main__":
    run_watch()
