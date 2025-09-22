# GitHub Workflow & .github Directory Guide

"""
Why: Provide a clear, centralized contract for contribution automation, agent usage, and branching so tools and humans follow the same process.
Where: Governs interactions with `.github/` (onboarding, instructions, workflows), links to diagnostics (`docs/copilot_diagnostics.md`), and repository root docs (`README.md`, `CHANGELOG.md`).
How: Defines branching (merge strategy), pull request expectations, agent onboarding sequence, and documentation integrity rules (single-source canonical patterns).
"""

## Overview
Clever uses a **merge-based** workflow (no interactive rebases in shared history) to minimize complex conflict scenarios—especially with fast-changing introspection and documentation files.

## Branching Strategy
- `main`: Always green, deployable, offline-compliant
- Feature branches: `feat/<slug>` or `chore/<slug>` or `docs/<slug>`
- Avoid long-lived branches (>5 days) to reduce drift

## Pull Request Guidelines
| Aspect | Requirement |
|--------|-------------|
| Tests | Mandatory for behavioral changes (persona, sanitizer, routes) |
| Docs | Update related spec (persona_spec, app_overview, etc.) |
| Offline Guard | Must retain `offline_guard.enable()` in `app.py` |
| Single DB | No additional DB files; only `config.DB_PATH` |
| Reasoning Leakage | New responses must not add meta tokens |
| Conflict Markers | PRs must not contain `<<<<<<<` / `>>>>>>>` |

## Agent Onboarding Sequence
1. Read `.github/AGENT_ONBOARDING.md`
2. Read `docs/architecture.md`
3. Read `docs/persona_spec.md`
4. Run `make diagnostics` (verify offline + single DB)
5. Run `make test`

## .github Directory Contents
| Path | Purpose |
|------|---------|
| `.github/AGENT_ONBOARDING.md` | Mandatory first-read checklist |
| `.github/copilot-instructions.md` | UI & architectural guardrails |
| `.github/instructions/` | Specialized instruction sets (UI, etc.) |
| `.github/prompts/` | (If present) Specialized LLM prompt templates |
| `.github/workflows/` | CI automation (diagnostics, tests, lint) |

## Documentation Canonical Sources
| Topic | Canonical File |
|-------|----------------|
| Changelog | `CHANGELOG.md` (root) |
| Persona | `docs/persona_spec.md` |
| Architecture | `docs/architecture.md` |
| App Routes | `docs/app_overview.md` |
| UI Behavior | `docs/ui_overview.md` |
| Config | `docs/configuration.md` |

Pointer (deprecated duplicates) files must include an explicit note: "Canonical source is <file>".

## Commit Hygiene
- Use present tense: "Add sanitizer edge case" not "Added"
- Group related changes; avoid omnibus commits mixing UI + backend unless atomic feature
- Include doc/test update in same commit where feasible

## Merge Conflict Resolution Pattern
1. Abort rebase if conflict complexity escalates (`git rebase --abort`)
2. Use merge: `git pull --no-rebase` (configured via `pull.rebase=false`)
3. Resolve conflicts logically (prefer preserving sanitizer + introspection integrity)
4. Re-run: `make test && make diagnostics`
5. Commit with message: `Merge: resolve <files>`

## Diagnostics & Guardrails
Run before pushing:
```bash
make test
make diagnostics
```
Failures must be addressed, not bypassed.

## Forbidden Practices
- Introducing network calls
- Adding second database path or file copy
- Emitting raw reasoning scaffolds to UI
- Committing secrets or tokens

## Automation Hooks (Planned)
- CI job: detect duplicate top-level doc names
- CI job: ensure persona spec hash referenced in PR description (traceability)

## PR Template (Recommended Fields)
```
Summary:
Why:
Changes:
Tests:
Docs Updated:
Risk:
Rollback Plan:
```

## Rollback Strategy
Small revert: `git revert <sha>` → new PR
Compound failure: branch from last green tag and cherry-pick safelist commits.

## Change Visibility
All major persona or sanitization adjustments must:
1. Update spec
2. Note in `CHANGELOG.md`
3. Include/modify a test

---
*Canonical Source*: `docs/github_workflow.md`