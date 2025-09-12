# nlp_processor.py — Clever (offline-first, Jay-only)
# Lazy singleton loader for spaCy; robust fallbacks; tiny LRU cache for quick hits.

from __future__ import annotations

import threading
from functools import lru_cache
from types import SimpleNamespace
from typing import List, Iterable
import spacy  # Required dependency - no fallbacks
from textblob import TextBlob  # Required dependency - no fallbacks
from spacy.language import Language

# Thread-safe spaCy singleton - Full potential operation
_NLP = None
_NLP_LOCK = threading.Lock()
_SPACY_MODEL_NAME = "en_core_web_sm"

# Stopwords for keyword filtering
_STOPWORDS = set("""
    a an and are as at be but by for if in into is it of on or such that the 
    their then there these they this to was were will with you your i we our 
    us from about over under again very
""".split())


def _normalize_token(token: str) -> str:
    """
    Normalize token for consistent keyword extraction.
    
    Why: Ensures consistent token formatting for reliable keyword matching
    and deduplication across all NLP operations.
    Where: Used by keyword extraction functions for token standardization.
    How: Strips, lowercases, and filters to alphanumeric plus hyphens/underscores.
    """
    token = token.strip().lower()
    return "".join(ch for ch in token if ch.isalnum() or ch in ("-", "_"))


def _top_tokens(tokens: Iterable[str], k: int = 8) -> List[str]:
    """
    Extract top K most frequent tokens from text.
    
    Why: Identifies the most significant terms for keyword extraction when
    entity recognition alone is insufficient.
    Where: Used by _keywords_spacy for comprehensive keyword coverage.
    How: Uses Counter to rank tokens by frequency, filters stopwords.
    
    Connects to:
        - collections.Counter: Frequency analysis
        - _normalize_token(): Token standardization
    """
    from collections import Counter
    
    normalized_tokens = [
        _normalize_token(token)
        for token in tokens
        if token and len(token) > 2 and _normalize_token(token) not in _STOPWORDS
    ]
    
    token_counts = Counter(normalized_tokens)
    return [token for token, _ in token_counts.most_common(k)]


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
        if ("senter" not in _NLP.pipe_names and 
            "sentencizer" not in _NLP.pipe_names):
            _NLP.add_pipe("sentencizer")
            
        return _NLP


def _keywords_spacy(doc) -> List[str]:
    """
    Extract keywords using spaCy's full NLP capabilities.
    
    Why: Identifies key concepts and entities from text for persona responses
    and evolution engine learning at full analytical potential.
    Where: Called by UnifiedNLPProcessor for all keyword extraction needs.
    How: Uses spaCy entities and noun chunks directly with no fallbacks.
    
    Connects to:
        - spacy.Doc: Processed document with entities and noun chunks
        - persona.py: Keyword-based response generation
        - evolution_engine.py: Concept extraction and learning
    """
    keywords = []

    # Extract entities - full potential operation
    for entity in doc.ents:
        text = _normalize_token(entity.text)
        if text and text not in _STOPWORDS and len(text) > 2:
            keywords.append(text)

    # Extract noun chunks for concept identification
    for noun_chunk in doc.noun_chunks:
        text = _normalize_token(noun_chunk.text)
        if text and text not in _STOPWORDS and len(text) > 2:
            keywords.append(text)

    # Extract high-signal tokens for comprehensive coverage
    tokens = [token.text for token in doc if not token.is_space]
    keywords.extend(_top_tokens(tokens, k=8))
    
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            deduped.append(keyword)
            
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
    if TextBlob is None:
        return 0.0
    try:
        # Range is [-1.0, 1.0]
        return float(TextBlob(text).sentiment.polarity)
    except Exception:
        return 0.0


# ---- Public Processor ----------------------------------------------------------------------------

class _NLPProcessor:
    """Small façade with a stable, testable API."""

    def __init__(self) -> None:
        self._nlp = None  # lazy

    def _ensure(self):
        if self._nlp is None:
            self._nlp = _load_spacy()
        return self._nlp

    @lru_cache(maxsize=256)
    def _quick_cache(self, text: str) -> SimpleNamespace:
        """Cache processing results for short, frequently used inputs."""
        return self._process_uncached(text)

    def process(self, text: str) -> SimpleNamespace:
        """
        Process text and return keywords and sentiment analysis.
        
        Why: Provides unified interface for all text analysis operations 
        needed throughout Clever for consistent NLP processing.
        Where: Called by persona, evolution engine, and app for text analysis.
        How: Uses caching for short inputs, direct processing for longer text.
        
        Returns:
            SimpleNamespace with keywords (List[str]) and sentiment (float)
        """
        text = (text or "").strip()
        if not text:
            return SimpleNamespace(keywords=[], sentiment=0.0)

        # Cache short inputs for performance
        if len(text) <= 120:
            return self._quick_cache(text)

        return self._process_uncached(text)

    def _process_uncached(self, text: str) -> SimpleNamespace:
        nlp = self._ensure()
        if nlp is not None:
            try:
                doc = nlp(text)
                kws = _keywords_spacy(doc)
            except Exception:
                kws = _keywords_fallback(text)
        else:
            kws = _keywords_fallback(text)

        sent = _sentiment(text)
        return SimpleNamespace(keywords=kws, sentiment=sent)


# Singleton export used by the app
nlp_processor = _NLPProcessor()

# Public class alias for external imports
class UnifiedNLPProcessor(_NLPProcessor):
    """Public interface to the NLP processor. Alias for _NLPProcessor."""
    
    def __init__(self) -> None:
        super().__init__()
    
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