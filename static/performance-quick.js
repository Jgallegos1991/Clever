/**
 * Clever Performance Boost - Quick Implementation
 * Essential performance optimizations without complex batching
 */

(function() {
  'use strict';
  
  console.log('⚡ Quick Performance Boost Loading...');
  
  // Performance monitoring
  class SimplePerformanceMonitor {
    constructor() {
      this.frameHistory = [];
      this.maxHistory = 30;
      this.lastFrameTime = performance.now();
    }
    
    update() {
      const now = performance.now();
      const frameTime = now - this.lastFrameTime;
      this.lastFrameTime = now;
      
      this.frameHistory.push(frameTime);
      if (this.frameHistory.length > this.maxHistory) {
        this.frameHistory.shift();
      }
      
      return frameTime;
    }
    
    getAverageFrameTime() {
      if (this.frameHistory.length === 0) return 16.67;
      return this.frameHistory.reduce((a, b) => a + b) / this.frameHistory.length;
    }
    
    getFPS() {
      return Math.round(1000 / this.getAverageFrameTime());
    }
    
    shouldReduceQuality() {
      return this.getAverageFrameTime() > 20; // Below 50fps
    }
    
    shouldIncreaseQuality() {
      return this.getAverageFrameTime() < 14; // Above 70fps
    }
  }
  
  // Hardware detection
  const hardwareInfo = {
    cores: navigator.hardwareConcurrency || 4,
    memory: navigator.deviceMemory || 4,
    isMobile: /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
    pixelRatio: window.devicePixelRatio || 1,
    hasTouch: 'ontouchstart' in window
  };
  
  // Quality presets
  const qualityPresets = {
    potato: { particles: 400, stride: 4, glow: 0.3, name: 'Potato 🥔' },
    low: { particles: 800, stride: 3, glow: 0.5, name: 'Low' },
    medium: { particles: 1200, stride: 2, glow: 0.7, name: 'Medium' },
    high: { particles: 1800, stride: 1, glow: 1.0, name: 'High' },
    ultra: { particles: 2400, stride: 1, glow: 1.2, name: 'Ultra ⚡' }
  };
  
  // Auto-detect initial quality
  function getInitialQuality() {
    if (hardwareInfo.isMobile) return 'low';
    if (hardwareInfo.cores >= 8 && hardwareInfo.memory >= 8) return 'ultra';
    if (hardwareInfo.cores >= 4 && hardwareInfo.memory >= 4) return 'high';
    return 'medium';
  }
  
  // Optimized canvas operations
  const canvasOptimizations = {
    // Pre-compile color strings
    colorCache: new Map(),
    
    getRGBAString(r, g, b, a) {
      const key = `${r},${g},${b},${a}`;
      if (this.colorCache.has(key)) {
        return this.colorCache.get(key);
      }
      
      const color = `rgba(${r},${g},${b},${a})`;
      if (this.colorCache.size > 100) {
        this.colorCache.clear(); // Prevent memory leak
      }
      this.colorCache.set(key, color);
      return color;
    },
    
    // Batch similar drawing operations
    batchDrawCircles(ctx, circles) {
      ctx.save();
      for (const circle of circles) {
        ctx.beginPath();
        ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
        ctx.fillStyle = circle.color;
        ctx.fill();
      }
      ctx.restore();
    }
  };
  
  // Export performance tools
  window.CleverPerformanceQuick = {
    monitor: new SimplePerformanceMonitor(),
    hardware: hardwareInfo,
    qualityPresets: qualityPresets,
    initialQuality: getInitialQuality(),
    canvas: canvasOptimizations,
    
    // Simple quality adjustment
    adjustQuality(currentSettings, frameTime) {
      if (frameTime > 25) { // Very poor performance
        if (currentSettings.stride < 4) return { ...currentSettings, stride: Math.min(4, currentSettings.stride + 1) };
      } else if (frameTime > 20) { // Poor performance
        if (currentSettings.glow > 0.3) return { ...currentSettings, glow: Math.max(0.3, currentSettings.glow - 0.1) };
      } else if (frameTime < 12) { // Excellent performance
        if (currentSettings.stride > 1) return { ...currentSettings, stride: Math.max(1, currentSettings.stride - 1) };
        if (currentSettings.glow < 1.2) return { ...currentSettings, glow: Math.min(1.2, currentSettings.glow + 0.1) };
      }
      return currentSettings;
    }
  };
  
  console.log('⚡ Performance Boost Ready!');
  console.log('🖥️ Hardware:', hardwareInfo);
  console.log('🎯 Initial Quality:', getInitialQuality());
  
})();
