/**
 * holographic-chamber.js - Particle System Engine for Clever's Cognitive Enhancement Interface
 * 
 * Why: Creates cognitive visualization representing Clever's thought processes and mental activity,
 * providing immersive visual feedback that enhances the digital brain extension experience.
 * Essential for making Clever's cognitive partnership tangible and engaging through dynamic
 * particle formations that respond to her thinking patterns and user interactions.
 * 
 * Where: Core particle engine loaded by templates/index.html before main.js initialization.
 * Central visual component of Clever's cognitive enhancement interface and digital brain extension.
 * 
 * How: Canvas-based particle physics with formation morphing, animations, and cognitive state
 * visualization through dynamic particle behavior and visual themes.
 * 
 * File Usage:
 *     - Cognitive visualization: Primary engine for visualizing Clever's thought processes
 *     - User engagement: Creates immersive interface enhancing cognitive partnership experience  
 *     - Performance rendering: Optimized particle system for smooth real-time visualization
 *     - State indication: Visual feedback system for Clever's cognitive and emotional states
 *     - Interactive response: Particle behavior responds to user interactions and system events
 *     - Theme management: Handles multiple visual themes for different cognitive states
 *     - Animation control: Manages complex particle animations and formation transitions
 *     - Hardware optimization: Adapts rendering based on device capabilities and performance
 * 
 * Connects to:
 *     - templates/index.html: Core template loading this engine before main application logic
 *     - static/js/main.js: Main application coordinating particle system lifecycle and control
 *     - static/css/style.css: CSS integration for canvas positioning and responsive design
 *     - app.py: Backend integration for cognitive state updates and particle behavior triggers
 *     - persona.py: Personality engine integration for particle themes matching Clever's moods
 *     - evolution_engine.py: Learning system integration for adaptive particle behavior
 *     - docs/config/device_specifications.md: Hardware constraints defining particle count limits
 *     - debug_config.py: Performance monitoring and optimization for particle rendering
 *     - cognitive_shape_engine.py: Advanced shape generation integration for complex formations
 */

console.log('🌟 Holographic Chamber engine loading...');

// Configuration constants
const PARTICLE_CONFIG = {
    MAX_PARTICLES: 100,
    PARTICLE_SIZE: 2,
    ANIMATION_SPEED: 0.8,
    ENERGY_DECAY: 0.98
};

// Visual themes
const VISUAL_THEMES = {
    idle: {
        colors: ['#00FFFF', '#4A9EFF', '#00BFFF'],
        energy: 0.4,
        formation: 'rotating_sphere',
        pulse: true
    },
    thinking: {
        colors: ['#00FF88', '#00FFFF', '#88FFFF'],
        energy: 0.7,
        formation: 'helix',
        pulse: false
    },
    creative: {
        colors: ['#FF6B9D', '#C44569', '#F8B500'],
        energy: 0.9,
        formation: 'constellation',
        pulse: false
    },
    observing: {
        colors: ['#FFD700', '#FFA500', '#FF8C00'],
        energy: 0.6,
        formation: 'rotating_sphere',
        pulse: true
    }
};

/**
 * Particle Class - Individual cognitive elements
 */
class Particle {
    constructor(x, y, chamber) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 2;
        this.vy = (Math.random() - 0.5) * 2;
        this.size = PARTICLE_CONFIG.PARTICLE_SIZE + Math.random();
        this.energy = Math.random() * 0.5 + 0.5;
        this.chamber = chamber;
        
        // Formation properties
        this.targetX = x;
        this.targetY = y;
        this.formationStrength = 0.1;
        this.isInFormation = false;
        
        // Rotation properties for idle state
        this.rotationAngle = Math.random() * Math.PI * 2;
        this.rotationRadius = 0;
        this.baseX = x;
        this.baseY = y;
        this.rotationSpeed = (Math.random() - 0.5) * 0.02;
        
        // Visual properties
        this.opacity = Math.random() * 0.5 + 0.5;
        this.colorIndex = Math.floor(Math.random() * 3);
        this.pulsePhase = Math.random() * Math.PI * 2;
        this.basePulse = Math.random() * 0.3 + 0.7;
    }
    
    update() {
        // Update rotation angle for continuous movement
        this.rotationAngle += this.rotationSpeed;
        
        // Formation behavior
        if (this.isInFormation) {
            const dx = this.targetX - this.x;
            const dy = this.targetY - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > 1) {
                // Enhanced formation strength for mathematical shapes
                const baseStrength = this.mathematicalPoint ? 0.05 : 0.01;
                this.vx += dx * this.formationStrength * baseStrength;
                this.vy += dy * this.formationStrength * baseStrength;
                
                // Additional direct movement for mathematical precision
                if (this.mathematicalPoint && distance > 5) {
                    this.vx += dx * 0.008;
                    this.vy += dy * 0.008;
                }
            }
            
            // Add rotation to formation targets for rotating formations (but not mathematical shapes)
            if (this.chamber.currentFormation === 'rotating_sphere' && !this.mathematicalPoint) {
                this.targetX += Math.cos(this.rotationAngle) * 0.5;
                this.targetY += Math.sin(this.rotationAngle) * 0.5;
            }
        }
        
        // Free movement with subtle rotation
        if (!this.isInFormation) {
            // Add rotational movement around base position
            const rotX = Math.cos(this.rotationAngle) * this.rotationRadius;
            const rotY = Math.sin(this.rotationAngle) * this.rotationRadius;
            
            this.vx += (Math.random() - 0.5) * 0.02;
            this.vy += (Math.random() - 0.5) * 0.02;
            
            // Subtle gravitational pull towards rotation center
            this.vx += (rotX * 0.001);
            this.vy += (rotY * 0.001);
        }
        
        // Apply velocity
        this.x += this.vx * PARTICLE_CONFIG.ANIMATION_SPEED;
        this.y += this.vy * PARTICLE_CONFIG.ANIMATION_SPEED;
        this.vx *= PARTICLE_CONFIG.ENERGY_DECAY;
        this.vy *= PARTICLE_CONFIG.ENERGY_DECAY;
        
        // Boundary conditions
        const canvas = this.chamber.canvas;
        const margin = 20;
        
        if (this.x < margin) {
            this.x = margin;
            this.vx = Math.abs(this.vx) * 0.5;
        }
        if (this.x > canvas.width - margin) {
            this.x = canvas.width - margin;
            this.vx = -Math.abs(this.vx) * 0.5;
        }
        if (this.y < margin) {
            this.y = margin;
            this.vy = Math.abs(this.vy) * 0.5;
        }
        if (this.y > canvas.height - margin) {
            this.y = canvas.height - margin;
            this.vy = -Math.abs(this.vy) * 0.5;
        }
        
        // Update energy
        this.energy = Math.max(0.1, this.energy * 0.999 + Math.random() * 0.001);
        this.opacity = this.energy * 0.8 + 0.2;
    }
    
    render(ctx) {
        const theme = VISUAL_THEMES[this.chamber.currentMode] || VISUAL_THEMES.idle;
        const color = theme.colors[this.colorIndex % theme.colors.length];
        
        // Calculate pulse effect if enabled
        let pulseMultiplier = 1;
        if (theme.pulse) {
            this.pulsePhase += 0.05;
            pulseMultiplier = this.basePulse + Math.sin(this.pulsePhase) * 0.3;
        }
        
        ctx.save();
        
        // Apply pulsing opacity and size
        ctx.globalAlpha = this.opacity * pulseMultiplier;
        const renderSize = this.size * pulseMultiplier;
        
        // Create glow effect
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, renderSize * 2);
        gradient.addColorStop(0, color);
        gradient.addColorStop(0.5, color + '80'); // Semi-transparent
        gradient.addColorStop(1, color + '00'); // Fully transparent
        
        // Draw glow
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, renderSize * 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw core particle
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, renderSize, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
    
    /**
     * Calculate distance to another particle
     * 
     * Why: Needed for connection line rendering between nearby particles
     * Where: Called by HolographicChamber.renderConnections() for proximity detection
     * How: Uses Euclidean distance formula for accurate spatial relationships
     */
    distanceTo(other) {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
}


/**
 * Holographic Chamber Main Class
 */
class HolographicChamber {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.currentMode = 'idle';
        this.currentFormation = 'sphere';
        this.isAnimating = false;
        this.animationId = null;
        
        // Shape rotation properties
        this.currentShapeData = null;
        this.isRotatingShape = false;
        
        this.createParticles();
        console.log('Chamber initialized with', this.particles.length, 'particles');
    }
    
    createParticles() {
        this.particles = [];
        const particleCount = 60; // REVERTED: Keep original count to maintain UI stability
        
        for (let i = 0; i < particleCount; i++) {
            const angle = (i / particleCount) * Math.PI * 2;
            const radius = Math.random() * Math.min(this.canvas.width, this.canvas.height) * 0.3;
            const centerX = this.canvas.width / 2;
            const centerY = this.canvas.height / 2;
            
            const x = centerX + Math.cos(angle) * radius + (Math.random() - 0.5) * 100;
            const y = centerY + Math.sin(angle) * radius + (Math.random() - 0.5) * 100;
            
            this.particles.push(new Particle(x, y, this));
        }
    }
    
    setMode(mode) {
        if (VISUAL_THEMES[mode]) {
            console.log('🧠 Cognitive mode transition:', this.currentMode, '->', mode);
            this.currentMode = mode;
            const theme = VISUAL_THEMES[mode];
            
            // Update particle energy with smooth transition
            this.particles.forEach(particle => {
                particle.energy = Math.random() * theme.energy + (1 - theme.energy) * 0.5;
                // Reset pulse phase for synchronized transitions
                if (theme.pulse) {
                    particle.pulsePhase = Math.random() * Math.PI * 2;
                }
            });
            
            // Morph formation if different
            if (theme.formation !== this.currentFormation) {
                this.morphToFormation(theme.formation);
            }
            
            console.log('✅ Cognitive state synchronized:', mode);
        }
    }

    /**
     * Maintain Cognitive Connection
     * 
     * Why: Ensures Clever maintains continuous cognitive presence and connection awareness
     * Where: Called periodically to maintain system coherence and prevent drift
     * How: Monitors particle coherence, adjusts formation strength, maintains cognitive flow
     * 
     * Connects to:
     *     - main.js: Should be called periodically to maintain system health
     *     - evolution_engine.py: Cognitive state should be logged for learning
     *     - persona.py: Mode changes should trigger cognitive adjustments
     */
    maintainCognitiveConnection() {
        // Check if particles are maintaining formation coherence
        let formationCoherence = 0;
        let totalEnergy = 0;
        
        this.particles.forEach(particle => {
            if (particle.isInFormation) {
                const dx = particle.targetX - particle.x;
                const dy = particle.targetY - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                formationCoherence += (distance < 50) ? 1 : 0;
            }
            totalEnergy += particle.energy;
        });
        
        const coherenceRatio = formationCoherence / this.particles.length;
        const avgEnergy = totalEnergy / this.particles.length;
        
        // Adjust formation strength if coherence is low
        if (coherenceRatio < 0.7) {
            this.particles.forEach(particle => {
                if (particle.isInFormation) {
                    particle.formationStrength = Math.min(0.3, particle.formationStrength + 0.01);
                }
            });
        }
        
        // Boost energy if system is getting sluggish
        if (avgEnergy < 0.3) {
            this.particles.forEach(particle => {
                particle.energy = Math.max(particle.energy, 0.4);
            });
        }
        
        // Log cognitive health
        const cognitiveHealth = {
            coherence: coherenceRatio,
            energy: avgEnergy,
            mode: this.currentMode,
            formation: this.currentFormation,
            timestamp: Date.now()
        };
        
        // Expose to window for external monitoring
        window.cleverCognitiveStatus = cognitiveHealth;
        
        return cognitiveHealth;
    }
    
    morphToFormation(formationType) {
        console.log('Morphing to formation:', formationType);
        this.currentFormation = formationType;
        
        switch (formationType) {
            case 'sphere':
                this.createSphereFormation();
                break;
            case 'rotating_sphere':
                this.createRotatingSphereFormation();
                break;
            case 'helix':
                this.createHelixFormation();
                break;
            case 'constellation':
                this.createConstellationFormation();
                break;
            default:
                this.releaseFormation();
        }
    }
    
    createSphereFormation() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(this.canvas.width, this.canvas.height) * 0.2;
        
        this.particles.forEach((particle, index) => {
            const phi = Math.acos(1 - 2 * (index + 0.5) / this.particles.length);
            const theta = Math.PI * (1 + Math.sqrt(5)) * (index + 0.5);
            
            particle.targetX = centerX + radius * Math.sin(phi) * Math.cos(theta);
            particle.targetY = centerY + radius * Math.sin(phi) * Math.sin(theta);
            particle.isInFormation = true;
            particle.formationStrength = 0.15;
        });
    }

    /**
     * Create Rotating Sphere Formation for Idle State
     * 
     * Why: Provides continuous gentle rotation representing Clever's cognitive background processing
     * Where: Used by idle and observing modes for continuous visual engagement
     * How: Fibonacci sphere distribution with rotation parameters for smooth orbital motion
     * 
     * Connects to:
     *     - setMode(): Called when switching to idle or observing modes
     *     - Particle.update(): Particles use rotation properties for continuous movement
     *     - VISUAL_THEMES: Uses rotation settings from theme configuration
     */
    createRotatingSphereFormation() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(this.canvas.width, this.canvas.height) * 0.25;
        
        this.particles.forEach((particle, index) => {
            // Clear mathematical shape properties for rotating sphere
            particle.mathematicalPoint = false;
            
            // Fibonacci sphere distribution for optimal coverage
            const phi = Math.acos(1 - 2 * (index + 0.5) / this.particles.length);
            const theta = Math.PI * (1 + Math.sqrt(5)) * (index + 0.5);
            
            // Base sphere position
            particle.baseX = centerX;
            particle.baseY = centerY;
            particle.rotationRadius = radius * Math.sin(phi);
            particle.targetX = centerX + particle.rotationRadius * Math.cos(theta);
            particle.targetY = centerY + particle.rotationRadius * Math.sin(theta);
            
            // Set rotation properties for continuous movement
            particle.rotationAngle = theta;
            particle.rotationSpeed = (0.005 + Math.random() * 0.01) * (Math.random() > 0.5 ? 1 : -1);
            
            particle.isInFormation = true;
            particle.formationStrength = 0.12;
        });
        
        console.log('🌀 Rotating sphere formation created for continuous cognitive visualization');
    }
    
    /**
     * Create Perfect 3D Mathematical Shape Formation
     * 
     * Why: Creates geometrically perfect 3D shapes using particles at vertices for
     *      stunning visual demonstrations of mathematical precision
     * Where: Called when shape_data is provided in context from persona responses
     * How: Places particles at calculated 3D vertices with proper perspective
     * 
     * Connects to:
     *     - shape_generator.py: Receives shape type and properties
     *     - persona.py: Called when shape commands generate shape_data in context
     *     - Particle.update(): Particles animate to 3D vertex positions
     */
    createMathematicalShape(shapeData) {
        if (!shapeData || !shapeData.properties) {
            console.warn('Invalid shape data provided to createMathematicalShape');
            return this.createSphereFormation(); // Fallback
        }

        const canvasWidth = this.canvas.width;
        const canvasHeight = this.canvas.height;
        const centerX = canvasWidth / 2;
        const centerY = canvasHeight / 2;

        // Detect shape type and create perfect 3D geometry
        const shapeName = shapeData.name.toLowerCase();
        const properties = shapeData.properties;
        
        console.log(`📐 Creating perfect 3D ${shapeName} with vertices`);

        let vertices = [];
        let radius = Math.min(canvasWidth, canvasHeight) * 0.25; // Size for visibility
        
        // Special scaling for DNA structures - make them much more prominent
        if (shapeName.includes('dna') || shapeName.includes('double helix') || shapeName.includes('genetic')) {
            radius = Math.min(canvasWidth, canvasHeight) * 0.4; // Larger base size for DNA
        }

        if (shapeName.includes('hexagon') || (properties.sides && properties.sides === 6)) {
            // Perfect 3D hexagon vertices
            vertices = this.createHexagonVertices(centerX, centerY, radius);
        } else if (shapeName.includes('triangle') || (properties.sides && properties.sides === 3)) {
            // Perfect 3D triangle vertices
            vertices = this.createTriangleVertices(centerX, centerY, radius);
        } else if (shapeName.includes('pentagon') || (properties.sides && properties.sides === 5)) {
            // Perfect 3D pentagon vertices
            vertices = this.createPentagonVertices(centerX, centerY, radius);
        } else if (shapeName.includes('square') || (properties.sides && properties.sides === 4)) {
            // Perfect 3D square vertices
            vertices = this.createSquareVertices(centerX, centerY, radius);
        } else if (shapeName.includes('cube') || shapeName.includes('box')) {
            // Perfect 3D cube wireframe vertices
            vertices = this.createCubeVertices(centerX, centerY, radius);
        } else if (shapeName.includes('pyramid') || shapeName.includes('tetrahedron')) {
            // Perfect 3D pyramid wireframe vertices  
            vertices = this.createPyramidVertices(centerX, centerY, radius);
        } else if (shapeName.includes('cone')) {
            // Perfect 3D cone wireframe vertices
            vertices = this.createConeVertices(centerX, centerY, radius);
        } else if (shapeName.includes('cylinder') || shapeName.includes('tube')) {
            // Perfect 3D cylinder wireframe vertices
            vertices = this.createCylinderVertices(centerX, centerY, radius);
        } else if (shapeName.includes('sphere_3d') || shapeName.includes('ball')) {
            // Perfect 3D sphere wireframe vertices
            vertices = this.create3DSphereVertices(centerX, centerY, radius);
        } else if (shapeName.includes('circle') || shapeName.includes('sphere')) {
            // Perfect circle vertices
            vertices = this.createCircleVertices(centerX, centerY, radius);
        } else if (shapeName.includes('dna') || shapeName.includes('double helix') || shapeName.includes('genetic')) {
            // DNA double helix vertices - CHECK BEFORE general helix to avoid conflicts
            vertices = this.createDNAVertices(centerX, centerY, radius, properties);
        } else if (shapeName.includes('spiral') || shapeName.includes('helix')) {
            // Spiral/helix vertices
            vertices = this.createSpiralVertices(centerX, centerY, radius, properties);
        } else if (shapeName.includes('fractal') || shapeName.includes('snowflake') || shapeName.includes('koch')) {
            // Fractal vertices
            vertices = this.createFractalVertices(centerX, centerY, radius, properties);
        } else if (shapeName.includes('star') || (properties.star_points)) {
            // Star polygon vertices
            vertices = this.createStarVertices(centerX, centerY, radius, properties.star_points || 5);
        } else if (shapeName.includes('polygon') && properties.sides) {
            // Specific sided polygon
            vertices = this.createPolygonVertices(centerX, centerY, radius, properties.sides);
        } else {
            // Generic polygon or fallback to hexagon for unknown shapes
            const sides = properties.sides || 6;
            vertices = this.createPolygonVertices(centerX, centerY, radius, sides);
        }

        // Clear all particles from previous formations
        this.particles.forEach(particle => {
            particle.isInFormation = false;
            particle.mathematicalPoint = null;
        });

        // Assign particles to vertices (one particle per vertex + extra distributed)
        const vertexCount = vertices.length;
        const particlesPerVertex = Math.floor(this.particles.length / vertexCount);
        const extraParticles = this.particles.length % vertexCount;

        let particleIndex = 0;

        // Place primary particles at vertices
        vertices.forEach((vertex, i) => {
            for (let j = 0; j < particlesPerVertex; j++) {
                if (particleIndex < this.particles.length) {
                    const particle = this.particles[particleIndex];
                    
                    // Add slight random offset for visual depth
                    const offsetRadius = j * 8; // Spread particles around vertex
                    const offsetAngle = (j / particlesPerVertex) * Math.PI * 2;
                    
                    particle.targetX = vertex.x + Math.cos(offsetAngle) * offsetRadius;
                    particle.targetY = vertex.y + Math.sin(offsetAngle) * offsetRadius;
                    particle.isInFormation = true;
                    particle.formationStrength = 0.3;
                    
                    // Mark as mathematical vertex
                    particle.mathematicalPoint = {
                        vertexIndex: i,
                        originalX: vertex.x,
                        originalY: vertex.y,
                        originalZ: vertex.z || 0,
                        shapeName: shapeData.name,
                        isVertex: true
                    };
                    
                    particleIndex++;
                }
            }
        });

        // Distribute remaining particles
        for (let i = 0; i < extraParticles; i++) {
            if (particleIndex < this.particles.length) {
                const particle = this.particles[particleIndex];
                const vertex = vertices[i % vertexCount];
                
                particle.targetX = vertex.x + (Math.random() - 0.5) * 30;
                particle.targetY = vertex.y + (Math.random() - 0.5) * 30;
                particle.isInFormation = true;
                particle.formationStrength = 0.2;
                
                particle.mathematicalPoint = {
                    vertexIndex: i % vertexCount,
                    originalX: vertex.x,
                    originalY: vertex.y,
                    originalZ: vertex.z || 0,
                    shapeName: shapeData.name,
                    isVertex: false
                };
                
                particleIndex++;
            }
        }

        console.log(`✨ Perfect 3D ${shapeName} created with ${vertexCount} vertices using ${particleIndex} particles`);
        
        // Store shape metadata
        this.currentShapeData = {
            ...shapeData,
            vertices: vertices,
            vertexCount: vertexCount
        };
    }

    createHexagonVertices(centerX, centerY, radius) {
        const vertices = [];
        for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI) / 3; // 60 degrees apart
            vertices.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                z: 0
            });
        }
        return vertices;
    }

    createTriangleVertices(centerX, centerY, radius) {
        const vertices = [];
        for (let i = 0; i < 3; i++) {
            const angle = (i * 2 * Math.PI) / 3 - Math.PI / 2; // Start at top
            vertices.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                z: 0
            });
        }
        return vertices;
    }

    createPentagonVertices(centerX, centerY, radius) {
        const vertices = [];
        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5 - Math.PI / 2;
            vertices.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                z: 0
            });
        }
        return vertices;
    }

    createSquareVertices(centerX, centerY, radius) {
        const vertices = [];
        for (let i = 0; i < 4; i++) {
            const angle = (i * Math.PI) / 2 + Math.PI / 4; // 45° offset for diamond orientation
            vertices.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                z: 0
            });
        }
        return vertices;
    }

    createPolygonVertices(centerX, centerY, radius, sides) {
        const vertices = [];
        for (let i = 0; i < sides; i++) {
            const angle = (i * 2 * Math.PI) / sides - Math.PI / 2;
            vertices.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                z: 0
            });
        }
        return vertices;
    }

    createCubeVertices(centerX, centerY, radius) {
        // Create 3D cube vertices with perspective projection
        const vertices = [];
        const size = radius * 0.8; // Scale for better visibility
        const perspectiveFactor = 300;
        
        // 8 vertices of cube in 3D space - Y is vertical axis
        const cubeVertices3D = [
            // Bottom face (y = -size/2)
            [-size/2, -size/2, -size/2],  // 0: back-left-bottom
            [ size/2, -size/2, -size/2],  // 1: back-right-bottom  
            [ size/2, -size/2,  size/2],  // 2: front-right-bottom
            [-size/2, -size/2,  size/2],  // 3: front-left-bottom
            // Top face (y = size/2)
            [-size/2,  size/2, -size/2],  // 4: back-left-top
            [ size/2,  size/2, -size/2],  // 5: back-right-top
            [ size/2,  size/2,  size/2],  // 6: front-right-top
            [-size/2,  size/2,  size/2],  // 7: front-left-top
        ];
        
        // Project 3D vertices to 2D with perspective
        cubeVertices3D.forEach(([x, y, z]) => {
            const projectedX = (x * perspectiveFactor) / (perspectiveFactor + z);
            const projectedY = (y * perspectiveFactor) / (perspectiveFactor + z);
            
            vertices.push({
                x: centerX + projectedX,
                y: centerY + projectedY,
                z: z
            });
        });
        
        return vertices;
    }

    createPyramidVertices(centerX, centerY, radius) {
        // Create 3D pyramid (tetrahedron) vertices with perspective projection
        const vertices = [];
        const size = radius * 0.8;
        const height = size * Math.sqrt(2/3); // Proper tetrahedron height
        const perspectiveFactor = 300;
        
        // 4 vertices of tetrahedron in 3D space - Y is vertical axis
        const pyramidVertices3D = [
            // Base triangle vertices (at y = -height/3)
            [-size/2, -height/3, -size/(2*Math.sqrt(3))], // Base vertex 1
            [ size/2, -height/3, -size/(2*Math.sqrt(3))], // Base vertex 2
            [0, -height/3, size/Math.sqrt(3)],            // Base vertex 3
            // Apex
            [0, height*2/3, 0]                            // Apex vertex (top)
        ];
        
        // Project 3D vertices to 2D with perspective
        pyramidVertices3D.forEach(([x, y, z]) => {
            const projectedX = (x * perspectiveFactor) / (perspectiveFactor + z);
            const projectedY = (y * perspectiveFactor) / (perspectiveFactor + z);
            
            vertices.push({
                x: centerX + projectedX,
                y: centerY + projectedY,
                z: z
            });
        });
        
        return vertices;
    }

    createConeVertices(centerX, centerY, radius) {
        /**
         * Create 3D Cone Wireframe Vertices with Perspective Projection
         * 
         * Why: Generates mathematical cone with circular base and apex for 3D visualization
         * Where: Called when cone shapes are detected in shape generation
         * How: Creates circular base vertices and apex, applies perspective projection
         */
        const vertices = [];
        const size = radius * 0.8;
        const height = size * 0.8;
        const baseRadius = size / 2;
        const numBasePoints = 12; // Circular base resolution
        const perspectiveFactor = 300;
        
        // Generate circular base vertices in 3D (at y = -height/2)
        for (let i = 0; i < numBasePoints; i++) {
            const angle = (2 * Math.PI * i) / numBasePoints;
            const x = baseRadius * Math.cos(angle);
            const z = baseRadius * Math.sin(angle);
            const y = -height / 2;
            
            // Apply perspective projection
            const projectedX = (x * perspectiveFactor) / (perspectiveFactor + z);
            const projectedY = (y * perspectiveFactor) / (perspectiveFactor + z);
            
            vertices.push({
                x: centerX + projectedX,
                y: centerY + projectedY,
                z: z
            });
        }
        
        // Add apex vertex (at y = height/2)
        const apexY = height / 2;
        vertices.push({
            x: centerX,
            y: centerY + apexY,
            z: 0
        });
        
        return vertices;
    }

    createCylinderVertices(centerX, centerY, radius) {
        /**
         * Create 3D Cylinder Wireframe Vertices with Perspective Projection
         * 
         * Why: Generates mathematical cylinder with top and bottom circles for 3D visualization
         * Where: Called when cylinder/tube shapes are detected in shape generation
         * How: Creates two circular ends connected by vertical lines, applies perspective
         */
        const vertices = [];
        const size = radius * 0.8;
        const height = size * 0.8;
        const cylRadius = size * 0.6;
        const numCirclePoints = 10; // Circle resolution
        const perspectiveFactor = 300;
        
        // Generate bottom circle vertices (at y = -height/2)
        for (let i = 0; i < numCirclePoints; i++) {
            const angle = (2 * Math.PI * i) / numCirclePoints;
            const x = cylRadius * Math.cos(angle);
            const z = cylRadius * Math.sin(angle);
            const y = -height / 2;
            
            const projectedX = (x * perspectiveFactor) / (perspectiveFactor + z);
            const projectedY = (y * perspectiveFactor) / (perspectiveFactor + z);
            
            vertices.push({
                x: centerX + projectedX,
                y: centerY + projectedY,
                z: z
            });
        }
        
        // Generate top circle vertices (at y = height/2)
        for (let i = 0; i < numCirclePoints; i++) {
            const angle = (2 * Math.PI * i) / numCirclePoints;
            const x = cylRadius * Math.cos(angle);
            const z = cylRadius * Math.sin(angle);
            const y = height / 2;
            
            const projectedX = (x * perspectiveFactor) / (perspectiveFactor + z);
            const projectedY = (y * perspectiveFactor) / (perspectiveFactor + z);
            
            vertices.push({
                x: centerX + projectedX,
                y: centerY + projectedY,
                z: z
            });
        }
        
        return vertices;
    }

    create3DSphereVertices(centerX, centerY, radius) {
        /**
         * Create 3D Sphere Wireframe Vertices with Latitude/Longitude Lines
         * 
         * Why: Generates true 3D sphere wireframe using spherical coordinates for realistic visualization
         * Where: Called when 3D sphere shapes are detected in shape generation
         * How: Uses spherical coordinates (theta, phi) to create latitude/longitude grid
         */
        const vertices = [];
        const sphereRadius = radius * 0.7;
        const latSegments = 6; // Latitude lines
        const lonSegments = 8; // Longitude lines
        const perspectiveFactor = 300;
        
        // Generate sphere vertices using spherical coordinates
        for (let lat = 0; lat <= latSegments; lat++) {
            const theta = (lat / latSegments) * Math.PI; // 0 to π (latitude)
            
            for (let lon = 0; lon < lonSegments; lon++) {
                const phi = (lon / lonSegments) * 2 * Math.PI; // 0 to 2π (longitude)
                
                // Convert spherical to cartesian coordinates - Y is vertical
                const x = sphereRadius * Math.sin(theta) * Math.cos(phi);
                const y = sphereRadius * Math.cos(theta);
                const z = sphereRadius * Math.sin(theta) * Math.sin(phi);
                
                // Apply perspective projection
                const projectedX = (x * perspectiveFactor) / (perspectiveFactor + z);
                const projectedY = (y * perspectiveFactor) / (perspectiveFactor + z);
                
                vertices.push({
                    x: centerX + projectedX,
                    y: centerY + projectedY,
                    z: z
                });
            }
        }
        
        return vertices;
    }

    createStarVertices(centerX, centerY, radius, starPoints = 5) {
        /**
         * Create Star Polygon Vertices
         * 
         * Why: Generates beautiful star shapes with alternating outer and inner points
         * Where: Called when star shapes are detected in shape generation
         * How: Creates alternating outer/inner vertices using trigonometry
         */
        const vertices = [];
        const outerRadius = radius;
        const innerRadius = radius * 0.4; // Inner points at 40% of outer radius
        const vertexCount = starPoints * 2; // Each star point creates 2 vertices
        
        for (let i = 0; i < vertexCount; i++) {
            const angle = (2 * Math.PI * i) / vertexCount - Math.PI / 2; // Start at top
            
            // Alternate between outer and inner radius
            const currentRadius = (i % 2 === 0) ? outerRadius : innerRadius;
            
            vertices.push({
                x: centerX + Math.cos(angle) * currentRadius,
                y: centerY + Math.sin(angle) * currentRadius,
                z: 0
            });
        }
        
        return vertices;
    }

    createCircleVertices(centerX, centerY, radius) {
        // Create vertices around a circle for sphere representation
        const vertices = [];
        const numPoints = 12; // Circle points for smooth sphere
        
        for (let i = 0; i < numPoints; i++) {
            const angle = (i * 2 * Math.PI) / numPoints;
            vertices.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                z: 0
            });
        }
        return vertices;
    }

    createSpiralVertices(centerX, centerY, radius, properties) {
        // Create 3D helix spiral vertices with depth and perspective projection
        const vertices = [];
        const turns = properties.turns || 3;
        const numPoints = properties.point_count || 60;
        const spiralType = properties.spiral_type || 'archimedean';
        const helixHeight = radius * 0.8; // Total height of the helix
        const perspectiveFactor = 300; // Perspective projection strength
        
        for (let i = 0; i < numPoints; i++) {
            const t = (i / numPoints) * turns * 2 * Math.PI;
            const progress = i / numPoints; // 0 to 1 progression along spiral
            let r, angle;
            
            if (spiralType === 'fibonacci') {
                // Fibonacci spiral (golden ratio)
                const phi = (1 + Math.sqrt(5)) / 2; // Golden ratio
                r = Math.sqrt(i) * (radius / Math.sqrt(numPoints)) * phi;
                angle = i * (137.508 * Math.PI / 180); // Golden angle in radians
            } else {
                // Archimedean spiral (constant spacing)
                r = progress * radius;
                angle = t;
            }
            
            // Create 3D helix coordinates - Y is vertical, X/Z horizontal
            const x3d = r * Math.cos(angle);  // X is horizontal circular motion
            const y3d = (progress - 0.5) * helixHeight;  // Y is vertical axis (screen vertical)
            const z3d = r * Math.sin(angle);  // Z is horizontal circular motion (depth)
            
            // Apply perspective projection for 3D depth effect
            const projectedX = (x3d * perspectiveFactor) / (perspectiveFactor + z3d);
            const projectedY = (y3d * perspectiveFactor) / (perspectiveFactor + z3d);
            
            vertices.push({
                x: centerX + projectedX,
                y: centerY + projectedY,
                z: z3d // Keep original z for rotation calculations
            });
        }
        return vertices;
    }

    createFractalVertices(centerX, centerY, radius, properties) {
        // Create 3D fractal vertices (Koch snowflake with depth variation)
        const vertices = [];
        const iterations = properties.iterations || 3;
        const baseSize = radius * 0.8;
        const maxDepth = radius * 0.3; // Maximum Z variation for 3D effect
        const perspectiveFactor = 300;
        
        // Start with triangle base
        const startTriangle = [
            { x: -baseSize, y: baseSize/2, z: 0 },
            { x: baseSize, y: baseSize/2, z: 0 },
            { x: 0, y: -baseSize * Math.sqrt(3)/2, z: 0 }
        ];
        
        // For simplicity, approximate fractal with many small segments
        const segments = Math.pow(4, iterations); // Each iteration quadruples segments
        
        startTriangle.forEach((vertex, vertexIndex) => {
            const nextVertex = startTriangle[(vertexIndex + 1) % 3];
            
            // Create fractal-like segments between vertices
            for (let i = 0; i <= segments/3; i++) {
                const t = i / (segments/3);
                const baseX = vertex.x + t * (nextVertex.x - vertex.x);
                const baseY = vertex.y + t * (nextVertex.y - vertex.y);
                
                // Add fractal-like noise/bumps with 3D depth
                const noiseAmplitude = baseSize * 0.1 / (iterations + 1);
                const noiseX = (Math.random() - 0.5) * noiseAmplitude;
                const noiseY = (Math.random() - 0.5) * noiseAmplitude;
                const noiseZ = (Math.random() - 0.5) * maxDepth; // Add Z variation
                
                // Apply perspective projection for 3D effect
                const x3d = baseX + noiseX;
                const y3d = baseY + noiseY;
                const z3d = noiseZ;
                
                const projectedX = (x3d * perspectiveFactor) / (perspectiveFactor + z3d);
                const projectedY = (y3d * perspectiveFactor) / (perspectiveFactor + z3d);
                
                vertices.push({
                    x: centerX + projectedX,
                    y: centerY + projectedY,
                    z: z3d
                });
            }
        });
        
        return vertices;
    }

    createDNAVertices(centerX, centerY, radius, properties) {
        // Create DNA double helix vertices with 3D perspective
        const vertices = [];
        const turns = properties.turns || 2.5;
        const numPoints = properties.point_count || 80;
        // Height should be proportional to screen, not radius, to keep DNA centered and visible
        const helixHeight = Math.min(this.canvas.height * 0.6, radius * 2.5); // Keep DNA within 60% of screen height
        const helixRadius = radius * 1.2; // Much larger radius for prominent DNA structure
        const perspectiveFactor = 300;
        
        for (let i = 0; i < numPoints; i++) {
            const t = (i / numPoints) * turns * 2 * Math.PI;
            const progress = i / numPoints; // 0 to 1 progression along helix
            
            // Vertical position along the helix
            const yPos = (progress - 0.5) * helixHeight;
            
            // First helix strand (backbone 1)
            const x1_3d = helixRadius * Math.cos(t);
            const z1_3d = helixRadius * Math.sin(t);
            
            // Second helix strand (backbone 2) - 180° phase shift
            const x2_3d = helixRadius * Math.cos(t + Math.PI);
            const z2_3d = helixRadius * Math.sin(t + Math.PI);
            
            // Apply perspective projection for 3D effect
            const x1_proj = (x1_3d * perspectiveFactor) / (perspectiveFactor + z1_3d);
            const x2_proj = (x2_3d * perspectiveFactor) / (perspectiveFactor + z2_3d);
            
            // Add backbone vertices
            vertices.push(
                {
                    x: centerX + x1_proj,
                    y: centerY + yPos,
                    z: z1_3d,
                    strand: 'backbone1'
                },
                {
                    x: centerX + x2_proj,
                    y: centerY + yPos,
                    z: z2_3d,
                    strand: 'backbone2'
                }
            );
            
            // Add base pairs (connecting rungs) every 6th point
            if (i % 6 === 0) {
                const baseSteps = 4; // Points between strands for base pair
                for (let step = 1; step < baseSteps; step++) {
                    const stepRatio = step / baseSteps;
                    
                    // Interpolate between the two strands
                    const base_x3d = x1_3d + stepRatio * (x2_3d - x1_3d);
                    const base_z3d = z1_3d + stepRatio * (z2_3d - z1_3d);
                    const base_x_proj = (base_x3d * perspectiveFactor) / (perspectiveFactor + base_z3d);
                    
                    vertices.push({
                        x: centerX + base_x_proj,
                        y: centerY + yPos,
                        z: base_z3d,
                        strand: 'base_pair'
                    });
                }
            }
        }
        
        return vertices;
    }

    createHelixFormation() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(this.canvas.width, this.canvas.height) * 0.15;
        const height = Math.min(this.canvas.width, this.canvas.height) * 0.3;
        
        this.particles.forEach((particle, index) => {
            const t = (index / this.particles.length) * Math.PI * 4;
            const y_offset = (index / this.particles.length) * height - height / 2;
            
            particle.targetX = centerX + radius * Math.cos(t);
            particle.targetY = centerY + y_offset + radius * 0.2 * Math.sin(t * 2);
            particle.isInFormation = true;
            particle.formationStrength = 0.12;
        });
    }
    
    createConstellationFormation() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const clusters = 5;
        
        this.particles.forEach((particle, index) => {
            const clusterIndex = Math.floor(index / (this.particles.length / clusters));
            const clusterAngle = (clusterIndex / clusters) * Math.PI * 2;
            const clusterRadius = Math.min(this.canvas.width, this.canvas.height) * 0.25;
            
            const clusterX = centerX + Math.cos(clusterAngle) * clusterRadius;
            const clusterY = centerY + Math.sin(clusterAngle) * clusterRadius;
            
            const spread = 50;
            particle.targetX = clusterX + (Math.random() - 0.5) * spread;
            particle.targetY = clusterY + (Math.random() - 0.5) * spread;
            particle.isInFormation = true;
            particle.formationStrength = 0.08;
        });
    }
    
    releaseFormation() {
        this.particles.forEach(particle => {
            particle.isInFormation = false;
            particle.formationStrength = 0;
            
            // Clear mathematical shape properties to restore idle rotation
            particle.mathematicalPoint = false;
            
            // Reset rotation properties for idle state
            particle.rotationSpeed = (Math.random() - 0.5) * 0.02;
            particle.rotationRadius = Math.random() * 20;
        });
        console.log('🌀 Formation released, particles restored to idle rotation');
    }
    
    /**
     * Render Connection Lines Between Nearby Particles
     * 
     * Why: Creates visible neural network connections that make formations more clear
     * Where: Called during animation loop before particle rendering
     * How: Draws lines between particles within connection distance with opacity based on proximity
     * 
     * Connects to:
     *     - animate(): Called during each animation frame
     *     - Particle.distanceTo(): Uses particle distance calculation
     *     - VISUAL_THEMES: Uses current mode colors for connection styling
     */
    renderConnections() {
        const connectionDistance = 120; // Maximum distance for connections
        const maxOpacity = 0.6;
        const theme = VISUAL_THEMES[this.currentMode] || VISUAL_THEMES.idle;
        
        this.ctx.save();
        
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const particle1 = this.particles[i];
                const particle2 = this.particles[j];
                const distance = particle1.distanceTo(particle2);
                
                if (distance < connectionDistance) {
                    // Calculate connection opacity based on distance
                    const opacity = maxOpacity * (1 - distance / connectionDistance);
                    
                    // Use theme color for connections
                    const connectionColor = theme.colors[0]; // Primary theme color
                    
                    this.ctx.strokeStyle = connectionColor;
                    this.ctx.globalAlpha = opacity * 0.4; // Subtle connections
                    this.ctx.lineWidth = 1;
                    
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle1.x, particle1.y);
                    this.ctx.lineTo(particle2.x, particle2.y);
                    this.ctx.stroke();
                }
            }
        }
        
        this.ctx.restore();
    }
    
    animate() {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        let frameCount = 0;
        
        const animateFrame = () => {
            frameCount++;
            
            // Clear canvas with subtle fade for smoother trails
            this.ctx.fillStyle = '#0B0F14';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            
            // Add cognitive background grid for depth
            this.renderCognitiveGrid(frameCount);
            
            // Update particles
            this.particles.forEach(particle => {
                particle.update();
            });
            
            // Render connection lines between nearby particles
            this.renderConnections();
            
            // Render particles
            this.particles.forEach(particle => {
                particle.render(this.ctx);
            });
            
            // Add central cognitive pulse for idle state
            if (this.currentMode === 'idle' || this.currentMode === 'observing') {
                this.renderCognitiveCore(frameCount);
            }
            
            this.animationId = requestAnimationFrame(animateFrame);
        };
        
        animateFrame();
        console.log('🧠 Cognitive animation started with enhanced visualization');
    }

    /**
     * Render Cognitive Grid Background
     * 
     * Why: Provides subtle spatial reference and depth for cognitive visualization
     * Where: Called during animation loop to create immersive background
     * How: Animated grid with breathing effect synchronized to cognitive state
     */
    renderCognitiveGrid(frameCount) {
        const theme = VISUAL_THEMES[this.currentMode] || VISUAL_THEMES.idle;
        const breathe = Math.sin(frameCount * 0.01) * 0.1 + 0.9;
        
        this.ctx.save();
        this.ctx.globalAlpha = 0.05 * breathe;
        this.ctx.strokeStyle = theme.colors[0];
        this.ctx.lineWidth = 1;
        
        const gridSize = 50;
        for (let x = 0; x < this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y < this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }

    /**
     * Render Central Cognitive Core
     * 
     * Why: Visual representation of Clever's central processing during idle states
     * Where: Called during idle/observing animation loops for cognitive presence
     * How: Pulsing central glow with synchronized breathing pattern
     */
    renderCognitiveCore(frameCount) {
        const theme = VISUAL_THEMES[this.currentMode] || VISUAL_THEMES.idle;
        const pulse = Math.sin(frameCount * 0.02) * 0.3 + 0.7;
        
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const coreRadius = 15 * pulse;
        
        this.ctx.save();
        
        // Create radial gradient for core
        const gradient = this.ctx.createRadialGradient(
            centerX, centerY, 0,
            centerX, centerY, coreRadius * 3
        );
        gradient.addColorStop(0, theme.colors[0] + '40');
        gradient.addColorStop(0.5, theme.colors[1] + '20');
        gradient.addColorStop(1, theme.colors[2] + '00');
        
        // Draw cognitive core
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, coreRadius * 3, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw inner core
        this.ctx.fillStyle = theme.colors[0] + '60';
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, coreRadius, 0, Math.PI * 2);
        this.ctx.fill();
        
        this.ctx.restore();
    }
    
    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        this.isAnimating = false;
        console.log('Animation stopped');
    }
    
    resize(width, height) {
        const oldWidth = this.canvas.width;
        const oldHeight = this.canvas.height;
        
        this.canvas.width = width;
        this.canvas.height = height;
        
        // Scale particle positions
        const scaleX = width / oldWidth;
        const scaleY = height / oldHeight;
        
        this.particles.forEach(particle => {
            particle.x *= scaleX;
            particle.y *= scaleY;
            particle.targetX *= scaleX;
            particle.targetY *= scaleY;
        });
        
        console.log('Chamber resized to', width, 'x', height);
    }
    
    /**
     * Start Shape Rotation Sequence
     * 
     * Why: Provides mesmerizing 720° rotation (2 full rotations) for mathematical shapes
     * Where: Called after shape formation completes to showcase geometric beauty
     * How: Applies smooth rotation transformation to all mathematical shape particles
     */
    startShapeRotation() {
        // Find ALL mathematical shape particles
        const mathParticles = this.particles.filter(p => p.mathematicalPoint);
        console.log(`Found ${mathParticles.length} particles for 3D rotation`);
        
        if (mathParticles.length === 0) {
            console.warn('No mathematical particles found for rotation');
            return;
        }
        
        // Detect shape type to choose appropriate rotation
        const shapeType = this.currentShapeData?.name?.toLowerCase() || 'unknown';
        const isDNA = shapeType.includes('dna') || shapeType.includes('helix');
        
        console.log(`🎡 Starting 3D rotation for ${shapeType}: ${isDNA ? 'drill/screw style' : 'ferris wheel style'}`);
        
        // Store original positions from mathematical points
        mathParticles.forEach(particle => {
            if (particle.mathematicalPoint) {
                particle.originalTargetX = particle.mathematicalPoint.originalX;
                particle.originalTargetY = particle.mathematicalPoint.originalY;
                particle.originalTargetZ = particle.mathematicalPoint.originalZ || 0;
            }
        });
        
        // Rotation parameters
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const totalRotation = Math.PI * 4; // 720 degrees (2 full rotations)
        const rotationDuration = isDNA ? 6000 : 8000; // Faster for DNA (6s vs 8s)
        const startTime = Date.now();
        
        this.isRotatingShape = true;
        
        // Choose rotation style based on shape type
        const rotateShape = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / rotationDuration, 1);
            
            // Smooth easing
            const easeInOutQuad = t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
            const easedProgress = easeInOutQuad(progress);
            
            const currentAngle = totalRotation * easedProgress;
            
            if (isDNA) {
                // DNA: Rotate around vertical Z-axis (like a drill/screw)
                mathParticles.forEach(particle => {
                    const relX = particle.originalTargetX - centerX;
                    const relY = particle.originalTargetY - centerY;
                    const relZ = particle.originalTargetZ || 0;
                    
                    // Rotation around Z-axis (drill motion) - X and Y rotate, Z stays same
                    const rotatedX = relX * Math.cos(currentAngle) - relY * Math.sin(currentAngle);
                    const rotatedY = relX * Math.sin(currentAngle) + relY * Math.cos(currentAngle);
                    
                    // Apply perspective for depth effect
                    const perspective = 800;
                    const projectedScale = perspective / (perspective + relZ);
                    
                    particle.targetX = centerX + (rotatedX * projectedScale);
                    particle.targetY = centerY + (rotatedY * projectedScale);
                    
                    // Depth-based scaling
                    const depthScale = 0.6 + (0.4 * projectedScale);
                    particle.scale = depthScale;
                });
            } else {
                // Other shapes: Ferris wheel rotation (around Y-axis)
                mathParticles.forEach(particle => {
                    const relX = particle.originalTargetX - centerX;
                    const relY = particle.originalTargetY - centerY;
                    const relZ = particle.originalTargetZ || 0;
                    
                    // 3D rotation around Y-axis (vertical ferris wheel motion)
                    // X and Z rotate, Y stays relatively the same
                    const rotatedX = relX * Math.cos(currentAngle) + relZ * Math.sin(currentAngle);
                    const rotatedZ = -relX * Math.sin(currentAngle) + relZ * Math.cos(currentAngle);
                    
                    // Apply perspective projection for 3D effect
                    const perspective = 800;
                    const projectedScale = perspective / (perspective + rotatedZ);
                    
                    particle.targetX = centerX + (rotatedX * projectedScale);
                    particle.targetY = centerY + (relY * projectedScale);
                    
                    // Add depth-based opacity/size effect (closer = brighter)
                    const depthScale = 0.6 + (0.4 * projectedScale);
                    particle.scale = depthScale;
                });
            }
            
            // Continue rotation until complete
            if (progress < 1) {
                requestAnimationFrame(rotateShape);
            } else {
                const rotationType = isDNA ? 'drill/screw motion' : 'ferris wheel motion';
                console.log(`✅ 3D rotation completed (720° ${rotationType})`);
                this.isRotatingShape = false;
                
                // Restore original positions
                mathParticles.forEach(particle => {
                    particle.targetX = particle.originalTargetX;
                    particle.targetY = particle.originalTargetY;
                    particle.scale = 1.0; // Reset scale
                });
            }
        };
        
        // Start rotation animation
        requestAnimationFrame(rotateShape);
    }
}

/**
 * Global initialization function
 */
window.startHolographicChamber = function(canvas) {
    try {
        if (!canvas || !(canvas instanceof HTMLCanvasElement)) {
            console.error('Invalid canvas provided to startHolographicChamber');
            return null;
        }
        
        const chamber = new HolographicChamber(canvas);
        chamber.setMode('idle');
        
        console.log('✅ Holographic chamber ready for cognitive visualization');
        return chamber;
        
    } catch (error) {
        console.error('Failed to start holographic chamber:', error);
        return null;
    }
};

console.log('🌟 Holographic Chamber engine loaded and ready');
