#!/usr/bin/env python3
"""Controls for the un-blinding step.

This is the one place in the harness where a bug inverts the conclusion instead of
breaking it. If A and B are mapped back the wrong way the run still completes, the
numbers still look plausible, and the losing arm is reported as the winner. Nothing
downstream can detect it.

So: a synthetic grading where the answer is known by construction, run through the
real key, plus a mutant where the key is swapped - which must produce the opposite
verdict, not the same one.

    python3 selftest_score.py [-v]
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blind  # noqa: E402
import score  # noqa: E402

R: list[tuple[bool, str]] = []


def check(ok, label, detail=""):
    R.append((ok, f"{label}{'  — ' + detail if detail and not ok else ''}"))


def synth(tmp: Path, *, with_wins: bool, swap_key: bool):
    """A grading where the `with` arm meets everything and `without` meets nothing."""
    key = {"1": {"A": "with", "B": "without"}, "2": {"A": "without", "B": "with"}}
    if swap_key:
        key = {q: {"A": v["B"], "B": v["A"]} for q, v in key.items()}
    per_q = []
    for qid in ("1", "2"):
        # rule by ARM, then place under the label the true key assigns
        true = {"1": {"A": "with", "B": "without"}, "2": {"A": "without", "B": "with"}}[qid]
        verdict = {"with": "met" if with_wins else "not met", "without": "not met"}
        per_q.append({"id": int(qid), "rulings": [
            {"expectation": "e1",
             "A": verdict[true["A"]], "A_evidence": "x",
             "B": verdict[true["B"]], "B_evidence": "y"}]})
    (tmp / "s.grade.r1.json").write_text(json.dumps({"per_question": per_q, "overall": ""}))
    (tmp / "s.key.r1.json").write_text(json.dumps(key))


def run(tmp: Path):
    score.RUNS = tmp
    paired, _ = score.rows_for("s", 1)
    w = [r for r in paired if r["arm"] == "with"]
    o = [r for r in paired if r["arm"] == "without"]
    return sum(r["correct"] for r in w), sum(r["correct"] for r in o)


def main() -> int:
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)

        synth(tmp, with_wins=True, swap_key=False)
        w, o = run(tmp)
        check((w, o) == (2, 0), "the correct key attributes the wins to the arm that earned them",
              f"with={w} without={o}")

        synth(tmp, with_wins=True, swap_key=True)
        w2, o2 = run(tmp)
        check((w2, o2) == (0, 2), "a swapped key INVERTS the result, so the control can see it",
              f"with={w2} without={o2}")
        check((w, o) != (w2, o2), "the two keys do not produce the same answer — "
                                  "a harness where they did could not detect the bug at all")

        synth(tmp, with_wins=False, swap_key=False)
        w3, o3 = run(tmp)
        check((w3, o3) == (0, 0), "no arm wins when nothing was met", f"with={w3} without={o3}")

        # unclear is not a pass
        g = json.loads((tmp / "s.grade.r1.json").read_text())
        g["per_question"][0]["rulings"][0]["A"] = "unclear"
        (tmp / "s.grade.r1.json").write_text(json.dumps(g))
        paired, _ = score.rows_for("s", 1)
        check(not any(r["correct"] for r in paired), "an unclear ruling is not a pass")

        # all-expectations, not most
        g["per_question"][0]["rulings"] = [
            {"expectation": "e1", "A": "met", "B": "not met"},
            {"expectation": "e2", "A": "not met", "B": "not met"}]
        (tmp / "s.grade.r1.json").write_text(json.dumps(g))
        paired, _ = score.rows_for("s", 1)
        q1 = [r for r in paired if r["test"] == "Q1"]
        check(all(not r["correct"] for r in q1) and any(r["n_met"] == 1 for r in q1),
              "one expectation of two met is not correct, and the partial count is kept")

        # the blinding key itself must vary, or blinding buys nothing
        flips = {blind.coin("x", 1, q) for q in range(1, 9)}
        check(len(flips) == 2, "the blinding coin is not constant across questions")

    bad = [m for ok, m in R if not ok]
    for ok, m in R:
        if "-v" in sys.argv or not ok:
            print(f"{'ok   ' if ok else 'FAIL '} {m}")
    print(f"\n{len(R) - len(bad)}/{len(R)} controls behaved")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
