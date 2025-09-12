from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'templates' / 'index.html'


def test_index_has_core_elements():
    html = INDEX.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    # Particle canvas present
    assert soup.find('canvas', id='particles') is not None
    # Grid overlay present
    assert soup.find('div', class_='grid-overlay') is not None
    # Panels present
    assert soup.find('div', class_='panel') is not None
    # Chat and Analysis placeholders
    assert soup.find(id='chat-log') is not None
    for id_ in ['intent', 'sentiment', 'entities', 'keywords']:
        assert soup.find(id=id_) is not None


def test_assets_wired_locally():
    html = INDEX.read_text(encoding='utf-8')
    assert "url_for('static', filename='style.css')" in html
    assert "url_for('static', filename='js/holographic-chamber.js')" in html
    assert "url_for('static', filename='js/core/app.js')" in html


def test_microcopy_placeholders():
    html = INDEX.read_text(encoding='utf-8')
    # Presence of placeholder copy that matches the brief tone
    assert 'Ambient creativity' in html or 'Your thought enters the flow' in html
