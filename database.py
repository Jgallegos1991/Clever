import sqlite3
import threading
import config
import os

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        self.db_path = config.DATABASE_NAME
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor() # Cursor is created once here
            self.db_lock = threading.Lock()
            self._ensure_tables()
            print("✅ DatabaseManager initialized successfully.")
            self._initialized = True
        except sqlite3.Error as e:
            print(f"❌ Error initializing database: {e}")
            self.conn, self.cursor, self._initialized = None, None, False

    def _ensure_tables(self):
        if not self.conn: return
        with self.db_lock:
            try:
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS sources (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, filepath TEXT NOT NULL UNIQUE, content TEXT, uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY AUTOINCREMENT, fact_key TEXT NOT NULL UNIQUE, fact_value TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY AUTOINCREMENT, user_message TEXT NOT NULL, ai_response TEXT NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                self.cursor.execute('''CREATE TABLE IF NOT EXISTS system_state (key TEXT PRIMARY KEY, value TEXT NOT NULL)''')
                self.conn.commit()
                print("Database tables ensured.")
            except sqlite3.Error as e:
                print(f"Error creating tables: {e}")

    def close(self):
        if self.conn:
            with self.db_lock:
                try: self.conn.close(); print("Database connection closed.")
                except sqlite3.Error as e: print(f"Error closing database connection: {e}")
            self.conn, self.cursor, DatabaseManager._instance, self._initialized = None, None, None, False

    def add_source(self, filename, filepath, content):
        if not self.conn: return
        with self.db_lock:
            try:
                self.cursor.execute("INSERT OR REPLACE INTO sources (filename, filepath, content) VALUES (?, ?, ?)", (filename, filepath, content))
                self.conn.commit()
            except sqlite3.IntegrityError:
                self.cursor.execute("UPDATE sources SET content = ? WHERE filepath = ?", (content, filepath))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error adding source: {e}")

    def get_all_sources(self):
        if not self.conn: return []
        with self.db_lock:
            try:
                self.cursor.row_factory = sqlite3.Row
                self.cursor.execute("SELECT id, filename FROM sources ORDER BY uploaded_at DESC")
                rows = self.cursor.fetchall()
                self.cursor.row_factory = None
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                print(f"Error getting all sources: {e}")
                return []

    def get_source_content_by_id(self, source_id):
        if not self.conn: return None
        with self.db_lock:
            try:
                self.cursor.row_factory = sqlite3.Row
                self.cursor.execute("SELECT content FROM sources WHERE id = ?", (source_id,))
                row = self.cursor.fetchone()
                self.cursor.row_factory = None
                return row['content'] if row else None
            except sqlite3.Error as e:
                print(f"Error getting source content: {e}")
                return None

    def add_fact(self, key, value):
        if not self.conn: return
        with self.db_lock:
            try:
                self.cursor.execute("INSERT OR REPLACE INTO knowledge (fact_key, fact_value) VALUES (?, ?)", (key.lower(), value))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error adding/updating fact: {e}")

    def get_fact(self, key):
        if not self.conn: return None
        with self.db_lock:
            try:
                # --- THIS IS THE FIX, APPLIED TO THE CURSOR ---
                self.cursor.row_factory = sqlite3.Row
                self.cursor.execute("SELECT fact_value FROM knowledge WHERE fact_key = ?", (key.lower(),))
                row = self.cursor.fetchone()
                self.cursor.row_factory = None
                return row['fact_value'] if row else None
            except sqlite3.Error as e:
                print(f"Error getting fact: {e}")
                return None

    def add_conversation(self, user_msg, ai_msg):
        if not self.conn: return
        with self.db_lock:
            try:
                self.cursor.execute("INSERT INTO conversations (user_message, ai_response) VALUES (?, ?)", (user_msg, ai_msg))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error adding conversation: {e}")

    def get_recent_conversations(self, limit=10):
        if not self.conn: return []
        with self.db_lock:
            try:
                self.cursor.row_factory = sqlite3.Row
                self.cursor.execute("SELECT user_message, ai_response FROM conversations ORDER BY timestamp DESC LIMIT ?", (limit,))
                rows = self.cursor.fetchall()
                self.cursor.row_factory = None
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                print(f"Error getting recent conversations: {e}")
                return []
            
    def set_system_mode(self, mode_name):
        if not self.conn: return
        with self.db_lock:
            try:
                self.cursor.execute("INSERT OR REPLACE INTO system_state (key, value) VALUES (?, ?)", ('system_mode', mode_name))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error setting system mode: {e}")
    
    def get_system_mode(self):
        if not self.conn: return config.DEFAULT_MODE
        with self.db_lock:
            try:
                self.cursor.execute("SELECT value FROM system_state WHERE key = ?", ('system_mode',))
                row = self.cursor.fetchone()
                return row[0] if row else config.DEFAULT_MODE
            except sqlite3.Error as e:
                print(f"Error getting system mode: {e}")
                return config.DEFAULT_MODE

db_manager = DatabaseManager()