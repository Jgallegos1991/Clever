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
        """
        Generate a reply given input text, mode, optional chat history, and context.
        """
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

        # Example proactive suggestion: if user asks for files or code but no snippets returned
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
        """
        Balanced tone for Auto mode.  Summarize intent and offer help.
        """
        parts = [f"Sure, let me think about “{text.strip()}.”"]

        if context:
            ctx_parts = []
            for k in ["project", "goal", "deadline", "priority"]:
                val = context.get(k)
                if val:
                    ctx_parts.append(f"{k}: {val}")
            if ctx_parts:
                parts.append("Context: " + "; ".join(ctx_parts))

        if history:
            parts.append("I’ll also take your recent messages into account.")

        return " ".join(parts)

    def _creative_style(self,
                        text: str,
                        keywords: List[str],
                        context: Dict[str, Any],
                        history: List[Dict[str, Any]]) -> str:
        """
        Creative tone.  Encourage brainstorming and imaginative twists.
        """
        intro = "✨ Let’s get creative! "
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
        """
        Deep Dive tone.  Break down problems systematically.
        """
        parts = ["Let’s dive deeper. Here’s a quick analysis:"]

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
        """
        Supportive tone.  Empathize and encourage.
        """
        parts = ["I'm here for you."]

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
        """
        Quick, direct responses.  Minimal fluff.
        """
        return f"Got it — “{text.strip()}.” I’m on it."

# Instantiate a global persona engine for use in app.py
persona_engine = PersonaEngine()
