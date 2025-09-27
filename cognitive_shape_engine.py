"""
Cognitive Shape Engine - Intelligent Shape Generation with Memory Integration

Why: Connects Clever's shape generation to her memory and cognitive systems,
     creating intelligent, context-aware, personalized geometric visualizations
     that learn from interactions and adapt to user preferences.
Where: Bridges shape_generator.py with memory_engine.py and persona.py
How: Uses memory patterns, preference learning, and contextual analysis
     to generate shapes that reflect cognitive state and learned aesthetics.

Connects to:
    - shape_generator.py: Uses base mathematical shape generation
    - memory_engine.py: Learns preferences and stores shape interaction patterns
    - persona.py: Receives contextual analysis and emotional state
    - nlp_processor.py: Analyzes shape requests for complexity and style hints
"""

import math
from dataclasses import dataclass
from collections import defaultdict, Counter

from shape_generator import get_shape_generator, Shape, ShapePoint
from memory_engine import get_memory_engine, MemoryContext
from debug_config import get_debugger, performance_monitor

debugger = get_debugger()

@dataclass
class CognitiveShapeContext:
    """Context for intelligent shape generation
    
    Why: Captures cognitive and emotional factors that influence shape aesthetics
    Where: Used by CognitiveShapeEngine for personalized generation
    How: Combines user intent, emotional state, learned preferences, and context
    """
    user_input: str
    detected_shape: str
    emotional_state: str = "neutral"
    complexity_preference: float = 0.5  # 0.0 = simple, 1.0 = complex
    aesthetic_preference: str = "balanced"  # minimal, balanced, ornate, mathematical
    conversation_context: List[str] = None
    mathematical_sophistication: float = 0.5  # Learned from interaction patterns
    color_palette: str = "default"  # Learned aesthetic preference
    size_preference: str = "medium"  # small, medium, large, adaptive
    animation_style: str = "smooth"  # smooth, dynamic, mathematical, organic

class CognitiveShapeEngine:
    """
    Intelligent Shape Generation Engine with Memory Integration
    
    Why: Creates personalized, context-aware shape generation that learns
         from user interactions and adapts to cognitive and aesthetic preferences
    Where: Core cognitive enhancement system for Clever's mathematical capabilities
    How: Integrates memory patterns, preference learning, and contextual analysis
         to generate shapes that reflect user's evolving mathematical journey
    """
    
    def __init__(self):
        """Initialize cognitive shape engine with memory integration
        
        Why: Sets up connection to memory system and preference tracking
        Where: Called during Clever's initialization for shape enhancement
        How: Connects to existing memory engine and initializes learning patterns
        """
        self.shape_generator = get_shape_generator()
        self.memory_engine = get_memory_engine()
        
        # Learned preference tracking
        self.shape_preferences = defaultdict(float)  # shape_type -> preference_score
        self.complexity_history = []  # Track complexity evolution over time
        self.aesthetic_patterns = defaultdict(int)  # Track aesthetic choices
        self.context_associations = defaultdict(list)  # Context -> shape patterns
        
        # Cognitive adaptation parameters
        self.learning_rate = 0.1
        self.complexity_adaptation_rate = 0.05
        self.aesthetic_memory_depth = 20  # Recent interactions to consider
        
        # Load existing preferences from memory
        self._load_cognitive_preferences()
        
        debugger.info('cognitive_shape_engine', 'Cognitive shape engine initialized with memory integration')
    
    def _load_cognitive_preferences(self):
        """Load learned preferences from memory system
        
        Why: Restores previously learned aesthetic and complexity preferences
        Where: Called during initialization to maintain continuity
        How: Queries memory engine for shape-related preference patterns
        """
        try:
            # Load shape type preferences
            preferences = self.memory_engine.predict_preferences("shape generation")
            
            # Extract shape-specific preferences
            for pref_key, pref_data in preferences.items():
                if 'shape_' in pref_key:
                    shape_type = pref_key.replace('shape_', '')
                    self.shape_preferences[shape_type] = pref_data.get('confidence', 0.5)
                    
            # Load complexity and aesthetic patterns from recent memories
            recent_memories = self.memory_engine.get_contextual_memory(
                "shape generation mathematical complexity", max_results=10
            )
            
            for memory in recent_memories:
                # Extract complexity patterns
                content = memory.get('content', '')
                if 'complexity' in content.lower():
                    # Parse complexity indicators from memory content
                    if 'simple' in content.lower():
                        self.complexity_history.append(0.3)
                    elif 'complex' in content.lower() or 'advanced' in content.lower():
                        self.complexity_history.append(0.8)
                    else:
                        self.complexity_history.append(0.5)
                        
            debugger.info('cognitive_shape_engine', f'Loaded {len(self.shape_preferences)} shape preferences and {len(self.complexity_history)} complexity patterns')
            
        except Exception as e:
            debugger.warning('cognitive_shape_engine', f'Could not load preferences: {e}')
            # Initialize with defaults
            self.complexity_history = [0.5]
    
    @performance_monitor('cognitive_shape_engine.generate_intelligent_shape')
    def generate_intelligent_shape(self, context: CognitiveShapeContext) -> Tuple[Shape, Dict[str, Any]]:
        """Generate shape with cognitive intelligence and memory integration
        
        Why: Creates personalized shapes that adapt to user's cognitive patterns,
             aesthetic preferences, and current emotional/contextual state
        Where: Called by persona engine when shape generation is requested
        How: Analyzes context, applies learned preferences, adapts complexity,
             generates shape, and stores interaction for future learning
        
        Args:
            context: Cognitive context including user intent and state
            
        Returns:
            Tuple of (Shape object, cognitive_metadata dict)
        """
        # Step 1: Analyze cognitive context and adapt parameters
        cognitive_params = self._analyze_cognitive_context(context)
        
        # Step 2: Apply learned preferences and patterns
        enhanced_params = self._apply_learned_preferences(context, cognitive_params)
        
        # Step 3: Generate base shape with enhanced parameters
        base_shape = self.shape_generator.create_shape(
            context.detected_shape,
            **enhanced_params['shape_params']
        )
        
        # Step 4: Apply cognitive enhancements (colors, patterns, adaptations)
        enhanced_shape = self._apply_cognitive_enhancements(
            base_shape, context, enhanced_params
        )
        
        # Step 5: Generate cognitive metadata for frontend and learning
        cognitive_metadata = self._generate_cognitive_metadata(
            context, enhanced_params, enhanced_shape
        )
        
        # Step 6: Store interaction for learning and adaptation
        self._store_cognitive_interaction(context, enhanced_shape, cognitive_metadata)
        
        debugger.info('cognitive_shape_engine', f'Generated intelligent {context.detected_shape} with cognitive adaptations')
        
        return enhanced_shape, cognitive_metadata
    
    def _analyze_cognitive_context(self, context: CognitiveShapeContext) -> Dict[str, Any]:
        """Analyze cognitive context to determine generation parameters
        
        Why: Interprets user's current cognitive state and contextual cues
        Where: First step in intelligent shape generation pipeline
        How: Analyzes emotional state, conversation flow, and environmental factors
        """
        analysis = {
            'adapted_complexity': self._calculate_adaptive_complexity(context),
            'emotional_influence': self._analyze_emotional_influence(context),
            'contextual_suggestions': self._analyze_contextual_patterns(context),
            'aesthetic_direction': self._determine_aesthetic_direction(context)
        }
        
        debugger.info('cognitive_shape_engine', f'Cognitive analysis: complexity={analysis["adapted_complexity"]:.2f}, aesthetic={analysis["aesthetic_direction"]}')
        return analysis
    
    def _calculate_adaptive_complexity(self, context: CognitiveShapeContext) -> float:
        """Calculate adaptive complexity based on user's mathematical journey
        
        Why: Gradually increases complexity as user demonstrates understanding
        Where: Used to determine appropriate mathematical sophistication level
        How: Analyzes complexity history and current context for adaptive scaling
        """
        # Base complexity from context
        base_complexity = context.complexity_preference
        
        # Historical complexity trend (learning curve)
        if self.complexity_history:
            avg_complexity = sum(self.complexity_history[-5:]) / len(self.complexity_history[-5:])
            trend = avg_complexity * 0.7 + base_complexity * 0.3
        else:
            trend = base_complexity
            
        # Emotional state influence
        emotional_modifiers = {
            'excited': 0.2,    # More complex when excited
            'curious': 0.15,   # Slightly more complex when curious
            'calm': 0.0,       # Neutral
            'frustrated': -0.1, # Simpler when frustrated
            'confused': -0.2    # Much simpler when confused
        }
        
        emotional_adjustment = emotional_modifiers.get(context.emotional_state, 0.0)
        
        # Mathematical sophistication influence
        sophistication_boost = context.mathematical_sophistication * 0.1
        
        # Calculate final adaptive complexity (clamped to 0.0-1.0)
        adaptive_complexity = max(0.0, min(1.0, trend + emotional_adjustment + sophistication_boost))
        
        return adaptive_complexity
    
    def _analyze_emotional_influence(self, context: CognitiveShapeContext) -> Dict[str, Any]:
        """Analyze how emotional state should influence shape generation
        
        Why: Creates emotionally resonant shapes that match user's current state
        Where: Used to adjust colors, patterns, and visual characteristics
        How: Maps emotional states to visual and mathematical properties
        """
        emotional_mappings = {
            'excited': {
                'color_energy': 0.9,
                'pattern_density': 0.8,
                'animation_intensity': 0.9,
                'size_boost': 0.2
            },
            'curious': {
                'color_energy': 0.7,
                'pattern_density': 0.6,
                'animation_intensity': 0.7,
                'size_boost': 0.1
            },
            'calm': {
                'color_energy': 0.4,
                'pattern_density': 0.3,
                'animation_intensity': 0.4,
                'size_boost': 0.0
            },
            'frustrated': {
                'color_energy': 0.6,
                'pattern_density': 0.2,
                'animation_intensity': 0.3,
                'size_boost': -0.1
            },
            'confused': {
                'color_energy': 0.3,
                'pattern_density': 0.1,
                'animation_intensity': 0.2,
                'size_boost': -0.2
            }
        }
        
        return emotional_mappings.get(context.emotional_state, emotional_mappings['calm'])
    
    def _analyze_contextual_patterns(self, context: CognitiveShapeContext) -> List[str]:
        """Analyze conversation context for shape suggestions and patterns
        
        Why: Provides contextually relevant shape suggestions and adaptations
        Where: Used to suggest related shapes and apply context-specific styling
        How: Analyzes conversation history and current context for pattern recognition
        """
        suggestions = []
        
        # Analyze conversation context if available
        if context.conversation_context:
            recent_context = ' '.join(context.conversation_context[-3:]).lower()
            
            # Mathematical context patterns
            if any(word in recent_context for word in ['geometry', 'mathematical', 'equation', 'formula']):
                suggestions.append('mathematical_precision')
                suggestions.append('educational_annotations')
                
            # Nature/organic context patterns  
            if any(word in recent_context for word in ['nature', 'organic', 'flower', 'tree', 'spiral']):
                suggestions.append('organic_styling')
                suggestions.append('natural_proportions')
                
            # Art/creative context patterns
            if any(word in recent_context for word in ['art', 'creative', 'design', 'aesthetic', 'beautiful']):
                suggestions.append('artistic_enhancement')
                suggestions.append('aesthetic_optimization')
                
            # Learning context patterns
            if any(word in recent_context for word in ['learn', 'understand', 'explain', 'teach']):
                suggestions.append('educational_focus')
                suggestions.append('step_by_step_reveal')
        
        # Add memory-based contextual suggestions
        try:
            contextual_memories = self.memory_engine.get_contextual_memory(
                f"shapes {context.detected_shape}", max_results=3
            )
            
            for memory in contextual_memories:
                if 'complex' in memory.get('content', '').lower():
                    suggestions.append('complexity_boost')
                if 'beautiful' in memory.get('content', '').lower():
                    suggestions.append('aesthetic_focus')
                    
        except Exception as e:
            debugger.warning('cognitive_shape_engine', f'Could not load contextual memories: {e}')
        
        return list(set(suggestions))  # Remove duplicates
    
    def _determine_aesthetic_direction(self, context: CognitiveShapeContext) -> str:
        """Determine aesthetic direction based on learned preferences
        
        Why: Applies consistent aesthetic style based on user's demonstrated preferences
        Where: Used to guide visual styling and enhancement choices
        How: Analyzes aesthetic patterns and current context preferences
        """
        # Base aesthetic from context
        base_aesthetic = context.aesthetic_preference
        
        # Check learned aesthetic patterns
        if self.aesthetic_patterns:
            most_common = Counter(self.aesthetic_patterns).most_common(1)
            if most_common and most_common[0][1] > 2:  # At least 3 occurrences
                learned_aesthetic = most_common[0][0]
                # Blend learned with current preference
                return learned_aesthetic if learned_aesthetic != 'default' else base_aesthetic
        
        return base_aesthetic
    
    def _apply_learned_preferences(self, context: CognitiveShapeContext, cognitive_params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned user preferences to shape generation parameters
        
        Why: Personalizes shape generation based on historical interaction patterns
        Where: Second step in intelligent generation pipeline
        How: Modifies generation parameters using learned preference patterns
        """
        enhanced_params = {
            'shape_params': {},
            'visual_enhancements': {},
            'cognitive_adaptations': {}
        }
        
        # Apply shape-specific preferences
        shape_preference = self.shape_preferences.get(context.detected_shape, 0.5)
        
        # Adjust size based on preference and emotional state
        base_size = 200
        preference_size_modifier = (shape_preference - 0.5) * 0.3  # ±15% based on preference
        emotional_size_modifier = cognitive_params['emotional_influence']['size_boost']
        
        enhanced_params['shape_params']['size'] = base_size * (1 + preference_size_modifier + emotional_size_modifier)
        
        # Apply complexity adaptations
        adaptive_complexity = cognitive_params['adapted_complexity']
        
        if adaptive_complexity > 0.7:
            # High complexity preferences
            enhanced_params['shape_params']['iterations'] = enhanced_params['shape_params'].get('iterations', 3) + 1
            enhanced_params['visual_enhancements']['detail_level'] = 'high'
        elif adaptive_complexity < 0.3:
            # Low complexity preferences  
            enhanced_params['visual_enhancements']['detail_level'] = 'minimal'
        else:
            enhanced_params['visual_enhancements']['detail_level'] = 'balanced'
        
        # Apply aesthetic direction
        aesthetic = cognitive_params['aesthetic_direction']
        enhanced_params['visual_enhancements']['aesthetic_style'] = aesthetic
        
        return enhanced_params
    
    def _apply_cognitive_enhancements(self, base_shape: Shape, context: CognitiveShapeContext, params: Dict[str, Any]) -> Shape:
        """Apply cognitive enhancements to base shape
        
        Why: Adds personalized visual and mathematical enhancements
        Where: Third step in intelligent generation pipeline  
        How: Modifies shape points, colors, and properties based on cognitive analysis
        """
        # Enhanced shape points with cognitive color mapping
        enhanced_points = []
        
        emotional_influence = params.get('emotional_influence', {})
        color_energy = emotional_influence.get('color_energy', 0.5)
        
        for i, point in enumerate(base_shape.points):
            # Apply cognitive color enhancement
            enhanced_color = self._calculate_cognitive_color(i, len(base_shape.points), color_energy)
            
            # Create enhanced point with cognitive metadata
            enhanced_point = ShapePoint(
                x=point.x,
                y=point.y,
                z=point.z,
                color=enhanced_color,
                size=point.size,
                metadata={
                    **(point.metadata or {}),
                    'cognitive_enhancement': True,
                    'emotional_resonance': color_energy,
                    'complexity_level': params.get('adapted_complexity', 0.5)
                }
            )
            enhanced_points.append(enhanced_point)
        
        # Create enhanced shape with cognitive properties
        enhanced_shape = Shape(
            name=f"Intelligent {base_shape.name}",
            points=enhanced_points,
            center=base_shape.center,
            bounding_box=base_shape.bounding_box,
            properties={
                **base_shape.properties,
                'cognitive_enhancement': True,
                'learning_integration': True,
                'aesthetic_style': params.get('visual_enhancements', {}).get('aesthetic_style', 'balanced'),
                'complexity_adaptation': params.get('adapted_complexity', 0.5),
                'emotional_resonance': color_energy,
                'personalization_level': min(len(self.complexity_history) / 10.0, 1.0)
            }
        )
        
        return enhanced_shape
    
    def _calculate_cognitive_color(self, index: int, total: int, energy: float) -> str:
        """Calculate cognitively-enhanced color based on emotional energy
        
        Why: Creates emotionally resonant color palettes that adapt to user state
        Where: Used in cognitive enhancement pipeline for point coloring
        How: Combines mathematical color progression with emotional energy mapping
        """
        # Base hue progression
        base_hue = (index / total) * 360
        
        # Energy-based saturation and lightness
        saturation = 40 + (energy * 40)  # 40-80% based on energy
        lightness = 50 + (energy * 20)   # 50-70% based on energy
        
        # Cognitive color harmony adjustments
        if energy > 0.7:
            # High energy: vibrant, warm colors
            base_hue = (base_hue + 30) % 360  # Shift toward warm spectrum
        elif energy < 0.3:
            # Low energy: cool, calm colors  
            base_hue = (base_hue + 180) % 360  # Shift toward cool spectrum
        
        return f"hsl({base_hue}, {saturation}%, {lightness}%)"
    
    def _generate_cognitive_metadata(self, context: CognitiveShapeContext, params: Dict[str, Any], shape: Shape) -> Dict[str, Any]:
        """Generate cognitive metadata for frontend and learning systems
        
        Why: Provides rich metadata for advanced visualization and learning
        Where: Used by frontend for enhanced rendering and by learning system for adaptation
        How: Combines cognitive analysis results with shape properties and user context
        """
        metadata = {
            'cognitive_analysis': {
                'complexity_level': params.get('adapted_complexity', 0.5),
                'emotional_state': context.emotional_state,
                'aesthetic_direction': params.get('aesthetic_direction', 'balanced'),
                'personalization_score': min(len(self.complexity_history) / 10.0, 1.0),
                'learning_iteration': len(self.complexity_history)
            },
            'visual_enhancements': params.get('visual_enhancements', {}),
            'contextual_suggestions': params.get('contextual_suggestions', []),
            'preference_influences': {
                'shape_preference': self.shape_preferences.get(context.detected_shape, 0.5),
                'complexity_trend': sum(self.complexity_history[-3:]) / len(self.complexity_history[-3:]) if self.complexity_history else 0.5,
                'aesthetic_consistency': len(self.aesthetic_patterns) > 0
            },
            'cognitive_adaptations': {
                'memory_integrated': True,
                'preference_learned': len(self.shape_preferences) > 0,
                'context_aware': len(params.get('contextual_suggestions', [])) > 0,
                'emotionally_responsive': context.emotional_state != 'neutral'
            }
        }
        
        return metadata
    
    def _store_cognitive_interaction(self, context: CognitiveShapeContext, shape: Shape, metadata: Dict[str, Any]):
        """Store interaction for cognitive learning and adaptation
        
        Why: Enables continuous learning and personalization improvement
        Where: Final step in intelligent generation pipeline
        How: Creates memory context and stores interaction patterns for future reference
        """
        try:
            # Create memory context for this cognitive interaction
            memory_context = MemoryContext(
                user_input=context.user_input,
                response_text=f"Generated intelligent {context.detected_shape} with cognitive enhancements",
                mode="cognitive_shape_generation",
                sentiment=context.emotional_state,
                session_id=f"shape_gen_{int(time.time())}",
                timestamp=time.time(),
                keywords=[context.detected_shape, 'intelligent_shapes', 'cognitive_generation'],
                entities=[context.detected_shape]
            )
            
            # Store interaction in memory system
            interaction_id = self.memory_engine.store_interaction(memory_context)
            
            # Update preference learning
            self._update_cognitive_preferences(context, metadata)
            
            debugger.info('cognitive_shape_engine', f'Stored cognitive interaction {interaction_id} for learning')
            
        except Exception as e:
            debugger.warning('cognitive_shape_engine', f'Could not store cognitive interaction: {e}')
    
    def _update_cognitive_preferences(self, context: CognitiveShapeContext, metadata: Dict[str, Any]):
        """Update cognitive preferences based on interaction
        
        Why: Enables continuous learning and preference adaptation
        Where: Called after each interaction to update learned patterns
        How: Updates preference scores and pattern tracking based on interaction success
        """
        # Update shape preference (assume positive interaction)
        current_pref = self.shape_preferences[context.detected_shape]
        self.shape_preferences[context.detected_shape] = current_pref + (self.learning_rate * (1.0 - current_pref))
        
        # Update complexity history
        complexity_level = metadata['cognitive_analysis']['complexity_level']
        self.complexity_history.append(complexity_level)
        
        # Trim history to maintain reasonable size
        if len(self.complexity_history) > 50:
            self.complexity_history = self.complexity_history[-50:]
        
        # Update aesthetic patterns
        aesthetic = context.aesthetic_preference
        self.aesthetic_patterns[aesthetic] += 1
        
        # Update context associations
        if context.conversation_context:
            recent_context = ' '.join(context.conversation_context[-2:])
            self.context_associations[recent_context].append(context.detected_shape)
        
        debugger.info('cognitive_shape_engine', f'Updated preferences: {context.detected_shape} preference now {self.shape_preferences[context.detected_shape]:.3f}')

# Global instance for application use
_cognitive_shape_engine = None

def get_cognitive_shape_engine() -> CognitiveShapeEngine:
    """Get global CognitiveShapeEngine instance
    
    Why: Provides singleton access to cognitive shape generation throughout app
    Where: Called by persona engine when intelligent shape generation is needed
    How: Creates instance on first call, returns existing instance on subsequent calls
    
    Connects to:
        - persona.py: PersonaEngine uses this for intelligent shape generation
        - memory_engine.py: Shares memory system for preference learning
        - shape_generator.py: Uses base shape generation capabilities
    """
    global _cognitive_shape_engine
    if _cognitive_shape_engine is None:
        _cognitive_shape_engine = CognitiveShapeEngine()
    return _cognitive_shape_engine