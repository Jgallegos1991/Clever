// AGGRESSIVE CANVAS TEST - Force visibility
console.log('🚨 AGGRESSIVE CANVAS TEST STARTING...');

function forceCanvasVisibility() {
    console.log('💪 Forcing canvas visibility...');
    
    const canvas = document.getElementById('particles');
    if (!canvas || !(canvas instanceof HTMLCanvasElement)) {
        console.error('❌ NO CANVAS OR NOT A CANVAS ELEMENT!');
        return;
    }
    
    // Force visible CSS
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '999999';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '1';
    canvas.style.background = 'rgba(255, 0, 0, 0.1)'; // Red tint to see canvas area
    
    console.log('🎨 Forced canvas styles applied');
    
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    
    const ctx = canvas.getContext('2d');
    
    // ULTRA-BRIGHT test pattern
    function drawUltraTest() {
        // Fill entire canvas with semi-transparent black
        ctx.fillStyle = 'rgba(0, 0, 0, 0.02)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        const time = Date.now() * 0.003;
        
        // Draw MASSIVE bright circles
        for (let i = 0; i < 20; i++) {
            const x = (Math.sin(time + i * 0.5) * 0.4 + 0.5) * canvas.width;
            const y = (Math.cos(time + i * 0.3) * 0.4 + 0.5) * canvas.height;
            
            // Huge outer glow
            ctx.save();
            ctx.globalAlpha = 0.3;
            ctx.fillStyle = `hsl(${(i * 20 + time * 50) % 360}, 100%, 50%)`;
            ctx.beginPath();
            ctx.arc(x, y, 60, 0, Math.PI * 2);
            ctx.fill();
            
            // Medium glow
            ctx.globalAlpha = 0.6;
            ctx.fillStyle = `hsl(${(i * 20 + time * 50) % 360}, 100%, 70%)`;
            ctx.beginPath();
            ctx.arc(x, y, 30, 0, Math.PI * 2);
            ctx.fill();
            
            // Bright core
            ctx.globalAlpha = 1;
            ctx.fillStyle = 'white';
            ctx.beginPath();
            ctx.arc(x, y, 15, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
        
        // MASSIVE text overlay
        ctx.fillStyle = 'white';
        ctx.font = 'bold 48px Arial';
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 4;
        ctx.strokeText('PARTICLES ACTIVE!', 50, 100);
        ctx.fillText('PARTICLES ACTIVE!', 50, 100);
        
        ctx.font = 'bold 24px Arial';
        ctx.fillText(`Canvas: ${canvas.width}x${canvas.height}`, 50, 150);
        ctx.fillText(`Time: ${time.toFixed(1)}`, 50, 180);
        
        requestAnimationFrame(drawUltraTest);
    }
    
    console.log('🚀 Starting ultra-bright test animation...');
    drawUltraTest();
}

// Run immediately
document.addEventListener('DOMContentLoaded', forceCanvasVisibility);
if (document.readyState !== 'loading') {
    forceCanvasVisibility();
}

console.log('💥 Aggressive canvas test loaded!');