/**
 * Clever Evolution Visualizer - Real-time Intelligence Growth Display
 * Shows Clever's autonomous learning and capability development
 */

class CleverEvolutionVisualizer {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.evolutionData = null;
        this.conceptNodes = [];
        this.connections = [];
        this.capabilities = {};
        this.animationId = null;
        this.pulsePhase = 0;
        this.lastUpdate = 0;
        
        this.init();
    }
    
    init() {
        this.createEvolutionCanvas();
        this.createEvolutionPanel();
        this.startEvolutionMonitoring();
        this.animate();
    }
    
    createEvolutionCanvas() {
        // Create dedicated evolution canvas
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'clever-evolution-canvas';
        this.canvas.style.position = 'fixed';
        this.canvas.style.bottom = '20px';
        this.canvas.style.right = '20px';
        this.canvas.style.width = '300px';
        this.canvas.style.height = '200px';
        this.canvas.style.border = '2px solid #00ffff';
        this.canvas.style.borderRadius = '15px';
        this.canvas.style.backgroundColor = 'rgba(0, 20, 40, 0.9)';
        this.canvas.style.backdropFilter = 'blur(10px)';
        this.canvas.style.zIndex = '1002';
        this.canvas.style.opacity = '0.9';
        
        document.body.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        
        // Set actual canvas size
        this.canvas.width = 300;
        this.canvas.height = 200;
    }
    
    createEvolutionPanel() {
        // Create floating evolution status panel
        const panel = document.createElement('div');
        panel.id = 'evolution-status-panel';
        panel.innerHTML = `
            <div class="evolution-header">
                <h3>🧠 Clever's Mind</h3>
                <div class="evolution-score">Evolution: <span id="evolution-score">0%</span></div>
            </div>
            <div class="evolution-stats">
                <div class="stat-item">
                    <span class="stat-label">Concepts:</span>
                    <span id="concept-count">0</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Connections:</span>
                    <span id="connection-count">0</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Network Density:</span>
                    <span id="network-density">0%</span>
                </div>
            </div>
            <div class="capabilities-section">
                <h4>🚀 Capabilities</h4>
                <div id="capabilities-list"></div>
            </div>
            <div class="recent-events">
                <h4>📈 Recent Growth</h4>
                <div id="evolution-events"></div>
            </div>
        `;
        
        // Style the panel
        panel.style.position = 'fixed';
        panel.style.bottom = '240px';
        panel.style.right = '20px';
        panel.style.width = '300px';
        panel.style.maxHeight = '400px';
        panel.style.overflowY = 'auto';
        panel.style.background = 'rgba(0, 20, 40, 0.95)';
        panel.style.border = '2px solid #00ffff';
        panel.style.borderRadius = '15px';
        panel.style.padding = '15px';
        panel.style.color = '#00ffff';
        panel.style.fontFamily = 'monospace';
        panel.style.fontSize = '12px';
        panel.style.backdropFilter = 'blur(15px)';
        panel.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.3)';
        panel.style.zIndex = '1001';
        panel.style.transform = 'translateX(100%)';
        panel.style.transition = 'transform 0.5s ease-out';
        
        // Add CSS for internal elements
        const style = document.createElement('style');
        style.textContent = `
            #evolution-status-panel .evolution-header {
                text-align: center;
                margin-bottom: 15px;
                border-bottom: 1px solid #00ffff;
                padding-bottom: 10px;
            }
            
            #evolution-status-panel h3 {
                margin: 0;
                color: #ff00ff;
                text-shadow: 0 0 10px #ff00ff;
            }
            
            #evolution-status-panel .evolution-score {
                margin-top: 5px;
                font-weight: bold;
            }
            
            #evolution-status-panel .stat-item {
                display: flex;
                justify-content: space-between;
                margin: 5px 0;
                padding: 3px 0;
            }
            
            #evolution-status-panel .stat-label {
                color: #88ccff;
            }
            
            #evolution-status-panel h4 {
                margin: 15px 0 8px 0;
                color: #ffaa00;
                border-bottom: 1px solid #ffaa00;
                padding-bottom: 3px;
            }
            
            #evolution-status-panel .capability-item {
                display: flex;
                justify-content: space-between;
                margin: 3px 0;
                font-size: 11px;
            }
            
            #evolution-status-panel .capability-bar {
                width: 60px;
                height: 8px;
                background: rgba(0, 255, 255, 0.2);
                border-radius: 4px;
                overflow: hidden;
            }
            
            #evolution-status-panel .capability-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ffff, #ff00ff);
                transition: width 0.5s ease;
            }
            
            #evolution-status-panel .evolution-event {
                margin: 3px 0;
                font-size: 10px;
                color: #cccccc;
                border-left: 2px solid #00ff00;
                padding-left: 5px;
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(panel);
        
        // Slide in after a moment
        setTimeout(() => {
            panel.style.transform = 'translateX(0)';
        }, 1000);
    }
    
    async fetchEvolutionData() {
        try {
            const response = await fetch('/evolution-status', {
                cache: 'no-cache'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.updateEvolutionData(data);
            }
        } catch (error) {
            console.log('Evolution data not available:', error);
        }
    }
    
    updateEvolutionData(data) {
        this.evolutionData = data;
        
        // Update concept nodes for visualization
        this.updateConceptNodes(data);
        
        // Update UI elements
        this.updateEvolutionPanel(data);
        
        // Update canvas visualization
        this.updateEvolutionVisualization(data);
    }
    
    updateConceptNodes(data) {
        const targetNodes = Math.min(50, data.concept_count || 0);
        
        // Add new nodes if needed
        while (this.conceptNodes.length < targetNodes) {
            this.conceptNodes.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 3 + 2,
                hue: Math.random() * 60 + 180,
                energy: Math.random() * 0.5 + 0.3,
                age: 0,
                connections: []
            });
        }
        
        // Remove excess nodes
        if (this.conceptNodes.length > targetNodes) {
            this.conceptNodes = this.conceptNodes.slice(0, targetNodes);
        }
        
        // Create connections based on network density
        const density = data.network_density || 0;
        const targetConnections = Math.floor(this.conceptNodes.length * density * 2);
        
        this.connections = [];
        for (let i = 0; i < targetConnections && i < this.conceptNodes.length - 1; i++) {
            const nodeA = this.conceptNodes[i];
            const nodeB = this.conceptNodes[i + 1];
            
            this.connections.push({
                nodeA: nodeA,
                nodeB: nodeB,
                strength: Math.random() * 0.5 + 0.3,
                age: 0
            });
        }
    }
    
    updateEvolutionPanel(data) {
        // Update main stats
        document.getElementById('evolution-score').textContent = 
            Math.round((data.evolution_score || 0) * 100) + '%';
        document.getElementById('concept-count').textContent = data.concept_count || 0;
        document.getElementById('connection-count').textContent = data.connection_count || 0;
        document.getElementById('network-density').textContent = 
            Math.round((data.network_density || 0) * 100) + '%';
        
        // Update capabilities
        const capabilitiesList = document.getElementById('capabilities-list');
        capabilitiesList.innerHTML = '';
        
        const capabilities = data.capabilities || {};
        Object.entries(capabilities).forEach(([name, level]) => {
            const capItem = document.createElement('div');
            capItem.className = 'capability-item';
            
            const displayName = name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            const percentage = Math.round(level * 100);
            
            capItem.innerHTML = `
                <span>${displayName}</span>
                <div class="capability-bar">
                    <div class="capability-fill" style="width: ${percentage}%"></div>
                </div>
            `;
            
            capabilitiesList.appendChild(capItem);
        });
        
        // Update recent events
        const eventsContainer = document.getElementById('evolution-events');
        eventsContainer.innerHTML = '';
        
        const events = data.recent_events || [];
        events.slice(0, 5).forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.className = 'evolution-event';
            
            const timestamp = new Date(event[3]).toLocaleTimeString();
            eventDiv.innerHTML = `<strong>${event[1]}</strong><br><small>${timestamp}</small>`;
            
            eventsContainer.appendChild(eventDiv);
        });
    }
    
    updateEvolutionVisualization(data) {
        // Trigger visual effects based on evolution score
        const evolutionScore = data.evolution_score || 0;
        
        // Increase energy of nodes based on evolution
        this.conceptNodes.forEach(node => {
            node.energy = Math.min(1, node.energy + evolutionScore * 0.1);
            
            if (evolutionScore > 0.5) {
                node.hue = 300; // Purple for high evolution
            } else if (evolutionScore > 0.3) {
                node.hue = 180; // Cyan for medium evolution
            } else {
                node.hue = 120; // Green for basic evolution
            }
        });
    }
    
    renderEvolutionCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections first
        this.connections.forEach(connection => {
            const alpha = connection.strength * 0.6;
            
            this.ctx.save();
            this.ctx.globalAlpha = alpha;
            this.ctx.strokeStyle = `hsl(180, 70%, 60%)`;
            this.ctx.lineWidth = connection.strength * 2;
            this.ctx.beginPath();
            this.ctx.moveTo(connection.nodeA.x, connection.nodeA.y);
            this.ctx.lineTo(connection.nodeB.x, connection.nodeB.y);
            this.ctx.stroke();
            this.ctx.restore();
            
            connection.age += 0.01;
        });
        
        // Draw concept nodes
        this.conceptNodes.forEach(node => {
            const pulse = Math.sin(this.pulsePhase + node.age) * 0.3 + 0.7;
            const size = node.size * pulse;
            const alpha = node.energy * 0.8;
            
            this.ctx.save();
            this.ctx.globalAlpha = alpha;
            this.ctx.fillStyle = `hsl(${node.hue}, 70%, 60%)`;
            this.ctx.shadowBlur = size * 2;
            this.ctx.shadowColor = `hsl(${node.hue}, 70%, 60%)`;
            
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, size, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.restore();
            
            // Update node physics
            node.x += node.vx;
            node.y += node.vy;
            
            // Boundary conditions
            if (node.x < 0 || node.x > this.canvas.width) node.vx *= -0.8;
            if (node.y < 0 || node.y > this.canvas.height) node.vy *= -0.8;
            
            node.x = Math.max(0, Math.min(this.canvas.width, node.x));
            node.y = Math.max(0, Math.min(this.canvas.height, node.y));
            
            // Apply drag
            node.vx *= 0.98;
            node.vy *= 0.98;
            
            node.age += 0.02;
        });
        
        // Draw evolution score overlay
        if (this.evolutionData) {
            const score = Math.round((this.evolutionData.evolution_score || 0) * 100);
            
            this.ctx.save();
            this.ctx.fillStyle = '#00ffff';
            this.ctx.font = '14px monospace';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(`Evolution: ${score}%`, this.canvas.width / 2, 25);
            this.ctx.restore();
        }
    }
    
    animate() {
        this.pulsePhase += 0.05;
        this.renderEvolutionCanvas();
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    startEvolutionMonitoring() {
        // Initial fetch
        this.fetchEvolutionData();
        
        // Periodic updates
        setInterval(() => {
            this.fetchEvolutionData();
        }, 5000); // Every 5 seconds
    }
    
    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        const canvas = document.getElementById('clever-evolution-canvas');
        const panel = document.getElementById('evolution-status-panel');
        
        if (canvas && canvas.parentNode) {
            canvas.parentNode.removeChild(canvas);
        }
        
        if (panel && panel.parentNode) {
            panel.parentNode.removeChild(panel);
        }
    }
}

// Auto-initialize evolution visualizer
document.addEventListener('DOMContentLoaded', () => {
    // Delay initialization to let other systems load first
    setTimeout(() => {
        window.cleverEvolutionUI = new CleverEvolutionVisualizer();
        console.log('🧠 Clever Evolution Visualizer initialized');
    }, 2000);
});

// Export for manual control
window.CleverEvolutionVisualizer = CleverEvolutionVisualizer;
