#!/usr/bin/env python3
"""Bundled knowledge goes stale, and nothing in the runtime will ever say so.

Every reference file in this library carries fetch dates because a date is the
only mechanism we get. But a date nobody reads is a date that does nothing, and
until now nothing read them.

This is deliberately not a pass/fail gate. Age is not a defect: a paper from 2023
about a measured effect may be perfectly current, and a vendor doc from last month
may already be wrong. So it reports AGE and the EXPIRY CONDITION where one was
written, and refuses to convert the first into a verdict.

What it does assert is the thing that is decidable: a claim with no date at all
cannot be checked for staleness by anyone, ever. That is a defect, and it is
reported as one.

    python3 staleness.py [--root DIR] [--days N] [--json]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATE = re.compile(r"\b((?:19|20)\d{2})-(\d{2})-(\d{2})\b")
EXPIRY_HINT = re.compile(r"expir|goes stale|no longer|until|re-?check|as of|superseded", re.I)


def scan(root: Path, warn_days: int) -> dict:
    today = dt.date.today()
    files, undated = [], []
    for p in sorted(root.rglob("references/*.md")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        dates = sorted({dt.date(int(a), int(b), int(c)) for a, b, c in DATE.findall(txt)})
        rel = str(p.relative_to(root))
        if not dates:
            undated.append(rel)
            continue
        oldest, newest = dates[0], dates[-1]
        files.append({
            "file": rel,
            "oldest": oldest.isoformat(), "newest": newest.isoformat(),
            "age_days_oldest": (today - oldest).days,
            "age_days_newest": (today - newest).days,
            "has_expiry_condition": bool(EXPIRY_HINT.search(txt)),
            "over_warn": (today - oldest).days >= warn_days,
        })
    files.sort(key=lambda f: -f["age_days_oldest"])
    return {
        "root": str(root), "today": today.isoformat(), "warn_days": warn_days,
        "files": files, "undated": undated,
        "no_expiry_condition": [f["file"] for f in files if not f["has_expiry_condition"]],
        "principle": ("Age is reported, never converted into a verdict: a 2023 paper on a measured "
                      "effect may be current and a vendor page from last month may already be "
                      "wrong. What IS a defect is a reference with no date, because nobody can ever "
                      "check it for staleness."),
    }


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--root", default=str(REPO / ".claude" / "skills"))
    a.add_argument("--days", type=int, default=365)
    a.add_argument("--json", action="store_true")
    args = a.parse_args()
    r = scan(Path(args.root), args.days)
    if args.json:
        print(json.dumps(r, indent=2))
        return 1 if r["undated"] else 0
    print(f"{len(r['files'])} dated reference file(s) · {len(r['undated'])} undated · "
          f"warn at {args.days} days\n")
    for f in r["files"][:12]:
        mark = "!" if f["over_warn"] else " "
        exp = "" if f["has_expiry_condition"] else "   (no expiry condition written)"
        print(f"  [{mark}] {f['age_days_oldest']:>4}d  {f['file']}{exp}")
    if r["undated"]:
        print("\nDEFECT — no date at all, so staleness can never be checked:")
        for u in r["undated"]:
            print(f"      {u}")
    print(f"\n{r['principle']}")
    return 1 if r["undated"] else 0


if __name__ == "__main__":
    sys.exit(main())
