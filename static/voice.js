// voice.js — Offline TTS manager using the browser's SpeechSynthesis (OS voices)
// Exports: initVoice({selectEl, toggleEl}), speak(text), isEnabled(), setEnabled(v)

let enabled = JSON.parse(localStorage.getItem('clever.tts.enabled') || 'true');
let selected = localStorage.getItem('clever.voice') || '';
let rate = Number(localStorage.getItem('clever.voice.rate') || '0.95');
let pitch = Number(localStorage.getItem('clever.voice.pitch') || '1.05');
let cachedVoices = [];

function loadVoices() {
  try {
    const vs = window.speechSynthesis?.getVoices?.() || [];
    cachedVoices = vs;
    return vs;
  } catch (_) {
    cachedVoices = [];
    return [];
  }
}

export function getVoices() {
  if (!cachedVoices.length) return loadVoices();
  return cachedVoices;
}

export function isEnabled() { return !!enabled; }
export function setEnabled(v) {
  enabled = !!v;
  localStorage.setItem('clever.tts.enabled', JSON.stringify(enabled));
}

export function speak(text) {
  if (!enabled) return;
  try {
    if (!('speechSynthesis' in window)) return;
    const u = new SpeechSynthesisUtterance(String(text || ''));
    // Pick selected voice if available
    const voices = getVoices();
    if (selected) {
      const v = voices.find(x => x.name === selected);
      if (v) u.voice = v;
    } else {
      // Prefer en-* voices by default if present
      const v = voices.find(x => /\ben[-_]/i.test(x.lang));
      if (v) u.voice = v;
    }
  // Gentle defaults, adjustable
  u.rate = rate; u.pitch = pitch; u.volume = 1.0;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
  } catch (_) {}
}

export function initVoice({ selectEl, toggleEl } = {}) {
  // Populate select when voices are ready
  function populate() {
    if (!selectEl) return;
    const voices = getVoices();
    // Filter to likely-local voices to keep list sane
    const filtered = voices.filter(v => /^(en|es|fr|de|it|pt|ja|ko|zh)/i.test(v.lang));
    selectEl.innerHTML = '';
    const optNone = document.createElement('option');
    optNone.value = '';
    optNone.textContent = 'Auto voice';
    selectEl.appendChild(optNone);
    for (const v of filtered) {
      const opt = document.createElement('option');
      opt.value = v.name;
      opt.textContent = `${v.name} (${v.lang})`;
      if (v.name === selected) opt.selected = true;
      selectEl.appendChild(opt);
    }
  }

  try {
    populate();
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = () => { loadVoices(); populate(); };
    }
  } catch (_) {}

  if (selectEl) {
    selectEl.addEventListener('change', () => {
      selected = selectEl.value || '';
      localStorage.setItem('clever.voice', selected);
    });
  }
  if (toggleEl) {
    toggleEl.setAttribute('aria-pressed', String(enabled));
    toggleEl.addEventListener('click', (e) => {
      e.preventDefault();
      setEnabled(!enabled);
      toggleEl.setAttribute('aria-pressed', String(enabled));
    });
  }
}

export function applyPersonaStyle(personaName) {
  // Light-touch mapping. Keep subtle.
  const p = String(personaName || '').toLowerCase();
  let r = 0.95, pi = 1.05;
  if (p.includes('calm') || p.includes('guide') || p.includes('mentor')) { r = 0.9; pi = 1.0; }
  if (p.includes('analyst') || p.includes('focus') || p.includes('task')) { r = 1.0; pi = 1.0; }
  if (p.includes('spark') || p.includes('creative') || p.includes('play')) { r = 1.05; pi = 1.1; }
  rate = r; pitch = pi;
  localStorage.setItem('clever.voice.rate', String(rate));
  localStorage.setItem('clever.voice.pitch', String(pitch));
}

