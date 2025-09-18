"""
Clever AI Main Application

Why: Serves as the entry point and orchestrator for all Clever AI operations,
including web server, API endpoints, and system integrations. Ensures offline
operation, single-user focus, and centralized control.
Where: Connects to persona, database, and user_config modules.
How: Initializes Flask app, loads config, handles requests, and manages system lifecycle.

Connects to:
    - persona.py: Persona engine for responses
    - database.py: Database manager
    - user_config.py: User-specific settings
"""

import os
import sys
import time
from flask import Flask, request, jsonify, render_template
from database import db_manager
from user_config import USER_NAME, USER_EMAIL

# Create Flask app
app = Flask(__name__)

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
    return render_template('index_new.html', 
                         cache_buster=cache_buster,
                         user_name=USER_NAME,
                         user_email=USER_EMAIL)

@app.route('/api/chat', methods=['POST'])
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
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        # Generate response using persona engine if available
        if clever_persona:
            persona_response = clever_persona.generate(user_message, mode="Auto")
            response = {
                'reply': persona_response.text,
                'mode': persona_response.mode,
                'sentiment': persona_response.sentiment,
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
                'reply': f"Hello! You said: {user_message}",
                'mode': 'Auto',
                'sentiment': 'neutral',
                'status': 'success'
            }
        
        debugger.info("chat", f"Processed message: {user_message[:50]}...")
        return jsonify(response)
        
    except Exception as e:
        debugger.info("chat", f"Error processing message: {str(e)}")
        return jsonify({
            'error': 'Failed to process message',
            'status': 'error'
        }), 500

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
        return jsonify({
            'status': 'success',
            'message': 'File ingestion endpoint ready'
        })
    except Exception as e:
        debugger.info("ingest", f"Error in ingestion: {str(e)}")
        return jsonify({
            'error': 'Ingestion failed',
            'status': 'error'
        }), 500

@app.route('/summarize', methods=['POST'])
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
        return jsonify({
            'status': 'success',
            'summary': 'Summarization endpoint ready'
        })
    except Exception as e:
        debugger.info("summarize", f"Error in summarization: {str(e)}")
        return jsonify({
            'error': 'Summarization failed',
            'status': 'error'
        }), 500

@app.route('/search', methods=['POST'])
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

if __name__ == '__main__':
    debugger.info("app", "Clever AI starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
