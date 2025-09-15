<<<<<<< HEAD
=======
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
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
from __future__ import annotations

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
from file_ingestor import FileIngestor
from database import db_manager


class IngestEventHandler(FileSystemEventHandler):
<<<<<<< HEAD
    def __init__(self):
=======
    """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
    File system event handler for automatic ingestion of changes in monitored directories.
    
    Why: Enables real-time knowledge base updates when files are modified,
         created, moved, or deleted in sync directories.
    Where: Used by watchdog Observer to monitor sync directories and maintain
           synchronized database state with file system changes.
    How: Inherits from FileSystemEventHandler, maintains per-directory FileIngestor
         instances, processes events by delegating to appropriate ingestor.

    File system event handler for automated content ingestion.
    
    Why: Responds to filesystem events (create, modify, move, delete) by
         triggering appropriate ingestion or cleanup actions automatically.
    
    Where: Used by file watcher system to handle events from monitored
           directories and maintain synchronized knowledge base content.
    
    How: Maps directory roots to ingestors, handles different event types,
         and ensures database consistency with filesystem changes.
 main
    """
    
    def __init__(self):
        """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
        Initialize event handler with FileIngestor instances for each sync directory.
        
        Why: Sets up dedicated ingestors for efficient processing of changes
             in both SYNC_DIR and SYNAPTIC_HUB_DIR locations.
        Where: Called by run_watch when setting up file system monitoring.
        How: Creates mapping of directory paths to FileIngestor instances
             using configured sync directory paths from config module.

        Initialize event handler with ingestors for configured directories.
        
        Why: Sets up directory-specific ingestors to handle different content
             types and processing requirements for each monitored location.
        
        Where: Called during watcher setup to prepare for filesystem monitoring.
        
        How: Creates FileIngestor instances for each configured sync directory
             using centralized configuration settings.
 main
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        super().__init__()
        self.ingestors = {
            config.SYNC_DIR: FileIngestor(config.SYNC_DIR),
            config.SYNAPTIC_HUB_DIR: FileIngestor(config.SYNAPTIC_HUB_DIR),
        }

    def on_modified(self, event):
<<<<<<< HEAD
=======
        """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
        Handle file modification events by triggering ingestion for updated content.
        
        Why: Ensures knowledge base reflects latest file content when
             files are edited or updated in monitored directories.
        Where: Called by watchdog when file modification events occur
               in directories under observation.
        How: Filters out directory events, passes file path to
             _ingest_file for processing with appropriate FileIngestor.

        Handle file modification events by triggering re-ingestion.
        
        Why: Ensures knowledge base stays current when files are updated,
             maintaining accuracy of AI responses based on latest content.
        
        Where: Called automatically by watchdog when files are modified in
               monitored directories.
        
        How: Filters directory events and delegates file ingestion to
             appropriate ingestor based on path matching.
 main
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_created(self, event):
<<<<<<< HEAD
=======
        """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
        Handle file creation events by ingesting newly created files.
        
        Why: Automatically adds new files to knowledge base when they
             appear in monitored sync directories.
        Where: Called by watchdog when new files are created in
               directories under observation.
        How: Filters out directory creation events, triggers ingestion
             for new files using _ingest_file method.

        Handle file creation events by triggering initial ingestion.
        
        Why: Automatically incorporates new files into knowledge base as they
             are added to monitored directories without manual intervention.
        
        Where: Called automatically by watchdog when new files are created in
               monitored directories.
        
        How: Filters directory events and delegates file ingestion to
             appropriate ingestor based on path matching.
 main
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_moved(self, event):
<<<<<<< HEAD
        if event.is_directory:
            return
        # delete old, ingest new
=======
        """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
        Handle file move/rename events by updating database paths and content.
        
        Why: Maintains accurate file path references in knowledge base
             when files are moved or renamed within sync directories.
        Where: Called by watchdog when files are moved or renamed in
               monitored directory structures.
        How: Removes old path from database, ingests file at new location
             to update database with correct path and any content changes.

        Handle file move/rename events by updating database references.
        
        Why: Maintains database consistency when files are moved or renamed,
             preventing orphaned entries and ensuring accurate references.
        
        Where: Called automatically by watchdog when files are moved within
               or into monitored directories.
        
        How: Removes old database entry and creates new entry for destination
             path to maintain consistent file tracking.
 main
        """
        if event.is_directory:
            return
        # Remove old entry, ingest at new location
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        db_manager.delete_source_by_path(event.src_path)
        self._ingest_file(event.dest_path)

    def on_deleted(self, event):
<<<<<<< HEAD
=======
        """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
        Handle file deletion events by removing entries from knowledge base.
        
        Why: Keeps database synchronized with file system state by removing
             records for files that no longer exist.
        Where: Called by watchdog when files are deleted from
               monitored sync directories.
        How: Filters out directory deletions, uses database manager to
             remove source records matching the deleted file path.

        Handle file deletion events by cleaning up database references.
        
        Why: Prevents stale database entries when files are deleted, maintaining
             database integrity and avoiding references to non-existent content.
        
        Where: Called automatically by watchdog when files are deleted from
               monitored directories.
        
        How: Removes corresponding database entry to keep knowledge base
             synchronized with actual filesystem state.
 main
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        if event.is_directory:
            return
        db_manager.delete_source_by_path(event.src_path)

    def _ingest_file(self, path: str):
<<<<<<< HEAD
        # pick ingestor based on root
        for root, ingestor in self.ingestors.items():
            if path.startswith(root):
                try:
                    ingestor.ingest_file(path)
                except Exception as e:
                    print("watch ingest error:", e)
                break


def run_watch():
    observer = Observer()
    handler = IngestEventHandler()
    for d in set([config.SYNC_DIR, config.SYNAPTIC_HUB_DIR]):
        if os.path.isdir(d):
            observer.schedule(handler, d, recursive=True)
    observer.start()
    print("Watching for changes...")
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.stop()
    observer.join()

=======
        """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
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

        Route file ingestion to appropriate ingestor based on path.
        
        Why: Ensures files are processed by the correct ingestor based on their
             location, allowing different processing rules per directory.
        
        Where: Called internally by event handlers to process files that have
               been created or modified in monitored directories.
        
        How: Matches file path to configured directory roots and delegates to
             corresponding ingestor with error handling for robustness.
        """
        # Select ingestor based on directory root
 main
        for root, ingestor in self.ingestors.items():
            if path.startswith(root):
                ingestor.ingest_file(path)
                break


 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
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
 main
    observer = Observer()
    
    for directory in directories:
        if os.path.exists(directory):
            observer.schedule(event_handler, directory, recursive=True)
            print(f"Watching directory: {directory}")
    
    observer.start()
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
    print("Watching for changes...")
    while True:
        observer.join(1)
    observer.stop()
    observer.join()

    print("File watcher started. Press Ctrl+C to stop.")
    
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        print("File watcher stopped.")
 main

>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b

if __name__ == "__main__":
    run_watch()
