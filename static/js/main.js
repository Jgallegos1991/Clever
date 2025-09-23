// Clever Digital Brain Extension - Main Logic
console.log('🧠 Clever initializing...');

let holographicChamber = null;

// Lifecycle timing constants (ms)
// Why: Centralized timing ensures consistent cognitive rhythm & easy tuning
// Where: Consumed by createChatBubble() + scheduleAutoHide()
// How: Single source of truth; CSS variables mirror these for transitions
const BUBBLE_FADE_IN_MS = 500;
const BUBBLE_VISIBLE_MS = 6000; // base visible window before fade
const BUBBLE_FADE_OUT_MS = 800;
const BUBBLE_TOTAL_LIFETIME = BUBBLE_FADE_IN_MS + BUBBLE_VISIBLE_MS + BUBBLE_FADE_OUT_MS;

// Respect reduced motion preference
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const EFFECTIVE_FADE_IN = prefersReducedMotion ? 0 : BUBBLE_FADE_IN_MS;
const EFFECTIVE_FADE_OUT = prefersReducedMotion ? 0 : BUBBLE_FADE_OUT_MS;

document.addEventListener('DOMContentLoaded', function() {
    initializeParticleSystem();
    initializeChatInterface();
    initializeKeyboardControls();
    console.log('✨ Clever ready!');
});

function initializeParticleSystem() {
    // Why: Particle canvas is the cognitive stage; must initialize or gracefully degrade
    // Where: Connects to holographic-chamber.js which exposes startHolographicChamber
    // How: Locate canonical #particles (contract in index.html). Fallback logged if absent
    const canvas = document.getElementById('particles');
    if (!canvas) {
        console.error('❌ Canvas #particles not found');
        return;
    }
    
    // Ensure canvas is properly sized
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.display = 'block';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '1';
    canvas.style.pointerEvents = 'none';
    
    console.log(`🎨 Canvas configured: ${canvas.width}x${canvas.height}`);
    
    // Test basic canvas functionality
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ Canvas context not available');
        return;
    }
    
    // Clear canvas with a test pattern first
    ctx.fillStyle = '#0B0F14';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    console.log('✅ Canvas cleared and ready');
    
    if (canvas instanceof HTMLCanvasElement && typeof window.startHolographicChamber === 'function') {
        try {
            holographicChamber = window.startHolographicChamber(canvas);
            if (holographicChamber) {
                window.holographicChamber = holographicChamber;
                console.log('✅ Particle system ready');
                console.log(`📊 Particles created: ${holographicChamber.particles ? holographicChamber.particles.length : 'Unknown'}`);
                
                // Let Clever's natural thinking patterns initialize
                // Her particles represent her cognitive state and thoughts
                console.log('🧠 Clever\'s particle system ready - letting her think naturally');
            } else {
                console.error('❌ startHolographicChamber returned null');
            }
        } catch (error) {
            console.error('❌ Particle system initialization failed:', error);
        }
    } else {
        console.error('❌ startHolographicChamber function not available');
    }
}

function initializeChatInterface() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (!chatInput || !sendBtn) return;
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
    
    sendBtn.addEventListener('click', sendMessage);
}

function initializeKeyboardControls() {
    document.addEventListener('keydown', function(e) {
        if (!e.shiftKey || !holographicChamber) return;
        
        const formations = {
            'c': 'cube',
            's': 'sphere',
            'h': 'helix',
            't': 'torus',
            'w': 'wave'
        };
        
        const formation = formations[e.key.toLowerCase()];
        if (formation) {
            e.preventDefault();
            holographicChamber.morphToFormation(formation);
        }
    });
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    if (!(input instanceof HTMLInputElement)) return;
    const message = input.value.trim();
    
    if (!message) return;
    
    input.value = '';
    createChatBubble(message, 'user');
    
    // Clever's particles respond to conversation state
    if (holographicChamber) {
        holographicChamber.summon(); // Clever focuses attention when user speaks
    }
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Clever enters dialogue state when responding
        if (holographicChamber) {
            holographicChamber.dialogue();
        }
        
        createChatBubble(data.response || 'I hear you!', 'ai');
        
        // Return to idle/thinking state after responding
        setTimeout(() => {
            if (holographicChamber) {
                holographicChamber.idle();
            }
        }, 3000);
        
    } catch (error) {
        console.error('Chat error:', error);
        createChatBubble('Processing... try again!', 'ai');
        
        // Return to idle state even on error
        if (holographicChamber) {
            setTimeout(() => holographicChamber.idle(), 2000);
        }
    }
}

function createChatBubble(text, type = 'ai') {
    /**
     * Why: Render an ephemeral thought bubble that reinforces conversational flow without clutter
     * Where: Appended under #chat-log; timeline interacts with particle engine (thinking/respond states)
     * How: Create DOM node, apply manifest/fade classes, schedule auto-hide respecting reduced motion
     */
    const chatLog = document.getElementById('chat-log');
    if (!chatLog) return;

    const bubble = document.createElement('div');
    // Map internal type to stylesheet naming (ai -> clever)
    const roleClass = type === 'user' ? 'user' : 'clever';
    bubble.className = 'chat-message manifesting ' + roleClass;
    bubble.textContent = text;

    chatLog.appendChild(bubble);

    // Force reflow then manifest
    requestAnimationFrame(() => {
        bubble.classList.add('manifested');
        bubble.classList.remove('manifesting');
    });

    scheduleAutoHide(bubble);
    announceForScreenReaders(text);
    return bubble;
}

function scheduleAutoHide(bubble) {
    /**
     * Why: Keep interface uncluttered; prevent memory bloat / DOM growth
     * Where: Called by createChatBubble; interacts with CSS fade transitions
     * How: Timer -> add fade-out class -> remove after transition (or immediate if reduced motion)
     */
    const visibleWindow = BUBBLE_VISIBLE_MS;
    const preRemovalDelay = EFFECTIVE_FADE_OUT || 0;

    setTimeout(() => {
        if (!bubble.isConnected) return;
        bubble.classList.add('fade-out');
        setTimeout(() => {
            if (bubble.isConnected) bubble.remove();
        }, preRemovalDelay + 30); // 30ms buffer
    }, visibleWindow);
}

function announceForScreenReaders(text) {
    /**
     * Why: Accessibility — provide conversational updates to assistive tech without duplicating UI noise
     * Where: Live region element #sr-live (created lazily if absent)
     * How: Inject sanitized text into aria-live region; throttle floods if needed
     */
    const MAX_LEN = 400;
    const sanitized = (text || '').slice(0, MAX_LEN).replace(/\s+/g, ' ').trim();
    if (!sanitized) return;
    let region = document.getElementById('sr-live');
    if (!region) {
        region = document.createElement('div');
        region.id = 'sr-live';
        region.setAttribute('aria-live', 'polite');
        region.setAttribute('aria-atomic', 'false');
        region.style.position = 'absolute';
        region.style.left = '-9999px';
        document.body.appendChild(region);
    }
    // Clear to retrigger announcement
    region.textContent = '';
    setTimeout(() => { region.textContent = sanitized; }, 10);
}

