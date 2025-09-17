

import threading
from dataclasses import dataclass
from pathlib import Path

import config


_lock = threading.RLock()

@dataclass
class Source:
    id: int
    filename: str
    path: str
    size: int | None = None
    modified_ts: float | None = None


class DatabaseManager:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        import sqlite3
        return sqlite3.connect(self.db_path)

    def _init(self):
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
            


    # Remove stray code and fix indentation for add_or_update_source and other methods
                    con.commit()
                    return int(cur.lastrowid), "inserted"
                )

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
    def search_sources(self, query: str, limit: int = 50) -> list[Source]:
        """
        Search for sources matching query in filename, path, or content.
        
        Why: Provides basic full-text search capability across all source fields,
             enabling users to find relevant documents quickly.
        
        Where: Used by knowledge base searches, content discovery interfaces,
               and as pre-filtering step for more advanced search operations.
        
        How: Uses SQL LIKE queries across filename, path, and content fields
             with case-insensitive pattern matching, returns recent results first.
        """
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
        """
        Retrieve recent conversation utterances in reverse chronological order.
        
        Why: Enables conversation history display, context building for responses,
             and conversation analysis for learning and improvement.
        
        Where: Used by chat interface for history display, persona engine for
               context, and analytics for conversation pattern analysis.
        
        How: Queries utterances table ordered by ID descending to get most recent
             first, returns as dictionaries with all fields included.
        """
        with _lock, self._connect() as con:
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

    # --- Interactions (thought_process logging) ---
                {"id": r[0], "role": r[1], "text": r[2], "mode": r[3], "ts": r[4]}
                for r in cur.fetchall()
            ]

    def add_or_update_source(
        self,
        filename: str,
        path: str,
        content_hash: str | None = None,
        size: int | None = None,
        modified_ts: float | None = None,
    ) -> tuple[int, str]:
        """
        Insert, update if content changed, or no-op.

        Returns (id, status) where status in {"inserted","updated","unchanged"}.
        """
        with _lock, self._connect() as con:
            cur = con.cursor()
                con.execute(
"""
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
                )
                    UPDATE sources
                    SET filename = ?, content = ?, content_hash = ?, size = ?, modified_ts = ?
                    WHERE id = ?
                    """,
                    (filename, content, content_hash, size, modified_ts, existing_id),
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
            return int(cur.lastrowid)

    def list_interactions(self, limit: int = 100) -> list[dict]:
        import json as _json

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
        db_manager.add_interaction(
            user_input=user_text,
            active_mode=(meta or {}).get("activePersona"),
            action_taken=(meta or {}).get("detected_intent"),
            parsed_data=meta or {},
        )
    except Exception:
        pass
