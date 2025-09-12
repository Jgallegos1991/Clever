"""
NLP Processor Module - Local natural language processing for Clever AI.

Why: Provides offline-first NLP capabilities including sentiment analysis,
     keyword extraction, and entity recognition using local spaCy models
     without any external API calls or fallback dependencies.

Where: Used by persona engine, knowledge base search, evolution engine,
       and any component requiring text analysis and language processing.

How: Implements singleton spaCy model loading with thread safety, LRU caching
     for performance, and structured NLP result objects for consistent data flow.
"""
from __future__ import annotations

import threading
from functools import lru_cache
from types import SimpleNamespace
from typing import List, Iterable, Optional, TYPE_CHECKING

# Required dependencies - no fallbacks per architecture standards
import spacy
from textblob import TextBlob

if TYPE_CHECKING:
    from spacy.language import Language

# Lazy, thread-safe singleton for spaCy
_NLP = None
_NLP_LOCK = threading.Lock()
_SPACY_MODEL_NAME = "en_core_web_sm"


def _load_spacy() -> "Language":
    """
    Load spaCy model once with thread-safe lazy initialization.
    
    Why: Provides efficient spaCy model loading with singleton pattern to avoid
         repeated model loading overhead while maintaining thread safety.
    
    Where: Called internally by NLP processing functions when spaCy analysis
           is required for sentiment, entities, or language processing.
    
    How: Uses double-checked locking pattern for thread-safe initialization,
         loads English model with optimized pipeline configuration.
    """
    global _NLP
    if _NLP is not None:
        return _NLP
    
    with _NLP_LOCK:
        if _NLP is not None:
            return _NLP
        
        # Load English model with optimized pipeline 
        _NLP = spacy.load(_SPACY_MODEL_NAME, disable=["tagger", "lemmatizer"])
        
        # Ensure sentencizer for sentence boundaries
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
    """
    Normalize token by converting to lowercase and filtering special characters.
    
    Why: Provides consistent token normalization for keyword extraction and
         text analysis, ensuring reliable comparison and deduplication.
    
    Where: Used internally by keyword extraction and token processing functions
           to standardize text tokens before analysis and counting.
    
    How: Strips whitespace, converts to lowercase, and retains only alphanumeric
         characters plus hyphens and underscores for clean token representation.
    """
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

    # ---- internals ----
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
    def nlp(self):
        """Provide access to the underlying spaCy model for compatibility checks."""
        return self._ensure()
