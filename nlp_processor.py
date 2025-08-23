import nltk
import spacy
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from collections import defaultdict, Counter
from datetime import datetime
import os

# Import the "Command Spotter" from our other module
import core_nlp_logic

# --- NLTK DATA MANAGEMENT ---
NLTK_DATA_PATH = os.path.join(os.path.expanduser('~'), 'nltk_data')
if not os.path.exists(NLTK_DATA_PATH):
    os.makedirs(NLTK_DATA_PATH)
nltk.data.path.append(NLTK_DATA_PATH)

def _download_nltk_data():
    """Checks for and downloads necessary NLTK corpora to a persistent location."""
    nltk_packages = ["vader_lexicon", "punkt", "punkt_tab", "stopwords"]
    for package in nltk_packages:
        try:
            # A more robust check for different data types
            if package == "vader_lexicon":
                nltk.data.find('sentiment/vader_lexicon')
            elif package == "punkt":
                nltk.data.find('tokenizers/punkt')
            elif package == "punkt_tab":
                nltk.data.find('tokenizers/punkt_tab')
            elif package == "stopwords":
                nltk.data.find('corpora/stopwords')
        except LookupError:
            print(f"Downloading missing NLTK data: {package}...")
            nltk.download(package, quiet=True, download_dir=NLTK_DATA_PATH)
            print(f"NLTK data '{package}' downloaded.")

class UnifiedNLPProcessor:
    def __init__(self):
        _download_nltk_data()
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.sia = SentimentIntensityAnalyzer()
            self.stop_words = set(stopwords.words('english'))
            print("✅ Unified NLP models loaded successfully")
        except Exception as e:
            print(f"❌ Error loading NLP models: {e}")
            self.nlp = None
            self.sia = None
            self.stop_words = set()
        # Lightweight emotion lexicon (compact, no external downloads)
        # Categories: joy, sadness, anger, fear, trust, surprise, disgust, anticipation
        self.emotion_lexicon = {
            'joy': {
                'happy','joy','delight','pleased','glad','excited','grateful','love','lovely','wonderful','awesome','great','amazing'
            },
            'sadness': {
                'sad','unhappy','down','depressed','melancholy','lonely','sorry','regret','mourning','tearful','disappointed'
            },
            'anger': {
                'angry','mad','furious','irritated','annoyed','outraged','resentful','hate','hating','rage','frustrated','upset'
            },
            'fear': {
                'afraid','scared','fear','terrified','anxious','nervous','worried','panic','alarmed','frightened','concerned'
            },
            'trust': {
                'trust','secure','confident','reliable','dependable','faith','assure','assured','support','supported','safe'
            },
            'surprise': {
                'surprised','astonished','amazed','startled','whoa','wow','unexpected','shocked','suddenly','gasp'
            },
            'disgust': {
                'disgust','gross','nasty','revolting','repulsed','ugh','yuck','vile','dislike','horrible','awful'
            },
            'anticipation': {
                'anticipate','expect','hope','eager','ready','waiting','soon','upcoming','looking forward','prepare','planning'
            }
        }

    def process(self, text):
        """
        Provides a comprehensive NLP analysis, now orchestrated with core_nlp_logic.
        """
        if not text or not self.nlp:
            return {"error": "Invalid input or NLP not loaded"}

        # 1) Core intent spotting (commands, questions)
        core_analysis = core_nlp_logic.process_text(self.nlp, text) or {}
        core_intent = core_analysis.get('intent')
        is_core_command = bool(core_intent) and core_intent not in ['chat', 'error', 'small_talk_greeting']

        # 2) Full NLP analysis
        doc = self.nlp(text)
        tokens = [token.text for token in doc]
        
        # 3) Determine the final intent
        final_intent = []
        if is_core_command:
            # Prioritize the specific command intent.
            final_intent = [core_intent]
        else:
            # If no command, use the broader intent detection.
            # We also check the core_analysis for a greeting.
            if core_intent == 'small_talk_greeting':
                final_intent = ['greeting']
            else:
                final_intent = self._detect_general_intent(text)

        # 3b) Enrich with keyphrases and emotions
        keyphrases = self._extract_keyphrases_rake(text)
        emotions = self._detect_emotions(text)
        primary_emotion = max(emotions, key=emotions.get) if emotions else None

        analysis = {
            "original_text": text,
            "timestamp": datetime.now().isoformat(),
            "tokens": tokens,
            "sentiment": self._analyze_sentiment(text),
            "entities": self._extract_entities(doc),
            "intent": final_intent,
            "keywords": self._extract_keywords(doc),
            "top_phrases": keyphrases[:7],
            "emotions": emotions,
            "primary_emotion": primary_emotion,
            "language_stats": self._get_language_stats(text),
            "response_suggestions": self._generate_response_suggestions(text),
            "core_data": core_analysis.get('data') if is_core_command else None
        }
        
        # This part remains for a specific UI feature
        if "shape_request" in analysis["intent"]:
            analysis['action'] = 'form_shape'
            analysis['shape_to_form'] = self._extract_shape(text)
        else:
            analysis['action'] = 'general_chat'
            
        return analysis

    def _extract_shape(self, text):
        """Extracts the name of a known shape from text."""
        shape_keywords = ['cube', 'sphere', 'pyramid', 'knot', 'torus', 'ring']
        text_lower = text.lower()
        for shape in shape_keywords:
            if shape in text_lower:
                return shape
        return None

    def _analyze_sentiment(self, text):
        if not self.sia:
            return {"error": "Sentiment Analyzer not loaded"}
        vader_scores = self.sia.polarity_scores(text)
        blob = TextBlob(text)
        return {
            "vader": vader_scores,
            "textblob": {"polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity},
            "overall_mood": self._determine_mood(vader_scores['compound'], blob.sentiment.polarity)
        }

    def _extract_entities(self, doc): # Now accepts a spaCy doc
        if not doc: return []
        return [{"text": ent.text, "label": ent.label_, "description": spacy.explain(ent.label_)} for ent in doc.ents]

    def _detect_general_intent(self, text): # Renamed for clarity
        text_lower = text.lower()
        intents = {
            "shape_request": ["form", "create", "make", "build", "generate a shape"],
            "question": ["what", "how", "why", "when", "where", "who", "?"],
            "request": ["please", "can you", "could you", "would you", "help"],
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "yo", "sup"],
            "goodbye": ["bye", "goodbye", "see you", "farewell"],
            "complaint": ["problem", "issue", "wrong", "error", "bug", "broken"],
            "compliment": ["great", "awesome", "excellent", "good job", "thank you"],
            "code_request": ["code", "program", "script", "function", "class"],
            "explanation": ["explain", "tell me about", "what is", "how does"]
        }
        detected = [intent for intent, keywords in intents.items() if any(keyword in text_lower for keyword in keywords)]
        return detected if detected else ["general"]

    def _extract_keywords(self, doc): # Now accepts a spaCy doc
        if not doc: return []
        return [{"word": token.text, "lemma": token.lemma_, "pos": token.pos_} for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN'] and not token.is_stop and not token.is_punct and len(token.text) > 2]

    def _extract_keyphrases_rake(self, text):
        """Simple RAKE-like keyphrase extraction without external deps.
        1) Split text into candidate phrases on stopwords/punct
        2) Score words by degree/frequency
        3) Score phrases as sum of word scores
        Returns ranked phrases (lowercased), deduped.
        """
        try:
            # Tokenize words and sentences
            sw = self.stop_words or set(stopwords.words('english'))
            # Use a regex to split on stopwords or non-word characters
            words = [w.lower() for w in word_tokenize(text)]
            separators = set(list(sw))
            # Build candidate phrases: contiguous non-stopword sequences
            phrases = []
            current = []
            for w in words:
                if re.match(r"^\W+$", w) or w in sw:
                    if current:
                        phrases.append(current)
                        current = []
                else:
                    current.append(w)
            if current:
                phrases.append(current)

            # Compute word degree (co-occurrence) and frequency
            freq = Counter()
            degree = Counter()
            for ph in phrases:
                unique = set(ph)
                for w in ph:
                    freq[w] += 1
                    # degree counts co-occurrence with others in phrase
                    degree[w] += (len(unique) - 1)
            # Word score = (degree + freq) / freq
            word_score = {}
            for w in freq:
                word_score[w] = (degree[w] + freq[w]) / float(freq[w])

            # Phrase score = sum(word scores)
            phrase_scores = []
            for ph in phrases:
                if not ph: continue
                # Filter very short phrases
                if len(" ".join(ph)) < 4: continue
                score = sum(word_score.get(w, 0) for w in ph)
                phrase_scores.append((" ".join(ph), score))

            # Rank and dedupe while preserving order
            phrase_scores.sort(key=lambda x: x[1], reverse=True)
            seen = set()
            ranked = []
            for ph, _ in phrase_scores:
                if ph in seen: continue
                seen.add(ph)
                ranked.append(ph)
            return ranked
        except Exception:
            return []

    def _detect_emotions(self, text):
        """Lightweight lexicon-based emotion scoring. Returns normalized scores 0..1."""
        try:
            tokens = [t.lower() for t in word_tokenize(text)]
            scores = defaultdict(int)
            total_hits = 0
            for emo, vocab in self.emotion_lexicon.items():
                for t in tokens:
                    # match exact words; also allow simple bigrams in vocab
                    if ' ' in t:
                        continue
                    if t in vocab:
                        scores[emo] += 1
                        total_hits += 1
            # Normalize
            if total_hits > 0:
                for k in list(scores.keys()):
                    scores[k] = round(scores[k] / total_hits, 3)
            else:
                # default neutral distribution
                for emo in self.emotion_lexicon.keys():
                    scores[emo] = 0.0
            return dict(scores)
        except Exception:
            return {emo: 0.0 for emo in self.emotion_lexicon.keys()}

    def _get_language_stats(self, text):
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        if not words: return {"word_count": 0, "sentence_count": 0, "avg_word_length": 0, "complexity_score": 0}
        return {
            "word_count": len(words), "sentence_count": len(sentences),
            "avg_word_length": sum(len(w) for w in words) / len(words),
            "complexity_score": self._calculate_complexity(text, words, sentences)
        }

    def _calculate_complexity(self, text, words, sentences):
        if not words or not sentences: return 0
        avg_word_len = sum(len(w) for w in words) / len(words)
        words_per_sentence = len(words) / len(sentences)
        # Simplified complexity score
        complexity = (avg_word_len * 0.4) + (words_per_sentence * 0.6)
        # Normalize to a 0-1 scale, assuming a max complexity score of around 20 for this calculation
        return min(complexity / 20, 1.0)

    def _determine_mood(self, vader_compound, textblob_polarity):
        avg_sentiment = (vader_compound + textblob_polarity) / 2.0
        if avg_sentiment >= 0.2: return "positive"
        elif avg_sentiment <= -0.2: return "negative"
        else: return "neutral"

    def _generate_response_suggestions(self, text):
        sentiment = self._analyze_sentiment(text)
        intent = self._detect_general_intent(text)
        suggestions = []
        if sentiment["overall_mood"] == "positive": suggestions.append("Respond with enthusiasm")
        elif sentiment["overall_mood"] == "negative": suggestions.append("Respond with empathy")
        if "question" in intent: suggestions.append("Provide a detailed answer")
        if "code_request" in intent: suggestions.append("Offer to write code")
        if "greeting" in intent: suggestions.append("Respond with a friendly greeting")
        return suggestions

    def get_smart_response_context(self, text):
        analysis = self.process(text)
        return {
            "user_mood": analysis["sentiment"]["overall_mood"],
            "primary_intent": analysis["intent"][0] if analysis["intent"] else "general",
            "key_topics": [kw["word"] for kw in analysis["keywords"][:5]],
            "complexity_level": analysis["language_stats"]["complexity_score"],
            "response_tone": self._suggest_response_tone(analysis),
            "suggested_actions": analysis["response_suggestions"],
            "primary_emotion": analysis.get("primary_emotion"),
            "top_phrases": analysis.get("top_phrases", [])[:5]
        }

    def _suggest_response_tone(self, analysis):
        """Suggests a response tone based on the overall analysis."""
        mood = analysis["sentiment"].get("overall_mood", "neutral")
        intent = analysis["intent"][0] if analysis["intent"] else "general"

        if intent == "complaint":
            return "reassuring_and_formal"
        if mood == "negative":
            return "empathetic_and_supportive"
        if intent == "compliment" or mood == "positive":
            return "warm_and_casual"
        if intent in ["code_request", "explanation"] and analysis["language_stats"]["complexity_score"] > 0.5:
            return "technical_and_precise"
        if intent == "question":
            return "informative_and_clear"
        
        return "neutral_and_helpful"

# Do not instantiate at import time to avoid duplicate model loads