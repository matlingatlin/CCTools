#!/usr/bin/env python3
"""Positive controls for the package admission gate.

A checker that cannot fail proves nothing. This file takes one package that the
gate admits cleanly, breaks exactly one thing in it, and asserts that the rule
which owns that thing is the one that turns red.

It asserts three things per case, and the third is the one that catches
over-reach:

  1. the named rule FAILS,
  2. it fails for the reason the case planted, not incidentally,
  3. no OTHER rule changes verdict unless the case declared it as collateral.

Point 3 is why the fixture is realistic rather than minimal: a rule that reads
fields it does not own shows up here as an undeclared change, which is how the
skill checker's three over-strict rules were found.

There is also a coverage gate on the selftest itself: every rule the contract
marks `check: code` must be the subject of at least one case, or this exits 2.
A rule with no control is an untested rule.

    python3 pipeline/validate/selftest_package.py
    python3 pipeline/validate/selftest_package.py -v

Exit 0 = all controls behaved. 1 = a control failed. 2 = a rule has no control.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import package_contract as pc  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "valid-package.json"


# --- mutations ---------------------------------------------------------------
# Each takes the clean package and breaks ONE thing.

def drop(field):
    def m(p):
        p.pop(field, None)
    return m


def set_(field, value):
    def m(p):
        p[field] = value
    return m


CASES = [
    # id, mutation, expected-failing rule, collateral rules allowed to change
    ("id absent", drop("id"), "pkg.id.present", ["pkg.id.kebab"]),
    ("id not kebab", set_("id", "Migration_Review"), "pkg.id.kebab", []),

    ("sentence absent", drop("candidate_sentence"), "pkg.sentence.present", ["pkg.sentence.single"]),
    ("sentence is a topic, not a scope", set_("candidate_sentence", "Reviews migrations."),
     "pkg.sentence.single", []),
    ("sentence is a paragraph",
     set_("candidate_sentence", "Reviews a database migration script and names the irreversible statements. "
                                "It also proposes a rollback plan for each one it finds."),
     "pkg.sentence.single", []),

    ("wrong builder", set_("unit_type", "agent"), "pkg.unit_type", []),
    ("content_kind outside the taxonomy", set_("content_kind", "narrative"), "pkg.content_kind", []),
    ("verifiable is a word, not a boolean", set_("verifiable", "yes"), "pkg.verifiable", []),
    ("failure_kind outside the three", set_("failure_kind", "vibes"), "pkg.failure_kind", []),
    ("failure_kind is discipline", set_("failure_kind", "discipline"),
     "pkg.failure_kind.not_discipline", []),

    ("no sources", set_("sources", []), "pkg.sources.present",
     ["pkg.sources.fields", "pkg.sources.fetched_iso", "pkg.sources.ids_unique",
      "pkg.claims.source_resolves"]),
    ("a source was found but not opened",
     lambda p: p["sources"][0].pop("read"), "pkg.sources.fields", []),
    ("fetched date is prose", lambda p: p["sources"][0].update(fetched="late August 2026"),
     "pkg.sources.fetched_iso", []),
    # Collateral is real here, not over-reach: renaming S2 to S1 removes S2 from
    # the source set, so the claim that cited it is genuinely left dangling.
    ("two sources share an id", lambda p: p["sources"][1].update(source_id="S1"),
     "pkg.sources.ids_unique", ["pkg.claims.source_resolves"]),

    ("no claims", set_("claims", []), "pkg.claims.present",
     ["pkg.claims.rows_not_prose", "pkg.claims.quote", "pkg.claims.source_resolves",
      "pkg.claims.locator", "pkg.claims.verdict", "pkg.claims.measured_needs_evidence"]),
    ("a claim arrived as prose",
     lambda p: p["claims"].__setitem__(0, "Renames cannot be rolled back once readers resolve the new name."),
     "pkg.claims.rows_not_prose", []),
    ("a claim with no verbatim line", lambda p: p["claims"][0].pop("quote"), "pkg.claims.quote", []),
    ("a claim points at a source that is not listed",
     lambda p: p["claims"][0].update(source_id="S9"), "pkg.claims.source_resolves", []),
    ("nobody recorded where they looked", lambda p: p["claims"][0].pop("locator"),
     "pkg.claims.locator", []),
    ("a verdict outside the two", lambda p: p["claims"][0].update(verdict="PROBABLY"),
     "pkg.claims.verdict", []),
    ("MEASURED with no number",
     lambda p: [p["claims"][1].pop("effect_size"), p["claims"][1].pop("sample")],
     "pkg.claims.measured_needs_evidence", []),

    ("the probe has no hypothesis", drop("expected_failure"), "pkg.expected_failure", []),
    ("too few trigger terms", lambda p: p.__setitem__("trigger_terms", p["trigger_terms"][:2]),
     "pkg.trigger_terms", []),

    ("one task cannot separate systematic from draw",
     lambda p: p.__setitem__("representative_tasks", p["representative_tasks"][:1]),
     "pkg.tasks.min", ["pkg.tasks.kinds"]),  # one task: kinds cannot be compared, INDET
    ("a task with nothing to score",
     lambda p: p["representative_tasks"][0].pop("artifact_expected"), "pkg.tasks.fields", []),
    ("every task runs on one kind of fixture and nobody says why",
     lambda p: [t.__setitem__("fixture_kind", "skill bundle") for t in p["representative_tasks"]],
     "pkg.tasks.kinds", []),
    ("a task with no fixture_kind at all",
     lambda p: p["representative_tasks"][0].pop("fixture_kind"), "pkg.tasks.kinds", []),

    ("budget is prose", lambda p: p["budget"].update(max_agents="two"), "pkg.budget", []),
    ("no decision rule before the measurement", set_("threshold", "   "), "pkg.threshold", []),

    # --- origin, and the one rule that keeps an artefact from vouching for itself
    ("an origin outside the five", set_("origin", "somewhere"), "pkg.origin", []),
    ("origin absent", drop("origin"), "pkg.origin", []),
    ("nobody named as having filled it in", drop("filled_by"), "pkg.origin.filled_by", []),
    ("gap_kind outside the three", set_("gap_kind", "vibes"), "pkg.gap_kind", []),
    ("gap_kind absent, so the improvement case cannot be stated",
     drop("gap_kind"), "pkg.gap_kind", []),

    # A finished skill citing itself. It looks like a well-sourced package: every
    # claim has a quote, every quote is verbatim, every source resolves. The
    # quotes are just the artefact's own assertions, which is the substitution
    # the quote gate exists to prevent.
    ("an incoming artefact cited as evidence for its own claims",
     lambda p: [p.__setitem__("origin", "existing-artifact"),
                p.__setitem__("incoming_artifact", "old-skill/SKILL.md"),
                p["sources"].append({"source_id": "SELF", "type": "incoming-artifact",
                                     "url": "file://old-skill/SKILL.md", "fetched": "2026-09-01",
                                     "access": "local", "read": "full"}),
                p["claims"].append({"claim": "FIXTURE. The skill says migrations need review.",
                                    "quote": "FIXTURE. Migrations need review.",
                                    "source_id": "SELF", "locator": "body",
                                    "verdict": "REPEATED"})],
     "pkg.claims.not_from_artifact", []),
]

# A control that must change NOTHING. It proves the diff above can tell
# "caught it" from "everything is always red", and that an unknown field is
# carried rather than rejected.
NOOP = ("an unrecognised field is carried, not rejected",
        set_("_provenance", "added by the harvest step"))


def verdicts(pkg, contract) -> dict[str, str]:
    return {r["id"]: r["verdict"] for r in pc.admit(pkg, contract)}


def _vocabulary_gate() -> list[str]:
    """The verdict vocabulary is OWNED by the claims contract, not copied here.

    It was written in both places. Adding DERIVED to one left the other behind,
    and admission refused a package whose claims the claims checker had just
    accepted - two gates disagreeing about a word because the word existed
    twice. Gated rather than merely checked, because a divergence here makes
    every downstream verdict unreliable rather than one case wrong.
    """
    repo = Path(__file__).resolve().parents[2]
    cc = json.loads((repo / "pipeline" / "contracts" / "claims.contract.json")
                    .read_text(encoding="utf-8"))
    declared = set(cc.get("verdicts") or ())
    if not declared:
        return ["the claims contract declares no verdict vocabulary at all"]
    allowed = pc._allowed_verdicts()
    if allowed != declared:
        return [f"admission allows {sorted(allowed)} while the claims contract declares "
                f"{sorted(declared)} - the vocabulary is written in two places again"]
    return []


def main() -> int:
    verbose = "-v" in sys.argv
    contract = pc.load_contract()

    # The other direction. coverage_gate catches a declared rule with no code;
    # this catches code with no declaration, which is never called at all
    # because the checker iterates the contract. Ungated on all three contracts
    # until 2026-09-02, when a rule added to a checker alone ran zero times and
    # every suite still reported each rule controlled.
    drift = _vocabulary_gate()
    if drift:
        print("ABORT — " + "; ".join(drift), file=sys.stderr)
        return 2

    orphans = pc.orphan_gate(contract)
    if orphans:
        print("ABORT — implemented but undeclared, so never run: " + ", ".join(orphans),
              file=sys.stderr)
        return 2
    missing = pc.coverage_gate(contract)
    if missing:
        print("ABORT — the engine does not implement:", ", ".join(missing), file=sys.stderr)
        return 2

    code_rules = [r["id"] for r in contract["rules"] if r.get("check") == "code"]
    uncontrolled = [r for r in code_rules if r not in {c[2] for c in CASES}]
    if uncontrolled:
        print("ABORT — rules with no positive control:", file=sys.stderr)
        for r in uncontrolled:
            print(f"  {r}", file=sys.stderr)
        return 2

    clean = json.loads(FIXTURE.read_text(encoding="utf-8"))
    base = verdicts(clean, contract)
    bad_base = {k: v for k, v in base.items() if v != pc.PASS}
    if bad_base:
        print(f"FAIL  the fixture itself is not clean: {bad_base}")
        return 1

    failures = 0

    name, mutate = NOOP
    p = copy.deepcopy(clean)
    mutate(p)
    changed = {k for k, v in verdicts(p, contract).items() if v != base[k]}
    if changed:
        print(f"FAIL  [no-op] {name}: changed {sorted(changed)}")
        failures += 1
    elif verbose:
        print(f"ok    [no-op] {name}")

    for name, mutate, expected, collateral in CASES:
        p = copy.deepcopy(clean)
        mutate(p)
        got = verdicts(p, contract)

        if got.get(expected) != pc.FAIL:
            print(f"FAIL  {name}: expected {expected} to FAIL, got {got.get(expected)}")
            failures += 1
            continue

        allowed = {expected, *collateral}
        surprises = sorted(k for k, v in got.items() if v != base[k] and k not in allowed)
        if surprises:
            print(f"FAIL  {name}: {expected} caught it, but these also changed "
                  f"and were not declared: {surprises}")
            failures += 1
            continue

        if verbose:
            extra = f"  (+{len(collateral)} collateral)" if collateral else ""
            print(f"ok    {name} -> {expected}{extra}")

    total = len(CASES) + 1
    print(f"\n{total - failures}/{total} controls behaved · "
          f"{len(code_rules)} code rules, all controlled")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
