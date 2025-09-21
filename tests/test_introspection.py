"""Tests for runtime introspection endpoint.

Why: Ensure the new /api/runtime_introspect endpoint surfaces render events and
Why/Where/How route metadata so regressions are caught early.
Where: Part of automated test suite executed in CI along with UI acceptance
checks and docstring coverage enforcement.
How: Uses Flask test client to hit home (trigger a render) then queries
introspection endpoint and validates expected structural keys.
"""
from __future__ import annotations
import json
from typing import Any

import pytest

import app as clever_app


@pytest.fixture
def client():
    """Flask test client fixture.

    Why: Provide isolated app context for endpoint tests.
    Where: Used by all tests in this module.
    How: Yields test_client() from imported app module.
    """
    clever_app.app.config['TESTING'] = True
    with clever_app.app.test_client() as c:
        yield c


def test_runtime_introspect_basic(client):
    """Hit home then introspection; verify last_render template and metadata.

    Why: Confirms render tracing captured the canonical index.html template and
    endpoint snapshot includes expected keys with Why/Where/How present (even if
    empty they should exist).
    Where: Protects the runtime introspection contract used by debug overlay.
    How: Performs sequential requests and asserts JSON structure.
    """
    # Trigger a render
    r = client.get('/')
    assert r.status_code == 200

    ir = client.get('/api/runtime_introspect')
    assert ir.status_code == 200
    data: Any = ir.get_json()
    assert 'last_render' in data
    assert data['last_render'] is not None
    assert data['last_render']['template'] == 'index.html'
    assert 'endpoints' in data and isinstance(data['endpoints'], list)
    # Find the home endpoint rule '/'
    home_meta = next((e for e in data['endpoints'] if e['rule'] == '/'), None)
    assert home_meta, 'Home endpoint metadata missing'
    for key in ('why', 'where', 'how'):
        assert key in home_meta, f"Missing {key} in endpoint meta"
    # New fields: slow flag optional, threshold, warnings list
    assert 'render_threshold_ms' in data
    assert 'warnings' in data
    assert isinstance(data['warnings'], list)
    assert 'reasoning_coverage' in data and isinstance(data['reasoning_coverage'], dict)
    rc = data['reasoning_coverage']
    for k in ('endpoints_total','endpoints_complete','percent'):
        assert k in rc
    if data['last_render']:
        assert 'slow' in data['last_render']


def test_runtime_introspect_reasoning_richness(client):
    """At least one endpoint should expose a non-empty Why section.

    Why: Guards against accidental stripping of docstrings or parsing logic
    regressions that would remove the directional "arrows" between system
    nodes (the purpose of the Why/Where/How design).
    Where: Operates on endpoints snapshot from runtime introspection state.
    How: Fetches /api/runtime_introspect and asserts any endpoint has a
    non-empty Why value after stripping whitespace.
    """
    client.get('/')
    data = client.get('/api/runtime_introspect').get_json()
    endpoints = data.get('endpoints') or []
    assert any((e.get('why') or '').strip() for e in endpoints), 'Expected at least one endpoint with non-empty Why section'


def test_runtime_introspect_schema_keys(client):
    """Validate presence of all top-level schema keys required by overlay.

    Why: Ensures debug overlay (and future tooling) can rely on consistent
    keys to visualize the reasoning map without defensive null checks.
    Where: Checks JSON returned by /api/runtime_introspect.
    How: Simple key existence assertions.
    """
    client.get('/')
    data = client.get('/api/runtime_introspect').get_json()
    for key in ['last_render', 'recent_renders', 'endpoints', 'persona_mode', 'last_error', 'version', 'generated_ts', 'warnings', 'render_threshold_ms', 'evolution', 'reasoning_coverage']:
        assert key in data, f"Missing key {key} in runtime introspection response"


def test_runtime_introspect_evolution_summary(client):
    """Ensure evolution summary keys exist after at least one chat interaction.

    Why: Confirms interaction counts surface in runtime JSON for overlay.
    Where: Evolution summary nested under 'evolution'.
    How: Simulate a chat post then fetch runtime state and assert fields.
    """
    client.post('/chat', json={'message': 'hello clever'})
    data = client.get('/api/runtime_introspect').get_json()
    evo = data.get('evolution')
    # May be None if evolution engine not present, so tolerate None gracefully
    if evo is not None:
        assert 'total_interactions' in evo
        assert 'recent_interactions' in evo


def test_runtime_introspect_includes_version(client):
    """Ensure version dictionary exists even if git hash None.

    Why: Overlay relies on presence of version key for display logic.
    Where: Tests resilience when git repo not available.
    How: Simple key assertions.
    """
    client.get('/')
    ir = client.get('/api/runtime_introspect')
    data = ir.get_json()
    assert 'version' in data and 'git' in data['version']
