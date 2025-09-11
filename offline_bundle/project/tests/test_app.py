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
    r = app_client.get('/health')
    assert r.status_code == 200
    data = r.get_json()
    # Accept either minimal health or structured report with overall_status
    ok_minimal = data.get('status') in ('ok', 'error') or 'monitoring' in data
    ok_structured = data.get('overall_status') in ('healthy', 'warning', 'error')
    assert ok_minimal or ok_structured


def test_index(app_client):
    r = app_client.get('/')
    assert r.status_code == 200
    assert b'Clever' in r.data


def test_chat_happy(app_client):
    r = app_client.post('/chat', json={'message': 'hey clever?'})
    assert r.status_code == 200
    data = r.get_json()
    # Current schema returns 'response' and 'analysis' dict
    assert 'response' in data and isinstance(data['response'], str)
    assert 'analysis' in data and isinstance(data['analysis'], (dict,))
    # Intent key is optional; when present, it should be a string
    if 'intent' in data['analysis']:
        assert isinstance(data['analysis']['intent'], str)


def test_chat_bad_request(app_client):
    r = app_client.post('/chat', json={'message': ''})
    assert r.status_code == 400


def test_ingest_form(app_client):
    r = app_client.post('/ingest', data={'name': 'jay'})
    assert r.status_code == 200
    data = r.get_json()
    assert data['message'].startswith('Form submitted successfully')
