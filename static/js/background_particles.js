// Starfield, far grid, and near grid rendering (DPI-safe, tuned density/parallax)
(function() {
    const starfield = document.getElementById('starfield');
    const farGrid = document.getElementById('farGrid');
    const nearGrid = document.getElementById('nearGrid');
    let dpr = window.devicePixelRatio || 1;
    let w = window.innerWidth, h = window.innerHeight;

    function resize() {
        dpr = window.devicePixelRatio || 1;
        [starfield, farGrid, nearGrid].forEach(c => {
            c.width = w = window.innerWidth * dpr;
            c.height = h = window.innerHeight * dpr;
            c.style.width = window.innerWidth + 'px';
            c.style.height = window.innerHeight + 'px';
        });
    }
    window.addEventListener('resize', resize);
    resize();

    // Starfield
    const starCount = Math.floor(180 * (w * h) / (1920 * 1080));
    const stars = Array.from({length: starCount}, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        z: Math.random() * 1.0 + 0.2,
        r: Math.random() * 0.7 + 0.3
    }));
    function drawStarfield() {
        const ctx = starfield.getContext('2d');
        ctx.setTransform(1,0,0,1,0,0);
        ctx.clearRect(0,0,w,h);
        for (const s of stars) {
            ctx.globalAlpha = 0.5 * s.z;
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r * s.z * 1.5 * dpr, 0, 2*Math.PI);
            ctx.fillStyle = '#e0e6f0';
            ctx.fill();
        }
        ctx.globalAlpha = 1;
    }

    // Far grid (tilted, parallax)
    function drawFarGrid() {
        const ctx = farGrid.getContext('2d');
        ctx.setTransform(1,0,0,1,0,0);
        ctx.clearRect(0,0,w,h);
        ctx.save();
        ctx.translate(w/2, h/2);
        ctx.rotate(-Math.PI/8);
        ctx.translate(-w/2, -h/2);
        ctx.strokeStyle = '#2a3a4a';
        ctx.lineWidth = 1.2 * dpr;
        for (let x = -w; x < w*2; x += 80 * dpr) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, h);
            ctx.stroke();
        }
        for (let y = -h; y < h*2; y += 80 * dpr) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(w, y);
            ctx.stroke();
        }
        ctx.restore();
    }

    // Near grid (fainter, less lines, parallax)
    function drawNearGrid() {
        const ctx = nearGrid.getContext('2d');
        ctx.setTransform(1,0,0,1,0,0);
        ctx.clearRect(0,0,w,h);
        ctx.save();
        ctx.translate(w/2, h/2);
        ctx.rotate(-Math.PI/8);
        ctx.translate(-w/2, -h/2);
        ctx.strokeStyle = '#3a4a5a';
        ctx.lineWidth = 2.2 * dpr;
        for (let x = -w; x < w*2; x += 220 * dpr) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, h);
            ctx.stroke();
        }
        for (let y = -h; y < h*2; y += 220 * dpr) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(w, y);
            ctx.stroke();
        }
        ctx.restore();
    }

    function animate() {
        drawStarfield();
        drawFarGrid();
        drawNearGrid();
        requestAnimationFrame(animate);
    }
    animate();
})();
