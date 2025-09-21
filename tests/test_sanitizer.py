import re
from app import _sanitize_persona_text

def test_sanitizer_removes_meta_markers():
    raw = (
        "Noted— you're reflecting on hey— balanced starting point. "
        "Time-of-day: afternoon; focal lens: essence. Vector: 1.15 complexity index. "
        "Earlier we touched on 'clev' which resonates here."
    )
    cleaned = _sanitize_persona_text(raw)
    banned = ["Time-of-day", "focal lens", "Vector:", "complexity index", "essence:"]
    for b in banned:
        assert b.lower() not in cleaned.lower()
    # Should still retain core conversational opening
    assert "balanced starting point" in cleaned
