#!/usr/bin/env python3
"""Which expectations have never separated the two arms?

Not a substitute for a human check and this file says so twice. What it is: a
mechanical test of the failure mode a human check was meant to catch. Three
independent graders in this repo reported the same thing in their own words -
"roughly half are satisfied by reciting a principle rather than obeying it" -
and every time it was found by reading, one set at a time, after the run.

An expectation that both arms meet in every repeat measured nothing. It may still
be a fine thing to ask for; it is simply not carrying any of the verdict, and a
set made mostly of those produces a confident-looking score with almost no
evidence under it.

Read across every blinded grading on disk, joined back through its key, this is
computable. Three buckets:

  discriminating   met by one arm and not the other, at least once
  always-met       met by both arms every time - free, and possibly unfailable
  always-missed    met by neither, ever - either too hard, or badly worded

The last bucket matters as much as the middle one and is easier to miss: an
expectation nothing ever satisfies is not a high bar, it is usually a sentence
nobody can act on.

    python3 expectation_power.py [--root DIR] [--json]
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def collect(root: Path) -> dict:
    stats = defaultdict(lambda: {"with_met": 0, "without_met": 0, "n": 0,
                                 "discriminated": 0, "where": set()})
    pairs = 0
    # What was on disk to read, recorded separately from what was read. A build
    # that graded but wrote its rulings somewhere else looks EXACTLY like a build
    # with no expectations if only the total is reported, and on 2026-09-01 it
    # did: this printed "0 expectations over 0 arm-pairs" for a build carrying 17
    # expectations and 24 graded rows, because the rulings went to events.jsonl
    # and never to grade.r*.json. A measured zero and an unread file are not the
    # same number, and this file exists to catch that class of mistake.
    grade_files = sorted(glob.glob(str(root / "**" / "grade.r*.json"), recursive=True))
    key_files = sorted(glob.glob(str(root / "**" / "key.r*.json"), recursive=True))
    unmatched_keys = [k for k in key_files
                      if not Path(k).with_name(Path(k).name.replace("key.", "grade.")).is_file()]
    for gp in grade_files:
        g = Path(gp)
        kp = g.with_name(g.name.replace("grade.", "key."))
        if not kp.is_file():
            continue
        grade = json.loads(g.read_text(encoding="utf-8"))
        key = json.loads(kp.read_text(encoding="utf-8"))
        unit = g.parent.parent.name
        for q in grade.get("per_question", []):
            qid = str(q.get("id"))
            m = key.get(qid)
            if not m:
                continue
            for r in q.get("rulings", []):
                name = str(r.get("expectation", "")).strip()
                if not name:
                    continue
                per = {}
                for lab in ("A", "B"):
                    per[m[lab]] = str(r.get(lab, "")).strip().lower() == "met"
                if "with" not in per or "without" not in per:
                    continue
                s = stats[(unit, f"Q{qid}", name)]
                s["n"] += 1
                s["with_met"] += per["with"]
                s["without_met"] += per["without"]
                s["discriminated"] += per["with"] != per["without"]
                s["where"].add(unit)
                pairs += 1

    out = {"pairs_examined": pairs, "expectations": len(stats),
           "grade_files_found": len(grade_files), "key_files_found": len(key_files),
           "keys_without_a_grade_file": unmatched_keys,
           "discriminating": [], "always_met": [], "always_missed": [], "other": []}
    for (unit, q, name), s in stats.items():
        row = {"unit": unit, "question": q, "expectation": name, "n": s["n"],
               "with_met": s["with_met"], "without_met": s["without_met"],
               "discriminated": s["discriminated"]}
        if s["discriminated"]:
            out["discriminating"].append(row)
        elif s["with_met"] == s["n"] and s["without_met"] == s["n"]:
            out["always_met"].append(row)
        elif s["with_met"] == 0 and s["without_met"] == 0:
            out["always_missed"].append(row)
        else:
            out["other"].append(row)
    for k in ("discriminating", "always_met", "always_missed", "other"):
        out[k].sort(key=lambda r: (r["unit"], r["question"]))
    n = out["expectations"]
    out["carrying_share"] = (len(out["discriminating"]) / n) if n else None

    # Three verdicts, never two. Nothing read is INDETERMINATE, never a zero.
    if pairs:
        out["verdict"] = "measured"
        out["could_not_read"] = None
    else:
        out["verdict"] = "indeterminate"
        why = []
        if not grade_files:
            why.append(f"no grade.r*.json anywhere under {root}")
        if unmatched_keys:
            why.append(f"{len(unmatched_keys)} blinding key(s) with no matching grade file "
                       f"beside them ({', '.join(Path(k).name for k in unmatched_keys[:3])}) - "
                       f"the signature of a build that graded and wrote the rulings elsewhere")
        if grade_files and not unmatched_keys:
            why.append("grade files were found but carried no arm-paired rulings")
        out["could_not_read"] = why
    out["not_a_human_check"] = (
        "This measures whether an expectation MOVED, not whether it was RIGHT. An expectation both "
        "arms always meet may be exactly the thing you want to demand; it is simply not carrying "
        "any of this verdict. Only a person can say whether the demands are the right demands, and "
        "that check remains open.")
    return out


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--root", default=str(REPO / "pipeline"))
    a.add_argument("--json", action="store_true")
    args = a.parse_args()
    r = collect(Path(args.root))
    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0 if r["verdict"] == "measured" else 2
    if r["verdict"] == "indeterminate":
        print("INDETERMINATE — nothing was read, so there is no share to report.")
        for w in r["could_not_read"]:
            print(f"   [?] {w}")
        print("\nA zero here would have meant 'no expectation carried the verdict'. "
              "That is a different\nstatement from 'no rulings were found', and only "
              "one of them is true.")
        return 2
    share = r["carrying_share"]
    print(f"{r['expectations']} expectations over {r['pairs_examined']} arm-pairs · "
          f"{len(r['discriminating'])} carried the verdict"
          + (f" ({share:.0%})" if share is not None else ""))
    for bucket, label in [("always_met", "ALWAYS MET by both arms — free"),
                          ("always_missed", "ALWAYS MISSED by both — usually unactionable, not hard")]:
        if r[bucket]:
            print(f"\n{label}: {len(r[bucket])}")
            for row in r[bucket][:10]:
                print(f"   {row['unit'][:22]:<22} {row['question']:<4} {row['expectation'][:70]}")
    print(f"\n{r['not_a_human_check']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
