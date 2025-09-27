#!/usr/bin/env python3
"""
NotebookLM-Inspired Document Analysis Engine for Clever

Why: Extends Clever's document analysis capabilities with source-grounded responses,
     cross-document synthesis, and intelligent querying inspired by Google's NotebookLM.
     Transforms Clever into a research partner that can deeply understand and connect
     information across multiple documents while maintaining digital sovereignty.

Where: Integrates with existing ingestion pipeline (pdf_ingestor.py, file_ingestor.py),
       database (database.py), NLP processing (nlp_processor.py), and persona system
       (persona.py) to provide enhanced document-based intelligence.

How: Analyzes ingested documents to create semantic embeddings, citation mappings,
     and cross-document connections. Provides source-grounded responses with citations,
     generates document summaries, identifies key concepts, and creates synthetic
     overviews combining multiple sources.

File Usage:
    - Primary callers: persona.py for document-grounded responses, app.py for API endpoints
    - Key dependencies: database.py for document storage, nlp_processor.py for text analysis
    - Data sources: Ingested documents from pdf_ingestor.py and file_ingestor.py
    - Data destinations: Enhanced responses to persona.py, citation data to database.py
    - Configuration: config.py for system settings and performance limits
    - Database interactions: sources table for document content, new citation tables
    - API endpoints: /api/analyze_documents, /api/generate_overview, /api/find_connections
    - Frontend connections: Document analysis UI components, citation display
    - Background processes: Document relationship analysis, semantic indexing

Connects to:
    - database.py: Document retrieval, citation storage, cross-reference mapping
    - nlp_processor.py: Text analysis, keyword extraction, entity recognition
    - persona.py: Source-grounded response generation with citations
    - pdf_ingestor.py: Enhanced document processing with semantic analysis
    - file_ingestor.py: Text document processing with relationship detection
    - academic_knowledge_engine.py: Academic concept identification and enhancement
    - evolution_engine.py: Learning from document analysis patterns and effectiveness

Performance Notes:
    - Memory usage: Document embeddings and citation maps cached in memory
    - CPU impact: Semantic analysis computationally intensive, batched processing
    - I/O operations: Document retrieval optimized with content hashing
    - Scaling limits: Document count limited by available memory for embeddings

Critical Dependencies:
    - Required packages: sqlite3, pathlib, typing, dataclasses
    - Optional packages: sentence-transformers for embeddings, sklearn for clustering
    - System requirements: Sufficient memory for document embeddings
    - Database schema: Extended sources table, new citations and relationships tables
"""

import json
import logging
import re
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import NamedTuple, Dict, List, Optional, Any, Set, Tuple

# Clever core modules
from database import DatabaseManager
from nlp_processor import get_nlp_processor

# Optional advanced features
try:
    from sentence_transformers import SentenceTransformer
    _EMBEDDINGS_AVAILABLE = True
except ImportError:
    _EMBEDDINGS_AVAILABLE = False

try:
    # Optional sklearn for advanced clustering (not currently used)
    _SKLEARN_AVAILABLE = False  # Disabled for offline sovereignty
except ImportError:
    _SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


class Citation(NamedTuple):
    """Represents a citation to a source document."""
    source_id: int
    filename: str
    excerpt: str
    confidence: float
    page_number: Optional[int] = None


@dataclass
class DocumentSummary:
    """Summary of a document's key information."""
    source_id: int
    filename: str
    key_concepts: List[str]
    main_topics: List[str]
    summary: str
    word_count: int
    reading_time_minutes: int
    academic_level: str
    document_type: str


@dataclass
class CrossDocumentConnection:
    """Represents a connection between two documents."""
    source_id_1: int
    source_id_2: int
    connection_type: str  # 'concept_overlap', 'citation_reference', 'topic_similarity'
    strength: float
    shared_concepts: List[str]
    explanation: str


@dataclass
class SourceGroundedResponse:
    """Response grounded in specific source documents with citations."""
    text: str
    citations: List[Citation]
    confidence: float
    source_ids: List[int]
    synthesis_quality: str  # 'direct', 'synthesized', 'inferred'


class NotebookLMEngine:
    """
    NotebookLM-inspired document analysis and synthesis engine.
    
    Provides source-grounded responses, cross-document analysis, and intelligent
    document querying while maintaining Clever's offline-first principles.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the NotebookLM engine.
        
        Why: Sets up document analysis capabilities with optional advanced features
        Where: Called during system initialization in app.py
        How: Initializes database connection, NLP processor, and optional embeddings
        """
        self.db = db_manager
        self.nlp = get_nlp_processor()
        self._document_cache: Dict[int, Dict[str, Any]] = {}
        self._embeddings_model = None
        self._embeddings_cache: Dict[int, Any] = {}
        
        # Initialize advanced features if available
        if _EMBEDDINGS_AVAILABLE:
            try:
                self._embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("NotebookLM Engine: Sentence embeddings enabled")
            except Exception as _e:
                logger.warning(f"NotebookLM Engine: Could not load embeddings model: {e}")
                self._embeddings_model = None
        
        # Initialize enhanced database schema
        self._init_enhanced_schema()
    
    def _init_enhanced_schema(self):
        """
        Initialize enhanced database schema for document analysis.
        
        Why: Extends existing database with tables for citations, document relationships,
             and semantic analysis results
        Where: Called during engine initialization
        How: Creates additional tables while respecting single-database constraint
        """
        with self.db._lock, self.db._connect() as conn:
            # Document summaries table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_summaries (
                    source_id INTEGER PRIMARY KEY,
                    key_concepts TEXT,  -- JSON array
                    main_topics TEXT,   -- JSON array
                    summary TEXT,
                    word_count INTEGER,
                    reading_time_minutes INTEGER,
                    academic_level TEXT,
                    document_type TEXT,
                    created_ts REAL,
                    FOREIGN KEY (source_id) REFERENCES sources (id)
                )
            """)
            
            # Cross-document connections
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id_1 INTEGER,
                    source_id_2 INTEGER,
                    connection_type TEXT,
                    strength REAL,
                    shared_concepts TEXT,  -- JSON array
                    explanation TEXT,
                    created_ts REAL,
                    FOREIGN KEY (source_id_1) REFERENCES sources (id),
                    FOREIGN KEY (source_id_2) REFERENCES sources (id)
                )
            """)
            
            # Citation tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS citations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_text TEXT,
                    source_id INTEGER,
                    excerpt TEXT,
                    confidence REAL,
                    page_number INTEGER,
                    created_ts REAL,
                    FOREIGN KEY (source_id) REFERENCES sources (id)
                )
            """)
            
            conn.commit()
    
    def analyze_document(self, source_id: int, force_reprocess: bool = False) -> DocumentSummary:
        """
        Analyze a single document to extract key information and create summary.
        
        Why: Provides comprehensive document understanding for source-grounded responses
        Where: Called when documents are ingested or when detailed analysis is needed
        How: Uses NLP processing and academic knowledge to extract concepts and topics
        
        Args:
            source_id: Database ID of the source document
            force_reprocess: Whether to reprocess even if summary exists
            
        Returns:
            DocumentSummary with key concepts, topics, and metadata
        """
        # Check if summary already exists
        if not force_reprocess:
            existing = self._get_document_summary(source_id)
            if existing:
                return existing
        
        # Retrieve document content
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute(
                "SELECT id, filename, content FROM sources WHERE id = ?",
                (source_id,)
            )
            row = cursor.fetchone()
            
        if not row:
            raise ValueError(f"Document with ID {source_id} not found")
        
        doc_id, filename, content = row
        
        # Analyze content with NLP
        analysis = self.nlp.process_text(content)
        
        # Extract key concepts and topics
        key_concepts = self._extract_key_concepts(content, analysis)
        main_topics = self._extract_main_topics(content, analysis)
        
        # Generate summary
        summary = self._generate_document_summary(content, key_concepts, main_topics)
        
        # Calculate metadata
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)  # Assume 200 WPM reading speed
        academic_level = self._assess_academic_level(analysis)
        document_type = self._identify_document_type(filename, content, analysis)
        
        # Create summary object
        doc_summary = DocumentSummary(
            source_id=doc_id,
            filename=filename,
            key_concepts=key_concepts,
            main_topics=main_topics,
            summary=summary,
            word_count=word_count,
            reading_time_minutes=reading_time,
            academic_level=academic_level,
            document_type=document_type
        )
        
        # Store in database
        self._store_document_summary(doc_summary)
        
        return doc_summary
    
    def query_documents(self, query: str, max_sources: int = 5) -> SourceGroundedResponse:
        """
        Query across all documents to provide source-grounded response.
        
        Why: Enables NotebookLM-style document querying with proper citations
        Where: Called by persona.py when user asks questions about documents
        How: Searches across all sources, ranks relevance, generates response with citations
        
        Args:
            query: User's question or search query
            max_sources: Maximum number of sources to consider
            
        Returns:
            SourceGroundedResponse with answer and citations
        """
        # Analyze query
        query_analysis = self.nlp.process_text(query)
        query_keywords = set(query_analysis.get('keywords', []))
        
        # Find relevant documents
        relevant_docs = self._find_relevant_documents(query, query_keywords, max_sources)
        
        if not relevant_docs:
            return SourceGroundedResponse(
                text="I don't have any documents that contain information relevant to your query.",
                citations=[],
                confidence=0.0,
                source_ids=[],
                synthesis_quality='none'
            )
        
        # Extract relevant excerpts and create citations
        citations = []
        response_parts = []
        
        for doc_id, relevance_score in relevant_docs[:max_sources]:
            excerpts = self._extract_relevant_excerpts(doc_id, query, query_keywords)
            
            # Get document info
            with self.db._lock, self.db._connect() as conn:
                cursor = conn.execute(
                    "SELECT filename FROM sources WHERE id = ?",
                    (doc_id,)
                )
                filename = cursor.fetchone()[0]
            
            for excerpt, confidence in excerpts[:2]:  # Max 2 excerpts per document
                citation = Citation(
                    source_id=doc_id,
                    filename=filename,
                    excerpt=excerpt,
                    confidence=confidence
                )
                citations.append(citation)
                response_parts.append(excerpt)
        
        # Synthesize response
        synthesized_text = self._synthesize_response(query, response_parts, citations)
        
        # Determine synthesis quality
        synthesis_quality = self._assess_synthesis_quality(query, citations, synthesized_text)
        
        # Calculate overall confidence
        overall_confidence = sum(c.confidence for c in citations) / len(citations) if citations else 0.0
        
        return SourceGroundedResponse(
            text=synthesized_text,
            citations=citations,
            confidence=overall_confidence,
            source_ids=[doc_id for doc_id, _ in relevant_docs],
            synthesis_quality=synthesis_quality
        )
    
    def find_cross_document_connections(self, source_id: Optional[int] = None) -> List[CrossDocumentConnection]:
        """
        Find connections between documents based on shared concepts and topics.
        
        Why: Enables discovery of relationships across document collection
        Where: Called for document analysis and research assistance
        How: Analyzes document summaries and content for overlapping concepts
        
        Args:
            source_id: If provided, find connections for this specific document
            
        Returns:
            List of cross-document connections with strength scores
        """
        # Get all document summaries
        summaries = self._get_all_document_summaries()
        
        if len(summaries) < 2:
            return []
        
        connections = []
        
        # Compare each pair of documents
        for i, summary1 in enumerate(summaries):
            for j, summary2 in enumerate(summaries[i+1:], i+1):
                # Skip if we're looking for connections to a specific document
                if source_id and summary1.source_id != source_id and summary2.source_id != source_id:
                    continue
                
                connection = self._analyze_document_connection(summary1, summary2)
                if connection and connection.strength > 0.3:  # Threshold for meaningful connections
                    connections.append(connection)
        
        # Sort by connection strength
        connections.sort(key=lambda x: x.strength, reverse=True)
        
        return connections
    
    def generate_collection_overview(self, focus_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate an overview of the entire document collection.
        
        Why: Provides high-level understanding of all ingested knowledge
        Where: Called for collection analysis and research starting points
        How: Aggregates document summaries and identifies key themes
        
        Args:
            focus_topic: Optional topic to focus the overview on
            
        Returns:
            Dictionary with collection statistics, key themes, and recommendations
        """
        summaries = self._get_all_document_summaries()
        
        if not summaries:
            return {
                'total_documents': 0,
                'total_words': 0,
                'key_themes': [],
                'document_types': {},
                'academic_levels': {},
                'reading_time_hours': 0,
                'recommendations': []
            }
        
        # Aggregate statistics
        total_docs = len(summaries)
        total_words = sum(s.word_count for s in summaries)
        total_reading_time = sum(s.reading_time_minutes for s in summaries)
        
        # Analyze themes and topics
        all_concepts = []
        all_topics = []
        doc_types = Counter()
        academic_levels = Counter()
        
        for summary in summaries:
            all_concepts.extend(summary.key_concepts)
            all_topics.extend(summary.main_topics)
            doc_types[summary.document_type] += 1
            academic_levels[summary.academic_level] += 1
        
        # Find most common themes
        key_themes = [concept for concept, count in Counter(all_concepts).most_common(10)]
        
        # Filter by focus topic if provided
        if focus_topic:
            focus_summaries = [s for s in summaries if focus_topic.lower() in ' '.join(s.key_concepts + s.main_topics).lower()]
            if focus_summaries:
                summaries = focus_summaries
                key_themes = [concept for concept, count in Counter(
                    concept for s in focus_summaries for concept in s.key_concepts
                ).most_common(10)]
        
        # Generate recommendations
        recommendations = self._generate_collection_recommendations(summaries, key_themes)
        
        # Get connections count safely
        try:
            connections_count = len(self.find_cross_document_connections())
        except Exception:
            connections_count = 0
        
        return {
            'total_documents': total_docs,
            'total_words': total_words,
            'key_themes': key_themes,
            'document_types': dict(doc_types),
            'academic_levels': dict(academic_levels),
            'reading_time_hours': round(total_reading_time / 60, 1),
            'top_concepts': Counter(all_concepts).most_common(15),
            'connections_found': connections_count,
            'recommendations': recommendations,
            'focus_topic': focus_topic
        }
    
    # Private helper methods
    
    def _get_document_summary(self, source_id: int) -> Optional[DocumentSummary]:
        """Retrieve existing document summary from database."""
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute("""
                SELECT s.filename, ds.key_concepts, ds.main_topics, ds.summary,
                       ds.word_count, ds.reading_time_minutes, ds.academic_level, ds.document_type
                FROM document_summaries ds
                JOIN sources s ON ds.source_id = s.id
                WHERE ds.source_id = ?
            """, (source_id,))
            row = cursor.fetchone()
            
        if not row:
            return None
            
        filename, key_concepts, main_topics, summary, word_count, reading_time, academic_level, document_type = row
        
        return DocumentSummary(
            source_id=source_id,
            filename=filename,
            key_concepts=json.loads(key_concepts) if key_concepts else [],
            main_topics=json.loads(main_topics) if main_topics else [],
            summary=summary,
            word_count=word_count,
            reading_time_minutes=reading_time,
            academic_level=academic_level,
            document_type=document_type
        )
    
    def _store_document_summary(self, summary: DocumentSummary):
        """Store document summary in database."""
        with self.db._lock, self.db._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO document_summaries 
                (source_id, key_concepts, main_topics, summary, word_count, 
                 reading_time_minutes, academic_level, document_type, created_ts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.source_id,
                json.dumps(summary.key_concepts),
                json.dumps(summary.main_topics),
                summary.summary,
                summary.word_count,
                summary.reading_time_minutes,
                summary.academic_level,
                summary.document_type,
                time.time()
            ))
            conn.commit()
    
    def _extract_key_concepts(self, content: str, analysis: Dict[str, Any]) -> List[str]:
        """Extract key concepts from document content."""
        # Start with NLP-extracted keywords
        concepts = set(analysis.get('keywords', []))
        
        # Add entities as concepts
        concepts.update(analysis.get('entities', []))
        
        # Extract academic concepts if academic engine is available
        try:
            from academic_knowledge_engine import get_academic_engine
            academic_engine = get_academic_engine()
            academic_analysis = academic_engine.analyze_academic_content(content)
            if academic_analysis.get('detected_concepts'):
                for concept_data in academic_analysis['detected_concepts'][:5]:
                    concepts.add(concept_data['concept'].name)
        except (ImportError, AttributeError):
            pass
        
        # Filter and rank concepts
        concept_list = list(concepts)
        concept_scores = {}
        
        for concept in concept_list:
            # Score based on frequency and position
            freq = content.lower().count(concept.lower())
            first_occurrence = content.lower().find(concept.lower())
            position_score = 1.0 - (first_occurrence / len(content)) if first_occurrence >= 0 else 0
            concept_scores[concept] = freq + position_score
        
        # Return top concepts
        sorted_concepts = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, score in sorted_concepts[:10]]
    
    def _extract_main_topics(self, content: str, analysis: Dict[str, Any]) -> List[str]:
        """Extract main topics from document content."""
        # Look for section headers and emphasized text
        topics = set()
        
        # Find headers (lines that are shorter and have fewer common words)
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) < 100 and len(line.split()) <= 8:
                # Check if it looks like a header
                if any(word.isupper() for word in line.split()) or ':' in line:
                    topics.add(line.strip(':#-*').strip())
        
        # Extract topics from keywords
        keywords = analysis.get('keywords', [])
        if len(keywords) >= 3:
            topics.update(keywords[:5])
        
        # Add academic topics if available
        try:
            from academic_knowledge_engine import get_academic_engine
            academic_engine = get_academic_engine()
            academic_analysis = academic_engine.analyze_academic_content(content)
            if academic_analysis.get('detected_concepts'):
                for concept_data in academic_analysis['detected_concepts'][:3]:
                    topics.add(concept_data['concept'].domain.value.replace('_', ' ').title())
        except (ImportError, AttributeError):
            pass
        
        return list(topics)[:8]
    
    def _generate_document_summary(self, content: str, key_concepts: List[str], main_topics: List[str]) -> str:
        """Generate a concise summary of the document."""
        # Extract first few sentences as base
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        if not sentences:
            return "Document content could not be summarized."
        
        # Take first sentence and try to find a good concluding sentence
        summary_parts = [sentences[0]]
        
        # Look for sentences containing key concepts
        concept_mentions = []
        for sentence in sentences[1:10]:  # Check first 10 sentences
            if any(concept.lower() in sentence.lower() for concept in key_concepts[:3]):
                concept_mentions.append(sentence)
        
        if concept_mentions:
            summary_parts.append(concept_mentions[0])
        
        # Add topic context if available
        if main_topics:
            topic_context = f"This document covers topics including {', '.join(main_topics[:3])}."
            summary_parts.append(topic_context)
        
        summary = ' '.join(summary_parts)
        
        # Limit summary length
        if len(summary) > 500:
            summary = summary[:497] + "..."
        
        return summary
    
    def _assess_academic_level(self, analysis: Dict[str, Any]) -> str:
        """Assess the academic level of the document."""
        # Basic heuristics based on text analysis
        avg_word_length = analysis.get('avg_word_length', 5)
        sentence_complexity = analysis.get('avg_sentence_length', 15)
        
        if avg_word_length > 6 and sentence_complexity > 20:
            return "Graduate"
        elif avg_word_length > 5.5 and sentence_complexity > 17:
            return "Undergraduate"
        elif avg_word_length > 5 and sentence_complexity > 14:
            return "High School"
        else:
            return "General"
    
    def _identify_document_type(self, filename: str, content: str, analysis: Dict[str, Any]) -> str:
        """Identify the type of document based on filename and content."""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Check filename patterns
        if any(ext in filename_lower for ext in ['.pd', '.doc', '.docx']):
            if 'research' in filename_lower or 'paper' in filename_lower:
                return "Research Paper"
            elif 'report' in filename_lower:
                return "Report"
            elif 'manual' in filename_lower or 'guide' in filename_lower:
                return "Manual/Guide"
        
        # Check content patterns
        if any(pattern in content_lower for pattern in ['abstract:', 'introduction:', 'methodology:', 'conclusion:']):
            return "Academic Paper"
        elif any(pattern in content_lower for pattern in ['chapter', 'table of contents', 'index']):
            return "Book/Chapter"
        elif 'memo' in content_lower[:100] or 'to:' in content_lower[:100]:
            return "Memo"
        elif any(pattern in content_lower for pattern in ['procedure', 'step 1', 'instructions']):
            return "Instructions"
        
        return "Document"
    
    def _find_relevant_documents(self, query: str, query_keywords: Set[str], max_sources: int) -> List[Tuple[int, float]]:
        """Find documents relevant to the query."""
        # Get all documents with their content
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute("SELECT id, filename, content FROM sources")
            documents = cursor.fetchall()
        
        relevance_scores = []
        
        for doc_id, filename, content in documents:
            score = self._calculate_relevance_score(query, query_keywords, content, filename)
            if score > 0.1:  # Minimum relevance threshold
                relevance_scores.append((doc_id, score))
        
        # Sort by relevance and return top results
        relevance_scores.sort(key=lambda x: x[1], reverse=True)
        return relevance_scores[:max_sources]
    
    def _calculate_relevance_score(self, query: str, query_keywords: Set[str], content: str, filename: str) -> float:
        """Calculate relevance score for a document given a query."""
        content_lower = content.lower()
        query_lower = query.lower()
        filename_lower = filename.lower()
        
        score = 0.0
        
        # Direct query match (highest weight)
        if query_lower in content_lower:
            score += 2.0
        
        # Filename relevance
        if any(word in filename_lower for word in query_lower.split()):
            score += 1.5
        
        # Keyword matches
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        keyword_matches = len(query_keywords & content_words)
        score += keyword_matches * 0.5
        
        # Phrase proximity (keywords appearing near each other)
        for keyword in query_keywords:
            if keyword in content_lower:
                score += 0.3
        
        # Document length normalization (prefer documents with more content)
        length_factor = min(1.0, len(content) / 1000)
        score *= (0.5 + length_factor)
        
        return score
    
    def _extract_relevant_excerpts(self, doc_id: int, query: str, query_keywords: Set[str]) -> List[Tuple[str, float]]:
        """Extract relevant excerpts from a document for a given query."""
        # Get document content
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute("SELECT content FROM sources WHERE id = ?", (doc_id,))
            content = cursor.fetchone()[0]
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        excerpts = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            query_lower = query.lower()
            
            confidence = 0.0
            
            # Direct query match
            if query_lower in sentence_lower:
                confidence += 0.8
            
            # Keyword matches
            sentence_words = set(re.findall(r'\b\w+\b', sentence_lower))
            keyword_matches = len(query_keywords & sentence_words)
            confidence += keyword_matches * 0.2
            
            # Context window (include surrounding sentences)
            if confidence > 0.3:
                # Find the sentence index
                try:
                    sentence_idx = sentences.index(sentence)
                    context_start = max(0, sentence_idx - 1)
                    context_end = min(len(sentences), sentence_idx + 2)
                    
                    context_sentences = sentences[context_start:context_end]
                    excerpt = ' '.join(context_sentences)
                    
                    # Limit excerpt length
                    if len(excerpt) > 300:
                        excerpt = excerpt[:297] + "..."
                    
                    excerpts.append((excerpt, confidence))
                except ValueError:
                    pass
        
        # Sort by confidence and return top excerpts
        excerpts.sort(key=lambda x: x[1], reverse=True)
        return excerpts[:3]  # Max 3 excerpts per document
    
    def _synthesize_response(self, query: str, response_parts: List[str], citations: List[Citation]) -> str:
        """Synthesize a coherent response from multiple sources."""
        if not response_parts:
            return "I couldn't find relevant information in the available documents."
        
        # Start with a direct answer approach
        synthesis = "Based on the available documents, here's what I found regarding your query:\n\n"
        
        # Group by source for better organization
        source_groups = defaultdict(list)
        for i, citation in enumerate(citations):
            if i < len(response_parts):
                source_groups[citation.filename].append(response_parts[i])
        
        # Present information by source
        for filename, excerpts in source_groups.items():
            synthesis += f"From {filename}:\n"
            for excerpt in excerpts[:2]:  # Limit excerpts per source
                clean_excerpt = excerpt.strip()
                if not clean_excerpt.endswith('.'):
                    clean_excerpt += "."
                synthesis += f"• {clean_excerpt}\n"
            synthesis += "\n"
        
        # Add connection insights if multiple sources
        if len(source_groups) > 1:
            synthesis += "These sources provide complementary perspectives on your query."
        
        return synthesis.strip()
    
    def _assess_synthesis_quality(self, query: str, citations: List[Citation], synthesized_text: str) -> str:
        """Assess the quality of the synthesized response."""
        if not citations:
            return 'none'
        
        citation_count = len(citations)
        avg_confidence = sum(c.confidence for c in citations) / citation_count
        
        if citation_count == 1 and avg_confidence > 0.7:
            return 'direct'
        elif citation_count > 1 and avg_confidence > 0.5:
            return 'synthesized'
        else:
            return 'inferred'
    
    def _analyze_document_connection(self, summary1: DocumentSummary, summary2: DocumentSummary) -> Optional[CrossDocumentConnection]:
        """Analyze the connection between two documents."""
        concepts1 = set(concept.lower() for concept in summary1.key_concepts)
        concepts2 = set(concept.lower() for concept in summary2.key_concepts)
        
        topics1 = set(topic.lower() for topic in summary1.main_topics)
        topics2 = set(topic.lower() for topic in summary2.main_topics)
        
        # Find overlaps
        concept_overlap = concepts1 & concepts2
        topic_overlap = topics1 & topics2
        
        if not concept_overlap and not topic_overlap:
            return None
        
        # Calculate connection strength
        total_concepts = len(concepts1 | concepts2)
        total_topics = len(topics1 | topics2)
        
        concept_strength = len(concept_overlap) / total_concepts if total_concepts > 0 else 0
        topic_strength = len(topic_overlap) / total_topics if total_topics > 0 else 0
        
        overall_strength = (concept_strength + topic_strength) / 2
        
        if overall_strength < 0.1:
            return None
        
        # Determine connection type
        if concept_overlap and topic_overlap:
            connection_type = 'concept_and_topic_overlap'
        elif concept_overlap:
            connection_type = 'concept_overlap'
        else:
            connection_type = 'topic_similarity'
        
        # Generate explanation
        shared_items = list(concept_overlap | topic_overlap)
        explanation = f"Documents share discussion of: {', '.join(shared_items[:3])}"
        
        return CrossDocumentConnection(
            source_id_1=summary1.source_id,
            source_id_2=summary2.source_id,
            connection_type=connection_type,
            strength=overall_strength,
            shared_concepts=shared_items,
            explanation=explanation
        )
    
    def _get_all_document_summaries(self) -> List[DocumentSummary]:
        """Retrieve all document summaries from database."""
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute("""
                SELECT ds.source_id, s.filename, ds.key_concepts, ds.main_topics, ds.summary,
                       ds.word_count, ds.reading_time_minutes, ds.academic_level, ds.document_type
                FROM document_summaries ds
                JOIN sources s ON ds.source_id = s.id
                ORDER BY ds.created_ts DESC
            """)
            rows = cursor.fetchall()
        
        summaries = []
        for row in rows:
            source_id, filename, key_concepts, main_topics, summary, word_count, reading_time, academic_level, document_type = row
            
            summaries.append(DocumentSummary(
                source_id=source_id,
                filename=filename,
                key_concepts=json.loads(key_concepts) if key_concepts else [],
                main_topics=json.loads(main_topics) if main_topics else [],
                summary=summary,
                word_count=word_count,
                reading_time_minutes=reading_time,
                academic_level=academic_level,
                document_type=document_type
            ))
        
        return summaries
    
    def _generate_collection_recommendations(self, summaries: List[DocumentSummary], key_themes: List[str]) -> List[str]:
        """Generate recommendations based on document collection analysis."""
        recommendations = []
        
        if not summaries:
            return ["Consider adding some documents to build your knowledge base."]
        
        # Analyze document types
        doc_types = Counter(s.document_type for s in summaries)
        academic_levels = Counter(s.academic_level for s in summaries)
        
        # Recommend based on collection composition
        if len(summaries) < 5:
            recommendations.append("Consider adding more documents for richer cross-document analysis.")
        
        if 'Research Paper' in doc_types and doc_types['Research Paper'] > 2:
            recommendations.append("You have several research papers - try asking about methodology comparisons.")
        
        if len(key_themes) > 5:
            recommendations.append(f"Your collection covers diverse topics. Focus queries on themes like: {', '.join(key_themes[:3])}")
        
        if 'Graduate' in academic_levels:
            recommendations.append("Your collection includes advanced academic content - perfect for in-depth analysis.")
        
        # Connection-based recommendations
        connections = self.find_cross_document_connections()
        if len(connections) > 3:
            recommendations.append("Strong connections found between documents - ask about relationships between sources.")
        
        return recommendations[:4]  # Limit to 4 recommendations


# Singleton instance for easy access
_notebooklm_engine = None

def get_notebooklm_engine() -> NotebookLMEngine:
    """
    Get the singleton NotebookLM engine instance.
    
    Why: Provides centralized access to document analysis capabilities
    Where: Called by persona.py, app.py, and other modules needing document analysis
    How: Creates singleton instance with database connection on first call
    """
    global _notebooklm_engine
    if _notebooklm_engine is None:
        from database import db_manager
        _notebooklm_engine = NotebookLMEngine(db_manager)
    return _notebooklm_engine

    def find_unlimited_connections(self, batch_size: int = 1000, 
                                 use_clustering: bool = True,
                                 parallel_processing: bool = True) -> List[CrossDocumentConnection]:
        """
        Ultra-scalable connection discovery for unlimited document collections.
        
        Handles massive collections through intelligent clustering, batching, and 
        parallel processing while maintaining connection quality.
        """
        summaries = self._get_all_document_summaries()
        
        if len(summaries) < 2:
            return []
        
        connections = []
        
        # For very large collections, use hierarchical clustering
        if len(summaries) > 10000:
            connections = self._hierarchical_connection_discovery(summaries)
        elif len(summaries) > 1000:
            connections = self._clustered_connection_discovery(summaries, batch_size)
        else:
            connections = self._standard_connection_discovery(summaries)
        
        # Apply intelligent filtering and ranking
        return self._optimize_connection_results(connections)
    
    def _hierarchical_connection_discovery(self, summaries: List[DocumentSummary]) -> List[CrossDocumentConnection]:
        """Hierarchical approach for massive collections (10k+ documents)."""
        
        # Create semantic clusters based on key concepts
        concept_clusters = defaultdict(list)
        
        for summary in summaries:
            primary_concepts = summary.key_concepts[:3]  # Top 3 concepts
            cluster_key = tuple(sorted(primary_concepts))
            concept_clusters[cluster_key].append(summary)
        
        connections = []
        
        # Find connections within clusters (high similarity)
        for cluster_docs in concept_clusters.values():
            if len(cluster_docs) > 1:
                cluster_connections = self._find_cluster_internal_connections(cluster_docs)
                connections.extend(cluster_connections)
        
        # Find cross-cluster connections (representative sampling)
        cluster_representatives = {}
        for cluster_key, cluster_docs in concept_clusters.items():
            # Select most representative document from each cluster
            representative = max(cluster_docs, key=lambda d: len(d.key_concepts))
            cluster_representatives[cluster_key] = representative
        
        # Compare representatives across clusters
        rep_list = list(cluster_representatives.values())
        for i, doc1 in enumerate(rep_list):
            for doc2 in rep_list[i+1:]:
                connection = self._analyze_document_connection(doc1, doc2)
                if connection and connection.strength > 0.4:  # Higher threshold for cross-cluster
                    connections.append(connection)
        
        return connections
        