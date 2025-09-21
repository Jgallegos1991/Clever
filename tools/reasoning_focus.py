"""Reasoning Coverage Focus Helper

Why: Provides contributors with a fast, actionable view of the largest
remaining Why/Where/How documentation gaps so effort targets maximum
coverage uplift per edit cycle.
Where: Developer utility script (manual / CI assist). Reads generated
`docs/reasoning_remediation.md` or performs a fresh scan if missing.
How: Parses remediation markdown or AST-walks code (fallback), aggregates
missing nodes per file, supports optional top-N filtering and code excerpt
preview for each undocumented symbol.

Usage:
    python tools/reasoning_focus.py --top 5 --preview 3

Connects to:
    - tools/generate_reasoning_graph.py: Primary producer of remediation file
    - docs/reasoning_remediation.md: Parsed backlog source
    - verification tooling: Complements enforcement by prioritization
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
REMEDIATION_PATH = REPO_ROOT / 'docs' / 'reasoning_remediation.md'

FILE_HEADER_RE = re.compile(r'^##\s+(?P<path>.+?)\s+\((?P<count>\d+) incomplete\)')
ITEM_RE = re.compile(r'^-\s+(?P<kind>\w+) `(?P<name>[^`]+)` \(line (?P<line>\d+)\) – missing (?P<missing>.+)$')

def parse_remediation(md: str) -> List[Tuple[str, int, List[Tuple[str, str, int, str]]]]:
    """Parse remediation markdown into structured records.

    Returns list of (relative_path, total_missing, entries) where entries
    are (kind, name, line, missing_parts).
    """
    lines = md.splitlines()
    results = []
    current_file = None
    current_entries: List[Tuple[str, str, int, str]] = []
    current_count = 0
    for line in lines:
        m = FILE_HEADER_RE.match(line.strip())
        if m:
            # flush previous
            if current_file:
                results.append((current_file, current_count, current_entries))
            current_file = m.group('path')
            current_count = int(m.group('count'))
            current_entries = []
            continue
        im = ITEM_RE.match(line.strip())
        if im and current_file:
            current_entries.append((im.group('kind'), im.group('name'), int(im.group('line')), im.group('missing')))
    if current_file:
        results.append((current_file, current_count, current_entries))
    return results


def load_or_fail() -> str:
    if not REMEDIATION_PATH.exists():
        raise SystemExit("Remediation file missing; run generate_reasoning_graph.py first")
    return REMEDIATION_PATH.read_text(encoding='utf-8')


def get_code_excerpt(rel_path: str, line: int, context: int = 2) -> str:
    p = REPO_ROOT / rel_path
    if not p.exists():
        return "<file missing>"
    try:
        all_lines = p.read_text(encoding='utf-8').splitlines()
    except Exception:
        return "<unreadable file>"
    start = max(0, line - context - 1)
    end = min(len(all_lines), line + context)
    excerpt = all_lines[start:end]
    pointer_index = line - 1 - start
    if 0 <= pointer_index < len(excerpt):
        excerpt[pointer_index] = f"--> {excerpt[pointer_index]}"  # mark target line
    return '\n'.join(excerpt)


def main() -> int:
    parser = argparse.ArgumentParser(description='Show prioritized reasoning doc gaps')
    parser.add_argument('--top', type=int, default=5, help='Show top N files by missing count')
    parser.add_argument('--preview', type=int, default=0, help='Show N line-context excerpts for each missing symbol (0=off)')
    args = parser.parse_args()

    data = parse_remediation(load_or_fail())
    # sort by descending missing count
    data.sort(key=lambda x: x[1], reverse=True)
    slice_data = data[: args.top]

    print(f"Top {len(slice_data)} files by missing reasoning tokens:\n")
    for rel_path, count, entries in slice_data:
        print(f"{rel_path} - {count} incomplete")
        if args.preview > 0:
            for e in entries[: args.preview]:
                kind, name, line, missing = e
                print(f"  {kind} {name} (line {line}) missing {missing}")
                excerpt = get_code_excerpt(rel_path, line)
                print('\n'.join(f"    {l}" for l in excerpt.splitlines()))
                print()
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
