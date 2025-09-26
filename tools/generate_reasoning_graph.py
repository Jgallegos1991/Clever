"""
generate_reasoning_graph.py - Generate reasoning graph markdown from Why/Where/How + Connects to tokens

Why: Transform distributed docstring reasoning metadata into a visualizable
knowledge map so engineers can traverse Clever's architecture via declared
edges instead of grep. This reinforces the "arrows between dots" paradigm
and provides an auditable artifact (`docs/reasoning_graph.md`) that CI or
humans can diff to spot architectural drift. Essential for maintaining
Clever's cognitive partnership system architecture and interconnection mapping.

Where: Run manually (`python -m tools.generate_reasoning_graph`) or wired into
future CI documentation jobs. Consumes in‑repo Python source only (offline).
Part of Clever's development toolkit for architectural analysis and documentation.

How: Walks the repository for `*.py` files (excluding venv/site-packages),
parses AST for module/class/function docstrings, extracts Why/Where/How and
"Connects to" adjacency declarations, and emits a Markdown file summarizing:
  1. Coverage stats  2. Node inventory with condensed Why line
  3. Edge list (source → targets)  4. Orphan detection (nodes without outgoing edges)

File Usage:
    - Architecture analysis: Primary tool for generating system interconnection graphs
    - Documentation generation: Creates comprehensive reasoning graph documentation
    - CI/CD integration: Used in automated documentation validation and generation
    - Development workflow: Run during architectural changes to update system maps
    - Debugging support: Helps visualize system relationships during troubleshooting
    - Code review: Generated graphs used to assess architectural impact of changes
    - Onboarding: Creates visual system maps for new developer orientation
    - Quality assurance: Validates documentation completeness and system coherence

Connects to:
    - tools/verify_reasoning_docs.py: Relies on same documentation discipline and standards
    - introspection.py: Runtime surfacing complement to static architectural graph
    - docs/reasoning_graph.md: Output artifact containing comprehensive system map
    - .github/copilot-instructions.md: Documentation standards this tool validates and enforces
    - tools/docstring_enforcer.py: Complementary documentation enforcement tooling
    - All Python modules: Source files analyzed for Why/Where/How and Connects to metadata
    - CI/CD workflows: Integration with automated documentation generation processes
    - app.py: Core application architecture mapped and analyzed
    - persona.py: Personality engine connections documented and graphed
    - evolution_engine.py: Learning system relationships mapped and tracked
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / 'docs' / 'reasoning_graph.md'
REMEDIATION_PATH = REPO_ROOT / 'docs' / 'reasoning_remediation.md'
BADGE_PATH = REPO_ROOT / 'docs' / 'reasoning_coverage_badge.svg'
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
    # name_map previously used for validation; retained logic simplified (unused)
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


def build_remediation(nodes: List[Node]) -> str:
    """Build remediation markdown listing nodes missing Why/Where/How.

    Why: Provide an actionable, sorted backlog so maintainers can rapidly
    raise reasoning coverage by fixing the highest value gaps first.
    Where: Generated alongside the main reasoning graph artifact; consumed
    by engineers & CI review to plan docstring improvements.
    How: Filter nodes missing at least one token, group by file, sort by
    descending count, and emit bullet lists with line references.
    """
    missing = [n for n in nodes if not (n.why and n.where and n.how)]
    if not missing:
        return ("# Reasoning Remediation Backlog\n\n"  # pragma: no cover - trivial
                "All nodes have complete Why/Where/How coverage. \n")
    # Group by file
    grouped: Dict[Path, List[Node]] = {}
    for n in missing:
        grouped.setdefault(n.file, []).append(n)
    # Sort groups by number of missing descending
    ordered = sorted(grouped.items(), key=lambda kv: len(kv[1]), reverse=True)
    lines: List[str] = []
    lines.append('# Reasoning Remediation Backlog')
    lines.append('')
    lines.append('Priority ordered by outstanding nodes per file (high → low).')
    lines.append('')
    total_missing = len(missing)
    lines.append(f'Total incomplete nodes: {total_missing}')
    lines.append('')
    for path, nodes_list in ordered:
        rel = path.relative_to(REPO_ROOT)
        lines.append(f'## {rel} ({len(nodes_list)} incomplete)')
        lines.append('')
        for n in sorted(nodes_list, key=lambda x: (x.lineno, x.kind, x.name)):
            missing_parts = [p for p, v in (('Why', n.why), ('Where', n.where), ('How', n.how)) if not v]
            parts_str = '/'.join(missing_parts)
            lines.append(f'- {n.kind} `{n.name}` (line {n.lineno}) – missing {parts_str}')
        lines.append('')
    return '\n'.join(lines) + '\n'


def generate_badge(coverage_pct: float) -> str:
    """Return simple SVG badge string representing reasoning coverage.

    Why: Provides at-a-glance visual indicator in README and PR diffs to
    incentivize continual improvement of reasoning docs.
    Where: Saved to docs/reasoning_coverage_badge.svg and referenced from
    README.md near top section.
    How: Minimal handcrafted SVG (no external deps) with dynamic width and
    color gradient based on percentage thresholds.
    """
    pct_text = f"{coverage_pct:.1f}%"
    # Color thresholds (red < 50, amber < 75, green otherwise)
    if coverage_pct < 50:
        color = '#d9534f'
    elif coverage_pct < 75:
        color = '#f0ad4e'
    else:
        color = '#5cb85c'
    label = 'reasoning'
    # Basic width estimation (approx 8px per char + padding)
    label_w = 8 * len(label) + 20
    pct_w = 8 * len(pct_text) + 20
    total_w = label_w + pct_w
    label_mid = label_w / 2
    pct_mid = label_w + pct_w / 2
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{total_w}' height='20' role='img' aria-label='{label}: {pct_text}'>\n  <linearGradient id='g' x2='0' y2='100%'>\n    <stop offset='0' stop-color='#fff' stop-opacity='.7'/>\n    <stop offset='1' stop-opacity='.7'/>\n  </linearGradient>\n  <rect rx='3' width='{total_w}' height='20' fill='#555'/>\n  <rect rx='3' x='{label_w}' width='{pct_w}' height='20' fill='{color}'/>\n  <rect rx='3' width='{total_w}' height='20' fill='url(#g)'/>\n  <g fill='#fff' text-anchor='middle' font-family='DejaVu Sans,Verdana,Geneva,sans-serif' font-size='11'>\n    <text x='{label_mid}' y='14'>{label}</text>\n    <text x='{pct_mid}' y='14'>{pct_text}</text>\n  </g>\n</svg>\n"""


def run(args: Optional[argparse.Namespace] = None) -> float:
    """Core execution function returning coverage percentage.

    Why: Allows reuse from CLI and potential future programmatic imports.
    Where: Invoked by main() and could be called in CI steps.
    How: Builds nodes, writes graph, optional remediation & badge, enforces
    threshold if provided via arguments.
    """
    nodes = build_nodes()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    markdown = generate_markdown(nodes)
    OUTPUT_PATH.write_text(markdown, encoding='utf-8')
    # Extract coverage from header line
    first_lines = markdown.splitlines()
    coverage_pct = 0.0
    for line in first_lines:
        if line.startswith('Total nodes:'):
            # parse trailing (...) percentage
            import re as _re
            m = _re.search(r'\((\d+\.\d+)%\)', line)
            if m:
                coverage_pct = float(m.group(1))
            break
    if args and args.remediation:
        REMEDIATION_PATH.write_text(build_remediation(nodes), encoding='utf-8')
    if args and args.badge:
        BADGE_PATH.write_text(generate_badge(coverage_pct), encoding='utf-8')
    if args and args.fail_under is not None and coverage_pct < args.fail_under:
        print(f"Coverage {coverage_pct:.2f}% below threshold {args.fail_under:.2f}%", file=sys.stderr)
        return coverage_pct
    print(f"Generated reasoning graph markdown at {OUTPUT_PATH} (coverage {coverage_pct:.2f}%)")
    return coverage_pct


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate Clever reasoning graph and optional remediation list.')
    parser.add_argument('--remediation', action='store_true', help='Also generate remediation backlog markdown.')
    parser.add_argument('--badge', action='store_true', help='Generate SVG badge for reasoning coverage.')
    parser.add_argument('--fail-under', type=float, default=None, help='If provided, exits non-zero when coverage below this percent.')
    ns = parser.parse_args()
    coverage = run(ns)
    if ns.fail_under is not None and coverage < ns.fail_under:
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
