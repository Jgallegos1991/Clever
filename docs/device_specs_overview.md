# Device Specs Overview (Concise)

"""
Why: Provide a fast-loading summary of hardware constraints guiding performance, UI animation budgets, and memory-aware design—without requiring full deep dive.
Where: Supplements detailed `docs/config/device_specifications.md`; referenced by `README.md`, performance tuning discussions, and future optimization tasks.
How: Extracts critical limits (CPU class, disk space, resolution, memory pressure vectors) into a compact table + actionable guidelines.
"""

## Critical Constraints
| Category | Key Facts | Design Impact |
|----------|----------|---------------|
| CPU | Intel(R) Pentium(R) Silver N6000 @ 1.10GHz (Jasper Lake) | Keep persona + NLP lightweight; avoid heavy parallelism |
| Storage | 85.6GB free (114GB total) | Keep DB < 1GB; prune logs; avoid large cached artifacts |
| Memory | 3.7GB RAM (3862416 kB); browser/Chrome tabs consume significant RAM | Limit in-memory caches; stream where possible |
| Display | 1366x768 primary | Favor minimal UI footprint; avoid verbose panels |
| Network | Offline-first requirement | No runtime external fetches; local models only |
| GPU/Canvas | Capable of particle effects | Maintain adaptive particle count for 45–60fps |

## Performance Guardrails
- Particle engine must degrade gracefully (quality scaling)
- Avoid loading large NLP models (stick to spaCy small)
- Keep chat response cycle < 150ms typical (I/O + persona + sanitize)

## Operational Limits
| Aspect | Recommended Ceiling |
|--------|---------------------|
| Particle Count | 8k nominal, auto-reduce to 3.5k under load |
| PDF Upload Size | 10MB each |
| Concurrent Background Jobs | 1 ingestion + 1 chat max |
| Log File Growth | Rotate > 25MB cumulative |

## Immediate Risks
- High disk utilization → risk of DB growth failure
- Memory spikes from many open browser tabs + particle engine

Mitigation: Add periodic DB size check & optional compaction (future task).

## Quick Checklist (Dev Changes)
Before merging a performance-sensitive feature:
1. Will it add >50MB memory transiently? Reassess.
2. Does it introduce new network calls? Reject.
3. Does it increase persistent storage footprint notably? Document & justify.
4. Does it slow baseline chat latency? Measure & optimize.

---
*Canonical Source*: `docs/config/device_specifications.md` (last updated: 2025-09-24)