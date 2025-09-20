"""Generate reasoning graph markdown from Why/Where/How + Connects to tokens.

Why: Transform distributed docstring reasoning metadata into a visualizable
knowledge map so engineers can traverse Clever's architecture via declared
edges instead of grep. This reinforces the "arrows between dots" paradigm
and provides an auditable artifact (`docs/reasoning_graph.md`) that CI or
humans can diff to spot architectural drift.
Where: Run manually (`python -m tools.generate_reasoning_graph`) or wired into
future CI documentation jobs. Consumes in‑repo Python source only (offline).
How: Walks the repository for `*.py` files (excluding venv/site-packages),
parses AST for module/class/function docstrings, extracts Why/Where/How and
"Connects to" adjacency declarations, and emits a Markdown file summarizing:
  1. Coverage stats
  2. Node inventory with condensed Why line
  3. Edge list (source → targets)
  4. Orphan detection (nodes without outgoing edges)

Connects to:
    - tools/verify_reasoning_docs.py: Relies on same doc discipline
    - introspection.py: Runtime surfacing complement to static graph
    - docs/reasoning_graph.md: Output artifact
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / 'docs' / 'reasoning_graph.md'
TOKEN_KEYS = ('Why:', 'Where:', 'How:')
CONNECTS_HEADER = 'Connects to:'

@dataclass
class Node:
    kind: str  # module|class|function
    name: str
    file: Path
    lineno: int
    why: str
    where: str
    how: str
    connects: List[str]


def extract_sections(doc: str) -> Tuple[str, str, str, List[str]]:
    """Parse Why/Where/How + Connects to lines from a docstring.

    Why: Central parser to keep semantics consistent with enforcement & graph.
    Where: Used for every object with a docstring.
    How: Line scanning with state flags (simple & robust without heavy parsing).
    """
    if not doc:
        return '', '', '', []
    why_lines: List[str] = []
    where_lines: List[str] = []
    how_lines: List[str] = []
    connects: List[str] = []
    current = None
    in_connects = False
    for raw in doc.splitlines():
        line = raw.rstrip()
        low = line.lower().strip()
        if low.startswith('why:'):
            current = 'why'; in_connects = False
            why_lines.append(line.split(':', 1)[1].strip())
            continue
        if low.startswith('where:'):
            current = 'where'; in_connects = False
            where_lines.append(line.split(':', 1)[1].strip())
            continue
        if low.startswith('how:'):
            current = 'how'; in_connects = False
            how_lines.append(line.split(':', 1)[1].strip())
            continue
        if line.strip().startswith(CONNECTS_HEADER):
            in_connects = True; current = None
            continue
        if in_connects:
            # expect bullet list lines beginning with '-'
            if line.strip().startswith('-'):
                target = line.strip()[1:].strip()
                if target:
                    # sanitize target to first token before spaces/colon
                    connects.append(target)
                continue
            # blank line ends connects section
            if not line.strip():
                in_connects = False
        else:
            if current == 'why' and line.strip():
                why_lines.append(line.strip())
            elif current == 'where' and line.strip():
                where_lines.append(line.strip())
            elif current == 'how' and line.strip():
                how_lines.append(line.strip())
    return (' '.join(why_lines).strip(),
            ' '.join(where_lines).strip(),
            ' '.join(how_lines).strip(), connects)


def scan_python_files() -> List[Path]:
    return [p for p in REPO_ROOT.rglob('*.py')
            if not any(seg in p.parts for seg in ('.venv', 'venv', 'site-packages', 'build', 'dist', '__pycache__'))]


def build_nodes() -> List[Node]:
    nodes: List[Node] = []
    for path in scan_python_files():
        try:
            src = path.read_text(encoding='utf-8')
        except Exception:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        mod_doc = ast.get_docstring(tree) or ''
        why, where, how, connects = extract_sections(mod_doc)
        nodes.append(Node('module', path.stem, path, 1, why, where, how, connects))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node) or ''
                w, wher, h, cts = extract_sections(doc)
                nodes.append(Node('class', node.name, path, getattr(node, 'lineno', 1), w, wher, h, cts))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node) or ''
                w, wher, h, cts = extract_sections(doc)
                nodes.append(Node('function', node.name, path, getattr(node, 'lineno', 1), w, wher, h, cts))
    return nodes


def generate_markdown(nodes: List[Node]) -> str:
    total = len(nodes)
    with_tokens = sum(1 for n in nodes if n.why and n.where and n.how)
    coverage_pct = (with_tokens / total * 100.0) if total else 100.0
    # Build adjacency
    edges: List[Tuple[str, str]] = []
    name_map = {f"{n.file.stem}:{n.name}" for n in nodes}
    for n in nodes:
        for tgt in n.connects:
            # Remove trailing punctuation and split off inline description
            cleaned = re.split(r'[\s:]', tgt, 1)[0]
            if cleaned:
                edges.append((f"{n.file.stem}:{n.name}", cleaned))
    out: List[str] = []
    out.append('# Clever Reasoning Graph')
    out.append('')
    out.append(f'Total nodes: {total}  |  Complete Why/Where/How: {with_tokens} ({coverage_pct:.2f}%)')
    out.append('')
    out.append('## Nodes')
    out.append('')
    for n in sorted(nodes, key=lambda x: (x.file.stem, n.kind, n.name)):
        short_why = (n.why[:140] + '…') if len(n.why) > 140 else n.why
        out.append(f"- **{n.file.stem}:{n.name}** ({n.kind}) – {short_why or 'No Why'}")
    out.append('')
    out.append('## Edges (Source → Target)')
    out.append('')
    if edges:
        for s, t in sorted(edges):
            out.append(f"- {s} → {t}")
    else:
        out.append('_No edges declared in Connects to sections._')
    out.append('')
    # Orphans = nodes without outgoing edges
    sources = {s for s, _ in edges}
    orphans = [n for n in nodes if f"{n.file.stem}:{n.name}" not in sources]
    out.append('## Orphan Nodes (no outgoing Connects)')
    out.append('')
    if orphans:
        for n in sorted(orphans, key=lambda x: (x.file.stem, n.name)):
            out.append(f"- {n.file.stem}:{n.name}")
    else:
        out.append('None')
    out.append('\n')
    return '\n'.join(out)


def main() -> int:
    nodes = build_nodes()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(generate_markdown(nodes), encoding='utf-8')
    print(f"Generated reasoning graph markdown at {OUTPUT_PATH}")
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
