"""
Lightweight watcher shim (clean) — delegates to sync_watcher.py

Why: The original utils/watcher.py was corrupted with merge artifacts. This
     shim preserves a stable API while the real watcher lives in sync_watcher.py.
Where: Any legacy code importing utils.watcher will still function.
How: Exposes a run_watch() that simply starts the sync watcher.

Connects to:
    - sync_watcher.py: The actual implementation using watchdog
    - file_ingestor.py: Used by sync watcher to ingest files
"""

from __future__ import annotations

from sync_watcher import main as _sync_main


def run_watch() -> None:
    """Start the sync watcher service.
    
    Why: Maintain backwards compatibility for callers expecting run_watch.
    Where: Called by legacy scripts; internally delegates to sync_watcher.main.
    How: Simple wrapper that invokes the consolidated watcher implementation.
    """
    _sync_main()


if __name__ == "__main__":
    run_watch()
