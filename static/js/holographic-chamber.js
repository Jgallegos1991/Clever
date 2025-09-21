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
    // Initialize holographic chamber (quiet mode; no on-screen debug)
    this.resize();
    this.createParticles();
    
    // Add mouse interaction
    this.mouse = { x: this.width / 2, y: this.height / 2 };
    this.addMouseInteraction();
    // Keep UI clean: no accessibility/debug toggle buttons by default
    this.accessibilityEnabled = false;
    this.debugOverlayEnabled = false;
    
  // Always start with whirlpool formation for idle
  this.morphToFormation('whirlpool');
    
  this.animate();
    
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
      // 3D projection helper
      function project3D(x, y, z, camera) {
        // Simple perspective projection
        const scale = camera / (camera - z);
        return {
          x: centerX + x * scale,
          y: centerY + y * scale
        };
      }
      const camera = radius * 2.5;
      switch (formation) {
        case 'sphere': {
          // Spherical coordinates
          const phi = Math.acos(1 - 2 * (i + 1) / this.particles.length);
          const theta = Math.PI * (1 + Math.sqrt(5)) * (i + 1);
          const r = radius * 0.8;
          const x = r * Math.sin(phi) * Math.cos(theta);
          const y = r * Math.sin(phi) * Math.sin(theta);
          const z = r * Math.cos(phi);
          const p = project3D(x, y, z, camera);
          particle.targetX = p.x + randomOffset();
          particle.targetY = p.y + randomOffset();
          break;
        }
        case 'cube': {
          // 3D cube vertices
          const cubeSize = radius * 1.2;
          const faces = 6;
          const vertsPerFace = Math.floor(this.particles.length / faces);
          const face = Math.floor(i / vertsPerFace);
          const idx = i % vertsPerFace;
          let x = 0, y = 0, z = 0;
          switch (face) {
            case 0: x = -cubeSize/2; y = -cubeSize/2 + idx * cubeSize / vertsPerFace; z = -cubeSize/2; break;
            case 1: x = cubeSize/2; y = -cubeSize/2 + idx * cubeSize / vertsPerFace; z = -cubeSize/2; break;
            case 2: x = -cubeSize/2 + idx * cubeSize / vertsPerFace; y = -cubeSize/2; z = -cubeSize/2; break;
            case 3: x = -cubeSize/2 + idx * cubeSize / vertsPerFace; y = cubeSize/2; z = -cubeSize/2; break;
            case 4: x = -cubeSize/2 + idx * cubeSize / vertsPerFace; y = -cubeSize/2; z = cubeSize/2; break;
            case 5: x = -cubeSize/2 + idx * cubeSize / vertsPerFace; y = cubeSize/2; z = cubeSize/2; break;
          }
          const p = project3D(x, y, z, camera);
          particle.targetX = p.x + randomOffset();
          particle.targetY = p.y + randomOffset();
          break;
        }
        case 'torus': {
          // 3D torus
          const r1 = radius * 0.7; // major radius
          const r2 = radius * 0.25; // minor radius
          const u = (i / this.particles.length) * Math.PI * 2;
          const v = ((i * 7) % this.particles.length) / this.particles.length * Math.PI * 2;
          const x = (r1 + r2 * Math.cos(v)) * Math.cos(u);
          const y = (r1 + r2 * Math.cos(v)) * Math.sin(u);
          const z = r2 * Math.sin(v);
          const p = project3D(x, y, z, camera);
          particle.targetX = p.x + randomOffset();
          particle.targetY = p.y + randomOffset();
          break;
        }
          
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
  // No on-canvas overlays in normal mode (keep stage clean)
    
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
    // Intentionally no-op to avoid adding toggle UI to the stage
    return;
  }

  // Debug overlay toggle
  addDebugToggle() {
    // Intentionally no-op to avoid adding toggle UI to the stage
    return;
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
// Quiet load: no console logs or UI updates; main.js will initialize when ready.
