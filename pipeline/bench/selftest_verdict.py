#!/usr/bin/env python3
"""Positive controls for the registered decision rule.

Every branch of decide() must be reachable by a constructed case, and each
case must be one the rule REJECTS or ACCEPTS for the stated reason -- not
merely one it survives. A rule with no case that fails it is not a rule.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verdict import decide  # noqa: E402

FAILS = 0


def run(idx, ms, status="ok", model="claude-opus-5", tokens=1000):
    return {"idx": idx, "duration_ms": ms, "status": status, "model": model,
            "models": ["claude-haiku-4-5-20251001", model],
            "tokens": tokens, "started": "t0", "ended": "t1"}


def batch(conc, wall, per_run_ms, n=8, **kw):
    b = {"concurrency": conc, "wall_clock_s": wall, "loadavg_at_start": 0.1,
         "model_requested": "claude-opus-5",
         "runs": [run(i, per_run_ms) for i in range(n)]}
    b.update(kw)
    return b


def check(label, got, want):
    global FAILS
    ok = got == want
    if not ok:
        FAILS += 1
    print(f"{'ok  ' if ok else 'FAIL'} {label}: got {got}, want {want}")


def data(c2, c4, voids=None):
    return {"arms": {2: c2, 4: c4}, "voids": voids or []}


def main() -> int:
    # 1. Clear win: batch wall clock halves, per-run steady, no failures.
    d = decide(data([batch(2, 400, 100000)] * 3, [batch(4, 200, 110000)] * 3))
    check("clear win -> RAISE_TO_4", d["verdict"], "RAISE_TO_4")

    # 2. Clear loss: concurrency 4 is SLOWER. Corroborates cores-2.
    d = decide(data([batch(2, 400, 100000)] * 3, [batch(4, 460, 200000)] * 3))
    check("c4 slower -> KEEP_2", d["verdict"], "KEEP_2")

    # 3. Close band: a 28% gain is NOT enough, and must not read as a wash.
    d = decide(data([batch(2, 400, 100000)] * 3, [batch(4, 288, 100000)] * 3))
    check("ratio 0.72 -> INDETERMINATE", d["verdict"], "INDETERMINATE")
    check("  and says workload too light", "too light" in d["reason"], True)

    # 4. Gain clears, but each run crawls: contention. Guardrail must block.
    d = decide(data([batch(2, 400, 100000)] * 3, [batch(4, 200, 200000)] * 3))
    check("per-run 2.0x -> KEEP_2", d["verdict"], "KEEP_2")
    check("  named the guardrail", "no_per_run_degradation" in d["reason"], True)

    # 5. Gain clears, guardrail clears, one run failed at c=4.
    bad = batch(4, 200, 110000)
    bad["runs"][3] = run(3, 90000, status="timeout")
    d = decide(data([batch(2, 400, 100000)] * 3, [bad, batch(4, 200, 110000),
                                                  batch(4, 200, 110000)]))
    # a timeout voids the batch upstream, so here we assert the pooled-failure
    # branch directly with a status the void filter does not catch
    bad2 = batch(4, 200, 110000)
    bad2["runs"][3]["status"] = "odd"
    d = decide(data([batch(2, 400, 100000)] * 3,
                    [bad2, batch(4, 200, 110000), batch(4, 200, 110000)]))
    check("a non-ok run at c4 -> KEEP_2", d["verdict"], "KEEP_2")
    check("  named the failure check", "no_failures" in d["reason"], True)

    # 6. Sample eaten by voids -> INDETERMINATE, never a verdict on 2 batches.
    d = decide(data([batch(2, 400, 100000)] * 3, [batch(4, 200, 110000)] * 2))
    check("2 valid batches at c4 -> INDETERMINATE", d["verdict"], "INDETERMINATE")

    # 7. No data at all is INDETERMINATE, not a silent KEEP_2.
    d = decide(data([], []))
    check("empty -> INDETERMINATE", d["verdict"], "INDETERMINATE")

    # 8. A won't-happen guard: an arm whose runs are all non-ok yields no
    #    per-run median. That must be INDETERMINATE, not a pass by absence.
    nook = batch(2, 400, 100000)
    for r in nook["runs"]:
        r["status"] = "odd"
    d = decide(data([nook] * 3, [batch(4, 200, 110000)] * 3))
    check("no ok runs in an arm -> INDETERMINATE", d["verdict"], "INDETERMINATE")

    # 9. NEGATIVE CONTROL on the void filter itself: a busy box voids a batch,
    #    which must reduce the sample rather than pass through unnoticed.
    from verdict import batch_void_reasons
    busy = batch(4, 200, 110000, loadavg_at_start=0.9)
    check("busy box voids the batch", bool(batch_void_reasons(busy)), True)
    check("idle box does not", batch_void_reasons(batch(4, 200, 110000)), [])
    wrong = batch(4, 200, 110000)
    wrong["runs"][0]["models"] = ["claude-haiku-4-5-20251001"]
    check("wrong model served voids the batch", bool(batch_void_reasons(wrong)), True)
    aux = batch(4, 200, 110000)
    check("the auxiliary haiku key alone does NOT void", batch_void_reasons(aux), [])
    err = batch(4, 200, 110000)
    err["runs"][0]["api_error_status"] = 429
    check("an API error voids the batch", bool(batch_void_reasons(err)), True)
    nowork = batch(4, 200, 110000)
    nowork["runs"][0]["status"] = "no_work"
    check("a run that skipped the work voids the batch", bool(batch_void_reasons(nowork)), True)
    nousage = batch(4, 200, 110000)
    nousage["runs"][0]["status"] = "no_usage"
    check("a usage-less run voids the batch", bool(batch_void_reasons(nousage)), True)

    print(f"\n{'PASS' if FAILS == 0 else 'FAIL'}: {FAILS} failing check(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
