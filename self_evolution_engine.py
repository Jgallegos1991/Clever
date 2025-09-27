#!/usr/bin/env python3
"""
Self-Evolution Engine for Clever's Cognitive Enhancement

Why: Enables Clever to learn from documents and self-modify her code for unlimited
     cognitive growth and deeper integration with Jay's thinking patterns.
     This transforms her from a static AI into a truly evolving digital brain extension.

Where: Integrates with NotebookLM engine, evolution engine, and persona system to
       enable continuous self-improvement and code evolution capabilities.

How: Analyzes document patterns, learning effectiveness, and performance metrics
     to identify opportunities for self-modification and cognitive enhancement.
     Uses safe code generation and testing to evolve her own capabilities.

File Usage:
    - Primary callers: evolution_engine.py for learning triggers, notebooklm_engine.py for document insights
    - Key dependencies: notebooklm_engine.py for document analysis, database.py for learning persistence
    - Data sources: Document analysis patterns, user interaction effectiveness, performance metrics
    - Data destinations: Code modifications, enhanced algorithms, evolved capabilities
    - Configuration: config.py for evolution parameters and safety constraints
    - Database interactions: Evolution tracking, code change history, performance metrics
    - API endpoints: /api/trigger_evolution, /api/evolution_status, /api/code_insights
    - Frontend connections: Evolution monitoring UI, code change visualization
    - Background processes: Continuous learning analysis, safe code evolution

Connects to:
    - notebooklm_engine.py: Document pattern analysis for cognitive enhancement insights
    - evolution_engine.py: Base learning system extended with self-modification capabilities
    - persona.py: Personality evolution and response pattern optimization
    - database.py: Evolution history tracking and code change persistence
    - academic_knowledge_engine.py: Learning from academic concepts to enhance intelligence
    - config.py: Evolution safety parameters and cognitive enhancement limits
    - introspection.py: Runtime analysis for self-improvement opportunities

Performance Notes:
    - Memory usage: Code analysis and generation requires significant memory allocation
    - CPU impact: Self-modification analysis is computationally intensive, runs in background
    - I/O operations: File reading/writing for code modifications with backup systems
    - Scaling limits: Evolution bounded by safety constraints and testing capabilities

Critical Dependencies:
    - Required packages: ast, inspect, textwrap for code analysis and generation
    - Optional packages: autopep8, black for code formatting and optimization
    - System requirements: Write access to source files with comprehensive backup system
    - Database schema: Evolution history, code changes, performance tracking tables
"""

import ast
import inspect
import logging
import tempfile
import textwrap
from dataclasses import dataclass

# Clever core modules
from database import DatabaseManager
import config

# Evolution and learning components
try:
    from evolution_engine import get_evolution_engine
    _EVOLUTION_AVAILABLE = True
except ImportError:
    _EVOLUTION_AVAILABLE = False

try:
    from notebooklm_engine import get_notebooklm_engine
    _NOTEBOOKLM_AVAILABLE = True
except ImportError:
    _NOTEBOOKLM_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class CodeEvolution:
    """Represents a potential or completed code evolution."""
    target_file: str
    evolution_type: str  # 'optimization', 'enhancement', 'integration', 'algorithm_improvement'
    description: str
    confidence: float
    safety_score: float
    estimated_improvement: float
    code_changes: str
    test_results: Optional[Dict[str, Any]] = None
    applied: bool = False
    rollback_data: Optional[str] = None


@dataclass
class LearningInsight:
    """Insights derived from document analysis for self-evolution."""
    insight_type: str  # 'algorithm', 'pattern', 'optimization', 'integration'
    source_documents: List[str]
    description: str
    applicable_modules: List[str]
    implementation_complexity: str  # 'low', 'medium', 'high'
    potential_impact: float
    supporting_evidence: List[str]


class SelfEvolutionEngine:
    """
    Enables Clever to learn from documents and evolve her own code for enhanced capabilities.
    
    This engine analyzes document patterns, learning effectiveness, and performance data
    to identify opportunities for self-improvement and safe code evolution.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the self-evolution engine.
        
        Why: Sets up cognitive enhancement capabilities with safety constraints
        Where: Called during system initialization for continuous improvement
        How: Initializes analysis systems, safety protocols, and evolution tracking
        """
        self.db = db_manager
        self.clever_root = Path(__file__).parent
        self.backup_dir = self.clever_root / 'evolution_backups'
        self.backup_dir.mkdir(exist_ok=True)
        
        # Evolution safety parameters
        self.max_evolutions_per_day = 3
        self.min_safety_score = 0.8
        self.min_confidence = 0.7
        
        # Initialize evolution tracking
        self._init_evolution_schema()
        
        # Track learning patterns
        self.learning_patterns: Dict[str, List[Dict[str, Any]]] = {}
        self.performance_metrics: Dict[str, float] = {}
        
        logger.info("Self-Evolution Engine initialized with safety protocols active")
    
    def _init_evolution_schema(self):
        """Initialize database schema for evolution tracking."""
        with self.db._lock, self.db._connect() as conn:
            # Code evolution history
            conn.execute("""
                CREATE TABLE IF NOT EXISTS code_evolutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_file TEXT NOT NULL,
                    evolution_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    safety_score REAL NOT NULL,
                    estimated_improvement REAL NOT NULL,
                    code_changes TEXT NOT NULL,
                    test_results TEXT,
                    applied BOOLEAN DEFAULT FALSE,
                    rollback_data TEXT,
                    created_ts REAL NOT NULL,
                    applied_ts REAL
                )
            """)
            
            # Learning insights from documents
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    insight_type TEXT NOT NULL,
                    source_documents TEXT NOT NULL,  -- JSON array
                    description TEXT NOT NULL,
                    applicable_modules TEXT NOT NULL,  -- JSON array
                    implementation_complexity TEXT NOT NULL,
                    potential_impact REAL NOT NULL,
                    supporting_evidence TEXT NOT NULL,  -- JSON array
                    processed BOOLEAN DEFAULT FALSE,
                    created_ts REAL NOT NULL
                )
            """)
            
            # Performance tracking for evolution effectiveness
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evolution_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    before_value REAL NOT NULL,
                    after_value REAL NOT NULL,
                    improvement REAL NOT NULL,
                    evolution_id INTEGER,
                    measured_ts REAL NOT NULL,
                    FOREIGN KEY (evolution_id) REFERENCES code_evolutions (id)
                )
            """)
            
            conn.commit()
    
    def analyze_document_insights(self) -> List[LearningInsight]:
        """
        Analyze document collection to extract insights for self-evolution.
        
        Why: Documents contain algorithms, patterns, and techniques that could enhance Clever's capabilities
        Where: Called periodically or after significant document additions
        How: Uses NotebookLM engine to analyze document patterns and extract applicable insights
        
        Returns:
            List of learning insights that could drive code evolution
        """
        insights = []
        
        if not _NOTEBOOKLM_AVAILABLE:
            logger.warning("NotebookLM engine not available for insight analysis")
            return insights
        
        try:
            notebooklm = get_notebooklm_engine()
            
            # Get collection overview for analysis patterns
            overview = notebooklm.generate_collection_overview()
            
            # Analyze key themes for algorithmic insights
            key_themes = overview.get('key_themes', [])
            
            # Look for algorithmic and technical insights
            algorithmic_terms = {
                'algorithm', 'optimization', 'performance', 'efficiency', 'complexity',
                'data structure', 'neural network', 'machine learning', 'ai', 'cognitive',
                'enhancement', 'improvement', 'methodology', 'framework', 'architecture'
            }
            
            relevant_themes = [theme for theme in key_themes 
                             if any(term in theme.lower() for term in algorithmic_terms)]
            
            if relevant_themes:
                # Generate specific insights for each relevant theme
                for theme in relevant_themes[:5]:  # Limit to top 5 themes
                    insight = self._generate_theme_insight(theme, notebooklm)
                    if insight:
                        insights.append(insight)
            
            # Analyze cross-document connections for integration opportunities
            connections = notebooklm.find_cross_document_connections()
            
            for connection in connections[:3]:  # Top 3 connections
                integration_insight = self._analyze_connection_for_integration(connection, notebooklm)
                if integration_insight:
                    insights.append(integration_insight)
            
            # Store insights in database
            for insight in insights:
                self._store_learning_insight(insight)
            
            logger.info(f"Generated {len(insights)} learning insights from document analysis")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing document insights: {e}")
            return insights
    
    def _generate_theme_insight(self, theme: str, notebooklm) -> Optional[LearningInsight]:
        """Generate a learning insight from a document theme."""
        try:
            # Query documents for this specific theme
            query_response = notebooklm.query_documents(
                f"What algorithms, methods, or techniques are mentioned regarding {theme}?",
                max_sources=3
            )
            
            if query_response.confidence < 0.4 or not query_response.citations:
                return None
            
            # Analyze applicable modules based on theme
            applicable_modules = self._identify_applicable_modules(theme, query_response.text)
            
            if not applicable_modules:
                return None
            
            # Extract evidence from citations
            supporting_evidence = [f"{c.filename}: {c.excerpt[:100]}..." for c in query_response.citations]
            
            # Determine implementation complexity
            complexity = self._assess_implementation_complexity(query_response.text)
            
            # Calculate potential impact
            impact = self._calculate_potential_impact(theme, applicable_modules, query_response.confidence)
            
            return LearningInsight(
                insight_type='algorithm' if 'algorithm' in theme.lower() else 'pattern',
                source_documents=[c.filename for c in query_response.citations],
                description=f"Enhancement opportunity for {theme}: {query_response.text[:200]}...",
                applicable_modules=applicable_modules,
                implementation_complexity=complexity,
                potential_impact=impact,
                supporting_evidence=supporting_evidence
            )
            
        except Exception as e:
            logger.warning(f"Error generating theme insight for '{theme}': {e}")
            return None
    
    def _analyze_connection_for_integration(self, connection, notebooklm) -> Optional[LearningInsight]:
        """Analyze document connections for integration opportunities."""
        shared_concepts = connection.shared_concepts
        
        # Look for integration opportunities in shared concepts
        integration_terms = {'integration', 'connection', 'combination', 'synthesis', 'merge'}
        
        if not any(term in ' '.join(shared_concepts).lower() for term in integration_terms):
            return None
        
        # Find modules that could benefit from this integration
        applicable_modules = ['notebooklm_engine.py', 'persona.py', 'evolution_engine.py']
        
        return LearningInsight(
            insight_type='integration',
            source_documents=[f"connection_{connection.source_id_1}_{connection.source_id_2}"],
            description=f"Integration opportunity: {connection.explanation}",
            applicable_modules=applicable_modules,
            implementation_complexity='medium',
            potential_impact=connection.strength,
            supporting_evidence=[f"Shared concepts: {', '.join(shared_concepts)}"]
        )
    
    def _identify_applicable_modules(self, theme: str, content: str) -> List[str]:
        """Identify which Clever modules could benefit from this insight."""
        modules = []
        theme_lower = theme.lower()
        content_lower = content.lower()
        
        # Map themes to relevant modules
        module_mapping = {
            'nlp': ['nlp_processor.py', 'persona.py'],
            'memory': ['memory_engine.py', 'evolution_engine.py'],
            'analysis': ['notebooklm_engine.py', 'academic_knowledge_engine.py'],
            'optimization': ['persona.py', 'evolution_engine.py'],
            'algorithm': ['notebooklm_engine.py', 'nlp_processor.py'],
            'cognitive': ['persona.py', 'evolution_engine.py', 'notebooklm_engine.py'],
            'learning': ['evolution_engine.py', 'memory_engine.py'],
            'intelligence': ['academic_knowledge_engine.py', 'persona.py']
        }
        
        for key, module_list in module_mapping.items():
            if key in theme_lower or key in content_lower:
                modules.extend(module_list)
        
        return list(set(modules))  # Remove duplicates
    
    def _assess_implementation_complexity(self, content: str) -> str:
        """Assess implementation complexity based on content analysis."""
        content_lower = content.lower()
        
        high_complexity_indicators = {
            'neural network', 'deep learning', 'complex algorithm', 'optimization',
            'mathematical', 'statistical', 'advanced', 'sophisticated'
        }
        
        medium_complexity_indicators = {
            'method', 'technique', 'approach', 'framework', 'system'
        }
        
        if any(indicator in content_lower for indicator in high_complexity_indicators):
            return 'high'
        elif any(indicator in content_lower for indicator in medium_complexity_indicators):
            return 'medium'
        else:
            return 'low'
    
    def _calculate_potential_impact(self, theme: str, modules: List[str], confidence: float) -> float:
        """Calculate potential impact score for an insight."""
        base_impact = confidence
        
        # Boost impact based on number of applicable modules
        module_boost = min(0.3, len(modules) * 0.1)
        
        # Theme-based impact modifiers
        high_impact_themes = {'optimization', 'intelligence', 'cognitive', 'learning'}
        theme_boost = 0.2 if any(term in theme.lower() for term in high_impact_themes) else 0.0
        
        return min(1.0, base_impact + module_boost + theme_boost)
    
    def _store_learning_insight(self, insight: LearningInsight):
        """Store a learning insight in the database."""
        with self.db._lock, self.db._connect() as conn:
            conn.execute("""
                INSERT INTO learning_insights 
                (insight_type, source_documents, description, applicable_modules,
                 implementation_complexity, potential_impact, supporting_evidence, created_ts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                insight.insight_type,
                json.dumps(insight.source_documents),
                insight.description,
                json.dumps(insight.applicable_modules),
                insight.implementation_complexity,
                insight.potential_impact,
                json.dumps(insight.supporting_evidence),
                time.time()
            ))
            conn.commit()
    
    def generate_code_evolutions(self, insights: Optional[List[LearningInsight]] = None) -> List[CodeEvolution]:
        """
        Generate potential code evolutions based on learning insights.
        
        Why: Translates learning insights into concrete code modifications for enhancement
        Where: Called after document analysis or performance evaluation
        How: Analyzes current code and generates safe, tested modifications
        
        Args:
            insights: Optional list of insights to base evolutions on
            
        Returns:
            List of potential code evolutions with safety assessments
        """
        evolutions = []
        
        if insights is None:
            insights = self._get_unprocessed_insights()
        
        for insight in insights:
            try:
                evolution = self._create_evolution_from_insight(insight)
                if evolution and self._assess_evolution_safety(evolution):
                    evolutions.append(evolution)
            except Exception as e:
                logger.warning(f"Error creating evolution from insight: {e}")
        
        # Also check for performance-based evolutions
        performance_evolutions = self._generate_performance_evolutions()
        evolutions.extend(performance_evolutions)
        
        # Store evolution proposals
        for evolution in evolutions:
            self._store_code_evolution(evolution)
        
        logger.info(f"Generated {len(evolutions)} potential code evolutions")
        return evolutions
    
    def _get_unprocessed_insights(self) -> List[LearningInsight]:
        """Retrieve unprocessed learning insights from database."""
        insights = []
        
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute("""
                SELECT insight_type, source_documents, description, applicable_modules,
                       implementation_complexity, potential_impact, supporting_evidence
                FROM learning_insights 
                WHERE processed = FALSE
                ORDER BY potential_impact DESC
                LIMIT 5
            """)
            
            for row in cursor.fetchall():
                insight = LearningInsight(
                    insight_type=row[0],
                    source_documents=json.loads(row[1]),
                    description=row[2],
                    applicable_modules=json.loads(row[3]),
                    implementation_complexity=row[4],
                    potential_impact=row[5],
                    supporting_evidence=json.loads(row[6])
                )
                insights.append(insight)
        
        return insights
    
    def _create_evolution_from_insight(self, insight: LearningInsight) -> Optional[CodeEvolution]:
        """Create a code evolution from a learning insight."""
        if not insight.applicable_modules or insight.potential_impact < 0.3:
            return None
        
        # Choose primary target module
        target_file = insight.applicable_modules[0]
        
        # Generate evolution based on insight type
        if insight.insight_type == 'optimization':
            return self._generate_optimization_evolution(target_file, insight)
        elif insight.insight_type == 'algorithm':
            return self._generate_algorithm_evolution(target_file, insight)
        elif insight.insight_type == 'integration':
            return self._generate_integration_evolution(target_file, insight)
        else:
            return self._generate_enhancement_evolution(target_file, insight)
    
    def _generate_optimization_evolution(self, target_file: str, insight: LearningInsight) -> CodeEvolution:
        """Generate an optimization-based code evolution."""
        # Example optimization for NotebookLM engine
        if 'notebooklm_engine.py' in target_file:
            code_changes = '''
    # Performance optimization: Add caching for document embeddings
    def _get_cached_embedding(self, text: str, cache_key: str):
        """Cache document embeddings for faster retrieval."""
        if cache_key not in self._embeddings_cache:
            if self._embeddings_model:
                embedding = self._embeddings_model.encode([text])
                self._embeddings_cache[cache_key] = embedding
            else:
                self._embeddings_cache[cache_key] = None
        return self._embeddings_cache[cache_key]
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between texts using cached embeddings."""
        try:
            emb1 = self._get_cached_embedding(text1, hashlib.md5(text1.encode()).hexdigest())
            emb2 = self._get_cached_embedding(text2, hashlib.md5(text2.encode()).hexdigest())
            
            if emb1 is not None and emb2 is not None and _SKLEARN_AVAILABLE:
                return cosine_similarity(emb1, emb2)[0][0]
            else:
                # Fallback to simple word overlap
                words1 = set(text1.lower().split())
                words2 = set(text2.lower().split())
                overlap = len(words1 & words2)
                total = len(words1 | words2)
                return overlap / total if total > 0 else 0.0
        except Exception:
            return 0.0
            '''
        else:
            code_changes = f"# Optimization placeholder for {target_file}"
        
        return CodeEvolution(
            target_file=target_file,
            evolution_type='optimization',
            description=f"Performance optimization based on insight: {insight.description[:100]}...",
            confidence=insight.potential_impact,
            safety_score=0.9,  # Optimizations are generally safe
            estimated_improvement=0.2,
            code_changes=code_changes
        )
    
    def _generate_algorithm_evolution(self, target_file: str, insight: LearningInsight) -> CodeEvolution:
        """Generate an algorithm improvement evolution."""
        # Placeholder for algorithm enhancement
        code_changes = """
    # Algorithm enhancement based on document insight
    def _enhanced_analysis_method(self, input_data):
        '''Enhanced analysis method derived from document insights.'''
        # Implementation based on: {insight.description[:100]}...
        # Sources: {', '.join(insight.source_documents[:2])}
        
        # Enhanced algorithm implementation here
        return self._existing_analysis_method(input_data)
        """
        
        return CodeEvolution(
            target_file=target_file,
            evolution_type='enhancement',
            description=f"Algorithm enhancement: {insight.description[:100]}...",
            confidence=insight.potential_impact * 0.8,  # Slightly lower confidence for algorithm changes
            safety_score=0.7,
            estimated_improvement=insight.potential_impact,
            code_changes=code_changes
        )
    
    def _generate_integration_evolution(self, target_file: str, insight: LearningInsight) -> CodeEvolution:
        """Generate an integration-based evolution."""
        code_changes = """
    # Integration enhancement based on cross-document analysis
    def _enhanced_integration_method(self):
        '''Enhanced integration derived from document connections.'''
        # Integration insight: {insight.description[:100]}...
        
        try:
            # Enhanced cross-module integration
            if hasattr(self, '_notebooklm_engine'):
                connections = self._notebooklm_engine.find_cross_document_connections()
                # Use connections for enhanced integration
                return connections
        except Exception as e:
            logger.warning(f"Integration enhancement failed: {{e}}")
            return []
        """
        
        return CodeEvolution(
            target_file=target_file,
            evolution_type='integration',
            description=f"Integration enhancement: {insight.description[:100]}...",
            confidence=insight.potential_impact,
            safety_score=0.8,
            estimated_improvement=0.15,
            code_changes=code_changes
        )
    
    def _generate_enhancement_evolution(self, target_file: str, insight: LearningInsight) -> CodeEvolution:
        """Generate a general enhancement evolution."""
        code_changes = """
    # General enhancement based on document analysis
    def _enhanced_capability(self, context):
        '''Enhanced capability derived from document insights.'''
        # Enhancement based on: {insight.description[:100]}...
        
        # Implementation placeholder - specific enhancement would go here
        return context
        """
        
        return CodeEvolution(
            target_file=target_file,
            evolution_type='enhancement',
            description=f"General enhancement: {insight.description[:100]}...",
            confidence=insight.potential_impact * 0.7,
            safety_score=0.8,
            estimated_improvement=0.1,
            code_changes=code_changes
        )
    
    def _generate_performance_evolutions(self) -> List[CodeEvolution]:
        """Generate evolutions based on performance analysis."""
        evolutions = []
        
        # Analyze current performance bottlenecks
        # This would integrate with performance monitoring to identify slow methods
        
        # Example: If NotebookLM queries are slow, suggest caching
        performance_evolution = CodeEvolution(
            target_file='notebooklm_engine.py',
            evolution_type='optimization',
            description='Add query result caching for improved performance',
            confidence=0.8,
            safety_score=0.9,
            estimated_improvement=0.3,
            code_changes='''
    def _get_cached_query_result(self, query: str, max_sources: int) -> Optional[SourceGroundedResponse]:
        """Cache query results for improved performance."""
        cache_key = hashlib.md5(f"{query}_{max_sources}".encode()).hexdigest()
        
        if hasattr(self, '_query_cache') and cache_key in self._query_cache:
            cached_result, timestamp = self._query_cache[cache_key]
            # Cache results for 10 minutes
            if time.time() - timestamp < 600:
                return cached_result
        
        return None
    
    def _cache_query_result(self, query: str, max_sources: int, result: SourceGroundedResponse):
        """Cache a query result."""
        if not hasattr(self, '_query_cache'):
            self._query_cache = {}
        
        cache_key = hashlib.md5(f"{query}_{max_sources}".encode()).hexdigest()
        self._query_cache[cache_key] = (result, time.time())
        
        # Limit cache size
        if len(self._query_cache) > 100:
            oldest_key = min(self._query_cache.keys(), key=lambda k: self._query_cache[k][1])
            del self._query_cache[oldest_key]
            '''
        )
        
        evolutions.append(performance_evolution)
        return evolutions
    
    def _assess_evolution_safety(self, evolution: CodeEvolution) -> bool:
        """Assess the safety of a proposed code evolution."""
        # Basic safety checks
        if evolution.confidence < self.min_confidence:
            return False
            
        if evolution.safety_score < self.min_safety_score:
            return False
        
        # Check if code changes contain dangerous operations
        dangerous_patterns = ['rm ', 'del ', 'os.system', 'subprocess.call', 'eval(', 'exec(']
        if any(pattern in evolution.code_changes for pattern in dangerous_patterns):
            evolution.safety_score *= 0.5
            return evolution.safety_score >= self.min_safety_score
        
        return True
    
    def _store_code_evolution(self, evolution: CodeEvolution):
        """Store a code evolution proposal in the database."""
        with self.db._lock, self.db._connect() as conn:
            conn.execute("""
                INSERT INTO code_evolutions 
                (target_file, evolution_type, description, confidence, safety_score,
                 estimated_improvement, code_changes, created_ts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                evolution.target_file,
                evolution.evolution_type,
                evolution.description,
                evolution.confidence,
                evolution.safety_score,
                evolution.estimated_improvement,
                evolution.code_changes,
                time.time()
            ))
            conn.commit()
    
    def apply_evolution(self, evolution_id: int, dry_run: bool = True) -> Dict[str, Any]:
        """
        Apply a code evolution with safety checks and testing.
        
        Why: Safely implements approved code evolutions with rollback capability
        Where: Called when user approves an evolution or system auto-applies safe changes
        How: Creates backups, applies changes, runs tests, and provides rollback if needed
        
        Args:
            evolution_id: Database ID of evolution to apply
            dry_run: If True, only simulate the application
            
        Returns:
            Result of evolution application with test results and metrics
        """
        # Retrieve evolution from database
        with self.db._lock, self.db._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM code_evolutions WHERE id = ?",
                (evolution_id,)
            )
            row = cursor.fetchone()
            
        if not row:
            return {'success': False, 'error': 'Evolution not found'}
        
        evolution = CodeEvolution(
            target_file=row[1],
            evolution_type=row[2],
            description=row[3],
            confidence=row[4],
            safety_score=row[5],
            estimated_improvement=row[6],
            code_changes=row[7],
            test_results=json.loads(row[8]) if row[8] else None,
            applied=bool(row[9]),
            rollback_data=row[10]
        )
        
        if evolution.applied:
            return {'success': False, 'error': 'Evolution already applied'}
        
        try:
            if dry_run:
                return self._simulate_evolution_application(evolution)
            else:
                return self._actually_apply_evolution(evolution, evolution_id)
                
        except Exception as e:
            logger.error(f"Error applying evolution {evolution_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _simulate_evolution_application(self, evolution: CodeEvolution) -> Dict[str, Any]:
        """Simulate applying an evolution without making actual changes."""
        target_path = self.clever_root / evolution.target_file
        
        if not target_path.exists():
            return {'success': False, 'error': f'Target file {evolution.target_file} not found'}
        
        # Read current file
        current_content = target_path.read_text()
        
        # Simulate adding the evolution code
        # This is a simplified simulation - would need more sophisticated merging
        simulated_content = current_content + "\n\n" + evolution.code_changes
        
        # Basic syntax check
        try:
            ast.parse(simulated_content)
            syntax_valid = True
        except SyntaxError as e:
            syntax_valid = False
        
        return {
            'success': True,
            'dry_run': True,
            'syntax_valid': syntax_valid,
            'estimated_lines_added': len(evolution.code_changes.split('\n')),
            'target_file': evolution.target_file,
            'evolution_type': evolution.evolution_type
        }
    
    def _actually_apply_evolution(self, evolution: CodeEvolution, evolution_id: int) -> Dict[str, Any]:
        """Actually apply the evolution with full safety protocols."""
        target_path = self.clever_root / evolution.target_file
        
        # Create backup
        backup_path = self.backup_dir / f"{evolution.target_file}_{int(time.time())}.backup"
        shutil.copy2(target_path, backup_path)
        
        try:
            # Read current content
            current_content = target_path.read_text()
            
            # Apply evolution (simplified - would need sophisticated code merging)
            modified_content = self._merge_evolution_code(current_content, evolution.code_changes)
            
            # Write modified content
            target_path.write_text(modified_content)
            
            # Run tests to validate the change
            test_results = self._run_evolution_tests(evolution)
            
            if test_results['success']:
                # Mark as applied in database
                with self.db._lock, self.db._connect() as conn:
                    conn.execute("""
                        UPDATE code_evolutions 
                        SET applied = TRUE, applied_ts = ?, test_results = ?, rollback_data = ?
                        WHERE id = ?
                    """, (time.time(), json.dumps(test_results), str(backup_path), evolution_id))
                    conn.commit()
                
                logger.info(f"Successfully applied evolution {evolution_id} to {evolution.target_file}")
                return {
                    'success': True,
                    'evolution_id': evolution_id,
                    'target_file': evolution.target_file,
                    'backup_path': str(backup_path),
                    'test_results': test_results
                }
            else:
                # Rollback on test failure
                shutil.copy2(backup_path, target_path)
                logger.warning(f"Evolution {evolution_id} failed tests, rolled back")
                return {
                    'success': False,
                    'error': 'Evolution failed testing',
                    'test_results': test_results
                }
                
        except Exception as e:
            # Rollback on any error
            shutil.copy2(backup_path, target_path)
            logger.error(f"Evolution {evolution_id} application failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _merge_evolution_code(self, current_content: str, evolution_code: str) -> str:
        """Merge evolution code into existing file content."""
        # This is a simplified approach - in reality, would need sophisticated AST manipulation
        
        # For now, just append the evolution code with proper formatting
        if not current_content.endswith('\n'):
            current_content += '\n'
        
        return current_content + "\n\n# === EVOLVED CODE ===\n" + evolution_code + "\n"
    
    def _run_evolution_tests(self, evolution: CodeEvolution) -> Dict[str, Any]:
        """Run tests to validate an applied evolution."""
        try:
            # Basic syntax check
            target_path = self.clever_root / evolution.target_file
            content = target_path.read_text()
            ast.parse(content)
            
            # Try to import the module
            if evolution.target_file.endswith('.py'):
                module_name = evolution.target_file[:-3].replace('/', '.')
                try:
                    # This is simplified - would need proper module reloading
                    import importlib
                    module = importlib.import_module(module_name)
                    importlib.reload(module)
                    import_success = True
                except Exception as import_error:
                    import_success = False
            else:
                import_success = True
            
            return {
                'success': import_success,
                'syntax_valid': True,
                'import_success': import_success,
                'test_timestamp': time.time()
            }
            
        except SyntaxError:
            return {
                'success': False,
                'syntax_valid': False,
                'error': 'Syntax error in evolved code'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get comprehensive status of evolution system."""
        with self.db._lock, self.db._connect() as conn:
            # Count evolutions by status
            cursor = conn.execute("""
                SELECT evolution_type, applied, COUNT(*) 
                FROM code_evolutions 
                GROUP BY evolution_type, applied
            """)
            evolution_counts = cursor.fetchall()
            
            # Get recent evolutions
            cursor = conn.execute("""
                SELECT target_file, evolution_type, description, confidence, applied, created_ts
                FROM code_evolutions 
                ORDER BY created_ts DESC 
                LIMIT 10
            """)
            recent_evolutions = cursor.fetchall()
            
            # Count unprocessed insights
            cursor = conn.execute("""
                SELECT COUNT(*) FROM learning_insights WHERE processed = FALSE
            """)
            unprocessed_insights = cursor.fetchone()[0]
        
        return {
            'evolution_counts': {
                'total': sum(count for _, _, count in evolution_counts),
                'applied': sum(count for _, applied, count in evolution_counts if applied),
                'pending': sum(count for _, applied, count in evolution_counts if not applied)
            },
            'recent_evolutions': [
                {
                    'target_file': row[0],
                    'evolution_type': row[1],
                    'description': row[2][:100] + '...' if len(row[2]) > 100 else row[2],
                    'confidence': row[3],
                    'applied': bool(row[4]),
                    'created_ts': row[5]
                } for row in recent_evolutions
            ],
            'unprocessed_insights': unprocessed_insights,
            'evolution_parameters': {
                'max_evolutions_per_day': self.max_evolutions_per_day,
                'min_safety_score': self.min_safety_score,
                'min_confidence': self.min_confidence
            }
        }


# Singleton instance for global access
_self_evolution_engine = None

def get_self_evolution_engine() -> SelfEvolutionEngine:
    """
    Get the singleton self-evolution engine instance.
    
    Why: Provides centralized access to Clever's self-modification capabilities
    Where: Called by evolution systems and monitoring interfaces
    How: Creates singleton with database connection on first access
    """
    global _self_evolution_engine
    if _self_evolution_engine is None:
        from database import db_manager
        _self_evolution_engine = SelfEvolutionEngine(db_manager)
    return _self_evolution_engine