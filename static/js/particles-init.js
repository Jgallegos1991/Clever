/**
 * particles-init.js
 *
 * Why: Initializes a minimal particle visualization and status indicators without
 * violating CSP restrictions (no inline scripts). Replaces previous inline
 * script that was blocked by Content Security Policy (script-src 'self').
 * Where: Loaded by `templates/index.html` at the bottom of the body. Connects to
 * the simple landing UI showing status + particle count. No dependency on the
 * legacy holographic system to keep this path reliable.
 * How: Waits for DOMContentLoaded, then updates status text, creates a canvas
 * animation loop, and logs diagnostics to the console. Provides defensive
 * checks so failure modes are visible instead of silent.
 *
 * Connects to:
 *  - templates/index.html: Expects elements #system-status, #particle-count, #particles
 *  - debug_config / logging pipeline indirectly via console until integrated
 */
(function(){
  // Diagnostic helpers for development
  function log(msg, ...rest){ console.log('[particles-init]', msg, ...rest); }
  function error(msg, ...rest){ console.error('[particles-init]', msg, ...rest); }

  // Helper to reflect phase into #js-init-status (if present)
  function phase(state){
    try {
      var el = document.getElementById('js-init-status');
      if(el) el.textContent = state;
    } catch(e){ /* swallow */ }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  function start(){
    try {
      phase('initializing');
      log('Starting initialization');
      const statusEl = document.getElementById('system-status');
      const countEl = document.getElementById('particle-count');
  const canvasEl = document.getElementById('particles');
  /** @type {HTMLCanvasElement|null} */
  const canvas = /** @type {any} */ (canvasEl);

      if(!canvas){
        error('Canvas #particles not found');
        if(statusEl) statusEl.textContent = 'Canvas missing';
        return;
      }
      if(!canvas.getContext){
        error('Canvas 2D context unsupported');
        if(statusEl) statusEl.textContent = 'No 2D ctx';
        return;
      }

      if(statusEl) statusEl.textContent = 'Online \u2713';

      const ctx = canvas.getContext('2d');
      resize();
      window.addEventListener('resize', resize);

      // Particle model
      const PARTICLE_COUNT = 25;
      const particles = [];
      for(let i=0;i<PARTICLE_COUNT;i++){
        particles.push({
          x: Math.random()*canvas.width,
          y: Math.random()*canvas.height,
          dx: (Math.random()-0.5)*3,
          dy: (Math.random()-0.5)*3,
          size: Math.random()*2 + 1
        });
      }
  if(countEl) countEl.textContent = String(particles.length);
      log('Particles created', particles.length);
      phase('particles-created');

      function resize(){
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
      }

      function animate(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle = '#00ff88';
        for(const p of particles){
          ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
            ctx.fill();
            p.x += p.dx; p.y += p.dy;
            if(p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if(p.y < 0 || p.y > canvas.height) p.dy *= -1;
        }
        requestAnimationFrame(animate);
      }
      animate();
      phase('running');
      log('Animation loop started');
    } catch (e){
      error('Initialization failed', e);
      const statusEl = document.getElementById('system-status');
      if(statusEl) statusEl.textContent = 'Init error';
      phase('error');
      // Expose failure diagnostics globally for quick console inspection
  try { (window /** @type {any} */)['__CLEVER_PARTICLES_ERROR__'] = e; } catch(_) {}
    }
  }
})();
