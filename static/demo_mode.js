// CLEVER AI - ULTIMATE DEMO MODE
// Showcase all the badass particle effects and intelligence

class CleverDemoMode {
    constructor(cleverUI) {
        this.cleverUI = cleverUI;
        this.isActive = false;
        this.demoSequence = [
            { state: 'excited', duration: 2000, description: 'Excitement burst!' },
            { state: 'thinking', duration: 3000, description: 'Deep contemplation...' },
            { state: 'creative', duration: 2500, description: 'Creative inspiration!' },
            { state: 'focused', duration: 2000, description: 'Laser focus mode' },
            { pattern: 'neural', duration: 3000, description: 'Neural network formation' },
            { pattern: 'wave', duration: 2500, description: 'Wave propagation' },
            { pattern: 'explosion', duration: 2000, description: 'Energy explosion!' },
            { pattern: 'tunnel', duration: 2500, description: 'Focus tunnel' },
            { pattern: 'spiral', duration: 3000, description: 'Spiral dance' },
            { pulse: 2.0, duration: 1000, description: 'Maximum pulse!' },
            { state: 'idle', duration: 2000, description: 'Return to serenity' }
        ];
        this.currentStep = 0;
    }

    start() {
        if (this.isActive) return;
        
        console.log('🎬 Starting Clever UI Demo Mode - Prepare for BADASSERY!');
        this.isActive = true;
        this.currentStep = 0;
        
        // Add demo notification
        this.addDemoMessage('🎬 DEMO MODE: Showcasing the smartest, most badass UI ever created!');
        
        this.runNextStep();
    }

    stop() {
        this.isActive = false;
        console.log('🎬 Demo Mode: Complete');
        this.addDemoMessage('✨ Demo complete! This is your new reality - the most magical UI ever!');
    }

    runNextStep() {
        if (!this.isActive || this.currentStep >= this.demoSequence.length) {
            this.stop();
            return;
        }

        const step = this.demoSequence[this.currentStep];
        console.log(`🎬 Demo Step ${this.currentStep + 1}: ${step.description}`);
        
        // Add step message
        this.addDemoMessage(`${this.currentStep + 1}/${this.demoSequence.length}: ${step.description}`);

        // Execute the demo step
        if (step.state) {
            this.cleverUI.triggerStateTransition(step.state, step.duration);
        } else if (step.pattern) {
            this.cleverUI.particleSystem.morphToPattern(step.pattern);
        } else if (step.pulse) {
            this.cleverUI.triggerPulse(step.pulse);
        }

        // Schedule next step
        setTimeout(() => {
            this.currentStep++;
            this.runNextStep();
        }, step.duration);
    }

    addDemoMessage(text) {
        const chatLog = document.getElementById('chat-log');
        if (!chatLog) return;

        const wrap = document.createElement('div');
        wrap.className = 'chat-message-wrapper';

        const bubble = document.createElement('div');
        bubble.className = 'chat-message demo-message';
        bubble.style.background = 'linear-gradient(135deg, rgba(255, 200, 0, 0.2) 0%, rgba(255, 150, 0, 0.15) 100%)';
        bubble.style.borderColor = 'rgba(255, 200, 0, 0.3)';
        bubble.style.animation = 'messageAppear 0.4s ease-out, magicalGlow 2s ease-in-out infinite alternate';

        const who = document.createElement('div');
        who.className = 'sender';
        who.textContent = 'Demo System';
        who.style.color = 'rgba(255, 200, 0, 0.9)';

        const message = document.createElement('p');
        message.textContent = text;

        bubble.append(who, message);
        wrap.appendChild(bubble);
        chatLog.appendChild(wrap);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
}

// Global demo controls
function startCleverDemo() {
    if (window.cleverMagicalUI && window.cleverMagicalUI.isInitialized) {
        if (!window.cleverDemo) {
            window.cleverDemo = new CleverDemoMode(window.cleverMagicalUI);
        }
        window.cleverDemo.start();
    } else {
        console.error('❌ Clever Magical UI not initialized');
    }
}

// Auto-start demo after 3 seconds if no user interaction
let autoStartTimer = setTimeout(() => {
    const hasMessages = document.querySelectorAll('.chat-message').length > 0;
    if (!hasMessages && window.cleverMagicalUI) {
        console.log('🎬 Auto-starting demo mode...');
        startCleverDemo();
    }
}, 3000);

// Cancel auto-start on user interaction
document.addEventListener('click', () => {
    if (autoStartTimer) {
        clearTimeout(autoStartTimer);
        autoStartTimer = null;
    }
});

document.addEventListener('keydown', () => {
    if (autoStartTimer) {
        clearTimeout(autoStartTimer);
        autoStartTimer = null;
    }
});

// Global access
window.startCleverDemo = startCleverDemo;

// Console welcome message
console.log(`
🚀 CLEVER AI - ULTIMATE BADASS UI SYSTEM 🚀

Features:
• 30,000+ intelligent particles
• Real-time emotion detection
• Form-reactive morphing
• Voice-responsive animations
• Confidence-based visual effects
• 6 magical particle patterns
• Ultra-smooth 60fps rendering

Commands:
• startCleverDemo() - Run the full demo
• Escape key - Return to calm
• Space key - Trigger pulse
• Type anywhere - Intelligent reactions

This is the smartest, most badass UI you've ever seen!
`);

export { CleverDemoMode, startCleverDemo };
