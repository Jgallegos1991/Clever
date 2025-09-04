/**
 * 🌌 CLEVER QUANTUM SCENE - Stable Version 🌌
 * Following COPILOT_UI_BRIEF core requirements
 */

(function(){
  console.log('🌌 Quantum Scene: Stable version loading...');
  
  function initScene() {
    const canvas = document.getElementById('scene');
    if(!canvas) {
      return setTimeout(initScene, 50);
    }
    
    const ctx = canvas.getContext('2d');
    
    // Resize canvas to full screen
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Particle system state
    let t = 0;
    let energy = 0.6;
    let targetShape = 'swarm';
    
    // Create particle swarm - optimized for performance
    const points = [];
    for(let i = 0; i < 600; i++) {  // Reduced for stability
      points.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        tx: Math.random() * canvas.width,
        ty: Math.random() * canvas.height,
        vx: 0,
        vy: 0,
        phase: Math.random() * Math.PI * 2,
        size: 0.8 + Math.random() * 1.2,
        // UI Brief color distribution: 70% teal, 30% magenta
        isTeal: Math.random() < 0.7
      });
    }
    
    // Shape generators - clean and reliable
    function generateSwarm() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.6;
      
      points.forEach((p, i) => {
        const angle = (i / points.length) * Math.PI * 2 + t * 0.0008;
        const radius = 120 + Math.sin(i * 0.08 + t * 0.002) * 60;
        
        p.tx = centerX + Math.cos(angle) * radius + Math.sin(i * 0.3 + t * 0.001) * 25;
        p.ty = centerY + Math.sin(angle) * radius * 0.5 + Math.cos(i * 0.3 + t * 0.001) * 15;
      });
    }
    
    function generateCube() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.6;
      const size = 100;
      
      points.forEach((p, i) => {
        const progress = i / points.length;
        
        if (progress < 0.2) {
          // 8 corner vertices
          const corner = Math.floor(progress * 8 / 0.2);
          const x = (corner & 1) ? size/2 : -size/2;
          const y = (corner & 2) ? size/2 : -size/2; 
          const z = (corner & 4) ? size/2 : -size/2;
          
          p.tx = centerX + x;
          p.ty = centerY + y + z * 0.3;
        } else {
          // Edges
          const edgeProgress = (progress - 0.2) / 0.8;
          const t_param = edgeProgress * 12; // 12 edges
          const edge = Math.floor(t_param);
          const local = t_param % 1;
          
          let x, y, z = 0;
          
          if (edge < 4) {
            // Bottom square
            const side = edge;
            if (side === 0) { x = (local - 0.5) * size; y = -size/2; }
            else if (side === 1) { x = size/2; y = (local - 0.5) * size; }
            else if (side === 2) { x = (0.5 - local) * size; y = size/2; }
            else { x = -size/2; y = (0.5 - local) * size; }
            z = -size/2;
          } else if (edge < 8) {
            // Top square
            const side = edge - 4;
            if (side === 0) { x = (local - 0.5) * size; y = -size/2; }
            else if (side === 1) { x = size/2; y = (local - 0.5) * size; }
            else if (side === 2) { x = (0.5 - local) * size; y = size/2; }
            else { x = -size/2; y = (0.5 - local) * size; }
            z = size/2;
          } else {
            // Vertical edges
            const corner = edge - 8;
            x = (corner & 1) ? size/2 : -size/2;
            y = (corner & 2) ? size/2 : -size/2;
            z = (local - 0.5) * size;
          }
          
          p.tx = centerX + x;
          p.ty = centerY + y + z * 0.3;
        }
      });
    }
    
    function generateSphere() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.6;
      const radius = 90;
      
      points.forEach((p, i) => {
        const phi = Math.acos(1 - 2 * (i + 0.5) / points.length);
        const theta = Math.PI * (1 + Math.sqrt(5)) * i;
        
        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.sin(phi) * Math.sin(theta);
        const z = radius * Math.cos(phi);
        
        p.tx = centerX + x;
        p.ty = centerY + y + z * 0.3;
      });
    }
    
    function generateTorus() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.6;
      const majorRadius = 70;
      const minorRadius = 25;
      
      points.forEach((p, i) => {
        const u = (i / points.length) * 2 * Math.PI;
        const v = ((i * 17) % points.length / points.length) * 2 * Math.PI;
        
        const x = (majorRadius + minorRadius * Math.cos(v)) * Math.cos(u);
        const y = (majorRadius + minorRadius * Math.cos(v)) * Math.sin(u);
        const z = minorRadius * Math.sin(v);
        
        p.tx = centerX + x;
        p.ty = centerY + y * 0.6 + z;
      });
    }
    
    // Animation loop - stable 60fps
    function animate() {
      t++;
      
      // Clear with subtle fade for trails
      ctx.fillStyle = 'rgba(11, 15, 20, 0.1)';  // UI Brief cosmic background
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Generate target positions based on shape
      switch(targetShape) {
        case 'cube': generateCube(); break;
        case 'sphere': generateSphere(); break;
        case 'torus': generateTorus(); break;
        default: generateSwarm(); break;
      }
      
      // Update and draw particles
      points.forEach((p, i) => {
        // Smooth movement toward target
        const dx = p.tx - p.x;
        const dy = p.ty - p.y;
        const distance = Math.sqrt(dx*dx + dy*dy);
        
        // Organic easing
        const ease = Math.min(0.06, distance * 0.0005 + 0.008);
        p.x += dx * ease;
        p.y += dy * ease;
        
        // Subtle breathing
        const breath = Math.sin(p.phase + t * 0.006) * 0.6;
        const flutter = Math.cos(p.phase * 1.2 + t * 0.008) * 0.4;
        p.x += breath;
        p.y += flutter;
        p.phase += 0.002;
        
        // Render particle
        const alpha = 0.9 + Math.sin(i * 0.1 + t * 0.01) * 0.1;
        const size = p.size * (0.7 + energy * 0.3);
        
        // UI Brief exact colors
        const color = p.isTeal ? '#69EACB' : '#FF6BFF';  // Electric teal or magenta
        const glowColor = p.isTeal ? 'rgba(105, 234, 203, 0.12)' : 'rgba(255, 107, 255, 0.15)';
        
        // Glow halo
        ctx.beginPath();
        ctx.arc(p.x, p.y, size * 1.5, 0, Math.PI * 2);
        ctx.fillStyle = glowColor;
        ctx.fill();
        
        // Core particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, size * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = color + Math.floor(alpha * 255).toString(16).padStart(2, '0');
        ctx.fill();
      });
      
      // Energy decay
      energy = Math.max(0.2, energy * 0.995);
      
      requestAnimationFrame(animate);
    }
    
    // Global interface functions
    window.__orbPulse = function(intensity) {
      energy = Math.min(1.0, energy + (intensity || 0.2));
    };
    
    window.__orbThinking = function(active) {
      if (active) {
        energy += 0.15;
        document.body.classList.add('thinking');
      } else {
        document.body.classList.remove('thinking');
      }
    };
    
    window.__sceneSetShape = function(shape) {
      if (shape !== targetShape) {
        energy += 0.4;
        targetShape = shape || 'swarm';
      }
    };
    
    window.__sceneMorphForDialogue = function(meta) {
      const m = meta || {};
      window.__sceneSetShape(m.shape || 'cube');
    };
    
    window.__sceneParticles = function() { return points; };
    window.__sceneSetParticleLevel = function(level) { /* No-op for performance */ };
    window.__sceneSetParticleBrightness = function(brightness) { 
      energy = Math.min(1.0, energy + brightness * 0.1);
    };
    window.__orbSetMood = function(mood) { /* Mood handled by color mix */ };
    window.__orbSetMode = function(mode) { /* Mode handled by energy */ };
    window.__sceneSpeakText = function(text) { energy += 0.2; };
    
    // Start the animation
    animate();
    console.log('✨ Stable quantum scene initialized');
  }

  // Initialize when ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScene);
  } else {
    initScene();
  }
})();
