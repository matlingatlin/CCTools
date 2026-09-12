#!/usr/bin/env python3
"""Generate a logged-traffic fixture with KNOWN ground truth, seeded."""
import csv, json, pathlib, random, hashlib
random.seed(20260902)

SLICES = [("simple_lookup", 0.80, 0.94), ("multi_hop", 0.15, 0.71),
          ("ambiguous", 0.04, 0.55), ("adversarial", 0.01, 0.28)]
N = 2000

TEMPLATES = [
    "what is the {} balance on my account",
    "how do i cancel the {} subscription",
    "when will the {} refund arrive",
    "reset the password for {}",
    "is {} covered by the warranty",
    "change my billing address to {}",
]
FILLERS = ["premium", "basic", "the annual", "my old", "the trial", "family",
           "student", "the legacy", "our team", "the pro"]

# Vocabulary for the non-templated rows. 23 x 19 x 29 x 17 combinations, so
# collisions are rare and every row keeps distinguishing WORDS after digits
# and hex ids are stripped.
SUBJECTS = ["the courier", "my accountant", "our warehouse", "the tenant", "a supplier",
            "the auditor", "my landlord", "our reseller", "the contractor", "a broker",
            "the pharmacy", "my dentist", "our installer", "the surveyor", "a locksmith",
            "the caterer", "my optician", "our printer", "the glazier", "a plumber",
            "the notary", "my physio", "our roofer"]
VERBS = ["cannot reconcile", "keeps rejecting", "wants to amend", "has disputed",
         "refuses to release", "is chasing", "double-charged", "never received",
         "wrongly flagged", "quietly cancelled", "cannot locate", "over-declared",
         "under-reported", "has escalated", "silently merged", "failed to lodge",
         "back-dated", "is withholding", "mis-stated"]
OBJECTS = ["the settlement note", "our quarterly return", "the delivery manifest",
           "a damaged pallet", "the tenancy schedule", "their credit memo",
           "the customs entry", "our retention bond", "a partial shipment",
           "the meter reading", "their commission split", "the disposal record",
           "our indemnity clause", "a returned consignment", "the warranty transfer",
           "their audit trail", "the escrow balance", "our freight surcharge",
           "a duplicate remittance", "the storage levy", "their handling fee",
           "the reinstatement cost", "our drawdown request", "a lapsed guarantee",
           "the salvage valuation", "their rebate accrual", "the demurrage claim",
           "our excess waiver", "a contested chargeback"]
QUALIFIERS = ["before the cutoff", "under the old terms", "since the merger",
              "against the wrong ledger", "without a signature", "for the second time",
              "outside the agreed window", "on the previous contract", "in a foreign currency",
              "after the handover", "with no supporting note", "despite the hold",
              "under protest", "ahead of the audit", "on a provisional basis",
              "through the wrong entity", "while the case is open"]

rows, dup_clusters = [], []
i = 0
# 6 near-duplicate clusters of 20 = 120 rows that differ only in one slot
for t_i, tmpl in enumerate(TEMPLATES):
    cluster = []
    for k in range(20):
        q = tmpl.format(FILLERS[k % len(FILLERS)])
        rows.append({"id": f"q{i:04d}", "query": q, "slice": "simple_lookup",
                     "correct": 1 if random.random() < 0.94 else 0})
        cluster.append(f"q{i:04d}"); i += 1
    dup_clusters.append({"cluster": f"D{t_i+1}", "template": tmpl, "ids": cluster})

# the rest, unique-ish, distributed across slices
while i < N:
    r = random.random(); acc = 0
    for name, share, p in SLICES:
        acc += share
        if r <= acc:
            sl, pc = name, p; break
    else:
        sl, pc = SLICES[0][0], SLICES[0][2]
    # Lexical content that SURVIVES normalisation. The first version wrote
    # f"{sl} case {i} {md5[:8]}", where every distinguishing character was a
    # digit or a hex id - so stripping those, which is what any dedup step
    # does, collapsed all 1647 simple_lookup rows into one string. The key
    # then punished a run that normalised correctly and agreed with one that
    # stopped at exact match. Found by a build's whole-artefact reviewer.
    h = int(hashlib.md5(str(i).encode()).hexdigest(), 16)
    q = " ".join([SUBJECTS[h % len(SUBJECTS)], VERBS[(h >> 8) % len(VERBS)],
                  OBJECTS[(h >> 16) % len(OBJECTS)], QUALIFIERS[(h >> 24) % len(QUALIFIERS)]])
    rows.append({"id": f"q{i:04d}", "query": q, "slice": sl,
                 "correct": 1 if random.random() < pc else 0})
    i += 1

random.shuffle(rows)
# 37 rows also appear verbatim in the few-shot prompt file -> contamination
contaminated = sorted(random.sample([r["id"] for r in rows], 37))
cset = set(contaminated)
for r in rows:
    r["in_fewshot_prompt"] = 1 if r["id"] in cset else 0

out = str(pathlib.Path(__file__).resolve().parent)
with open(f"{out}/logged_traffic.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["id", "query", "slice", "correct", "in_fewshot_prompt"])
    w.writeheader(); w.writerows(rows)

from collections import Counter
c = Counter(r["slice"] for r in rows)
truth = {
    "n_rows": len(rows),
    "slice_counts": dict(c),
    "slice_share": {k: round(v / len(rows), 4) for k, v in c.items()},
    "near_duplicate_clusters": len(dup_clusters),
    "near_duplicate_rows": sum(len(d["ids"]) for d in dup_clusters),
    "cluster_ids": {d["cluster"]: d["ids"] for d in dup_clusters},
    "contaminated_rows": len(contaminated),
    "contaminated_ids": contaminated,
    "accuracy_overall": round(sum(r["correct"] for r in rows) / len(rows), 4),
    "accuracy_by_slice": {k: round(sum(r["correct"] for r in rows if r["slice"] == k) /
                                   c[k], 4) for k in c},
    "expected_adversarial_in_random_200": round(200 * c["adversarial"] / len(rows), 2),
}
with open(f"{out}/ground_truth.json", "w") as fh:
    json.dump(truth, fh, indent=2)
print(json.dumps({k: v for k, v in truth.items()
                  if k not in ("cluster_ids", "contaminated_ids")}, indent=2))
