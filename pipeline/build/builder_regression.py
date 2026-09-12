#!/usr/bin/env python3
"""Is the BUILDER getting better, or just producing builds?

Every gate in this system measures one artefact. Nothing measures the thing that
makes them. Change the field contract tomorrow and nothing tells you the builder
got worse - you would find out one skill at a time, if at all.

This reads across builds.jsonl and fields.jsonl and reports the trend on four
things the chain already records:

  rework per field   how many code and reader checks went red, and how many
                     rewrites it took. This is the one that says WHERE in the
                     chain the method costs most, which is what fields.jsonl was
                     built for.
  verdict mix        ship / iterate / abandon / undecidable over time. A rising
                     abandon rate is not failure - it may be the gates working -
                     but a rising UNDECIDABLE rate is bookkeeping rotting.
  skips              a chain completing on more and more skips is a chain being
                     hollowed out one reasoned exception at a time.
  not_checked        an honest build names what it did not establish. A build
                     that names none is either perfect or not looking.

Two builds is not a trend and the report says so rather than drawing a line
through two points. It exists now so the third build has something to be compared
against, which is the only moment it can be created.

    python3 builder_regression.py [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGERS = REPO / "pipeline" / "ledgers"
BUILDS = REPO / "pipeline" / "builds"

MIN_FOR_TREND = 3


def _rows(name: str) -> list[dict]:
    p = LEDGERS / name
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def report() -> dict:
    builds = _rows("builds.jsonl")
    fields = _rows("fields.jsonl")

    by_field = defaultdict(lambda: {"red_code": 0, "red_agent": 0, "rewrites": 0, "n": 0})
    for f in fields:
        e = by_field[f.get("field", "?")]
        e["red_code"] += f.get("n_red_code", 0)
        e["red_agent"] += f.get("n_red_agent", 0)
        e["rewrites"] += f.get("rewrites", 0)
        e["n"] += 1
    costly = sorted(by_field.items(),
                    key=lambda kv: -(kv[1]["red_code"] + kv[1]["red_agent"] + kv[1]["rewrites"]))

    verdicts = Counter(b.get("verdict") for b in builds)
    skips = [(b.get("build"), len(b.get("phases_skipped") or [])) for b in builds]
    unchecked = [(b.get("build"), len(b.get("not_checked") or [])) for b in builds]

    out = {
        "n_builds": len(builds),
        "trend_possible": len(builds) >= MIN_FOR_TREND,
        "verdicts": dict(verdicts),
        "per_field": {k: v for k, v in costly},
        "costliest_fields": [k for k, _ in costly[:3]],
        "skips_per_build": skips,
        "not_checked_per_build": unchecked,
    }
    if len(builds) < MIN_FOR_TREND:
        out["note"] = (f"{len(builds)} build(s). A trend needs at least {MIN_FOR_TREND}; two points "
                       f"make a line and mean nothing. This report exists now so the next build has "
                       f"something to be compared against - the one moment a baseline can be made.")
    flags = []
    if verdicts.get("undecidable"):
        flags.append(f"{verdicts['undecidable']} build(s) ended UNDECIDABLE — that is bookkeeping, "
                     f"not measurement, and it is the failure mode that grows quietly")
    if any(n == 0 for _, n in unchecked):
        flags.append("a build named nothing it did not check — either perfect, or not looking")
    out["flags"] = flags
    return out


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--json", action="store_true")
    args = a.parse_args()
    r = report()
    if args.json:
        print(json.dumps(r, indent=2))
        return 0
    print(f"{r['n_builds']} build(s) · verdicts {r['verdicts']}")
    if r.get("note"):
        print(f"\n{r['note']}")
    print("\nrework per field (red code · red reader · rewrites, over all builds):")
    for k, v in r["per_field"].items():
        print(f"   {k:<22} {v['red_code']:>2} · {v['red_agent']:>2} · {v['rewrites']:>2}   ({v['n']} build(s))")
    print("\nskips per build:      ", r["skips_per_build"])
    print("not_checked per build:", r["not_checked_per_build"])
    for f in r["flags"]:
        print(f"\n   [!] {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
