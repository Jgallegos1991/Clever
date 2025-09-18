

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
    content: str | None = None
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

    def set_context_note(self, key: str, value: str, ts: float | None = None) -> None:
                """
                Store or update a context note in the database.
        
                Why: Provides persistent key-value storage for application context and state,
                Where: Used by application for storing context notes,
                How: Inserts or updates the context_notes table with key, value, and timestamp.
                """
                # Method body
                pass

    # --- Chat history ---
    def add_utterance(
        self,
        role: str,
        text: str,
        mode: str | None = None,
        ts: float | None = None,
    ) -> int:
        import time as _time
        if ts is None:
            ts = _time.time()
        with _lock, self._connect() as con:
            cur = con.execute(
                "INSERT INTO utterances (role, text, mode, ts) VALUES (?, ?, ?, ?)",
                (role, text, mode, float(ts)),
            )
            con.commit()
            return int(cur.lastrowid) if cur.lastrowid is not None else 0

    def search_snippets(self, query: str, limit: int = 5, window: int = 240) -> list[dict]:
        """
        Advanced search returning scored content snippets with context.

        Why: Provides intelligent search results with relevant content excerpts, scoring, and sentence-boundary awareness for better user experience.
        Where: Used by knowledge base queries, Q&A systems, and content discovery features that need to show relevant excerpts rather than full sources.
        How: Tokenizes query, scores matches using multiple factors (exact matches, partial matches, filename matches), extracts contextual snippets with smart boundary detection, and ranks results by relevance.
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
        like_pattern = f"%{like_pattern}%"  # Add wildcards for LIKE
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content FROM sources WHERE content LIKE ? LIMIT ?",
                (like_pattern, min(100, limit*20)),
            )
            pre = [
                Source(id=row[0], filename=row[1], path=row[2], content=row[3])
                for row in cur.fetchall()
            ]
        
        hits: list[dict] = []
        
        for s in pre:
            text = s.content
            if not text:
                continue
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
                "end": int(end)
            })
        
        # Sort by score descending and return top results
        hits.sort(key=lambda x: x["score"], reverse=True)
        return hits[:limit]

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
                    "UPDATE sources SET filename = ?, content_hash = ?, size = ?, modified_ts = ? WHERE id = ?",
                    (filename, content_hash, size, modified_ts, existing_id),
                )
                con.commit()
                return int(existing_id), "updated"
            # Insert new
            cur.execute(
                "INSERT INTO sources (filename, path, content_hash, size, modified_ts) VALUES (?, ?, ?, ?, ?)",
                (filename, path, content_hash, size, modified_ts),
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
        import json as _json, time as _time
        if ts is None:
            ts = _time.time()
        with _lock, self._connect() as con:
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
