"""
Advanced AI Enhancement Module for Clever

Why: Extends Clever's intelligence with advanced memory, learning, and 
contextual awareness capabilities beyond basic NLP processing.
Where: Plugs into persona.py and evolution_engine.py to supercharge responses
How: Implements memory networks, context graphs, and adaptive learning

Connects to:
    - persona.py: Enhanced response generation with memory
    - evolution_engine.py: Advanced learning and growth tracking
    - database.py: Persistent memory storage and retrieval
"""
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)


class MemoryNetwork:
    """
    Advanced memory system for contextual awareness
    
    Why: Gives Clever long-term memory and context understanding
    Where: Core component for intelligent conversation continuity  
    How: Graph-based memory with weighted connections and decay
    """
    
    def __init__(self, db_manager=None):
        """
        Initialize memory network
        
        Why: Set up advanced memory storage and retrieval system
        Where: Called during PersonaEngine initialization
        How: Create memory graphs, connection weights, and decay systems
        """
        self.db = db_manager
        self.short_term_memory = deque(maxlen=20)  # Last 20 interactions
        self.concept_graph = defaultdict(lambda: defaultdict(float))  # Concept connections
        self.memory_weights = defaultdict(float)  # Memory importance scores
        self.context_history = defaultdict(list)  # User context patterns
        
    def store_interaction(self, user_input: str, response: str, context: Dict[str, Any]):
        """
        Store interaction in memory network
        
        Why: Build long-term understanding of user patterns and preferences
        Where: Called after each user interaction
        How: Extract concepts, build connections, weight importance
        """
        timestamp = datetime.now()
        interaction_id = hashlib.md5(f"{user_input}{timestamp}".encode()).hexdigest()[:8]
        
        # Store in short-term memory
        memory_item = {
            'id': interaction_id,
            'timestamp': timestamp,
            'user_input': user_input,
            'response': response,
            'context': context,
            'concepts': self._extract_concepts(user_input)
        }
        self.short_term_memory.append(memory_item)
        
        # Build concept connections
        self._build_concept_connections(memory_item['concepts'], context)
        
        # Update memory weights based on interaction quality
        self._update_memory_weights(interaction_id, context)
        
        logger.info(f"[memory] Stored interaction {interaction_id} with {len(memory_item['concepts'])} concepts")
    
    def retrieve_relevant_context(self, current_input: str, max_items: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve contextually relevant memories
        
        Why: Provide Clever with relevant past context for better responses
        Where: Called during response generation in persona.py  
        How: Use concept similarity and memory weights to find relevant items
        """
        current_concepts = self._extract_concepts(current_input)
        relevance_scores = []
        
        for memory in self.short_term_memory:
            score = self._calculate_relevance(current_concepts, memory['concepts'])
            weight = self.memory_weights.get(memory['id'], 1.0)
            final_score = score * weight
            
            if final_score > 0.1:  # Minimum relevance threshold
                relevance_scores.append((final_score, memory))
        
        # Sort by relevance and return top items
        relevance_scores.sort(reverse=True, key=lambda x: x[0])
        return [memory for score, memory in relevance_scores[:max_items]]
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Enhanced concept extraction with NLP patterns
        import re
        
        concepts = []
        
        # Extract action words (verbs)
        action_patterns = r'\b(build|create|make|fix|update|enhance|improve|develop|design|implement)\w*\b'
        actions = re.findall(action_patterns, text.lower())
        concepts.extend([f"action:{action}" for action in actions])
        
        # Extract tech terms
        tech_patterns = r'\b(ai|ui|api|database|python|javascript|react|flask|git|branch|merge|code|function|class|method)\b'
        tech_terms = re.findall(tech_patterns, text.lower())
        concepts.extend([f"tech:{term}" for term in tech_terms])
        
        # Extract emotional indicators
        emotion_patterns = r'\b(excited|happy|frustrated|confused|love|hate|awesome|terrible|amazing|brilliant)\b'
        emotions = re.findall(emotion_patterns, text.lower())
        concepts.extend([f"emotion:{emotion}" for emotion in emotions])
        
        return list(set(concepts))
    
    def _build_concept_connections(self, concepts: List[str], context: Dict[str, Any]):
        """Build weighted connections between concepts"""
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                # Increase connection weight
                self.concept_graph[concept1][concept2] += 1.0
                self.concept_graph[concept2][concept1] += 1.0
    
    def _calculate_relevance(self, current_concepts: List[str], memory_concepts: List[str]) -> float:
        """Calculate relevance score between concept sets"""
        if not current_concepts or not memory_concepts:
            return 0.0
        
        # Direct concept overlap
        overlap = set(current_concepts) & set(memory_concepts)
        direct_score = len(overlap) / max(len(current_concepts), len(memory_concepts))
        
        # Indirect connections through concept graph
        indirect_score = 0.0
        for current in current_concepts:
            for memory in memory_concepts:
                connection_weight = self.concept_graph[current].get(memory, 0.0)
                indirect_score += connection_weight
        
        # Normalize indirect score
        if len(current_concepts) * len(memory_concepts) > 0:
            indirect_score /= (len(current_concepts) * len(memory_concepts))
        
        return direct_score * 0.7 + indirect_score * 0.3
    
    def _update_memory_weights(self, interaction_id: str, context: Dict[str, Any]):
        """Update memory importance weights"""
        base_weight = 1.0
        
        # Boost weight for positive interactions
        if context.get('sentiment') == 'positive':
            base_weight *= 1.5
        
        # Boost weight for complex interactions
        if context.get('word_count', 0) > 20:
            base_weight *= 1.2
        
        # Boost weight for technical discussions
        if any(tech in str(context).lower() for tech in ['code', 'ai', 'development', 'programming']):
            base_weight *= 1.3
        
        self.memory_weights[interaction_id] = base_weight


class IntelligenceAmplifier:
    """
    Advanced intelligence enhancement system
    
    Why: Makes Clever smarter through pattern recognition and adaptive learning
    Where: Integrates with PersonaEngine for enhanced response generation
    How: Analyzes patterns, predicts needs, suggests improvements
    """
    
    def __init__(self, memory_network: MemoryNetwork):
        """Initialize intelligence amplifier"""
        self.memory = memory_network
        self.pattern_detector = PatternDetector()
        self.response_optimizer = ResponseOptimizer()
        
    def enhance_response(self, user_input: str, base_response: str, context: Dict[str, Any]) -> Tuple[str, List[str]]:
        """
        Enhance response with intelligence amplification
        
        Why: Make responses more intelligent and contextually aware
        Where: Called by PersonaEngine before returning response
        How: Apply memory context, pattern analysis, and optimization
        """
        # Get relevant context from memory
        relevant_memories = self.memory.retrieve_relevant_context(user_input)
        
        # Detect patterns in user behavior
        patterns = self.pattern_detector.analyze_patterns(user_input, relevant_memories)
        
        # Optimize response based on patterns and context
        enhanced_response = self.response_optimizer.optimize_response(
            base_response, patterns, context, relevant_memories
        )
        
        # Generate proactive suggestions
        suggestions = self._generate_proactive_suggestions(patterns, context)
        
        return enhanced_response, suggestions
    
    def _generate_proactive_suggestions(self, patterns: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate intelligent proactive suggestions"""
        suggestions = []
        
        # Pattern-based suggestions
        if patterns.get('frequent_topics'):
            top_topic = patterns['frequent_topics'][0]
            suggestions.append(f"Want to dive deeper into {top_topic}?")
        
        # Context-based suggestions  
        if context.get('sentiment') == 'positive' and 'code' in context.get('keywords', []):
            suggestions.append("Ready to implement this or explore related features?")
        
        if context.get('sentiment') == 'negative':
            suggestions.append("Need help troubleshooting or a different approach?")
        
        return suggestions[:3]  # Limit to 3 suggestions


class PatternDetector:
    """Detects patterns in user behavior and preferences"""
    
    def analyze_patterns(self, current_input: str, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in user interactions"""
        patterns = {
            'frequent_topics': self._find_frequent_topics(memories),
            'time_patterns': self._analyze_time_patterns(memories),
            'interaction_style': self._analyze_interaction_style(memories),
            'technical_focus': self._analyze_technical_focus(memories)
        }
        return patterns
    
    def _find_frequent_topics(self, memories: List[Dict[str, Any]]) -> List[str]:
        """Find most frequently discussed topics"""
        topic_counts = defaultdict(int)
        for memory in memories:
            for concept in memory.get('concepts', []):
                if concept.startswith('tech:') or concept.startswith('action:'):
                    topic_counts[concept] += 1
        
        return [topic for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _analyze_time_patterns(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal patterns in interactions"""
        if not memories:
            return {}
        
        timestamps = [memory['timestamp'] for memory in memories]
        hours = [ts.hour for ts in timestamps]
        
        return {
            'most_active_hour': max(set(hours), key=hours.count) if hours else None,
            'session_length': len(memories)
        }
    
    def _analyze_interaction_style(self, memories: List[Dict[str, Any]]) -> str:
        """Analyze user's preferred interaction style"""
        if not memories:
            return "balanced"
        
        avg_length = sum(len(m['user_input'].split()) for m in memories) / len(memories)
        
        if avg_length > 20:
            return "detailed"
        elif avg_length < 5:
            return "concise"
        else:
            return "balanced"
    
    def _analyze_technical_focus(self, memories: List[Dict[str, Any]]) -> List[str]:
        """Analyze technical areas of focus"""
        tech_focus = defaultdict(int)
        for memory in memories:
            for concept in memory.get('concepts', []):
                if concept.startswith('tech:'):
                    tech_area = concept.split(':')[1]
                    tech_focus[tech_area] += 1
        
        return [area for area, count in sorted(tech_focus.items(), key=lambda x: x[1], reverse=True)[:3]]


class ResponseOptimizer:
    """Optimizes responses based on context and patterns"""
    
    def optimize_response(self, base_response: str, patterns: Dict[str, Any], 
                         context: Dict[str, Any], memories: List[Dict[str, Any]]) -> str:
        """Optimize response based on patterns and context"""
        response = base_response
        
        # Adjust for interaction style
        style = patterns.get('interaction_style', 'balanced')
        if style == 'concise' and len(response.split()) > 15:
            response = self._make_concise(response)
        elif style == 'detailed' and len(response.split()) < 10:
            response = self._add_detail(response, context)
        
        # Add contextual references
        if memories:
            response = self._add_contextual_reference(response, memories[0])
        
        return response
    
    def _make_concise(self, response: str) -> str:
        """Make response more concise"""
        sentences = response.split('. ')
        if len(sentences) > 2:
            return '. '.join(sentences[:2]) + '.'
        return response
    
    def _add_detail(self, response: str, context: Dict[str, Any]) -> str:
        """Add relevant detail to response"""
        keywords = context.get('keywords', [])
        if keywords:
            detail = f" Focusing on {keywords[0]} specifically,"
            return response + detail
        return response
    
    def _add_contextual_reference(self, response: str, recent_memory: Dict[str, Any]) -> str:
        """Add subtle reference to recent context"""
        if recent_memory and 'concepts' in recent_memory:
            concepts = recent_memory['concepts']
            if concepts:
                concept = concepts[0].split(':')[-1]
                if concept not in response.lower():
                    return f"{response} (Building on our {concept} discussion.)"
        return response