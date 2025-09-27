"""
Simple Persona Engine for Clever AI

Why: Provides basic AI personality and response generation
Where: Used by app.py for chat responses
How: Simple response generation with personality traits

Connects to:
    - app.py: Main interface for chat response generation
    - database.py: May log interactions (if implemented)
    - user_config.py: User personalization settings
"""

from dataclasses import dataclass

@dataclass
class PersonaResponse:
    """
    Response from Clever's persona engine
    
    Why: Standardizes AI response format with metadata
    Where: Returned by PersonaEngine.generate()
    How: Simple dataclass with text, mode, and sentiment
    """
    text: str
    mode: str = "Auto"
    sentiment: str = "neutral"
    proactive_suggestions: Optional[list] = None

class PersonaEngine:
    """
    Simple Clever AI Persona Engine
    
    Why: Generates responses with Clever's personality
    Where: Core AI interaction component
    How: Rule-based response generation with wit and empathy
    """
    
    def __init__(self, name: str = "Clever", user_name: str = "User"):
        """
        Initialize the persona engine
        
        Why: Sets up Clever's personality and user context
        Where: Called by app.py during startup
        How: Stores name and user context for personalization
        """
        self.name = name
        self.user_name = user_name
        
    def generate(self, user_input: str, mode: str = "Auto") -> PersonaResponse:
        """
        Generate a response from Clever
        
        Why: Main interface for AI response generation
        Where: Called by app.py chat endpoint
        How: Analyzes input and generates contextual response
        
        Args:
            user_input: User's message
            mode: Response mode (Auto, Creative, etc.)
            
        Returns:
            PersonaResponse with generated text and metadata
        """
        user_input = user_input.strip().lower()
        
        # Simple response logic
        if any(word in user_input for word in ['hello', 'hi', 'hey']):
            response_text = f"Hello {self.user_name}! I'm Clever, your AI companion. What can I help you explore today?"
            
        elif any(word in user_input for word in ['how', 'what', 'why', 'when', 'where']):
            response_text = f"Great question! Let me think about that... {user_input.capitalize()}? That's something I'd love to explore with you."
            
        elif any(word in user_input for word in ['help', 'assist', 'support']):
            response_text = "I'm here to help! I can chat, brainstorm ideas, answer questions, or just be a thoughtful companion. What would you like to work on?"
            
        elif any(word in user_input for word in ['creative', 'idea', 'imagine', 'dream']):
            response_text = "Now we're talking! I love creative exploration. Let's dive into the realm of possibilities together!"
            mode = "Creative"
            
        else:
            response_text = f"Interesting point about '{user_input}'. Tell me more about what you're thinking - I'm genuinely curious about your perspective."
        
        return PersonaResponse(
            text=response_text,
            mode=mode,
            sentiment="positive"
        )