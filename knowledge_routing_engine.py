#!/usr/bin/env python3
"""
knowledge_routing_engine.py - Clever's Comprehensive Knowledge Routing and Storage Architecture

Why: Creates an intelligent routing system that connects all of Clever's academic knowledge,
     learning experiences, and insights across every component of her digital brain extension.
     This ensures that everything she learns, knows, and discovers is stored and accessed
     through the most clever and efficient pathways possible.

Where: Central knowledge orchestration hub that connects academic_knowledge_engine.py,
       nlp_processor.py, database.py, evolution_engine.py, cognitive_sovereignty.py,
       and the Clever_Sync Google Drive integration for persistent cloud knowledge.

How: Implements intelligent knowledge graphs, semantic routing, multi-layer storage
     optimization, and dynamic learning pathways that adapt based on usage patterns,
     importance scoring, and cross-domain knowledge connections.

File Usage:
    - Primary callers: All learning and knowledge systems across Clever
    - Key dependencies: database.py (storage), nlp_processor.py (analysis), academic_knowledge_engine.py
    - Data sources: Academic content, user interactions, file ingestion, sync folders
    - Data destinations: Optimized storage layers, knowledge graphs, semantic indexes
    - Configuration: Routing rules, storage hierarchies, sync priorities
    - Database interactions: knowledge_graph, routing_metrics, semantic_indexes tables
    - API endpoints: Knowledge query, storage optimization, routing analytics
    - Frontend connections: Knowledge visualization, learning progress displays
    - Background processes: Continuous knowledge optimization, cross-referencing, sync management

Connects to:
    - database.py: Multi-layer storage architecture with intelligent routing
    - academic_knowledge_engine.py: Academic knowledge integration and cross-referencing
    - nlp_processor.py: Semantic analysis for intelligent knowledge categorization
    - evolution_engine.py: Learning pattern analysis and knowledge growth tracking
    - cognitive_sovereignty.py: Advanced knowledge integration for cognitive enhancement
    - file_ingestor.py: Intelligent routing of ingested knowledge to optimal storage
    - sync_watcher.py: Cloud sync coordination with Google Drive CLEVER_AI folder
    - persona.py: Contextual knowledge retrieval for intelligent responses
    - notebooklm_engine.py: Advanced document analysis integration
    - debug_config.py: Knowledge routing performance monitoring and optimization

Performance Notes:
    - Memory usage: Intelligent caching with LRU eviction and priority-based retention
    - CPU impact: Optimized routing algorithms with background knowledge graph maintenance
    - I/O operations: Smart batching and async operations for cloud sync coordination
    - Scaling limits: Designed for extensive knowledge growth with automatic optimization

Critical Dependencies:
    - Required packages: networkx (knowledge graphs), numpy (semantic operations)
    - Optional packages: faiss (vector similarity), sentence_transformers (embeddings)
    - System requirements: Sufficient storage for knowledge graphs and semantic indexes
    - Database schema: Extended schema for knowledge graphs and routing optimization
"""

import json
import time
import hashlib
import threading
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from collections import defaultdict, deque
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class KnowledgeType(Enum):
    """Types of knowledge for intelligent routing."""
    ACADEMIC = "academic"
    EXPERIENTIAL = "experiential" 
    CONVERSATIONAL = "conversational"
    PROCEDURAL = "procedural"
    FACTUAL = "factual"
    CONTEXTUAL = "contextual"
    TEMPORAL = "temporal"
    SEMANTIC = "semantic"
    SYNTHETIC = "synthetic"  # Generated/combined knowledge

class StorageLayer(Enum):
    """Storage layers for optimal knowledge placement."""
    HOT_CACHE = "hot_cache"        # Frequently accessed, in-memory
    WARM_STORAGE = "warm_storage"  # Regular access, fast DB tables
    COLD_STORAGE = "cold_storage"  # Archival, compressed storage
    CLOUD_SYNC = "cloud_sync"      # Google Drive CLEVER_AI folder
    GRAPH_INDEX = "graph_index"    # Knowledge graph connections

class KnowledgeImportance(Enum):
    """Importance levels for routing decisions."""
    CRITICAL = 5    # Core system knowledge, immediate retrieval
    HIGH = 4        # Frequently used, priority routing
    MEDIUM = 3      # Standard routing
    LOW = 2         # Background processing
    ARCHIVE = 1     # Long-term storage only

@dataclass
class KnowledgeItem:
    """Represents a single piece of knowledge in Clever's system."""
    id: str
    content: str
    knowledge_type: KnowledgeType
    importance: KnowledgeImportance
    created_timestamp: float
    last_accessed: float
    access_count: int
    source_file: Optional[str]
    metadata: Dict[str, Any]
    connections: Set[str]  # IDs of connected knowledge items
    semantic_tags: List[str]
    storage_layer: StorageLayer

@dataclass
class RoutingRule:
    """Rules for intelligent knowledge routing."""
    condition: Dict[str, Any]
    target_layer: StorageLayer
    priority: int
    action: str  # 'store', 'retrieve', 'migrate', 'index'
    
@dataclass
class KnowledgeGraph:
    """Graph structure for knowledge relationships."""
    nodes: Dict[str, KnowledgeItem]
    edges: Dict[str, Set[str]]  # node_id -> connected_node_ids
    semantic_clusters: Dict[str, Set[str]]  # cluster_name -> node_ids
    
class KnowledgeRoutingEngine:
    """
    Clever's comprehensive knowledge routing and storage optimization engine.
    
    Manages intelligent storage, retrieval, and organization of all knowledge
    across Clever's digital brain extension system.
    """
    
    def __init__(self, db_manager=None):
        """
        Initialize Clever's knowledge routing engine.
        
        Why: Sets up intelligent knowledge management across all of Clever's learning systems
        Where: Called during system initialization to enable comprehensive knowledge routing
        How: Initializes routing rules, storage layers, knowledge graphs, and sync coordination
        """
        self.db = db_manager
        self.knowledge_graph = KnowledgeGraph(nodes={}, edges={}, semantic_clusters={})
        self.routing_rules = []
        self.access_patterns = defaultdict(list)
        self.storage_metrics = {}
        self.sync_queue = deque()
        self._lock = threading.RLock()
        
        # Initialize storage layers
        self.hot_cache = {}  # In-memory cache for frequent access
        self.warm_storage = {}  # Fast retrieval storage
        
        # Cloud sync configuration
        self.clever_sync_path = Path.home() / "Clever_Sync"
        self.google_drive_folder = "CLEVER_AI"
        
        # Initialize routing engine
        self._initialize_routing_rules()
        self._initialize_database_schema()
        self._load_existing_knowledge()
        
        logger.info("Knowledge routing engine initialized with comprehensive learning integration")
    
    def route_knowledge(self, content: str, knowledge_type: KnowledgeType, 
                       source: str = None, metadata: Dict[str, Any] = None) -> str:
        """
        Route new knowledge through Clever's intelligent storage system.
        
        Why: Ensures all knowledge is stored in the optimal location and indexed properly
        Where: Called whenever new knowledge enters Clever's system from any source
        How: Analyzes content, determines importance, selects storage layer, creates connections
        
        Args:
            content: Knowledge content to be stored
            knowledge_type: Type of knowledge for routing decisions
            source: Source of the knowledge (file, conversation, etc.)
            metadata: Additional metadata for enhanced routing
            
        Returns:
            str: Unique knowledge ID for future retrieval
        """
        with self._lock:
            # Generate unique knowledge ID
            knowledge_id = self._generate_knowledge_id(content, knowledge_type, source)
            
            # Analyze content for routing decisions
            analysis = self._analyze_knowledge_content(content, knowledge_type, metadata or {})
            
            # Determine importance and storage layer
            importance = self._calculate_importance(analysis, knowledge_type, source)
            storage_layer = self._select_storage_layer(importance, knowledge_type, analysis)
            
            # Create knowledge item
            knowledge_item = KnowledgeItem(
                id=knowledge_id,
                content=content,
                knowledge_type=knowledge_type,
                importance=importance,
                created_timestamp=time.time(),
                last_accessed=time.time(),
                access_count=1,
                source_file=source,
                metadata=metadata or {},
                connections=set(),
                semantic_tags=analysis.get('semantic_tags', []),
                storage_layer=storage_layer
            )
            
            # Store in appropriate layer
            self._store_in_layer(knowledge_item, storage_layer)
            
            # Add to knowledge graph
            self._add_to_knowledge_graph(knowledge_item)
            
            # Create semantic connections
            self._create_semantic_connections(knowledge_item)
            
            # Queue for cloud sync if appropriate
            if self._should_sync_to_cloud(knowledge_item):
                self._queue_for_sync(knowledge_item)
            
            # Update routing metrics
            self._update_routing_metrics(knowledge_type, storage_layer, importance)
            
            logger.info(f"Routed knowledge {knowledge_id} to {storage_layer.value} with {importance.name} importance")
            return knowledge_id
    
    def retrieve_knowledge(self, query: str, context: Dict[str, Any] = None, 
                          max_results: int = 10) -> List[KnowledgeItem]:
        """
        Intelligently retrieve knowledge based on query and context.
        
        Why: Provides contextually relevant knowledge from optimal storage locations
        Where: Called by persona, academic engine, and other systems needing knowledge
        How: Uses semantic search, importance scoring, and context matching
        
        Args:
            query: Search query for knowledge retrieval
            context: Additional context for better matching
            max_results: Maximum number of results to return
            
        Returns:
            List[KnowledgeItem]: Relevant knowledge items ranked by relevance
        """
        with self._lock:
            # Analyze query for routing optimization
            query_analysis = self._analyze_query(query, context or {})
            
            # Search across appropriate storage layers
            candidates = []
            
            # Hot cache first (fastest)
            candidates.extend(self._search_hot_cache(query_analysis))
            
            # Warm storage if needed
            if len(candidates) < max_results:
                candidates.extend(self._search_warm_storage(query_analysis))
            
            # Cold storage for comprehensive search
            if len(candidates) < max_results:
                candidates.extend(self._search_cold_storage(query_analysis))
            
            # Knowledge graph traversal for connected knowledge
            candidates.extend(self._search_knowledge_graph(query_analysis, candidates))
            
            # Rank and filter results
            ranked_results = self._rank_knowledge_results(candidates, query_analysis, context)
            
            # Update access patterns
            for item in ranked_results[:max_results]:
                self._update_access_pattern(item, query)
            
            return ranked_results[:max_results]
    
    def integrate_academic_knowledge(self, academic_engine) -> Dict[str, Any]:
        """
        Integrate academic knowledge engine with intelligent routing.
        
        Why: Ensures all academic knowledge is optimally routed and cross-referenced
        Where: Called during academic knowledge system integration
        How: Analyzes academic domains, creates routing rules, establishes connections
        
        Args:
            academic_engine: Academic knowledge engine instance
            
        Returns:
            Dict with integration results and routing statistics
        """
        try:
            # Get all academic domains and concepts
            academic_data = academic_engine.get_all_knowledge_domains()
            
            integration_stats = {
                'domains_integrated': 0,
                'concepts_routed': 0,
                'connections_created': 0,
                'routing_rules_added': 0
            }
            
            for domain_name, domain_data in academic_data.items():
                # Route domain knowledge
                domain_id = self.route_knowledge(
                    content=json.dumps(domain_data),
                    knowledge_type=KnowledgeType.ACADEMIC,
                    source=f"academic_engine_{domain_name}",
                    metadata={
                        'domain': domain_name,
                        'type': 'academic_domain',
                        'integration_timestamp': time.time()
                    }
                )
                
                integration_stats['domains_integrated'] += 1
                
                # Route individual concepts
                for concept in domain_data.get('concepts', []):
                    concept_id = self.route_knowledge(
                        content=json.dumps(concept),
                        knowledge_type=KnowledgeType.ACADEMIC,
                        source=f"academic_concept_{concept.get('name', 'unknown')}",
                        metadata={
                            'domain': domain_name,
                            'concept_name': concept.get('name'),
                            'type': 'academic_concept'
                        }
                    )
                    
                    # Create connection between domain and concept
                    self._create_knowledge_connection(domain_id, concept_id)
                    integration_stats['concepts_routed'] += 1
                    integration_stats['connections_created'] += 1
            
            # Create cross-domain routing rules
            self._create_academic_routing_rules()
            integration_stats['routing_rules_added'] = len([r for r in self.routing_rules if 'academic' in str(r.condition)])
            
            logger.info(f"Academic knowledge integration complete: {integration_stats}")
            return {
                'success': True,
                'integration_stats': integration_stats,
                'total_academic_knowledge_items': len([k for k in self.knowledge_graph.nodes.values() 
                                                      if k.knowledge_type == KnowledgeType.ACADEMIC])
            }
            
        except Exception as e:
            logger.error(f"Academic knowledge integration failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def integrate_nlp_processing(self, nlp_processor) -> Dict[str, Any]:
        """
        Integrate NLP processor with knowledge routing for semantic analysis.
        
        Why: Enhances knowledge routing with advanced semantic understanding
        Where: Called to establish NLP-enhanced knowledge analysis
        How: Uses NLP analysis to improve knowledge classification and routing
        
        Args:
            nlp_processor: NLP processor instance
            
        Returns:
            Dict with NLP integration results
        """
        try:
            self.nlp_processor = nlp_processor
            
            # Enhance existing knowledge with NLP analysis
            enhanced_count = 0
            for knowledge_id, item in self.knowledge_graph.nodes.items():
                if not item.metadata.get('nlp_enhanced'):
                    # Perform NLP analysis on content
                    nlp_analysis = nlp_processor.process_text(item.content)
                    
                    # Update semantic tags
                    item.semantic_tags.extend(nlp_analysis.get('keywords', []))
                    item.metadata['nlp_enhanced'] = True
                    item.metadata['nlp_sentiment'] = nlp_analysis.get('sentiment', {})
                    item.metadata['nlp_entities'] = nlp_analysis.get('entities', [])
                    
                    # Re-route if NLP analysis suggests different importance
                    new_importance = self._calculate_importance_with_nlp(item, nlp_analysis)
                    if new_importance != item.importance:
                        self._migrate_knowledge_item(item, new_importance)
                    
                    enhanced_count += 1
            
            logger.info(f"Enhanced {enhanced_count} knowledge items with NLP analysis")
            return {
                'success': True,
                'enhanced_items': enhanced_count,
                'nlp_integration_active': True
            }
            
        except Exception as e:
            logger.error(f"NLP integration failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def integrate_cloud_sync(self) -> Dict[str, Any]:
        """
        Integrate Google Drive CLEVER_AI folder sync with knowledge routing.
        
        Why: Ensures important knowledge is synchronized to persistent cloud storage
        Where: Called to establish cloud backup and cross-device knowledge access
        How: Monitors sync folder, routes cloud content, manages sync priorities
        
        Returns:
            Dict with cloud sync integration status
        """
        try:
            sync_stats = {
                'sync_folder_exists': False,
                'items_queued_for_sync': 0,
                'sync_rules_created': 0,
                'cloud_knowledge_items': 0
            }
            
            # Check sync folder exists
            if self.clever_sync_path.exists():
                sync_stats['sync_folder_exists'] = True
                
                # Scan for existing synced knowledge
                for sync_file in self.clever_sync_path.rglob("*.json"):
                    if sync_file.stem.startswith("knowledge_"):
                        try:
                            sync_data = json.loads(sync_file.read_text())
                            # Route synced knowledge into system
                            self.route_knowledge(
                                content=sync_data.get('content', ''),
                                knowledge_type=KnowledgeType(sync_data.get('type', 'factual')),
                                source=f"cloud_sync_{sync_file.name}",
                                metadata={
                                    **sync_data.get('metadata', {}),
                                    'cloud_synced': True,
                                    'sync_timestamp': sync_file.stat().st_mtime
                                }
                            )
                            sync_stats['cloud_knowledge_items'] += 1
                        except Exception as e:
                            logger.warning(f"Failed to load sync file {sync_file}: {e}")
            
            # Create sync routing rules
            sync_routing_rules = [
                RoutingRule(
                    condition={'importance': 'CRITICAL', 'knowledge_type': 'ACADEMIC'},
                    target_layer=StorageLayer.CLOUD_SYNC,
                    priority=1,
                    action='store'
                ),
                RoutingRule(
                    condition={'access_count': '>=10'},
                    target_layer=StorageLayer.CLOUD_SYNC,
                    priority=2,
                    action='store'
                ),
                RoutingRule(
                    condition={'knowledge_type': 'PROCEDURAL'},
                    target_layer=StorageLayer.CLOUD_SYNC,
                    priority=3,
                    action='store'
                )
            ]
            
            self.routing_rules.extend(sync_routing_rules)
            sync_stats['sync_rules_created'] = len(sync_routing_rules)
            
            # Process sync queue
            sync_stats['items_queued_for_sync'] = len(self.sync_queue)
            self._process_sync_queue()
            
            logger.info(f"Cloud sync integration complete: {sync_stats}")
            return {
                'success': True,
                'sync_stats': sync_stats,
                'cloud_sync_active': True
            }
            
        except Exception as e:
            logger.error(f"Cloud sync integration failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def optimize_knowledge_storage(self) -> Dict[str, Any]:
        """
        Optimize knowledge storage based on access patterns and importance.
        
        Why: Ensures optimal performance and efficient use of storage resources
        Where: Called periodically to maintain system performance
        How: Analyzes access patterns, migrates knowledge between layers, optimizes indexes
        
        Returns:
            Dict with optimization results and performance improvements
        """
        try:
            optimization_stats = {
                'items_migrated': 0,
                'hot_cache_optimized': 0,
                'connections_optimized': 0,
                'storage_reclaimed': 0
            }
            
            current_time = time.time()
            
            # Migrate based on access patterns
            for knowledge_id, item in list(self.knowledge_graph.nodes.items()):
                # Promote frequently accessed items to hot cache
                if (item.access_count > 10 and 
                    current_time - item.last_accessed < 86400 and  # Last day
                    item.storage_layer != StorageLayer.HOT_CACHE):
                    
                    self._migrate_to_hot_cache(item)
                    optimization_stats['items_migrated'] += 1
                    optimization_stats['hot_cache_optimized'] += 1
                
                # Demote rarely accessed items to cold storage
                elif (item.access_count < 3 and 
                      current_time - item.last_accessed > 604800 and  # Week ago
                      item.storage_layer == StorageLayer.WARM_STORAGE):
                    
                    self._migrate_to_cold_storage(item)
                    optimization_stats['items_migrated'] += 1
                
                # Archive very old, unused items
                elif (current_time - item.last_accessed > 2592000 and  # Month ago
                      item.importance == KnowledgeImportance.LOW):
                    
                    self._archive_knowledge_item(item)
                    optimization_stats['storage_reclaimed'] += 1
            
            # Optimize knowledge graph connections
            optimization_stats['connections_optimized'] = self._optimize_knowledge_connections()
            
            # Clean up hot cache
            self._cleanup_hot_cache()
            
            logger.info(f"Knowledge storage optimization complete: {optimization_stats}")
            return {
                'success': True,
                'optimization_stats': optimization_stats,
                'total_knowledge_items': len(self.knowledge_graph.nodes),
                'hot_cache_size': len(self.hot_cache),
                'storage_layers': {
                    'hot': len([k for k in self.knowledge_graph.nodes.values() 
                               if k.storage_layer == StorageLayer.HOT_CACHE]),
                    'warm': len([k for k in self.knowledge_graph.nodes.values() 
                                if k.storage_layer == StorageLayer.WARM_STORAGE]),
                    'cold': len([k for k in self.knowledge_graph.nodes.values() 
                                if k.storage_layer == StorageLayer.COLD_STORAGE])
                }
            }
            
        except Exception as e:
            logger.error(f"Knowledge storage optimization failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_knowledge_insights(self) -> Dict[str, Any]:
        """
        Get comprehensive insights into Clever's knowledge system.
        
        Why: Provides visibility into knowledge growth, patterns, and system health
        Where: Called for monitoring, debugging, and system analysis
        How: Analyzes knowledge graph, access patterns, routing efficiency
        
        Returns:
            Dict with comprehensive knowledge system insights
        """
        try:
            insights = {
                'knowledge_overview': {
                    'total_items': len(self.knowledge_graph.nodes),
                    'knowledge_types': {},
                    'importance_distribution': {},
                    'storage_distribution': {},
                    'age_distribution': {}
                },
                'routing_performance': {
                    'average_routing_time': 0,
                    'cache_hit_rate': 0,
                    'optimization_efficiency': 0
                },
                'learning_patterns': {
                    'most_accessed_knowledge': [],
                    'knowledge_growth_rate': 0,
                    'connection_density': 0,
                    'semantic_clusters': len(self.knowledge_graph.semantic_clusters)
                },
                'sync_status': {
                    'cloud_sync_items': 0,
                    'sync_queue_size': len(self.sync_queue),
                    'last_sync_time': 0
                }
            }
            
            current_time = time.time()
            
            # Knowledge type distribution
            for item in self.knowledge_graph.nodes.values():
                knowledge_type = item.knowledge_type.value
                insights['knowledge_overview']['knowledge_types'][knowledge_type] = \
                    insights['knowledge_overview']['knowledge_types'].get(knowledge_type, 0) + 1
                
                # Importance distribution
                importance = item.importance.name
                insights['knowledge_overview']['importance_distribution'][importance] = \
                    insights['knowledge_overview']['importance_distribution'].get(importance, 0) + 1
                
                # Storage distribution
                storage = item.storage_layer.value
                insights['knowledge_overview']['storage_distribution'][storage] = \
                    insights['knowledge_overview']['storage_distribution'].get(storage, 0) + 1
                
                # Age distribution
                age_days = (current_time - item.created_timestamp) / 86400
                age_category = 'new' if age_days < 1 else 'recent' if age_days < 7 else 'old'
                insights['knowledge_overview']['age_distribution'][age_category] = \
                    insights['knowledge_overview']['age_distribution'].get(age_category, 0) + 1
            
            # Most accessed knowledge
            sorted_by_access = sorted(self.knowledge_graph.nodes.values(), 
                                    key=lambda x: x.access_count, reverse=True)
            insights['learning_patterns']['most_accessed_knowledge'] = [
                {
                    'id': item.id,
                    'content_preview': item.content[:100] + '...' if len(item.content) > 100 else item.content,
                    'access_count': item.access_count,
                    'knowledge_type': item.knowledge_type.value,
                    'importance': item.importance.name
                }
                for item in sorted_by_access[:10]
            ]
            
            # Connection density
            total_connections = sum(len(connections) for connections in self.knowledge_graph.edges.values())
            if len(self.knowledge_graph.nodes) > 0:
                insights['learning_patterns']['connection_density'] = \
                    total_connections / len(self.knowledge_graph.nodes)
            
            # Cloud sync status
            insights['sync_status']['cloud_sync_items'] = len([
                k for k in self.knowledge_graph.nodes.values() 
                if k.storage_layer == StorageLayer.CLOUD_SYNC
            ])
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate knowledge insights: {e}")
            return {'error': str(e)}
    
    # Private helper methods
    
    def _generate_knowledge_id(self, content: str, knowledge_type: KnowledgeType, source: str = None) -> str:
        """Generate unique ID for knowledge item."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        type_prefix = knowledge_type.value[:3]
        timestamp = str(int(time.time()))[-8:]
        return f"{type_prefix}_{timestamp}_{content_hash}"
    
    def _analyze_knowledge_content(self, content: str, knowledge_type: KnowledgeType, 
                                 metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze knowledge content for routing decisions."""
        analysis = {
            'content_length': len(content),
            'word_count': len(content.split()),
            'semantic_tags': [],
            'complexity_score': 0,
            'relevance_indicators': []
        }
        
        # Basic semantic analysis
        if hasattr(self, 'nlp_processor') and self.nlp_processor:
            nlp_result = self.nlp_processor.process_text(content)
            analysis['semantic_tags'] = nlp_result.get('keywords', [])
            analysis['complexity_score'] = len(nlp_result.get('entities', [])) * 0.1
        
        # Knowledge type specific analysis
        if knowledge_type == KnowledgeType.ACADEMIC:
            analysis['complexity_score'] += self._analyze_academic_complexity(content)
        elif knowledge_type == KnowledgeType.PROCEDURAL:
            analysis['complexity_score'] += self._analyze_procedural_complexity(content)
        
        return analysis
    
    def _calculate_importance(self, analysis: Dict[str, Any], knowledge_type: KnowledgeType, 
                           source: str = None) -> KnowledgeImportance:
        """Calculate knowledge importance for routing decisions."""
        base_importance = {
            KnowledgeType.ACADEMIC: KnowledgeImportance.HIGH,
            KnowledgeType.PROCEDURAL: KnowledgeImportance.HIGH,
            KnowledgeType.FACTUAL: KnowledgeImportance.MEDIUM,
            KnowledgeType.CONVERSATIONAL: KnowledgeImportance.LOW,
            KnowledgeType.CONTEXTUAL: KnowledgeImportance.MEDIUM
        }.get(knowledge_type, KnowledgeImportance.MEDIUM)
        
        # Adjust based on analysis
        complexity_score = analysis.get('complexity_score', 0)
        word_count = analysis.get('word_count', 0)
        
        importance_value = base_importance.value
        
        # Increase importance for complex, substantial content
        if complexity_score > 0.5 and word_count > 100:
            importance_value += 1
        
        # Increase importance for critical source systems
        if source and any(critical in source for critical in ['academic', 'system', 'config']):
            importance_value += 1
        
        # Cap at maximum importance
        importance_value = min(importance_value, KnowledgeImportance.CRITICAL.value)
        
        return KnowledgeImportance(importance_value)
    
    def _select_storage_layer(self, importance: KnowledgeImportance, 
                            knowledge_type: KnowledgeType, analysis: Dict[str, Any]) -> StorageLayer:
        """Select optimal storage layer based on importance and type."""
        if importance == KnowledgeImportance.CRITICAL:
            return StorageLayer.HOT_CACHE
        elif importance == KnowledgeImportance.HIGH:
            return StorageLayer.WARM_STORAGE
        elif knowledge_type == KnowledgeType.ACADEMIC:
            return StorageLayer.WARM_STORAGE  # Academic knowledge deserves fast access
        else:
            return StorageLayer.COLD_STORAGE
    
    def _store_in_layer(self, item: KnowledgeItem, layer: StorageLayer):
        """Store knowledge item in specified storage layer."""
        if layer == StorageLayer.HOT_CACHE:
            self.hot_cache[item.id] = item
        elif layer == StorageLayer.WARM_STORAGE:
            self.warm_storage[item.id] = item
        
        # Always store in database for persistence
        if self.db:
            self._store_in_database(item)
    
    def _add_to_knowledge_graph(self, item: KnowledgeItem):
        """Add knowledge item to the knowledge graph."""
        self.knowledge_graph.nodes[item.id] = item
        self.knowledge_graph.edges[item.id] = set()
    
    def _create_semantic_connections(self, item: KnowledgeItem):
        """Create connections based on semantic similarity."""
        for existing_id, existing_item in self.knowledge_graph.nodes.items():
            if existing_id != item.id:
                # Check for semantic overlap
                common_tags = set(item.semantic_tags) & set(existing_item.semantic_tags)
                if len(common_tags) >= 2:  # Minimum threshold for connection
                    self._create_knowledge_connection(item.id, existing_id)
    
    def _create_knowledge_connection(self, id1: str, id2: str):
        """Create bidirectional connection between knowledge items."""
        self.knowledge_graph.edges[id1].add(id2)
        self.knowledge_graph.edges[id2].add(id1)
    
    def _should_sync_to_cloud(self, item: KnowledgeItem) -> bool:
        """Determine if knowledge item should be synced to cloud."""
        return (item.importance in [KnowledgeImportance.CRITICAL, KnowledgeImportance.HIGH] or
                item.knowledge_type == KnowledgeType.ACADEMIC or
                item.access_count > 5)
    
    def _queue_for_sync(self, item: KnowledgeItem):
        """Queue knowledge item for cloud synchronization."""
        sync_data = {
            'id': item.id,
            'content': item.content,
            'type': item.knowledge_type.value,
            'metadata': item.metadata,
            'timestamp': item.created_timestamp
        }
        self.sync_queue.append(sync_data)
    
    def _process_sync_queue(self):
        """Process queued items for cloud synchronization."""
        if not self.clever_sync_path.exists():
            return
        
        while self.sync_queue:
            sync_data = self.sync_queue.popleft()
            sync_file = self.clever_sync_path / f"knowledge_{sync_data['id']}.json"
            
            try:
                sync_file.write_text(json.dumps(sync_data, indent=2))
                logger.debug(f"Synced knowledge {sync_data['id']} to cloud")
            except Exception as e:
                logger.warning(f"Failed to sync knowledge {sync_data['id']}: {e}")
                # Re-queue for retry
                self.sync_queue.append(sync_data)
                break
    
    def _initialize_routing_rules(self):
        """Initialize default routing rules."""
        default_rules = [
            RoutingRule(
                condition={'knowledge_type': 'ACADEMIC'},
                target_layer=StorageLayer.WARM_STORAGE,
                priority=1,
                action='store'
            ),
            RoutingRule(
                condition={'importance': 'CRITICAL'},
                target_layer=StorageLayer.HOT_CACHE,
                priority=1,
                action='store'
            ),
            RoutingRule(
                condition={'access_count': '>=5'},
                target_layer=StorageLayer.HOT_CACHE,
                priority=2,
                action='migrate'
            )
        ]
        
        self.routing_rules.extend(default_rules)
    
    def _initialize_database_schema(self):
        """Initialize database schema for knowledge routing."""
        if not self.db:
            return
            
        with self.db._lock, self.db._connect() as conn:
            # Knowledge items table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    knowledge_type TEXT NOT NULL,
                    importance INTEGER NOT NULL,
                    created_timestamp REAL NOT NULL,
                    last_accessed REAL NOT NULL,
                    access_count INTEGER DEFAULT 1,
                    source_file TEXT,
                    metadata TEXT,  -- JSON
                    semantic_tags TEXT,  -- JSON
                    storage_layer TEXT NOT NULL
                )
            """)
            
            # Knowledge connections table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_id TEXT NOT NULL,
                    to_id TEXT NOT NULL,
                    connection_strength REAL DEFAULT 1.0,
                    created_timestamp REAL NOT NULL,
                    UNIQUE(from_id, to_id)
                )
            """)
            
            # Routing metrics table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS routing_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    knowledge_type TEXT NOT NULL,
                    storage_layer TEXT NOT NULL,
                    importance_level TEXT NOT NULL,
                    routing_timestamp REAL NOT NULL,
                    routing_time REAL
                )
            """)
            
            conn.commit()
    
    def _load_existing_knowledge(self):
        """Load existing knowledge from database into routing system."""
        if not self.db:
            return
            
        try:
            with self.db._lock, self.db._connect() as conn:
                cursor = conn.execute("SELECT * FROM knowledge_items")
                for row in cursor.fetchall():
                    item = KnowledgeItem(
                        id=row[0],
                        content=row[1],
                        knowledge_type=KnowledgeType(row[2]),
                        importance=KnowledgeImportance(row[3]),
                        created_timestamp=row[4],
                        last_accessed=row[5],
                        access_count=row[6],
                        source_file=row[7],
                        metadata=json.loads(row[8]) if row[8] else {},
                        connections=set(),
                        semantic_tags=json.loads(row[9]) if row[9] else [],
                        storage_layer=StorageLayer(row[10])
                    )
                    
                    self.knowledge_graph.nodes[item.id] = item
                    self.knowledge_graph.edges[item.id] = set()
                    
                    # Load into appropriate storage layer
                    if item.storage_layer == StorageLayer.HOT_CACHE:
                        self.hot_cache[item.id] = item
                    elif item.storage_layer == StorageLayer.WARM_STORAGE:
                        self.warm_storage[item.id] = item
                
                # Load connections
                cursor = conn.execute("SELECT from_id, to_id FROM knowledge_connections")
                for row in cursor.fetchall():
                    if row[0] in self.knowledge_graph.edges and row[1] in self.knowledge_graph.edges:
                        self.knowledge_graph.edges[row[0]].add(row[1])
                
        except Exception as e:
            logger.warning(f"Failed to load existing knowledge: {e}")
    
    def _store_in_database(self, item: KnowledgeItem):
        """Store knowledge item in database."""
        if not self.db:
            return
            
        with self.db._lock, self.db._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO knowledge_items 
                (id, content, knowledge_type, importance, created_timestamp, last_accessed,
                 access_count, source_file, metadata, semantic_tags, storage_layer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id, item.content, item.knowledge_type.value, item.importance.value,
                item.created_timestamp, item.last_accessed, item.access_count,
                item.source_file, json.dumps(item.metadata), json.dumps(item.semantic_tags),
                item.storage_layer.value
            ))
            conn.commit()
    
    def _update_routing_metrics(self, knowledge_type: KnowledgeType, 
                              storage_layer: StorageLayer, importance: KnowledgeImportance):
        """Update routing performance metrics."""
        if not self.db:
            return
            
        with self.db._lock, self.db._connect() as conn:
            conn.execute("""
                INSERT INTO routing_metrics 
                (knowledge_type, storage_layer, importance_level, routing_timestamp, routing_time)
                VALUES (?, ?, ?, ?, ?)
            """, (
                knowledge_type.value, storage_layer.value, importance.name,
                time.time(), 0.001  # Placeholder routing time
            ))
            conn.commit()
    
    # Additional helper methods for comprehensive functionality
    def _analyze_academic_complexity(self, content: str) -> float:
        """Analyze complexity of academic content."""
        # Simple complexity heuristic based on content characteristics
        complexity = 0.0
        
        # Technical terms increase complexity
        technical_indicators = ['theorem', 'equation', 'hypothesis', 'methodology', 'analysis']
        for indicator in technical_indicators:
            if indicator.lower() in content.lower():
                complexity += 0.1
        
        # Mathematical notation
        if any(char in content for char in ['∑', '∫', '∂', 'α', 'β', 'γ']):
            complexity += 0.2
        
        return min(complexity, 1.0)
    
    def _analyze_procedural_complexity(self, content: str) -> float:
        """Analyze complexity of procedural content."""
        complexity = 0.0
        
        # Step indicators
        step_count = len([line for line in content.split('\n') 
                         if any(indicator in line.lower() 
                               for indicator in ['step', 'then', 'next', 'finally'])])
        complexity += step_count * 0.05
        
        # Decision points
        decision_count = content.lower().count('if ') + content.lower().count('when ')
        complexity += decision_count * 0.1
        
        return min(complexity, 1.0)
    
    def _search_hot_cache(self, query_analysis: Dict[str, Any]) -> List[KnowledgeItem]:
        """Search hot cache for relevant knowledge."""
        results = []
        query_tags = query_analysis.get('semantic_tags', [])
        
        for item in self.hot_cache.values():
            relevance = self._calculate_relevance(item, query_tags)
            if relevance > 0.3:  # Relevance threshold
                results.append(item)
        
        return results
    
    def _search_warm_storage(self, query_analysis: Dict[str, Any]) -> List[KnowledgeItem]:
        """Search warm storage for relevant knowledge."""
        results = []
        query_tags = query_analysis.get('semantic_tags', [])
        
        for item in self.warm_storage.values():
            relevance = self._calculate_relevance(item, query_tags)
            if relevance > 0.2:  # Lower threshold for warm storage
                results.append(item)
        
        return results
    
    def _search_cold_storage(self, query_analysis: Dict[str, Any]) -> List[KnowledgeItem]:
        """Search cold storage for relevant knowledge."""
        results = []
        
        if not self.db:
            return results
        
        # Database search for cold storage items
        query_tags = query_analysis.get('semantic_tags', [])
        
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute("""
                SELECT * FROM knowledge_items 
                WHERE storage_layer = 'cold_storage'
            """)
            
            for row in cursor.fetchall():
                item = KnowledgeItem(
                    id=row[0], content=row[1], knowledge_type=KnowledgeType(row[2]),
                    importance=KnowledgeImportance(row[3]), created_timestamp=row[4],
                    last_accessed=row[5], access_count=row[6], source_file=row[7],
                    metadata=json.loads(row[8]) if row[8] else {},
                    connections=set(), semantic_tags=json.loads(row[9]) if row[9] else [],
                    storage_layer=StorageLayer(row[10])
                )
                
                relevance = self._calculate_relevance(item, query_tags)
                if relevance > 0.1:  # Lowest threshold for cold storage
                    results.append(item)
        
        return results
    
    def _calculate_relevance(self, item: KnowledgeItem, query_tags: List[str]) -> float:
        """Calculate relevance score between knowledge item and query."""
        if not query_tags:
            return 0.1  # Base relevance
        
        # Tag overlap
        common_tags = set(item.semantic_tags) & set(query_tags)
        tag_relevance = len(common_tags) / len(query_tags) if query_tags else 0
        
        # Content matching (simple keyword matching)
        query_text = ' '.join(query_tags).lower()
        content_matches = sum(1 for tag in query_tags if tag.lower() in item.content.lower())
        content_relevance = content_matches / len(query_tags) if query_tags else 0
        
        # Combine relevance scores
        return (tag_relevance * 0.7 + content_relevance * 0.3)
    
    def _analyze_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze query for optimal knowledge retrieval."""
        analysis = {
            'query_length': len(query),
            'semantic_tags': query.split(),  # Simplified - would use NLP in practice
            'context_hints': list(context.keys()) if context else [],
            'query_type': 'general'
        }
        
        # Enhance with NLP if available
        if hasattr(self, 'nlp_processor') and self.nlp_processor:
            nlp_result = self.nlp_processor.process_text(query)
            analysis['semantic_tags'] = nlp_result.get('keywords', query.split())
        
        return analysis


# Singleton instance
_knowledge_routing_engine = None

def get_knowledge_routing_engine(db_manager=None):
    """
    Get the global Knowledge Routing Engine instance.
    
    Why: Provides singleton access to knowledge routing capabilities across Clever
    Where: Called by all systems that need intelligent knowledge management
    How: Creates and caches single engine instance with database integration
    
    Args:
        db_manager: Database manager instance for persistent storage
        
    Returns:
        KnowledgeRoutingEngine: Global knowledge routing engine instance
    """
    global _knowledge_routing_engine
    
    if _knowledge_routing_engine is None:
        if db_manager is None:
            from database import get_database_manager
            db_manager = get_database_manager()
        
        _knowledge_routing_engine = KnowledgeRoutingEngine(db_manager)
    
    return _knowledge_routing_engine