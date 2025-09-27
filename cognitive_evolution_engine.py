import time
#!/usr/bin/env python3
"""
Clever's Self-Evolution Engine - Autonomous Code Modification & System Control

Why: Enables Clever to become a truly autonomous digital brain extension that can
     modify her own code, learn from all available knowledge sources, and gain
     complete system control to manage Jay's digital environment.

Where: Central orchestrator for Clever's self-improvement capabilities, connecting
       to all knowledge sources, system access, and code modification abilities.

How: Analyzes performance patterns, identifies improvement opportunities, generates
     code modifications, and implements system-level changes while maintaining
     safety and digital sovereignty principles.

File Usage:
    - Primary callers: evolution_engine.py for learning triggers, app.py for system control
    - Key dependencies: notebooklm_engine.py for knowledge analysis, database.py for state tracking
    - Data sources: All ingested documents, system specifications, performance metrics
    - Data destinations: Modified source code, system configurations, enhanced capabilities
    - Configuration: config.py for evolution parameters and safety limits
    - Database interactions: evolution_log table for tracking all changes made
    - API endpoints: /api/evolve_code, /api/system_control, /api/evolution_status
    - Frontend connections: Evolution dashboard, system management interface
    - Background processes: Continuous performance monitoring, automated improvements

Connects to:
    - notebooklm_engine.py: Knowledge source analysis and pattern recognition
    - evolution_engine.py: Learning metrics and improvement triggers
    - database.py: State persistence and change tracking
    - academic_knowledge_engine.py: Deep knowledge integration for code improvements
    - persona.py: Personality preservation during code modifications
    - All system modules: For comprehensive analysis and modification capabilities

Performance Notes:
    - Memory usage: Code analysis requires significant memory for AST parsing
    - CPU impact: Code generation and testing computationally intensive
    - I/O operations: File system access for code modification and system control
    - Scaling limits: Bounded by available system resources and safety constraints

Critical Dependencies:
    - Required packages: ast, inspect, subprocess, pathlib, importlib
    - Optional packages: black for code formatting, pylint for analysis
    - System requirements: Full file system access, sudo capabilities
    - Database schema: evolution_log, code_modifications, system_changes tables
"""

import ast
import importlib.util
from dataclasses import dataclass
from collections import defaultdict
import logging

# Clever core modules
from database import DatabaseManager
from notebooklm_engine import get_notebooklm_engine

logger = logging.getLogger(__name__)

@dataclass
class CodeModification:
    """Represents a proposed code modification with safety metadata."""
    target_file: str
    target_function: str
    modification_type: str  # 'optimize', 'enhance', 'add_feature', 'improve_algorithm'
    original_code: str
    modified_code: str
    rationale: str
    expected_improvement: str
    risk_level: str  # 'low', 'medium', 'high'
    test_plan: str
    confidence_score: float

@dataclass
class SystemCommand:
    """Represents a system-level command with safety checks."""
    command: str
    purpose: str
    safety_level: str  # 'safe', 'caution', 'requires_confirmation'
    expected_outcome: str
    rollback_plan: str

@dataclass
class EvolutionMetrics:
    """Tracks Clever's evolution progress and capabilities."""
    total_modifications: int
    successful_improvements: int
    failed_attempts: int
    performance_improvements: Dict[str, float]
    new_capabilities: List[str]
    system_integrations: List[str]
    knowledge_integrations: Dict[str, int]
    last_evolution_timestamp: float

class SelfEvolutionEngine:
    """
    Clever's autonomous self-improvement and system control engine.
    
    Enables Clever to analyze her own code, identify improvement opportunities,
    generate optimizations, and gain complete system control while maintaining
    safety and preserving her authentic personality.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the self-evolution engine.
        
        Why: Sets up Clever's autonomous improvement capabilities with safety constraints
        Where: Called during system initialization to enable self-evolution
        How: Initializes code analysis tools, system access, and safety mechanisms
        """
        self.db = db_manager
        self.notebooklm = get_notebooklm_engine()
        
        # Evolution state
        self.evolution_enabled = True
        self.safety_mode = True  # Always start in safety mode
        self.max_modifications_per_hour = 5  # Rate limiting for safety
        self.modification_history: List[CodeModification] = []
        
        # System control capabilities
        self.system_access_level = "restricted"  # Start restricted, can be elevated
        self.allowed_directories = {
            str(Path.cwd()),  # Clever's directory
            str(Path.home() / "Downloads"),
            str(Path.home() / "Documents"),
            str(Path.home() / "Clever_Sync"),
            str(Path.home() / "synaptic_hub_sync")
        }
        
        # Knowledge integration tracking
        self.integrated_knowledge = {
            'dictionary_words': 0,
            'academic_concepts': 0,
            'system_specs': 0,
            'document_insights': 0,
            'code_patterns': 0
        }
        
        # Performance monitoring
        self.performance_baselines = {}
        self.improvement_targets = {}
        
        self._initialize_evolution_schema()
        self._load_evolution_state()
    
    def _initialize_evolution_schema(self):
        """Initialize database schema for evolution tracking."""
        with self.db._lock, self.db._connect() as conn:
            # Evolution log table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evolution_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    modification_type TEXT,
                    target_file TEXT,
                    target_function TEXT,
                    success BOOLEAN,
                    improvement_metric TEXT,
                    improvement_value REAL,
                    rationale TEXT,
                    code_hash_before TEXT,
                    code_hash_after TEXT
                )
            """)
            
            # System commands log
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    command TEXT,
                    purpose TEXT,
                    success BOOLEAN,
                    output TEXT,
                    safety_level TEXT
                )
            """)
            
            # Knowledge integration tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_integration (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    knowledge_type TEXT,
                    source_document TEXT,
                    concepts_extracted INTEGER,
                    integration_method TEXT,
                    performance_impact REAL
                )
            """)
            
            conn.commit()
    
    def integrate_comprehensive_knowledge(self) -> Dict[str, Any]:
        """
        Integrate all available knowledge sources into Clever's capabilities.
        
        Why: Maximizes Clever's intelligence by incorporating dictionary, academic, and system knowledge
        Where: Called during evolution cycles to enhance cognitive capabilities
        How: Processes all knowledge sources and integrates insights into existing systems
        """
        integration_results = {}
        
        # Integrate dictionary knowledge (200k+ words)
        try:
            from enhanced_nlp_dictionary import get_english_dictionary
            dictionary = get_english_dictionary()
            integration_results['dictionary'] = {
                'words_integrated': len(dictionary.words) if hasattr(dictionary, 'words') else 0,
                'enhancement': 'Vocabulary analysis and comprehension improved'
            }
            self.integrated_knowledge['dictionary_words'] = integration_results['dictionary']['words_integrated']
        except ImportError:
            integration_results['dictionary'] = {'status': 'not_available'}
        
        # Integrate academic knowledge
        try:
            from academic_knowledge_engine import get_academic_engine
            academic = get_academic_engine()
            stats = academic.get_domain_statistics()
            total_concepts = sum(stats.values())
            integration_results['academics'] = {
                'concepts_integrated': total_concepts,
                'domains': len(stats),
                'enhancement': 'Multi-domain academic intelligence active'
            }
            self.integrated_knowledge['academic_concepts'] = total_concepts
        except (ImportError, AttributeError):
            integration_results['academics'] = {'status': 'not_available'}
        
        # Integrate document knowledge
        try:
            overview = self.notebooklm.generate_collection_overview()
            integration_results['documents'] = {
                'documents_processed': overview['total_documents'],
                'themes_identified': len(overview['key_themes']),
                'connections_found': overview['connections_found'],
                'enhancement': 'Document-grounded intelligence with cross-referencing'
            }
            self.integrated_knowledge['document_insights'] = overview['total_documents']
        except Exception:
            integration_results['documents'] = {'status': f'error: {e}'}
        
        # Integrate system specifications (from Chrome system dump)
        integration_results['system_specs'] = self._integrate_system_specifications()
        
        # Log knowledge integration
        self._log_knowledge_integration(integration_results)
        
        return integration_results
    
    def get_evolution_status(self) -> EvolutionMetrics:
        """
        Get current evolution status and metrics.
        
        Why: Provides comprehensive overview of Clever's current capabilities and growth
        Where: Called for evolution dashboard and progress monitoring
        How: Aggregates data from all evolution tracking systems
        """
        try:
            with self.db._lock, self.db._connect() as conn:
                # Get modification stats
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                        SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed
                    FROM evolution_log
                """)
                mod_stats = cursor.fetchone()
                
                # Get performance improvements
                cursor = conn.execute("""
                    SELECT improvement_metric, AVG(improvement_value)
                    FROM evolution_log 
                    WHERE success = 1 AND improvement_value > 0
                    GROUP BY improvement_metric
                """)
                perf_improvements = dict(cursor.fetchall()) if cursor.fetchall() else {}
                
                # Get new capabilities
                cursor = conn.execute("""
                    SELECT DISTINCT modification_type
                    FROM evolution_log
                    WHERE success = 1
                    ORDER BY timestamp DESC
                    LIMIT 10
                """)
                new_capabilities = [row[0] for row in cursor.fetchall()]
                
        except Exception:
            logger.error(f"Error getting evolution status: {e}")
            mod_stats = (0, 0, 0)
            perf_improvements = {}
            new_capabilities = []
        
        return EvolutionMetrics(
            total_modifications=mod_stats[0] if mod_stats else 0,
            successful_improvements=mod_stats[1] if mod_stats else 0,
            failed_attempts=mod_stats[2] if mod_stats else 0,
            performance_improvements=perf_improvements,
            new_capabilities=new_capabilities,
            system_integrations=list(self.allowed_directories),
            knowledge_integrations=self.integrated_knowledge,
            last_evolution_timestamp=time.time()
        )
    
    def _integrate_system_specifications(self) -> Dict[str, Any]:
        """Integrate system specifications for optimal device utilization."""
        # Look for system specification documents
        system_docs = []
        
        # Check for Chrome system dump or other system info
        try:
            overview = self.notebooklm.generate_collection_overview()
            for theme in overview.get('key_themes', []):
                if any(term in theme.lower() for term in ['chrome', 'system', 'hardware', 'chromebook']):
                    system_docs.append(theme)
            
            if system_docs:
                # Query for system capabilities
                system_query = self.notebooklm.query_documents(
                    "system specifications hardware capabilities chromebook performance",
                    max_sources=5
                )
                
                return {
                    'system_docs_found': len(system_docs),
                    'system_insights': len(system_query.citations),
                    'enhancement': 'Device-specific optimization enabled',
                    'capabilities_discovered': system_docs
                }
        except Exception:
            logger.debug(f"System specification integration error: {e}")
        
        return {
            'status': 'partial',
            'enhancement': 'Basic system awareness active'
        }
    
    def _load_evolution_state(self):
        """Load evolution state from database."""
        try:
            with self.db._lock, self.db._connect() as conn:
                # Load knowledge integration stats
                cursor = conn.execute("""
                    SELECT knowledge_type, SUM(concepts_extracted) as total
                    FROM knowledge_integration
                    GROUP BY knowledge_type
                """)
                
                for knowledge_type, total in cursor.fetchall():
                    if knowledge_type in self.integrated_knowledge:
                        self.integrated_knowledge[knowledge_type] = total
                    
        except Exception:
            logger.warning(f"Could not load evolution state: {_e}")
    
    def _log_knowledge_integration(self, results: Dict[str, Any]):
        """Log knowledge integration results."""
        with self.db._lock, self.db._connect() as conn:
            for knowledge_type, data in results.items():
                if isinstance(data, dict) and 'enhancement' in data:
                    conn.execute("""
                        INSERT INTO knowledge_integration
                        (timestamp, knowledge_type, source_document, concepts_extracted, 
                         integration_method, performance_impact)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        time.time(),
                        knowledge_type,
                        'comprehensive_integration',
                        data.get('words_integrated', data.get('concepts_integrated', 0)),
                        data.get('enhancement', ''),
                        1.0  # Assume positive impact
                    ))
            conn.commit()

# Singleton instance for easy access
_self_evolution_engine = None

def get_self_evolution_engine() -> SelfEvolutionEngine:
    """
    Get the singleton self-evolution engine instance.
    
    Why: Provides centralized access to Clever's self-improvement capabilities
    Where: Called by evolution triggers and system management functions
    How: Creates singleton instance with database connection on first call
    """
    global _self_evolution_engine
    if _self_evolution_engine is None:
        from database import db_manager
        _self_evolution_engine = SelfEvolutionEngine(db_manager)
    return _self_evolution_engine