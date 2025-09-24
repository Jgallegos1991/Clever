/**
 * Holographic Chamber - Particle System for Clever AI
 * 
 * Why: Creates cognitive visualization representing Clever's thought processes
 * Where: Core particle engine loaded by templates/index.html before main.js
 * How: Canvas-based particle physics with formation morphing and animations
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
        energy: 0.3,
        formation: 'sphere'
    },
    thinking: {
        colors: ['#00FF88', '#00FFFF', '#88FFFF'],
        energy: 0.7,
        formation: 'helix'
    },
    creative: {
        colors: ['#FF6B9D', '#C44569', '#F8B500'],
        energy: 0.9,
        formation: 'constellation'
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
        
        // Visual properties
        this.opacity = Math.random() * 0.5 + 0.5;
        this.colorIndex = Math.floor(Math.random() * 3);
    }
    
    update() {
        // Formation behavior
        if (this.isInFormation) {
            const dx = this.targetX - this.x;
            const dy = this.targetY - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > 1) {
                this.vx += dx * this.formationStrength * 0.01;
                this.vy += dy * this.formationStrength * 0.01;
            }
        }
        
        // Free movement
        if (!this.isInFormation) {
            this.vx += (Math.random() - 0.5) * 0.02;
            this.vy += (Math.random() - 0.5) * 0.02;
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
        
        ctx.save();
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
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
        
        this.createParticles();
        console.log('Chamber initialized with', this.particles.length, 'particles');
    }
    
    createParticles() {
        this.particles = [];
        const particleCount = 60;
        
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
            console.log('Switching to mode:', mode);
            this.currentMode = mode;
            const theme = VISUAL_THEMES[mode];
            
            // Update particle energy
            this.particles.forEach(particle => {
                particle.energy = Math.random() * theme.energy + (1 - theme.energy) * 0.5;
            });
            
            // Morph formation
            if (theme.formation !== this.currentFormation) {
                this.morphToFormation(theme.formation);
            }
        }
    }
    
    morphToFormation(formationType) {
        console.log('Morphing to formation:', formationType);
        this.currentFormation = formationType;
        
        switch (formationType) {
            case 'sphere':
                this.createSphereFormation();
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
        });
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
        
        const animateFrame = () => {
            // Clear canvas completely (no trails)
            this.ctx.fillStyle = '#0B0F14';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            
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
            
            this.animationId = requestAnimationFrame(animateFrame);
        };
        
        animateFrame();
        console.log('Animation started');
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
