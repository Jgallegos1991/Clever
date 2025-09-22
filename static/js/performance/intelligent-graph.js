/*
Enhanced Intelligent Graph Visualization System

Why: Transform the basic graph debug overlay into a powerful AI-driven architecture
analysis tool that visualizes problems, suggests fixes, and provides interactive
insights about code quality, performance, and architectural patterns. This elevates
the Why/Where/How system into an intelligent development assistant.

Where: Loaded by index.html when ?graph=1 or ?debug=graph is present. Connects to
enhanced runtime_introspect endpoint that includes intelligent analysis results.
Integrates with the existing graph system while adding layers of AI insights.

How: Builds on the existing canvas-based graph renderer with enhanced problem
highlighting, interactive fix suggestions, intelligent filtering, trend analysis,
and real-time recommendations. Uses color coding, animations, and overlays to
make problems and insights immediately visible and actionable.

Connects to:
    - introspection.py: Enhanced runtime state with intelligent analysis
    - intelligent_analyzer.py: AI-powered problem detection and insights
    - graph-debug.js: Base graph visualization (extends this functionality)
*/
(function(){
  const enabled = /[?&](graph=1|debug=graph|intelligent=1)/.test(location.search);
  if(!enabled) return;

  // Enhanced graph visualization with AI insights
  const canvas = document.createElement('canvas');
  canvas.id = 'intelligent-graph-canvas';
  Object.assign(canvas.style, {
    position:'fixed', top:'0', left:'0', width:'520px', height:'520px',
    zIndex: 9998, background:'rgba(5,10,15,0.88)', border:'2px solid #0066cc',
    borderRadius:'8px', font:'12px system-ui, sans-serif', color:'#e0f0ff',
    boxShadow:'0 6px 32px rgba(0,50,100,0.6)', pointerEvents:'auto',
    transition: 'all 0.3s ease'
  });
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  // Problem severity colors
  const SEVERITY_COLORS = {
    'CRITICAL': '#ff0000',
    'HIGH': '#ff4444', 
    'MEDIUM': '#ff8800',
    'LOW': '#ffcc00'
  };

  const CATEGORY_COLORS = {
    'ARCHITECTURAL': '#ff4444',
    'PERFORMANCE': '#ff8800',
    'DOCUMENTATION': '#ffcc00', 
    'SECURITY': '#cc0000',
    'COUPLING': '#ff6600',
    'COMPLEXITY': '#ffaa00',
    'OPTIMIZATION': '#4488ff'
  };

  // Maintain logical pixel ratio
  function resize(){
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
  }
  resize(); 
  window.addEventListener('resize', resize);

  const state = {
    nodes: {}, // id -> {id,label,type,x,y,vx,vy,deg,problems:[]}
    edges: [],
    problems: [], // intelligent analysis results
    insights: [], // architectural insights
    lastFetch: 0,
    focus: null,
    selectedProblem: null,
    filter: 'all', // all|problems|critical|performance|architecture
    showRecommendations: false,
    qualityScore: 0,
    trendData: {},
    meta: { rg_ts: null, cg_ts: null, ia_ts: null }
  };

  // Enhanced legend with intelligent analysis info
  const legend = document.createElement('div');
  Object.assign(legend.style, {
    position:'fixed', top:'6px', left:'530px', padding:'12px', 
    background:'rgba(10,20,35,0.92)', color:'#e0f0ff', 
    font:'12px system-ui, sans-serif', zIndex:9999, 
    border:'2px solid #0066cc', borderRadius:'8px',
    lineHeight:'1.4', maxWidth:'280px'
  });
  
  legend.innerHTML = `
    <div style="display:flex;align-items:center;margin-bottom:8px">
      <strong style="color:#66ccff;font-size:14px">🧠 Intelligent Graph</strong>
      <div id="quality-score" style="margin-left:auto;font-weight:bold"></div>
    </div>
    <div style="font-size:11px;color:#99ccff;margin-bottom:8px">
      <em>Keys:</em> [0]=All [1]=Problems [2]=Critical [3]=Performance [4]=Architecture<br>
      <em>Click:</em> Node to focus, Problem to see fix suggestions
    </div>
    <div id="gd-counts" style="margin-bottom:6px"></div>
    <div id="gd-problem-stats" style="margin-bottom:6px"></div>
    <div id="gd-timestamps" style="font-size:10px;color:#77aadd"></div>
  `;
  
  document.body.appendChild(legend);
  const countsEl = legend.querySelector('#gd-counts');
  const problemStatsEl = legend.querySelector('#gd-problem-stats');
  const tsEl = legend.querySelector('#gd-timestamps');
  const qualityScoreEl = legend.querySelector('#quality-score');

  // Recommendations panel
  const recommendationsPanel = document.createElement('div');
  Object.assign(recommendationsPanel.style, {
    position:'fixed', top:'540px', left:'0px', width:'520px', 
    maxHeight:'200px', overflow:'auto', padding:'12px',
    background:'rgba(10,20,35,0.95)', color:'#e0f0ff',
    border:'2px solid #0066cc', borderRadius:'8px',
    font:'11px system-ui, sans-serif', lineHeight:'1.3',
    display:'none', zIndex:9999
  });
  document.body.appendChild(recommendationsPanel);

  async function fetchIntelligentGraph(){
    try {
      const res = await fetch('/api/runtime_introspect');
      if(!res.ok) return;
      const data = await res.json();
      
      // Process traditional graph data
      const rg = data.reasoning_graph || {nodes:[],edges:[]};
      const cg = data.concept_graph || null;
      const ia = data.intelligent_analysis || null;
      
      state.meta.rg_ts = rg.generated_at || rg.generated_ts || null;
      state.meta.cg_ts = cg && (cg.generated_at || cg.generated_ts) || null;
      state.meta.ia_ts = ia && ia.generated_at || null;
      
      // Merge traditional nodes
      const combinedNodes = [...rg.nodes];
      if(cg && cg.nodes){ combinedNodes.push(...cg.nodes.map(n=>({...n, type:n.type||'concept'}))); }
      const combinedEdges = [...rg.edges];
      if(cg && cg.edges){ combinedEdges.push(...cg.edges); }
      
      // Process intelligent analysis
      if(ia && !ia.error) {
        state.problems = ia.analysis_results || [];
        state.insights = ia.architectural_insights || [];
        state.qualityScore = ia.quality_score || 0;
        state.trendData = ia.trend_analysis || {};
        
        // Attach problems to nodes
        combinedNodes.forEach(node => {
          node.problems = state.problems.filter(p => 
            p.node_id === node.id || p.node_id.includes(node.id)
          );
        });
      }
      
      // Initialize or update node positions
      combinedNodes.forEach((n,i)=>{
        if(!state.nodes[n.id]){
          const angle = i / Math.max(1, combinedNodes.length) * Math.PI*2;
          state.nodes[n.id] = {
            id:n.id, label:n.label||n.id, type:n.type||'node',
            x: 240 + Math.cos(angle)*150 + (Math.random()*10-5),
            y: 240 + Math.sin(angle)*150 + (Math.random()*10-5),
            vx:0, vy:0, problems: n.problems || []
          };
        } else {
          // Update problems for existing nodes
          state.nodes[n.id].problems = n.problems || [];
        }
      });
      
      // Remove stale nodes
      Object.keys(state.nodes).forEach(id=>{
        if(!combinedNodes.find(n=>n.id === id)) delete state.nodes[id];
      });
      
      state.edges = combinedEdges.filter(e=>state.nodes[e.source] && state.nodes[e.target]);
      
      // Compute degrees
      Object.values(state.nodes).forEach(n=>{ n.deg = 0; });
      state.edges.forEach(e=>{ 
        const a=state.nodes[e.source]; 
        const b=state.nodes[e.target]; 
        if(a) a.deg++; 
        if(b) b.deg++; 
      });
      
      state.lastFetch = performance.now();
      updateIntelligentLegend();
    } catch(e){ 
      console.warn('Failed to fetch intelligent graph data:', e);
    }
  }

  // Enhanced physics with problem-based attraction/repulsion
  const REP = 3200; // increased for larger canvas
  const SPRING = 0.06;
  const DAMP = 0.88;
  const CENTER_PULL = 0.015;
  const PROBLEM_REPULSION = 800; // nodes with problems repel more

  function step(){
    const nodes = Object.values(state.nodes);
    
    // Enhanced repulsion with problem weighting
    for(let i=0;i<nodes.length;i++){
      for(let j=i+1;j<nodes.length;j++){
        const a = nodes[i], b = nodes[j];
        let dx = a.x - b.x; let dy = a.y - b.y; let d2 = dx*dx + dy*dy + 0.01;
        
        // Increase repulsion for nodes with problems
        let repulsion = REP;
        if(a.problems?.length > 0 || b.problems?.length > 0) {
          repulsion += PROBLEM_REPULSION;
        }
        
        const f = repulsion / d2;
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
      const cx = 260 - n.x; const cy = 260 - n.y;
      n.vx += cx * CENTER_PULL; n.vy += cy * CENTER_PULL;
      n.vx *= DAMP; n.vy *= DAMP;
      n.x += n.vx * 0.016; n.y += n.vy * 0.016;
    });
  }

  function updateIntelligentLegend(){
    const nodes = Object.values(state.nodes);
    const counts = {endpoint:0,target:0,concept:0,problems:0};
    
    nodes.forEach(n=>{
      counts[n.type] = (counts[n.type]||0)+1;
      if(n.problems?.length > 0) counts.problems++;
    });
    
    countsEl.textContent = `Nodes: ${counts.endpoint||0}E ${counts.target||0}T ${counts.concept||0}C | Problems: ${counts.problems}`;
    
    // Problem statistics
    const problemCounts = {CRITICAL:0, HIGH:0, MEDIUM:0, LOW:0};
    state.problems.forEach(p => {
      problemCounts[p.severity] = (problemCounts[p.severity] || 0) + 1;
    });
    
    problemStatsEl.innerHTML = `
      <span style="color:${SEVERITY_COLORS.CRITICAL}">●${problemCounts.CRITICAL}</span>
      <span style="color:${SEVERITY_COLORS.HIGH}">●${problemCounts.HIGH}</span>
      <span style="color:${SEVERITY_COLORS.MEDIUM}">●${problemCounts.MEDIUM}</span>
      <span style="color:${SEVERITY_COLORS.LOW}">●${problemCounts.LOW}</span>
    `;
    
    // Quality score with color coding
    const scoreColor = state.qualityScore >= 80 ? '#00ff00' : 
                      state.qualityScore >= 60 ? '#ffff00' : '#ff6600';
    qualityScoreEl.innerHTML = `<span style="color:${scoreColor}">${state.qualityScore.toFixed(0)}%</span>`;
    
    const fmt = ts=> ts? new Date(ts*1000).toLocaleTimeString() : '—';
    tsEl.textContent = `RG: ${fmt(state.meta.rg_ts)} | IA: ${fmt(state.meta.ia_ts)}`;
  }

  function draw(){
    const rectW = canvas.width; const rectH = canvas.height;
    const dpr = window.devicePixelRatio;
    ctx.clearRect(0,0,rectW,rectH);
    ctx.save();
    ctx.scale(dpr, dpr);
    
    // Enhanced edge rendering with problem highlighting
    ctx.lineWidth = 1;
    state.edges.forEach(e=>{
      const a = state.nodes[e.source]; const b = state.nodes[e.target]; 
      if(!a||!b) return;
      
      if(state.filter !== 'all') {
        const shouldShow = checkFilterMatch(a) || checkFilterMatch(b);
        if(!shouldShow) return;
      }
      
      // Highlight edges connected to problem nodes
      const hasProblem = (a.problems?.length > 0) || (b.problems?.length > 0);
      const isSelected = (state.focus && (e.source===state.focus || e.target===state.focus));
      
      if(isSelected) {
        ctx.strokeStyle = '#66ccff';
        ctx.lineWidth = 2;
      } else if(hasProblem) {
        ctx.strokeStyle = 'rgba(255,100,100,0.4)';
      } else {
        ctx.strokeStyle = 'rgba(180,220,255,0.25)';
      }
      
      ctx.beginPath(); 
      ctx.moveTo(a.x,a.y); 
      ctx.lineTo(b.x,b.y); 
      ctx.stroke();
      ctx.lineWidth = 1;
    });
    
    // Enhanced node rendering with problem visualization
    const nodes = Object.values(state.nodes);
    nodes.forEach(n=>{
      if(state.filter !== 'all' && !checkFilterMatch(n)) return;
      
      const base = n.type === 'endpoint' ? 9 : (n.type==='concept'?6:7);
      const degreeBonus = Math.min(8, (n.deg||0)*0.8);
      const problemBonus = (n.problems?.length || 0) * 2;
      const r = base + degreeBonus + problemBonus;
      
      // Determine node color based on problems
      let nodeColor = '#99ccff'; // default
      if(n.id === state.focus) {
        nodeColor = '#66ccff';
      } else if(n.problems?.length > 0) {
        // Color by most severe problem
        const severities = n.problems.map(p => p.severity);
        if(severities.includes('CRITICAL')) nodeColor = SEVERITY_COLORS.CRITICAL;
        else if(severities.includes('HIGH')) nodeColor = SEVERITY_COLORS.HIGH;
        else if(severities.includes('MEDIUM')) nodeColor = SEVERITY_COLORS.MEDIUM;
        else nodeColor = SEVERITY_COLORS.LOW;
      } else if(n.type === 'concept') {
        nodeColor = '#55aa99';
      }
      
      ctx.beginPath();
      
      // Add pulsing effect for critical problems
      if(n.problems?.some(p => p.severity === 'CRITICAL')) {
        const pulse = Math.sin(Date.now() * 0.008) * 0.3 + 1;
        ctx.arc(n.x, n.y, r * pulse, 0, Math.PI*2);
        ctx.fillStyle = nodeColor;
        ctx.fill();
        
        // Add warning ring
        ctx.beginPath();
        ctx.arc(n.x, n.y, r + 3, 0, Math.PI*2);
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.lineWidth = 1;
      } else {
        ctx.arc(n.x, n.y, r, 0, Math.PI*2);
        ctx.fillStyle = nodeColor;
        ctx.fill();
        
        // Add problem indicator ring
        if(n.problems?.length > 0) {
          ctx.beginPath();
          ctx.arc(n.x, n.y, r + 2, 0, Math.PI*2);
          ctx.strokeStyle = nodeColor;
          ctx.lineWidth = 1.5;
          ctx.stroke();
        }
      }
    });
    
    // Enhanced labels with problem counts
    ctx.font = '11px system-ui,sans-serif';
    nodes.slice(0,100).forEach(n=>{
      if(state.filter !== 'all' && !checkFilterMatch(n)) return;
      
      ctx.fillStyle = '#e0f0ff';
      let label = n.label.slice(0,18);
      if(n.problems?.length > 0) {
        label += ` (${n.problems.length})`;
      }
      ctx.fillText(label, n.x+12, n.y+4);
    });
    
    // Quality trend indicator
    if(state.trendData.quality_trend) {
      ctx.fillStyle = state.trendData.quality_trend === 'improving' ? '#00ff00' : 
                     state.trendData.quality_trend === 'declining' ? '#ff6600' : '#ffff00';
      const trendSymbol = state.trendData.quality_trend === 'improving' ? '↗' : 
                         state.trendData.quality_trend === 'declining' ? '↘' : '→';
      ctx.font = '16px system-ui,sans-serif';
      ctx.fillText(`Quality ${trendSymbol}`, 8, 30);
    }
    
    ctx.restore();
  }

  function checkFilterMatch(node) {
    switch(state.filter) {
      case 'problems': return node.problems?.length > 0;
      case 'critical': return node.problems?.some(p => p.severity === 'CRITICAL');
      case 'performance': return node.problems?.some(p => p.category === 'PERFORMANCE');
      case 'architecture': return node.problems?.some(p => p.category === 'ARCHITECTURAL');
      default: return true;
    }
  }

  function showRecommendations(problem) {
    if(!problem) {
      recommendationsPanel.style.display = 'none';
      return;
    }
    
    let html = `
      <div style="border-bottom:1px solid #0066cc;padding-bottom:8px;margin-bottom:8px">
        <strong style="color:${CATEGORY_COLORS[problem.category] || '#ffcc00'}">${problem.title}</strong>
        <span style="float:right;color:${SEVERITY_COLORS[problem.severity]}">${problem.severity}</span>
      </div>
      <div style="margin-bottom:8px;color:#ccddee">${problem.description}</div>
    `;
    
    if(problem.fix_suggestions?.length > 0) {
      html += `<div style="color:#99ccff;font-weight:bold;margin-bottom:4px">💡 Fix Suggestions:</div>`;
      problem.fix_suggestions.forEach(fix => {
        html += `<div style="margin-left:12px;margin-bottom:3px">• ${fix}</div>`;
      });
    }
    
    if(problem.performance_impact) {
      html += `<div style="color:#88ff88;margin-top:6px">⚡ Impact: ${problem.performance_impact}</div>`;
    }
    
    recommendationsPanel.innerHTML = html;
    recommendationsPanel.style.display = 'block';
  }

  // Enhanced click handling
  canvas.addEventListener('click', (e)=>{
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left); 
    const y = (e.clientY - rect.top);
    
    let closest = null; 
    let best = 1e9;
    let clickedProblem = null;
    
    Object.values(state.nodes).forEach(n=>{
      const dx = n.x - x; const dy = n.y - y; const d2 = dx*dx+dy*dy;
      if(d2 < best && d2 < 600) { 
        best = d2; 
        closest = n.id;
        // Find the most severe problem for this node
        if(n.problems?.length > 0) {
          clickedProblem = n.problems.sort((a,b) => {
            const severityOrder = {CRITICAL:4, HIGH:3, MEDIUM:2, LOW:1};
            return severityOrder[b.severity] - severityOrder[a.severity];
          })[0];
        }
      }
    });
    
    state.focus = closest;
    state.selectedProblem = clickedProblem;
    showRecommendations(clickedProblem);
  });

  async function loop(){
    if(performance.now() - state.lastFetch > 8000){ // slower refresh for complex analysis
      fetchIntelligentGraph(); 
    }
    step(); 
    draw(); 
    requestAnimationFrame(loop);
  }
  
  fetchIntelligentGraph(); 
  loop();

  // Enhanced keyboard controls
  window.addEventListener('keydown', (e)=>{
    switch(e.key) {
      case '0': state.filter='all'; break;
      case '1': state.filter='problems'; break;
      case '2': state.filter='critical'; break;
      case '3': state.filter='performance'; break;
      case '4': state.filter='architecture'; break;
      case 'r': fetchIntelligentGraph(); break; // manual refresh
      case 'Escape': 
        state.selectedProblem = null;
        showRecommendations(null);
        break;
    }
  });

  // Auto-hide recommendations after 30 seconds
  setInterval(() => {
    if(state.selectedProblem && recommendationsPanel.style.display === 'block') {
      const age = Date.now() - (state.selectedProblem.timestamp * 1000);
      if(age > 30000) { // 30 seconds
        showRecommendations(null);
      }
    }
  }, 5000);

})();