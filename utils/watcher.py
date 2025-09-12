from __future__ import annotations

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
from file_ingestor import FileIngestor
from database import db_manager


class IngestEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.ingestors = {
            config.SYNC_DIR: FileIngestor(config.SYNC_DIR),
            config.SYNAPTIC_HUB_DIR: FileIngestor(config.SYNAPTIC_HUB_DIR),
        }

    def on_modified(self, event):
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self._ingest_file(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        # delete old, ingest new
        db_manager.delete_source_by_path(event.src_path)
        self._ingest_file(event.dest_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        db_manager.delete_source_by_path(event.src_path)

    def _ingest_file(self, path: str):
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


if __name__ == "__main__":
    run_watch()
