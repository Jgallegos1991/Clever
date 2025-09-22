"""Central database management module for Clever's single-file SQLite persistence layer.

Why:
    The project enforces a strict offline, single-user, single-database paradigm. All
    persisted state (ingested source documents, chat utterances, interaction telemetry,
    and contextual key/value notes) must live inside one SQLite file referenced by
    ``config.DB_PATH``. Centralizing schema creation, thread safety, and CRUD helpers
    here eliminates duplication and prevents accidental creation of additional
    databases elsewhere in the codebase.
Where:
    This module is imported by ingestion utilities (``file_ingestor.py``,
    ``pdf_ingestor.py``), synchronization/watch components (``sync_watcher.py``),
    conversational systems (``persona.py``, ``clever_conversation_engine.py``), the
    evolution / learning layer (``evolution_engine.py``), health / validation utilities
    (``system_validator.py``, ``health_monitor.py``), and various tooling scripts that
    need read‑only analytics. A shared singleton instance ``db_manager`` is exposed at
    the bottom and reused by modules that don't need custom lifecycle management.
How:
    Provides the ``DatabaseManager`` class which lazily initializes (idempotent) schema
    tables on first construction and applies backward-compatible column backfills using
    PRAGMA inspection. Thread safety is ensured with a re-entrant lock (``RLock``)
    guarding every connection context to avoid concurrent write hazards under the
    Flask app's multi-threaded request model. Higher-level helper methods encapsulate
    insert/select logic for each table, always returning primitive Python structures
    (dicts / lists / ints) to keep calling code decoupled from SQL details. Only this
    module opens SQLite connections; callers should never manage raw connections.

Connects to:
    - config.py: Imports `DB_PATH` to define the single source of truth for the database file location.
    - evolution_engine.py: `add_interaction` is called (often via `app.py`) to log user interactions, which are fundamental to the evolution engine's learning process.
    - persona.py: (Indirectly via `memory_engine.py`) The persona engine relies on the database for all its memory functions, using methods like `add_utterance` to record conversations and `list_utterances` to retrieve history for contextual responses.
    - file_ingestor.py: `FileIngestor.ingest_file()` calls `add_or_update_source()` to add or update file-based knowledge into the database.
    - pdf_ingestor.py: `EnhancedFileIngestor.ingest_file()` calls `add_or_update_source()` to process and store PDF content.
    - sync_watcher.py: The `SyncEventHandler` triggers the file ingestors, which in turn write to the database, keeping Clever's knowledge synchronized.
    - health_monitor.py: `SystemHealthMonitor.check_database_health()` connects to the database to verify its existence, check table integrity, and report statistics.
    - system_validator.py: `SystemValidator._validate_single_database()` checks for the existence of the database file specified in `config.py` to enforce the single database rule.
"""

import threading
from dataclasses import dataclass
from pathlib import Path

import config

@dataclass
class Source:
    id: int
    filename: str
    path: str
    content: str | None = None
    size: int | None = None
    modified_ts: float | None = None


class DatabaseManager:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self._lock = threading.RLock()  # Thread-safe DB access
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        import sqlite3
        return sqlite3.connect(self.db_path)

    def _init(self):
        """Initialize all required database tables.

        Why: Ensures single-file SQLite schema (sources, utterances, interactions, context_notes)
        exists before any operations; supports offline, single-user constraints.
        Where: Called from __init__ immediately after path is prepared.
        How: Creates tables idempotently; backfills missing columns using PRAGMA
        inspection. All executed under thread lock for safety during first-run
        initialization in multi-threaded Flask contexts.
        """
        with self._lock, self._connect() as con:
            con.execute(
                """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    path TEXT NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT,
    size INTEGER,
    modified_ts REAL,
    UNIQUE(path)
);
                """
            )
            # Backfill columns if the table pre-existed without them
            cols = {row[1] for row in con.execute("PRAGMA table_info(sources)")}
            if "content_hash" not in cols:
                con.execute("ALTER TABLE sources ADD COLUMN content_hash TEXT")
            if "size" not in cols:
                con.execute("ALTER TABLE sources ADD COLUMN size INTEGER")
            if "modified_ts" not in cols:
                con.execute("ALTER TABLE sources ADD COLUMN modified_ts REAL")
            # Chat history table (utterances)
            con.execute(
                """
CREATE TABLE IF NOT EXISTS utterances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    text TEXT NOT NULL,
    mode TEXT,
    ts REAL
);
                """
            )
            # Interaction telemetry (thought_process)
            con.execute(
                """
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    user_input TEXT,
    active_mode TEXT,
    action_taken TEXT,
    parsed_data TEXT
);
                """
            )
            # Context notes table
            con.execute(
                """
CREATE TABLE IF NOT EXISTS context_notes (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    ts REAL
);
                """
            )
            # NOTE: No explicit commit after exiting context; managed by with-block

    def set_context_note(self, key: str, value: str, ts: float | None = None) -> None:
        """
        Store or update a context note in the database.

        Why:
            Provides persistent key-value storage for application context and state
            that must survive process restarts (e.g., last processed sync marker).
        Where:
            Used by application logic (e.g., sync components, evolution engine) for
            storing small ephemeral control values without creating new tables.
        How:
            Executes an INSERT OR REPLACE into the ``context_notes`` table with the
            provided key/value and float timestamp for chronological auditing.
        """
        import time as _time
        if ts is None:
            ts = _time.time()
        with self._lock, self._connect() as con:
            con.execute(
                "INSERT OR REPLACE INTO context_notes (key, value, ts) VALUES (?, ?, ?)",
                (key, value, float(ts)),
            )
            con.commit()

    # --- Chat history ---
    def add_utterance(
        self,
        role: str,
        text: str,
        mode: str | None = None,
        ts: float | None = None,
    ) -> int:
        """Insert a single conversation utterance.

        Why: Persist chat turns (user/assistant) for context building, analytics,
        and evolution engine metrics.
        Where: Called by persona / conversation layers and compatibility shims.
        How: Inserts row into utterances with timestamp; returns new row id (0 if
        unavailable). Thread-safe via instance lock.
        """
        import time as _time
        if ts is None:
            ts = _time.time()
        with self._lock, self._connect() as con:
            cur = con.execute(
                "INSERT INTO utterances (role, text, mode, ts) VALUES (?, ?, ?, ?)",
                (role, text, mode, float(ts)),
            )
            con.commit()
            return int(cur.lastrowid) if cur.lastrowid is not None else 0

    def list_utterances(self, limit: int = 50) -> list[dict]:
        """
        Retrieve recent conversation utterances in reverse chronological order.
        
        Why: Enables conversation history display, context building for responses,
            and conversation analysis for learning and improvement.
        
        Where: Used by chat interface for history display, persona engine for
            context, and analytics for conversation pattern analysis.
        
        How: Queries utterances table ordered by ID descending to get most recent
            first, returns as dictionaries with all fields included.
        """
        with self._lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, role, text, mode, ts FROM utterances ORDER BY id DESC LIMIT ?",
                (int(limit),),
            )
            return [
                {
                    "id": r[0],
                    "role": r[1],
                    "text": r[2],
                    "mode": r[3],
                    "ts": r[4],
                }
                for r in cur.fetchall()
            ]

    def add_or_update_source(
        self,
        filename: str,
        path: str,
        content: str | None = None,
        content_hash: str | None = None,
        size: int | None = None,
        modified_ts: float | None = None,
    ) -> tuple[int, str]:
        """
        Insert, update if content changed, or no-op.

        Returns (id, status) where status in {"inserted","updated","unchanged"}.
        """
        with self._lock, self._connect() as con:
            # Ensure table exists even if db_path changed after initialization
            con.execute(
                """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    path TEXT NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT,
    size INTEGER,
    modified_ts REAL,
    UNIQUE(path)
);
                """
            )
            cur = con.cursor()
            cur.execute(
                "SELECT id, content_hash FROM sources WHERE path = ?",
                (path,),
            )
            row = cur.fetchone()
            if row:
                existing_id, existing_hash = row[0], row[1]
                if existing_hash == content_hash and content_hash is not None:
                    return int(existing_id), "unchanged"
                # Update existing
                cur.execute(
                    "UPDATE sources SET filename = ?, content = ?, content_hash = ?, size = ?, modified_ts = ? WHERE id = ?",
                    (filename, content or "", content_hash, size, modified_ts, existing_id),
                )
                con.commit()
                return int(existing_id), "updated"
            # Insert new
            cur.execute(
                "INSERT INTO sources (filename, path, content, content_hash, size, modified_ts) VALUES (?, ?, ?, ?, ?, ?)",
                (filename, path, content or "", content_hash, size, modified_ts),
            )
            con.commit()
            return int(cur.lastrowid) if cur.lastrowid is not None else 0, "inserted"

    def list_interactions(self, limit: int = 100) -> list[dict]:
        """
        Retrieve recent interaction records for analytics and learning.
        
        Why: Provides access to structured interaction data for evolution engine analysis, pattern recognition, and system learning algorithms.
        Where: Used by evolution engine, analytics dashboards, and learning systems that need to analyze user interaction patterns.
        How: Queries interactions table in reverse chronological order, parses JSON metadata safely, returns structured dictionaries.
        """
        import json as _json
        with self._lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, ts, user_input, active_mode, action_taken, parsed_data FROM interactions ORDER BY id DESC LIMIT ?",
                (int(limit),),
            )
            out = []
            for r in cur.fetchall():
                try:
                    pd = _json.loads(r[5] or "{}")
                except Exception:
                    pd = {}
                out.append(
                    {
                        "id": r[0],
                        "ts": r[1],
                        "user_input": r[2],
                        "active_mode": r[3],
                        "action_taken": r[4],
                        "parsed_data": pd,
                    }
                )
            return out

    def add_interaction(
        self,
        user_input: str,
        active_mode: str | None = None,
        action_taken: str | None = None,
        parsed_data: dict | None = None,
        ts: float | None = None,
    ) -> int:
        """
        Add a new interaction record for analytics and learning.
        
        Why: Captures structured interaction data for evolution engine analysis and system learning.
        Where: Called by conversation handlers to log user interactions for pattern analysis.
        How: Inserts interaction data into interactions table with JSON serialization of parsed_data.
        """
        import json as _json
        import time as _time
        if ts is None:
            ts = _time.time()
        with self._lock, self._connect() as con:
            cur = con.execute(
                "INSERT INTO interactions (ts, user_input, active_mode, action_taken, parsed_data) VALUES (?, ?, ?, ?, ?)",
                (float(ts), user_input, active_mode, action_taken, _json.dumps(parsed_data or {})),
            )
            con.commit()
            return int(cur.lastrowid) if cur.lastrowid is not None else 0

    # --- Compatibility: store user+assistant exchange and an interaction ---
    def add_conversation(
        self, user_text: str, reply_text: str, *, meta: dict | None = None
    ) -> None:
        try:
            self.add_utterance(
                "user", user_text, mode=(meta or {}).get("detected_intent")
            )
            self.add_utterance(
                "assistant", reply_text, mode=(meta or {}).get("activePersona")
            )
            self.add_interaction(
                user_input=user_text,
                active_mode=(meta or {}).get("activePersona"),
                action_taken=(meta or {}).get("detected_intent"),
                parsed_data=meta or {},
            )
        except Exception:
            pass


# Shared instance
db_manager = DatabaseManager(config.DB_PATH)


# --- Compatibility shim ---
def add_conversation(
    user_text: str, reply_text: str, *, meta: dict | None = None
) -> None:
    db_manager.add_utterance("user", user_text, mode=(meta or {}).get("detected_intent"))
    db_manager.add_utterance("assistant", reply_text, mode=(meta or {}).get("activePersona"))
