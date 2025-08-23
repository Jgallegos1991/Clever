// three-bridge.js
// Loads Three.js and addons as ES modules locally, then exposes a global THREE
// so existing non-module scripts (orb_engine.js, ui.js) can keep using window.THREE.

let alreadyReady = false;
function dispatchReadyOnce() {
	if (alreadyReady) return;
	alreadyReady = true;
	window.dispatchEvent(new Event('three-ready'));
}
import * as THREEImport from '/static/vendor/threejs/build/three.module.js';
import { CSS3DRenderer, CSS3DObject, CSS3DSprite } from '/static/vendor/threejs/examples/jsm/renderers/CSS3DRenderer.js';
import { MeshSurfaceSampler } from '/static/vendor/threejs/examples/jsm/math/MeshSurfaceSampler.js';

try {
	const THREE = window.THREE || Object.assign({}, THREEImport);
	window.THREE = THREE; // expose mutable copy
	if (!THREE.CSS3DRenderer) {
		THREE.CSS3DRenderer = CSS3DRenderer;
		THREE.CSS3DObject = CSS3DObject;
		THREE.CSS3DSprite = CSS3DSprite;
	}
	if (!THREE.MeshSurfaceSampler) {
		THREE.MeshSurfaceSampler = MeshSurfaceSampler;
	}
	dispatchReadyOnce();
} catch (err) {
	console.error('[three-bridge] Failed to initialize THREE bridge:', err);
}
