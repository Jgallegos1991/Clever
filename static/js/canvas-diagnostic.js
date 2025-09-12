// Canvas Diagnostic - Check if canvas is working at all
console.log('🔍 Canvas Diagnostic Starting...');

function runCanvasDiagnostic() {
    console.log('🎯 Running canvas diagnostic...');
    
    const canvas = document.getElementById('particles');
    if (!canvas) {
        console.error('❌ NO CANVAS FOUND!');
        return false;
    }
    
    console.log('✅ Canvas element found:', canvas);
    console.log('📐 Canvas computed style:', getComputedStyle(canvas));
    console.log('📏 Canvas offset dimensions:', canvas.offsetWidth, 'x', canvas.offsetHeight);
    console.log('📏 Canvas client dimensions:', canvas.clientWidth, 'x', canvas.clientHeight);
    console.log('📏 Canvas actual size:', canvas.width, 'x', canvas.height);
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ NO 2D CONTEXT!');
        return false;
    }
    
    console.log('✅ 2D Context obtained:', ctx);
    
    // Set canvas size explicitly
    const rect = canvas.getBoundingClientRect();
    console.log('📦 Canvas bounding rect:', rect);
    
    canvas.width = rect.width || window.innerWidth;
    canvas.height = rect.height || window.innerHeight;
    
    console.log('🎨 Canvas size set to:', canvas.width, 'x', canvas.height);
    
    // Draw a simple test pattern
    console.log('🎬 Drawing test pattern...');
    
    // Clear with black
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw bright test squares in corners
    ctx.fillStyle = 'white';
    ctx.fillRect(10, 10, 50, 50); // Top left
    ctx.fillRect(canvas.width - 60, 10, 50, 50); // Top right
    ctx.fillRect(10, canvas.height - 60, 50, 50); // Bottom left
    ctx.fillRect(canvas.width - 60, canvas.height - 60, 50, 50); // Bottom right
    
    // Draw center cross
    ctx.fillStyle = 'red';
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    ctx.fillRect(centerX - 25, centerY - 2, 50, 4);
    ctx.fillRect(centerX - 2, centerY - 25, 4, 50);
    
    // Draw animated circle
    let frame = 0;
    function animateTest() {
        frame++;
        
        // Draw pulsing circle
        ctx.fillStyle = `hsl(${frame % 360}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(centerX, centerY + 100, 20 + Math.sin(frame * 0.1) * 10, 0, Math.PI * 2);
        ctx.fill();
        
        // Add text
        ctx.fillStyle = 'white';
        ctx.font = '20px Arial';
        ctx.fillText(`Frame: ${frame}`, 20, canvas.height - 20);
        
        if (frame < 300) { // Run for 5 seconds at 60fps
            requestAnimationFrame(animateTest);
        } else {
            console.log('🏁 Test animation complete');
        }
    }
    
    requestAnimationFrame(animateTest);
    console.log('✨ Test pattern drawn and animation started');
    
    return true;
}

// Run diagnostic when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runCanvasDiagnostic);
} else {
    runCanvasDiagnostic();
}

console.log('🚀 Canvas diagnostic loaded');