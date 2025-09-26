/**
 * NotebookLM-Inspired Document Analysis UI Component
 * 
 * Why: Provides intuitive interface for Clever's enhanced document analysis capabilities
 * Where: Integrated into Clever's holographic UI for seamless document interaction
 * How: Clean, modern interface with document querying, citation display, and collection overview
 * 
 * Connects to:
 *   - app.py: NotebookLM API endpoints for document analysis and querying
 *   - main.js: Integration with core Clever UI system
 *   - holographic-chamber.js: Particle effects for enhanced visual experience
 */

class NotebookLMInterface {
    constructor() {
        this.isVisible = false;
        this.currentQuery = '';
        this.queryInProgress = false;
        
        this.initializeInterface();
        this.bindEvents();
    }
    
    initializeInterface() {
        // Create the main interface container
        const interfaceHTML = `
            <div id="notebooklm-interface" class="notebooklm-hidden">
                <div class="notebooklm-container">
                    <div class="notebooklm-header">
                        <h2>🧠 Document Intelligence</h2>
                        <button class="notebooklm-close" aria-label="Close">×</button>
                    </div>
                    
                    <div class="notebooklm-content">
                        <!-- Query Section -->
                        <div class="notebooklm-query-section">
                            <div class="notebooklm-input-group">
                                <input 
                                    type="text" 
                                    id="notebooklm-query-input" 
                                    placeholder="Ask about your documents..."
                                    autocomplete="off"
                                >
                                <button id="notebooklm-query-btn" class="notebooklm-btn-primary">
                                    Query Documents
                                </button>
                            </div>
                            <div class="notebooklm-suggestions">
                                <span class="notebooklm-suggestion-label">Try asking:</span>
                                <button class="notebooklm-suggestion" data-query="What is digital sovereignty?">
                                    What is digital sovereignty?
                                </button>
                                <button class="notebooklm-suggestion" data-query="How does cognitive enhancement work?">
                                    How does cognitive enhancement work?
                                </button>
                                <button class="notebooklm-suggestion" data-query="Summarize the key research findings">
                                    Summarize the key research findings
                                </button>
                            </div>
                        </div>
                        
                        <!-- Results Section -->
                        <div id="notebooklm-results" class="notebooklm-results">
                            <div class="notebooklm-welcome">
                                <h3>📚 Your Knowledge Base</h3>
                                <p>Ask questions about your documents and I'll provide source-grounded answers with citations.</p>
                                
                                <div class="notebooklm-features">
                                    <div class="notebooklm-feature">
                                        <span class="notebooklm-icon">🔍</span>
                                        <span>Smart document search</span>
                                    </div>
                                    <div class="notebooklm-feature">
                                        <span class="notebooklm-icon">📖</span>
                                        <span>Source citations</span>
                                    </div>
                                    <div class="notebooklm-feature">
                                        <span class="notebooklm-icon">🔗</span>
                                        <span>Cross-document connections</span>
                                    </div>
                                    <div class="notebooklm-feature">
                                        <span class="notebooklm-icon">📊</span>
                                        <span>Collection overview</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Action Buttons -->
                        <div class="notebooklm-actions">
                            <button id="notebooklm-overview-btn" class="notebooklm-btn-secondary">
                                📊 Collection Overview
                            </button>
                            <button id="notebooklm-connections-btn" class="notebooklm-btn-secondary">
                                🔗 Document Connections
                            </button>
                            <button id="notebooklm-enhance-btn" class="notebooklm-btn-secondary">
                                ⚡ Enhance Analysis
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add to document
        document.body.insertAdjacentHTML('beforeend', interfaceHTML);
        
        // Add CSS styles
        this.addStyles();
    }
    
    addStyles() {
        const styles = `
            .notebooklm-hidden {
                display: none !important;
            }
            
            #notebooklm-interface {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(10px);
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .notebooklm-container {
                background: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(79, 70, 229, 0.3);
                border-radius: 16px;
                width: 90%;
                max-width: 800px;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
            }
            
            .notebooklm-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 24px;
                border-bottom: 1px solid rgba(79, 70, 229, 0.2);
                background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(147, 51, 234, 0.1));
            }
            
            .notebooklm-header h2 {
                margin: 0;
                color: #e2e8f0;
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            .notebooklm-close {
                background: none;
                border: none;
                color: #94a3b8;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.2s ease;
            }
            
            .notebooklm-close:hover {
                background: rgba(248, 113, 113, 0.1);
                color: #f87171;
            }
            
            .notebooklm-content {
                padding: 24px;
            }
            
            .notebooklm-query-section {
                margin-bottom: 24px;
            }
            
            .notebooklm-input-group {
                display: flex;
                gap: 12px;
                margin-bottom: 16px;
            }
            
            #notebooklm-query-input {
                flex: 1;
                padding: 12px 16px;
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(79, 70, 229, 0.3);
                border-radius: 8px;
                color: #e2e8f0;
                font-size: 1rem;
                transition: all 0.2s ease;
            }
            
            #notebooklm-query-input:focus {
                outline: none;
                border-color: #4f46e5;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }
            
            #notebooklm-query-input::placeholder {
                color: #64748b;
            }
            
            .notebooklm-btn-primary, .notebooklm-btn-secondary {
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 0.95rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                white-space: nowrap;
            }
            
            .notebooklm-btn-primary {
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
            }
            
            .notebooklm-btn-primary:hover {
                background: linear-gradient(135deg, #4338ca, #6d28d9);
                transform: translateY(-1px);
                box-shadow: 0 8px 15px rgba(79, 70, 229, 0.3);
            }
            
            .notebooklm-btn-secondary {
                background: rgba(79, 70, 229, 0.1);
                color: #a78bfa;
                border: 1px solid rgba(79, 70, 229, 0.3);
            }
            
            .notebooklm-btn-secondary:hover {
                background: rgba(79, 70, 229, 0.2);
                color: #c4b5fd;
            }
            
            .notebooklm-suggestions {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                align-items: center;
            }
            
            .notebooklm-suggestion-label {
                color: #64748b;
                font-size: 0.875rem;
                margin-right: 8px;
            }
            
            .notebooklm-suggestion {
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(79, 70, 229, 0.2);
                color: #94a3b8;
                padding: 6px 12px;
                border-radius: 16px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .notebooklm-suggestion:hover {
                background: rgba(79, 70, 229, 0.1);
                color: #c4b5fd;
                border-color: rgba(79, 70, 229, 0.4);
            }
            
            .notebooklm-results {
                min-height: 200px;
            }
            
            .notebooklm-welcome {
                text-align: center;
                color: #94a3b8;
            }
            
            .notebooklm-welcome h3 {
                margin: 0 0 12px 0;
                color: #e2e8f0;
            }
            
            .notebooklm-welcome p {
                margin: 0 0 24px 0;
                font-size: 1.05rem;
            }
            
            .notebooklm-features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
                margin-top: 24px;
            }
            
            .notebooklm-feature {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 12px;
                background: rgba(30, 41, 59, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(79, 70, 229, 0.1);
            }
            
            .notebooklm-icon {
                font-size: 1.2rem;
            }
            
            .notebooklm-actions {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                margin-top: 24px;
                padding-top: 20px;
                border-top: 1px solid rgba(79, 70, 229, 0.1);
            }
            
            .notebooklm-response {
                background: rgba(30, 41, 59, 0.3);
                border: 1px solid rgba(79, 70, 229, 0.2);
                border-radius: 12px;
                padding: 20px;
                margin: 16px 0;
            }
            
            .notebooklm-response-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
            }
            
            .notebooklm-response-text {
                color: #e2e8f0;
                line-height: 1.6;
                margin-bottom: 16px;
            }
            
            .notebooklm-citations {
                border-top: 1px solid rgba(79, 70, 229, 0.1);
                padding-top: 16px;
            }
            
            .notebooklm-citations h4 {
                margin: 0 0 12px 0;
                color: #a78bfa;
                font-size: 1rem;
            }
            
            .notebooklm-citation {
                background: rgba(15, 23, 42, 0.5);
                border: 1px solid rgba(79, 70, 229, 0.1);
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
            }
            
            .notebooklm-citation-file {
                font-weight: 500;
                color: #c4b5fd;
                margin-bottom: 6px;
            }
            
            .notebooklm-citation-excerpt {
                color: #94a3b8;
                font-size: 0.9rem;
                font-style: italic;
                line-height: 1.4;
            }
            
            .notebooklm-loading {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                padding: 40px 20px;
                color: #a78bfa;
            }
            
            .notebooklm-spinner {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(167, 139, 250, 0.2);
                border-top: 2px solid #a78bfa;
                border-radius: 50%;
                animation: notebooklm-spin 1s linear infinite;
            }
            
            @keyframes notebooklm-spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .notebooklm-error {
                background: rgba(248, 113, 113, 0.1);
                border: 1px solid rgba(248, 113, 113, 0.3);
                color: #fca5a5;
                padding: 16px;
                border-radius: 8px;
                margin: 16px 0;
            }
            
            /* Responsive design */
            @media (max-width: 640px) {
                .notebooklm-container {
                    width: 95%;
                    margin: 20px;
                }
                
                .notebooklm-input-group {
                    flex-direction: column;
                }
                
                .notebooklm-actions {
                    flex-direction: column;
                }
                
                .notebooklm-features {
                    grid-template-columns: 1fr;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    bindEvents() {
        const interface$ = document.getElementById('notebooklm-interface');
        const closeBtn = document.querySelector('.notebooklm-close');
        const queryInput = document.getElementById('notebooklm-query-input');
        const queryBtn = document.getElementById('notebooklm-query-btn');
        const suggestions = document.querySelectorAll('.notebooklm-suggestion');
        const overviewBtn = document.getElementById('notebooklm-overview-btn');
        const connectionsBtn = document.getElementById('notebooklm-connections-btn');
        const enhanceBtn = document.getElementById('notebooklm-enhance-btn');
        
        // Close interface
        closeBtn.addEventListener('click', () => this.hide());
        interface$.addEventListener('click', (e) => {
            if (e.target === interface$) this.hide();
        });
        
        // Query handling
        queryBtn.addEventListener('click', () => this.handleQuery());
        queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleQuery();
        });
        
        // Suggestion clicks
        suggestions.forEach(btn => {
            btn.addEventListener('click', () => {
                queryInput.value = btn.dataset.query;
                this.handleQuery();
            });
        });
        
        // Action buttons
        overviewBtn.addEventListener('click', () => this.showCollectionOverview());
        connectionsBtn.addEventListener('click', () => this.showDocumentConnections());
        enhanceBtn.addEventListener('click', () => this.enhanceAnalysis());
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isVisible) {
                this.hide();
            }
        });
    }
    
    show() {
        const interface$ = document.getElementById('notebooklm-interface');
        interface$.classList.remove('notebooklm-hidden');
        this.isVisible = true;
        
        // Focus on input
        setTimeout(() => {
            document.getElementById('notebooklm-query-input').focus();
        }, 100);
    }
    
    hide() {
        const interface$ = document.getElementById('notebooklm-interface');
        interface$.classList.add('notebooklm-hidden');
        this.isVisible = false;
    }
    
    async handleQuery() {
        const queryInput = document.getElementById('notebooklm-query-input');
        const query = queryInput.value.trim();
        
        if (!query || this.queryInProgress) return;
        
        this.currentQuery = query;
        this.queryInProgress = true;
        
        this.showLoading('Searching documents...');
        
        try {
            const response = await fetch('/api/query_documents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query, max_sources: 5 })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayQueryResponse(data.response, query);
            } else {
                this.showError(`Query failed: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        } finally {
            this.queryInProgress = false;
        }
    }
    
    displayQueryResponse(response, query) {
        const resultsDiv = document.getElementById('notebooklm-results');
        
        const responseHTML = `
            <div class="notebooklm-response">
                <div class="notebooklm-response-header">
                    <h4>💡 Response to: "${query}"</h4>
                    <small>Confidence: ${(response.confidence * 100).toFixed(0)}% | Quality: ${response.synthesis_quality}</small>
                </div>
                
                <div class="notebooklm-response-text">
                    ${response.text.replace(/\n/g, '<br>')}
                </div>
                
                ${response.citations.length > 0 ? `
                    <div class="notebooklm-citations">
                        <h4>📚 Sources (${response.citations.length})</h4>
                        ${response.citations.map((citation, i) => `
                            <div class="notebooklm-citation">
                                <div class="notebooklm-citation-file">
                                    ${i + 1}. ${citation.filename} 
                                    <small>(${(citation.confidence * 100).toFixed(0)}% match)</small>
                                </div>
                                <div class="notebooklm-citation-excerpt">
                                    "${citation.excerpt}"
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
        
        resultsDiv.innerHTML = responseHTML;
    }
    
    async showCollectionOverview() {
        this.showLoading('Analyzing document collection...');
        
        try {
            const response = await fetch('/api/collection_overview');
            const data = await response.json();
            
            if (data.success) {
                this.displayCollectionOverview(data.overview);
            } else {
                this.showError(`Failed to load overview: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        }
    }
    
    displayCollectionOverview(overview) {
        const resultsDiv = document.getElementById('notebooklm-results');
        
        const overviewHTML = `
            <div class="notebooklm-response">
                <div class="notebooklm-response-header">
                    <h4>📊 Collection Overview</h4>
                </div>
                
                <div class="notebooklm-response-text">
                    <div class="notebooklm-features">
                        <div class="notebooklm-feature">
                            <span class="notebooklm-icon">📄</span>
                            <span>${overview.total_documents} Documents</span>
                        </div>
                        <div class="notebooklm-feature">
                            <span class="notebooklm-icon">📝</span>
                            <span>${overview.total_words.toLocaleString()} Words</span>
                        </div>
                        <div class="notebooklm-feature">
                            <span class="notebooklm-icon">⏱️</span>
                            <span>${overview.reading_time_hours}h Reading</span>
                        </div>
                        <div class="notebooklm-feature">
                            <span class="notebooklm-icon">🔗</span>
                            <span>${overview.connections_found} Connections</span>
                        </div>
                    </div>
                    
                    <h5 style="color: #c4b5fd; margin: 20px 0 10px 0;">🎯 Key Themes</h5>
                    <p style="margin: 0 0 16px 0;">${overview.key_themes.slice(0, 8).join(', ')}</p>
                    
                    <h5 style="color: #c4b5fd; margin: 20px 0 10px 0;">💡 Recommendations</h5>
                    <ul style="margin: 0; padding-left: 20px;">
                        ${overview.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
        
        resultsDiv.innerHTML = overviewHTML;
    }
    
    async showDocumentConnections() {
        this.showLoading('Finding document connections...');
        
        try {
            const response = await fetch('/api/document_connections');
            const data = await response.json();
            
            if (data.success) {
                this.displayDocumentConnections(data.connections);
            } else {
                this.showError(`Failed to load connections: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        }
    }
    
    displayDocumentConnections(connections) {
        const resultsDiv = document.getElementById('notebooklm-results');
        
        if (connections.length === 0) {
            resultsDiv.innerHTML = `
                <div class="notebooklm-response">
                    <div class="notebooklm-response-text">
                        <p>No significant connections found between documents. Add more documents or check back after enhanced analysis.</p>
                    </div>
                </div>
            `;
            return;
        }
        
        const connectionsHTML = `
            <div class="notebooklm-response">
                <div class="notebooklm-response-header">
                    <h4>🔗 Document Connections (${connections.length})</h4>
                </div>
                
                <div class="notebooklm-response-text">
                    ${connections.slice(0, 10).map((conn, i) => `
                        <div class="notebooklm-citation">
                            <div class="notebooklm-citation-file">
                                Connection ${i + 1} - Strength: ${(conn.strength * 100).toFixed(0)}%
                            </div>
                            <div class="notebooklm-citation-excerpt">
                                <strong>Type:</strong> ${conn.connection_type}<br>
                                <strong>Shared concepts:</strong> ${conn.shared_concepts.slice(0, 5).join(', ')}<br>
                                <strong>Explanation:</strong> ${conn.explanation}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        resultsDiv.innerHTML = connectionsHTML;
    }
    
    async enhanceAnalysis() {
        this.showLoading('Enhancing document analysis...');
        
        try {
            const response = await fetch('/api/enhance_ingestion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayEnhanceResults(data);
            } else {
                this.showError(`Enhancement failed: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        }
    }
    
    displayEnhanceResults(data) {
        const resultsDiv = document.getElementById('notebooklm-results');
        
        const enhanceHTML = `
            <div class="notebooklm-response">
                <div class="notebooklm-response-header">
                    <h4>⚡ Enhanced Analysis Complete</h4>
                </div>
                
                <div class="notebooklm-response-text">
                    <p><strong>Processed:</strong> ${data.processed_count} of ${data.total_documents} documents</p>
                    <p><strong>Processing Time:</strong> ${(data.processing_time_ms / 1000).toFixed(1)}s</p>
                    
                    ${data.errors.length > 0 ? `
                        <h5 style="color: #fca5a5; margin: 16px 0 8px 0;">Errors:</h5>
                        <ul style="color: #fca5a5; margin: 0; padding-left: 20px;">
                            ${data.errors.slice(0, 5).map(error => `<li>${error}</li>`).join('')}
                        </ul>
                    ` : ''}
                    
                    <p style="margin-top: 16px; color: #a78bfa;">
                        ${data.message} Your documents now have enhanced analysis for better querying and connections.
                    </p>
                </div>
            </div>
        `;
        
        resultsDiv.innerHTML = enhanceHTML;
    }
    
    showLoading(message) {
        const resultsDiv = document.getElementById('notebooklm-results');
        
        resultsDiv.innerHTML = `
            <div class="notebooklm-loading">
                <div class="notebooklm-spinner"></div>
                <span>${message}</span>
            </div>
        `;
    }
    
    showError(message) {
        const resultsDiv = document.getElementById('notebooklm-results');
        
        resultsDiv.innerHTML = `
            <div class="notebooklm-error">
                <strong>Error:</strong> ${message}
            </div>
        `;
    }
    
    toggle() {
        if (this.isVisible) {
            this.hide();
        } else {
            this.show();
        }
    }
}

// Export for use in main.js
window.NotebookLMInterface = NotebookLMInterface;