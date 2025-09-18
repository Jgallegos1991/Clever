"""
Simple NLP Processor for Clever AI

Why: Provides basic natural language processing without complex dependencies
Where: Used by persona.py and other modules for text analysis
How: Simple rule-based processing following offline requirements

Connects to:
    - persona.py: Text analysis for response generation
    - evolution_engine.py: Text processing for learning
"""
import re
from typing import List, Dict, Any, Optional
from collections import Counter


class SimpleNLPProcessor:
    """
    Simple NLP processor for offline operation
    
    Why: Provide text analysis without external dependencies
    Where: Core component for all text processing needs
    How: Rule-based analysis with basic pattern matching
    """
    
    def __init__(self):
        """
        Initialize simple NLP processor
        
        Why: Set up basic text processing capabilities
        Where: Called once during system initialization
        How: Define stopwords and basic processing rules
        """
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 
            'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 
            'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text and extract basic information
        
        Why: Provide comprehensive text analysis for system use
        Where: Main entry point for all text processing
        How: Combine multiple analysis methods into single result
        
        Connects to:
            - persona.py: Response generation analysis
            - evolution_engine.py: Learning and context extraction
        """
        return {
            'keywords': self.extract_keywords(text),
            'sentiment': self.analyze_sentiment(text),
            'entities': self.extract_entities(text),
            'word_count': len(text.split()),
            'char_count': len(text)
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text
        
        Why: Identify important concepts for contextual responses
        Where: Used by persona engine for response customization
        How: Remove stopwords and find significant terms
        """
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in self.stopwords and len(word) > 2]
        
        # Count frequency and return most common
        word_freq = Counter(keywords)
        return [word for word, count in word_freq.most_common(10)]
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze text sentiment
        
        Why: Understand emotional tone for appropriate responses
        Where: Used by persona engine for tone matching
        How: Simple rule-based sentiment classification
        """
        positive_words = {
            'good', 'great', 'awesome', 'excellent', 'amazing', 'wonderful',
            'fantastic', 'love', 'like', 'happy', 'excited', 'pleased',
            'joy', 'perfect', 'brilliant', 'outstanding', 'superb'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike',
            'sad', 'angry', 'frustrated', 'annoyed', 'disappointed',
            'worried', 'upset', 'stressed', 'concerned', 'troubled'
        }
        
        words = set(re.findall(r'\b\w+\b', text.lower()))
        
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def extract_entities(self, text: str) -> List[str]:
        """
        Extract basic entities from text
        
        Why: Identify important names and concepts
        Where: Used for context building and response personalization
        How: Simple pattern matching for common entity types
        """
        entities = []
        
        # Find capitalized words (potential proper nouns)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities.extend(proper_nouns)
        
        # Find numbers
        numbers = re.findall(r'\b\d+\b', text)
        entities.extend(numbers)
        
        return list(set(entities))  # Remove duplicates
    
    def tokenize(self, text: str) -> List[str]:
        """
        Basic text tokenization
        
        Why: Split text into individual words for analysis
        Where: Used by other processing methods
        How: Simple regex-based word extraction
        """
        return re.findall(r'\b\w+\b', text.lower())
    
    def get_word_frequency(self, text: str) -> Dict[str, int]:
        """
        Get word frequency distribution
        
        Why: Understand text composition and emphasis
        Where: Used for content analysis and keyword weighting
        How: Count occurrences of each word
        """
        words = self.tokenize(text)
        return dict(Counter(words))
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        Alias for process_text for backward compatibility
        
        Why: Some modules expect 'process' method name
        Where: Used by enhanced_conversation_engine and other modules
        How: Delegates to process_text method
        """
        return self.process_text(text)


# Global processor instance
nlp_processor = SimpleNLPProcessor()