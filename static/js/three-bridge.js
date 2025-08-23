// three-bridge.js
// Loads Three.js and addons as ES modules from CDN, then exposes a global THREE
// so existing non-module scripts (orb_engine.js, ui.js) can keep using window.THREE.

import * as THREE from '/static/vendor/threejs/build/three.module.js';
import { CSS3DRenderer, CSS3DObject, CSS3DSprite } from '/static/vendor/threejs/examples/jsm/renderers/CSS3DRenderer.js';
import { MeshSurfaceSampler } from '/static/vendor/threejs/examples/jsm/math/MeshSurfaceSampler.js';

// Expose to global for legacy scripts
window.THREE = THREE;
THREE.CSS3DRenderer = CSS3DRenderer;
THREE.CSS3DObject = CSS3DObject;
THREE.CSS3DSprite = CSS3DSprite;
THREE.MeshSurfaceSampler = MeshSurfaceSampler;

// Signal that THREE is ready for legacy scripts
window.dispatchEvent(new Event('three-ready'));
