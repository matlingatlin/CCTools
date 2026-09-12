#!/usr/bin/env python3
"""Aggregate every dispatched run across builds by JOB CLASS.

Reads pipeline/builds/*/cost/measured.jsonl (one row per dispatched run, written by
pipeline/build/dispatch.py or by the pre-harness shell of earlier builds) and
pipeline/builds/*/cost/coordinator.jsonl (one row per coordinator turn, with a kind).

A job class is what a routing table would key on: probe, arm, reader, writer, reviewer,
calibrate, grader, trigger, other. It is derived from the row's label and phase, never
from the tier, so a run that was routed down still counts in its class.

Usage:
  python3 pipeline/queries/job_class_cost.py            # table over all builds
  python3 pipeline/queries/job_class_cost.py --json     # rows as JSON
  python3 pipeline/queries/job_class_cost.py --build X  # one build

Every number is a sum over rows that carried it. A missing field is counted as absent
(reported in the 'rows_without' column), never as zero.
"""
import argparse, glob, json, os, re, sys
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILDS = os.path.join(REPO, "pipeline", "builds")

CLASS_RULES = [  # first match wins; checked against "label|phase"
    (r"probe", "probe"),
    (r"calib", "calibrate"),
    (r"grade|grader", "grader"),
    (r"trigger|6\.5", "trigger"),
    (r"review|5\.2", "reviewer"),
    (r"verify|3\.4", "verifier"),
    (r"^read\.|reader|read\.4|read-", "reader"),
    (r"writer|author", "writer"),
    (r"\barm\b|with|without|incumbent|6\.1|6\.6|field-trial", "arm"),
]

def job_class(row):
    text = f"{row.get('label','')}|{row.get('phase','')}"
    arm = row.get("arm")
    if arm in ("with", "without", "incumbent") and str(row.get("phase", "")).startswith("6"):
        return "arm"
    if arm == "without" and str(row.get("phase", "")).startswith("2"):
        return "probe"
    for pat, cls in CLASS_RULES:
        if re.search(pat, text, re.I):
            return cls
    return "other"

def load(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows

def aggregate(builds):
    per = defaultdict(lambda: {"runs": 0, "ms": 0, "tokens": 0, "tool_calls": 0,
                               "rows_without": defaultdict(int), "tiers": defaultdict(int),
                               "max_ms": 0, "builds": set()})
    coord = defaultdict(lambda: {"turns": 0, "ms": 0, "builds": set()})
    for b in builds:
        name = os.path.basename(b.rstrip("/"))
        for r in load(os.path.join(b, "cost", "measured.jsonl")):
            c = per[job_class(r)]
            if r.get("cached") is True:
                c["cached"] = c.get("cached", 0) + 1   # a replay, never a measurement of load
                continue
            c["runs"] += 1; c["builds"].add(name)
            for k in ("duration_ms", "tokens", "tool_calls"):
                v = r.get(k)
                if isinstance(v, (int, float)):
                    c[{"duration_ms": "ms", "tokens": "tokens", "tool_calls": "tool_calls"}[k]] += v
                else:
                    c["rows_without"][k] += 1
            if isinstance(r.get("duration_ms"), (int, float)):
                c["max_ms"] = max(c["max_ms"], r["duration_ms"])
            c["tiers"][r.get("tier") or "absent"] += 1
        for r in load(os.path.join(b, "cost", "coordinator.jsonl")):
            k = coord[r.get("kind") or "unknown"]
            k["turns"] += 1; k["builds"].add(name)
            if isinstance(r.get("duration_ms"), (int, float)):
                k["ms"] += r["duration_ms"]
    return per, coord

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    builds = sorted(glob.glob(os.path.join(BUILDS, a.build or "*", "")))
    per, coord = aggregate(builds)
    if a.json:
        out = {cls: {**{k: v for k, v in c.items() if k not in ("builds", "rows_without", "tiers")},
                     "builds": sorted(c["builds"]), "rows_without": dict(c["rows_without"]),
                     "tiers": dict(c["tiers"])} for cls, c in per.items()}
        out["_coordinator"] = {k: {"turns": v["turns"], "ms": v["ms"], "builds": sorted(v["builds"])} for k, v in coord.items()}
        print(json.dumps(out, indent=2)); return
    total_ms = sum(c["ms"] for c in per.values()) or 1
    total_tok = sum(c["tokens"] for c in per.values()) or 1
    print(f"builds: {len(builds)}  ({', '.join(os.path.basename(b.rstrip('/')) for b in builds)})")
    print(f"{'class':<10}{'runs':>5}{'min':>8}{'%min':>6}{'Mtok':>8}{'%tok':>6}{'max run':>9}{'tools':>7}  tiers / rows without a field")
    for cls, c in sorted(per.items(), key=lambda kv: -kv[1]["ms"]):
        rw = ", ".join(f"{k}:{v}" for k, v in c["rows_without"].items()) or "-"
        tiers = ",".join(f"{k}:{v}" for k, v in c["tiers"].items())
        cached = f"  cached replays: {c['cached']}" if c.get("cached") else ""
        print(f"{cls:<10}{c['runs']:>5}{c['ms']/60000:>8.1f}{100*c['ms']/total_ms:>6.0f}{c['tokens']/1e6:>8.2f}{100*c['tokens']/total_tok:>6.0f}{c['max_ms']/60000:>9.1f}{c['tool_calls']:>7}  {tiers} / {rw}{cached}")
    print(f"{'total':<10}{sum(c['runs'] for c in per.values()):>5}{total_ms/60000:>8.1f}{'':>6}{total_tok/1e6:>8.2f}")
    if coord:
        print("\ncoordinator turns (only builds that recorded them):")
        for k, v in sorted(coord.items(), key=lambda kv: -kv[1]["ms"]):
            print(f"  {k:<16}{v['turns']:>4} turns {v['ms']/60000:>7.1f} min  in {len(v['builds'])} build(s)")

if __name__ == "__main__":
    main()
