"""Why/Where/How Enforcement Script (Pre-Commit Friendly)

Why: Enforce the Clever reasoning documentation contract so every new or
modified Python artifact preserves the "arrows between dots" (Why → Where →
How). Failing fast at commit time keeps the runtime introspection graph
complete, enabling the domino effect of instant traceability and safer
refactors.
Where: Invoked via the optional Git pre-commit hook (see
`tools/install_hooks.sh`) or manually (`python tools/verify_reasoning_docs.py`).
How: Collects staged Python files (unless explicit paths provided), parses
them with `ast` to examine module, class, and function docstrings, and
verifies presence of all three tokens (case‑insensitive). Emits a concise
error report and exits non‑zero on violations.

Connects to:
    - .github/copilot-instructions.md: Rationale for Why/Where/How arrows
    - introspection.py: Runtime surfacing of reasoning metadata
    - tools/runtime_dump.py: CLI snapshot relying on intact arrows
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Iterable

REQUIRED_TOKENS = ("why:", "where:", "how:")  # lower-case match
SKIP_MARKER = "reasoning-skip"  # place '# reasoning-skip' in file to bypass


def _debug(msg: str) -> None:
    if '--verbose' in sys.argv:
        print(f"[verify] {msg}")


def gather_staged_python_files() -> List[Path]:
    """Return list of staged Python files (Added, Copied, Modified).

    Why: Scope enforcement to changed code only for fast commits.
    Where: Called when script invoked with no explicit path arguments.
    How: Uses `git diff --cached --name-only --diff-filter=ACM` and filters
    for `.py` suffix excluding virtual env / site-packages noise.
    """
    try:
        out = subprocess.check_output([
            'git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'
        ], text=True)
    except Exception:
        return []
    files = []
    for line in out.splitlines():
        p = Path(line.strip())
        if p.suffix == '.py' and not any(seg in p.parts for seg in ('.venv', 'venv', 'site-packages')):
            if p.exists():
                files.append(p)
    return files


def extract_docstring_nodes(tree: ast.AST) -> Iterable[Tuple[str, ast.AST, str]]:
    """Yield (kind, node, docstring) for module, classes, and functions.

    Why: Centralize traversal so enforcement uniformly evaluates objects.
    Where: Used by `analyze_file` for per file reasoning coverage.
    How: Gets module docstring, then walks AST for class & function nodes.
    """
    # Module docstring
    mod_doc = ast.get_docstring(tree) or ""
    yield ("module", tree, mod_doc)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield ("function", node, ast.get_docstring(node) or "")
        elif isinstance(node, ast.ClassDef):
            yield ("class", node, ast.get_docstring(node) or "")


def has_all_tokens(text: str) -> bool:
    lowered = text.lower()
    return all(tok in lowered for tok in REQUIRED_TOKENS)


def analyze_file(path: Path) -> List[str]:
    """Return list of violation messages for a single file.

    Why: Provide granular feedback pinpointing missing reasoning arrows.
    Where: Called for each staged file before commit.
    How: Skips files with skip marker; parses AST and validates docstrings.
    """
    try:
        src = path.read_text(encoding='utf-8')
    except Exception as e:
        return [f"{path}: unable to read file ({e})"]

    if SKIP_MARKER in src:
        _debug(f"Skipping {path} due to marker")
        return []

    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"{path}: syntax error prevents doc enforcement: {e}"]

    violations: List[str] = []
    for kind, node, doc in extract_docstring_nodes(tree):
        # Only enforce if the object contains *some* docstring; empty docstrings
        # implicitly violate the broader docs policy, but keep enforcement
        # focused on missing tokens to avoid noisy duplicate failures.
        if not doc.strip():
            violations.append(f"{path}:{getattr(node, 'lineno', 1)} {kind} missing docstring (needs Why/Where/How)")
            continue
        if not has_all_tokens(doc):
            violations.append(
                f"{path}:{getattr(node, 'lineno', 1)} {kind} docstring missing tokens -> required: Why/Where/How"
            )
    return violations


def main(argv: List[str]) -> int:
    explicit_paths = [Path(a) for a in argv if a.endswith('.py') and Path(a).exists()]
    targets = explicit_paths or gather_staged_python_files()
    if not targets:
        _debug("No Python files to check; exiting cleanly")
        return 0
    all_violations: List[str] = []
    for path in targets:
        all_violations.extend(analyze_file(path))
    if all_violations:
        print("\nReasoning documentation enforcement failed (Why/Where/How).")
        print("These issues break the live reasoning graph; fix before commit:\n")
        for v in all_violations:
            print(f" - {v}")
        print("\nAdd '# reasoning-skip' ONLY for generated or vendor code (rare).")
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
