from __future__ import annotations

from flask import Flask, jsonify, request, render_template, send_from_directory, Response
import threading
import time
import logging
import os
import json
import traceback
from typing import Optional, Dict, Any, List, Tuple

import config
from database import db_manager
from file_ingestor import FileIngestor
from nlp_processor import nlp_processor
from persona import persona_engine
import fixer
from sync_tools import sync_clever_from_remote, sync_synaptic_from_remote

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
_ingest_state = {"running": False, "last_start": 0.0, "last_end": 0.0}
_ingest_lock = threading.Lock()

# ---- Basic health ------------------------------------------------------------

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

# Service worker route (served from /static but exposed at /sw.js)
@app.get("/sw.js")
def service_worker():
    return send_from_directory("static/js/core", "sw.js", mimetype="application/javascript")

# ---- UI routes expected by app.js -------------------------------------------

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    enable = getattr(config, 'ENABLE_RCLONE', False)
    # Try to serve templates/index.html if present; otherwise fall back to a simple shell
    try:
        return render_template("index.html", ENABLE_RCLONE=enable)
    except Exception:
        html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Clever</title>
  <link rel="stylesheet" href="/static/css/style.css?v=2"/>
</head>
<body>
  <div id="selfcheck" class="selfcheck">Checking…</div>
  <main class="wrap">
    <div class="chipline">
      <button id="ingest-btn" class="chip">Ingest</button>
      <button id="files-btn" class="chip">Open Files</button>
      <button id="pulse-btn" class="chip">Pulse</button>
    </div>
    <section id="chat" class="chat"></section>
    <div class="composer">
      <input id="chat-input" placeholder="Talk to Clever…" />
      <button id="mic-btn" title="Talk to Clever">🎤</button>
      <button onclick="window.__send && window.__send()">Send</button>
    </div>
  </main>
  <script src="/static/js/core/app.js?v=11"></script>
  <script>
    // small shim so the inline Send button works even if app.js binds Enter only
    (function(){ 
      const input=document.getElementById('chat-input');
      window.__send = async ()=> {
        const e = new KeyboardEvent('keydown', {key:'Enter'});
        input.dispatchEvent(e);
      };
    })();
  </script>
</body>
</html>"""
        return Response(html, mimetype="text/html")

@app.get("/ui/files")
def ui_files():
    """
    Serve projects.html if available (you uploaded it).
    If it isn't there, serve a tiny file browser shell.
    """
    proj = os.path.join(ROOT_DIR, "projects.html")
    if os.path.exists(proj):
        return send_from_directory(ROOT_DIR, "projects.html")
    # minimal fallback
    html = """<!doctype html><meta charset="utf-8">
<title>Files</title><link rel="stylesheet" href="/static/css/style.css?v=2">
<h1 style="margin:1rem;">Context Files</h1>
<div id="roots" style="margin:1rem;"></div>
<script>
(async ()=>{
  const r = await fetch('/local/fs/roots').then(r=>r.json()).catch(()=>({roots:[]}));
  const el = document.getElementById('roots');
  el.innerHTML = '<pre>'+JSON.stringify(r, null, 2)+'</pre>';
})();
</script>"""
    return Response(html, mimetype="text/html")

@app.get("/ui/sources")
def ui_sources():
    """
    Simple Sources page: lists indexed sources and lets you click to view.
    """
    html = """<!doctype html><meta charset="utf-8">
<title>Sources</title><link rel="stylesheet" href="/static/css/style.css?v=2">
<h1 style="margin:1rem;">Indexed Sources</h1>
<div class="chipline" style="margin:1rem;">
  <button class="chip" onclick="refresh()">Refresh</button>
</div>
<table id="tbl" style="margin:1rem; width: calc(100% - 2rem); border-collapse: collapse;">
  <thead><tr>
    <th style="text-align:left;border-bottom:1px solid #555;">ID</th>
    <th style="text-align:left;border-bottom:1px solid #555;">Filename</th>
    <th style="text-align:left;border-bottom:1px solid #555;">Path</th>
    <th style="text-align:left;border-bottom:1px solid #555;">Size</th>
  </tr></thead>
  <tbody></tbody>
</table>
<script>
async function refresh(){
  const j = await fetch('/sources').then(r=>r.json());
  const tb = document.querySelector('#tbl tbody');
  tb.innerHTML = '';
  (j||[]).forEach(row=>{
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>'+row.id+'</td>'+
                   '<td><a href="#" data-id="'+row.id+'" class="src">'+row.filename+'</a></td>'+
                   '<td>'+row.path+'</td>'+
                   '<td>'+row.size+'</td>';
    tb.appendChild(tr);
  });
  tb.querySelectorAll('a.src').forEach(a=>{
    a.addEventListener('click', async (e)=>{
      e.preventDefault();
      const id = a.getAttribute('data-id');
      const s = await fetch('/sources/'+id+'?content=true').then(r=>r.json());
      alert(s.content ? s.content.slice(0,1500) : '(no content)');
    });
  });
}
refresh();
</script>"""
    return Response(html, mimetype="text/html")

@app.get("/ui/generate")
def ui_generate():
    gen = os.path.join(ROOT_DIR, "generate_output.html")
    if os.path.exists(gen):
        return send_from_directory(ROOT_DIR, "generate_output.html")
    return Response("<h1>Generate</h1><p>Drop your generator UI here.</p>", mimetype="text/html")

# ---- Sources & Ingest --------------------------------------------------------

@app.get("/sources")
def list_sources():
    q = request.args.get("search", "").strip()
    sources = db_manager.search_sources(q) if q else db_manager.list_sources()
    return jsonify([
        {
            "id": s.id,
            "filename": s.filename,
            "path": s.path,
            "size": s.size if s.size is not None else len(s.content),
            "hash": s.content_hash,
            "modified_ts": s.modified_ts,
        }
        for s in sources
    ])

@app.post("/ingest")
def ingest():
    """Robust offline-safe ingestion with parameterized DB writes and JSON summary."""
    with _ingest_lock:
        if _ingest_state.get("running"):
            return jsonify({"indexed": 0, "skipped": 0, "errors": ["Ingest already running"]}), 409

        try:
            body = request.get_json(silent=True) or {}
            action = body.get("action", "scan")

            if action != "scan":
                return jsonify({"indexed": 0, "skipped": 0, "errors": ["Invalid action. Use 'scan'"]}), 400

            _ingest_state.update({"running": True, "last_start": time.time()})

            # Determine directories to scan
            base_dir = body.get("base_dir")
            dirs_to_scan = []
            
            if base_dir:
                if not os.path.exists(base_dir) or not os.path.isdir(base_dir):
                    return jsonify({"indexed": 0, "skipped": 0, "errors": [f"Invalid base_dir: {base_dir}"]}), 400
                dirs_to_scan = [base_dir]
            else:
                for dir_path in [config.SYNC_DIR, config.SYNAPTIC_HUB_DIR]:
                    if hasattr(config, 'SYNC_DIR') and os.path.exists(dir_path):
                        dirs_to_scan.append(dir_path)

            if not dirs_to_scan:
                return jsonify({"indexed": 0, "skipped": 0, "errors": ["No valid directories to scan"]}), 400

            indexed_count = 0
            skipped_count = 0
            errors = []

            for directory in dirs_to_scan:
                try:
                    dir_result = _scan_directory_safely(directory)
                    indexed_count += dir_result["indexed"]
                    skipped_count += dir_result["skipped"]
                    errors.extend(dir_result["errors"])
                except Exception as e:
                    errors.append(f"Failed to scan directory {directory}: {str(e)}")
                    logger.error(f"Failed to scan directory {directory}: {str(e)}")

            logger.info(f"Ingest complete: {indexed_count} indexed, {skipped_count} skipped, {len(errors)} errors")

            return jsonify({
                "indexed": indexed_count,
                "skipped": skipped_count,
                "errors": errors
            })

        except Exception as e:
            error_msg = f"Ingest failed: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({"indexed": 0, "skipped": 0, "errors": [error_msg]}), 500
        finally:
            _ingest_state.update({"running": False, "last_end": time.time()})

def _scan_directory_safely(directory: str) -> dict:
    """Scan a single directory with size caps and error collection."""
    result = {"indexed": 0, "skipped": 0, "errors": []}
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

    try:
        if not os.path.exists(directory):
            result["errors"].append(f"Directory not found: {directory}")
            return result

        if not os.access(directory, os.R_OK):
            result["errors"].append(f"Directory not readable: {directory}")
            return result

        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                # Skip hidden files and common non-text files
                if filename.startswith('.') or filename.lower().endswith(('.jpg', '.png', '.gif', '.pdf', '.zip', '.tar', '.gz')):
                    result["skipped"] += 1
                    continue
                    
                filepath = os.path.join(root, filename)
                try:
                    if not os.access(filepath, os.R_OK):
                        result["skipped"] += 1
                        continue
                        
                    file_size = os.path.getsize(filepath)
                    if file_size > MAX_FILE_SIZE:
                        result["skipped"] += 1
                        logger.debug(f"Skipped oversized file: {filepath} ({file_size} bytes)")
                        continue

                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()

                    if not content.strip():  # Skip empty files
                        result["skipped"] += 1
                        continue

                    stat = os.stat(filepath)
                    modified_ts = stat.st_mtime

                    try:
                        db_manager.add_or_update_source(
                            filename=filename,
                            path=filepath,
                            content=content,
                            size=file_size,
                            modified_ts=modified_ts
                        )
                        result["indexed"] += 1
                    except Exception as e:
                        result["errors"].append(f"Database error for {filepath}: {str(e)}")
                        logger.error(f"Database error for {filepath}: {str(e)}")

                except (UnicodeDecodeError, PermissionError, OSError) as e:
                    result["skipped"] += 1
                    logger.debug(f"Skipped file {filepath}: {str(e)}")
                except Exception as e:
                    result["errors"].append(f"Error processing {filepath}: {str(e)}")
                    logger.error(f"Error processing {filepath}: {str(e)}")

    except Exception as e:
        result["errors"].append(f"Error scanning directory {directory}: {str(e)}")
        logger.error(f"Error scanning directory {directory}: {str(e)}")

    return result

@app.get("/ingest/status")
def ingest_status():
    return jsonify({
        "running": bool(_ingest_state.get("running")),
        "last_start": float(_ingest_state.get("last_start", 0.0)),
        "last_end": float(_ingest_state.get("last_end", 0.0)),
    })

# ---- NLP & Chat --------------------------------------------------------------

@app.post("/analyze")
def analyze():
    body = request.get_json(force=True)
    text = body.get("text", "")
    res = nlp_processor.process(text)
    return jsonify({"keywords": res.keywords})

@app.get("/chat/history")
def chat_history():
    limit = int(request.args.get("limit", 50))
    return jsonify({"items": db_manager.list_utterances(limit)})

@app.post("/chat/send")
def chat_send():
    try:
        body = request.get_json(force=True)
        text = body.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "Empty message"}), 400
            
        if len(text) > 10000:  # Reasonable limit
            return jsonify({"error": "Message too long"}), 400
            
        # Mode: user-provided overrides, else infer automatically
        user_mode = body.get("mode")
        mode = user_mode or _infer_mode(text)

        # Fast path for simple greetings and short interactions
        simple_words = text.lower().split()
        if len(simple_words) <= 3 and any(word in simple_words for word in ['hey', 'hi', 'hello', 'yo', 'sup', 'yes', 'no', 'ok', 'thanks']):
            try:
                db_manager.add_utterance("user", text, mode=mode)
                pr = persona_engine.generate(text, mode=mode, history=[], context={})
                db_manager.add_utterance("assistant", pr.text, mode=pr.mode)
                return jsonify({
                    "reply": pr.text,
                    "mode": pr.mode,
                    "intensity": 0.3,
                    "sentiment": getattr(pr, 'sentiment', 0.0) if hasattr(pr, 'sentiment') else 0.0,
                    "intent": "greeting" if any(word in simple_words for word in ['hey', 'hi', 'hello']) else "simple",
                    "citations": [],
                    "validated": True,
                })
            except Exception as e:
                logger.error(f"Error in simple greeting handler: {str(e)}")
                return jsonify({
                    "reply": "Hi there! I'm experiencing some issues but I'm here to help.",
                    "mode": "Recovery",
                    "intensity": 0.3,
                    "sentiment": 0.0,
                    "intent": "greeting",
                    "citations": [],
                    "validated": False,
                })

        # Pre-response validation
        preflight = _preflight_validate(text)

        # Allow quick preference updates
        if _maybe_handle_preferences(text):
            try:
                db_manager.add_utterance("assistant", "Preference saved.", mode="Prefs")
                return jsonify({
                    "reply": "Preference saved.",
                    "mode": "Prefs",
                    "intensity": 0.15,
                    "sentiment": 0.1,
                    "intent": "prefs:update",
                    "citations": [],
                    "validated": True,
                })
            except Exception as e:
                logger.error(f"Error saving preferences: {str(e)}")

        try:
            db_manager.add_utterance("user", text, mode=mode)
        except Exception as e:
            logger.error(f"Error saving user utterance: {str(e)}")

        # Conversational local operations (require explicit 'allow')
        handled = _handle_local_via_chat(text)
        if handled is not None:
            reply, intent = handled
            try:
                db_manager.add_utterance("assistant", reply, mode="Local")
            except Exception as e:
                logger.error(f"Error saving local response: {str(e)}")
            return jsonify({
                "reply": reply,
                "mode": "Local",
                "intensity": 0.2,
                "sentiment": 0.0,
                "intent": intent,
                "citations": [],
                "validated": True,
            })

        # Special: limited self-fix via chat
        if text.lower().startswith("fix"):
            try:
                resp = _handle_fix_via_chat(text)
                db_manager.add_utterance("assistant", resp, mode="Fix")
                return jsonify({
                    "reply": resp,
                    "mode": "Fix",
                    "intensity": 0.2,
                    "sentiment": 0.0,
                    "intent": None,
                    "citations": [],
                })
            except Exception as e:
                logger.error(f"Error in fix handler: {str(e)}")
                return jsonify({
                    "reply": "Fix functionality is temporarily unavailable.",
                    "mode": "Recovery",
                    "intensity": 0.2,
                    "sentiment": 0.0,
                    "intent": None,
                    "citations": [],
                })

        try:
            # Persona-tailored reply (offline, heuristic)
            history = db_manager.list_utterances(limit=12)
            ctx = db_manager.get_context_notes()

            # Auto-extract and merge context for longer messages
            extracted_ctx = {}
            if len(text.split()) > 6:
                extracted_ctx = _extract_conversational_context(text)
                if extracted_ctx:
                    merged_ctx = {**ctx, **extracted_ctx}
                    try:
                        db_manager.set_context_notes(extracted_ctx)
                        ctx = merged_ctx
                    except Exception as e:
                        logger.error(f"Error saving context: {str(e)}")

            # Enhanced auto mode switching
            if not user_mode:
                word_count = len(text.split())
                complex_indicators = any(word in text.lower() for word in
                    ['analyze', 'explain', 'compare', 'design', 'architecture', 'strategy', 'research'])

                if word_count > 30 or complex_indicators:
                    mode = 'Deep Dive'
                elif any(word in text.lower() for word in ['idea', 'creative', 'design', 'brainstorm']):
                    mode = 'Creative'
                elif any(word in text.lower() for word in ['help', 'stuck', 'problem', 'issue', 'error']):
                    mode = 'Support'

            pr = persona_engine.generate(text, mode=mode, history=history[-3:], context=ctx)

            # Local retrieval with smarter search
            snippets = []
            word_count = len(text.split())
            try:
                if word_count > 8 and any(word in text.lower() for word in ['file', 'code', 'project', 'build', 'what', 'how', 'show']):
                    snippets = db_manager.search_snippets(text, limit=3)
                elif word_count > 12:
                    snippets = db_manager.search_snippets(text, limit=2)
            except Exception as e:
                logger.error(f"Error searching snippets: {str(e)}")
                snippets = []

            reply = _compose_reply_with_snippets(text, pr.text, snippets)

            # Proactive suggestions
            suggestions = []
            if hasattr(pr, 'proactive_suggestions') and pr.proactive_suggestions:
                suggestions.extend(pr.proactive_suggestions)
            if not snippets and any(word in text.lower() for word in ["file", "code", "project", "build", "run"]):
                try:
                    context_suggestions = _suggest_upgrades(text, snippets, ctx, mode)
                    suggestions.extend(context_suggestions)
                except Exception as e:
                    logger.error(f"Error generating suggestions: {str(e)}")
            if suggestions:
                reply = reply + "\n\n💡 **Proactive Insights:**\n" + "\n".join(f"• {s}" for s in suggestions[:3])

            try:
                db_manager.add_utterance("assistant", reply, mode=mode)
                db_manager.add_interaction(
                    user_input=text,
                    active_mode=mode,
                    action_taken="reply",
                    parsed_data={
                        "preflight": preflight,
                        "keywords": nlp_processor.process(text).keywords,
                        "ctx_keys": list((ctx or {}).keys()),
                        "snippets": [s.get("path") for s in snippets],
                    },
                )
            except Exception as e:
                logger.error(f"Error saving response: {str(e)}")
            
            sent = 0.0
            try:
                sent = nlp_processor.process(text).sentiment
            except Exception as e:
                logger.error(f"Error processing sentiment: {str(e)}")

            lt = text.lower()
            intent = None
            if any(k in lt for k in ["cube", "square", "box", "3d box", "cone"]):
                intent = "shape_request:cube"
            elif any(k in lt for k in ["ring", "circle", "orb", "torus"]):
                intent = "shape_request:torus" if "torus" in lt else "shape_request:ring"
            elif "wave" in lt or "grid" in lt:
                intent = "shape_request:wave"
            elif any(k in lt for k in ["sphere", "globe", "ball"]):
                intent = "shape_request:sphere"
            elif any(k in lt for k in ["knot", "trefoil"]):
                intent = "shape_request:knot"
            elif any(k in lt for k in ["pyramid", "tetra"]):
                intent = "shape_request:pyramid"

            return jsonify({
                "reply": reply,
                "mode": mode,
                "intensity": min(1.0, max(0.1, len(text)/200)),
                "sentiment": sent,
                "intent": intent,
                "citations": [{"id": s.get("id"), "filename": s.get("filename"), "path": s.get("path")} for s in snippets if s.get("id")],
                "validated": preflight.get("validated", False) or ("[validated" in pr.text),
            })
        except Exception as e:
            logger.error(f"Error in main chat handler: {str(e)}\n{traceback.format_exc()}")
            fallback = "Something hiccuped. I can still chat and act on local commands. Say 'fix: help' for safe repair options."
            try:
                db_manager.add_utterance("assistant", fallback, mode="Recovery")
                db_manager.add_interaction(user_input=text, active_mode=mode, action_taken="exception", parsed_data={"error": str(e), "preflight": preflight})
            except Exception as e2:
                logger.error(f"Error saving fallback response: {str(e2)}")
            return jsonify({
                "reply": fallback,
                "mode": "Recovery",
                "intensity": 0.15,
                "sentiment": 0.0,
                "intent": None,
                "citations": [],
                "validated": False,
            })
    except Exception as e:
        logger.error(f"Critical error in chat_send: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": "Internal server error",
            "reply": "I'm experiencing technical difficulties. Please try again.",
            "mode": "Error",
            "intensity": 0.1,
            "sentiment": 0.0,
            "intent": None,
            "citations": [],
            "validated": False,
        }), 500

# ---- Snippets & Context ------------------------------------------------------

@app.get("/search/snippets")
def search_snippets():
    q = request.args.get("q", "")
    lim = int(request.args.get("limit", 5))
    out = db_manager.search_snippets(q, limit=lim)
    return jsonify(out)

@app.get("/context/notes")
def get_context_notes():
    return jsonify(db_manager.get_context_notes())

@app.post("/context/notes")
def set_context_notes():
    body = request.get_json(silent=True) or {}
    allowed = {"project", "goal", "deadline", "priority", "owner"}
    notes = {k: str(v) for k, v in body.items() if k in allowed}
    if not notes:
        return jsonify({"ok": False, "error": "no valid keys"}), 400
    db_manager.set_context_notes(notes)
    return jsonify({"ok": True, "saved": notes})

# ---- Sync (optional) ---------------------------------------------------------

@app.post("/sync/rclone/clever")
def sync_clever():
    if not config.ENABLE_RCLONE:
        return jsonify({"status": "disabled"}), 200
    code, out, err = sync_clever_from_remote()
    status = "ok" if code == 0 else ("unavailable" if code in (2, 127) else "error")
    return jsonify({"status": status, "code": code, "stdout": out, "stderr": err}), 200

@app.post("/sync/rclone/synaptic")
def sync_synaptic():
    if not config.ENABLE_RCLONE:
        return jsonify({"status": "disabled"}), 200
    code, out, err = sync_synaptic_from_remote()
    status = "ok" if code == 0 else ("unavailable" if code in (2, 127) else "error")
    return jsonify({"status": status, "code": code, "stdout": out, "stderr": err}), 200

# ---- Sources detail ----------------------------------------------------------

@app.get("/sources/<int:source_id>")
def get_source(source_id: int):
    include_content = request.args.get("content", "false").lower() in {"1", "true", "yes", "on"}
    s = db_manager.get_source(source_id)
    if not s:
        return jsonify({"error": "not found"}), 404
    data = {
        "id": s.id,
        "filename": s.filename,
        "path": s.path,
        "size": s.size if s.size is not None else len(s.content),
        "hash": s.content_hash,
        "modified_ts": s.modified_ts,
    }
    if include_content:
        data["content"] = s.content
    return jsonify(data)

# ---- Boot helpers ------------------------------------------------------------

def main():
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)

def _kickoff_initial_ingest():
    try:
        if len(db_manager.list_sources()) == 0:
            def _bg():
                try:
                    with _ingest_lock:
                        _ingest_state.update({"running": True, "last_start": time.time()})
                    for d in [getattr(config, 'SYNC_DIR', ''), getattr(config, 'SYNAPTIC_HUB_DIR', '')]:
                        if d and os.path.exists(d):
                            try:
                                FileIngestor(d).ingest_all_files()
                            except Exception as e:
                                logger.error(f"Initial ingest error for {d}: {str(e)}")
                except Exception as e:
                    logger.error(f"Initial ingest background error: {str(e)}")
                finally:
                    with _ingest_lock:
                        _ingest_state.update({"running": False, "last_end": time.time()})
            threading.Thread(target=_bg, daemon=True).start()
    except Exception as e:
        logger.error(f"Initial ingest trigger error: {str(e)}")

_kickoff_initial_ingest()

# ---- Chat helpers ------------------------------------------------------------

def _compose_reply_with_snippets(question: str, persona_text: str, snippets: list[dict]) -> str:
    if not snippets:
        return persona_text
    import re
    from nlp_processor import nlp_processor as _nlp
    q_res = _nlp.process(question)
    q_tokens = set(q_res.keywords)
    candidates: list[tuple[float, str, dict]] = []
    for s in snippets:
        text = s.get("snippet", "")
        parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text) if p.strip()]
        for sent in parts:
            toks = [t.lower() for t in re.split(r"\W+", sent) if len(t) > 2]
            overlap = len(q_tokens.intersection(toks))
            score = overlap + 0.1 * min(len(sent), 200) / 200.0
            if overlap > 0:
                candidates.append((score, sent, s))
    candidates.sort(key=lambda x: x[0], reverse=True)
    picked: list[tuple[str, dict]] = []
    seen = set()
    for _, sent, meta in candidates:
        sig = sent.lower()[:80]
        if sig in seen:
            continue
        seen.add(sig)
        picked.append((sent, meta))
        if len(picked) >= 4:
            break
    if not picked:
        return _append_citations(persona_text, snippets)
    bullets = [f"- {sent}" for sent, _ in picked]
    answer = ["From your files:", *bullets]
    if persona_text:
        first_line = persona_text.splitlines()[0]
        if first_line and len(first_line) < 140:
            answer.append("")
            answer.append(first_line)
    reply = "\n".join(answer)
    reply = _append_citations(reply, snippets)
    return reply

def _append_citations(text: str, snippets: list[dict]) -> str:
    cite_lines = []
    for s in snippets:
        preview = (s["snippet"][:240] + "…") if len(s["snippet"]) > 240 else s["snippet"]
        cite_lines.append(f"[{s['filename']}] {preview}")
    if not cite_lines:
        return text
    return text + "\n\nSources:\n" + "\n".join(f"- {line}" for line in cite_lines)

def _infer_mode(text: str) -> str:
    lt = text.lower().strip()
    L = len(lt)
    if any(w in lt for w in ["brainstorm", "ideas", "imagine", "creative", "story", "poem", "design"]):
        return "Creative"
    if any(w in lt for w in ["why", "how", "explain", "analyze", "deep", "dive", "compare", "tradeoff", "plan", "architecture"]) or L > 180:
        return "Deep Dive"
    if any(w in lt for w in ["stressed", "overwhelmed", "stuck", "can't", "cant", "help me", "support", "motivate", "encourage"]):
        return "Support"
    if L < 80 or any(lt.startswith(v) for v in ["form", "make", "show", "build", "create", "summarize", "open", "go to", "fix", "ingest"]):
        return "Quick Hit"
    return "Quick Hit"

def _extract_conversational_context(text: str) -> dict[str, str]:
    import re
    from datetime import datetime, timedelta
    context = {}
    lt = text.lower()
    project_patterns = [
        r"working on (\w+(?:\s+\w+)*)",
        r"building (\w+(?:\s+\w+)*)",
        r"my (\w+) project",
        r"(\w+) app",
        r"(\w+) system",
        r"this (\w+)"
    ]
    for pattern in project_patterns:
        match = re.search(pattern, lt)
        if match:
            project = match.group(1).strip()
            if len(project.split()) <= 3 and project not in ["it", "this", "that", "the"]:
                context["project"] = project.title()
                break
    goal_patterns = [
        r"want to (\w+(?:\s+\w+)*)",
        r"trying to (\w+(?:\s+\w+)*)",
        r"need to (\w+(?:\s+\w+)*)",
        r"goal is to (\w+(?:\s+\w+)*)",
        r"should (\w+(?:\s+\w+)*)"
    ]
    for pattern in goal_patterns:
        match = re.search(pattern, lt)
        if match:
            goal = match.group(1).strip()
            if len(goal.split()) <= 5:
                context["goal"] = goal
                break
    deadline_patterns = [
        r"by (\w+day)",
        r"due (\w+day)",
        r"deadline (\w+day)",
        r"by (\d{4}-\d{2}-\d{2})",
        r"today", r"tomorrow", r"this week", r"next week"
    ]
    for pattern in deadline_patterns:
        if re.search(pattern, lt):
            if "today" in lt:
                context["deadline"] = datetime.now().strftime("%Y-%m-%d")
            elif "tomorrow" in lt:
                context["deadline"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            elif "this week" in lt:
                context["deadline"] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            break
    if any(word in lt for word in ["urgent", "asap", "critical", "important"]):
        context["priority"] = "High"
    elif any(word in lt for word in ["quick", "fast", "rush"]):
        context["priority"] = "Medium"
    elif any(word in lt for word in ["later", "someday", "eventually"]):
        context["priority"] = "Low"
    return context

def _preflight_validate(text: str) -> dict:
    notes = []
    ok = True
    lt = (text or "").strip().lower()
    if not lt:
        return {"validated": False, "notes": ["empty input"]}
    if any(w in lt for w in ["rm -rf", "format", "drop table", "delete all"]):
        ok = False
        notes.append("dangerous-intent")
    try:
        ctx = db_manager.get_context_notes()
        if not ctx.get("project") or not ctx.get("goal"):
            notes.append("missing-context")
    except Exception:
        notes.append("ctx-unavailable")
    return {"validated": ok, "notes": notes}

def _looks_like_loop(text: str) -> bool:
    try:
        hist = db_manager.list_utterances(limit=4)
        last_two_users = [u["text"] for u in hist if u["role"] == "user"][:2]
        if len(last_two_users) == 2 and _levenshtein(last_two_users[0], last_two_users[1]) <= 3:
            return True
    except Exception:
        pass
    return False

def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    dp = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev = i
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            prev, dp[j] = dp[j], min(dp[j] + 1, prev + 1, dp[j - 1] + cost)
        dp[0] = i
    return dp[-1]

@app.get("/telemetry/interactions")
def list_interactions():
    lim = int(request.args.get("limit", 100))
    return jsonify({"items": db_manager.list_interactions(lim)})

def _handle_fix_via_chat(text: str) -> str:
    lt = text.lower()
    allowed = (" allow" in lt) or (" permitted" in lt) or (" yes" in lt)
    if "help" in lt or lt.strip() in {"fix", "fix:", "fix?"}:
        ops = fixer.list_operations()
        return "Fix options (say: 'fix <op> allow'):\n- " + "\n- ".join(ops)
    op = None
    if "particles" in lt or "boost" in lt:
        op = "boost_particles"
    elif "bright" in lt or "glow" in lt:
        op = "brighten_scene"
    elif "service worker" in lt or "sw" in lt:
        op = "ensure_service_worker"
    elif "citations" in lt or "sources chip" in lt:
        op = "ensure_citations"
    elif "autoswitch" in lt or "mode" in lt:
        op = "enable_autoswitch"
    if not op:
        return "Unknown fix. Say 'fix help' to list safe operations."
    if not allowed:
        return f"I can run '{op}', but I need permission. Say: fix {op} allow"
    ok, msg = fixer.apply(op)
    return ("Applied: " + op + " — " + msg) if ok else ("Could not apply: " + op + " — " + msg)

def _suggest_upgrades(question: str, snippets: list[dict], ctx: dict, mode: str) -> list[str]:
    out: list[str] = []
    lt = (question or "").lower()
    auto_context = _extract_conversational_context(question)
    if auto_context:
        db_manager.set_context_notes(auto_context)
    if not snippets and any(w in lt for w in ["file", "code", "project", "build", "run"]):
        out.append("I'll scan your files to give better context.")
        _maybe_trigger_auto_ingest()
    if mode == "Quick Hit" and len(lt) > 220:
        out.append("This seems complex - let me dive deeper for you.")
    if any(w in lt for w in ["edit", "file", "browse", "open"]):
        try:
            if any(config.ALLOWED_ROOTS):
                out.append("I can help you with those files.")
        except Exception:
            pass
    return out

_last_auto_ingest_ts = 0.0
_auto_ingest_lock = threading.Lock()

def _maybe_trigger_auto_ingest():
    import time as _t
    global _last_auto_ingest_ts
    
    with _auto_ingest_lock:
        now = _t.time()
        cooldown = max(5, int(getattr(config, 'AUTO_INGEST_COOLDOWN_MINUTES', 20))) * 60
        if now - _last_auto_ingest_ts < cooldown:
            return
        _last_auto_ingest_ts = now

    try:
        def _bg():
            try:
                with _ingest_lock:
                    _ingest_state.update({"running": True, "last_start": _t.time()})
                
                for dir_path in [getattr(config, 'SYNC_DIR', ''), getattr(config, 'SYNAPTIC_HUB_DIR', '')]:
                    if dir_path and os.path.exists(dir_path):
                        try:
                            FileIngestor(dir_path).ingest_all_files()
                        except Exception as e:
                            logger.error(f"Auto-ingest error for {dir_path}: {str(e)}")
            except Exception as e:
                logger.error(f"Auto-ingest background error: {str(e)}")
            finally:
                with _ingest_lock:
                    _ingest_state.update({"running": False, "last_end": _t.time()})
        threading.Thread(target=_bg, daemon=True).start()
    except Exception as e:
        logger.error(f"Auto-ingest trigger error: {str(e)}")

# --- Local FS and Exec (opt-in, restricted) ----------------------------------

@app.get("/local/fs/roots")
def fs_roots():
    return jsonify({"roots": list(config.ALLOWED_ROOTS)})

def _is_allowed_path(path: str) -> bool:
    import os as _os
    ap = _os.path.abspath(path)
    for root in config.ALLOWED_ROOTS:
        rr = _os.path.abspath(root)
        if ap.startswith(rr + _os.sep) or ap == rr:
            return True
    return False

@app.post("/local/fs/list")
def fs_list():
    try:
        body = request.get_json(force=True)
        base = body.get("path", "")
        allow = bool(body.get("allow", False))
        
        if not allow:
            return jsonify({"ok": False, "error": "permission required"}), 400
            
        if not base or not isinstance(base, str):
            return jsonify({"ok": False, "error": "invalid path"}), 400
            
        if not _is_allowed_path(base):
            return jsonify({"ok": False, "error": "path not allowed"}), 403
            
        import os as _os
        
        if not _os.path.exists(base):
            return jsonify({"ok": False, "error": "path does not exist"}), 404
            
        if not _os.path.isdir(base):
            return jsonify({"ok": False, "error": "path is not a directory"}), 400

        try:
            entries = []
            for name in _os.listdir(base):
                p = _os.path.join(base, name)
                try:
                    st = _os.stat(p)
                    entries.append({
                        "name": name,
                        "path": p,
                        "is_dir": _os.path.isdir(p),
                        "size": int(getattr(st, 'st_size', 0)),
                        "mtime": float(getattr(st, 'st_mtime', 0.0)),
                    })
                except (OSError, PermissionError):
                    entries.append({"name": name, "path": p, "is_dir": None, "size": 0, "mtime": 0.0})
            return jsonify({"ok": True, "items": entries})
        except PermissionError:
            return jsonify({"ok": False, "error": "permission denied"}), 403
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error in fs_list: {str(e)}")
        return jsonify({"ok": False, "error": "internal server error"}), 500

@app.post("/local/fs/read")
def fs_read():
    try:
        body = request.get_json(force=True)
        path = body.get("path", "")
        allow = bool(body.get("allow", False))
        
        if not allow:
            return jsonify({"ok": False, "error": "permission required"}), 400
            
        if not path or not isinstance(path, str):
            return jsonify({"ok": False, "error": "invalid path"}), 400
            
        if not _is_allowed_path(path):
            return jsonify({"ok": False, "error": "path not allowed"}), 403
            
        import os as _os
        
        if not _os.path.exists(path):
            return jsonify({"ok": False, "error": "file does not exist"}), 404
            
        if not _os.path.isfile(path):
            return jsonify({"ok": False, "error": "path is not a file"}), 400
            
        try:
            file_size = _os.path.getsize(path)
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                return jsonify({"ok": False, "error": "file too large"}), 400
                
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                data = f.read()
            return jsonify({"ok": True, "content": data})
        except PermissionError:
            return jsonify({"ok": False, "error": "permission denied"}), 403
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error in fs_read: {str(e)}")
        return jsonify({"ok": False, "error": "internal server error"}), 500

@app.post("/local/fs/write")
def fs_write():
    try:
        body = request.get_json(force=True)
        path = body.get("path", "")
        content = body.get("content", "")
        allow = bool(body.get("allow", False))
        
        if not allow:
            return jsonify({"ok": False, "error": "permission required"}), 400
            
        if not path or not isinstance(path, str):
            return jsonify({"ok": False, "error": "invalid path"}), 400
            
        if not isinstance(content, str):
            return jsonify({"ok": False, "error": "invalid content"}), 400
            
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({"ok": False, "error": "content too large"}), 400
            
        if not _is_allowed_path(path):
            return jsonify({"ok": False, "error": "path not allowed"}), 403
            
        try:
            import os as _os
            dir_path = _os.path.dirname(path)
            if dir_path and not _os.path.exists(dir_path):
                _os.makedirs(dir_path, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return jsonify({"ok": True})
        except PermissionError:
            return jsonify({"ok": False, "error": "permission denied"}), 403
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error in fs_write: {str(e)}")
        return jsonify({"ok": False, "error": "internal server error"}), 500

@app.post("/local/exec")
def local_exec():
    try:
        body = request.get_json(force=True)
        cmd = body.get("cmd", "")
        cwd = body.get("cwd") or getattr(config, 'ROOT_DIR', os.getcwd())
        allow = bool(body.get("allow", False))
        
        if not allow:
            return jsonify({"ok": False, "error": "permission required"}), 400
            
        if not cmd:
            return jsonify({"ok": False, "error": "no command provided"}), 400
            
        if cwd and not _is_allowed_path(str(cwd)):
            return jsonify({"ok": False, "error": "cwd not allowed"}), 403
            
        # Basic command validation - prevent dangerous commands
        dangerous_patterns = ['rm -rf', 'format', 'mkfs', 'dd if=', '> /dev/', 'sudo', 'su -']
        cmd_str = cmd if isinstance(cmd, str) else ' '.join(cmd)
        if any(pattern in cmd_str.lower() for pattern in dangerous_patterns):
            return jsonify({"ok": False, "error": "dangerous command blocked"}), 403
            
        try:
            import subprocess, shlex
            import os as _os
            
            if not _os.path.exists(str(cwd)):
                return jsonify({"ok": False, "error": "working directory does not exist"}), 400
                
            proc = subprocess.run(
                cmd if isinstance(cmd, list) else shlex.split(str(cmd)), 
                cwd=str(cwd), 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return jsonify({
                "ok": proc.returncode == 0, 
                "code": proc.returncode, 
                "stdout": proc.stdout, 
                "stderr": proc.stderr
            })
        except subprocess.TimeoutExpired:
            return jsonify({"ok": False, "error": "command timed out"}), 408
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error in local_exec: {str(e)}")
        return jsonify({"ok": False, "error": "internal server error"}), 500

def _maybe_handle_preferences(text: str) -> bool:
    """Handle preference updates safely"""
    try:
        # Simple preference detection
        if any(phrase in text.lower() for phrase in ['set preference', 'save setting', 'remember that']):
            return True
        return False
    except Exception:
        return False

def _handle_local_via_chat(text: str) -> Optional[Tuple[str, str]]:
    """Handle local operations via chat safely"""
    try:
        lt = text.lower().strip()
        if 'allow' not in lt:
            return None
            
        if any(cmd in lt for cmd in ['list files', 'show files', 'ls']):
            return ("I can list files with permission. Use the file browser or API.", "file:list")
        elif any(cmd in lt for cmd in ['read file', 'show file', 'cat']):
            return ("I can read files with permission. Use the file API.", "file:read")
        elif any(cmd in lt for cmd in ['run command', 'execute', 'exec']):
            return ("I can execute commands with permission. Use the exec API.", "exec")
            
        return None
    except Exception:
        return None

_last_auto_ingest_ts = 0.0
_auto_ingest_lock = threading.Lock()

def _maybe_trigger_auto_ingest():
    import time as _t
    global _last_auto_ingest_ts
    
    with _auto_ingest_lock:
        now = _t.time()
        cooldown = max(5, int(getattr(config, 'AUTO_INGEST_COOLDOWN_MINUTES', 20))) * 60
        if now - _last_auto_ingest_ts < cooldown:
            return
        _last_auto_ingest_ts = now

    try:
        def _bg():
            try:
                with _ingest_lock:
                    _ingest_state.update({"running": True, "last_start": _t.time()})
                
                for dir_path in [getattr(config, 'SYNC_DIR', ''), getattr(config, 'SYNAPTIC_HUB_DIR', '')]:
                    if dir_path and os.path.exists(dir_path):
                        try:
                            FileIngestor(dir_path).ingest_all_files()
                        except Exception as e:
                            logger.error(f"Auto-ingest error for {dir_path}: {str(e)}")
            except Exception as e:
                logger.error(f"Auto-ingest background error: {str(e)}")
            finally:
                with _ingest_lock:
                    _ingest_state.update({"running": False, "last_end": _t.time()})
        threading.Thread(target=_bg, daemon=True).start()
    except Exception as e:
        logger.error(f"Auto-ingest trigger error: {str(e)}")
