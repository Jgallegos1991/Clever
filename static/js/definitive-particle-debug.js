// DEFINITIVE PARTICLE DEBUG - Find the root cause
console.log('🔬 DEFINITIVE PARTICLE DEBUG STARTING...');

function definitiveDebug() {
    console.log('🔍 Running definitive debug...');
    
    const canvas = document.getElementById('particles');
    console.log('🎯 Canvas element:', canvas);
    
    if (!canvas || !(canvas instanceof HTMLCanvasElement)) {
        console.error('❌ CRITICAL: No canvas element found or not a canvas!');
        console.log('📋 Available elements with id:', Array.from(document.querySelectorAll('[id]')).map(el => el.id));
        return;
    }
    
    console.log('✅ Canvas found');
    console.log('📐 Canvas client rect:', canvas.getBoundingClientRect());
    console.log('📏 Canvas offset dimensions:', canvas.offsetWidth, 'x', canvas.offsetHeight);
    console.log('🎨 Canvas computed style:', getComputedStyle(canvas));
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ CRITICAL: Cannot get 2D context!');
        return;
    }
    
    console.log('✅ 2D Context obtained');
    
    // Force canvas size
    const rect = canvas.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) {
        console.warn('⚠️ Canvas has zero dimensions! Forcing size...');
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        // Recalculate
        const newRect = canvas.getBoundingClientRect();
        console.log('🔧 New canvas rect:', newRect);
    }
    
    const finalRect = canvas.getBoundingClientRect();
    canvas.width = finalRect.width;
    canvas.height = finalRect.height;
    
    console.log('🎨 Final canvas size:', canvas.width, 'x', canvas.height);
    
    if (canvas.width === 0 || canvas.height === 0) {
        console.error('❌ CRITICAL: Canvas still has zero size after forcing!');
        return;
    }
    
    // Test basic drawing
    console.log('🖌️ Testing basic canvas drawing...');
    
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'red';
    ctx.fillRect(50, 50, 100, 100);
    
    ctx.fillStyle = 'blue';
    ctx.beginPath();
    ctx.arc(canvas.width/2, canvas.height/2, 50, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.fillStyle = 'black';
    ctx.font = '24px Arial';
    ctx.fillText('CANVAS DRAWING WORKS!', 20, 30);
    
    console.log('✅ Basic drawing completed');
    
    // Test animation
    let frame = 0;
    function testAnimate() {
        frame++;
        
        // Semi-transparent overlay
        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Moving circle
        const x = (Math.sin(frame * 0.05) * 0.4 + 0.5) * canvas.width;
        const y = (Math.cos(frame * 0.05) * 0.4 + 0.5) * canvas.height;
        
        ctx.fillStyle = `hsl(${frame % 360}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(x, y, 30, 0, Math.PI * 2);
        ctx.fill();
        
        // Frame counter
        ctx.fillStyle = 'black';
        ctx.font = '16px Arial';
        ctx.fillText(`Frame: ${frame}`, 10, canvas.height - 10);
        
        if (frame < 200) { // Run for ~3 seconds
            requestAnimationFrame(testAnimate);
        } else {
            console.log('✅ Animation test completed successfully');
            
            // Now try to initialize the actual holographic chamber
            console.log('🚀 Attempting to start holographic chamber...');
            if (typeof window['HolographicChamber'] === 'function') {
                try {
                    const chamber = new window['HolographicChamber'](canvas);
                    window['holographicChamber'] = chamber;
                    console.log('✅ Holographic chamber started successfully!');
                } catch (error) {
                    console.error('❌ Error starting holographic chamber:', error);
                }
            } else {
                console.error('❌ HolographicChamber class not available!');
            }
        }
    }
    
    console.log('🎬 Starting animation test...');
    requestAnimationFrame(testAnimate);
}

// Run after a delay to ensure everything is loaded
setTimeout(() => {
    console.log('⏰ Starting delayed definitive debug...');
    definitiveDebug();
}, 1000);

console.log('🚀 Definitive particle debug loaded!');