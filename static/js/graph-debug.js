/*
Graph Debug Overlay (Reasoning + Concept Graph)

Why: Provide an offline, lightweight visualization of the docstring-declared
"arrows" (reasoning_graph) and optional evolution concept network (concept_graph)
so architectural relationships are explorable in real time without external libs.
Where: Loaded by index.html when the URL contains ?graph=1 or ?debug=graph
and attaches to a fixed canvas overlay. Queries /api/runtime_introspect which
already provides reasoning_graph + concept_graph payloads.
How: Performs periodic fetch, builds in-memory node/edge set, runs a tiny force
layout (repulsion + spring) each frame, and renders circles + lines on canvas.
No external dependencies for offline compliance.
*/
(function(){
  const enabled = /[?&](graph=1|debug=graph)/.test(location.search);
  if(!enabled) return;
  const canvas = document.createElement('canvas');
  canvas.id = 'graph-debug-canvas';
  Object.assign(canvas.style, {
    position:'fixed', top:'0', left:'0', width:'420px', height:'420px',
    zIndex: 9998, background:'rgba(10,14,20,0.78)', border:'1px solid #123',
    borderRadius:'6px', font:'12px system-ui, sans-serif', color:'#cff',
    boxShadow:'0 4px 24px rgba(0,0,0,0.4)', pointerEvents:'auto'
  });
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  // Maintain logical pixel ratio
  function resize(){
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
  }
  resize(); window.addEventListener('resize', resize);

  const state = {
    nodes: {}, // id -> {id,label,type,x,y,vx,vy}
    edges: [],
    lastFetch: 0,
    focus: null,
    warning: null,
  };

  async function fetchGraph(){
    try {
      const res = await fetch('/api/runtime_introspect');
      if(!res.ok) return;
      const data = await res.json();
      const rg = data.reasoning_graph || {nodes:[],edges:[]};
      const cg = data.concept_graph || null;
      state.warning = rg.truncated ? 'reasoning truncated' : null;
      // Merge nodes (concept nodes get suffix to avoid id collision if any)
      const combinedNodes = [...rg.nodes];
      if(cg && cg.nodes){ combinedNodes.push(...cg.nodes.map(n=>({...n, type:n.type||'concept'}))); }
      const combinedEdges = [...rg.edges];
      if(cg && cg.edges){ combinedEdges.push(...cg.edges); }
      // Initialize or update positions
      combinedNodes.forEach((n,i)=>{
        if(!state.nodes[n.id]){
          const angle = i / Math.max(1, combinedNodes.length) * Math.PI*2;
          state.nodes[n.id] = {
            id:n.id, label:n.label||n.id, type:n.type||'node',
            x: 180 + Math.cos(angle)*120 + (Math.random()*8-4),
            y: 180 + Math.sin(angle)*120 + (Math.random()*8-4),
            vx:0, vy:0
          };
        }
      });
      // Remove stale nodes
      Object.keys(state.nodes).forEach(id=>{
        if(!combinedNodes.find(n=>n.id === id)) delete state.nodes[id];
      });
      state.edges = combinedEdges.filter(e=>state.nodes[e.source] && state.nodes[e.target]);
      state.lastFetch = performance.now();
    } catch(e){ /* silent */ }
  }

  // Physics parameters
  const REP = 2600; // repulsion strength
  const SPRING = 0.08; // edge spring
  const DAMP = 0.85; // velocity damping
  const CENTER_PULL = 0.02; // mild centering force

  function step(){
    const nodes = Object.values(state.nodes);
    // Repulsion
    for(let i=0;i<nodes.length;i++){
      for(let j=i+1;j<nodes.length;j++){
        const a = nodes[i], b = nodes[j];
        let dx = a.x - b.x; let dy = a.y - b.y; let d2 = dx*dx + dy*dy + 0.01;
        const f = REP / d2;
        const df = f / Math.sqrt(d2);
        a.vx += dx*df; a.vy += dy*df;
        b.vx -= dx*df; b.vy -= dy*df;
      }
    }
    // Springs
    state.edges.forEach(e=>{
      const a = state.nodes[e.source]; const b = state.nodes[e.target];
      if(!a||!b) return;
      const dx = b.x - a.x; const dy = b.y - a.y;
      a.vx += dx * SPRING; a.vy += dy * SPRING;
      b.vx -= dx * SPRING; b.vy -= dy * SPRING;
    });
    // Integrate & center
    nodes.forEach(n=>{
      const cx = 180 - n.x; const cy = 180 - n.y;
      n.vx += cx * CENTER_PULL; n.vy += cy * CENTER_PULL;
      n.vx *= DAMP; n.vy *= DAMP;
      n.x += n.vx * 0.016; n.y += n.vy * 0.016; // assume ~60fps
    });
  }

  function draw(){
    const rectW = canvas.width; const rectH = canvas.height;
    ctx.clearRect(0,0,rectW,rectH);
    ctx.save();
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    // Edges
    ctx.lineWidth = 1;
    state.edges.forEach(e=>{
      const a = state.nodes[e.source]; const b = state.nodes[e.target]; if(!a||!b) return;
      ctx.strokeStyle = (state.focus && (e.source===state.focus || e.target===state.focus)) ? '#6ff' : 'rgba(180,220,255,0.25)';
      ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
    });
    // Nodes
    const nodes = Object.values(state.nodes);
    nodes.forEach(n=>{
      const r = n.type === 'endpoint' ? 8 : (n.type==='concept'?5:6);
      ctx.beginPath();
      ctx.fillStyle = n.id===state.focus ? '#6ff' : (n.type==='concept' ? '#5fa' : '#9cf');
      ctx.arc(n.x, n.y, r, 0, Math.PI*2);
      ctx.fill();
    });
    // Labels (limited for perf)
    ctx.font = '11px system-ui,sans-serif';
    ctx.fillStyle = '#cfe';
    nodes.slice(0,120).forEach(n=>{
      ctx.fillText(n.label.slice(0,18), n.x+10, n.y+4);
    });
    if(state.warning){
      ctx.fillStyle = '#f99';
      ctx.fillText(state.warning, 8, rectH/window.devicePixelRatio - 12);
    }
    ctx.restore();
  }

  canvas.addEventListener('click', (e)=>{
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left); const y = (e.clientY - rect.top);
    let closest = null; let best = 1e9;
    Object.values(state.nodes).forEach(n=>{
      const dx = n.x - x; const dy = n.y - y; const d2 = dx*dx+dy*dy;
      if(d2 < best && d2 < 400) { best = d2; closest = n.id; }
    });
    state.focus = closest;
  });

  async function loop(){
    if(performance.now() - state.lastFetch > 5000){ fetchGraph(); }
    step(); draw(); requestAnimationFrame(loop);
  }
  fetchGraph(); loop();
})();
