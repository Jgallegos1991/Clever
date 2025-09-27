"""Simplified knowledge_base stub.

Why: The original module accumulated legacy artifacts. This minimal, documented
compatibility layer lets lingering imports keep working without reintroducing
complex or duplicated DB logic.
Where: Used by lightweight smoke tests and any legacy utilities that still log
basic interactions. Primary persistence is managed by database.DatabaseManager.
How: Provides three helpers that operate on the single SQLite DB at config.DB_PATH
using DatabaseManager for thread-safe connections.

Connects to:
    - database.py: Uses DatabaseManager for the single DB
    - config.py: Centralized DB_PATH enforcing single-database rule
"""

from database import DatabaseManager
import config

# Single shared DatabaseManager instance bound to the configured single DB.
_db = DatabaseManager(config.DB_PATH)


def init_db() -> bool:
    """Create the minimal interactions table if missing.

    Why: Some legacy utilities expect a tiny logging table even though the
    broader tracking has moved elsewhere.
    Where: Invoked during startup by legacy scripts or tests that import this
    module for side effects.
    How: Executes a single CREATE TABLE IF NOT EXISTS against the unified DB.

    Returns:
        True on success (or already present), False on error.

    Connects to:
        - database.py: Thread-safe connection helper
        - config.py: Source of DB_PATH
    """
    try:
        with _db._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL,
                    user_message TEXT,
                    clever_response TEXT
                )"""
            )
        return True
    except Exception:
        return False


def log_interaction(user_message: str, clever_response: str, **kwargs: Any) -> None:
    """Insert a simple interaction row (extra args ignored for compatibility).

    Why: Maintains backwards compatibility with older code that may still call
    this function with additional metadata parameters.
    Where: Potentially referenced by residual legacy modules not yet refactored
    to the evolution logging path.
    How: Ignores extra kwargs and writes a minimal record (timestamp, user
    message, response) into the interactions table (created lazily).

    Args:
        user_message: Raw user input text.
        clever_response: Generated response text.
        **kwargs: Ignored legacy metadata (kept to avoid breaking callers).

    Connects to:
        - database.py for persistence
    """
    init_db()
    with _db._connect() as conn:
        conn.execute(
            "INSERT INTO interactions (ts, user_message, clever_response) VALUES (?,?,?)",
            (time.time(), user_message, clever_response),
        )


def get_recent_interactions(limit: int = 10) -> List[Dict[str, Any]]:
    """Return the most recent interaction rows ordered newest first.

    Why: Provides a lightweight inspection/diagnostic hook during development
    or tests without exposing broader database query surface area.
    Where: May be called by debug tooling or ad-hoc scripts.
    How: Performs a SELECT with ORDER/DESC + LIMIT and converts rows to dicts.

    Args:
        limit: Maximum number of rows to return (default 10).

    Returns:
        List of recent interaction dicts with id, ts, user_message, clever_response.
    """
    init_db()
    with _db._connect() as conn:
        rows = conn.execute(
            "SELECT id, ts, user_message, clever_response FROM interactions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {"id": r[0], "ts": r[1], "user_message": r[2], "clever_response": r[3]}
        for r in rows
    ]


__all__ = [
    "init_db",
    "log_interaction",
    "get_recent_interactions",
]
