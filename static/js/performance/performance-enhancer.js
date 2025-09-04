/**
 * Clever Performance Enhancement Suite
 * Advanced optimizations for smoother particle rendering
 */

(function() {
  'use strict';
  
  // Performance Enhancement Configuration
  const PERF_CONFIG = {
    // WebGL detection and fallback
    webglEnabled: false,
    webglContext: null,
    
    // Advanced batching
    batchSize: 50,
    renderBatches: true,
    
    // GPU optimization
    offscreenCanvas: null,
    offscreenCtx: null,
    
    // Memory pools
    particlePool: [],
    projectionCache: new Map(),
    
    // Frame rate targets
    adaptiveQuality: true,
    targetFPS: 60,
    maxFrameTime: 16.67, // ~60fps
    
    // Hardware detection
    hardwareInfo: {
      cores: navigator.hardwareConcurrency || 4,
      deviceMemory: navigator.deviceMemory || 4,
      isMobile: /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
      hasTouch: 'ontouchstart' in window,
      pixelRatio: window.devicePixelRatio || 1
    }
  };
  
  // Initialize WebGL if available
  function initWebGL(canvas) {
    try {
      const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
      if (gl) {
        PERF_CONFIG.webglEnabled = true;
        PERF_CONFIG.webglContext = gl;
        console.log('🚀 WebGL acceleration enabled');
        return true;
      }
    } catch (e) {
      console.warn('WebGL initialization failed:', e);
    }
    return false;
  }
  
  // Advanced particle batching system
  class ParticleBatcher {
    constructor(ctx, webgl = false) {
      this.ctx = ctx;
      this.webgl = webgl;
      this.batches = [];
      this.currentBatch = null;
      this.batchCount = 0;
    }
    
    startBatch(style) {
      this.currentBatch = {
        particles: [],
        style: style,
        count: 0
      };
    }
    
    addParticle(x, y, size, alpha, color) {
      if (!this.currentBatch || this.currentBatch.count >= PERF_CONFIG.batchSize) {
        this.finishBatch();
        this.startBatch(this.currentBatch?.style || {});
      }
      
      this.currentBatch.particles.push({ x, y, size, alpha, color });
      this.currentBatch.count++;
    }
    
    finishBatch() {
      if (this.currentBatch && this.currentBatch.count > 0) {
        this.batches.push(this.currentBatch);
        this.currentBatch = null;
      }
    }
    
    renderBatches() {
      // Render all batches with optimized canvas state changes
      for (const batch of this.batches) {
        this.renderBatch(batch);
      }
      this.batches.length = 0; // Clear batches
    }
    
    renderBatch(batch) {
      const ctx = this.ctx;
      
      // Set common batch properties once
      ctx.globalCompositeOperation = 'screen';
      
      for (const particle of batch.particles) {
        // Optimized particle rendering
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2, false);
        ctx.fillStyle = particle.color;
        ctx.fill();
      }
      
      ctx.globalCompositeOperation = 'source-over';
    }
  }
  
  // Memory pool for particle objects
  class MemoryPool {
    constructor(initialSize = 100) {
      this.pool = [];
      this.active = [];
      
      // Pre-allocate objects
      for (let i = 0; i < initialSize; i++) {
        this.pool.push(this.createObject());
      }
    }
    
    createObject() {
      return {
        x: 0, y: 0, z: 0,
        tx: 0, ty: 0, tz: 0,
        sx: 0, sy: 0,
        phase: 0, speed: 0, life: 0, size: 0,
        depth: 0, scale: 0
      };
    }
    
    acquire() {
      if (this.pool.length > 0) {
        const obj = this.pool.pop();
        this.active.push(obj);
        return obj;
      }
      
      // Pool exhausted, create new object
      const newObj = this.createObject();
      this.active.push(newObj);
      return newObj;
    }
    
    release(obj) {
      const index = this.active.indexOf(obj);
      if (index > -1) {
        this.active.splice(index, 1);
        this.pool.push(obj);
      }
    }
    
    releaseAll() {
      this.pool.push(...this.active);
      this.active.length = 0;
    }
  }
  
  // Adaptive Quality Manager
  class QualityManager {
    constructor() {
      this.frameHistory = new Array(30).fill(16.67);
      this.historyIndex = 0;
      this.adjustmentCooldown = 0;
      this.lastQualityChange = 0;
      
      this.qualityLevels = {
        ultra: { particles: 2400, stride: 1, glow: 1.2, effects: 1.0 },
        high:  { particles: 1800, stride: 1, glow: 1.0, effects: 0.9 },
        med:   { particles: 1200, stride: 2, glow: 0.8, effects: 0.7 },
        low:   { particles: 800,  stride: 3, glow: 0.6, effects: 0.5 },
        potato:{ particles: 400,  stride: 4, glow: 0.4, effects: 0.3 }
      };
      
      this.currentLevel = 'high';
    }
    
    recordFrameTime(frameTime) {
      this.frameHistory[this.historyIndex] = frameTime;
      this.historyIndex = (this.historyIndex + 1) % this.frameHistory.length;
      
      if (this.adjustmentCooldown > 0) {
        this.adjustmentCooldown--;
        return this.currentLevel;
      }
      
      const avgFrameTime = this.frameHistory.reduce((a, b) => a + b) / this.frameHistory.length;
      const now = performance.now();
      
      // Only adjust if we have significant performance change
      if (now - this.lastQualityChange < 2000) return this.currentLevel;
      
      const levels = Object.keys(this.qualityLevels);
      const currentIndex = levels.indexOf(this.currentLevel);
      
      if (avgFrameTime > 20 && currentIndex < levels.length - 1) {
        // Performance poor, reduce quality
        this.currentLevel = levels[currentIndex + 1];
        this.adjustmentCooldown = 30;
        this.lastQualityChange = now;
        console.log(`🔻 Quality reduced to ${this.currentLevel} (avg: ${avgFrameTime.toFixed(1)}ms)`);
      } else if (avgFrameTime < 14 && currentIndex > 0) {
        // Performance good, increase quality
        this.currentLevel = levels[currentIndex - 1];
        this.adjustmentCooldown = 60; // Be more conservative when increasing
        this.lastQualityChange = now;
        console.log(`🔺 Quality increased to ${this.currentLevel} (avg: ${avgFrameTime.toFixed(1)}ms)`);
      }
      
      return this.currentLevel;
    }
    
    getSettings() {
      return this.qualityLevels[this.currentLevel];
    }
  }
  
  // Optimized 3D projection with caching
  class ProjectionOptimizer {
    constructor() {
      this.cache = new Map();
      this.cacheHits = 0;
      this.cacheMisses = 0;
      this.maxCacheSize = 1000;
    }
    
    project3D(x, y, z, camera, canvas) {
      // Create cache key (rounded to reduce cache size)
      const key = `${Math.round(x*10)}:${Math.round(y*10)}:${Math.round(z*10)}:${Math.round(camera.rotY*1000)}`;
      
      if (this.cache.has(key)) {
        this.cacheHits++;
        return this.cache.get(key);
      }
      
      this.cacheMisses++;
      
      // Standard 3D projection
      const cosY = Math.cos(camera.rotY);
      const sinY = Math.sin(camera.rotY);
      const rotX = cosY * x - sinY * z;
      const rotZ = sinY * x + cosY * z;
      
      const cosX = Math.cos(camera.rotX);
      const sinX = Math.sin(camera.rotX);
      const finalY = cosX * y - sinX * rotZ;
      const finalZ = sinX * y + cosX * rotZ + camera.z;
      
      if (finalZ > -50) return null;
      
      const scale = camera.fov / -finalZ;
      const result = {
        x: canvas.width/2 + rotX * scale,
        y: canvas.height/2 + finalY * scale,
        z: finalZ,
        scale: scale
      };
      
      // Cache the result
      if (this.cache.size >= this.maxCacheSize) {
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
      
      this.cache.set(key, result);
      return result;
    }
    
    clearCache() {
      this.cache.clear();
    }
    
    getStats() {
      const total = this.cacheHits + this.cacheMisses;
      return {
        hitRate: total > 0 ? (this.cacheHits / total * 100).toFixed(1) : 0,
        size: this.cache.size
      };
    }
  }
  
  // Export performance enhancement tools
  window.CleverPerformance = {
    config: PERF_CONFIG,
    ParticleBatcher,
    MemoryPool,
    QualityManager,
    ProjectionOptimizer,
    initWebGL
  };
  
  // Initialize hardware detection
  console.log('🔧 Clever Performance Suite initialized');
  console.log('📊 Hardware:', PERF_CONFIG.hardwareInfo);
  
})();
