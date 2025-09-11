# persona.py — Clever Persona Engine (offline‑only, Jay‑specific)
from __future__ import annotations

from types import SimpleNamespace
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import your NLP helper (lazy-loaded spaCy + sentiment)
from nlp_processor import nlp_processor

logger = logging.getLogger(__name__)

class PersonaResponse(SimpleNamespace):
    """
    Simple container for persona responses.  Fields:
      text: str              -> The assistant’s reply
      mode: str              -> The mode used (Auto, Creative, Deep Dive, Support, Quick Hit)
      sentiment: float       -> Sentiment score of the user’s input [-1.0, 1.0]
      proactive_suggestions: List[str] -> Suggestions appended to reply (if any)
      quality_score: Optional[float]    -> Reserved for future scoring
    """
    text: str
    mode: str
    sentiment: float
    proactive_suggestions: List[str]
    quality_score: Optional[float] = None

class PersonaEngine:
    """
    Persona engine for Clever.  Each mode has a style function and an optional
    suggestion generator.  This engine never calls external services—everything
    runs locally via the nlp_processor and simple heuristics.
    """
    def __init__(self, name: str = "Clever", owner: str = "Jay") -> None:
        self.name = name
        self.owner = owner
        self.modes = {
            "Auto": self._auto_style,
            "Creative": self._creative_style,
            "Deep Dive": self._deep_dive_style,
            "Support": self._support_style,
            "Quick Hit": self._quick_hit_style,
        }

    def generate(self,
                 text: str,
                 mode: str = "Auto",
                 history: Optional[List[Dict[str, Any]]] = None,
                 context: Optional[Dict[str, Any]] = None) -> PersonaResponse:
        """Generate a reply given input text, mode, optional chat history, and context."""
        if not text:
            return PersonaResponse(text="", mode=mode, sentiment=0.0, proactive_suggestions=[])

        history = history or []
        context = context or {}

        # Compute sentiment once via NLP
        nlp_res = nlp_processor.process(text)
        sentiment = nlp_res.sentiment
        keywords = nlp_res.keywords

        # Select style function; default to Auto if unknown
        style_fn = self.modes.get(mode, self._auto_style)

        # Build reply text and suggestions
        reply = style_fn(text, keywords, context, history)
        suggestions: List[str] = []

        # Proactive suggestion example
        if mode == "Auto" and any(w in text.lower() for w in ["file", "code", "project"]) and not suggestions:
            suggestions.append("I can search your files for more details. Try describing your problem or code.")

        return PersonaResponse(
            text=reply,
            mode=mode,
            sentiment=sentiment,
            proactive_suggestions=suggestions,
            quality_score=None,
        )

    # --------- Mode Styles ---------

    def _auto_style(self,
                    text: str,
                    keywords: List[str],
                    context: Dict[str, Any],
                    history: List[Dict[str, Any]]) -> str:
        """Balanced and useful: reflect + next steps + ask follow-up."""
        t = text.strip()
        parts = [f"Got it — {t}."]
        # Quick actionable next-step suggestions from keywords
        if keywords:
            parts.append("We can tackle it like this:")
            steps = []
            for k in keywords[:3]:
                steps.append(f"• Focus on {k}")
            parts.append("\n".join(steps))
        parts.append("Want me to go quick or dive deeper?")
        return " ".join(parts)

    def _creative_style(self,
                        text: str,
                        keywords: List[str],
                        context: Dict[str, Any],
                        history: List[Dict[str, Any]]) -> str:
        """Creative tone. Encourage brainstorming and imaginative twists."""
        intro = "✨ Let’s get creative. "
        idea = f"Imagine “{text.strip()}” as part of a story or design. "
        if keywords:
            idea += f"We could weave in themes like {', '.join(keywords[:3])}. "
        if context.get("goal"):
            idea += f"All while staying true to your goal of {context['goal']}."
        return intro + idea

    def _deep_dive_style(self,
                         text: str,
                         keywords: List[str],
                         context: Dict[str, Any],
                         history: List[Dict[str, Any]]) -> str:
        """Deep Dive tone. Break down problems systematically."""
        parts = ["Let’s dive deeper. Quick analysis:"]

        if keywords:
            parts.append("Key topics: " + ", ".join(keywords[:5]) + ".")
        if context:
            ctx_parts = []
            for k in ["project", "goal"]:
                if context.get(k):
                    ctx_parts.append(f"{k}: {context[k]}")
            if ctx_parts:
                parts.append("Context – " + "; ".join(ctx_parts) + ".")
        parts.append("Feel free to ask follow‑up questions or provide more details.")
        return " ".join(parts)

    def _support_style(self,
                       text: str,
                       keywords: List[str],
                       context: Dict[str, Any],
                       history: List[Dict[str, Any]]) -> str:
        """Supportive tone. Empathize and encourage."""
        parts = ["I’m here for you."]

        if any(w in text.lower() for w in ["stress", "overwhelm", "can’t", "stuck", "help"]):
            parts.append("It sounds like you're facing a challenge—remember it's okay to take it slow.")
        if context.get("goal"):
            parts.append(f"You're working towards {context['goal']}, and that’s admirable.")
        parts.append("How can I assist further?")
        return " ".join(parts)

    def _quick_hit_style(self,
                         text: str,
                         keywords: List[str],
                         context: Dict[str, Any],
                         history: List[Dict[str, Any]]) -> str:
        """Quick, direct responses. Minimal fluff."""
        return f"On it — {text.strip()}."

# Instantiate a global persona engine for use in app.py
persona_engine = PersonaEngine()

class CleverPersona:
    """
    Main persona class that integrates with NLP processor and database manager.
    This is the interface expected by app.py.
    """
    
    def __init__(self, nlp_processor, db_manager):
        """Initialize CleverPersona with NLP processor and database manager."""
        self.nlp_processor = nlp_processor
        self.db_manager = db_manager
        self.persona_engine = PersonaEngine(name="Clever", owner="Jay")
        self.last_used_trait = "core"  # Default trait
        
    def generate_response(self, analysis):
        """Generate a response based on provided analysis (dict or namespace).

        Accepts either a dict from app.py or a SimpleNamespace. Uses the original
        user text, enriches with local NLP when needed, and crafts a concise,
        helpful reply in the selected mode.
        """
        # Normalize analysis into a dict
        a = analysis
        if hasattr(a, '__dict__'):
            a = vars(a)
        if not isinstance(a, dict):
            a = {}

        user_text = (a.get('user_input') or '').strip()
        # Pull keywords/sentiment from analysis or compute locally
        kws = list(a.get('keywords') or [])
        sent = a.get('sentiment')
        if user_text and (not kws or sent is None):
            try:
                n = nlp_processor.process(user_text)
                if not kws:
                    kws = list(getattr(n, 'keywords', []) or [])
                if sent is None:
                    sent = float(getattr(n, 'sentiment', 0.0) or 0.0)
            except Exception:
                sent = float(sent or 0.0)
        if sent is None:
            sent = 0.0

        # Determine mode from sentiment/keywords
        mode = self._determine_mode(sent, kws)
        # Map mode to visual trait for the renderer
        trait_map = {
            "Support": "Calm",
            "Creative": "Excited",
            "Deep Dive": "Analytical",
            "Quick Hit": "Base",
            "Auto": "Base",
        }
        trait = trait_map.get(mode, "Base")
        if trait == "Base":
            if sent > 0.3:
                trait = "Positive"
            elif sent < -0.3:
                trait = "Negative"
        self.last_used_trait = trait

        # Use original text, not a placeholder
        source_text = user_text or (', '.join(kws) if kws else 'your request')

        # Generate the reply
        response = self.persona_engine.generate(
            text=source_text,
            mode=mode,
            history=[],
            context={},
        )

        # Tighten overly generic outputs by adding a small actionable nudge
        out_text = response.text.strip()
        if user_text and user_text.endswith('?') and 'Let’s' not in out_text and "Let's" not in out_text:
            out_text += " If you can share one detail, I’ll get specific."

        return {
            "text": out_text,
            "mode": response.mode,
            "sentiment": response.sentiment,
            "keywords": kws,
            "proactive_suggestions": response.proactive_suggestions,
        }
    
    def _determine_mode(self, sentiment, keywords):
        """Determine the appropriate mode based on sentiment and keywords."""
        if sentiment < -0.3:
            return "Support"
        if sentiment > 0.5:
            return "Creative"
        if any(word in keywords for word in ["analyze", "deep", "detail", "explain"]):
            return "Deep Dive"
        if any(word in keywords for word in ["quick", "fast", "brief"]):
            return "Quick Hit"
        return "Auto"
