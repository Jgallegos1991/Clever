/**
 * 🌌 CLEVER QUANTUM SCENE - Simplified Working Version 🌌
 */

(function(){
  console.log('🌌 Quantum Scene: Starting simplified version...');
  
  function initScene() {
    console.log('🔍 initScene called');
    const canvas = document.getElementById('scene');
    if(!canvas) {
      console.warn('Canvas not found, retrying...');
      return setTimeout(initScene, 50);
    }
    console.log('✅ Canvas found:', canvas);
    
    const ctx = canvas.getContext('2d');
    console.log('✅ Context created:', ctx);
    
    // Resize canvas to full screen
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      console.log('📐 Canvas resized to:', canvas.width, 'x', canvas.height);
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Simple particle system state
    let t = 0;
    let energy = 0.8;
    let targetShape = 'swarm';
    
    // Create 1000 particles
    const points = [];
    for(let i = 0; i < 1000; i++) {
      points.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        tx: Math.random() * canvas.width,
        ty: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        phase: Math.random() * Math.PI * 2,
        size: 1 + Math.random() * 2,
        hue: 180 + Math.random() * 60
      });
    }
    
    console.log('⚛️ Created', points.length, 'particles');
    
    // Shape generators
    function generateSwarm() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.7;
      
      points.forEach((p, i) => {
        const angle = (i / points.length) * Math.PI * 2 + t * 0.001;
        const radius = 150 + Math.sin(i * 0.1 + t * 0.003) * 80;
        
        p.tx = centerX + Math.cos(angle) * radius + Math.sin(i + t * 0.002) * 40;
        p.ty = centerY + Math.sin(angle) * radius * 0.6 + Math.cos(i + t * 0.002) * 20;
      });
    }
    
    function generateCube() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.7;
      const size = 120;
      
      points.forEach((p, i) => {
        const face = i % 6;
        const u = (Math.random() - 0.5) * size;
        const v = (Math.random() - 0.5) * size;
        
        // Add perfect cube corners energy ✨
        const cornerMagic = Math.sin(t * 0.05) * 15;
        
        switch(face) {
          case 0: p.tx = centerX + size/2 + cornerMagic; p.ty = centerY + u; break;
          case 1: p.tx = centerX - size/2 - cornerMagic; p.ty = centerY + u; break;
          case 2: p.tx = centerX + u; p.ty = centerY + size/2 + cornerMagic; break;
          case 3: p.tx = centerX + u; p.ty = centerY - size/2 - cornerMagic; break;
          case 4: p.tx = centerX + u + cornerMagic; p.ty = centerY + v; break;
          case 5: p.tx = centerX + u - cornerMagic; p.ty = centerY + v; break;
        }
      });
    }
    
    function generateCone() {
      const centerX = canvas.width / 2;
      const centerY = canvas.height * 0.7;
      const baseRadius = 100;
      const height = 140;
      
      points.forEach((p, i) => {
        const progress = i / points.length;
        const level = Math.floor(progress * 8) / 8; // 8 levels
        const radius = baseRadius * (1 - level);
        const angle = (i * 137.508) % (Math.PI * 2); // Golden angle distribution
        
        p.tx = centerX + Math.cos(angle) * radius;
        p.ty = centerY + level * height - height/2;
      });
    }
    
    // Animation loop
    function animate() {
      t++;
      
      // Clear with fade
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Generate target positions
      if (targetShape === 'cube') {
        generateCube();
      } else if (targetShape === 'cone') {
        generateCone();
      } else {
        generateSwarm();
      }
      
      // Update and draw particles
      points.forEach((p, i) => {
        // Move towards target
        p.x += (p.tx - p.x) * 0.02;
        p.y += (p.ty - p.y) * 0.02;
        
        // Add organic motion
        p.x += Math.sin(p.phase + t * 0.01) * 1.5;
        p.y += Math.cos(p.phase + t * 0.01) * 1.5;
        p.phase += 0.005;
        
        // Draw particle with glow
        const alpha = 0.8 + Math.sin(i + t * 0.02) * 0.3;
        const size = p.size * (0.8 + energy * 0.4);
        
        ctx.beginPath();
        ctx.arc(p.x, p.y, size * 2, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue}, 70%, 60%, 0.3)`;
        ctx.shadowBlur = 15;
        ctx.shadowColor = `hsl(${p.hue}, 70%, 60%)`;
        ctx.fill();
        
        // Core
        ctx.beginPath();
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue}, 70%, 80%, ${alpha})`;
        ctx.shadowBlur = 0;
        ctx.fill();
      });
      
      // Energy decay
      energy = Math.max(0.3, energy * 0.99);
      
      requestAnimationFrame(animate);
    }
    
    // App.js compatibility functions
    window.__orbPulse = function(intensity) {
      energy = Math.min(1.2, energy + (intensity || 0.25));
      console.log('🔮 Pulse:', intensity);
    };
    
    window.__orbThinking = function(active) {
      if (active) energy += 0.2;
      console.log('🧠 Thinking:', active);
    };
    
    window.__sceneSetShape = function(shape) {
      targetShape = shape || 'swarm';
      energy += 0.4;
      console.log('🔄 Shape:', shape);
    };
    
    window.__sceneMorphForDialogue = function(meta) {
      const m = meta || {};
      const shape = m.shape || 'cube';
      window.__sceneSetShape(shape);
    };
    
    window.__sceneParticles = function() {
      return points;
    };
    
    // Missing functions that app.js expects
    window.__sceneSetParticleLevel = function(level) {
      const newCount = Math.floor(1000 * Math.max(0.5, Math.min(2.0, level)));
      console.log('⚛️ Particle level:', level, '→', newCount);
      // Don't actually change count in simplified version, just log
    };
    
    window.__sceneSetParticleBrightness = function(brightness) {
      console.log('💡 Particle brightness:', brightness);
      // Apply brightness to energy for visual effect
      energy = Math.min(1.2, energy + brightness * 0.2);
    };
    
    window.__orbSetMood = function(mood) {
      console.log('🎭 Mood:', mood);
      // Apply mood to hue variation
      points.forEach(p => {
        p.hue = 180 + mood * 40 + Math.random() * 20;
      });
    };

    window.__orbSetMode = function(mode) {
      console.log('🔄 Mode:', mode);
      // Mode switching - could affect particle behavior
      if (mode === 'Deep Dive') {
        energy = Math.max(0.1, energy - 0.1); // Calmer for deep thinking
      } else if (mode === 'Quick Hit') {
        energy = Math.min(1.0, energy + 0.2); // More energetic
      }
    };
    
    window.__sceneSpeakText = function(text) {
      console.log('💬 Speaking:', text);
      // Pulse energy when speaking
      energy += 0.3;
    };
    
    console.log('🚀 Starting simplified animation...');
    animate();
    
    console.log('🌌 Simplified quantum scene initialized');
    console.log('🔗 Compatibility functions loaded');
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScene);
  } else {
    initScene();
  }
})();
