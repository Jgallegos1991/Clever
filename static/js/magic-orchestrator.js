/**
 * magic-orchestrator.js
 *
 * Why: Implements the UI Brief "magical space" behavior by orchestrating the
 * particle system (HolographicChamber) and the manifestation of UI elements
 * (cards, microcopy, thinking pulses). Provides a resilient state machine so
 * degraded environments still show a usable interface.
 * Where: Loaded after holographic-chamber.js inside index.html. Connects to
 * DOM elements (#particles, #magical-status, #microcopy-line, #manifestation-root,
 * #conversation-stream, #input-panel) and coordinates visual states.
 * How: Initializes particle system if performant, rotates microcopy phrases,
 * exposes a lightweight API for future chat integration, and handles fallback
 * if WebGL/context creation fails. Maintains strictly offline + CSP compliant
 * behavior (no external calls, no inline code).
 *
 * Connects to:
 *  - holographic-chamber.js: Advanced particle engine
 *  - index.html template structure
 *  - Potential future chat logic in main.js (not yet wired here)
 */
(function(){
  'use strict';

  // ---------------------------- Configuration ---------------------------------
  const MICROCOPY = [
    'Ideas crystallizing…',
    'Energy takes shape.',
    'Your thought enters the flow.',
    'Concept lattice forming…',
    'Meaning is manifesting…',
    'Synapses preparing pathways…',
    'Subtle patterns assembling…'
  ];

  const STATE = {
    IDLE: 'idle',
    SUMMON: 'summon',
    DIALOGUE: 'dialogue',
    DISSOLVE: 'dissolve'
  };

  const PERF = {
    MIN_WIDTH: 640,   // skip heavy effects on very small viewports
    MAX_FRAME_INIT_MS: 22, // soft target for initial frame work
    PARTICLE_CAP_LOW: 600,
  };

  // ---------------------------- DOM refs --------------------------------------
  const canvas = document.getElementById('particles');
  const magicalStatus = document.getElementById('magical-status');
  const microcopyLine = document.getElementById('microcopy-line');
  const convoStream = document.getElementById('conversation-stream');
  const inputPanel = document.getElementById('input-panel');
  const fallbackPanel = document.getElementById('fallback-panel');

  // Legacy debug spans (if still present)
  const systemStatus = document.getElementById('system-status');
  const jsInitStatus = document.getElementById('js-init-status');

  function markStatus(text){ if(systemStatus) systemStatus.textContent = text; }
  function markPhase(text){ if(jsInitStatus) jsInitStatus.textContent = text; }

  // ---------------------------- State machine ---------------------------------
  let currentState = STATE.IDLE;
  function setState(next){
    if(currentState === next) return;
    document.body.classList.remove('idle','summon','dialogue','dissolve','thinking');
    currentState = next;
    document.body.classList.add(next);
  }

  // Public lightweight API (for future integration)
  const api = {
    summon(){ setState(STATE.SUMMON); triggerPulse(1.25); rotateMicrocopy('Energy condenses…'); },
    dialogue(){ setState(STATE.DIALOGUE); document.body.classList.add('thinking'); rotateMicrocopy('Forging response…'); },
    idle(){ setState(STATE.IDLE); document.body.classList.remove('thinking'); },
    dissolve(){ setState(STATE.DISSOLVE); rotateMicrocopy('Releasing form…'); },
    manifestMessage(role, text){
      const card = document.createElement('div');
      card.className = 'manifest-card';
      card.setAttribute('data-role', role);
      card.textContent = text;
      convoStream.appendChild(card);
      // Auto-scroll gently
      setTimeout(()=> { card.scrollIntoView({behavior:'smooth', block:'end'}); }, 30);
      // Return a handle for future dissolve
      return card;
    },
    dissolveMessage(card){ if(card){ card.classList.add('dissolving'); setTimeout(()=> card.remove(), 650); }},
    rotateMicrocopy,
  };
  // Expose API globally (cast to any to satisfy type-aware tooling)
  (window /** @type {any} */)['CleverMagicalUI'] = api; // dev/testing access

  // ---------------------------- Microcopy rotation ----------------------------
  let microIdx = 0;
  let microTimer = null;

  function rotateMicrocopy(forceText){
    if(!microcopyLine) return;
    const text = forceText || MICROCOPY[microIdx++ % MICROCOPY.length];
    microcopyLine.textContent = text;
  }

  function startMicroLoop(){
    if(microTimer) clearInterval(microTimer);
    rotateMicrocopy();
    microTimer = setInterval(()=> rotateMicrocopy(), 6000);
  }

  // ---------------------------- Particle init ---------------------------------
  let chamber = null;
  let initFailed = false;

  function initParticles(){
    markPhase('initializing');
    const t0 = performance.now();
    try {
      if(!canvas){ throw new Error('Canvas #particles missing'); }
      // Basic performance / environment guard
      if(window.innerWidth < PERF.MIN_WIDTH){ console.warn('[magic-orchestrator] Small viewport – light mode'); }
      if(!window.HolographicChamber){ throw new Error('HolographicChamber unavailable'); }

      chamber = new window.HolographicChamber(canvas);
      markStatus('Online ✓');
      markPhase('running');
      document.body.classList.add('particles-active');
    } catch(e){
      console.error('[magic-orchestrator] Particle init failed:', e);
      initFailed = true;
      markStatus('Fallback mode');
      markPhase('failed');
      enableFallback();
    } finally {
      const dt = performance.now() - t0;
      if(dt > 150){ console.warn('[magic-orchestrator] Slow init', dt.toFixed(1),'ms'); }
    }
  }

  function enableFallback(){
    if(fallbackPanel) fallbackPanel.style.display = 'block';
    // Attempt dynamic light fallback using minimal script if available later:
    // (Deferred: we keep code here commented to preserve CSP safety and avoid extra HTTP.)
  }

  // Simple pulse bridging to advanced system if present
  function triggerPulse(intensity){
    try { if(chamber && typeof window.triggerPulse === 'function'){ window.triggerPulse(intensity); } } catch(_){ /* ignore */ }
  }

  // ---------------------------- Input wiring (basic) --------------------------
  function wireInput(){
    const form = document.getElementById('chat-form');
  const userInput = /** @type {HTMLInputElement|null} */ (document.getElementById('user-input'));
    if(!form || !userInput) return;

    form.addEventListener('submit', (e)=>{
      e.preventDefault();
  const val = ((userInput && userInput.value) || '').trim();
      if(!val) return;
      api.summon();
      const userCard = api.manifestMessage('user', val);
      userCard.classList.add('user-card');
  if(userInput) userInput.value = '';
      setTimeout(()=> api.dialogue(), 300);
      // Simulated AI response placeholder until backend chat wiring reattached
      setTimeout(()=>{
        const aiCard = api.manifestMessage('ai', '✨ (Demo) Clever is aligning with your intent: "'+val+'"');
        document.body.classList.remove('thinking');
        api.idle();
        rotateMicrocopy('Form released.');
      }, 1600);
    });
  }

  // ---------------------------- Boot sequence ---------------------------------
  function boot(){
    markPhase('booting');
    startMicroLoop();
    initParticles();
    wireInput();
    setState(STATE.IDLE);
    // Safety timeout: if nothing happened within 5s and no particles detected, fallback.
    setTimeout(()=>{
      if(!chamber && !initFailed){ console.warn('[magic-orchestrator] Watchdog activating fallback'); enableFallback(); }
    }, 5000);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
