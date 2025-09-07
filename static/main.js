// CLEVER AI - ULTIMATE BADASS UI INTEGRATION
// The most magical, intelligent UI system ever created

import { initVoice, speak as speakOut, isEnabled as ttsEnabled, setEnabled as setTTSEnabled, applyPersonaStyle } from './voice.js'

function $(id) { return document.getElementById(id); }

// Setup magical canvas for the ultimate UI
function setupMagicalCanvas() {
    const canvas = $('main-canvas');
    if (!canvas) {
        console.error('❌ Missing #main-canvas - creating one for maximum badassery');
        const magicalCanvas = document.createElement('canvas');
        magicalCanvas.id = 'main-canvas';
        magicalCanvas.style.position = 'fixed';
        magicalCanvas.style.top = '0';
        magicalCanvas.style.left = '0';
        magicalCanvas.style.width = '100vw';
        magicalCanvas.style.height = '100vh';
        magicalCanvas.style.pointerEvents = 'none';
        magicalCanvas.style.zIndex = '1';
        document.body.prepend(magicalCanvas);
        return magicalCanvas;
    }
    
    // Enhance existing canvas for badassery
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'auto';
    canvas.style.zIndex = '1';
    
    // Resize for crispy pixels
    function resizeCanvas() {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        canvas.style.width = rect.width + 'px';
        canvas.style.height = rect.height + 'px';
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    return canvas;
}

// Enhanced chat with magical integration
function setupMagicalChat(cleverUI) {
    const form = $('input-form');
    const input = $('chat-input');
    const log = $('chat-log');
    const voiceSelect = $('voice-select');
    const ttsToggle = $('tts-toggle');
    
    if (!form || !input || !log) {
        console.error('❌ Missing required chat elements');
        return;
    }
    
    // Enhanced focus system with magical feedback
    const focusInput = () => { 
        try { 
            input.focus({ preventScroll: true }); 
            cleverUI.onFormFocus();
        } catch(_) { 
            input.focus(); 
            cleverUI.onFormFocus();
        } 
    };
    
    // Magical click-to-focus with particle attraction
    document.addEventListener('pointerdown', (e) => {
        const tag = (e.target && e.target.tagName || '').toLowerCase();
        if (['input','textarea','button','select','a'].includes(tag)) return;
        focusInput();
    });
    
    // Type-anywhere with intelligent particle reactions
    document.addEventListener('keydown', (e) => {
        const active = document.activeElement;
        const isTyping = active && ['input','textarea'].includes((active.tagName||'').toLowerCase());
        
        if (isTyping) {
            // User is typing - show thinking particles
            if (e.key.length === 1) {
                cleverUI.onUserTyping(e.key);
            }
            return;
        }
        
        if (e.metaKey || e.ctrlKey || e.altKey) return;
        
        // Submit on Enter with magical effect
        if (e.key === 'Enter') {
            focusInput();
            cleverUI.triggerStateTransition('excited', 500);
            form.requestSubmit();
            e.preventDefault();
            return;
        }
        
        // Basic text keys with particle attraction
        if (e.key && e.key.length === 1) {
            focusInput();
            input.value = (input.value || '') + e.key;
            cleverUI.onUserTyping(e.key);
            e.preventDefault();
        }
        
        // Backspace with ripple effect
        if (e.key === 'Backspace') {
            focusInput();
            input.value = (input.value || '').slice(0, -1);
            cleverUI.onUserTyping('Backspace');
            e.preventDefault();
        }
    });
    
    // Enhanced input monitoring for intelligent reactions
    if (input) {
        input.addEventListener('input', (e) => {
            cleverUI.onFormInput(e.target.value);
        });
        
        input.addEventListener('focus', () => {
            cleverUI.onFormFocus();
        });
    }
    
    // Magical form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = (input.value || '').trim();
        if (!msg) return;

        input.value = '';
        addMessageToLog('You', msg);
        
        // Show processing with intelligent particles
        cleverUI.showProcessing();

        // Magical thinking placeholder
        const holder = document.createElement('div');
        holder.className = 'chat-message-wrapper';
        holder.innerHTML = `<div class="chat-message clever-message">
            <div class="sender">Clever</div>
            <p>✨ thinking with 30k particles...</p>
        </div>`;
        log.appendChild(holder);
        log.scrollTop = log.scrollHeight;

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({ message: msg })
            });
            let data = null;
            try { data = await res.json(); } catch {}

            holder.remove();

            if (!res.ok || !data || (!data.reply && !data.error)) {
                addMessageToLog('System Error', `Core did not return a reply (HTTP ${res.status}).`);
                cleverUI.triggerStateTransition('idle');
                return;
            }

            if (data.error && !data.reply) {
                addMessageToLog('Clever', "I'm in basic mode right now, but I'm with you.");
                cleverUI.triggerStateTransition('idle');
                return;
            }

            // Magical response with intelligent particle reactions
            addMessageToLog('Clever', data.reply);
            
            // Analyze response for magical effects
            const analysis = data.analysis || {};
            const emotion = determineEmotionFromResponse(data.reply, analysis);
            const confidence = analysis.confidence || 0.8;
            
            cleverUI.onCleverResponse(data.reply, { emotion, confidence, ...analysis });
            
            // Shape morphing based on intent
            if (analysis.detected_intent) {
                handleIntentMorphing(cleverUI, analysis);
            }
            
            // Broadcast for other magical systems
            window.dispatchEvent(new CustomEvent('clever-response', { 
                detail: { response: data.reply, metadata: { emotion, confidence, ...analysis } } 
            }));
            
        } catch (err) {
            holder.remove();
            console.error('[Clever UI] /chat failed:', err);
            addMessageToLog('System Error', "Connection to Clever's core lost.");
            cleverUI.triggerStateTransition('idle');
        }
    });
}

// Determine emotion from Clever's response for magical reactions
function determineEmotionFromResponse(reply, analysis) {
    const text = reply.toLowerCase();
    
    // Excitement indicators
    if (text.includes('amazing') || text.includes('incredible') || text.includes('fantastic')) {
        return 'excited';
    }
    
    // Creative indicators
    if (text.includes('create') || text.includes('design') || text.includes('imagine')) {
        return 'creative';
    }
    
    // Thoughtful indicators
    if (text.includes('analyze') || text.includes('consider') || text.includes('complex')) {
        return 'thoughtful';
    }
    
    // Confident indicators
    if (text.includes('definitely') || text.includes('clearly') || text.includes('obviously')) {
        return 'excited';
    }
    
    return 'neutral';
}

// Handle intent-based particle morphing
function handleIntentMorphing(cleverUI, analysis) {
    const intent = analysis.detected_intent;
    
    switch(intent) {
        case 'ask_question':
            cleverUI.triggerPulse(1.2);
            cleverUI.setIntelligenceMode('analytical');
            break;
        case 'creative_request':
            cleverUI.setIntelligenceMode('creative');
            break;
        case 'technical_help':
            cleverUI.setIntelligenceMode('analytical');
            break;
        case 'casual_chat':
            cleverUI.setIntelligenceMode('supportive');
            break;
        default:
            cleverUI.triggerPulse(0.8);
    }
    
    // Check for shape morphing commands
    const intents = analysis.intents || [];
    const shapeIntent = intents.find(i => i && i.name === 'ui.shape');
    if (shapeIntent && shapeIntent.details) {
        const shape = shapeIntent.details.toLowerCase();
        if (['sphere', 'neural', 'wave', 'explosion', 'tunnel', 'spiral'].includes(shape)) {
            cleverUI.particleSystem.morphToPattern(shape);
        }
    }
}

// Enhanced message logging with magical effects
function addMessageToLog(sender, message) {
    const chatLog = $('chat-log');
    if (!chatLog) throw new Error('Missing #chat-log element');
    
    const wrap = document.createElement('div');
    wrap.className = 'chat-message-wrapper';

    const bubble = document.createElement('div');
    bubble.className = `chat-message ${sender.toLowerCase()}-message`;

    const who = document.createElement('div');
    who.className = 'sender';
    who.textContent = sender;

    const text = document.createElement('p');
    text.textContent = message;

    bubble.append(who, text);
    wrap.appendChild(bubble);
    chatLog.appendChild(wrap);
    chatLog.scrollTop = chatLog.scrollHeight;
    
    // Trigger magical effects for Clever responses
    if (sender.toLowerCase() === 'clever' && window.cleverMagicalUI) {
        window.cleverMagicalUI.showComplete();
    }
}

// Voice recording with magical feedback
async function recordAndTranscribe(seconds = 6) {
    if (!navigator.mediaDevices?.getUserMedia) throw new Error('mic not available');
    
    // Trigger voice recording visual state
    if (window.cleverMagicalUI) {
        window.cleverMagicalUI.triggerStateTransition('focused', seconds * 1000);
    }
    
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const ctx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
    const src = ctx.createMediaStreamSource(stream);
    const processor = ctx.createScriptProcessor(4096, 1, 1);
    const bufs = [];
    
    processor.onaudioprocess = (e) => {
        const ch = e.inputBuffer.getChannelData(0);
        bufs.push(new Float32Array(ch));
        
        // Visual feedback for audio levels
        if (window.cleverMagicalUI) {
            const level = Math.max(...ch.map(Math.abs));
            window.cleverMagicalUI.particleSystem.addEnergyPulse(level * 0.1);
        }
    };
    
    src.connect(processor); 
    processor.connect(ctx.destination);
    await new Promise(r => setTimeout(r, Math.max(1000, seconds * 1000)));
    src.disconnect(); 
    processor.disconnect(); 
    stream.getTracks().forEach(t => t.stop());
    
    // Process audio data to WAV
    let length = bufs.reduce((a, b) => a + b.length, 0);
    const pcm16 = new Int16Array(length);
    let offset = 0;
    for (const b of bufs) {
        for (let i = 0; i < b.length; i++) {
            let s = Math.max(-1, Math.min(1, b[i]));
            pcm16[offset++] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }
    }
    
    // Write WAV header
    const buffer = new ArrayBuffer(44 + pcm16.byteLength);
    const view = new DataView(buffer);
    function wStr(o, s){ for(let i=0;i<s.length;i++) view.setUint8(o+i, s.charCodeAt(i)); }
    let p = 0;
    wStr(p, 'RIFF'); p += 4;
    view.setUint32(p, 36 + pcm16.byteLength, true); p += 4;
    wStr(p, 'WAVE'); p += 4;
    wStr(p, 'fmt '); p += 4;
    view.setUint32(p, 16, true); p += 4;
    view.setUint16(p, 1, true); p += 2;
    view.setUint16(p, 1, true); p += 2;
    view.setUint32(p, 16000, true); p += 4;
    view.setUint32(p, 16000 * 2, true); p += 4;
    view.setUint16(p, 2, true); p += 2;
    view.setUint16(p, 16, true); p += 2;
    wStr(p, 'data'); p += 4;
    view.setUint32(p, pcm16.byteLength, true); p += 4;
    new Int16Array(buffer, 44).set(pcm16);
    
    const wavBlob = new Blob([buffer], { type: 'audio/wav' });
    const fd = new FormData();
    fd.append('audio', wavBlob, 'speech.wav');
    const res = await fetch('/api/stt', { method: 'POST', body: fd });
    const data = await res.json();
    if (!res.ok) throw new Error(data?.error || 'stt failed');
    return String(data.text || '').trim();
}

// DOM Ready - Initialize the ULTIMATE BADASS system
window.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing ULTIMATE BADASS Clever UI System...');
    
    // Setup magical canvas
    const magicalCanvas = setupMagicalCanvas();
    
    // Initialize the magical UI system
    let cleverUI = null;
    try {
        cleverUI = new CleverMagicalUI();
        cleverUI.initialize(magicalCanvas);
        cleverUI.integrateChatEvents();
        
        // Make it globally accessible for maximum badassery
        window.cleverMagicalUI = cleverUI;
        console.log('✨ BADASS Clever UI System: ACTIVATED');
        
    } catch (error) {
        console.error('❌ Failed to initialize magical UI:', error);
        console.log('📱 Falling back to basic mode...');
    }
    
    // Setup enhanced chat functionality
    setupMagicalChat(cleverUI || { 
        onFormFocus: () => {}, 
        onUserTyping: () => {}, 
        showProcessing: () => {}, 
        showComplete: () => {},
        triggerStateTransition: () => {},
        onCleverResponse: () => {},
        triggerPulse: () => {},
        setIntelligenceMode: () => {}
    });
    
    // Enhanced voice integration
    const mic = $('mic-btn');
    if (mic) {
        mic.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                mic.disabled = true;
                const text = await recordAndTranscribe(6);
                if (text) {
                    const input = $('chat-input');
                    if (input) {
                        input.value = text;
                        $('input-form').requestSubmit();
                    }
                }
            } catch (err) {
                console.error('🎤 Voice input failed:', err);
                if (cleverUI) {
                    cleverUI.triggerStateTransition('idle');
                }
            } finally {
                mic.disabled = false;
            }
        });
    }
    
    // Demo mode button
    const demoBtn = $('demo-btn');
    if (demoBtn) {
        demoBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (window.startCleverDemo) {
                window.startCleverDemo();
            } else {
                console.log('🎬 Demo mode not available');
            }
        });
    }
    
    // Enhanced TTS integration
    try { 
        initVoice({ selectEl: $('voice-select'), toggleEl: $('tts-toggle') }); 
        
        // Auto-speak Clever responses with magical timing
        const origAdd = addMessageToLog;
        addMessageToLog = (sender, message) => {
            origAdd(sender, message);
            if (sender.toLowerCase() === 'clever' && ttsEnabled()) {
                // Delay speech to sync with visual effects
                setTimeout(() => speakOut(message), 300);
            }
        };
        
    } catch (error) {
        console.log('🔊 Voice features unavailable');
    }
    
    // React TTS style to persona changes
    window.addEventListener('clever-response', (ev) => {
        try { 
            applyPersonaStyle(ev.detail?.metadata?.activePersona || ''); 
        } catch (_) {}
    });
    
    // Global keyboard shortcuts for maximum badassery
    document.addEventListener('keydown', (e) => {
        // Escape to trigger calm state
        if (e.key === 'Escape' && cleverUI) {
            cleverUI.triggerStateTransition('idle', 800);
        }
        
        // Space for pulse (when not typing)
        if (e.key === ' ' && !e.target.matches('input, textarea') && cleverUI) {
            cleverUI.triggerPulse(1.0);
            e.preventDefault();
        }
    });
    
    console.log('🎯 BADASS Clever UI System: FULLY OPERATIONAL');
});
