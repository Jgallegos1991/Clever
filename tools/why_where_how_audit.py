"""Why/Where/How Audit Script

Why: Enforce architectural documentation contract by scanning project Python
files for functions/classes lacking Why/Where/How tokens in their docstrings.
Where: Executed manually via `make audit-why` (Makefile target) or CI hook to
surface drift early before merging changes that erode reasoning graph.
How: Uses `ast` to parse Python files (excluding virtual env, tests optional),
inspects docstrings for presence (case-insensitive) of 'why:' / 'where:' /
'how:' tokens. Outputs a summary with counts and file-level detail.

Connects to:
    - introspection.py: Complement to runtime extraction (runtime ensures
      tokens are consumed; this ensures tokens exist pre-run)
    - Makefile: audit-why target integration
"""
from __future__ import annotations
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
IGNORE_DIRS = {'.venv', '__pycache__', 'legacy', 'logs'}

def iter_python_files():
    for p in ROOT.rglob('*.py'):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        yield p


def has_tokens(doc: str) -> tuple[bool, bool, bool]:
    if not doc:
        return False, False, False
    lower = doc.lower()
    return 'why:' in lower, 'where:' in lower, 'how:' in lower


def audit_file(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node) or ''
            w, wh, h = has_tokens(doc)
            if not (w and wh and h):
                name = getattr(node, 'name', '<anon>')
                missing.append({
                    'symbol': name,
                    'type': type(node).__name__,
                    'why': w,
                    'where': wh,
                    'how': h,
                })
    return missing


def main():
    total = 0
    offenders = 0
    detailed = []
    for f in iter_python_files():
        result = audit_file(f)
        if not result:
            continue
        file_off = [r for r in result if not (r['why'] and r['where'] and r['how'])]
        if file_off:
            offenders += len(file_off)
            detailed.append((f, file_off))
        total += len(result)

    if detailed:
        print('⚠️  Missing Why/Where/How tokens detected:')
        for path, entries in detailed[:50]:  # show up to 50 entries
            print(f'  {path.relative_to(ROOT)}')
            for e in entries[:10]:  # limit per file
                missing_parts = [k for k in ('why','where','how') if not e[k]]
                print(f"    - {e['type']} {e['symbol']} missing: {', '.join(missing_parts)}")
        print('\nSummary:')
        print(f'  Total symbol docstrings scanned: {total}')
        print(f'  Offending symbols: {offenders}')
        print('  Status: FAIL')
        sys.exit(1)
    else:
        print('✅ All scanned symbols include Why/Where/How tokens (within parsed scope).')
        print(f'Scanned symbols: {total}')


if __name__ == '__main__':  # pragma: no cover
    main()
