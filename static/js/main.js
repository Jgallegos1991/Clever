// Track last AI bubble globally for positioning the analysis card (scoped)
let lastAiElMain = null;
// Ephemeral preview bubble + hide timer
let typingGhostEl = null;
let hideBarTimer = null;
// In-memory telemetry (frontend perspective)
const FRONTEND_TELEMETRY = { chatCount:0, avgLatencyMs:0, lastLatencyMs:0, lastError:null };
// Fade & lifecycle configuration - slowed down for more comfortable reading
const MESSAGE_LIFECYCLE = { AUTO_HIDE_MS: 20000, FADE_DURATION_MS: 3000 };
function showToast(msg, type='info', ttl=7000){ // Slowed down default toast duration from 4000ms to 7000ms
  const id='toast-stack';
  let stack=document.getElementById(id);
  if(!stack){
    stack=document.createElement('div');
    stack.id=id;
    stack.style.cssText='position:fixed;bottom:1rem;right:1rem;display:flex;flex-direction:column;gap:.5rem;z-index:9999;pointer-events:none;';
    document.body.appendChild(stack);
  }
  const el=document.createElement('div');
  el.className=`toast toast-${type}`;
  el.textContent=msg;
  el.style.cssText='background:rgba(20,30,38,0.85);color:#cde;padding:6px 10px;font:12px system-ui,monospace;border:1px solid #2d5; border-radius:6px;opacity:0;transition:opacity .8s'; // Slowed down opacity transition from .35s to .8s
  stack.appendChild(el);
  requestAnimationFrame(()=> el.style.opacity='1');
  setTimeout(()=>{ el.style.opacity='0'; setTimeout(()=> el.remove(),1200); }, ttl); // Slowed down removal delay from 600ms to 1200ms
}

document.addEventListener('DOMContentLoaded', () => {
  // --- Defensive microcopy scrub -------------------------------------------------
  (function scrubAmbientMicrocopy(){
    /**
     * Why: Despite removing microcopy from the canonical template, the served HTML
     *       (likely from a stale cached template variant) still contains hidden
     *       spans ("Ambient creativity", "Your thought enters the flow"). These
     *       leak unintended text onto the stage. We proactively remove them at
     *       runtime to guarantee a clean, minimal surface.
     * Where: Runs immediately on DOMContentLoaded inside main.js—the active
     *       frontend controller—so it neutralizes any legacy template artifacts
     *       before user interaction.
     * How: Query for any elements whose textContent matches the disallowed phrases
     *       (case‑insensitive), remove them, then set up a MutationObserver to
     *       continue stripping if dynamically reinserted by legacy scripts.
     *
     * Connects to:
     *  - templates/index.html (canonical) which no longer defines these spans.
     *  - static/js/core/app.js (legacy) which is suppressed but could still load.
     *  - tests/test_ui_brief_acceptance.py (updated to drop microcopy assertion).
     */
    const BLOCKED = [/ambient creativity/i, /your thought enters the flow/i];
    function purge(root=document){
      const walker = document.createTreeWalker(root.body || root, NodeFilter.SHOW_ELEMENT, null);
      const toRemove = [];
      while(walker.nextNode()){
        const el = walker.currentNode;
        if(!(el instanceof HTMLElement)) continue;
        const txt = el.textContent?.trim() || '';
        if(!txt) continue;
        if(BLOCKED.some(r=> r.test(txt))) toRemove.push(el);
      }
      toRemove.forEach(el=> el.remove());
    }
    purge();
    // Observe future insertions
    const mo = new MutationObserver(muts => {
      muts.forEach(m => m.addedNodes.forEach(n => {
        if(!(n instanceof HTMLElement)) return;
        if(BLOCKED.some(r=> r.test(n.textContent||''))) n.remove();
        // Also scan small subtrees quickly
        n.querySelectorAll && n.querySelectorAll('*').forEach(child => {
          if(BLOCKED.some(r=> r.test(child.textContent||''))) child.remove();
        });
      }));
    });
    try { mo.observe(document.documentElement, { childList:true, subtree:true }); } catch(_){}
  })();
  // --- Runtime module registration (introspection) -------------------------
  try {
    window['CLEVER_RUNTIME'] = window['CLEVER_RUNTIME'] || { modules: [] };
    window['CLEVER_RUNTIME'].modules.push({
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
  const floatingInput = document.getElementById('floating-input');
  const chatLog = document.getElementById('chat-log');
  const sendButton = document.getElementById('send-btn');
  const analysisPanel = document.querySelector('.analysis-panel');
  const modeBtn = document.getElementById('mode-btn');

  // Initialize unified holographic chamber system (no fallbacks)
  const canvasElem = document.getElementById('particles');
  if (canvasElem instanceof HTMLCanvasElement && typeof window['startHolographicChamber'] === 'function') {
    const chamber = window['startHolographicChamber'](canvasElem);
    if (chamber) {
      window['holographicChamber'] = chamber;
      console.log('🌌 Clever\'s holographic chamber is active');
    } else {
      console.error('❌ Failed to initialize holographic chamber');
    }
  } else {
    console.error('❌ Canvas element or HolographicChamber not available');
  }

  // Initialize UI Foundation System
  if (typeof window.CleverUIFoundation === 'function') {
    try { 
      window.uiFoundation = new window.CleverUIFoundation(); 
      console.log('🧠 UI Foundation System initialized');
    } catch (e) { 
      console.warn('UI Foundation initialization failed:', e.message); 
    }
  }

  // Send on click or Enter
  sendButton?.addEventListener('click', () => sendMessage());
  userInput?.addEventListener('keypress', e => {
    if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
  });
  // Visual glow on focus/blur
  if (userInput instanceof HTMLInputElement && floatingInput) {
    userInput.addEventListener('focus', () => floatingInput.classList.add('active'));
    userInput.addEventListener('blur', () => floatingInput.classList.remove('active'));
    // Show what you're typing as a subtle ghost bubble
    userInput.addEventListener('input', () => {
      const val = userInput.value;
      if (!val) {
        if (typingGhostEl) { typingGhostEl.remove(); typingGhostEl = null; }
        return;
      }
      if (!typingGhostEl) {
        typingGhostEl = document.createElement('div');
        typingGhostEl.className = 'message user manifested';
        // Why: Remove label chips to keep stage minimal (no boxes), show only raw text while typing
        // Where: This connects to the chat stream (#chat-log) as a transient preview node
        // How: Create a minimal bubble element with the current input value; no role chips are appended
        const bubble = document.createElement('div'); bubble.className = 'bubble';
        typingGhostEl.append(bubble);
        chatLog?.append(typingGhostEl);
        chatLog && (chatLog.scrollTop = chatLog.scrollHeight);
      }
      const bubbleEl = typingGhostEl.querySelector('.bubble');
      if (bubbleEl) bubbleEl.textContent = val;
    });
  }

  // Removed idle microcopy display (stage must remain visually clean)
  // showStatus('Ambient creativity waiting…');

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
      setTimeout(() => grid.classList.remove('ripple'), 1200); // Slowed down ripple effect from 600ms to 1200ms
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
      floatingInput?.classList.add('active');
  scheduleAutoHideBar();
      // Trigger the same grid ripple effect as manual focus
      const grid = document.querySelector('.grid-overlay');
      if (grid) {
        grid.classList.add('ripple');
        setTimeout(() => grid.classList.remove('ripple'), 1200); // Slowed down ripple effect from 600ms to 1200ms
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
      floatingInput?.classList.add('active');
      scheduleAutoHideBar();
    }
  });

  // Mode button is a status chip, not a toggle (auto-inferred mode)
  if (modeBtn) {
    modeBtn.addEventListener('click', () => {
      modeBtn.title = 'Mode adapts automatically based on your intent';
    });
  }

  // 🎆 PARTICLE SYSTEM KEYBOARD CONTROLS 🎆
  // Advanced holographic particle control system for Jay's digital brain extension
  document.addEventListener('keydown', (e) => {
    // Only trigger if not typing in input fields and using special key combos
    const target = e.target;
    if (target instanceof Element && 
        target.matches('input, textarea, [contenteditable]')) {
      return;
    }

    // Particle effects with Ctrl + key combinations
    if (e.ctrlKey && !e.altKey && !e.metaKey) {
      switch (e.key.toLowerCase()) {
        case 'e': // Explode particles (gentler)
          e.preventDefault();
          window.explodeParticles?.(0.8);
          showToast('💥 Gentle Explosion!', 'info', 2000);
          break;
        case 'i': // Implode particles (smoother)
          e.preventDefault();
          window.implodeParticles?.(0.6);
          showToast('🌀 Smooth Implosion!', 'info', 2000);
          break;
        case 'v': // Create vortex
          e.preventDefault();
          window.createVortex?.();
          showToast('🌪️ Vortex Created!', 'info', 2000);
          break;
        case 'w': // Energy wave
          e.preventDefault();
          window.createEnergyWave?.();
          showToast('〰️ Energy Wave!', 'info', 2000);
          break;
        case 'l': // Lightning between particles
          e.preventDefault();
          window.createLightning?.();
          showToast('⚡ Lightning Strike!', 'info', 2000);
          break;
        case 'd': // Dance party mode (chill vibes)
          e.preventDefault();
          window.startDanceParty?.(8000);
          showToast('🕺 Chill Dance Mode!', 'info', 3000);
          break;
        case 't': // Toggle trail mode
          e.preventDefault();
          window.toggleTrails?.();
          showToast('✨ Trail Mode Toggled!', 'info', 2000);
          break;
        case 'm': // Add magnetic field at center
          e.preventDefault();
          window.addMagneticField?.();
          showToast('🧲 Magnetic Field Added!', 'info', 2000);
          break;
        case 'p': // Pulse effect (much gentler)
          e.preventDefault();
          window.triggerPulse?.(0.5);
          showToast('💫 Gentle Pulse!', 'info', 2000);
          break;
      }
    }

    // Formation changes with Shift + key combinations
    if (e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey && window.holographicChamber) {
      switch (e.key.toLowerCase()) {
        case 'c': // Cube formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('cube');
          showToast('📦 Cube Formation!', 'info', 2000);
          break;
        case 's': // Sphere formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('sphere');
          showToast('🌐 Sphere Formation!', 'info', 2000);
          break;
        case 'h': // Helix formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('helix');
          showToast('🧬 Helix Formation!', 'info', 2000);
          break;
        case 't': // Torus formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('torus');
          showToast('🍩 Torus Formation!', 'info', 2000);
          break;
        case 'w': // Wave formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('wave');
          showToast('🌊 Wave Formation!', 'info', 2000);
          break;
        case 'p': // Spiral formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('spiral');
          showToast('🌀 Spiral Formation!', 'info', 2000);
          break;
        case 'x': // Scatter formation
          e.preventDefault();
          window.holographicChamber.morphToFormation('scatter');
          showToast('💫 Scatter Formation!', 'info', 2000);
          break;
        case 'z': // Back to whirlpool (idle)
          e.preventDefault();
          window.holographicChamber.morphToFormation('whirlpool');
          showToast('🌪️ Whirlpool Formation!', 'info', 2000);
          break;
      }
    }

    // Text morphing with Alt + typing
    if (e.altKey && !e.ctrlKey && !e.shiftKey && !e.metaKey) {
      if (e.key.length === 1 && /[a-zA-Z0-9]/.test(e.key)) {
        // Start text input mode - could be enhanced to show input dialog
        showToast('💬 Use morphToText("your text") in console!', 'info', 3000);
      }
    }
  });

  // Show keyboard shortcuts on startup
  setTimeout(() => {
    showToast('🎮 Particle Controls Loaded! Try Ctrl+E for explosion, Shift+C for cube!', 'info', 8000);
  }, 3000); // Slowed down from 2000ms to 3000ms, and toast duration from 5000 to 8000

  // Maintain snap on resize and when user scrolls chat
  window.addEventListener('resize', () => {
    if (lastAiElMain) snapAnalysisTo(lastAiElMain);
  });
  chatLog?.addEventListener('scroll', () => {
    if (lastAiElMain) snapAnalysisTo(lastAiElMain);
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
      modules: (window['CLEVER_RUNTIME'] && window['CLEVER_RUNTIME'].modules) || []
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
  // Clear typing ghost immediately on send
  if (typingGhostEl) { typingGhostEl.remove(); typingGhostEl = null; }
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
  if (preShape && window.holographicChamber && typeof window.holographicChamber.morphToFormation === 'function') {
    window.holographicChamber.morphToFormation(preShape);
    console.log(`🌌 User requested shape: ${preShape}`);
  }
  // Visual ripple: show grid thinking effect
  const grid = document.querySelector('.grid-overlay');
  if (grid) {
    grid.classList.add('ripple');
    setTimeout(() => grid.classList.remove('ripple'), 600);
  }
  inputElem.value = '';
  scheduleAutoHideBar();
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
    // Debug schema validation (temporary instrumentation)
    const requiredKeys = ['response','analysis'];
    const missing = requiredKeys.filter(k => !(k in data));
    if (missing.length) {
      console.warn('[chat] Missing expected keys', { missing, got:Object.keys(data) });
      showToast('Schema mismatch ('+missing.join(',')+')', 'warning', 4500);
    }
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
      // Morph particles based on detected shape intent
      const shape = inferShapeFromTextAndAnalysis(null, data.analysis || {});
      if (shape && window.holographicChamber && typeof window.holographicChamber.morphToFormation === 'function') {
        window.holographicChamber.morphToFormation(shape);
        console.log(`🌌 Morphing particles to: ${shape}`);
      }
      // Snap analysis panel under the latest AI message and animate highlight
      if (aiEl) {
        lastAiElMain = aiEl;
        snapAnalysisTo(aiEl);
        const panel = document.querySelector('.analysis-panel');
        if (panel) {
          panel.classList.add('updated');
          setTimeout(() => panel.classList.remove('updated'), 1600); // Slowed down from 800ms to 1600ms
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
    if (window.holographicChamber && typeof window.holographicChamber.morphToFormation === 'function') {
      // Map approach/intent to explicit morph shape for clearer storytelling
      const intent = mapApproachToIntent(data.approach, data?.analysis?.intent);
      window.holographicChamber.morphToFormation(intent);
      console.log(`🌌 AI response triggered shape: ${intent}`);
    }
    // AI response complete: visual and status update
    if (/money|dollar|finance/i.test(reply)) {
      if (window.holographicChamber && typeof window.holographicChamber.morphToFormation === 'function') {
        window.holographicChamber.morphToFormation('spiral'); // Money/finance gets spiral formation
      }
      if (window.triggerPulse) window.triggerPulse(1.0);
    }
  // Mark done and show copy
  setSelfcheckState('ok', 'Done');
  
    // Return to idle state after a delay
    setTimeout(() => {
      if (window.holographicChamber) {
        window.holographicChamber.idle();
      }
    }, 6000); // Slowed down from 3000ms to 6000ms
  showStatus('Energy takes shape.');
    // After a delay, return to idle microcopy
    setTimeout(() => {
      // Removed ambient microcopy reinsertion
      const dissolve = window['dissolveToSwarm'];
      if (typeof dissolve === 'function') dissolve();
    }, 4000); // Slowed down from 2000ms to 4000ms
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

function scheduleAutoHideBar() {
  const bar = document.getElementById('floating-input');
  if (!bar) return;
  if (hideBarTimer) clearTimeout(hideBarTimer);
  hideBarTimer = setTimeout(() => { bar.classList.remove('active'); }, 8000); // Slowed down from 3500ms to 8000ms
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
  setTimeout(()=>{ const ts = Number(panel.dataset.ts||0); if(Date.now()-ts>9500){ panel.style.transition='opacity 600ms'; panel.style.opacity='0'; } }, 10000);
}

function appendMessage(who, text) {
  if (who === 'ai') {
    // Final client-side scrub: remove any residual meta markers if server missed
    // Why: Belt-and-suspenders protection so UI never shows internal reasoning.
    // Where: Right before DOM insertion of AI bubble.
    // How: Regex removes fragments like 'Time-of-day: ...', 'focal lens: ...', 'Vector: ...', 'complexity index', 'essence:' plus stray double spaces.
    try {
      const patterns = [
        /Time-of-day:\s*[^;.,\n]+[;,.]?/gi,
        /focal lens:\s*[^;.,\n]+[;,.]?/gi,
        /Vector:\s*[^;.,\n]+[;,.]?/gi,
        /complexity index[^;.,\n]*[;,.]?/gi,
        /essence:\s*[^;.,\n]+[;,.]?/gi
      ];
      patterns.forEach(p => { text = text.replace(p, ''); });
      text = text.replace(/\s{2,}/g,' ').trim();
    } catch(_) { /* silent */ }
  }
  const log = document.getElementById('chat-log');
  const wrap = document.createElement('div');
  wrap.classList.add('message', who, 'manifesting');
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  wrap.append(bubble);
  // Minimal bubble only (chips removed for clean stage)
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
  // Intentionally no-op: prevent any analysis/meta text from rendering on stage
  return;
}

function showStatus(msg) {
  // Status chip intentionally removed to keep stage minimal; enforce no-op.
  return; // Guard against any legacy calls trying to surface microcopy
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
  // Check for explicit shape request from Clever first
  if (analysis && analysis.requested_shape) {
    console.log(`🔍 Found requested shape in analysis: ${analysis.requested_shape}`);
    return analysis.requested_shape;
  }
  
  const t = String(userText || (analysis && analysis.user_input) || '').toLowerCase();
  console.log(`🔍 Analyzing text for shapes: "${t}"`);
  
  // Direct shape mentions take precedence
  if (/cube|box|square/.test(t)) {
    console.log('🎯 Detected shape: cube');
    return 'cube';
  }
  if (/torus|donut|ring/.test(t)) {
    console.log('🎯 Detected shape: torus');
    return 'torus';
  }
  if (/sphere|ball|circle/.test(t)) {
    console.log('🎯 Detected shape: sphere');
    return 'sphere';
  }
  if (/galaxy|spiral|swirl/.test(t)) {
    console.log('🎯 Detected shape: galaxy');
    return 'galaxy';
  }
  if (/grid|plane/.test(t)) {
    console.log('🎯 Detected shape: grid');
    return 'grid';
  }
  if (/wave|ripple/.test(t)) {
    console.log('🎯 Detected shape: wave');
    return 'wave';
  }
  if (/helix|dna/.test(t)) {
    console.log('🎯 Detected shape: helix');
    return 'helix';
  }
  if (/scatter|spread/.test(t)) {
    console.log('🎯 Detected shape: scatter');
    return 'scatter';
  }
  
  // Infer from analysis intent if available
  const intent = String(analysis && analysis.intent || '').toLowerCase();
  if (intent.includes('shape')) return 'cube';
  if (intent.includes('creative')) return 'torus';
  if (intent.includes('deep')) return 'cube';
  if (intent.includes('casual') || intent.includes('chat')) return 'sphere';
  if (intent.includes('explore')) return 'galaxy';
  
  console.log('🔍 No shape detected');
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

// --- UI Component Helper Functions ---
// These demonstrate the holographic UI components from the screenshots

function toggleAnalysisDisplay() {
  if (!window.uiFoundation) return;
  
  const existing = window.uiFoundation.getComponent('main-analysis');
  if (existing) {
    window.uiFoundation.removeComponent('main-analysis');
    showToast('📊 Analysis Display Hidden', 'info', 2000);
  } else {
    const analysis = window.uiFoundation.createComponent('AnalysisDisplay', 'main-analysis', {
      title: 'Cognitive Analysis',
      position: { x: 'auto', y: 'auto' }
    });
    
    // Demo data similar to screenshots
    analysis.updateAnalysis({
      intent: 'Holographic Interface Design',
      mood: 'creative_focused',
      keywords: ['UI', 'holographic', 'particles', 'brain'],
      formation: 'cube'
    });
    
    showToast('📊 Analysis Display Shown', 'info', 2000);
  }
}

function showStatus(text, type = 'info') {
  if (!window.uiFoundation) return;
  
  const status = window.uiFoundation.createComponent('StatusIndicator', `status-${Date.now()}`, {
    text: text,
    type: type,
    position: 'top-center'
  });
  
  // Auto-remove after delay
  setTimeout(() => {
    if (status) {
      window.uiFoundation.removeComponent(status.id);
    }
  }, 3000);
}

function showFloatingPanel(title, content) {
  if (!window.uiFoundation) return;
  
  const panel = window.uiFoundation.createComponent('FloatingPanel', `panel-${Date.now()}`, {
    title: title,
    content: content,
    width: 320,
    style: 'holographic',
    position: { x: 'auto', y: 'auto' }
  });
  
  // Auto-remove after 8 seconds
  setTimeout(() => {
    if (panel) {
      window.uiFoundation.removeComponent(panel.id);
    }
  }, 8000);
  
  return panel;
}

function createChatBubble(message, role = 'ai') {
  if (!window.uiFoundation) return;
  
  const bubble = window.uiFoundation.createComponent('ChatBubble', `bubble-${Date.now()}`, {
    message: message,
    role: role,
    autoHide: true,
    hideDelay: 6000
  });
  
  return bubble;
}

function getSystemInfo() {
  const particleCount = window.holographicChamber ? 
    (window.holographicChamber.particles ? window.holographicChamber.particles.length : '?') : '?';
  
  return `
    <div style="font-family: 'Courier New', monospace; font-size: 11px; line-height: 1.6;">
      <div style="color: #69EACB; margin-bottom: 8px;">CLEVER DIGITAL BRAIN v2.0</div>
      <div>Particles: ${particleCount}</div>
      <div>Formation: ${window.holographicChamber?.currentFormation || 'whirlpool'}</div>
      <div>Performance: ${Math.round(performance.now() / 1000)}s uptime</div>
      <div>UI Components: ${window.uiFoundation ? window.uiFoundation.componentCount : 0}</div>
      <div style="margin-top: 8px; color: #69EACB;">Neural Link: ●○○ ACTIVE</div>
    </div>
  `;
}