/**
 * Clever's Enhanced Conversation Interface - Real-time magical interaction system
 * Brings Clever's authentic personality to life through UI reactions and conversation flow
 */

class CleverConversationInterface {
    constructor() {
        this.isInitialized = false;
        this.conversationHistory = [];
        this.cleverState = {
            mood: 'curious',
            energy: 0.7,
            processing: false,
            last_response_time: null,
            excitement: 0.5,
            creativity: 0.7
        };
        
        // Connect with existing particle systems
        this.particleSystem = this.detectParticleSystem();
        
        this.init();
    }
    
    detectParticleSystem() {
        // Check for existing particle systems in priority order
        if (window.nanobotSwarm) {
            console.log('🌟 Connected to nanobot swarm for Clever reactions');
            return window.nanobotSwarm;
        }
        
        if (window.scene && window.scene.particles) {
            console.log('🌟 Connected to scene.js particle system');
            return window.scene;
        }
        
        if (window.particleField) {
            console.log('🌟 Connected to particle field system');
            return window.particleField;
        }
        
        console.log('💫 No particle system detected - using standalone reactions');
        return null;
    }
    
    init() {
        if (this.isInitialized) return;
        
        this.setupConversationInterface();
        this.setupEventListeners();
        this.startConversationFlow();
        
        this.isInitialized = true;
        console.log('🎭 Clever enhanced conversation interface initialized - ready for magical interactions!');
    }
    
    setupConversationInterface() {
        // Enhance existing chat interface or create comprehensive new one
        const existingChat = document.getElementById('chat-messages');
        
        if (existingChat) {
            this.enhanceExistingChat(existingChat);
        } else {
            this.createFullChatInterface();
        }
        
        // Add Clever's personality dashboard
        this.addPersonalityDashboard();
        this.addChatStyles();
    }
    
    enhanceExistingChat(chatElement) {
        // Enhance existing chat with Clever's personality features
        chatElement.classList.add('clever-enhanced-chat');
        
        // Add Clever status header if not present
        if (!document.getElementById('clever-status-header')) {
            const statusHeader = document.createElement('div');
            statusHeader.id = 'clever-status-header';
            statusHeader.className = 'clever-status-header';
            statusHeader.innerHTML = `
                <div class="clever-avatar">🧠</div>
                <div class="clever-info">
                    <div class="clever-name">Clever</div>
                    <div class="clever-status" id="clever-status">Ready to think together</div>
                </div>
                <div class="clever-energy-indicator" id="clever-energy-indicator"></div>
            `;
            
            chatElement.parentNode.insertBefore(statusHeader, chatElement);
        }
    }
    
    createFullChatInterface() {
        const chatPanel = document.createElement('div');
        chatPanel.id = 'clever-chat-panel';
        chatPanel.className = 'clever-chat-panel';
        chatPanel.innerHTML = `
            <div class="clever-header">
                <div class="clever-avatar">🧠</div>
                <div class="clever-info">
                    <div class="clever-name">Clever</div>
                    <div class="clever-status" id="clever-status">Ready for magical thinking</div>
                </div>
                <div class="clever-mood-indicator" id="clever-mood-indicator">
                    <span class="mood-emoji">🤔</span>
                    <span class="mood-text">Curious</span>
                </div>
            </div>
            <div class="chat-messages" id="chat-messages"></div>
            <div class="chat-input-container" id="chat-input-container">
                <input type="text" id="user-input" placeholder="Hey Clever, what's sparking your curiosity?" />
                <button id="send-button">
                    <span class="button-text">Send</span>
                    <span class="button-icon">🚀</span>
                </button>
            </div>
        `;
        
        // Position elegantly on the page
        chatPanel.style.cssText = `
            position: fixed;
            right: 20px;
            top: 20px;
            width: 450px;
            height: 650px;
            z-index: 1000;
        `;
        
        document.body.appendChild(chatPanel);
    }
    
    addPersonalityDashboard() {
        if (document.getElementById('clever-personality-dashboard')) return;
        
        const dashboard = document.createElement('div');
        dashboard.id = 'clever-personality-dashboard';
        dashboard.className = 'personality-dashboard';
        dashboard.innerHTML = `
            <div class="dashboard-header">
                <span class="dashboard-title">Clever's Mind</span>
                <span class="dashboard-toggle" onclick="this.parentNode.parentNode.classList.toggle('collapsed')">−</span>
            </div>
            <div class="dashboard-content">
                <div class="personality-state">
                    <div class="state-item">
                        <span class="state-label">Mood:</span>
                        <span class="state-value" id="mood-display">Curious</span>
                    </div>
                    <div class="state-item">
                        <span class="state-label">Energy:</span>
                        <div class="energy-bar">
                            <div class="energy-fill" id="energy-fill" style="width: 70%"></div>
                        </div>
                    </div>
                    <div class="state-item">
                        <span class="state-label">Focus:</span>
                        <div class="focus-indicator" id="focus-indicator">
                            <div class="focus-ring"></div>
                        </div>
                    </div>
                </div>
                <div class="insights-section">
                    <div class="insights-header">Live Insights</div>
                    <div class="insights-list" id="insights-list">
                        <div class="insight-item">🧠 Ready for deep thinking...</div>
                    </div>
                </div>
                <div class="conversation-patterns">
                    <div class="patterns-header">Conversation Flow</div>
                    <div class="patterns-display" id="patterns-display">
                        Fresh conversation beginning
                    </div>
                </div>
            </div>
        `;
        
        // Position the dashboard
        dashboard.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            width: 280px;
            max-height: 400px;
            z-index: 999;
        `;
        
        document.body.appendChild(dashboard);
    }
    
    addChatStyles() {
        if (document.getElementById('clever-enhanced-chat-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'clever-enhanced-chat-styles';
        styles.textContent = `
            .clever-chat-panel {
                background: rgba(0, 20, 40, 0.95);
                border: 2px solid #00ffff;
                border-radius: 20px;
                backdrop-filter: blur(20px);
                box-shadow: 0 0 40px rgba(0, 255, 255, 0.4);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                font-family: 'SF Pro Display', -apple-system, system-ui, sans-serif;
            }
            
            .clever-header {
                display: flex;
                align-items: center;
                padding: 20px;
                background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 150, 0.1));
                border-bottom: 1px solid rgba(0, 255, 255, 0.3);
            }
            
            .clever-avatar {
                font-size: 28px;
                margin-right: 15px;
                animation: cleverpulse 3s infinite;
                filter: drop-shadow(0 0 10px #00ffff);
            }
            
            .clever-info {
                flex: 1;
                margin-right: 15px;
            }
            
            .clever-name {
                font-weight: 700;
                color: #00ffff;
                font-size: 20px;
                margin-bottom: 2px;
            }
            
            .clever-status {
                font-size: 13px;
                color: #ffffff;
                opacity: 0.8;
            }
            
            .clever-mood-indicator {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                min-width: 60px;
            }
            
            .mood-emoji {
                font-size: 20px;
                margin-bottom: 4px;
            }
            
            .mood-text {
                font-size: 11px;
                color: #00ffff;
                font-weight: 500;
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
                scroll-behavior: smooth;
            }
            
            .message {
                padding: 15px;
                border-radius: 18px;
                max-width: 85%;
                word-wrap: break-word;
                line-height: 1.4;
                animation: messageAppear 0.4s ease-out;
                position: relative;
            }
            
            .user-message {
                background: linear-gradient(135deg, rgba(255, 0, 150, 0.25), rgba(255, 0, 100, 0.15));
                border: 1px solid rgba(255, 0, 150, 0.4);
                color: #ffffff;
                align-self: flex-end;
                margin-left: auto;
                border-bottom-right-radius: 6px;
            }
            
            .clever-message {
                background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 200, 255, 0.1));
                border: 1px solid rgba(0, 255, 255, 0.3);
                color: #ffffff;
                align-self: flex-start;
                border-bottom-left-radius: 6px;
                padding-left: 20px;
            }
            
            .clever-message::before {
                content: "🧠";
                position: absolute;
                left: -8px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 18px;
                background: rgba(0, 20, 40, 0.9);
                padding: 4px;
                border-radius: 50%;
                border: 1px solid #00ffff;
            }
            
            .clever-excited {
                animation: excitedGlow 2s ease-in-out infinite alternate;
                border-color: #ff00ff !important;
            }
            
            .clever-thinking {
                color: #00ffff;
                font-style: italic;
                opacity: 0.9;
            }
            
            .clever-slang {
                color: #ff00ff;
                font-weight: bold;
                text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
            }
            
            .chat-input-container {
                padding: 20px;
                border-top: 1px solid rgba(0, 255, 255, 0.3);
                display: flex;
                gap: 12px;
                background: rgba(0, 255, 255, 0.05);
            }
            
            #user-input {
                flex: 1;
                background: rgba(0, 0, 0, 0.4);
                border: 2px solid rgba(0, 255, 255, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                color: #ffffff;
                font-family: inherit;
                font-size: 14px;
                transition: all 0.3s ease;
            }
            
            #user-input:focus {
                outline: none;
                border-color: #00ffff;
                box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
                background: rgba(0, 0, 0, 0.6);
            }
            
            #send-button {
                background: linear-gradient(135deg, #00ffff, #ff00ff);
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                color: #000;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
                min-width: 80px;
                justify-content: center;
            }
            
            #send-button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
            }
            
            #send-button:active {
                transform: scale(0.98);
            }
            
            .personality-dashboard {
                background: rgba(0, 20, 40, 0.92);
                border: 2px solid #00ffff;
                border-radius: 15px;
                backdrop-filter: blur(15px);
                box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
                overflow: hidden;
                transition: all 0.3s ease;
                font-family: 'SF Pro Display', -apple-system, system-ui, sans-serif;
            }
            
            .personality-dashboard.collapsed .dashboard-content {
                display: none;
            }
            
            .dashboard-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 18px;
                background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 150, 0.1));
                border-bottom: 1px solid rgba(0, 255, 255, 0.3);
            }
            
            .dashboard-title {
                font-weight: 600;
                color: #00ffff;
                font-size: 16px;
            }
            
            .dashboard-toggle {
                color: #ffffff;
                cursor: pointer;
                font-size: 18px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
                transition: background 0.2s ease;
            }
            
            .dashboard-toggle:hover {
                background: rgba(0, 255, 255, 0.2);
            }
            
            .dashboard-content {
                padding: 18px;
            }
            
            .personality-state {
                margin-bottom: 18px;
            }
            
            .state-item {
                display: flex;
                align-items: center;
                margin-bottom: 12px;
                font-size: 13px;
            }
            
            .state-label {
                color: #ffffff;
                font-weight: 500;
                min-width: 50px;
                margin-right: 10px;
            }
            
            .state-value {
                color: #00ffff;
                font-weight: 600;
            }
            
            .energy-bar {
                flex: 1;
                height: 8px;
                background: rgba(0, 0, 0, 0.4);
                border-radius: 4px;
                overflow: hidden;
                margin-left: 10px;
            }
            
            .energy-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ffff, #ff00ff);
                border-radius: 4px;
                transition: width 0.5s ease;
                position: relative;
            }
            
            .energy-fill::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                animation: energyShimmer 2s infinite;
            }
            
            .focus-indicator {
                width: 24px;
                height: 24px;
                margin-left: 10px;
                position: relative;
            }
            
            .focus-ring {
                width: 100%;
                height: 100%;
                border: 2px solid #00ffff;
                border-radius: 50%;
                border-top-color: transparent;
                animation: focusSpin 3s linear infinite;
            }
            
            .insights-section, .conversation-patterns {
                margin-bottom: 15px;
            }
            
            .insights-header, .patterns-header {
                font-size: 12px;
                font-weight: 600;
                color: #00ffff;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .insights-list {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            
            .insight-item {
                font-size: 11px;
                color: #ffffff;
                opacity: 0.8;
                padding: 6px 0;
                border-left: 2px solid rgba(0, 255, 255, 0.3);
                padding-left: 8px;
                animation: insightFade 0.5s ease-in;
            }
            
            .patterns-display {
                font-size: 11px;
                color: #ffffff;
                opacity: 0.7;
                font-style: italic;
            }
            
            @keyframes cleverpulse {
                0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px #00ffff); }
                50% { transform: scale(1.1); filter: drop-shadow(0 0 20px #00ffff); }
            }
            
            @keyframes messageAppear {
                0% {
                    opacity: 0;
                    transform: translateY(15px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes excitedGlow {
                0% { box-shadow: 0 0 10px rgba(255, 0, 255, 0.4); }
                100% { box-shadow: 0 0 25px rgba(255, 0, 255, 0.8); }
            }
            
            @keyframes energyShimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            
            @keyframes focusSpin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes insightFade {
                0% { opacity: 0; transform: translateX(-10px); }
                100% { opacity: 0.8; transform: translateX(0); }
            }
            
            .clever-processing {
                position: relative;
            }
            
            .clever-processing::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
                animation: processingShimmer 1.5s infinite;
                border-radius: inherit;
            }
            
            @keyframes processingShimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
        `;
        
        document.head.appendChild(styles);
    }
    
    setupEventListeners() {
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        
        if (userInput && sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
            
            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            // Enhanced input feedback
            userInput.addEventListener('input', () => {
                this.handleInputFeedback();
            });
        }
    }
    
    handleInputFeedback() {
        // Provide real-time feedback as user types
        const userInput = document.getElementById('user-input');
        const message = userInput.value.trim();
        
        if (message.length > 3) {
            this.triggerTypingReaction();
        }
    }
    
    triggerTypingReaction() {
        // Subtle particle reaction while user is typing
        if (this.particleSystem && this.particleSystem.addEnergy) {
            this.particleSystem.addEnergy(0.3);
        }
        
        // Update Clever's status
        this.updateCleverStatus("Listening...", "anticipating");
    }
    
    async sendMessage() {
        const userInput = document.getElementById('user-input');
        const message = userInput.value.trim();
        
        if (!message) return;
        
        // Clear input and show user message
        userInput.value = '';
        this.addMessageToChat(message, 'user');
        
        // Update Clever's state to processing
        this.updateCleverState({ 
            processing: true, 
            mood: 'thinking',
            status: "Processing your thoughts..."
        });
        this.triggerProcessingReaction();
        
        try {
            // Send to Clever's enhanced backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Update Clever's complete state
                this.updateCleverState({
                    processing: false,
                    mood: data.mood || 'engaged',
                    energy: data.energy || 0.7,
                    excitement: data.excitement || 0.5,
                    creativity: data.creativity || 0.7,
                    last_response_time: new Date().toISOString(),
                    status: "Ready for the next thought"
                });
                
                // Add Clever's response with full personality
                this.addCleverResponse(data.response, data);
                
                // Trigger magical particle reactions
                this.triggerResponseReaction(data);
                
                // Update personality dashboard
                this.updatePersonalityDashboard(data);
                
                // Update insights and patterns
                this.updateInsights(data.insights || []);
                this.updateConversationPatterns(data.conversation_context || {});
                
            } else {
                throw new Error('Failed to get response from Clever');
            }
            
        } catch (error) {
            console.error('Conversation error:', error);
            this.updateCleverState({ 
                processing: false, 
                mood: 'apologetic',
                status: "Experiencing a small glitch"
            });
            this.addCleverResponse(
                "Hey Jay, I hit a small glitch there but I'm still here! Mind trying that again? My neural pathways are still learning. 🧠✨", 
                { error: true, mood: 'apologetic' }
            );
        }
    }
    
    addMessageToChat(message, sender) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        messageElement.textContent = message;
        
        // Add timestamp for reference
        const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        messageElement.setAttribute('data-timestamp', timestamp);
        
        chatMessages.appendChild(messageElement);
        this.scrollToBottom(chatMessages);
        
        // Store in conversation history
        this.conversationHistory.push({
            timestamp: new Date().toISOString(),
            sender: sender,
            message: message
        });
    }
    
    addCleverResponse(response, responseData) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'message clever-message';
        
        // Add excitement styling based on Clever's state
        if (responseData.mood === 'excited' || responseData.excitement > 0.7) {
            messageElement.classList.add('clever-excited');
        }
        
        if (responseData.processing) {
            messageElement.classList.add('clever-processing');
        }
        
        // Parse and format Clever's response with personality
        messageElement.innerHTML = this.formatCleverResponse(response);
        
        chatMessages.appendChild(messageElement);
        this.scrollToBottom(chatMessages);
        
        // Store in conversation history with data
        this.conversationHistory.push({
            timestamp: new Date().toISOString(),
            sender: 'clever',
            message: response,
            data: responseData
        });
    }
    
    formatCleverResponse(response) {
        let formatted = response;
        
        // Format emotional expressions with styling
        formatted = formatted.replace(/\*(.*?)\*/g, '<em class="clever-thinking">$1</em>');
        
        // Style emojis with enhanced display
        formatted = formatted.replace(/(🧠|✨|🔥|💙|🚀|💫|🎯|⚡|🌟)/g, '<span style="font-size: 1.2em; filter: drop-shadow(0 0 3px currentColor);">$1</span>');
        
        // Style Jay-specific slang with Clever's personality
        const slangWords = ['no cap', 'fire', 'lowkey', 'bet', 'YOOO', 'LETS GOOO', 'fr', 'that hits different'];
        slangWords.forEach(slang => {
            const regex = new RegExp(`\\b${slang}\\b`, 'gi');
            formatted = formatted.replace(regex, `<span class="clever-slang">${slang}</span>`);
        });
        
        // Style technical terms
        const techTerms = ['AI', 'algorithm', 'neural', 'system', 'code', 'data'];
        techTerms.forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            formatted = formatted.replace(regex, `<span style="color: #00ffff; font-weight: 500;">${term}</span>`);
        });
        
        return formatted;
    }
    
    updateCleverState(newState) {
        this.cleverState = { ...this.cleverState, ...newState };
        
        // Update status display
        this.updateCleverStatus(newState.status, newState.mood);
        
        // Update mood indicator
        this.updateMoodIndicator(newState.mood);
    }
    
    updateCleverStatus(status, mood) {
        const statusElement = document.getElementById('clever-status');
        if (statusElement && status) {
            statusElement.textContent = status;
            
            // Color coding based on mood
            if (this.cleverState.processing) {
                statusElement.style.color = '#ffff00';
            } else if (mood === 'excited') {
                statusElement.style.color = '#ff00ff';
            } else if (mood === 'supportive') {
                statusElement.style.color = '#00ff80';
            } else {
                statusElement.style.color = '#00ffff';
            }
        }
    }
    
    updateMoodIndicator(mood) {
        const moodEmoji = document.querySelector('.mood-emoji');
        const moodText = document.querySelector('.mood-text');
        
        if (moodEmoji && moodText) {
            const moodMap = {
                'curious': { emoji: '🤔', text: 'Curious' },
                'excited': { emoji: '🤩', text: 'Excited' },
                'supportive': { emoji: '💙', text: 'Supportive' },
                'creative': { emoji: '🎨', text: 'Creative' },
                'analytical': { emoji: '🧠', text: 'Analytical' },
                'thinking': { emoji: '💭', text: 'Thinking' },
                'apologetic': { emoji: '😅', text: 'Apologetic' }
            };
            
            const moodData = moodMap[mood] || moodMap['curious'];
            moodEmoji.textContent = moodData.emoji;
            moodText.textContent = moodData.text;
        }
    }
    
    updatePersonalityDashboard(responseData) {
        // Update energy display
        const energyFill = document.getElementById('energy-fill');
        if (energyFill && responseData.energy !== undefined) {
            const energyPercent = responseData.energy * 100;
            energyFill.style.width = `${energyPercent}%`;
            
            // Dynamic energy bar coloring
            if (energyPercent > 80) {
                energyFill.style.background = 'linear-gradient(90deg, #ff00ff, #ffff00)';
            } else if (energyPercent > 60) {
                energyFill.style.background = 'linear-gradient(90deg, #00ffff, #ff00ff)';
            } else {
                energyFill.style.background = 'linear-gradient(90deg, #00ffff, #ffffff)';
            }
        }
        
        // Update mood display
        const moodDisplay = document.getElementById('mood-display');
        if (moodDisplay && responseData.mood) {
            moodDisplay.textContent = responseData.mood.charAt(0).toUpperCase() + responseData.mood.slice(1);
        }
        
        // Update focus indicator based on approach
        const focusIndicator = document.getElementById('focus-indicator');
        if (focusIndicator && responseData.approach) {
            const focusRing = focusIndicator.querySelector('.focus-ring');
            if (responseData.approach === 'strategic_deep_dive') {
                focusRing.style.borderColor = '#00ff00';
                focusRing.style.animationDuration = '1s';
            } else if (responseData.approach === 'creative_catalyst') {
                focusRing.style.borderColor = '#ff00ff';
                focusRing.style.animationDuration = '0.5s';
            } else {
                focusRing.style.borderColor = '#00ffff';
                focusRing.style.animationDuration = '3s';
            }
        }
    }
    
    updateInsights(insights) {
        const insightsList = document.getElementById('insights-list');
        if (!insightsList || !insights.length) return;
        
        // Clear old insights and add new ones
        insightsList.innerHTML = '';
        
        insights.slice(-3).forEach(insight => {
            const insightElement = document.createElement('div');
            insightElement.className = 'insight-item';
            insightElement.innerHTML = `💡 ${insight}`;
            insightsList.appendChild(insightElement);
        });
    }
    
    updateConversationPatterns(patterns) {
        const patternsDisplay = document.getElementById('patterns-display');
        if (!patternsDisplay || !patterns) return;
        
        let patternText = '';
        
        if (patterns.primary_interaction_mode) {
            patternText += `${patterns.primary_interaction_mode} mode`;
        }
        
        if (patterns.conversation_depth) {
            patternText += ` • ${patterns.conversation_depth} depth`;
        }
        
        if (patterns.energy_trajectory) {
            patternText += ` • ${patterns.energy_trajectory} energy`;
        }
        
        patternsDisplay.textContent = patternText || 'Analyzing conversation flow...';
    }
    
    triggerProcessingReaction() {
        if (!this.particleSystem) return;
        
        // Trigger thinking/processing particle reaction
        if (this.particleSystem.morphToShape) {
            this.particleSystem.morphToShape('thinking_spiral');
        } else if (this.particleSystem.setMode) {
            this.particleSystem.setMode('processing');
        } else if (this.particleSystem.particles) {
            // Generic processing animation
            this.particleSystem.particles.forEach(p => {
                if (p.color) p.color = '#ffff00'; // Yellow for thinking
            });
        }
    }
    
    triggerResponseReaction(responseData) {
        if (!this.particleSystem) return;
        
        const approach = responseData.approach || 'curious_collaborator';
        const intensity = responseData.particle_intensity || 0.6;
        const uiReactions = responseData.ui_reactions || {};
        
        // Trigger specific reactions based on Clever's response approach
        switch (approach) {
            case 'creative_catalyst':
                this.triggerCreativeReaction(uiReactions, intensity);
                break;
            case 'celebration_amplifier':
                this.triggerCelebrationReaction(uiReactions, intensity);
                break;
            case 'strategic_deep_dive':
                this.triggerAnalyticalReaction(uiReactions, intensity);
                break;
            case 'supportive_genius':
                this.triggerSupportiveReaction(uiReactions, intensity);
                break;
            case 'witty_quick_hit':
                this.triggerQuickReaction(uiReactions, intensity);
                break;
            default:
                this.triggerCuriousReaction(uiReactions, intensity);
        }
    }
    
    triggerCreativeReaction(reactions, intensity) {
        if (this.particleSystem.explodeFromCenter) {
            this.particleSystem.explodeFromCenter();
        } else if (this.particleSystem.morphToShape) {
            this.particleSystem.morphToShape('creative_burst');
        } else if (this.particleSystem.addEnergy) {
            this.particleSystem.addEnergy(intensity * 1.5);
        }
    }
    
    triggerCelebrationReaction(reactions, intensity) {
        if (this.particleSystem.celebrationBurst) {
            this.particleSystem.celebrationBurst();
        } else if (this.particleSystem.explodeFromCenter) {
            this.particleSystem.explodeFromCenter();
            setTimeout(() => this.particleSystem.explodeFromCenter(), 200);
        }
    }
    
    triggerAnalyticalReaction(reactions, intensity) {
        if (this.particleSystem.morphToShape) {
            this.particleSystem.morphToShape('grid_pattern');
        } else if (this.particleSystem.setMode) {
            this.particleSystem.setMode('analytical');
        }
    }
    
    triggerSupportiveReaction(reactions, intensity) {
        if (this.particleSystem.gentleWave) {
            this.particleSystem.gentleWave();
        } else if (this.particleSystem.addEnergy) {
            this.particleSystem.addEnergy(intensity * 0.8);
        }
    }
    
    triggerQuickReaction(reactions, intensity) {
        if (this.particleSystem.quickFlash) {
            this.particleSystem.quickFlash();
        } else if (this.particleSystem.addEnergy) {
            this.particleSystem.addEnergy(intensity * 1.2);
        }
    }
    
    triggerCuriousReaction(reactions, intensity) {
        if (this.particleSystem.addEnergy) {
            this.particleSystem.addEnergy(intensity);
        }
    }
    
    scrollToBottom(container) {
        container.scrollTop = container.scrollHeight;
    }
    
    startConversationFlow() {
        // Show Clever's dynamic greeting
        setTimeout(() => {
            this.showCleverGreeting();
        }, 1500);
        
        // Periodic state updates
        setInterval(() => {
            this.updatePersonalityDisplay();
        }, 8000);
    }
    
    async showCleverGreeting() {
        try {
            // Get Clever's dynamic greeting from enhanced backend
            const response = await fetch('/api/clever-greeting');
            const data = await response.json();
            
            // Show greeting with full personality
            this.addCleverResponse(data.greeting || "Hey Jay! 🌟 Ready for some magical thinking together?", {
                mood: data.mood || 'curious',
                energy: data.energy || 0.7,
                approach: 'curious_collaborator'
            });
            
            // Update personality dashboard
            this.updatePersonalityDashboard(data);
            
            // Trigger welcoming particle reaction
            this.triggerCuriousReaction({}, 0.6);
            
        } catch (error) {
            console.log('Using default greeting - backend not ready yet');
            this.addCleverResponse("Hey Jay! 🌟 Ready for some magical thinking together?", {
                mood: 'curious',
                energy: 0.7
            });
        }
    }
    
    async updatePersonalityDisplay() {
        try {
            const response = await fetch('/api/clever-state');
            const data = await response.json();
            
            if (data.clever_state) {
                this.updatePersonalityDashboard(data);
            }
        } catch (error) {
            // Silently handle - not critical for core functionality
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure other systems are loaded
    setTimeout(() => {
        const conversationInterface = new CleverConversationInterface();
        
        // Make globally available for debugging and integration
        window.cleverConversation = conversationInterface;
        
        console.log('🎭 Clever enhanced conversation interface ready for magical interactions!');
    }, 500);
});

// Export for module use if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CleverConversationInterface;
}
