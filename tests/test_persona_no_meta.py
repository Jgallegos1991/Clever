from persona import PersonaEngine

META_TOKENS = [
    'Time-of-day:', 'focal lens:', 'Vector:', 'complexity index', 'essence:'
]

def test_persona_generate_no_meta_tokens():
    """Ensure persona.generate does not emit internal meta reasoning markers.

    Why: Prevent leakage of internal reasoning or telemetry phrases into user-visible text
    Where: Guards the persona layer itself so upstream changes don't reintroduce leakage
    How: Generate a sample response and assert banned substrings absent (case-insensitive)
    """
    p = PersonaEngine()
    resp = p.generate("Quick hello test", mode="Auto")
    text = resp.text.lower()
    for token in META_TOKENS:
        assert token.lower() not in text, f"Meta token leaked: {token} in {resp.text!r}"
    assert resp.text.strip(), "Response should not be empty"
