<<<<<<< HEAD
"""
Clever's Evolution Engine - Self-Learning Intelligence Core

Why: Drives autonomous intelligence growth for Clever by learning from user
interactions, extracting concepts, and forming connections. Operates at full
potential with no fallbacks, leveraging advanced NLP and network analysis.
Where: Used by app.py, file_ingestor.py, persona.py, and other modules for
self-learning, memory, and growth metrics.
How: Implements concept graph, learning algorithms, evolution triggers, and
database integration. Uses spaCy, numpy, networkx, and config.DB_PATH.

Connects to:
    - app.py: Main application, logs interactions
    - file_ingestor.py, pdf_ingestor.py: Knowledge ingestion
    - database.py: Persistence and retrieval
    - persona.py: Persona engine for context
    - config.py: Centralized configuration
"""

# !/usr/bin/env python3

import sqlite3
import json
from datetime import datetime
from collections import Counter
import hashlib
import re
from dataclasses import dataclass
from typing import Dict, List, Set, Optional
import numpy as np
import networkx as nx
import spacy
from config import DB_PATH
from database import DatabaseManager

# Load spaCy model - required for full operation
=======
#!/usr/bin/env python3
"""
Evolution Engine Module - Self-learning intelligence core for Clever AI.

Why: Implements adaptive learning algorithms that analyze interaction patterns,
     build concept networks, and continuously evolve Clever's knowledge and
     response capabilities based on user feedback and usage patterns.

Where: Used throughout the application to log interactions, analyze patterns,
       build knowledge graphs, and provide learning-based insights for
       persona adaptation and knowledge discovery.

How: Combines database-backed interaction logging with concept mapping, pattern
     recognition, and network analysis to create emergent intelligence through
     cascading learning from conversation and content analysis.
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import hashlib
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set

# Required dependencies for mathematical and NLP processing
import numpy as np
import networkx as nx
import spacy

import config

# Load spaCy model for text processing
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
nlp = spacy.load("en_core_web_sm")


@dataclass
class ConceptNode:
<<<<<<< HEAD
    """Represents a learned concept in Clever's mind"""

=======
    """
    Represents a learned concept in Clever's evolving knowledge network.
    
    Why: Provides structured representation of discovered concepts with temporal
         tracking, relationship mapping, and confidence scoring for adaptive
         learning and knowledge graph construction.
    
    Where: Used throughout evolution engine to track learned concepts, build
           semantic networks, and provide context for intelligent responses.
    
    How: Stores concept metadata including creation time, strength metrics,
         related concepts as a network, and source interactions for traceability.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    concept_id: str
    name: str
    strength: float
    creation_time: datetime
    last_reinforced: datetime
    related_concepts: Set[str]
    source_interactions: List[str]
    confidence: float

<<<<<<< HEAD

class CleverEvolutionEngine:
    """
    Autonomous intelligence growth system - Full potential, no fallbacks

    Why: Drives autonomous intelligence growth for Clever by learning from user
    interactions, extracting concepts, and forming connections. Operates at full
    potential with no fallbacks, leveraging advanced NLP and network analysis.
    Where: Used by app.py, file_ingestor.py, persona.py, and other modules for
    self-learning, memory, and growth metrics.
    How: Implements concept graph, learning algorithms, evolution triggers, and
    centralized database integration via DatabaseManager.

    Connects to:
        - app.py: Main application, logs interactions via log_interaction()
        - file_ingestor.py, pdf_ingestor.py: Knowledge ingestion pipeline
        - database.py: Centralized persistence via DatabaseManager
        - persona.py: Persona engine for context and capabilities
        - config.py: Centralized configuration and DB_PATH
    """

    def __init__(self):
        self.db_manager = DatabaseManager(DB_PATH)
        self.learning_threshold = 0.3
        self.evolution_log = []
        self.concept_cache = {}

        # NetworkX graph for full network analysis capabilities
        self.concept_graph = nx.DiGraph()

        self.init_evolution_database()
        self.load_existing_knowledge()

    def init_evolution_database(self):
        """
        Initialize evolution tracking tables in the centralized database

        Why: Sets up necessary tables for concept storage, interaction patterns,
        knowledge connections, and evolution events tracking
        Where: Called during CleverEvolutionEngine initialization
        How: Uses centralized DatabaseManager for thread-safe table creation

        Connects to:
            - database.py: Uses DatabaseManager._connect() for database operations
            - config.py: Database location via DB_PATH
        """
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

            # Concept network table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS concept_network (
                    concept_id TEXT PRIMARY KEY,
                    name TEXT,
                    strength REAL DEFAULT 0.1,
                    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_reinforced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    related_concepts TEXT,
                    source_interactions TEXT,
                    confidence REAL DEFAULT 0.1,
                    evolution_score REAL DEFAULT 0.0
                )
            """
            )

            # Interaction patterns table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS interaction_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_hash TEXT UNIQUE,
                    pattern_type TEXT,
                    frequency INTEGER DEFAULT 1,
                    effectiveness REAL DEFAULT 0.5,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_tags TEXT
                )
            """
            )

            # Knowledge connections table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    concept_a TEXT,
                    concept_b TEXT,
                    connection_strength REAL DEFAULT 0.1,
                    connection_type TEXT,
                    discovered_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reinforcement_count INTEGER DEFAULT 1
                )
            """
            )

            # Evolution events table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS evolution_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    description TEXT,
                    trigger_data TEXT,
                    impact_score REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Capability tracking table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS capability_evolution (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    capability_name TEXT,
                    current_level REAL DEFAULT 0.1,
                    growth_rate REAL DEFAULT 0.01,
                    last_exercise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    mastery_indicators TEXT,
                    next_evolution_target REAL DEFAULT 0.2
                )
            """
            )

            conn.commit()

    def load_existing_knowledge(self):
        """
        Load existing concepts into the concept graph for analysis

        Why: Rebuilds the in-memory concept graph from persisted database state
        to enable network analysis and connection discovery
        Where: Called during CleverEvolutionEngine initialization
        How: Queries concept_network table and knowledge_connections via DatabaseManager

        Connects to:
            - database.py: Uses DatabaseManager for thread-safe database access
            - NetworkX: Builds concept_graph for network analysis
        """
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM concept_network")
            for row in cursor.fetchall():
                (
                    concept_id,
                    name,
                    strength,
                    creation_time,
                    last_reinforced,
                    related_json,
                    source_json,
                    confidence,
                    evolution_score,
                ) = row

                related_concepts = set(
                    json.loads(related_json) if related_json else []
                )
                source_interactions = (
                    json.loads(source_json) if source_json else []
                )

                concept = ConceptNode(
                    concept_id=concept_id,
                    name=name,
                    strength=strength,
                    creation_time=datetime.fromisoformat(creation_time),
                    last_reinforced=datetime.fromisoformat(last_reinforced),
                    related_concepts=related_concepts,
                    source_interactions=source_interactions,
                    confidence=confidence,
                )

                self.concept_cache[concept_id] = concept
                self.concept_graph.add_node(concept_id, concept=concept)

            # Load all concept connections
            cursor.execute(
                """
                SELECT concept_a, concept_b, connection_strength,
                       connection_type FROM knowledge_connections
            """
            )
            for concept_a, concept_b, strength, conn_type in cursor.fetchall():
                if (
                    concept_a in self.concept_graph
                    and concept_b in self.concept_graph
                ):
                    self.concept_graph.add_edge(
                        concept_a,
                        concept_b,
                        weight=strength,
                        connection_type=conn_type,
                    )

    def log_interaction(self, interaction_data: Dict):
        """Main entry point for logging interactions and triggering learning

        Why: Serves as the primary interface for the rest of the application
        to trigger learning from user interactions
        Where: Called by app.py after generating responses to users
        How: Extracts parameters from interaction_data dict and delegates
        to analyze_interaction method for actual learning

        Connects to:
        - app.py: Main caller after user interactions
        - analyze_interaction: Core learning logic
        """
        user_input = interaction_data.get("user_input", "")
        response = interaction_data.get("response", "")
        mode = interaction_data.get("active_mode", "Auto")
        sentiment = interaction_data.get("sentiment", 0.0)

        # Analyze this interaction for learning
        analysis = self.analyze_interaction(
            user_input, response, mode, sentiment
        )

        # Log the evolution event if significant learning occurred
        if analysis["new_concepts"] or analysis["new_connections"]:
            self.log_evolution_event(
                "learning_event",
                f"Learned {len(analysis['new_concepts'])} concepts, "
                f"{len(analysis['new_connections'])} connections",
                interaction_data,
                0.3,
            )

    def analyze_interaction(
        self,
        user_message: str,
        clever_response: str,
        intent: str,
        sentiment: float,
    ) -> Dict:
        """Analyze interaction for learning opportunities"""
        analysis = {
            "new_concepts": [],
            "reinforced_concepts": [],
            "new_connections": [],
            "pattern_evolution": [],
            "capability_growth": [],
        }

        # Extract concepts from interaction
        user_concepts = self.extract_concepts(user_message)
        response_concepts = self.extract_concepts(clever_response)

        # Process new concepts
        for concept in user_concepts + response_concepts:
            concept_id = self.generate_concept_id(concept)

            if concept_id not in self.concept_graph:
                # New concept discovered
                new_concept = self.create_concept(
                    concept, user_message, clever_response
                )
                analysis["new_concepts"].append(new_concept.name)
                self.log_evolution_event(
                    "concept_discovery",
                    f"Discovered: {concept}",
                    {"concept": concept, "source": "interaction"},
                    0.3,
                )
            else:
                # Reinforce existing concept
                self.reinforce_concept(concept_id, sentiment)
                analysis["reinforced_concepts"].append(concept)

        # Discover new connections
        for i, concept_a in enumerate(user_concepts + response_concepts):
            for concept_b in (user_concepts + response_concepts)[i + 1 :]:
                full_context = user_message + " " + clever_response
                connection = self.analyze_concept_connection(
                    concept_a, concept_b, full_context
                )
                if connection:
                    analysis["new_connections"].append(connection)

        # Learn interaction patterns
        pattern = self.analyze_interaction_pattern(
            user_message, clever_response, intent, sentiment
        )
        if pattern:
            analysis["pattern_evolution"].append(pattern)

        # Update capabilities
        capability_growth = self.update_capabilities(
            intent, sentiment, len(user_message), len(clever_response)
        )
        analysis["capability_growth"] = capability_growth

        return analysis

    def extract_concepts(self, text: str) -> List[str]:
        """Extract meaningful concepts from text using advanced NLP"""
        concepts = []
        doc = nlp(text)

        # Extract named entities with full coverage
        entity_types = [
            "PERSON",
            "ORG",
            "GPE",
            "EVENT",
            "WORK_OF_ART",
            "LAW",
            "LANGUAGE",
            "PRODUCT",
            "NORP",
            "FAC",
        ]
        for ent in doc.ents:
            if ent.label_ in entity_types and len(ent.text.strip()) > 2:
                concepts.append(ent.text.lower().strip())

        # Extract sophisticated noun phrases
        for chunk in doc.noun_chunks:
            # Filter for meaningful chunks
            if (
                2 <= len(chunk.text.split()) <= 4
                and chunk.root.pos_ in ["NOUN", "PROPN"]
                and not chunk.root.is_stop
            ):
                concepts.append(chunk.text.lower().strip())

        # Extract key individual terms
        for token in doc:
            if (
                token.pos_ in ["NOUN", "PROPN", "ADJ"]
                and not token.is_stop
                and not token.is_punct
                and len(token.text) > 3
                and token.lemma_ != "-PRON-"
            ):
                concepts.append(token.lemma_.lower())

        # Advanced pattern extraction for technical terms
        tech_patterns = re.findall(r"\b[A-Z]{2,}(?:[A-Z][a-z]+)*\b", text)
        concepts.extend([p.lower() for p in tech_patterns])

        # Filter and deduplicate with enhanced exclusions
        filtered_concepts = []
        excluded_terms = {
            "user",
            "message",
            "response",
            "clever",
            "system",
            "thing",
            "way",
            "time",
            "part",
            "place",
            "person",
            "word",
            "text",
            "example",
        }

        for concept in concepts:
            concept = concept.strip()
            if (
                len(concept) > 2
                and concept not in excluded_terms
                and not concept.isdigit()
                and not concept.startswith(("http", "www"))
                and len(concept.split()) <= 4
            ):
                filtered_concepts.append(concept)

        # Prioritize by frequency and return top concepts
        concept_counts = Counter(filtered_concepts)
        return [concept for concept, _ in concept_counts.most_common(15)]

    def generate_concept_id(self, concept_name: str) -> str:
        """Generate unique ID for concept"""
        return hashlib.md5(concept_name.lower().encode()).hexdigest()[:12]

    def create_concept(
        self, name: str, user_message: str, clever_response: str
    ) -> ConceptNode:
        """Create new concept node"""
        concept_id = self.generate_concept_id(name)
        now = datetime.now()

=======
class CleverEvolutionEngine:
    """Autonomous intelligence growth system"""
    
    def __init__(self, db_path="clever.db"):
        self.db_path = db_path
        self.concept_graph = {}  # Fallback dict if networkx not available
        self.learning_threshold = 0.3
        self.evolution_log = []
        
        # Use networkx if available, otherwise simple dict
        if nx:
            self.concept_graph = nx.DiGraph()
        
        self.init_evolution_database()
        self.load_existing_knowledge()
        
    def init_evolution_database(self):
        """Initialize evolution tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Concept network table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concept_network (
                concept_id TEXT PRIMARY KEY,
                name TEXT,
                strength REAL DEFAULT 0.1,
                creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_reinforced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                related_concepts TEXT,
                source_interactions TEXT,
                confidence REAL DEFAULT 0.1,
                evolution_score REAL DEFAULT 0.0
            )
        ''')
        
        # Interaction patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interaction_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_hash TEXT UNIQUE,
                pattern_type TEXT,
                frequency INTEGER DEFAULT 1,
                effectiveness REAL DEFAULT 0.5,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                context_tags TEXT
            )
        ''')
        
        # Knowledge connections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_a TEXT,
                concept_b TEXT,
                connection_strength REAL DEFAULT 0.1,
                connection_type TEXT,
                discovered_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reinforcement_count INTEGER DEFAULT 1
            )
        ''')
        
        # Evolution events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolution_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                description TEXT,
                trigger_data TEXT,
                impact_score REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Capability tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS capability_evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capability_name TEXT,
                current_level REAL DEFAULT 0.1,
                growth_rate REAL DEFAULT 0.01,
                last_exercise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mastery_indicators TEXT,
                next_evolution_target REAL DEFAULT 0.2
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_existing_knowledge(self):
        """Load existing concepts into the graph"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM concept_network')
        for row in cursor.fetchall():
            concept_id, name, strength, creation_time, last_reinforced, related_json, source_json, confidence, evolution_score = row
            
            related_concepts = set(json.loads(related_json) if related_json else [])
            source_interactions = json.loads(source_json) if source_json else []
            
            concept = ConceptNode(
                concept_id=concept_id,
                name=name,
                strength=strength,
                creation_time=datetime.fromisoformat(creation_time),
                last_reinforced=datetime.fromisoformat(last_reinforced),
                related_concepts=related_concepts,
                source_interactions=source_interactions,
                confidence=confidence
            )
            
            if nx:
                self.concept_graph.add_node(concept_id, concept=concept)
            else:
                self.concept_graph[concept_id] = concept
            
        # Load connections if networkx available
        if nx:
            cursor.execute('SELECT concept_a, concept_b, connection_strength, connection_type FROM knowledge_connections')
            for concept_a, concept_b, strength, conn_type in cursor.fetchall():
                if concept_a in self.concept_graph and concept_b in self.concept_graph:
                    self.concept_graph.add_edge(concept_a, concept_b, 
                                              weight=strength, 
                                              connection_type=conn_type)
        
        conn.close()
        
    def analyze_interaction(self, user_message: str, clever_response: str, intent: str, sentiment: float) -> Dict:
        """Analyze interaction for learning opportunities"""
        analysis = {
            'new_concepts': [],
            'reinforced_concepts': [],
            'new_connections': [],
            'pattern_evolution': [],
            'capability_growth': []
        }
        
        # Extract concepts from interaction
        user_concepts = self.extract_concepts(user_message)
        response_concepts = self.extract_concepts(clever_response)
        
        # Process new concepts
        for concept in user_concepts + response_concepts:
            concept_id = self.generate_concept_id(concept)
            
            if concept_id not in self.concept_graph:
                # New concept discovered
                new_concept = self.create_concept(concept, user_message, clever_response)
                analysis['new_concepts'].append(new_concept.name)
                self.log_evolution_event("concept_discovery", f"Discovered: {concept}", 
                                        {"concept": concept, "source": "interaction"}, 0.3)
            else:
                # Reinforce existing concept
                self.reinforce_concept(concept_id, sentiment)
                analysis['reinforced_concepts'].append(concept)
        
        # Discover new connections
        for i, concept_a in enumerate(user_concepts + response_concepts):
            for concept_b in (user_concepts + response_concepts)[i+1:]:
                connection = self.analyze_concept_connection(concept_a, concept_b, user_message + " " + clever_response)
                if connection:
                    analysis['new_connections'].append(connection)
        
        # Learn interaction patterns
        pattern = self.analyze_interaction_pattern(user_message, clever_response, intent, sentiment)
        if pattern:
            analysis['pattern_evolution'].append(pattern)
        
        # Update capabilities
        capability_growth = self.update_capabilities(intent, sentiment, len(user_message), len(clever_response))
        analysis['capability_growth'] = capability_growth
        
        return analysis
        
    def extract_concepts(self, text: str) -> List[str]:
        """Extract meaningful concepts from text"""
        concepts = []
        
        if nlp:
            doc = nlp(text)
            
            # Extract named entities
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']:
                    concepts.append(ent.text.lower().strip())
            
            # Extract noun phrases
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) <= 3 and chunk.root.pos_ in ['NOUN', 'PROPN']:
                    concepts.append(chunk.text.lower().strip())
            
            # Extract important single nouns
            for token in doc:
                if (token.pos_ in ['NOUN', 'PROPN'] and 
                    not token.is_stop and 
                    not token.is_punct and 
                    len(token.text) > 2):
                    concepts.append(token.lemma_.lower())
        else:
            # Fallback extraction
            words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]{4,}\b', text)
            concepts = [word.lower() for word in words]
        
        # Filter and deduplicate
        filtered_concepts = []
        for concept in concepts:
            if (len(concept) > 2 and 
                concept not in ['user', 'message', 'response', 'clever', 'system'] and
                not concept.isdigit()):
                filtered_concepts.append(concept)
        
        return list(set(filtered_concepts))
    
    def generate_concept_id(self, concept_name: str) -> str:
        """Generate unique ID for concept"""
        return hashlib.md5(concept_name.lower().encode()).hexdigest()[:12]
    
    def create_concept(self, name: str, user_message: str, clever_response: str) -> ConceptNode:
        """Create new concept node"""
        concept_id = self.generate_concept_id(name)
        now = datetime.now()
        
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        concept = ConceptNode(
            concept_id=concept_id,
            name=name,
            strength=0.1,
            creation_time=now,
            last_reinforced=now,
            related_concepts=set(),
            source_interactions=[user_message[:100]],
<<<<<<< HEAD
            confidence=0.1,
        )

        self.concept_graph.add_node(  # type: ignore
            concept_id, concept=concept
        )
        self.save_concept(concept)

        return concept

    def reinforce_concept(self, concept_id: str, sentiment_bonus: float = 0.0):
        """Strengthen existing concept"""
        if concept_id in self.concept_graph:
            # type: ignore
            # type: ignore
            concept = self.concept_graph.nodes[concept_id]["concept"]

=======
            confidence=0.1
        )
        
        self.concept_graph.add_node(concept_id, concept=concept)
        self.save_concept(concept)
        
        return concept
    
    def reinforce_concept(self, concept_id: str, sentiment_bonus: float = 0.0):
        """Strengthen existing concept"""
        if concept_id in self.concept_graph:
            concept = self.concept_graph.nodes[concept_id]['concept']
            
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            # Calculate reinforcement
            base_reinforcement = 0.05
            sentiment_multiplier = 1.0 + (sentiment_bonus * 0.5)
            time_decay = self.calculate_time_decay(concept.last_reinforced)
<<<<<<< HEAD

            reinforcement = (
                base_reinforcement * sentiment_multiplier * time_decay
            )

            concept.strength = min(1.0, concept.strength + reinforcement)
            concept.confidence = min(
                1.0, concept.confidence + reinforcement * 0.3
            )
            concept.last_reinforced = datetime.now()

            self.save_concept(concept)

    def analyze_concept_connection(
        self, concept_a: str, concept_b: str, context: str
    ) -> Optional[Dict]:
        """Analyze potential connection between concepts"""
        id_a = self.generate_concept_id(concept_a)
        id_b = self.generate_concept_id(concept_b)

        is_invalid = (
            id_a == id_b
            or (id_a not in self.concept_graph)
            or (id_b not in self.concept_graph)
        )
        if is_invalid:
            return None

        # Check if connection already exists
        if self.concept_graph.has_edge(id_a, id_b):  # type: ignore
            # Strengthen existing connection
            current_weight = self.concept_graph[id_a][id_b]["weight"]
            new_weight = min(1.0, current_weight + 0.1)
            self.concept_graph[id_a][id_b]["weight"] = new_weight
            self.update_connection_strength(id_a, id_b, new_weight)
            return {
                "type": "reinforced",
                "concepts": [concept_a, concept_b],
                "strength": new_weight,
            }
        else:
            # Create new connection
            connection_strength = self.calculate_connection_strength(
                concept_a, concept_b, context
            )

            if connection_strength > 0.2:  # Threshold for new connections
                self.concept_graph.add_edge(  # type: ignore
                    id_a,
                    id_b,
                    weight=connection_strength,
                    connection_type="contextual",
                )
                self.save_connection(
                    id_a, id_b, connection_strength, "contextual"
                )

                # Add to related concepts
                self.concept_graph.nodes[id_a]["concept"].related_concepts.add(  # type: ignore # type: ignore
                    id_b
                )
                self.concept_graph.nodes[id_b]["concept"].related_concepts.add(  # type: ignore # type: ignore
                    id_a
                )

                self.log_evolution_event(
                    "connection_discovery",
                    f"Connected: {concept_a} <-> {concept_b}",
                    {
                        "concepts": [concept_a, concept_b],
                        "strength": connection_strength,
                    },
                    connection_strength,
                )

                return {
                    "type": "new",
                    "concepts": [concept_a, concept_b],
                    "strength": connection_strength,
                }

        return None

    def calculate_connection_strength(
        self, concept_a: str, concept_b: str, context: str
    ) -> float:
=======
            
            reinforcement = base_reinforcement * sentiment_multiplier * time_decay
            
            concept.strength = min(1.0, concept.strength + reinforcement)
            concept.confidence = min(1.0, concept.confidence + reinforcement * 0.3)
            concept.last_reinforced = datetime.now()
            
            self.save_concept(concept)
    
    def analyze_concept_connection(self, concept_a: str, concept_b: str, context: str) -> Dict:
        """Analyze potential connection between concepts"""
        id_a = self.generate_concept_id(concept_a)
        id_b = self.generate_concept_id(concept_b)
        
        if id_a == id_b or (id_a not in self.concept_graph) or (id_b not in self.concept_graph):
            return None
        
        # Check if connection already exists
        if self.concept_graph.has_edge(id_a, id_b):
            # Strengthen existing connection
            current_weight = self.concept_graph[id_a][id_b]['weight']
            new_weight = min(1.0, current_weight + 0.1)
            self.concept_graph[id_a][id_b]['weight'] = new_weight
            self.update_connection_strength(id_a, id_b, new_weight)
            return {"type": "reinforced", "concepts": [concept_a, concept_b], "strength": new_weight}
        else:
            # Create new connection
            connection_strength = self.calculate_connection_strength(concept_a, concept_b, context)
            
            if connection_strength > 0.2:  # Threshold for new connections
                self.concept_graph.add_edge(id_a, id_b, weight=connection_strength, connection_type="contextual")
                self.save_connection(id_a, id_b, connection_strength, "contextual")
                
                # Add to related concepts
                self.concept_graph.nodes[id_a]['concept'].related_concepts.add(id_b)
                self.concept_graph.nodes[id_b]['concept'].related_concepts.add(id_a)
                
                self.log_evolution_event("connection_discovery", 
                                       f"Connected: {concept_a} <-> {concept_b}",
                                       {"concepts": [concept_a, concept_b], "strength": connection_strength},
                                       connection_strength)
                
                return {"type": "new", "concepts": [concept_a, concept_b], "strength": connection_strength}
        
        return None
    
    def calculate_connection_strength(self, concept_a: str, concept_b: str, context: str) -> float:
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        """Calculate strength of connection between concepts"""
        # Distance in text
        context_lower = context.lower()
        pos_a = context_lower.find(concept_a.lower())
        pos_b = context_lower.find(concept_b.lower())
<<<<<<< HEAD

        if pos_a == -1 or pos_b == -1:
            return 0.0

        distance = abs(pos_a - pos_b)
        proximity_score = max(0, 1.0 - (distance / 100))  # Closer = stronger

        # Advanced semantic similarity using spaCy vectors
        try:
            doc_a = nlp(concept_a)
            doc_b = nlp(concept_b)
            if doc_a.vector.any() and doc_b.vector.any():
                semantic_score = doc_a.similarity(doc_b)
            else:
                # Calculate word-level similarity for out-of-vocab terms
                words_a = [
                    token.text.lower() for token in doc_a if not token.is_stop
                ]
                words_b = [
                    token.text.lower() for token in doc_b if not token.is_stop
                ]
                common_words = set(words_a) & set(words_b)
                total_words = set(words_a) | set(words_b)
                semantic_score = len(common_words) / max(1, len(total_words))
        except Exception:
            semantic_score = 0.1

        # Co-occurrence frequency
        cooccurrence_score = (
            0.3  # Base score, would be calculated from history
        )

        connection_strength = (
            proximity_score * 0.4
            + semantic_score * 0.4
            + cooccurrence_score * 0.2
        )

        return min(1.0, connection_strength)

    def analyze_interaction_pattern(
        self,
        user_message: str,
        clever_response: str,
        intent: str,
        sentiment: float,
    ) -> Dict:
        """Learn from interaction patterns"""
        pattern_data = {
            "message_length": len(user_message),
            "response_length": len(clever_response),
            "intent": intent,
            "sentiment_range": self.categorize_sentiment(sentiment),
            "question_type": self.detect_question_type(user_message),
            "response_style": self.analyze_response_style(clever_response),
        }

        pattern_hash = hashlib.md5(
            json.dumps(pattern_data, sort_keys=True).encode()
        ).hexdigest()[:16]

        # Update pattern frequency
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        cursor.execute(
            """SELECT frequency, effectiveness FROM interaction_patterns
               WHERE pattern_hash = ?""",
            (pattern_hash,),
        )
        existing = cursor.fetchone()

        if existing:
            frequency, effectiveness = existing
            new_frequency = frequency + 1
            # Update effectiveness based on sentiment (positive sentiment =
            # more effective)
            new_effectiveness = (
                effectiveness * frequency + max(0, sentiment)
            ) / new_frequency

            cursor.execute(
                """
                UPDATE interaction_patterns
                SET frequency = ?, effectiveness = ?,
                    last_used = CURRENT_TIMESTAMP
                WHERE pattern_hash = ?
            """,
                (new_frequency, new_effectiveness, pattern_hash),
                # Project Coding Instructions:
                # See .github/copilot-instructions.md for architecture, documentation, and workflow rules.
                # All code must follow these standards.
            )
        else:
            cursor.execute(
                """
                INSERT INTO interaction_patterns
                (pattern_hash, pattern_type, frequency, effectiveness,
                 context_tags)
                VALUES (?, ?, 1, ?, ?)
            """,
                (
                    pattern_hash,
                    intent,
                    max(0.1, sentiment),
                    json.dumps(pattern_data),
                ),
            )

        conn.commit()

        return {"pattern_hash": pattern_hash, "data": pattern_data}

    def update_capabilities(
        self,
        intent: str,
        sentiment: float,
        input_length: int,
        output_length: int,
    ) -> List[Dict]:
        """Update Clever's capability levels"""
        capabilities_growth = []

        capability_updates = {
            "conversation_handling": min(0.01, input_length / 1000),
            "response_generation": min(0.01, output_length / 1000),
            "sentiment_understanding": abs(sentiment) * 0.005,
            "intent_recognition": 0.003 if intent != "unknown" else 0.001,
        }

        # Intent-specific capabilities
        if intent == "creative_mode":
            capability_updates["creativity"] = 0.008
        elif intent == "deep_dive_mode":
            capability_updates["analytical_thinking"] = 0.008
        elif intent == "support_mode":
            capability_updates["empathy"] = 0.008

        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        for capability, growth in capability_updates.items():
            cursor.execute(
                """SELECT current_level, growth_rate FROM capability_evolution
                   WHERE capability_name = ?""",
                (capability,),
            )
            existing = cursor.fetchone()

            if existing:
                current_level, growth_rate = existing
                new_level = min(1.0, current_level + growth)
                adaptive_growth_rate = growth_rate + (
                    growth * 0.1
                )  # Growth accelerates with use

                cursor.execute(
                    """
                    UPDATE capability_evolution
                    SET current_level = ?, growth_rate = ?,
                        last_exercise = CURRENT_TIMESTAMP
                    WHERE capability_name = ?
                """,
                    (new_level, adaptive_growth_rate, capability),
                )

                capabilities_growth.append(
                    {
                        "capability": capability,
                        "old_level": current_level,
                        "new_level": new_level,
                        "growth": growth,
                    }
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO capability_evolution
                    (capability_name, current_level, growth_rate)
                    VALUES (?, ?, ?)
                """,
                    (capability, growth, 0.01),
                )

                capabilities_growth.append(
                    {
                        "capability": capability,
                        "old_level": 0.0,
                        "new_level": growth,
                        "growth": growth,
                    }
                )

        conn.commit()

        return capabilities_growth

    def process_pdf_knowledge(
        self,
        filename: str,
        content: str,
        entities: List[Dict],
        keywords: List[str],
    ) -> Dict:
        """Process PDF content for autonomous learning"""
        learning_results = {
            "concepts_learned": 0,
            "connections_formed": 0,
            "knowledge_clusters": [],
            "evolution_triggered": False,
        }

        # Extract high-value concepts from PDF
        pdf_concepts = self.extract_pdf_concepts(content, entities, keywords)

        for concept in pdf_concepts:
            concept_id = self.generate_concept_id(concept["name"])

=======
        
        if pos_a == -1 or pos_b == -1:
            return 0.0
        
        distance = abs(pos_a - pos_b)
        proximity_score = max(0, 1.0 - (distance / 100))  # Closer = stronger
        
        # Semantic similarity (if spaCy available)
        semantic_score = 0.5
        if nlp:
            try:
                doc_a = nlp(concept_a)
                doc_b = nlp(concept_b)
                if doc_a.vector.any() and doc_b.vector.any():
                    semantic_score = doc_a.similarity(doc_b)
            except:
                pass
        
        # Co-occurrence frequency
        cooccurrence_score = 0.3  # Base score, would be calculated from history
        
        connection_strength = (proximity_score * 0.4 + 
                             semantic_score * 0.4 + 
                             cooccurrence_score * 0.2)
        
        return min(1.0, connection_strength)
    
    def analyze_interaction_pattern(self, user_message: str, clever_response: str, intent: str, sentiment: float) -> Dict:
        """Learn from interaction patterns"""
        pattern_data = {
            'message_length': len(user_message),
            'response_length': len(clever_response),
            'intent': intent,
            'sentiment_range': self.categorize_sentiment(sentiment),
            'question_type': self.detect_question_type(user_message),
            'response_style': self.analyze_response_style(clever_response)
        }
        
        pattern_hash = hashlib.md5(json.dumps(pattern_data, sort_keys=True).encode()).hexdigest()[:16]
        
        # Update pattern frequency
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT frequency, effectiveness FROM interaction_patterns WHERE pattern_hash = ?', (pattern_hash,))
        existing = cursor.fetchone()
        
        if existing:
            frequency, effectiveness = existing
            new_frequency = frequency + 1
            # Update effectiveness based on sentiment (positive sentiment = more effective)
            new_effectiveness = (effectiveness * frequency + max(0, sentiment)) / new_frequency
            
            cursor.execute('''
                UPDATE interaction_patterns 
                SET frequency = ?, effectiveness = ?, last_used = CURRENT_TIMESTAMP
                WHERE pattern_hash = ?
            ''', (new_frequency, new_effectiveness, pattern_hash))
        else:
            cursor.execute('''
                INSERT INTO interaction_patterns 
                (pattern_hash, pattern_type, frequency, effectiveness, context_tags)
                VALUES (?, ?, 1, ?, ?)
            ''', (pattern_hash, intent, max(0.1, sentiment), json.dumps(pattern_data)))
        
        conn.commit()
        conn.close()
        
        return {"pattern_hash": pattern_hash, "data": pattern_data}
    
    def update_capabilities(self, intent: str, sentiment: float, input_length: int, output_length: int) -> List[Dict]:
        """Update Clever's capability levels"""
        capabilities_growth = []
        
        capability_updates = {
            'conversation_handling': min(0.01, input_length / 1000),
            'response_generation': min(0.01, output_length / 1000),
            'sentiment_understanding': abs(sentiment) * 0.005,
            'intent_recognition': 0.003 if intent != 'unknown' else 0.001
        }
        
        # Intent-specific capabilities
        if intent == 'creative_mode':
            capability_updates['creativity'] = 0.008
        elif intent == 'deep_dive_mode':
            capability_updates['analytical_thinking'] = 0.008
        elif intent == 'support_mode':
            capability_updates['empathy'] = 0.008
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for capability, growth in capability_updates.items():
            cursor.execute('SELECT current_level, growth_rate FROM capability_evolution WHERE capability_name = ?', (capability,))
            existing = cursor.fetchone()
            
            if existing:
                current_level, growth_rate = existing
                new_level = min(1.0, current_level + growth)
                adaptive_growth_rate = growth_rate + (growth * 0.1)  # Growth accelerates with use
                
                cursor.execute('''
                    UPDATE capability_evolution 
                    SET current_level = ?, growth_rate = ?, last_exercise = CURRENT_TIMESTAMP
                    WHERE capability_name = ?
                ''', (new_level, adaptive_growth_rate, capability))
                
                capabilities_growth.append({
                    'capability': capability,
                    'old_level': current_level,
                    'new_level': new_level,
                    'growth': growth
                })
            else:
                cursor.execute('''
                    INSERT INTO capability_evolution (capability_name, current_level, growth_rate)
                    VALUES (?, ?, ?)
                ''', (capability, growth, 0.01))
                
                capabilities_growth.append({
                    'capability': capability,
                    'old_level': 0.0,
                    'new_level': growth,
                    'growth': growth
                })
        
        conn.commit()
        conn.close()
        
        return capabilities_growth
    
    def process_pdf_knowledge(self, filename: str, content: str, entities: List[Dict], keywords: List[str]) -> Dict:
        """Process PDF content for autonomous learning"""
        learning_results = {
            'concepts_learned': 0,
            'connections_formed': 0,
            'knowledge_clusters': [],
            'evolution_triggered': False
        }
        
        # Extract high-value concepts from PDF
        pdf_concepts = self.extract_pdf_concepts(content, entities, keywords)
        
        for concept in pdf_concepts:
            concept_id = self.generate_concept_id(concept['name'])
            
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            if concept_id not in self.concept_graph:
                # Create new concept from PDF
                new_concept = ConceptNode(
                    concept_id=concept_id,
<<<<<<< HEAD
                    name=concept["name"],
                    strength=concept["strength"],
=======
                    name=concept['name'],
                    strength=concept['strength'],
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
                    creation_time=datetime.now(),
                    last_reinforced=datetime.now(),
                    related_concepts=set(),
                    source_interactions=[f"PDF: {filename}"],
<<<<<<< HEAD
                    confidence=concept["confidence"],
                )

                if hasattr(self.concept_graph, "add_node"):
                    self.concept_graph.add_node(  # type: ignore
                        concept_id, concept=new_concept
                    )
                else:
                    self.concept_graph[concept_id] = (  # type: ignore
                        new_concept
                    )
                self.save_concept(new_concept)
                learning_results["concepts_learned"] += 1

                self.log_evolution_event(
                    "pdf_concept_discovery",
                    f"Learned from PDF: {concept['name']}",
                    {"source": filename, "concept": concept["name"]},
                    concept["strength"],
                )
            else:
                # Reinforce with PDF knowledge
                self.reinforce_concept(concept_id, concept["strength"])

        # Form connections between PDF concepts
        for i, concept_a in enumerate(pdf_concepts):
            for concept_b in pdf_concepts[i + 1 :]:
                connection = self.analyze_concept_connection(
                    concept_a["name"], concept_b["name"], content[:500]
                )
                if connection:
                    learning_results["connections_formed"] += 1

        # Check for evolution threshold
        if (
            learning_results["concepts_learned"] > 5
            or learning_results["connections_formed"] > 3
        ):
            self.trigger_evolution_cascade()
            learning_results["evolution_triggered"] = True

        return learning_results

    def extract_pdf_concepts(
        self, content: str, entities: List[Dict], keywords: List[str]
    ) -> List[Dict]:
        """Extract high-value concepts from PDF content"""
        concepts = []

        # Process entities
        for entity in entities:
            if entity["label"] in [
                "PERSON",
                "ORG",
                "GPE",
                "EVENT",
                "WORK_OF_ART",
            ]:
                concepts.append(
                    {
                        "name": entity["text"].lower(),
                        "strength": 0.3,  # Entities are moderately strong
                        "confidence": 0.6,
                        "type": "entity",
                    }
                )

        # Process keywords with frequency analysis
        keyword_freq = Counter(keywords)
        total_keywords = len(keywords)

        for keyword, freq in keyword_freq.most_common(20):  # Top 20 keywords
            strength = min(
                0.8, freq / total_keywords * 10
            )  # Frequency-based strength
            concepts.append(
                {
                    "name": keyword,
                    "strength": strength,
                    "confidence": strength * 0.8,
                    "type": "keyword",
                }
            )

        # Extract domain-specific terms
        domain_terms = self.extract_domain_terms(content)
        for term in domain_terms:
            concepts.append(
                {
                    "name": term,
                    "strength": 0.4,
                    "confidence": 0.5,
                    "type": "domain_term",
                }
            )

        return concepts

=======
                    confidence=concept['confidence']
                )
                
                if hasattr(self.concept_graph, "add_node"):
                    self.concept_graph.add_node(concept_id, concept=new_concept)
                else:
                    self.concept_graph[concept_id] = new_concept
                self.save_concept(new_concept)
                learning_results['concepts_learned'] += 1
                
                self.log_evolution_event("pdf_concept_discovery", 
                                       f"Learned from PDF: {concept['name']}",
                                       {"source": filename, "concept": concept['name']},
                                       concept['strength'])
            else:
                # Reinforce with PDF knowledge
                self.reinforce_concept(concept_id, concept['strength'])
        
        # Form connections between PDF concepts
        for i, concept_a in enumerate(pdf_concepts):
            for concept_b in pdf_concepts[i+1:]:
                connection = self.analyze_concept_connection(concept_a['name'], concept_b['name'], content[:500])
                if connection:
                    learning_results['connections_formed'] += 1
        
        # Check for evolution threshold
        if learning_results['concepts_learned'] > 5 or learning_results['connections_formed'] > 3:
            self.trigger_evolution_cascade()
            learning_results['evolution_triggered'] = True
        
        return learning_results
    
    def extract_pdf_concepts(self, content: str, entities: List[Dict], keywords: List[str]) -> List[Dict]:
        """Extract high-value concepts from PDF content"""
        concepts = []
        
        # Process entities
        for entity in entities:
            if entity['label'] in ['PERSON', 'ORG', 'GPE', 'EVENT', 'WORK_OF_ART']:
                concepts.append({
                    'name': entity['text'].lower(),
                    'strength': 0.3,  # Entities are moderately strong
                    'confidence': 0.6,
                    'type': 'entity'
                })
        
        # Process keywords with frequency analysis
        keyword_freq = Counter(keywords)
        total_keywords = len(keywords)
        
        for keyword, freq in keyword_freq.most_common(20):  # Top 20 keywords
            strength = min(0.8, freq / total_keywords * 10)  # Frequency-based strength
            concepts.append({
                'name': keyword,
                'strength': strength,
                'confidence': strength * 0.8,
                'type': 'keyword'
            })
        
        # Extract domain-specific terms
        domain_terms = self.extract_domain_terms(content)
        for term in domain_terms:
            concepts.append({
                'name': term,
                'strength': 0.4,
                'confidence': 0.5,
                'type': 'domain_term'
            })
        
        return concepts
    
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    def extract_domain_terms(self, content: str) -> List[str]:
        """Extract domain-specific terminology"""
        # Technical terms, proper nouns, specialized vocabulary
        domain_patterns = [
<<<<<<< HEAD
            r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b",  # CamelCase
            r"\b[A-Z]{2,}\b",  # Acronyms
            r"\b\w+(?:[-_]\w+)+\b",  # Hyphenated/underscored terms
        ]

=======
            r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',  # CamelCase
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+(?:[-_]\w+)+\b',  # Hyphenated/underscored terms
        ]
        
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        terms = []
        for pattern in domain_patterns:
            matches = re.findall(pattern, content)
            terms.extend([match.lower() for match in matches])
<<<<<<< HEAD

        return list(set(terms))[:15]  # Limit to prevent noise

    def trigger_evolution_cascade(self):
        """Trigger cascade of intelligence evolution"""
        self.log_evolution_event(
            "evolution_cascade",
            "Intelligence evolution cascade triggered",
            {"trigger": "learning_threshold_reached"},
            0.8,
        )

        # Strengthen concept network
        self.strengthen_concept_network()

        # Optimize connection weights
        self.optimize_connection_weights()

        # Identify knowledge clusters
        clusters = self.identify_knowledge_clusters()

        # Update response generation weights
        self.update_response_generation()

        return clusters

    def strengthen_concept_network(self):
        """Strengthen the overall concept network"""
        for node_id in self.concept_graph.nodes():  # type: ignore
            concept = (
                # type: ignore # type: ignore
                self.concept_graph.nodes[node_id]["concept"]
            )

            # Boost concepts with many connections
            connection_count = len(
                list(  # type: ignore
                    self.concept_graph.neighbors(node_id)  # type: ignore
                )
            )
            connection_bonus = min(0.2, connection_count * 0.02)

            concept.strength = min(1.0, concept.strength + connection_bonus)
            concept.confidence = min(
                1.0, concept.confidence + connection_bonus * 0.5
            )

            self.save_concept(concept)

=======
        
        return list(set(terms))[:15]  # Limit to prevent noise
    
    def trigger_evolution_cascade(self):
        """Trigger cascade of intelligence evolution"""
        self.log_evolution_event("evolution_cascade", 
                                "Intelligence evolution cascade triggered",
                                {"trigger": "learning_threshold_reached"},
                                0.8)
        
        # Strengthen concept network
        self.strengthen_concept_network()
        
        # Optimize connection weights
        self.optimize_connection_weights()
        
        # Identify knowledge clusters
        clusters = self.identify_knowledge_clusters()
        
        # Update response generation weights
        self.update_response_generation()
        
        return clusters
    
    def strengthen_concept_network(self):
        """Strengthen the overall concept network"""
        for node_id in self.concept_graph.nodes():
            concept = self.concept_graph.nodes[node_id]['concept']
            
            # Boost concepts with many connections
            connection_count = len(list(self.concept_graph.neighbors(node_id)))
            connection_bonus = min(0.2, connection_count * 0.02)
            
            concept.strength = min(1.0, concept.strength + connection_bonus)
            concept.confidence = min(1.0, concept.confidence + connection_bonus * 0.5)
            
            self.save_concept(concept)
    
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    def optimize_connection_weights(self):
        """Optimize connection weights using network analysis"""
        # Use PageRank to identify important concepts
        try:
<<<<<<< HEAD
            pagerank_scores = nx.pagerank(self.concept_graph)  # type: ignore

            for node_id, score in pagerank_scores.items():
                # type: ignore
                # type: ignore
                concept = self.concept_graph.nodes[node_id]["concept"]
                importance_bonus = score * 0.1
                concept.strength = min(
                    1.0, concept.strength + importance_bonus
                )
                self.save_concept(concept)

        except Exception as e:
            print(f"PageRank optimization failed: {e}")

=======
            pagerank_scores = nx.pagerank(self.concept_graph)
            
            for node_id, score in pagerank_scores.items():
                concept = self.concept_graph.nodes[node_id]['concept']
                importance_bonus = score * 0.1
                concept.strength = min(1.0, concept.strength + importance_bonus)
                self.save_concept(concept)
                
        except Exception as e:
            print(f"PageRank optimization failed: {e}")
    
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    def identify_knowledge_clusters(self) -> List[Dict]:
        """Identify clusters of related knowledge"""
        try:
            # Use community detection
<<<<<<< HEAD
            undirected_graph = self.concept_graph.to_undirected()  # type: ignore
            communities = nx.community.greedy_modularity_communities(  # type: ignore
                undirected_graph
            )

=======
            undirected_graph = self.concept_graph.to_undirected()
            communities = nx.community.greedy_modularity_communities(undirected_graph)
            
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            clusters = []
            for i, community in enumerate(communities):
                cluster_concepts = []
                for node_id in community:
<<<<<<< HEAD
                    # type: ignore
                    # type: ignore
                    concept = self.concept_graph.nodes[node_id]["concept"]
                    cluster_concepts.append(
                        {
                            "name": concept.name,
                            "strength": concept.strength,
                            "confidence": concept.confidence,
                        }
                    )

                if len(cluster_concepts) > 2:  # Only meaningful clusters
                    clusters.append(
                        {
                            "cluster_id": i,
                            "concepts": cluster_concepts,
                            "size": len(cluster_concepts),
                        }
                    )

            return clusters

        except Exception as e:
            print(f"Cluster identification failed: {e}")
            return []

    def update_response_generation(self):
        """
        Update response generation capabilities based on recent interactions

        Why: Tracks and improves Clever's response quality over time through
        learning from interaction patterns and effectiveness metrics
        Where: Called by analyze_interaction after processing user conversations
        How: Updates capability scores in database via DatabaseManager

        Connects to:
            - database.py: Uses DatabaseManager for thread-safe updates
            - analyze_interaction: Called as part of learning pipeline
        """
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        # Get most effective patterns
        cursor.execute(
            """
            SELECT pattern_type, AVG(effectiveness), COUNT(*) as usage_count
            FROM interaction_patterns
            WHERE effectiveness > 0.6
            GROUP BY pattern_type
            ORDER BY AVG(effectiveness) DESC, usage_count DESC
        """
        )

        effective_patterns = cursor.fetchall()

=======
                    concept = self.concept_graph.nodes[node_id]['concept']
                    cluster_concepts.append({
                        'name': concept.name,
                        'strength': concept.strength,
                        'confidence': concept.confidence
                    })
                
                if len(cluster_concepts) > 2:  # Only meaningful clusters
                    clusters.append({
                        'cluster_id': i,
                        'concepts': cluster_concepts,
                        'size': len(cluster_concepts)
                    })
            
            return clusters
            
        except Exception as e:
            print(f"Cluster identification failed: {e}")
            return []
    
    def update_response_generation(self):
        """Update response generation based on learned patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get most effective patterns
        cursor.execute('''
            SELECT pattern_type, AVG(effectiveness), COUNT(*) as usage_count
            FROM interaction_patterns 
            WHERE effectiveness > 0.6
            GROUP BY pattern_type
            ORDER BY AVG(effectiveness) DESC, usage_count DESC
        ''')
        
        effective_patterns = cursor.fetchall()
        
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
        # Update pattern weights for future responses
        pattern_weights = {}
        for pattern_type, avg_effectiveness, usage_count in effective_patterns:
            weight = avg_effectiveness * (1 + usage_count * 0.1)
            pattern_weights[pattern_type] = min(2.0, weight)
<<<<<<< HEAD

        # Save pattern weights
        cursor.execute(
            """
=======
        
        # Save pattern weights
        cursor.execute('''
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
            CREATE TABLE IF NOT EXISTS response_patterns (
                pattern_type TEXT PRIMARY KEY,
                weight REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
<<<<<<< HEAD
        """
        )

        for pattern_type, weight in pattern_weights.items():
            cursor.execute(
                """
                INSERT OR REPLACE INTO response_patterns (pattern_type, weight)
                VALUES (?, ?)
            """,
                (pattern_type, weight),
            )

        conn.commit()

    def get_evolution_status(self) -> Dict:
        """
        Get comprehensive status of evolution engine's learning progress

        Why: Provides real-time insights into Clever's learning state, network
        complexity, and capability growth for monitoring and debugging
        Where: Called by app.py for status endpoints and debug interfaces
        How: Analyzes concept graph, queries capability scores via DatabaseManager

        Args:
            None

        Returns:
            Dict containing evolution metrics, network stats, and capability scores

        Connects to:
            - database.py: Queries capability_evolution table via DatabaseManager
            - NetworkX: Analyzes concept_graph for network metrics
            - app.py: Status reporting and monitoring endpoints
        """
        """Get current evolution status"""
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        # Network analysis with full NetworkX capabilities
        concept_count = len(self.concept_graph.nodes())
        connection_count = len(self.concept_graph.edges())
        network_density = (
            nx.density(self.concept_graph) if concept_count > 0 else 0
        )

        # Advanced network metrics
        clustering_coefficient = (
            nx.average_clustering(self.concept_graph.to_undirected())
            if concept_count > 0
            else 0
        )

        # Calculate centrality measures for top concepts
        centrality_scores = {}
        if concept_count > 1:
            try:
                betweenness = nx.betweenness_centrality(self.concept_graph)
                eigenvector = nx.eigenvector_centrality(self.concept_graph)
                centrality_scores = {
                    "top_betweenness": sorted(
                        betweenness.items(), key=lambda x: x[1], reverse=True
                    )[:5],
                    "top_eigenvector": sorted(
                        eigenvector.items(), key=lambda x: x[1], reverse=True
                    )[:5],
                }
            except Exception:
                centrality_scores = {"error": "Unable to calculate centrality"}

        # Get capability levels
        cursor.execute(
            """SELECT capability_name, current_level
            FROM capability_evolution
            ORDER BY current_level DESC"""
        )
        capabilities = dict(cursor.fetchall())

        # Get recent evolution events
        cursor.execute(
            """SELECT event_type, description, impact_score, timestamp
            FROM evolution_events
            ORDER BY timestamp DESC LIMIT 5"""
        )
        recent_events = cursor.fetchall()

        return {
            "concept_count": concept_count,
            "connection_count": connection_count,
            "capabilities": capabilities,
            "recent_events": recent_events,
            "network_density": network_density,
            "evolution_score": self.calculate_overall_evolution_score(),
        }

    def calculate_overall_evolution_score(self) -> float:
        """Calculate comprehensive intelligence evolution score"""
        node_count = len(self.concept_graph.nodes())
        if node_count == 0:
            return 0.0

        # Advanced network complexity metrics
        network_score = min(1.0, node_count / 1000)
        density_score = nx.density(self.concept_graph)

        # Calculate average concept strength using numpy for efficiency
        concept_strengths = [
            self.concept_graph.nodes[node_id]["concept"].strength
            for node_id in self.concept_graph.nodes()
            if node_id in self.concept_cache
        ]
        avg_strength = np.mean(concept_strengths) if concept_strengths else 0.0

        # Advanced network analysis
        clustering_score = 0.0
        centrality_score = 0.0

        if node_count > 1:
            try:
                # Clustering coefficient
                clustering_score = nx.average_clustering(
                    self.concept_graph.to_undirected()
                )

                # Network centralization
                betweenness = nx.betweenness_centrality(self.concept_graph)
                centrality_score = np.std(list(betweenness.values()))
            except Exception:
                clustering_score = density_score * 0.5
                centrality_score = 0.1

        # Capability progression analysis
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()
        cursor.execute("SELECT AVG(current_level) FROM capability_evolution")
        avg_capability = cursor.fetchone()[0] or 0.1

        # Learning velocity (recent growth trends)
        cursor.execute(
            """
            SELECT AVG(growth_rate) FROM capability_evolution
            WHERE last_exercise > datetime('now', '-7 days')
        """
        )
        recent_growth = cursor.fetchone()[0] or 0.01

        # Comprehensive evolution score with advanced weighting
        evolution_score = (
            network_score * 0.25  # Network size
            + density_score * 0.20  # Connection density
            + avg_strength * 0.25  # Concept strength
            + avg_capability * 0.20  # Capability levels
            + clustering_score * 0.05  # Network clustering
            + centrality_score * 0.03  # Network centralization
            + min(recent_growth * 50, 0.02)  # Recent learning velocity
        )

        return min(1.0, max(0.0, evolution_score))

=======
        ''')
        
        for pattern_type, weight in pattern_weights.items():
            cursor.execute('''
                INSERT OR REPLACE INTO response_patterns (pattern_type, weight)
                VALUES (?, ?)
            ''', (pattern_type, weight))
        
        conn.commit()
        conn.close()
    
    def get_evolution_status(self) -> Dict:
        """Get current evolution status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count concepts
        if nx and hasattr(self.concept_graph, 'nodes'):
            concept_count = len(self.concept_graph.nodes())
            connection_count = len(self.concept_graph.edges())
            network_density = nx.density(self.concept_graph) if concept_count > 0 else 0
        else:
            concept_count = len(self.concept_graph) if isinstance(self.concept_graph, dict) else 0
            connection_count = 0
            network_density = 0
        
        # Get capability levels
        cursor.execute('SELECT capability_name, current_level FROM capability_evolution ORDER BY current_level DESC')
        capabilities = dict(cursor.fetchall())
        
        # Get recent evolution events
        cursor.execute('SELECT event_type, description, impact_score, timestamp FROM evolution_events ORDER BY timestamp DESC LIMIT 5')
        recent_events = cursor.fetchall()
        
        conn.close()
        
        return {
            'concept_count': concept_count,
            'connection_count': connection_count,
            'capabilities': capabilities,
            'recent_events': recent_events,
            'network_density': network_density,
            'evolution_score': self.calculate_overall_evolution_score()
        }
    
    def calculate_overall_evolution_score(self) -> float:
        """Calculate overall intelligence evolution score"""
        if nx and hasattr(self.concept_graph, 'nodes'):
            node_count = len(self.concept_graph.nodes())
            if node_count == 0:
                return 0.0
            
            # Network complexity
            network_score = min(1.0, node_count / 1000)
            
            # Connection density
            density_score = nx.density(self.concept_graph)
            
            # Average concept strength
            total_strength = sum(
                self.concept_graph.nodes[node_id]['concept'].strength 
                for node_id in self.concept_graph.nodes()
            )
            avg_strength = total_strength / node_count
            
        else:
            # Fallback calculation without networkx
            node_count = len(self.concept_graph) if isinstance(self.concept_graph, dict) else 0
            if node_count == 0:
                return 0.0
            
            network_score = min(1.0, node_count / 1000)
            density_score = 0.1  # Basic fallback
            avg_strength = 0.3   # Basic fallback
        
        # Capability progression
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT AVG(current_level) FROM capability_evolution')
        avg_capability = cursor.fetchone()[0] or 0.1
        conn.close()
        
        evolution_score = (network_score * 0.3 + 
                          density_score * 0.2 + 
                          avg_strength * 0.3 + 
                          avg_capability * 0.2)
        
        return min(1.0, evolution_score)
    
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    # Utility methods
    def categorize_sentiment(self, sentiment: float) -> str:
        """Categorize sentiment into ranges"""
        if sentiment > 0.3:
            return "positive"
        elif sentiment < -0.3:
            return "negative"
        else:
            return "neutral"
<<<<<<< HEAD

    def detect_question_type(self, message: str) -> str:
        """Detect type of question"""
        message_lower = message.lower()
        if any(
            word in message_lower
            for word in ["what", "how", "why", "when", "where", "who"]
        ):
            return "wh_question"
        elif message.endswith("?"):
            return "yes_no_question"
        elif any(
            word in message_lower
            for word in ["can you", "could you", "please"]
        ):
            return "request"
        else:
            return "statement"

=======
    
    def detect_question_type(self, message: str) -> str:
        """Detect type of question"""
        message_lower = message.lower()
        if any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            return "wh_question"
        elif message.endswith('?'):
            return "yes_no_question"
        elif any(word in message_lower for word in ['can you', 'could you', 'please']):
            return "request"
        else:
            return "statement"
    
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    def analyze_response_style(self, response: str) -> str:
        """Analyze Clever's response style"""
        if len(response) > 200:
            return "detailed"
<<<<<<< HEAD
        elif any(
            word in response.lower()
            for word in ["!", "awesome", "great", "excited"]
        ):
            return "enthusiastic"
        elif any(
            word in response.lower()
            for word in ["however", "although", "consider"]
        ):
            return "analytical"
        else:
            return "conversational"

=======
        elif any(word in response.lower() for word in ['!', 'awesome', 'great', 'excited']):
            return "enthusiastic"
        elif any(word in response.lower() for word in ['however', 'although', 'consider']):
            return "analytical"
        else:
            return "conversational"
    
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    def calculate_time_decay(self, last_time: datetime) -> float:
        """Calculate time decay factor"""
        hours_passed = (datetime.now() - last_time).total_seconds() / 3600
        return max(0.1, 1.0 - (hours_passed / 168))  # Decay over week
<<<<<<< HEAD

    def save_concept(self, concept: ConceptNode):
        """
        Persist concept node to the centralized database

        Why: Ensures learned concepts survive across application restarts
        and enables persistent knowledge accumulation
        Where: Called by analyze_interaction after creating new concepts
        How: Serializes ConceptNode data and stores via DatabaseManager

        Args:
            concept: ConceptNode instance with learned concept data

        Connects to:
            - database.py: Uses DatabaseManager for thread-safe persistence
            - concept_network table: Stores concept data with JSON serialization
        """
        """Save concept to database"""
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO concept_network
            (concept_id, name, strength, creation_time, last_reinforced,
             related_concepts, source_interactions, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                concept.concept_id,
                concept.name,
                concept.strength,
                concept.creation_time.isoformat(),
                concept.last_reinforced.isoformat(),
                json.dumps(list(concept.related_concepts)),
                json.dumps(concept.source_interactions),
                concept.confidence,
            ),
        )

        conn.commit()

    def save_connection(
        self, concept_a: str, concept_b: str, strength: float, conn_type: str
    ):
        """Save connection to database"""
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO knowledge_connections
            (concept_a, concept_b, connection_strength, connection_type)
            VALUES (?, ?, ?, ?)
        """,
            (concept_a, concept_b, strength, conn_type),
        )

        conn.commit()

    def update_connection_strength(
        self, concept_a: str, concept_b: str, new_strength: float
    ):
        """Update existing connection strength"""
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE knowledge_connections
            SET connection_strength = ?,
                reinforcement_count = reinforcement_count + 1
            WHERE (concept_a = ? AND concept_b = ?)
               OR (concept_a = ? AND concept_b = ?)
        """,
            (new_strength, concept_a, concept_b, concept_b, concept_a),
        )

        conn.commit()

    def log_evolution_event(
        self,
        event_type: str,
        description: str,
        trigger_data: Dict,
        impact_score: float,
    ):
        """
        Log significant learning events for evolution tracking

        Why: Records major learning milestones and capability improvements
        for debugging and understanding Clever's growth patterns
        Where: Called by analyze_interaction when significant learning occurs
        How: Persists event data to evolution_events table via DatabaseManager

        Args:
            event_type: Category of evolution event (e.g., "learning_event")
            description: Human-readable description of the event
            trigger_data: Context data that triggered the evolution
            impact_score: Numerical significance of the event (0.0-1.0)

        Connects to:
            - database.py: Uses DatabaseManager for event persistence
            - evolution_events table: Stores chronological learning history
        """
        """Log evolution event"""
        with self.db_manager._connect() as conn:
            cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO evolution_events
            (event_type, description, trigger_data, impact_score)
            VALUES (?, ?, ?, ?)
        """,
            (event_type, description, json.dumps(trigger_data), impact_score),
        )

        conn.commit()

        self.evolution_log.append(
            {
                "event_type": event_type,
                "description": description,
                "timestamp": datetime.now(),
                "impact_score": impact_score,
            }
        )

=======
    
    def save_concept(self, concept: ConceptNode):
        """Save concept to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO concept_network 
            (concept_id, name, strength, creation_time, last_reinforced, related_concepts, source_interactions, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            concept.concept_id,
            concept.name,
            concept.strength,
            concept.creation_time.isoformat(),
            concept.last_reinforced.isoformat(),
            json.dumps(list(concept.related_concepts)),
            json.dumps(concept.source_interactions),
            concept.confidence
        ))
        
        conn.commit()
        conn.close()
    
    def save_connection(self, concept_a: str, concept_b: str, strength: float, conn_type: str):
        """Save connection to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge_connections 
            (concept_a, concept_b, connection_strength, connection_type)
            VALUES (?, ?, ?, ?)
        ''', (concept_a, concept_b, strength, conn_type))
        
        conn.commit()
        conn.close()
    
    def update_connection_strength(self, concept_a: str, concept_b: str, new_strength: float):
        """Update existing connection strength"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE knowledge_connections 
            SET connection_strength = ?, reinforcement_count = reinforcement_count + 1
            WHERE (concept_a = ? AND concept_b = ?) OR (concept_a = ? AND concept_b = ?)
        ''', (new_strength, concept_a, concept_b, concept_b, concept_a))
        
        conn.commit()
        conn.close()
    
    def log_evolution_event(self, event_type: str, description: str, trigger_data: Dict, impact_score: float):
        """Log evolution event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO evolution_events (event_type, description, trigger_data, impact_score)
            VALUES (?, ?, ?, ?)
        ''', (event_type, description, json.dumps(trigger_data), impact_score))
        
        conn.commit()
        conn.close()
        
        self.evolution_log.append({
            'event_type': event_type,
            'description': description,
            'timestamp': datetime.now(),
            'impact_score': impact_score
        })
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b

# Global evolution engine instance
evolution_engine = None

<<<<<<< HEAD

=======
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
def get_evolution_engine():
    """Get global evolution engine instance"""
    global evolution_engine
    if evolution_engine is None:
        evolution_engine = CleverEvolutionEngine()
    return evolution_engine
