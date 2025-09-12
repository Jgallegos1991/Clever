"""
File Watcher Module - Automated file ingestion through filesystem monitoring.

Why: Provides real-time monitoring of configured directories to automatically
     ingest new and modified files into the knowledge base without manual
     intervention, maintaining up-to-date content for AI responses.

Where: Used by sync systems and background processes to watch for file changes
       in configured sync directories for automated knowledge base updates.

How: Implements watchdog-based filesystem monitoring with event handlers that
     trigger appropriate ingestion based on file operations and directory roots.
"""
from __future__ import annotations

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
from file_ingestor import FileIngestor
from database import db_manager


class IngestEventHandler(FileSystemEventHandler):
    """
    File system event handler for automated content ingestion.
    
    Why: Responds to filesystem events (create, modify, move, delete) by
         triggering appropriate ingestion or cleanup actions automatically.
    
    Where: Used by file watcher system to handle events from monitored
           directories and maintain synchronized knowledge base content.
    
    How: Maps directory roots to ingestors, handles different event types,
         and ensures database consistency with filesystem changes.
    """
    
    def __init__(self):
        """
        Initialize event handler with ingestors for configured directories.
        
        Why: Sets up directory-specific ingestors to handle different content
             types and processing requirements for each monitored location.
        
        Where: Called during watcher setup to prepare for filesystem monitoring.
        
        How: Creates FileIngestor instances for each configured sync directory
             using centralized configuration settings.
        """
        super().__init__()
        self.ingestors = {
            config.SYNC_DIR: FileIngestor(config.SYNC_DIR),
            config.SYNAPTIC_HUB_DIR: FileIngestor(config.SYNAPTIC_HUB_DIR),
        }

    def on_modified(self, event):
        """
        Handle file modification events by triggering re-ingestion.
        
        Why: Ensures knowledge base stays current when files are updated,
             maintaining accuracy of AI responses based on latest content.
        
        Where: Called automatically by watchdog when files are modified in
               monitored directories.
        
        How: Filters directory events and delegates file ingestion to
             appropriate ingestor based on path matching.
        """
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_created(self, event):
        """
        Handle file creation events by triggering initial ingestion.
        
        Why: Automatically incorporates new files into knowledge base as they
             are added to monitored directories without manual intervention.
        
        Where: Called automatically by watchdog when new files are created in
               monitored directories.
        
        How: Filters directory events and delegates file ingestion to
             appropriate ingestor based on path matching.
        """
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_moved(self, event):
        """
        Handle file move/rename events by updating database references.
        
        Why: Maintains database consistency when files are moved or renamed,
             preventing orphaned entries and ensuring accurate references.
        
        Where: Called automatically by watchdog when files are moved within
               or into monitored directories.
        
        How: Removes old database entry and creates new entry for destination
             path to maintain consistent file tracking.
        """
        if event.is_directory:
            return
        # Remove old entry, ingest at new location
        db_manager.delete_source_by_path(event.src_path)
        self._ingest_file(event.dest_path)

    def on_deleted(self, event):
        """
        Handle file deletion events by cleaning up database references.
        
        Why: Prevents stale database entries when files are deleted, maintaining
             database integrity and avoiding references to non-existent content.
        
        Where: Called automatically by watchdog when files are deleted from
               monitored directories.
        
        How: Removes corresponding database entry to keep knowledge base
             synchronized with actual filesystem state.
        """
        if event.is_directory:
            return
        db_manager.delete_source_by_path(event.src_path)

    def _ingest_file(self, path: str):
        """
        Route file ingestion to appropriate ingestor based on path.
        
        Why: Ensures files are processed by the correct ingestor based on their
             location, allowing different processing rules per directory.
        
        Where: Called internally by event handlers to process files that have
               been created or modified in monitored directories.
        
        How: Matches file path to configured directory roots and delegates to
             corresponding ingestor with error handling for robustness.
        """
        # Select ingestor based on directory root
        for root, ingestor in self.ingestors.items():
            if path.startswith(root):
                try:
                    ingestor.ingest_file(path)
                except Exception as e:
                    print("watch ingest error:", e)
                break


def run_watch(directories=None):
    """
    Start filesystem monitoring for automated file ingestion.
    
    Why: Provides continuous monitoring of configured directories to maintain
         real-time synchronization between filesystem and knowledge base.
    
    Where: Called by sync systems and background processes to start monitoring
           configured directories for automatic content updates.
    
    How: Sets up watchdog observer with event handler, monitors specified
         directories or defaults to configured sync directories.
    """
    if directories is None:
        directories = [config.SYNC_DIR, config.SYNAPTIC_HUB_DIR]
    
    event_handler = IngestEventHandler()
    observer = Observer()
    
    for directory in directories:
        if os.path.exists(directory):
            observer.schedule(event_handler, directory, recursive=True)
            print(f"Watching directory: {directory}")
    
    observer.start()
    print("File watcher started. Press Ctrl+C to stop.")
    
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        print("File watcher stopped.")


if __name__ == "__main__":
    run_watch()
