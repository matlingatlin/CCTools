#!/usr/bin/env python3
"""Positive controls for the round-convergence analyser.

The load-bearing case is the real one: the references field of
abstention-threshold-design-v2, six rounds, whose findings name two defect
classes over and over on different instances. If that does not come back
recurring-class, the tool cannot see the pattern it was built for.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from round_convergence import analyse_field, stem, terms, shaving, parse_rounds  # noqa: E402

FAILS = 0


def check(ok, label, detail=""):
    global FAILS
    if not ok:
        FAILS += 1
    print(f"{'ok  ' if ok else 'FAIL'} {label}{('  — ' + str(detail)) if detail and not ok else ''}")


# The real findings, verbatim from pipeline/ledgers/fields.jsonl.
REAL_REFS = [
    "r1: C1 8-10 percent read off a figure, used to derive 4-5x, not quoted",
    "r1: C10 alpha-as-input asserted without a quote",
    "r1: procedural directives to the reader in C10, C11 and the expiry section",
    "r2: C10 mechanism claim still unquoted and unmarked",
    "r2: three navigational directives remain (Use C2, definition to quote at anyone, Note the unit)",
    "r3: C6 attribution sentence carried as flat fact, unmarked",
    "r4: C4 Reuters line and C7 conditionality and 62 percent figures unmarked",
    "r4: but state it as one - a directive in the expiry section",
    "r4: C11 tagged MEASURED while its own Limits says no value is reported",
    "r5: C2 Bonferroni assertion and C8 white-box AUROC figures unmarked",
    "r5: the expiry bullet still instructs the reader to measure separation on their own signal",
    "r6: two unmarked paraphrases in C11 (the 90/10 illustration, the stratified diagnostics)",
    "r6: Treat C11 as a definition - a directive",
    "r6: C5 and C10 carry the same MEASURED tag mismatch as C11 and were not flagged",
]


def main() -> int:
    # 1. THE REAL CASE.
    r = analyse_field({"build": "b", "field": "references", "rewrites": 6,
                       "red_agent": REAL_REFS, "red_code": []})
    check(r["verdict"] == "recurring-class", "the real 6-round field reads as recurring-class",
          r["verdict"])
    check("directive" in r["recurring_terms"],
          "and it names 'directive' as a recurring class", list(r["recurring_terms"]))
    check("unmarked" in r["recurring_terms"],
          "and 'unmarked' too", list(r["recurring_terms"]))

    # 2. The stemmer must not split a class on its plural. This is the defect
    #    that hid 'directive' behind 'directives' until it was fixed.
    check(stem("directives") == stem("directive"), "directives and directive stem alike",
          f"{stem('directives')} vs {stem('directive')}")
    check(stem("figures") == stem("figure"), "figures and figure stem alike")
    check(stem("boxes") == "box", "a sibilant stem still loses the whole es")
    check(stem("matches") == "match", "matches -> match")
    check(stem("analysis") == "analysis", "analysis is not mangled into analysi")
    check(stem("its") == "its", "a short word is left alone")

    # 3. NEGATIVE CONTROL: a genuinely converging field must NOT be called
    #    recurring. Findings fall and no round restates the last.
    conv = ["r1: the heading order is wrong", "r1: a step has no observed failure behind it",
            "r2: the fixture path is absolute", "r3: a trailing space in the table"]
    r = analyse_field({"build": "b", "field": "f", "rewrites": 3,
                       "red_agent": conv, "red_code": []})
    check(r["verdict"] == "converging", "a field with falling, unrelated findings converges",
          r["verdict"])

    # 4. NEGATIVE CONTROL: one round of findings can never earn a verdict.
    r = analyse_field({"build": "b", "field": "f", "rewrites": 1,
                       "red_agent": ["r1: something"], "red_code": []})
    check(r["verdict"] == "indeterminate", "one round is indeterminate, never a pass",
          r["verdict"])
    r = analyse_field({"build": "b", "field": "f", "rewrites": 0,
                       "red_agent": [], "red_code": []})
    check(r["verdict"] == "indeterminate", "no findings at all is indeterminate")

    # 5. Churn: findings do not fall and rounds raise new ground each time.
    churn = ["r1: a", "r1: b", "r2: totally different thing here",
             "r2: another unrelated matter", "r3: yet more unconnected material",
             "r3: and something else again entirely"]
    r = analyse_field({"build": "b", "field": "f", "rewrites": 3,
                       "red_agent": churn, "red_code": []})
    check(r["verdict"] in ("churn", "recurring-class"),
          "non-falling findings are not called converging", r["verdict"])

    # 6. Shaving: a monotone approach to a cap in ever-smaller steps.
    s = shaving(["desc.max 1076 -> 1068 -> 1050 -> 1035 -> 1030 -> 1028"])
    check(s is not None, "an asymptotic approach to a threshold is detected")
    check(s and s["total_moved"] == 48, "and it reports how far the value actually moved",
          s and s["total_moved"])
    check(shaving(["desc.max 1076 -> 900"]) is None,
          "two values are not enough to call it shaving")
    check(shaving(["nothing numeric here"]) is None, "prose without numbers is not shaving")

    # 7. Round parsing: an unprefixed finding belongs to round 1, not to nowhere.
    p = parse_rounds(["no prefix here", "r2: later"])
    check(p.get(1) == ["no prefix here"], "an unprefixed finding lands in round 1", p)
    check(p.get(2) == ["later"], "and a prefixed one in its own round", p)

    # 8. Instance marks must not become class vocabulary, or every round would
    #    look unique and nothing would ever recur. Asserted on the properties
    #    themselves rather than on one pair, because a pair that differs only in
    #    an identifier passes even when the scrubbing does nothing at all.
    t1, t2 = terms("C10 alpha asserted"), terms("C11 alpha asserted")
    check(t1 == t2, "two findings differing only in identifier reduce alike", f"{t1} vs {t2}")
    v = terms("C10 and r4 saw 62 percent and a 4-5x lift in the figures")
    check(not any(any(ch.isdigit() for ch in w) for w in v),
          "no token carrying a digit survives into the vocabulary", sorted(v))
    check("figure" in v and "percent" in v, "while the class words do survive", sorted(v))

    print(f"\n{'PASS' if FAILS == 0 else 'FAIL'}: {FAILS} failing check(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
