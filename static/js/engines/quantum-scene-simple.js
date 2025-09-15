// Quantum Scene - Simple Particle Engine
// Optimized for Chromebook performance (45+ FPS)
// Simplified version of the advanced quantum particle system

class QuantumSceneSimple {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.mousePos = { x: 0, y: 0 };
    this.config = {
      particleCount: 80, // Reduced for performance
      connectionDistance: 100,
      speed: 0.3,
      size: { min: 1, max: 3 },
      alpha: { min: 0.3, max: 0.8 }
    };
    
    this.init();
  }

  init() {
    this.resize();
    this.createParticles();
    this.bindEvents();
    this.animate();
  }

  bindEvents() {
    window.addEventListener('resize', () => this.resize());
    
    // Track mouse for particle attraction
    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mousePos.x = e.clientX - rect.left;
      this.mousePos.y = e.clientY - rect.top;
    });
  }

  resize() {
    const rect = this.canvas.getBoundingClientRect();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    
    this.ctx.scale(dpr, dpr);
    this.canvas.style.width = rect.width + 'px';
    this.canvas.style.height = rect.height + 'px';
    
    this.width = rect.width;
    this.height = rect.height;
  }

  createParticles() {
    this.particles = [];
    
    for (let i = 0; i < this.config.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * this.config.speed,
        vy: (Math.random() - 0.5) * this.config.speed,
        size: Math.random() * (this.config.size.max - this.config.size.min) + this.config.size.min,
        alpha: Math.random() * (this.config.alpha.max - this.config.alpha.min) + this.config.alpha.min,
        hue: Math.random() * 60 + 160, // Teal to cyan
        phase: Math.random() * Math.PI * 2
      });
    }
  }

  update() {
    this.particles.forEach(particle => {
      // Update position
      particle.x += particle.vx;
      particle.y += particle.vy;
      
      // Bounce off walls
      if (particle.x <= 0 || particle.x >= this.width) particle.vx *= -1;
      if (particle.y <= 0 || particle.y >= this.height) particle.vy *= -1;
      
      // Keep particles in bounds
      particle.x = Math.max(0, Math.min(this.width, particle.x));
      particle.y = Math.max(0, Math.min(this.height, particle.y));
      
      // Mouse attraction (subtle)
      const dx = this.mousePos.x - particle.x;
      const dy = this.mousePos.y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < 150) {
        const force = (150 - distance) / 150 * 0.002;
        particle.vx += dx * force;
        particle.vy += dy * force;
      }
      
      // Update phase for pulsing effect
      particle.phase += 0.02;
    });
  }

  draw() {
    // Clear with trail effect
    this.ctx.fillStyle = 'rgba(11, 15, 20, 0.08)';
    this.ctx.fillRect(0, 0, this.width, this.height);
    
    // Draw connections first (behind particles)
    this.drawConnections();
    
    // Draw particles
    this.particles.forEach(particle => {
      const pulse = Math.sin(particle.phase) * 0.2 + 0.8;
      const finalAlpha = particle.alpha * pulse;
      
      // Particle glow
      this.ctx.save();
      this.ctx.globalAlpha = finalAlpha * 0.4;
      this.ctx.fillStyle = `hsl(${particle.hue}, 70%, 60%)`;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size * 2.5, 0, Math.PI * 2);
      this.ctx.fill();
      
      // Particle core
      this.ctx.globalAlpha = finalAlpha;
      this.ctx.fillStyle = `hsl(${particle.hue}, 80%, 70%)`;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    });
  }

  drawConnections() {
    const maxDistance = this.config.connectionDistance;
    
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];
        
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < maxDistance) {
          const alpha = (1 - distance / maxDistance) * 0.15;
          
          this.ctx.save();
          this.ctx.globalAlpha = alpha;
          this.ctx.strokeStyle = `hsl(${(p1.hue + p2.hue) / 2}, 60%, 65%)`;
          this.ctx.lineWidth = 0.5;
          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();
          this.ctx.restore();
        }
      }
    }
  }

  animate() {
    this.update();
    this.draw();
    requestAnimationFrame(() => this.animate());
  }

  // Public API for external control
  triggerPulse(intensity = 1) {
    this.particles.forEach(particle => {
      particle.vx += (Math.random() - 0.5) * intensity * 0.5;
      particle.vy += (Math.random() - 0.5) * intensity * 0.5;
    });
  }

  setSpeed(speed) {
    this.config.speed = speed;
  }

  setParticleCount(count) {
    this.config.particleCount = Math.max(20, Math.min(200, count));
    this.createParticles();
  }
}

// Export for use
window.QuantumSceneSimple = QuantumSceneSimple;