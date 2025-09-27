from __future__ import annotations

"""
Safe, opt-in fixer for small self-repairs. Only runs whitelisted operations.

Why: Provides automated system maintenance and repair capabilities through
safe, whitelisted operations that can fix common issues without manual intervention.
Where: Used by system monitoring tools and maintenance scripts for automated
system health maintenance and issue resolution.
How: Implements controlled self-repair operations with validation and safety
checks to prevent unintended system modifications.

Connects to:
    - system_validator.py: Provides repair operations for validation failures
    - automated_monitor.py: Used for automated system maintenance
    - debug_config.py: Logs repair operations and results
    - Various system files: Applies targeted fixes to maintain system health
"""

# NOTE: Minimal, idempotent edits directly to project files.

def list_operations() -> List[str]:
    """
    Return list of available self-repair operations for Clever AI system.

    Why: Provides safe, whitelisted operations for automated system
         maintenance and UI enhancements without manual intervention.
    Where: Used by repair systems and administrative tools to discover
           available self-repair capabilities.
    How: Returns hardcoded list of operation names that can be passed
         to the apply() function for execution.

    Returns:
        List[str]: Names of available repair operations
    """
    return [
        "ensure_service_worker",
        "ensure_citations",
        "enable_autoswitch",
        "brighten_scene",
        "boost_particles",
        "fix_indentation",
        "remove_stray_sql",
        "clean_merge_markers",
        "repair_dependencies",
        "validate_config",
        "check_database_integrity",
        "cleanup_logs",
    ]

def apply(op: str) -> Tuple[bool, str]:
    """
    Execute specified self-repair operation with safety validation.

    Why: Provides controlled execution of whitelisted repair operations
         to maintain system functionality and enhance user experience.
    Where: Called by automated repair systems or administrative tools
           to perform specific maintenance tasks.
    How: Validates operation name against whitelist, dispatches to
         appropriate internal handler function, returns success status.

    Args:
        op: Name of the operation to execute (from list_operations)

    Returns:
        Tuple[bool, str]: (success_flag, status_message)
    """
    if op == "ensure_service_worker":
        return _ensure_service_worker_present()
    if op == "ensure_citations":
        return _ensure_citations_chip()
    if op == "enable_autoswitch":
        return _enable_autoswitch_mode()
    if op == "brighten_scene":
        return _brighten_scene_constants()
    if op == "boost_particles":
        return _boost_particle_count()
    if op == "fix_indentation":
        return _run_code_cleaner("fix_indentation")
    if op == "remove_stray_sql":
        return _run_code_cleaner("remove_stray_sql")
    if op == "clean_merge_markers":
        return _run_code_cleaner("clean_merge_markers")
    if op == "repair_dependencies":
        return _repair_dependencies()
    if op == "validate_config":
        return _validate_config_files()
    if op == "check_database_integrity":
        return _check_database_integrity()
    if op == "cleanup_logs":
        return _cleanup_logs()
    return False, "unknown operation"

def _repair_dependencies() -> Tuple[bool, str]:
    """
    Check and reinstall missing Python packages using requirements.txt.
    """

    try:
        result = subprocess.run(
            ["pip", "install", "-r", "requirements.txt"], capture_output=True, text=True
        )
        if result.returncode == 0:
            return True, "Dependencies repaired."
        else:
            return False, f"Dependency repair failed: {result.stderr.strip()}"
    except Exception:
        return False, f"Dependency repair error: {e}"

def _validate_config_files() -> Tuple[bool, str]:
    """
    Validate and auto-correct config.py and user_config.py for required keys and values.
    """
    import importlib.util

    required_keys = ["DB_PATH", "DEBUG"]
    config_files = ["config.py", "user_config.py"]
    fixed = []
    for fname in config_files:
        try:
            spec = importlib.util.spec_from_file_location("cfg", fname)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load spec for {fname}")
            cfg = importlib.util.module_from_spec(spec)
            sys.modules["cfg"] = cfg
            spec.loader.exec_module(cfg)
            missing = [k for k in required_keys if not hasattr(cfg, k)]
            if missing:
                with open(fname, "a") as f:
                    for k in missing:
                        f.write(f"\n{k} = None  # Auto-added by fixer\n")
                fixed.append(f"{fname}: added {missing}")
        except Exception:
            fixed.append(f"{fname}: error {e}")
    if fixed:
        return True, ", ".join(fixed)
    return True, "Config files validated."

def _check_database_integrity() -> Tuple[bool, str]:
    """Validate clever.db integrity; restore from backup if corrupted.
    Why: Ensures single database reliability for persistence guarantees.
    Where: Invoked by diagnostic tooling in fixer.
    How: PRAGMA integrity_check; if failed attempt restore from optional backup.
    """
    import sqlite3
    db_path = "clever.db"
    try:
        con = sqlite3.connect(db_path)
        result = con.execute("PRAGMA integrity_check;").fetchone()
        con.close()
        if result and result[0] == "ok":
            return True, "Database integrity OK."
        backup = Path("clever.db.bak")
        if backup.exists():
            Path(db_path).write_bytes(backup.read_bytes())
            return True, "Database restored from backup."
        return False, f"Database integrity failed: {result[0] if result else 'Unknown error'}"
    except Exception:
        return False, f"Database integrity error: {e}"

def _cleanup_logs() -> Tuple[bool, str]:
    """
    Archive or clean up old log files in logs/.
    """
    from datetime import datetime

    log_dir = Path("logs")
    archive_dir = log_dir / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not log_dir.exists():
        return True, "No logs directory."
    log_files = [f for f in log_dir.iterdir() if f.is_file() and f.suffix == ".log"]
    if not log_files:
        return True, "No log files to clean."
    archive_dir.mkdir(parents=True, exist_ok=True)
    for f in log_files:
        shutil.move(str(f), str(archive_dir / f.name))
    return True, f"Archived {len(log_files)} log files."

def _run_code_cleaner(mode: str) -> Tuple[bool, str]:
    """
    Run context-aware code cleaner for self-healing.
    Args:
        mode: Which fix to apply (fix_indentation, remove_stray_sql, clean_merge_markers)
    Returns:
        Tuple[bool, str]: Success flag and status message
    """

    script = "auto_code_cleaner_v2.py"
    arg_map = {
        "fix_indentation": "--fix",
        "remove_stray_sql": "--fix",
        "clean_merge_markers": "--fix",
    }
    try:
        result = subprocess.run(
            ["python3", script, arg_map.get(mode, "--fix")],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True, f"{mode} completed: {result.stdout.strip()}"
        else:
            return False, f"{mode} failed: {result.stderr.strip()}"
    except Exception:
        return False, f"{mode} error: {e}"

def _ensure_service_worker_present() -> Tuple[bool, str]:
    sw = Path("static/sw.js")
    if sw.exists():
        return True, "present"
    sw.write_text(
        "self.addEventListener('install',()=>self.skipWaiting());\nself.addEventListener('activate',e=>e.waitUntil(clients.claim()));\n"
    )
    return True, "created"

def _ensure_citations_chip() -> Tuple[bool, str]:
    # Already implemented in static/app.js; report present
    p = Path("static/app.js")
    txt = p.read_text(encoding="utf-8") if p.exists() else ""
    return (
        "citations" in txt,
        "ok: citation chips enabled" if "citations" in txt else "not found in app.js",
    )

def _enable_autoswitch_mode() -> Tuple[bool, str]:
    # Backend infers mode now; confirm presence
    p = Path("app.py")
    ok = p.exists() and ("def _infer_mode" in p.read_text(encoding="utf-8"))
    return ok, "autoswitch active" if ok else "infer_mode not found"

def _brighten_scene_constants() -> Tuple[bool, str]:
    p = Path("static/scene.js")
    if not p.exists():
        return False, "scene.js missing"
    s = p.read_text(encoding="utf-8")
    # Increase glow subtly if not already boosted
    if "shadowBlur = glow;" in s and "glow);\n      ctx.fill();" in s:
        # Adjust nothing; we already use energy-based glow
        return True, "already bright"
    return True, "no-op"

def _boost_particle_count() -> Tuple[bool, str]:
    p = Path("static/scene.js")
    if not p.exists():
        return False, "scene.js missing"
    s = p.read_text(encoding="utf-8")
    if "new Array(4800)" in s:
        s2 = s.replace("new Array(4800)", "new Array(6200)")
        p.write_text(s2, encoding="utf-8")
        return True, "particles increased to 6200"
    return True, "already boosted"
