"""
Auto Code Cleaner v2: Context-Aware Python Fixer

Why: Upgrades the original cleaner to handle indentation errors inside functions/classes, misplaced code blocks, and stray SQL with AST/context awareness.
Where: Run in project root to scan/fix all .py files (excluding venv and third-party packages).
How: Uses ast and regex to detect/fix errors, outputs a detailed report, and can auto-fix issues.

Connects to:
    - None: This is a standalone utility script.

Usage:
    python3 auto_code_cleaner_v2.py [--fix]
"""

import re
import ast

PYTHON_FILE_PATTERN = re.compile(r".*\.py$")
SQL_PATTERN = re.compile(
    r"^(\s*)(CREATE|ALTER|INSERT|SELECT|UPDATE|DELETE)\s+TABLE", re.IGNORECASE
)
MERGE_MARKER_PATTERN = re.compile(r"^(<<<<<<<|=======|>>>>>>>)")
EXCLUDE_DIRS = {"venv", ".venv", "site-packages", "__pycache__"}

REPORT = []


def is_in_function_or_class(node):
    while node:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return True
        node = getattr(node, "parent", None)
    return False


def attach_parents(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def scan_file(path: Path, fix: bool = False):
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    new_lines = []
    changed = False
    # Remove merge markers and stray SQL outside triple quotes
    for i, line in enumerate(lines):
        if MERGE_MARKER_PATTERN.match(line):
            REPORT.append(f"{path}: Merge marker at line {i+1}")
            changed = True
            continue
        if SQL_PATTERN.match(line):
            prev = lines[i - 1] if i > 0 else ""
            next = lines[i + 1] if i + 1 < len(lines) else ""
            if not (prev.strip().startswith('"""') or next.strip().endswith('"""')):
                REPORT.append(f"{path}: Stray SQL at line {i+1}")
                changed = True
                continue
        new_lines.append(line)
    # AST-based indentation and misplaced code block detection
    try:
        tree = ast.parse("".join(new_lines))
        attach_parents(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                # Check for stray SQL in string expressions not assigned or used
                if SQL_PATTERN.match(node.value.s):
                    if not is_in_function_or_class(node):
                        REPORT.append(
                            f"{path}: Stray SQL string outside function/class at line {node.lineno}"
                        )
                        changed = True
            if isinstance(node, ast.FunctionDef):
                # Check for indentation errors in function body
                for stmt in node.body:
                    if hasattr(stmt, "col_offset") and stmt.col_offset % 4 != 0:
                        REPORT.append(
                            f"{path}: Indentation error in function '{node.name}' at line {stmt.lineno}"
                        )
                        changed = True
    except Exception as e:
        REPORT.append(f"{path}: AST parse error: {e}")
    if changed and fix:
        with path.open("w", encoding="utf-8") as f:
            f.writelines(new_lines)


def main():
    fix = "--fix" in sys.argv
    root = Path(os.getcwd())
    for dirpath, _, filenames in os.walk(root):
        if any(ex in dirpath for ex in EXCLUDE_DIRS):
            continue
        for fname in filenames:
            if PYTHON_FILE_PATTERN.match(fname):
                scan_file(Path(dirpath) / fname, fix=fix)
    print("\nAuto Code Cleaner v2 Report:")
    for entry in REPORT:
        print(entry)
    if fix:
        print("\nFixes applied where possible.")
    else:
        print("\nRun with --fix to apply fixes.")


if __name__ == "__main__":
    main()
