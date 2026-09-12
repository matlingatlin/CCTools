#!/usr/bin/env python3
"""Phase 7.1 - did every run write the same helper?

When several independent runs of a skill each write the same small piece of code,
that code is not part of the answer. It is scaffolding the method needs, and the
skill should ship it instead of asking for it to be rewritten every time.

The signal is REPETITION ACROSS INDEPENDENT RUNS. One run writing a helper says
that run wanted one; three runs writing the same helper says the method requires
one. So a candidate needs occurrences in at least `min_runs` distinct runs, and
the default is 2 for the same reason a verdict needs two repeats.

Nothing found is the normal outcome, and it is reported as a finding rather than
as an empty result: "no helper repeated" is information about the method.

The gate that matters is at the end. A bundled script is executable code that
ships with the skill, so a candidate is NOT a proposal to bundle - it is a
proposal to review. It goes through the skill contract's own script rules (no
network, no credentials, no installers, documented constants) and then to a human
or an external auditor. Never straight in.

    python3 extract_scripts.py <run1.md> <run2.md> [...] [--min-runs N] [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

FENCE = re.compile(r"```(?:python|py|bash|sh)?\n(.*?)```", re.S)
MIN_LINES = 3


def normalise(code: str) -> str:
    """Strip what varies between two writings of the same helper.

    Comments, blank lines, docstrings and leading indentation go; identifier
    names stay. Two runs that write the same function with different variable
    names are NOT the same helper - renaming is where a shared abstraction stops
    being shared, and collapsing that would over-report.
    """
    out = []
    for line in code.split("\n"):
        s = line.split("#")[0].rstrip()
        if not s.strip():
            continue
        out.append(s.strip())
    return "\n".join(out)


def blocks(text: str) -> list[str]:
    found = []
    for m in FENCE.finditer(text):
        code = m.group(1)
        if len([l for l in code.split("\n") if l.strip()]) >= MIN_LINES:
            found.append(code)
    return found


def signature(code: str) -> str:
    return hashlib.sha256(normalise(code).encode()).hexdigest()[:16]


def extract(paths: list[Path], min_runs: int = 2) -> dict:
    seen: dict[str, dict] = defaultdict(lambda: {"runs": set(), "example": None, "lines": 0})
    for p in paths:
        text = p.read_text(encoding="utf-8", errors="replace")
        for code in blocks(text):
            sig = signature(code)
            e = seen[sig]
            e["runs"].add(p.name)
            if e["example"] is None:
                e["example"] = code
                e["lines"] = len([l for l in code.split("\n") if l.strip()])
    candidates = [{"signature": s, "runs": sorted(e["runs"]), "n_runs": len(e["runs"]),
                   "lines": e["lines"], "code": e["example"]}
                  for s, e in seen.items() if len(e["runs"]) >= min_runs]
    candidates.sort(key=lambda c: (-c["n_runs"], -c["lines"]))
    return {
        "runs_examined": [p.name for p in paths],
        "min_runs": min_runs,
        "blocks_seen": sum(len(e["runs"]) for e in seen.values()),
        "candidates": candidates,
        "finding": (f"{len(candidates)} helper(s) written by at least {min_runs} independent runs"
                    if candidates else
                    f"NO helper was written by {min_runs} or more runs. That is a finding about the "
                    f"method, not an empty result: nothing here is scaffolding the method requires."),
        "next": ("A candidate is a proposal to REVIEW, never to bundle. A bundled script is "
                 "executable code that ships with the skill: run it through the skill contract's "
                 "script rules (no network, no credentials, no installers, documented constants) "
                 "and then past a reader who did not write it."),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--min-runs", type=int, default=2)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = extract([Path(p) for p in a.runs], a.min_runs)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    print(r["finding"])
    for c in r["candidates"]:
        print(f"\n  {c['signature']}  {c['n_runs']} run(s), {c['lines']} lines — {', '.join(c['runs'])}")
        print("  " + "\n  ".join(c["code"].strip().split("\n")[:6]))
    print("\n" + r["next"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
