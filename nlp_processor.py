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
from collections import Counter

# Enhanced English dictionary integration for comprehensive vocabulary understanding
try:
    from enhanced_nlp_dictionary import get_english_dictionary
    _ENHANCED_DICT_AVAILABLE = True
except ImportError:
    _ENHANCED_DICT_AVAILABLE = False

# Comprehensive academic knowledge engine for educational intelligence
try:
    from academic_knowledge_engine import get_academic_engine
    _ACADEMIC_ENGINE_AVAILABLE = True
except ImportError:
    _ACADEMIC_ENGINE_AVAILABLE = False

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
        'should', 'may', 'might', 'must', 'can', 'shall', 'to', 'o', 'in',
        'for', 'on', 'with', 'at', 'by', 'from', 'about', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out',
        'of', 'over', 'under', 'again', 'further', 'then', 'once', 'and',
        'but', 'or', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
        'too', 'very', 'just', 'now', 'i', 'you', 'he', 'she', 'it', 'we',
        'they', 'me', 'him', 'her', 'us', 'them',
    }
    
    def __init__(self):
        """
        Initialize advanced text processing capabilities with mathematical shape understanding.
        
        Why: Set up comprehensive text processing with deep geometric concept recognition
        Where: Called once during system initialization
        How: Define stopwords, shape vocabularies, and mathematical concept mappings
        
        Connects to:
            - persona.py: Response generation analysis enhanced with shape detection
            - evolution_engine.py: Learning and context extraction with mathematical concepts
            - shape_generator.py: Mathematical shape generation based on detected concepts
        """
        self.stopwords = self.STOPWORDS
        
        # Enhanced shape recognition vocabulary for cognitive evolution
        self.shape_vocabulary = {
            'basic_polygons': {
                'triangle': ['triangle', 'triangular', 'tri', 'three-sided', '3-sided'],
                'square': ['square', 'rectangle', 'rectangular', 'four-sided', '4-sided', 'quad'],
                'pentagon': ['pentagon', 'pentagonal', 'five-sided', '5-sided'],
                'hexagon': ['hexagon', 'hexagonal', 'six-sided', '6-sided', 'honeycomb'],
                'heptagon': ['heptagon', 'heptagonal', 'seven-sided', '7-sided'],
                'octagon': ['octagon', 'octagonal', 'eight-sided', '8-sided'],
                'polygon': ['polygon', 'polygonal', 'sided', 'regular', 'n-sided']
            },
            'curved_shapes': {
                'circle': ['circle', 'circular', 'round', 'ring', 'loop'],
                'sphere': ['sphere', 'spherical', 'ball', 'orb', 'globe'],
                'ellipse': ['ellipse', 'elliptical', 'oval', 'oblong'],
                'torus': ['torus', 'donut', 'doughnut', 'ring', 'tube']
            },
            '3d_shapes': {
                'cube': ['cube', 'box', 'cubic', 'square prism', 'hexahedron'],
                'pyramid': ['pyramid', 'triangular pyramid', 'tetrahedron', 'apex'],
                'prism': ['prism', 'rectangular prism', 'triangular prism'],
                'cylinder': ['cylinder', 'cylindrical', 'tube', 'pipe'],
                'cone': ['cone', 'conical', 'funnel', 'pointed'],
                'dodecahedron': ['dodecahedron', '12-sided', 'twelve-sided'],
                'icosahedron': ['icosahedron', '20-sided', 'twenty-sided'],
                'octahedron': ['octahedron', 'diamond', 'bipyramid']
            },
            'complex_mathematical': {
                'spiral': ['spiral', 'coil', 'helix', 'helical', 'twist', 'swirl'],
                'dna': ['dna', 'double helix', 'genetic', 'nucleotide', 'base pairs', 'chromosome', 'genome'],
                'fibonacci': ['fibonacci', 'golden', 'phi', 'golden ratio', 'natural'],
                'fractal': ['fractal', 'recursive', 'self-similar', 'mandelbrot', 'koch', 'snowflake'],
                'wave': ['wave', 'sine', 'cosine', 'sinusoidal', 'periodic', 'oscillating']
            },
            'mathematical_concepts': {
                'geometry': ['geometry', 'geometric', 'mathematical', 'math', 'calculate'],
                'symmetry': ['symmetry', 'symmetric', 'balanced', 'regular', 'uniform'],
                'properties': ['area', 'perimeter', 'circumference', 'radius', 'diameter', 'angle', 'vertex'],
                'precision': ['precise', 'exact', 'perfect', 'accurate', 'mathematical']
            }
        }
        
        # Mathematical action verbs for shape commands
        self.shape_actions = {
            'create': ['create', 'make', 'build', 'construct', 'generate'],
            'form': ['form', 'shape', 'morph', 'transform', 'arrange'],
            'show': ['show', 'display', 'demonstrate', 'present', 'reveal'],
            'draw': ['draw', 'sketch', 'trace', 'outline', 'plot'],
            'calculate': ['calculate', 'compute', 'determine', 'find', 'derive']
        }
        
        # Educational mathematical keywords for enhanced responses
        self.mathematical_topics = {
            'angles': ['angle', 'degree', 'radian', 'interior', 'exterior', 'acute', 'obtuse', 'right'],
            'measurements': ['area', 'perimeter', 'volume', 'surface', 'length', 'width', 'height'],
            'ratios': ['ratio', 'proportion', 'golden', 'phi', 'pi', 'constant'],
            'complexity': ['iteration', 'recursive', 'infinite', 'dimension', 'fractal']
        }
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text and extract features with enhanced mathematical shape understanding.
        
        Why: Main entry point for text analysis with deep geometric concept recognition
        Where: Called by persona.py, evolution_engine.py, memory_engine.py for cognitive enhancement
        How: Extracts keywords, sentiment, entities, mathematical concepts, and shape intents
        
        Args:
            text: The text string to process
            
        Returns:
            Dictionary containing comprehensive analysis including keywords, sentiment, 
            entities, mathematical concepts, detected shapes, educational topics, and metrics
            
        Connects to:
            - persona.py: Enhanced shape detection drives mathematical response generation
            - shape_generator.py: Detected shapes trigger precise mathematical generation
            - evolution_engine.py: Mathematical concept learning and cognitive development
        """
        # Compute base extraction
        keywords = self.extract_keywords(text)
        sentiment = self.analyze_sentiment(text)
        entities = self.extract_entities(text)
        word_count = len(text.split())
        char_count = len(text)
        noise_metrics = self._noise_metrics(text)
        
        # Enhanced mathematical shape analysis
        shape_analysis = self.analyze_mathematical_concepts(text)
        
        # Comprehensive academic knowledge analysis
        academic_analysis = {}
        if _ACADEMIC_ENGINE_AVAILABLE:
            try:
                academic_engine = get_academic_engine()
                academic_analysis = academic_engine.analyze_academic_content(text)
            except Exception as e:
                print(f"⚠️ Academic analysis failed: {e}")
                academic_analysis = {
                    'detected_concepts': [],
                    'primary_domain': None,
                    'domain_scores': {},
                    'total_concepts': 0,
                    'confidence': 0.0
                }
        
        return {
            'keywords': keywords,
            'sentiment': sentiment,
            'entities': entities,
            'word_count': word_count,
            'char_count': char_count,
            **noise_metrics,
            **shape_analysis,
            'academic_analysis': academic_analysis
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
        """
        Estimate noise characteristics (typos, gibberish, smash) using complete English dictionary.

        Why: Persona needs to recognize when user input is accidental (keyboard smash) 
             or heavily typo-laden to prompt clarification, using comprehensive vocabulary
        Where: Included in analysis dict used by persona.generate for intelligent responses
        How: Enhanced dictionary lookup (235K+ words) + pattern analysis for true accuracy

        Returns keys:
            - typo_ratio: float 0..1 approximate tokens likely misspelled
            - smash_score: float 0..1 intensity of random input patterns  
            - needs_clarification: bool high noise composite flag
            - dictionary_coverage: float 0..1 ratio of words found in dictionary
        """
        lowered = text.lower()
        tokens = re.findall(r"[a-zA-Z]+", lowered)
        if not tokens:
            return {
                "typo_ratio": 0.0, 
                "smash_score": 0.0, 
                "needs_clarification": False,
                "dictionary_coverage": 1.0
            }
        
        # Use enhanced English dictionary for accurate word validation
        misspelled = 0
        dictionary_hits = 0
        
        if _ENHANCED_DICT_AVAILABLE:
            try:
                english_dict = get_english_dictionary()
                for token in tokens:
                    # Skip very short tokens and numbers for validation
                    if len(token) <= 2 or token.isdigit():
                        dictionary_hits += 1  # Don't penalize short words/numbers
                        continue
                    
                    if english_dict.is_english_word(token):
                        dictionary_hits += 1
                    else:
                        # Additional checks for technical terms, abbreviations, names
                        if self._is_likely_valid_term(token):
                            dictionary_hits += 1
                        else:
                            misspelled += 1
                            
            except Exception as e:
                # Fallback to enhanced core vocabulary if dictionary fails
                print(f"⚠️ Dictionary lookup failed: {e}")
                misspelled, dictionary_hits = self._fallback_typo_detection(tokens)
        else:
            # Fallback when enhanced dictionary not available
            misspelled, dictionary_hits = self._fallback_typo_detection(tokens)
        
        # Pattern-based noise detection for keyboard smashing
        consonant_runs = 0
        long_repeats = 0
        total_chars = sum(len(t) for t in tokens)
        
        for t in tokens:
            # Consonant run length measure (excessive consonant clusters)
            cruns = re.findall(r"[^aeiou\W]{4,}", t)
            consonant_runs += sum(len(c) for c in cruns)
            
            # Repeated character sequences (like "aaaaa" or "123123")
            if re.search(r"(.)\1{3,}", t):
                long_repeats += 1
        
        # Calculate metrics
        typo_ratio = misspelled / max(1, len(tokens))
        dictionary_coverage = dictionary_hits / max(1, len(tokens))
        
        # Shannon-like entropy proxy: unique chars / length
        unique_chars = len(set(lowered))
        entropy_proxy = unique_chars / max(1, len(lowered))
        
        # Enhanced smash score considering dictionary coverage
        smash_score = min(1.0, 
            0.3 * typo_ratio + 
            0.2 * (consonant_runs / max(1, total_chars)) + 
            0.2 * (long_repeats / max(1, len(tokens))) +
            0.3 * (1.0 - dictionary_coverage)  # Penalty for low dictionary coverage
        )
        
        # Intelligent thresholds - only flag truly problematic text
        needs_clarification = (
            (typo_ratio > self.NOISE_TYPO_THRESHOLD and dictionary_coverage < 0.4) or
            (long_repeats >= self.NOISE_REPEAT_THRESHOLD) or 
            (entropy_proxy < self.NOISE_ENTROPY_THRESHOLD and len(tokens) > 2) or
            (smash_score > 0.8 and dictionary_coverage < 0.3)
        )
        
        return {
            "typo_ratio": round(typo_ratio, 3),
            "smash_score": round(smash_score, 3), 
            "needs_clarification": needs_clarification,
            "dictionary_coverage": round(dictionary_coverage, 3)
        }
    
    def _is_likely_valid_term(self, token: str) -> bool:
        """
        Check if a token is likely a valid term even if not in dictionary.
        
        Why: Handle technical terms, names, abbreviations, and modern language
        Where: Used by enhanced noise detection for comprehensive validation
        How: Pattern matching for common valid non-dictionary terms
        """
        # Common patterns for valid terms
        patterns = [
            r'^[A-Z][a-z]+$',           # Capitalized words (names, brands)  
            r'^[A-Z]{2,}$',             # Acronyms (API, HTML, CSS)
            r'^[a-z]+[A-Z][a-z]*$',     # camelCase (JavaScript, iPhone)
            r'^[a-z]+(ed|ing|ly|tion|ment|ness)$',  # Common suffixes
            r'^(un|re|pre|dis|mis|over|under)[a-z]+$',  # Common prefixes
            r'^[a-z]+[0-9]+$',          # alphanumeric (html5, css3)
        ]
        
        return any(re.match(pattern, token) for pattern in patterns)
    
    def _fallback_typo_detection(self, tokens: List[str]) -> tuple[int, int]:
        """
        Fallback typo detection when enhanced dictionary is unavailable.
        
        Why: Provide reasonable typo detection even without full dictionary
        Where: Used when enhanced_nlp_dictionary import fails
        How: Enhanced core vocabulary + pattern heuristics
        """
        # Enhanced core vocabulary (expanded significantly from original 200 words)
        enhanced_core_vocab = {
            # Core English (1000+ most common words)
            "the","and","that","this","you","for","with","have","are","but","not","can","your","from","what","about","just","like","time","need","want","make","good","great","right","work","way","use","get","new","know","take","come","go","see","look","think","say","tell","ask","try","give","find","help","start","call","feel","leave","put","move","live","show","play","run","walk","talk","sit","stand","turn","bring","keep","hold","let","begin","hear","watch","follow","stop","create","open","close","read","write","learn","teach","understand","remember","forget","believe","hope","wish","love","like","hate","enjoy","prefer","choose","decide","plan","prepare","organize","manage","control","lead","guide","direct","support","assist","serve","provide","offer","share","receive","accept","reject","agree","disagree","argue","discuss","explain","describe","suggest","recommend","advise","warn","remind","promise","threaten","apologize","thank","congratulate","welcome","invite","visit","meet","introduce","greet","goodbye","hello","please","sorry","excuse","pardon","yes","no","maybe","perhaps","probably","certainly","definitely","absolutely","never","always","sometimes","often","usually","rarely","seldom","occasionally","frequently","regularly","daily","weekly","monthly","yearly","today","tomorrow","yesterday","morning","afternoon","evening","night","early","late","now","then","soon","later","before","after","during","while","when","where","why","how","what","which","who","whose","whom","that","this","these","those","all","some","many","few","little","much","more","most","less","least","each","every","any","no","none","both","either","neither","other","another","same","different","similar","equal","opposite","near","far","here","there","everywhere","somewhere","anywhere","nowhere","up","down","in","out","on","of","over","under","above","below","beside","between","among","through","across","around","along","toward","away","inside","outside","forward","backward","left","right","north","south","east","west","big","small","large","little","huge","tiny","tall","short","long","wide","narrow","thick","thin","heavy","light","strong","weak","hard","soft","hot","cold","warm","cool","dry","wet","clean","dirty","new","old","young","fresh","modern","ancient","recent","past","future","present","current","fast","slow","quick","rapid","sudden","gradual","easy","difficult","hard","simple","complex","complicated","clear","unclear","obvious","hidden","public","private","open","closed","free","busy","available","ready","finished","complete","incomplete","perfect","imperfect","correct","wrong","true","false","real","fake","natural","artificial","normal","strange","usual","unusual","common","rare","popular","famous","unknown","important","unimportant","necessary","unnecessary","possible","impossible","certain","uncertain","sure","unsure","confident","worried","happy","sad","angry","calm","excited","bored","interested","surprised","shocked","afraid","brave","careful","careless","patient","impatient","kind","mean","friendly","unfriendly","polite","rude","honest","dishonest","fair","unfair","right","wrong","legal","illegal","safe","dangerous","healthy","sick","alive","dead","awake","asleep","active","passive","busy","lazy","rich","poor","expensive","cheap","valuable","worthless","beautiful","ugly","attractive","pretty","handsome","nice","wonderful","terrible","awful","amazing","incredible","fantastic","excellent","perfect","good","bad","better","worse","best","worst","fine","okay","alright","well","sick","ill","hurt","pain","doctor","nurse","hospital","medicine","health","food","eat","drink","cook","kitchen","restaurant","breakfast","lunch","dinner","bread","meat","fish","chicken","bee","pork","rice","pasta","pizza","salad","soup","coffee","tea","water","milk","juice","beer","wine","house","home","apartment","room","bedroom","bathroom","kitchen","living","office","school","university","college","library","store","shop","market","bank","post","hotel","church","park","street","road","car","bus","train","plane","bike","walk","drive","travel","trip","vacation","holiday","work","job","career","business","company","office","meeting","computer","internet","phone","email","message","letter","book","newspaper","magazine","television","radio","music","movie","game","sport","football","basketball","baseball","tennis","soccer","swimming","running","dancing","singing","painting","drawing","writing","reading","studying","learning","teaching","working","playing","sleeping","eating","drinking","cooking","cleaning","shopping","driving","walking","running","sitting","standing","lying","talking","listening","watching","looking","seeing","hearing","feeling","touching","smelling","tasting","thinking","knowing","understanding","remembering","forgetting","learning","teaching","studying","working","playing","helping","loving","liking","hating","wanting","needing","having","getting","giving","taking","making","doing","going","coming","leaving","staying","moving","stopping","starting","finishing","continuing","beginning","ending","opening","closing","buying","selling","paying","spending","saving","earning","winning","losing","finding","searching","looking","waiting","hoping","wishing","trying","succeeding","failing","improving","changing","growing","developing","building","creating","destroying","breaking","fixing","repairing","cleaning","washing","drying","cooking","eating","drinking","sleeping","waking","getting","dressing","undressing","wearing","putting","taking","holding","carrying","lifting","pushing","pulling","throwing","catching","hitting","kicking","running","walking","jumping","climbing","falling","swimming","flying","driving","riding","traveling","arriving","departing","entering","exiting","visiting","meeting","greeting","introducing","talking","speaking","saying","telling","asking","answering","explaining","describing","discussing","arguing","agreeing","disagreeing","deciding","choosing","planning","preparing","organizing","managing","controlling","leading","following","guiding","helping","supporting","serving","working","playing","resting","relaxing","exercising","studying","learning","teaching","reading","writing","drawing","painting","singing","dancing","listening","watching","looking","seeing","hearing","feeling","touching","smelling","tasting","thinking","remembering","forgetting","knowing","understanding","believing","hoping","wishing","loving","liking","hating","fearing","worrying","caring","trusting","respecting","admiring","appreciating","enjoying","preferring","wanting","needing","having","owning","possessing","keeping","losing","finding","searching","discovering","exploring","investigating","examining","observing","noticing","recognizing","identifying","comparing","contrasting","measuring","counting","calculating","estimating","guessing","predicting","expecting","assuming","supposing","imagining","dreaming","planning","intending","attempting","trying","practicing","training","preparing","organizing","arranging","scheduling","managing","controlling","supervising","monitoring","checking","testing","examining","evaluating","judging","criticizing","praising","complimenting","thanking","apologizing","forgiving","blaming","accusing","defending","protecting","attacking","fighting","competing","cooperating","collaborating","sharing","giving","receiving","exchanging","trading","buying","selling","paying","spending","investing","saving","earning","making","creating","producing","manufacturing","building","constructing","designing","planning","developing","improving","enhancing","upgrading","updating","modifying","changing","transforming","converting","translating","interpreting","explaining","clarifying","simplifying","complicating","solving","resolving","fixing","repairing","maintaining","preserving","protecting","defending","securing","locking","unlocking","opening","closing","starting","stopping","pausing","continuing","resuming","finishing","completing","achieving","accomplishing","succeeding","failing","winning","losing","gaining","obtaining","acquiring","getting","receiving","accepting","rejecting","refusing","denying","confirming","approving","disapproving","allowing","permitting","forbidding","preventing","avoiding","escaping","hiding","revealing","showing","displaying","demonstrating","presenting","introducing","announcing","declaring","stating","claiming","asserting","insisting","demanding","requesting","asking","begging","pleading","urging","encouraging","discouraging","persuading","convincing","influencing","affecting","impacting","changing","altering","modifying","adjusting","adapting","conforming","complying","obeying","disobeying","rebelling","resisting","opposing","supporting","backing","endorsing","promoting","advertising","marketing","selling","recommending","suggesting","proposing","offering","providing","supplying","delivering","transporting","moving","transferring","shifting","relocating","traveling","journeying","visiting","touring","exploring","discovering","finding","locating","positioning","placing","putting","setting","installing","establishing","founding","creating","building","constructing","developing","growing","expanding","extending","stretching","reaching","touching","contacting","connecting","linking","joining","uniting","combining","merging","mixing","blending","separating","dividing","splitting","breaking","cutting","tearing","ripping","destroying","damaging","harming","hurting","injuring","healing","curing","treating","helping","assisting","supporting","comforting","consoling","encouraging","motivating","inspiring","influencing","guiding","leading","directing","managing","supervising","overseeing","monitoring","controlling","regulating","governing","ruling","commanding","ordering","instructing","teaching","training","educating","informing","telling","explaining","describing","discussing","talking","speaking","communicating","expressing","conveying","transmitting","sending","delivering","receiving","getting","obtaining","acquiring","gaining","earning","making","producing","creating","generating","causing","resulting","leading","bringing","taking","carrying","moving","transporting","delivering","supplying","providing","offering","giving","presenting","showing","displaying","demonstrating","proving","confirming","verifying","validating","checking","testing","examining","inspecting","investigating","researching","studying","analyzing","evaluating","assessing","measuring","calculating","computing","determining","deciding","choosing","selecting","picking","preferring","favoring","liking","loving","enjoying","appreciating","valuing","respecting","admiring","praising","complimenting","thanking","congratulating","celebrating","honoring","rewarding","recognizing","acknowledging","accepting","approving","agreeing","supporting","backing","endorsing","recommending","suggesting","proposing","advising","counseling","guiding","directing","instructing","teaching","training","educating","learning","studying","practicing","exercising","working","laboring","toiling","striving","struggling","fighting","battling","competing","contending","opposing","resisting","defending","protecting","guarding","watching","observing","monitoring","supervising","overseeing","managing","controlling","regulating","governing","administering","operating","running","conducting","performing","executing","implementing","carrying","accomplishing","achieving","succeeding","completing","finishing","ending","concluding","stopping","ceasing","quitting","leaving","departing","going","moving","traveling","journeying","walking","running","driving","riding","flying","sailing","swimming","climbing","jumping","falling","rising","ascending","descending","approaching","retreating","advancing","progressing","developing","growing","increasing","expanding","extending","spreading","widening","broadening","deepening","strengthening","weakening","improving","deteriorating","declining","decreasing","reducing","diminishing","shrinking","contracting","narrowing","shortening","lengthening","extending","stretching","reaching","touching","grasping","holding","gripping","clutching","releasing","letting","dropping","falling","rising","lifting","raising","lowering","pushing","pulling","dragging","carrying","moving","shifting","transferring","transporting","delivering","bringing","taking","getting","fetching","retrieving","collecting","gathering","assembling","organizing","arranging","sorting","separating","dividing","distributing","sharing","spreading","scattering","dispersing","concentrating","focusing","centering","targeting","aiming","pointing","directing","guiding","leading","following","chasing","pursuing","hunting","searching","seeking","looking","finding","discovering","exploring","investigating","examining","studying","analyzing","researching","learning","understanding","knowing","recognizing","identifying","distinguishing","differentiating","comparing","contrasting","relating","connecting","linking","associating","combining","joining","uniting","merging","mixing","blending","integrating","incorporating","including","adding","inserting","putting","placing","setting","positioning","locating","situating","establishing","founding","creating","building","making","producing","manufacturing","generating","developing","designing","planning","preparing","organizing","arranging","scheduling","timing","coordinating","synchronizing","balancing","equalizing","adjusting","regulating","controlling","managing","supervising","directing","guiding","leading","commanding","governing","ruling","administering","operating","running","conducting","performing","executing","implementing","applying","using","utilizing","employing","exploiting","taking","benefiting","profiting","gaining","earning","making","getting","obtaining","acquiring","receiving","accepting","taking","grabbing","seizing","capturing","catching","holding","keeping","maintaining","preserving","protecting","defending","guarding","securing","saving","storing","keeping","retaining","maintaining","continuing","persisting","enduring","lasting","remaining","staying","living","existing","surviving","thriving","flourishing","prospering","succeeding","achieving","accomplishing","completing","finishing","ending","stopping","ceasing","quitting","giving","abandoning","leaving","departing","going","moving","changing","shifting","transforming","converting","becoming","turning","growing","developing","evolving","progressing","advancing","improving","enhancing","upgrading","updating","modernizing","renovating","restoring","repairing","fixing","correcting","adjusting","modifying","altering","changing","varying","differing","distinguishing","separating","dividing","splitting","breaking","cutting","tearing","destroying","damaging","ruining","spoiling","corrupting","contaminating","polluting","cleaning","washing","purifying","clarifying","simplifying","complicating","confusing","puzzling","mystifying","solving","resolving","settling","deciding","determining","concluding","ending","finishing","completing","accomplishing","achieving","succeeding","winning","triumphing","conquering","defeating","beating","overcoming","surpassing","exceeding","outperforming","outdoing","outshining","excelling","leading","guiding","directing","managing","controlling","governing","ruling","commanding","ordering","instructing","teaching","training","educating","learning","studying","practicing","rehearsing","preparing","planning","organizing","arranging","scheduling","coordinating","managing","supervising","overseeing","monitoring","watching","observing","noticing","seeing","looking","viewing","examining","inspecting","investigating","exploring","discovering","finding","locating","detecting","identifying","recognizing","distinguishing","differentiating","comparing","contrasting","evaluating","assessing","judging","analyzing","studying","researching","investigating","examining","testing","checking","verifying","confirming","validating","proving","demonstrating","showing","displaying","presenting","exhibiting","revealing","exposing","uncovering","discovering","finding","detecting","noticing","observing","watching","monitoring","tracking","following","chasing","pursuing","hunting","searching","seeking","looking","scanning","surveying","exploring","investigating","examining","studying","analyzing","researching","learning","understanding","comprehending","grasping","realizing","recognizing","knowing","remembering","recalling","forgetting","ignoring","neglecting","overlooking","missing","losing","finding","recovering","regaining","getting","obtaining","acquiring","gaining","earning","making","creating","producing","generating","developing","building","constructing","establishing","founding","starting","beginning","initiating","launching","opening","closing","shutting","ending","finishing","completing","concluding","stopping","ceasing","pausing","continuing","resuming","restarting","repeating","duplicating","copying","imitating","mimicking","reproducing","regenerating","recreating","rebuilding","reconstructing","restoring","repairing","fixing","correcting","adjusting","tuning","calibrating","setting","configuring","programming","coding","developing","creating","designing","planning","preparing","organizing","managing","controlling","operating","running","executing","performing","conducting","leading","directing","guiding","supervising","overseeing","monitoring","checking","testing","evaluating","assessing","measuring","calculating","computing","processing","analyzing","examining","studying","researching","investigating","exploring","discovering","learning","understanding","knowing","thinking","considering","pondering","reflecting","meditating","contemplating","wondering","questioning","doubting","believing","trusting","hoping","expecting","anticipating","predicting","forecasting","estimating","guessing","assuming","supposing","imagining","dreaming","fantasizing","visualizing","picturing","seeing","looking","watching","observing","noticing","recognizing","identifying","distinguishing","differentiating","comparing","contrasting","matching","fitting","suiting","adapting","adjusting","modifying","changing","altering","varying","differing","opposing","contrasting","conflicting","disagreeing","arguing","debating","discussing","talking","speaking","communicating","expressing","saying","telling","explaining","describing","narrating","reporting","announcing","declaring","proclaiming","stating","claiming","asserting","insisting","demanding","requesting","asking","questioning","inquiring","wondering","doubting","challenging","disputing","objecting","protesting","complaining","criticizing","blaming","accusing","charging","suing","prosecuting","defending","protecting","supporting","backing","endorsing","approving","agreeing","accepting","welcoming","embracing","adopting","taking","receiving","getting","obtaining","acquiring","gaining","earning","winning","achieving","accomplishing","succeeding","completing","finishing","ending","concluding","stopping","halting","ceasing","quitting","leaving","departing","going","coming","arriving","reaching","getting","making","doing","performing","executing","carrying","conducting","operating","running","managing","controlling","directing","guiding","leading","supervising","overseeing","monitoring","watching","observing","checking","testing","examining","inspecting","investigating","studying","analyzing","evaluating","assessing","measuring","calculating","determining","deciding","choosing","selecting","picking","preferring","liking","loving","enjoying","appreciating","valuing","treasuring","cherishing","adoring","worshipping","respecting","admiring","praising","complimenting","flattering","encouraging","supporting","helping","assisting","aiding","serving","benefiting","favoring","promoting","advancing","forwarding","facilitating","enabling","allowing","permitting","authorizing","approving","endorsing","sanctioning","licensing","certifying","validating","confirming","verifying","proving","demonstrating","showing","displaying","exhibiting","presenting","introducing","announcing","declaring","revealing","disclosing","exposing","uncovering","discovering","finding","detecting","locating","identifying","recognizing","distinguishing","characterizing","describing","defining","explaining","clarifying","interpreting","translating","converting","transforming","changing","altering","modifying","adjusting","adapting","accommodating","fitting","matching","suiting","corresponding","relating","connecting","linking","associating","combining","joining","uniting","merging","integrating","incorporating","including","adding","inserting","introducing","bringing","taking","moving","shifting","transferring","transporting","carrying","delivering","supplying","providing","offering","giving","presenting","granting","awarding","bestowing","conferring","donating","contributing","sharing","distributing","allocating","assigning","designating","appointing","nominating","electing","choosing","selecting","picking","deciding","determining","resolving","settling","solving","fixing","repairing","correcting","adjusting","improving","enhancing","upgrading","updating","modernizing","advancing","progressing","developing","growing","expanding","extending","increasing","multiplying","doubling","tripling","quadrupling","magnifying","amplifying","enlarging","broadening","widening","deepening","heightening","raising","lifting","elevating","promoting","advancing","boosting","strengthening","reinforcing","supporting","backing","endorsing","encouraging","motivating","inspiring","stimulating","exciting","thrilling","delighting","pleasing","satisfying","fulfilling","gratifying","rewarding","compensating","paying","reimbursing","repaying","returning","giving","restoring","replacing","substituting","exchanging","trading","swapping","switching","changing","altering","varying","modifying","adjusting","adapting","converting","transforming","turning","becoming","growing","developing","evolving","maturing","aging","getting","becoming","turning","going","coming","moving","traveling","journeying","walking","running","driving","flying","sailing","swimming","diving","climbing","jumping","dancing","singing","playing","working","studying","learning","teaching","helping","serving","living","existing","being","staying","remaining","continuing","lasting","enduring","surviving","thriving","flourishing","succeeding","winning","achieving","accomplishing","completing","finishing",
            
            # Technical & Programming Terms (500+ terms)
            "code","coding","program","programming","software","hardware","computer","system","database","server","client","network","internet","web","website","application","app","interface","user","data","information","file","folder","directory","document","text","image","video","audio","media","content","digital","electronic","online","offline","cloud","local","remote","virtual","real","actual","physical","logical","abstract","concrete","specific","general","particular","individual","personal","private","public","open","closed","secure","safe","protected","encrypted","decrypted","compressed","decompressed","uploaded","downloaded","imported","exported","created","deleted","modified","updated","saved","loaded","processed","analyzed","computed","calculated","generated","produced","developed","designed","built","constructed","tested","debugged","optimized","enhanced","improved","upgraded","downgraded","installed","uninstalled","configured","setup","initialized","started","stopped","paused","resumed","executed","run","running","active","inactive","enabled","disabled","available","unavailable","online","offline","connected","disconnected","linked","unlinked","synchronized","synced","asynchronous","async","synchronous","sync","automatic","manual","interactive","batch","real-time","live","static","dynamic","responsive","adaptive","scalable","portable","compatible","incompatible","stable","unstable","reliable","unreliable","fast","slow","efficient","inefficient","optimal","suboptimal","maximum","minimum","average","median","standard","custom","default","advanced","basic","simple","complex","easy","difficult","hard","soft","light","heavy","small","large","big","tiny","huge","enormous","massive","minimal","maximal","full","empty","complete","incomplete","partial","total","whole","entire","all","some","none","any","every","each","individual","collective","shared","common","unique","special","normal","abnormal","regular","irregular","standard","nonstandard","conventional","unconventional","traditional","modern","contemporary","current","recent","past","future","present","temporary","permanent","short","long","brie","extended","quick","slow","fast","rapid","instant","immediate","delayed","postponed","scheduled","planned","unplanned","expected","unexpected","predictable","unpredictable","certain","uncertain","sure","unsure","confident","doubtful","clear","unclear","obvious","hidden","visible","invisible","apparent","transparent","opaque","solid","liquid","gas","matter","energy","force","power","strength","weakness","advantage","disadvantage","benefit","cost","price","value","worth","quality","quantity","amount","number","count","total","sum","difference","ratio","percentage","fraction","decimal","integer","float","double","string","character","text","message","signal","input","output","feedback","response","request","query","command","instruction","order","rule","law","principle","concept","idea","thought","notion","theory","hypothesis","assumption","fact","truth","reality","fiction","fantasy","imagination","dream","vision","goal","objective","target","purpose","intention","plan","strategy","method","approach","technique","procedure","process","step","stage","phase","level","degree","grade","rank","position","location","place","spot","point","area","region","zone","section","part","piece","component","element","item","object","thing","stuf","material","substance","content","information","data","knowledge","wisdom","understanding","comprehension","insight","awareness","consciousness","intelligence","smartness","cleverness","brightness","brilliance","genius","talent","skill","ability","capability","capacity","potential","power","strength","energy","force","effort","work","labor","task","job","duty","responsibility","obligation","commitment","promise","agreement","contract","deal","arrangement","plan","project","program","initiative","campaign","mission","operation","action","activity","event","occurrence","happening","incident","accident","mistake","error","fault","problem","issue","trouble","difficulty","challenge","obstacle","barrier","limitation","restriction","constraint","boundary","limit","border","edge","margin","frame","structure","framework","system","network","connection","link","relationship","association","partnership","collaboration","cooperation","competition","contest","game","sport","play","fun","entertainment","amusement","enjoyment","pleasure","happiness","joy","delight","satisfaction","contentment","peace","calm","quiet","silence","noise","sound","music","song","melody","rhythm","beat","tempo","speed","pace","rate","frequency","intensity","volume","level","amount","quantity","size","dimension","measurement","scale","proportion","balance","harmony","symmetry","pattern","design","style","fashion","trend","mode","way","manner","method","approach","technique","skill","art","craft","trade","profession","occupation","career","job","work","business","industry","company","organization","institution","agency","department","division","section","team","group","crew","staf","personnel","people","person","individual","human","man","woman","child","adult","senior","junior","young","old","new","fresh","original","unique","special","different","same","similar","identical","equal","equivalent","comparable","relative","absolute","exact","approximate","rough","precise","accurate","correct","right","wrong","false","true","real","fake","genuine","artificial","natural","synthetic","organic","inorganic","biological","chemical","physical","mental","emotional","psychological","spiritual","material","immaterial","tangible","intangible","concrete","abstract","solid","liquid","gas","plasma","matter","energy","mass","weight","density","volume","area","length","width","height","depth","thickness","distance","space","time","duration","period","interval","moment","instant","second","minute","hour","day","week","month","year","decade","century","millennium","past","present","future","before","after","during","while","when","where","why","how","what","which","who","whose","whom","that","this","these","those","here","there","everywhere","somewhere","anywhere","nowhere","now","then","soon","later","early","late","always","never","sometimes","often","usually","rarely","seldom","frequently","occasionally","regularly","daily","weekly","monthly","yearly","annually","constantly","continuously","continually","perpetually","forever","eternal","temporary","permanent","stable","unstable","fixed","mobile","movable","immovable","static","dynamic","active","passive","aggressive","defensive","offensive","protective","safe","dangerous","risky","secure","insecure","certain","uncertain","sure","unsure","confident","nervous","calm","excited","bored","interested","curious","surprised","shocked","amazed","astonished","delighted","pleased","happy","sad","angry","mad","furious","annoyed","irritated","frustrated","disappointed","worried","concerned","afraid","scared","terrified","brave","courageous","bold","shy","timid","humble","proud","arrogant","modest","boastful","honest","dishonest","truthful","lying","sincere","fake","genuine","authentic","original","copy","duplicate","replica","model","example","sample","specimen","instance","case","situation","condition","state","status","position","location","place","spot","area","region","territory","country","nation","state","city","town","village","community","neighborhood","district","zone","sector","field","domain","realm","sphere","world","universe","space","environment","surrounding","context","background","foreground","front","back","side","top","bottom","left","right","center","middle","inside","outside","interior","exterior","internal","external","inner","outer","upper","lower","higher","lower","superior","inferior","better","worse","best","worst","good","bad","excellent","terrible","perfect","imperfect","complete","incomplete","finished","unfinished","done","undone","ready","unready","prepared","unprepared","organized","disorganized","neat","messy","clean","dirty","pure","impure","clear","unclear","transparent","opaque","bright","dark","light","heavy","easy","difficult","simple","complex","plain","fancy","ordinary","extraordinary","common","rare","usual","unusual","normal","abnormal","standard","special","regular","irregular","straight","curved","smooth","rough","flat","bumpy","even","uneven","level","slanted","horizontal","vertical","diagonal","parallel","perpendicular","circular","square","rectangular","triangular","oval","round","pointed","sharp","blunt","dull","bright","dim","loud","quiet","soft","hard","warm","cold","hot","cool","dry","wet","moist","humid","arid","fertile","barren","rich","poor","thick","thin","wide","narrow","broad","slim","fat","skinny","tall","short","high","low","deep","shallow","long","short","big","small","large","little","huge","tiny","enormous","miniature","giant","dwar","maximum","minimum","major","minor","main","secondary","primary","secondary","first","last","beginning","end","start","finish","opening","closing","entrance","exit","arrival","departure","coming","going","approach","retreat","advance","retreat","forward","backward","upward","downward","inward","outward","toward","away","near","far","close","distant","next","previous","following","preceding","subsequent","prior","former","latter","initial","final","original","ultimate","first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth","hundred","thousand","million","billion","trillion","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety","zero","nothing","something","anything","everything","everyone","someone","anyone","no one","nobody","somebody","anybody","everybody",
            
            # Mathematical & Scientific Terms (300+ terms)
            "math","mathematics","mathematical","number","numeral","digit","figure","integer","decimal","fraction","percentage","ratio","proportion","equation","formula","calculation","computation","addition","subtraction","multiplication","division","algebra","geometry","trigonometry","calculus","statistics","probability","logic","reasoning","proo","theorem","hypothesis","theory","principle","law","rule","method","technique","procedure","process","analysis","synthesis","research","study","investigation","experiment","observation","measurement","data","result","conclusion","finding","discovery","invention","innovation","creation","development","progress","advancement","improvement","enhancement","optimization","efficiency","effectiveness","accuracy","precision","exactness","approximation","estimation","prediction","forecast","projection","trend","pattern","sequence","series","set","group","class","category","type","kind","sort","variety","diversity","similarity","difference","comparison","contrast","relation","relationship","connection","link","association","correlation","correspondence","equivalence","identity","equality","inequality","balance","imbalance","symmetry","asymmetry","proportion","disproportion","order","disorder","organization","disorganization","structure","chaos","pattern","randomness","regularity","irregularity","uniformity","variation","change","stability","constancy","consistency","inconsistency","continuity","discontinuity","sequence","consequence","cause","effect","reason","result","origin","source","beginning","end","start","finish","input","output","process","transformation","conversion","translation","interpretation","representation","symbol","sign","notation","expression","statement","declaration","assertion","claim","argument","evidence","proo","demonstration","illustration","example","instance","case","sample","specimen","model","prototype","template","framework","structure","system","network","organization","arrangement","configuration","setup","design","plan","scheme","strategy","approach","method","technique","procedure","algorithm","formula","recipe","instruction","direction","guidance","advice","suggestion","recommendation","proposal","offer","invitation","request","demand","requirement","specification","description","definition","explanation","clarification","interpretation","translation","meaning","significance","importance","relevance","value","worth","merit","quality","property","characteristic","feature","attribute","aspect","element","component","part","piece","section","segment","portion","fragment","bit","unit","measure","quantity","amount","size","dimension","scale","level","degree","grade","rank","position","status","state","condition","situation","circumstance","context","environment","setting","background","foreground","scene","view","perspective","angle","point","focus","center","core","heart","essence","nature","character","personality","identity","sel","individual","person","human","being","existence","life","living","survival","growth","development","evolution","progress","advancement","improvement","enhancement","change","transformation","modification","alteration","adjustment","adaptation","accommodation","flexibility","rigidity","stability","instability","balance","imbalance","equilibrium","disequilibrium","harmony","discord","agreement","disagreement","consensus","conflict","cooperation","competition","collaboration","partnership","relationship","association","connection","link","bond","tie","attachment","separation","division","split","break","crack","gap","space","distance","interval","period","duration","time","moment","instant","second","minute","hour","day","week","month","year","age","era","epoch","generation","lifetime","eternity","infinity","finite","infinite","limited","unlimited","bounded","unbounded","restricted","unrestricted","constrained","unconstrained","controlled","uncontrolled","regulated","unregulated","organized","disorganized","systematic","unsystematic","methodical","unmethodical","logical","illogical","rational","irrational","reasonable","unreasonable","sensible","nonsensical","practical","impractical","realistic","unrealistic","possible","impossible","probable","improbable","likely","unlikely","certain","uncertain","definite","indefinite","specific","general","particular","universal","local","global","regional","national","international","worldwide","cosmic","universal","global","total","partial","complete","incomplete","whole","part","entire","fragment","all","some","none","every","each","individual","collective","singular","plural","unique","common","special","ordinary","exceptional","normal","abnormal","standard","nonstandard","regular","irregular","typical","atypical","usual","unusual","conventional","unconventional","traditional","modern","contemporary","ancient","old","new","recent","current","past","future","present","temporary","permanent","lasting","brie","short","long","extended","prolonged","quick","slow","fast","rapid","swift","sluggish","immediate","delayed","instant","gradual","sudden","abrupt","smooth","rough","gentle","harsh","mild","severe","light","heavy","weak","strong","soft","hard","flexible","rigid","elastic","plastic","solid","liquid","gas","dense","sparse","thick","thin","concentrated","diluted","pure","impure","clean","dirty","clear","cloudy","transparent","opaque","visible","invisible","apparent","hidden","obvious","subtle","direct","indirect","straight","crooked","curved","bent","twisted","round","square","circular","angular","pointed","blunt","sharp","dull","bright","dim","light","dark","colored","colorless","vivid","pale","intense","faint","loud","quiet","high","low","deep","shallow","wide","narrow","broad","slim","fat","thin","tall","short","big","small","large","little","huge","tiny","enormous","microscopic","giant","miniature","maximum","minimum","greatest","least","most","fewest","many","few","several","numerous","countless","infinite","zero","one","single","double","triple","multiple","hal","quarter","third","fourth","fifth","whole","entire","complete","total","full","empty","vacant","occupied","available","unavailable","present","absent","here","there","near","far","close","distant","inside","outside","within","without","above","below","over","under","up","down","left","right","front","back","forward","backward","ahead","behind","before","after","first","last","beginning","end","start","finish","initial","final","primary","secondary","main","subsidiary","major","minor","important","unimportant","significant","insignificant","relevant","irrelevant","necessary","unnecessary","essential","nonessential","required","optional","mandatory","voluntary","compulsory","free","open","closed","public","private","personal","impersonal","individual","collective","social","antisocial","friendly","unfriendly","kind","cruel","nice","mean","good","bad","right","wrong","correct","incorrect","true","false","real","fake","genuine","artificial","natural","synthetic","original","copy","authentic","imitation","legitimate","illegitimate","legal","illegal","valid","invalid","acceptable","unacceptable","appropriate","inappropriate","suitable","unsuitable","fitting","unfitting","proper","improper","decent","indecent","moral","immoral","ethical","unethical","honest","dishonest","fair","unfair","just","unjust","equal","unequal","balanced","unbalanced","neutral","biased","objective","subjective","rational","emotional","logical","intuitive","scientific","artistic","technical","creative","practical","theoretical","concrete","abstract","material","spiritual","physical","mental","bodily","psychological","internal","external","inner","outer","personal","social","private","public","individual","group","local","global","specific","general","detailed","broad","precise","vague","exact","approximate","accurate","inaccurate","correct","wrong","right","false","true","real","imaginary","actual","potential","possible","impossible","probable","improbable","certain","doubtful","sure","unsure","confident","hesitant","determined","undecided","resolved","unresolved","settled","unsettled","finished","unfinished","complete","incomplete","done","undone","ready","unready","prepared","unprepared","willing","unwilling","eager","reluctant","enthusiastic","unenthusiastic","interested","uninterested","curious","incurious","attentive","inattentive","careful","careless","cautious","reckless","safe","dangerous","secure","insecure","protected","unprotected","defended","undefended","guarded","unguarded","watched","unwatched","supervised","unsupervised","controlled","uncontrolled","managed","unmanaged","organized","disorganized","planned","unplanned","scheduled","unscheduled","arranged","unarranged","ordered","disordered","systematic","random","regular","irregular","consistent","inconsistent","steady","unsteady","stable","unstable","fixed","variable","constant","changing","permanent","temporary","lasting","brie","enduring","fleeting","eternal","momentary","infinite","finite","unlimited","limited","boundless","bounded","endless","terminal","continuous","discontinuous","unbroken","broken","whole","fragmented","intact","damaged","perfect","imperfect","flawless","flawed","ideal","realistic","theoretical","practical","abstract","concrete","general","specific","universal","particular","broad","narrow","wide","limited","extensive","restricted","comprehensive","partial","complete","incomplete","total","fractional","full","empty","maximum","minimum","optimal","suboptimal","best","worst","better","worse","superior","inferior","excellent","terrible","outstanding","mediocre","exceptional","ordinary","remarkable","unremarkable","notable","unnotable","significant","trivial","important","unimportant","major","minor","primary","secondary","central","peripheral","core","marginal","essential","optional","necessary","unnecessary","required","voluntary","compulsory","free","mandatory","discretionary","automatic","manual","mechanical","electronic","digital","analog","virtual","real","simulated","genuine","artificial","natural","synthetic","organic","inorganic","living","nonliving","animate","inanimate","conscious","unconscious","aware","unaware","alert","sleepy","awake","asleep","active","inactive","busy","idle","working","resting","moving","stationary","dynamic","static","energetic","lethargic","vigorous","weak","strong","powerful","powerless","capable","incapable","able","unable","skilled","unskilled","talented","untalented","gifted","ungifted","smart","stupid","intelligent","unintelligent","clever","foolish","wise","unwise","knowledgeable","ignorant","educated","uneducated","learned","unlearned","experienced","inexperienced","expert","novice","professional","amateur","qualified","unqualified","competent","incompetent","efficient","inefficient","effective","ineffective","successful","unsuccessful","productive","unproductive","useful","useless","helpful","unhelpful","beneficial","harmful","advantageous","disadvantageous","favorable","unfavorable","positive","negative","good","bad","excellent","poor","superior","inferior","high","low","great","small","large","little","big","tiny","huge","minute","enormous","microscopic","gigantic","massive","lightweight","heavy","light","dense","sparse","thick","thin","wide","narrow","broad","slim","fat","skinny","tall","short","long","brie","extended","prolonged","quick","slow","fast","rapid","swift","sluggish","speedy","tardy","prompt","delayed","immediate","eventual","instant","gradual","sudden","abrupt","smooth","rough","gentle","harsh","soft","hard","tender","tough","delicate","sturdy","fragile","durable","weak","strong","flimsy","solid","liquid","gaseous","frozen","melted","hot","cold","warm","cool","burning","freezing","boiling","chilled","heated","cooled","dry","wet","moist","damp","humid","arid","soaked","parched","flooded","drought"
        }
        
        misspelled = 0
        dictionary_hits = 0
        
        for token in tokens:
            # Skip very short tokens and numbers
            if len(token) <= 2 or token.isdigit():
                dictionary_hits += 1
                continue
                
            if token in enhanced_core_vocab or self._is_likely_valid_term(token):
                dictionary_hits += 1
            else:
                # Additional heuristics for likely valid words
                if not (not re.search(r"[aeiou]", token) or re.search(r"[^aeiou]{5,}", token)):
                    dictionary_hits += 1  # Has vowels and reasonable consonant patterns
                else:
                    misspelled += 1
        
        return misspelled, dictionary_hits
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze text sentiment with comprehensive emotional vocabulary understanding.
        
        Why: Understand emotional tone for appropriate responses using extensive vocabulary
        Where: Used by persona engine for tone matching and response personalization
        How: Enhanced rule-based sentiment classification with 500+ emotional terms
        """
        # Comprehensive positive sentiment vocabulary (200+ words)
        positive_words = {
            'good', 'great', 'awesome', 'excellent', 'amazing', 'wonderful', 'fantastic', 
            'love', 'like', 'happy', 'excited', 'pleased', 'joy', 'perfect', 'brilliant', 
            'outstanding', 'superb', 'magnificent', 'marvelous', 'spectacular', 'fabulous',
            'incredible', 'extraordinary', 'phenomenal', 'remarkable', 'impressive', 
            'stunning', 'breathtaking', 'beautiful', 'gorgeous', 'lovely', 'charming',
            'delightful', 'enchanting', 'captivating', 'fascinating', 'intriguing',
            'inspiring', 'motivating', 'uplifting', 'encouraging', 'positive', 'optimistic',
            'hopeful', 'confident', 'enthusiastic', 'passionate', 'energetic', 'vibrant',
            'lively', 'cheerful', 'joyful', 'blissful', 'ecstatic', 'elated', 'thrilled',
            'overjoyed', 'delighted', 'content', 'satisfied', 'fulfilled', 'gratified',
            'proud', 'honored', 'blessed', 'lucky', 'fortunate', 'successful', 'victorious',
            'triumphant', 'winning', 'achieving', 'accomplishing', 'succeeding', 'excelling',
            'flourishing', 'thriving', 'prospering', 'advancing', 'progressing', 'improving',
            'enhancing', 'upgrading', 'optimizing', 'perfecting', 'refining', 'polishing',
            'brilliant', 'genius', 'intelligent', 'clever', 'smart', 'wise', 'insightful',
            'innovative', 'creative', 'artistic', 'talented', 'gifted', 'skilled', 'capable',
            'competent', 'efficient', 'effective', 'productive', 'useful', 'helpful',
            'beneficial', 'valuable', 'precious', 'treasured', 'cherished', 'adored',
            'beloved', 'dear', 'sweet', 'kind', 'gentle', 'caring', 'loving', 'affectionate',
            'tender', 'warm', 'friendly', 'welcoming', 'inviting', 'embracing', 'accepting',
            'inclusive', 'supportive', 'encouraging', 'reassuring', 'comforting', 'soothing',
            'calming', 'peaceful', 'serene', 'tranquil', 'harmonious', 'balanced', 'stable',
            'secure', 'safe', 'protected', 'comfortable', 'cozy', 'relaxed', 'easy',
            'smooth', 'effortless', 'natural', 'organic', 'authentic', 'genuine', 'real',
            'true', 'honest', 'sincere', 'trustworthy', 'reliable', 'dependable', 'loyal',
            'faithful', 'devoted', 'committed', 'dedicated', 'determined', 'persistent',
            'resilient', 'strong', 'powerful', 'robust', 'healthy', 'fit', 'vigorous',
            'energetic', 'dynamic', 'active', 'lively', 'spirited', 'animated', 'vivacious',
            'radiant', 'glowing', 'shining', 'sparkling', 'dazzling', 'bright', 'luminous',
            'clear', 'transparent', 'open', 'accessible', 'available', 'ready', 'prepared',
            'organized', 'structured', 'systematic', 'methodical', 'logical', 'rational',
            'sensible', 'practical', 'realistic', 'achievable', 'possible', 'feasible',
            'workable', 'viable', 'sustainable', 'lasting', 'enduring', 'permanent',
            'eternal', 'timeless', 'classic', 'traditional', 'established', 'proven',
            'tested', 'verified', 'confirmed', 'validated', 'approved', 'endorsed',
            'recommended', 'suggested', 'advised', 'preferred', 'chosen', 'selected',
            'picked', 'nominated', 'appointed', 'designated', 'assigned', 'allocated'
        }
        
        # Comprehensive negative sentiment vocabulary (200+ words)
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry',
            'frustrated', 'annoyed', 'disappointed', 'worried', 'upset', 'stressed',
            'concerned', 'troubled', 'disturbed', 'bothered', 'irritated', 'aggravated',
            'furious', 'enraged', 'livid', 'incensed', 'outraged', 'indignant', 'resentful',
            'bitter', 'hostile', 'aggressive', 'violent', 'destructive', 'harmful', 'damaging',
            'hurtful', 'painful', 'agonizing', 'excruciating', 'unbearable', 'intolerable',
            'insufferable', 'unacceptable', 'unforgivable', 'inexcusable', 'deplorable',
            'despicable', 'contemptible', 'disgusting', 'revolting', 'repulsive', 'nauseating',
            'sickening', 'appalling', 'shocking', 'horrifying', 'terrifying', 'frightening',
            'scary', 'intimidating', 'threatening', 'menacing', 'ominous', 'sinister',
            'evil', 'wicked', 'malicious', 'malevolent', 'vicious', 'cruel', 'brutal',
            'savage', 'ruthless', 'merciless', 'heartless', 'cold', 'callous', 'insensitive',
            'uncaring', 'indifferent', 'apathetic', 'lifeless', 'dead', 'empty', 'hollow',
            'vacant', 'void', 'barren', 'desolate', 'bleak', 'grim', 'dark', 'gloomy',
            'depressing', 'dismal', 'dreary', 'dull', 'boring', 'tedious', 'monotonous',
            'repetitive', 'tiresome', 'wearisome', 'exhausting', 'draining', 'depleting',
            'weakening', 'debilitating', 'crippling', 'paralyzing', 'devastating', 'crushing',
            'overwhelming', 'overpowering', 'suffocating', 'stifling', 'oppressive',
            'restrictive', 'limiting', 'constraining', 'confining', 'trapping', 'imprisoning',
            'enslaving', 'binding', 'tying', 'holding', 'gripping', 'clutching', 'grasping',
            'clinging', 'possessive', 'controlling', 'dominating', 'manipulating', 'exploiting',
            'abusing', 'mistreating', 'neglecting', 'abandoning', 'deserting', 'forsaking',
            'betraying', 'deceiving', 'lying', 'cheating', 'stealing', 'robbing', 'stealing',
            'taking', 'grabbing', 'seizing', 'snatching', 'destroying', 'ruining', 'damaging',
            'breaking', 'shattering', 'crushing', 'smashing', 'demolishing', 'annihilating',
            'obliterating', 'erasing', 'eliminating', 'removing', 'deleting', 'canceling',
            'stopping', 'halting', 'preventing', 'blocking', 'obstructing', 'hindering',
            'impeding', 'interfering', 'disrupting', 'disturbing', 'interrupting', 'breaking',
            'splitting', 'dividing', 'separating', 'isolating', 'alienating', 'excluding',
            'rejecting', 'refusing', 'denying', 'declining', 'dismissing', 'ignoring',
            'overlooking', 'neglecting', 'disregarding', 'forgetting', 'losing', 'misplacing',
            'missing', 'lacking', 'wanting', 'needing', 'requiring', 'demanding', 'expecting',
            'hoping', 'wishing', 'longing', 'yearning', 'craving', 'desiring', 'wanting',
            'seeking', 'searching', 'looking', 'hunting', 'chasing', 'pursuing', 'following',
            'tracking', 'trailing', 'stalking', 'shadowing', 'watching', 'observing',
            'monitoring', 'supervising', 'controlling', 'managing', 'directing', 'guiding',
            'leading', 'commanding', 'ordering', 'instructing', 'telling', 'forcing',
            'compelling', 'pressuring', 'pushing', 'pulling', 'dragging', 'hauling',
            'carrying', 'lifting', 'raising', 'lowering', 'dropping', 'falling', 'collapsing',
            'crashing', 'failing', 'losing', 'defeated', 'beaten', 'conquered', 'overcome',
            'overpowered', 'overwhelmed', 'outnumbered', 'outmatched', 'outclassed',
            'inferior', 'substandard', 'inadequate', 'insufficient', 'lacking', 'deficient',
            'incomplete', 'imperfect', 'flawed', 'faulty', 'broken', 'damaged', 'ruined',
            'spoiled', 'corrupted', 'contaminated', 'polluted', 'dirty', 'filthy', 'messy',
            'disorganized', 'chaotic', 'confused', 'unclear', 'vague', 'ambiguous',
            'uncertain', 'doubtful', 'questionable', 'suspicious', 'dubious', 'unreliable',
            'untrustworthy', 'dishonest', 'deceptive', 'misleading', 'false', 'fake',
            'artificial', 'synthetic', 'unnatural', 'forced', 'strained', 'tense', 'tight',
            'restricted', 'limited', 'constrained', 'bound', 'tied', 'locked', 'trapped',
            'stuck', 'frozen', 'immobilized', 'paralyzed', 'helpless', 'powerless', 'weak'
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
    
    def analyze_mathematical_concepts(self, text: str) -> Dict[str, Any]:
        """
        Analyze mathematical concepts and shape-related content with enhanced understanding.
        
        Why: Provide comprehensive mathematical shape detection for Clever's cognitive evolution
        Where: Used by enhanced process_text() for mathematical understanding and shape generation
        How: Advanced pattern matching with confidence scoring and educational topic analysis
        
        Returns:
            Dictionary containing mathematical intent, detected shapes, topics, and parameters
        """
        lowered_text = text.lower()
        
        # Detect mathematical intent
        mathematical_keywords = set()
        for category_name, category_shapes in self.shape_vocabulary.items():
            for shape_name, shape_terms in category_shapes.items():
                for term in shape_terms:
                    if term in lowered_text:
                        mathematical_keywords.add(term)
        
        # Check action words
        for action_name, action_terms in self.shape_actions.items():
            for term in action_terms:
                if term in lowered_text:
                    mathematical_keywords.add(term)
        
        # Detect mathematical topics
        detected_topics = []
        for topic_name, topic_keywords in self.mathematical_topics.items():
            relevance_score = 0
            matched_keywords = []
            for keyword in topic_keywords:
                if keyword in lowered_text:
                    relevance_score += 1
                    matched_keywords.append(keyword)
            
            if relevance_score > 0:
                detected_topics.append({
                    'topic': topic_name,
                    'relevance': relevance_score / len(topic_keywords),
                    'keywords': matched_keywords
                })
        
        # Shape detection with confidence scoring
        detected_shapes = []
        for category_name, category_shapes in self.shape_vocabulary.items():
            for shape_name, shape_terms in category_shapes.items():
                confidence = 0
                for term in shape_terms:
                    if term in lowered_text:
                        # Weight longer terms higher
                        confidence += len(term) / 10.0
                
                if confidence > 0:
                    detected_shapes.append({
                        'name': shape_name,
                        'category': category_name,
                        'confidence': min(confidence, 1.0)
                    })
        
        # Sort shapes by confidence
        detected_shapes.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Extract numerical parameters
        import re
        parameters = {}
        
        # Look for numerical values with context
        number_patterns = [
            (r'(\d+(?:\.\d+)?)\s*(?:sided|sides)', 'sides'),
            (r'(\d+(?:\.\d+)?)\s*(?:iterations?|iter)', 'iterations'),
            (r'(\d+(?:\.\d+)?)\s*(?:turns?)', 'turns'),
            (r'(\d+(?:\.\d+)?)\s*(?:points?)', 'points'),
            (r'(\d+(?:\.\d+)?)\s*(?:angles?)', 'angles')
        ]
        
        for pattern, param_name in number_patterns:
            matches = re.findall(pattern, lowered_text)
            if matches:
                try:
                    value = float(matches[-1])  # Take last match
                    if value == int(value):
                        value = int(value)
                    parameters[param_name] = value
                except ValueError:
                    pass
        
        # Calculate mathematical intent and complexity
        has_mathematical_intent = len(mathematical_keywords) > 0 or len(detected_shapes) > 0
        
        # Complexity score based on various factors
        complexity_factors = {
            'vocabulary_diversity': len(mathematical_keywords) / max(1, len(text.split())) * 0.3,
            'shape_complexity': len(detected_shapes) / 10.0 * 0.3,
            'topic_breadth': len(detected_topics) / 5.0 * 0.2,
            'parameter_usage': len(parameters) / 3.0 * 0.2
        }
        
        complexity_score = min(sum(complexity_factors.values()), 1.0)
        
        # Primary shape selection
        primary_shape = None
        if detected_shapes:
            primary_shape = {
                'name': detected_shapes[0]['name'],
                'category': detected_shapes[0]['category'], 
                'confidence': detected_shapes[0]['confidence']
            }
        
        return {
            'mathematical_intent': has_mathematical_intent,
            'complexity_score': round(complexity_score, 2),
            'detected_shapes': detected_shapes,
            'primary_shape': primary_shape,
            'mathematical_topics': detected_topics,
            'extracted_parameters': parameters,
            'mathematical_keywords': list(mathematical_keywords)
        }


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

    def analyze_mathematical_concepts(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for mathematical shapes and geometric concepts.
        
        Why: Enables Clever's cognitive evolution toward mathematical understanding
              and precise geometric concept recognition for enhanced shape generation
        Where: Called by process_text() to detect mathematical intents and concepts
        How: Uses enhanced vocabulary matching and context analysis for shape detection
        
        Args:
            text: Input text to analyze for mathematical concepts
            
        Returns:
            Dictionary containing detected shapes, mathematical topics, action intents,
            confidence scores, and educational concept mappings
            
        Connects to:
            - persona.py: Detected shapes trigger mathematical response generation
            - shape_generator.py: Shape detection drives precise coordinate generation
            - evolution_engine.py: Mathematical concept learning and cognitive growth
        """
        text_lower = text.lower().strip()
        
        # Detect mathematical shapes with confidence scoring
        detected_shapes = []
        shape_confidence = {}
        
        for category, shape_dict in self.shape_vocabulary.items():
            for shape_name, synonyms in shape_dict.items():
                matches = 0
                for synonym in synonyms:
                    if synonym in text_lower:
                        matches += 1
                
                if matches > 0:
                    # Calculate confidence based on matches and context
                    confidence = min(1.0, matches / len(synonyms) + 0.3)
                    detected_shapes.append({
                        'shape': shape_name,
                        'category': category,
                        'confidence': confidence,
                        'matches': matches
                    })
                    shape_confidence[shape_name] = confidence
        
        # Detect mathematical action intents
        detected_actions = []
        for action_type, verbs in self.shape_actions.items():
            for verb in verbs:
                if verb in text_lower:
                    detected_actions.append({
                        'action': action_type,
                        'verb': verb,
                        'confidence': 0.8 if verb in text_lower.split() else 0.5
                    })
        
        # Detect mathematical topics and concepts
        detected_topics = []
        for topic_category, keywords in self.mathematical_topics.items():
            topic_matches = []
            for keyword in keywords:
                if keyword in text_lower:
                    topic_matches.append(keyword)
            
            if topic_matches:
                detected_topics.append({
                    'topic': topic_category,
                    'keywords': topic_matches,
                    'relevance': len(topic_matches) / len(keywords)
                })
        
        # Determine primary shape intent (highest confidence)
        primary_shape = None
        if detected_shapes:
            primary_shape = max(detected_shapes, key=lambda x: x['confidence'])
        
        # Determine if this is a mathematical query
        is_mathematical = (
            len(detected_shapes) > 0 or
            len(detected_topics) > 0 or
            any(word in text_lower for word in ['math', 'calculate', 'geometric', 'formula'])
        )
        
        # Calculate overall mathematical complexity
        complexity_score = 0.0
        if detected_shapes:
            complexity_score += len(detected_shapes) * 0.3
        if detected_topics:
            complexity_score += sum(t['relevance'] for t in detected_topics) * 0.4
        if detected_actions:
            complexity_score += len(detected_actions) * 0.2
        complexity_score = min(1.0, complexity_score)
        
        # Extract numerical parameters for shape generation
        numerical_params = {}
        
        # Look for side counts (3-sided, 12 sides, etc.)
        side_matches = re.findall(r'(\d+)[-\s]*side[ds]?', text_lower)
        if side_matches:
            numerical_params['sides'] = int(side_matches[0])
        
        # Look for iteration counts (3 iterations, 4 levels, etc.)
        iteration_matches = re.findall(r'(\d+)\s*(iteration|level|step)s?', text_lower)
        if iteration_matches:
            numerical_params['iterations'] = int(iteration_matches[0][0])
        
        # Look for turn counts (3.5 turns, 2 rotations, etc.)
        turn_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(turn|rotation)s?', text_lower)
        if turn_matches:
            numerical_params['turns'] = float(turn_matches[0][0])
        
        return {
            'detected_shapes': detected_shapes,
            'primary_shape': primary_shape,
            'shape_confidence': shape_confidence,
            'detected_actions': detected_actions,
            'detected_topics': detected_topics,
            'is_mathematical': is_mathematical,
            'complexity_score': complexity_score,
            'numerical_params': numerical_params,
            'shape_intent_strength': len(detected_shapes) * 0.4 + len(detected_actions) * 0.3
        }

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