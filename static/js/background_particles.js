


// Glassy, glowing orb with pixel form-shaping (text/waveform morph)
(function() {
    const canvas = document.getElementById('particleCloud');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const cx = w/2, cy = h/2;
    const N = 2200;
    let t = 0;

    // State for pulse effect
    let pulse = 0;

    // Particle definition
    function makeParticle() {
        // Spherical distribution
        const phi = Math.random() * 2 * Math.PI;
        const costheta = Math.random() * 2 - 1;
        const u = Math.random();
        const theta = Math.acos(costheta);
        const r = 120 * Math.cbrt(u);
        return {
            x: cx + r * Math.sin(theta) * Math.cos(phi),
            y: cy + r * Math.sin(theta) * Math.sin(phi),
            tx: cx + r * Math.sin(theta) * Math.cos(phi),
            ty: cy + r * Math.sin(theta) * Math.sin(phi),
            baseR: r,
            phi,
            theta,
            speed: 0.002 + Math.random() * 0.004,
            colorSeed: Math.random(),
            alpha: 1
        };
    }
    let particles = Array.from({length: N}, makeParticle);


    // Pulse effect on reply
    function triggerPulse() {
        pulse = 1.0;
    }


    // Listen for NLP/text events (trigger pulse only)
    canvas.addEventListener('clever-nlp', e => {
        triggerPulse();
    });


    // Demo: click to pulse
    canvas.addEventListener('click', () => {
        triggerPulse();
    });

    function animate() {
        t++;
        ctx.clearRect(0,0,w,h);

    // Draw glassy orb background with pulse
    let orbGradient = ctx.createRadialGradient(cx, cy, 24, cx, cy, 120 + 24*pulse);
    orbGradient.addColorStop(0, 'rgba(255,255,255,0.25)');
    orbGradient.addColorStop(0.3, 'rgba(45,224,255,0.18)');
    orbGradient.addColorStop(0.7, 'rgba(40,80,180,0.10)');
    orbGradient.addColorStop(1, 'rgba(10,20,40,0.01)');
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, 120 + 24*pulse, 0, 2*Math.PI);
    ctx.fillStyle = orbGradient;
    ctx.shadowColor = '#2de0ff';
    ctx.shadowBlur = 32 + 32*pulse;
    ctx.globalAlpha = 0.85 + 0.15*pulse;
    ctx.fill();
    ctx.restore();
    ctx.globalAlpha = 1;

    // Animate pulse decay
    if (pulse > 0) pulse *= 0.88;

        // Animate and draw all particles
        for (let i=0; i<N; ++i) {
            const p = particles[i];
            // Morphing
            p.x += (p.tx - p.x) * 0.18;
            p.y += (p.ty - p.y) * 0.18;
            // Neon color cycling
            const hue = 200 + 80 * Math.sin(t*0.008 + p.colorSeed*8);
            const sat = 90 + 10 * Math.sin(t*0.01 + p.colorSeed*12);
            const light = 60 + 30 * Math.sin(t*0.012 + p.colorSeed*7);
            ctx.save();
            ctx.beginPath();
            ctx.arc(p.x, p.y, 1.2 + 0.7*Math.sin(t*0.02 + p.colorSeed*20), 0, 2*Math.PI);
            ctx.shadowColor = `hsl(${hue},100%,85%)`;
            ctx.shadowBlur = 16;
            ctx.globalAlpha = (0.18 + 0.7 * Math.pow(1 - (Math.hypot(p.x-cx,p.y-cy)/120), 2)) * (p.alpha||1);
            ctx.fillStyle = `hsl(${hue},${sat}%,${light}%)`;
            ctx.fill();
            ctx.restore();
        }

        // Glassy orb highlight
        ctx.save();
        ctx.globalAlpha = 0.18;
        ctx.beginPath();
        ctx.ellipse(cx-30, cy-40, 38, 16, -0.3, 0, 2*Math.PI);
        ctx.fillStyle = '#fff';
        ctx.shadowColor = '#fff';
        ctx.shadowBlur = 18;
        ctx.fill();
        ctx.restore();

        // Central waveform (for demo, animated)
        ctx.save();
        ctx.strokeStyle = '#2de0ff';
        ctx.lineWidth = 2.2;
        ctx.shadowColor = '#2de0ff';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        let amp = 22 + 8*Math.sin(t*0.02);
        let y0 = cy;
        for (let x=0; x<=240; x+=6) {
            let px = cx-120 + x;
            let py = cy + Math.sin((x/240)*4*Math.PI + t*0.06) * amp * Math.sin(t*0.01 + x*0.03);
            if (x===0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.restore();

        requestAnimationFrame(animate);
    }
    animate();
})();

