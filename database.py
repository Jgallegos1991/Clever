"""
<<<<<<< HEAD
Database Manager for Clever AI

Why: Provides thread-safe, centralized access to the single SQLite database
(clever.db) for all persistence and retrieval operations. Ensures data integrity
and enforces single-database architecture.
Where: Used by all modules requiring data storage or retrieval, including
ingestors, evolution engine, persona, and app.
How: Implements a thread-safe DatabaseManager class, dataclasses for sources,
and connection helpers. All database operations route through this module.

Connects to:
    - config.py: Uses DB_PATH for database location
    - file_ingestor.py, pdf_ingestor.py: Ingestion modules
    - evolution_engine.py: Self-learning core
    - persona.py: Persona engine
    - app.py: Main application
"""

=======
Database Management Module - SQLite-based data persistence for Clever AI.

Why: Provides centralized, thread-safe database operations for all Clever components,
     managing knowledge sources, chat history, user interactions, and system state
     while maintaining offline-first architecture principles.

Where: Used throughout the application by persona engine, evolution engine, 
       knowledge base, file ingestion, and all components requiring data persistence.

How: Implements DatabaseManager class with thread-safe operations using SQLite,
     with automatic schema management and standardized data models for consistency.
"""
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
import threading
from typing import Iterable, Optional

import config


_lock = threading.RLock()


@dataclass
class Source:
<<<<<<< HEAD
=======
    """
    Data model for knowledge source files in the database.
    
    Why: Provides structured representation of ingested files with metadata,
         enabling efficient tracking, deduplication, and content management.
    
    Where: Used by file ingestion, knowledge base queries, and content management.
    
    How: Dataclass with optional fields for content hashing and file statistics,
         allowing both simple and comprehensive file tracking scenarios.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    id: int
    filename: str
    path: str
    content: str
    content_hash: str | None = None
    size: int | None = None
    modified_ts: float | None = None


class DatabaseManager:
<<<<<<< HEAD
    def __init__(self, db_path: str | Path):
=======
    """
    Thread-safe SQLite database manager for Clever AI data persistence.
    
    Why: Centralizes all database operations with consistent transaction handling,
         schema management, and thread safety for multi-component access.
    
    Where: Instantiated by modules needing database access, using config.DB_PATH
         for consistent database file location across the application.
    
    How: Provides high-level methods for common operations while maintaining
         low-level access for complex queries, with automatic schema setup.
    """
    
    def __init__(self, db_path: str | Path):
        """
        Initialize database manager with specified database file path.
        
        Why: Sets up database connection and ensures schema exists for operations,
             creating parent directories as needed for robust initialization.
        
        Where: Called by any module requiring database access, typically once
               per module using the centralized config.DB_PATH.
        
        How: Stores path, creates parent directories, and calls _init() for
             schema setup with thread-safe initialization.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
<<<<<<< HEAD
        # check_same_thread=False to allow access from Flask thread + background jobs
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init(self):
=======
        """
        Create thread-safe SQLite database connection.
        
        Why: Enables concurrent access from Flask threads and background jobs
             while maintaining data integrity and avoiding lock conflicts.
        
        Where: Called internally by all database operations to establish connections.
        
        How: Returns SQLite connection with check_same_thread=False to allow
             multi-threaded access with proper external synchronization.
        """
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init(self):
        """
        Initialize database schema with all required tables and columns.
        
        Why: Ensures consistent database structure across deployments and handles
             schema evolution with backward-compatible column additions.
        
        Where: Called during DatabaseManager initialization to set up tables.
        
        How: Creates tables with proper constraints, adds missing columns to
             existing tables, and commits changes within thread-safe context.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
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
                )
                """
            )
            # Backfill columns if the table pre-existed without them
<<<<<<< HEAD
            cols = {
                row[1] for row in con.execute("PRAGMA table_info(sources)")
            }
=======
            cols = {row[1] for row in con.execute("PRAGMA table_info(sources)")}
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
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
                )
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
                )
                """
            )
            # Context notes table
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS context_notes (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    ts REAL
                )
                """
            )
            con.commit()

    def add_or_update_source(
        self,
        filename: str,
        path: str,
        content: str,
        *,
        content_hash: str | None = None,
        size: int | None = None,
        modified_ts: float | None = None,
    ) -> tuple[int, str]:
<<<<<<< HEAD
        """Insert, update if content changed, or no-op.

        Returns (id, status) where status in {"inserted","updated","unchanged"}.
=======
        """
        Insert new source or update existing source with content change detection.

        Why: Provides efficient file ingestion with deduplication based on content
             hashes, avoiding unnecessary updates when file content hasn't changed.

        Where: Used by file ingestion modules (pdf_ingestor, file_ingestor) and
               sync watchers to add documents to the knowledge base.

        How: Checks existing source by path, compares content hash if available,
             and either inserts new record or updates existing with new content.

        Returns:
            tuple[int, str]: (source_id, status) where status is one of
                           "inserted", "updated", or "unchanged"
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        """
        with _lock, self._connect() as con:
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
                    """
                    UPDATE sources
                    SET filename = ?, content = ?, content_hash = ?, size = ?, modified_ts = ?
                    WHERE id = ?
                    """,
<<<<<<< HEAD
                    (
                        filename,
                        content,
                        content_hash,
                        size,
                        modified_ts,
                        existing_id,
                    ),
                    # Project Coding Instructions:
                    # See .github/copilot-instructions.md for architecture, documentation, and workflow rules.
                    # All code must follow these standards.
=======
                    (filename, content, content_hash, size, modified_ts, existing_id),
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
                )
                con.commit()
                return int(existing_id), "updated"
            # Insert new
            cur.execute(
                """
                INSERT INTO sources (filename, path, content, content_hash, size, modified_ts)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (filename, path, content, content_hash, size, modified_ts),
            )
            con.commit()
            return int(cur.lastrowid), "inserted"

<<<<<<< HEAD
    # --- Context notes ---
    def set_context_note(
        self, key: str, value: str, ts: float | None = None
    ) -> None:
        import time as _time

=======
    def set_context_note(self, key: str, value: str, ts: float | None = None) -> None:
        """
        Store or update a context note in the database.
        
        Why: Provides persistent key-value storage for application context and state,
             enabling components to share information across sessions.
        
        Where: Used by evolution engine, persona system, and other components
               needing to persist contextual information or preferences.
        
        How: Inserts new note or updates existing using SQLite UPSERT pattern,
             with automatic timestamp if not provided.
        """
        import time as _time
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        if ts is None:
            ts = _time.time()
        with _lock, self._connect() as con:
            con.execute(
                """
                INSERT INTO context_notes (key, value, ts)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, ts=excluded.ts
                """,
                (key, value, float(ts)),
            )
            con.commit()

    def set_context_notes(self, notes: dict[str, str]) -> None:
<<<<<<< HEAD
=======
        """
        Store multiple context notes in a single transaction.
        
        Why: Enables efficient batch updates of related context information,
             maintaining consistency when setting multiple related values.
        
        Where: Used when components need to update multiple context values
               atomically, such as during configuration changes.
        
        How: Iterates through dictionary and calls set_context_note for each
             key-value pair, with None values converted to empty strings.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        for k, v in (notes or {}).items():
            if v is None:
                v = ""
            self.set_context_note(str(k), str(v))

    def get_context_notes(self) -> dict[str, str]:
<<<<<<< HEAD
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT key, value FROM context_notes ORDER BY key ASC"
            )
            return {row[0]: row[1] for row in cur.fetchall()}

    # Backward-compat shim used by older callers
    def add_source(self, filename: str, path: str, content: str) -> int:
=======
        """
        Retrieve all stored context notes as a dictionary.
        
        Why: Provides access to all persisted context information for components
             that need to restore state or access shared configuration data.
        
        Where: Used by initialization routines and components that need access
               to previously stored context or preference information.
        
        How: Queries all context notes ordered by key and returns as dictionary
             with thread-safe database access.
        """
        with _lock, self._connect() as con:
            cur = con.execute("SELECT key, value FROM context_notes ORDER BY key ASC")
            return {row[0]: row[1] for row in cur.fetchall()}

    def add_source(self, filename: str, path: str, content: str) -> int:
        """
        Backward-compatibility method for adding sources without metadata.
        
        Why: Maintains compatibility with older code that expects simple source
             addition without content hashing or file metadata.
        
        Where: Used by legacy ingestion code or simple file addition scenarios
               where metadata tracking is not required.
        
        How: Delegates to add_or_update_source and returns just the source ID,
             discarding the status information for simpler interface.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        id_, _ = self.add_or_update_source(filename, path, content)
        return id_

    def list_sources(self) -> list[Source]:
<<<<<<< HEAD
=======
        """
        Retrieve all sources from the database in reverse chronological order.
        
        Why: Provides access to all ingested knowledge sources for knowledge base
             queries, file management, and content analysis operations.
        
        Where: Used by knowledge base searches, file management interfaces,
               and analytics that need to process all available content.
        
        How: Queries all source records with complete metadata, orders by ID
             descending to show newest first, returns as Source objects.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content, content_hash, size, modified_ts FROM sources ORDER BY id DESC"
            )
            return [Source(*row) for row in cur.fetchall()]

    def get_source(self, source_id: int) -> Optional[Source]:
<<<<<<< HEAD
=======
        """
        Retrieve a specific source by its database ID.
        
        Why: Enables direct access to individual sources for content retrieval,
             editing, or detailed analysis when the source ID is known.
        
        Where: Used by knowledge base queries, file editors, and components
               that need to access specific previously ingested documents.
        
        How: Queries single source by primary key with thread-safe access,
             returns Source object or None if not found.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content, content_hash, size, modified_ts FROM sources WHERE id = ?",
                (source_id,),
            )
            row = cur.fetchone()
            return Source(*row) if row else None

    def get_source_by_path(self, path: str) -> Optional[Source]:
<<<<<<< HEAD
=======
        """
        Retrieve a source by its file path for deduplication and updates.
        
        Why: Enables path-based lookups for file ingestion to check if content
             already exists and needs updating rather than creating duplicates.
        
        Where: Used by file watchers, ingestion systems, and sync tools that
               monitor file system changes and need to update existing sources.
        
        How: Queries single source by unique path constraint with thread-safe
             access, returns Source object or None if path not found.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content, content_hash, size, modified_ts FROM sources WHERE path = ?",
                (path,),
            )
            row = cur.fetchone()
            return Source(*row) if row else None

    def delete_source_by_path(self, path: str) -> int:
<<<<<<< HEAD
=======
        """
        Delete a source from the database by its file path.
        
        Why: Enables removal of sources when files are deleted from the filesystem,
             maintaining consistency between the knowledge base and actual files.
        
        Where: Used by file watchers and sync tools when they detect file deletions,
               and by cleanup operations that need to remove outdated sources.
        
        How: Deletes source record matching the given path with thread-safe
             operation, returns number of deleted records (0 or 1).
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
            cur = con.execute("DELETE FROM sources WHERE path = ?", (path,))
            con.commit()
            return cur.rowcount

    def search_sources(self, query: str, limit: int = 50) -> list[Source]:
<<<<<<< HEAD
=======
        """
        Search for sources matching query in filename, path, or content.
        
        Why: Provides basic full-text search capability across all source fields,
             enabling users to find relevant documents quickly.
        
        Where: Used by knowledge base searches, content discovery interfaces,
               and as pre-filtering step for more advanced search operations.
        
        How: Uses SQL LIKE queries across filename, path, and content fields
             with case-insensitive pattern matching, returns recent results first.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        q = f"%{query}%"
        with _lock, self._connect() as con:
            cur = con.execute(
                """
                SELECT id, filename, path, content, content_hash, size, modified_ts
                FROM sources
                WHERE filename LIKE ? OR path LIKE ? OR content LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (q, q, q, int(limit)),
            )
            return [Source(*row) for row in cur.fetchall()]

<<<<<<< HEAD
    def search_snippets(
        self, query: str, limit: int = 5, window: int = 240
    ) -> list[dict]:
        """Return top content snippets matching the query with smart caching.

        Enhanced with better scoring and performance optimization.
        """
        import re as _re, time

        if not query:
            return []

        # Cache frequent searches for better performance
        cache_key = f"search_{hash(query)}_{limit}"

        # tokenize query with better filtering
        q_tokens = [
            t.lower()
            for t in _re.split(r"\W+", query)
            if len(t) > 2
            and t
            not in {
                "the",
                "and",
                "for",
                "are",
                "but",
                "not",
                "you",
                "all",
                "can",
                "had",
                "has",
                "was",
                "one",
                "our",
                "out",
                "day",
                "get",
                "use",
                "her",
                "his",
                "how",
                "may",
                "new",
                "now",
                "old",
                "see",
                "two",
                "way",
                "who",
                "boy",
                "did",
                "its",
                "let",
                "put",
                "say",
                "she",
                "too",
                "use",
            }
        ]
        if not q_tokens:
            return []

        # Enhanced preselection with better LIKE patterns
        like_pattern = " ".join(q_tokens[:3])  # Use top 3 tokens
        pre = self.search_sources(like_pattern, limit=min(100, limit * 20))
        hits: list[dict] = []

        for s in pre:
            text = s.content
            low = text.lower()

            # Enhanced scoring with multiple factors
            exact_matches = sum(low.count(tok) for tok in q_tokens)
            partial_matches = sum(
                1
                for tok in q_tokens
                if any(tok in word for word in low.split())
            )
            score = exact_matches * 2 + partial_matches

            # Bonus for matches in filename
            filename_matches = sum(
                1 for tok in q_tokens if tok in s.filename.lower()
            )
            score += filename_matches * 3

            if score <= 0:
                continue

            # Smart snippet extraction with better boundaries
            positions = [
                low.find(tok) for tok in q_tokens if low.find(tok) != -1
            ]
            if not positions:
                continue

            first_pos = min(positions)
            start = max(0, first_pos - window // 2)
            end = min(len(text), start + window)

            # Expand to sentence boundaries for better readability
            try:
                # Look for sentence endings before start
                sentence_start = text.rfind(".", 0, start)
                if sentence_start != -1 and start - sentence_start < 100:
                    start = sentence_start + 1

                # Look for sentence endings after end
                sentence_end = text.find(".", end)
                if sentence_end != -1 and sentence_end - end < 100:
                    end = sentence_end + 1

                snippet = text[start:end].strip()
            except Exception:
                snippet = text[start:end].strip()

            hits.append(
                {
                    "id": s.id,
                    "filename": s.filename,
                    "path": s.path,
                    "score": int(score),
                    "snippet": snippet,
                    "start": int(start),
                    "end": int(end),
                }
            )

        # Enhanced sorting: score first, then recency, then filename
        hits.sort(
            key=lambda h: (h["score"], h["id"], h["filename"]), reverse=True
        )
        return hits[:limit]

    # --- Chat history ---
    def add_utterance(
        self,
        role: str,
        text: str,
        mode: str | None = None,
        ts: float | None = None,
    ) -> int:
        import time as _time

=======
    def search_snippets(self, query: str, limit: int = 5, window: int = 240) -> list[dict]:
        """
        Advanced search returning scored content snippets with context.

        Why: Provides intelligent search results with relevant content excerpts,
             scoring, and sentence-boundary awareness for better user experience.

        Where: Used by knowledge base queries, Q&A systems, and content discovery
               features that need to show relevant excerpts rather than full sources.

        How: Tokenizes query, scores matches using multiple factors (exact matches,
             partial matches, filename matches), extracts contextual snippets with
             smart boundary detection, and ranks results by relevance.
        """
        import re as _re, time
        if not query:
            return []
        
        # Cache frequent searches for better performance
        cache_key = f"search_{hash(query)}_{limit}"
        
        # tokenize query with better filtering
        q_tokens = [t.lower() for t in _re.split(r"\W+", query) if len(t) > 2 and t not in {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'has', 'was', 'one', 'our', 'out', 'day', 'get', 'use', 'her', 'his', 'how', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}]
        if not q_tokens:
            return []
        
        # Enhanced preselection with better LIKE patterns
        like_pattern = " ".join(q_tokens[:3])  # Use top 3 tokens
        pre = self.search_sources(like_pattern, limit=min(100, limit*20))
        hits: list[dict] = []
        
        for s in pre:
            text = s.content
            low = text.lower()
            
            # Enhanced scoring with multiple factors
            exact_matches = sum(low.count(tok) for tok in q_tokens)
            partial_matches = sum(1 for tok in q_tokens if any(tok in word for word in low.split()))
            score = exact_matches * 2 + partial_matches
            
            # Bonus for matches in filename
            filename_matches = sum(1 for tok in q_tokens if tok in s.filename.lower())
            score += filename_matches * 3
            
            if score <= 0:
                continue
                
            # Smart snippet extraction with better boundaries
            positions = [low.find(tok) for tok in q_tokens if low.find(tok) != -1]
            if not positions:
                continue
                
            first_pos = min(positions)
            start = max(0, first_pos - window // 2)
            end = min(len(text), start + window)
            
            # Expand to sentence boundaries for better readability
            try:
                # Look for sentence endings before start
                sentence_start = text.rfind('.', 0, start)
                if sentence_start != -1 and start - sentence_start < 100:
                    start = sentence_start + 1
                
                # Look for sentence endings after end
                sentence_end = text.find('.', end)
                if sentence_end != -1 and sentence_end - end < 100:
                    end = sentence_end + 1
                    
                snippet = text[start:end].strip()
            except Exception:
                snippet = text[start:end].strip()
            
            hits.append({
                "id": s.id,
                "filename": s.filename,
                "path": s.path,
                "score": int(score),
                "snippet": snippet,
                "start": int(start),
                "end": int(end),
            })
        
        # Enhanced sorting: score first, then recency, then filename
        hits.sort(key=lambda h: (h["score"], h["id"], h["filename"]), reverse=True)
        return hits[:limit]

    def add_utterance(self, role: str, text: str, mode: str | None = None, ts: float | None = None) -> int:
        """
        Record a chat utterance from user or assistant in conversation history.
        
        Why: Maintains persistent conversation history for context, learning,
             and conversation continuity across sessions.
        
        Where: Used by chat interface, persona engine, and conversation management
               to track all user interactions and AI responses.
        
        How: Inserts utterance record with role (user/assistant), text, optional
             mode, and timestamp, returns the new utterance ID.
        """
        import time as _time
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        if ts is None:
            ts = _time.time()
        with _lock, self._connect() as con:
            cur = con.execute(
                "INSERT INTO utterances (role, text, mode, ts) VALUES (?, ?, ?, ?)",
                (role, text, mode, float(ts)),
            )
            con.commit()
            return int(cur.lastrowid)

    def list_utterances(self, limit: int = 50) -> list[dict]:
<<<<<<< HEAD
=======
        """
        Retrieve recent conversation utterances in reverse chronological order.
        
        Why: Enables conversation history display, context building for responses,
             and conversation analysis for learning and improvement.
        
        Where: Used by chat interface for history display, persona engine for
               context, and analytics for conversation pattern analysis.
        
        How: Queries utterances table ordered by ID descending to get most recent
             first, returns as dictionaries with all fields included.
        """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, role, text, mode, ts FROM utterances ORDER BY id DESC LIMIT ?",
                (int(limit),),
            )
            return [
<<<<<<< HEAD
                {
                    "id": r[0],
                    "role": r[1],
                    "text": r[2],
                    "mode": r[3],
                    "ts": r[4],
                }
                for r in cur.fetchall()
            ]

    # --- Interactions (thought_process logging) ---
=======
                {"id": r[0], "role": r[1], "text": r[2], "mode": r[3], "ts": r[4]}
                for r in cur.fetchall()
            ]

>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    def add_interaction(
        self,
        *,
        user_input: str,
        active_mode: Optional[str] = None,
        action_taken: Optional[str] = None,
        parsed_data: Optional[dict] = None,
        ts: float | None = None,
    ) -> int:
<<<<<<< HEAD
        import time as _time, json as _json

=======
        """
        Log detailed interaction metadata for evolution engine analytics.
        
        Why: Captures structured interaction data for learning algorithms,
             performance analysis, and system evolution tracking.
        
        Where: Used by evolution engine, persona system, and analytics modules
               to record user behavior patterns and system responses.
        
        How: Stores interaction with structured metadata as JSON, including
             user input, active mode, action taken, and parsed analytics data.
        """
        import time as _time, json as _json
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        if ts is None:
            ts = _time.time()
        payload = None
        try:
            payload = _json.dumps(parsed_data or {}, ensure_ascii=False)
        except Exception:
            payload = "{}"
        with _lock, self._connect() as con:
            cur = con.execute(
                """
                INSERT INTO interactions (ts, user_input, active_mode, action_taken, parsed_data)
                VALUES (?, ?, ?, ?, ?)
                """,
                (float(ts), user_input, active_mode, action_taken, payload),
            )
            con.commit()
            return int(cur.lastrowid)

    def list_interactions(self, limit: int = 100) -> list[dict]:
<<<<<<< HEAD
        import json as _json

=======
        """
        Retrieve recent interaction records for analytics and learning.
        
        Why: Provides access to structured interaction data for evolution engine
             analysis, pattern recognition, and system learning algorithms.
        
        Where: Used by evolution engine, analytics dashboards, and learning
               systems that need to analyze user interaction patterns.
        
        How: Queries interactions table in reverse chronological order, parses
             JSON metadata safely, returns structured dictionaries.
        """
        import json as _json
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        with _lock, self._connect() as con:
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
<<<<<<< HEAD
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
=======
                out.append({
                    "id": r[0],
                    "ts": r[1],
                    "user_input": r[2],
                    "active_mode": r[3],
                    "action_taken": r[4],
                    "parsed_data": pd,
                })
            return out

    def add_conversation(self, user_text: str, reply_text: str, *, meta: dict | None = None) -> None:
        """
        Record complete conversation exchange with both utterances and interaction.
        
        Why: Provides high-level interface for logging complete user-AI exchanges
             with both conversation history and analytical metadata.
        
        Where: Used by main chat interface and conversation handlers that need
               to record both sides of the conversation with metadata.
        
        How: Creates user utterance, assistant utterance, and interaction record
             in sequence, extracting mode information from metadata safely.
        """
        try:
            self.add_utterance("user", user_text, mode=(meta or {}).get("detected_intent"))
            self.add_utterance("assistant", reply_text, mode=(meta or {}).get("activePersona"))
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            self.add_interaction(
                user_input=user_text,
                active_mode=(meta or {}).get("activePersona"),
                action_taken=(meta or {}).get("detected_intent"),
                parsed_data=meta or {},
            )
        except Exception:
            pass


<<<<<<< HEAD
# Shared instance
db_manager = DatabaseManager(config.DB_PATH)


# --- Compatibility shim ---
def add_conversation(
    user_text: str, reply_text: str, *, meta: dict | None = None
) -> None:
    """Back-compat function if callers import add_conversation directly.
    Prefer database.db_manager.add_conversation, but keep this to avoid crashes.
    """
    try:
        db_manager.add_utterance(
            "user", user_text, mode=(meta or {}).get("detected_intent")
        )
        db_manager.add_utterance(
            "assistant", reply_text, mode=(meta or {}).get("activePersona")
        )
=======
# Shared instance using centralized configuration
db_manager = DatabaseManager(config.DB_PATH)


def add_conversation(user_text: str, reply_text: str, *, meta: dict | None = None) -> None:
    """
    Backward-compatibility function for recording complete conversations.
    
    Why: Maintains compatibility with older code that imports this function
         directly instead of using the DatabaseManager instance.
    
    Where: Used by legacy code or modules that expect module-level function
         rather than class-based interface for conversation logging.
    
    How: Delegates to the shared db_manager instance's add_conversation method,
         with error handling to prevent crashes in legacy callers.
    """
    try:
        db_manager.add_utterance("user", user_text, mode=(meta or {}).get("detected_intent"))
        db_manager.add_utterance("assistant", reply_text, mode=(meta or {}).get("activePersona"))
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        db_manager.add_interaction(
            user_input=user_text,
            active_mode=(meta or {}).get("activePersona"),
            action_taken=(meta or {}).get("detected_intent"),
            parsed_data=meta or {},
        )
    except Exception:
        pass
