import importlib.util
from pathlib import Path
import io

APP_PATH = Path(__file__).resolve().parents[1] / 'app.py'
spec = importlib.util.spec_from_file_location('clever_app', str(APP_PATH))
clever_app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(clever_app)


def test_summarize_ok():
    c = clever_app.app.test_client()
    r = c.post('/api/summarize', json={'text': 'Hello world. This is Clever. Local only.'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'summary' in data


def test_search_empty():
    c = clever_app.app.test_client()
    r = c.get('/api/search?q=')
    assert r.status_code == 200
    assert r.get_json() == []
