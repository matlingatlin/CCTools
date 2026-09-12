#!/usr/bin/env python3
"""Code check for the references field: every quote in the file must be BYTE-IDENTICAL
to the package's `quote` string, and every claim must be present.

A reader asked to verify 13 quotes by eye is a reader spending its judgement on
something a script decides in milliseconds. This is that script.
"""
import json, re, sys, unicodedata
from pathlib import Path

pkg = json.loads(Path("/home/user/skills-repo/pipeline/packages/data-contract-assertions-v2.json").read_text())
ref = Path(sys.argv[1]).read_text()

def norm(s):
    # only whitespace collapse - NOT punctuation, which is what would hide a paraphrase
    return re.sub(r"\s+", " ", s).strip()

body = norm(ref)
bad, missing_claim, missing_date, ok = [], [], [], 0
for c in pkg["claims"]:
    q = norm(c["quote"])
    if q in body:
        ok += 1
    else:
        # is a MUTILATED version present? find the longest prefix that matches
        lo, hi = 0, len(q)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if q[:mid] in body: lo = mid
            else: hi = mid - 1
        bad.append((c["claim_id"], lo, q[:lo][-60:] if lo else "", q[lo:lo+60]))
    if c["claim_id"] not in ref:
        missing_claim.append(c["claim_id"])
for s in pkg["sources"]:
    if s["fetched"] not in ref:
        missing_date.append(s["source_id"])

# forbidden: an invented magnitude threshold stated as advice
invented = re.findall(r"(?i)\b(?:warn|alert|page|threshold|band|cutoff)\b[^.\n]{0,40}?\b0\.\d+\b", ref)

print(f"quotes byte-matched: {ok}/{len(pkg['claims'])}")
for cid, n, tail, rest in bad:
    print(f"  [E] {cid}: quote diverges after {n} chars. matched ...{tail!r} | package continues {rest!r}")
if missing_claim: print(f"  [E] claim ids absent from the file: {missing_claim}")
if missing_date: print(f"  [E] sources with no fetch date in the file: {missing_date}")
if invented: print(f"  [?] magnitude-threshold-shaped phrases to read in context: {invented[:6]}")
print("VERDICT:", "RED" if (bad or missing_claim or missing_date) else "GREEN")
sys.exit(1 if (bad or missing_claim or missing_date) else 0)
