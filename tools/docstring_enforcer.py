"""
Docstring Enforcement Utility

Why: Enforces documentation standard requiring Why/Where/How presence for each significant Python file to improve maintainability and architectural clarity.
Where: Operates across the repository, scanning `.py` files excluding virtual environments, caches, and tests optionally.
How: For each file, if it contains one or more function or class definitions, we ensure at least one occurrence each of 'Why:', 'Where:', and 'How:' within the file.

Connects to:
    - CI (`clever-ci.yml`) can invoke this for a stricter (failing) mode
    - Developer workflow: run locally before committing for compliance
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable, List, Tuple

EXCLUDE_DIRS = {".venv", "venv", "__pycache__", ".git", "home"}
OPTIONAL_EXCLUDE = {"tests"}
REQUIRED_TOKENS = ["Why:", "Where:", "How:"]


def iter_python_files(root: pathlib.Path, include_tests: bool) -> Iterable[pathlib.Path]:
    """
    Iterate through python files honoring exclusion rules.

    Why: Centralizes traversal logic to ensure consistent filtering in enforcement.
    Where: Used by main() when building list of candidate files.
    How: Walk directory tree; skip excluded directories; optionally skip tests.

    Connects to:
        - docstring pattern enforcement pipeline
    """
    for path in root.rglob("*.py"):
        # Use relative parts so that system path prefixes (e.g. /home/username) do not
        # trigger exclusions erroneously. This allows us to intentionally exclude a
        # nested duplicate project directory named 'home' inside the repo while still
        # scanning the actual root files located at /home/username/... on disk.
        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:  # pragma: no cover - should not happen but safe guard
            rel_parts = path.parts
        rel_set = set(rel_parts)
        if rel_set & EXCLUDE_DIRS:
            continue
        if "site-packages" in rel_set:
            continue
        if not include_tests and "tests" in rel_set:
            continue
        yield path


def scan_file(path: pathlib.Path) -> Tuple[bool, List[str]]:
    """
    Scan a single file for required documentation tokens.

    Why: Provides atomic evaluation to allow future parallelization.
    Where: Called by the aggregation loop in main().
    How: Read text once; check for presence of each token; collect missing tokens.

    Connects to:
        - iter_python_files(): supplies file list
        - CI reporting consumer
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:  # pragma: no cover - rare filesystem edge
        return False, [f"read_error: {e}"]
    missing = [t for t in REQUIRED_TOKENS if t not in text]
    return (len(missing) == 0), missing


def main(argv: list[str]) -> int:
    """
    CLI entrypoint.

    Why: Offers developers and CI a single executable interface.
    Where: Invoked manually or via CI step for stricter enforcement than current non-blocking grep.
    How: Parse args, iterate files, compute coverage %, emit report; optionally fail if below threshold or any missing.

    Connects to:
        - clever-ci.yml (future enhancement: replace ad-hoc grep step)
    """
    parser = argparse.ArgumentParser(description="Docstring Why/Where/How enforcement")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--include-tests", action="store_true", help="Also enforce within tests")
    parser.add_argument("--fail-on-missing", action="store_true", help="Exit non-zero if any file missing tokens")
    parser.add_argument("--min-coverage", type=float, default=0.0, help="Minimum ratio (0-1) of compliant files required")
    args = parser.parse_args(argv)

    files = list(iter_python_files(args.root.resolve(), include_tests=args.include_tests))
    total = len(files)
    compliant = 0
    failures: list[str] = []

    for f in files:
        ok, missing = scan_file(f)
        if ok:
            compliant += 1
        else:
            failures.append(f"{f}: missing {', '.join(missing)}")

    _coverage = compliant / total if total else 1.0

    # Why: Simpler static string; removed unused f-string placeholder for lint cleanliness
    print("Docstring Enforcement Report")
    print(f"Total files scanned: {total}")
    print(f"Compliant files: {compliant}")
    print(f"Coverage: {coverage:.2%}")

    if failures:
        print("\nNon-compliant files:")
        for line in failures:
            print(f" - {line}")

    if args.fail_on_missing and failures:
        return 2
    if coverage < args.min_coverage:
        return 3
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
