// Holographic Chamber - Advanced Particle System for Clever AI
// Quantum swarm with morphing behaviors: idle → summon → dialogue → dissolve

class HolographicChamber {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.state = 'idle'; // idle, summon, dialogue, dissolve
    this.targetFormation = null;
    
    // Performance settings optimized for Chromebook
    this.maxParticles = 150;
    this.dpr = Math.min(2, window.devicePixelRatio || 1);
    
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
    
    // Start with a formation cycle
    this.startFormationCycle();
    
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
    
    this.canvas.addEventListener('click', () => {
      this.triggerRandomFormation();
    });
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
    const rect = this.canvas.getBoundingClientRect();
    this.width = rect.width;
    this.height = rect.height;
    
    this.canvas.width = this.width * this.dpr;
    this.canvas.height = this.height * this.dpr;
    this.ctx.scale(this.dpr, this.dpr);
    
    this.canvas.style.width = this.width + 'px';
    this.canvas.style.height = this.height + 'px';
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.maxParticles; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2,
        targetX: Math.random() * this.width,
        targetY: Math.random() * this.height,
        size: Math.random() * 4 + 2, // Larger particles
        alpha: Math.random() * 0.4 + 0.6, // Brighter alpha
        hue: Math.random() * 60 + 160, // Teal to cyan range
        phase: Math.random() * Math.PI * 2,
        speed: 0.05 + Math.random() * 0.03, // Faster movement
        energy: Math.random() * 0.5 + 0.5 // Energy level for pulsing
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
    
    switch (newState) {
      case 'idle':
        this.morphToFormation('scatter');
        break;
      case 'summon':
        this.morphToFormation('sphere');
        break;
      case 'dialogue':
        this.morphToFormation('helix');
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
        particle.vx += dx * particle.speed;
        particle.vy += dy * particle.speed;
      }
      
      // Mouse interaction - subtle attraction
      if (this.mouse) {
        const mouseDx = this.mouse.x - particle.x;
        const mouseDy = this.mouse.y - particle.y;
        const mouseDistance = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
        
        if (mouseDistance < 150) {
          const attraction = (150 - mouseDistance) / 150 * 0.003;
          particle.vx += mouseDx * attraction;
          particle.vy += mouseDy * attraction;
          
          // Increase energy when near mouse
          particle.energy = Math.min(1, particle.energy + 0.02);
        } else {
          // Decrease energy when away from mouse
          particle.energy = Math.max(0.3, particle.energy - 0.01);
        }
      }
      
      // Apply velocity with damping
      particle.vx *= 0.92;
      particle.vy *= 0.92;
      
      particle.x += particle.vx;
      particle.y += particle.vy;
      
      // Update phase for pulsing (speed up when energized)
      particle.phase += 0.03 + particle.energy * 0.05;
      
      // Update hue slightly for color shifting
      particle.hue += 0.1;
      if (particle.hue > 220) particle.hue = 160;
      
      // Wrap around screen edges
      if (particle.x < 0) particle.x = this.width;
      if (particle.x > this.width) particle.x = 0;
      if (particle.y < 0) particle.y = this.height;
      if (particle.y > this.height) particle.y = 0;
    });
  }

  draw() {
  // Add debug info to confirm canvas is drawing
  this.ctx.fillStyle = 'rgba(105, 234, 203, 0.8)';
  this.ctx.font = '16px Arial';
  this.ctx.fillText(`✨ Particles: ${this.particles.length} | Formation: ${this.targetFormation || 'whirlpool'}`, 10, 25);

  // Add visible debug info
  this.ctx.font = 'bold 16px Arial';
  this.ctx.fillStyle = 'rgba(105, 234, 203, 1.0)'; // FULLY OPAQUE debug text
  this.ctx.fillText(`🌊 PARTICLES: ${this.particles.length} | STATE: ${this.state}`, 20, 50);
  this.ctx.fillText(`🎯 CANVAS: ${this.width}x${this.height}`, 20, 70);
    
    this.particles.forEach(particle => {
      const pulse = Math.sin(particle.phase) * 0.3 + 0.7; // Strong pulse
      const energyPulse = Math.sin(particle.phase * 2) * particle.energy;
      const finalAlpha = 1.0; // MAXIMUM ALPHA - no transparency!
      const finalSize = Math.max(8, particle.size * (1.5 + energyPulse * 0.8)); // Guaranteed large size
      
      // MEGA OUTER GLOW (impossible to miss)
      this.ctx.save();
      this.ctx.globalAlpha = 0.8; // Very visible
      this.ctx.fillStyle = `hsl(${particle.hue}, 100%, 60%)`; // Brighter
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, finalSize * 8, 0, Math.PI * 2);
      this.ctx.fill();
      
      // LARGE MIDDLE GLOW
      this.ctx.globalAlpha = 0.9;
      this.ctx.fillStyle = `hsl(${particle.hue}, 100%, 75%)`;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, finalSize * 4, 0, Math.PI * 2);
      this.ctx.fill();
      
      // PARTICLE CORE (BRILLIANT WHITE CENTER)
      this.ctx.globalAlpha = 1.0; // Full opacity
      this.ctx.fillStyle = 'white'; // Pure white, no HSL
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, finalSize * 2, 0, Math.PI * 2);
      this.ctx.fill();
      
      // Extra bright center dot
      this.ctx.fillStyle = 'cyan';
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, finalSize * 0.8, 0, Math.PI * 2);
      this.ctx.fill();
      
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
    this.update();
    this.draw();
    requestAnimationFrame(() => this.animate());
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
