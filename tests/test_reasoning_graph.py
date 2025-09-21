"""Test that runtime introspection exposes reasoning_graph with nodes and edges.

Why: Ensure graph backend feature (reasoning + optional concept graph) is present so frontend debug overlay can rely on stable contract.
Where: Part of tests/ executed in CI before deployment; touches /api/runtime_introspect endpoint.
How: Uses Flask test client to query endpoint and assert minimal shape & required keys.
"""
from __future__ import annotations
import importlib


def test_runtime_introspection_reasoning_graph():
    app_module = importlib.import_module('app')
    app = app_module.app  # Flask instance
    client = app.test_client()
    resp = client.get('/api/runtime_introspect')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'reasoning_graph' in data, 'reasoning_graph missing from payload'
    rg = data['reasoning_graph']
    assert isinstance(rg, dict)
    assert 'nodes' in rg and 'edges' in rg
    assert isinstance(rg['nodes'], list) and isinstance(rg['edges'], list)
    # minimal structural expectations
    if rg['nodes']:
        sample = rg['nodes'][0]
        assert 'id' in sample and 'type' in sample
    # concept graph optional
    if 'concept_graph' in data and data['concept_graph']:
        cg = data['concept_graph']
        assert 'nodes' in cg and 'edges' in cg
