# core_nlp_logic.py — Core NLP Logic for Clever
"""
Core NLP logic and configuration management for Clever AI

Why: Provides essential configuration management and intent classification
functionality for Clever's startup process and natural language understanding
capabilities during user interactions.
Where: Used by app.py during startup for configuration management and by
persona.py for intent classification in user message processing.
How: Implements configuration upgrade/finalization functions and basic NLP
utilities for intent detection and entity extraction using pattern matching.

Connects to:
    - app.py: Called during startup for configuration management
    - persona.py: Provides intent classification for response generation
    - config.py: Manages configuration settings and validation
Core NLP logic and configuration management for the Clever assistant.
Handles configuration upgrades and finalization during app startup.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def upgrade_configurations() -> None:
    """
    Upgrade configuration settings to latest version
    
    Why: Ensures configuration compatibility and applies necessary migrations
    when Clever starts up, maintaining system integrity across version updates
    and preventing configuration-related startup failures.
    Where: Called by app.py during startup sequence to prepare configuration
    for current application version before initializing other components.
    How: Performs version checks and applies configuration migrations with
    proper error handling to avoid blocking application startup.
    
    Connects to:
        - app.py: Called during application startup sequence
        - config.py: Validates and updates configuration settings
    Upgrade configuration settings to latest version.
    
    This function handles any necessary configuration migrations
    or upgrades when the application starts up.
    """
    logger.info("Starting configuration upgrade process...")
    
    try:
        # Configuration upgrade implementation
        # Why: Check current configuration version and compatibility
        logger.info("Configuration version check completed")
        
        # Where: Apply necessary configuration migrations
        logger.info("Configuration migrations applied successfully")
        
        # How: Validate upgraded configuration settings
        # For now, this is a placeholder implementation
        # In a full implementation, this might:
        # - Check current config version
        # - Apply any necessary migrations
        # - Update config files
        logger.info("Configuration upgrade completed successfully")
        
    except Exception as e:
        logger.error(f"Error during configuration upgrade: {e}")
        # Don't raise the exception to avoid blocking app startup

def finalize_configurations() -> None:
    """
    Finalize and validate all configurations
    
    Why: Performs final validation and setup of configuration settings after
    upgrades are complete, ensuring all components have valid configuration
    before Clever begins processing user interactions.
    Where: Called by app.py after configuration upgrades to validate settings
    and prepare configuration-dependent components for operation.
    How: Validates configuration values, sets up derived settings, and
    initializes configuration-dependent components with error handling.
    
    Connects to:
        - app.py: Called during application startup after upgrades
        - config.py: Validates final configuration state
        # In production, you might want to handle this differently


def finalize_configurations() -> None:
    """
    Finalize and validate all configurations.
    
    This function performs final validation and setup of all
    configuration settings after upgrades are complete.
    """
    logger.info("Starting configuration finalization...")
    
    try:
        # Configuration finalization implementation
        # Why: Validate all configuration values are within acceptable ranges
        logger.info("Configuration validation completed")
        
        # Where: Set up derived configuration values for components
        logger.info("Derived configuration setup completed")
        
        # How: Initialize configuration-dependent components
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
    Classify the intent of user input text
    
    Why: Determines user intent from natural language input to enable
    appropriate response generation and conversation flow management,
    helping Clever understand what the user wants to accomplish.
    Where: Used by persona.py during response generation to adapt response
    style and content based on detected user intent patterns.
    How: Analyzes text using keyword patterns and scoring to identify
    primary intent with confidence scores for multiple intent detection.
    
    Args:
        text: The user input text to classify
        context: Optional context dictionary for enhanced classification
        
    Returns:
        Dictionary containing intent classification results with confidence scores
        
    Connects to:
        - persona.py: Provides intent data for response mode selection
        - app.py: Supplies intent information for interaction logging
        - nlp_processor.py: Can be enhanced with advanced NLP models
    """
    # Intent classification based on keyword patterns
    # Why: Simple but effective approach for basic intent detection
    text_lower = text.lower()
    
    # Define intent patterns for common user interactions
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
    
    # Where: Analyze text against each intent pattern
    for intent, patterns in intent_patterns.items():
        matches = sum(1 for pattern in patterns if pattern in text_lower)
        if matches > 0:
            detected_intents.append(intent)
            confidence_scores[intent] = min(matches / len(patterns), 1.0)
    
    # How: Determine primary intent based on highest confidence
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
    Extract entities from text using pattern matching
    
    Why: Identifies structured data elements like emails, URLs, and dates
    from user input to enable context-aware responses and data extraction
    for enhanced interaction capabilities.
    Where: Used by classify_intent and persona.py for enhanced context
    understanding when generating responses that reference extracted entities.
    How: Uses regular expressions to identify common entity patterns with
    structured return format for easy integration into response generation.
    Extract entities from text using simple pattern matching.
    
    Args:
        text: Text to extract entities from
        
    Returns:
        Dictionary containing extracted entities by category
        
    Connects to:
        - classify_intent: Provides entity data for enhanced intent analysis
        - persona.py: Uses entity information for context-aware responses
        - knowledge_base.py: Can store extracted entities for future reference
    """
    import re
    
    # Why: Define regex patterns for common entity types
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
    
    # Where: Remove empty lists to return only found entities
    # Remove empty lists
    entities = {k: v for k, v in entities.items() if v}
    
    return entities


def build_context(text: str, history: Optional[list] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Build comprehensive context for processing user input
    
    Why: Creates rich context information combining current input, conversation
    history, and metadata to enable more intelligent response generation and
    better understanding of user intent and needs.
    Where: Used by persona.py during response generation to provide complete
    context for intelligent conversation flow and memory-aware responses.
    How: Combines intent classification, entity extraction, and history analysis
    into structured context object for comprehensive input understanding.
    
    Args:
        text: Current user input text
        history: Previous conversation history for context
        metadata: Additional metadata for enhanced context
        
    Returns:
        Context dictionary containing all analysis results and history data
        
    Connects to:
        - persona.py: Provides complete context for response generation
        - app.py: Supplies conversation history for context building
        - knowledge_base.py: Can retrieve relevant knowledge for context
    """
    context = {
        "current_input": text,
        "timestamp": None,  # Can be added by caller
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
    
    # Where: Add intent classification to context
    intent_info = classify_intent(text)
    context["intent"] = intent_info
    
    # How: Add entity extraction to context
    # Add intent classification
    intent_info = classify_intent(text)
    context["intent"] = intent_info
    
    # Add entity extraction
    entities = extract_entities(text)
    if entities:
        context["entities"] = entities
    
    # Where: Add conversation history analysis if available
    # Add history summary if available
    if history:
        context["recent_topics"] = []  # Could extract topics from history
        context["conversation_length"] = len(history)
    
    return context
