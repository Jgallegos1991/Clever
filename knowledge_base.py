"""
<<<<<<< HEAD
Knowledge Base Module - Centralized data management for Clever AI

Why: Provides advanced database operations beyond basic DatabaseManager including
chat history, knowledge sources, content chunks, user preferences, and personality
state management. Enables Clever to build comprehensive memory and learning
capabilities while maintaining thread-safe operations and single database architecture.
Where: Used by app.py for chat interactions, evolution_engine for learning analysis,
sync modules for knowledge ingestion, and persona.py for context retrieval. Acts as
high-level database API layer above DatabaseManager for specialized Clever operations.
How: Extends DatabaseManager functionality with specialized tables and operations
for Clever's specific data needs including interaction logging, content search,
preference management, and personality tracking using centralized DB_PATH configuration.

Connects to:
    - database.py: Uses centralized DatabaseManager for all database operations
    - config.py: Uses DB_PATH for single database configuration  
    - app.py: Chat history logging, context retrieval, and user preference management
    - evolution_engine.py: Knowledge storage, interaction analysis, and personality state tracking
    - persona.py: Context building and knowledge-aware response generation
    - sync modules: Knowledge source registration and content chunk management
    - nlp_processor.py: Stores processed keywords, entities, and analysis results
"""

=======
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
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
import json
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

<<<<<<< HEAD
from database import DatabaseManager
import config

# Thread-safe database operations - reuse from DatabaseManager
_db_lock = threading.RLock()

# Global database instance
_db_manager = None

def init_db() -> bool:
    """
    Initialize the knowledge base database with extended tables
    
    Why: Creates specialized tables for chat history, knowledge sources, user
    preferences, and personality state that extend beyond basic DatabaseManager
    functionality for comprehensive Clever AI memory and learning.
    Where: Called at module import to ensure database schema is ready for
    knowledge base operations used by app.py and evolution_engine.py.
    How: Uses centralized DatabaseManager to create tables with proper schema
    for advanced Clever AI functionality while maintaining single DB architecture.
    
    Returns:
        bool: True if initialization successful, False otherwise
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe database operations
        - config.py: Uses centralized DB_PATH configuration
    """
    global _db_manager
    
    try:
        with _db_lock:
            # Use centralized DatabaseManager - no direct sqlite3 connections
            _db_manager = DatabaseManager(config.DB_PATH)
            
            # Use DatabaseManager's connection for table creation
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
                
                # Create interactions table for chat history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    clever_response TEXT NOT NULL,
                    intent_detected TEXT,
                    sentiment_compound REAL,
                    nlp_analysis TEXT
                )
            ''')
=======
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
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return True
            
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False

def log_interaction(user_message: str, clever_response: str, intent_detected: str = None,
                   sentiment_compound: float = None, nlp_analysis: Dict = None) -> int:
    """
<<<<<<< HEAD
    Log a chat interaction to the knowledge base
    
    Why: Stores chat interactions for learning, memory, and conversation history
    that enables Clever to build context and improve responses over time.
    Where: Called by app.py after each user interaction to maintain complete
    conversation history and enable evolution_engine learning.
    How: Uses centralized DatabaseManager to insert interaction data into the
    interactions table with structured metadata for NLP analysis.
    
    Args:
        user_message: The user's input message
        clever_response: Clever's generated response
        intent_detected: Optional detected intent category
        sentiment_compound: Optional sentiment score [-1.0, 1.0]
        nlp_analysis: Optional dictionary of NLP analysis results
        
    Returns:
        int: Interaction ID if successful, -1 if failed
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe database operations
        - app.py: Receives interaction data from main application flow
        - evolution_engine.py: Provides data for learning analysis
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
            
                # Use the existing schema with user_input and action_taken columns
                cursor.execute('''
                    INSERT INTO interactions 
                    (timestamp, user_input, action_taken, active_mode, parsed_data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    user_message,
                    clever_response,  # Store response in action_taken
                    intent_detected or 'chat',  # Store intent in active_mode
                    json.dumps({
                        'sentiment_compound': sentiment_compound,
                        'nlp_analysis': nlp_analysis
                    }) if (sentiment_compound is not None or nlp_analysis) else None
                ))
            
            interaction_id = cursor.lastrowid
            conn.commit()
            
            return interaction_id
=======
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
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
    except Exception as e:
        print(f"Failed to log interaction: {e}")
        return -1

def get_recent_interactions(limit: int = 10) -> List[Dict]:
<<<<<<< HEAD
    """
    Retrieve recent chat interactions from the knowledge base
    
    Why: Provides conversation history for context building and memory recall
    that enables Clever to maintain conversation continuity and reference
    previous interactions for more coherent responses.
    Where: Used by app.py for context building and evolution_engine for
    analyzing interaction patterns and learning opportunities.
    How: Queries the interactions table using DatabaseManager with proper
    field mapping to return structured conversation history data.
    
    Args:
        limit: Maximum number of recent interactions to retrieve
        
    Returns:
        List[Dict]: List of interaction dictionaries with conversation data
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe database queries
        - app.py: Provides context for response generation
        - evolution_engine.py: Supplies data for learning analysis
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
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
                
                return interactions
                
=======
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
            
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    except Exception as e:
        print(f"Failed to get recent interactions: {e}")
        return []

def add_knowledge_source(filename: str, file_path: str = None, content_type: str = None,
                        file_size: int = None, content_hash: str = None) -> int:
<<<<<<< HEAD
    """
    Add a knowledge source to the database
    
    Why: Tracks ingested files and documents to build Clever's knowledge base
    and prevent duplicate processing while maintaining source attribution
    for generated responses that reference learned material.
    Where: Used by pdf_ingestor.py and file_ingestor.py during content
    ingestion to register new sources before content chunking.
    How: Inserts source metadata into knowledge_sources table using
    DatabaseManager with timestamp and hash tracking for deduplication.
    
    Args:
        filename: Name of the source file
        file_path: Optional full path to source file
        content_type: Optional MIME type or file type
        file_size: Optional file size in bytes
        content_hash: Optional hash for duplicate detection
        
    Returns:
        int: Source ID if successful, -1 if failed
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe operations
        - pdf_ingestor.py: Registers PDF sources during ingestion
        - file_ingestor.py: Registers text file sources during ingestion
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Add a knowledge source to the database"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return source_id
            
    except Exception as e:
        print(f"Failed to add knowledge source: {e}")
        return -1

def add_content_chunk(source_id: int, chunk_index: int, content: str,
                     keywords: List[str] = None, entities: List[str] = None) -> int:
<<<<<<< HEAD
    """
    Add a content chunk to the database for a knowledge source
    
    Why: Breaks down large documents into searchable chunks with extracted
    keywords and entities to enable efficient retrieval and context-aware
    responses based on ingested knowledge.
    Where: Called by ingestor modules after processing documents to store
    processed content chunks with NLP-extracted metadata for retrieval.
    How: Stores content chunks with JSON-serialized keywords and entities
    using DatabaseManager, linked to parent source via foreign key.
    
    Args:
        source_id: ID of the parent knowledge source
        chunk_index: Index of this chunk within the source
        content: The text content of the chunk
        keywords: Optional list of extracted keywords
        entities: Optional list of extracted entities
        
    Returns:
        int: Chunk ID if successful, -1 if failed
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe operations
        - nlp_processor.py: Receives processed keywords and entities
        - ingestor modules: Stores processed content chunks
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Add a content chunk to the database"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return chunk_id
            
    except Exception as e:
        print(f"Failed to add content chunk: {e}")
        return -1

def search_content(query: str, limit: int = 5) -> List[Dict]:
<<<<<<< HEAD
    """
    Search content chunks for relevant information
    
    Why: Enables Clever to find and reference relevant knowledge from ingested
    documents to provide informed responses based on learned material rather
    than relying solely on pre-trained knowledge.
    Where: Used by app.py during response generation when user queries might
    benefit from referencing ingested documents and knowledge sources.
    How: Performs text search across content chunks, keywords, and entities
    using DatabaseManager with JOIN to include source attribution.
    
    Args:
        query: Search query text to match against content and metadata
        limit: Maximum number of results to return
        
    Returns:
        List[Dict]: Search results with content, metadata, and source info
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe search queries
        - app.py: Provides knowledge retrieval for response generation
        - persona.py: Supplies context for knowledge-aware responses
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Search content chunks for relevant information"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
            
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            return results
            
    except Exception as e:
        print(f"Failed to search content: {e}")
        return []

def get_user_preference(key: str) -> Optional[str]:
<<<<<<< HEAD
    """
    Retrieve a user preference value
    
    Why: Enables personalization by storing and retrieving Jay's preferences
    for response style, behavior settings, and custom configurations that
    make Clever more tailored to the single user's needs.
    Where: Used by app.py and persona.py to customize behavior based on
    stored preferences, ensuring consistent personalized experience.
    How: Queries user_preferences table using DatabaseManager to retrieve
    preference value by key for runtime behavior customization.
    
    Args:
        key: Preference key identifier
        
    Returns:
        Optional[str]: Preference value if found, None otherwise
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe preference queries
        - app.py: Retrieves preferences for behavior customization
        - persona.py: Adapts response generation based on user preferences
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
            
            cursor.execute('SELECT preference_value FROM user_preferences WHERE preference_key = ?', (key,))
            result = cursor.fetchone()
=======
    """Get a user preference value"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('SELECT preference_value FROM user_preferences WHERE preference_key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return result[0] if result else None
            
    except Exception as e:
        print(f"Failed to get user preference: {e}")
        return None

def set_user_preference(key: str, value: str) -> bool:
<<<<<<< HEAD
    """
    Set a user preference value
    
    Why: Stores Jay's preferences and settings to enable personalization
    and consistent behavior across sessions, allowing Clever to adapt
    to user preferences and maintain customized experience.
    Where: Used by app.py when user configures settings or when persona.py
    learns preferred interaction styles during conversations.
    How: Uses INSERT OR REPLACE with DatabaseManager to update user_preferences
    table with timestamp tracking for preference management.
    
    Args:
        key: Preference key identifier
        value: Preference value to store
        
    Returns:
        bool: True if successful, False otherwise
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe preference updates
        - app.py: Stores user configuration changes
        - persona.py: Learns and stores interaction preferences
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Set a user preference value"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, last_updated)
                VALUES (?, ?, ?)
            ''', (key, value, datetime.now().isoformat()))
            
            conn.commit()
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return True
            
    except Exception as e:
        print(f"Failed to set user preference: {e}")
        return False

def update_personality_state(emotional_state: str, mood_score: float, interaction_count: int) -> bool:
<<<<<<< HEAD
    """
    Update Clever's personality state
    
    Why: Tracks Clever's evolving personality and emotional state to enable
    consistent personality development and mood-aware responses that create
    a more engaging and empathetic user experience.
    Where: Used by evolution_engine.py during learning analysis and by
    persona.py to adjust response generation based on current personality state.
    How: Updates personality_state table using DatabaseManager with fixed ID
    for singleton personality tracking with timestamp for state evolution.
    
    Args:
        emotional_state: Current emotional state description
        mood_score: Numerical mood score for quantitative tracking
        interaction_count: Current total interaction count
        
    Returns:
        bool: True if successful, False otherwise
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe state updates
        - evolution_engine.py: Updates personality based on learning analysis
        - persona.py: Retrieves state for mood-aware response generation
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Update Clever's personality state"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            cursor.execute('''
                INSERT OR REPLACE INTO personality_state 
                (id, emotional_state, mood_score, interaction_count, last_updated)
                VALUES (1, ?, ?, ?, ?)
            ''', (emotional_state, mood_score, interaction_count, datetime.now().isoformat()))
            
            conn.commit()
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return True
            
    except Exception as e:
        print(f"Failed to update personality state: {e}")
        return False

def get_personality_state() -> Optional[Dict]:
<<<<<<< HEAD
    """
    Retrieve Clever's current personality state
    
    Why: Provides current personality and emotional state data for mood-aware
    response generation and personality consistency across interactions,
    enabling Clever to maintain coherent character development.
    Where: Used by persona.py for response generation and evolution_engine.py
    for personality analysis and development tracking.
    How: Queries personality_state table using DatabaseManager for singleton
    personality record with structured state data return.
    
    Returns:
        Optional[Dict]: Personality state data if available, None otherwise
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe state queries
        - persona.py: Retrieves state for personality-aware responses
        - evolution_engine.py: Analyzes personality development patterns
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
            
            cursor.execute('SELECT emotional_state, mood_score, interaction_count, last_updated FROM personality_state WHERE id = 1')
            result = cursor.fetchone()
=======
    """Get Clever's current personality state"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
            
            cursor.execute('SELECT emotional_state, mood_score, interaction_count, last_updated FROM personality_state WHERE id = 1')
            result = cursor.fetchone()
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
<<<<<<< HEAD
    """
    Log a system performance or behavior metric
    
    Why: Tracks system performance, behavior patterns, and operational metrics
    to enable monitoring, debugging, and performance optimization for
    continuous improvement of Clever's operation.
    Where: Used by debug_config.py for performance tracking and health_monitor.py
    for system status monitoring with metric aggregation.
    How: Inserts metric data into system_metrics table using DatabaseManager
    with JSON serialization for complex metric data structures.
    
    Args:
        metric_name: Name/identifier of the metric being logged
        metric_value: Numerical value of the metric
        metric_data: Optional additional metric metadata
        
    Returns:
        bool: True if successful, False otherwise
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe metric logging
        - debug_config.py: Logs performance and debugging metrics
        - health_monitor.py: Records system health and status metrics
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Log a system metric"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
<<<<<<< HEAD
=======
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
            return True
            
    except Exception as e:
        print(f"Failed to log system metric: {e}")
        return False

def get_database_stats() -> Dict[str, Any]:
<<<<<<< HEAD
    """
    Retrieve comprehensive database statistics
    
    Why: Provides system monitoring data for database usage, table sizes,
    and storage metrics to enable performance monitoring and capacity
    planning for Clever's knowledge and interaction storage.
    Where: Used by health_monitor.py for system status reporting and
    debug_config.py for performance analysis and troubleshooting.
    How: Queries table counts across all knowledge base tables using
    DatabaseManager and calculates database file size for storage metrics.
    
    Returns:
        Dict[str, Any]: Database statistics including table counts and file size
        
    Connects to:
        - database.py: Uses DatabaseManager for thread-safe statistics queries
        - health_monitor.py: Reports database health and usage metrics
        - debug_config.py: Provides debugging and performance data
    """
    try:
        with _db_lock:
            with _db_manager._connect() as conn:
                cursor = conn.cursor()
=======
    """Get database statistics"""
    try:
        with _db_lock:
            conn = sqlite3.connect("clever.db")
            cursor = conn.cursor()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            
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
            
<<<<<<< HEAD
            # Database file size using centralized config
            import os
            if os.path.exists(config.DB_PATH):
                stats['database_size_mb'] = os.path.getsize(config.DB_PATH) / (1024 * 1024)
            
=======
            # Database file size
            import os
            if os.path.exists("clever.db"):
                stats['database_size_mb'] = os.path.getsize("clever.db") / (1024 * 1024)
            
            conn.close()
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            return stats
            
    except Exception as e:
        print(f"Failed to get database stats: {e}")
        return {}

<<<<<<< HEAD
# Initialize database on import - no parameters needed, uses config.DB_PATH
=======
# Initialize database on import
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
init_db()
