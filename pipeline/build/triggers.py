#!/usr/bin/env python3
"""Phase 6.5 - does the unit actually get PICKED?

Everything else in this chain measures what a skill does once it is loaded.
None of it shows that a router would ever reach for it. A skill that is correct,
measured and never selected is dead weight that still costs its description in
every context window.

The test is a matrix, not a score. Positives: queries a person types when they
HAVE this problem. Negatives: NEAR MISSES - queries that belong to the nearest
sibling and must NOT come here. Far-off negatives prove nothing; nobody was ever
going to route "reset my password" to a blinding skill.

Two failures, and they are not symmetric:

  no-fire   the unit exists and is unreachable. Costs its description forever and
            returns nothing.
  mis-fire  the unit answers a question that belongs to a sibling. Worse: the
            sibling's answer is the right one and never arrives, and the person
            has no way to know.

    python3 triggers.py build <package.json> --siblings a,b --out queries.json
    python3 triggers.py score <queries.json> <routing.json>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def target_from_skill_dir(skill_dir: Path) -> str | None:
    """The name the router will actually see: SKILL.md frontmatter, not the package id."""
    f = Path(skill_dir) / "SKILL.md"
    if not f.is_file():
        return None
    m = re.search(r"^---\s*$(.*?)^---\s*$", f.read_text(encoding="utf-8"),
                  re.S | re.M)
    if not m:
        return None
    n = re.search(r"^name:\s*(.+?)\s*$", m.group(1), re.M)
    return n.group(1).strip() if n else None


def build_queries(pkg: dict, siblings: list[str], target: str | None = None) -> dict:
    """The query set, from the package - never invented at scoring time.

    Positives come from trigger_terms and the representative tasks, which is
    where the user's own vocabulary lives. Negatives are left for a human or a
    sibling scan to fill: a near miss has to be a real neighbouring job, and this
    file cannot know one.

    The target is the name the ROUTER sees - SKILL.md's frontmatter name - which
    is not the package id. On 2026-09-01 a package id of
    abstention-threshold-design-v2 was scored against a skill named
    abstention-threshold-design, and all 12 positives came back as no-fires while
    the router had in fact chosen the skill every single time. A 0/12 recall
    reads as a finding, not as a bug, which is why the default is now recorded
    and the score refuses rather than reports it.
    """
    target_source = "explicit"
    if target is None:
        target, target_source = pkg["id"], "package-id-fallback"
    pos = []
    for t in pkg.get("trigger_terms", []):
        pos.append({"query": t, "expect": target, "kind": "positive", "source": "trigger_terms"})
    for t in pkg.get("representative_tasks", []):
        pos.append({"query": t["task"], "expect": target, "kind": "positive",
                    "source": "representative_tasks"})
    neg = [{"query": None, "expect": s, "kind": "near-miss", "source": "sibling",
            "todo": f"write a query that genuinely belongs to {s}"} for s in siblings]
    return {"target": target, "target_source": target_source, "queries": pos + neg,
            "note": ("negatives are stubs until someone writes them; an empty near-miss set makes "
                     "the mis-fire rate unmeasurable, and this file says so rather than scoring 0"),
            "target_warning": (
                "target taken from the package id because none was given; if the built skill's "
                "frontmatter name differs, every positive will score as a no-fire"
            ) if target_source == "package-id-fallback" else None}


def score(qs: dict, routing: dict) -> dict:
    """routing: {query: chosen_unit}. Absent means the router chose nothing."""
    target = qs["target"]
    pos = [q for q in qs["queries"] if q["kind"] == "positive" and q.get("query")]
    neg = [q for q in qs["queries"] if q["kind"] == "near-miss" and q.get("query")]

    fired = [q for q in pos if routing.get(q["query"]) == target]
    no_fire = [q for q in pos if routing.get(q["query"]) != target]
    mis_fire = [q for q in neg if routing.get(q["query"]) == target]
    right_sibling = [q for q in neg if routing.get(q["query"]) == q["expect"]]

    # The wrong-target signature. Nothing fired, yet the router consistently
    # chose ONE other unit: that is a name mismatch, not a skill that fails to
    # trigger, and the two are indistinguishable from the recall number alone.
    # Refusing here is the whole point -- the run this guard comes from produced
    # a clean-looking 0/12 that a reader took at face value.
    if pos and not fired:
        chosen = [routing.get(q["query"]) for q in pos if routing.get(q["query"])]
        if chosen and len(set(chosen)) == 1 and len(chosen) >= max(2, len(pos) // 2):
            other = chosen[0]
            return {"target": target, "verdict": "indeterminate",
                    "clauses": [{"clause": "target", "verdict": "indeterminate",
                                 "detail": (f"no positive routed to {target!r}, but {len(chosen)} "
                                            f"of {len(pos)} routed to {other!r}. That is a target "
                                            f"name mismatch, not a recall failure. Re-run with "
                                            f"--target {other} or --skill-dir.")}],
                    "counts": {"positives": len(pos), "fired": 0, "routed_elsewhere": len(chosen)},
                    "suspected_target": other}

    clauses = []
    if not pos:
        clauses.append({"clause": "recall", "verdict": "indeterminate",
                        "detail": "no positive queries"})
    else:
        r = len(fired) / len(pos)
        clauses.append({"clause": "recall", "verdict": "pass" if r >= 0.8 else "fail",
                        "detail": f"{len(fired)}/{len(pos)} positives routed here ({r:.0%}, floor 80%)"
                                  + ("" if not no_fire else
                                     " — no-fire on: " + "; ".join(q["query"][:45] for q in no_fire[:3]))})
    if not neg:
        clauses.append({"clause": "mis-fire", "verdict": "indeterminate",
                        "detail": ("no near-miss queries — the mis-fire rate is UNMEASURED, not zero. "
                                   "A unit tested only on its own vocabulary has been shown nothing "
                                   "about the boundary it shares with a sibling.")})
    else:
        clauses.append({"clause": "mis-fire", "verdict": "pass" if not mis_fire else "fail",
                        "detail": f"{len(mis_fire)}/{len(neg)} near misses wrongly routed here"
                                  + ("" if not mis_fire else
                                     " — " + "; ".join(q["query"][:45] for q in mis_fire[:3]))})
        clauses.append({"clause": "sibling-reached", "verdict":
                        "pass" if len(right_sibling) == len(neg) else "warn",
                        "detail": f"{len(right_sibling)}/{len(neg)} near misses reached the sibling "
                                  f"they belong to — a near miss that routes NOWHERE is a hole in the "
                                  f"library, not a success for this unit"})

    bad = [c for c in clauses if c["verdict"] == "fail"]
    ind = [c for c in clauses if c["verdict"] == "indeterminate"]
    verdict = "fail" if bad else ("indeterminate" if ind else "pass")
    return {"target": target, "verdict": verdict, "clauses": clauses,
            "counts": {"positives": len(pos), "near_misses": len(neg),
                       "fired": len(fired), "mis_fired": len(mis_fire)}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("package"); b.add_argument("--siblings", default="")
    b.add_argument("--out", required=True)
    b.add_argument("--target", default=None,
                   help="the name the router sees; defaults to the package id, which is often wrong")
    b.add_argument("--skill-dir", default=None,
                   help="read the target from this skill's SKILL.md frontmatter name")
    s = sub.add_parser("score"); s.add_argument("queries"); s.add_argument("routing")
    a = ap.parse_args()

    if a.cmd == "build":
        pkg = json.loads(Path(a.package).read_text(encoding="utf-8"))
        sib = [x.strip() for x in a.siblings.split(",") if x.strip()]
        target = a.target
        if target is None and a.skill_dir:
            target = target_from_skill_dir(Path(a.skill_dir))
            if target is None:
                print(f"could not read a frontmatter name from {a.skill_dir}/SKILL.md", file=sys.stderr)
                return 2
        qs = build_queries(pkg, sib, target)
        Path(a.out).write_text(json.dumps(qs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        stubs = sum(1 for q in qs["queries"] if not q.get("query"))
        print(f"{len(qs['queries'])} queries -> {a.out}  target={qs['target']!r} "
              f"({qs['target_source']})"
              + (f"  ({stubs} near-miss stub(s) still to write)" if stubs else ""))
        if qs.get("target_warning"):
            print(f"   [?] {qs['target_warning']}")
        return 0

    r = score(json.loads(Path(a.queries).read_text(encoding="utf-8")),
              json.loads(Path(a.routing).read_text(encoding="utf-8")))
    print(f"{r['verdict'].upper()}  {r['counts']}")
    for c in r["clauses"]:
        print(f"   [{ {'pass':'ok','fail':' E','warn':' w','indeterminate':' ?'}[c['verdict']] }] "
              f"{c['clause']:<16} {c['detail']}")
    return {"pass": 0, "fail": 1, "indeterminate": 2}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
