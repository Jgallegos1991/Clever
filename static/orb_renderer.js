// Minimal offline orb renderer (20k particles would be heavy; we draw a soft orb)
let ctx, w, h, rafId;
let hue = 200; // soft neon blue
let pulse = 0;

export function startRenderer(canvas) {
	if (!canvas) throw new Error('startRenderer: canvas is required');
	ctx = canvas.getContext('2d');
	if (!ctx) throw new Error('2D context not available');
	const resize = () => {
		w = canvas.width = window.innerWidth;
		h = canvas.height = window.innerHeight;
	};
	window.addEventListener('resize', resize);
	resize();
	cancelAnimationFrame(rafId);
	const loop = () => {
		rafId = requestAnimationFrame(loop);
		ctx.clearRect(0, 0, w, h);
		const cx = w * 0.5, cy = h * 0.5;
		const radius = Math.min(w, h) * 0.18 + Math.sin(Date.now() * 0.002 + pulse) * 4;
		const grad = ctx.createRadialGradient(cx, cy, radius * 0.2, cx, cy, radius);
		grad.addColorStop(0, `hsla(${hue}, 100%, 60%, 0.22)`);
		grad.addColorStop(1, `hsla(${hue}, 100%, 60%, 0.00)`);
		ctx.fillStyle = grad;
		ctx.beginPath();
		ctx.arc(cx, cy, radius, 0, Math.PI * 2);
		ctx.fill();
	};
	loop();
}

export function triggerPulseAnimation() {
	pulse = (pulse + Math.PI / 2) % (Math.PI * 2);
}

export function updateOrbColors(mode = 'Base') {
	// Map persona/mood to hue; keep alpha soft
	const map = {
		Base: 200,
		Calm: 210,
		Curious: 270,
		Analytical: 50,
		Excited: 30,
		Positive: 150,
		Negative: 0,
	};
	hue = map[mode] ?? 200;
}
