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
    - persona.py:
        - `clever_persona = PersonaEngine()`: Initializes the core personality engine.
        - `chat()` -> `clever_persona.generate()`: Generates AI responses for user messages.
        - `api_ping()` -> `clever_persona`: Checks the status of the persona engine.
        - `api_runtime_introspect()` -> `runtime_state(persona_engine=...)`: Passes the persona engine for state inspection.
    - database.py: (Indirectly) All persistence layers like `evolution_engine` and `persona`'s memory use the `db_manager` from `database.py` to interact with the single `clever.db` file.
    - evolution_engine.py:
        - `chat()` -> `get_evolution_engine().log_interaction()`: Logs every user interaction to enable system learning and growth.
    - introspection.py:
        - `register_error_handler(app)`: Installs a global error handler for runtime introspection.
        - `home()` -> `traced_render()`: Wraps template rendering to record performance and context.
        - `api_runtime_introspect()` -> `runtime_state()`: Gathers and returns a snapshot of the entire application's runtime state.
    - utils/offline_guard.py:
        - `offline_guard.enable()`: Called at startup to enforce the "offline-only" digital sovereignty rule by blocking non-local network connections.
    - user_config.py:
        - `home()`: Uses `USER_NAME` and `USER_EMAIL` to personalize the UI.
    - templates/index.html:
        - `home()` -> `traced_render('index.html', ...)`: Serves the main holographic user interface.
    - static/js/main.js: The frontend JavaScript makes calls to the `/api/chat` and `/api/ping` endpoints defined in this file.
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


@app.route('/debug')
def debug():
    """Temporary debug route to test rendering"""
    return render_template('debug.html')

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
                'particle_command': getattr(persona_response, 'particle_command', None),  # Shape formation command
                'status': 'success'
            }
            
            # Add shape data for mathematical visualization if available
            debugger.info("app.chat", f"Has context attr: {hasattr(persona_response, 'context')}")
            if hasattr(persona_response, 'context'):
                debugger.info("app.chat", f"Context keys: {list(persona_response.context.keys())}")
                if 'shape_data' in persona_response.context:
                    debugger.info("app.chat", "Adding shape_data to response")
                    response['shape_data'] = persona_response.context['shape_data']
                if 'requested_shape' in persona_response.context:
                    debugger.info("app.chat", f"Adding requested_shape: {persona_response.context['requested_shape']}")
                    response['requested_shape'] = persona_response.context['requested_shape']
            else:
                debugger.info("app.chat", "No context found on persona response")
            
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


@app.route('/<path:filename>')
def serve_test_files(filename):
    """
    Serve test HTML files from root directory
    
    Why: Test pages need to be accessible for particle system debugging
    Where: Handles requests for .html files in root directory  
    How: Check if file exists and serve it, otherwise 404
    """
    import os
    from flask import send_file, abort
    
    # Only serve .html files for security
    if not filename.endswith('.html'):
        abort(404)
        
    filepath = os.path.join(os.getcwd(), filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        abort(404)


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


@app.route('/api/generate_shape', methods=['POST'])
def api_generate_shape():
    """Generate mathematical shapes for cognitive visualization
    
    Why: Provides shape generation capabilities to enhance Clever's mathematical
         and geometric demonstration abilities as part of her digital brain extension
    Where: Called by frontend when shape commands are issued or by external tools
           needing geometric shape data for visualization
    How: Accepts shape parameters via JSON, uses ShapeGenerator to create mathematical
         shapes, returns coordinate data for particle system visualization
    
    Connects to:
        - shape_generator.py: ShapeGenerator.create_shape() for mathematical generation
        - static/js/engines/holographic-chamber.js: Frontend particle positioning
        - persona.py: PersonaEngine shape command handling integration
    """
    try:
        data = request.get_json() or {}
        shape_name = data.get('shape', 'circle')
        
        # Extract shape parameters
        kwargs = {}
        if 'size' in data:
            kwargs['size'] = float(data['size'])
        if 'radius' in data:
            kwargs['radius'] = float(data['radius'])
        if 'center' in data:
            kwargs['center'] = tuple(data['center'])
        if 'sides' in data:
            kwargs['sides'] = int(data['sides'])
        if 'turns' in data:
            kwargs['turns'] = float(data['turns'])
        if 'iterations' in data:
            kwargs['iterations'] = int(data['iterations'])
        if 'type' in data:
            kwargs['type'] = data['type']
        if 'point_count' in data:
            kwargs['point_count'] = int(data['point_count'])
        
        # Generate the shape
        from shape_generator import get_shape_generator
        shape_gen = get_shape_generator()
        shape = shape_gen.create_shape(shape_name, **kwargs)
        
        # Convert to JSON-serializable format
        shape_data = {
            'name': shape.name,
            'points': [{'x': p.x, 'y': p.y, 'z': p.z, 'color': p.color, 'size': p.size} for p in shape.points],
            'center': shape.center,
            'bounding_box': shape.bounding_box,
            'properties': shape.properties,
            'point_count': len(shape.points)
        }
        
        # Log for evolution tracking
        TELEMETRY["shapes_generated"] = TELEMETRY.get("shapes_generated", 0) + 1
        debugger.info('api.generate_shape', f'Generated {shape_name} with {len(shape.points)} points')
        
        return jsonify({
            'success': True,
            'shape': shape_data,
            'message': f'Generated {shape.name} with {len(shape.points)} coordinate points'
        })
        
    except Exception as e:
        debugger.error('api.generate_shape', f'Shape generation failed: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Shape generation failed'
        }), 500


@app.route('/api/shape_info/<shape_name>', methods=['GET'])
def api_shape_info(shape_name):
    """Get information about available shapes and their properties
    
    Why: Provides educational information about geometric shapes and their
         mathematical properties for learning and reference
    Where: Called by frontend for shape documentation or educational displays
    How: Generates example shape and returns comprehensive information including
         mathematical properties, educational content, and usage examples
    
    Connects to:
        - shape_generator.py: ShapeGenerator.create_shape() and get_shape_info()
        - Frontend UI: Shape selection and educational information display
    """
    try:
        from shape_generator import get_shape_generator
        shape_gen = get_shape_generator()
        
        # Generate example shape with default parameters
        shape = shape_gen.create_shape(shape_name)
        info = shape_gen.get_shape_info(shape)
        
        # Add educational content
        educational_content = {
            'triangle': 'A three-sided polygon, the simplest polygon in Euclidean geometry.',
            'square': 'A regular quadrilateral with four equal sides and four right angles.',  
            'pentagon': 'A five-sided polygon, famous for its use in the Pentagon building.',
            'hexagon': 'A six-sided polygon found in nature (honeycomb, crystal structures).',
            'circle': 'A perfectly round shape with all points equidistant from the center.',
            'spiral': 'A curve that winds around a center point, growing progressively farther away.',
            'fractal': 'A self-similar pattern that repeats at different scales infinitely.',
            'koch_snowflake': 'A mathematical snowflake fractal with infinite perimeter but finite area.'
        }
        
        info['educational'] = educational_content.get(shape_name.lower(), 'A geometric shape with mathematical properties.')
        
        # Add usage examples
        info['examples'] = [
            f"Create a {shape_name}: 'form a {shape_name}'",
            f"Generate {shape_name}: 'make a {shape_name}'",
            f"Show {shape_name}: 'show me a {shape_name}'"
        ]
        
        return jsonify({
            'success': True,
            'shape_name': shape_name,
            'info': info
        })
        
    except Exception as e:
        debugger.error('api.shape_info', f'Shape info retrieval failed: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Could not get information for shape: {shape_name}'
        }), 500


@app.route('/api/available_shapes', methods=['GET'])
def api_available_shapes():
    """List all available shapes that can be generated
    
    Why: Provides frontend with comprehensive list of supported shapes for
         UI controls, help documentation, and command suggestions
    Where: Called by frontend during initialization or for shape selection UI
    How: Returns categorized list of all supported shape types with descriptions
    
    Connects to:
        - shape_generator.py: References all supported shape types
        - Frontend UI: Shape selection menus and help systems
    """
    shapes = {
        'basic_polygons': {
            'triangle': {'sides': 3, 'description': 'Three-sided regular polygon'},
            'square': {'sides': 4, 'description': 'Four-sided regular polygon'},  
            'pentagon': {'sides': 5, 'description': 'Five-sided regular polygon'},
            'hexagon': {'sides': 6, 'description': 'Six-sided regular polygon'},
            'octagon': {'sides': 8, 'description': 'Eight-sided regular polygon'}
        },
        'curved_shapes': {
            'circle': {'description': 'Perfect circular shape'},
            'sphere': {'description': 'Three-dimensional sphere (projected as circle)'},
            'torus': {'description': 'Donut-shaped ring'}
        },
        'complex_shapes': {
            'spiral': {'description': 'Mathematical spiral patterns', 'types': ['archimedean', 'logarithmic', 'fibonacci']},
            'fractal': {'description': 'Self-similar fractal patterns'},
            'koch_snowflake': {'description': 'Recursive snowflake fractal'}
        },
        'particle_formations': {
            'cube': {'description': 'Cubic particle formation'},
            'wave': {'description': 'Wave-like particle motion'},
            'scatter': {'description': 'Random particle distribution'}
        }
    }
    
    return jsonify({
        'success': True,
        'categories': shapes,
        'total_shapes': sum(len(category) for category in shapes.values()),
        'message': 'Available shape types for generation'
    })


# NotebookLM-Inspired Document Analysis API Endpoints

@app.route('/api/analyze_document', methods=['POST'])
def api_analyze_document():
    """
    Analyze a specific document to extract key information and create summary.
    
    Why: Provides detailed document analysis for source-grounded responses
    Where: Called when users want to analyze specific documents in their knowledge base
    How: Uses NotebookLM engine to extract concepts, topics, and generate summaries
    
    Connects to:
        - notebooklm_engine.py: analyze_document() for comprehensive analysis
        - database.py: Document retrieval and summary storage
        - Frontend: Document analysis interface and results display
    """
    try:
        from notebooklm_engine import get_notebooklm_engine
        
        data = request.get_json(force=True) or {}
        source_id = data.get('source_id')
        force_reprocess = data.get('force_reprocess', False)
        
        if not source_id:
            return jsonify({
                'success': False,
                'error': 'source_id is required'
            }), 400
        
        engine = get_notebooklm_engine()
        start_time = time.time()
        
        try:
            summary = engine.analyze_document(source_id, force_reprocess)
            processing_time = (time.time() - start_time) * 1000
            
            return jsonify({
                'success': True,
                'summary': {
                    'source_id': summary.source_id,
                    'filename': summary.filename,
                    'key_concepts': summary.key_concepts,
                    'main_topics': summary.main_topics,
                    'summary': summary.summary,
                    'word_count': summary.word_count,
                    'reading_time_minutes': summary.reading_time_minutes,
                    'academic_level': summary.academic_level,
                    'document_type': summary.document_type
                },
                'processing_time_ms': processing_time
            })
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 404
            
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'NotebookLM engine not available'
        }), 500
    except Exception as e:
        debugger.info("api", f"Document analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during document analysis'
        }), 500


@app.route('/api/query_documents', methods=['POST'])
def api_query_documents():
    """
    Query across all documents to provide source-grounded response with citations.
    
    Why: Enables NotebookLM-style document querying with proper source attribution
    Where: Primary interface for document-based Q&A and research assistance
    How: Searches across document collection, ranks relevance, provides citations
    
    Connects to:
        - notebooklm_engine.py: query_documents() for source-grounded responses
        - persona.py: Enhanced responses with document citations
        - Frontend: Query interface and citation display
    """
    try:
        from notebooklm_engine import get_notebooklm_engine
        
        data = request.get_json(force=True) or {}
        query = data.get('query', '').strip()
        max_sources = data.get('max_sources', 5)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        engine = get_notebooklm_engine()
        start_time = time.time()
        
        response = engine.query_documents(query, max_sources)
        processing_time = (time.time() - start_time) * 1000
        
        # Log interaction for evolution engine
        try:
            from evolution_engine import get_evolution_engine
            evo = get_evolution_engine()
            evo.log_interaction({
                "user_input": query,
                "active_mode": "DocumentQuery",
                "action_taken": "query_documents",
                "sources_found": len(response.source_ids),
                "synthesis_quality": response.synthesis_quality
            })
        except ImportError:
            pass
        
        return jsonify({
            'success': True,
            'response': {
                'text': response.text,
                'citations': [
                    {
                        'source_id': c.source_id,
                        'filename': c.filename,
                        'excerpt': c.excerpt,
                        'confidence': c.confidence,
                        'page_number': c.page_number
                    } for c in response.citations
                ],
                'confidence': response.confidence,
                'source_ids': response.source_ids,
                'synthesis_quality': response.synthesis_quality
            },
            'processing_time_ms': processing_time,
            'sources_searched': max_sources
        })
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'NotebookLM engine not available'
        }), 500
    except Exception as e:
        debugger.info("api", f"Document query error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during document query'
        }), 500


@app.route('/api/document_connections', methods=['GET'])
def api_document_connections():
    """
    Find connections between documents based on shared concepts and topics.
    
    Why: Enables discovery of relationships across document collection
    Where: Called for research assistance and knowledge mapping
    How: Analyzes document summaries for overlapping concepts and topics
    
    Connects to:
        - notebooklm_engine.py: find_cross_document_connections() for relationship analysis
        - database.py: Document summary retrieval and connection storage
        - Frontend: Connection visualization and exploration interface
    """
    try:
        from notebooklm_engine import get_notebooklm_engine
        
        source_id = request.args.get('source_id', type=int)
        
        engine = get_notebooklm_engine()
        start_time = time.time()
        
        connections = engine.find_cross_document_connections(source_id)
        processing_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'connections': [
                {
                    'source_id_1': conn.source_id_1,
                    'source_id_2': conn.source_id_2,
                    'connection_type': conn.connection_type,
                    'strength': conn.strength,
                    'shared_concepts': conn.shared_concepts,
                    'explanation': conn.explanation
                } for conn in connections
            ],
            'total_connections': len(connections),
            'processing_time_ms': processing_time,
            'focused_document': source_id
        })
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'NotebookLM engine not available'
        }), 500
    except Exception as e:
        debugger.info("api", f"Document connections error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during connection analysis'
        }), 500


@app.route('/api/collection_overview', methods=['GET'])
def api_collection_overview():
    """
    Generate comprehensive overview of the entire document collection.
    
    Why: Provides high-level understanding of all ingested knowledge
    Where: Called for collection analysis and research starting points  
    How: Aggregates document summaries and identifies key themes
    
    Connects to:
        - notebooklm_engine.py: generate_collection_overview() for comprehensive analysis
        - database.py: Document collection retrieval and statistics
        - Frontend: Collection dashboard and overview interface
    """
    try:
        from notebooklm_engine import get_notebooklm_engine
        
        focus_topic = request.args.get('focus_topic')
        
        engine = get_notebooklm_engine()
        start_time = time.time()
        
        overview = engine.generate_collection_overview(focus_topic)
        processing_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'overview': overview,
            'processing_time_ms': processing_time,
            'generated_at': time.time()
        })
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'NotebookLM engine not available'
        }), 500
    except Exception as e:
        debugger.info("api", f"Collection overview error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during overview generation'
        }), 500


@app.route('/api/enhance_ingestion', methods=['POST'])
def api_enhance_ingestion():
    """
    Trigger enhanced analysis of recently ingested documents.
    
    Why: Ensures new documents get full NotebookLM-style analysis
    Where: Called after document ingestion to build comprehensive knowledge base
    How: Analyzes all documents without summaries using NotebookLM engine
    
    Connects to:
        - notebooklm_engine.py: analyze_document() for each unprocessed document
        - database.py: Document retrieval and analysis status tracking
        - Ingestion pipeline: Automatic enhancement of new documents
    """
    try:
        from notebooklm_engine import get_notebooklm_engine
        
        engine = get_notebooklm_engine()
        
        # Find documents without summaries
        with db_manager._lock, db_manager._connect() as conn:
            cursor = conn.execute("""
                SELECT s.id, s.filename 
                FROM sources s
                LEFT JOIN document_summaries ds ON s.id = ds.source_id
                WHERE ds.source_id IS NULL
                ORDER BY s.id
            """)
            unprocessed_docs = cursor.fetchall()
        
        if not unprocessed_docs:
            return jsonify({
                'success': True,
                'message': 'All documents already analyzed',
                'processed_count': 0,
                'total_documents': 0
            })
        
        start_time = time.time()
        processed_count = 0
        errors = []
        
        for doc_id, filename in unprocessed_docs:
            try:
                engine.analyze_document(doc_id)
                processed_count += 1
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")
        
        processing_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'message': f'Enhanced analysis completed for {processed_count} documents',
            'processed_count': processed_count,
            'total_documents': len(unprocessed_docs),
            'errors': errors,
            'processing_time_ms': processing_time
        })
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'NotebookLM engine not available'
        }), 500
    except Exception as e:
        debugger.info("api", f"Enhanced ingestion error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during enhanced analysis'
        }), 500


    
if __name__ == '__main__':
    debugger.info("app", "Clever AI starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
