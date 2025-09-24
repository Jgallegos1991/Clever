/*
Clever Digital Brain Extension - Main Application Logic

Why: Central JavaScript controller orchestrating Clever's cognitive interface initialization
Where: Loaded by templates/index.html as primary script after engine dependencies
How: Coordinates particle system, chat interface, and user interaction handling

Connects to:
    - templates/index.html: Script loaded after DOM parsing for initialization
    - static/js/engines/holographic-chamber.js: Uses window.startHolographicChamber()
    - static/js/components/chat-fade.js: Uses createChatBubble() for message display
    - static/css/style.css: Queries and manipulates elements styled by CSS
    - app.py: Sends requests to /api/chat endpoint for Clever responses
*/

console.log('🧠 Clever Digital Brain Extension initializing...');

// Global state management for cognitive interface
let holographicChamber = null;
let isProcessingMessage = false;

// Timing constants for chat bubble lifecycle management
/*
Why: Centralized timing ensures consistent cognitive rhythm and easy tuning
Where: Used by createChatBubble() and scheduleAutoHide() for message flow
How: Single source of truth mirrored by CSS variables for visual consistency
*/
const BUBBLE_FADE_IN_MS = 500;
const BUBBLE_VISIBLE_MS = 6000; // base visible window before fade
const BUBBLE_FADE_OUT_MS = 1000;

/**
 * Initialize Particle System
 * 
 * Why: Start Clever's cognitive visualization representing brain activity
 * Where: Called during DOMContentLoaded to establish visual foundation
 * How: Targets canvas element and initializes HolographicChamber engine
 * 
 * Connects to:
 *     - static/js/engines/holographic-chamber.js: window.startHolographicChamber() function
 *     - templates/index.html: Canvas element with id="particles"
 *     - static/css/style.css: Canvas positioning and styling
 */
function initializeParticleSystem() {
    const canvas = document.getElementById('particles');
    if (!canvas) {
        console.error('❌ Particles canvas not found - cognitive visualization unavailable');
        return;
    }

    // Cast to HTMLCanvasElement for proper typing
    const canvasElement = /** @type {HTMLCanvasElement} */ (canvas);
    
    // Set canvas dimensions to viewport
    canvasElement.width = window.innerWidth;
    canvasElement.height = window.innerHeight;

    // Initialize holographic chamber if engine is available
    if (typeof window.startHolographicChamber === 'function') {
        holographicChamber = window.startHolographicChamber(canvasElement);
        if (holographicChamber) {
            holographicChamber.animate();
            console.log('✅ Cognitive visualization active');
        } else {
            console.error('❌ Failed to initialize holographic chamber');
        }
    } else {
        console.error('❌ Holographic chamber engine not loaded');
    }

    // Handle window resize for responsive particle system
    window.addEventListener('resize', () => {
        canvasElement.width = window.innerWidth;
        canvasElement.height = window.innerHeight;
        if (holographicChamber && typeof holographicChamber.resize === 'function') {
            holographicChamber.resize(canvasElement.width, canvasElement.height);
        }
    });
}

/**
 * Initialize Chat Interface
 * 
 * Why: Set up conversation system for cognitive partnership with Clever
 * Where: Called during DOMContentLoaded to enable user interaction
 * How: Event handlers for form submission, keyboard shortcuts, and message processing
 * 
 * Connects to:
 *     - templates/index.html: Form element with id="chat-form"
 *     - static/js/components/chat-fade.js: createChatBubble() function
 *     - app.py: /api/chat endpoint for message processing
 *     - static/css/style.css: Chat interface styling and animations
 */
function initializeChatInterface() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-btn');

    if (!chatForm || !chatInput || !sendButton) {
        console.error('❌ Chat interface elements not found');
        return;
    }

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleMessageSubmit();
    });

    // Handle send button click
    sendButton.addEventListener('click', async (e) => {
        e.preventDefault();
        await handleMessageSubmit();
    });

    // Keyboard shortcuts for enhanced interaction
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleMessageSubmit();
        }
        
        // Particle mode shortcuts
        if (e.shiftKey && holographicChamber) {
            switch (e.key.toLowerCase()) {
                case 'c':
                    e.preventDefault();
                    holographicChamber.setMode('creative');
                    showSystemMessage('🎨 Creative mode activated');
                    break;
                case 's':
                    e.preventDefault();
                    holographicChamber.setMode('thinking');
                    showSystemMessage('🧠 Thinking mode activated');
                    break;
                case 'i':
                    e.preventDefault();
                    holographicChamber.setMode('idle');
                    showSystemMessage('😌 Idle mode activated');
                    break;
            }
        }
    });

    console.log('✅ Chat interface initialized');
}

/**
 * Handle Message Submit
 * 
 * Why: Process user input and communicate with Clever's cognitive engine
 * Where: Called by form submit and send button events
 * How: Validate input, send to API, display response with fade animations
 * 
 * Connects to:
 *     - app.py: POST request to /api/chat endpoint
 *     - static/js/components/chat-fade.js: createChatBubble() for display
 *     - persona.py: Backend processing of user message
 */
async function handleMessageSubmit() {
    if (isProcessingMessage) {
        console.log('⏳ Message already processing...');
        return;
    }

    const chatInput = /** @type {HTMLInputElement} */ (document.getElementById('chat-input'));
    const message = chatInput.value.trim();

    if (!message) {
        console.log('❌ Empty message - nothing to send');
        return;
    }

    isProcessingMessage = true;
    
    try {
        // Display user message
        displayMessage(message, 'user');
        chatInput.value = '';

        // Set thinking mode if particle system available
        if (holographicChamber && typeof holographicChamber.setMode === 'function') {
            holographicChamber.setMode('thinking');
        }

        // Send message to Clever's cognitive engine
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Display Clever's response
        if (data.response) {
            displayMessage(data.response, 'clever');
        } else {
            console.error('❌ No response in API data:', data);
            showSystemMessage('❌ No response received from Clever');
        }

        // Return to idle mode
        if (holographicChamber && typeof holographicChamber.setMode === 'function') {
            holographicChamber.setMode('idle');
        }

    } catch (error) {
        console.error('❌ Chat error:', error);
        showSystemMessage(`❌ Error: ${error.message}`);
        
        // Return to idle mode on error
        if (holographicChamber && typeof holographicChamber.setMode === 'function') {
            holographicChamber.setMode('idle');
        }
    } finally {
        isProcessingMessage = false;
    }
}

/**
 * Display Message
 * 
 * Why: Show conversation messages with fade animations for cognitive flow
 * Where: Called by handleMessageSubmit() and showSystemMessage()
 * How: Creates chat bubble elements with proper styling and lifecycle management
 * 
 * Connects to:
 *     - static/js/components/chat-fade.js: createChatBubble() function
 *     - static/css/style.css: Chat message styling and animations
 *     - templates/index.html: #chat-log container for message insertion
 */
function displayMessage(text, sender = 'system') {
    if (typeof window.createChatBubble === 'function') {
        // Use chat-fade component if available
        window.createChatBubble(text, sender);
    } else {
        // Fallback to simple message display
        console.log(`${sender.toUpperCase()}: ${text}`);
        
        const chatLog = document.getElementById('chat-log');
        if (chatLog) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${sender}`;
            messageDiv.innerHTML = `
                <div class="message-content">${text}</div>
                <div class="message-meta">${new Date().toLocaleTimeString()}</div>
            `;
            
            chatLog.appendChild(messageDiv);
            
            // Add show class for animation
            requestAnimationFrame(() => {
                messageDiv.classList.add('show');
            });
            
            // Auto-scroll to bottom
            chatLog.scrollTop = chatLog.scrollHeight;
            
            // Schedule auto-hide
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.classList.add('fade-out');
                    setTimeout(() => {
                        if (messageDiv.parentNode) {
                            messageDiv.remove();
                        }
                    }, BUBBLE_FADE_OUT_MS);
                }
            }, BUBBLE_VISIBLE_MS);
        }
    }
}

/**
 * Show System Message
 * 
 * Why: Display system notifications and status updates
 * Where: Called for particle mode changes and error notifications
 * How: Uses displayMessage() with system styling
 * 
 * Connects to:
 *     - displayMessage(): Message display system
 *     - Keyboard shortcuts: Mode change notifications
 */
function showSystemMessage(text) {
    displayMessage(text, 'system');
}

/**
 * Initialize Application
 * 
 * Why: Coordinate startup of all cognitive interface systems
 * Where: Called on DOMContentLoaded to ensure DOM is ready
 * How: Sequential initialization of particle system and chat interface
 * 
 * Connects to:
 *     - initializeParticleSystem(): Cognitive visualization startup
 *     - initializeChatInterface(): Conversation system startup
 *     - templates/index.html: DOM structure ready for manipulation
 */
function initializeApplication() {
    console.log('🚀 Starting Clever initialization sequence...');
    
    try {
        // Initialize particle system first for visual foundation
        initializeParticleSystem();
        
        // Then initialize chat interface for interaction
        initializeChatInterface();
        
        console.log('✅ Clever Digital Brain Extension ready');
        showSystemMessage('🧠 Clever is ready for cognitive partnership');
        
    } catch (error) {
        console.error('❌ Initialization failed:', error);
        showSystemMessage('❌ System initialization error');
    }
}

// Wait for DOM to be fully loaded before initialization
/*
Why: Ensure all HTML elements are available before JavaScript manipulation
Where: Standard event listener for reliable cross-browser compatibility
How: DOMContentLoaded event fires after HTML parsing is complete
*/
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApplication);
} else {
    // DOM already loaded
    initializeApplication();
}

// Export for debugging and external access
/*
Why: Provide access to internal state for development and debugging
Where: Available in browser console for runtime inspection
How: Global window properties for key functions and state
*/
/** @type {any} */ (window).CleverApp = {
    holographicChamber,
    isProcessingMessage,
    displayMessage,
    showSystemMessage,
    version: '1.0.0'
};

console.log('📦 Clever main.js loaded and ready');
