// Clever Digital Brain Extension - Main Logic
console.log('🧠 Clever initializing...');

let holographicChamber = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeParticleSystem();
    initializeChatInterface();
    initializeKeyboardControls();
    console.log('✨ Clever ready!');
});

function initializeParticleSystem() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) {
        console.error('❌ Canvas not found');
        return;
    }
    
    if (typeof window.startHolographicChamber === 'function') {
        holographicChamber = window.startHolographicChamber(canvas);
        window.holographicChamber = holographicChamber;
        console.log('✅ Particle system ready');
        
        setTimeout(() => {
            if (holographicChamber && holographicChamber.morphToFormation) {
                holographicChamber.morphToFormation('whirlpool');
            }
        }, 2000);
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
    const message = input.value.trim();
    
    if (!message) return;
    
    input.value = '';
    createChatBubble(message, 'user');
    
    if (holographicChamber) {
        holographicChamber.summon();
    }
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        createChatBubble(data.response || 'I hear you!', 'ai');
        
    } catch (error) {
        console.error('Chat error:', error);
        createChatBubble('Processing... try again!', 'ai');
    }
}

function createChatBubble(text, type = 'ai') {
    const chatLog = document.getElementById('chat-log');
    if (!chatLog) return;
    
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ' + type;
    bubble.textContent = text;
    
    const x = Math.random() * (window.innerWidth - 300);
    const y = Math.random() * (window.innerHeight - 200) + 50;
    
    bubble.style.left = x + 'px';
    bubble.style.top = y + 'px';
    
    chatLog.appendChild(bubble);
    
    setTimeout(() => {
        if (bubble.parentNode) {
            bubble.parentNode.removeChild(bubble);
        }
    }, 20000);
}

