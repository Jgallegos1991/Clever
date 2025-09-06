import os, sys, time
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from io import BytesIO
import json as _json
# Ensure repo root on path so utils.* resolves in tests and runtime
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from utils import offline_guard

# -------- config (tolerate missing) ----------
try:
    import config as user_config
    DEBUG = getattr(user_config, "DEBUG", True)
except Exception:
    DEBUG = True

# -------- database (tolerate missing) --------
class _NullDB:
    def add_conversation(self, *_args, **_kwargs): pass
db_manager = _NullDB()
try:
    # if your database.py exposes DatabaseManager or a global db_manager, use it
    from database import db_manager as real_db
    db_manager = real_db or db_manager
except Exception as e:
    print(f"[WARN] DB not wired, running without persistence: {e}")

# -------- NLP (tolerate missing) -------------
nlp_processor = None
try:
    from nlp_processor import UnifiedNLPProcessor
    nlp_processor = UnifiedNLPProcessor()
except Exception as e:
    print(f"[WARN] NLP offline/unavailable: {e}")

# -------- Persona (required, but degrade) ----
class _FallbackPersona:
    last_used_trait = "Base"
    def generate_response(self, analysis):
        msg = analysis.get("user_input","")
        if msg.endswith("?"): self.last_used_trait = "Curious"
        else: self.last_used_trait = "Calm"
        return "Copy that. Tiny machines are on it."
try:
    from persona import CleverPersona
    clever_persona = CleverPersona(nlp_processor, db_manager)
except Exception as e:
    print(f"[WARN] Persona fallback in use: {e}")
    clever_persona = _FallbackPersona()

app = Flask(
    __name__,
    static_folder=os.path.join(APP_ROOT, 'static'),
    template_folder=os.path.join(APP_ROOT, 'templates')
)

# Enforce no-internet at runtime (allow loopback only)
try:
    offline_guard.enable()
except Exception as e:
    print(f"[WARN] offline guard not applied: {e}")

@app.route('/')
def index():
    # Serve the beautiful particle UI with 20k nanobots
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    try:
        return app.send_static_file('img/favicon.svg')
    except Exception:
        return ("", 204)

@app.route('/sw.js')
def service_worker_stub():
    # Keep console clean; no offline SW in this build
    return ("// no-op service worker\n", 200, {"Content-Type": "application/javascript"})

@app.route('/chat', methods=['POST'])
def chat():
    t0 = time.time()
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get('message') or '').strip()
    if not user_message:
        return jsonify({"error": "No message received."}), 400

    # analysis (offline safe)
    analysis = {"user_input": user_message, "detected_intent": "chat", "intents": []}
    if user_message.endswith("?"):
        analysis["detected_intent"] = "ask_question"

    if nlp_processor and hasattr(nlp_processor, "process"):
        try:
            # enrich, but never fail the request; coerce SimpleNamespace to dict
            extra = nlp_processor.process(user_message) or {}
            if hasattr(extra, "__dict__"):
                extra = vars(extra)
            if isinstance(extra, dict):
                for k, v in extra.items():
                    if k not in ("__dict__",):
                        analysis[k] = v
        except Exception as e:
            print(f"[WARN] NLP process error: {e}")

    # lightweight shape intent
    try:
        t = user_message.lower()
        shape = None
        if any(w in t for w in ("cube", "box")): shape = "cube"
        elif any(w in t for w in ("sphere", "ball", "orb", "globe")): shape = "sphere"
        elif any(w in t for w in ("torus", "ring", "donut")): shape = "torus"
        elif any(w in t for w in ("pyramid", "cone")): shape = "cone"
        elif "dodeca" in t: shape = "dodecahedron"
        if shape:
            analysis.setdefault("intents", []).append({
                "name": "ui.shape",
                "confidence": 0.9,
                "details": {"shape": shape}
            })
    except Exception:
        pass

    raw_reply = "I’m here with you, Jay."
    try:
        raw_reply = clever_persona.generate_response(analysis)
    except Exception as e:
        print(f"[WARN] Persona generate_response failed: {e}")

    # Ensure frontend gets a plain text reply
    reply_text = None
    if isinstance(raw_reply, dict):
        # common shapes: { text, analysis/meta, keywords, ... }
        reply_text = str(raw_reply.get("text") or raw_reply.get("reply") or "")
        extra = raw_reply.get("analysis") or raw_reply.get("meta") or None
        if isinstance(extra, dict):
            # non-destructive merge of any extra analysis
            for k, v in extra.items():
                analysis.setdefault(k, v)
    else:
        reply_text = str(raw_reply)

    try:
        # Enhanced logging with user context and timestamp
        conversation_data = {
            "user_message": user_message,
            "ai_reply": reply_text,
            "analysis": analysis,
            "persona_trait": getattr(clever_persona, "last_used_trait", "Base"),
            "timestamp": time.time()
        }
        db_manager.add_conversation(user_message, reply_text, meta=conversation_data)
    except Exception as e:
        print(f"[WARN] DB add_conversation failed: {e}")
        # Log to file as backup
        try:
            with open(os.path.join(APP_ROOT, 'logs', 'conversations_backup.log'), 'a') as f:
                f.write(f"{time.time()}|{user_message}|{reply_text}\n")
        except Exception:
            pass

    thought = {
        "activePersona": getattr(clever_persona, "last_used_trait", "Base"),
        "responseTime": int((time.time() - t0) * 1000),
        "detected_intent": analysis.get("detected_intent", "chat"),
        "intents": analysis.get("intents", []),
    }
    return jsonify({"reply": reply_text, "analysis": thought})

@app.post('/api/stt')
def stt():
    """Offline speech-to-text via Vosk if available and model present.
    Accepts multipart/form-data with file field 'audio' (mono 16k WAV preferred).
    """
    try:
        f = request.files.get('audio')
        if not f or not f.filename:
            return jsonify({"error": "no audio provided"}), 400
        data = f.read()
        # Lazy imports
        try:
            import wave
            import vosk  # type: ignore
            import audioop
        except Exception:
            return jsonify({"error": "stt model not installed (vosk)"}), 400

        # Read WAV header
        wf = wave.open(BytesIO(data), 'rb')
        n_channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        sampwidth = wf.getsampwidth()

        # Resolve and cache Vosk model
        model_dir = os.environ.get('VOSK_MODEL', os.path.join(APP_ROOT, 'models', 'vosk', 'en-us'))
        if not os.path.isdir(model_dir):
            return jsonify({
                "error": "vosk model not found", 
                "hint": f"Place model at {model_dir} or set VOSK_MODEL env var",
                "info": "Download from https://alphacephei.com/vosk/models (offline use only)"
            }), 400
        global _VOSK_MODEL
        try:
            _VOSK_MODEL
        except NameError:
            _VOSK_MODEL = None  # type: ignore
        if _VOSK_MODEL is None:
            _VOSK_MODEL = vosk.Model(model_dir)
        model = _VOSK_MODEL

        target_rate = 16000
        rec = vosk.KaldiRecognizer(model, target_rate)

        # Convert to mono 16-bit @16kHz in chunks
        state = None
        results = []
        while True:
            raw = wf.readframes(4000)
            if not raw:
                break
            if sampwidth != 2:
                try:
                    raw = audioop.lin2lin(raw, sampwidth, 2)
                except Exception:
                    return jsonify({"error": f"cannot convert sample width {sampwidth} -> 16-bit"}), 400
            if n_channels == 2:
                try:
                    raw = audioop.tomono(raw, 2, 0.5, 0.5)
                except Exception:
                    return jsonify({"error": "failed to downmix stereo"}), 400
            elif n_channels != 1:
                return jsonify({"error": f"unsupported channel count {n_channels}"}), 400
            if sample_rate != target_rate:
                raw, state = audioop.ratecv(raw, 2, 1, sample_rate, target_rate, state)
            if rec.AcceptWaveform(raw):
                part = _json.loads(rec.Result())
                if part.get('text'):
                    results.append(part['text'])
        final = _json.loads(rec.FinalResult()).get('text', '')
        text = ' '.join([*results, final]).strip()
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get('/api/selfcheck')
def selfcheck():
    """Expose a quick local-only status for UI and diagnostics."""
    try:
        # Offline guard
        og_enabled = False
        try:
            from utils import offline_guard as _og
            og_enabled = bool(getattr(_og, 'is_enabled', lambda: False)())
        except Exception:
            og_enabled = False

        # DB status
        db_ok, db_path = False, getattr(getattr(db_manager, 'db_path', None), 'strip', lambda: '')() or getattr(db_manager, 'db_path', '')
        try:
            p = db_path or os.path.join(APP_ROOT, 'clever.db')
            db_ok = os.path.exists(p)
        except Exception:
            db_ok = False

        # NLP status
        spacy_loaded = False
        try:
            spacy_loaded = bool(getattr(getattr(nlp_processor, 'nlp', None), 'pipe_names', None))
        except Exception:
            spacy_loaded = False

        # Vosk status (model path exists)
        model_dir = os.environ.get('VOSK_MODEL', os.path.join(APP_ROOT, 'models', 'vosk', 'en-us'))
        vosk_available = os.path.isdir(model_dir)

        return jsonify({
            'offline_guard': og_enabled,
            'database': {'ok': db_ok, 'path': db_path},
            'nlp': {'spacy_loaded': spacy_loaded},
            'stt': {'vosk_model_found': vosk_available, 'model_dir': model_dir},
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.post('/api/summarize')
def summarize():
    """Local quick summary using nlp_processor (offline)."""
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({"error": "no text"}), 400
    # naive: select keywords and first 2-3 sentences
    try:
        from textwrap import shorten
        import re
        res = {}
        if nlp_processor and hasattr(nlp_processor, 'process'):
            ns = nlp_processor.process(text)
            res['keywords'] = getattr(ns, 'keywords', [])
        sents = re.split(r'(?:\.|\!|\?)\s+', text)
        summary = ' '.join(sents[:3]).strip()
        res['summary'] = summary[:1000]
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get('/api/search')
def search():
    """Search local ingested sources (SQLite) and return snippets."""
    q = (request.args.get('q') or '').strip()
    if not q:
        return jsonify([])
    try:
        if hasattr(db_manager, 'search_snippets'):
            hits = db_manager.search_snippets(q, limit=10)
            return jsonify(hits)
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ingest', methods=['POST'])
def ingest():
    try:
        form_data = request.form.to_dict()
        processed = {k: (v or "").upper() for k, v in form_data.items()}
        return jsonify({"message": "Form submitted successfully!", "processed_data": processed})
    except Exception as e:
        return jsonify({"error": f"ingest failed: {e}"}), 400

@app.get('/health')
def health():
    return jsonify({"status": "ok"})

@app.after_request
def add_security_headers(resp):
    # Disallow fetching external assets; self + data URIs only.
    csp = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; media-src 'self' data:;"
    resp.headers.setdefault('Content-Security-Policy', csp)
    resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resp.headers.setdefault('Referrer-Policy', 'no-referrer')
    return resp

if __name__ == '__main__':
    print("🌟 Synaptic Hub Neural Interface Ready!")
    print("🔗 Local: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)

