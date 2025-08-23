
// Main wiring for Clever UI
(function() {
    const input = document.getElementById('mainInput');


    // Send message to /chat

    window.CleverUI.onSend = function(msg) {
        // Idle microcopy
        if (!msg.trim()) {
            window.CleverUI.showMicrocopy('Ambient creativity waiting...');
            return;
        }
        // Morph command: "form cube", "form torus", "form sphere"
        if (/form (cube|torus|sphere)/i.test(msg)) {
            const shape = msg.match(/form (cube|torus|sphere)/i)[1];
            window.Clever3D.setMorph(shape);
            window.CleverUI.showMicrocopy(`Ideas crystallizing as a ${shape}...`);
            window.CleverUI.pushLog('Clever', `Ideas crystallizing as a ${shape}...`);
            return;
        }
        // Summon microcopy
        window.CleverUI.showMicrocopy('Energy takes shape.');
        fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        })
        .then(r => r.json())
        .then(data => {
            if (data.reply) {
                window.CleverUI.pushLog('Clever', data.reply);
                window.CleverUI.spawnPanel({
                    message: data.reply,
                    context: data.analysis?.detected_intent,
                    source: data.analysis?.activePersona,
                    confidence: data.analysis?.user_mood
                });
                // Dialogue microcopy
                window.CleverUI.showMicrocopy('Your thought enters the flow.');
                // Grid ripple and magical panel emergence
                window.Clever3D.gridRipple();
                window.Clever3D.floatPanel('synaptic-hub-card', 10, 6, 0);
            } else if (data.error) {
                window.CleverUI.pushLog('Error', data.error || 'Unknown error from backend.');
            }
        })
        .catch((err) => {
            window.CleverUI.pushLog('Error', 'Network error.');
            if (window.console && err) console.error('Network error:', err);
        });
    };

    // Upload file to /ingest
    window.CleverUI.onUpload = function(file) {
        const fd = new FormData();
        fd.append('file', file);
        fetch('/ingest', { method: 'POST', body: fd })
        .then(r => r.json())
        .then(data => {
            if (data.message) {
                window.CleverUI.pushLog('System', data.message);
            } else if (data.error) {
                window.CleverUI.pushLog('Error', data.error);
            }
        })
        .catch(() => window.CleverUI.pushLog('Error', 'Upload failed.'));
    };
})();
