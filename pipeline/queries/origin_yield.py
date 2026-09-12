#!/usr/bin/env python3
"""Which source shape yields skills worth having?

Every gate in this system judges one build. This asks the question no build can
answer about itself, and it is the reason `origin` exists on the package at all:
if we never record where a package came from, the question cannot be reconstructed
later - the builds are over.

Five questions, in the order they become answerable:

  1. yield        which origin ships, and at what rate
  2. warrant      does a package with SOURCED claims fare better than one without
  3. hypothesis   how often the probe REFUTES the gap the package predicted,
                  per origin. Refuted 2 of 2 so far, both agent-authored.
  4. axis         which axis each origin wins on. An origin that only ever wins
                  on shape is telling you something about that origin.
  5. cost         so an expensive source shape can be dropped on evidence

It refuses to compute a rate from fewer than MIN_PER_CELL builds and says so per
cell, rather than printing 100% over one row. Almost every cell will be empty for
a long time. That is the correct state of a ledger with two builds in it, and
printing it empty is how the emptiness stays visible.

    python3 origin_yield.py [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "pipeline" / "ledgers" / "builds.jsonl"
MIN_PER_CELL = 3


def rows() -> list[dict]:
    if not LEDGER.is_file():
        return []
    return [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()]


def analyse() -> dict:
    rs = rows()
    by_origin = defaultdict(list)
    for r in rs:
        by_origin[r.get("origin") or "(unrecorded)"].append(r)

    yield_rows = []
    for o, group in sorted(by_origin.items()):
        ships = sum(1 for r in group if r.get("verdict") == "ship")
        refuted = sum(1 for r in group if str(r.get("probe_outcome") or "").lower().find("refut") >= 0)
        axes = [r.get("won_on") for r in group if r.get("won_on")]
        toks = [r.get("cost", {}).get("tokens") for r in group]
        yield_rows.append({
            "origin": o, "n": len(group), "ships": ships,
            "ship_rate": (ships / len(group)) if len(group) >= MIN_PER_CELL else None,
            "hypothesis_refuted": refuted,
            "refuted_rate": (refuted / len(group)) if len(group) >= MIN_PER_CELL else None,
            "won_on": axes,
            "median_tokens": (sorted(t for t in toks if isinstance(t, int))[len(
                [t for t in toks if isinstance(t, int)]) // 2]
                if any(isinstance(t, int) for t in toks) else None),
            "enough_to_rate": len(group) >= MIN_PER_CELL,
        })

    sourced = [r for r in rs if (r.get("n_measured_claims") or 0) > 0]
    unsourced = [r for r in rs if not (r.get("n_measured_claims") or 0)]
    warrant = {
        "with_measured_claims": {"n": len(sourced),
                                 "ships": sum(1 for r in sourced if r.get("verdict") == "ship")},
        "without": {"n": len(unsourced),
                    "ships": sum(1 for r in unsourced if r.get("verdict") == "ship")},
        "comparable": len(sourced) >= MIN_PER_CELL and len(unsourced) >= MIN_PER_CELL,
    }
    return {"n_builds": len(rs), "min_per_cell": MIN_PER_CELL,
            "yield": yield_rows, "warrant": warrant,
            "unrecorded_origin": sum(1 for r in rs if not r.get("origin")),
            "note": ("A rate is withheld below "
                     f"{MIN_PER_CELL} builds per cell. Empty cells are printed rather than hidden - "
                     "with two builds in the ledger, an empty table IS the finding, and a table "
                     "that filled itself in anyway would be the problem.")}


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--json", action="store_true")
    args = a.parse_args()
    r = analyse()
    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False)); return 0
    print(f"{r['n_builds']} build(s) in the ledger · "
          f"{r['unrecorded_origin']} with no origin recorded\n")
    print(f"{'origin':<20} {'n':>3} {'ships':>6} {'rate':>6} {'refuted':>8} {'med tok':>9}  won on")
    for y in r["yield"]:
        rate = f"{y['ship_rate']:.0%}" if y["ship_rate"] is not None else "  —"
        tok = f"{y['median_tokens']/1e6:.2f}M" if y["median_tokens"] else "    —"
        print(f"{y['origin']:<20} {y['n']:>3} {y['ships']:>6} {rate:>6} "
              f"{y['hypothesis_refuted']:>8} {tok:>9}  {', '.join(a[:34] for a in y['won_on'][:2])}")
    w = r["warrant"]
    print(f"\nsourced vs unsourced: {w['with_measured_claims']['ships']}/{w['with_measured_claims']['n']}"
          f" ship  ·  {w['without']['ships']}/{w['without']['n']} ship"
          f"   {'(comparable)' if w['comparable'] else '(NOT yet comparable)'}")
    print(f"\n{r['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
