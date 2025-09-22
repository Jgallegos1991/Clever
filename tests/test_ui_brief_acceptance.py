from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'templates' / 'index.html'


def test_index_has_core_elements():
    """
    Validate presence of essential UI elements in the index template.
    
    Why: Ensures the main interface contains all required components
         for Clever AI's 3D holographic chamber experience.
    Where: UI acceptance test verifying template structure meets
           design specifications for particle UI and grid overlay.
    How: Parses index.html with BeautifulSoup, searches for specific
         elements by ID and class, asserts their existence.
    """
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
     """
     Confirm core local asset references are present (minimal set).

     Why: The UI was simplified—legacy core/app.js and microcopy removed—so the
           acceptance test must reflect the authoritative minimal template.
     Where: Ensures offline local references remain intact for style + particles.
     How: Asserts Flask url_for usage for required assets only.
     """
     html = INDEX.read_text(encoding='utf-8')
     assert "url_for('static', filename='style.css')" in html
     assert "url_for('static', filename='js/engines/holographic-chamber.js')" in html
     # core/app.js intentionally excluded after UI minimization


def test_microcopy_placeholders():
    """
    Verify all static assets are properly wired for local serving.
    
    Why: Ensures offline-first operation by confirming no external
         CDN dependencies and all assets use Flask's url_for routing.
    Where: Asset validation test supporting Clever AI's strict
           offline-only architecture requirements.
    How: Searches index.html content for Flask url_for template
         syntax in CSS and JavaScript asset references.
    """
    html = INDEX.read_text(encoding='utf-8')
    assert "url_for('static', filename='style.css')" in html
    assert "url_for('static', filename='js/components/chat-fade.js')" in html
    assert "url_for('static', filename='js/main.js')" in html


def test_microcopy_removed():
    """
    Verify legacy ambient microcopy was removed per minimal UI spec.

    Why: User requested a stage free of persistent meta/ambient text—only
         conversational chat bubbles should appear.
    Where: Guards against reintroduction of hidden spans in index.html.
    How: Assert those phrases are absent from the canonical template.
    """
    html = INDEX.read_text(encoding='utf-8')
    assert 'Ambient creativity' not in html
    assert 'Your thought enters the flow' not in html
