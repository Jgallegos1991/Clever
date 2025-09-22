/*
Clever Holographic UI Components - Specific Component Classes

Why: Implements the specific holographic UI elements seen in Jay's screenshots -
     floating panels, analysis displays, chat bubbles, and status indicators
Where: Used by CleverUIFoundation to create modular, reusable UI components
How: Each component class handles its own styling, behavior, and lifecycle
*/

// Floating Panel Component (for analysis displays, status panels, etc.)
class FloatingPanel extends UIComponent {
    get defaultOptions() {
        return {
            ...super.defaultOptions,
            width: 300,
            height: 'auto',
            position: { x: 'auto', y: 'auto' },
            title: '',
            content: '',
            style: 'holographic', // holographic, minimal, analysis
            layer: 'analysis'
        };
    }

    setupElement() {
        const { width, height, title, content, style } = this.options;
        
        this.element.style.cssText = `
            position: absolute;
            width: ${typeof width === 'number' ? width + 'px' : width};
            height: ${typeof height === 'number' ? height + 'px' : height};
            background: rgba(11, 15, 20, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(105, 234, 203, 0.3);
            border-radius: 12px;
            box-shadow: 
                0 0 0 1px rgba(105, 234, 203, 0.2),
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 16px;
            color: #e9f1fb;
            font-family: Inter, system-ui;
            font-size: 13px;
            pointer-events: auto;
            contain: layout style paint;
        `;

        if (style === 'holographic') {
            this.element.style.background = 'rgba(11, 15, 20, 0.75)';
            this.element.style.border = '1px solid rgba(105, 234, 203, 0.4)';
            this.element.style.boxShadow += ', 0 0 20px rgba(105, 234, 203, 0.15)';
        }

        // Add title if provided
        if (title) {
            const titleEl = document.createElement('div');
            titleEl.style.cssText = `
                font-weight: 600;
                font-size: 12px;
                color: #69EACB;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            `;
            titleEl.textContent = title;
            this.element.appendChild(titleEl);
        }

        // Add content container
        this.contentEl = document.createElement('div');
        this.contentEl.style.cssText = `
            line-height: 1.4;
            color: #d9e7ef;
        `;
        this.contentEl.innerHTML = content;
        this.element.appendChild(this.contentEl);

        this.positionPanel();
    }

    positionPanel() {
        const { position } = this.options;
        
        if (position.x === 'auto' && position.y === 'auto') {
            // Smart positioning to avoid particle dense areas
            const viewport = {
                width: window.innerWidth,
                height: window.innerHeight
            };
            
            // Position in corners or edges, avoiding center where particles are
            const positions = [
                { top: '20px', left: '20px' },
                { top: '20px', right: '20px' },
                { bottom: '80px', left: '20px' },
                { bottom: '80px', right: '20px' },
                { top: '50%', left: '20px', transform: 'translateY(-50%)' },
                { top: '50%', right: '20px', transform: 'translateY(-50%)' }
            ];
            
            const pos = positions[Math.floor(Math.random() * positions.length)];
            Object.assign(this.element.style, pos);
        } else {
            if (typeof position.x === 'number') {
                this.element.style.left = position.x + 'px';
            } else if (position.x) {
                this.element.style.left = position.x;
            }
            
            if (typeof position.y === 'number') {
                this.element.style.top = position.y + 'px';
            } else if (position.y) {
                this.element.style.top = position.y;
            }
        }
    }

    updateContent(content) {
        this.contentEl.innerHTML = content;
        this.lastActivity = Date.now();
    }

    setStatus(status, color = '#69EACB') {
        const statusEl = this.element.querySelector('.status-indicator') || 
                        document.createElement('div');
        
        if (!statusEl.parentNode) {
            statusEl.className = 'status-indicator';
            statusEl.style.cssText = `
                position: absolute;
                top: -6px;
                right: -6px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: 2px solid rgba(0, 0, 0, 0.8);
                transition: background-color 0.3s ease;
            `;
            this.element.appendChild(statusEl);
        }
        
        statusEl.style.backgroundColor = color;
        statusEl.title = status;
    }
}

// Analysis Display Component (shows Clever's cognitive process)
class AnalysisDisplay extends FloatingPanel {
    get defaultOptions() {
        return {
            ...super.defaultOptions,
            title: 'Cognitive Analysis',
            width: 280,
            style: 'analysis',
            position: { x: 'auto', y: 'auto' }
        };
    }

    setupElement() {
        super.setupElement();
        
        this.analysisData = {
            intent: 'Analyzing...',
            mood: 'neutral',
            keywords: [],
            formation: 'whirlpool'
        };
        
        this.renderAnalysis();
    }

    renderAnalysis() {
        const { intent, mood, keywords, formation } = this.analysisData;
        
        const content = `
            <div style="margin-bottom: 8px;">
                <span style="color: #69EACB; font-weight: 500;">Intent:</span>
                <span style="margin-left: 8px; color: #d9e7ef;">${intent}</span>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="color: #69EACB; font-weight: 500;">Mood:</span>
                <span style="margin-left: 8px; color: #d9e7ef;">${mood}</span>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="color: #69EACB; font-weight: 500;">Formation:</span>
                <span style="margin-left: 8px; color: #d9e7ef;">${formation}</span>
            </div>
            ${keywords.length > 0 ? `
                <div style="margin-top: 12px;">
                    <span style="color: #69EACB; font-weight: 500; display: block; margin-bottom: 4px;">Keywords:</span>
                    <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                        ${keywords.map(keyword => 
                            `<span style="background: rgba(105, 234, 203, 0.2); 
                                          color: #69EACB; 
                                          padding: 2px 6px; 
                                          border-radius: 4px; 
                                          font-size: 11px;">${keyword}</span>`
                        ).join('')}
                    </div>
                </div>
            ` : ''}
        `;
        
        this.updateContent(content);
    }

    updateAnalysis(data) {
        Object.assign(this.analysisData, data);
        this.renderAnalysis();
    }
}

// Chat Bubble Component (floating chat messages)
class ChatBubble extends UIComponent {
    get defaultOptions() {
        return {
            ...super.defaultOptions,
            message: '',
            role: 'ai', // ai, user
            autoHide: true,
            hideDelay: 8000,
            layer: 'chat'
        };
    }

    setupElement() {
        const { message, role, autoHide, hideDelay } = this.options;
        
        const isUser = role === 'user';
        
        this.element.style.cssText = `
            position: absolute;
            max-width: 480px;
            background: ${isUser ? 'rgba(18, 40, 48, 0.85)' : 'rgba(11, 15, 20, 0.85)'};
            backdrop-filter: blur(12px);
            border: 1px solid rgba(105, 234, 203, 0.25);
            border-radius: 16px;
            padding: 12px 16px;
            color: #d9e7ef;
            font-family: Inter, system-ui;
            font-size: 14px;
            line-height: 1.4;
            box-shadow: 
                0 0 0 1px rgba(105, 234, 203, 0.15),
                0 8px 24px rgba(0, 0, 0, 0.3);
            pointer-events: auto;
            contain: layout style paint;
        `;

        this.element.textContent = message;
        this.positionBubble();

        if (autoHide) {
            this.hideTimer = setTimeout(() => {
                this.hide();
            }, hideDelay);
        }
    }

    positionBubble() {
        // Smart positioning to avoid overlapping and particle interference
        const bubbles = document.querySelectorAll('.chatbubble');
        const viewport = { width: window.innerWidth, height: window.innerHeight };
        
        // Position on sides, avoiding center particle area
        const side = Math.random() > 0.5 ? 'left' : 'right';
        const verticalOffset = 100 + (bubbles.length * 80);
        
        if (side === 'left') {
            this.element.style.left = '20px';
        } else {
            this.element.style.right = '20px';
        }
        
        this.element.style.top = Math.min(verticalOffset, viewport.height - 200) + 'px';
    }

    destroy() {
        if (this.hideTimer) {
            clearTimeout(this.hideTimer);
        }
        super.destroy();
    }
}

// Status Indicator Component (formation status, system status, etc.)
class StatusIndicator extends UIComponent {
    get defaultOptions() {
        return {
            ...super.defaultOptions,
            text: '',
            type: 'info', // info, success, warning, error, formation
            position: 'top-right',
            layer: 'status'
        };
    }

    setupElement() {
        const { text, type, position } = this.options;
        
        const colors = {
            info: '#69EACB',
            success: '#4AE54A',
            warning: '#FFB84D',
            error: '#FF6B6B',
            formation: '#FF6BFF'
        };

        this.element.style.cssText = `
            position: absolute;
            background: rgba(11, 15, 20, 0.9);
            backdrop-filter: blur(8px);
            border: 1px solid ${colors[type] || colors.info}40;
            border-radius: 20px;
            padding: 8px 16px;
            color: ${colors[type] || colors.info};
            font-family: Inter, system-ui;
            font-size: 12px;
            font-weight: 500;
            box-shadow: 
                0 0 0 1px ${colors[type] || colors.info}20,
                0 4px 16px rgba(0, 0, 0, 0.3);
            pointer-events: none;
            contain: layout style paint;
        `;

        // Add pulsing effect for formation status
        if (type === 'formation') {
            this.element.style.animation = 'pulse 2s infinite';
            
            // Add pulse keyframes if not already present
            if (!document.querySelector('#status-pulse-keyframes')) {
                const style = document.createElement('style');
                style.id = 'status-pulse-keyframes';
                style.textContent = `
                    @keyframes pulse {
                        0%, 100% { opacity: 1; transform: scale(1); }
                        50% { opacity: 0.7; transform: scale(1.05); }
                    }
                `;
                document.head.appendChild(style);
            }
        }

        this.element.textContent = text;
        this.positionIndicator(position);
    }

    positionIndicator(position) {
        const positions = {
            'top-left': { top: '20px', left: '20px' },
            'top-right': { top: '20px', right: '20px' },
            'top-center': { top: '20px', left: '50%', transform: 'translateX(-50%)' },
            'bottom-left': { bottom: '20px', left: '20px' },
            'bottom-right': { bottom: '20px', right: '20px' },
            'bottom-center': { bottom: '20px', left: '50%', transform: 'translateX(-50%)' }
        };

        const pos = positions[position] || positions['top-right'];
        Object.assign(this.element.style, pos);
    }

    updateText(text) {
        this.element.textContent = text;
        this.lastActivity = Date.now();
    }
}

// Export components
window.FloatingPanel = FloatingPanel;
window.AnalysisDisplay = AnalysisDisplay;
window.ChatBubble = ChatBubble;
window.StatusIndicator = StatusIndicator;