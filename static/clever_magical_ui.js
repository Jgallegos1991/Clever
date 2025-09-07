// CLEVER AI - ULTIMATE BADASS UI SYSTEM
// The smartest, most magical interface ever created
// 30k+ particles, form-reactive intelligence, pure magic

class CleverMagicalUI {
    constructor() {
        this.isInitialized = false;
        this.particleSystem = null;
        this.intelligenceLevel = 0;
        this.formMode = 'idle';
        this.currentEmotion = 'curious';
        this.conversationContext = [];
        this.adaptiveResponses = new Map();
        
        // Magical states
        this.states = {
            idle: { color: [0.4, 0.8, 1.0], energy: 0.3, pattern: 'sphere' },
            thinking: { color: [1.0, 0.6, 0.8], energy: 0.8, pattern: 'neural' },
            responding: { color: [0.6, 1.0, 0.4], energy: 0.9, pattern: 'wave' },
            excited: { color: [1.0, 0.8, 0.2], energy: 1.0, pattern: 'explosion' },
            focused: { color: [0.8, 0.4, 1.0], energy: 0.7, pattern: 'tunnel' },
            creative: { color: [1.0, 0.4, 0.6], energy: 0.85, pattern: 'spiral' }
        };
        
        this.currentState = this.states.idle;
        this.targetState = this.states.idle;
        this.stateTransition = 0;
    }

    initialize(canvas) {
        console.log('🧠 Initializing Clever Magical UI System...');
        
        // Setup WebGL with maximum badassery
        this.canvas = canvas;
        this.gl = canvas.getContext('webgl2', {
            alpha: true,
            antialias: true,
            powerPreference: 'high-performance'
        });
        
        if (!this.gl) {
            throw new Error('WebGL2 required for maximum badassery');
        }
        
        // Initialize the particle system with intelligence
        this.particleSystem = new IntelligentParticleSystem(this.gl);
        this.setupEventListeners();
        this.startMagicalLoop();
        
        this.isInitialized = true;
        console.log('✨ Clever UI System: READY TO BE BADASS');
        
        // Initial magical entrance
        this.triggerStateTransition('excited', 2000);
        setTimeout(() => this.triggerStateTransition('idle'), 2000);
    }

    setupEventListeners() {
        // Mouse interaction - particles follow and react
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width * 2 - 1;
            const y = -((e.clientY - rect.top) / rect.height * 2 - 1);
            
            this.particleSystem.setAttractor(x, y, 0.8);
            this.onUserInteraction('mouse_move', { x, y });
        });

        // Click events - major particle reactions
        this.canvas.addEventListener('click', (e) => {
            this.triggerPulse(1.5);
            this.onUserInteraction('click');
        });

        // Keyboard events - show intelligence
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                this.onUserTyping(e.key);
            }
        });
    }

    onUserInteraction(type, data = {}) {
        // Adaptive UI responses based on interaction patterns
        switch(type) {
            case 'mouse_move':
                if (this.formMode === 'idle') {
                    this.triggerStateTransition('curious', 500);
                }
                break;
            case 'click':
                this.triggerStateTransition('excited', 800);
                break;
            case 'typing':
                this.triggerStateTransition('thinking', 300);
                break;
        }
    }

    onUserTyping(key) {
        // React to typing with intelligence
        if (key === 'Backspace') {
            this.particleSystem.createRipple(-0.3);
        } else if (key === 'Enter') {
            this.triggerStateTransition('responding', 1000);
        } else if (key.length === 1) {
            this.particleSystem.addEnergyPulse(0.1);
            this.triggerStateTransition('thinking', 200);
        }
    }

    triggerStateTransition(stateName, duration = 1000) {
        if (this.states[stateName]) {
            this.targetState = this.states[stateName];
            this.stateTransition = 0;
            this.transitionDuration = duration;
            
            // Update particle system
            this.particleSystem.morphToPattern(this.targetState.pattern);
            this.particleSystem.setEnergyLevel(this.targetState.energy);
        }
    }

    triggerPulse(intensity = 1.0) {
        this.particleSystem.triggerPulse(intensity);
    }

    // Form-specific reactions
    onFormFocus() {
        this.formMode = 'focused';
        this.triggerStateTransition('focused', 600);
        this.particleSystem.createFormFocusEffect();
    }

    onFormInput(text) {
        // Analyze input for intelligent reactions
        const sentiment = this.analyzeSentiment(text);
        const complexity = this.analyzeComplexity(text);
        
        if (complexity > 0.7) {
            this.triggerStateTransition('thinking', 800);
        } else if (sentiment > 0.5) {
            this.triggerStateTransition('excited', 600);
        } else {
            this.triggerStateTransition('curious', 400);
        }
        
        // Dynamic particle count based on content complexity
        const targetCount = Math.floor(20000 + (complexity * 10000));
        this.particleSystem.adjustParticleCount(targetCount);
    }

    onCleverResponse(response, metadata) {
        // React to Clever's responses with appropriate magic
        const emotion = metadata.emotion || 'neutral';
        const confidence = metadata.confidence || 0.5;
        
        switch(emotion) {
            case 'excited':
                this.triggerStateTransition('excited', 1500);
                break;
            case 'thoughtful':
                this.triggerStateTransition('thinking', 2000);
                break;
            case 'creative':
                this.triggerStateTransition('creative', 1800);
                break;
            default:
                this.triggerStateTransition('responding', 1200);
        }
        
        // Confidence-based visual effects
        this.particleSystem.setConfidenceLevel(confidence);
    }

    analyzeSentiment(text) {
        // Simple sentiment analysis for UI reactions
        const positive = ['amazing', 'awesome', 'great', 'excellent', 'fantastic', 'love', 'perfect'];
        const negative = ['bad', 'terrible', 'awful', 'hate', 'horrible', 'wrong'];
        
        let score = 0.5; // neutral
        const words = text.toLowerCase().split(' ');
        
        words.forEach(word => {
            if (positive.includes(word)) score += 0.2;
            if (negative.includes(word)) score -= 0.2;
        });
        
        return Math.max(0, Math.min(1, score));
    }

    analyzeComplexity(text) {
        // Analyze text complexity for appropriate UI response
        const words = text.split(' ').length;
        const sentences = text.split(/[.!?]+/).length;
        const avgWordLength = text.replace(/\s/g, '').length / words;
        
        let complexity = 0;
        complexity += Math.min(words / 50, 1) * 0.4; // word count
        complexity += Math.min(sentences / 5, 1) * 0.3; // sentence count  
        complexity += Math.min(avgWordLength / 8, 1) * 0.3; // word complexity
        
        return complexity;
    }

    startMagicalLoop() {
        const animate = (timestamp) => {
            if (!this.isInitialized) return;
            
            // Update state transitions
            if (this.stateTransition < 1) {
                this.stateTransition = Math.min(1, this.stateTransition + 0.016);
                this.interpolateStates();
            }
            
            // Update particle system
            if (this.particleSystem) {
                this.particleSystem.update(timestamp);
                this.particleSystem.render();
            }
            
            requestAnimationFrame(animate);
        };
        
        requestAnimationFrame(animate);
    }

    interpolateStates() {
        // Smooth interpolation between states
        const t = this.easeInOutCubic(this.stateTransition);
        
        this.currentState = {
            color: this.lerpColor(this.currentState.color, this.targetState.color, t),
            energy: this.lerp(this.currentState.energy, this.targetState.energy, t),
            pattern: this.targetState.pattern
        };
        
        this.particleSystem.updateVisualState(this.currentState);
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
    }

    lerp(a, b, t) {
        return a + (b - a) * t;
    }

    lerpColor(colorA, colorB, t) {
        return [
            this.lerp(colorA[0], colorB[0], t),
            this.lerp(colorA[1], colorB[1], t),
            this.lerp(colorA[2], colorB[2], t)
        ];
    }

    // Public API for integration
    setIntelligenceMode(mode) {
        const modeMap = {
            'creative': 'creative',
            'analytical': 'focused', 
            'supportive': 'excited',
            'deep_dive': 'thinking'
        };
        
        if (modeMap[mode]) {
            this.triggerStateTransition(modeMap[mode], 1000);
        }
    }

    showProcessing() {
        this.triggerStateTransition('thinking', 2000);
    }

    showComplete() {
        this.triggerStateTransition('excited', 800);
        setTimeout(() => this.triggerStateTransition('idle'), 1500);
    }

    // Integration with chat system
    integrateChatEvents() {
        // Hook into form events
        const chatForm = document.querySelector('#chat-form');
        const messageInput = document.querySelector('#message-input');
        
        if (messageInput) {
            messageInput.addEventListener('focus', () => this.onFormFocus());
            messageInput.addEventListener('input', (e) => this.onFormInput(e.target.value));
        }
        
        if (chatForm) {
            chatForm.addEventListener('submit', () => {
                this.showProcessing();
            });
        }
        
        // Hook into response events
        window.addEventListener('clever-response', (e) => {
            this.onCleverResponse(e.detail.response, e.detail.metadata);
        });
    }
}

// Intelligent Particle System
class IntelligentParticleSystem {
    constructor(gl) {
        this.gl = gl;
        this.particleCount = 30000; // More particles for maximum badassery
        this.positions = new Float32Array(this.particleCount * 3);
        this.velocities = new Float32Array(this.particleCount * 3);
        this.targets = new Float32Array(this.particleCount * 3);
        
        this.setupShaders();
        this.setupBuffers();
        this.initializeParticles();
        
        // Intelligence parameters
        this.attractorPos = [0, 0, 0];
        this.attractorStrength = 0;
        this.energyLevel = 0.3;
        this.confidence = 0.5;
        this.currentPattern = 'sphere';
        this.pulseTime = 0;
    }

    setupShaders() {
        const vertexShader = `#version 300 es
            precision highp float;
            layout(location=0) in vec3 a_position;
            uniform mat4 u_projection;
            uniform float u_time;
            uniform float u_pointSize;
            uniform float u_energy;
            uniform vec3 u_attractor;
            uniform float u_attractorStrength;
            
            void main() {
                vec3 pos = a_position;
                
                // Dynamic rotation based on energy
                float rotSpeed = u_energy * 0.5;
                float angle = u_time * rotSpeed;
                float ca = cos(angle);
                float sa = sin(angle);
                
                // Rotate around Y axis
                pos = vec3(
                    pos.x * ca + pos.z * sa,
                    pos.y,
                    -pos.x * sa + pos.z * ca
                );
                
                // Attractor influence
                vec3 toAttractor = u_attractor - pos;
                float dist = length(toAttractor);
                if (dist > 0.0) {
                    pos += normalize(toAttractor) * u_attractorStrength * (1.0 / (1.0 + dist * 2.0));
                }
                
                vec4 clipPos = u_projection * vec4(pos, 1.0);
                gl_Position = clipPos;
                
                // Energy-based point size
                float baseSize = u_pointSize * (0.5 + u_energy * 1.5);
                float perspective = 1.0 / max(0.001, clipPos.w);
                gl_PointSize = baseSize * clamp(perspective * 2.0, 0.8, 4.0);
            }
        `;

        const fragmentShader = `#version 300 es
            precision highp float;
            out vec4 outColor;
            uniform vec3 u_color;
            uniform float u_energy;
            uniform float u_confidence;
            uniform float u_time;
            
            void main() {
                vec2 p = gl_PointCoord.xy * 2.0 - 1.0;
                float r = length(p);
                
                if (r > 1.0) discard;
                
                // Energy-based glow
                float intensity = 1.0 - r;
                intensity = pow(intensity, 1.5 - u_energy * 0.5);
                
                // Confidence-based brightness variation
                float brightness = 0.3 + u_confidence * 0.7;
                
                // Subtle time-based shimmer
                float shimmer = 0.9 + 0.1 * sin(u_time * 3.0 + r * 10.0);
                
                vec3 color = u_color * brightness * shimmer;
                float alpha = intensity * (0.1 + u_energy * 0.4);
                
                outColor = vec4(color, alpha);
            }
        `;

        this.program = this.createProgram(vertexShader, fragmentShader);
        this.gl.useProgram(this.program);
        
        // Get uniform locations
        this.uniforms = {
            projection: this.gl.getUniformLocation(this.program, 'u_projection'),
            time: this.gl.getUniformLocation(this.program, 'u_time'),
            pointSize: this.gl.getUniformLocation(this.program, 'u_pointSize'),
            energy: this.gl.getUniformLocation(this.program, 'u_energy'),
            color: this.gl.getUniformLocation(this.program, 'u_color'),
            confidence: this.gl.getUniformLocation(this.program, 'u_confidence'),
            attractor: this.gl.getUniformLocation(this.program, 'u_attractor'),
            attractorStrength: this.gl.getUniformLocation(this.program, 'u_attractorStrength')
        };
    }

    setupBuffers() {
        this.buffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, this.positions, this.gl.DYNAMIC_DRAW);
        
        this.gl.enableVertexAttribArray(0);
        this.gl.vertexAttribPointer(0, 3, this.gl.FLOAT, false, 0, 0);
    }

    initializeParticles() {
        // Initialize in sphere formation
        this.morphToPattern('sphere');
    }

    morphToPattern(pattern) {
        this.currentPattern = pattern;
        
        switch(pattern) {
            case 'sphere':
                this.createSphere();
                break;
            case 'neural':
                this.createNeuralNetwork();
                break;
            case 'wave':
                this.createWave();
                break;
            case 'explosion':
                this.createExplosion();
                break;
            case 'tunnel':
                this.createTunnel();
                break;
            case 'spiral':
                this.createSpiral();
                break;
            default:
                this.createSphere();
        }
        
        this.updateBuffers();
    }

    createSphere() {
        for (let i = 0; i < this.particleCount; i++) {
            const phi = Math.acos(2 * Math.random() - 1);
            const theta = 2 * Math.PI * Math.random();
            const radius = 0.8 + Math.random() * 0.4;
            
            const idx = i * 3;
            this.positions[idx] = radius * Math.sin(phi) * Math.cos(theta);
            this.positions[idx + 1] = radius * Math.sin(phi) * Math.sin(theta);
            this.positions[idx + 2] = radius * Math.cos(phi);
        }
    }

    createNeuralNetwork() {
        // Create neural network-like structure
        const layers = 8;
        const nodesPerLayer = Math.floor(this.particleCount / layers);
        
        for (let i = 0; i < this.particleCount; i++) {
            const layer = Math.floor(i / nodesPerLayer);
            const nodeInLayer = i % nodesPerLayer;
            
            const idx = i * 3;
            const z = (layer / layers) * 2 - 1;
            const angle = (nodeInLayer / nodesPerLayer) * Math.PI * 2;
            const radius = 0.3 + Math.random() * 0.7;
            
            this.positions[idx] = radius * Math.cos(angle) + (Math.random() - 0.5) * 0.2;
            this.positions[idx + 1] = radius * Math.sin(angle) + (Math.random() - 0.5) * 0.2;
            this.positions[idx + 2] = z + (Math.random() - 0.5) * 0.1;
        }
    }

    createWave() {
        for (let i = 0; i < this.particleCount; i++) {
            const idx = i * 3;
            const x = (Math.random() - 0.5) * 3;
            const z = (Math.random() - 0.5) * 3;
            const y = Math.sin(x * 2) * Math.cos(z * 2) * 0.3;
            
            this.positions[idx] = x;
            this.positions[idx + 1] = y;
            this.positions[idx + 2] = z;
        }
    }

    createExplosion() {
        for (let i = 0; i < this.particleCount; i++) {
            const idx = i * 3;
            const phi = Math.acos(2 * Math.random() - 1);
            const theta = 2 * Math.PI * Math.random();
            const radius = Math.pow(Math.random(), 0.3) * 2;
            
            this.positions[idx] = radius * Math.sin(phi) * Math.cos(theta);
            this.positions[idx + 1] = radius * Math.sin(phi) * Math.sin(theta);
            this.positions[idx + 2] = radius * Math.cos(phi);
        }
    }

    createTunnel() {
        for (let i = 0; i < this.particleCount; i++) {
            const idx = i * 3;
            const angle = Math.random() * Math.PI * 2;
            const z = (Math.random() - 0.5) * 4;
            const radius = 0.3 + 0.7 * Math.abs(z) / 2;
            
            this.positions[idx] = radius * Math.cos(angle);
            this.positions[idx + 1] = radius * Math.sin(angle);
            this.positions[idx + 2] = z;
        }
    }

    createSpiral() {
        for (let i = 0; i < this.particleCount; i++) {
            const idx = i * 3;
            const t = (i / this.particleCount) * Math.PI * 8;
            const radius = 0.1 + (i / this.particleCount) * 1.2;
            
            this.positions[idx] = radius * Math.cos(t);
            this.positions[idx + 1] = (i / this.particleCount - 0.5) * 2;
            this.positions[idx + 2] = radius * Math.sin(t);
        }
    }

    setAttractor(x, y, strength) {
        this.attractorPos = [x, y, 0];
        this.attractorStrength = strength;
    }

    setEnergyLevel(energy) {
        this.energyLevel = Math.max(0, Math.min(1, energy));
    }

    setConfidenceLevel(confidence) {
        this.confidence = Math.max(0, Math.min(1, confidence));
    }

    triggerPulse(intensity) {
        this.pulseTime = performance.now();
        this.pulseIntensity = intensity;
    }

    updateBuffers() {
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.buffer);
        this.gl.bufferSubData(this.gl.ARRAY_BUFFER, 0, this.positions);
    }

    updateVisualState(state) {
        // Update colors and energy based on state
        this.setEnergyLevel(state.energy);
        this.currentColor = state.color;
    }

    update(timestamp) {
        // Update particle physics here if needed
        this.time = timestamp * 0.001;
        
        // Pulse decay
        if (this.pulseTime) {
            const elapsed = timestamp - this.pulseTime;
            if (elapsed > 2000) {
                this.pulseTime = 0;
                this.pulseIntensity = 0;
            }
        }
    }

    render() {
        const gl = this.gl;
        
        // Setup projection matrix
        const aspect = gl.canvas.width / gl.canvas.height;
        const projMatrix = this.createPerspectiveMatrix(45, aspect, 0.1, 100);
        
        gl.useProgram(this.program);
        
        // Set uniforms
        gl.uniformMatrix4fv(this.uniforms.projection, false, projMatrix);
        gl.uniform1f(this.uniforms.time, this.time);
        gl.uniform1f(this.uniforms.pointSize, 2.0);
        gl.uniform1f(this.uniforms.energy, this.energyLevel);
        gl.uniform3fv(this.uniforms.color, this.currentColor || [0.4, 0.8, 1.0]);
        gl.uniform1f(this.uniforms.confidence, this.confidence);
        gl.uniform3fv(this.uniforms.attractor, this.attractorPos);
        gl.uniform1f(this.uniforms.attractorStrength, this.attractorStrength);
        
        // Render particles
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.drawArrays(gl.POINTS, 0, this.particleCount);
    }

    createProgram(vsSource, fsSource) {
        const gl = this.gl;
        const vs = this.loadShader(gl.VERTEX_SHADER, vsSource);
        const fs = this.loadShader(gl.FRAGMENT_SHADER, fsSource);
        
        const program = gl.createProgram();
        gl.attachShader(program, vs);
        gl.attachShader(program, fs);
        gl.linkProgram(program);
        
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            throw new Error('Shader program failed to link');
        }
        
        return program;
    }

    loadShader(type, source) {
        const gl = this.gl;
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            throw new Error('Shader compilation error: ' + gl.getShaderInfoLog(shader));
        }
        
        return shader;
    }

    createPerspectiveMatrix(fov, aspect, near, far) {
        const f = Math.tan(Math.PI * 0.5 - 0.5 * fov * Math.PI / 180);
        const rangeInv = 1.0 / (near - far);
        
        return new Float32Array([
            f / aspect, 0, 0, 0,
            0, f, 0, 0,
            0, 0, (near + far) * rangeInv, -1,
            0, 0, near * far * rangeInv * 2, 0
        ]);
    }

    // Additional intelligent features
    createFormFocusEffect() {
        this.morphToPattern('tunnel');
        this.setEnergyLevel(0.8);
    }

    createRipple(intensity) {
        // Create ripple effect through particles
        this.triggerPulse(Math.abs(intensity));
    }

    addEnergyPulse(amount) {
        this.setEnergyLevel(Math.min(1, this.energyLevel + amount));
    }

    adjustParticleCount(newCount) {
        // Dynamically adjust particle count for performance/complexity
        if (newCount !== this.particleCount && newCount > 1000 && newCount < 50000) {
            this.particleCount = newCount;
            this.positions = new Float32Array(this.particleCount * 3);
            this.velocities = new Float32Array(this.particleCount * 3);
            this.targets = new Float32Array(this.particleCount * 3);
            
            this.morphToPattern(this.currentPattern);
        }
    }
}

// Export the magical UI system
window.CleverMagicalUI = CleverMagicalUI;
