// Chat Fade Component - Core Animation System
// Why: Handles sophisticated fade transitions for chat bubble lifecycle
// Where: Integrated with main.js chat bubble creation and animation pipeline
// How: Provides optimized CSS transitions with reduced motion support

console.log('💬 Chat fade component loaded');

window.chatFadeComponent = {
    initialized: true,
    version: '2.0.0',
    
    // Optimized fade timing constants
    FADE_IN_DURATION: 400,
    FADE_OUT_DURATION: 600,
    HOLD_DURATION: 5000,
    
    // Apply enhanced fade effects to chat bubble
    enhanceFade: function(element) {
        if (!element || typeof element.classList === 'undefined') return;
        
        element.style.transition = `opacity ${this.FADE_IN_DURATION}ms cubic-bezier(0.4, 0.0, 0.2, 1), transform ${this.FADE_IN_DURATION}ms cubic-bezier(0.4, 0.0, 0.2, 1)`;
        
        // Respect reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            element.style.transition = 'none';
        }
    }
};