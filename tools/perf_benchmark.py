"""Performance & variation benchmark for PersonaEngine.

Why: Provides concrete latency metrics and variation statistics for the
persona response generation pipeline so regressions or performance
improvements can be tracked over time via CI perf job.
Where: Invoked by the perf-scan job in the unified GitHub Actions
workflow (`.github/workflows/clever-ci.yml`). Results artifact uploaded
for inspection. Also usable locally via `python tools/perf_benchmark.py`.
How: Warm-up run followed by timed runs over a fixed prompt set. Measures
per-response latency, computes summary stats (mean, p95). Variation is
quantified via unique first-line ratio and hash diversity. Output is
written to `perf_results.txt` in a simple key:value format plus a JSON
blob for programmatic consumption if needed.

Connects to:
  - persona.py: Uses PersonaEngine.generate for content & metadata
  - memory_engine.py: Indirect usage when PersonaEngine retrieves memory
  - nlp_processor.py: Exercises NLP pipeline to surface latency impact
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path as _PathForSys

# Ensure project root is on sys.path for direct script execution
_root = _PathForSys(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
import statistics
import time
from pathlib import Path
import os
from typing import List, Dict, Any

from persona import PersonaEngine

RESULT_PATH = Path("perf_results.txt")
HISTORY_PATH = Path("perf_history.jsonl")


def _now() -> float:
    """High resolution timestamp wrapper (separate for testability).

    Why: Abstracts time access for potential future mocking.
    Where: Used in benchmark timing loops only.
    How: Returns time.perf_counter for higher precision than time.time.
    """
    return time.perf_counter()


def benchmark_persona(iterations: int = 12) -> Dict[str, object]:
    """Run latency & variation benchmark.

    Why: Establish consistent metric capture (latency & variation) to
    detect regressions early in CI.
    Where: Called by main entrypoint when script executed. Data consumed
    by CI artifact retention, optionally future trend tooling.
    How: Executes warm-up, then loops over prompts collecting latency
    and signatures to compute summary statistics.

    Args:
        iterations: Number of generation calls (across prompt set cycles).

    Returns:
        Dictionary with latency stats & variation metrics.

    Connects to:
        - persona.PersonaEngine.generate: core generation path.
        - nlp_processor.AdvancedNLPProcessor: exercised for analysis.
    """
    engine = PersonaEngine()

    prompts: List[str] = [
        "Explain quantum tunneling simply",
        "Summarize black hole evaporation",
        "Give a supportive note about learning Python",
        "Offer a quick tip for focus",
    ]

    # Warm-up (not measured) to allow any lazy initialization
    cold_samples: List[float] = []
    for p in prompts:
        st = _now()
        engine.generate(p, mode="Auto")
        cold_samples.append(_now() - st)

    latencies: List[float] = []
    first_lines: List[str] = []
    signatures: List[str] = []
    char_counts: List[int] = []
    memory_items_considered: List[int] = []
    memory_items_used: List[int] = []
    predicted_mode_changes: int = 0

    # We derive a simple signature from first 48 chars to approximate diversity
    for i in range(iterations):
        prompt = prompts[i % len(prompts)]
        start = _now()
        resp = engine.generate(prompt, mode="Auto")
        elapsed = _now() - start
        latencies.append(elapsed)
        line0 = resp.text.splitlines()[0].strip()
        first_lines.append(line0)
        signatures.append(line0[:48])
        char_counts.append(len(resp.text))
        dbg: Any = getattr(resp, 'debug_metrics', {}) or {}
        memory_items_considered.append(dbg.get('memory_items_considered', 0))
        memory_items_used.append(dbg.get('memory_items_used', 0))
        if dbg.get('predicted_mode_changed'):
            predicted_mode_changes += 1

    mean_latency = statistics.mean(latencies)
    std_latency = statistics.pstdev(latencies) if len(latencies) > 1 else 0.0
    p95_latency = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)

    unique_first = len(set(first_lines))
    unique_sig = len(set(signatures))

    warm_segment = latencies[4:] if len(latencies) > 4 else latencies
    cold_mean = statistics.mean(cold_samples) if cold_samples else 0.0
    warm_mean = statistics.mean(warm_segment) if warm_segment else 0.0
    result = {
        "iterations": iterations,
        "mean_latency_sec": round(mean_latency, 5),
        "std_latency_sec": round(std_latency, 5),
        "max_latency_sec": round(max(latencies), 5),
        "p95_latency_sec": round(p95_latency, 5),
        "cold_mean_latency_sec": round(cold_mean, 5),
        "warm_mean_latency_sec": round(warm_mean, 5),
        "unique_first_lines": unique_first,
        "unique_first_line_ratio": round(unique_first / len(first_lines), 3),
        "unique_signatures": unique_sig,
        "avg_chars": round(statistics.mean(char_counts), 2) if char_counts else 0,
        "memory_items_considered_avg": round(statistics.mean(memory_items_considered), 3) if memory_items_considered else 0.0,
        "memory_items_used_avg": round(statistics.mean(memory_items_used), 3) if memory_items_used else 0.0,
        "memory_utilization_ratio": round((statistics.mean(memory_items_used) / statistics.mean(memory_items_considered)) if memory_items_considered and statistics.mean(memory_items_considered) else 0.0, 3),
        "predicted_mode_change_count": predicted_mode_changes,
        "timestamp": time.time(),
    }
    return result


def write_results(data: Dict[str, object]) -> None:
    """Persist results to text file plus embedded JSON.

    Why: Artifact captured by CI for longitudinal comparison.
    Where: Called at script end after bench execution; file consumed by
    GitHub Actions artifact upload step.
    How: Writes human-readable key:value lines then JSON block.

    Args:
        data: Benchmark metrics.

    Connects to:
        - CI workflow (artifact upload step) reading perf_results.txt
    """
    lines = [f"{k}: {v}" for k, v in data.items()]
    RESULT_PATH.write_text("\n".join(lines) + "\n\nJSON=" + json.dumps(data, indent=2))
    # Trend tracking: append JSON line to history log (rotation simple cap 300 lines)
    try:
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with HISTORY_PATH.open("a", encoding="utf-8") as hf:
            hf.write(json.dumps(data) + "\n")
        # Simple trim if file grows large
        stat = HISTORY_PATH.stat()
        if stat.st_size > 512_000:  # ~0.5MB safety cap
            lines = HISTORY_PATH.read_text().strip().splitlines()[-300:]
            HISTORY_PATH.write_text("\n".join(lines) + "\n")
    except Exception as e:  # Non-fatal; continue
        print(f"WARNING: Failed to update history: {e}")


def _check_thresholds(metrics: Dict[str, object]) -> bool:
    """Check environment-defined thresholds; return True if pass.

    Why: Enforce performance & variation guardrails so regressions do not silently
    land in main.
    Where: Called in main() after metric generation.
    How: Reads MAX_MEAN_LATENCY (float) and MIN_VARIATION_RATIO (float) env vars.
    Exits non-zero (handled by caller) if thresholds violated.
    """
    max_mean = os.getenv("MAX_MEAN_LATENCY")
    min_var = os.getenv("MIN_VARIATION_RATIO")
    ok = True
    if max_mean:
        try:
            raw_mean = metrics.get("mean_latency_sec", 0.0)
            mean_latency = float(raw_mean) if isinstance(raw_mean, (int, float, str)) else 0.0
            if mean_latency > float(max_mean):
                print(f"THRESHOLD FAIL: mean_latency_sec {mean_latency} > {max_mean}")
                ok = False
        except ValueError:
            print("WARNING: Invalid MAX_MEAN_LATENCY value")
    if min_var:
        try:
            raw_var = metrics.get("unique_first_line_ratio", 0.0)
            variation_ratio = float(raw_var) if isinstance(raw_var, (int, float, str)) else 0.0
            if variation_ratio < float(min_var):
                print(f"THRESHOLD FAIL: unique_first_line_ratio {variation_ratio} < {min_var}")
                ok = False
        except ValueError:
            print("WARNING: Invalid MIN_VARIATION_RATIO value")
    return ok


def main() -> int:
    """CLI entrypoint for benchmark script.

    Why: Provides standalone execution path outside CI.
    Where: Invoked when running `python tools/perf_benchmark.py` or by
    CI perf job.
    How: Calls benchmark_persona then writes results.
    """
    data = benchmark_persona()
    write_results(data)
    # Basic success heuristic: ensure some variation
    unique_first_val = data.get("unique_first_lines", 0)
    try:
        unique_first_int = int(unique_first_val)  # type: ignore[arg-type]
    except Exception:
        unique_first_int = 0
    if unique_first_int < 2:
        print("WARNING: Low variation detected")
    if not _check_thresholds(data):
        return 2
    print("Benchmark complete. Metrics written to", RESULT_PATH)
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
