// UI logic for Clever: input focus, send, esc clear, ctrl+U upload, analysis panel, floating panels
(function() {
    const input = document.getElementById('mainInput');
    // Remove static analysis panel usage
    let fileInput = null;
    // Panel stack container (bottom-right, non-overlapping)
    let panelStack = document.getElementById('panel-stack');
    if (!panelStack) {
        panelStack = document.createElement('div');
        panelStack.id = 'panel-stack';
        panelStack.className = 'panel-stack';
        document.body.appendChild(panelStack);
    }

    // Hide input until focused
        input.style.opacity = '0'; 
        input.style.pointerEvents = 'none'; 

    function showInput() {
        input.style.opacity = '1';
        input.style.pointerEvents = 'auto';
        input.focus();
    }

    // Click anywhere (except controls) focuses input
    document.body.addEventListener('mousedown', e => {
        if (!input.contains(e.target)) showInput();
    });

    // Keydown handler
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const msg = input.value.trim();
            if (msg) {
                window.CleverUI.pushLog('User', msg);
                window.CleverUI.onSend && window.CleverUI.onSend(msg);
                input.value = '';
            }
        } else if (e.key === 'Escape') {
            input.value = '';
        } else if ((e.ctrlKey || e.metaKey) && (e.key === 'u' || e.key === 'U')) {
            e.preventDefault();
            if (!fileInput) {
                fileInput = document.createElement('input');
                fileInput.type = 'file';
                fileInput.style.display = 'none';
                document.body.appendChild(fileInput);
                fileInput.addEventListener('change', function() {
                    if (fileInput.files.length) {
                        window.CleverUI.pushLog('System', 'Uploading file...');
                        window.CleverUI.onUpload && window.CleverUI.onUpload(fileInput.files[0]);
                    }
                    fileInput.value = '';
                });
            }
            fileInput.click();
        }
    });

    // Show input on first click
    setTimeout(() => {
        document.body.addEventListener('click', showInput, { once: true });
    }, 100);

    // Analysis log bubble
    // All logs/status/analysis now use floating panels

    // Magical dissolve effect for panels
    function dissolvePanel(card) {
        card.style.transition = 'opacity 0.5s cubic-bezier(.4,2,.6,1), filter 0.7s cubic-bezier(.4,2,.6,1)';
        card.style.filter = 'blur(8px) brightness(2)';
        card.style.opacity = '0';
        setTimeout(() => card.remove(), 700);
    }

    // Microcopy disabled per request (no top context banner)
    function showMicrocopy(_) { return; }

    function pushLog(kind, text) {
        if (!text) return;
        const card = document.createElement('div');
        card.className = 'floating-panel';
        card.innerHTML = `
            <div class="panel-main"><span class="bubble-tag">${kind}</span> ${text}</div>
        `;
        panelStack.appendChild(card);
        // keep a bounded number of panels
        while (panelStack.childElementCount > 5) {
            panelStack.firstElementChild.remove();
        }
        setTimeout(() => dissolvePanel(card), 7000);
    }

    // Floating response panel (structured data)

    function spawnPanel({message, context, source, confidence}) {
        const card = document.createElement('div');
        card.className = 'floating-panel';
        card.innerHTML = `
            <div class="panel-main">${message || ''}</div>
            <div class="panel-meta">
                ${context ? `<span>Intent: ${context}</span>` : ''}
                ${source ? `<span>Source: ${source}</span>` : ''}
                ${confidence ? `<span>Mood: ${confidence}</span>` : ''}
            </div>
        `;
        panelStack.appendChild(card);
        while (panelStack.childElementCount > 5) {
            panelStack.firstElementChild.remove();
        }
        setTimeout(() => dissolvePanel(card), 7000);
    }



    // Persona switching logic removed; mode is set by intent only

    // Voice input logic (Web Speech API)
    const micBtn = document.getElementById('mic-btn');
    let recognition = null;
    let recognizing = false;
    if (micBtn && 'webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.onstart = function() {
            recognizing = true;
            micBtn.style.background = '#2de0ff33';
        };
        recognition.onend = function() {
            recognizing = false;
            micBtn.style.background = '';
        };
        recognition.onresult = function(event) {
            if (event.results.length > 0) {
                const transcript = event.results[0][0].transcript;
                input.value = transcript;
                input.focus();
                // Optionally auto-send:
                window.CleverUI.pushLog('User', transcript);
                window.CleverUI.onSend && window.CleverUI.onSend(transcript);
                input.value = '';
            }
        };
        micBtn.addEventListener('click', function() {
            if (recognizing) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    } else if (micBtn) {
        micBtn.disabled = true;
        micBtn.title = 'Voice input not supported in this browser';
    }

    // Expose for main.js
    window.CleverUI = {
        pushLog,
        spawnPanel,
        showMicrocopy,
        onSend: null,
        onUpload: null
    };
})();
