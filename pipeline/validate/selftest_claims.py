#!/usr/bin/env python3
"""Positive controls for the fetched-claim gate.

Same shape as the other two: one clean fixture, one planted defect at a time,
each case asserting the owning rule turns red AND that no other rule changes
unless the case declared it. Coverage gate on the selftest itself - a rule with
no control aborts.

The two cases that carry the most weight are the ones a well-formed claim set
passes anyway: a claim verified by whoever gathered it, and a claim that failed
verification and was adopted regardless. Both leave a file that looks complete.

    python3 selftest_claims.py [-v]
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claims_contract as cc  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "valid-claims.json"


def drop(field):
    def m(d): d.pop(field, None)
    return m


CASES = [
    ("claims are prose, not rows", lambda d: d.__setitem__("claims", ["a paragraph about locks"]),
     "cl.rows", ["cl.quote", "cl.locator", "cl.source_resolves", "cl.verdict",
                 "cl.measured_evidence", "cl.verified", "cl.verifier_not_gatherer",
                 "cl.unsupported_dropped", "cl.reach_vs_read", "cl.contradictions_kept"]),
    ("a claim with no verbatim line", lambda d: d["claims"][0].pop("quote"), "cl.quote", []),
    ("nobody recorded where they looked", lambda d: d["claims"][0].pop("locator"), "cl.locator", []),
    ("a claim points at a source that is not listed",
     lambda d: d["claims"][0].update(source_id="F9"), "cl.source_resolves", ["cl.reach_vs_read"]),
    ("a verdict outside the three", lambda d: d["claims"][0].update(verdict="PROBABLY"),
     "cl.verdict", ["cl.measured_evidence"]),
    # DERIVED is neither measured nor repeated: a figure computed from assumed
    # parameters. It is admissible, and only if it says what it assumed - a
    # computed number whose assumptions are unstated reads as a measured one.
    ("DERIVED without naming its assumption",
     lambda d: d["claims"][0].update(verdict="DERIVED", claim="the floor is about 1000 questions"),
     "cl.derived_names_its_assumption", ["cl.measured_evidence"]),
    ("MEASURED with no number",
     lambda d: [d["claims"][0].pop("effect_size"), d["claims"][0].pop("sample")],
     "cl.measured_evidence", []),

    ("a fetched claim nobody ruled on", lambda d: d["claims"][0].pop("verification"),
     "cl.verified", ["cl.verifier_not_gatherer", "cl.unsupported_dropped"]),
    ("verified by whoever gathered it",
     lambda d: d["claims"][0]["verification"].update(by=d["claims"][0]["gathered_by"]),
     "cl.verifier_not_gatherer", []),
    ("a claim that failed verification, adopted anyway",
     lambda d: d["claims"][2].update(adopted=True), "cl.unsupported_dropped", []),

    ("a source that does not say how much was read",
     lambda d: d["sources"][0].pop("read"), "cl.reach_vs_read", []),
    ("MEASURED resting on an abstract-only source",
     lambda d: d["claims"][0].update(source_id="F2"), "cl.reach_vs_read", []),
    ("a source with no fetch date", lambda d: d["sources"][0].update(fetched="recently"),
     "cl.dated", []),
    # Collateral is real, not over-reach: renaming F2 to F1 removes F2 from the
    # source set, so the claim citing it is genuinely orphaned.
    ("two sources share an id", lambda d: d["sources"][1].update(source_id="F1"),
     "cl.no_dup_source_ids", ["cl.reach_vs_read", "cl.source_resolves"]),

    ("one side of a contradiction was dropped",
     lambda d: d.__setitem__("claims", [c for c in d["claims"] if c.get("claim_id") != "G2"]),
     "cl.contradictions_kept", []),
    ("no coverage list at all", drop("coverage"), "cl.coverage_answered", []),
    ("an observed failure with no covered verdict",
     lambda d: d["coverage"][0].pop("covered"), "cl.coverage_answered", []),
]

NOOP = ("an unrecognised field is carried, not rejected",
        lambda d: d.__setitem__("_provenance", "added by the gather step"))


def verdicts(d, contract):
    return {r["id"]: r["verdict"] for r in cc.check(d, contract)}


def main() -> int:
    verbose = "-v" in sys.argv
    contract = cc.load_contract()
    # The other direction. coverage_gate catches a declared rule with no code;
    # this catches code with no declaration, which is never called at all
    # because the checker iterates the contract. Ungated on all three contracts
    # until 2026-09-02, when a rule added to a checker alone ran zero times and
    # every suite still reported each rule controlled.
    orphans = cc.orphan_gate(contract)
    if orphans:
        print("ABORT — implemented but undeclared, so never run: " + ", ".join(orphans),
              file=sys.stderr)
        return 2
    missing = cc.coverage_gate(contract)
    if missing:
        print("ABORT — engine does not implement: " + ", ".join(missing), file=sys.stderr)
        return 2
    code_rules = [r["id"] for r in contract["rules"] if r.get("check") == "code"]
    uncontrolled = [r for r in code_rules if r not in {c[2] for c in CASES}]
    if uncontrolled:
        print("ABORT — rules with no positive control: " + ", ".join(uncontrolled), file=sys.stderr)
        return 2

    clean = json.loads(FIXTURE.read_text(encoding="utf-8"))
    base = verdicts(clean, contract)
    bad_base = {k: v for k, v in base.items() if v != cc.PASS}
    if bad_base:
        print(f"FAIL  the fixture itself is not clean: {bad_base}")
        return 1

    failures = 0
    name, mut = NOOP
    p = copy.deepcopy(clean); mut(p)
    changed = {k for k, v in verdicts(p, contract).items() if v != base[k]}
    if changed:
        print(f"FAIL  [no-op] {name}: changed {sorted(changed)}"); failures += 1
    elif verbose:
        print(f"ok    [no-op] {name}")

    for label, mut, expected, collateral in CASES:
        p = copy.deepcopy(clean); mut(p)
        got = verdicts(p, contract)
        if got.get(expected) != cc.FAIL:
            print(f"FAIL  {label}: expected {expected} to FAIL, got {got.get(expected)}")
            failures += 1; continue
        allowed = {expected, *collateral}
        surprises = sorted(k for k, v in got.items() if v != base[k] and k not in allowed)
        if surprises:
            print(f"FAIL  {label}: {expected} caught it, but these also changed and were "
                  f"not declared: {surprises}")
            failures += 1; continue
        if verbose:
            print(f"ok    {label} -> {expected}" + (f"  (+{len(collateral)} collateral)" if collateral else ""))

    total = len(CASES) + 1
    print(f"\n{total - failures}/{total} controls behaved · {len(code_rules)} code rules, all controlled")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
