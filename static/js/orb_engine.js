// orb_engine.js - Core 3D engine for Clever UI
// Three.js-based particle system with morph targets and 3D grid, CSS3D panels

// --- Clever 3D UI Engine ---
// Magical swarm, morphing, grid ripple, panel emergence, smooth enchanted transitions

// Uses global THREE provided by /static/js/three-bridge.js (ES module)
let scene, camera, renderer, cssRenderer, particleSystem, grid, fog;
let morphTargets = {};
let currentMorph = 'sphere';
let morphProgress = 0;
let morphDuration = 1.2; // seconds
let morphStart, morphEnd, morphFrom, morphTo;
const PARTICLE_COUNT = 1200;
let positions, geometry;
let gridRipple = {active: false, t: 0, origin: [0,0]};

// Swirl and dissolve states
let swirl = { active: false, start: 0, duration: 600, strength: 0.06 };
let dissolve = { active: false, start: 0, duration: 900 };

// Pixel mode state
let pixelMode = false;
let particleMaterial = null;
const original = {
    dpr: (window.devicePixelRatio || 1),
    material: {
        size: 2.2,
        sizeAttenuation: true,
        blending: null, // to be filled after material creation
        opacity: 0.9
    }
};

function init3D() {
    // Scene and camera
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 100);
    camera.position.set(0, 0, 18);
    scene.fog = new THREE.FogExp2(0x0b0f14, 0.02);

    // Renderer
    if (!('WebGLRenderingContext' in window)) {
        console.error('[Clever3D] WebGL not supported in this browser.');
        return;
    }
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.setClearColor(0x0b0f14, 1);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.domElement.style.position = 'absolute';
    renderer.domElement.style.top = 0;
    document.body.appendChild(renderer.domElement);

    // CSS3DRenderer for panels
    cssRenderer = new THREE.CSS3DRenderer();
    cssRenderer.setSize(window.innerWidth, window.innerHeight);
    cssRenderer.domElement.style.position = 'absolute';
    cssRenderer.domElement.style.top = 0;
    cssRenderer.domElement.style.pointerEvents = 'none';
    document.body.appendChild(cssRenderer.domElement);

    // 3D Grid (holographic, rippling)
    const gridGeo = new THREE.PlaneGeometry(40, 40, 20, 20);
    const gridMat = new THREE.MeshBasicMaterial({ color: 0x69eacb, wireframe: true, opacity: 0.13, transparent: true });
    grid = new THREE.Mesh(gridGeo, gridMat);
    grid.rotation.x = -Math.PI/2;
    grid.position.y = -6;
    scene.add(grid);

    // Particles (magical swarm)
    geometry = new THREE.BufferGeometry();
    positions = new Float32Array(PARTICLE_COUNT * 3);
    // Seed initial particle positions with a small jitter so they are visible before morph completes
    for (let i = 0; i < PARTICLE_COUNT * 3; i += 3) {
        positions[i + 0] = (Math.random() - 0.5) * 0.2;
        positions[i + 1] = (Math.random() - 0.5) * 0.2;
        positions[i + 2] = (Math.random() - 0.5) * 0.2;
    }
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleMaterial = new THREE.PointsMaterial({ color: 0x69eacb, size: 2.2, transparent: true, opacity: 0.9, sizeAttenuation: true, blending: THREE.AdditiveBlending, depthWrite: false });
    original.material.blending = THREE.AdditiveBlending;
    particleSystem = new THREE.Points(geometry, particleMaterial);
    scene.add(particleSystem);

    // Morph targets
    morphTargets.sphere = createSphere(PARTICLE_COUNT, 5);
    morphTargets.cube = createCube(PARTICLE_COUNT, 7);
    morphTargets.torus = createTorus(PARTICLE_COUNT, 4, 1.5);
    setMorph('sphere');

    // Responsive
    window.addEventListener('resize', onWindowResize);

    // Kick a subtle grid ripple so the stage feels alive
    gridRipple.active = true;
    gridRipple.t = 0;

    // Showcase the hub panel shortly after init
    setTimeout(() => {
        if (window.Clever3D && typeof window.Clever3D.floatPanel === 'function') {
            window.Clever3D.floatPanel('synaptic-hub-card', 10, 6, 0);
        }
    }, 800);

    animate();
}

function createSphere(count, radius) {
    const arr = [];
    for (let i = 0; i < count; i++) {
        const phi = Math.acos(2 * Math.random() - 1);
        const theta = 2 * Math.PI * Math.random();
        arr.push(
            radius * Math.sin(phi) * Math.cos(theta),
            radius * Math.sin(phi) * Math.sin(theta),
            radius * Math.cos(phi)
        );
    }
    return arr;
}
function createCube(count, size) {
    const arr = [];
    for (let i = 0; i < count; i++) {
        arr.push(
            (Math.random() - 0.5) * size,
            (Math.random() - 0.5) * size,
            (Math.random() - 0.5) * size
        );
    }
    return arr;
}
function createTorus(count, r, tube) {
    const arr = [];
    for (let i = 0; i < count; i++) {
        const u = Math.random() * 2 * Math.PI;
        const v = Math.random() * 2 * Math.PI;
        arr.push(
            (r + tube * Math.cos(v)) * Math.cos(u),
            (r + tube * Math.cos(v)) * Math.sin(u),
            tube * Math.sin(v)
        );
    }
    return arr;
}

function setMorph(target) {
    morphFrom = geometry.attributes.position.array.slice();
    morphTo = morphTargets[target];
    morphStart = performance.now();
    morphEnd = morphStart + morphDuration * 1000;
    currentMorph = target;
    morphProgress = 0;
}

function animate() {
    requestAnimationFrame(animate);
    const now = performance.now();
    
    // Pre-morph swirl: accelerate and rotate the swarm inward before condensing
    if (swirl.active) {
        const p = Math.min(1, (now - swirl.start) / swirl.duration);
        for (let i = 0; i < PARTICLE_COUNT * 3; i += 3) {
            const x = positions[i], y = positions[i+1];
            // rotate around Z and pull slightly to center
            const angle = Math.atan2(y, x) + swirl.strength * (1.2 - p);
            const radius = Math.sqrt(x*x + y*y) * (0.99 - 0.15 * (1 - p));
            positions[i]   = Math.cos(angle) * radius;
            positions[i+1] = Math.sin(angle) * radius;
            // gentle z wobble
            positions[i+2] += Math.sin((i + now)/900) * 0.003;
        }
        geometry.attributes.position.needsUpdate = true;
        if (p >= 1) swirl.active = false;
    }
    
    // Morphing
    if (morphTo && morphFrom) {
        morphProgress = Math.min(1, (now - morphStart) / (morphEnd - morphStart));
        const ease = easeInOutCubic(morphProgress);
        for (let i = 0; i < PARTICLE_COUNT * 3; i++) {
            positions[i] = morphFrom[i] + (morphTo[i] - morphFrom[i]) * ease;
        }
        geometry.attributes.position.needsUpdate = true;
    }
    // Idle: magical stardust flow
    if (!morphTo || morphProgress >= 1) {
        for (let i = 0; i < PARTICLE_COUNT * 3; i+=3) {
            positions[i+0] += Math.sin(performance.now()/900 + i) * 0.002;
            positions[i+1] += Math.cos(performance.now()/1100 + i) * 0.002;
            positions[i+2] += Math.sin(performance.now()/1300 + i) * 0.002;
        }
        geometry.attributes.position.needsUpdate = true;
    }

    // Dissolve effect: shimmer and expand, then return to idle
    if (dissolve.active) {
        const pd = Math.min(1, (now - dissolve.start) / dissolve.duration);
        const pulse = 0.6 + 0.4 * Math.sin(now / 80);
        particleSystem.material.opacity = 0.9 * pulse;
        for (let i = 0; i < PARTICLE_COUNT * 3; i += 3) {
            const nx = (Math.random() - 0.5) * 0.02;
            const ny = (Math.random() - 0.5) * 0.02;
            const nz = (Math.random() - 0.5) * 0.02;
            positions[i]   += nx * (0.5 + pd);
            positions[i+1] += ny * (0.5 + pd);
            positions[i+2] += nz * (0.5 + pd);
        }
        geometry.attributes.position.needsUpdate = true;
        if (pd >= 1) {
            dissolve.active = false;
            particleSystem.material.opacity = 0.9;
        }
    }
    // Grid ripple effect
    if (gridRipple.active) {
        gridRipple.t += 0.04;
        let verts = grid.geometry.attributes.position;
        for (let i = 0; i < verts.count; i++) {
            let x = verts.getX(i), y = verts.getY(i), d = Math.sqrt(x*x + y*y);
            let ripple = Math.sin(4*d - gridRipple.t*6) * Math.exp(-d*0.5 - gridRipple.t*1.2) * 0.7;
            verts.setZ(i, ripple);
        }
        verts.needsUpdate = true;
        if (gridRipple.t > 2.5) {
            gridRipple.active = false;
            for (let i = 0; i < verts.count; i++) verts.setZ(i, 0);
            verts.needsUpdate = true;
        }
    }
    renderer.render(scene, camera);
    cssRenderer.render(scene, camera);
}

function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    cssRenderer.setSize(window.innerWidth, window.innerHeight);
}

// --- Panel Emergence (CSS3D) ---
function floatPanel(domId, x, y, z) {
    // Make a DOM element float in 3D
    const dom = document.getElementById(domId);
    if (!dom) return;
    dom.style.opacity = '0';
    const obj = new THREE.CSS3DObject(dom);
    obj.position.set(x, y, z);
    scene.add(obj);
    setTimeout(() => { dom.style.transition = 'opacity 0.7s cubic-bezier(.4,2,.6,1)'; dom.style.opacity = '1'; }, 100);
    return obj;
}

// --- Event Hooks ---
window.Clever3D = {
    setMorph,
    init3D,
    // Pixel mode: chunky look with nearest-neighbor upscaling
    pixelMode: function(mode) {
        if (!renderer || !particleMaterial) return;
        const want = mode === 'toggle' ? !pixelMode : !!mode && mode !== 'off' && mode !== false;
        pixelMode = want;
        if (pixelMode) {
            renderer.setPixelRatio(0.6);
            renderer.domElement.style.imageRendering = 'pixelated';
            particleMaterial.sizeAttenuation = false;
            particleMaterial.size = 4.0;
            particleMaterial.opacity = 1.0;
            particleMaterial.blending = THREE.NormalBlending;
            particleMaterial.needsUpdate = true;
        } else {
            renderer.setPixelRatio(Math.min(original.dpr, 1.5));
            renderer.domElement.style.imageRendering = '';
            particleMaterial.sizeAttenuation = original.material.sizeAttenuation;
            particleMaterial.size = original.material.size;
            particleMaterial.opacity = original.material.opacity;
            particleMaterial.blending = original.material.blending;
            particleMaterial.needsUpdate = true;
        }
    },
    // Summon: swirl then condense to a sphere
    summon: function() {
        swirl.active = true; swirl.start = performance.now();
        setTimeout(() => setMorph('sphere'), swirl.duration - 50);
        gridRipple.active = true; gridRipple.t = 0;
    },
    // Dissolve: shimmer and merge back to swarm
    dissolve: function() {
        dissolve.active = true; dissolve.start = performance.now();
    },
    gridRipple: function() {
        gridRipple.active = true;
        gridRipple.t = 0;
    },
    floatPanel
};

// Auto-init
function tryStart() {
    if (window.THREE && THREE.CSS3DRenderer) {
        init3D();
        return true;
    }
    return false;
}

// Start when DOM is ready and THREE is loaded (from the module bridge)
window.addEventListener('DOMContentLoaded', () => {
    if (!tryStart()) {
        // Wait for bridge to finish loading
        window.addEventListener('three-ready', tryStart, { once: true });
    }
});

console.log('[Clever3D] orb_engine loaded; awaiting THREE bridge to init.');
