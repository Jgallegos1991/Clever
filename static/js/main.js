// Track last AI bubble globally for positioning the analysis card
let lastAiEl = null;

document.addEventListener('DOMContentLoaded', () => {
  const userInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-btn');
  const chatLog = document.getElementById('chat-log');
  const analysisPanel = document.querySelector('.analysis-panel');
  const modeBtn = document.getElementById('mode-btn');

<<<<<<< HEAD
  // Initialize holographic chamber with debugging
  const debugDiv = document.getElementById('debug-info');
  const canvasElem = document.getElementById('particles');
  
  debugDiv.innerHTML = 'Canvas found: ' + (canvasElem ? 'YES' : 'NO');
  console.log('🔧 Main.js initializing holographic chamber...');
  console.log('🎯 Canvas element found:', canvasElem);
  console.log('🎨 Canvas dimensions:', canvasElem?.offsetWidth, 'x', canvasElem?.offsetHeight);
  
  debugDiv.innerHTML += '<br/>startFunction: ' + typeof window['startHolographicChamber'];
  
  if (canvasElem instanceof HTMLCanvasElement && typeof window['startHolographicChamber'] === 'function') {
    console.log('🚀 Starting holographic chamber from main.js...');
    debugDiv.innerHTML += '<br/>Initializing particles...';
    try {
      window['holographicChamber'] = window['startHolographicChamber'](canvasElem);
      console.log('✅ Holographic chamber initialized:', window['holographicChamber']);
      debugDiv.innerHTML += '<br/>✅ Particles initialized!';
    } catch (error) {
      console.error('❌ Particle initialization failed:', error);
      debugDiv.innerHTML += '<br/>❌ Init failed: ' + error.message;
    }
  } else {
    console.error('❌ Cannot initialize holographic chamber:', {
      canvas: canvasElem,
      startFunction: typeof window['startHolographicChamber']
    });
    debugDiv.innerHTML += '<br/>❌ Missing function or canvas';
=======
  // Initialize particle canvas if present
  const canvasElem = document.getElementById('particles');
  if (canvasElem instanceof HTMLCanvasElement && typeof window.startParticles === 'function') {
    window.startParticles(canvasElem, { count: 4000 });
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
  }

  // Send on click or Enter
  sendButton?.addEventListener('click', () => sendMessage());
  userInput?.addEventListener('keypress', e => {
    if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
  });

  showStatus('Ambient creativity waiting…');

  // Animate panels in as if condensing from the swarm
  const panels = document.querySelectorAll('.panel');
  panels.forEach(p => {
    p.classList.add('appear');
    p.addEventListener('animationend', () => p.classList.remove('appear'), { once: true });
  });

  // Summon behavior: on input focus, ripple the grid and add a subtle pulse
  userInput?.addEventListener('focus', () => {
    const grid = document.querySelector('.grid-overlay');
    if (grid) {
      grid.classList.add('ripple');
      setTimeout(() => grid.classList.remove('ripple'), 600);
    }
    if (typeof window.triggerPulse === 'function') window.triggerPulse(0.5);
  });

<<<<<<< HEAD
  // Click anywhere to focus input (immersive mode)
  document.addEventListener('click', (e) => {
    const target = e.target;
    // Don't interfere with actual clickable elements
    if (target instanceof Element && 
        target.matches('input, button, select, textarea, a, [contenteditable], .message, .chip')) {
      return;
    }
    // Focus the input field when clicking anywhere else
    if (userInput instanceof HTMLInputElement) {
      userInput.focus();
      // Trigger the same grid ripple effect as manual focus
      const grid = document.querySelector('.grid-overlay');
      if (grid) {
        grid.classList.add('ripple');
        setTimeout(() => grid.classList.remove('ripple'), 600);
      }
      if (typeof window.triggerPulse === 'function') window.triggerPulse(0.3);
    }
  });

  // Auto-focus input on any keypress when no other element is focused
  document.addEventListener('keydown', (e) => {
    const target = e.target;
    // Don't interfere if user is already typing in an input
    if (target instanceof Element && 
        target.matches('input, textarea, [contenteditable]')) {
      return;
    }
    // Don't interfere with special keys
    if (e.ctrlKey || e.altKey || e.metaKey || e.key === 'Tab' || e.key === 'Escape') {
      return;
    }
    // Focus input and let the character through
    if (userInput instanceof HTMLInputElement) {
      userInput.focus();
    }
  });

=======
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
  // Mode button is a status chip, not a toggle (auto-inferred mode)
  if (modeBtn) {
    modeBtn.addEventListener('click', () => {
      modeBtn.title = 'Mode adapts automatically based on your intent';
    });
  }

  // Maintain snap on resize and when user scrolls chat
  window.addEventListener('resize', () => {
    if (lastAiEl) snapAnalysisTo(lastAiEl);
  });
  chatLog?.addEventListener('scroll', () => {
    if (lastAiEl) snapAnalysisTo(lastAiEl);
  });
});

async function sendMessage() {
  const inputElem = document.getElementById('chat-input');
  if (!(inputElem instanceof HTMLInputElement)) return;
  const text = inputElem.value.trim();
  if (!text) return;
  appendMessage('user', text);
  // Update status indicator (thinking) and mode chip based on initial guess
  setSelfcheckState('thinking', 'Thinking…');
  updateModeChip(inferModeFromAnalysis({ intent: guessIntentFromText(text) }, text));
<<<<<<< HEAD
  
  // Trigger particle summon state
  if (window.holographicChamber) {
    window.holographicChamber.summon();
  }
=======
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
  // Try to morph shape immediately from user request (e.g., "form a cube")
  const preShape = inferShapeFromTextAndAnalysis(text, null);
  if (preShape && typeof window.morphForIntent === 'function') {
    window.morphForIntent(preShape);
  }
  // Visual ripple: show grid thinking effect
  const grid = document.querySelector('.grid-overlay');
  if (grid) {
    grid.classList.add('ripple');
    setTimeout(() => grid.classList.remove('ripple'), 600);
  }
  inputElem.value = '';
  showStatus('Ideas crystallizing...');
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    const reply = data.response || '...';
  const aiEl = appendMessage('ai', reply);
<<<<<<< HEAD
  
    // Switch to dialogue state when receiving response
    if (window.holographicChamber) {
      window.holographicChamber.dialogue();
    }
=======
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
    if (data && typeof data === 'object') {
      updateAnalysis(data.analysis || {});
      // Update adaptive mode chip from analysis + reply semantics
      const mode = inferModeFromAnalysis(data.analysis || {}, reply);
      updateModeChip(mode);
<<<<<<< HEAD
      // Morph holographic chamber based on shape intent
      
      // Show/hide glass panels based on conversation state
=======
      // Morph field based on detected shape intent
      const shape = inferShapeFromTextAndAnalysis(null, data.analysis || {});
      if (shape && typeof window.morphForIntent === 'function') {
        window.morphForIntent(shape);
      }
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
      // Snap analysis panel under the latest AI message and animate highlight
      if (aiEl) {
        lastAiEl = aiEl;
        snapAnalysisTo(aiEl);
        const panel = document.querySelector('.analysis-panel');
        if (panel) {
          panel.classList.add('updated');
          setTimeout(() => panel.classList.remove('updated'), 800);
        }
      }
    }
    // Particle reactions
    if (typeof window.updateFieldMode === 'function') {
      window.updateFieldMode(data.mood || 'Base');
    }
    if (typeof window.triggerPulse === 'function') {
      window.triggerPulse(data.particle_intensity || 0.5);
    }
    if (typeof window.morphForIntent === 'function') {
      // Map approach/intent to explicit morph shape for clearer storytelling
      const intent = mapApproachToIntent(data.approach, data?.analysis?.intent);
      window.morphForIntent(intent);
    }
    // AI response complete: visual and status update
    if (/money|dollar|finance/i.test(reply)) {
      window.morphForIntent('-'); // text morph to $ or text morph to '💰'
      if (window.triggerPulse) window.triggerPulse(1.0);
    }
  // Mark done and show copy
  setSelfcheckState('ok', 'Done');
<<<<<<< HEAD
  
    // Return to idle state after a delay
    setTimeout(() => {
      if (window.holographicChamber) {
        window.holographicChamber.idle();
      }
    }, 3000);
=======
>>>>>>> 332a7fbc65d1718ef294b5be0d4b6c43bef8468b
  showStatus('Energy takes shape.');
    // After a delay, return to idle microcopy
    setTimeout(() => {
      showStatus('Ambient creativity waiting...');
  const dissolve = window['dissolveToSwarm'];
  if (typeof dissolve === 'function') dissolve();
    }, 2000);
  } catch (err) {
    appendMessage('ai', 'Error.');
    console.error(err);
  setSelfcheckState('error', 'Error');
  showStatus('Error occurred');
  }
}

function appendMessage(who, text) {
  const log = document.getElementById('chat-log');
  const wrap = document.createElement('div');
  wrap.classList.add('message', who, 'manifesting');
  // Optional role chip like screenshot (User / Clever)
  const chip = document.createElement('div');
  chip.className = 'chip';
  chip.textContent = who === 'user' ? 'User' : 'Clever';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  wrap.append(chip, bubble);
  log.append(wrap);
  // animate in
  requestAnimationFrame(() => wrap.classList.add('manifested'));
  log.scrollTop = log.scrollHeight;
  return wrap;
}

function mapApproachToIntent(approach, fallbackIntent){
  const a = String(approach||'').toLowerCase();
  const f = String(fallbackIntent||'').toLowerCase();
  if (a.includes('creative')) return 'creative'; // torus
  if (a.includes('deep') || a.includes('analy')) return 'deep'; // cube
  if (a.includes('explore') || a.includes('discover')) return 'galaxy';
  if (f.includes('casual') || f.includes('chat')) return 'casual_chat'; // sphere
  if (f.includes('creative')) return 'creative';
  if (f.includes('deep')) return 'deep';
  return 'casual_chat';
}

function updateAnalysis(analysis) {
  const intentEl = document.getElementById('intent');
  const sentimentEl = document.getElementById('sentiment');
  const entitiesEl = document.getElementById('entities');
  const keywordsEl = document.getElementById('keywords');
  if (!intentEl || !sentimentEl || !entitiesEl || !keywordsEl) return;

  intentEl.textContent = 'Intent: ' + (analysis.intent || '—');
  const s = analysis.sentiment;
  // Compute sentiment text
  let sentimentText = '—';
  if (s && typeof s.compound === 'number') {
    sentimentText = s.compound.toFixed(2);
  } else if (typeof s === 'number') {
    sentimentText = s.toString();
  }
  sentimentEl.textContent = 'Sentiment: ' + sentimentText;
  entitiesEl.textContent = 'Entities: ' + ((analysis.entities||[]).join(', ') || '—');
  keywordsEl.textContent = 'Keywords: ' + ((analysis.keywords||[]).join(', ') || '—');
}

function showStatus(msg) {
  const status = document.getElementById('selfcheck');
  if (status) status.textContent = msg;
}

// Position the analysis panel under the target element (AI message)
function snapAnalysisTo(targetEl) {
  const el = document.querySelector('.analysis-panel');
  if (!el || !targetEl) return;
  if (!(el instanceof HTMLElement)) return;
  const rect = targetEl.getBoundingClientRect();
  const margin = 8;
  // Prefer bottom-left of the ai bubble
  let top = rect.bottom + margin;
  let left = rect.left;
  // Clamp within viewport
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const panelWidth = Math.min(420, vw - 16);
  left = Math.max(8, Math.min(left, vw - panelWidth - 8));
  if (top > vh - 100) top = vh - 100; // avoid falling off bottom
  el.style.position = 'fixed';
  el.style.top = `${top}px`;
  el.style.left = `${left}px`;
  el.style.right = 'auto';
  el.style.bottom = 'auto';
}

// --- Helpers: intent/mode/shape + selfcheck lifecycle ---------------------

function updateModeChip(mode) {
  const modeBtn = document.getElementById('mode-btn');
  if (!(modeBtn instanceof HTMLElement)) return;
  const label = String(mode || 'Auto');
  modeBtn.textContent = label.split(' ').map(s => s[0]).join('').slice(0, 2) || 'A';
  modeBtn.title = `Mode: ${label} (auto)`;
  if (typeof window.updateFieldMode === 'function') {
    try { window.updateFieldMode(label); } catch (_) { /* noop */ }
  }
}

function guessIntentFromText(text) {
  const t = String(text || '').toLowerCase();
  if (/cube|square|box/.test(t)) return 'shape_request';
  if (/torus|donut|ring/.test(t)) return 'shape_request';
  if (/sphere|ball|circle/.test(t)) return 'shape_request';
  if (/analy(z|s)e|deep|why|architecture|design/.test(t)) return 'analysis';
  if (/idea|brainstorm|creative|imagine/.test(t)) return 'creative';
  if (/help|stuck|issue|error|bug/.test(t)) return 'support';
  if (t.length < 24) return 'quick';
  return 'general';
}

function inferModeFromAnalysis(analysis, replyText) {
  const intent = String((analysis && analysis.intent) || guessIntentFromText(replyText)).toLowerCase();
  if (intent.includes('creative')) return 'Creative';
  if (intent.includes('analysis') || intent.includes('deep')) return 'Deep Dive';
  if (intent.includes('support') || /help|stuck|issue/.test(String(replyText||'').toLowerCase())) return 'Support';
  if (intent.includes('quick') || String(replyText||'').length < 36) return 'Quick Hit';
  return 'Auto';
}

function inferShapeFromTextAndAnalysis(userText, analysis) {
  const t = String(userText || (analysis && analysis.user_input) || '').toLowerCase();
  // Direct shape mentions take precedence
  if (/cube|box|square/.test(t)) return 'cube';
  if (/torus|donut|ring/.test(t)) return 'torus';
  if (/sphere|ball|circle/.test(t)) return 'sphere';
  if (/galaxy|spiral|swirl/.test(t)) return 'galaxy';
  if (/grid|plane/.test(t)) return 'grid';
  if (/wave|ripple/.test(t)) return 'wave';
  // Infer from analysis intent if available
  const intent = String(analysis && analysis.intent || '').toLowerCase();
  if (intent.includes('shape')) return 'cube';
  if (intent.includes('creative')) return 'torus';
  if (intent.includes('deep')) return 'cube';
  if (intent.includes('casual') || intent.includes('chat')) return 'sphere';
  if (intent.includes('explore')) return 'galaxy';
  return '';
}

function setSelfcheckState(state, text) {
  const el = document.getElementById('selfcheck');
  if (!(el instanceof HTMLElement)) return;
  el.classList.remove('ok', 'error', 'warning', 'thinking');
  if (state === 'thinking') el.classList.add('thinking');
  if (state === 'ok') el.classList.add('ok');
  if (state === 'error') el.classList.add('error');
  if (typeof text === 'string' && text) el.textContent = text;
}