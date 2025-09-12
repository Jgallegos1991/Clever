// Performance Dashboard - Monitor FPS and system performance
// Quick performance monitoring for Clever UI

class PerformanceDashboard {
  constructor() {
    this.fps = 0;
    this.lastTime = 0;
    this.frameCount = 0;
    this.isMonitoring = false;
    
    // Create minimal performance display
    this.createDisplay();
    this.bindControls();
  }

  createDisplay() {
    // Only show if debug mode or requested
    if (!window.location.search.includes('debug')) return;
    
    this.display = document.createElement('div');
    this.display.id = 'perf-dashboard';
    this.display.style.cssText = `
      position: fixed;
      top: 50px;
      right: 12px;
      background: rgba(11, 15, 20, 0.9);
      color: #69EACB;
      font-family: 'Courier New', monospace;
      font-size: 11px;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid rgba(105, 234, 203, 0.3);
      backdrop-filter: blur(8px);
      z-index: 9998;
      min-width: 80px;
      text-align: right;
    `;
    
    document.body.appendChild(this.display);
    this.updateDisplay();
  }

  bindControls() {
    // Toggle with Ctrl+Shift+P
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        this.toggle();
      }
    });
  }

  toggle() {
    this.isMonitoring = !this.isMonitoring;
    
    if (!this.display) {
      this.createDisplay();
    }
    
    if (this.display) {
      this.display.style.display = this.isMonitoring ? 'block' : 'none';
    }
    
    if (this.isMonitoring) {
      this.startMonitoring();
    }
  }

  startMonitoring() {
    const monitor = (currentTime) => {
      if (!this.isMonitoring) return;
      
      if (this.lastTime) {
        const delta = currentTime - this.lastTime;
        this.fps = Math.round(1000 / delta);
        this.frameCount++;
        
        // Update display every 10 frames
        if (this.frameCount % 10 === 0) {
          this.updateDisplay();
        }
      }
      
      this.lastTime = currentTime;
      requestAnimationFrame(monitor);
    };
    
    requestAnimationFrame(monitor);
  }

  updateDisplay() {
    if (!this.display) return;
    
    const memoryInfo = performance.memory ? 
      `${Math.round(performance.memory.usedJSHeapSize / 1048576)}MB` : 
      'N/A';
      
    this.display.innerHTML = `
      FPS: ${this.fps}<br>
      MEM: ${memoryInfo}<br>
      Particles: ${this.getParticleCount()}
    `;
    
    // Color code FPS
    if (this.fps >= 45) {
      this.display.style.color = '#69EACB'; // Good
    } else if (this.fps >= 30) {
      this.display.style.color = '#FFB366'; // Warning
    } else {
      this.display.style.color = '#FF6B6B'; // Poor
    }
  }

  getParticleCount() {
    // Try to get particle count from active systems
    if (window.holographicChamber && window.holographicChamber.particles) {
      return window.holographicChamber.particles.length;
    }
    return 0;
  }

  // Public API
  logPerformance(label, duration) {
    if (this.isMonitoring) {
      console.log(`⚡ ${label}: ${duration.toFixed(2)}ms`);
    }
  }

  measureFunction(fn, label) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    this.logPerformance(label, end - start);
    return result;
  }
}

// Auto-initialize
let perfDashboard = null;

document.addEventListener('DOMContentLoaded', () => {
  perfDashboard = new PerformanceDashboard();
  
  // Auto-start if debug mode
  if (window.location.search.includes('debug')) {
    perfDashboard.toggle();
  }
});

// Export for global access
window.PerformanceDashboard = PerformanceDashboard;
window.getPerfDashboard = () => perfDashboard;