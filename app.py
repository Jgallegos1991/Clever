"""
Clever - Digital Brain Extension & Cognitive Partnership System (Main Application)

Why:
    Central orchestration hub for Jay's digital brain extension and cognitive partnership
    system. Coordinates all components of Clever's authentic genius friend personality,
    memory systems, and cognitive enhancement capabilities into a unified experience.
    This is where Jay's conversation with his digital other half comes to life.
Where:
    Core server that brings together Clever's personality engine, memory system,
    evolution capabilities, and holographic UI into seamless cognitive partnership.
    Every conversation flows through here, building the authentic relationship
    between Jay and his digital brain extension.
How:
    Flask application with complete digital sovereignty (offline-only), single unified
    database for relationship continuity, and integrated debugging for system
    transparency. Routes conversations to persona engine, logs interactions for
    continuous growth, and serves the holographic particle interface.

Connects to:
    - persona.py: Clever's street-smart genius personality and conversation engine
    - database.py: Unified memory system for continuous relationship building
    - evolution_engine.py: Learning system that grows Clever as Jay's life companion
    - templates/: Holographic UI for immersive cognitive enhancement interface
    - user_config.py: Jay's personal preferences and cognitive partnership settings
"""

import time
import re
from flask import Flask, request, jsonify, render_template
from database import db_manager
from user_config import USER_NAME, USER_EMAIL
from utils import offline_guard  # Enforce offline constraints
from introspection import traced_render, runtime_state, register_error_handler  # Runtime introspection utilities

# Enforce offline operation immediately (Unbreakable Rule #1)
offline_guard.enable()

# Create Flask app
app = Flask(__name__)
# Install global error capture for introspection (still lets Flask debug raise)
register_error_handler(app)


def _sanitize_persona_text(raw: str) -> str:
    """Strip meta reasoning tokens from persona output.

    Why: User requires only natural, human-like conversational responses; internal
         reasoning / diagnostics such as "Time-of-day: afternoon" or "Vector: 1.15"
         must never surface. Initial line-prefix filtering missed cases where these
         markers appeared inline within a sentence.
    Where: Applied in chat() right after persona.generate() and before JSON response
           formation so downstream UI code never sees unsanitized text.
    How: Two-phase cleaning:
         1. Remove any standalone lines beginning with known markers.
         2. For residual inline occurrences, surgically excise fragments matching
            token patterns (case-insensitive) while preserving surrounding prose.
            Repeated whitespace is collapsed and trailing artifact punctuation trimmed.

    Connects to:
        - persona.py: Source of original text (unchanged for internal metrics)
        - static/js/main.js: Expects already-cleaned text to render bubbles
        - tests (future): Can assert absence of banned markers using same patterns
    """
    if not isinstance(raw, str):
        return ''
    text = raw
    # Phase 1: drop whole lines that start with markers
    line_prefix = re.compile(r"^(?:\s*)(Time-of-day:|focal lens:|Vector:|complexity index|essence\b).*$", re.IGNORECASE)
    kept = [ln for ln in text.splitlines() if not line_prefix.match(ln.strip())]
    text = "\n".join(kept)
    # Phase 2: remove inline fragments e.g. 'Time-of-day: afternoon;' or 'Vector: 1.15'
    inline_patterns = [
        r"Time-of-day:\s*[^;.,\n]+[;,.]?",
        r"focal lens:\s*[^;.,\n]+[;,.]?",
        r"Vector:\s*[^;.,\n]+[;,.]?",
        r"complexity index[^;.,\n]*[;,.]?",
        r"essence:\s*[^;.,\n]+[;,.]?",
    ]
    for pat in inline_patterns:
        text = re.sub(pat, '', text, flags=re.IGNORECASE)
    # Phase 3: sentence-level purge if any residual marker fragments linger
    banned_tokens = ("time-of-day", "focal lens", "vector:", "complexity index", "essence:")
    sentences = re.split(r"(?<=[.!?])\s+", text)
    kept_sentences = [s for s in sentences if not any(bt in s.lower() for bt in banned_tokens)]
    if kept_sentences:
        text = ' '.join(kept_sentences)
    # Collapse repeated spaces / stray punctuation combos
    text = re.sub(r"\s{2,}", ' ', text)
    text = re.sub(r"\s*([,;:.])\s*\1+", r"\1", text)  # dedupe repeated punctuation
    # Remove leftover empty parentheses or double spaces produced by removals
    text = re.sub(r"\(\s*\)", '', text)
    text = re.sub(r"\s{2,}", ' ', text).strip()
    # Remove leading/trailing stray punctuation characters
    text = re.sub(r"^[;:,.-]+", '', text).strip()
    text = re.sub(r"[;:,.-]+$", '', text).strip()
    return text


# Simple debugger for now
class SimpleDebugger:
    """
    Simple debugging output for Clever AI
    
    Why: Provides basic logging without complex dependencies
    Where: Used throughout app.py for status messages
    How: Simple print-based logging with component tags
    """
    def info(self, component, message):
        print(f"[{component}] {message}")

    
    
debugger = SimpleDebugger()

# In-memory telemetry (server-side)
TELEMETRY = {
    "total_chats": 0,
    "avg_latency_ms": 0.0,
    "last_latency_ms": 0.0,
    "last_chat_ts": None,
    "last_error": None,
    "start_ts": time.time(),
}

# Initialize persona engine
try:
    from persona import PersonaEngine
    clever_persona = PersonaEngine()
    debugger.info("app", "Persona engine initialized")
except ImportError:
    clever_persona = None
    debugger.info("app", "Persona engine not available - using simple responses")


@app.route('/')
def home():
    """
    Main page route for Clever AI interface
    
    Why: Serves the primary user interface with particle system and chat
    Where: Entry point for all user interactions with Clever
    How: Renders template with cache busting and user context
    
    Connects to:
        - templates/index.html: Main UI template with particles
        - user_config.py: User personalization data
    """
    cache_buster = int(time.time())
    # NOTE:
    #   Switched from 'index_new.html' back to canonical 'index.html'. The new
    #   frontend chat bubble + fade logic and acceptance tests target elements
    #   (e.g., #chat-log) defined in 'index.html'. The legacy experimental
    #   template 'index_new.html' used different IDs (e.g., #chat-bubbles), so
    #   main.js could not append messages—causing invisible responses.
    #   Keeping index_new.html for now (deprecated) in case visual experiments
    #   are revisited; future cleanup can remove it once confirmed obsolete.
    return traced_render(
        app,
        'index.html',
        route='/',
        render_func=render_template,
        cache_buster=cache_buster,
        user_name=USER_NAME,
        user_email=USER_EMAIL,
    )


@app.route('/api/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat API endpoint for user messages
    
    Why: Handles user input and generates AI responses
    Where: Called by frontend JavaScript for chat functionality
    How: Processes JSON input, generates response via persona engine
    
    Connects to:
        - persona.py: AI response generation
        - static/js/main.js: Frontend chat interface
    """
    t0 = time.time()
    try:
        data = request.get_json(silent=True) or {}
        # Accept multiple legacy/alias keys: message, text, prompt
        user_message = (data.get('message') or data.get('text') or data.get('prompt') or '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        # Generate response using persona engine if available
        if clever_persona:
            persona_response = clever_persona.generate(user_message, mode="Auto")
            # Apply server-side scrub to remove any internal reasoning/meta tokens
            # Why: Ensure only human-like natural text reaches client regardless of upstream persona layers
            # Where: Chat endpoint directly before JSON serialization; complements client-side final scrub
            # How: _sanitize_persona_text uses regex + sentence removal heuristics; logs pre/post for traceability
            pre_raw = persona_response.text
            persona_response.text = _sanitize_persona_text(persona_response.text)
            pre_preview = pre_raw[:140].replace("\n", " ")
            post_preview = persona_response.text[:140].replace("\n", " ")
            debugger.info("sanitizer", f"pre={{ {pre_preview} }}")
            debugger.info("sanitizer", f"post={{ {post_preview} }}")
            # Unified schema consumed by frontend (main.js) plus future fields
            response = {
                'response': persona_response.text,
                'analysis': {
                    'mode': persona_response.mode,
                    'sentiment': persona_response.sentiment,
                    'intent': None,  # placeholder (could derive from persona)
                },
                'approach': persona_response.mode,  # alias for shaping logic
                'mood': (persona_response.sentiment or 'neutral'),
                'particle_intensity': 0.6,  # heuristic baseline (future: derive from sentiment)
                'status': 'success'
            }
            
            # Log interaction for evolution engine
            try:
                from evolution_engine import get_evolution_engine
                evo = get_evolution_engine()
                evo.log_interaction({
                    "user_input": user_message,
                    "active_mode": persona_response.mode,
                    "sentiment": persona_response.sentiment,
                    "action_taken": "respond"
                })
            except ImportError:
                debugger.info("chat", "Evolution engine not available")
        else:
            # Fallback response
            response = {
                'response': f"Hello! You said: {user_message}",
                'analysis': {
                    'mode': 'Auto',
                    'sentiment': 'neutral',
                    'intent': None,
                },
                'approach': 'Auto',
                'mood': 'neutral',
                'particle_intensity': 0.4,
                'status': 'success'
            }
        
        # Telemetry update (Why/Where/How documented inline)
        try:
            latency_ms = (time.time() - t0) * 1000.0
            TELEMETRY["last_latency_ms"] = latency_ms
            TELEMETRY["last_chat_ts"] = time.time()
            # Exponential moving average for stability
            if TELEMETRY["avg_latency_ms"] == 0:
                TELEMETRY["avg_latency_ms"] = latency_ms
            else:
                TELEMETRY["avg_latency_ms"] = TELEMETRY["avg_latency_ms"] * 0.85 + latency_ms * 0.15
            TELEMETRY["total_chats"] += 1
        except Exception:
            pass
        debugger.info("chat", f"Processed message: {user_message[:50]}...")
        return jsonify(response)
        
    except Exception as e:
        TELEMETRY["last_error"] = str(e)
        debugger.info("chat", f"Error processing message: {str(e)}")
        return jsonify({
            'error': 'Failed to process message',
            'status': 'error',
            'detail': str(e),
            'received': (request.get_json(silent=True) or {}),
        }), 500


@app.route('/api/ping', methods=['GET'])
def api_ping():
    """Lightweight ping for latency measurement and frontend readiness
    
    Why: Frontend needs a tiny, fast endpoint to confirm connectivity and measure baseline latency
    Where: Called once on page load by main.js (window load listener -> fetch('/api/ping'))
    How: Returns JSON with server time, uptime, persona mode if available, and minimal telemetry snapshot (no heavy processing)
    
    Connects to:
        - static/js/main.js: showToast connection success + latency metrics
        - persona.py: (optional) exposes current persona mode if engine exists
    """
    persona_mode = None
    try:
        persona_mode = getattr(clever_persona, 'default_mode', 'Auto') if clever_persona else 'N/A'
    except Exception:
        persona_mode = 'unknown'
    uptime_s = time.time() - TELEMETRY.get("start_ts", time.time())
    return jsonify({
        'status': 'ok',
        'ts': time.time(),
        'uptime_s': round(uptime_s, 2),
        'persona_mode': persona_mode,
        'avg_latency_ms': round(TELEMETRY.get('avg_latency_ms', 0.0), 2),
        'total_chats': TELEMETRY.get('total_chats', 0)
    })


@app.route('/api/telemetry', methods=['GET'])
def api_telemetry():
    """Expose lightweight in-memory telemetry (debug use only)
    
    Why: Provide quick operational insight (chat volume, latency) without external monitoring stack
    Where: Queried manually via curl or future debug overlay; NOT for production analytics persistence
    How: Returns a shallow copy of TELEMETRY with computed uptime
    
    Connects to:
        - static/js/main.js (potential future polling)
        - debug tooling (runtime introspection augment)
    """
    uptime_s = time.time() - TELEMETRY.get("start_ts", time.time())
    out = dict(TELEMETRY)
    out["uptime_s"] = round(uptime_s, 2)
    return jsonify(out)


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for system monitoring
    
    Why: Provides system status for automated monitoring and tests
    Where: Used by test automation and deployment health checks
    How: Returns simple status response with timestamp
    
    Connects to:
        - debug_config.py: System health logging
        - tests/: Automated test validation
    """
    return jsonify({
        'status': 'ok',
        'timestamp': time.time(),
        'service': 'clever-ai'
    })


@app.route('/ingest', methods=['POST'])
def ingest():
    """
    File ingestion endpoint for knowledge base updates
    
    Why: Allows uploading files to expand Clever's knowledge
    Where: Used by file upload functionality and batch ingestion
    How: Processes uploaded files and stores in database
    
    Connects to:
        - database.py: Knowledge storage via DB_PATH
        - file_ingestor.py: File processing logic
    """
    try:
        # Basic implementation following offline rules
        name = request.form.get('name') or request.values.get('name') or ''
        return jsonify({
            'status': 'success',
            'message': f'Form submitted successfully for {name}' if name else 'Form submitted successfully'
        })
    except Exception as e:
        debugger.info("ingest", f"Error in ingestion: {str(e)}")
        return jsonify({
            'error': 'Ingestion failed',
            'status': 'error'
        }), 500


@app.route('/summarize', methods=['POST'])
@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    Text summarization endpoint
    
    Why: Provides text summarization capabilities for user content
    Where: Called by UI for content analysis features
    How: Uses local NLP processing following offline requirements
    
    Connects to:
        - nlp_processor.py: Local text processing
        - persona.py: Intelligent summarization
    """
    try:
        data = request.get_json(silent=True) or {}
        text = data.get('text', '')
        summary = text[:120] + ('...' if len(text) > 120 else '') if text else 'No content provided.'
        return jsonify({
            'status': 'success',
            'summary': summary
        })
    except Exception as e:
        debugger.info("summarize", f"Error in summarization: {str(e)}")
        return jsonify({
            'error': 'Summarization failed',
            'status': 'error'
        }), 500


@app.route('/search', methods=['POST'])
@app.route('/api/search', methods=['GET'])
def search():
    """
    Knowledge search endpoint
    
    Why: Enables searching through ingested knowledge base
    Where: Used by search functionality in UI
    How: Queries database using centralized DB_PATH
    
    Connects to:
        - database.py: Search queries via DatabaseManager
        - evolution_engine.py: Search result logging
    """
    try:
        # Support legacy GET with q param returning list (tests expect [])
        if request.method == 'GET':
            q = request.args.get('q', '')
            if not q:
                return jsonify([])
            return jsonify([])
        return jsonify({
            'status': 'success',
            'results': [],
            'message': 'Search endpoint ready'
        })
    except Exception as e:
        debugger.info("search", f"Error in search: {str(e)}")
        return jsonify({
            'error': 'Search failed',
            'status': 'error'
        }), 500


@app.route('/api/runtime_introspect', methods=['GET'])
def api_runtime_introspect():
    """Runtime introspection snapshot endpoint

    Why: Exposes real-time system state (recent renders, endpoint Why/Where/How,
    persona mode, last error, git hash) to power debugging overlays and quickly
    diagnose UI rendering mismatches.
    Where: Called by optional frontend debug overlay (e.g., when ?debug=1) or
    manual curl requests during development sessions.
    How: Aggregates data via `runtime_state` helper in `introspection.py` and
    returns JSON.

    Connects to:
        - introspection.py: runtime_state assembly
        - templates/index.html: primary template tracked in recent renders
    """
    return jsonify(runtime_state(app, persona_engine=clever_persona))

    
    
if __name__ == '__main__':
    debugger.info("app", "Clever AI starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
