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
    from persona_simple import PersonaEngine
    clever_persona = PersonaEngine("Clever", USER_NAME)
    debugger.info("app", "Simple persona engine initialized")
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

if __name__ == '__main__':
    debugger.info("app", "Clever AI starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
