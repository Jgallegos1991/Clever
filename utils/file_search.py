"""Local file search utility (offline, safe, single-root).

Why: Allow PersonaEngine to fulfill user intents like "find all python files
with memory in the name" or "locate pdf docs" by performing on-disk searches
within the project root only—aligning capability with responses.
Where: Invoked indirectly from PersonaEngine when detecting file search intent.
How: Provides search_files(patterns, max_results) supporting glob-style
patterns and simple substring filters. Enforces root confinement and ignores
venv, git, and large binary directories.

Connects to:
  - persona.py: Intent detection logic will call search_files
  - app.py: User queries routed through PersonaEngine
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IGNORE_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', 'logs', 'site-packages'}
MAX_DEFAULT_RESULTS = 50


def _iter_candidate_files(root: Path) -> Iterable[Path]:
    """Yield candidate files under root respecting ignore list.

    Why: Centralize traversal to ensure every higher-level search obeys
    safety and filtering rules.
    Where: Used by search_files() for enumeration.
    How: Walk with rglob but skip ignored directories early.
    """
    for p in root.rglob('*'):
        # Skip anything inside ignored directories (any segment)
        if any(seg in IGNORE_DIRS for seg in p.parts):
            continue
        if p.is_dir():
            continue  # We only yield files
        # Skip very large files (>5MB) for responsiveness
        try:
            if p.stat().st_size > 5 * 1024 * 1024:
                continue
        except OSError:
            continue
        yield p


def search_files(patterns: List[str], max_results: int = MAX_DEFAULT_RESULTS) -> List[str]:
    """Search project for files matching any of the provided patterns.

    Why: Bridge user natural language requests for locating files with
    deterministic local search—enabling the assistant to *do* what it says.
    Where: Called by PersonaEngine once an intent like "find"+extension or
    "locate"+keyword is detected.
    How: For each file path, apply simple matching rules:
         - Glob-like wildcard translation (*)
         - Case-insensitive substring presence for plain tokens
    Returns sorted unique path strings (relative to project root).

    Args:
        patterns: List of user-derived search tokens or wildcard patterns.
        max_results: Upper bound on results returned.

    Returns:
        List of relative file paths.

    Connects to:
        - persona.py: Intent detection will format patterns from user query.
    """
    norm_patterns = [p.strip().lower() for p in patterns if p.strip()]
    if not norm_patterns:
        return []
    results: List[str] = []
    seen = set()
    for path in _iter_candidate_files(PROJECT_ROOT):
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        name_lower = rel.lower()
        for pat in norm_patterns:
            # Simple wildcard support: treat '*' as 'contains'
            if pat == '*':
                match = True
            elif '*' in pat:
                segments = [s for s in pat.split('*') if s]
                match = all(seg in name_lower for seg in segments)
            else:
                match = pat in name_lower
            if match:
                if rel not in seen:
                    seen.add(rel)
                    results.append(rel)
                break
        if len(results) >= max_results:
            break
    return sorted(results)


def search_by_extension(ext: str, max_results: int = MAX_DEFAULT_RESULTS) -> List[str]:
    """Shortcut to search by file extension (case-insensitive).

    Why: Common user queries revolve around extension classes ("find all .py files").
    Where: Called by PersonaEngine when parsing queries for extension filter.
    How: Enumerates candidates and matches suffix ignoring case.
    """
    e = ext.lower().lstrip('.')
    matches = []
    for p in _iter_candidate_files(PROJECT_ROOT):
        if p.suffix.lower().lstrip('.') == e:
            matches.append(p.relative_to(PROJECT_ROOT).as_posix())
            if len(matches) >= max_results:
                break
    return matches


__all__ = [
    'search_files',
    'search_by_extension'
]
