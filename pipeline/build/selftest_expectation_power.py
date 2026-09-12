#!/usr/bin/env python3
"""Positive controls for the expectation-power query.

The load-bearing case is the one it got wrong: a build that graded, and wrote
its rulings somewhere other than grade.r*.json, must come back INDETERMINATE
with the reason - never as a measured zero.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from expectation_power import collect  # noqa: E402

FAILS = 0


def check(ok, label, detail=""):
    global FAILS
    if not ok:
        FAILS += 1
    print(f"{'ok  ' if ok else 'FAIL'} {label}{('  — ' + str(detail)) if detail and not ok else ''}")


def write(d: Path, rulings, key=None):
    d.mkdir(parents=True, exist_ok=True)
    (d / "key.r1.json").write_text(json.dumps(key or {"1": {"A": "with", "B": "without"}}))
    if rulings is not None:
        (d / "grade.r1.json").write_text(json.dumps(
            {"per_question": [{"id": 1, "rulings": rulings}]}))


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        # 1. THE DEFECT. Keys on disk, no grade files: the build graded and put
        #    the rulings elsewhere. This printed "0 expectations over 0 pairs".
        a = tmp / "a" / "u" / "measure"
        write(a, None)
        r = collect(tmp / "a")
        check(r["verdict"] == "indeterminate", "keys with no grade files -> INDETERMINATE",
              r["verdict"])
        check(r["carrying_share"] is None, "and the share is null, not zero",
              r["carrying_share"])
        check(any("no matching grade file" in w for w in r["could_not_read"]),
              "and it names the orphaned key, which is the whole diagnostic",
              r["could_not_read"])
        check(len(r["keys_without_a_grade_file"]) == 1, "the orphan is counted")

        # 2. Nothing on disk at all is also indeterminate, for its own reason.
        (tmp / "empty").mkdir()
        r = collect(tmp / "empty")
        check(r["verdict"] == "indeterminate", "an empty tree -> INDETERMINATE")
        check(any("no grade.r*.json" in w for w in r["could_not_read"]),
              "and says so", r["could_not_read"])

        # 3. A real discriminating expectation.
        b = tmp / "b" / "u" / "measure"
        write(b, [{"expectation": "E1", "A": "met", "B": "not met"}])
        r = collect(tmp / "b")
        check(r["verdict"] == "measured", "rulings present -> measured", r["verdict"])
        check(len(r["discriminating"]) == 1, "an expectation met by one arm only discriminates")
        check(r["carrying_share"] == 1.0, "and the share is 1.0", r["carrying_share"])

        # 4. NEGATIVE CONTROL: an expectation both arms meet carries nothing, and
        #    a REAL zero share must still be reportable as a measurement.
        c = tmp / "c" / "u" / "measure"
        write(c, [{"expectation": "E1", "A": "met", "B": "met"}])
        r = collect(tmp / "c")
        check(r["verdict"] == "measured", "both arms met is a MEASUREMENT, not a read failure",
              r["verdict"])
        check(r["carrying_share"] == 0.0,
              "and a genuine zero share is reported as zero, not suppressed",
              r["carrying_share"])
        check(len(r["always_met"]) == 1, "it lands in always-met")

        # 5. Neither arm ever meets it: usually unactionable, not hard.
        e = tmp / "e" / "u" / "measure"
        write(e, [{"expectation": "E1", "A": "not met", "B": "not met"}])
        r = collect(tmp / "e")
        check(len(r["always_missed"]) == 1, "an expectation nobody meets lands in always-missed")

        # 6. A grade file whose key does not name both arms yields no pair, and
        #    that must read as unread rather than as a zero.
        f = tmp / "f" / "u" / "measure"
        write(f, [{"expectation": "E1", "A": "met", "B": "not met"}],
              key={"1": {"A": "with", "B": "incumbent"}})
        r = collect(tmp / "f")
        check(r["verdict"] == "indeterminate",
              "a key naming no with/without pair reads as unread, not as zero", r["verdict"])

    print(f"\n{'PASS' if FAILS == 0 else 'FAIL'}: {FAILS} failing check(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
