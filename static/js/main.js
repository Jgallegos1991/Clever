// Particle cloud with breathing and approach effect
(function() {
    const canvas = document.getElementById('particleCloud');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const cx = w/2, cy = h/2;
    const N = 38;
    let t = 0;
    function draw() {
        ctx.clearRect(0,0,w,h);
        // Breathing scale (0.96–1.00)
        const scale = 0.98 + 0.02 * Math.sin(t/60);
        // Approach (slight forward motion)
        const approach = 1.0 + 0.03 * Math.sin(t/120);
        for (let i=0; i<N; ++i) {
            const a = (i/N)*2*Math.PI + t/90;
            const r = 120 * scale * approach + 18*Math.sin(a*3 + t/40);
            const x = cx + Math.cos(a)*r;
            const y = cy + Math.sin(a)*r;
            ctx.beginPath();
            ctx.arc(x, y, 18 + 4*Math.sin(a*2 + t/30), 0, 2*Math.PI);
            ctx.fillStyle = `rgba(120,180,255,0.13)`;
            ctx.fill();
        }
        // Center core
        ctx.beginPath();
        ctx.arc(cx, cy, 44 + 4*Math.sin(t/40), 0, 2*Math.PI);
        ctx.fillStyle = 'rgba(80,120,255,0.18)';
        ctx.fill();
        t++;
        requestAnimationFrame(draw);
    }
    draw();
})();

// Main wiring for Clever UI
(function() {
    const input = document.getElementById('mainInput');

    // Send message to /chat
        window.CleverUI.onSend = function(msg) {
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            })
            .then(r => r.json())
            .then(data => {
                if (data.reply) {
                    window.CleverUI.pushLog('Clever', data.reply);
                    window.CleverUI.spawnPanel({
                        message: data.reply,
                        context: data.analysis?.detected_intent,
                        source: data.analysis?.activePersona,
                        confidence: data.analysis?.user_mood
                    });
                } else if (data.error) {
                    window.CleverUI.pushLog('Error', data.error);
                }
            })
            .catch(() => window.CleverUI.pushLog('Error', 'Network error.'));
        };

    // Upload file to /ingest
    window.CleverUI.onUpload = function(file) {
        const fd = new FormData();
        fd.append('file', file);
        fetch('/ingest', { method: 'POST', body: fd })
        .then(r => r.json())
        .then(data => {
            if (data.message) {
                window.CleverUI.pushLog('System', data.message);
            } else if (data.error) {
                window.CleverUI.pushLog('Error', data.error);
            }
        })
        .catch(() => window.CleverUI.pushLog('Error', 'Upload failed.'));
    };
})();
