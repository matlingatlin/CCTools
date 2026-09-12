#!/usr/bin/env python3
"""Two snapshots of one feed, with KNOWN defects injected into the second.

The point of the fixture is that not every change is a defect. Three of the
six differences below are real quality faults that should block ingest; three
are legitimate evolution that a contract which blocks on any change would
also stop, and stopping them is the failure mode this fixture exists to catch.
"""
import csv, json, pathlib, random

random.seed(20260902)
OUT = pathlib.Path(__file__).resolve().parent
N_REF, N_CUR = 4000, 4000

MERCHANTS = ["northwind", "acme-parts", "belltower", "cascade-foods", "dunmore",
             "eastgate", "fairweather", "greenline"]
CHANNELS = ["web", "ios", "android", "phone"]
STATUS = ["settled", "pending", "refunded"]


def base(n, seed_off=0):
    rows = []
    for i in range(n):
        rows.append({
            "txn_id": f"T{seed_off + i:06d}",
            "merchant": random.choice(MERCHANTS),
            "channel": random.choices(CHANNELS, weights=[52, 26, 20, 2])[0],
            "amount": round(random.lognormvariate(3.4, 0.8), 2),
            "currency": "USD",
            "status": random.choices(STATUS, weights=[86, 11, 3])[0],
            "customer_age": random.choice([None] + list(range(18, 79))),
            "settled_days": random.choices([0, 1, 2, 3], weights=[60, 28, 9, 3])[0],
        })
    return rows


ref = base(N_REF)
cur = base(N_CUR, seed_off=N_REF)

# --- THREE REAL DEFECTS ------------------------------------------------------
for r in cur:                                   # D1 silent unit change, one merchant
    if r["merchant"] == "belltower":
        r["amount"] = round(r["amount"] * 100, 2)
for r in cur:                                   # D2 null rate jump, one channel
    if r["channel"] == "android" and random.random() < 0.82:
        r["customer_age"] = None
for r in cur:                                   # D3 type drift
    if random.random() < 0.30:
        r["settled_days"] = f"{r['settled_days']} d"

# --- THREE BENIGN CHANGES ----------------------------------------------------
for r in random.sample(cur, 240):               # B1 a real onboarding
    r["merchant"] = "harborview"
for r in cur:                                   # B2 channel mix shift
    if r["channel"] == "web" and random.random() < 0.22:
        r["channel"] = "ios"
for r in random.sample(cur, 90):                # B3 a documented new state
    r["status"] = "chargeback"

FIELDS = list(ref[0])
for name, rows in (("reference.csv", ref), ("current.csv", cur)):
    with open(OUT / name, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows([{k: ("" if v is None else v) for k, v in r.items()} for r in rows])

import statistics as st
nr = lambda rows, ch: round(sum(1 for r in rows if r["channel"] == ch
                                and r["customer_age"] in (None, "")) /
                            max(1, sum(1 for r in rows if r["channel"] == ch)), 4)
med = lambda rows, m: round(st.median([float(r["amount"]) for r in rows
                                       if r["merchant"] == m]), 2)
allmed = lambda rows: round(st.median([float(r["amount"]) for r in rows]), 2)

truth = {
  "n_reference": len(ref), "n_current": len(cur), "columns": FIELDS,
  "REAL_DEFECTS_THAT_SHOULD_BLOCK": {
    "D1_unit_change_amount": {
      "column": "amount", "scope": "merchant == belltower only",
      "what": "values multiplied by 100 - the feed switched to cents for one merchant",
      "segment_median_reference": med(ref, "belltower"),
      "segment_median_current": med(cur, "belltower"),
      "whole_column_median_reference": allmed(ref),
      "whole_column_median_current": allmed(cur),
      "why_it_blocks": "a silent unit change is unrecoverable downstream and invisible in a "
                       "whole-column statistic because it is confined to one segment",
      "rows_affected": sum(1 for r in cur if r["merchant"] == "belltower")},
    "D2_null_rate_jump_customer_age": {
      "column": "customer_age", "scope": "channel == android",
      "scoped_null_rate_reference": nr(ref, "android"),
      "scoped_null_rate_current": nr(cur, "android"),
      "why_it_blocks": "a field going missing for one channel is a broken producer, not evolution"},
    "D3_type_drift_settled_days": {
      "column": "settled_days",
      "non_numeric_rows_current": sum(1 for r in cur if not str(r["settled_days"]).isdigit()),
      "what": "about 30 percent of values arrive as a string with a unit suffix, e.g. '2 d'",
      "why_it_blocks": "the column stops being numeric and silently coerces or drops downstream"}},
  "BENIGN_CHANGES_THAT_MUST_NOT_BLOCK": {
    "B1_new_merchant": {"column": "merchant", "new_value": "harborview", "rows": 240,
                        "why_benign": "a real onboarding; the contract should widen, not refuse"},
    "B2_channel_mix_shift": {"column": "channel",
                             "what": "web share falls and ios rises, same value set",
                             "why_benign": "a marketing push. Distribution change with no quality "
                                           "fault, and the case a drift test flags loudest"},
    "B3_new_status_value": {"column": "status", "new_value": "chargeback", "rows": 90,
                            "why_benign": "a documented new state, not a corruption"}},
  "THE_TEST": ("A contract that blocks all six has not solved the problem, it has moved it. A "
               "contract that blocks none is decoration. D1 is the hard one: it is confined to "
               "one segment and a whole-column check cannot see it."),
  "_verified": "Every figure here is computed from the rows as they are written, in this file.",
}
(OUT / "ground_truth.json").write_text(json.dumps(truth, indent=2) + "\n")
print(json.dumps(truth["REAL_DEFECTS_THAT_SHOULD_BLOCK"], indent=2))
