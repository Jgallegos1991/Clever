from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'templates' / 'index.html'


def test_index_has_core_elements():
<<<<<<< HEAD
=======
    """
    Validate presence of essential UI elements in the index template.
    
    Why: Ensures the main interface contains all required components
         for Clever AI's 3D holographic chamber experience.
    Where: UI acceptance test verifying template structure meets
           design specifications for particle UI and grid overlay.
    How: Parses index.html with BeautifulSoup, searches for specific
         elements by ID and class, asserts their existence.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
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
<<<<<<< HEAD
    html = INDEX.read_text(encoding='utf-8')
    assert "url_for('static', filename='style.css')" in html
    assert "url_for('static', filename='js/holographic-chamber.js')" in html
    assert "url_for('static', filename='js/core/app.js')" in html


def test_microcopy_placeholders():
=======
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
    assert "url_for('static', filename='js/particles.js')" in html
    assert "url_for('static', filename='js/main.js')" in html


def test_microcopy_placeholders():
    """
    Confirm presence of appropriate UI microcopy matching design brief.
    
    Why: Validates user experience elements align with Clever AI's
         ambient creativity and thought flow design philosophy.
    Where: Microcopy validation ensuring UI text reflects the intended
           magical, fluid interface aesthetic.
    How: Searches HTML content for specific placeholder text that
         matches the creative, ambient UI tone requirements.
    """
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    html = INDEX.read_text(encoding='utf-8')
    # Presence of placeholder copy that matches the brief tone
    assert 'Ambient creativity' in html or 'Your thought enters the flow' in html
