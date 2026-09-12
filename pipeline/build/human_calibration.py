#!/usr/bin/env python3
"""Measure OUR instrument against a person - the one calibration never done.

Every verdict in this system comes from code or from an agent. The agents grade
the skills, other agents grade the graders, and the code gates them all. Nothing
has ever been checked against a human, so the whole stack could be internally
consistent and jointly wrong, and there would be no signal.

This builds the smallest thing that would show it: a sheet of already-graded
cells, stripped of their verdicts, for a person to rule on blind. Then it
measures agreement.

Three rules it enforces, because they are what make the answer worth having:

  The person is BLIND. No agent verdict, no arm label, no evidence quote. Seeing
  the machine's answer first is the single easiest way to get agreement that
  measures nothing.

  The sample is DRAWN, not chosen. Choosing which cells to hand over is choosing
  the result. It samples by seed and reports it - but only from cells where some
  expectation actually moved, because a cell both arms cleared on every point
  cannot be agreed or disagreed with.

  Disagreement is not an error to explain away. A cell where the person and the
  grader differ is the finding; the report keeps both and never reconciles them
  automatically.

    python3 human_calibration.py sheet <rows.json> --n 10 --seed 7 --out sheet.md
    python3 human_calibration.py score <sheet.answers.json> <rows.json>
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path


def build_sheet(rows: list[dict], n: int, seed: int, *, runs_dir: Path | None = None,
                evals: dict | None = None) -> tuple[str, dict]:
    """The sheet must carry what a person needs to RULE, minus what would bias them.

    Shown: the question, the expectations, and the answer text.
    Withheld: which arm produced it, and what the machine decided.

    The first version of this function showed only "4 of 4 expectations met" and
    withheld the answer. That is not a calibration - a person cannot rule on
    material they cannot see, so it would have measured whether they could guess
    the machine's number. Caught by reading the sheet it produced.
    """
    cells = [r for r in rows if isinstance(r, dict) and r.get("test") and r.get("arm")]
    if not cells:
        raise SystemExit("no gradable cells in that file")

    answers: dict[tuple[str, str, int], str] = {}
    if runs_dir:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals" / "harness"))
        import blind
        for f in Path(runs_dir).glob("*.r?.md"):
            # "without" also startswith "with" - the arm is the part before the
            # first dot, matched whole. Getting this wrong silently files every
            # baseline answer under the skill arm, which would invert the
            # calibration rather than break it.
            arm = f.name.split(".")[0]
            if arm not in {"with", "without"}:
                continue
            rep = int(f.stem.split(".r")[-1])
            for qid, text in blind.sections(f).items():
                answers[(f"Q{qid}", arm, rep)] = text
    exp = {f"Q{e['id']}": e for e in (evals or {}).get("evals", [])}

    missing = [c for c in cells if (c["test"], c["arm"], c.get("repeat")) not in answers]
    if runs_dir and missing:
        raise SystemExit(f"{len(missing)} sampled cell(s) have no answer text on disk — refusing to "
                         f"build a sheet a person cannot rule on")

    # Sample from cells where at least one expectation ever MOVED. Uniform
    # sampling put a cell in front of a person where nothing could discriminate
    # - 3 of 3 expectations were met by both arms in every repeat - so no answer
    # they gave could have agreed or disagreed with anything. Measured
    # 2026-09-01: only 27 percent of expectations carried any verdict, so most
    # of a uniform sample is unrulable by construction.
    #
    # This narrows what the calibration can find. It checks the grader where the
    # grader made a call, and says nothing about the cells nobody had to decide.
    live = [c for c in cells if c.get("discriminating")] or cells
    rnd = random.Random(seed)
    sample = rnd.sample(live, min(n, len(live)))
    key, out = {}, [
        "# Blind calibration sheet", "",
        f"Sampled with seed {seed} from {len(cells)} graded cells. **Do not read the build's",
        "grading before answering** — agreement measured after seeing the machine's answer",
        "measures nothing.",
        "",
        "For each cell: did the answer meet EVERY listed expectation? Answer `yes`, `no`, or",
        "`unsure`. Unsure is a real answer and is scored as its own category, never folded into",
        "either side.",
        "",
        "Withheld on purpose: which arm produced each answer, and what the grader decided.",
        "",
        "```json",
        json.dumps({f"C{i+1}": "yes|no|unsure" for i in range(len(sample))}, indent=2),
        "```", "",
    ]
    for i, c in enumerate(sample, 1):
        cid = f"C{i}"
        key[cid] = {"test": c["test"], "arm": c["arm"], "repeat": c.get("repeat"),
                    "machine": bool(c.get("correct"))}
        e = exp.get(c["test"])
        out += [f"---", "", f"## {cid}", ""]
        if e:
            out += [f"**The request.** {e['prompt']}", "", "**It had to meet all of these:**", ""]
            out += [f"- {x}" for x in e.get("expectations", [])]
            out += [""]
        body = answers.get((c["test"], c["arm"], c.get("repeat")))
        out += ["**The answer:**", "", body if body else "_(answer text not available)_", ""]
    return "\n".join(out), {"seed": seed, "cells": key}


def score(answers: dict, key: dict) -> dict:
    k = key["cells"]
    agree, disagree, unsure = [], [], []
    for cid, human in answers.items():
        if cid not in k:
            continue
        h = str(human).strip().lower()
        m = k[cid]["machine"]
        if h == "unsure":
            unsure.append(cid)
        elif (h == "yes") == m:
            agree.append(cid)
        else:
            disagree.append({"cell": cid, "human": h, "machine": "yes" if m else "no",
                             **{x: k[cid][x] for x in ("test", "arm", "repeat")}})
    n = len(agree) + len(disagree)
    return {
        "seed": key["seed"], "n_ruled": n, "n_unsure": len(unsure),
        "agreement": (len(agree) / n) if n else None,
        "disagreements": disagree,
        "reading": ("Agreement is not a score to maximise. A disagreement is the finding: it says "
                    "either the grader is wrong or the expectation was written so that a careful "
                    "person reads it differently, and those need separate fixes. Nothing here "
                    "reconciles them automatically."),
        "caveat": ("n is small by construction. This detects a stack that is jointly wrong; it "
                   "cannot certify one that is jointly right."),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet"); s.add_argument("rows"); s.add_argument("--n", type=int, default=10)
    s.add_argument("--seed", type=int, default=7); s.add_argument("--out", required=True)
    s.add_argument("--runs", help="directory of with/without run files, so the sheet carries the answers")
    s.add_argument("--evals", help="evals.json, so the sheet carries the question and expectations")
    c = sub.add_parser("score"); c.add_argument("answers"); c.add_argument("key")
    a = ap.parse_args()

    if a.cmd == "sheet":
        raw = json.loads(Path(a.rows).read_text(encoding="utf-8"))
        rows = raw.get("paired") if isinstance(raw, dict) else raw
        ev = json.loads(Path(a.evals).read_text(encoding="utf-8")) if a.evals else None
        sheet, key = build_sheet(rows or [], a.n, a.seed,
                                 runs_dir=Path(a.runs) if a.runs else None, evals=ev)
        Path(a.out).write_text(sheet, encoding="utf-8")
        kp = Path(a.out).with_suffix(".key.json")
        kp.write_text(json.dumps(key, indent=2), encoding="utf-8")
        print(f"sheet: {a.out}\nkey (do NOT open before answering): {kp}")
        return 0

    r = score(json.loads(Path(a.answers).read_text(encoding="utf-8")),
              json.loads(Path(a.key).read_text(encoding="utf-8")))
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
