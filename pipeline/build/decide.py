#!/usr/bin/env python3
"""Phase 8.1 — the verdict, against the threshold the package preregistered.

Code, not judgement, and deliberately so. The threshold was written before any
number existed; letting a model read the results and then interpret the rule
hands back exactly the freedom the preregistration was there to remove. In this
repo a conclusion was once drawn on n=1 and four documents were rewritten on it.

WHICH rule is evaluated:

  threshold_rule present   its parameters are used
  prose == the contract's default_rule   the default parameters are used
  otherwise                UNDECIDABLE, and it says why

The third branch is not a failure of this file. A preregistration that no code
can evaluate has to be read by whoever wants the answer, and if they read it
after seeing the results the registration bought nothing. The build record keeps
the refusal so the next package carries a structured rule.

The default rule, from the contract's acceptance block:

    Across k >= 2 repeats: zero regressions on correctness, no more than 20
    percent worse on tokens or tool calls, and at least one test where the skill
    wins with the win surviving the repeat.

Three things it will not do:

  * A missing measurement is never a pass. A null token count makes the cost
    axis INDETERMINATE and the verdict undecidable - it does not quietly clear.
  * A measured zero is not a missing measurement. 0 tool calls is a result.
  * One repeat never decides. MIN_ITERS_FOR_VERDICT = 2 in CONSTANTS.md: one
    iteration never earns a verdict, however extreme. And the clean-baseline case
    is exactly where a single run cannot tell a tie from a small regression.

A build opened in fast mode (record.json's mode) ran the with-arm only, so
there is no baseline and nothing was beaten. Its best verdict is fast_pass -
every with-arm run correct across the repeats - and it is never ship, whatever
the rows contain.

    python3 pipeline/build/decide.py <build-dir>
    python3 pipeline/build/decide.py <build-dir> --json

Exit 0 = ship. 1 = iterate or abandon. 2 = undecidable. 3 = fast_pass.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import record as rec  # noqa: E402

CONTRACT = rec.REPO / "pipeline" / "contracts" / "skill.contract.json"

SHIP, ITERATE, ABANDON, UNDECIDABLE = "ship", "iterate", "abandon", "undecidable"
CANDIDATE = "candidate"   # 4.0.0: filled, code-checked, reviewed once, rewritten once; measured at promotion
FAST_PASS = "fast_pass"   # fast mode's ceiling: passed its own tests, beat nothing

DEFAULTS = {
    "min_repeats": 2,          # CONSTANTS.md MIN_ITERS_FOR_VERDICT
    "cost_tolerance": 0.20,    # no more than 20 percent worse
    "cost_axes": ["tokens", "tool_calls"],
    "require_win": True,       # at least one test the skill wins
    "win_must_survive": True,  # ...in every repeat, not one of them
    "win_axes": ["correctness", "shape"],  # a win on EITHER satisfies the clause
    "max_repair_loops": 3,     # beyond this, iterate becomes abandon
    # The spec's own table (SKILL-BUILDER-SPEC section 2, phase 2): baseline
    # FAILS on every task -> "1 suffices"; passes unevenly or cleanly -> >= 2.
    # Read off the 2.3 gap_verdict event's probe_outcome. Any outcome not in the
    # map, or no event, keeps min_repeats.
    "repeats_by_probe": {"fails": 1, "uneven": 2, "clean": 2, "refuted": 2},
    # The probe already ran the representative tasks without the skill, in
    # fresh sessions, fixture as a path - the without-arm's definition. Its rows
    # count for the correctness clauses; never for cost, which needs the same
    # turn and the same load as the with-arm.
    "probe_rows_for_correctness": True,
}


def _norm(s) -> str:
    return " ".join(str(s or "").lower().split())


def resolve_rule(head: dict) -> tuple[dict | None, str]:
    """Which rule applies, and the sentence that says why."""
    pkg = head.get("package", {})
    supplied = pkg.get("threshold_rule")
    if isinstance(supplied, dict):
        rule = dict(DEFAULTS)
        rule.update(supplied)
        return rule, "the package supplied a structured threshold_rule"
    acc = json.loads(CONTRACT.read_text(encoding="utf-8"))["acceptance"]
    default_prose = acc["default_rule"]
    if _norm(pkg.get("threshold")) == _norm(default_prose):
        return dict(DEFAULTS), "the preregistered prose is the contract's default rule verbatim"
    # A phrasing the contract registers as equivalent, WITH its parameter mapping
    # written beside it (acceptance.equivalent_prose). Registered as data so the
    # equivalence is a claim someone checked, not a guess made after the numbers.
    for eq in acc.get("equivalent_prose") or []:
        if isinstance(eq, dict) and _norm(pkg.get("threshold")) == _norm(eq.get("prose")):
            return dict(DEFAULTS), ("the preregistered prose is a phrasing the contract registers as "
                                    "equivalent to the default rule: " + str(eq.get("maps_to"))[:120])
    return None, ("the preregistered threshold is prose that is not the contract's default rule, "
                  "and no threshold_rule was supplied — no code can evaluate it. Read it yourself, "
                  "and note that reading it now means reading it after the results")


# --- the measurement ---------------------------------------------------------

def rows_of(root: Path, rule: dict | None = None) -> list[dict]:
    """run_paired rows, plus the probe's rows for correctness when the rule allows.

    A probe row is a probe_gap event row carrying test, repeat, arm="without"
    and correct. It is tagged source="probe" here so evaluate() can keep it out
    of every cost clause.
    """
    rule = rule or DEFAULTS
    ev = rec.last(root, "run_paired")
    rows = [dict(r, source=r.get("source") or "paired") for r in (ev.get("rows") or [])] if ev else []
    if rule.get("probe_rows_for_correctness"):
        pe = rec.last(root, "probe_gap")
        for r in (pe.get("rows") or []) if pe else []:
            if r.get("arm", "without") == "without" and "test" in r and "repeat" in r:
                rows.append(dict(r, arm="without", source="probe"))
    return rows


def resolve_repeats(root: Path, rule: dict) -> tuple[int, str | None]:
    """min_repeats for THIS build, from the gap verdict the probe produced."""
    ev = rec.last(root, "gap_verdict")
    outcome = (ev.get("probe_outcome") or ev.get("classification")) if ev else None
    table = rule.get("repeats_by_probe") or {}
    if outcome in table:
        return int(table[outcome]), outcome
    return int(rule["min_repeats"]), outcome


def _by_test(rows: list[dict]) -> dict[str, dict[int, dict[str, dict]]]:
    out: dict = {}
    for r in rows:
        out.setdefault(r["test"], {}).setdefault(int(r["repeat"]), {})[r["arm"]] = r
    return out


def _mean(vals: list) -> float | None:
    clean = [v for v in vals if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return sum(clean) / len(clean) if len(clean) == len(vals) and clean else None


def evaluate(rows: list[dict], rule: dict) -> dict:
    """Returns the finding per clause. A clause is pass / fail / indeterminate."""
    out = {"clauses": [], "n_tests": 0, "n_rows": len(rows)}
    if not rows:
        out["clauses"].append({"clause": "data", "verdict": "indeterminate",
                               "detail": "no run_paired event in the record"})
        return out

    tests = _by_test(rows)
    out["n_tests"] = len(tests)

    # k >= 2 repeats, both arms, every test
    thin = []
    for t, reps in tests.items():
        full = [k for k, arms in reps.items() if {"with", "without"} <= set(arms)]
        if len(full) < rule["min_repeats"]:
            thin.append(f"{t}: {len(full)} paired repeat(s)")
    out["clauses"].append(
        {"clause": "repeats", "verdict": "pass" if not thin else "indeterminate",
         "detail": f"min {rule['min_repeats']} paired repeats per test"
                   + ("" if not thin else " — " + "; ".join(thin[:4]))})

    # zero correctness regressions
    regressions, unknown = [], []
    for t, reps in tests.items():
        for k, arms in reps.items():
            w, o = arms.get("with"), arms.get("without")
            if not w or not o:
                continue
            if w.get("correct") is None or o.get("correct") is None:
                unknown.append(f"{t} r{k}")
            elif o.get("correct") and not w.get("correct"):
                regressions.append(f"{t} r{k}")
    if unknown:
        out["clauses"].append({"clause": "no_regression", "verdict": "indeterminate",
                               "detail": f"correctness not recorded for {', '.join(unknown[:4])}"})
    else:
        out["clauses"].append(
            {"clause": "no_regression", "verdict": "pass" if not regressions else "fail",
             "detail": "none" if not regressions
                       else f"the skill lost a correct baseline on {', '.join(regressions[:4])}"})

    # cost within tolerance - paired rows only. A probe row was run in another
    # turn under another load; its tokens say nothing about the with-arm's.
    cost_rows = [r for r in rows if r.get("source", "paired") != "probe"]
    for axis in rule["cost_axes"]:
        w = _mean([r.get(axis) for r in cost_rows if r["arm"] == "with"])
        o = _mean([r.get(axis) for r in cost_rows if r["arm"] == "without"])
        if w is None or o is None:
            out["clauses"].append({"clause": f"cost:{axis}", "verdict": "indeterminate",
                                   "detail": f"{axis} not recorded on every run — a missing "
                                             f"measurement is not a pass"})
            continue
        if o == 0:
            ok, det = w == 0, f"baseline mean 0, skill mean {w}"
        else:
            ratio = w / o
            ok = ratio <= 1 + rule["cost_tolerance"]
            det = f"{w:.1f} vs {o:.1f} = {ratio:.2f}x (cap {1 + rule['cost_tolerance']:.2f}x)"
        out["clauses"].append({"clause": f"cost:{axis}",
                               "verdict": "pass" if ok else "fail", "detail": det})

    # at least one surviving win, on ANY of the rule's axes
    #
    # Correctness alone cannot express the case the contract's probe_never_gates
    # clause is about: a run where both arms are right on every test and the skill
    # earned its place by making the OUTPUT SHAPE right. Scored on correctness only,
    # that run is a tie and the skill is discarded for a reason nobody measured.
    if rule["require_win"]:
        axes = {
            "correctness": lambda a: (a["with"].get("correct"), a["without"].get("correct")),
            "shape": lambda a: (a["with"].get("shape_ok"), a["without"].get("shape_ok")),
        }
        wins, fragile = [], []
        for t, reps in tests.items():
            paired = [a for a in reps.values() if {"with", "without"} <= set(a)]
            if not paired:
                continue
            for axis in rule["win_axes"]:
                read = axes.get(axis)
                if read is None:
                    continue
                # a win needs BOTH sides recorded; an unrecorded axis is not a win
                scored = [a for a in paired if all(v is not None for v in read(a))]
                if len(scored) < len(paired):
                    continue
                won = [a for a in scored if read(a)[0] and not read(a)[1]]
                if not won:
                    continue
                if not rule["win_must_survive"] or len(won) == len(scored):
                    wins.append(f"{t} ({axis})")
                    break
                fragile.append(f"{t} on {axis} ({len(won)}/{len(scored)} repeats)")
        detail = ("won: " + ", ".join(wins)) if wins else (
            "no test where the skill wins on " + " or ".join(rule["win_axes"]))
        if not wins and fragile:
            detail += " — did not survive the repeat: " + "; ".join(fragile[:4])
        out["clauses"].append({"clause": "win", "verdict": "pass" if wins else "fail",
                               "detail": detail})
    return out


def decide_candidate(root: Path) -> dict:
    """Candidate mode (4.0.0). No measurement: the verdict says the artefact is
    filled, green under the code checker, read once by the reviewer, and
    rewritten once if the review was red. Nothing here claims it beats a
    baseline - that is the promote mode's verdict."""
    missing = rec.chain_gate(root, version=1)
    if missing:
        names = ", ".join(f"{m['id']} {m['fn']}" for m in missing[:5])
        return {"verdict": UNDECIDABLE, "rule": None, "clauses": [], "missing_phases": [m["id"] for m in missing],
                "reason": f"{len(missing)} phase(s) left no event: {names}"}
    ev = rec.events(root)
    checks = [e for e in ev if e.get("function") == "validate_artifact" and not e.get("skipped") and not e.get("self_sweep")]
    reviews = [e for e in ev if e.get("function") == "review_artifact" and not e.get("skipped")]
    clauses = []
    last_check = checks[-1] if checks else None
    green = last_check is not None and last_check.get("errors") == 0
    clauses.append({"clause": "code_check", "verdict": "pass" if green else ("indeterminate" if last_check is None or "errors" not in last_check else "fail"),
                    "detail": "last 5.1 event carries errors == 0" if green else ("no 5.1 event with an errors field" if last_check is None or "errors" not in last_check else f"{last_check.get('errors')} error(s)")})
    if not reviews:
        clauses.append({"clause": "review", "verdict": "indeterminate", "detail": "no 5.2 event"})
    else:
        rv = reviews[-1]
        if rv.get("class_finding") is True:
            after = [e for e in ev[ev.index(rv) + 1:] if e.get("function") == "validate_artifact" and not e.get("skipped")]
            clauses.append({"clause": "review", "verdict": "pass" if after else "fail",
                            "detail": "class finding, one rewrite, code check re-run" if after else "class finding with no rewrite (no 5.1 after the review)"})
        else:
            clauses.append({"clause": "review", "verdict": "pass", "detail": "reviewed, no class finding"})
    bad = [c for c in clauses if c["verdict"] != "pass"]
    if not bad:
        return {"verdict": CANDIDATE, "rule": None, "clauses": clauses,
                "reason": "filled, code check green, reviewed once and rewritten once if red; not measured - promote to measure"}
    if any(c["verdict"] == "fail" for c in clauses):
        return {"verdict": ABANDON, "rule": None, "clauses": clauses, "reason": "; ".join(f"{c['clause']}: {c['detail']}" for c in bad)}
    return {"verdict": UNDECIDABLE, "rule": None, "clauses": clauses, "reason": "; ".join(f"{c['clause']}: {c['detail']}" for c in bad)}


def decide_fast(root: Path, unmeasured: list[str]) -> dict:
    """Fast mode. With-arm only, so no clause that needs a baseline can be judged.

    Two clauses: the minimum repeats per test, and every with-arm run correct.
    Nothing about cost - there is no baseline to be within 20 percent of - and
    nothing about a win, because a win is over somebody. That is why the
    ceiling is FAST_PASS and not SHIP, and the ceiling holds even if a fast
    build happened to log a without-arm too: it did not run the calibrated,
    blinded comparison the ship verdict stands for.
    """
    rows = [r for r in rows_of(root) if r.get("arm") == "with"]
    clauses = []
    if not rows:
        clauses.append({"clause": "data", "verdict": "indeterminate",
                        "detail": "no with-arm rows in the run_paired event"})
    else:
        tests = _by_test(rows)
        thin = [f"{t}: {len(reps)} repeat(s)" for t, reps in tests.items()
                if len(reps) < DEFAULTS["min_repeats"]]
        clauses.append({"clause": "repeats", "verdict": "pass" if not thin else "indeterminate",
                        "detail": f"min {DEFAULTS['min_repeats']} with-arm repeats per test"
                                  + ("" if not thin else " — " + "; ".join(thin[:4]))})
        unknown = [f"{r['test']} r{r['repeat']}" for r in rows if r.get("correct") is None]
        wrong = [f"{r['test']} r{r['repeat']}" for r in rows if r.get("correct") is False]
        if unknown:
            clauses.append({"clause": "correct", "verdict": "indeterminate",
                            "detail": f"correctness not recorded for {', '.join(unknown[:4])}"})
        else:
            clauses.append({"clause": "correct", "verdict": "pass" if not wrong else "fail",
                            "detail": "every with-arm run correct" if not wrong
                                      else f"wrong on {', '.join(wrong[:4])}"})
    indet = [c for c in clauses if c["verdict"] == "indeterminate"]
    failed = [c for c in clauses if c["verdict"] == "fail"]
    base = {"mode": "fast", "rule": None, "clauses": clauses}
    if indet:
        return {**base, "verdict": UNDECIDABLE,
                "reason": "cannot decide — " + "; ".join(f"{c['clause']}: {c['detail']}"
                                                         for c in indet[:3])}
    if failed:
        return {**base, "verdict": ITERATE,
                "reason": "; ".join(f"{c['clause']}: {c['detail']}" for c in failed[:3])}
    out = {**base, "verdict": FAST_PASS,
           "reason": ("fast mode: every with-arm run correct across the repeats. Not ship — "
                      "no baseline ran, so nothing was beaten; a ship decision needs a full build")}
    if unmeasured:
        out["unmeasured_runs"] = unmeasured
    return out


def _ship_reachable(mode: str) -> bool:
    """A mode reaches ship only if the chain contract lists ship among its verdicts.

    Read from the contract, not from the mode's name: fast is the mode whose
    ceiling is fast_pass today, and a mode added tomorrow inherits the rule
    without this file learning its name.
    """
    modes = rec.load_chain().get("modes") or {}
    block = modes.get(mode)
    if not isinstance(block, dict):
        return mode != "fast"
    return "ship" in (block.get("verdicts") or [])


def decide(root: Path) -> dict:
    root = Path(root)
    head = rec.header(root)

    # 4.0.0: decide writes its own 8.1 event first. A build once called decide
    # before logging 8.1 and the chain gate (rightly) returned undecidable for
    # that alone; the fix is that the phase cannot be forgotten by the caller.
    rec.append(root, phase="8.1", function="decide", out="decide.py invoked")

    mode = head.get("mode", "full")
    if mode == "candidate":
        return decide_candidate(root)

    # A phase that left no event is not a phase that went well. Checked BEFORE
    # the measurement, because a verdict computed over a chain with a hole in it
    # is a verdict about a run nobody can reconstruct.
    missing = rec.chain_gate(root, version=1)
    if missing:
        names = ", ".join(f"{m['id']} {m['fn']}" for m in missing[:5])
        return {"verdict": UNDECIDABLE, "rule": None, "clauses": [],
                "missing_phases": [m["id"] for m in missing],
                "reason": (f"{len(missing)} v1 phase(s) left no event, neither a run nor a skip: "
                           f"{names}. A skip is allowed and needs a reason; an absence is not.")}

    # A dispatched run with no duration is a measurement that was available and
    # not taken. It does not block the verdict - the verdict is about the skill,
    # not about our bookkeeping - but it is reported, because the alternative is
    # discovering months later that two thirds of the run was never timed.
    unmeasured = rec.cost_gate(root)

    # A fan-out whose revert did not happen is not a measurement of this
    # artefact (chain contract `fanout`). Checked before the rows are read.
    fan = rec.fanout_gate(root)
    if fan:
        return {"verdict": UNDECIDABLE, "rule": None, "clauses": [], "fanout": fan,
                "reason": "cannot decide - " + "; ".join(fan)}

    if not _ship_reachable(head.get("mode", "full")):
        return decide_fast(root, unmeasured)

    # Chain 3.1.1: under review_before_arms a build whose reviews stayed red at
    # class level up to the mode's cap never runs an arm. That is not "no data";
    # it is the build's verdict - the text could not be made consistent in the
    # rounds allowed, so the candidate is abandoned as unconverged at review.
    mode_block = (rec.load_chain().get("modes") or {}).get(head.get("mode", "full")) or {}
    cap = mode_block.get("max_reviews")
    ev_all = rec.events(root)
    if cap and not [e for e in ev_all if e.get("function") == "run_paired" and not e.get("skipped")]:
        reviews = [e for e in ev_all if e.get("function") == "review_artifact"]
        red = [e for e in reviews if e.get("class_finding") is True]
        if reviews and reviews[-1].get("class_finding") is True and len(red) >= cap:
            return {"verdict": ABANDON, "rule": None, "clauses": [], "reviews_red": len(red),
                    "reason": (f"unconverged at review: {len(red)} whole-artefact review(s) red at class "
                               f"level, at the cap of {cap}; no arm ran (review_before_arms), so the "
                               f"candidate is abandoned on the text, not on a measurement")}

    rule, why = resolve_rule(head)
    if rule is None:
        return {"verdict": UNDECIDABLE, "reason": why, "rule": None, "clauses": []}

    k, outcome = resolve_repeats(root, rule)
    rule = dict(rule, min_repeats=k)
    found = evaluate(rows_of(root, rule), rule)
    clauses = found["clauses"]
    indet = [c for c in clauses if c["verdict"] == "indeterminate"]
    failed = [c for c in clauses if c["verdict"] == "fail"]

    if indet:
        return {"verdict": UNDECIDABLE, "rule": rule, "clauses": clauses,
                "min_repeats_applied": k, "probe_outcome": outcome,
                "reason": "cannot decide — " + "; ".join(f"{c['clause']}: {c['detail']}"
                                                         for c in indet[:3])}
    if not failed:
        out = {"verdict": SHIP, "rule": rule, "clauses": clauses,
               "min_repeats_applied": k, "probe_outcome": outcome,
               "reason": f"every clause of the preregistered rule holds ({why}; "
                         f"k={k} from probe outcome {outcome!r})"}
        if unmeasured:
            out["unmeasured_runs"] = unmeasured
            out["reason"] += (f" — note: {len(unmeasured)} dispatched run(s) logged no duration, "
                              f"so this build cannot be compared on wall clock")
        return out

    loops = len([e for e in rec.events(root) if e["function"] == "triage_failure"])
    verdict = ABANDON if loops >= rule["max_repair_loops"] else ITERATE
    tail = (f" after {loops} repair loop(s), at the cap of {rule['max_repair_loops']}"
            if verdict == ABANDON else "")
    return {"verdict": verdict, "rule": rule, "clauses": clauses, "repair_loops": loops,
            "reason": "; ".join(f"{c['clause']}: {c['detail']}" for c in failed[:3]) + tail}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("build_dir")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--record", action="store_true",
                    help="append the verdict to the build record")
    args = ap.parse_args()

    d = decide(Path(args.build_dir))
    if args.json:
        print(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print(f"{d['verdict'].upper()}  {d['reason']}")
        for c in d["clauses"]:
            mark = {"pass": "ok", "fail": " E", "indeterminate": " ?"}[c["verdict"]]
        if d.get("mode") == "fast":
            print("   (fast mode: with-arm only, no baseline — ship is not reachable)")
            print(f"   [{mark}] {c['clause']:<16} {c['detail']}")
    if args.record:
        rec.append(Path(args.build_dir), phase="8", function="decide",
                   verdict=d["verdict"], reason=d["reason"], clauses=d["clauses"])
    return {SHIP: 0, ITERATE: 1, ABANDON: 1, UNDECIDABLE: 2, FAST_PASS: 3}[d["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
