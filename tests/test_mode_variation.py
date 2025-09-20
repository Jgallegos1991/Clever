"""Mode variation & memory metrics tests

Why: Ensure per-mode responses show variation (not identical signatures) and debug memory metrics appear.
Where: Validates persona.generate across multiple modes.
How: Generate two responses per mode and assert differing signatures and presence of debug metrics fields.

Connects to:
    - persona.py: PersonaEngine.generate logic
    - nlp_processor.py: Provides analysis influencing variation
"""
from persona import PersonaEngine

MODES = ["Auto", "Creative", "Deep Dive", "Support", "Quick Hit"]


def _signature(text: str) -> str:
    return text.strip().lower().split('\n', 1)[0][:120]


def test_mode_variation_and_memory_metrics():
    engine = PersonaEngine()
    base_prompt = "Analyze system resilience under load and propose strategies?"
    for mode in MODES:
        r1 = engine.generate(base_prompt, mode=mode)
        r2 = engine.generate(base_prompt, mode=mode)
        assert hasattr(r1, 'debug_metrics'), "debug_metrics missing on first response"
        assert hasattr(r2, 'debug_metrics'), "debug_metrics missing on second response"
        # Variation: allow forced suffix differences; signatures should differ eventually
        assert _signature(r1.text) != _signature(r2.text), f"No variation for mode {mode}"
        dm = r1.debug_metrics
        assert set(['memory_items_considered','memory_items_used','conversation_history_count','predicted_mode_changed']).issubset(dm.keys()), "Missing memory metric fields"
