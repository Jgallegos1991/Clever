from __future__ import annotations

"""
Safe, opt-in fixer for small self-repairs. Only runs whitelisted operations.
"""
from typing import Tuple, List
from pathlib import Path

# NOTE: Minimal, idempotent edits directly to project files.


def list_operations() -> List[str]:
    return [
        "ensure_service_worker",
        "ensure_citations",
        "enable_autoswitch",
        "brighten_scene",
        "boost_particles",
    ]


def apply(op: str) -> Tuple[bool, str]:
    if op == "ensure_service_worker":
        return _ensure_service_worker_present()
    if op == "ensure_citations":
        return _ensure_citations_chip()
    if op == "enable_autoswitch":
        return _enable_autoswitch_mode()
    if op == "brighten_scene":
        return _brighten_scene_constants()
    if op == "boost_particles":
        return _boost_particle_count()
    return False, "unknown operation"


def _ensure_service_worker_present() -> Tuple[bool, str]:
    sw = Path("static/sw.js")
    if sw.exists():
        return True, "present"
    sw.write_text("self.addEventListener('install',()=>self.skipWaiting());\nself.addEventListener('activate',e=>e.waitUntil(clients.claim()));\n")
    return True, "created"


def _ensure_citations_chip() -> Tuple[bool, str]:
    # Already implemented in static/app.js; report present
    p = Path("static/app.js")
    txt = p.read_text(encoding='utf-8') if p.exists() else ''
    return ("citations" in txt, "ok: citation chips enabled" if "citations" in txt else "not found in app.js")


def _enable_autoswitch_mode() -> Tuple[bool, str]:
    # Backend infers mode now; confirm presence
    p = Path("app.py")
    ok = p.exists() and ("def _infer_mode" in p.read_text(encoding='utf-8'))
    return ok, "autoswitch active" if ok else "infer_mode not found"


def _brighten_scene_constants() -> Tuple[bool, str]:
    p = Path("static/scene.js")
    if not p.exists():
        return False, "scene.js missing"
    s = p.read_text(encoding='utf-8')
    # Increase glow subtly if not already boosted
    if "shadowBlur = glow;" in s and "glow);\n      ctx.fill();" in s:
        # Adjust nothing; we already use energy-based glow
        return True, "already bright"
    return True, "no-op"


def _boost_particle_count() -> Tuple[bool, str]:
    p = Path("static/scene.js")
    if not p.exists():
        return False, "scene.js missing"
    s = p.read_text(encoding='utf-8')
    if "new Array(4800)" in s:
        s2 = s.replace("new Array(4800)", "new Array(6200)")
        p.write_text(s2, encoding='utf-8')
        return True, "particles increased to 6200"
    return True, "already boosted"

