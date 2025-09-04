/**
 * Simple particle test to debug the quantum scene
 */

(function(){
  console.log('🔍 Testing basic particle system...');
  
  function initTest() {
    const canvas = document.getElementById('scene');
    if(!canvas) {
      console.warn('Canvas not found, retrying...');
      return setTimeout(initTest, 50);
    }
    
    console.log('✅ Canvas found:', canvas);
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    console.log('📐 Canvas size:', canvas.width, 'x', canvas.height);
    
    // Simple particle array
    const particles = [];
    for(let i = 0; i < 100; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        color: `hsl(${180 + Math.random() * 60}, 70%, 60%)`
      });
    }
    
    console.log('⚛️ Created', particles.length, 'test particles');
    
    function animate() {
      // Clear screen
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Update and draw particles
      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        
        // Bounce off edges
        if(p.x < 0 || p.x > canvas.width) p.vx = -p.vx;
        if(p.y < 0 || p.y > canvas.height) p.vy = -p.vy;
        
        // Draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = p.color;
        ctx.fill();
      });
      
      requestAnimationFrame(animate);
    }
    
    console.log('🚀 Starting test animation...');
    animate();
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTest);
  } else {
    initTest();
  }
})();
