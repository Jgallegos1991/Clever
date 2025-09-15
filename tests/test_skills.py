import importlib.util
from pathlib import Path
import io

APP_PATH = Path(__file__).resolve().parents[1] / 'app.py'
spec = importlib.util.spec_from_file_location('clever_app', str(APP_PATH))
clever_app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(clever_app)


def test_summarize_ok():
<<<<<<< HEAD
=======
    """
    Test successful text summarization API endpoint functionality.
    
    Why: Validates that the /api/summarize endpoint correctly processes
         text input and returns structured summary data.
    Where: Part of integration test suite for Clever AI's API capabilities.
    How: Uses Flask test client to POST text data, validates HTTP 200 response
         and confirms 'summary' field exists in JSON response.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    c = clever_app.app.test_client()
    r = c.post('/api/summarize', json={'text': 'Hello world. This is Clever. Local only.'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'summary' in data


def test_search_empty():
<<<<<<< HEAD
=======
    """
    Test search API endpoint behavior with empty query parameters.
    
    Why: Ensures search functionality gracefully handles empty queries
         without errors and returns appropriate empty results.
    Where: Integration test validating search API robustness and
           edge case handling for Clever AI's search capabilities.
    How: Sends GET request with empty query parameter, validates
         HTTP 200 status and empty list response format.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    c = clever_app.app.test_client()
    r = c.get('/api/search?q=')
    assert r.status_code == 200
    assert r.get_json() == []
