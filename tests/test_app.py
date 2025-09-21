import os
import json
import tempfile
import types
import pytest

import importlib.util
from pathlib import Path

APP_PATH = Path(__file__).resolve().parents[1] / 'app.py'
spec = importlib.util.spec_from_file_location('clever_app', str(APP_PATH))
assert spec is not None and spec.loader is not None
clever_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clever_app)

@pytest.fixture(autouse=True)
def app_client(monkeypatch):
    """
    Set up Flask test client with isolated database for testing.
    
    Why: Provides clean test environment with temporary database to
         prevent test interference and data pollution in main database.
    Where: Pytest fixture automatically applied to all tests in this
           module for consistent test isolation and setup.
    How: Forces testing environment, creates temporary database file
         for database manager, yields configured Flask test client.
    
    Args:
        monkeypatch: Pytest monkeypatch fixture for environment modification
        
    Yields:
        Flask test client configured for isolated testing
    """
    # Force DEBUG off for tests
    monkeypatch.setenv('FLASK_ENV', 'testing')

    # Use a temp db if database manager exists
    if hasattr(clever_app, 'db_manager') and hasattr(clever_app.db_manager, 'db_path'):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        clever_app.db_manager.db_path = tmp.name

    client = clever_app.app.test_client()
    yield client


def test_health(app_client):
    """
    Test health endpoint functionality and response structure validation.
    
    Why: Ensures system health monitoring endpoint works correctly and
         returns expected data structure for monitoring systems.
    Where: Integration test validating /health endpoint used for
           system status monitoring and operational health checks.
    How: Makes GET request to /health, validates HTTP 200 response,
         checks for valid status fields in both minimal and structured formats.
    """
    r = app_client.get('/health')
    assert r.status_code == 200
    data = r.get_json()
    # Accept either minimal health or structured report with overall_status
    ok_minimal = data.get('status') in ('ok', 'error') or 'monitoring' in data
    ok_structured = data.get('overall_status') in ('healthy', 'warning', 'error')
    assert ok_minimal or ok_structured


def test_index(app_client):
    """
    Test main index page loads correctly with expected content.
    
    Why: Validates the primary user interface loads properly and
         contains essential Clever AI branding elements.
    Where: UI integration test ensuring main application page
           renders correctly for user interaction.
    How: Makes GET request to root path, validates HTTP 200 status
         and confirms "Clever" text appears in response content.
    """
    r = app_client.get('/')
    assert r.status_code == 200
    assert b'Clever' in r.data


def test_chat_happy(app_client):
    """
    Test successful chat interaction with valid message input.
    
    Why: Validates core chat functionality works correctly with proper
         message processing and response structure generation.
    Where: Integration test for primary chat API endpoint that handles
           user conversations and NLP analysis operations.
    How: Posts valid chat message, validates HTTP 200 response,
         checks for required response and analysis fields in JSON output.
    """
    r = app_client.post('/chat', json={'message': 'hey clever?'})
    assert r.status_code == 200
    data = r.get_json()
    # Schema returns 'response' and 'analysis' dict plus optional extended fields
    assert 'response' in data and isinstance(data['response'], str)
    assert 'analysis' in data and isinstance(data['analysis'], dict)
    # Extended fields (non-fatal if missing in legacy mode)
    for k in ['approach', 'mood', 'particle_intensity']:
        if k in data:
            assert data[k] is not None
     # Intent key is optional; when present, it should be a string
     if 'intent' in data['analysis'] and data['analysis']['intent'] is not None:
          assert isinstance(data['analysis']['intent'], str)


def test_chat_bad_request(app_client):
    """
    Test chat endpoint error handling with invalid empty message input.
    
    Why: Ensures proper error handling and validation for chat API
         when users submit invalid or empty message content.
    Where: Error validation test for chat endpoint robustness and
           user input validation in conversation processing.
    How: Posts empty message to chat endpoint, validates HTTP 400
         status indicating proper client error response handling.
    """
    r = app_client.post('/chat', json={'message': ''})
    assert r.status_code == 400
    data = r.get_json()
    assert data.get('status') == 'error'
    assert 'error' in data


def test_ingest_form(app_client):
    """
    Test form submission functionality for ingestion endpoint.
    
    Why: Validates form-based data submission works correctly for
         file ingestion and data processing workflows.
    Where: Integration test for form handling in ingestion system
           used for manual data submission and processing.
    How: Posts form data to /ingest endpoint, validates HTTP 200
         response and success message format in JSON response.
    """
    r = app_client.post('/ingest', data={'name': 'jay'})
    assert r.status_code == 200
    data = r.get_json()
    assert data['message'].startswith('Form submitted successfully')
