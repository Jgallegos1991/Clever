import os
import pathlib
import datetime
from collections import defaultdict

REPO_ROOT = pathlib.Path(__file__).parent.parent
INVENTORY_PATH = REPO_ROOT / "file-inventory.md"


def get_file_stats():
    """Collect file extension stats: count, lines of code, and size."""
    stats = defaultdict(lambda: {'count': 0, 'loc': 0, 'size': 0})
    for root, dirs, files in os.walk(REPO_ROOT):
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = pathlib.Path(fname).suffix.lstrip('.') or 'other'
            try:
                size = os.path.getsize(fpath)
                with open(fpath, 'rb') as f:
                    lines = sum(1 for _ in f)
            except Exception:
                size = 0
                lines = 0
            stats[ext]['count'] += 1
            stats[ext]['loc'] += lines
            stats[ext]['size'] += size
    return stats


def get_last_modified():
    """Get last modified date for each file."""
    mod_dates = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                mtime = os.path.getmtime(fpath)
                mod_dates[fpath] = datetime.datetime.fromtimestamp(
                    mtime
                ).isoformat()
            except Exception:
                mod_dates[fpath] = 'N/A'
    return mod_dates


def generate_inventory():
    """Generate markdown file inventory."""
    stats = get_file_stats()
    mod_dates = get_last_modified()
    lines = [
        "# File Inventory (Auto-Generated)",
        "",
        f"_Generated: {datetime.datetime.now().isoformat()}_",
        ""
    ]
    lines.append("| Extension | Count | Total LOC | Total Size (bytes) |")
    lines.append("|-----------|-------|-----------|--------------------|")
    for ext, data in sorted(stats.items(), key=lambda x: -x[1]['count']):
        lines.append(
            f"| {ext} | {data['count']} | {data['loc']} | {data['size']} |"
        )
    lines.append("")
    lines.append("## Last Modified Dates (Top 20 files)")
    top_mod = sorted(mod_dates.items(), key=lambda x: x[1], reverse=True)[:20]
    for fpath, mdate in top_mod:
        rel_path = os.path.relpath(fpath, REPO_ROOT)
        lines.append(f"- `{rel_path}`: {mdate}")
    with open(INVENTORY_PATH, "w") as f:
        f.write('\n'.join(lines))
    print(f"Inventory written to {INVENTORY_PATH}")


if __name__ == "__main__":
    generate_inventory()
