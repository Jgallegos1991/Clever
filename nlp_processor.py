"""
NLP Processor for Clever AI

Why: Provides natural language processing for Clever's genius-level text understanding
Where: Used by persona.py and other modules for advanced text analysis
How: Rule-based processing with optional advanced capabilities when available

Core Purpose:
    - Text analysis and feature extraction without external APIs
    - Sentiment detection and keyword extraction for context understanding
    - Entity recognition and noise detection for intelligent responses
    - Provides foundation for all text understanding in Clever

Connects to:
    - persona.py:
        - `generate()` -> `get_nlp_processor()`: Lazily initializes the NLP processor.
        - `generate()` -> `process_text()`: The core method called to analyze user input for keywords, sentiment, entities, and other metrics, which then drives the entire response generation logic.
    - memory_engine.py: (Indirectly) The `MemoryContext` object, which is created in `persona.py` using the output from `process_text()`, is passed to `memory_engine.store_interaction()`. This is how NLP analysis results are persisted.
    - file_ingestor.py:
        - `ingest_file()` -> `nlp_processor.process_text()`: Used to extract keywords and entities from ingested text files to enrich the knowledge base.
    - system_validator.py:
        - `_validate_nlp_capabilities()` -> `nlp_processor.process()`: The validator calls the processor to ensure it is functional and returning the expected analysis structure.

Processing Flow:
    1. Text input → tokenization → stopword removal
    2. Feature extraction (keywords, entities, sentiment)
    3. Noise/gibberish detection for quality control
    4. Advanced features (when available): NER, readability, topic vectors
    5. Aggregated analysis dict returned to calling module

Key Methods:
    - process_text(): Main entry point returning comprehensive analysis
    - extract_keywords(): Critical concepts for context
    - analyze_sentiment(): Emotional tone detection
    - extract_entities(): Names, numbers, and proper nouns
    - _noise_metrics(): Typo/gibberish detection for clarification

Design Principles:
    - Confident-first (Clever always responds intelligently)
    - Offline-first (no external dependencies required)
    - Extensible (new features enhance existing capabilities)
    - Performance-conscious (lightweight operations)
"""

import re
from typing import List, Dict, Any, Optional
from collections import Counter

try:  # Optional heavy libs – never required
    import spacy  # type: ignore
    _SPACY_AVAILABLE = True
except (ImportError, ModuleNotFoundError):  # pragma: no cover - environment dependent
    _SPACY_AVAILABLE = False

try:  # TextBlob sentiment (polarity / subjectivity)
    from textblob import TextBlob  # type: ignore
    _TEXTBLOB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    _TEXTBLOB_AVAILABLE = False

try:  # NLTK VADER (already in requirements)
    from nltk.sentiment import SentimentIntensityAnalyzer  # type: ignore
    # Test if VADER lexicon is available
    _ = SentimentIntensityAnalyzer()
    _VADER_AVAILABLE = True
except (ImportError, ModuleNotFoundError, LookupError):  # pragma: no cover
    _VADER_AVAILABLE = False


def _safe_lower(text: str) -> str:
    """Internal helper to guard against non-string input."""
    return text.lower() if isinstance(text, str) else ""


class SimpleNLPProcessor:
    """
    Simple NLP processor for offline operation.
    
    Why: Provide text analysis without external dependencies
    Where: Core component for all text processing needs
    How: Rule-based analysis with basic pattern matching
    """
    
    # Noise detection thresholds - configurable for easier tuning
    NOISE_TYPO_THRESHOLD = 0.8
    NOISE_SMASH_THRESHOLD = 0.6
    NOISE_REPEAT_THRESHOLD = 3
    NOISE_ENTROPY_THRESHOLD = 0.15
    
    # Common English stopwords
    STOPWORDS = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'shall', 'to', 'of', 'in',
        'for', 'on', 'with', 'at', 'by', 'from', 'about', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out',
        'off', 'over', 'under', 'again', 'further', 'then', 'once', 'and',
        'but', 'or', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
        'too', 'very', 'just', 'now', 'i', 'you', 'he', 'she', 'it', 'we',
        'they', 'me', 'him', 'her', 'us', 'them',
    }
    
    def __init__(self):
        """
        Initialize basic text processing capabilities.
        
        Why: Set up basic text processing capabilities
        Where: Called once during system initialization
        How: Define stopwords and basic processing rules
        
        Connects to:
            - persona.py: Response generation analysis
            - evolution_engine.py: Learning and context extraction
        """
        self.stopwords = self.STOPWORDS
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text and extract features.
        
        Why: Main entry point for text analysis
        Where: Called by persona.py, evolution_engine.py, memory_engine.py, enhanced_conversation_engine.py
        How: Extracts keywords, sentiment, entities and metrics
        
        Args:
            text: The text string to process
            
        Returns:
            Dictionary containing extracted features including keywords,
            sentiment, entities, word count, character count, and noise metrics
        """
        # Compute base extraction
        keywords = self.extract_keywords(text)
        sentiment = self.analyze_sentiment(text)
        entities = self.extract_entities(text)
        word_count = len(text.split())
        char_count = len(text)
        noise_metrics = self._noise_metrics(text)
        return {
            'keywords': keywords,
            'sentiment': sentiment,
            'entities': entities,
            'word_count': word_count,
            'char_count': char_count,
            **noise_metrics
        }

    def process(self, text: str) -> Dict[str, Any]:  # Backward-compatible alias
        """Alias for process_text to support legacy callers.

        Why: Some higher-level engines (e.g., enhanced conversation engine)
        invoke `process`; adding an alias avoids widespread refactors while
        maintaining a single implementation source of truth.
        Where: Called by `enhanced_conversation_engine.py` during comprehensive
        analysis stages to obtain NLP features.
        How: Thin passthrough returning `process_text(text)` results; keeps
        external contract stable and future-proofs naming consistency.
        """
        return self.process_text(text)
    
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

    # ---------- Noise / gibberish detection helpers ----------
    def _noise_metrics(self, text: str) -> Dict[str, Any]:
        """Estimate noise characteristics (typos, gibberish, smash).

        Why: Persona needs to recognize when user input is accidental
        (keyboard smash) or heavily typo-laden to prompt clarification.
        Where: Included in analysis dict used by persona.generate.
        How: Heuristics: consonant run lengths, vowel ratio, non-dictionary
        token ratio, repeated char bursts, entropy approximation.

        Returns keys:
            - typo_ratio: float 0..1 approximate tokens likely misspelled
            - smash_score: float 0..1 intensity of random input patterns
            - needs_clarification: bool high noise composite flag
        """
        lowered = text.lower()
        tokens = re.findall(r"[a-zA-Z]+", lowered)
        if not tokens:
            return {"typo_ratio": 0.0, "smash_score": 0.0, "needs_clarification": False}
        # Simple english core set (small to stay offline/light) + technical terms
        core_vocab = {
            # Common English words  
            "the","and","that","this","you","for","with","have","are","but","not","can","your","from","what","about","just","like","time","need","want","make",
            # Clever-specific terms to prevent false typo detection
            "code","test","file","data","project","shape","shifting","capabilities","particles","clever","working","right","message","understand","trying","system","interface","holographic","particle","engine",
            # Additional common tech terms
            "python","javascript","html","css","json","api","server","client","function","method","class","object","array","variable","debug","error","syntax","config","settings","import","export","async","await","callback","event","handler","component","element","property","value","input","output","database","memory","storage","network","http","https","url","request","response","header","status","query","auth","login","session","cache","load","save","create","read","write","update","delete","search","filter","sort","map","validation","format","template","style","theme","color","background","text","font","button","menu","modal","notification","loading","progress","image","video","audio","upload","download","browser","window","document","element","attribute","content","layout","design","framework","library","module","package","version","dependency","installation","configuration","deployment","production","development","testing","optimization","performance","security","encryption","authentication","authorization","permission","access","control","user","admin","guest","public","private","local","remote","cloud","backup","restore","sync","migration","integration","automation","workflow","pipeline","monitoring","logging","analytics","metrics","reporting","dashboard","visualization","chart","graph","table","list","grid","form","field","label","placeholder","tooltip","dropdown","checkbox","radio","slider","toggle","tab","panel","section","header","footer","sidebar","navbar","breadcrumb","pagination","search","filter","sort","group","category","tag","priority","status","state","active","inactive","enabled","disabled","visible","hidden","selected","focused","hover","click","touch","drag","drop","resize","scroll","zoom","rotate","scale","transition","animation","mobile","tablet","desktop","responsive","adaptive","accessibility","usability","cross-browser","compatibility","progressive","enhancement","graceful","degradation"
        }
        misspelled = 0
        consonant_runs = 0
        long_repeats = 0
        total_chars = sum(len(t) for t in tokens)
        for t in tokens:
            if t not in core_vocab and len(t) > 3:
                # crude heuristic: lacks vowel or has improbable pattern
                if not re.search(r"[aeiou]", t) or re.search(r"[^aeiou]{5,}", t):
                    misspelled += 1
            # consonant run length measure
            cruns = re.findall(r"[^aeiou\W]{4,}", t)
            consonant_runs += sum(len(c) for c in cruns)
            # repeated char sequences
            if re.search(r"(.)\1{3,}", t):
                long_repeats += 1
        typo_ratio = misspelled / max(1, len(tokens))
        # Shannon-like entropy proxy: unique chars / length
        unique_chars = len(set(lowered))
        entropy_proxy = unique_chars / max(1, len(lowered))
        smash_score = min(1.0, 0.4*typo_ratio + 0.3*(consonant_runs/ max(1,total_chars)) + 0.3*(long_repeats / max(1,len(tokens))))
        # Relaxed thresholds - only flag truly garbled text, not technical terms or minor typos
        needs = (typo_ratio > self.NOISE_TYPO_THRESHOLD and smash_score > self.NOISE_SMASH_THRESHOLD) or (long_repeats >= self.NOISE_REPEAT_THRESHOLD) or (entropy_proxy < self.NOISE_ENTROPY_THRESHOLD)
        return {
            "typo_ratio": round(typo_ratio, 3),
            "smash_score": round(smash_score, 3),
            "needs_clarification": needs,
        }
    
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
        
        lowered = text.lower()
        words = set(re.findall(r'\b\w+\b', lowered))

        # Fast-path neutrality heuristics
        # Why: Short operational/procedural sentences ("processing continues without notable change")
        # should not be classified positive simply because of a single weak positive token like 'continues'.
        # Where: Shields persona tone selection in persona.generate from over-optimistic bias.
        # How: Detect absence of strong affect terms and presence of stability phrases → force neutral.
        stability_markers = {"continues", "without", "notable", "change", "standard", "baseline", "normal"}
        if words and not (words & positive_words) and not (words & negative_words) and (words & stability_markers):
            return "neutral"
        if words and len(words & positive_words) == 1 and not (words & negative_words) and len(words & stability_markers) >= 2:
            return "neutral"

        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))

        if positive_count > negative_count:
            return "positive"
        if negative_count > positive_count:
            return "negative"
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


class AdvancedNLPProcessor(SimpleNLPProcessor):
    """Advanced (still offline) NLP processor.

    Why: Provide richer semantic signal for the persona engine so responses can
    feel analytical, insightful, and *Einstein-level* without any external API.
    Where: Consumed by `persona.py` when available (graceful degradation to
    `SimpleNLPProcessor`). Integrated anywhere deeper text understanding is
    useful (e.g., evolution engine, future knowledge ranking).
    How: Layered capability detection (spaCy → TextBlob → VADER → rule-based).
    Extracts: keywords, entities (NER if spaCy), sentiment (hybrid), readability,
    question type, conceptual density, and generates a lightweight topic vector.

    Connects to:
        - persona.py: Supplies enriched analysis dict
        - evolution_engine.py: (potential future) richer interaction features
        - memory_engine.py: Can store enhanced semantic descriptors
    """

    def __init__(self):  # noqa: D401
        super().__init__()
        self._nlp = None
        if _SPACY_AVAILABLE:
            try:  # Load small English model if present; never downloads
                self._nlp = spacy.load("en_core_web_sm")  # pragma: no cover (env)
            except (OSError, IOError, ImportError):  # More specific exceptions for model loading
                self._nlp = None
        self._vader = None
        if _VADER_AVAILABLE:
            try:
                self._vader = SentimentIntensityAnalyzer()
            except (LookupError, OSError):  # Catch missing VADER lexicon data
                self._vader = None

    # ---------- Public API ----------
    def process_text(self, text: str) -> Dict[str, Any]:
        """Enhance base processing with deeper semantic layers.

        Returns extended dict while preserving base keys so existing code
        remains compatible.
        """
        base = super().process_text(text)
        doc = self._nlp(text) if self._nlp else None

        enriched: Dict[str, Any] = {
            **base,
            "entities": self._extract_entities_advanced(text, doc),
            "sentiment": self._hybrid_sentiment(text),
            "readability": self._readability(text),
            "question_type": self._question_type(text),
            "concept_density": self._concept_density(base["keywords"], text),
            "topic_vector": self._topic_vector(base["keywords"]),
        }
        return enriched

    # ---------- Enriched Feature Methods ----------
    def _extract_entities_advanced(self, text: str, doc: Optional[Any]) -> List[str]:
        if doc is not None:
            ents = {e.text for e in doc.ents if len(e.text) < 60}
        else:
            ents = set(super().extract_entities(text))
        # Add math / physics heuristic entities (Einstein vibe)
        lower = _safe_lower(text)
        for token in ["relativity", "quantum", "tensor", "entropy", "vector", "matrix"]:
            if token in lower:
                ents.add(token)
        return list(ents)

    def _hybrid_sentiment(self, text: str) -> str:
        """Hybrid sentiment cascade.

        Why: Improve robustness and analyzer friendliness (avoid static type
        complaints about attribute access) while keeping offline operation.
        Where: Used by process_text for enriched sentiment classification.
        How: Try VADER → guarded TextBlob access → fallback to base rule set.
        """
        # VADER first (fast + compound score)
        try:
            if self._vader:
                score = self._vader.polarity_scores(text)["compound"]
                if score >= 0.25:
                    return "positive"
                if score <= -0.25:
                    return "negative"
                return "neutral"
        except Exception:
            pass  # Silent fallback

        # TextBlob second — add attribute guards to appease static analysis
        if _TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                sentiment_obj = getattr(blob, 'sentiment', None)
                polarity = getattr(sentiment_obj, 'polarity', None) if sentiment_obj is not None else None
                if isinstance(polarity, (int, float)):
                    if polarity > 0.2:
                        return "positive"
                    if polarity < -0.2:
                        return "negative"
                    return "neutral"
            except (AttributeError, TypeError, ValueError):  # More specific TextBlob exceptions
                pass

        # Fallback to rule-based sentiment
        return super().analyze_sentiment(text)

    def _readability(self, text: str) -> Dict[str, float]:
        words = re.findall(r"\b\w+\b", text)
        if not words:
            return {"flesch_like": 0.0, "avg_word_len": 0.0}
        syllables = sum(self._estimate_syllables(w) for w in words)
        sentences = max(1, text.count(".") + text.count("?") + text.count("!"))
        words_count = len(words)
        # Simplified Flesch-like score (no external libs)
        flesch_like = 206.835 - 1.015 * (words_count / sentences) - 84.6 * (syllables / words_count)
        return {
            "flesch_like": round(flesch_like, 2),
            "avg_word_len": round(sum(len(w) for w in words) / words_count, 2),
        }

    def _question_type(self, text: str) -> str:
        lower = _safe_lower(text).strip()
        if not lower.endswith("?"):
            return "none"
        for w, label in [
            ("why", "why"), ("how", "how"), ("what", "what"), ("when", "when"),
            ("where", "where"), ("who", "who"), ("which", "which"), ("can", "can"),
        ]:
            if lower.startswith(w):
                return label
        return "generic"

    def _concept_density(self, keywords: List[str], text: str) -> float:
        words = re.findall(r"\b\w+\b", text)
        if not words:
            return 0.0
        unique_kw = len(set(keywords))
        return round(unique_kw / len(words), 3)

    def _topic_vector(self, keywords: List[str]) -> List[int]:
        # Deterministic lightweight vector (hash mod a small prime set)
        primes = [3, 5, 7, 11, 13]
        vec = [0] * len(primes)
        for kw in keywords:
            for i, p in enumerate(primes):
                vec[i] = (vec[i] + (hash(kw) % p)) % 97
        return vec

    # ---------- Helpers ----------
    def _estimate_syllables(self, word: str) -> int:
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_vowel = False
        for ch in word:
            is_vowel = ch in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        # Adjust for silent e
        if word.endswith('e') and count > 1:
            count -= 1
        return max(1, count)


def get_nlp_processor() -> SimpleNLPProcessor:
    """Factory returning the most capable available processor.

    Why: Central place for persona or other modules to obtain NLP features
    without duplicating capability detection.
    Where: Imported by persona.py (and future modules) to obtain analysis.
    How: Returns AdvancedNLPProcessor if optional libs load, else SimpleNLPProcessor.
    """
    try:
        return AdvancedNLPProcessor()
    except (ImportError, ModuleNotFoundError, OSError):  # Safety net – never break core flow
        return SimpleNLPProcessor()


# Global processor instance - wrapped in try-except to ensure module always loads
try:
    nlp_processor = get_nlp_processor()
except (ImportError, ModuleNotFoundError, OSError):
    # Fallback to simple processor if any error occurs during initialization
    nlp_processor = SimpleNLPProcessor()