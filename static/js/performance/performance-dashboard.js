/**
 * Clever Performance Dashboard
 * Real-time monitoring overlay for performance metrics
 */

(function() {
  'use strict';
  
  if (!window.CleverPerformanceQuick) {
    console.warn('Performance Quick not loaded, dashboard disabled');
    return;
  }
  
  let dashboard = null;
  let isVisible = false;
  let updateInterval = null;
  
  function createDashboard() {
    dashboard = document.createElement('div');
    dashboard.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(0, 20, 40, 0.9);
      border: 1px solid #00e6ff;
      border-radius: 8px;
      padding: 10px;
      font-family: 'Courier New', monospace;
      font-size: 12px;
      color: #00e6ff;
      z-index: 10000;
      min-width: 200px;
      backdrop-filter: blur(10px);
      box-shadow: 0 0 20px rgba(0, 230, 255, 0.3);
      transition: opacity 0.3s ease;
    `;
    
    dashboard.innerHTML = `
      <div style="font-weight: bold; margin-bottom: 8px; color: #38f0c8;">
        ⚡ Performance Monitor
      </div>
      <div id="fps-display">FPS: --</div>
      <div id="frame-time">Frame: -- ms</div>
      <div id="quality-level">Quality: --</div>
      <div id="particles-count">Particles: --</div>
      <div id="hardware-info" style="margin-top: 8px; font-size: 10px; color: #7fd0ff;">
        Loading...
      </div>
      <div style="margin-top: 8px; font-size: 10px; color: #999;">
        Press 'P' to toggle
      </div>
    `;
    
    document.body.appendChild(dashboard);
    return dashboard;
  }
  
  function updateDashboard() {
    if (!dashboard || !isVisible) return;
    
    const monitor = window.CleverPerformanceQuick.monitor;
    const hardware = window.CleverPerformanceQuick.hardware;
    
    const fps = monitor.getFPS();
    const frameTime = monitor.getAverageFrameTime();
    
    // Color-code performance
    let fpsColor = '#00e6ff';
    if (fps < 30) fpsColor = '#ff6b6b';
    else if (fps < 50) fpsColor = '#feca57';
    else if (fps > 55) fpsColor = '#48dbfb';
    
    document.getElementById('fps-display').innerHTML = 
      `<span style="color: ${fpsColor}">FPS: ${fps}</span>`;
    
    document.getElementById('frame-time').innerHTML = 
      `Frame: ${frameTime.toFixed(1)} ms`;
    
    // Try to get current particle count from window globals
    const particleCount = window.__sceneParticleCount || 'Unknown';
    document.getElementById('particles-count').innerHTML = 
      `Particles: ${particleCount}`;
    
    // Hardware info (static, only update once)
    if (document.getElementById('hardware-info').innerHTML === 'Loading...') {
      document.getElementById('hardware-info').innerHTML = 
        `${hardware.cores} cores | ${hardware.memory}GB RAM<br>` +
        `${hardware.isMobile ? '📱 Mobile' : '🖥️ Desktop'} | ${hardware.pixelRatio}x DPI`;
    }
  }
  
  function toggleDashboard() {
    if (!dashboard) {
      createDashboard();
    }
    
    isVisible = !isVisible;
    dashboard.style.opacity = isVisible ? '1' : '0';
    dashboard.style.pointerEvents = isVisible ? 'auto' : 'none';
    
    if (isVisible && !updateInterval) {
      updateInterval = setInterval(updateDashboard, 100); // Update 10x per second
      console.log('📊 Performance dashboard enabled');
    } else if (!isVisible && updateInterval) {
      clearInterval(updateInterval);
      updateInterval = null;
      console.log('📊 Performance dashboard disabled');
    }
  }
  
  // Keyboard shortcut
  document.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'p' && !e.ctrlKey && !e.altKey && !e.metaKey) {
      // Only if not typing in an input field
      if (document.activeElement.tagName !== 'INPUT' && 
          document.activeElement.tagName !== 'TEXTAREA') {
        toggleDashboard();
        e.preventDefault();
      }
    }
  });
  
  // Auto-show on performance issues
  setTimeout(() => {
    if (window.CleverPerformanceQuick.monitor.getAverageFrameTime() > 25) {
      console.log('🐌 Poor performance detected, showing dashboard');
      toggleDashboard();
    }
  }, 5000);
  
  console.log('📊 Performance Dashboard loaded - Press "P" to toggle');
  
})();
