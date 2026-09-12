#!/usr/bin/env python3
"""Controls for the trigger matrix.

The one that matters: an empty near-miss set must be INDETERMINATE, never a clean
mis-fire score. A unit tested only on its own vocabulary has been shown nothing
about the boundary it shares with a sibling, and reporting that as 0 mis-fires is
the most flattering lie this file could tell.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import triggers as tg  # noqa: E402

R: list[tuple[bool, str]] = []


def check(ok, label, detail=""):
    R.append((ok, f"{label}{'  — ' + detail if detail and not ok else ''}"))


PKG = {"id": "unit-a", "trigger_terms": ["blind the grader", "A/B", "which arm"],
       "representative_tasks": [{"task": "Set up grading for two arms."},
                                {"task": "Write the un-blinding test."}]}


def qs(neg):
    q = tg.build_queries(PKG, [])
    q["queries"] += neg
    return q


def main() -> int:
    _target_cases()
    q = tg.build_queries(PKG, ["sibling-b"])
    check(sum(1 for x in q["queries"] if x["kind"] == "positive") == 5,
          "positives come from trigger_terms and the tasks, not from invention")
    check(any(x["kind"] == "near-miss" and not x.get("query") for x in q["queries"]),
          "a sibling produces a near-miss STUB rather than a made-up query")

    # THE control: no negatives is unmeasured, not clean
    r = tg.score(tg.build_queries(PKG, []), {x: "unit-a" for x in
                 ["blind the grader", "A/B", "which arm",
                  "Set up grading for two arms.", "Write the un-blinding test."]})
    mis = next(c for c in r["clauses"] if c["clause"] == "mis-fire")
    check(mis["verdict"] == "indeterminate" and r["verdict"] == "indeterminate",
          "with no near misses the mis-fire rate is UNMEASURED, not zero", mis["verdict"])
    check("not zero" in mis["detail"], "and it says so in the detail, not only in the verdict")

    routing = {x: "unit-a" for x in ["blind the grader", "A/B", "which arm",
                                     "Set up grading for two arms.", "Write the un-blinding test."]}
    near = [{"query": "validate my judge against human labels", "expect": "sibling-b",
             "kind": "near-miss", "source": "sibling"}]

    r = tg.score(qs(near), {**routing, near[0]["query"]: "sibling-b"})
    check(r["verdict"] == "pass", "full recall and a clean near miss passes", str(r["counts"]))

    r = tg.score(qs(near), {**routing, near[0]["query"]: "unit-a"})
    check(r["verdict"] == "fail" and r["counts"]["mis_fired"] == 1,
          "a near miss routed here is a mis-fire and fails")

    r = tg.score(qs(near), {**{k: "unit-a" for k in list(routing)[:2]}, near[0]["query"]: "sibling-b"})
    rec = next(c for c in r["clauses"] if c["clause"] == "recall")
    check(r["verdict"] == "fail" and "no-fire" in rec["detail"],
          "2 of 5 positives firing fails recall and names which missed")

    r = tg.score(qs(near), {**routing})   # near miss routes NOWHERE
    sib = next(c for c in r["clauses"] if c["clause"] == "sibling-reached")
    check(sib["verdict"] == "warn" and "hole in the library" in sib["detail"],
          "a near miss that routes nowhere is a hole, not a win for this unit")

    bad = [m for ok, m in R if not ok]
    for ok, m in R:
        if "-v" in sys.argv or not ok:
            print(f"{'ok   ' if ok else 'FAIL '} {m}")
    print(f"\n{len(R) - len(bad)}/{len(R)} controls behaved")
    return 1 if bad else 0


def _target_cases():
    """The 2026-09-01 defect, reconstructed, plus the guard that now catches it."""
    import tempfile
    from pathlib import Path as _P
    from triggers import build_queries, score, target_from_skill_dir

    pkg = {"id": "abstention-threshold-design-v2",
           "trigger_terms": ["confidence cut", "auto-approve threshold", "abstention"],
           "representative_tasks": [{"task": "where do we set the auto-approve line"}]}

    # 1. The fallback still works, and now SAYS it is a fallback.
    q = build_queries(pkg, [])
    check(q["target"] == "abstention-threshold-design-v2", "fallback target is the package id")
    check(q["target_source"] == "package-id-fallback", "fallback is labelled as one")
    check(bool(q.get("target_warning")), "fallback carries a warning")

    # 2. THE DEFECT. The router chose the real skill on every query and the old
    #    code returned 0/12 recall. The guard must refuse, not report a number.
    routing = {x["query"]: "abstention-threshold-design"
               for x in q["queries"] if x.get("query")}
    r = score(q, routing)
    check(r["verdict"] == "indeterminate", "wrong target refuses instead of scoring recall")
    check(r.get("suspected_target") == "abstention-threshold-design",
          "and it names the target the router actually chose")

    # 3. NEGATIVE CONTROL: a genuine no-fire must still be scored as a red. If
    #    the guard swallowed this, it would hide the failures it exists beside.
    r = score(q, {})
    check(r.get("suspected_target") is None, "a genuine no-fire is not excused as a mismatch")

    # 4. NEGATIVE CONTROL: scattered routing is not a name mismatch.
    scattered = {x["query"]: f"other-{i}"
                 for i, x in enumerate(q["queries"]) if x.get("query")}
    r = score(q, scattered)
    check(r.get("suspected_target") is None, "scattered routing is not called a mismatch")

    # 5. An explicit target is recorded as explicit and warns about nothing.
    q2 = build_queries(pkg, [], "abstention-threshold-design")
    check(q2["target_source"] == "explicit", "explicit target is recorded as explicit")
    check(q2.get("target_warning") is None, "explicit target carries no warning")
    r = score(q2, {x["query"]: "abstention-threshold-design"
                   for x in q2["queries"] if x.get("query")})
    check(r.get("suspected_target") is None, "the right target scores rather than refusing")

    # 6. The target can be read from the artefact the router will see.
    with tempfile.TemporaryDirectory() as td:
        d = _P(td) / "s"
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: abstention-threshold-design\n"
                                    "description: x\n---\n\n# Body\n")
        check(target_from_skill_dir(d) == "abstention-threshold-design",
              "target read from SKILL.md frontmatter")
        (d / "SKILL.md").write_text("no frontmatter here\n")
        check(target_from_skill_dir(d) is None, "no frontmatter yields None, never a guess")


if __name__ == "__main__":
    sys.exit(main())
