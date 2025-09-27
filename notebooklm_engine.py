"""
notebooklm_engine.py - Minimal Document Analysis System

Why: Provides basic document analysis for Clever's knowledge system
Where: Integrates with database for document storage  
How: Simple document processing without complex dependencies
"""

from typing import Dict, List, Any, Optional
import json
from database import DatabaseManager
from debug_config import get_debugger
import config


class NotebookLMEngine:
    """
    Minimal Document Analysis Engine
    
    Why: Provides basic document analysis capabilities for Clever
    Where: Called by memory system for document processing
    How: Simple analysis without heavy ML dependencies
    """
    
    def __init__(self, db_path: str = None):
        """Initialize with basic database connection"""
        self.db_path = db_path or config.DB_PATH
        self.db = DatabaseManager(self.db_path)
        self.debugger = get_debugger()
        
        # Initialize basic schema
        self._init_schema()
    
    def _init_schema(self):
        """Initialize minimal document analysis schema"""
        with self.db._lock, self.db._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_analysis (
                    source_id INTEGER PRIMARY KEY,
                    word_count INTEGER,
                    summary TEXT,
                    created_at REAL,
                    FOREIGN KEY (source_id) REFERENCES sources(id)
                )
            """)
            conn.commit()

    def analyze_document(self, source_id: int) -> Optional[Dict[str, Any]]:
        """Basic document analysis"""
        try:
            with self.db._lock, self.db._connect() as conn:
                cursor = conn.execute(
                    "SELECT id, filename, content FROM sources WHERE id = ?",
                    (source_id,)
                )
                row = cursor.fetchone()
            
            if not row:
                return None
                
            doc_id, filename, content = row
            word_count = len(content.split())
            summary = content[:200] + "..." if len(content) > 200 else content
            
            # Store analysis
            with self.db._lock, self.db._connect() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO document_analysis 
                    (source_id, word_count, summary, created_at)
                    VALUES (?, ?, ?, ?)
                """, (doc_id, word_count, summary, 1000))
                conn.commit()
            
            return {
                'doc_id': doc_id,
                'filename': filename, 
                'word_count': word_count,
                'summary': summary
            }
        
        except Exception as e:
            self.debugger.error('notebooklm.analyze_document', f"Analysis failed: {e}")
            return None
