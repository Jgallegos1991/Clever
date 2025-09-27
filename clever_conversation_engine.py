"""Deprecated CleverConversationEngine (stub).

Why:
    The original conversation engine grew extremely large, duplicated logic,
    and introduced persistent lint/syntax issues. We've migrated to
    persona.PersonaEngine as the authoritative response system. This file now
    exists ONLY as an import compatibility shim for any lingering legacy paths.
Where:
    Root of repository; archived full legacy implementation (read‑only) is
    preserved under legacy/clever_conversation_engine.py for reference.
How:
    Provides a minimal class that clearly raises at construction and exposes a
    single safe helper to direct developers toward the supported engine.

Connects to:
    - persona.py: Current, supported persona engine
    - legacy/clever_conversation_engine.py: Archived (do not modify / import)
"""

from __future__ import annotations

from typing import Any, Dict
from datetime import datetime

class CleverConversationEngine:  # pragma: no cover - intentional stub
    """Deprecated legacy engine placeholder.

    Why:
        Prevent accidental runtime use of the deprecated legacy engine while
        keeping import compatibility for old references so refactors can
        proceed incrementally without hard crashes elsewhere.
    Where:
        Imported only by outdated modules or historical tooling. New code must
        construct and use persona.PersonaEngine instead.
    How:
        Raises NotImplementedError on instantiation with a clear migration
        message. Provides a minimal get_dynamic_greeting helper retained
        because some legacy UI code may still call it harmlessly; it returns a
        deterministic structure without side effects.

    Connects to:
        - persona.py: Recommended replacement
        - legacy/clever_conversation_engine.py: Historical reference only
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError(
            "CleverConversationEngine is deprecated. Use persona.PersonaEngine instead."
        )

    @staticmethod
    def get_dynamic_greeting() -> Dict[str, Any]:  # pragma: no cover
        """Return a simple deterministic greeting structure.

        Why:
            Some legacy UI code expected this method; keeping a harmless,
            predictable return avoids KeyErrors while migration completes.
        Where:
            Potentially called in old front-end glue code or tests.
        How:
            Returns a fixed payload with current day-of-week for minimal
            continuity—no randomness, no side effects.
        """
        now = datetime.now()
        return {
            "greeting": f"Hello Jay - {now.strftime('%A')} legacy stub active.",
            "mood": "neutral",
            "energy": 0.0,
            "particle_intensity": 0.0,
            "ui_state": "deprecated",
        }

def deprecated_engine_warning() -> str:  # pragma: no cover
    """Provide guidance string about deprecation.

    Why:
        Centralizes migration messaging so tools or diagnostics can surface
        consistent guidance.
    Where:
        Could be invoked by system validators or migration scripts.
    How:
        Returns a static advisory message.
    """
    return (
        "CleverConversationEngine is deprecated. Use persona.PersonaEngine. "
        "See legacy/clever_conversation_engine.py for archived reference."
    )
