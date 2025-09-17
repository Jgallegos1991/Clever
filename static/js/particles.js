// Particle Field — magical swarm with shape morphs (Canvas2D, Chromebook-friendly)
(function(){
  let state = {
    ctx: null,
    canvas: null,
    w: 0,
    h: 0,
    dpr: 1,
    pts: [],
    targets: null,
    speed: 1,
    pulse: 0,
    running: false
  };

  function resize(){
    if (!state.canvas || !state.ctx) return;
    const c = state.canvas, ctx = state.ctx;
    state.w = c.clientWidth; state.h = c.clientHeight;
    state.dpr = Math.min(2, window.devicePixelRatio || 1);
    c.width = Math.max(1, Math.floor(state.w * state.dpr));
    c.height = Math.max(1, Math.floor(state.h * state.dpr));
    ctx.setTransform(state.dpr, 0, 0, state.dpr, 0, 0);
  }

  function makePoints(n){
    const pts = new Array(n);
    for (let i=0;i<n;i++){
      pts[i] = {
        x: Math.random()*state.w,
        y: Math.random()*state.h,
        vx: (Math.random()-0.5)*0.25,
        vy: (Math.random()-0.5)*0.25,
        tx: null, ty: null,
        a: Math.random()*0.5 + 0.15,
        s: Math.random()*0.8 + 0.6
      };
    }
    return pts;
  }

  function shapeToPoints(kind, n){
    const pts = [];
    const cx = state.w*0.5, cy = state.h*0.5;
    const minDim = Math.min(state.w, state.h);
    const R = Math.max(40, minDim*0.28);
    if (kind === 'sphere'){
      // circle ring + fill sampling
      for (let i=0;i<n;i++){
        const t = Math.random()*Math.PI*2;
        const r = Math.sqrt(Math.random())*R; // denser center
        pts.push({x: cx + Math.cos(t)*r, y: cy + Math.sin(t)*r});
      }
    } else if (kind === 'torus'){
      const r1 = R*0.75, thickness = Math.max(8, R*0.20);
      for (let i=0;i<n;i++){
        const t = (i/n)*Math.PI*2 + Math.random()*0.02;
        const r = r1 + (Math.random()-0.5)*thickness;
        pts.push({x: cx + Math.cos(t)*r, y: cy + Math.sin(t)*r});
      }
    } else if (kind === 'cube'){
      const w = R*1.4, h = R*1.0;
      const cols = Math.max(10, Math.floor(Math.sqrt(n)));
      const rows = Math.max(8, Math.floor(n/cols));
      for (let r=0;r<rows;r++){
        for (let c=0;c<cols;c++){
          if (pts.length>=n) break;
          const x = cx - w/2 + (c/(cols-1))*w;
          const y = cy - h/2 + (r/(rows-1))*h;
          pts.push({x, y});
        }
      }
    } else if (kind === 'galaxy'){
      // spiral galaxy
      const arms = 3, twist = 5;
      for (let i=0;i<n;i++){
        const arm = i % arms;
        const t = (i/n)*Math.PI*2*twist + arm*(Math.PI*2/arms);
        const r = (i/n)*R;
        const jitter = Math.random()*8;
        pts.push({x: cx + Math.cos(t)*r + (Math.random()-0.5)*jitter,
                  y: cy + Math.sin(t)*r + (Math.random()-0.5)*jitter});
      }
    } else { // swarm/random
      for (let i=0;i<n;i++) pts.push({x: Math.random()*state.w, y: Math.random()*state.h});
    }
    return pts;
  }

  function setTargets(kind){
    if (!state.pts?.length) return;
    const n = state.pts.length;
    const targets = shapeToPoints(kind, n);
    for (let i=0;i<n;i++){
      const p = state.pts[i];
      const t = targets[i];
      p.tx = t.x; p.ty = t.y;
    }
    state.targets = kind;
  }

  function draw(){
    const {ctx,w,h,pts} = state;
    if (!ctx) return;
    ctx.clearRect(0,0,w,h);
    
    const base = 'rgba(105,234,203,'; // soft teal
    const pulse = state.pulse;
    for (const p of pts){
      // integrate motion
      if (p.tx!=null && p.ty!=null){
        // spring to target
        const dx = p.tx - p.x, dy = p.ty - p.y;
        p.vx += dx*0.0025*state.speed; p.vy += dy*0.0025*state.speed;
      } else {
        // gentle drift
        p.vx += (Math.random()-0.5)*0.015*state.speed;
        p.vy += (Math.random()-0.5)*0.015*state.speed;
      }
      // damping
      p.vx *= 0.98; p.vy *= 0.98;
        p.vx += (Math.random()-0.5)*0.02*state.speed;
        p.vy += (Math.random()-0.5)*0.02*state.speed;
      }
      // damping
      p.vx *= 0.965; p.vy *= 0.965;
      p.x += p.vx; p.y += p.vy;
      if (p.x<0) p.x=w; else if (p.x>w) p.x=0;
      if (p.y<0) p.y=h; else if (p.y>h) p.y=0;

      // More subtle, elegant particles
      const baseAlpha = Math.min(0.4, Math.max(0.02, p.a + pulse*0.2));
      const size = Math.max(0.5, p.s * 0.8 + pulse*0.5);
      
      // Create gradient effect for more beauty
      const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, size*2);
      gradient.addColorStop(0, `rgba(105,234,203,${baseAlpha})`);
      gradient.addColorStop(0.7, `rgba(105,234,203,${baseAlpha*0.5})`);
      gradient.addColorStop(1, 'rgba(105,234,203,0)');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
      ctx.fill();
    }
    // decay pulse
    state.pulse *= 0.94;
      const a = Math.min(1, Math.max(0.06, p.a + pulse*0.35));
      const s = (p.s + pulse*1.1);
      ctx.fillStyle = base + a + ')';
      ctx.fillRect(p.x, p.y, s, s);
    }
    // decay pulse
    state.pulse *= 0.92;
  }

  function loop(){
    if (!state.running) return;
    draw();
    requestAnimationFrame(loop);
  }

  function startParticles(canvas, opts){
    if (!(canvas instanceof HTMLCanvasElement)) return;
    state.canvas = canvas; state.ctx = canvas.getContext('2d');
    if (!state.ctx) return;
    resize();
    const maxCount = Math.min(7000, Math.floor((state.w*state.h)/800));
    const count = Math.min(maxCount, (opts && opts.count) || 5000);
    state.pts = makePoints(count);
    state.running = true;
    addEventListener('resize', () => {
      const prevTargets = state.targets; resize();
      // preserve particles; re-target to new shape space
      if (state.pts?.length){
        const n = state.pts.length;
        const newPts = makePoints(n);
        // keep current positions, only ensure in-bounds
        for (let i=0;i<n;i++){
          const p = state.pts[i];
          p.x = Math.min(state.w, Math.max(0, p.x));
          p.y = Math.min(state.h, Math.max(0, p.y));
        }
        if (prevTargets) setTargets(prevTargets);
      }
    });
    loop();
  }

  function updateFieldMode(mode){
    // Map modes to speed/behavior
    const m = String(mode||'').toLowerCase();
    if (m.includes('creative')) state.speed = 1.25;
    else if (m.includes('deep')) state.speed = 0.9;
    else if (m.includes('focus')) state.speed = 0.8;
    else state.speed = 1.0;
  }

  function triggerPulse(intensity){
    const k = Math.max(0.1, Math.min(1.8, Number(intensity)||0.6));
    state.pulse = Math.max(state.pulse, k);
  }

  function morphForIntent(intent){
    const i = String(intent||'').toLowerCase();
    if (i.includes('creative')) setTargets('torus');
    else if (i.includes('deep')) setTargets('cube');
    else if (i.includes('galaxy')) setTargets('galaxy');
    else if (i.includes('casual') || i.includes('chat')) setTargets('sphere');
    else setTargets('sphere');
    triggerPulse(0.7);
  }

  // Dissolve: release targets so particles drift back to ambient swarm
  function dissolveToSwarm(){
    if (!state.pts) return;
    for (const p of state.pts){
      p.tx = null; p.ty = null;
      // give a tiny randomized nudge to create a shimmer
      p.vx += (Math.random()-0.5)*0.6;
      p.vy += (Math.random()-0.5)*0.6;
    }
    state.targets = null;
    triggerPulse(0.4);
  }

  // Export API
  window.startParticles = startParticles;
  window.updateFieldMode = updateFieldMode;
  window.triggerPulse = triggerPulse;
  window.morphForIntent = morphForIntent;
  // Use bracket notation to appease TS/linters in JS context
  window['dissolveToSwarm'] = dissolveToSwarm;
})();
