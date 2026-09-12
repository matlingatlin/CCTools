#!/usr/bin/env python3
"""Controls for the extend gate.

The whole file exists to make one thing impossible: improving a skill on one axis
while quietly breaking what someone already relied on. So the controls are mostly
about what must NOT be forgiven.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extend_gate as eg  # noqa: E402

R: list[tuple[bool, str]] = []


def check(ok, label, detail=""):
    R.append((ok, f"{label}{'  — ' + detail if detail and not ok else ''}"))


def suite(**kw):
    return {"scenarios": [{"scenario": k, "result": "pass" if v else "fail"} for k, v in kw.items()]}


def main() -> int:
    before = suite(Q1=True, Q2=True, Q3=False)

    r = eg.compare(before, suite(Q1=True, Q2=True, Q3=True))
    check(r["verdict"] == eg.CLEAR, "fixing a failure while keeping the rest is clear", r["reason"])

    r = eg.compare(before, suite(Q1=True, Q2=False, Q3=False))
    check(r["verdict"] == eg.BLOCKED and r["counts"]["regressions"] == 1,
          "a scenario that passed before and fails now BLOCKS", r["reason"])

    r = eg.compare(before, suite(Q1=True, Q2=False, Q3=True, Q4=True, Q5=True))
    check(r["verdict"] == eg.BLOCKED,
          "and it still blocks when the change wins everywhere else — somebody relied on that one",
          r["reason"])

    r = eg.compare(before, suite(Q1=True, Q2=True))
    check(r["verdict"] == eg.BLOCKED and r["counts"]["dropped"] == 1,
          "dropping a scenario blocks — that is how a red suite goes green without a fix", r["reason"])

    r = eg.compare(before, suite(Q1=True, Q2=True, Q3=False, Q4=False))
    check(r["verdict"] == eg.CLEAR and any(c["clause"] == "new-failures" and c["verdict"] == "warn"
                                           for c in r["clauses"]),
          "a NEW scenario failing is ordinary iterate, not a regression", r["reason"])

    r = eg.compare(before, suite(Q1=True, Q2=True, Q3=False))
    still = next(c for c in r["clauses"] if c["clause"] == "pre-existing-failures")
    check(r["verdict"] == eg.CLEAR and still["verdict"] == "warn",
          "a pre-existing failure is not a regression, and is still reported")
    check("we broke it" in still["detail"],
          "and the report separates 'we did not fix it' from 'we broke it'")

    r = eg.compare({"scenarios": []}, suite(Q1=True))
    check(r["verdict"] == eg.UNDECIDABLE and "flattering" in r["reason"],
          "an unmeasured incumbent is UNDECIDABLE, never 'no regressions'", r["verdict"])

    r = eg.compare(before, {"scenarios": [{"scenario": "Q1"}, {"scenario": "Q2", "result": "pass"},
                                          {"scenario": "Q3", "result": "fail"}]})
    check(r["verdict"] == eg.BLOCKED,
          "a scenario with no recorded result is not a pass, so it reads as a regression")

    bad = [m for ok, m in R if not ok]
    for ok, m in R:
        if "-v" in sys.argv or not ok:
            print(f"{'ok   ' if ok else 'FAIL '} {m}")
    print(f"\n{len(R) - len(bad)}/{len(R)} controls behaved")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
