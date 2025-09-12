def test_persona_auto_mode_smoke():
    """
    Smoke test for PersonaEngine auto mode functionality.
    
    Why: Validates core PersonaEngine functionality works correctly with
         basic input and returns expected response structure.
    Where: Part of the test suite ensuring PersonaEngine reliability
           for Clever AI's conversation capabilities.
    How: Imports PersonaEngine, generates response in Auto mode,
         validates response structure and content requirements.
    """
    # Import inside test to avoid import-time side effects
    from persona import PersonaEngine

    p = PersonaEngine()
    resp = p.generate("hello there", mode="Auto")

    assert hasattr(resp, "text") and isinstance(resp.text, str)
    assert resp.text != ""
    assert resp.mode == "Auto"
