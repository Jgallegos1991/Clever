// Diagnostic script to check Clever's initialization
console.log('🔍 Starting Clever diagnostics...');

// Check DOM elements
setTimeout(() => {
    console.log('=== DOM Element Check ===');
    
    const particles = document.getElementById('particles');
    console.log('Particles canvas:', particles ? '✅ Found' : '❌ Missing');
    
    const chatLog = document.getElementById('chat-log');
    console.log('Chat log:', chatLog ? '✅ Found' : '❌ Missing');
    
    const chatInput = document.getElementById('chat-input');
    console.log('Chat input:', chatInput ? '✅ Found' : '❌ Missing');
    
    const chatForm = document.getElementById('chat-form');
    console.log('Chat form:', chatForm ? '✅ Found' : '❌ Missing');
    
    const sendBtn = document.getElementById('send-btn');
    console.log('Send button:', sendBtn ? '✅ Found' : '❌ Missing');
    
    console.log('=== Function Availability ===');
    
    console.log('window.startHolographicChamber:', typeof window.startHolographicChamber);
    console.log('window.createChatBubble:', typeof window.createChatBubble);
    console.log('window.createCognitiveStatusOverlay:', typeof window.createCognitiveStatusOverlay);
    
    console.log('=== CleverApp State ===');
    
    if (window.CleverApp) {
        console.log('CleverApp.holographicChamber:', window.CleverApp.holographicChamber);
        console.log('CleverApp.isProcessingMessage:', window.CleverApp.isProcessingMessage);
        console.log('CleverApp version:', window.CleverApp.version);
    } else {
        console.log('❌ CleverApp not found');
    }
    
    console.log('=== CSS Computed Styles ===');
    
    if (chatInput) {
        const styles = window.getComputedStyle(chatInput);
        console.log('Chat input display:', styles.display);
        console.log('Chat input visibility:', styles.visibility);
        console.log('Chat input opacity:', styles.opacity);
    }
    
    const floatingInput = document.querySelector('.floating-input');
    if (floatingInput) {
        const styles = window.getComputedStyle(floatingInput);
        console.log('Floating input display:', styles.display);
        console.log('Floating input position:', styles.position);
        console.log('Floating input bottom:', styles.bottom);
        console.log('Floating input left:', styles.left);
        console.log('Floating input z-index:', styles.zIndex);
    } else {
        console.log('❌ .floating-input not found');
    }
    
    console.log('🔍 Diagnostics complete');
}, 2000);