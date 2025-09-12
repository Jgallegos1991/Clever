from __future__ import annotations

import time
import threading

import config
from sync_tools import sync_clever_from_remote, sync_synaptic_from_remote
from file_ingestor import FileIngestor


def _run_cycle():
    # sync both (best effort) then ingest both roots
    if config.ENABLE_RCLONE:
        sync_clever_from_remote()
        sync_synaptic_from_remote()
    for d in [config.SYNC_DIR, config.SYNAPTIC_HUB_DIR]:
        FileIngestor(d).ingest_all_files()


def run_scheduler(stop_event: threading.Event | None = None):
    if not config.AUTO_RCLONE_SCHEDULE:
        print("Scheduler disabled.")
        return
    iv = max(1, int(config.RCLONE_INTERVAL_MINUTES)) * 60
    print(f"Scheduler running every {iv//60} min(s)...")
    while True:
        if stop_event and stop_event.is_set():
            break
        try:
            _run_cycle()
        except Exception as e:
            print("scheduler cycle error:", e)
        # sleep in small chunks so we can exit promptly
        for _ in range(iv):
            if stop_event and stop_event.is_set():
                break
            time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
