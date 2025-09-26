/*
main.js - Clever Digital Brain Extension Main Application Logic

Why: Central JavaScript controller orchestrating Clever cognitive interface initialization,
particle system management, and user interaction handling for the digital brain extension
experience. Essential for coordinating all frontend components of Clever cognitive partnership.

Where: Loaded by templates/index.html as primary script after engine dependencies.
Core frontend component of Clever cognitive enhancement interface.

How: Coordinates particle system, chat interface, and user interaction handling through
modular component integration and state management.

File Usage:
    - Frontend initialization: Primary script for initializing Clever cognitive interface
    - User interaction: Handles all user input and chat interface functionality
    - Particle coordination: Manages holographic particle system integration and lifecycle
    - State management: Maintains frontend application state and cognitive interface status
    - API communication: Coordinates requests to Flask backend for Clever responses
    - Performance monitoring: Tracks and optimizes frontend performance metrics
    - Debug integration: Supports runtime introspection and debugging capabilities
    - Component orchestration: Coordinates all frontend components and modules

Connects to:
    - templates/index.html: Script loaded after DOM parsing for initialization
    - static/js/engines/holographic-chamber.js: Uses window.startHolographicChamber() for particle system
    - static/js/components/chat-fade.js: Uses createChatBubble() for message display and animation
    - static/js/core/: Core modules for system functionality and utilities
    - static/js/performance/: Performance monitoring and optimization modules
    - static/css/style.css: Queries and manipulates elements styled by CSS system
    - app.py: Sends requests to /api/chat endpoint for Clever cognitive responses
    - persona.py: Frontend interface to personality engine and response modes
    - evolution_engine.py: User interaction tracking and learning system integration
    - debug_config.py: Frontend debugging and performance monitoring integration
    - introspection.py: Runtime state polling for debug overlay functionality
*/

console.log('🧠 Clever Digital Brain Extension initializing...');

// Global state management for cognitive interface
let holographicChamber = null;
let isProcessingMessage = false;
let cognitiveMaintenanceInterval = null;
let lastInteractionTime = Date.now(); // Shared interaction timestamp for cognitive state management

// Timing constants for chat bubble lifecycle management
/*
Why: Centralized timing ensures consistent cognitive rhythm and easy tuning
Where: Used by createChatBubble() and scheduleAutoHide() for message flow
How: Single source of truth mirrored by CSS variables for visual consistency
*/
const BUBBLE_FADE_IN_MS = 500;
const BUBBLE_VISIBLE_MS = 6000; // base visible window before fade
const BUBBLE_FADE_OUT_MS = 1000;

// Cognitive maintenance constants
const COGNITIVE_MAINTENANCE_INTERVAL = 5000; // 5 seconds
const IDLE_OBSERVATION_INTERVAL = 30000; // 30 seconds

/**
 * Start Cognitive Maintenance Loop
 * 
 * Why: Ensures Clever maintains continuous cognitive processing and connection awareness
 * Where: Called after particle system initialization to maintain system coherence
 * How: Periodic monitoring of cognitive state with automatic adjustments and observations
 * 
 * Connects to:
 *     - static/js/engines/holographic-chamber.js: Calls maintainCognitiveConnection()
 *     - app.py: Reports cognitive status for system monitoring
 *     - evolution_engine.py: Logs cognitive patterns for learning
 */
function startCognitiveMaintenanceLoop() {
    if (cognitiveMaintenanceInterval) {
        clearInterval(cognitiveMaintenanceInterval);
    }
    
    cognitiveMaintenanceInterval = setInterval(() => {
        if (!holographicChamber) return;
        
        try {
            // Maintain cognitive connection with error handling
            const cognitiveStatus = holographicChamber.maintainCognitiveConnection();
            
            // Log cognitive health for debugging
            console.log('🧠 Cognitive Status:', {
                coherence: Math.round(cognitiveStatus.coherence * 100) + '%',
                energy: Math.round(cognitiveStatus.energy * 100) + '%',
                mode: cognitiveStatus.mode
            });
            
            // Switch to observing mode during extended idle periods
            const now = Date.now();
            const timeSinceLastInteraction = now - lastInteractionTime;
            
            if (timeSinceLastInteraction > IDLE_OBSERVATION_INTERVAL && 
                holographicChamber.currentMode === 'idle') {
                holographicChamber.setMode('observing');
                console.log('🔍 Entered observation mode - Clever is actively observing');
            }
            
            // Return to idle if recently active
            if (timeSinceLastInteraction < IDLE_OBSERVATION_INTERVAL && 
                holographicChamber.currentMode === 'observing') {
                holographicChamber.setMode('idle');
            }
            
        } catch (error) {
            console.error('❌ Cognitive maintenance error:', error);
            // Continue maintenance even if individual operations fail
        }
        
    }, COGNITIVE_MAINTENANCE_INTERVAL);
    
    console.log('🧠 Cognitive maintenance loop started - Clever will maintain full connection');
}

/**
 * Update Last Interaction Time
 * 
 * Why: Tracks user interaction for cognitive mode management
 * Where: Called by chat interface and other interaction handlers
 * How: Updates timestamp to manage idle/observation state transitions
 */
function updateLastInteraction() {
    if (holographicChamber && holographicChamber.currentMode === 'observing') {
        holographicChamber.setMode('idle');
    }
    // Update global interaction tracking for maintenance loop
    lastInteractionTime = Date.now();
}

/**
 * Initialize Particle System
 * 
 * Why: Start Clever cognitive visualization representing brain activity
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
            
            // Start cognitive maintenance cycle
            startCognitiveMaintenanceLoop();
            
            console.log('✅ Cognitive visualization active with maintenance loop');
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
                    updateLastInteraction();
                    holographicChamber.setMode('creative');
                    showSystemMessage('🎨 Creative mode activated');
                    break;
                case 's':
                    e.preventDefault();
                    updateLastInteraction();
                    holographicChamber.setMode('thinking');
                    showSystemMessage('🧠 Thinking mode activated');
                    break;
                case 'i':
                    e.preventDefault();
                    updateLastInteraction();
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
        // Update interaction tracking for cognitive maintenance
        updateLastInteraction();
        
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
        
        // Process shape data if present (mathematical shape generation)
        if (data.shape_data && holographicChamber && typeof holographicChamber.createMathematicalShape === 'function') {
            console.log('📐 Processing mathematical shape data:', data.shape_data);
            
            // Create mathematical shape formation with rotation
            holographicChamber.createMathematicalShape(data.shape_data);
            
            // Set to creative mode temporarily to highlight the mathematical shape
            holographicChamber.setMode('creative');
            
            // Start shape rotation after formation completes (1 second delay)
            setTimeout(() => {
                if (holographicChamber && typeof holographicChamber.startShapeRotation === 'function') {
                    holographicChamber.startShapeRotation();
                }
            }, 1000);
            
            // Return to observing mode after full rotation sequence (10 seconds total)
            setTimeout(() => {
                if (holographicChamber && typeof holographicChamber.setMode === 'function') {
                    holographicChamber.setMode('observing');
                }
            }, 10000);
        }
        // Handle legacy particle commands for backwards compatibility
        else if (data.requested_shape && holographicChamber) {
            console.log('🔄 Processing legacy shape command:', data.requested_shape);
            
            // Map to existing formations
            const shapeMap = {
                'cube': 'createCubeFormation',
                'sphere': 'createSphereFormation', 
                'torus': 'createTorusFormation',
                'helix': 'createHelixFormation',
                'spiral': 'createHelixFormation',
                'constellation': 'createConstellationFormation'
            };
            
            const formationMethod = shapeMap[data.requested_shape];
            if (formationMethod && typeof holographicChamber[formationMethod] === 'function') {
                holographicChamber[formationMethod]();
                holographicChamber.setMode('creative');
                
                // Return to idle after formation
                setTimeout(() => {
                    if (holographicChamber && typeof holographicChamber.setMode === 'function') {
                        holographicChamber.setMode('idle');
                    }
                }, 2000);
            }
        }
        
        // Display Clever's response
        if (data.response) {
            displayMessage(data.response, 'clever');
        } else {
            console.error('❌ No response in API data:', data);
            showSystemMessage('❌ No response received from Clever');
        }

        // Return to idle mode if no shape processing occurred
        if (!data.shape_data && !data.requested_shape && holographicChamber && typeof holographicChamber.setMode === 'function') {
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
 * Why: Bootstrap Clever's cognitive interface when DOM is ready
 * Where: Event listener for DOMContentLoaded ensures proper initialization order
 * How: Sequential initialization of particle system, chat interface, and cognitive features
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🧠 Clever Digital Brain Extension - Initializing...');
    
    initializeParticleSystem();
    initializeChatInterface();
    initializeCognitiveStatus();
    initializeKeyboardShortcuts();
    
    console.log('✅ Clever Digital Brain Extension - Ready for cognitive partnership with full connection monitoring');
});

/**
 * Initialize Cognitive Status Overlay
 * 
 * Why: Provides real-time monitoring of Clever's cognitive health and connection status
 * Where: Called during initialization to establish system monitoring interface
 * How: Creates status overlay and starts monitoring loop for particle system health
 */
function initializeCognitiveStatus() {
    if (typeof window.createCognitiveStatusOverlay === 'function') {
        window.createCognitiveStatusOverlay();
        console.log('✅ Cognitive status monitoring active');
    } else {
        console.warn('⚠️ Cognitive status component not available');
    }
}

/**
 * Generate Mathematical Shape
 * 
 * Why: Direct API interface for mathematical shape generation and visualization
 * Where: Can be called programmatically or via console for shape testing
 * How: Makes API request to shape generator, applies result to particle system
 * 
 * Connects to:
 *     - app.py: POST request to /api/generate_shape endpoint
 *     - shape_generator.py: Backend mathematical shape generation
 *     - holographic-chamber.js: createMathematicalShape() for visualization
 */
async function generateShape(shapeName, options = {}) {
    try {
        console.log(`📐 Generating mathematical shape: ${shapeName}`);
        
        const response = await fetch('/api/generate_shape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                shape: shapeName,
                ...options
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        if (data.success && data.shape) {
            console.log(`✅ Shape generated: ${data.shape.name} with ${data.shape.point_count} points`);
            
            // Apply to particle system if available
            if (holographicChamber && typeof holographicChamber.createMathematicalShape === 'function') {
                holographicChamber.createMathematicalShape(data.shape);
                holographicChamber.setMode('creative');
                
                // Return to observing mode after visualization
                setTimeout(() => {
                    if (holographicChamber && typeof holographicChamber.setMode === 'function') {
                        holographicChamber.setMode('observing');
                    }
                }, 4000);
            }
            
            return data.shape;
        } else {
            throw new Error(data.error || 'Shape generation failed');
        }
        
    } catch (error) {
        console.error('❌ Shape generation error:', error);
        showSystemMessage(`❌ Shape generation failed: ${error.message}`);
        throw error;
    }
}

/**
 * Get Available Shapes
 * 
 * Why: Provides list of available shapes for UI controls and help systems
 * Where: Called by UI components that need shape selection options
 * How: Fetches shape catalog from API with categorized information
 */
async function getAvailableShapes() {
    try {
        const response = await fetch('/api/available_shapes');
        const data = await response.json();
        
        if (data.success) {
            console.log(`📚 Available shapes: ${data.total_shapes} shapes in ${Object.keys(data.categories).length} categories`);
            return data.categories;
        } else {
            throw new Error(data.error || 'Failed to get available shapes');
        }
        
    } catch (error) {
        console.error('❌ Error fetching available shapes:', error);
        return {};
    }
}

// Expose shape functions globally for console access and testing
if (typeof window !== 'undefined') {
    window.generateShape = generateShape;
    window.getAvailableShapes = getAvailableShapes;
}

/**
 * Initialize Keyboard Shortcuts
 * 
 * Why: Provides quick access to cognitive interface controls for power users
 * Where: Called during initialization to establish global keyboard handlers
 * How: Event listeners for key combinations that control cognitive interface features
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl+Shift+S: Toggle cognitive status overlay
        if (e.ctrlKey && e.shiftKey && e.key === 'S') {
            e.preventDefault();
            if (typeof window.toggleCognitiveStatus === 'function') {
                window.toggleCognitiveStatus();
            }
        }
        
        // Ctrl+Shift+O: Switch to observation mode
        if (e.ctrlKey && e.shiftKey && e.key === 'O') {
            e.preventDefault();
            updateLastInteraction();
            if (holographicChamber && typeof holographicChamber.setMode === 'function') {
                holographicChamber.setMode('observing');
                console.log('🔍 Manual observation mode activated');
            }
        }
        
        // Ctrl+Shift+I: Return to idle mode
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            updateLastInteraction();
            if (holographicChamber && typeof holographicChamber.setMode === 'function') {
                holographicChamber.setMode('idle');
                console.log('🧠 Returned to idle cognitive mode');
            }
        }
    });
    
    console.log('⌨️ Keyboard shortcuts initialized (Ctrl+Shift+S, O, I)');
}

// Main initialization handled above via DOMContentLoaded event listener

// Export for debugging and external access
/*
Why: Provide access to internal state for development and debugging
Where: Available in browser console for runtime inspection
How: Global window properties for key functions and state
*/
/** @type {any} */ (window).CleverApp = {
    get holographicChamber() { return holographicChamber; },
    get isProcessingMessage() { return isProcessingMessage; },
    displayMessage,
    showSystemMessage,
    updateLastInteraction,
    version: '1.0.0'
};

console.log('📦 Clever main.js loaded and ready');
