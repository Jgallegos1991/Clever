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
#!/usr/bin/env python3

import sqlite3
import json
from datetime import datetime
from collections import Counter, defaultdict
import hashlib
import re
from dataclasses import dataclass
from typing import Dict, List, Set, Optional
from config import DB_PATH

# Optional dependencies with graceful fallbacks
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False
    print("Warning: numpy not available, using fallback math")

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    nx = None
    HAS_NETWORKX = False
    print("Warning: networkx not available, using simple graph fallback")

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        HAS_SPACY = True
    except OSError:
        nlp = None
        HAS_SPACY = False
        print("Warning: spacy model not found, using basic text processing")
except ImportError:
    spacy = None
    nlp = None
    HAS_SPACY = False
    print("Warning: spacy not available, using basic text processing")


@dataclass
class ConceptNode:
    """Represents a learned concept in Clever's mind"""

    concept_id: str
    name: str
    strength: float
    creation_time: datetime
    last_reinforced: datetime
    related_concepts: Set[str]
    source_interactions: List[str]
    confidence: float


class CleverEvolutionEngine:
    """
    Autonomous intelligence growth system
    
    Why: Provides adaptive learning and concept formation for Clever AI system
         with graceful fallbacks when advanced dependencies are unavailable.
    Where: Core intelligence engine used throughout Clever for learning and memory
    How: Uses NetworkX for advanced graph analysis when available, otherwise
         uses simple dict-based graph representation. Supports spaCy for NLP
         with regex fallbacks, and numpy for advanced math with pure Python fallbacks.
    """

    def __init__(self):
        self.db_path = DB_PATH
        self.learning_threshold = 0.3
        self.evolution_log = []
        self.concept_cache = {}

        # Use NetworkX if available, otherwise simple dict-based graph
        if HAS_NETWORKX:
            self.concept_graph = nx.DiGraph()
        else:
            self.concept_graph = defaultdict(set)  # Fallback: dict with concept connections

        self.init_evolution_database()
        self.load_existing_knowledge()

    def init_evolution_database(self):
        """Initialize evolution tracking tables"""
        conn = sqlite3.connect(self.db_path)
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
        conn.close()

    def load_existing_knowledge(self):
        """Load existing concepts into the graph"""
        conn = sqlite3.connect(self.db_path)
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
            
            if HAS_NETWORKX:
                self.concept_graph.add_node(concept_id, concept=concept)
            else:
                # Fallback: Store in dict
                self.concept_graph[concept_id] = concept

        # Load connections
        if HAS_NETWORKX:
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

        conn.close()

    def learn_from_interaction(self, user_input: str, clever_response: str, context: Dict = None):
        """
        Main learning entry point - backwards compatibility with tests
        
        Why: Provides the interface expected by test_suite.py while delegating
             to the core log_interaction method for actual learning processing.
        Where: Called by test_suite.py and other modules expecting this interface
        How: Wraps the interaction data and delegates to log_interaction
        """
        interaction_data = {
            'user_input': user_input,
            'response': clever_response,
            'active_mode': 'Auto',
            'sentiment': 0.0,
            'context': context or {}
        }
        return self.log_interaction(interaction_data)

    def log_interaction(self, interaction_data: Dict):
        """
        Main entry point for logging interactions and triggering learning
        
        Why: Processes user interactions to extract concepts, form connections,
             and drive autonomous intelligence evolution
        Where: Called by app.py and other core modules after user interactions
        How: Analyzes the interaction, extracts concepts, forms connections,
             and logs evolution events
        """
        user_input = interaction_data.get('user_input', '')
        response = interaction_data.get('response', '')
        mode = interaction_data.get('active_mode', 'Auto')
        sentiment = interaction_data.get('sentiment', 0.0)
        
        # Analyze this interaction for learning
        analysis = self.analyze_interaction(user_input, response, mode, sentiment)
        
        # Log the evolution event if significant learning occurred
        if analysis['new_concepts'] or analysis['new_connections']:
            self.log_evolution_event(
                "learning_event",
                f"Learned {len(analysis['new_concepts'])} concepts, {len(analysis['new_connections'])} connections",
                interaction_data,
                0.3
            )

        return analysis

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
            for concept_b in (user_concepts + response_concepts)[i + 1:]:
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
        """
        Extract meaningful concepts from text using available NLP tools
        
        Why: Concept extraction is core to learning - identifies key terms and
             entities from interactions to build knowledge graph
        Where: Used throughout learning pipeline to identify concepts from text
        How: Uses spaCy for advanced NLP when available, falls back to regex
             patterns and word analysis for basic concept extraction
        """
        concepts = []

        if HAS_SPACY and nlp:
            # Advanced extraction with spaCy
            doc = nlp(text)

            # Extract named entities with full coverage
            entity_types = [
                "PERSON", "ORG", "GPE", "EVENT", "WORK_OF_ART",
                "LAW", "LANGUAGE", "PRODUCT", "NORP", "FAC"
            ]
            for ent in doc.ents:
                if ent.label_ in entity_types and len(ent.text.strip()) > 2:
                    concepts.append(ent.text.lower().strip())

            # Extract sophisticated noun phrases
            for chunk in doc.noun_chunks:
                # Filter for meaningful chunks
                if (2 <= len(chunk.text.split()) <= 4 and
                    chunk.root.pos_ in ["NOUN", "PROPN"] and
                        not chunk.root.is_stop):
                    concepts.append(chunk.text.lower().strip())

            # Extract key individual terms
            for token in doc:
                if (token.pos_ in ["NOUN", "PROPN", "ADJ"] and
                    not token.is_stop and not token.is_punct and
                        len(token.text) > 3 and token.lemma_ != "-PRON-"):
                    concepts.append(token.lemma_.lower())

            # Advanced pattern extraction for technical terms
            tech_patterns = re.findall(r'\b[A-Z]{2,}(?:[A-Z][a-z]+)*\b', text)
            concepts.extend([p.lower() for p in tech_patterns])
        else:
            # Fallback extraction without spaCy
            # Extract capitalized words (potential proper nouns)
            proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            concepts.extend([noun.lower() for noun in proper_nouns])

            # Extract technical terms and acronyms
            tech_terms = re.findall(r'\b[A-Z]{2,}\b', text)
            concepts.extend([term.lower() for term in tech_terms])

            # Extract significant words (nouns, adjectives)
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
            concepts.extend([word.lower() for word in words])

        # Filter and deduplicate with enhanced exclusions
        filtered_concepts = []
        excluded_terms = {
            "user", "message", "response", "clever", "system", "thing", "way",
            "time", "part", "place", "person", "word", "text", "example",
            "this", "that", "with", "from", "they", "have", "will", "been"
        }

        for concept in concepts:
            concept = concept.strip()
            if (len(concept) > 2 and
                concept not in excluded_terms and
                not concept.isdigit() and
                not concept.startswith(('http', 'www')) and
                    len(concept.split()) <= 4):
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

        concept = ConceptNode(
            concept_id=concept_id,
            name=name,
            strength=0.1,
            creation_time=now,
            last_reinforced=now,
            related_concepts=set(),
            source_interactions=[user_message[:100]],
            confidence=0.1,
        )

        if HAS_NETWORKX:
            self.concept_graph.add_node(concept_id, concept=concept)
        else:
            # Fallback: Store in dict
            self.concept_graph[concept_id] = concept

        self.concept_cache[concept_id] = concept
        self.save_concept(concept)

        return concept

    def reinforce_concept(self, concept_id: str, sentiment_bonus: float = 0.0):
        """Strengthen existing concept"""
        concept = None
        
        if HAS_NETWORKX:
            if concept_id in self.concept_graph:
                concept = self.concept_graph.nodes[concept_id]["concept"]
        else:
            if concept_id in self.concept_graph:
                concept = self.concept_graph[concept_id]

        if concept:
            # Calculate reinforcement
            base_reinforcement = 0.05
            sentiment_multiplier = 1.0 + (sentiment_bonus * 0.5)
            time_decay = self.calculate_time_decay(concept.last_reinforced)

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
        connection_exists = False
        current_weight = 0.1
        
        if HAS_NETWORKX:
            connection_exists = self.concept_graph.has_edge(id_a, id_b)
            if connection_exists:
                current_weight = self.concept_graph[id_a][id_b]["weight"]
        else:
            # Fallback: Check related concepts in concept nodes
            concept_a_obj = self.concept_graph[id_a]
            if hasattr(concept_a_obj, 'related_concepts'):
                connection_exists = id_b in concept_a_obj.related_concepts

        if connection_exists:
            # Strengthen existing connection
            new_weight = min(1.0, current_weight + 0.1)
            if HAS_NETWORKX:
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
                if HAS_NETWORKX:
                    self.concept_graph.add_edge(
                        id_a,
                        id_b,
                        weight=connection_strength,
                        connection_type="contextual",
                    )
                    # Add to related concepts in NetworkX nodes
                    self.concept_graph.nodes[id_a]["concept"].related_concepts.add(id_b)
                    self.concept_graph.nodes[id_b]["concept"].related_concepts.add(id_a)
                else:
                    # Fallback: Add to related concepts in concept objects
                    self.concept_graph[id_a].related_concepts.add(id_b)
                    self.concept_graph[id_b].related_concepts.add(id_a)
                    
                self.save_connection(
                    id_a, id_b, connection_strength, "contextual"
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
        """Calculate strength of connection between concepts"""
        # Distance in text
        context_lower = context.lower()
        pos_a = context_lower.find(concept_a.lower())
        pos_b = context_lower.find(concept_b.lower())

        if pos_a == -1 or pos_b == -1:
            return 0.0

        distance = abs(pos_a - pos_b)
        proximity_score = max(0, 1.0 - (distance / 100))  # Closer = stronger

        # Semantic similarity using spaCy vectors when available
        semantic_score = 0.1  # Default fallback
        if HAS_SPACY and nlp:
            try:
                doc_a = nlp(concept_a)
                doc_b = nlp(concept_b)
                if doc_a.vector.any() and doc_b.vector.any():
                    semantic_score = doc_a.similarity(doc_b)
                else:
                    # Calculate word-level similarity for out-of-vocab terms
                    words_a = [token.text.lower()
                               for token in doc_a if not token.is_stop]
                    words_b = [token.text.lower()
                               for token in doc_b if not token.is_stop]
                    common_words = set(words_a) & set(words_b)
                    total_words = set(words_a) | set(words_b)
                    semantic_score = len(common_words) / max(1, len(total_words))
            except Exception:
                semantic_score = 0.1
        else:
            # Fallback: Simple word overlap similarity
            words_a = set(concept_a.lower().split())
            words_b = set(concept_b.lower().split())
            common_words = words_a & words_b
            total_words = words_a | words_b
            semantic_score = len(common_words) / max(1, len(total_words))

        # Co-occurrence frequency (simplified for now)
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
        conn = sqlite3.connect(self.db_path)
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
        conn.close()

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

        conn = sqlite3.connect(self.db_path)
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
        conn.close()

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

            if concept_id not in self.concept_graph:
                # Create new concept from PDF
                new_concept = ConceptNode(
                    concept_id=concept_id,
                    name=concept["name"],
                    strength=concept["strength"],
                    creation_time=datetime.now(),
                    last_reinforced=datetime.now(),
                    related_concepts=set(),
                    source_interactions=[f"PDF: {filename}"],
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
            for concept_b in pdf_concepts[i + 1:]:
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

    def extract_domain_terms(self, content: str) -> List[str]:
        """Extract domain-specific terminology"""
        # Technical terms, proper nouns, specialized vocabulary
        domain_patterns = [
            r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b",  # CamelCase
            r"\b[A-Z]{2,}\b",  # Acronyms
            r"\b\w+(?:[-_]\w+)+\b",  # Hyphenated/underscored terms
        ]

        terms = []
        for pattern in domain_patterns:
            matches = re.findall(pattern, content)
            terms.extend([match.lower() for match in matches])

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
            connection_count = len(list(  # type: ignore
                self.concept_graph.neighbors(node_id)  # type: ignore
            ))
            connection_bonus = min(0.2, connection_count * 0.02)

            concept.strength = min(1.0, concept.strength + connection_bonus)
            concept.confidence = min(
                1.0, concept.confidence + connection_bonus * 0.5
            )

            self.save_concept(concept)

    def optimize_connection_weights(self):
        """Optimize connection weights using network analysis"""
        # Use PageRank to identify important concepts
        try:
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

    def identify_knowledge_clusters(self) -> List[Dict]:
        """Identify clusters of related knowledge"""
        try:
            # Use community detection
            undirected_graph = self.concept_graph.to_undirected()  # type: ignore
            communities = nx.community.greedy_modularity_communities(  # type: ignore
                undirected_graph
            )

            clusters = []
            for i, community in enumerate(communities):
                cluster_concepts = []
                for node_id in community:
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
        """Update response generation based on learned patterns"""
        conn = sqlite3.connect(self.db_path)
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

        # Update pattern weights for future responses
        pattern_weights = {}
        for pattern_type, avg_effectiveness, usage_count in effective_patterns:
            weight = avg_effectiveness * (1 + usage_count * 0.1)
            pattern_weights[pattern_type] = min(2.0, weight)

        # Save pattern weights
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS response_patterns (
                pattern_type TEXT PRIMARY KEY,
                weight REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
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
        conn.close()

    def get_evolution_status(self) -> Dict:
        """
        Get current evolution status
        
        Why: Provides comprehensive overview of evolution progress and intelligence
             growth metrics for monitoring and debugging
        Where: Called by test_suite.py and other modules needing evolution metrics
        How: Analyzes concept graph, calculates network metrics using NetworkX when
             available, otherwise provides basic fallback metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Network analysis with NetworkX or fallbacks
        if HAS_NETWORKX:
            concept_count = len(self.concept_graph.nodes())
            connection_count = len(self.concept_graph.edges())
            network_density = nx.density(
                self.concept_graph) if concept_count > 0 else 0

            # Advanced network metrics
            clustering_coefficient = (
                nx.average_clustering(self.concept_graph.to_undirected())
                if concept_count > 0 else 0
            )

            # Calculate centrality measures for top concepts
            centrality_scores = {}
            if concept_count > 1:
                try:
                    betweenness = nx.betweenness_centrality(self.concept_graph)
                    eigenvector = nx.eigenvector_centrality(self.concept_graph)
                    centrality_scores = {
                        "top_betweenness": sorted(betweenness.items(),
                                                  key=lambda x: x[1], reverse=True)[:5],
                        "top_eigenvector": sorted(eigenvector.items(),
                                                  key=lambda x: x[1], reverse=True)[:5]
                    }
                except Exception:
                    centrality_scores = {"error": "Unable to calculate centrality"}
        else:
            # Fallback metrics without NetworkX
            concept_count = len(self.concept_graph) if isinstance(self.concept_graph, dict) else 0
            connection_count = 0
            network_density = 0.1  # Basic fallback
            clustering_coefficient = 0.1
            centrality_scores = {"fallback": "NetworkX not available"}

            # Count connections from database
            cursor.execute("SELECT COUNT(*) FROM knowledge_connections")
            connection_count = cursor.fetchone()[0] or 0

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

        conn.close()

        return {
            "concept_count": concept_count,
            "connection_count": connection_count,
            "capabilities": capabilities,
            "recent_events": recent_events,
            "network_density": network_density,
            "clustering_coefficient": clustering_coefficient,
            "centrality_scores": centrality_scores,
            "evolution_score": self.calculate_overall_evolution_score(),
        }

    def calculate_overall_evolution_score(self) -> float:
        """
        Calculate comprehensive intelligence evolution score
        
        Why: Provides single metric representing overall intelligence development
             and learning progress for monitoring and growth tracking
        Where: Used by get_evolution_status and other metrics systems
        How: Combines network complexity, concept strength, capabilities, and
             learning velocity with different weighting for comprehensive score
        """
        # Get node count with appropriate fallback
        if HAS_NETWORKX:
            node_count = len(self.concept_graph.nodes())
        else:
            node_count = len(self.concept_graph) if isinstance(self.concept_graph, dict) else 0
            
        if node_count == 0:
            return 0.0

        # Basic network complexity metrics
        network_score = min(1.0, node_count / 1000)
        
        if HAS_NETWORKX:
            density_score = nx.density(self.concept_graph)
            
            # Calculate average concept strength using numpy when available
            concept_strengths = [
                self.concept_graph.nodes[node_id]["concept"].strength
                for node_id in self.concept_graph.nodes()
                if node_id in self.concept_cache
            ]
        else:
            density_score = 0.1  # Basic fallback
            
            # Fallback: Get concept strengths from cached concepts
            concept_strengths = [
                concept.strength for concept in self.concept_cache.values()
            ]

        # Calculate average strength with numpy or fallback
        if HAS_NUMPY and concept_strengths:
            avg_strength = np.mean(concept_strengths)
        elif concept_strengths:
            avg_strength = sum(concept_strengths) / len(concept_strengths)
        else:
            avg_strength = 0.0

        # Network analysis metrics with fallbacks
        clustering_score = 0.0
        centrality_score = 0.0

        if HAS_NETWORKX and node_count > 1:
            try:
                # Clustering coefficient
                clustering_score = nx.average_clustering(
                    self.concept_graph.to_undirected()
                )

                # Network centralization
                betweenness = nx.betweenness_centrality(self.concept_graph)
                if HAS_NUMPY:
                    centrality_score = np.std(list(betweenness.values()))
                else:
                    values = list(betweenness.values())
                    mean_val = sum(values) / len(values)
                    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
                    centrality_score = variance ** 0.5  # std dev
            except Exception:
                clustering_score = density_score * 0.5
                centrality_score = 0.1

        # Capability progression analysis
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(current_level) FROM capability_evolution")
        avg_capability = cursor.fetchone()[0] or 0.1

        # Learning velocity (recent growth trends)
        cursor.execute("""
            SELECT AVG(growth_rate) FROM capability_evolution
            WHERE last_exercise > datetime('now', '-7 days')
        """)
        recent_growth = cursor.fetchone()[0] or 0.01
        conn.close()

        # Comprehensive evolution score with adaptive weighting
        evolution_score = (
            network_score * 0.25 +        # Network size
            density_score * 0.20 +        # Connection density
            avg_strength * 0.25 +         # Concept strength
            avg_capability * 0.20 +       # Capability levels
            clustering_score * 0.05 +     # Network clustering
            centrality_score * 0.03 +     # Network centralization
            min(recent_growth * 50, 0.02)  # Recent learning velocity
        )

        return min(1.0, max(0.0, evolution_score))

    # Utility methods
    def categorize_sentiment(self, sentiment: float) -> str:
        """Categorize sentiment into ranges"""
        if sentiment > 0.3:
            return "positive"
        elif sentiment < -0.3:
            return "negative"
        else:
            return "neutral"

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

    def analyze_response_style(self, response: str) -> str:
        """Analyze Clever's response style"""
        if len(response) > 200:
            return "detailed"
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

    def calculate_time_decay(self, last_time: datetime) -> float:
        """Calculate time decay factor"""
        hours_passed = (datetime.now() - last_time).total_seconds() / 3600
        return max(0.1, 1.0 - (hours_passed / 168))  # Decay over week

    def save_concept(self, concept: ConceptNode):
        """Save concept to database"""
        conn = sqlite3.connect(self.db_path)
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
        conn.close()

    def save_connection(
        self, concept_a: str, concept_b: str, strength: float, conn_type: str
    ):
        """Save connection to database"""
        conn = sqlite3.connect(self.db_path)
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
        conn.close()

    def update_connection_strength(
        self, concept_a: str, concept_b: str, new_strength: float
    ):
        """Update existing connection strength"""
        conn = sqlite3.connect(self.db_path)
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
        conn.close()

    def log_evolution_event(
        self,
        event_type: str,
        description: str,
        trigger_data: Dict,
        impact_score: float,
    ):
        """Log evolution event"""
        conn = sqlite3.connect(self.db_path)
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
        conn.close()

        self.evolution_log.append(
            {
                "event_type": event_type,
                "description": description,
                "timestamp": datetime.now(),
                "impact_score": impact_score,
            }
        )


# Global evolution engine instance
evolution_engine = None


def get_evolution_engine():
    """Get global evolution engine instance"""
    global evolution_engine
    if evolution_engine is None:
        evolution_engine = CleverEvolutionEngine()
    return evolution_engine
