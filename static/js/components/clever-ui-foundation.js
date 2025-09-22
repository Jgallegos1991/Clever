/*
Clever Holographic UI Components - Modular Foundation System

Why: Create a stable, performant foundation that can scale into complex holographic interfaces
     without breaking. Each component is self-contained and Chrome OS optimized.
Where: Imported by main.js and used to build floating panels, analysis displays, and chat systems
How: Object-oriented component system with lifecycle management, positioning, and animations

Connects to:
    - main.js: Primary UI controller and event handling
    - holographic-chamber.js: Particle system integration and formation status
    - style.css: CSS variables and base styling for consistent theming
*/

class CleverUIFoundation {
    constructor() {
        this.components = new Map();
        this.panels = new Map();
        this.activeAnimations = new Set();
        this.performanceMode = 'auto'; // auto, minimal, full
        
        // Chrome OS performance constraints
        this.maxActiveComponents = 8;
        this.animationThrottle = 16; // ~60fps
        
        this.init();
    }

    init() {
        // Create base UI layers
        this.createUILayers();
        
        // Set up component lifecycle management
        this.setupComponentLifecycle();
        
        // Performance monitoring for Chrome OS
        this.setupPerformanceMonitoring();
        
        console.log('[CleverUI] Foundation initialized with performance mode:', this.performanceMode);
    }

    createUILayers() {
        // Create layered UI structure for proper z-indexing
        this.layers = {
            background: this.createLayer('ui-background', 1),
            analysis: this.createLayer('ui-analysis', 5),
            chat: this.createLayer('ui-chat', 10),
            status: this.createLayer('ui-status', 15),
            overlay: this.createLayer('ui-overlay', 20)
        };
    }

    createLayer(id, zIndex) {
        const layer = document.createElement('div');
        layer.id = id;
        layer.style.cssText = `
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: ${zIndex};
            contain: layout style paint;
        `;
        document.body.appendChild(layer);
        return layer;
    }

    setupComponentLifecycle() {
        // Component cleanup to prevent memory leaks
        this.cleanupInterval = setInterval(() => {
            this.cleanupInactiveComponents();
        }, 30000); // Every 30 seconds
    }

    setupPerformanceMonitoring() {
        // Monitor frame rate and adjust performance mode
        let frameCount = 0;
        let lastTime = performance.now();
        
        const monitorPerformance = () => {
            frameCount++;
            const currentTime = performance.now();
            
            if (currentTime - lastTime >= 1000) {
                const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                
                if (fps < 45 && this.performanceMode !== 'minimal') {
                    this.performanceMode = 'minimal';
                    this.optimizeForPerformance();
                } else if (fps > 55 && this.performanceMode === 'minimal') {
                    this.performanceMode = 'auto';
                }
                
                frameCount = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(monitorPerformance);
        };
        
        requestAnimationFrame(monitorPerformance);
    }

    optimizeForPerformance() {
        // Reduce animations and effects for Chrome OS
        document.documentElement.style.setProperty('--animation-duration', '0.2s');
        document.documentElement.style.setProperty('--blur-strength', '3px');
        
        // Limit active components
        const activeComponents = Array.from(this.components.values())
            .filter(comp => comp.active)
            .sort((a, b) => b.priority - a.priority);
            
        if (activeComponents.length > this.maxActiveComponents) {
            activeComponents.slice(this.maxActiveComponents).forEach(comp => {
                comp.minimize();
            });
        }
    }

    createComponent(type, options = {}) {
        const componentId = `${type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        let component;
        switch (type) {
            case 'floating-panel':
                component = new FloatingPanel(componentId, options, this);
                break;
            case 'analysis-display':
                component = new AnalysisDisplay(componentId, options, this);
                break;
            case 'chat-bubble':
                component = new ChatBubble(componentId, options, this);
                break;
            case 'status-indicator':
                component = new StatusIndicator(componentId, options, this);
                break;
            default:
                console.warn('[CleverUI] Unknown component type:', type);
                return null;
        }
        
        this.components.set(componentId, component);
        return component;
    }

    removeComponent(componentId) {
        const component = this.components.get(componentId);
        if (component) {
            component.destroy();
            this.components.delete(componentId);
        }
    }

    cleanupInactiveComponents() {
        const toRemove = [];
        this.components.forEach((component, id) => {
            if (!component.active && component.lastActivity < Date.now() - 60000) {
                toRemove.push(id);
            }
        });
        
        toRemove.forEach(id => this.removeComponent(id));
    }
}

// Base Component Class
class UIComponent {
    constructor(id, options, foundation) {
        this.id = id;
        this.foundation = foundation;
        this.options = { ...this.defaultOptions, ...options };
        this.element = null;
        this.active = false;
        this.priority = this.options.priority || 1;
        this.lastActivity = Date.now();
        
        this.create();
    }

    get defaultOptions() {
        return {
            priority: 1,
            persistent: false,
            animation: true,
            layer: 'overlay'
        };
    }

    create() {
        this.element = document.createElement('div');
        this.element.className = `clever-component ${this.constructor.name.toLowerCase()}`;
        this.element.id = this.id;
        
        this.setupElement();
        this.attachToLayer();
        
        if (this.options.animation) {
            this.animateIn();
        }
    }

    setupElement() {
        // Override in subclasses
    }

    attachToLayer() {
        const layer = this.foundation.layers[this.options.layer];
        if (layer) {
            layer.appendChild(this.element);
        }
    }

    animateIn() {
        if (this.foundation.performanceMode === 'minimal') return;
        
        this.element.style.opacity = '0';
        this.element.style.transform = 'translateY(10px) scale(0.95)';
        
        requestAnimationFrame(() => {
            this.element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            this.element.style.opacity = '1';
            this.element.style.transform = 'translateY(0) scale(1)';
        });
    }

    animateOut(callback) {
        if (this.foundation.performanceMode === 'minimal') {
            if (callback) callback();
            return;
        }
        
        this.element.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        this.element.style.opacity = '0';
        this.element.style.transform = 'translateY(-10px) scale(0.95)';
        
        setTimeout(() => {
            if (callback) callback();
        }, 200);
    }

    show() {
        this.active = true;
        this.lastActivity = Date.now();
        this.element.style.display = 'block';
        if (this.options.animation) this.animateIn();
    }

    hide() {
        this.active = false;
        if (this.options.animation) {
            this.animateOut(() => {
                this.element.style.display = 'none';
            });
        } else {
            this.element.style.display = 'none';
        }
    }

    minimize() {
        // Reduce visual complexity for performance
        this.element.style.filter = 'none';
        this.element.style.backdropFilter = 'none';
    }

    destroy() {
        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }
    }
}

// Export for use in main.js
window.CleverUIFoundation = CleverUIFoundation;
window.UIComponent = UIComponent;