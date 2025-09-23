"""
Auto Code Cleaner for Python Projects

Why: Automates detection and correction of common syntax/indentation errors, stray SQL, and merge markers in Python files.
Where: Run in project root to scan/fix all .py files.
How: Scans files, applies regex-based fixes, and outputs a report or auto-fixes issues.

Usage:
    python auto_code_cleaner.py [--fix]
    # --fix: actually applies fixes, otherwise just reports

Connects to:
    - None: This is a standalone utility script.
"""

import os
import re
import sys
from pathlib import Path

PYTHON_FILE_PATTERN = re.compile(r".*\.py$")
SQL_PATTERN = re.compile(
    r"^(\s*)(CREATE|ALTER|INSERT|SELECT|UPDATE|DELETE)\s+TABLE", re.IGNORECASE
)
MERGE_MARKER_PATTERN = re.compile(r"^(<<<<<<<|=======|>>>>>>>)")

INDENT_ERROR_PATTERN = re.compile(r"^\s+[^\s].*")

REPORT = []


def scan_file(path: Path, fix: bool = False):
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    new_lines = []
    changed = False
    for i, line in enumerate(lines):
        # Remove merge conflict markers
        if MERGE_MARKER_PATTERN.match(line):
            REPORT.append(f"{path}: Merge marker at line {i+1}")
            changed = True
            continue
        # Remove stray SQL outside triple quotes
        if SQL_PATTERN.match(line):
            # Only keep if inside triple quotes
            prev = lines[i - 1] if i > 0 else ""
            next = lines[i + 1] if i + 1 < len(lines) else ""
            if not (prev.strip().startswith('"""') or next.strip().endswith('"""')):
                REPORT.append(f"{path}: Stray SQL at line {i+1}")
                changed = True
                continue
        new_lines.append(line)
    # Indentation error detection (simple)
    for i, line in enumerate(new_lines):
        if line.startswith("    ") and line.lstrip().startswith("def "):
            # Function should not be indented unless inside a class
            prev = new_lines[i - 1] if i > 0 else ""
            if not prev.strip().startswith("class "):
                REPORT.append(f"{path}: Possible indentation error at line {i+1}")
                changed = True
    if changed and fix:
        with path.open("w", encoding="utf-8") as f:
            f.writelines(new_lines)


def main():
    fix = "--fix" in sys.argv
    root = Path(os.getcwd())
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if PYTHON_FILE_PATTERN.match(fname):
                scan_file(Path(dirpath) / fname, fix=fix)
    print("\nAuto Code Cleaner Report:")
    for entry in REPORT:
        print(entry)
    if fix:
        print("\nFixes applied where possible.")
    else:
        print("\nRun with --fix to apply fixes.")


if __name__ == "__main__":
    main()
