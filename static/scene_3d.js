// Clever's 3D Shape-Forming Particle System
(function(){
  function initScene() {
    const canvas = document.getElementById('scene');
    if(!canvas) {
      console.warn('Canvas not found, retrying...');
      return setTimeout(initScene, 100);
    }
    
    const ctx = canvas.getContext('2d');
    
    // Resize canvas to full screen
    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    // 3D System State
    let time = 0;
    let energy = 0.8;
    let currentShape = 'swarm';
    let thinking = false;
    
    // Visual settings
    const settings = {
      particleCount: 1200,
      rotationSpeed: 0.01,
      morphSpeed: 0.05,
      particleSize: 3,
      glowSize: 15,
      colors: ['#00e6ff', '#38f0c8', '#69EACB'],
      brightness: 1.5
    };

    // 3D Camera
    const camera = { x: 0, y: 0, z: -300, rotX: 0, rotY: 0 };

    // Create particles with 3D coordinates
    const particles = Array.from({ length: settings.particleCount }, (_, i) => ({
      id: i,
      x: (Math.random() - 0.5) * 200,
      y: (Math.random() - 0.5) * 200,
      z: (Math.random() - 0.5) * 200,
      targetX: 0,
      targetY: 0,
      targetZ: 0,
      size: 1 + Math.random() * 2,
      phase: Math.random() * Math.PI * 2,
      speed: 0.02 + Math.random() * 0.03
    }));

    console.log(`Clever 3D: ${particles.length} particles initialized`);

    // 3D Projection
    function project(x, y, z) {
      // Apply camera rotation
      const cosX = Math.cos(camera.rotX);
      const sinX = Math.sin(camera.rotX);
      const cosY = Math.cos(camera.rotY);
      const sinY = Math.sin(camera.rotY);
      
      // Rotate around Y axis (horizontal)
      const rotatedX = cosY * x - sinY * z;
      const rotatedZ = sinY * x + cosY * z;
      
      // Rotate around X axis (vertical)
      const finalY = cosX * y - sinX * rotatedZ;
      const finalZ = sinX * y + cosX * rotatedZ + camera.z;
      
      // Perspective projection
      if (finalZ >= -10) return null;
      
      const perspective = 400 / -finalZ;
      return {
        x: canvas.width/2 + rotatedX * perspective,
        y: canvas.height/2 + finalY * perspective,
        size: perspective,
        depth: -finalZ
      };
    }

    // 3D Shape Generators
    function generateSphere(radius = 80) {
      const phi = Math.PI * (3 - Math.sqrt(5)); // Golden angle
      particles.forEach((p, i) => {
        const y = 1 - (i / (particles.length - 1)) * 2;
        const radiusAtY = Math.sqrt(1 - y * y) * radius;
        const theta = phi * i;
        
        p.targetX = Math.cos(theta) * radiusAtY;
        p.targetY = y * radius;
        p.targetZ = Math.sin(theta) * radiusAtY;
      });
    }

    function generateCube(size = 70) {
      const half = size / 2;
      particles.forEach((p, i) => {
        const face = i % 6;
        const u = (Math.random() - 0.5) * size;
        const v = (Math.random() - 0.5) * size;
        
        switch(face) {
          case 0: p.targetX = half;  p.targetY = u; p.targetZ = v; break; // Right
          case 1: p.targetX = -half; p.targetY = u; p.targetZ = v; break; // Left
          case 2: p.targetX = u; p.targetY = half;  p.targetZ = v; break; // Top
          case 3: p.targetX = u; p.targetY = -half; p.targetZ = v; break; // Bottom
          case 4: p.targetX = u; p.targetY = v; p.targetZ = half;  break; // Front
          case 5: p.targetX = u; p.targetY = v; p.targetZ = -half; break; // Back
        }
      });
    }

    function generateTorus(majorR = 60, minorR = 20) {
      particles.forEach((p, i) => {
        const u = (i / particles.length) * Math.PI * 2;
        const v = ((i * 13) % particles.length / particles.length) * Math.PI * 2;
        
        p.targetX = (majorR + minorR * Math.cos(v)) * Math.cos(u);
        p.targetY = minorR * Math.sin(v);
        p.targetZ = (majorR + minorR * Math.cos(v)) * Math.sin(u);
      });
    }

    function generateHelix(radius = 50, height = 120, turns = 3) {
      particles.forEach((p, i) => {
        const t = (i / particles.length) * turns * Math.PI * 2;
        const y = (i / particles.length - 0.5) * height;
        
        p.targetX = radius * Math.cos(t);
        p.targetY = y;
        p.targetZ = radius * Math.sin(t);
      });
    }

    function generateWave() {
      const gridSize = Math.ceil(Math.sqrt(particles.length));
      particles.forEach((p, i) => {
        const x = (i % gridSize) / gridSize * 120 - 60;
        const z = Math.floor(i / gridSize) / gridSize * 120 - 60;
        const wave = Math.sin(x * 0.1 + time * 0.005) * Math.cos(z * 0.1 + time * 0.003);
        
        p.targetX = x;
        p.targetY = wave * 30;
        p.targetZ = z;
      });
    }

    function generateSwarm() {
      particles.forEach((p, i) => {
        const t = time * 0.001 + i * 0.1;
        const radius = 80 + Math.sin(t * 0.8) * 30;
        const theta = i * 2.4 + t * 0.6;
        const phi = Math.sin(i * 0.2 + t * 0.4) * Math.PI;
        
        p.targetX = radius * Math.sin(phi) * Math.cos(theta);
        p.targetY = radius * Math.sin(phi) * Math.sin(theta) * 0.8;
        p.targetZ = radius * Math.cos(phi);
      });
    }

    // Main animation loop
    function animate() {
      time += 16;
      
      // Clear canvas with slight trail for smooth motion
      ctx.fillStyle = 'rgba(11, 15, 20, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Smooth camera rotation
      camera.rotY += settings.rotationSpeed;
      camera.rotX = Math.sin(time * 0.001) * 0.2;
      
      // Generate shape targets
      switch(currentShape) {
        case 'sphere': generateSphere(); break;
        case 'cube': generateCube(); break;
        case 'torus': generateTorus(); break;
        case 'helix': generateHelix(); break;
        case 'wave': generateWave(); break;
        default: generateSwarm(); break;
      }
      
      // Update and render particles
      const visible = [];
      
      particles.forEach((p, i) => {
        // Move towards target position
        p.x += (p.targetX - p.x) * settings.morphSpeed;
        p.y += (p.targetY - p.y) * settings.morphSpeed;
        p.z += (p.targetZ - p.z) * settings.morphSpeed;
        
        // Add organic motion
        const jitter = energy * 2;
        p.x += Math.sin(p.phase + time * 0.003) * jitter;
        p.y += Math.cos(p.phase * 1.2 + time * 0.002) * jitter;
        p.z += Math.sin(p.phase * 0.9 + time * 0.004) * jitter * 0.5;
        
        p.phase += p.speed;
        
        // Project to 2D screen
        const projected = project(p.x, p.y, p.z);
        if (projected && projected.x > -50 && projected.x < canvas.width + 50 && 
            projected.y > -50 && projected.y < canvas.height + 50) {
          visible.push({ ...projected, particle: p, index: i });
        }
      });
      
      // Sort by depth for proper rendering
      visible.sort((a, b) => b.depth - a.depth);
      
      // Render particles with glow
      visible.forEach(({ x, y, size, particle, index }) => {
        const alpha = Math.min(1, size * 0.5) * settings.brightness;
        const particleSize = settings.particleSize * particle.size * size;
        const colorIndex = index % settings.colors.length;
        const color = settings.colors[colorIndex];
        
        if (alpha > 0.1 && particleSize > 0.5) {
          // Outer glow
          ctx.beginPath();
          ctx.arc(x, y, particleSize + settings.glowSize * size, 0, Math.PI * 2);
          ctx.fillStyle = color.replace(')', ', 0.2)').replace('rgb', 'rgba').replace('#', 'rgba(');
          if (color.startsWith('#')) {
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);
            ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha * 0.2})`;
          }
          ctx.fill();
          
          // Core particle
          ctx.beginPath();
          ctx.arc(x, y, particleSize, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
          ctx.fill();
        }
      });
      
      // Energy decay
      energy = Math.max(0.3, energy * 0.995);
      
      requestAnimationFrame(animate);
    }

    // Control functions
    function setShape(shape) {
      currentShape = shape;
      energy = Math.min(1.2, energy + 0.4);
      console.log(`Clever: Morphing to ${shape}`);
    }

    function pulse() {
      energy = Math.min(1.2, energy + 0.3);
    }

    // Global API for Clever integration
    window.__sceneSetShape = setShape;
    window.__orbPulse = pulse;
    window.__orbBrighten = pulse;
    window.__orbThinking = (active) => { thinking = active; };
    window.__orbSetMode = () => {}; // Compatibility
    window.__orbSetMood = () => {}; // Compatibility
    
    // Missing functions that app.js expects
    window.__sceneParticles = (cmd) => {
      if (cmd === 'more' || cmd === 'up') {
        settings.particleCount = Math.min(2000, settings.particleCount + 200);
        initializeParticles();
        pulse();
      } else if (cmd === 'less' || cmd === 'down') {
        settings.particleCount = Math.max(400, settings.particleCount - 200);
        initializeParticles();
      }
    };
    
    window.__sceneSetParticleLevel = (level) => {
      const l = Math.max(0.3, Math.min(2.0, level || 1.0));
      settings.particleCount = Math.floor(600 * l);
      initializeParticles();
      pulse();
    };
    
    window.__sceneSetParticleBrightness = (brightness) => {
      const b = Math.max(0.5, Math.min(2.0, brightness || 1.0));
      // Adjust visual brightness - could modify particle colors/glow
      energy = Math.min(1.2, energy * b);
    };
    
    window.__sceneSpeakText = (text, opts) => {
      // Visual effect for spoken text - pulse the particles
      pulse();
      // Could implement text-to-particle morphing here
      console.log('Clever speaking:', text);
    };
    
    window.__sceneMorphForDialogue = (meta) => {
      const m = meta || {};
      const shape = (m.shape || m.shape_to_form || '').toLowerCase();
      
      const shapeMap = {
        'cube': 'cube', 'box': 'cube', 'square': 'cube',
        'sphere': 'sphere', 'ball': 'sphere', 'circle': 'sphere', 
        'ring': 'torus', 'donut': 'torus', 'torus': 'torus',
        'spiral': 'helix', 'helix': 'helix', 'twist': 'helix',
        'wave': 'wave', 'ocean': 'wave'
      };
      
      const targetShape = shapeMap[shape] || 'sphere';
      setShape(targetShape);
      
      // Return to swarm after hold time
      setTimeout(() => setShape('swarm'), m.holdMs || 3000);
    };

    // Start with a pulse of energy
    energy = 0.8;
    animate();
    console.log('Clever 3D particle system ready! Try: __sceneSetShape("cube")');
  }
  
  // Initialize when ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScene);
  } else {
    initScene();
  }
})();
