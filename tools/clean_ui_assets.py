#!/usr/bin/env python3
"""
Clean unused legacy UI asset files.

Why: Keeps the repository lightweight and ensures only actively referenced static assets
are retained, reducing noise, bundle size, and potential confusion for future UI work.
Where: Invoked manually via the `make clean-ui` target in the project `Makefile`. It
interfaces with the `templates/` directory and the `static/` tree to discover which
files are currently referenced by HTML templates.
How: Scans all HTML templates for static asset references (JS/CSS). Builds a set of
referenced filenames, merges with a small allow‑list of always‑kept core assets, then
iterates a curated list of known legacy asset filenames and deletes those not referenced.
Also optionally prunes a handful of obsolete template files. Execution is best‑effort;
failures to delete are logged and do not abort the script.

Connects to:
    - Makefile (clean-ui target): Provides developer entry point
    - templates/*.html: Source of truth for active asset usage
    - static/js & static/css: Asset directories subject to pruning
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
STATIC_JS = STATIC / "js"
STATIC_CSS = STATIC / "css"

# Collect references from templates (*.html)
ref_regex = re.compile(r"static/(?:js/|css/)?([\w\-./]+\.(?:js|css))")
referenced = set()
for html in TEMPLATES.glob("**/*.html"):
    try:
        text = html.read_text(encoding="utf-8", errors="ignore")
        for m in ref_regex.finditer(text):
            referenced.add(m.group(1))
    except Exception:
        pass

# Always keep core files
keep = {
    "style.css",
    "js/particles.js",
    "js/main.js",
}

referenced |= keep

# Known legacy files to prune if unreferenced
legacy = [
    "clever_conversation_interface.js",
    "clever_evolution.js",
    "clever_invisible_personality.js",
    "clever_magical_ui.js",
    "clever_minimal_personality.js",
    "clever_personality_enhancer.js",
    "demo_mode.js",
    "magical_interface.js",
    "magical_particle_engine.js",
    "main.js",
    "main_clean.js",
    "main_simple.js",
    "nanobot_swarm.js",
    "orb_renderer.js",
    "particle_field.js",
    "tailwindcss.js",
    "ui.js",
    "voice.js",
    "js/capability_crystals.js",
    "js/clever_cosmic_mind.js",
    "js/clever_magical_ui.js",
    "js/cosmic_particles.js",
    "js/enhanced_ui.js",
    "js/magical_integration.js",
    "js/magical_particles.js",
    "js/main_simple.js",
    "js/simple_main.js",
    "js/simple_particles_test.js",
    "js/thought_manifestation.js",
    "css/cosmic_space.css",
    "css/magical_space.css",
    "css/magical_ui.css",
    "css/synaptic-hub.css",
    "css/synaptic_hub.css",
]

removed = []
for rel in legacy:
    # Skip if referenced
    if rel in referenced:
        continue
    p = STATIC / rel
    if p.exists():
        try:
            p.unlink()
            removed.append(str(p.relative_to(ROOT)))
        except Exception as e:
            print(f"WARN: could not remove {p}: {e}")

# Optional: prune unused templates (legacy pages)
legacy_templates = [
    "index_simple.html",
    "generate_output.html",
    "projects.html",
    "index_classic.html",
    "magical_ui.html",
]
for name in legacy_templates:
    p = TEMPLATES / name
    if p.exists():
        try:
            # keep index.html always
            if name != "index.html":
                p.unlink()
                removed.append(str(p.relative_to(ROOT)))
        except Exception as e:
            print(f"WARN: could not remove {p}: {e}")

print("Removed:")
for r in removed:
    print(" -", r)
print(f"Total removed: {len(removed)}")
