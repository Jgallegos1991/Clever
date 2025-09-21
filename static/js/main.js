// Track last AI bubble globally for positioning the analysis card
let lastAiEl = null;
// In-memory telemetry (frontend perspective)
const FRONTEND_TELEMETRY = {
  chatCount: 0,
  avgLatencyMs: 0,
  lastLatencyMs: 0,
  lastError: null,
};

// Fade & lifecycle configuration (single source of truth)
const MESSAGE_LIFECYCLE = {
  AUTO_HIDE_MS: 14000,   // Time before fade starts
  FADE_DURATION_MS: 1200 // Must match CSS .message.fading transition
};

// Utility: show ephemeral toast notifications (errors, status)
function showToast(msg, type = 'info', ttl = 4000) {
  /**
   * Why: Provide lightweight, non-blocking user feedback (errors, connectivity, mode hints)
   * Where: Invoked by sendMessage error handling, ping health check, and future proactive system notices
   * How: Creates a div in #toast-stack with fade-in/out CSS classes; removed after TTL
   */
  const stack = document.getElementById('toast-stack');
  if (!stack) return; // graceful no-op
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.textContent = msg;
  stack.appendChild(el);
  requestAnimationFrame(()=> el.classList.add('visible'));
  setTimeout(()=> {
    el.classList.remove('visible');
    setTimeout(()=> el.remove(), 600);
  }, ttl);
}

document.addEventListener('DOMContentLoaded', () => {
  // --- Runtime module registration (introspection) -------------------------
  try {
    window.CLEVER_RUNTIME = window.CLEVER_RUNTIME || { modules: [] };
    window.CLEVER_RUNTIME.modules.push({
      name: 'main.js',
      initTs: Date.now(),
    });
  } catch (e) { /* non-fatal */ }

  const debugFlag = /[?&]debug=1/.test(location.search);
  if (debugFlag) {
    injectDebugOverlay();
    // Poll runtime introspection every 4s
    setInterval(fetchIntrospectionAndRender, 4000);
    fetchIntrospectionAndRender();
  }
  const userInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-btn');
  const chatLog = document.getElementById('chat-log');
  const analysisPanel = document.querySelector('.analysis-panel');
  const modeBtn = document.getElementById('mode-btn');

  // Initialize holographic chamber with debugging
  const debugDiv = document.getElementById('debug-info');
  const canvasElem = document.getElementById('particles');
  
  if (debugDiv) debugDiv.innerHTML = 'Canvas found: ' + (canvasElem ? 'YES' : 'NO');
  console.log('🔧 Main.js initializing holographic chamber...');
  console.log('🎯 Canvas element found:', canvasElem);
  console.log('🎨 Canvas dimensions:', canvasElem?.offsetWidth, 'x', canvasElem?.offsetHeight);
  
  if (debugDiv) debugDiv.innerHTML += '<br/>startFunction: ' + typeof window['startHolographicChamber'];
  
  if (canvasElem instanceof HTMLCanvasElement && typeof window['startHolographicChamber'] === 'function') {
    console.log('🚀 Starting holographic chamber from main.js...');
  if (debugDiv) debugDiv.innerHTML += '<br/>Initializing particles...';
    try {
      window['holographicChamber'] = window['startHolographicChamber'](canvasElem);
      console.log('✅ Holographic chamber initialized:', window['holographicChamber']);
  if (debugDiv) debugDiv.innerHTML += '<br/>✅ Particles initialized!';
    } catch (error) {
      console.error('❌ Particle initialization failed:', error);
  if (debugDiv) debugDiv.innerHTML += '<br/>❌ Init failed: ' + error.message;
    }
  } else {
    console.error('❌ Cannot initialize holographic chamber:', {
      canvas: canvasElem,
      startFunction: typeof window['startHolographicChamber']
    });
  if (debugDiv) debugDiv.innerHTML += '<br/>❌ Missing function or canvas';
    // Why: Provide a graceful degradation path so the rest of the chat UI still works
    // Where: Fallback lives inside main.js init; connects to legacy particle starter if present
    // How: Attempt to start legacy particles() engine instead of holographic chamber
    try {
      if (canvasElem instanceof HTMLCanvasElement && typeof window.startParticles === 'function') {
        window.startParticles(canvasElem, { count: 4000 });
        console.log('✨ Fallback particle engine started');
      }
    } catch (e) {
      console.warn('Fallback particle init failed (non-fatal)', e);
    }
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

// --- Debug overlay (optional) ------------------------------------------------
function injectDebugOverlay() {
  if (document.getElementById('clever-debug-overlay')) return;
  const panel = document.createElement('div');
  panel.id = 'clever-debug-overlay';
  panel.style.cssText = [
    'position:fixed','top:8px','right:8px','z-index:9999','max-width:360px',
    'font:12px/1.4 monospace','background:rgba(10,12,20,0.82)',
    'color:#9fe7ff','padding:8px 10px','border:1px solid #1d3a50',
    'backdrop-filter:blur(6px)','border-radius:8px','box-shadow:0 0 0 1px #133, 0 4px 14px -4px #000',
    'overflow:hidden','display:flex','flex-direction:column','gap:4px'
  ].join(';');
  panel.innerHTML = '<div style="font-weight:600">Clever Runtime</div><pre id="clever-debug-pre" style="margin:0;white-space:pre-wrap;max-height:260px;overflow:auto"></pre>';
  document.body.appendChild(panel);
}

async function fetchIntrospectionAndRender() {
  try {
    const res = await fetch('/api/runtime_introspect');
    if (!res.ok) return;
    const data = await res.json();
    const pre = document.getElementById('clever-debug-pre');
    if (!pre) return;
    // Light transform to shrink noise
    const slim = {
      last_render: data.last_render,
      persona_mode: data.persona_mode,
      endpoints: (data.endpoints||[]).slice(0,6).map(e => ({r:e.rule, why:e.why.slice(0,60)})),
      last_error: data.last_error,
      version: data.version,
      warnings: data.warnings || [],
      evolution: data.evolution || null,
      modules: (window.CLEVER_RUNTIME && window.CLEVER_RUNTIME.modules) || []
    };
    pre.textContent = JSON.stringify(slim, null, 2);
  } catch (e) {
    // swallow errors to avoid UI disruption
  }
}

async function sendMessage() {
  const inputElem = document.getElementById('chat-input');
  if (!(inputElem instanceof HTMLInputElement)) return;
  const text = inputElem.value.trim();
  if (!text) return;
  appendMessage('user', text);
  // Update status indicator (thinking) and mode chip based on initial guess
  setSelfcheckState('thinking', 'Thinking…');
  updateModeChip(inferModeFromAnalysis({ intent: guessIntentFromText(text) }, text));
  
  // Trigger particle summon state
  if (window.holographicChamber) {
    window.holographicChamber.summon();
  }
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
    // Why: Provide resilience if one route alias fails (proxy/cache issue) and surface diagnostics
    // Where: sendMessage flow inside main.js; connects to Flask /chat and /api/chat endpoints
    // How: Attempt /chat first; on network or JSON failure, retry /api/chat, log details
    const attemptFetch = async (url) => {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      let data; let parseOk = true;
      try { data = await res.json(); } catch (e) { parseOk = false; }
      return { res, data, parseOk };
    };
    let { res, data, parseOk } = await attemptFetch('/chat');
    if (!res.ok || !parseOk || !data || typeof data !== 'object') {
      console.warn('Primary /chat failed or invalid JSON. Fallback to /api/chat', { status: res && res.status, parseOk, data });
      ({ res, data, parseOk } = await attemptFetch('/api/chat'));
    }
    if (!res.ok || !parseOk || !data) throw new Error('Chat endpoint failure');
    const reply = data.response || '(no response text)';
  const aiEl = appendMessage('ai', reply);
  
    // Switch to dialogue state when receiving response
    if (window.holographicChamber) {
      window.holographicChamber.dialogue();
    }
    if (data && typeof data === 'object') {
      updateAnalysis(data.analysis || {});
      // Update adaptive mode chip from analysis + reply semantics
      const mode = inferModeFromAnalysis(data.analysis || {}, reply);
      updateModeChip(mode);
      // Morph holographic chamber based on shape intent
      
      // Show/hide glass panels based on conversation state
      // Morph field based on detected shape intent
      const shape = inferShapeFromTextAndAnalysis(null, data.analysis || {});
      if (shape && typeof window.morphForIntent === 'function') {
        window.morphForIntent(shape);
      }
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
  
    // Return to idle state after a delay
    setTimeout(() => {
      if (window.holographicChamber) {
        window.holographicChamber.idle();
      }
    }, 3000);
  showStatus('Energy takes shape.');
    // After a delay, return to idle microcopy
    setTimeout(() => {
      showStatus('Ambient creativity waiting...');
  const dissolve = window['dissolveToSwarm'];
  if (typeof dissolve === 'function') dissolve();
    }, 2000);
  } catch (err) {
    // Why: Provide structured, user-visible diagnostics for transient chat failures without forcing console inspection
    // Where: Error path of sendMessage, connected to toast + optional inline last-error overlay
    // How: Capture message, stack (if any), timestamp; update FRONTEND_TELEMETRY and surface toast + inline panel
    const info = {
      message: err && err.message || String(err),
      stack: err && err.stack || null,
      ts: Date.now(),
      phase: 'fetch/chat'
    };
    FRONTEND_TELEMETRY.lastError = info;
    console.error('[chat] fetch error', info);
    appendMessage('ai', 'Error contacting Clever.');
    setSelfcheckState('error', 'Error');
    showStatus('Error occurred');
    showToast('Chat error: ' + info.message, 'error', 6000);
    injectLastErrorOverlay(info);
  }
}

function injectLastErrorOverlay(errInfo){
  /**
   * Why: Surface the most recent operational error inline for rapid debugging (no console required)
   * Where: Called from sendMessage error catch block; attaches small fixed panel lower-right
   * How: Creates or updates #last-error-overlay with sanitized message + relative age, auto-fades after inactivity
   */
  let panel = document.getElementById('last-error-overlay');
  if(!panel){
    panel = document.createElement('div');
    panel.id = 'last-error-overlay';
    Object.assign(panel.style, {
      position:'fixed', bottom:'10px', right:'10px', zIndex:9999,
      background:'rgba(40,0,0,0.85)', color:'#fdd', padding:'8px 10px', border:'1px solid #a33',
      font:'11px system-ui,monospace', borderRadius:'6px', maxWidth:'260px', lineHeight:'1.35'
    });
    document.body.appendChild(panel);
  }
  panel.dataset.ts = String(errInfo.ts);
  panel.textContent = `[chat error] ${errInfo.message}`;
  panel.style.opacity = '1';
  // Auto fade after 10s if no newer error
  setTimeout(()=>{
    const ts = Number(panel.dataset.ts||0);
    if(Date.now() - ts > 9500){ panel.style.transition='opacity 600ms'; panel.style.opacity='0'; }
  }, 10000);
}

function appendMessage(who, text) {
  const log = document.getElementById('chat-log');
  const wrap = document.createElement('div');
  wrap.classList.add('message', who, 'manifesting');
  // Why: Need ephemeral chat bubbles that fade away after a period to keep stage focused on holographic chamber (per UI vision)
  // Where: appendMessage is the single construction path for every chat bubble; adding logic here guarantees uniform lifecycle handling
  // How: Add timed fade + removal sequence using CSS classes (fade-out) and a timeout schedule; expose constants for adjustability
  // (Moved constants to MESSAGE_LIFECYCLE for centralized control)
  // Optional role chip like screenshot (User / Clever)
  const chip = document.createElement('div');
  chip.className = 'chip';
  chip.textContent = who === 'user' ? 'User' : 'Clever';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  // Add pin button (only for AI messages for now)
  const pinBtn = document.createElement('button');
  pinBtn.type = 'button';
  pinBtn.className = 'pin-btn';
  pinBtn.title = 'Pin message (prevent auto-hide)';
  pinBtn.textContent = '📌';
  pinBtn.setAttribute('aria-label', 'Pin message');
  if (who === 'ai') bubble.appendChild(pinBtn);
  wrap.append(chip, bubble);
  log.append(wrap);
  // animate in
  requestAnimationFrame(() => wrap.classList.add('manifested'));
  log.scrollTop = log.scrollHeight;
  if (who === 'ai') {
    // Accessibility announcement: update polite live region with trimmed text
    const live = document.getElementById('sr-live');
    if (live) {
      live.textContent = 'Clever: ' + String(text).slice(0, 160);
    }
  }

  // Ephemeral lifecycle: schedule fade + DOM removal
  // Skip auto-hide for extremely short control/system messages
  if (text && text.length > 0) {
    scheduleMessageAutoHide(wrap);
  }

  // Pause on hover & pin logic
  let pinned = false;
  const pause = () => wrap.classList.add('paused');
  const resume = () => { if (!pinned) wrap.classList.remove('paused'); };
  wrap.addEventListener('mouseenter', pause);
  wrap.addEventListener('mouseleave', resume);
  pinBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    pinned = !pinned;
    if (pinned) {
      wrap.classList.add('pinned');
      wrap.classList.remove('fading');
      wrap.dataset.pinned = '1';
      pinBtn.textContent = '❌';
      pinBtn.title = 'Unpin message';
      showToast('Message pinned', 'info', 1800);
    } else {
      wrap.classList.remove('pinned');
      delete wrap.dataset.pinned;
      pinBtn.textContent = '📌';
      pinBtn.title = 'Pin message';
      // Reschedule fade from now
      scheduleMessageAutoHide(wrap, 3000); // shorter delay after unpin
    }
  });
  return wrap;
}

function scheduleMessageAutoHide(wrap, overrideDelay) {
  /**
   * Why: Centralized function to manage message auto-hide respecting pause/pin state
   * Where: Called from appendMessage and when unpinning an existing bubble
   * How: Uses timeouts referencing shared MESSAGE_LIFECYCLE constants; checks data-pinned and .paused
   */
  const delay = typeof overrideDelay === 'number' ? overrideDelay : MESSAGE_LIFECYCLE.AUTO_HIDE_MS;
  setTimeout(() => {
    if (!wrap.isConnected) return;
    if (wrap.dataset.pinned === '1' || wrap.classList.contains('paused')) return; // skip
    wrap.classList.add('fading');
    setTimeout(() => { if (wrap.isConnected && wrap.dataset.pinned !== '1') wrap.remove(); }, MESSAGE_LIFECYCLE.FADE_DURATION_MS);
  }, delay);
}

// Ping server for latency & health once DOM is ready (defer minimal)
window.addEventListener('load', async () => {
  try {
    const t0 = performance.now();
    const res = await fetch('/api/ping');
    if (!res.ok) throw new Error('ping status ' + res.status);
    await res.json();
    const dt = performance.now() - t0;
    FRONTEND_TELEMETRY.lastLatencyMs = dt;
    FRONTEND_TELEMETRY.avgLatencyMs = FRONTEND_TELEMETRY.avgLatencyMs ? (FRONTEND_TELEMETRY.avgLatencyMs * 0.8 + dt * 0.2) : dt;
    showToast('Connected (' + Math.round(dt) + ' ms)', 'info', 2500);
  } catch (e) {
    FRONTEND_TELEMETRY.lastError = String(e.message||e);
    showToast('Connection issue (ping failed)', 'error', 5000);
  }
});

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