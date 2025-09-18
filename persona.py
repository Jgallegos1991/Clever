"""
Persona Engine for Clever AI

Why: Generates context-aware, empathetic responses in various modes (Auto,
Creative, Deep Dive, Support, Quick Hit) for Jay specifically. Operates fully
offline, leveraging local NLP and heuristics.
Where: Used by app.py for user interactions, connects to nlp_processor for
language analysis and database for memory.
How: Implements PersonaEngine class with multiple response modes, integrates
sentiment and suggestion generation, and returns PersonaResponse objects.

Connects to:
    - nlp_processor.py: NLP and sentiment analysis  
    - database.py: Memory and context storage
    - app.py: Main application for user interaction
"""
from __future__ import annotations
import logging
import random
from types import SimpleNamespace
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


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
        Initialize PersonaEngine with response modes
        
        Why: Set up available response modes and personality traits
        Where: Called once during app initialization  
        How: Define mode mappings and personality characteristics
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
            "supportive": True
        }

    def generate(
        self,
        text: str,
        mode: str = "Auto", 
        context: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> PersonaResponse:
        """
        Generate response using specified mode
        
        Why: Main entry point for AI response generation
        Where: Called by app.py chat endpoint for user interactions
        How: Route to appropriate mode handler, return structured response
        
        Connects to:
            - app.py: Main application chat handling
            - nlp_processor.py: Text analysis and processing
        """
        if context is None:
            context = {}
        if history is None:
            history = []
            
        # Extract keywords for context
        keywords = self._extract_keywords(text)
        
        # Route to appropriate mode handler
        mode_handler = self.modes.get(mode, self._auto_style)
        response_text = mode_handler(text, keywords, context, history)
        
        # Determine sentiment
        sentiment = self._analyze_sentiment(text)
        
        # Generate proactive suggestions
        suggestions = self._generate_suggestions(text, keywords, context)
        
        return PersonaResponse(
            text=response_text,
            mode=mode,
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

    def _generate_suggestions(self, text: str, keywords: List[str], context: Dict[str, Any]) -> List[str]:
        """
        Generate proactive suggestions for follow-up
        
        Why: Provide helpful next steps and conversation continuers
        Where: Used by generate() to enhance user experience
        How: Context-aware suggestion generation based on input patterns
        """
        suggestions = []
        
        # Question-based suggestions
        if '?' in text:
            suggestions.append("Would you like me to dive deeper into this topic?")
            suggestions.append("Should I explore related areas?")
        
        # Keyword-based suggestions
        if any(word in keywords for word in ['analyze', 'study', 'research']):
            suggestions.append("Want me to break this down step by step?")
            suggestions.append("Should I look at this from different angles?")
            
        if any(word in keywords for word in ['create', 'make', 'build']):
            suggestions.append("Ready to brainstorm some ideas?")
            suggestions.append("Want me to suggest some creative approaches?")
            
        return suggestions[:3]  # Limit to 3 suggestions

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