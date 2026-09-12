#!/usr/bin/env python3
"""Controls for the helper extractor.

Two failures pull opposite ways and both are quiet:

  over-report - collapsing two DIFFERENT helpers into one candidate, which bundles
  code no run actually asked for; and

  under-report - missing that two runs wrote the same helper because one added a
  comment, which leaves the method demanding the same scaffolding forever.

The third control is the one that keeps it honest: finding nothing must be
reported as a FINDING about the method, not as an empty result.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_scripts as ex  # noqa: E402

R: list[tuple[bool, str]] = []


def check(ok, label, detail=""):
    R.append((ok, f"{label}{'  — ' + detail if detail and not ok else ''}"))


HELPER = '''```python
def split(text):
    out = []
    for chunk in text.split(";"):
        if chunk.strip():
            out.append(chunk.strip())
    return out
```'''

HELPER_COMMENTED = '''```python
# split a migration into statements
def split(text):
    out = []

    for chunk in text.split(";"):
        # skip blanks
        if chunk.strip():
            out.append(chunk.strip())
    return out
```'''

OTHER = '''```python
def tally(rows, key):
    counts = {}
    for r in rows:
        counts[key(r)] = counts.get(key(r), 0) + 1
    return counts
```'''

TINY = '''```python
x = 1
```'''


def files(tmp, *contents):
    out = []
    for i, c in enumerate(contents, 1):
        p = tmp / f"run{i}.md"
        p.write_text(f"## Q1\n\n{c}\n", encoding="utf-8")
        out.append(p)
    return out


def main() -> int:
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)

        r = ex.extract(files(tmp, HELPER, HELPER), 2)
        check(len(r["candidates"]) == 1 and r["candidates"][0]["n_runs"] == 2,
              "the same helper in two runs is one candidate", str(len(r["candidates"])))

        r = ex.extract(files(tmp / _mk(tmp, "b"), HELPER, HELPER_COMMENTED), 2)
        check(len(r["candidates"]) == 1,
              "comments and blank lines do not hide a repeated helper", str(len(r["candidates"])))

        r = ex.extract(files(tmp / _mk(tmp, "c"), HELPER, OTHER), 2)
        check(not r["candidates"],
              "two DIFFERENT helpers are not collapsed into one candidate",
              str([c["n_runs"] for c in r["candidates"]]))

        r = ex.extract(files(tmp / _mk(tmp, "d"), HELPER, OTHER), 1)
        check(len(r["candidates"]) == 2,
              "at min_runs=1 both appear — the clustering is by code, not by luck")

        r = ex.extract(files(tmp / _mk(tmp, "e"), HELPER), 2)
        check(not r["candidates"] and "NO helper" in r["finding"] and "finding about the" in r["finding"],
              "one run writing a helper is not a candidate, and nothing found is reported as a FINDING",
              r["finding"][:60])

        r = ex.extract(files(tmp / _mk(tmp, "f"), TINY, TINY), 2)
        check(not r["candidates"],
              "a two-line fragment is not a helper", str(len(r["candidates"])))

        r = ex.extract(files(tmp / _mk(tmp, "g"), HELPER, HELPER), 2)
        check("REVIEW" in r["next"] and "never to bundle" in r["next"],
              "the output says a candidate is a proposal to review, never to bundle")

    bad = [m for ok, m in R if not ok]
    for ok, m in R:
        if "-v" in sys.argv or not ok:
            print(f"{'ok   ' if ok else 'FAIL '} {m}")
    print(f"\n{len(R) - len(bad)}/{len(R)} controls behaved")
    return 1 if bad else 0


def _mk(tmp, name):
    (tmp / name).mkdir(exist_ok=True)
    return name


if __name__ == "__main__":
    sys.exit(main())
