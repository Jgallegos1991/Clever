(async function(){
  // Self-check banner + ingest chip
  const banner = document.createElement('div');
  banner.id = 'selfcheck';
  banner.textContent = 'Checking…';
  banner.className = 'selfcheck';
  document.documentElement && document.body ? document.body.prepend(banner) : null;

  async function refreshSelfCheck(){
    try{
      const [h,c] = await Promise.all([
        fetch('/health').then(r=>r.ok).catch(()=>false),
        fetch('/context/notes').then(r=>r.ok).catch(()=>false),
      ]);
      const ok = h && c;
      banner.textContent = ok ? '✓ Ready' : '… Starting';
      banner.classList.toggle('ok', ok);
    }catch{
      banner.textContent = '… Starting';
      banner.classList.remove('ok');
    }
  }
  refreshSelfCheck();
  setInterval(refreshSelfCheck, 15000);

  const chatEl  = document.getElementById('chat');
  const inputEl = document.getElementById('chat-input');
  const modeEl  = document.getElementById('mode-select');
  const pulseBtn = document.getElementById('pulse-btn');
  const ingestBtn = document.getElementById('ingest-btn');
  const filesBtn = document.getElementById('files-btn');

  // FIX: actually request an ingest scan
  async function ingest(){
    try{
      const res = await fetch('/ingest', {
        method: 'POST',
        headers: {'content-type':'application/json'},
        body: JSON.stringify({ action: 'scan' })
      });
      // optional: nudge the user when errors come back
      if (!res.ok) {
        console.warn('Ingest HTTP error:', res.status, res.statusText);
        return;
      }
      const j = await res.json();
      if (j && Array.isArray(j.errors) && j.errors.length){
        console.warn('Ingest completed with errors:', j.errors);
      }
    }catch(e){
      console.error('Ingest failed:', e);
    }
  }

  if (ingestBtn) ingestBtn.onclick = ingest;
  if (pulseBtn)  pulseBtn.onclick  = ()=> window.__orbPulse(0.35);
  if (filesBtn)  filesBtn.onclick  = ()=> { window.location.href = '/ui/files'; };

  // Ingesting chip on chipline if present
  const chiplineCandidate = document.querySelector('.chipline');
  const ingestChip = document.createElement('span');
  ingestChip.className = 'chip ingest';
  ingestChip.textContent = 'Ingesting…';
  ingestChip.style.display = 'none';
  if (chiplineCandidate) {
    chiplineCandidate.appendChild(ingestChip);
    async function pollIngest(){
      try{
        const s = await fetch('/ingest/status').then(r=>r.json());
        ingestChip.style.display = s && s.running ? '' : 'none';
      }catch{
        ingestChip.style.display = 'none';
      }
    }
    setInterval(pollIngest, 5000);
    pollIngest();
  }

  // Clean mode toggle
  function setClean(on){ document.body.classList.toggle('clean', !!on); }
  let clean = false;
  window.__uiClean = (mode)=>{ if (mode==null){ return clean; } clean = !!mode; setClean(clean); };

  // Keyboard: Ctrl/Cmd+M toggles clean
  window.addEventListener('keydown', (e)=>{
    if ((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==='m'){
      clean = !clean; setClean(clean); e.preventDefault();
    }
  }, {passive:false});

  // optional: keyboard shortcut 'f' to open Files
  window.addEventListener('keydown', (e)=>{
    if(e.key==='f' && (e.ctrlKey||e.metaKey)){
      e.preventDefault();
      window.location.href='/ui/files';
    }
  }, {passive:false});

  function openSource(id){
    const url = new URL('/ui/sources', window.location.origin);
    url.searchParams.set('select', String(id));
    window.location.href = url.toString();
  }

  function makeMsg(role, text, meta){
    const wrap = document.createElement('div');
    wrap.className = 'msg ' + (role === 'user' ? 'user' : 'assistant');
    const body = document.createElement('div');
    body.textContent = text;
    wrap.appendChild(body);

    if (meta && (meta.intent || meta.source || meta.mood !== undefined || meta.mode || (meta.citations && meta.citations.length))){
      const chips = document.createElement('div'); chips.className = 'chipline';
      const add = (label)=>{ const c=document.createElement('span'); c.className='chip'; c.textContent=label; chips.appendChild(c); };
      if (meta.intent) add('Intent: ' + meta.intent);
      if (meta.source) add('Source: ' + meta.source);
      if (meta.mode)   add('Mode: ' + meta.mode);
      if (meta.validated) add('validated ✓');
      if (typeof meta.mood === 'number') add('Mood: ' + (meta.mood>0? 'positive' : meta.mood<0? 'negative':'neutral'));
      if (meta.citations && meta.citations.length){
        meta.citations.slice(0,3).forEach(c => {
          const btn = document.createElement('button');
          btn.className = 'chip';
          btn.textContent = c.filename;
          btn.title = c.path;
          btn.onclick = ()=> openSource(c.id);
          chips.appendChild(btn);
        });
      }
      wrap.appendChild(chips);
    }
    return wrap;
  }

  function renderHistory(items){
    chatEl.innerHTML = '';
    items.slice().reverse().forEach(it => {
      chatEl.appendChild(makeMsg(it.role, it.text));
    });
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  async function loadHistory(){
    const res = await fetch('/chat/history?limit=50');
    const j = await res.json();
    renderHistory(j.items || []);
  }
  await loadHistory();

  function detectShapeIntent(text){
    const s = text.toLowerCase();
    if (s.includes('cube') || s.includes('square') || s.includes('box') || s.includes('3d box') || s.includes('cone')) return 'cube';
    if (s.includes('ring') || s.includes('circle') || s.includes('orb') || s.includes('torus')) return s.includes('torus') ? 'torus' : 'ring';
    if (s.includes('wave') || s.includes('grid')) return 'wave';
    if (s.includes('sphere') || s.includes('ball') || s.includes('globe')) return 'sphere';
    if (s.includes('knot') || s.includes('trefoil')) return 'knot';
    if (s.includes('pyramid') || s.includes('tetra')) return 'pyramid';
    return null;
  }

  async function send(){
    const text = inputEl.value.trim();
    if(!text) return;
    inputEl.value='';
    if (window.__orbThinking) window.__orbThinking(true);

    // Local command routing
    const low = text.toLowerCase();
    if (low.includes('clean mode')){
      const on = !clean;
      clean = on; setClean(clean); if (window.__orbPulse) window.__orbPulse(0.15);
      if (window.__orbThinking) window.__orbThinking(false);
      return;
    }

    // Quick nav: files browser
    if (
      (low.includes('browse') && low.includes('context') && low.includes('files')) ||
      (low.includes('browse') && low.includes('files')) ||
      (low.includes('open') && low.includes('files')) ||
      low.includes('open file browser') ||
      low.includes('file browser') ||
      low === 'files' ||
      low.includes('context files')
    ){
      window.location.href = '/ui/files';
      if (window.__orbThinking) window.__orbThinking(false);
      return;
    }

    if (low === 'sources' || low.startsWith('open sources')){
      window.location.href = '/ui/sources';
      return;
    }

    if (low.includes('glow') && (low.includes('brighter') || low.includes('up'))){
      window.__orbPulse(0.6);
    }
    if (low.includes('particles')){
      window.__orbPulse(0.4);
      if (low.includes('more') || low.includes('up')){ if (window.__sceneParticles) window.__sceneParticles('more'); }
      if (low.includes('less') || low.includes('down')){ if (window.__sceneParticles) window.__sceneParticles('less'); }
    }

    const shape = detectShapeIntent(text);
    if (shape) {
      if (window.__sceneMorphForDialogue) window.__sceneMorphForDialogue({ shape, holdMs: 1500 });
      else if (window.__sceneSetShape) window.__sceneSetShape(shape);
    }

    window.__orbPulse(0.4);

    // We don't render a visible selector; treat it as "Auto" by default.
    const selectedMode = 'Auto';
    chatEl.appendChild(makeMsg('user', text, { mode: selectedMode }));
    chatEl.scrollTop = chatEl.scrollHeight;

    try {
      // FIX: Let backend infer modes when Auto
      const payload = { text };
      if (selectedMode !== 'Auto') payload.mode = selectedMode;

      const res = await fetch('/chat/send', {
        method:'POST',
        headers:{'content-type':'application/json'},
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

      const j = await res.json();

      if (window.__orbThinking) window.__orbThinking(false);
      if(j && typeof j.intensity === 'number') window.__orbPulse(j.intensity);
      if(j && typeof j.sentiment === 'number') window.__orbSetMood(j.sentiment);

      // Map intensity/sentiment to particle density/brightness
      if (typeof window.__sceneSetParticleLevel === 'function' && typeof j.intensity === 'number'){
        const lvl = Math.max(0.6, Math.min(2.4, 0.8 + j.intensity*1.6));
        window.__sceneSetParticleLevel(lvl);
      }
      if (typeof window.__sceneSetParticleBrightness === 'function' && typeof j.sentiment === 'number'){
        const b = 0.9 + Math.min(0.8, Math.abs(j.sentiment)*0.6);
        window.__sceneSetParticleBrightness(b);
      }

      if(j && j.mode){ window.__orbSetMode(j.mode); }
      const replyText = (j && j.reply) ? j.reply : 'On it — quick pass incoming.';

      chatEl.appendChild(makeMsg('assistant', replyText, {
        mode: j.mode,
        intent: j.intent,
        mood: j.sentiment,
        citations: j.citations || [],
        validated: !!j.validated
      }));

      // “pixel-born panel” for short replies
      if (typeof window.__sceneSpeakText === 'function'){
        const plain = (replyText || '').replace(/\s+/g, ' ').trim();
        if (plain && plain.length > 0 && plain.length <= 80){
          window.__sceneSpeakText(plain);
        }
      }

      // If backend inferred a shape intent, ensure morph cycle
      if (!shape && j && j.intent && /shape_request:(\w+)/.test(j.intent)){
        const sh = j.intent.split(':')[1];
        if (window.__sceneMorphForDialogue) window.__sceneMorphForDialogue({ shape: sh, holdMs: 1500 });
      }

      chatEl.scrollTop = chatEl.scrollHeight;
    } catch (error) {
      console.error('Chat send error:', error);
      if (window.__orbThinking) window.__orbThinking(false);

      const errorMsg = error.message.includes('fetch') 
        ? "I'm having trouble connecting. Check if Clever is running." 
        : "Something went wrong. I'm still here though!";

      chatEl.appendChild(makeMsg('assistant', errorMsg, {mode: 'Error', error: true}));
      chatEl.scrollTop = chatEl.scrollHeight;
    }
  }

  // Press Enter to send
  if (inputEl){
    inputEl.addEventListener('keydown', (e)=>{ if(e.key==='Enter') send(); });
  }

  // Voice input functionality
  const micBtn = document.getElementById('mic-btn');
  let recognition = null;
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (micBtn && SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    let isListening = false;

    micBtn.addEventListener('click', ()=>{
      if (isListening) { recognition.stop(); return; }
      try {
        recognition.start();
        isListening = true;
        micBtn.classList.add('listening');
        micBtn.title = 'Listening... (click to stop)';
        inputEl.placeholder = 'Listening for your voice...';
      } catch(e) {
        console.error('Speech recognition failed to start:', e);
      }
    });

    recognition.onresult = (e)=>{
      if (e.results.length > 0) {
        const transcript = e.results[0][0].transcript.trim();
        inputEl.value = transcript;
        send();
      }
    };

    recognition.onend = ()=>{
      isListening = false;
      micBtn.classList.remove('listening');
      micBtn.title = 'Talk to Clever';
      inputEl.placeholder = 'Talk to Clever...';
    };

    recognition.onerror = (e)=>{
      console.error('Speech recognition error:', e.error);
      isListening = false;
      micBtn.classList.remove('listening');
      micBtn.title = 'Talk to Clever';
      inputEl.placeholder = 'Talk to Clever...';
    };
  } else if (micBtn) {
    // Graceful fallback for unsupported browsers
    micBtn.addEventListener('click', ()=>{
      alert('Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.');
    });
  }

  // Keep mode feedback handler if the selector exists in some views
  if (modeEl){
    modeEl.addEventListener('change', ()=>{
      const m = modeEl.value || 'Auto';
      if (m === 'Deep Dive')      { window.__orbSetMood(-0.05); window.__orbPulse(0.2); }
      else if (m === 'Creative')  { window.__orbSetMood(0.15);  window.__orbPulse(0.3); }
      else if (m === 'Support')   { window.__orbSetMood(0.1);   window.__orbPulse(0.15); }
      else if (m === 'Quick Hit') { window.__orbSetMood(0.0);   window.__orbPulse(0.25); }
      else                        { window.__orbSetMood(0.0); }
    });
  }
})();
