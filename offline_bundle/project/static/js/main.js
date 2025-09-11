document.addEventListener('DOMContentLoaded', () => {
  const userInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-btn');

  // Initialize particle canvas if present
  const canvasElem = document.getElementById('particles');
  if (canvasElem instanceof HTMLCanvasElement && typeof window.startParticles === 'function') {
    window.startParticles(canvasElem, { count: 4000 });
  }

  // Send on click or Enter
  sendButton?.addEventListener('click', () => sendMessage());
  userInput?.addEventListener('keypress', e => {
    if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
  });

  showStatus('Ambient creativity waiting…');

  // Animate panels in as if condensing from the swarm
  const panels = document.querySelectorAll('.panel');
  panels.forEach(p => {
    p.classList.add('appear');
    p.addEventListener('animationend', () => p.classList.remove('appear'), { once: true });
  });

  // Summon behavior: on input focus, ripple the grid and add a subtle pulse
  userInput?.addEventListener('focus', () => {
    const grid = document.querySelector('.grid-overlay');
    if (grid) {
      grid.classList.add('ripple');
      setTimeout(() => grid.classList.remove('ripple'), 600);
    }
    if (typeof window.triggerPulse === 'function') window.triggerPulse(0.5);
  });
});

async function sendMessage() {
  const inputElem = document.getElementById('chat-input');
  if (!(inputElem instanceof HTMLInputElement)) return;
  const text = inputElem.value.trim();
  if (!text) return;
  appendMessage('user', text);
  // Visual ripple: show grid thinking effect
  const grid = document.querySelector('.grid-overlay');
  if (grid) {
    grid.classList.add('ripple');
    setTimeout(() => grid.classList.remove('ripple'), 600);
  }
  inputElem.value = '';
  showStatus('Ideas crystallizing...');
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    const reply = data.response || '...';
    appendMessage('ai', reply);
    if (data && typeof data === 'object') updateAnalysis(data.analysis || {});
    // Particle reactions
    if (typeof window.updateFieldMode === 'function') {
      window.updateFieldMode(data.mood || 'Base');
    }
    if (typeof window.triggerPulse === 'function') {
      window.triggerPulse(data.particle_intensity || 0.5);
    }
    if (typeof window.morphForIntent === 'function') {
      // Map approach/intent to explicit morph shape for clearer storytelling
      const intent = mapApproachToIntent(data.approach, data?.analysis?.intent);
      window.morphForIntent(intent);
    }
    // AI response complete: visual and status update
    if (/money|dollar|finance/i.test(reply)) {
      window.morphForIntent('-'); // text morph to $ or text morph to '💰'
      if (window.triggerPulse) window.triggerPulse(1.0);
    }
    // Show energy manifestation copy
    showStatus('Energy takes shape.');
    // After a delay, return to idle microcopy
    setTimeout(() => {
      showStatus('Ambient creativity waiting...');
  const dissolve = window['dissolveToSwarm'];
  if (typeof dissolve === 'function') dissolve();
    }, 2000);
  } catch (err) {
    appendMessage('ai', 'Error.');
    console.error(err);
    showStatus('Error occurred');
  }
}

function appendMessage(who, text) {
  const log = document.getElementById('chat-log');
  const div = document.createElement('div');
  div.classList.add('message', who);
  div.textContent = text;
  // subtle condense-from-swarm entrance
  div.classList.add('appear');
  div.addEventListener('animationend', () => div.classList.remove('appear'), { once: true });
  log.append(div);
  log.scrollTop = log.scrollHeight;
}

function mapApproachToIntent(approach, fallbackIntent){
  const a = String(approach||'').toLowerCase();
  const f = String(fallbackIntent||'').toLowerCase();
  if (a.includes('creative')) return 'creative'; // torus
  if (a.includes('deep') || a.includes('analy')) return 'deep'; // cube
  if (a.includes('explore') || a.includes('discover')) return 'galaxy';
  if (f.includes('casual') || f.includes('chat')) return 'casual_chat'; // sphere
  if (f.includes('creative')) return 'creative';
  if (f.includes('deep')) return 'deep';
  return 'casual_chat';
}

function updateAnalysis(analysis) {
  const intentEl = document.getElementById('intent');
  const sentimentEl = document.getElementById('sentiment');
  const entitiesEl = document.getElementById('entities');
  const keywordsEl = document.getElementById('keywords');
  if (!intentEl || !sentimentEl || !entitiesEl || !keywordsEl) return;

  intentEl.textContent = 'Intent: ' + (analysis.intent || '—');
  const s = analysis.sentiment;
  // Compute sentiment text
  let sentimentText = '—';
  if (s && typeof s.compound === 'number') {
    sentimentText = s.compound.toFixed(2);
  } else if (typeof s === 'number') {
    sentimentText = s.toString();
  }
  sentimentEl.textContent = 'Sentiment: ' + sentimentText;
  entitiesEl.textContent = 'Entities: ' + ((analysis.entities||[]).join(', ') || '—');
  keywordsEl.textContent = 'Keywords: ' + ((analysis.keywords||[]).join(', ') || '—');
}

function showStatus(msg) {
  const status = document.getElementById('selfcheck');
  if (status) status.textContent = msg;
}