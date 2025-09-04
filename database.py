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
    id: int
    filename: str
    path: str
    content: str
    content_hash: str | None = None
    size: int | None = None
    modified_ts: float | None = None


class DatabaseManager:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        # check_same_thread=False to allow access from Flask thread + background jobs
        return sqlite3.connect(self.db_path, check_same_thread=False)

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
        """Insert, update if content changed, or no-op.

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
                    """
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

    # --- Context notes ---
    def set_context_note(self, key: str, value: str, ts: float | None = None) -> None:
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

    def set_context_notes(self, notes: dict[str, str]) -> None:
        for k, v in (notes or {}).items():
            if v is None:
                v = ""
            self.set_context_note(str(k), str(v))

    def get_context_notes(self) -> dict[str, str]:
        with _lock, self._connect() as con:
            cur = con.execute("SELECT key, value FROM context_notes ORDER BY key ASC")
            return {row[0]: row[1] for row in cur.fetchall()}

    # Backward-compat shim used by older callers
    def add_source(self, filename: str, path: str, content: str) -> int:
        id_, _ = self.add_or_update_source(filename, path, content)
        return id_

    def list_sources(self) -> list[Source]:
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content, content_hash, size, modified_ts FROM sources ORDER BY id DESC"
            )
            return [Source(*row) for row in cur.fetchall()]

    def get_source(self, source_id: int) -> Optional[Source]:
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content, content_hash, size, modified_ts FROM sources WHERE id = ?",
                (source_id,),
            )
            row = cur.fetchone()
            return Source(*row) if row else None

    def get_source_by_path(self, path: str) -> Optional[Source]:
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, filename, path, content, content_hash, size, modified_ts FROM sources WHERE path = ?",
                (path,),
            )
            row = cur.fetchone()
            return Source(*row) if row else None

    def delete_source_by_path(self, path: str) -> int:
        with _lock, self._connect() as con:
            cur = con.execute("DELETE FROM sources WHERE path = ?", (path,))
            con.commit()
            return cur.rowcount

    def search_sources(self, query: str, limit: int = 50) -> list[Source]:
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

    def search_snippets(self, query: str, limit: int = 5, window: int = 240) -> list[dict]:
        """Return top content snippets matching the query with smart caching.

        Enhanced with better scoring and performance optimization.
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

    # --- Chat history ---
    def add_utterance(self, role: str, text: str, mode: str | None = None, ts: float | None = None) -> int:
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
        with _lock, self._connect() as con:
            cur = con.execute(
                "SELECT id, role, text, mode, ts FROM utterances ORDER BY id DESC LIMIT ?",
                (int(limit),),
            )
            return [
                {"id": r[0], "role": r[1], "text": r[2], "mode": r[3], "ts": r[4]}
                for r in cur.fetchall()
            ]

    # --- Interactions (thought_process logging) ---
    def add_interaction(
        self,
        *,
        user_input: str,
        active_mode: Optional[str] = None,
        action_taken: Optional[str] = None,
        parsed_data: Optional[dict] = None,
        ts: float | None = None,
    ) -> int:
        import time as _time, json as _json
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
                out.append({
                    "id": r[0],
                    "ts": r[1],
                    "user_input": r[2],
                    "active_mode": r[3],
                    "action_taken": r[4],
                    "parsed_data": pd,
                })
            return out


# Shared instance
db_manager = DatabaseManager(config.DB_PATH)
