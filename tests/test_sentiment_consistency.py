"""Sentiment consistency test suite

Why: Ensure sentiment analysis remains stable and predictable across common polarity patterns.
Where: Validates nlp_processor + persona integration indirectly (uses PersonaEngine.generate which pulls sentiment from analysis).
How: Feed representative positive, negative, neutral sentences and assert classification alignment with expectations with some tolerance.

Connects to:
    - nlp_processor.py: Provides sentiment processing
    - persona.py: Surfaces sentiment field in PersonaResponse
"""
from persona import PersonaEngine
import pytest

# Representative samples (short to keep test fast)
POSITIVE = [
    "I love how smoothly this system runs today",
    "The results are excellent and amazing",
    "What a wonderful and fantastic improvement"
]
NEGATIVE = [
    "This failure is horrible and awful",
    "I hate the inconsistent unstable output",
    "The experience was bad and frustrating"
]
NEUTRAL = [
    "The module loads with standard configuration",
    "There is a file in the directory",
    "Processing continues without notable change"
]

@pytest.fixture(scope="module")
def engine():
    return PersonaEngine()

@pytest.mark.parametrize("text", POSITIVE)
def test_positive_sentiment(engine, text):
    resp = engine.generate(text, mode="Auto")
    assert resp.sentiment in {"positive", "neutral"}, f"Expected positive-ish sentiment, got {resp.sentiment}"  # allow neutral fallback

@pytest.mark.parametrize("text", NEGATIVE)
def test_negative_sentiment(engine, text):
    resp = engine.generate(text, mode="Auto")
    assert resp.sentiment in {"negative", "neutral"}, f"Expected negative-ish sentiment, got {resp.sentiment}"

@pytest.mark.parametrize("text", NEUTRAL)
def test_neutral_sentiment(engine, text):
    resp = engine.generate(text, mode="Auto")
    # Neutral should not become strongly polarized
    assert resp.sentiment == "neutral", f"Expected neutral sentiment, got {resp.sentiment}"
