/*
Cognitive Status Component - Real-time Cognitive State Monitoring

Why: Displays Clever's cognitive health and connection status for system observation
Where: Loaded by templates/index.html to provide real-time cognitive feedback
How: Creates floating status overlay with live particle system metrics

Connects to:
    - static/js/engines/holographic-chamber.js: Reads from window.cleverCognitiveStatus
    - static/js/main.js: Displays cognitive maintenance loop status
    - static/css/style.css: Uses status overlay styling
    - app.py: Provides cognitive metrics for debugging and optimization
*/

console.log('🧠 Cognitive Status component loading...');

/**
 * Create Cognitive Status Overlay
 * 
 * Why: Provides real-time visibility into Clever's cognitive processing state
 * Where: Called during initialization to create persistent status display
 * How: Creates floating overlay with live-updating metrics from particle system
 * 
 * Connects to:
 *     - templates/index.html: Appends status overlay to body
 *     - static/js/engines/holographic-chamber.js: Reads cognitive status data
 *     - static/css/style.css: Uses .cognitive-status styling
 */
function createCognitiveStatusOverlay() {
    // Create status container (hidden by default for better mobile experience)
    const statusOverlay = document.createElement('div');
    statusOverlay.id = 'cognitive-status';
    statusOverlay.className = 'cognitive-status';
    statusOverlay.style.display = 'none'; // Hidden by default
    statusOverlay.innerHTML = `
        <div class="status-header">
            <span class="status-icon">🧠</span>
            <span class="status-title">Cognitive Status</span>
        </div>
        <div class="status-metrics">
            <div class="metric">
                <span class="metric-label">Coherence:</span>
                <span class="metric-value" id="coherence-value">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Energy:</span>
                <span class="metric-value" id="energy-value">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Mode:</span>
                <span class="metric-value" id="mode-value">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Formation:</span>
                <span class="metric-value" id="formation-value">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Connection:</span>
                <span class="metric-value status-indicator" id="connection-status">🟢</span>
            </div>
        </div>
    `;
    
    document.body.appendChild(statusOverlay);
    
    // Add toggle functionality
    setupCognitiveStatusToggle();
    
    // Start updating the status
    startStatusUpdates();
    
    console.log('✅ Cognitive status overlay created (hidden by default for mobile)');
}

/**
 * Start Status Updates
 * 
 * Why: Continuously updates cognitive status display with live system metrics
 * Where: Called after overlay creation to maintain real-time feedback
 * How: Periodic polling of cognitive status and DOM updates
 */
function startStatusUpdates() {
    setInterval(() => {
        updateCognitiveStatus();
    }, 1000); // Update every second
}

/**
 * Update Cognitive Status Display
 * 
 * Why: Refreshes status overlay with current cognitive metrics
 * Where: Called by status update interval for live monitoring
 * How: Reads from window.cleverCognitiveStatus and updates DOM elements
 */
function updateCognitiveStatus() {
    // Get cognitive status from particle system
    const status = window.cleverCognitiveStatus || {};
    
    // Update coherence percentage
    const coherenceEl = document.getElementById('coherence-value');
    if (coherenceEl && status.coherence !== undefined) {
        const coherencePercent = Math.round(status.coherence * 100);
        coherenceEl.textContent = coherencePercent + '%';
        coherenceEl.className = 'metric-value ' + getCognitiveHealthClass(coherencePercent);
    }
    
    // Update energy percentage
    const energyEl = document.getElementById('energy-value');
    if (energyEl && status.energy !== undefined) {
        const energyPercent = Math.round(status.energy * 100);
        energyEl.textContent = energyPercent + '%';
        energyEl.className = 'metric-value ' + getCognitiveHealthClass(energyPercent);
    }
    
    // Update mode
    const modeEl = document.getElementById('mode-value');
    if (modeEl && status.mode) {
        modeEl.textContent = status.mode;
        modeEl.className = 'metric-value mode-' + status.mode;
    }
    
    // Update formation
    const formationEl = document.getElementById('formation-value');
    if (formationEl && status.formation) {
        formationEl.textContent = status.formation.replace('_', ' ');
    }
    
    // Update connection status
    const connectionEl = document.getElementById('connection-status');
    if (connectionEl) {
        const isConnected = status.timestamp && (Date.now() - status.timestamp) < 10000; // 10 second threshold
        connectionEl.textContent = isConnected ? '🟢' : '🔴';
        connectionEl.title = isConnected ? 'Cognitive connection active' : 'Cognitive connection lost';
    }
}

/**
 * Get Cognitive Health Class
 * 
 * Why: Provides visual feedback for cognitive health levels
 * Where: Used by status update functions for metric styling
 * How: Returns CSS class based on percentage thresholds
 */
function getCognitiveHealthClass(percent) {
    if (percent >= 70) return 'health-good';
    if (percent >= 40) return 'health-medium';
    return 'health-low';
}

/**
 * Toggle Status Overlay Visibility
 * 
 * Why: Allows users to show/hide cognitive status for unobstructed view
 * Where: Can be called by keyboard shortcuts or UI controls
 * How: Toggles display property of status overlay element
 */
function toggleCognitiveStatus() {
    const statusOverlay = document.getElementById('cognitive-status');
    if (statusOverlay) {
        const isVisible = statusOverlay.style.display !== 'none';
        statusOverlay.style.display = isVisible ? 'none' : 'block';
        console.log('🧠 Cognitive status overlay:', isVisible ? 'hidden' : 'shown');
    }
}

// Expose functions globally
window.createCognitiveStatusOverlay = createCognitiveStatusOverlay;
window.toggleCognitiveStatus = toggleCognitiveStatus;

console.log('🧠 Cognitive Status component loaded and ready');