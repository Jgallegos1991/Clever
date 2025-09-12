// Simple Particle Test - Debug version to verify canvas is working
console.log('🚀 Loading simple particle test...');

function startSimpleTest() {
  console.log('🎯 Starting simple particle test...');
  
  const canvas = document.getElementById('particles');
  if (!canvas) {
    console.error('❌ No canvas found!');
    return;
  }
  
  console.log('✅ Canvas found:', canvas);
  console.log('📐 Canvas dimensions:', canvas.offsetWidth, 'x', canvas.offsetHeight);
  
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    console.error('❌ No 2D context!');
    return;
  }
  
  // Set canvas size
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  
  console.log('🎨 Canvas size set to:', canvas.width, 'x', canvas.height);
  
  // Draw a simple test
  function drawTest() {
    // Clear
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw bright test circles
    const time = Date.now() * 0.001;
    
    for (let i = 0; i < 50; i++) {
      const x = (Math.sin(time + i) * 0.5 + 0.5) * canvas.width;
      const y = (Math.cos(time + i * 0.5) * 0.5 + 0.5) * canvas.height;
      
      ctx.fillStyle = `hsl(${(i * 10 + time * 50) % 360}, 100%, 50%)`;
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fill();
    }
    
    requestAnimationFrame(drawTest);
  }
  
  console.log('🎬 Starting animation...');
  drawTest();
}

// Start immediately when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startSimpleTest);
} else {
  startSimpleTest();
}

console.log('✨ Simple particle test loaded!');