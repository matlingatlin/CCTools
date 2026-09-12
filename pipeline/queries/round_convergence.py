#!/usr/bin/env python3
"""Why a field took N rounds - read off the ledger, not off a memory of the run.

The field ledger already records what each reader round found. Nobody read it
across rounds, so a field that took 7 rounds looked like diligence. Rendered
round over round on one build it was not: the same two defect CLASSES came back
every round on different instances, each fixed singly.

  r1  a claim is unquoted; directives to the reader in two sections
  r2  another claim still unquoted; three directives remain
  ...
  r6  two more unquoted paraphrases; another directive

That is not disagreement failing to converge. It is a class-level defect being
repaired one instance at a time, and the reader finding the next instance each
round. The fix is to sweep the class, not to answer the instance.

This tool names that pattern from the data. Four verdicts, never two:

  converging      findings shrink and rounds do not repeat each other
  recurring-class the same vocabulary comes back across rounds - whack-a-mole
  churn           every round raises new ground and the count is not falling
  indeterminate   too few rounds to say (never a pass)

    round_convergence.py [--ledger PATH] [--build ID] [--builds-dir DIR] [--json]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "pipeline" / "ledgers" / "fields.jsonl"
BUILDS = REPO / "pipeline" / "builds"

# Deliberately generic: identifiers, ordinals and digits are INSTANCE marks, and
# the class is what survives stripping them. That stripping is done by WORD
# alone - it requires three or more letter characters, so C10, r4, 62 and 4-5x
# never become vocabulary in the first place. An explicit identifier-scrubbing
# regex used to sit here too; removing it changed no output and failed no
# control, which is the definition of dead code dressed as a safeguard.
WORD = re.compile(r"[a-z][a-z-]{2,}")
STOP = {
    "the", "and", "for", "not", "was", "were", "are", "its", "it", "is", "of", "to", "in",
    "on", "a", "an", "that", "this", "with", "has", "have", "had", "but", "which", "while",
    "from", "one", "two", "three", "own", "still", "been", "than", "then", "there", "them",
    "they", "any", "all", "can", "cannot", "does", "did", "into", "out", "over", "same",
    "other", "another", "more", "most", "some", "such", "only", "also", "just", "yet",
}
MIN_ROUNDS = 2          # fewer than this cannot show a trend
RECUR_SIM = 0.25        # Jaccard between consecutive rounds that reads as repetition
RECUR_ROUNDS = 3        # a term in this many rounds is a class, not a coincidence


def stem(w: str) -> str:
    """Light stemming, because a class splits on plurals otherwise.

    One build's recurring class was 'directive': round 1 wrote 'directives',
    rounds 4 and 6 wrote 'a directive'. Unstemmed they are three tokens across
    two buckets and the class recurs in 2 rounds; stemmed it recurs in 3 and
    crosses the threshold. The word that names the class is exactly the word
    most likely to appear in both numbers.
    """
    if len(w) <= 4:
        return w
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("es"):
        # Strip the whole 'es' ONLY after a sibilant (boxes -> box, matches ->
        # match). Everywhere else the 'e' belongs to the stem, and taking it
        # splits the class rather than merging it: an earlier version mapped
        # 'directives' to 'directiv' while 'directive' stayed whole, so the one
        # word naming the recurring class landed in two buckets and the class
        # scored as not recurring.
        stem_ = w[:-2]
        if stem_.endswith(("s", "x", "z", "ch", "sh")):
            return stem_
        return w[:-1]
    if w.endswith("s") and not w.endswith(("ss", "sis", "us", "is")):
        return w[:-1]
    return w


def terms(text: str) -> set[str]:
    """A finding reduced to its class vocabulary, instance marks removed."""
    return {stem(w) for w in WORD.findall(text.lower()) if w not in STOP}


def parse_rounds(entries: list[str]) -> dict[int, list[str]]:
    """Ledger findings are prefixed 'rN: '. Anything unprefixed is round 1."""
    out: dict[int, list[str]] = collections.defaultdict(list)
    for e in entries:
        m = re.match(r"\s*r(\d+)\s*[:.]?\s*(.*)", str(e), re.I)
        if m:
            out[int(m.group(1))].append(m.group(2))
        else:
            out[1].append(str(e))
    return dict(out)


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a or b) else 0.0


def shaving(red_code: list[str]) -> dict | None:
    """A monotone numeric sequence creeping toward a limit.

    Approaching a cap in small decrements is the same instance-at-a-time habit
    in code-check form: the value was 50 over and each round removed 8.
    """
    for entry in red_code:
        nums = [float(x) for x in re.findall(r"\b(\d{2,6})\b", str(entry))]
        if len(nums) < 3:
            continue
        steps = [b - a for a, b in zip(nums, nums[1:])]
        if all(s < 0 for s in steps) and abs(steps[-1]) < abs(steps[0]):
            return {"sequence": nums, "steps": steps, "entry": str(entry)[:90],
                    "total_moved": nums[0] - nums[-1],
                    "note": ("each step is smaller than the last - an asymptotic approach to a "
                             "threshold, which costs a round per step")}
    return None


def analyse_field(row: dict, durations: list[float] | None = None) -> dict:
    rounds = parse_rounds(row.get("red_agent") or [])
    n = max(rounds) if rounds else 0
    per_round = {r: [terms(f) for f in fs] for r, fs in rounds.items()}
    counts = {r: len(fs) for r, fs in rounds.items()}

    out = {"build": row.get("build"), "field": row.get("field"),
           "rewrites": row.get("rewrites"), "rounds_with_findings": n,
           "findings_per_round": counts,
           "shaving": shaving(row.get("red_code") or [])}

    if n < MIN_ROUNDS:
        out["verdict"] = "indeterminate"
        out["reason"] = f"{n} round(s) of findings - too few to show a trend"
        return out

    # Consecutive-round repetition, measured FINDING to FINDING rather than
    # round to round. A union of every word in a round is diluted by everything
    # else it raised, so a round that repeats one of last round's findings
    # verbatim still scores near zero. What matters is whether ANY finding this
    # round restates one from last round; the strongest such pair is the signal.
    sims = []
    for k in range(2, n + 1):
        prev, cur = per_round.get(k - 1) or [], per_round.get(k) or []
        if not prev or not cur:
            continue
        sims.append(round(max(jaccard(a, b) for b in cur for a in prev), 3))
    out["consecutive_similarity"] = sims

    # which vocabulary keeps coming back, and in how many rounds
    seen = collections.Counter()
    for r, fs in per_round.items():
        for w in set().union(*fs) if fs else set():
            seen[w] += 1
    recurring = {w: c for w, c in seen.items() if c >= RECUR_ROUNDS}
    out["recurring_terms"] = dict(sorted(recurring.items(), key=lambda kv: -kv[1])[:12])

    ordered = [counts.get(k, 0) for k in range(1, n + 1)]
    # Non-increasing AND actually lower at the end. Flat is not falling: three
    # rounds raising two fresh findings each is churn, and an all(b <= a) test
    # called it convergence because nothing got worse.
    falling = (all(b <= a for a, b in zip(ordered, ordered[1:]))
               and len(ordered) >= 2 and ordered[-1] < ordered[0])

    if durations and len(durations) >= 3:
        out["duration_trend_s"] = [round(d, 0) for d in durations]
        out["slower_each_round"] = all(b >= a for a, b in zip(durations, durations[1:]))
        out["last_over_first"] = round(durations[-1] / durations[0], 2) if durations[0] else None

    hi_sim = sims and statistics.mean(sims) >= RECUR_SIM
    if recurring and (hi_sim or n >= RECUR_ROUNDS + 1):
        out["verdict"] = "recurring-class"
        top = ", ".join(list(out["recurring_terms"])[:5])
        out["reason"] = (f"{len(recurring)} term(s) recur across {RECUR_ROUNDS}+ rounds "
                         f"({top}). The rounds are answering instances of one class. "
                         f"Sweep the class instead of the instance the reader named.")
    elif falling and not hi_sim:
        out["verdict"] = "converging"
        out["reason"] = f"findings fall {ordered} and rounds do not repeat each other"
    else:
        out["verdict"] = "churn"
        out["reason"] = (f"findings {ordered} are not falling and rounds raise new ground - "
                         f"the field may be underspecified rather than badly written")
    return out


def round_durations(build: str, field: str, builds_dir: Path) -> list[float]:
    """Per-round wall clock, matched by the reader labels in the cost ledger."""
    p = Path(builds_dir) / build / "cost" / "measured.jsonl"
    if not p.is_file():
        return []
    key = field.replace("_", "").replace("bodysteps", "steps")[:5].lower()
    hits = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        lab = str(r.get("label") or "").lower()
        if "read." in lab and key in lab.replace("_", "") and r.get("duration_ms"):
            hits.append((lab, r["duration_ms"] / 1000))
    hits.sort(key=lambda x: x[0])
    return [d for _, d in hits]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", type=Path, default=LEDGER)
    ap.add_argument("--builds-dir", type=Path, default=BUILDS)
    ap.add_argument("--build", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not a.ledger.is_file():
        print(f"no field ledger at {a.ledger}", file=sys.stderr)
        return 2
    rows = [json.loads(l) for l in a.ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
    if a.build:
        rows = [r for r in rows if r.get("build") == a.build]
    if not rows:
        print("no ledger rows match", file=sys.stderr)
        return 2

    results = [analyse_field(r, round_durations(r.get("build", ""), r.get("field", ""), a.builds_dir))
               for r in rows]
    if a.json:
        print(json.dumps(results, indent=2))
        return 0

    order = {"recurring-class": 0, "churn": 1, "converging": 2, "indeterminate": 3}
    for r in sorted(results, key=lambda x: (order[x["verdict"]], -(x["rewrites"] or 0))):
        if r["verdict"] == "indeterminate" and not r["rewrites"]:
            continue
        print(f"\n{r['build']} · {r['field']}  [{r['verdict'].upper()}]  "
              f"{r['rewrites']} rewrite(s)")
        print(f"  {r['reason']}")
        if r.get("findings_per_round"):
            print(f"  findings per round: {r['findings_per_round']}")
        if r.get("consecutive_similarity"):
            print(f"  round-to-round repetition: {r['consecutive_similarity']}")
        if r.get("duration_trend_s"):
            tr = r["duration_trend_s"]
            tail = (f", last is {r['last_over_first']}x the first" if r.get("last_over_first") else "")
            print(f"  round durations (s): {tr}{tail}"
                  + ("  SLOWER EVERY ROUND" if r.get("slower_each_round") else ""))
        if r.get("shaving"):
            s = r["shaving"]
            print(f"  shaving: {s['sequence']} — moved {s['total_moved']:g} in "
                  f"{len(s['steps'])} steps, each smaller than the last")
    return 0


if __name__ == "__main__":
    sys.exit(main())
