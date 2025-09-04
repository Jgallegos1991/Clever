/**
 * Clever Performance Quick - Lightweight performance monitoring stub
 * Provides basic compatibility for performance dashboard
 */

(function() {
  'use strict';
  
  // Minimal performance monitoring stub
  window.CleverPerformanceQuick = {
    monitor: {
      getAverageFrameTime: function() {
        return 16.67; // 60 FPS
      },
      getFrameRate: function() {
        return 60;
      },
      getMetrics: function() {
        return {
          fps: 60,
          frameTime: 16.67,
          particles: 1800,
          renderTime: 8.0,
          memoryUsage: 'Optimal'
        };
      }
    },
    
    startFrame: function() {
      return performance.now();
    },
    
    endFrame: function(startTime) {
      return performance.now() - startTime;
    },
    
    getMetrics: function() {
      return {
        fps: 60,
        frameTime: 16.67,
        particles: 1800,
        renderTime: 8.0,
        memoryUsage: 'Optimal'
      };
    },
    
    isEnabled: function() {
      return true;
    }
  };
  
  console.log('🚀 CleverPerformanceQuick stub loaded');
})();
