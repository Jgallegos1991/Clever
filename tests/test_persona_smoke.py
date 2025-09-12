def test_persona_auto_mode_smoke():
    # Import inside test to avoid import-time side effects
    from persona import PersonaEngine

    p = PersonaEngine()
    resp = p.generate("hello there", mode="Auto")

    assert hasattr(resp, "text") and isinstance(resp.text, str)
    assert resp.text != ""
    assert resp.mode == "Auto"
