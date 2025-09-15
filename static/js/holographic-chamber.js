// Holographic Chamber - Advanced Particle System for Clever AI
// CONFIG NOTE: For best performance, render particles as simple pixels (fillRect) instead of blurred/glowing circles. This eliminates lag and ensures smooth animation even with high particle counts.
// Quantum swarm with morphing behaviors: idle → summon → dialogue → dissolve

class HolographicChamber {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.state = 'idle'; // idle, summon, dialogue, dissolve
    this.targetFormation = null;
    
    // Performance settings optimized for Chromebook
    // Adaptive performance: auto-tune particle count based on device
  // Lower particle count for performance
  this.maxParticles = 60;
  // Force dpr to 1 for crisp pixel rendering and avoid scaling issues
  this.dpr = 1;
    
    this.init();
  }

  init() {
    console.log('🔧 Initializing holographic chamber...');
    this.resize();
    console.log(`📏 Canvas size: ${this.width}x${this.height}`);
    this.createParticles();
    console.log(`✨ Created ${this.particles.length} particles`);
    
    // Add mouse interaction
    this.mouse = { x: this.width / 2, y: this.height / 2 };
    this.addMouseInteraction();
    this.addAccessibilityControls();
    this.addDebugToggle();
    
  // Always start with whirlpool formation for idle
  this.morphToFormation('whirlpool');
    
    this.animate();
    console.log('🎬 Animation started with whirlpool formation');
    console.log('🎯 Particles should now be EXTREMELY VISIBLE with debug text');
    
    // Listen for window resize
    window.addEventListener('resize', () => this.resize());
  }

  addMouseInteraction() {
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = e.clientX - rect.left;
      this.mouse.y = e.clientY - rect.top;
    });
    // Removed random formation trigger on canvas click to keep whirlpool idle state
  }

  startFormationCycle() {
    const formations = ['whirlpool', 'sphere', 'cube', 'torus', 'helix', 'wave', 'spiral', 'scatter'];
    let currentIndex = 0;
    
    // Change formation every 6 seconds for more dynamic feel
    setInterval(() => {
      this.morphToFormation(formations[currentIndex]);
      currentIndex = (currentIndex + 1) % formations.length;
    }, 6000);
    
    // Start with whirlpool - the signature "bottom centered lively whirlpool"
    this.morphToFormation('whirlpool');
  }

  triggerRandomFormation() {
    const formations = ['cube', 'torus', 'helix', 'wave', 'spiral'];
    const randomFormation = formations[Math.floor(Math.random() * formations.length)];
    this.morphToFormation(randomFormation);
  }

  resize() {
  // Use window innerWidth/innerHeight for full viewport coverage
  this.width = window.innerWidth;
  this.height = window.innerHeight;
  this.canvas.width = this.width;
  this.canvas.height = this.height;
  this.ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset any scaling
  this.canvas.style.width = this.width + 'px';
  this.canvas.style.height = this.height + 'px';
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.maxParticles; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
    vx: (Math.random() - 0.5) * 0.2,
    vy: (Math.random() - 0.5) * 0.2,
    targetX: Math.random() * this.width,
    targetY: Math.random() * this.height,
    size: Math.random() * 2 + 1,
    alpha: Math.random() * 0.4 + 0.6,
    hue: Math.random() * 60 + 160,
    phase: Math.random() * Math.PI * 2,
    speed: 0.005 + Math.random() * 0.004, // Minimum movement
    energy: Math.random() * 0.08 + 0.08 // Minimum pulsing
      });
    }
  }

  morphToFormation(formation) {
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    const radius = Math.min(this.width, this.height) * 0.35;

    this.particles.forEach((particle, i) => {
      // Add some randomness for organic feel
      const randomOffset = () => (Math.random() - 0.5) * 20;
      
      switch (formation) {
        case 'sphere':
          const angle = (i / this.particles.length) * Math.PI * 2;
          const layers = Math.floor(i / 30); // Multiple concentric circles
          const layerRadius = radius * (0.4 + layers * 0.2);
          particle.targetX = centerX + Math.cos(angle) * layerRadius + randomOffset();
          particle.targetY = centerY + Math.sin(angle) * layerRadius + randomOffset();
          break;
          
        case 'cube':
          // Form a 3D-looking cube wireframe
          const face = Math.floor(i / (this.particles.length / 6));
          const progress = (i % (this.particles.length / 6)) / (this.particles.length / 6);
          const cubeSize = radius * 1.2;
          
          if (face === 0) { // Front face
            particle.targetX = centerX + (progress - 0.5) * cubeSize;
            particle.targetY = centerY + (Math.sin(progress * Math.PI * 2) * 0.5) * cubeSize;
          } else if (face === 1) { // Back face (smaller perspective)
            particle.targetX = centerX + (progress - 0.5) * cubeSize * 0.6;
            particle.targetY = centerY + (Math.sin(progress * Math.PI * 2) * 0.3) * cubeSize;
          } else { // Connecting edges
            const edgeProgress = progress * 2 - 1;
            particle.targetX = centerX + edgeProgress * cubeSize * 0.8;
            particle.targetY = centerY + Math.sin(edgeProgress * Math.PI) * cubeSize * 0.6;
          }
          particle.targetX += randomOffset();
          particle.targetY += randomOffset();
          break;
          
        case 'torus':
          const torusAngle = (i / this.particles.length) * Math.PI * 4;
          const ringRadius = radius * 0.8;
          const tubeRadius = radius * 0.3;
          const tubeAngle = (i / this.particles.length) * Math.PI * 8;
          
          particle.targetX = centerX + (ringRadius + Math.cos(tubeAngle) * tubeRadius) * Math.cos(torusAngle);
          particle.targetY = centerY + (ringRadius + Math.cos(tubeAngle) * tubeRadius) * Math.sin(torusAngle);
          break;
          
        case 'helix':
          const helixAngle = (i / this.particles.length) * Math.PI * 6;
          const helixRadius = radius * (0.4 + Math.sin(helixAngle * 0.5) * 0.3);
          const helixHeight = this.height * 0.8;
          particle.targetX = centerX + Math.cos(helixAngle) * helixRadius + randomOffset();
          particle.targetY = centerY - helixHeight/2 + (i / this.particles.length) * helixHeight;
          break;
          
        case 'wave':
          const waveX = (i / this.particles.length) * this.width;
          const waveFreq = 3;
          const waveAmp = radius * 0.6;
          particle.targetX = waveX;
          particle.targetY = centerY + Math.sin(waveX * waveFreq / this.width * Math.PI * 2) * waveAmp;
          break;
          
        case 'spiral':
          const spiralAngle = (i / this.particles.length) * Math.PI * 8;
          const spiralRadius = (i / this.particles.length) * radius;
          particle.targetX = centerX + Math.cos(spiralAngle) * spiralRadius;
          particle.targetY = centerY + Math.sin(spiralAngle) * spiralRadius;
          break;
          
        case 'whirlpool':
          // Bottom-centered lively whirlpool effect
          const whirlCenterX = centerX;
          const whirlCenterY = this.height * 0.75; // Bottom center
          const whirlAngle = (i / this.particles.length) * Math.PI * 6 + Date.now() * 0.001; // Rotating
          const whirlRadius = radius * (0.3 + Math.sin(whirlAngle * 0.5) * 0.4);
          const whirlHeight = Math.sin(whirlAngle * 2) * 50; // Vertical motion
          
          particle.targetX = whirlCenterX + Math.cos(whirlAngle) * whirlRadius + randomOffset();
          particle.targetY = whirlCenterY + Math.sin(whirlAngle) * whirlRadius * 0.5 + whirlHeight;
          break;
          
        case 'scatter':
        default:
          particle.targetX = Math.random() * this.width;
          particle.targetY = Math.random() * this.height;
          break;
      }
    });
  }

  setState(newState) {
    if (this.state === newState) return;
    
    this.state = newState;
    
    // Map Clever's thought process/intent to formation
    switch (newState) {
      case 'idle':
        // Clever's idol: angled whirlpool as default idle state
        this.morphToFormation('whirlpool');
        break;
      case 'summon':
        this.morphToFormation('sphere');
        break;
      case 'dialogue':
        if (window.cleverIntent === 'shape_request' || window.cleverIntent === 'cube') {
          this.morphToFormation('cube');
        } else if (window.cleverIntent === 'creative') {
          this.morphToFormation('torus');
        } else if (window.cleverIntent === 'deep') {
          this.morphToFormation('cube');
        } else if (window.cleverIntent === 'galaxy') {
          this.morphToFormation('spiral');
        } else {
          this.morphToFormation('helix');
        }
        break;
      case 'dissolve':
        this.morphToFormation('scatter');
        break;
    }
  }

  update() {
    this.particles.forEach(particle => {
      // Move towards target formation
      const dx = particle.targetX - particle.x;
      const dy = particle.targetY - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance > 1) {
        particle.vx += dx * (particle.speed * 0.08); // Minimum formation movement
        particle.vy += dy * (particle.speed * 0.08);
      }
      
      // Mouse interaction - subtle attraction
      if (this.mouse) {
        const mouseDx = this.mouse.x - particle.x;
        const mouseDy = this.mouse.y - particle.y;
        const mouseDistance = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
        
        if (mouseDistance < 150) {
          const attraction = (150 - mouseDistance) / 150 * 0.0002; // Minimum mouse attraction
          particle.vx += mouseDx * attraction;
          particle.vy += mouseDy * attraction;
          
          // Increase energy when near mouse
          particle.energy = Math.min(1, particle.energy + 0.001); // Minimum energy change
        } else {
          // Decrease energy when away from mouse
          particle.energy = Math.max(0.08, particle.energy - 0.0005);
        }
      }
      
      // Apply velocity with damping
  particle.vx *= 0.995; // Maximum damping
  particle.vy *= 0.995;
      
  particle.x += particle.vx;
  particle.y += particle.vy;
      
  // Update phase for pulsing (minimum)
  particle.phase += 0.0015 + particle.energy * 0.002;
      
  // Update hue slightly for color shifting (slower)
  particle.hue += 0.04;
  if (particle.hue > 220) particle.hue = 160;
      
      // Wrap around screen edges
      if (particle.x < 0) particle.x = this.width;
      if (particle.x > this.width) particle.x = 0;
      if (particle.y < 0) particle.y = this.height;
      if (particle.y > this.height) particle.y = 0;
    });
  }

  draw() {
  // Clear canvas each frame to prevent pixel trails
  this.ctx.clearRect(0, 0, this.width, this.height);
  // Minimal debug info for performance
  // ...existing code...
    
  // Accessibility overlay
  if (this.accessibilityEnabled) {
    this.ctx.save();
    this.ctx.globalAlpha = 1.0;
    this.ctx.fillStyle = '#000';
    this.ctx.fillRect(0, 0, this.width, 40);
    this.ctx.font = 'bold 18px Arial';
    this.ctx.fillStyle = '#fff';
    this.ctx.fillText('Accessibility Mode: High Contrast', 10, 30);
    this.ctx.restore();
  }
    
  // Debug overlay
  if (this.debugOverlayEnabled) {
    this.ctx.save();
    this.ctx.globalAlpha = 0.95;
    this.ctx.fillStyle = 'rgba(0,0,0,0.7)';
    this.ctx.fillRect(0, this.height - 80, this.width, 80);
    this.ctx.font = 'bold 16px Arial';
    this.ctx.fillStyle = '#39ff14';
    this.ctx.fillText(`Particles: ${this.particles.length} | Formation: ${this.targetFormation || 'whirlpool'}`, 20, this.height - 55);
    this.ctx.fillText(`State: ${this.state} | Canvas: ${this.width}x${this.height}`, 20, this.height - 35);
    this.ctx.fillText(`DevicePixelRatio: ${this.dpr}`, 20, this.height - 15);
    this.ctx.restore();
  }
    
  this.particles.forEach(particle => {
  // Render as simple pixel for performance
  this.ctx.save();
  this.ctx.globalAlpha = 1.0;
  this.ctx.fillStyle = '#69EACB'; // Neon teal pixel
  this.ctx.fillRect(Math.round(particle.x), Math.round(particle.y), 2, 2);
  this.ctx.restore();
  });
    
    // Draw much brighter connections
    this.drawConnections();
  }

  drawConnections() {
    const maxDistance = 100;
    
    this.ctx.save();
    this.ctx.strokeStyle = 'rgba(105, 234, 203, 0.8)'; // Much brighter connections
    this.ctx.lineWidth = 3; // Even thicker lines
    this.ctx.globalAlpha = 1.0;
    
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];
        
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < maxDistance) {
          const alpha = (1 - distance / maxDistance) * 0.9; // Maximum visibility
          
          this.ctx.globalAlpha = alpha;
          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();
        }
      }
    }
    this.ctx.restore();
  }

  animate() {
    // Standard animation loop: update simulation, render frame, schedule next frame
    this.update();
    this.draw();
    requestAnimationFrame(() => this.animate());
  }

  // Move manifestCard and public methods outside animate()
  manifestCard(opts) {
    const { x, y, w, h, color = '#69EACB', onComplete } = opts;
    // Pick 40 particles closest to card center
    const centerX = x + w / 2;
    const centerY = y + h / 2;
    const manifestParticles = this.particles
      .map(p => ({ p, dist: Math.hypot(p.x - centerX, p.y - centerY) }))
      .sort((a, b) => a.dist - b.dist)
      .slice(0, 40)
      .map(obj => obj.p);

    // Animate them to card bounds
    manifestParticles.forEach((p, i) => {
      p.targetX = x + (i % 8) * (w / 8) + Math.random() * 8;
      p.targetY = y + Math.floor(i / 8) * (h / 5) + Math.random() * 8;
      p.size = 8 + Math.random() * 4;
      p.alpha = 1;
      p.hue = 170 + Math.random() * 40;
      p.manifesting = true;
    });

    // Fade out and trigger callback after animation
    let frame = 0;
    const animateManifest = () => {
      frame++;
      manifestParticles.forEach(p => {
        // Move toward target
        p.x += (p.targetX - p.x) * 0.18;
        p.y += (p.targetY - p.y) * 0.18;
        // Fade out
        if (frame > 18) p.alpha -= 0.07;
      });
      this.draw();
      if (frame < 28) {
        requestAnimationFrame(animateManifest);
      } else {
        manifestParticles.forEach(p => { p.manifesting = false; p.alpha = 0.7; p.size = 4; });
        if (typeof onComplete === 'function') onComplete();
      }
    };
    animateManifest();
  }

  // Public methods for external control
  triggerPulse(intensity = 1) {
    this.particles.forEach(particle => {
      particle.vx += (Math.random() - 0.5) * intensity;
      particle.vy += (Math.random() - 0.5) * intensity;
    });
  }

  summon() {
    this.setState('summon');
  }

  // Adaptive particle count based on device performance
  getAdaptiveParticleCount() {
    // Use hardware concurrency and memory as hints (feature-detected)
    const cores = navigator.hardwareConcurrency || 2;
    const navAny = /** @type {any} */ (navigator);
    const mem = typeof navAny.deviceMemory === 'number' ? navAny.deviceMemory : 4;
  // Mobile: fewer particles
  if (/Mobi|Android/i.test(navigator.userAgent)) return 60;
  // Low-end: fewer particles
  if (cores <= 2 || mem < 3) return 80;
  // Mid-range: moderate
  if (cores <= 4 || mem < 6) return 120;
  // High-end: max
  return 180;
  }

  // Accessibility controls
  addAccessibilityControls() {
    // Add a toggle button to the DOM
    const btn = document.createElement('button');
    btn.textContent = 'Toggle Accessibility';
    btn.style.position = 'absolute';
    btn.style.top = '10px';
    btn.style.right = '10px';
  btn.style.zIndex = "1000";
    btn.style.background = '#222';
    btn.style.color = '#fff';
    btn.style.border = '2px solid #39ff14';
    btn.style.padding = '8px 16px';
    btn.style.fontSize = '16px';
    btn.style.borderRadius = '6px';
    btn.style.cursor = 'pointer';
    btn.setAttribute('aria-label', 'Toggle high contrast accessibility mode');
    btn.onclick = () => {
      this.accessibilityEnabled = !this.accessibilityEnabled;
    };
    document.body.appendChild(btn);
  }

  // Debug overlay toggle
  addDebugToggle() {
    const btn = document.createElement('button');
    btn.textContent = 'Toggle Debug Overlay';
    btn.style.position = 'absolute';
    btn.style.top = '50px';
    btn.style.right = '10px';
  btn.style.zIndex = "1000";
    btn.style.background = '#222';
    btn.style.color = '#39ff14';
    btn.style.border = '2px solid #fff';
    btn.style.padding = '8px 16px';
    btn.style.fontSize = '16px';
    btn.style.borderRadius = '6px';
    btn.style.cursor = 'pointer';
    btn.setAttribute('aria-label', 'Toggle debug performance overlay');
    btn.onclick = () => {
      this.debugOverlayEnabled = !this.debugOverlayEnabled;
    };
    document.body.appendChild(btn);
  }
  dialogue() {
    this.setState('dialogue');
  }

  dissolve() {
    this.setState('dissolve');
  }

  idle() {
    this.setState('idle');
  }
}

// Global functions for compatibility with main.js
window.HolographicChamber = HolographicChamber;

window.startHolographicChamber = function(canvas) {
  if (!window.holographicChamber) {
    window.holographicChamber = new HolographicChamber(canvas);
  }
  return window.holographicChamber;
};

window.triggerPulse = function(intensity) {
  if (window.holographicChamber) {
    window.holographicChamber.triggerPulse(intensity);
  }
};

// Note: Auto-initialization removed to prevent conflicts with main.js
// The chamber is initialized by main.js using window.startHolographicChamber()
console.log('🔧 Holographic chamber loaded, waiting for main.js initialization...');

// Debug: Check if functions are exported
console.log('🎯 startHolographicChamber type:', typeof window.startHolographicChamber);
console.log('🎯 HolographicChamber type:', typeof window.HolographicChamber);

// Update debug display if available
setTimeout(() => {
  const debugDiv = document.getElementById('debug-info');
  if (debugDiv) {
    debugDiv.innerHTML = 'Holographic chamber JS loaded!<br/>Functions exported: ' + 
                        (typeof window.startHolographicChamber === 'function' ? 'YES' : 'NO');
  }
}, 100);
