"""
Persona Engine for Clever AI

Why: Generates context-aware, empathetic responses in various modes (Auto,
Creative, Deep Dive, Support, Quick Hit) for Jay specifically. Operates fully
offline, leveraging advanced memory system and local NLP.
Where: Used by app.py for user interactions, connects to memory_engine for
intelligent context and nlp_processor for language analysis.
How: Implements PersonaEngine class with multiple response modes, integrates
advanced memory system, predictive capabilities, and returns PersonaResponse objects.

Connects to:
    - memory_engine.py: Advanced memory and learning system
    - nlp_processor.py: NLP and sentiment analysis  
    - database.py: Persistent storage via memory engine
    - app.py: Main application for user interaction
"""
from __future__ import annotations
import logging
import random
import time
from types import SimpleNamespace
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import the advanced memory system
try:
    from memory_engine import get_memory_engine, MemoryContext
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

from debug_config import get_debugger

logger = logging.getLogger(__name__)
debugger = get_debugger()


class PersonaResponse(SimpleNamespace):
    """
    Response object from PersonaEngine
    
    Why: Structured container for AI responses with metadata
    Where: Returned by PersonaEngine.generate() to app.py
    How: SimpleNamespace with response text, mode, sentiment, suggestions
    """
    def __init__(self, text: str, mode: str = "Auto", sentiment: str = "neutral", 
                 proactive_suggestions: Optional[List[str]] = None):
        super().__init__()
        self.text = text
        self.mode = mode  
        self.sentiment = sentiment
        self.proactive_suggestions = proactive_suggestions or []


class PersonaEngine:
    """
    Main persona engine for Clever AI
    
    Why: Generates contextual responses matching Jay's preferences
    Where: Core component used by Flask app for all AI interactions
    How: Multiple response modes with personality traits and context awareness
    """
    
    def __init__(self):
        """
        Initialize PersonaEngine with response modes and advanced memory
        
        Why: Set up available response modes, personality traits, and memory integration
        Where: Called once during app initialization  
        How: Define mode mappings, personality characteristics, and memory engine connection
        
        Connects to:
            - memory_engine.py: Advanced memory and learning capabilities
        """
        self.modes = {
            "Auto": self._auto_style,
            "Creative": self._creative_style,
            "Deep Dive": self._deep_dive_style,
            "Support": self._support_style,
            "Quick Hit": self._quick_hit_style,
        }
        
        # Jay-specific personality traits
        self.personality_traits = {
            "witty": True,
            "empathetic": True,
            "analytical": True,
            "creative": True,
            "supportive": True,
            "memory_enhanced": MEMORY_AVAILABLE
        }
        
        # Initialize memory engine connection
        self.memory_engine = None
        self.memory_available = MEMORY_AVAILABLE
        if self.memory_available:
            try:
                self.memory_engine = get_memory_engine()
                debugger.info('persona_engine', 'Advanced memory system connected successfully')
            except Exception as e:
                debugger.warning('persona_engine', f'Memory system unavailable: {e}')
                self.memory_available = False
        
        debugger.info('persona_engine', f'PersonaEngine initialized with memory: {self.memory_available}')

    def generate(
        self,
        text: str,
        mode: str = "Auto", 
        context: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> PersonaResponse:
        """
        Generate response using specified mode with advanced memory integration
        
        Why: Main entry point for AI response generation with learning capabilities
        Where: Called by app.py chat endpoint for user interactions
        How: Route to appropriate mode handler with memory context, return structured response
        
        Connects to:
            - app.py: Main application chat handling
            - memory_engine.py: Advanced memory and learning system
            - nlp_processor.py: Text analysis and processing
        """
        if context is None:
            context = {}
        if history is None:
            history = []
        
        start_time = time.time()
        
        # Extract keywords and entities for context
        keywords = self._extract_keywords(text)
        entities = self._extract_entities(text)
        
        # Determine sentiment
        sentiment = self._analyze_sentiment(text)
        
        # Memory-enhanced processing
        memory_context = None
        predicted_mode = mode
        relevant_memories = []
        conversation_history = []
        
        if self.memory_available and self.memory_engine:
            try:
                # Get relevant memories for context
                relevant_memories = self.memory_engine.get_contextual_memory(text, max_results=3)
                
                # Get conversation history for context
                conversation_history = self.memory_engine.get_conversation_history(session_limit=5)
                
                # Predict optimal mode if in Auto mode
                if mode == "Auto":
                    predictions = self.memory_engine.predict_preferences(text)
                    if predictions['confidence'] > 0.6:
                        predicted_mode = predictions['suggested_mode']
                        debugger.info('persona_engine', f'Memory predicted mode: {predicted_mode} (confidence: {predictions["confidence"]:.2f})')
                
                # Create memory context for storage
                memory_context = MemoryContext(
                    user_input=text,
                    timestamp=start_time,
                    session_id=self.memory_engine.session_id,
                    mode=predicted_mode,
                    sentiment=sentiment,
                    keywords=keywords,
                    entities=entities,
                    importance_score=self._calculate_importance(text, keywords, entities)
                )
                
            except Exception as e:
                debugger.warning('persona_engine', f'Memory processing failed: {e}')
        
        # Enhanced context with memory
        enhanced_context = {
            **context,
            'relevant_memories': relevant_memories,
            'conversation_history': conversation_history,
            'predicted_mode': predicted_mode,
            'memory_available': self.memory_available
        }
        
        # Route to appropriate mode handler
        mode_handler = self.modes.get(predicted_mode, self._auto_style)
        response_text = mode_handler(text, keywords, enhanced_context, history)
        
        # Generate memory-enhanced proactive suggestions
        suggestions = self._generate_suggestions(text, keywords, enhanced_context)
        
        # Store interaction in memory
        if self.memory_available and self.memory_engine and memory_context:
            try:
                memory_context.response_text = response_text
                self.memory_engine.store_interaction(memory_context)
                debugger.info('persona_engine', 'Interaction stored in memory successfully')
            except Exception as e:
                debugger.warning('persona_engine', f'Failed to store interaction: {e}')
        
        # Performance logging
        processing_time = time.time() - start_time
        debugger.info('persona_engine', f'Response generated in {processing_time:.3f}s with mode: {predicted_mode}')
        
        return PersonaResponse(
            text=response_text,
            mode=predicted_mode,
            sentiment=sentiment,
            proactive_suggestions=suggestions
        )

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract key terms from user input
        
        Why: Identify important concepts for contextual responses
        Where: Used by all mode handlers for content awareness
        How: Simple word extraction with common word filtering
        """
        # Simple keyword extraction (avoiding spaCy dependency issues)
        words = text.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords[:10]  # Limit to top 10 keywords

    def _analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of user input
        
        Why: Adapt response tone to user's emotional state
        Where: Used by generate() for response customization
        How: Simple rule-based sentiment detection
        """
        positive_words = ['good', 'great', 'awesome', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'excited', 'pleased']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'annoyed', 'disappointed', 'worried']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _extract_entities(self, text: str) -> List[str]:
        """
        Extract basic entities from user input
        
        Why: Identify important names, places, and concepts for memory storage
        Where: Used by generate() for enhanced context building
        How: Simple pattern matching for entity detection
        """
        import re
        entities = []
        
        # Find capitalized words (potential proper nouns)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(proper_nouns)
        
        # Find numbers and dates
        numbers = re.findall(r'\b\d+\b', text)
        entities.extend(numbers)
        
        # Find email-like patterns
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        entities.extend(emails)
        
        return list(set(entities))  # Remove duplicates
    
    def _calculate_importance(self, text: str, keywords: List[str], entities: List[str]) -> float:
        """
        Calculate importance score for interaction
        
        Why: Determine how significant this interaction is for memory storage
        Where: Used by generate() for memory context creation
        How: Combine multiple factors to calculate relevance score
        """
        importance = 0.3  # Base importance
        
        # Length factor (longer messages often more important)
        word_count = len(text.split())
        if word_count > 20:
            importance += 0.2
        elif word_count > 10:
            importance += 0.1
        
        # Keyword richness
        if len(keywords) > 5:
            importance += 0.2
        elif len(keywords) > 2:
            importance += 0.1
        
        # Entity presence (names, dates, etc. often important)
        if len(entities) > 2:
            importance += 0.3
        elif len(entities) > 0:
            importance += 0.1
        
        # Question detection (questions often important)
        if '?' in text:
            importance += 0.1
        
        # Exclamation detection (emotional content)
        if '!' in text:
            importance += 0.05
        
        return min(1.0, importance)  # Cap at 1.0

    def _generate_suggestions(self, text: str, keywords: List[str], context: Dict[str, Any]) -> List[str]:
        """
        Generate proactive suggestions for follow-up with memory enhancement
        
        Why: Provide helpful next steps and conversation continuers based on memory and context
        Where: Used by generate() to enhance user experience with intelligent suggestions
        How: Context-aware suggestion generation using memory patterns and learned preferences
        """
        suggestions = []
        
        # Memory-enhanced suggestions
        relevant_memories = context.get('relevant_memories', [])
        conversation_history = context.get('conversation_history', [])
        
        # Memory-based suggestions
        if relevant_memories:
            memory_topics = [mem['content'] for mem in relevant_memories[:2]]
            if memory_topics:
                suggestions.append(f"This reminds me of when we discussed {memory_topics[0]}. Want to explore that connection?")
        
        # Conversation flow suggestions  
        if conversation_history:
            recent_modes = [conv.get('mode', 'Auto') for conv in conversation_history[:3]]
            if 'Creative' in recent_modes and context.get('predicted_mode') != 'Creative':
                suggestions.append("Want to get creative with this like we did earlier?")
            elif 'Deep Dive' in recent_modes:
                suggestions.append("Should we do another deep dive analysis?")
        
        # Question-based suggestions
        if '?' in text:
            suggestions.append("Would you like me to dive deeper into this topic?")
            suggestions.append("Should I explore related areas?")
        
        # Keyword-based suggestions with memory context
        if any(word in keywords for word in ['analyze', 'study', 'research']):
            suggestions.append("Want me to break this down step by step?")
            if relevant_memories:
                suggestions.append("I can connect this to what we've learned before!")
            
        if any(word in keywords for word in ['create', 'make', 'build']):
            suggestions.append("Ready to brainstorm some ideas?")
            suggestions.append("Want me to suggest some creative approaches?")
            
        # Pattern-based suggestions from memory
        if self.memory_available and len(keywords) > 0:
            # Add suggestions based on learned patterns
            suggestions.append("I notice patterns in how you like to explore topics - want my insights?")
        
        # Limit and deduplicate suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))  # Remove duplicates while preserving order
        return unique_suggestions[:3]  # Limit to 3 suggestions

    def _auto_style(self, text: str, keywords: List[str], context: Dict[str, Any], history: List[Dict[str, Any]]) -> str:
        """
        Auto mode - balanced, contextual responses
        
        Why: Default mode providing natural, balanced responses
        Where: Used when no specific mode is requested
        How: Analyze input and provide appropriate response style
        """
        # Simple response based on input characteristics
        if '?' in text:
            responses = [
                f"Great question about {keywords[0] if keywords else 'that topic'}! Let me think through this with you.",
                f"Interesting you're asking about {keywords[0] if keywords else 'this'}. Here's my take:",
                f"That's a thoughtful question. Let me share some insights on {keywords[0] if keywords else 'this topic'}."
            ]
        else:
            responses = [
                f"I see you're thinking about {keywords[0] if keywords else 'this'}. That's fascinating!",
                f"Thanks for sharing that with me. The topic of {keywords[0] if keywords else 'this'} is really interesting.",
                f"I appreciate you bringing up {keywords[0] if keywords else 'this topic'}. Let me add some thoughts."
            ]
            
        return random.choice(responses)

    def _creative_style(self, text: str, keywords: List[str], context: Dict[str, Any], history: List[Dict[str, Any]]) -> str:
        """
        Creative mode - imaginative, innovative responses
        
        Why: Generate creative, out-of-the-box thinking for brainstorming
        Where: Used when user requests creative exploration
        How: Use metaphors, analogies, and creative language patterns
        """
        creative_starters = [
            "Ooh, let's paint outside the lines here! ",
            "Time to unleash some creative magic! ",
            "Let's approach this like artists approaching a blank canvas! ",
            "Here's where we can get delightfully unconventional! "
        ]
        
        if keywords:
            creative_response = f"What if we reimagined {keywords[0]} completely? We could explore it through the lens of {random.choice(['storytelling', 'design thinking', 'musical composition', 'architectural principles', 'nature patterns'])}."
        else:
            creative_response = "Let's think about this in a completely fresh way, breaking all the conventional rules!"
            
        return random.choice(creative_starters) + creative_response

    def _deep_dive_style(self, text: str, keywords: List[str], context: Dict[str, Any], history: List[Dict[str, Any]]) -> str:
        """
        Deep Dive mode - thorough, analytical responses
        
        Why: Provide comprehensive analysis for complex topics
        Where: Used when user requests detailed exploration
        How: Structure response with multiple perspectives and depth
        """
        deep_starters = [
            "Let's dig deep into this. ",
            "Time for a thorough analysis. ",
            "Let me break this down comprehensively. ",
            "Here's a detailed exploration of this topic. "
        ]
        
        analysis_aspects = ["historical context", "current implications", "future possibilities", "different perspectives", "underlying principles"]
        
        if keywords:
            deep_response = f"When examining {keywords[0]}, we should consider {random.choice(analysis_aspects)}. This connects to broader themes and requires careful consideration of multiple factors."
        else:
            deep_response = "This topic deserves thorough analysis from multiple angles, considering both immediate and long-term implications."
            
        return random.choice(deep_starters) + deep_response

    def _support_style(self, text: str, keywords: List[str], context: Dict[str, Any], history: List[Dict[str, Any]]) -> str:
        """
        Support mode - empathetic, encouraging responses
        
        Why: Provide emotional support and encouragement
        Where: Used when user needs motivation or reassurance  
        How: Use empathetic language and supportive messaging
        """
        support_starters = [
            "I'm here with you on this. ",
            "You've got this, and I'm here to help. ",
            "I understand this might be challenging. ",
            "Let's work through this together. "
        ]
        
        if keywords:
            support_response = f"Dealing with {keywords[0]} can be complex, but you're approaching it thoughtfully. Remember that progress often comes in small steps."
        else:
            support_response = "Whatever you're working through, remember that you have the strength and capability to handle it."
            
        return random.choice(support_starters) + support_response

    def _quick_hit_style(self, text: str, keywords: List[str], context: Dict[str, Any], history: List[Dict[str, Any]]) -> str:
        """
        Quick Hit mode - concise, direct responses
        
        Why: Provide fast, actionable answers for efficiency
        Where: Used when user needs quick information or decisions
        How: Deliver key points without lengthy explanations
        """
        if keywords:
            return f"Quick take on {keywords[0]}: {random.choice(['Focus on the essentials.', 'Start with the fundamentals.', 'Prioritize the key factors.', 'Keep it simple and actionable.'])}"
        else:
            return random.choice([
                "Bottom line: Keep it focused and actionable.",
                "Key point: Start with what matters most.",
                "Quick advice: Break it down into clear steps.",
                "Essential approach: Focus on high-impact actions."
            ])


# Global instance for app.py
persona_engine = PersonaEngine()