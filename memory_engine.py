"""
Advanced Memory Engine for Clever AI

Why: Creates persistent, intelligent memory system that learns from every interaction,
builds context awareness, and enables predictive responses for Jay specifically.
Where: Core component connecting all modules for enhanced AI capabilities.
How: Multi-layered memory architecture with semantic understanding, temporal context,
and relationship mapping for continuous learning and adaptation.

Connects to:
    - database.py:
        - `__init__(db_manager)`: Takes a `DatabaseManager` instance for all database operations.
        - `_initialize_memory_schema()`: Creates all memory-related tables (`memory_nodes`, `conversation_context`, etc.).
        - All methods with database interactions use `self.db._execute_query()` which relies on the `DatabaseManager`.
    - persona.py:
        - `generate()` -> `get_contextual_memory()`: The persona engine calls this to fetch relevant memories for generating a response.
        - `generate()` -> `get_conversation_history()`: Called to get recent conversation turns for context.
        - `generate()` -> `predict_preferences()`: Called to suggest the best response mode.
        - `generate()` -> `store_interaction()`: The persona engine calls this after a response is generated to log the full interaction.
    - nlp_processor.py: (Indirectly) The `MemoryContext` object processed by `store_interaction` is created in `persona.py` using the analysis (keywords, entities, sentiment) from the `nlp_processor`.
    - config.py: The `get_memory_engine()` factory function uses `config.DB_PATH` to initialize the `DatabaseManager`.
    - debug_config.py: `get_debugger()` is used for logging throughout the module.
"""
import threading
import json
from datetime import datetime
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from database import DatabaseManager
from debug_config import get_debugger


debugger = get_debugger()


@dataclass
class MemoryContext:
    """
    Context container for memory operations
    
    Why: Structured representation of conversation context
    Where: Used throughout memory system for context tracking
    How: Immutable data class with key context elements
    """
    user_input: str
    timestamp: float
    session_id: str
    mode: str
    sentiment: str
    keywords: List[str]
    entities: List[str]
    response_text: str = ""
    importance_score: float = 0.5
    context_links: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.context_links is None:
            self.context_links = []


@dataclass  
class MemoryNode:
    """
    Individual memory node with relationships
    
    Why: Represents single piece of learned information with connections
    Where: Building blocks of the memory graph system
    How: Contains content, metadata, and relationship links
    """
    id: str
    content: str
    category: str
    importance: float
    created_at: float
    accessed_count: int = 0
    last_accessed: float = 0
    related_nodes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.related_nodes is None:
            self.related_nodes = []
        if self.tags is None:
            self.tags = []


class AdvancedMemoryEngine:
    """
    Advanced memory system with learning and prediction
    
    Why: Provide sophisticated memory capabilities for Jay's AI assistant
    Where: Core memory component used by all AI modules
    How: Multi-layered architecture with semantic understanding, context building,
    temporal awareness, and predictive capabilities
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize advanced memory engine
        
        Why: Set up comprehensive memory system with database persistence
        Where: Called once during system initialization
        How: Initialize database schema, memory structures, and learning components
        
        Connects to:
            - database.py: Persistent storage via DatabaseManager
            - All modules: Memory services for enhanced AI capabilities
        """
        self.db = db_manager
        self._lock = threading.Lock()
        self.session_id = self._generate_session_id()
        self.conversation_buffer = []  # Recent conversation context
        self.semantic_cache = {}  # Cache for semantic similarity
        self.learning_patterns = defaultdict(list)  # Pattern learning
        self.preference_model = {}  # Jay's preferences
        self.context_window = 10  # Number of recent interactions to consider
        
        # Initialize database schema
        self._initialize_memory_schema()
        self._load_preferences()
        
        debugger.info('memory_engine', f'Advanced memory engine initialized with session {self.session_id}')
    
    def _execute_query(self, query: str, params: tuple = ()) -> List[tuple]:
        """
        Execute database query with proper error handling
        
        Why: Provide safe database access with connection management
        Where: Used by all database operations in memory engine
        How: Use DatabaseManager connection with proper locking
        """
        try:
            with self.db._lock, self.db._connect() as con:
                cursor = con.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    con.commit()
                    return []
        except Exception as _e:
            debugger.error('memory_engine', f'Database query failed: {e}')
            raise
    
    def _generate_session_id(self) -> str:
        """
        Generate unique session identifier
        
        Why: Track conversation sessions for temporal context
        Where: Used for session-based memory organization
        How: Create timestamp-based unique ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_component = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        return f"session_{timestamp}_{random_component}"
    
    def _initialize_memory_schema(self):
        """
        Initialize database schema for memory system
        
        Why: Ensure database has all required tables for memory operations
        Where: Called during engine initialization
        How: Create tables if they don't exist with proper indexes
        
        Connects to:
            - database.py: Uses DatabaseManager for schema creation
        """
        with self._lock:
            try:
                # Memory nodes table
                self._execute_query("""
                    CREATE TABLE IF NOT EXISTS memory_nodes (
                        id TEXT PRIMARY KEY,
                        content TEXT NOT NULL,
                        category TEXT,
                        importance REAL DEFAULT 0.5,
                        created_at REAL,
                        accessed_count INTEGER DEFAULT 0,
                        last_accessed REAL DEFAULT 0,
                        tags TEXT,
                        metadata TEXT
                    )
                """)
                
                # Memory relationships table
                self._execute_query("""
                    CREATE TABLE IF NOT EXISTS memory_relationships (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_node TEXT,
                        target_node TEXT,
                        relationship_type TEXT,
                        strength REAL DEFAULT 0.5,
                        created_at REAL,
                        FOREIGN KEY (source_node) REFERENCES memory_nodes (id),
                        FOREIGN KEY (target_node) REFERENCES memory_nodes (id)
                    )
                """)
                
                # Conversation context table
                self._execute_query("""
                    CREATE TABLE IF NOT EXISTS conversation_context (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        user_input TEXT,
                        response_text TEXT,
                        mode TEXT,
                        sentiment TEXT,
                        keywords TEXT,
                        entities TEXT,
                        importance_score REAL,
                        timestamp REAL,
                        context_metadata TEXT
                    )
                """)
                
                # Preferences table  
                self._execute_query("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        category TEXT,
                        confidence REAL DEFAULT 0.5,
                        last_updated REAL
                    )
                """)
                
                # Create indexes for better performance
                self._execute_query("CREATE INDEX IF NOT EXISTS idx_memory_category ON memory_nodes (category)")
                self._execute_query("CREATE INDEX IF NOT EXISTS idx_memory_importance ON memory_nodes (importance DESC)")
                self._execute_query("CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_context (session_id)")
                self._execute_query("CREATE INDEX IF NOT EXISTS idx_conversation_timestamp ON conversation_context (timestamp DESC)")
                
                debugger.info('memory_engine', 'Memory database schema initialized successfully')
                
            except Exception as _e:
                debugger.error('memory_engine', f'Failed to initialize memory schema: {e}')
                raise
    
    def store_interaction(self, context: MemoryContext) -> str:
        """
        Store interaction in memory with full context
        
        Why: Capture and persist every interaction for learning and context building
        Where: Called after each user interaction from app.py
        How: Store conversation data, extract insights, build relationships
        
        Args:
            context: MemoryContext containing interaction details
            
        Returns:
            str: Unique ID of stored interaction
            
        Connects to:
            - app.py: Primary interaction storage
            - persona.py: Response context storage
            - nlp_processor.py: Semantic analysis integration
        """
        with self._lock:
            try:
                # Store conversation context
                context_id = self._store_conversation_context(context)
                
                # Extract and store memory nodes
                self._extract_memory_nodes(context)
                
                # Update conversation buffer
                self.conversation_buffer.append(context)
                if len(self.conversation_buffer) > self.context_window:
                    self.conversation_buffer.pop(0)
                
                # Learn patterns
                self._learn_patterns(context)
                
                # Update preferences
                self._update_preferences(context)
                
                debugger.info('memory_engine', f'Stored interaction with ID: {context_id}')
                return context_id
                
            except Exception as _e:
                debugger.error('memory_engine', f'Failed to store interaction: {e}')
                raise
    
    def _store_conversation_context(self, context: MemoryContext) -> str:
        """
        Store conversation context in database
        
        Why: Persist conversation data for future retrieval and analysis
        Where: Called by store_interaction for data persistence
        How: Insert context data into conversation_context table
        """
        context_metadata = {
            'context_links': context.context_links,
            'session_id': self.session_id
        }
        
        self._execute_query("""
            INSERT INTO conversation_context 
            (session_id, user_input, response_text, mode, sentiment, keywords, 
             entities, importance_score, timestamp, context_metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            context.session_id,
            context.user_input,
            context.response_text,
            context.mode,
            context.sentiment,
            json.dumps(context.keywords),
            json.dumps(context.entities),
            context.importance_score,
            context.timestamp,
            json.dumps(context_metadata)
        ))
        
        # Return the last inserted row ID as string
        return str(self._execute_query("SELECT last_insert_rowid()")[0][0])
    
    def _extract_memory_nodes(self, context: MemoryContext):
        """
        Extract and store memory nodes from interaction
        
        Why: Create persistent knowledge nodes from conversation content
        Where: Called during interaction storage for knowledge extraction
        How: Analyze context for important concepts and create memory nodes
        """
        # Extract important concepts from keywords and entities
        important_concepts = []
        
        # High-value keywords (longer, more specific)
        for keyword in context.keywords:
            if len(keyword) > 4:  # Focus on substantial keywords
                importance = min(0.8, 0.3 + len(keyword) * 0.05)  # Length-based importance
                important_concepts.append((keyword, 'keyword', importance))
        
        # Entities are generally important
        for entity in context.entities:
            important_concepts.append((entity, 'entity', 0.7))
        
        # Store memory nodes
        for concept, category, importance in important_concepts:
            node_id = self._create_memory_node(
                content=concept,
                category=category,
                importance=importance,
                tags=[context.mode, context.sentiment]
            )
            
            # Link to recent nodes if semantic similarity exists
            self._create_semantic_links(node_id, concept)
    
    def _create_memory_node(self, content: str, category: str, importance: float, tags: Optional[List[str]] = None) -> str:
        """
        Create new memory node
        
        Why: Store individual pieces of learned information
        Where: Called during memory extraction and learning
        How: Generate unique ID and store node in database
        """
        if tags is None:
            tags = []
            
        node_id = hashlib.md5(f"{content}_{category}_{time.time()}".encode()).hexdigest()
        
        # Check if similar node already exists
        existing = self._execute_query("""
            SELECT id, importance, accessed_count FROM memory_nodes 
            WHERE content = ? AND category = ?
        """, (content, category))
        
        if existing:
            # Update existing node
            existing_id, existing_importance, accessed_count = existing[0]
            new_importance = min(1.0, existing_importance + importance * 0.1)  # Gradual importance increase
            
            self._execute_query("""
                UPDATE memory_nodes 
                SET importance = ?, accessed_count = ?, last_accessed = ?
                WHERE id = ?
            """, (new_importance, accessed_count + 1, time.time(), existing_id))
            
            return existing_id
        else:
            # Create new node
            self._execute_query("""
                INSERT INTO memory_nodes 
                (id, content, category, importance, created_at, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                node_id, content, category, importance, time.time(),
                json.dumps(tags), json.dumps({})
            ))
            
            return node_id
    
    def _create_semantic_links(self, node_id: str, content: str):
        """
        Create semantic relationships between memory nodes
        
        Why: Build knowledge graph with meaningful connections
        Where: Called during memory node creation
        How: Find similar content and create weighted relationships
        """
        # Find recently created nodes for potential linking
        recent_nodes = self._execute_query("""
            SELECT id, content FROM memory_nodes 
            WHERE id != ? AND created_at > ?
            ORDER BY created_at DESC LIMIT 20
        """, (node_id, time.time() - 3600))  # Last hour
        
        for other_id, other_content in recent_nodes:
            similarity = self._calculate_similarity(content, other_content)
            
            if similarity > 0.3:  # Minimum similarity threshold
                self._create_relationship(node_id, other_id, 'semantic', similarity)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between texts
        
        Why: Determine relationship strength between concepts
        Where: Used for creating memory node relationships
        How: Simple word overlap and length-based similarity
        """
        # Simple similarity based on word overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _create_relationship(self, source_id: str, target_id: str, relationship_type: str, strength: float):
        """
        Create relationship between memory nodes
        
        Why: Build knowledge graph connections
        Where: Called during semantic linking
        How: Store bidirectional relationship in database
        """
        # Check if relationship already exists
        existing = self._execute_query("""
            SELECT strength FROM memory_relationships
            WHERE source_node = ? AND target_node = ? AND relationship_type = ?
        """, (source_id, target_id, relationship_type))
        
        if existing:
            # Update existing relationship strength
            current_strength = existing[0][0]
            new_strength = min(1.0, current_strength + strength * 0.1)
            
            self._execute_query("""
                UPDATE memory_relationships 
                SET strength = ? WHERE source_node = ? AND target_node = ? AND relationship_type = ?
            """, (new_strength, source_id, target_id, relationship_type))
        else:
            # Create new relationship
            self._execute_query("""
                INSERT INTO memory_relationships 
                (source_node, target_node, relationship_type, strength, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (source_id, target_id, relationship_type, strength, time.time()))
    
    def _learn_patterns(self, context: MemoryContext):
        """
        Learn patterns from user interactions
        
        Why: Identify Jay's communication patterns and preferences
        Where: Called during interaction storage
        How: Analyze context for recurring patterns and preferences
        """
        # Learn mode preferences based on input characteristics
        input_length = len(context.user_input.split())
        
        pattern_key = f"input_length_{context.mode}"
        self.learning_patterns[pattern_key].append(input_length)
        
        # Learn sentiment patterns
        sentiment_pattern = f"sentiment_{context.sentiment}_{context.mode}"
        self.learning_patterns[sentiment_pattern].append(time.time())
        
        # Learn keyword preferences
        for keyword in context.keywords:
            keyword_pattern = f"keyword_{keyword}"
            self.learning_patterns[keyword_pattern].append(context.mode)
    
    def _update_preferences(self, context: MemoryContext):
        """
        Update user preferences based on interaction
        
        Why: Build model of Jay's preferences and habits
        Where: Called during interaction storage
        How: Analyze context for preference indicators and update model
        """
        # Update mode preferences
        mode_key = f"preferred_mode_{context.mode}"
        self._update_preference(mode_key, "1", "behavior", 0.1)
        
        # Update sentiment preferences
        if context.sentiment != "neutral":
            sentiment_key = f"response_sentiment_{context.sentiment}"
            self._update_preference(sentiment_key, "positive", "interaction", 0.05)
        
        # Update topic preferences based on keywords
        for keyword in context.keywords[:3]:  # Top 3 keywords only
            topic_key = f"topic_interest_{keyword}"
            self._update_preference(topic_key, "high", "content", 0.03)
    
    def _update_preference(self, key: str, value: str, category: str, confidence_delta: float):
        """
        Update specific user preference
        
        Why: Maintain accurate model of Jay's preferences
        Where: Called by _update_preferences for individual preference updates
        How: Increment confidence and update preference value
        """
        existing = self._execute_query("""
            SELECT confidence FROM user_preferences WHERE key = ?
        """, (key,))
        
        if existing:
            current_confidence = existing[0][0]
            new_confidence = min(1.0, current_confidence + confidence_delta)
            
            self._execute_query("""
                UPDATE user_preferences 
                SET confidence = ?, last_updated = ?
                WHERE key = ?
            """, (new_confidence, time.time(), key))
        else:
            self._execute_query("""
                INSERT INTO user_preferences (key, value, category, confidence, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (key, value, category, confidence_delta, time.time()))
    
    def _load_preferences(self):
        """
        Load existing preferences from database
        
        Why: Initialize preference model with historical data
        Where: Called during engine initialization
        How: Load all preferences into memory for fast access
        """
        try:
            preferences = self._execute_query("""
                SELECT key, value, confidence FROM user_preferences
                WHERE confidence > 0.1
                ORDER BY confidence DESC
            """)
            
            for key, value, confidence in preferences:
                self.preference_model[key] = {
                    'value': value,
                    'confidence': confidence
                }
            
            debugger.info('memory_engine', f'Loaded {len(self.preference_model)} preferences')
            
        except Exception as _e:
            debugger.warning('memory_engine', f'Could not load preferences: {e}')
            self.preference_model = {}
    
    def get_contextual_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve contextually relevant memories
        
        Why: Provide relevant context for response generation
        Where: Called by persona engine for context-aware responses
        How: Search memory nodes and relationships for relevant information
        
        Args:
            query: Search query or current input
            max_results: Maximum number of memory items to return
            
        Returns:
            List of relevant memory items with metadata
            
        Connects to:
            - persona.py: Context retrieval for response generation
        """
        try:
            # Extract keywords from query
            query_keywords = [word.lower() for word in query.split() if len(word) > 2]
            
            relevant_memories = []
            
            # Search memory nodes
            for keyword in query_keywords:
                memories = self._execute_query("""
                    SELECT id, content, category, importance, accessed_count
                    FROM memory_nodes 
                    WHERE LOWER(content) LIKE ? 
                    ORDER BY importance DESC, accessed_count DESC
                    LIMIT ?
                """, (f'%{keyword}%', max_results))
                
                for memory in memories:
                    node_id, content, category, importance, accessed_count = memory
                    
                    # Update access count
                    self._execute_query("""
                        UPDATE memory_nodes 
                        SET accessed_count = ?, last_accessed = ?
                        WHERE id = ?
                    """, (accessed_count + 1, time.time(), node_id))
                    
                    relevant_memories.append({
                        'id': node_id,
                        'content': content,
                        'category': category,
                        'importance': importance,
                        'relevance': importance * (1 + accessed_count * 0.1)
                    })
            
            # Remove duplicates and sort by relevance
            unique_memories = {mem['id']: mem for mem in relevant_memories}
            sorted_memories = sorted(unique_memories.values(), 
                                   key=lambda x: x['relevance'], reverse=True)
            
            return sorted_memories[:max_results]
            
        except Exception as _e:
            debugger.error('memory_engine', f'Failed to retrieve contextual memory: {e}')
            return []
    
    def get_conversation_history(self, session_limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent conversation history
        
        Why: Provide conversation context for response generation
        Where: Called by persona engine for context awareness
        How: Retrieve recent interactions from current and previous sessions
        """
        try:
            history = self._execute_query("""
                SELECT user_input, response_text, mode, sentiment, timestamp
                FROM conversation_context
                ORDER BY timestamp DESC
                LIMIT ?
            """, (session_limit,))
            
            return [{
                'user_input': row[0],
                'response_text': row[1],
                'mode': row[2],
                'sentiment': row[3],
                'timestamp': row[4]
            } for row in history]
            
        except Exception as _e:
            debugger.error('memory_engine', f'Failed to retrieve conversation history: {e}')
            return []
    
    def predict_preferences(self, context: str) -> Dict[str, Any]:
        """
        Predict user preferences for current context
        
        Why: Enable proactive response customization
        Where: Called by persona engine for predictive responses
        How: Analyze context against learned preference patterns
        """
        predictions = {
            'suggested_mode': 'Auto',
            'confidence': 0.5,
            'reasoning': []
        }
        
        try:
            context_keywords = [word.lower() for word in context.split() if len(word) > 2]
            
            # Analyze mode preferences
            # Explicit typing for static analyzers
            mode_scores: Dict[str, float] = defaultdict(float)
            
            for keyword in context_keywords:
                pref_key = f"topic_interest_{keyword}"
                if pref_key in self.preference_model:
                    confidence = self.preference_model[pref_key]['confidence']
                    
                    # Find associated modes
                    mode_patterns = self.learning_patterns.get(f"keyword_{keyword}", [])
                    if mode_patterns:
                        most_common_mode = Counter(mode_patterns).most_common(1)[0][0]
                        mode_scores[most_common_mode] += confidence
                        predictions['reasoning'].append(f"Keyword '{keyword}' suggests {most_common_mode} mode")
            
            if mode_scores:
                # Using .get as key is fine at runtime; static analyzer may need a hint
                best_mode = max(mode_scores, key=lambda k: mode_scores.get(k, 0.0))
                predictions['suggested_mode'] = best_mode
                predictions['confidence'] = min(0.9, mode_scores[best_mode])
            
        except Exception as _e:
            debugger.error('memory_engine', f'Failed to predict preferences: {e}')
        
        return predictions
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory system statistics
        
        Why: Provide insights into memory system performance and learning
        Where: Used by monitoring and health check systems
        How: Aggregate statistics from all memory components
        """
        try:
            stats = {}
            
            # Memory node statistics
            node_stats = self._execute_query("""
                SELECT COUNT(*), AVG(importance), MAX(accessed_count)
                FROM memory_nodes
            """)[0]
            
            stats['memory_nodes'] = {
                'total': node_stats[0],
                'avg_importance': round(node_stats[1] or 0, 3),
                'max_accessed': node_stats[2] or 0
            }
            
            # Relationship statistics
            rel_stats = self._execute_query("""
                SELECT COUNT(*), AVG(strength)
                FROM memory_relationships
            """)[0]
            
            stats['relationships'] = {
                'total': rel_stats[0],
                'avg_strength': round(rel_stats[1] or 0, 3)
            }
            
            # Conversation statistics
            conv_stats = self._execute_query("""
                SELECT COUNT(*), COUNT(DISTINCT session_id)
                FROM conversation_context
            """)[0]
            
            stats['conversations'] = {
                'total_interactions': conv_stats[0],
                'unique_sessions': conv_stats[1]
            }
            
            # Preference statistics
            pref_count = self._execute_query("SELECT COUNT(*) FROM user_preferences")[0][0]
            stats['preferences'] = {
                'total': pref_count,
                'loaded': len(self.preference_model)
            }
            
            stats['session'] = {
                'current_session': self.session_id,
                'buffer_size': len(self.conversation_buffer),
                'learning_patterns': len(self.learning_patterns)
            }
            
            return stats
            
        except Exception as _e:
            debugger.error('memory_engine', f'Failed to get memory stats: {e}')
            return {'error': str(e)}


# Global memory engine instance  
_memory_engine = None
_memory_lock = threading.Lock()


def get_memory_engine() -> AdvancedMemoryEngine:
    """
    Get global memory engine instance
    
    Why: Provide singleton access to memory system across application
    Where: Used by all modules needing memory capabilities
    How: Create or return existing engine instance with database connection
    
    Connects to:
        - app.py: Main application memory operations
        - persona.py: Context retrieval for responses
        - All modules: Universal memory access
    """
    global _memory_engine
    
    with _memory_lock:
        if _memory_engine is None:
            db_manager = DatabaseManager(config.DB_PATH)
            _memory_engine = AdvancedMemoryEngine(db_manager)
            debugger.info('memory_engine', 'Global memory engine created')
        
        return _memory_engine


def reset_memory_engine():
    """
    Reset global memory engine
    
    Why: Allow clean state for testing and development
    Where: Used in test cases and development workflows
    How: Clear global engine variable
    """
    global _memory_engine
    with _memory_lock:
        _memory_engine = None
        debugger.info('memory_engine', 'Global memory engine reset')