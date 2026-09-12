#!/usr/bin/env python3
"""The `extend` branch - building on a skill that already exists.

`author` writes something new and only has to beat a baseline. `extend` changes
something people already rely on, and that is a different obligation: the
incumbent's own evals must STILL PASS.

The rule is asymmetric on purpose.

  A scenario that passed before and fails now is a REGRESSION and it blocks. It
  does not matter how much better the new material is elsewhere - somebody was
  relying on the old behaviour and nobody told them.

  A NEW scenario that fails is ordinary iterate. It was never promised.

  A scenario that failed before and still fails is not a regression either, but
  it is reported, because "we did not fix it" and "we broke it" get confused the
  moment nobody separates them.

Two absences are refused rather than assumed away:

  no stored baseline for the incumbent - then nothing can be called a regression,
  and the honest verdict is that this cannot be extended until its current
  behaviour is measured. Treating an unmeasured incumbent as "no regressions" is
  the flattering reading.

  a scenario present before and missing now - the test was DROPPED, which is how
  a red suite is made green without fixing anything.

    python3 extend_gate.py <before.json> <after.json>

Exit 0 clear · 1 blocked · 2 cannot be decided.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLEAR, BLOCKED, UNDECIDABLE = "clear", "blocked", "undecidable"


def _index(rows: list[dict]) -> dict[str, bool]:
    """scenario -> passed. A row without a result is not a pass."""
    out = {}
    for r in rows or []:
        if not isinstance(r, dict) or not r.get("scenario"):
            continue
        out[r["scenario"]] = (r.get("result") == "pass")
    return out


def compare(before: dict, after: dict) -> dict:
    b, a = _index(before.get("scenarios")), _index(after.get("scenarios"))

    if not b:
        return {"verdict": UNDECIDABLE, "clauses": [], "reason": (
            "no stored baseline for the incumbent, so nothing here can be called a regression. "
            "An unmeasured incumbent read as 'no regressions' is the flattering reading; the "
            "honest one is that this skill cannot be extended until its current behaviour is "
            "measured.")}

    dropped = sorted(set(b) - set(a))
    regressions = sorted(s for s in b if s in a and b[s] and not a[s])
    still_failing = sorted(s for s in b if s in a and not b[s] and not a[s])
    fixed = sorted(s for s in b if s in a and not b[s] and a[s])
    new_fail = sorted(s for s in a if s not in b and not a[s])
    new_pass = sorted(s for s in a if s not in b and a[s])

    clauses = [
        {"clause": "regressions", "verdict": "pass" if not regressions else "fail",
         "detail": "none" if not regressions else
                   f"{len(regressions)} scenario(s) passed before and fail now: {', '.join(regressions[:5])}"},
        {"clause": "dropped-tests", "verdict": "pass" if not dropped else "fail",
         "detail": "none" if not dropped else
                   f"{len(dropped)} scenario(s) present before and missing now: {', '.join(dropped[:5])}"
                   " — a dropped test is how a red suite goes green without a fix"},
        {"clause": "new-failures", "verdict": "pass" if not new_fail else "warn",
         "detail": "none" if not new_fail else
                   f"{len(new_fail)} new scenario(s) fail: {', '.join(new_fail[:5])}"
                   " — ordinary iterate, never promised to anyone"},
        {"clause": "pre-existing-failures", "verdict": "pass" if not still_failing else "warn",
         "detail": "none" if not still_failing else
                   f"{len(still_failing)} still failing: {', '.join(still_failing[:5])}"
                   " — not a regression, reported so 'we did not fix it' is not read as 'we broke it'"},
    ]
    blocked = [c for c in clauses if c["verdict"] == "fail"]
    return {"verdict": BLOCKED if blocked else CLEAR, "clauses": clauses,
            "counts": {"before": len(b), "after": len(a), "regressions": len(regressions),
                       "dropped": len(dropped), "fixed": len(fixed),
                       "new_pass": len(new_pass), "new_fail": len(new_fail)},
            "reason": ("no scenario the incumbent passed has been broken, and none was dropped"
                       if not blocked else
                       "; ".join(c["detail"] for c in blocked))}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = compare(json.loads(Path(a.before).read_text(encoding="utf-8")),
                json.loads(Path(a.after).read_text(encoding="utf-8")))
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"{r['verdict'].upper()}  {r['reason']}")
        for c in r.get("clauses", []):
            print(f"   [{ {'pass':'ok','fail':' E','warn':' w'}[c['verdict']] }] {c['clause']:<22} {c['detail']}")
        if r.get("counts"):
            print(f"   {r['counts']}")
    return {CLEAR: 0, BLOCKED: 1, UNDECIDABLE: 2}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
