import { startParticles, triggerPulse, updateFieldMode, morphForIntent } from './particle_field.js'
import { startRenderer, triggerPulseAnimation, updateOrbColors } from './orb_renderer.js'
import { initVoice, speak as speakOut, isEnabled as ttsEnabled, setEnabled as setTTSEnabled, applyPersonaStyle } from './voice.js'

function $(id) { return document.getElementById(id); }

function addMessageToLog(sender, message) {
	const chatLog = $('chat-log');
	if (!chatLog) throw new Error('Missing #chat-log element');
	const wrap = document.createElement('div');
	wrap.className = 'chat-message-wrapper';

	const bubble = document.createElement('div');
	bubble.className = `chat-message ${sender.toLowerCase()}-message`;

	const who = document.createElement('div');
	who.className = 'sender';
	who.textContent = sender;

	const text = document.createElement('p');
	text.textContent = message;

	bubble.append(who, text);
	wrap.appendChild(bubble);
	chatLog.appendChild(wrap);
	chatLog.scrollTop = chatLog.scrollHeight;
}

function updateAnalysisPanel(analysis) {
	// Optional: integrate with your side-panels (ui.js). Throws if not present.
	if (!analysis) return;
}

window.addEventListener('DOMContentLoaded', () => {
	const canvas = $('main-canvas');
	if (!canvas) throw new Error('Missing #main-canvas element');
	let usingWebGL = false;
	try {
		const canGL = !!canvas.getContext('webgl2');
		if (canGL) { 
			startParticles(canvas, { count: 20000 }); 
			usingWebGL = true; 
		}
	} catch (err) {
		console.warn('[Clever] WebGL2 unavailable, falling back to 2D orb:', err);
	}
	if (!usingWebGL) { 
		startRenderer(canvas); 
	}

	const form = $('input-form');
	const input = $('chat-input');
	const log = $('chat-log');
	const voiceSelect = $('voice-select');
	const ttsToggle = $('tts-toggle');
	if (!form || !input || !log) throw new Error('Missing required DOM ids: input-form, chat-input, chat-log');

	// Click anywhere to focus input
	const focusInput = () => { try { input.focus({ preventScroll: true }); } catch(_) { input.focus(); } };
	document.addEventListener('pointerdown', (e) => {
		// Don’t steal focus from interactive elements
		const tag = (e.target && e.target.tagName || '').toLowerCase();
		if (['input','textarea','button','select','a'].includes(tag)) return;
		focusInput();
	});

	// Type-anywhere: route keystrokes into the input when nothing else is focused
	document.addEventListener('keydown', (e) => {
		const active = document.activeElement;
		const isTyping = active && ['input','textarea'].includes((active.tagName||'').toLowerCase());
		if (isTyping) return;
		if (e.metaKey || e.ctrlKey || e.altKey) return;
		// Submit on Enter
		if (e.key === 'Enter') {
			focusInput();
			form.requestSubmit();
			e.preventDefault();
			return;
		}
		// Basic text keys
		if (e.key && e.key.length === 1) {
			focusInput();
			input.value = (input.value || '') + e.key;
			e.preventDefault();
		}
		// Backspace routing
		if (e.key === 'Backspace') {
			focusInput();
			input.value = (input.value || '').slice(0, -1);
			e.preventDefault();
		}
	});

	// Submit via button or Enter
	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		const msg = (input.value || '').trim();
		if (!msg) return;

		input.value = '';
		addMessageToLog('You', msg);

		// placeholder while waiting
		const holder = document.createElement('div');
		holder.className = 'chat-message-wrapper';
		holder.innerHTML = `<div class="chat-message clever-message"><div class="sender">Clever</div><p>…</p></div>`;
		log.appendChild(holder);
		log.scrollTop = log.scrollHeight;

		try {
			const res = await fetch('/chat', {
				method: 'POST',
				headers: {'Content-Type':'application/json'},
				body: JSON.stringify({ message: msg })
			});
			let data = null;
			try { data = await res.json(); } catch {}

			holder.remove();

			if (!res.ok || !data || (!data.reply && !data.error)) {
				addMessageToLog('System Error', `Core did not return a reply (HTTP ${res.status}).`);
				if (usingWebGL) updateFieldMode('Base'); else updateOrbColors(); 
				return;
			}

			if (data.error && !data.reply) {
				addMessageToLog('Clever', 'I’m in basic mode right now, but I’m with you.');
				if (usingWebGL) updateFieldMode('Base'); else updateOrbColors(); 
				return;
			}

			addMessageToLog('Clever', data.reply);
			updateAnalysisPanel(data.analysis || null);
			// Visual reactions
			const a = data.analysis || {};
			if (usingWebGL) { 
				if (a.detected_intent === 'ask_question') triggerPulse();
				updateFieldMode(a.activePersona);
				morphForIntent(a);
			} else {
				if (a.detected_intent === 'ask_question') triggerPulseAnimation();
				updateOrbColors(a.activePersona);
			}

			// Visual feedback
			if (data.analysis && data.analysis.detected_intent === 'ask_question') {
				triggerPulse();
			}
			updateFieldMode(data.analysis?.activePersona);
			// Shape morph if intent present
			try {
				const intents = data.analysis?.intents || [];
				const ui = intents.find(i => i && i.name === 'ui.shape');
				if (ui && ui.details) morphForIntent(ui.details);
			} catch (_) {}
			// Broadcast analysis for optional listeners
			try { window.dispatchEvent(new CustomEvent('clever:analysis', { detail: data.analysis })); } catch(_) {}
		} catch (err) {
			holder.remove();
			console.error('[Clever UI] /chat failed:', err);
			addMessageToLog('System Error', "Connection to Clever's core lost.");
			if (usingWebGL) updateFieldMode('Base'); else updateOrbColors();
		}
	});


	// Speak Clever replies automatically
	const origAdd = addMessageToLog;
	addMessageToLog = (sender, message) => {
		origAdd(sender, message);
		if (sender.toLowerCase() === 'clever' && ttsEnabled()) speakOut(message);
	};

	// --- Voice input (browser recorder + POST /api/stt) ---
	async function recordAndTranscribe(seconds = 6) {
		if (!navigator.mediaDevices?.getUserMedia) throw new Error('mic not available');
		const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
		const ctx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
		const src = ctx.createMediaStreamSource(stream);
		const processor = ctx.createScriptProcessor(4096, 1, 1);
		const bufs = [];
		processor.onaudioprocess = (e) => {
			const ch = e.inputBuffer.getChannelData(0);
			bufs.push(new Float32Array(ch));
		};
		src.connect(processor); processor.connect(ctx.destination);
		await new Promise(r => setTimeout(r, Math.max(1000, seconds * 1000)));
		src.disconnect(); processor.disconnect(); stream.getTracks().forEach(t => t.stop());
		// Merge float32 → Int16 PCM
		let length = bufs.reduce((a, b) => a + b.length, 0);
		const pcm16 = new Int16Array(length);
		let offset = 0;
		for (const b of bufs) {
			for (let i = 0; i < b.length; i++) {
				let s = Math.max(-1, Math.min(1, b[i]));
				pcm16[offset++] = s < 0 ? s * 0x8000 : s * 0x7FFF;
			}
		}
		// Write WAV header (mono, 16-bit, 16kHz)
		const bytesPerSample = 2;
		const blockAlign = 1 * bytesPerSample;
		const byteRate = 16000 * blockAlign;
		const buffer = new ArrayBuffer(44 + pcm16.byteLength);
		const view = new DataView(buffer);
		function wStr(o, s){ for(let i=0;i<s.length;i++) view.setUint8(o+i, s.charCodeAt(i)); }
		let p = 0;
		wStr(p, 'RIFF'); p += 4;
		view.setUint32(p, 36 + pcm16.byteLength, true); p += 4;
		wStr(p, 'WAVE'); p += 4;
		wStr(p, 'fmt '); p += 4;
		view.setUint32(p, 16, true); p += 4; // PCM header size
		view.setUint16(p, 1, true); p += 2;  // PCM format
		view.setUint16(p, 1, true); p += 2;  // mono
		view.setUint32(p, 16000, true); p += 4; // sample rate
		view.setUint32(p, byteRate, true); p += 4;
		view.setUint16(p, blockAlign, true); p += 2;
		view.setUint16(p, 16, true); p += 2; // bits per sample
		wStr(p, 'data'); p += 4;
		view.setUint32(p, pcm16.byteLength, true); p += 4;
		new Int16Array(buffer, 44).set(pcm16);
		const wavBlob = new Blob([buffer], { type: 'audio/wav' });
		const fd = new FormData();
		fd.append('audio', wavBlob, 'speech.wav');
		const res = await fetch('/api/stt', { method: 'POST', body: fd });
		const data = await res.json();
		if (!res.ok) throw new Error(data?.error || 'stt failed');
		return String(data.text || '').trim();
	}

	// Mic button behavior (if present)
	const mic = $('mic-btn');
	if (mic) {
		mic.addEventListener('click', async (e) => {
			e.preventDefault();
			try {
				mic.disabled = true;
				const text = await recordAndTranscribe(6);
				if (text) {
					input.value = text;
					form.requestSubmit();
				}
			} catch (err) {
				console.error('voice input failed:', err);
			} finally {
				mic.disabled = false;
			}
		});
	}

	// Wire voice manager
	try { initVoice({ selectEl: voiceSelect, toggleEl: ttsToggle }); } catch (_) {}

	// React TTS style to persona
	window.addEventListener('clever:analysis', (ev) => {
		try { applyPersonaStyle(ev.detail?.activePersona || ''); } catch (_) {}
	});
});
