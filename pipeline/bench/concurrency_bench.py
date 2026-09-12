#!/usr/bin/env python3
"""Batch benchmark for the dispatch-concurrency cap (W_MAX_AGENTS).

Runs N identical headless `claude -p` runs at a fixed concurrency and records,
per run and per batch, exactly what the preregistration at
pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md says will decide.

This script MEASURES. It does not decide: `verdict.py` applies the registered
threshold to the rows this writes, so the analysis cannot quietly become a
different analysis by editing the runner.

Usage:
    concurrency_bench.py --concurrency 2 --batch b1 [--n 8] [--out DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO / "pipeline" / "bench" / "runs"

# The workload. Fixed by the registration: 2-4 real tool calls (grep + read +
# a short structured answer) over a fixed file in this repo. Identical in both
# arms -- the ONLY thing that differs between arms is how many run at once.
TARGET = "pipeline/validate/staleness.py"

# The run cannot read outside its own cwd, so the target is COPIED into each
# scratch directory. Found by the smoke run: without this the model refuses in
# ~6s having done no work at all, and eight parallel refusals would have read
# as a large win for concurrency 4 -- an inverted result, not a broken one.
PROMPT = (
    "Look at the file staleness.py in this directory.\n"
    "1. Run: grep -n '^def ' staleness.py\n"
    "2. Read the file.\n"
    "3. Answer in exactly this form and nothing else:\n"
    "FUNCTIONS: <count of top-level def statements>\n"
    "LINES: <total line count>\n"
    "VERDICT: <one sentence on what the module decides>\n"
)

# Pinned, not defaulted. `claude -p` in a fresh directory served haiku-4-5,
# which is not what dispatched readers run. The registration voids a batch on
# MIXED models but never said WHICH -- so a whole benchmark could have run on
# the wrong model and passed every void check.
#
# Opus 5 by instruction (amendment 3): it is the model dispatched readers
# actually run on, so the result needs no transfer argument at all.
MODEL = "claude-opus-5"

# A run must actually do the work. A run that answers without the tool calls
# is doing a different job than the one being timed.
MIN_TURNS = 2

# A run that outlives this is terminated and recorded as a timeout -- an
# invalid-run condition under the registration, not a slow success.
RUN_TIMEOUT_S = 300


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def loadavg() -> float:
    return os.getloadavg()[0]


def one_run(idx: int) -> dict:
    """Dispatch a single headless run from a fresh scratch directory."""
    scratch = tempfile.mkdtemp(prefix=f"bench-{idx}-")
    shutil.copy(REPO / TARGET, Path(scratch) / Path(TARGET).name)
    prompt = PROMPT
    started = time.time()
    started_iso = now_iso()
    row = {
        "idx": idx,
        "started": started_iso,
        "scratch": scratch,
        "status": "unknown",
        "duration_ms": None,
        "tokens": None,          # null, never a zero standing in for "unmeasured"
        "num_turns": None,
        "model": None,
    }
    try:
        proc = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "json",
             "--model", MODEL],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        row["ended"] = now_iso()
        row["duration_ms"] = int(round((time.time() - started) * 1000))
        row["status"] = "timeout"
        return row

    ended = time.time()
    row["ended"] = now_iso()
    row["duration_ms"] = int(round((ended - started) * 1000))
    row["exit_code"] = proc.returncode

    if proc.returncode != 0:
        row["status"] = "error"
        row["stderr"] = (proc.stderr or "")[-500:]
        return row

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        row["status"] = "unparseable"
        row["stdout_tail"] = (proc.stdout or "")[-500:]
        return row

    usage = payload.get("usage") or {}
    total = None
    if usage:
        total = sum(
            v for k, v in usage.items()
            if k.endswith("tokens") and isinstance(v, int)
        )
    row["tokens"] = total            # stays None when the run reported no usage
    row["num_turns"] = payload.get("num_turns")
    # modelUsage carries MORE THAN ONE key: the requested model plus whatever
    # auxiliary model the CLI uses internally. Reading [0] reported haiku for a
    # run correctly served by the pinned model, which would have voided every
    # batch on a mismatch that never happened. Record the set; the pinned model
    # must be IN it.
    row["models"] = sorted((payload.get("modelUsage") or {}).keys())
    row["model"] = MODEL if MODEL in row["models"] else None
    row["cost_usd"] = payload.get("total_cost_usd")
    # Exploratory, not registered: splits waiting-on-the-API from local work,
    # which is the mechanism the cap is actually arguing about.
    row["duration_api_ms"] = payload.get("duration_api_ms")
    row["ttft_ms"] = payload.get("ttft_ms")
    row["api_error_status"] = payload.get("api_error_status")
    row["answer"] = (payload.get("result") or "")[:300]
    # A run that completed but reported no usage is NOT a clean success: the
    # registration voids its batch for the primary metric.
    if not total:
        row["status"] = "no_usage"
    elif (payload.get("num_turns") or 0) < MIN_TURNS:
        # Completed, reported usage, but short-circuited the work.
        row["status"] = "no_work"
    else:
        row["status"] = "ok"
    return row


def run_batch(concurrency: int, batch: str, n: int, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    load_start = loadavg()
    batch_started = time.time()
    batch_started_iso = now_iso()

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        rows = list(pool.map(one_run, range(n)))

    wall_clock_s = round(time.time() - batch_started, 3)
    result = {
        "batch": batch,
        "concurrency": concurrency,
        "n": n,
        "started": batch_started_iso,
        "ended": now_iso(),
        "wall_clock_s": wall_clock_s,          # THE PRIMARY METRIC
        "loadavg_at_start": round(load_start, 3),
        "loadavg_at_end": round(loadavg(), 3),
        "cores": os.cpu_count(),
        "target": TARGET,
        "model_requested": MODEL,
        "run_timeout_s": RUN_TIMEOUT_S,
        "runs": rows,
    }
    path = out_dir / f"{batch}-c{concurrency}.json"
    path.write_text(json.dumps(result, indent=2) + "\n")

    ok = sum(1 for r in rows if r["status"] == "ok")
    bad = [r["status"] for r in rows if r["status"] != "ok"]
    print(f"batch {batch} c={concurrency} n={n}: wall_clock {wall_clock_s}s, "
          f"{ok}/{n} ok, loadavg at start {load_start:.2f}")
    if bad:
        print(f"  NON-OK RUNS (registration: these void the batch): {bad}")
    if load_start > 0.50:
        print(f"  VOID: loadavg at start {load_start:.2f} > 0.50 "
              f"(box was not idle; re-run in the same alternation position)")
    print(f"  -> {path}")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--concurrency", type=int, required=True)
    ap.add_argument("--batch", required=True, help="batch id, e.g. b1")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    run_batch(args.concurrency, args.batch, args.n, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
