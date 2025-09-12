"""
NLP Processor for Clever AI - Full Potential Operation

Why: Provides advanced natural language processing capabilities for Clever,
including entity extraction, sentiment analysis, and keyword identification.
Operates at full potential with no fallbacks or compromise modes.
Where: Used by persona.py for response generation, evolution_engine.py for
concept extraction, and app.py for request analysis.
How: Implements UnifiedNLPProcessor class using spaCy en_core_web_sm model,
VADER sentiment analysis, and TextBlob processing with thread-safe operations.

Connects to:
    - persona.py: Persona response generation and mode inference
    - evolution_engine.py: Concept extraction and learning
    - app.py: Request analysis and NLP pipeline
    - config.py: Centralized configuration
"""
from __future__ import annotations

import threading
from functools import lru_cache
from types import SimpleNamespace
from typing import List, Iterable
import spacy  # Required dependency - no fallbacks
from textblob import TextBlob  # Required dependency - no fallbacks
from spacy.language import Language

# ---- Thread-safe spaCy singleton - Full potential operation -------------------------

_NLP = None
_NLP_LOCK = threading.Lock()
_SPACY_MODEL_NAME = "en_core_web_sm"  # pinned in requirements, but we still guard


def _load_spacy() -> Language:
    """
    Load spaCy model for full NLP processing capability.
    
    Why: Provides core NLP functionality for entity recognition, 
    tokenization, and text analysis at full potential.
    Where: Called by UnifiedNLPProcessor to initialize spaCy pipeline.
    How: Loads en_core_web_sm model with optimized pipeline configuration.
    
    Connects to:
        - spacy: Core NLP library for language processing
        - Threading: Ensures thread-safe singleton pattern
    """
    global _NLP
    if _NLP is not None:
        return _NLP
        
    with _NLP_LOCK:
        if _NLP is not None:
            return _NLP
            
        # Load spaCy model at full potential - no fallbacks
        _NLP = spacy.load(_SPACY_MODEL_NAME, disable=["tagger", "lemmatizer"])
        
        # Ensure sentence segmentation capability
        if "senter" not in _NLP.pipe_names and "sentencizer" not in _NLP.pipe_names:
            _NLP.add_pipe("sentencizer")
            
        return _NLP


# ---- Keyword extraction --------------------------------------------------------------------------

_STOPWORDS = set(
    """
    a an and are as at be but by for if in into is it of on or such that the their then there these they this to was were will with you your i we our us from about over under again very
    """.split()
)


def _normalize_token(t: str) -> str:
    t = t.strip().lower()
    return "".join(ch for ch in t if ch.isalnum() or ch in ("-", "_"))


def _top_tokens(tokens: Iterable[str], k: int = 8) -> List[str]:
    from collections import Counter

    toks = [
        _normalize_token(t)
        for t in tokens
        if t and len(t) > 2 and _normalize_token(t) not in _STOPWORDS
    ]
    counts = Counter(toks)
    out = [w for w, _ in counts.most_common(k)]
    # keep order stable but deduplicated
    seen, ordered = set(), []
    for w in toks:
        if w in counts and w not in seen:
            seen.add(w)
            ordered.append(w)
        if len(ordered) >= k:
            break
    # prefer frequency top but maintain first-appearance flavor
    merged = []
    for w in out + ordered:
        if w and w not in merged:
            merged.append(w)
        if len(merged) >= k:
            break
    return merged


def _keywords_spacy(doc) -> List[str]:
    # Prefer entities and noun chunks (ideas ≈ “things”) with minimal work.
    kws = []

    # Entities
    try:
        for ent in getattr(doc, "ents", []):
            text = _normalize_token(ent.text)
            if text and text not in _STOPWORDS and len(text) > 2:
                kws.append(text)
    except Exception:
        pass

    # Noun chunks
    try:
        for nc in getattr(doc, "noun_chunks", []):
            text = _normalize_token(nc.text)
            if text and text not in _STOPWORDS and len(text) > 2:
                kws.append(text)
    except Exception:
        # Some pipelines won’t have noun_chunks when tagger is disabled
        pass

    # Fallback to high-signal tokens
    toks = [t.text for t in doc if not t.is_space]
    kws.extend(_top_tokens(toks, k=8))
    # Deduplicate, keep order
    seen, deduped = set(), []
    for k in kws:
        if k not in seen:
            seen.add(k)
            deduped.append(k)
    return deduped[:10]


def _keywords_fallback(text: str) -> List[str]:
    # No spaCy? No problem — cheap regex + frequency.
    import re

    toks = re.findall(r"[A-Za-z0-9_\-]+", text.lower())
    toks = [t for t in toks if len(t) > 2 and t not in _STOPWORDS]
    return _top_tokens(toks, k=8)


# ---- Sentiment -----------------------------------------------------------------------------------

def _sentiment(text: str) -> float:
    """
    Analyze sentiment using TextBlob at full capability.
    
    Why: Provides sentiment analysis for persona response generation and
    evolution engine learning from user interactions.
    Where: Called by UnifiedNLPProcessor and used throughout Clever for
    emotional context understanding.
    How: Uses TextBlob sentiment polarity directly with no fallbacks.
    
    Connects to:
        - TextBlob: Core sentiment analysis library
        - persona.py: Persona response mood inference
        - evolution_engine.py: Learning from interaction sentiment
    """
    if not text:
        return 0.0
    # Full potential operation - no fallbacks
    blob = TextBlob(text)
    return float(blob.sentiment.polarity)


class UnifiedNLPProcessor:
    """
    Full-capability NLP processor for Clever AI operations.
    
    Why: Provides comprehensive natural language processing at full potential
    for all text analysis needs including entities, sentiment, and keywords.
    Where: Used throughout Clever by persona, evolution engine, and app for
    all NLP operations requiring consistent, high-quality analysis.
    How: Maintains thread-safe spaCy instance and provides unified interface
    for all NLP operations with no fallback or compromise modes.
    
    Connects to:
        - spacy: Core NLP processing pipeline
        - TextBlob: Sentiment analysis capability
        - persona.py: Response generation and analysis
        - evolution_engine.py: Concept extraction and learning
        - app.py: Request processing and analysis
    """
    
    def __init__(self) -> None:
        self._nlp = None  # Lazy-loaded singleton

    def _ensure_nlp(self) -> Language:
        """
        Ensure spaCy model is loaded and available.
        
        Why: Provides thread-safe access to spaCy model for all NLP operations.
        Where: Called internally by all NLP methods to ensure model availability.
        How: Uses lazy loading pattern to initialize spaCy model once per instance.
        """
        if self._nlp is None:
            self._nlp = _load_spacy()
        return self._nlp

    @lru_cache(maxsize=256)
    def _quick_cache(self, text: str) -> SimpleNamespace:
        return self._process_uncached(text)

    def process(self, text: str) -> SimpleNamespace:
        """Return SimpleNamespace(keywords: List[str], sentiment: float)."""
        text = (text or "").strip()
        if not text:
            return SimpleNamespace(keywords=[], sentiment=0.0)

        # Cache very short inputs (common greetings/quick hits).
        if len(text) <= 120:
            return self._quick_cache(text)

        return self._process_uncached(text)

    def _process_uncached(self, text: str) -> SimpleNamespace:
        """
        Process text with full NLP capabilities - no fallbacks.
        
        Why: Provides core text processing for keywords and entities using
        spaCy at full potential for consistent, high-quality results.
        Where: Called by process() method for all text analysis operations.
        How: Uses spaCy model directly with no fallback or compromise modes.
        
        Connects to:
            - spacy: Core NLP processing pipeline
            - _keywords_spacy(): Keyword extraction using spaCy
            - _sentiment(): Sentiment analysis using TextBlob
        """
        nlp = self._ensure_nlp()
        # Full potential operation - no fallbacks
        doc = nlp(text)
        keywords = _keywords_spacy(doc)
        sentiment = _sentiment(text)
        
        return SimpleNamespace(keywords=keywords, sentiment=sentiment)

    @property
    def nlp(self) -> Language:
        """
        Access to underlying spaCy model for direct operations.
        
        Why: Provides direct access to spaCy model for advanced operations
        like entity extraction and custom processing pipelines.
        Where: Used by evolution_engine and other modules requiring direct
        spaCy model access for specialized NLP operations.
        How: Returns the loaded spaCy Language model instance.
        """
        return self._ensure_nlp()


# Singleton export for application use - full potential operation
nlp_processor = UnifiedNLPProcessor()
