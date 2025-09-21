"""Diagnostics test ensuring architectural invariants hold.

Why: Automatically verify the lightweight drift checks (offline guard, single DB, diagnostics doc) so regressions are caught in CI and local dev without manually running `make diagnostics`.
Where: Part of pytest suite under tests/ and executed in standard `make test` pipeline before deployment; complements runtime introspection by pre-validating static guarantees.
How: Invokes the diagnostics_check script in-process by importing its module and calling `main()`, capturing SystemExit. Fails the test if diagnostics script exits non-zero or prints DRIFT lines.

Connects to:
    - tools/diagnostics_check.py: Source of the validation logic
    - Makefile: `test` target already runs pytest; this test adds enforcement
"""
from __future__ import annotations
import io
import contextlib
import importlib.util
from pathlib import Path


def run_diagnostics_module():
    """Load and execute the diagnostics_check module main() function.

    Why: Avoid spawning a subprocess (faster, deterministic in CI) while still
    executing the exact logic shipped in the diagnostics tool.
    Where: Called only inside the pytest context; not used at runtime.
    How: Dynamically loads the module from path, captures stdout/stderr, and
    returns (exit_code, combined_output).
    """
    root = Path(__file__).resolve().parent.parent
    module_path = root / "tools" / "diagnostics_check.py"
    spec = importlib.util.spec_from_file_location("_diag_mod", module_path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader, "Failed to load diagnostics module spec"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            spec.loader.exec_module(mod)  # type: ignore
            # Call main only if not executed automatically (module guard present)
            if hasattr(mod, "main"):
                try:
                    mod.main()  # type: ignore
                    exit_code = 0
                except SystemExit as e:  # script may call sys.exit
                    exit_code = int(getattr(e, 'code', 1) or 0)
        except Exception:  # pragma: no cover - any unexpected error surfaces in output
            import traceback
            traceback.print_exc()
            exit_code = 1
    output = buf.getvalue()
    return exit_code, output


def test_diagnostics_invariants():
    code, out = run_diagnostics_module()
    drift_lines = [line for line in out.splitlines() if line.startswith('[DRIFT]')]
    assert code == 0, f"Diagnostics script reported failure (exit {code}). Output:\n{out}"
    assert not drift_lines, "Unexpected drift detected:\n" + "\n".join(drift_lines)
    assert '[OK] offline guard present' in out
    assert '[OK] single DB_PATH referencing clever.db' in out
