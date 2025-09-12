// ULTIMATE DIAGNOSTIC - Test every possible issue
console.log('🔥 ULTIMATE DIAGNOSTIC STARTING...');

function ultimateDiagnostic() {
    console.log('🔍 Running ultimate particle diagnostic...');
    
    // 1. Test basic DOM elements
    console.log('=== DOM STRUCTURE TEST ===');
    const canvas = document.getElementById('particles');
    const body = document.body;
    const html = document.documentElement;
    
    console.log('Canvas element:', canvas);
    console.log('Body element:', body);
    console.log('HTML element:', html);
    console.log('Document ready state:', document.readyState);
    
    if (!canvas) {
        console.error('❌ CRITICAL: No canvas found in DOM!');
        console.log('All elements with IDs:', Array.from(document.querySelectorAll('[id]')).map(el => `${el.tagName}#${el.id}`));
        return false;
    }
    
    // 2. Test canvas properties
    console.log('=== CANVAS PROPERTIES TEST ===');
    console.log('Canvas instanceof HTMLCanvasElement:', canvas instanceof HTMLCanvasElement);
    console.log('Canvas nodeName:', canvas.nodeName);
    console.log('Canvas tagName:', canvas.tagName);
    
    if (!(canvas instanceof HTMLCanvasElement)) {
        console.error('❌ CRITICAL: Canvas is not a canvas element!');
        return false;
    }
    
    // 3. Test canvas dimensions and positioning
    console.log('=== CANVAS DIMENSIONS TEST ===');
    const rect = canvas.getBoundingClientRect();
    const computedStyle = getComputedStyle(canvas);
    
    console.log('Canvas bounding rect:', rect);
    console.log('Canvas offset dimensions:', { width: canvas.offsetWidth, height: canvas.offsetHeight });
    console.log('Canvas client dimensions:', { width: canvas.clientWidth, height: canvas.clientHeight });
    console.log('Canvas internal dimensions:', { width: canvas.width, height: canvas.height });
    
    console.log('Canvas computed styles:', {
        position: computedStyle.position,
        top: computedStyle.top,
        left: computedStyle.left,
        width: computedStyle.width,
        height: computedStyle.height,
        zIndex: computedStyle.zIndex,
        opacity: computedStyle.opacity,
        display: computedStyle.display,
        visibility: computedStyle.visibility,
        pointerEvents: computedStyle.pointerEvents,
        background: computedStyle.background
    });
    
    // 4. Test canvas context
    console.log('=== CANVAS CONTEXT TEST ===');
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ CRITICAL: Cannot get 2D context!');
        return false;
    }
    console.log('✅ 2D Context obtained:', ctx);
    
    // 5. Force canvas size and test basic drawing
    console.log('=== CANVAS DRAWING TEST ===');
    if (rect.width === 0 || rect.height === 0) {
        console.warn('⚠️ Zero dimensions! Forcing canvas size...');
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.zIndex = '999999';
    }
    
    const finalRect = canvas.getBoundingClientRect();
    canvas.width = finalRect.width;
    canvas.height = finalRect.height;
    
    console.log('Final canvas dimensions:', { width: canvas.width, height: canvas.height });
    
    if (canvas.width === 0 || canvas.height === 0) {
        console.error('❌ CRITICAL: Canvas still has zero dimensions!');
        return false;
    }
    
    // 6. Test basic drawing operations
    console.log('Testing basic drawing operations...');
    
    // Clear canvas with solid color
    ctx.fillStyle = 'red';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    console.log('✅ Filled canvas with red');
    
    // Draw white rectangle
    ctx.fillStyle = 'white';
    ctx.fillRect(100, 100, 200, 100);
    console.log('✅ Drew white rectangle');
    
    // Draw circle
    ctx.fillStyle = 'blue';
    ctx.beginPath();
    ctx.arc(canvas.width/2, canvas.height/2, 50, 0, Math.PI * 2);
    ctx.fill();
    console.log('✅ Drew blue circle');
    
    // Draw text
    ctx.fillStyle = 'yellow';
    ctx.font = 'bold 48px Arial';
    ctx.fillText('DIAGNOSTIC TEST', 50, 50);
    console.log('✅ Drew diagnostic text');
    
    // 7. Test if browser supports advanced canvas features
    console.log('=== BROWSER CAPABILITIES TEST ===');
    console.log('Canvas 2D context properties:', {
        globalAlpha: 'globalAlpha' in ctx,
        globalCompositeOperation: 'globalCompositeOperation' in ctx,
        shadowBlur: 'shadowBlur' in ctx,
        createLinearGradient: 'createLinearGradient' in ctx,
        getImageData: 'getImageData' in ctx
    });
    
    // 8. Test animation capability
    console.log('=== ANIMATION TEST ===');
    let animFrame = 0;
    function testAnimation() {
        animFrame++;
        
        // Clear with semi-transparent overlay
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw animated circle
        const x = (Math.sin(animFrame * 0.1) * 0.4 + 0.5) * canvas.width;
        const y = (Math.cos(animFrame * 0.1) * 0.4 + 0.5) * canvas.height;
        
        ctx.fillStyle = `hsl(${animFrame % 360}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(x, y, 30, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw frame counter
        ctx.fillStyle = 'white';
        ctx.font = '20px Arial';
        ctx.fillText(`Frame: ${animFrame}`, 20, canvas.height - 20);
        
        if (animFrame < 120) { // Run for 2 seconds
            requestAnimationFrame(testAnimation);
        } else {
            console.log('✅ Animation test completed');
            
            // 9. Now test HolographicChamber initialization
            console.log('=== HOLOGRAPHIC CHAMBER TEST ===');
            testHolographicChamber();
        }
    }
    
    requestAnimationFrame(testAnimation);
    
    return true;
}

function testHolographicChamber() {
    console.log('Testing HolographicChamber initialization...');
    
    const canvas = document.getElementById('particles');
    
    // Check if HolographicChamber class exists
    if (typeof window['HolographicChamber'] !== 'function') {
        console.error('❌ HolographicChamber class not found!');
        console.log('Available window properties:', Object.keys(window).filter(k => k.includes('Holo') || k.includes('Chamber') || k.includes('particle')));
        return;
    }
    
    console.log('✅ HolographicChamber class found');
    
    // Try to create instance
    try {
        console.log('Creating HolographicChamber instance...');
        const chamber = new window['HolographicChamber'](canvas);
        console.log('✅ HolographicChamber created successfully:', chamber);
        
        // Test particle creation
        console.log('Particle count:', chamber.particles ? chamber.particles.length : 'undefined');
        console.log('Chamber state:', chamber.state);
        console.log('Canvas dimensions in chamber:', chamber.width, 'x', chamber.height);
        
        // Store global reference
        window['holographicChamber'] = chamber;
        console.log('✅ HolographicChamber stored in window.holographicChamber');
        
    } catch (error) {
        console.error('❌ Error creating HolographicChamber:', error);
        console.error('Error stack:', error.stack);
    }
}

// Run diagnostic after everything is loaded
setTimeout(() => {
    console.log('⏰ Starting ultimate diagnostic...');
    ultimateDiagnostic();
}, 2000);

console.log('🚀 Ultimate diagnostic loaded!');