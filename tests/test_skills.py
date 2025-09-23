"""
Test suite for Clever AI skills and capabilities

Why: Validates core AI capabilities like text summarization and processing
to ensure Clever's skills operate correctly and reliably.
Where: Part of pytest test suite for comprehensive system validation.
How: Tests API endpoints and skill functions with various input scenarios.

Connects to:
    - app.py: Flask application endpoints being tested
    - nlp_processor.py: Natural language processing capabilities
    - persona.py: AI skill integration and response generation
    - pytest: Testing framework and assertions
"""

import importlib.util
from pathlib import Path
import io

APP_PATH = Path(__file__).resolve().parents[1] / 'app.py'
spec = importlib.util.spec_from_file_location('clever_app', str(APP_PATH))
clever_app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(clever_app)


def test_summarize_ok():
    """
    Test successful text summarization API endpoint functionality.
    
    Why: Validates that the /api/summarize endpoint correctly processes
         text input and returns structured summary data.
    Where: Part of integration test suite for Clever AI's API capabilities.
    How: Uses Flask test client to POST text data, validates HTTP 200 response
         and confirms 'summary' field exists in JSON response.
    """
    c = clever_app.app.test_client()
    r = c.post('/api/summarize', json={'text': 'Hello world. This is Clever. Local only.'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'summary' in data


def test_search_empty():
    """
    Test search API endpoint behavior with empty query parameters.
    
    Why: Ensures search functionality gracefully handles empty queries
         without errors and returns appropriate empty results.
    Where: Integration test validating search API robustness and
           edge case handling for Clever AI's search capabilities.
    How: Sends GET request with empty query parameter, validates
         HTTP 200 status and empty list response format.
    """
    c = clever_app.app.test_client()
    r = c.get('/api/search?q=')
    assert r.status_code == 200
    assert r.get_json() == []
