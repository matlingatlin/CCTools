#!/usr/bin/env python3
"""Apply the registered decision rule to the concurrency-benchmark rows.

The rule lives in pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md and is
transcribed here as constants. This file does not measure and the runner does
not decide -- separated so that neither can quietly become the other.

Three verdicts, never two: RAISE_TO_4 / KEEP_2 / INDETERMINATE.
A check that could not run is never a pass.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUNS = REPO / "pipeline" / "bench" / "runs"

# --- the registered rule, transcribed. Changing a number here without a dated
# --- amendment in the prereg file is bar-moving.
GAIN_RATIO = 0.70          # W4 <= 0.70 * W2
CLOSE_BAND = (0.65, 0.75)  # amendment 1: inclusive -> INDETERMINATE
PER_RUN_MAX = 1.5          # median per-run at 4 <= 1.5x median at 2
MIN_VALID_BATCHES = 3      # per arm, after voids
MAX_LOAD_AT_START = 0.50


def batch_void_reasons(b: dict) -> list[str]:
    """Invalid-run criteria, judged on evidence independent of the result."""
    reasons = []
    if b.get("loadavg_at_start", 0) > MAX_LOAD_AT_START:
        reasons.append(f"loadavg at start {b['loadavg_at_start']} > {MAX_LOAD_AT_START}")
    for r in b.get("runs", []):
        st = r.get("status")
        if st in ("error", "unparseable"):
            reasons.append(f"run {r['idx']}: {st}")
        elif st == "timeout":
            reasons.append(f"run {r['idx']}: timeout")
        elif st == "no_usage":
            reasons.append(f"run {r['idx']}: completed but reported no usage")
        elif st == "no_work":
            reasons.append(f"run {r['idx']}: completed without doing the tool work")
        if not r.get("started") or not r.get("ended"):
            reasons.append(f"run {r['idx']}: missing started/ended")
    want = b.get("model_requested")
    for r in b.get("runs", []):
        served = r.get("models")
        if served is None:
            continue
        if want and want not in served:
            reasons.append(f"run {r['idx']}: requested {want}, served {served}")
    if any(r.get("api_error_status") for r in b.get("runs", [])):
        reasons.append("an API error status was reported in this batch")
    return reasons


def load(runs_dir: Path) -> dict:
    arms: dict[int, list] = {2: [], 4: []}
    voids: list[tuple[str, list[str]]] = []
    for path in sorted(runs_dir.glob("*.json")):
        b = json.loads(path.read_text())
        reasons = batch_void_reasons(b)
        if reasons:
            voids.append((path.name, reasons))
            continue
        arms.setdefault(b["concurrency"], []).append(b)
    return {"arms": arms, "voids": voids}


def per_run_median(batches: list) -> float | None:
    d = [r["duration_ms"] for b in batches for r in b["runs"] if r.get("status") == "ok"]
    return statistics.median(d) if d else None


def decide(data: dict) -> dict:
    arms, voids = data["arms"], data["voids"]
    a2, a4 = arms.get(2, []), arms.get(4, [])
    out = {
        "valid_batches": {"c2": len(a2), "c4": len(a4)},
        "voided_batches": [{"file": f, "reasons": r} for f, r in voids],
    }

    if len(a2) < MIN_VALID_BATCHES or len(a4) < MIN_VALID_BATCHES:
        out["verdict"] = "INDETERMINATE"
        out["reason"] = (
            f"need {MIN_VALID_BATCHES} valid batches per arm, have "
            f"c2={len(a2)} c4={len(a4)}. The cap stays 2."
        )
        return out

    w2 = statistics.median(b["wall_clock_s"] for b in a2)
    w4 = statistics.median(b["wall_clock_s"] for b in a4)
    ratio = w4 / w2
    p2, p4 = per_run_median(a2), per_run_median(a4)
    fails_at_4 = sum(1 for b in a4 for r in b["runs"] if r.get("status") != "ok")

    out.update({"W2_s": round(w2, 3), "W4_s": round(w4, 3), "ratio": round(ratio, 4),
                "per_run_median_ms": {"c2": p2, "c4": p4},
                "per_run_ratio": round(p4 / p2, 4) if (p2 and p4) else None,
                "failures_at_c4": fails_at_4})

    if CLOSE_BAND[0] <= ratio <= CLOSE_BAND[1]:
        out["verdict"] = "INDETERMINATE"
        out["reason"] = (
            f"ratio {ratio:.3f} falls in the close band {CLOSE_BAND} -- the workload was too "
            f"light to decide. The cap stays 2. This is not 'no significant difference'."
        )
        return out

    checks = {
        "gain": ratio < CLOSE_BAND[0],
        "no_per_run_degradation": (p2 is not None and p4 is not None and p4 <= PER_RUN_MAX * p2),
        "no_failures": fails_at_4 == 0,
    }
    out["checks"] = checks

    if p2 is None or p4 is None:
        out["verdict"] = "INDETERMINATE"
        out["reason"] = "per-run guardrail could not be computed: no ok runs in an arm."
        return out

    if all(checks.values()):
        out["verdict"] = "RAISE_TO_4"
        out["reason"] = (
            f"W4/W2 = {ratio:.3f} < {GAIN_RATIO}; per-run {p4/p2:.2f}x <= {PER_RUN_MAX}x; "
            f"0 failures at c=4. All three registered conditions hold."
        )
    else:
        failed = [k for k, v in checks.items() if not v]
        out["verdict"] = "KEEP_2"
        out["reason"] = f"registered condition(s) not met: {failed}. The status quo wins."
    return out


def main() -> int:
    runs = Path(sys.argv[1]) if len(sys.argv) > 1 else RUNS
    if not runs.exists() or not list(runs.glob("*.json")):
        print(json.dumps({"verdict": "INDETERMINATE",
                          "reason": f"no batches recorded under {runs}"}, indent=2))
        return 0
    print(json.dumps(decide(load(runs)), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
