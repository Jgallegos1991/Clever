/**
 * 🌌 CLEVER QUANTUM SCENE - Einstein Edition 🌌
 * "The most beautiful thing we can experience is the mysterious" - Einstein
 */

(function(){
  console.log('🌌 Quantum Scene: Loading Einstein-optimized particle system...');
  
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

    // Initialize Einstein Engine
    let physics = null;
    let geometry = null;
    let optimizer = null;
    let constants = null;
    
    if (window.CleverEinsteinEngine) {
      physics = window.CleverEinsteinEngine.physics;
      geometry = window.CleverEinsteinEngine.geometry;
      optimizer = window.CleverEinsteinEngine.optimizer;
      constants = window.CleverEinsteinEngine.constants;
      console.log('⚛️ Quantum physics engine: ONLINE');
    } else {
      console.warn('⚠️ Einstein Engine not loaded, using classical physics');
    }

    // Canvas setup with quantum precision
    function fit(){ 
      canvas.width = window.innerWidth; 
      canvas.height = window.innerHeight; 
    }
    window.addEventListener('resize', fit, {passive:true});
    fit();

    // Quantum particle system state
    let t = 0;
    let energy = 0.25;
    let mood = 0; // Emotional quantum state
    let targetShape = 'swarm';
    let morphBusy = false;
    
    // Einstein-inspired style parameters
    const style = { 
      jitter: 1.0, 
      rotationSpeed: 0.002,
      colorA: '#00e6ff', 
      colorB: '#38f0c8', 
      brightness: 1.2,
      particleSize: 2.0,
      glowRadius: 6,
      quantumUncertainty: 0.1
    };
    
    // Relativistic camera system
    const camera = {
      x: 0, y: 0, z: -400,
      rotX: 0, rotY: 0, rotZ: 0,
      fov: 800,
      velocity: { x: 0, y: 0, z: 0 }
    };
    
    // Quantum performance monitor
    const perf = {
      mode: 'einstein', // Special mode for quantum optimization
      lastNow: performance.now(),
      frames: 0,
      stride: 1,
      glowScale: 1.0,
      targetFPS: 60,
      quantumFluctuation: 0,
      relativisticFactor: 1
    };
    
    // Quantum state variables for app.js compatibility
    let thinking = { active: false };
    let morphing = { active: false, shape: 'swarm', progress: 0 };
    let particles = []; // Reference to points array
    
    // Vortex system for dynamic shape formation
    let vortex = {
      active: false,
      centerX: 0,
      centerY: 0, 
      centerZ: 0,
      strength: 0,
      radius: 150,
      rotationSpeed: 0.05,
      phase: 0,
      targetStrength: 0,
      decayRate: 0.95,
      spiralTightness: 0.3,
      verticalPull: 0.1
    };
    
    // Initialize particle field with golden ratio distribution
    let particleCount = 1800;
    let points = [];
    
    function initializeParticles() {
      points = [];
      for (let i = 0; i < particleCount; i++) {
        let pos;
        if (geometry) {
          // Use golden ratio sphere distribution for perfect harmony
          pos = geometry.goldenRatioSphere(i, particleCount, 200);
        } else {
          // Fallback to random distribution
          pos = {
            x: (Math.random() - 0.5) * 400,
            y: (Math.random() - 0.5) * 400,
            z: (Math.random() - 0.5) * 400
          };
        }
        
        points.push({
          // Current position in spacetime
          x: pos.x, y: pos.y, z: pos.z,
          // Target position for morphing
          tx: pos.x, ty: pos.y, tz: pos.z,
          // Screen coordinates
          sx: 0, sy: 0, depth: 0, scale: 1,
          // Quantum properties
          phase: Math.random() * constants?.TAU || Math.PI * 2,
          frequency: 0.02 + Math.random() * 0.03,
          amplitude: 1.0 + Math.random() * 0.5,
          mass: 1.0,
          charge: Math.random() > 0.5 ? 1 : -1,
          spin: Math.random() * 2 - 1,
          // Einstein special properties
          restMass: 1.0,
          momentum: { x: 0, y: 0, z: 0 },
          field: Math.random()
        });
      }
      console.log(`⚛️ Quantum field initialized: ${particleCount} particles`);
    }
    
    // Quantum 3D projection with relativistic effects
    function project3D(x, y, z) {
      // Apply spacetime curvature if physics engine available
      if (physics) {
        const warped = physics.warpSpacetime(x, y, z, energy);
        x = warped.x; y = warped.y; z = warped.z;
      }
      
      // Standard 3D projection with relativistic corrections
      const cosY = Math.cos(camera.rotY);
      const sinY = Math.sin(camera.rotY);
      const rotX = cosY * x - sinY * z;
      const rotZ = sinY * x + cosY * z;
      
      const cosX = Math.cos(camera.rotX);
      const sinX = Math.sin(camera.rotX);
      const finalY = cosX * y - sinX * rotZ;
      const finalZ = sinX * y + cosX * rotZ + camera.z;
      
      if (finalZ > -50) return null; // Behind camera
      
      // Apply time dilation effects
      let timeDilation = 1;
      if (window.CleverEinsteinEngine) {
        const velocity = Math.sqrt(camera.velocity.x * camera.velocity.x + camera.velocity.y * camera.velocity.y + camera.velocity.z * camera.velocity.z);
        timeDilation = window.CleverEinsteinEngine.relativisticTime(velocity, 10);
      }
      
      const scale = (camera.fov / -finalZ) * timeDilation;
      return {
        x: canvas.width/2 + rotX * scale,
        y: canvas.height/2 + finalY * scale,
        z: finalZ,
        scale: scale,
        timeDilation: timeDilation
      };
    }
    
    // Quantum shape generators using sacred geometry
    function generateQuantumSphere(radius = 150) {
      points.forEach((p, i) => {
        if (geometry) {
          const pos = geometry.goldenRatioSphere(i, points.length, radius);
          p.tx = pos.x; p.ty = pos.y; p.tz = pos.z;
        } else {
          // Fibonacci sphere fallback
          const phi = Math.acos(1 - 2 * (i + 0.5) / points.length);
          const theta = Math.PI * (1 + Math.sqrt(5)) * i;
          p.tx = radius * Math.sin(phi) * Math.cos(theta);
          p.ty = radius * Math.sin(phi) * Math.sin(theta);
          p.tz = radius * Math.cos(phi);
        }
      });
    }
    
    function generateQuantumCube(size = 120) {
      const half = size / 2;
      points.forEach((p, i) => {
        const face = i % 6;
        const u = (i / 6) % 1;
        const v = Math.floor(i / (6 * points.length)) % 1;
        
        switch(face) {
          case 0: p.tx = -half; p.ty = (u-0.5)*size; p.tz = (v-0.5)*size; break;
          case 1: p.tx = half; p.ty = (u-0.5)*size; p.tz = (v-0.5)*size; break;
          case 2: p.tx = (u-0.5)*size; p.ty = -half; p.tz = (v-0.5)*size; break;
          case 3: p.tx = (u-0.5)*size; p.ty = half; p.tz = (v-0.5)*size; break;
          case 4: p.tx = (u-0.5)*size; p.ty = (v-0.5)*size; p.tz = -half; break;
          case 5: p.tx = (u-0.5)*size; p.ty = (v-0.5)*size; p.tz = half; break;
        }
      });
    }
    
    function generateSwarm() {
      const cx = 0, cy = 0, cz = 0;
      points.forEach(p => {
        const angle = Math.random() * constants?.TAU || Math.PI * 2;
        const radius = 50 + Math.random() * 150;
        const height = (Math.random() - 0.5) * 200;
        
        p.tx = cx + Math.cos(angle) * radius;
        p.ty = cy + height;
        p.tz = cz + Math.sin(angle) * radius;
      });
    }
    
    // Background with quantum field visualization
    function drawQuantumBackground() {
      const alpha = 0.12;
      ctx.fillStyle = `rgba(0,0,0,${alpha})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Add quantum field fluctuations
      if (perf.quantumFluctuation > 0.1) {
        ctx.fillStyle = `rgba(0,230,255,${perf.quantumFluctuation * 0.05})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }
    }
    
    // Vortex system for magical shape morphing
    function activateVortex(centerX, centerY, centerZ, strength = 1.0, duration = 1500) {
      vortex.active = true;
      vortex.centerX = centerX || 0;
      vortex.centerY = centerY || 0;
      vortex.centerZ = centerZ || 0;
      vortex.targetStrength = strength;
      vortex.strength = 0; // Start from zero and build up
      vortex.phase = 0;
      
      console.log('🌪️ Quantum vortex activated!', { strength, duration });
      
      // Auto-deactivate after duration
      setTimeout(() => {
        vortex.targetStrength = 0; // Gradual fade out
        setTimeout(() => {
          vortex.active = false;
        }, 800);
      }, duration);
    }
    
    function updateVortex() {
      if (!vortex.active) return;
      
      // Smoothly interpolate vortex strength
      vortex.strength += (vortex.targetStrength - vortex.strength) * 0.08;
      vortex.phase += vortex.rotationSpeed;
      
      // Apply vortex forces to particles
      points.forEach((p, i) => {
        if (vortex.strength < 0.01) return;
        
        // Distance from vortex center
        const dx = p.x - vortex.centerX;
        const dy = p.y - vortex.centerY;
        const dz = p.z - vortex.centerZ;
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
        
        if (dist < vortex.radius * 2) {
          // Vortex influence based on distance (closer = stronger)
          const influence = vortex.strength * (1 - Math.min(1, dist / vortex.radius));
          
          // Spiral motion around the center
          const angle = Math.atan2(dz, dx) + vortex.phase;
          const spiralRadius = dist * (1 - vortex.spiralTightness * influence);
          
          // Calculate vortex target position
          const vortexX = vortex.centerX + Math.cos(angle) * spiralRadius;
          const vortexZ = vortex.centerZ + Math.sin(angle) * spiralRadius;
          const vortexY = p.y + (vortex.centerY - p.y) * vortex.verticalPull * influence;
          
          // Blend current position with vortex position
          p.x += (vortexX - p.x) * influence * 0.3;
          p.y += (vortexY - p.y) * influence * 0.2;
          p.z += (vortexZ - p.z) * influence * 0.3;
          
          // Add some quantum uncertainty for life
          const uncertainty = influence * 0.5;
          p.x += (Math.random() - 0.5) * uncertainty;
          p.y += (Math.random() - 0.5) * uncertainty;
          p.z += (Math.random() - 0.5) * uncertainty;
        }
      });
    }
    
    // Einstein's main animation loop
    function quantumStep() {
      if (t === 0) console.log('🚀 First quantum step - animation starting!');
      const frameStart = performance.now();
      const dt = Math.max(0.0001, frameStart - perf.lastNow);
      perf.lastNow = frameStart;
      perf.frames++;
      
      // Update magical vortex system
      updateVortex();
      
      // Update quantum optimizer
      if (optimizer) {
        optimizer.recordPerformance(dt);
        
        if (perf.frames % 60 === 0) { // Update every second
          const settings = optimizer.calculateOptimalSettings();
          
          // Apply quantum-optimized settings
          if (Math.abs(settings.particleCount - particleCount) > 100) {
            particleCount = settings.particleCount;
            console.log(`⚛️ Quantum adjustment: ${particleCount} particles`);
            initializeParticles();
          }
          
          perf.stride = settings.stride;
          perf.glowScale = settings.glowIntensity;
          perf.quantumFluctuation = settings.quantumFluctuation;
          perf.relativisticFactor = settings.relativisticAdjustment;
        }
      }
      
      t += perf.relativisticFactor;
      drawQuantumBackground();
      
      // Camera rotation with quantum uncertainty
      camera.rotY += style.rotationSpeed;
      camera.rotX = Math.sin(t * 0.001) * 0.05;
      
      // Apply Heisenberg uncertainty if physics available
      if (physics && style.quantumUncertainty > 0) {
        const uncertainty = physics.heisenbergUncertainty(camera.rotY, style.rotationSpeed);
        camera.rotY += uncertainty.deltaPosition * style.quantumUncertainty;
      }
      
      // Generate target positions
      if (targetShape === 'sphere') {
        generateQuantumSphere(120 + Math.sin(t * 0.002) * 20);
      } else if (targetShape === 'cube') {
        generateQuantumCube(100 + Math.sin(t * 0.003) * 15);
      } else {
        generateSwarm();
      }
      
      // Process particles with quantum mechanics
      const visibleParticles = [];
      
      for (let i = 0; i < points.length; i += perf.stride) {
        const p = points[i];
        
        // Quantum tunneling for smooth movement
        const lerpFactor = 0.03 + energy * 0.02;
        if (physics && physics.quantumTunnel(
          Math.sqrt((p.tx-p.x)*(p.tx-p.x) + (p.ty-p.y)*(p.ty-p.y) + (p.tz-p.z)*(p.tz-p.z)) / 100
        )) {
          // Instant tunneling
          p.x = p.tx; p.y = p.ty; p.z = p.tz;
        } else {
          // Classical movement
          p.x += (p.tx - p.x) * lerpFactor;
          p.y += (p.ty - p.y) * lerpFactor;
          p.z += (p.tz - p.z) * lerpFactor;
        }
        
        // Add quantum jitter with uncertainty principle
        const jitterAmount = style.jitter * energy;
        if (physics) {
          const fastSin = physics.fastSin((p.phase + t * 0.1) * 57.2958); // Convert to degrees
          const fastCos = physics.fastCos((p.phase * 1.3 + t * 0.08) * 57.2958);
          
          p.x += fastSin * jitterAmount;
          p.y += fastCos * jitterAmount;
          p.z += fastSin * 0.5 * jitterAmount;
        } else {
          p.x += Math.sin(p.phase + t * 0.003) * jitterAmount;
          p.y += Math.cos(p.phase * 1.3 + t * 0.002) * jitterAmount;
          p.z += Math.sin(p.phase * 0.7 + t * 0.004) * jitterAmount * 0.5;
        }
        
        p.phase += p.frequency;
        
        // Project to screen with relativistic effects
        const projected = project3D(p.x, p.y, p.z);
        if (projected) {
          p.sx = projected.x;
          p.sy = projected.y;
          p.depth = -projected.z;
          p.scale = projected.scale;
          visibleParticles.push({ particle: p, index: i, depth: p.depth });
        }
      }
      
      // Sort by depth for proper rendering
      visibleParticles.sort((a, b) => b.depth - a.depth);
      
      // Render particles with quantum effects
      for (const { particle: p, index: i } of visibleParticles) {
        const depthFactor = Math.max(0.1, Math.min(1.0, p.scale * 0.002));
        const size = (style.particleSize + Math.sin(i + t * 0.04) * 0.3) * p.amplitude * depthFactor;
        const alpha = depthFactor * style.brightness * perf.relativisticFactor;
        
        if (size > 0.2 && alpha > 0.03) {
          // Quantum color based on particle properties
          const hue = (p.charge > 0 ? 190 : 200) + p.spin * 10;
          const saturation = 80 + p.field * 20;
          const lightness = 50 + alpha * 50;
          
          // Glow effect with quantum uncertainty
          ctx.beginPath();
          ctx.arc(p.sx, p.sy, size * 1.5, 0, Math.PI * 2);
          ctx.fillStyle = `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha * 0.4})`;
          ctx.shadowBlur = style.glowRadius * depthFactor * perf.glowScale;
          ctx.shadowColor = `hsl(${hue}, ${saturation}%, ${lightness + 20}%)`;
          ctx.fill();
          
          // Core particle
          ctx.shadowBlur = 0;
          ctx.beginPath();
          ctx.arc(p.sx, p.sy, size, 0, Math.PI * 2);
          ctx.fillStyle = `hsla(${hue}, ${saturation}%, ${lightness + 30}%, ${alpha})`;
          ctx.fill();
        }
      }
      
      // Energy decay with quantum fluctuations
      energy = Math.max(0.15, energy * 0.985 + perf.quantumFluctuation * 0.001);
      
      requestAnimationFrame(quantumStep);
    }
    
    // Public API with Einstein naming
        
    // Particle management functions
    function setParticleCount(count) {
      const newCount = Math.max(400, Math.min(3000, count));
      particleCount = newCount;
      console.log('⚛️ Quantum field adjusted to', particleCount, 'particles');
      // Note: Particle reinitialization would require full system restart
    }

    window.__quantumMorphTo = function(shape, hold = 2000) {
      if (morphBusy) return;
      morphBusy = true;
      targetShape = shape;
      energy += 0.3; // Energy boost for morphing
      
      // Activate magical vortex during shape formation! 🌪️✨
      const canvas = document.getElementById('scene');
      if (canvas) {
        const centerX = 0;
        const centerY = -50; // Slightly above center for better visual
        const centerZ = 0;
        const vortexStrength = 0.8 + energy * 0.4; // Stronger vortex with more energy
        
        // Activate vortex for the shape formation
        activateVortex(centerX, centerY, centerZ, vortexStrength, Math.min(hold * 0.6, 1200));
        
        console.log('🌪️ Vortex formation activated for shape:', shape);
      }
      
      setTimeout(() => {
        morphBusy = false;
        targetShape = 'swarm';
        
        // Small vortex pulse when returning to swarm
        activateVortex(0, 0, 0, 0.4, 800);
      }, hold);
    };
    
    window.__quantumEnergy = function(level) {
      energy = Math.max(0.1, Math.min(1.0, level));
    };
    
    // Compatibility functions for app.js integration
    window.__orbPulse = function(intensity) {
      energy = Math.min(1.2, energy + (intensity || 0.25));
      console.log('🔮 Quantum pulse:', intensity);
    };
    
    window.__orbThinking = function(active) {
      thinking.active = !!active;
      if (active) {
        energy += 0.1;
        style.brightness = Math.min(2.0, style.brightness + 0.2);
        
        // Add gentle vortex during thinking for alive feel ✨
        activateVortex(0, -30, 0, 0.3, 1000);
      }
      console.log('🧠 Quantum thinking mode:', active);
    };
    
    window.__sceneParticles = function(cmd) {
      if (cmd === 'more' || cmd === 'up') {
        setParticleCount(Math.min(2400, particleCount + 200));
      } else if (cmd === 'less' || cmd === 'down') {
        setParticleCount(Math.max(600, particleCount - 200));
      }
      console.log('⚛️ Quantum particle adjustment:', cmd, particleCount);
    };
    
    window.__sceneMorphForDialogue = function(meta) {
      const m = meta || {};
      const shape = (m.shape || '').toLowerCase();
      const hold = m.holdMs || 2000;
      
      const shapeMap = {
        'cube': 'cube', 'box': 'cube', 'square': 'cube',
        'sphere': 'sphere', 'ball': 'sphere', 'circle': 'sphere',
        'ring': 'torus', 'donut': 'torus', 'torus': 'torus'
      };
      
      const targetShape = shapeMap[shape] || 'sphere';
      window.__quantumMorphTo(targetShape, hold);
      console.log('💬 Quantum dialogue morph:', shape, '->', targetShape);
    };
    
    window.__sceneSetShape = function(shape) {
      setShape(shape || 'swarm');
      energy += 0.3;
      console.log('🔄 Quantum shape set:', shape);
    };
    
    // Initialize the quantum field
    initializeParticles();
    quantumStep();
    
    console.log('🌌 Quantum scene initialized with Einstein physics');
    console.log('🔗 App.js compatibility functions loaded');
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScene);
  } else {
    initScene();
  }
})();
