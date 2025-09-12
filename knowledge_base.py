"""
Knowledge Base Module - Extended database functionality for content management.

Why: Provides high-level interface for knowledge management operations including
     chat history, source tracking, user preferences, and system metrics
     while building on the core DatabaseManager infrastructure.

Where: Used by chat interface, content ingestion systems, analytics modules,
       and any component requiring knowledge-oriented database operations.

How: Wraps DatabaseManager with domain-specific methods for interactions,
     knowledge sources, preferences, and system state management using
     centralized configuration and consistent database access patterns.
"""

import sqlite3
import json
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

import config
from database import DatabaseManager, Source

# Thread-safe database operations
_db_lock = threading.RLock()

# Global database instance using centralized configuration
_db_manager = None


def init_db(db_path: str | None = None) -> bool:
    """
    Initialize knowledge base database with extended schema.
    
    Why: Sets up additional database tables and functionality beyond core
         DatabaseManager for knowledge-specific operations and analytics.
    
    Where: Called during application startup to ensure knowledge base
           schema exists and is properly configured.
    
    How: Uses centralized config.DB_PATH by default, creates extended tables
         for interactions, sources, preferences, and metrics with proper
         constraints and relationships.
    """
    global _db_manager
    
    if db_path is None:
        db_path = config.DB_PATH
        
    with _db_lock:
        # Initialize core database manager
        _db_manager = DatabaseManager(db_path)
        
        # Create extended knowledge base tables
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enhanced interactions table for chat history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT NOT NULL,
                clever_response TEXT NOT NULL,
                intent_detected TEXT,
                sentiment_compound REAL,
                nlp_analysis TEXT
            )
        ''')
            
            # Create knowledge sources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT,
                    content_type TEXT,
                    processed_date TEXT,
                    file_size INTEGER,
                    content_hash TEXT
                )
            ''')
            
            # Create content chunks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER,
                    chunk_index INTEGER,
                    content TEXT NOT NULL,
                    embedding_vector TEXT,
                    keywords TEXT,
                    entities TEXT,
                    FOREIGN KEY (source_id) REFERENCES knowledge_sources (id)
                )
            ''')
            
            # Create user preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    preference_key TEXT UNIQUE NOT NULL,
                    preference_value TEXT,
                    last_updated TEXT
                )
            ''')
            
            # Create personality state table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personality_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emotional_state TEXT,
                    mood_score REAL,
                    interaction_count INTEGER,
                    last_updated TEXT
                )
            ''')
            
            # Create system metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    metric_data TEXT,
                    timestamp TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            return True
            
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False

def log_interaction(user_message: str, clever_response: str, intent_detected: str = None,
                   sentiment_compound: float = None, nlp_analysis: Dict = None) -> int:
    """
    Log a chat interaction with analytics metadata.
    
    Why: Records user conversations with sentiment analysis and intent detection
         for learning algorithms, conversation analytics, and response improvement.
    
    Where: Used by chat interface and conversation handlers to track all
           interactions for evolution engine analysis and pattern recognition.
    
    How: Stores interaction data in standardized database format with JSON
         metadata for sentiment and NLP analysis results using centralized DB.
    """
    try:
        with _db_lock:
            if _db_manager is None:
                init_db()
            
            # Use DatabaseManager's add_interaction method
            return _db_manager.add_interaction(
                user_input=user_message,
                active_mode=intent_detected or 'chat',
                action_taken=clever_response,
                parsed_data={
                    'sentiment_compound': sentiment_compound,
                    'nlp_analysis': nlp_analysis
                } if (sentiment_compound is not None or nlp_analysis) else None
            )
            
    except Exception as e:
        print(f"Failed to log interaction: {e}")
        return -1

def get_recent_interactions(limit: int = 10) -> List[Dict]:
    """Get recent chat interactions"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, user_input, action_taken, active_mode, parsed_data
                FROM interactions 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            interactions = []
            for row in cursor.fetchall():
                timestamp, user_input, action_taken, active_mode, parsed_data_json = row
                
                parsed_data = {}
                if parsed_data_json:
                    try:
                        parsed_data = json.loads(parsed_data_json)
                    except:
                        pass
                
                interactions.append({
                    'timestamp': timestamp,
                    'user_message': user_input,  # Map to expected field name
                    'clever_response': action_taken,  # Map to expected field name
                    'intent_detected': active_mode,
                    'sentiment_compound': parsed_data.get('sentiment_compound'),
                    'nlp_analysis': parsed_data.get('nlp_analysis')
                })
            
            conn.close()
            return interactions
            
    except Exception as e:
        print(f"Failed to get recent interactions: {e}")
        return []

def add_knowledge_source(filename: str, file_path: str = None, content_type: str = None,
                        file_size: int = None, content_hash: str = None) -> int:
    """Add a knowledge source to the database"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO knowledge_sources 
                (filename, file_path, content_type, processed_date, file_size, content_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                filename,
                file_path,
                content_type,
                datetime.now().isoformat(),
                file_size,
                content_hash
            ))
            
            source_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return source_id
            
    except Exception as e:
        print(f"Failed to add knowledge source: {e}")
        return -1

def add_content_chunk(source_id: int, chunk_index: int, content: str,
                     keywords: List[str] = None, entities: List[str] = None) -> int:
    """Add a content chunk to the database"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO content_chunks 
                (source_id, chunk_index, content, keywords, entities)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                source_id,
                chunk_index,
                content,
                json.dumps(keywords) if keywords else None,
                json.dumps(entities) if entities else None
            ))
            
            chunk_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return chunk_id
            
    except Exception as e:
        print(f"Failed to add content chunk: {e}")
        return -1

def search_content(query: str, limit: int = 5) -> List[Dict]:
    """Search content chunks for relevant information"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            # Simple text search - in production, would use embeddings
            cursor.execute('''
                SELECT cc.content, cc.keywords, cc.entities, ks.filename
                FROM content_chunks cc
                JOIN knowledge_sources ks ON cc.source_id = ks.id
                WHERE cc.content LIKE ? OR cc.keywords LIKE ? OR cc.entities LIKE ?
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            results = []
            for row in cursor.fetchall():
                content, keywords_json, entities_json, filename = row
                
                keywords = []
                entities = []
                try:
                    if keywords_json:
                        keywords = json.loads(keywords_json)
                    if entities_json:
                        entities = json.loads(entities_json)
                except:
                    pass
                
                results.append({
                    'content': content,
                    'keywords': keywords,
                    'entities': entities,
                    'source_filename': filename
                })
            
            conn.close()
            return results
            
    except Exception as e:
        print(f"Failed to search content: {e}")
        return []

def get_user_preference(key: str) -> Optional[str]:
    """Get a user preference value"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('SELECT preference_value FROM user_preferences WHERE preference_key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
    except Exception as e:
        print(f"Failed to get user preference: {e}")
        return None

def set_user_preference(key: str, value: str) -> bool:
    """Set a user preference value"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, last_updated)
                VALUES (?, ?, ?)
            ''', (key, value, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return True
            
    except Exception as e:
        print(f"Failed to set user preference: {e}")
        return False

def update_personality_state(emotional_state: str, mood_score: float, interaction_count: int) -> bool:
    """Update Clever's personality state"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO personality_state 
                (id, emotional_state, mood_score, interaction_count, last_updated)
                VALUES (1, ?, ?, ?, ?)
            ''', (emotional_state, mood_score, interaction_count, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return True
            
    except Exception as e:
        print(f"Failed to update personality state: {e}")
        return False

def get_personality_state() -> Optional[Dict]:
    """Get Clever's current personality state"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('SELECT emotional_state, mood_score, interaction_count, last_updated FROM personality_state WHERE id = 1')
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'emotional_state': result[0],
                    'mood_score': result[1],
                    'interaction_count': result[2],
                    'last_updated': result[3]
                }
            
            return None
            
    except Exception as e:
        print(f"Failed to get personality state: {e}")
        return None

def log_system_metric(metric_name: str, metric_value: float, metric_data: Dict = None) -> bool:
    """Log a system metric"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_metrics (metric_name, metric_value, metric_data, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                metric_name,
                metric_value,
                json.dumps(metric_data) if metric_data else None,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
    except Exception as e:
        print(f"Failed to log system metric: {e}")
        return False

def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            stats = {}
            
            # Table counts
            tables = ['interactions', 'knowledge_sources', 'content_chunks', 'user_preferences', 'personality_state', 'system_metrics']
            for table in tables:
                try:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    count = cursor.fetchone()[0]
                    stats[f'{table}_count'] = count
                except:
                    stats[f'{table}_count'] = 0
            
            # Database file size
            import os
            if os.path.exists("clever.db"):
                stats['database_size_mb'] = os.path.getsize("clever.db") / (1024 * 1024)
            
            conn.close()
            return stats
            
    except Exception as e:
        print(f"Failed to get database stats: {e}")
        return {}

# Initialize database on import
init_db()
