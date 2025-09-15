// Minimal Working Particle System for Clever AI
console.log('🔧 Loading minimal particle system...');

class SimpleParticleSystem {
  constructor(canvas) {
    console.log('🎯 SimpleParticleSystem constructor called');
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.init();
  }

  init() {
    console.log('🎯 Initializing simple particles...');
    this.resize();
    this.createParticles();
    this.animate();
    console.log('✅ Simple particles started!');
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.canvas.style.width = window.innerWidth + 'px';
    this.canvas.style.height = window.innerHeight + 'px';
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < 20; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        size: Math.random() * 4 + 2
      });
    }
    console.log('🎯 Created ' + this.particles.length + ' simple particles');
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Draw particles
    this.ctx.fillStyle = '#00ff88';
    this.particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      
      // Bounce off walls
      if (p.x <= 0 || p.x >= this.canvas.width) p.vx *= -1;
      if (p.y <= 0 || p.y >= this.canvas.height) p.vy *= -1;
      
      // Draw particle
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fill();
    });
    
    requestAnimationFrame(() => this.animate());
  }
}

// Export functions
window.SimpleParticleSystem = SimpleParticleSystem;

window.startHolographicChamber = function(canvas) {
  console.log('🚀 startHolographicChamber called with canvas:', canvas);
  if (!window.simpleParticleSystem) {
    window.simpleParticleSystem = new SimpleParticleSystem(canvas);
  }
  return window.simpleParticleSystem;
};

console.log('🔧 Minimal particle system loaded successfully!');
console.log('🎯 startHolographicChamber available:', typeof window.startHolographicChamber);