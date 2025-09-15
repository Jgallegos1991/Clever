from __future__ import annotations

import time
import threading

import config
from sync_tools import sync_clever_from_remote, sync_synaptic_from_remote
from file_ingestor import FileIngestor


def _run_cycle():
<<<<<<< HEAD
=======
    """
    Execute one complete sync and ingestion cycle for all configured directories.
    
    Why: Performs automated synchronization and file processing to maintain
         up-to-date knowledge base without manual intervention.
    Where: Called by run_scheduler at configured intervals to process
           both sync directories and ingest new content.
    How: Conditionally syncs from remote using rclone (if enabled), then
         runs FileIngestor on both SYNC_DIR and SYNAPTIC_HUB_DIR.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    # sync both (best effort) then ingest both roots
    if config.ENABLE_RCLONE:
        sync_clever_from_remote()
        sync_synaptic_from_remote()
    for d in [config.SYNC_DIR, config.SYNAPTIC_HUB_DIR]:
        FileIngestor(d).ingest_all_files()


def run_scheduler(stop_event: threading.Event | None = None):
<<<<<<< HEAD
=======
    """
    Run the continuous scheduling system for automated sync and ingestion.
    
    Why: Provides automated background processing to keep Clever AI's
         knowledge base synchronized with external file changes.
    Where: Main scheduler entry point, typically run as background service
           or in dedicated thread for continuous operation.
    How: Checks configuration, calculates interval timing, runs sync cycles
         in loop with interruptible sleep, handles errors gracefully.
    
    Args:
        stop_event: Optional threading Event to enable graceful shutdown
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    if not config.AUTO_RCLONE_SCHEDULE:
        print("Scheduler disabled.")
        return
    iv = max(1, int(config.RCLONE_INTERVAL_MINUTES)) * 60
    print(f"Scheduler running every {iv//60} min(s)...")
    while True:
        if stop_event and stop_event.is_set():
            break
<<<<<<< HEAD
        try:
            _run_cycle()
        except Exception as e:
            print("scheduler cycle error:", e)
=======
        _run_cycle()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        # sleep in small chunks so we can exit promptly
        for _ in range(iv):
            if stop_event and stop_event.is_set():
                break
            time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
