// UI logic for Clever: input focus, send, esc clear, ctrl+U upload, analysis panel, floating panels
(function() {
    const input = document.getElementById('mainInput');
    const panel = document.getElementById('analysis-panel');
    let fileInput = null;

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
    function pushLog(kind, text) {
        if (!text) return;
        const div = document.createElement('div');
        div.className = 'analysis-bubble ' + kind.toLowerCase();
        div.innerHTML = `<span class="bubble-tag">${kind}</span> ${text}`;
        panel.appendChild(div);
        setTimeout(() => {
            div.style.opacity = '0';
            setTimeout(() => div.remove(), 1200);
        }, 7000);
    }

    // Floating response panel
    function spawnPanel({message, context, source, confidence}) {
        const card = document.createElement('div');
        card.className = 'floating-panel';
        card.style.right = (32 + Math.random() * 24) + 'px';
        card.style.bottom = (100 + Math.random() * 40) + 'px';
        card.innerHTML = `
            <div class="panel-main">${message || ''}</div>
            <div class="panel-meta">
                ${context ? `<span>${context}</span>` : ''}
                ${source ? `<span>Source: ${source}</span>` : ''}
                ${confidence ? `<span>Conf: ${confidence}</span>` : ''}
            </div>
        `;
        document.body.appendChild(card);
        setTimeout(() => {
            card.style.opacity = '0';
            setTimeout(() => card.remove(), 1200);
        }, 7000);
    }

    // Expose for main.js
    window.CleverUI = {
        pushLog,
        spawnPanel,
        onSend: null,
        onUpload: null
    };
})();
