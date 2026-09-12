#!/usr/bin/env python3
"""Un-blind a grader's JSON, and turn it into rows the verdict function can read.

The grader ruled on answers labelled A and B. This maps them back through the key
it never saw, and emits:

  * one `run_paired` row per (question, repeat, arm) - {test, repeat, arm, correct}
  * one `evals.jsonl` row per scenario, in the shape DATA.md fixes

`correct` is all-expectations-met. Not most, not the important ones: an
expectation that was allowed to fail quietly is one nobody has to write carefully.
An `unclear` ruling is NOT met - a check that could not be made is not a pass, the
same rule the two contract checkers run on.

    python3 score.py <run-dir> <skill> --all      # merges every repeat found
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2] / "skills"
RUNS = Path("runs")


def load(skill: str, repeat: int) -> tuple[dict, dict]:
    g = json.loads((RUNS / f"{skill}.grade.r{repeat}.json").read_text(encoding="utf-8"))
    k = json.loads((RUNS / f"{skill}.key.r{repeat}.json").read_text(encoding="utf-8"))
    return g, k


def rows_for(skill: str, repeat: int) -> tuple[list[dict], list[dict]]:
    grade, key = load(skill, repeat)
    paired, scenarios = [], []
    for q in grade["per_question"]:
        qid = str(q["id"])
        mapping = key[qid]                      # {"A": "with"|"without", "B": ...}
        per_arm = {"with": [], "without": []}
        for r in q["rulings"]:
            for label in ("A", "B"):
                per_arm[mapping[label]].append(str(r.get(label, "")).strip().lower() == "met")
        for arm, met in per_arm.items():
            paired.append({"test": f"Q{qid}", "repeat": repeat, "arm": arm,
                           "correct": bool(met) and all(met),
                           "n_expectations": len(met), "n_met": sum(met),
                           "tokens": None, "tool_calls": None})
        w = next(r for r in paired if r["test"] == f"Q{qid}" and r["arm"] == "with"
                 and r["repeat"] == repeat)
        o = next(r for r in paired if r["test"] == f"Q{qid}" and r["arm"] == "without"
                 and r["repeat"] == repeat)
        scenarios.append({
            "ts": None, "talent": skill, "scenario": f"Q{qid}", "kind": "normal",
            "baseline": "pass" if o["correct"] else "miss",
            "with": "pass" if w["correct"] else "miss",
            "result": "pass" if (w["correct"] and not o["correct"]) else
                      ("pass" if w["correct"] and o["correct"] else "fail"),
            "repeat": repeat, "backfill": False,
            "expectation_critique": q.get("expectation_critique"),
        })
    return paired, scenarios


def main() -> int:
    global RUNS
    RUNS = Path(sys.argv[1]) / "runs"
    skill = sys.argv[2]
    reps = ([int(sys.argv[3])] if sys.argv[3] != "--all"
            else sorted(int(p.stem.split(".r")[-1]) for p in RUNS.glob(f"{skill}.grade.r*.json")))
    paired, scen = [], []
    for r in reps:
        p, s = rows_for(skill, r)
        paired += p
        scen += s
    out = RUNS / f"{skill}.rows.json"
    out.write_text(json.dumps({"skill": skill, "repeats": reps, "paired": paired,
                               "scenarios": scen}, indent=2), encoding="utf-8")
    for r in reps:
        w = [x for x in paired if x["arm"] == "with" and x["repeat"] == r]
        o = [x for x in paired if x["arm"] == "without" and x["repeat"] == r]
        print(f"r{r}: with {sum(x['correct'] for x in w)}/{len(w)} · "
              f"without {sum(x['correct'] for x in o)}/{len(o)}")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
