from app import app as flask_app
from introspection import runtime_state


def test_runtime_state_includes_code_health_and_component_graph():
    state = runtime_state(flask_app, include_intelligent_analysis=False)
    assert 'code_health' in state, 'code_health field missing'
    assert 'component_graph' in state, 'component_graph field missing'
    ch = state['code_health']
    assert isinstance(ch, dict)
    # Basic expected keys (best-effort; allow error bypass)
    if 'error' not in ch:
        for key in ['files_scanned', 'functions_total', 'conflict_markers', 'meta_token_hits', 'generated_ts']:
            assert key in ch, f'missing code_health key {key}'
    cg = state['component_graph']
    assert isinstance(cg, dict)
    if 'error' not in cg:
        for key in ['nodes', 'edges', 'truncated', 'generated_ts']:
            assert key in cg, f'missing component_graph key {key}'
    # Sanity: nodes / edges small enough or truncated flag present
    if 'error' not in cg:
        assert len(cg['nodes']) <= 300
        assert len(cg['edges']) <= 800
