"""Persona smoke & variability tests.

Why: Ensure core persona generation pipeline produces responses, includes
required metadata, and exhibits variation for repeated inputs (addresses
prior repetition complaints).
Where: Executed by clever-ci.yml test stage; guards against regression in
persona/nlp integration.
How: Instantiate PersonaEngine, generate multiple responses for same
prompt, assert non-empty text, presence of mode/sentiment, and at least
two distinct first lines across attempts.
"""

from persona import PersonaEngine


def test_persona_basic_response():
    p = PersonaEngine()
    resp = p.generate("Explain quantum tunneling briefly?", mode="Auto")
    assert resp.text and isinstance(resp.text, str)
    assert resp.mode in {"Auto", "Creative", "Deep Dive", "Support", "Quick Hit"}
    assert resp.sentiment in {"positive", "negative", "neutral"}


def test_persona_variation():
    p = PersonaEngine()
    prompt = "Explain quantum tunneling briefly?"
    first_lines = set()
    for _ in range(4):
        r = p.generate(prompt, mode="Auto")
        first_line = r.text.splitlines()[0].strip()
        first_lines.add(first_line)
    # Expect at least 2 distinct openings due to variation logic
    assert len(first_lines) >= 2, f"Variation insufficient: {first_lines}"


def test_persona_auto_mode_smoke():
    """Additional smoke test focusing on Auto mode structure.

    Why: Acts as a guardrail for future template changes so CI will flag
    breaking structural changes early.
    Where: Complements variation & basic tests in this module.
    How: Simple assertion set on response fields.
    """
    p = PersonaEngine()
    resp = p.generate("hello there", mode="Auto")
    assert hasattr(resp, "text") and isinstance(resp.text, str) and resp.text
    assert resp.mode == "Auto"
