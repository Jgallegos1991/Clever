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
    this.maxParticles = 80; // Slightly increased for better visual density
    // Force dpr to 1 for crisp pixel rendering and avoid scaling issues
    this.dpr = 1;
    
    // Advanced particle control systems
    this.magneticFields = [];
    this.particleGroups = new Map();
    this.energyWaves = [];
    this.attractors = [];
    this.customFormations = new Map();
    
    // Visual enhancement settings
    this.trailMode = false;
    this.energyFlowMode = true;
    this.particlePhysics = {
      gravity: 0,
      magnetism: 0.5,
      cohesion: 0.3,
      separation: 0.2
    };
    
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
          // Dynamic center-stage whirlpool effect
          const whirlCenterX = centerX;
          const whirlCenterY = centerY; // True center for stage focus
          const whirlAngle = (i / this.particles.length) * Math.PI * 8 + Date.now() * 0.0015; // Faster rotation
          const whirlRadius = radius * (0.4 + Math.sin(whirlAngle * 0.3) * 0.3);
          const whirlHeight = Math.sin(whirlAngle * 1.5) * 40; // Gentle vertical motion
          const whirlSpiral = (i / this.particles.length) * radius * 0.2; // Spiral inward/outward
          
          particle.targetX = whirlCenterX + Math.cos(whirlAngle) * (whirlRadius + whirlSpiral) + randomOffset();
          particle.targetY = whirlCenterY + Math.sin(whirlAngle) * (whirlRadius + whirlSpiral) * 0.6 + whirlHeight;
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
    // Update magnetic fields
    this.magneticFields = this.magneticFields.filter(field => {
      field.strength *= field.decay;
      return field.strength > 0.01;
    });

    // Update energy waves
    this.energyWaves = this.energyWaves.filter(wave => {
      if (wave.active) {
        wave.radius += wave.speed;
        if (wave.radius > wave.maxRadius) {
          wave.active = false;
          return false;
        }
      }
      return wave.active;
    });

    this.particles.forEach((particle, i) => {
      // Move towards target formation
      const dx = particle.targetX - particle.x;
      const dy = particle.targetY - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance > 1) {
        particle.vx += dx * (particle.speed * 0.08);
        particle.vy += dy * (particle.speed * 0.08);
      }

      // Apply magnetic field effects
      this.magneticFields.forEach(field => {
        const fieldDx = field.x - particle.x;
        const fieldDy = field.y - particle.y;
        const fieldDistance = Math.sqrt(fieldDx * fieldDx + fieldDy * fieldDy);
        
        if (fieldDistance < field.radius && fieldDistance > 1) {
          const fieldStrength = field.strength * field.polarity / (fieldDistance * fieldDistance) * 1000;
          particle.vx += fieldDx * fieldStrength;
          particle.vy += fieldDy * fieldStrength;
        }
      });

      // Apply energy wave effects
      this.energyWaves.forEach(wave => {
        const waveDx = wave.x - particle.x;
        const waveDy = wave.y - particle.y;
        const waveDistance = Math.sqrt(waveDx * waveDx + waveDy * waveDy);
        
        if (Math.abs(waveDistance - wave.radius) < 20) {
          const waveForce = wave.intensity * 0.1;
          const angle = Math.atan2(-waveDy, -waveDx);
          particle.vx += Math.cos(angle) * waveForce;
          particle.vy += Math.sin(angle) * waveForce;
          particle.energy = Math.min(1, particle.energy + wave.intensity * 0.1);
          particle.hue = wave.hue;
        }
      });

      // Group behavior (flocking)
      this.particleGroups.forEach((group, groupId) => {
        if (group.particles.includes(i)) {
          let avgX = 0, avgY = 0, avgVx = 0, avgVy = 0;
          let separationVx = 0, separationVy = 0;
          let groupSize = 0;

          group.particles.forEach(pi => {
            if (pi !== i && pi < this.particles.length) {
              const other = this.particles[pi];
              avgX += other.x;
              avgY += other.y;
              avgVx += other.vx;
              avgVy += other.vy;
              groupSize++;

              // Separation force
              const sepDx = particle.x - other.x;
              const sepDy = particle.y - other.y;
              const sepDist = Math.sqrt(sepDx * sepDx + sepDy * sepDy);
              if (sepDist < 30 && sepDist > 0) {
                separationVx += sepDx / sepDist;
                separationVy += sepDy / sepDist;
              }
            }
          });

          if (groupSize > 0) {
            avgX /= groupSize;
            avgY /= groupSize;
            avgVx /= groupSize;
            avgVy /= groupSize;

            // Cohesion: move toward group center
            particle.vx += (avgX - particle.x) * group.cohesion * 0.001;
            particle.vy += (avgY - particle.y) * group.cohesion * 0.001;

            // Alignment: match group velocity
            particle.vx += (avgVx - particle.vx) * group.alignment * 0.1;
            particle.vy += (avgVy - particle.vy) * group.alignment * 0.1;

            // Separation: avoid crowding
            particle.vx += separationVx * group.separation * 0.01;
            particle.vy += separationVy * group.separation * 0.01;
          }
        }
      });
      
      // Mouse interaction - enhanced attraction
      if (this.mouse) {
        const mouseDx = this.mouse.x - particle.x;
        const mouseDy = this.mouse.y - particle.y;
        const mouseDistance = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
        
        if (mouseDistance < 200) {
          const attraction = (200 - mouseDistance) / 200 * 0.0005;
          particle.vx += mouseDx * attraction;
          particle.vy += mouseDy * attraction;
          
          // Increase energy when near mouse
          particle.energy = Math.min(1, particle.energy + 0.002);
          
          // Create mini magnetic field at mouse position
          if (Math.random() < 0.1) {
            this.addMagneticField(this.mouse.x, this.mouse.y, 0.1, 50, 1);
          }
        } else {
          // Decrease energy when away from mouse
          particle.energy = Math.max(0.08, particle.energy - 0.001);
        }
      }
      
      // Apply velocity with damping
      particle.vx *= 0.992; // Slightly less damping for more fluid movement
      particle.vy *= 0.992;
      
      particle.x += particle.vx;
      particle.y += particle.vy;
      
      // Update phase for pulsing with breathing effect
      particle.phase += 0.003 + particle.energy * 0.005;
      
      // Enhanced size pulsing based on energy
      const breathingPhase = Date.now() * 0.001 + particle.phase;
      const energyPulse = Math.sin(particle.phase * 2) * particle.energy * 0.5;
      particle.size = particle.size * 0.98 + (1.5 + Math.sin(breathingPhase) * 0.5 + energyPulse) * 0.02;
      
      // Dynamic color shifting based on energy and connections
      const colorShift = particle.energy * 0.2 + Math.sin(particle.phase) * 0.1;
      particle.hue += colorShift;
      if (particle.hue > 220) particle.hue = 160;
      if (particle.hue < 160) particle.hue = 220;
      
      // Wrap around screen edges
      if (particle.x < 0) particle.x = this.width;
      if (particle.x > this.width) particle.x = 0;
      if (particle.y < 0) particle.y = this.height;
      if (particle.y > this.height) particle.y = 0;
    });

    // Update energy streams
    if (this.energyStreams) {
      this.energyStreams = this.energyStreams.filter(stream => {
        const age = Date.now() - stream.startTime;
        if (age > stream.duration) return false;
        
        stream.particles.forEach(streamParticle => {
          streamParticle.progress += streamParticle.speed;
          if (streamParticle.progress > 1) streamParticle.progress = 0;
        });
        
        return true;
      });
    }
  }

  draw() {
    // Clear canvas (or create trail effect if enabled)
    if (this.trailMode) {
      this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      this.ctx.fillRect(0, 0, this.width, this.height);
    } else {
      this.ctx.clearRect(0, 0, this.width, this.height);
    }

    // Draw energy waves first (background layer)
    this.drawEnergyWaves();

    // Draw magnetic fields
    this.drawMagneticFields();

    // Draw energy streams
    this.drawEnergyStreams();
    
    // Draw particle connections
    this.drawConnections();

    // Draw particles with enhanced effects
    this.particles.forEach((particle, i) => {
      this.ctx.save();
      
      // Dynamic alpha based on energy and phase
      const dynamicAlpha = particle.alpha * (0.7 + Math.sin(particle.phase) * 0.3) * (0.8 + particle.energy * 0.2);
      this.ctx.globalAlpha = dynamicAlpha;
      
      // Energy-based size multiplier
      const energySize = particle.size * (1 + particle.energy * 0.5);
      
      // Create multi-layer glow effect
      const layers = [
        { radius: energySize * 4, alpha: 0.2, hueShift: 0 },
        { radius: energySize * 2.5, alpha: 0.4, hueShift: 20 },
        { radius: energySize * 1.5, alpha: 0.6, hueShift: 10 }
      ];
      
      layers.forEach(layer => {
        const gradient = this.ctx.createRadialGradient(
          particle.x, particle.y, 0,
          particle.x, particle.y, layer.radius
        );
        const hue = (particle.hue + layer.hueShift) % 360;
        const lightness = 60 + particle.energy * 20;
        
        gradient.addColorStop(0, `hsla(${hue}, 85%, ${lightness}%, ${layer.alpha})`);
        gradient.addColorStop(0.7, `hsla(${hue}, 85%, ${lightness}%, ${layer.alpha * 0.5})`);
        gradient.addColorStop(1, `hsla(${hue}, 85%, ${lightness}%, 0)`);
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, layer.radius, 0, Math.PI * 2);
        this.ctx.fill();
      });
      
      // Bright center core with energy pulsing
      this.ctx.globalAlpha = 1.0;
      const coreSize = 1 + particle.energy * 2;
      const coreHue = (particle.hue + 40) % 360;
      this.ctx.fillStyle = `hsl(${coreHue}, 100%, 85%)`;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, coreSize, 0, Math.PI * 2);
      this.ctx.fill();
      
      // Super bright pixel center
      this.ctx.fillStyle = '#FFFFFF';
      this.ctx.fillRect(Math.round(particle.x - 0.5), Math.round(particle.y - 0.5), 1, 1);
      
      this.ctx.restore();
    });
  }

  drawEnergyWaves() {
    this.ctx.save();
    this.energyWaves.forEach(wave => {
      if (wave.active) {
        const alpha = wave.intensity * (1 - wave.radius / wave.maxRadius);
        this.ctx.strokeStyle = `hsla(${wave.hue}, 80%, 60%, ${alpha * 0.3})`;
        this.ctx.lineWidth = 2;
        this.ctx.globalAlpha = alpha;
        
        this.ctx.beginPath();
        this.ctx.arc(wave.x, wave.y, wave.radius, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Inner ripple
        this.ctx.strokeStyle = `hsla(${wave.hue + 30}, 90%, 80%, ${alpha * 0.6})`;
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.arc(wave.x, wave.y, wave.radius * 0.7, 0, Math.PI * 2);
        this.ctx.stroke();
      }
    });
    this.ctx.restore();
  }

  drawMagneticFields() {
    this.ctx.save();
    this.magneticFields.forEach(field => {
      const alpha = field.strength * 0.1;
      const hue = field.polarity > 0 ? 200 : 0; // Blue for attraction, red for repulsion
      
      this.ctx.strokeStyle = `hsla(${hue}, 70%, 50%, ${alpha})`;
      this.ctx.lineWidth = 1;
      this.ctx.globalAlpha = alpha;
      
      // Draw field boundary
      this.ctx.beginPath();
      this.ctx.arc(field.x, field.y, field.radius, 0, Math.PI * 2);
      this.ctx.stroke();
      
      // Draw field center
      this.ctx.fillStyle = `hsla(${hue}, 90%, 70%, ${alpha * 2})`;
      this.ctx.beginPath();
      this.ctx.arc(field.x, field.y, 3, 0, Math.PI * 2);
      this.ctx.fill();
    });
    this.ctx.restore();
  }

  drawEnergyStreams() {
    if (!this.energyStreams) return;
    
    this.ctx.save();
    this.energyStreams.forEach(stream => {
      const fromParticle = this.particles[stream.from];
      const toParticle = this.particles[stream.to];
      
      if (!fromParticle || !toParticle) return;
      
      // Draw main stream line
      this.ctx.strokeStyle = stream.color;
      this.ctx.lineWidth = 2;
      this.ctx.globalAlpha = stream.intensity * 0.7;
      
      this.ctx.beginPath();
      this.ctx.moveTo(fromParticle.x, fromParticle.y);
      this.ctx.lineTo(toParticle.x, toParticle.y);
      this.ctx.stroke();
      
      // Draw flowing particles
      stream.particles.forEach(streamParticle => {
        const x = fromParticle.x + (toParticle.x - fromParticle.x) * streamParticle.progress;
        const y = fromParticle.y + (toParticle.y - fromParticle.y) * streamParticle.progress;
        
        this.ctx.globalAlpha = streamParticle.alpha;
        this.ctx.fillStyle = stream.color;
        this.ctx.beginPath();
        this.ctx.arc(x, y, streamParticle.size, 0, Math.PI * 2);
        this.ctx.fill();
      });
    });
    this.ctx.restore();
  }

  drawConnections() {
    const maxDistance = 140;
    const maxConnections = 200; // Increased for more connectivity
    let connectionCount = 0;
    const time = Date.now() * 0.001;
    
    this.ctx.save();
    
    for (let i = 0; i < this.particles.length && connectionCount < maxConnections; i++) {
      for (let j = i + 1; j < this.particles.length && connectionCount < maxConnections; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];
        
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < maxDistance) {
          const connectionStrength = (1 - distance / maxDistance);
          const alpha = connectionStrength * 0.8;
          
          // Dynamic color based on connection strength and time
          const hue = 160 + connectionStrength * 60 + Math.sin(time + i * 0.1) * 20;
          const saturation = 85 + connectionStrength * 15;
          const lightness = 60 + connectionStrength * 30;
          
          // Pulsing effect based on particle energy
          const pulseIntensity = (p1.energy + p2.energy) * 0.5;
          const pulseFactor = 0.7 + Math.sin(time * 3 + distance * 0.05) * 0.3 * pulseIntensity;
          
          // Variable line width based on connection strength
          this.ctx.lineWidth = 0.5 + connectionStrength * 2.5;
          
          // Create gradient line for energy flow effect
          const gradient = this.ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
          gradient.addColorStop(0, `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha * pulseFactor})`);
          gradient.addColorStop(0.5, `hsla(${hue + 20}, ${saturation + 10}%, ${lightness + 20}%, ${alpha * pulseFactor * 1.5})`);
          gradient.addColorStop(1, `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha * pulseFactor})`);
          
          this.ctx.strokeStyle = gradient;
          this.ctx.globalAlpha = 1;
          
          // Draw main connection line
          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();
          
          // Add energy particles flowing along connections for strong links
          if (connectionStrength > 0.7 && Math.random() < 0.1) {
            const flowProgress = (time * 2 + i + j) % 1;
            const flowX = p1.x + (p2.x - p1.x) * flowProgress;
            const flowY = p1.y + (p2.y - p1.y) * flowProgress;
            
            this.ctx.save();
            this.ctx.globalAlpha = alpha * 2;
            this.ctx.fillStyle = `hsl(${hue + 40}, 100%, 80%)`;
            this.ctx.beginPath();
            this.ctx.arc(flowX, flowY, 1.5, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.restore();
          }
          
          connectionCount++;
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

  // Advanced particle control methods
  triggerPulse(intensity = 1) {
    this.particles.forEach(particle => {
      particle.vx += (Math.random() - 0.5) * intensity;
      particle.vy += (Math.random() - 0.5) * intensity;
      particle.energy = Math.min(1, particle.energy + intensity * 0.3);
    });
  }

  // Create a magnetic field that attracts/repels particles
  addMagneticField(x, y, strength = 1, radius = 200, polarity = 1) {
    this.magneticFields.push({
      x, y, strength, radius, polarity,
      id: Date.now() + Math.random(),
      decay: 0.98
    });
  }

  // Create energy wave that ripples through particles
  createEnergyWave(x, y, maxRadius = 300, speed = 5, intensity = 1) {
    this.energyWaves.push({
      x, y, radius: 0, maxRadius, speed, intensity,
      hue: 160 + Math.random() * 60,
      active: true
    });
  }

  // Group particles for coordinated movement
  createParticleGroup(particleIndices, groupId = null) {
    const id = groupId || `group_${Date.now()}`;
    this.particleGroups.set(id, {
      particles: particleIndices,
      cohesion: 0.5,
      separation: 0.3,
      alignment: 0.2
    });
    return id;
  }

  // Make particles form text or custom shapes
  morphToText(text, fontSize = 40) {
    // Create invisible canvas to measure text
    const textCanvas = document.createElement('canvas');
    const textCtx = textCanvas.getContext('2d');
    textCtx.font = `${fontSize}px Arial`;
    const metrics = textCtx.measureText(text);
    
    textCanvas.width = metrics.width + 20;
    textCanvas.height = fontSize + 20;
    textCtx.font = `${fontSize}px Arial`;
    textCtx.fillStyle = 'white';
    textCtx.fillText(text, 10, fontSize);
    
    // Get pixel data
    const imageData = textCtx.getImageData(0, 0, textCanvas.width, textCanvas.height);
    const pixels = [];
    
    for (let y = 0; y < textCanvas.height; y += 3) {
      for (let x = 0; x < textCanvas.width; x += 3) {
        const index = (y * textCanvas.width + x) * 4;
        if (imageData.data[index + 3] > 128) { // Alpha > 50%
          pixels.push({
            x: this.width / 2 - textCanvas.width / 2 + x,
            y: this.height / 2 - textCanvas.height / 2 + y
          });
        }
      }
    }
    
    // Assign particles to text positions
    this.particles.forEach((particle, i) => {
      if (i < pixels.length) {
        particle.targetX = pixels[i].x + (Math.random() - 0.5) * 5;
        particle.targetY = pixels[i].y + (Math.random() - 0.5) * 5;
      } else {
        // Extra particles form a cloud around the text
        const angle = Math.random() * Math.PI * 2;
        const distance = 50 + Math.random() * 100;
        particle.targetX = this.width / 2 + Math.cos(angle) * distance;
        particle.targetY = this.height / 2 + Math.sin(angle) * distance;
      }
    });
  }

  // Create flowing energy streams between specific particles
  createEnergyStream(fromIndex, toIndex, color = '#69EACB', duration = 3000) {
    const stream = {
      from: fromIndex,
      to: toIndex,
      color,
      intensity: 1,
      startTime: Date.now(),
      duration,
      particles: []
    };
    
    // Create small particles that flow along the stream
    for (let i = 0; i < 5; i++) {
      stream.particles.push({
        progress: i / 5,
        speed: 0.02 + Math.random() * 0.01,
        size: 2 + Math.random() * 2,
        alpha: 0.8
      });
    }
    
    this.energyStreams = this.energyStreams || [];
    this.energyStreams.push(stream);
  }

  // Make particles dance to audio (if available)
  syncToAudio(audioData) {
    if (!audioData || !audioData.length) return;
    
    const bassLevel = audioData.slice(0, 10).reduce((a, b) => a + b) / 10;
    const midLevel = audioData.slice(10, 100).reduce((a, b) => a + b) / 90;
    const highLevel = audioData.slice(100).reduce((a, b) => a + b) / (audioData.length - 100);
    
    this.particles.forEach((particle, i) => {
      // Bass affects particle size and energy
      particle.energy = Math.max(0.1, bassLevel / 255);
      
      // Mids affect movement
      const midInfluence = midLevel / 255 * 0.5;
      particle.vx += (Math.random() - 0.5) * midInfluence;
      particle.vy += (Math.random() - 0.5) * midInfluence;
      
      // Highs affect color
      particle.hue = (particle.hue + highLevel / 255 * 10) % 360;
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

  // New mind-blowing interaction methods!
  
  // Particle explosion from center
  explode(intensity = 1) {
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    
    this.particles.forEach(particle => {
      const angle = Math.atan2(particle.y - centerY, particle.x - centerX);
      const force = intensity * (0.5 + Math.random() * 0.5);
      particle.vx += Math.cos(angle) * force;
      particle.vy += Math.sin(angle) * force;
      particle.energy = Math.min(1, particle.energy + intensity * 0.5);
    });
    
    // Create energy wave
    this.createEnergyWave(centerX, centerY, 400, 8, intensity);
  }

  // Particle implosion to center
  implode(intensity = 1) {
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    
    this.particles.forEach(particle => {
      const angle = Math.atan2(centerY - particle.y, centerX - particle.x);
      const force = intensity * (0.3 + Math.random() * 0.3);
      particle.vx += Math.cos(angle) * force;
      particle.vy += Math.sin(angle) * force;
    });
    
    // Add magnetic attractor at center
    this.addMagneticField(centerX, centerY, intensity * 2, 300, 1);
  }

  // Create swirling vortex
  createVortex(x, y, strength = 1, duration = 5000) {
    const vortex = {
      x, y, strength, radius: 200,
      startTime: Date.now(),
      duration
    };
    
    this.attractors.push(vortex);
    
    // Apply immediate swirl force
    this.particles.forEach(particle => {
      const dx = x - particle.x;
      const dy = y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < vortex.radius) {
        const angle = Math.atan2(dy, dx) + Math.PI / 2;
        const force = strength * (1 - distance / vortex.radius) * 0.02;
        particle.vx += Math.cos(angle) * force;
        particle.vy += Math.sin(angle) * force;
      }
    });
  }

  // Lightning effect between particles
  createLightning(fromIndex, toIndex) {
    const from = this.particles[fromIndex];
    const to = this.particles[toIndex];
    if (!from || !to) return;
    
    // Create jagged lightning path
    const lightningPath = [];
    const steps = 10;
    
    for (let i = 0; i <= steps; i++) {
      const progress = i / steps;
      const x = from.x + (to.x - from.x) * progress + (Math.random() - 0.5) * 20;
      const y = from.y + (to.y - from.y) * progress + (Math.random() - 0.5) * 20;
      lightningPath.push({ x, y });
    }
    
    // Draw lightning
    this.ctx.save();
    this.ctx.strokeStyle = '#FFFFFF';
    this.ctx.lineWidth = 3;
    this.ctx.shadowColor = '#69EACB';
    this.ctx.shadowBlur = 10;
    
    this.ctx.beginPath();
    this.ctx.moveTo(lightningPath[0].x, lightningPath[0].y);
    for (let i = 1; i < lightningPath.length; i++) {
      this.ctx.lineTo(lightningPath[i].x, lightningPath[i].y);
    }
    this.ctx.stroke();
    this.ctx.restore();
    
    // Energize connected particles
    from.energy = Math.min(1, from.energy + 0.5);
    to.energy = Math.min(1, to.energy + 0.5);
  }

  // Particle dance party!
  danceParty(duration = 10000) {
    const startTime = Date.now();
    const originalSpeeds = this.particles.map(p => p.speed);
    
    const dance = () => {
      const elapsed = Date.now() - startTime;
      if (elapsed > duration) {
        // Restore original speeds
        this.particles.forEach((p, i) => {
          p.speed = originalSpeeds[i];
        });
        return;
      }
      
      // Make particles dance
      this.particles.forEach((particle, i) => {
        const dancePhase = elapsed * 0.005 + i * 0.2;
        const danceIntensity = 0.5 + Math.sin(elapsed * 0.003) * 0.3;
        
        particle.vx += Math.sin(dancePhase) * danceIntensity * 0.01;
        particle.vy += Math.cos(dancePhase * 1.3) * danceIntensity * 0.01;
        particle.energy = 0.5 + Math.sin(dancePhase * 2) * 0.3;
        particle.hue = (160 + Math.sin(dancePhase) * 60) % 360;
      });
      
      requestAnimationFrame(dance);
    };
    
    dance();
  }

  // Toggle trail mode for psychedelic effects
  toggleTrailMode() {
    this.trailMode = !this.trailMode;
  }

  // Create custom formation from array of {x, y} points
  morphToCustomFormation(points, scale = 1) {
    const centerX = this.width / 2;
    const centerY = this.height / 2;
    
    this.particles.forEach((particle, i) => {
      if (i < points.length) {
        particle.targetX = centerX + points[i].x * scale;
        particle.targetY = centerY + points[i].y * scale;
      } else {
        // Extra particles orbit around the formation
        const angle = (i / this.particles.length) * Math.PI * 2;
        const radius = 100 + Math.random() * 50;
        particle.targetX = centerX + Math.cos(angle) * radius;
        particle.targetY = centerY + Math.sin(angle) * radius;
      }
    });
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

// Enhanced global functions for external control
window.triggerPulse = function(intensity) {
  if (window.holographicChamber) {
    window.holographicChamber.triggerPulse(intensity);
  }
};

window.explodeParticles = function(intensity = 1) {
  if (window.holographicChamber) {
    window.holographicChamber.explode(intensity);
  }
};

window.implodeParticles = function(intensity = 1) {
  if (window.holographicChamber) {
    window.holographicChamber.implode(intensity);
  }
};

window.createVortex = function(x, y, strength = 1) {
  if (window.holographicChamber) {
    window.holographicChamber.createVortex(x || window.innerWidth/2, y || window.innerHeight/2, strength);
  }
};

window.morphToText = function(text) {
  if (window.holographicChamber) {
    window.holographicChamber.morphToText(text);
  }
};

window.startDanceParty = function(duration = 10000) {
  if (window.holographicChamber) {
    window.holographicChamber.danceParty(duration);
  }
};

window.createLightning = function() {
  if (window.holographicChamber) {
    const particles = window.holographicChamber.particles;
    const from = Math.floor(Math.random() * particles.length);
    const to = Math.floor(Math.random() * particles.length);
    window.holographicChamber.createLightning(from, to);
  }
};

window.toggleTrails = function() {
  if (window.holographicChamber) {
    window.holographicChamber.toggleTrailMode();
  }
};

window.addMagneticField = function(x, y, strength = 1, polarity = 1) {
  if (window.holographicChamber) {
    window.holographicChamber.addMagneticField(x || window.innerWidth/2, y || window.innerHeight/2, strength, 200, polarity);
  }
};

window.createEnergyWave = function(x, y, intensity = 1) {
  if (window.holographicChamber) {
    window.holographicChamber.createEnergyWave(x || window.innerWidth/2, y || window.innerHeight/2, 300, 5, intensity);
  }
};

// Note: Auto-initialization removed to prevent conflicts with main.js
// The chamber is initialized by main.js using window.startHolographicChamber()
// Quiet load: no console logs or UI updates; main.js will initialize when ready.
