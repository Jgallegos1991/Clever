// EMERGENCY PARTICLE SYSTEM - Minimal, guaranteed to work
console.log('🚨 EMERGENCY PARTICLE SYSTEM LOADING...');

function createEmergencyParticleSystem() {
    console.log('🔧 Creating emergency particle system...');
    
    const canvas = document.getElementById('particles');
    if (!canvas) {
        console.error('❌ No canvas found for emergency system!');
        return;
    }
    
    console.log('✅ Canvas found, setting up emergency particles...');
    
    // Force canvas to be visible and full screen
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '1';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '1';
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ No 2D context for emergency system!');
        return;
    }
    
    // Set canvas internal size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    console.log(`📏 Emergency canvas size: ${canvas.width}x${canvas.height}`);
    
    // Create simple particles
    const particles = [];
    const particleCount = 100;
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 2,
            vy: (Math.random() - 0.5) * 2,
            size: Math.random() * 3 + 2,
            hue: Math.random() * 60 + 160 // Teal range
        });
    }
    
    console.log(`✨ Created ${particles.length} emergency particles`);
    
    // Animation loop
    function animate() {
        // Clear with trail
        ctx.fillStyle = 'rgba(11, 15, 20, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Update and draw particles
        particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Bounce off walls
            if (particle.x <= 0 || particle.x >= canvas.width) particle.vx *= -1;
            if (particle.y <= 0 || particle.y >= canvas.height) particle.vy *= -1;
            
            // Keep in bounds
            particle.x = Math.max(0, Math.min(canvas.width, particle.x));
            particle.y = Math.max(0, Math.min(canvas.height, particle.y));
            
            // Draw particle with glow
            ctx.save();
            
            // Outer glow
            ctx.globalAlpha = 0.3;
            ctx.fillStyle = `hsl(${particle.hue}, 100%, 50%)`;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size * 4, 0, Math.PI * 2);
            ctx.fill();
            
            // Inner glow
            ctx.globalAlpha = 0.7;
            ctx.fillStyle = `hsl(${particle.hue}, 100%, 70%)`;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size * 2, 0, Math.PI * 2);
            ctx.fill();
            
            // Core
            ctx.globalAlpha = 1;
            ctx.fillStyle = `hsl(${particle.hue}, 100%, 90%)`;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.restore();
        });
        
        // Draw debug info
        ctx.fillStyle = 'rgba(105, 234, 203, 0.8)';
        ctx.font = '16px Arial';
        ctx.fillText(`EMERGENCY PARTICLES: ${particles.length}`, 20, 30);
        ctx.fillText(`Canvas: ${canvas.width}x${canvas.height}`, 20, 50);
        ctx.fillText(`Time: ${Date.now()}`, 20, 70);
        
        requestAnimationFrame(animate);
    }
    
    console.log('🎬 Starting emergency particle animation...');
    animate();
    
    // Create whirlpool formation at bottom center
    setTimeout(() => {
        console.log('🌊 Creating whirlpool formation...');
        const centerX = canvas.width / 2;
        const centerY = canvas.height * 0.75; // Bottom 25%
        
        particles.forEach((particle, i) => {
            const angle = (i / particles.length) * Math.PI * 2;
            const radius = 150;
            particle.x = centerX + Math.cos(angle) * radius;
            particle.y = centerY + Math.sin(angle) * radius * 0.3; // Flatten vertically
            particle.vx = Math.cos(angle + Math.PI/2) * 0.5; // Rotational velocity
            particle.vy = Math.sin(angle + Math.PI/2) * 0.2;
        });
    }, 3000);
    
    return { particles, canvas, ctx };
}

// Start emergency system
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚨 DOM ready, starting emergency particle system...');
    setTimeout(createEmergencyParticleSystem, 1000);
});

console.log('💥 Emergency particle system loaded!');