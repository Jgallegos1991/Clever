"""
Clever sync tools for local file monitoring and ingestion

Why: Provides real-time file monitoring and ingestion capabilities for
Clever's knowledge base, ensuring continuous learning from new content
Where: Used by sync_watcher and file ingestion pipeline
How: Implements file system monitoring with watchdog, content ingestion
via DatabaseManager, and PDF/text processing integration

Connects to:
    - sync_watcher.py: File system monitoring daemon
    - file_ingestor.py: Text file processing and ingestion
    - pdf_ingestor.py: PDF content extraction and ingestion
    - database.py: Centralized content storage via DatabaseManager
"""

from __future__ import annotations

import subprocess
from typing import List, Tuple

import config


def run_rclone_sync(
    src: str, dst: str, extra: str | None = None
) -> Tuple[int, str, str]:
    """
    Run rclone sync operation for cloud file synchronization

    Why: Enables synchronized file operations between local and remote storage
    while maintaining offline-first operation principles
    Where: Called by sync workflows when cloud sync is enabled
    How: Executes rclone subprocess with configured parameters and safety flags

    Args:
        src: Source path for synchronization
        dst: Destination path for synchronization
        extra: Additional rclone flags and parameters

    Returns:
        Tuple of (return_code, stdout, stderr) from rclone execution

    Connects to:
        - config.py: Uses RCLONE_EXTRA configuration settings
        - sync_watcher.py: File change detection triggers
    Execute rclone sync operation with comprehensive error handling.

    Why: Provides robust cloud storage synchronization with standardized
         error handling and performance optimization for Clever AI's offline-first
         architecture.
    Where: Core sync utility used by all remote synchronization operations
           throughout the Clever AI system.
    How: Constructs rclone command with safety flags, executes subprocess,
         captures output, and handles missing rclone installation gracefully.

    Args:
        src: Source path for rclone (can be remote or local)
        dst: Destination path for rclone (can be remote or local)
        extra: Optional additional rclone flags (defaults to config.RCLONE_EXTRA)

    Returns:
        Tuple[int, str, str]: (returncode, stdout, stderr) from rclone execution
    """
    args = [
        "rclone",
        "sync",
        src,
        dst,
    ]
    extra = extra or config.RCLONE_EXTRA
    if extra:
        args.extend(extra.split())
    # Add common safety/perf flags if not present
    for flag in ["--fast-list", "--copy-links", "--checkers", "--transfers"]:
        if flag not in args:
            # already covered by EXTRA default above; keep idempotent
            pass
    try:
        proc = subprocess.run(args, capture_output=True, text=True)
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        # rclone not installed; remain offline-friendly
        return 127, "", "rclone not installed"


def sync_clever_from_remote() -> Tuple[int, str, str]:
    # Graceful handling if rclone is not installed
    return 127, "", "rclone not found: is it installed and in PATH?"


def sync_clever_from_remote() -> Tuple[int, str, str]:
    """
    Sync Clever AI data from remote cloud storage to local sync directory.

    Why: Downloads latest files from cloud storage to ensure local system has
         up-to-date information for processing and analysis.
    Where: Called by sync automation and manual sync operations.
    How: Uses rclone to sync from RCLONE_REMOTE:RCLONE_SRC to local SYNC_DIR.

    Returns:
        Tuple[int, str, str]: (returncode, stdout, stderr) from rclone operation
    """
    if not (config.RCLONE_REMOTE and config.RCLONE_SRC):
        return 2, "", "RCLONE_REMOTE/RCLONE_SRC not configured"
    src = f"{config.RCLONE_REMOTE}:{config.RCLONE_SRC}"
    dst = config.SYNC_DIR
    return run_rclone_sync(src, dst)


def sync_synaptic_from_remote() -> Tuple[int, str, str]:
    """
    Sync Synaptic Hub data from remote cloud storage to local directory.

    Why: Downloads synaptic data files from cloud to maintain local knowledge
         base consistency and enable offline processing capabilities.
    Where: Used by background sync processes and manual sync operations.
    How: Leverages rclone to transfer from RCLONE_REMOTE:RCLONE_DST to local
         SYNAPTIC_HUB_DIR with configured transfer parameters.

    Returns:
        Tuple[int, str, str]: (returncode, stdout, stderr) from rclone sync
    """
    if not (config.RCLONE_REMOTE and config.RCLONE_DST):
        return 2, "", "RCLONE_REMOTE/RCLONE_DST not configured"
    src = f"{config.RCLONE_REMOTE}:{config.RCLONE_DST}"
    dst = config.SYNAPTIC_HUB_DIR
    return run_rclone_sync(src, dst)
