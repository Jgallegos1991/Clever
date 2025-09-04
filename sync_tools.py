from __future__ import annotations

import subprocess
from typing import List, Tuple

import config


def run_rclone_sync(src: str, dst: str, extra: str | None = None) -> Tuple[int, str, str]:
    """Run rclone sync and return (returncode, stdout, stderr)."""
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
    if not (config.RCLONE_REMOTE and config.RCLONE_SRC):
        return 2, "", "RCLONE_REMOTE/RCLONE_SRC not configured"
    src = f"{config.RCLONE_REMOTE}:{config.RCLONE_SRC}"
    dst = config.SYNC_DIR
    return run_rclone_sync(src, dst)


def sync_synaptic_from_remote() -> Tuple[int, str, str]:
    if not (config.RCLONE_REMOTE and config.RCLONE_DST):
        return 2, "", "RCLONE_REMOTE/RCLONE_DST not configured"
    src = f"{config.RCLONE_REMOTE}:{config.RCLONE_DST}"
    dst = config.SYNAPTIC_HUB_DIR
    return run_rclone_sync(src, dst)
