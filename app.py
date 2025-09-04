
import os, time
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template, render_template_string
from werkzeug.utils import secure_filename

# ---------- Safe Mode ----------
SAFE_MODE = False  # set False later to use your full NLP/DB stack

if not SAFE_MODE:
    import config
    from database import db_manager
    from nlp_processor import UnifiedNLPProcessor
    from persona import CleverPersona
    from core_nlp_logic import upgrade_configurations, finalize_configurations

app = Flask(__name__, static_folder="static", template_folder="templates")

# --- Capabilities route ---
@app.get("/capabilities")
def capabilities():
    return jsonify({
        "name": "Clever",
        "role": "AI co-pilot and strategic thinking partner",
        "mission": "Blend high-level intelligence with authentic, human-like interaction to amplify user potential and productivity.",
        "operational_attributes": [
            "Witty Intelligence",
            "Intuitive Anticipation",
            "Adaptive Genius",
            "Empathetic Collaboration",
            "Proactive Problem-Solving",
            "Comprehensive Contextual Memory",
            "Custom & Secure (offline only)",
            "Mode Switching (curious, analytical, etc.)"
        ],
        "features": [
            "Offline operation (no cloud, no tracking)",
            "Animated starfield and 3D grid UI",
            "Particle cloud centerpiece (breathing effect)",
            "Responsive input and analysis log",
            "Floating, auto-fading response panels",
            "File ingestion and contextual analysis"
        ],
        "ui_style": {
            "theme": "Dark, high-contrast space (deep blues, neon accents)",
            "fonts": "Modern, crisp sans-serif",
            "structure": "Minimalist, clean, advanced but welcoming"
        }
    }), 200

# Upload dir
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Initialize full stack if Safe Mode is off
if not SAFE_MODE:
    app.config['UPLOAD_FOLDER'] = getattr(config, "UPLOAD_FOLDER", str(UPLOAD_DIR))
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    nlp_processor = UnifiedNLPProcessor()
    clever_persona = CleverPersona(nlp_processor, db_manager)
    print("🚀 Initializing Clever's NLP Core...")
    try:
        upgrade_configurations()
        finalize_configurations()
    except Exception as e:
        print(f"[WARN] upgrade/finalize failed: {e}")
    print("✅ Clever's NLP Core is Online.")

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("img/favicon.svg")

@app.route('/sw.js')
def service_worker():
    # Serve SW from root scope
    return app.send_static_file('js/sw.js')

@app.after_request
def add_pwa_headers(resp):
    # Basic headers to help installability and caching safety
    resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
    return resp


@app.get("/health")
def health():
    details = {"status": "ok"}
    try:
        if not SAFE_MODE:
            details.update({
                "db": "up" if getattr(db_manager, 'conn', None) else "down",
                "nlp": "loaded" if getattr(nlp_processor, 'nlp', None) else "missing",
            })
    except Exception as _:
        pass
    return jsonify(details), 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        start = time.time()
        data = request.get_json(silent=True) or {}
        msg = (data.get("message") or "").strip()
        if not msg:
            return jsonify(ok=False, error="No message received."), 400

        if SAFE_MODE:
            # Keep UI responsive while you iterate
            reply = f"Echo: “{msg}”. (Safe Mode reply.)"
            analysis = {
                "intent": ["general"],
                "sentiment": {"overall_mood": "neutral"},
                "keywords": [{"word": w} for w in msg.split()[:3]],
                "entities": [],
            }
            active_persona = "core"
            try:
                with open("conversations.json", "a", encoding="utf-8") as fh:
                    ts = datetime.now().isoformat(timespec="seconds")
                    fh.write(f'{ts}\tUSER:{msg}\tCLEVER:{reply}\n')
            except Exception as e:
                print(f"[WARN] could not append conversation log: {e}")
        else:
            # Full pipeline with graceful fallbacks
            try:
                analysis = nlp_processor.process(msg)
                reply = clever_persona.generate_response(analysis)
                try:
                    db_manager.add_conversation(msg, reply)
                except Exception as e:
                    print(f"[WARN] DB persist failed: {e}")
                active_persona = getattr(clever_persona, "last_used_trait", "core")
            except Exception as e:
                print(f"[WARN] NLP pipeline failed: {e}")
                reply = f"I heard: “{msg}”. (Fallback reply.)"
                analysis = {"intent": ["general"], "sentiment": {"overall_mood": "neutral"}, "keywords": [], "entities": []}
                active_persona = "core"

        # Extract key NLP fields for frontend
        detected_intent = (analysis.get("intent") or ["general"])[0]
        user_mood = (analysis.get("sentiment") or {}).get("overall_mood")
        key_topics = [kw.get("word") for kw in (analysis.get("keywords") or [])[:3]]
        entities = analysis.get("entities") or []

        # Enhanced response for UI feedback
        response_time_ms = round((time.time() - start) * 1000)
        
        return jsonify(
            reply=reply,
            analysis={
                "user_input": msg,
                "active_mode": "safe" if SAFE_MODE else "full",
                "detected_intent": detected_intent,
                "user_mood": user_mood,
                "key_topics": key_topics,
                "entities": entities,
                "full_nlp_analysis": analysis,
                "activePersona": active_persona,
                "responseTime": response_time_ms,
            },
            ui_state={
                "orb_mood": user_mood or "neutral",
                "orb_activity": "processing" if response_time_ms > 500 else "active",
                "particle_color": get_mood_color(user_mood),
                "grid_intensity": min(1.0, response_time_ms / 1000),
            }
        )
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


def get_mood_color(mood):
    """Convert mood to particle color for magical UI effects"""
    mood_colors = {
        "positive": "#00ff88",
        "negative": "#ff4444", 
        "neutral": "#2de0ff",
        "excited": "#ff8800",
        "calm": "#88ccff",
        "curious": "#cc88ff",
        "analytical": "#ffcc00"
    }
    return mood_colors.get(mood, "#2de0ff")


@app.route("/ingest", methods=["POST"])
def ingest():
    try:
        f = request.files.get("file")
        if not f or not f.filename:
            return jsonify(ok=False, error="No selected file."), 400

        save_dir = Path(app.config.get("UPLOAD_FOLDER") or UPLOAD_DIR)
        save_dir.mkdir(parents=True, exist_ok=True)

        filename = secure_filename(f.filename)
        path = save_dir / filename
        f.save(path)

        # Extract text (best-effort)
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            try:
                content = path.read_bytes().decode("utf-8", errors="ignore")
            except Exception:
                content = f"[binary file] {filename} ({path.stat().st_size} bytes)"

        if not SAFE_MODE:
            # Persist file into the knowledge base
            try:
                db_manager.add_source(filename, str(path), content)
            except Exception as e:
                print(f"[WARN] add_source failed: {e}")

        return jsonify(message="File uploaded and ingested successfully.", filename=filename)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

# ---- The missing endpoints that broke url_for ----
@app.route("/generator_page")
def generator_page():
    t = Path("templates/generate_output.html")
    if t.exists():
        return render_template("generate_output.html")
    # fallback minimal page so url_for always resolves
    return render_template_string("<h1>Output Generator</h1><p>Coming soon.</p>")

@app.route("/projects_page")
def projects_page():
    t = Path("templates/projects.html")
    if t.exists():
        return render_template("projects.html")
    return render_template_string("<h1>Active Projects</h1><p>Coming soon.</p>")


@app.route("/api/system_status")
def system_status():
    """Provide real-time system status for UI particle effects"""
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "mode": "safe" if SAFE_MODE else "full",
            "orb_state": "idle",
            "particle_count": 150,
            "grid_activity": 0.3,
            "ai_mood": "ready",
            "system_health": "optimal"
        }
        
        if not SAFE_MODE:
            # Add more detailed status when full system is active
            try:
                status.update({
                    "db_status": "connected" if getattr(db_manager, 'conn', None) else "disconnected",
                    "nlp_status": "loaded" if getattr(nlp_processor, 'nlp', None) else "missing",
                    "persona_active": hasattr(clever_persona, 'last_used_trait'),
                })
            except Exception:
                pass
                
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500


@app.route("/api/orb_pulse", methods=["POST"])
def orb_pulse():
    """Trigger visual orb reactions for specific events"""
    try:
        data = request.get_json() or {}
        pulse_type = data.get("type", "default")
        intensity = data.get("intensity", 0.5)
        
        # Define pulse patterns for different events
        pulse_patterns = {
            "thinking": {"color": "#ffcc00", "pattern": "pulse", "duration": 2000},
            "processing": {"color": "#2de0ff", "pattern": "ripple", "duration": 1500},
            "success": {"color": "#00ff88", "pattern": "burst", "duration": 1000},
            "error": {"color": "#ff4444", "pattern": "shake", "duration": 800},
            "greeting": {"color": "#cc88ff", "pattern": "wave", "duration": 1200},
        }
        
        pattern = pulse_patterns.get(pulse_type, pulse_patterns["thinking"])
        pattern["intensity"] = min(1.0, max(0.1, intensity))
        
        return jsonify({"pulse_pattern": pattern, "status": "triggered"})
    except Exception as e:
        return jsonify({"error": str(e)}, 500)

# ---------- Run ----------
if __name__ == "__main__":
    print("🌟 Synaptic Hub UI Ready!  (SAFE_MODE =", SAFE_MODE, ")")
    print("🔗 http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

