"""
File Inventory Generator

Why: To automatically create a markdown file (`file-inventory.md`) that provides
     a statistical overview of the project's files. This helps in understanding
     the project's composition, such as which file types are most common.
Where: This is a standalone utility script, typically run from the command line
       or via a `make` command (`make file-inventory`). It is not imported by
       other parts of the Clever application.
How: It walks through the project directory, collects statistics (count, lines of
     code, size) for each file extension, and gets the last modification date for
     each file. It then formats this information into a markdown table and writes
     it to `file-inventory.md`.

Connects to:
    - (None): This script is self-contained and does not import or interact with other custom modules from the Clever project.
"""

import os
import pathlib
import datetime
from collections import defaultdict

REPO_ROOT = pathlib.Path(__file__).parent.parent
INVENTORY_PATH = REPO_ROOT / "file-inventory.md"


def get_file_stats():
    """Collect file extension stats: count, lines of code, and size."""
    """
    Collect comprehensive file extension statistics across repository.
    
    Why: Provides insights into project composition and file distribution
         for documentation and project analysis purposes.
    Where: Called by inventory generation to build statistical overview
           of repository contents and file type distribution.
    How: Walks directory tree, categorizes files by extension, counts
         files and lines, measures sizes with error handling for access issues.
         
    Returns:
        defaultdict: Statistics dict with count, LOC, and size per extension
    """
    stats = defaultdict(lambda: {"count": 0, "loc": 0, "size": 0})
    for root, dirs, files in os.walk(REPO_ROOT):
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = pathlib.Path(fname).suffix.lstrip(".") or "other"
            try:
                size = os.path.getsize(fpath)
                with open(fpath, "rb") as f:
                    lines = sum(1 for _ in f)
            except Exception:
                size = 0
                lines = 0
                raise  # Re-raise to maintain visibility of errors
            stats[ext]["count"] += 1
            stats[ext]["loc"] += lines
            stats[ext]["size"] += size
    return stats


def get_last_modified():
    """Get last modified date for each file."""
    """
    Extract last modification timestamps for all repository files.
    
    Why: Tracks file activity and recent changes for project maintenance
         and development activity analysis across repository contents.
    Where: Used by inventory generation to identify recently modified
           files and provide development activity insights.
    How: Walks file system, extracts modification times, converts to
         ISO format with graceful error handling for inaccessible files.
         
    Returns:
        dict: Mapping of file paths to ISO-formatted modification timestamps
    """
    mod_dates = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                mtime = os.path.getmtime(fpath)
                mod_dates[fpath] = datetime.datetime.fromtimestamp(mtime).isoformat()
            except Exception:
                mod_dates[fpath] = "N/A"
                raise  # Re-raise to maintain error visibility
    return mod_dates


def generate_inventory():
    """Generate markdown file inventory."""
    """
    Generate comprehensive markdown file inventory report for repository.
    
    Why: Creates automated documentation of project structure and file
         composition for development reference and project analysis.
    Where: Main function called to produce file-inventory.md documentation
           used by development team and project management processes.
    How: Combines file statistics and modification data, formats as markdown
         table, writes to inventory file with timestamp and structured sections.
    """
    stats = get_file_stats()
    mod_dates = get_last_modified()
    lines = [
        "# File Inventory (Auto-Generated)",
        "",
        f"_Generated: {datetime.datetime.now().isoformat()}_",
        "",
    ]
    lines.append("| Extension | Count | Total LOC | Total Size (bytes) |")
    lines.append("|-----------|-------|-----------|--------------------|")
    for ext, data in sorted(stats.items(), key=lambda x: -x[1]["count"]):
        lines.append(f"| {ext} | {data['count']} | {data['loc']} | {data['size']} |")
    lines.append("")
    lines.append("## Last Modified Dates (Top 20 files)")
    top_mod = sorted(mod_dates.items(), key=lambda x: x[1], reverse=True)[:20]
    for fpath, mdate in top_mod:
        rel_path = os.path.relpath(fpath, REPO_ROOT)
        lines.append(f"- `{rel_path}`: {mdate}")
    with open(INVENTORY_PATH, "w") as f:
        f.write("\n".join(lines))
    print(f"Inventory written to {INVENTORY_PATH}")


if __name__ == "__main__":
    generate_inventory()
