# core_nlp_logic.py — Core NLP Logic for Clever
"""
Core NLP logic and configuration management for the Clever assistant.
Handles configuration upgrades and finalization during app startup.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def upgrade_configurations() -> None:
    """
    Upgrade configuration settings to latest version.
    
    This function handles any necessary configuration migrations
    or upgrades when the application starts up.
    """
    logger.info("Starting configuration upgrade process...")
    
    try:
        # For now, this is a placeholder implementation
        # In a full implementation, this might:
        # - Check current config version
        # - Apply any necessary migrations
        # - Update config files
        logger.info("Configuration upgrade completed successfully")
        
    except Exception as e:
        logger.error(f"Error during configuration upgrade: {e}")
        # Don't raise the exception to avoid blocking app startup
        # In production, you might want to handle this differently


def finalize_configurations() -> None:
    """
    Finalize and validate all configurations.
    
    This function performs final validation and setup of all
    configuration settings after upgrades are complete.
    """
    logger.info("Starting configuration finalization...")
    
    try:
        # For now, this is a placeholder implementation
        # In a full implementation, this might:
        # - Validate all configuration values
        # - Set up any derived configuration
        # - Initialize configuration-dependent components
        logger.info("Configuration finalization completed successfully")
        
    except Exception as e:
        logger.error(f"Error during configuration finalization: {e}")
        # Don't raise the exception to avoid blocking app startup


def classify_intent(text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Classify the intent of user input text.
    
    Args:
        text: The user input text to classify
        context: Optional context dictionary for better classification
        
    Returns:
        Dictionary containing intent classification results
    """
    # Simple intent classification based on keywords
    # This is a basic implementation - could be enhanced with ML models
    
    text_lower = text.lower()
    
    # Define intent patterns
    intent_patterns = {
        "question": ["what", "how", "why", "when", "where", "who", "?"],
        "request": ["please", "can you", "could you", "would you", "help"],
        "command": ["do", "make", "create", "run", "execute", "start", "stop"],
        "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
        "goodbye": ["bye", "goodbye", "see you", "farewell"],
        "affirmation": ["yes", "ok", "okay", "sure", "absolutely"],
        "negation": ["no", "nope", "not", "don't", "won't", "can't"],
    }
    
    detected_intents = []
    confidence_scores = {}
    
    for intent, patterns in intent_patterns.items():
        matches = sum(1 for pattern in patterns if pattern in text_lower)
        if matches > 0:
            detected_intents.append(intent)
            confidence_scores[intent] = min(matches / len(patterns), 1.0)
    
    # Determine primary intent (highest confidence)
    primary_intent = "unknown"
    if detected_intents:
        primary_intent = max(detected_intents, key=lambda x: confidence_scores[x])
    
    return {
        "primary_intent": primary_intent,
        "all_intents": detected_intents,
        "confidence_scores": confidence_scores,
        "text_length": len(text),
        "word_count": len(text.split())
    }


def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract entities from text using simple pattern matching.
    
    Args:
        text: Text to extract entities from
        
    Returns:
        Dictionary containing extracted entities
    """
    import re
    
    entities = {
        "emails": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
        "urls": re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text),
        "phone_numbers": re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text),
        "dates": re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text),
        "numbers": re.findall(r'\b\d+\.?\d*\b', text),
    }
    
    # Remove empty lists
    entities = {k: v for k, v in entities.items() if v}
    
    return entities


def build_context(text: str, history: Optional[list] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Build context for processing user input.
    
    Args:
        text: Current user input
        history: Previous conversation history
        metadata: Additional metadata
        
    Returns:
        Context dictionary for processing
    """
    context = {
        "current_input": text,
        "timestamp": None,  # Could be added
        "session_length": len(history) if history else 0,
        "metadata": metadata or {}
    }
    
    # Add intent classification
    intent_info = classify_intent(text)
    context["intent"] = intent_info
    
    # Add entity extraction
    entities = extract_entities(text)
    if entities:
        context["entities"] = entities
    
    # Add history summary if available
    if history:
        context["recent_topics"] = []  # Could extract topics from history
        context["conversation_length"] = len(history)
    
    return context
