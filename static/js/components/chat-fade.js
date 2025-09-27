/*
Chat Fade Component - Message Bubble Lifecycle Management

Why: Handles sophisticated fade transitions for chat bubble lifecycle
Where: Loaded by templates/index.html to support chat interface message display
How: Creates animated message bubbles with fade-in/fade-out lifecycle management

Connects to:
    - templates/index.html: Chat bubbles inserted into #chat-log container
    - static/js/main.js: displayMessage() calls createChatBubble()
    - static/css/style.css: Chat bubble styling and fade animations
    - app.py: Message content comes from API responses
*/

console.log('💬 Chat fade component loading...');

// Chat bubble lifecycle configuration
/*
Why: Timing constants for smooth chat bubble appearance and disappearance
Where: Used by createChatBubble() and scheduleAutoHide() for consistent timing
How: Coordinated with CSS transition durations for synchronized animations

Connects to:
    - static/css/style.css: CSS transition durations should match these values
    - static/js/main.js: BUBBLE_FADE timing constants should be synchronized
*/
const CHAT_CONFIG = {
    FADE_IN_MS: 500,
    BASE_VISIBLE_MS: 5000,  // Minimum display time (increased from 3000)
    READING_SPEED_WPM: 180, // Slightly slower reading speed for better comprehension
    FADE_OUT_MS: 1000,
    PERSISTENCE_MODE: false, // When true, messages stay visible much longer
    PERSISTENCE_MULTIPLIER: 4 // Multiply display time when in persistence mode
};

// Make config globally accessible for main.js toggle
window.CHAT_CONFIG = CHAT_CONFIG;

/**
 * Calculate Display Duration
 * 
 * Why: Dynamic message display time based on text length for comfortable reading
 * Where: Called by createChatBubble() to determine how long to show each message
 * How: Calculates reading time based on word count and adds buffer time
 * 
 * @param {string} text - Message content to analyze
 * @returns {number} Display duration in milliseconds
 */
function calculateDisplayDuration(text) {
    const wordCount = text.trim().split(/\s+/).length;
    const readingTimeMs = (wordCount / CHAT_CONFIG.READING_SPEED_WPM) * 60 * 1000;
    
    // Ensure minimum display time and add comfortable buffer
    let displayDuration = Math.max(
        CHAT_CONFIG.BASE_VISIBLE_MS,
        readingTimeMs + 3000 // Add 3 seconds buffer for processing and reflection
    );
    
    // Apply persistence multiplier if enabled
    if (CHAT_CONFIG.PERSISTENCE_MODE) {
        displayDuration *= CHAT_CONFIG.PERSISTENCE_MULTIPLIER;
        console.log(`💬 Persistence mode: extending to ${Math.round(displayDuration/1000)}s`);
    }
    
    console.log(`💬 Message: ${wordCount} words, ${Math.round(displayDuration/1000)}s display time`);
    return displayDuration;
}

/**
 * Create Chat Bubble
 * 
 * Why: Display conversation messages with smooth fade animations for cognitive flow
 * Where: Called by main.js displayMessage() function for all chat interactions
 * How: Creates DOM element, applies styling, handles lifecycle, auto-removal
 * 
 * @param {string} text - Message content to display
 * @param {string} sender - Message sender type ('user', 'clever', 'system')
 * 
 * Connects to:
 *     - templates/index.html: Inserts into #chat-log container
 *     - static/css/style.css: Uses .chat-message styling classes
 *     - static/js/main.js: Called by displayMessage() function
 */
function createChatBubble(text, sender = 'system') {
    const chatLog = document.getElementById('chat-log');
    if (!chatLog) {
        console.error('❌ Chat log container not found');
        return;
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    // Create message content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    // Create message metadata
    const metaDiv = document.createElement('div');
    metaDiv.className = 'message-meta';
    metaDiv.textContent = new Date().toLocaleTimeString();
    
    // Assemble message
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(metaDiv);
    
    // Add to chat log
    chatLog.appendChild(messageDiv);
    
    // Trigger fade-in animation
    requestAnimationFrame(() => {
        messageDiv.classList.add('show');
    });
    
    // Auto-scroll to bottom
    chatLog.scrollTop = chatLog.scrollHeight;
    
    // Calculate display duration based on message length
    const displayDuration = calculateDisplayDuration(text);
    
    // Schedule auto-hide with length-based timing (skip if persistence mode with very long messages)
    const shouldAutoHide = !CHAT_CONFIG.PERSISTENCE_MODE || displayDuration < 30000; // Don't auto-hide if > 30s in persistence mode
    
    if (shouldAutoHide) {
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.classList.add('fade-out');
                setTimeout(() => {
                    if (messageDiv.parentNode) {
                        messageDiv.remove();
                    }
                }, CHAT_CONFIG.FADE_OUT_MS);
            }
        }, displayDuration);
    } else {
        console.log(`💬 Message will persist indefinitely (${Math.round(displayDuration/1000)}s calculated)`);
    }
    
    console.log(`💬 Chat bubble created: ${sender} - ${text.substring(0, 50)}...`);
}

/**
 * Clear All Chat Messages
 * 
 * Why: Provide ability to clear conversation history for fresh cognitive sessions
 * Where: Can be called by main.js or external systems for chat management
 * How: Removes all message elements from chat log container
 * 
 * Connects to:
 *     - templates/index.html: Clears #chat-log container
 *     - Keyboard shortcuts: Could be triggered by clear command
 */
function clearChatMessages() {
    const chatLog = document.getElementById('chat-log');
    if (chatLog) {
        chatLog.innerHTML = '';
        console.log('💬 Chat messages cleared');
    }
}

/**
 * Get Message Count
 * 
 * Why: Track conversation length for cognitive load management
 * Where: Available for monitoring and analytics systems
 * How: Counts visible message elements in chat log
 * 
 * Returns: Number of currently displayed messages
 */
function getMessageCount() {
    const chatLog = document.getElementById('chat-log');
    return chatLog ? chatLog.children.length : 0;
}

// Export functions for global access
/*
Why: Make chat bubble functions available to main.js and other components
Where: Global window object for cross-component communication
How: Attaches functions to window for universal access
*/
window.createChatBubble = createChatBubble;
window.clearChatMessages = clearChatMessages;
window.getMessageCount = getMessageCount;

// Component health check
/*
Why: Verify chat system is properly initialized and ready for use
Where: Run at component load time for early error detection
How: Check for required DOM elements and log initialization status
*/
function initializeChatComponent() {
    const chatLog = document.getElementById('chat-log');
    if (!chatLog) {
        console.warn('⚠️ Chat log container not found - chat bubbles may not display');
        return false;
    }
    
    console.log('✅ Chat fade component initialized successfully');
    return true;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeChatComponent);
} else {
    initializeChatComponent();
}

console.log('💬 Chat fade component loaded and ready');
