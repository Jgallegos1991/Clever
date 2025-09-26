#!/usr/bin/env python3
"""
memory_optimized_code_intelligence.py - Memory-Efficient Code Intelligence for Clever

Why: Provides code analysis and modification capabilities optimized for low-memory environments
     like Chromebooks while maintaining expert-level functionality for Clever's cognitive sovereignty.

Where: Replaces heavyweight code intelligence with memory-conscious patterns for constrained environments.
       Integrates with cognitive_sovereignty.py without overwhelming system resources.

How: Uses streaming analysis, minimal caching, and lightweight patterns instead of memory-intensive
     AST operations. Prioritizes essential functionality over comprehensive analysis.

Memory Optimization Notes:
    - Streaming file processing (no full content in memory)
    - Minimal caching with LRU eviction
    - Lightweight regex patterns over heavy AST parsing
    - Batch processing with memory cleanup
    - Generator-based analysis for large codebases

Performance Constraints:
    - Target: <50MB memory footprint
    - Processing: <100MB temporary memory usage
    - Cache limit: 20 analysis results maximum
    - File limit: Process max 5 files simultaneously
"""

import re
import time
import gc
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

# Minimal language patterns (memory efficient)
LANGUAGE_ESSENTIALS = {
    'python': {
        'ext': ['.py'],
        'func_pattern': r'^\s*def\s+(\w+)\s*\(',
        'class_pattern': r'^\s*class\s+(\w+)',
        'import_pattern': r'^\s*(?:from\s+\w+\s+)?import\s+',
        'complexity_indicators': ['if', 'for', 'while', 'try', 'except', 'elif', 'and', 'or']
    },
    'javascript': {
        'ext': ['.js', '.jsx'],
        'func_pattern': r'(?:function\s+(\w+)|const\s+(\w+)\s*=)',
        'class_pattern': r'^\s*class\s+(\w+)',
        'import_pattern': r'^\s*(?:import|const.*=.*require)',
        'complexity_indicators': ['if', 'for', 'while', 'try', 'catch', '&&', '||']
    },
    'typescript': {
        'ext': ['.ts', '.tsx'],
        'func_pattern': r'(?:function\s+(\w+)|const\s+(\w+)\s*=)',
        'class_pattern': r'^\s*(?:class|interface)\s+(\w+)',
        'import_pattern': r'^\s*(?:import|const.*=.*require)',
        'complexity_indicators': ['if', 'for', 'while', 'try', 'catch', '&&', '||']
    }
}

class CodeQuality(Enum):
    """Simplified quality levels."""
    LOW = 0.3
    MEDIUM = 0.6  
    HIGH = 0.8
    EXCELLENT = 0.95

@dataclass
class LightweightAnalysis:
    """Memory-efficient code analysis results."""
    file_path: str
    language: str
    lines_of_code: int
    function_count: int
    class_count: int  
    import_count: int
    estimated_complexity: int
    quality_score: float
    has_documentation: bool
    analysis_time: float

@dataclass
class SafeModification:
    """Memory-efficient modification specification."""
    file_path: str
    operation: str  # 'add', 'modify', 'optimize'
    target_line: int
    original_snippet: str
    new_snippet: str
    safety_score: float
    timestamp: float

class MemoryOptimizedCodeIntelligence:
    """
    Memory-efficient code intelligence engine for Clever.
    
    Designed for Chromebook environments with limited RAM while maintaining
    essential code analysis and self-modification capabilities.
    """
    
    def __init__(self, max_cache_size: int = 20, max_memory_mb: int = 50):
        """
        Initialize memory-optimized code intelligence.
        
        Why: Sets up lightweight code analysis with strict memory limits
        Where: Called during Clever initialization with memory awareness
        How: Uses LRU cache and streaming processing to minimize memory usage
        
        Args:
            max_cache_size: Maximum analysis results to cache
            max_memory_mb: Memory limit for processing (not enforced, guideline)
        """
        self.max_cache_size = max_cache_size
        self.max_memory_mb = max_memory_mb
        self.analysis_cache = OrderedDict()  # LRU cache
        self.modification_count = 0
        self.total_analyzed_files = 0
        
        # System awareness
        self.system_constraints = self._detect_system_constraints()
        
    def _detect_system_constraints(self) -> Dict[str, Any]:
        """
        Detect system memory and performance constraints.
        
        Why: Enables Clever to understand her hardware environment
        Where: Called during initialization for system awareness
        How: Analyzes available memory and adjusts processing accordingly
        
        Returns:
            Dict with system constraint information
        """
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            # Determine processing strategy based on available memory
            available_mb = memory.available / (1024 * 1024)
            
            if available_mb < 200:
                strategy = 'minimal'
                batch_size = 1
                cache_limit = 5
            elif available_mb < 500:
                strategy = 'conservative'  
                batch_size = 2
                cache_limit = 10
            else:
                strategy = 'standard'
                batch_size = 5
                cache_limit = 20
                
            return {
                'total_memory_mb': memory.total / (1024 * 1024),
                'available_memory_mb': available_mb,
                'memory_percent_used': memory.percent,
                'processing_strategy': strategy,
                'batch_size': batch_size,
                'cache_limit': cache_limit,
                'low_memory_mode': available_mb < 300
            }
            
        except ImportError:
            # Fallback if psutil not available
            return {
                'total_memory_mb': 2048,  # Assume typical Chromebook
                'available_memory_mb': 200,  # Assume low memory
                'memory_percent_used': 85,
                'processing_strategy': 'conservative',
                'batch_size': 2,
                'cache_limit': 10,
                'low_memory_mode': True
            }
    
    def analyze_file_lightweight(self, file_path: str) -> Optional[LightweightAnalysis]:
        """
        Perform lightweight analysis of a single file.
        
        Why: Provides code understanding with minimal memory footprint
        Where: Called for individual file analysis without overwhelming system
        How: Uses streaming line processing and regex patterns instead of AST
        
        Args:
            file_path: Path to code file to analyze
            
        Returns:
            LightweightAnalysis or None if analysis fails
        """
        try:
            path = Path(file_path)
            
            # Check cache first
            cache_key = f"{file_path}:{path.stat().st_mtime}"
            if cache_key in self.analysis_cache:
                # Move to end (LRU)
                self.analysis_cache.move_to_end(cache_key)
                return self.analysis_cache[cache_key]
            
            # Detect language
            language = self._detect_language_fast(path)
            if language not in LANGUAGE_ESSENTIALS:
                return None
            
            patterns = LANGUAGE_ESSENTIALS[language]
            
            # Streaming analysis (memory efficient)
            analysis = self._analyze_file_stream(path, language, patterns)
            
            # Cache with LRU eviction
            self._cache_analysis(cache_key, analysis)
            
            self.total_analyzed_files += 1
            return analysis
            
        except Exception as e:
            print(f"Lightweight analysis failed for {file_path}: {e}")
            return None
    
    def _analyze_file_stream(self, path: Path, language: str, patterns: Dict) -> LightweightAnalysis:
        """
        Analyze file using streaming line processing.
        
        Why: Minimizes memory usage by processing one line at a time
        Where: Called by analyze_file_lightweight for memory-efficient analysis
        How: Processes file line-by-line without loading entire content into memory
        
        Args:
            path: Path object for file
            language: Detected programming language
            patterns: Language-specific regex patterns
            
        Returns:
            LightweightAnalysis with basic code metrics
        """
        start_time = time.time()
        
        loc = 0
        function_count = 0
        class_count = 0
        import_count = 0
        complexity_score = 0
        has_doc_comments = False
        
        try:
            with path.open('r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines
                    if not line:
                        continue
                        
                    # Count lines of code
                    if not line.startswith('#') and not line.startswith('//'):
                        loc += 1
                    
                    # Check for documentation
                    if '"""' in line or "'''" in line or line.startswith('/**') or line.startswith('*'):
                        has_doc_comments = True
                    
                    # Count functions
                    if re.search(patterns['func_pattern'], line):
                        function_count += 1
                    
                    # Count classes/interfaces
                    if re.search(patterns['class_pattern'], line):
                        class_count += 1
                    
                    # Count imports
                    if re.search(patterns['import_pattern'], line):
                        import_count += 1
                    
                    # Estimate complexity
                    for indicator in patterns['complexity_indicators']:
                        if indicator in line:
                            complexity_score += 1
                    
                    # Memory safety: limit processing for very large files
                    if line_num > 2000:  # Stop processing extremely large files
                        break
                        
        except Exception:
            # Fallback for files that can't be read
            loc = 0
        
        # Calculate quality score
        quality = self._calculate_quality_fast(loc, function_count, class_count, has_doc_comments, complexity_score)
        
        return LightweightAnalysis(
            file_path=str(path),
            language=language,
            lines_of_code=loc,
            function_count=function_count,
            class_count=class_count,
            import_count=import_count,
            estimated_complexity=min(complexity_score, 50),  # Cap complexity
            quality_score=quality,
            has_documentation=has_doc_comments,
            analysis_time=time.time() - start_time
        )
    
    def _detect_language_fast(self, path: Path) -> str:
        """Fast language detection using file extension only."""
        suffix = path.suffix.lower()
        
        for language, config in LANGUAGE_ESSENTIALS.items():
            if suffix in config['ext']:
                return language
        
        return 'unknown'
    
    def _calculate_quality_fast(self, loc: int, functions: int, classes: int, 
                              has_docs: bool, complexity: int) -> float:
        """
        Calculate code quality score using lightweight metrics.
        
        Why: Provides quality assessment without heavy analysis
        Where: Called during streaming analysis for quality scoring
        How: Uses simple heuristics based on structure and documentation
        
        Args:
            loc: Lines of code count
            functions: Number of functions found
            classes: Number of classes found
            has_docs: Whether documentation was detected
            complexity: Estimated complexity score
            
        Returns:
            float: Quality score between 0.0 and 1.0
        """
        score = 0.5  # Base score
        
        # Documentation bonus
        if has_docs:
            score += 0.2
        
        # Structure bonus (functions and classes indicate organized code)
        if functions > 0 or classes > 0:
            score += 0.1
        
        # Complexity penalty
        avg_complexity = complexity / max(loc / 10, 1)  # Rough complexity per code block
        if avg_complexity < 2:
            score += 0.1  # Simple code bonus
        elif avg_complexity > 5:
            score -= 0.2  # Complex code penalty
        
        # Length penalty (very long files are harder to maintain)
        if loc > 500:
            score -= 0.1
        elif loc > 1000:
            score -= 0.2
        
        return max(0.1, min(1.0, score))
    
    def _cache_analysis(self, key: str, analysis: LightweightAnalysis):
        """
        Cache analysis result with LRU eviction.
        
        Why: Provides caching while respecting memory constraints
        Where: Called after successful analysis to cache results
        How: Uses OrderedDict for LRU behavior with size limits
        
        Args:
            key: Cache key for the analysis
            analysis: Analysis result to cache
        """
        # Add to cache
        self.analysis_cache[key] = analysis
        
        # LRU eviction
        cache_limit = self.system_constraints['cache_limit']
        while len(self.analysis_cache) > cache_limit:
            self.analysis_cache.popitem(last=False)  # Remove oldest
    
    def analyze_clever_codebase_batch(self) -> Dict[str, Any]:
        """
        Analyze Clever's codebase in memory-efficient batches.
        
        Why: Provides codebase overview without overwhelming system memory
        Where: Called by cognitive sovereignty for self-awareness
        How: Processes files in small batches with memory cleanup between batches
        
        Returns:
            Dict with codebase analysis summary
        """
        clever_dir = Path(__file__).parent
        python_files = list(clever_dir.glob('*.py'))
        
        # Limit files to prevent memory overload
        max_files = min(len(python_files), 15)  # Process max 15 files
        batch_size = self.system_constraints['batch_size']
        
        total_analysis = {
            'files_processed': 0,
            'total_loc': 0,
            'total_functions': 0,
            'total_classes': 0,
            'quality_scores': [],
            'languages': {},
            'modification_candidates': []
        }
        
        # Process in batches
        for i in range(0, max_files, batch_size):
            batch = python_files[i:i+batch_size]
            
            for file_path in batch:
                # Skip problematic files
                if file_path.name.startswith('.') or file_path.stat().st_size > 500_000:  # Skip large files
                    continue
                
                analysis = self.analyze_file_lightweight(str(file_path))
                if analysis:
                    total_analysis['files_processed'] += 1
                    total_analysis['total_loc'] += analysis.lines_of_code
                    total_analysis['total_functions'] += analysis.function_count
                    total_analysis['total_classes'] += analysis.class_count
                    total_analysis['quality_scores'].append(analysis.quality_score)
                    
                    # Track languages
                    lang = analysis.language
                    if lang not in total_analysis['languages']:
                        total_analysis['languages'][lang] = 0
                    total_analysis['languages'][lang] += 1
                    
                    # Identify modification candidates (high quality, manageable size)
                    if (analysis.quality_score > 0.6 and 
                        analysis.lines_of_code < 200 and
                        analysis.function_count > 0):
                        total_analysis['modification_candidates'].append({
                            'file': file_path.name,
                            'quality': analysis.quality_score,
                            'functions': analysis.function_count
                        })
            
            # Memory cleanup between batches
            gc.collect()
        
        # Calculate summary statistics
        avg_quality = (sum(total_analysis['quality_scores']) / 
                      len(total_analysis['quality_scores'])) if total_analysis['quality_scores'] else 0.5
        
        return {
            'summary': total_analysis,
            'average_quality': avg_quality,
            'codebase_health': 'excellent' if avg_quality > 0.8 else 'good' if avg_quality > 0.6 else 'fair',
            'memory_usage': self._get_memory_status(),
            'system_constraints': self.system_constraints,
            'modification_readiness': len(total_analysis['modification_candidates']) > 0
        }
    
    def _get_memory_status(self) -> Dict[str, Any]:
        """Get current memory usage status."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            process = psutil.Process()
            
            return {
                'system_available_mb': memory.available / (1024 * 1024),
                'system_percent_used': memory.percent,
                'process_memory_mb': process.memory_info().rss / (1024 * 1024),
                'cache_entries': len(self.analysis_cache),
                'memory_pressure': memory.percent > 85
            }
        except ImportError:
            return {
                'system_available_mb': 'unknown',
                'memory_pressure': True,  # Assume pressure without monitoring
                'cache_entries': len(self.analysis_cache)
            }
    
    def get_system_awareness_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive system awareness report for Clever.
        
        Why: Enables Clever to understand her hardware environment and constraints
        Where: Called by cognitive sovereignty for system self-awareness
        How: Combines memory analysis, system constraints, and processing capabilities
        
        Returns:
            Dict with detailed system awareness information
        """
        memory_status = self._get_memory_status()
        
        # Determine Clever's operational mode based on constraints
        if self.system_constraints['low_memory_mode']:
            operational_mode = 'conservation_mode'
            capabilities = ['lightweight_analysis', 'safe_modifications', 'batch_processing']
            recommendations = [
                'Process files in small batches',
                'Use streaming analysis for large files', 
                'Limit concurrent operations',
                'Clear cache frequently'
            ]
        else:
            operational_mode = 'standard_mode'
            capabilities = ['full_analysis', 'code_generation', 'comprehensive_modifications']
            recommendations = [
                'Standard processing available',
                'Can handle larger codebases',
                'Full feature set enabled'
            ]
        
        return {
            'device_type': 'chromebook',
            'operational_mode': operational_mode,
            'memory_constraints': {
                'total_memory_mb': self.system_constraints['total_memory_mb'],
                'available_memory_mb': self.system_constraints['available_memory_mb'],
                'memory_pressure': memory_status.get('memory_pressure', True),
                'low_memory_threshold': 300  # MB
            },
            'code_intelligence_capabilities': capabilities,
            'processing_strategy': self.system_constraints['processing_strategy'],
            'performance_limits': {
                'max_batch_size': self.system_constraints['batch_size'],
                'max_cache_entries': self.system_constraints['cache_limit'],
                'max_file_size_kb': 500,  # Skip files larger than 500KB
                'max_concurrent_analyses': 2
            },
            'recommendations': recommendations,
            'optimization_status': {
                'cache_usage': f"{len(self.analysis_cache)}/{self.system_constraints['cache_limit']}",
                'files_analyzed': self.total_analyzed_files,
                'modifications_performed': self.modification_count,
                'memory_efficient': True
            }
        }
    
    def suggest_safe_modification(self, file_path: str, enhancement_type: str = 'documentation') -> Optional[SafeModification]:
        """
        Suggest a safe code modification that won't break functionality.
        
        Why: Enables Clever to safely improve her own code
        Where: Called by cognitive sovereignty for self-improvement
        How: Identifies low-risk modifications like adding documentation or optimizing imports
        
        Args:
            file_path: Path to file to modify
            enhancement_type: Type of enhancement ('documentation', 'optimization', 'cleanup')
            
        Returns:
            SafeModification or None if no safe modifications found
        """
        analysis = self.analyze_file_lightweight(file_path)
        if not analysis:
            return None
        
        # Only suggest modifications for high-quality, manageable files
        if analysis.quality_score < 0.5 or analysis.lines_of_code > 300:
            return None
        
        try:
            path = Path(file_path)
            content = path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            if enhancement_type == 'documentation' and not analysis.has_documentation:
                # Suggest adding file-level docstring
                if not lines[0].strip().startswith('"""') and not lines[1].strip().startswith('"""'):
                    suggested_docstring = f'"""\n{path.name} - Enhanced by Clever\'s code intelligence\n\nWhy: Auto-generated documentation for improved code clarity\nWhere: {path.name} in Clever\'s codebase\nHow: Added comprehensive documentation following Clever\'s standards\n"""'
                    
                    return SafeModification(
                        file_path=file_path,
                        operation='add',
                        target_line=1,
                        original_snippet='',
                        new_snippet=suggested_docstring,
                        safety_score=0.9,
                        timestamp=time.time()
                    )
            
            elif enhancement_type == 'optimization':
                # Suggest simple optimizations like removing unused imports (very safe)
                unused_imports = self._find_unused_imports_simple(lines)
                if unused_imports:
                    return SafeModification(
                        file_path=file_path,
                        operation='modify',
                        target_line=unused_imports[0]['line'],
                        original_snippet=unused_imports[0]['content'],
                        new_snippet='# ' + unused_imports[0]['content'] + '  # Commented by Clever - appears unused',
                        safety_score=0.8,
                        timestamp=time.time()
                    )
        
        except Exception:
            pass
            
        return None
    
    def _find_unused_imports_simple(self, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Find potentially unused imports using simple text analysis.
        
        Why: Identifies optimization opportunities safely
        Where: Called by suggest_safe_modification for code cleanup
        How: Uses text matching to find imports that don't appear to be used
        
        Args:
            lines: List of code lines to analyze
            
        Returns:
            List of potentially unused import dictionaries
        """
        imports = []
        code_content = ' '.join(lines[10:])  # Skip header for usage checking
        
        for i, line in enumerate(lines[:20]):  # Only check first 20 lines for imports
            line = line.strip()
            
            # Simple import detection
            if line.startswith('import ') and ' as ' not in line:
                module_name = line.replace('import ', '').split('.')[0].strip()
                # Check if module name appears anywhere in the code
                if module_name not in code_content and len(module_name) > 2:
                    imports.append({
                        'line': i + 1,
                        'content': line,
                        'module': module_name
                    })
        
        return imports[:2]  # Return max 2 to be conservative
    
    def clear_cache(self):
        """Clear analysis cache to free memory."""
        self.analysis_cache.clear()
        gc.collect()

# Singleton for memory efficiency
_memory_optimized_engine = None

def get_memory_optimized_code_intelligence():
    """
    Get the memory-optimized code intelligence engine.
    
    Why: Provides singleton access to memory-efficient code analysis
    Where: Called by cognitive sovereignty and other systems needing code intelligence
    How: Creates single instance optimized for current system constraints
    
    Returns:
        MemoryOptimizedCodeIntelligence: Lightweight code intelligence engine
    """
    global _memory_optimized_engine
    
    if _memory_optimized_engine is None:
        _memory_optimized_engine = MemoryOptimizedCodeIntelligence()
    
    return _memory_optimized_engine