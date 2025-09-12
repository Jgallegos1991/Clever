# Jay’s Copilot Recipes

## UI — Nanobots brightness & count
Prompt: 
“@workspace Update nanobot_swarm.js: set count=20000, alpha≈0.22, sizeMin≈0.6 sizeMax≈1.2, keep halo subtle. Return a unified diff and explain perf impact.”

## UI — Morph on app states
Prompt:
“Wire swarm morphs: thinking→torus, ingesting→ring, success→sphere, idle→panel. Touch only main.js & ui.js. Show exact code patches and where to call them.”

## Flask — New local endpoint
Prompt:
“Add /api/summarize (POST), accepts text, returns 3-sentence local summary using spaCy only. No external calls. Show unit test with pytest.”

## NLP — Expand free-text shape intents
Prompt:
“Loosen nlp_processor to detect shapes from free descriptions (‘wave’, ‘spiral’, ‘petals’). Map to procedural targets in nebula_renderer.js. Provide diffs + quick demo messages.”

## Tests — SQLite temp DB
Prompt:
“Create pytest fixtures for a temp SQLite db; ensure DatabaseManager points to it for tests only. Add tests for backup_manager backup/restore happy paths.”

## Refactor — Safe patch
Prompt:
“@file nanobot_swarm.js refactor into smaller helpers (physics, draw, shapes). Keep behavior identical. Return a diff annotated with brief comments.”
