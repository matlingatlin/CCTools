#!/usr/bin/env python3
"""Positive controls for the chain-contract coverage gate.

The gate's whole value is refusing a rule that says nothing about how it is
held. If a rule with neither enforced_by nor convention passes, the gate is
decoration - and every rule in the real contract passed that way until it
existed, including two that predated the evening's work.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chain_contract import coverage_gate, rule_blocks, check_block, PASS, FAIL  # noqa: E402

FAILS = 0
REPO = Path(__file__).resolve().parents[2]


def check(ok, label, detail=""):
    global FAILS
    if not ok:
        FAILS += 1
    print(f"{'ok  ' if ok else 'FAIL'} {label}{('  — ' + str(detail)) if detail and not ok else ''}")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "real.py").write_text("# exists\n")

        # 1. THE DEFECT. A rule stating nothing about enforcement must FAIL.
        r = check_block("x", {"rule": "do the thing"}, tmp)
        check(r["verdict"] == FAIL, "a bare rule is unaccounted for", r)

        # 2. enforced_by pointing at a real path passes.
        r = check_block("x", {"rule": "r", "enforced_by": "real.py"}, tmp)
        check(r["verdict"] == PASS, "enforced_by an existing path passes", r)

        # 3. enforced_by pointing at nothing FAILS - naming a file that does not
        #    exist is how a rule looks enforced while being held by no one.
        r = check_block("x", {"rule": "r", "enforced_by": "ghost.py"}, tmp)
        check(r["verdict"] == FAIL, "enforced_by a missing path fails", r)

        # 4. A convention must say WHY, or it is indistinguishable from a rule
        #    nobody got round to enforcing.
        r = check_block("x", {"rule": "r", "convention": True}, tmp)
        check(r["verdict"] == FAIL, "a convention with no reason fails", r)
        r = check_block("x", {"rule": "r", "convention": True,
                              "why_no_gate": "dispatch has no hook"}, tmp)
        check(r["verdict"] == PASS, "a convention with a reason passes", r)
        r = check_block("x", {"rule": "r", "convention": True, "why_no_gate": "   "}, tmp)
        check(r["verdict"] == FAIL, "whitespace is not a reason", r)

        # 5. Both at once is a contradiction: code-held is not a convention.
        r = check_block("x", {"rule": "r", "enforced_by": "real.py", "convention": True,
                              "why_no_gate": "because"}, tmp)
        check(r["verdict"] == FAIL, "declaring both enforced_by and convention fails", r)

        # 6. Nested rule blocks are found, or a rule can hide one level down.
        blocks = rule_blocks({"a": {"rule": "top", "b": {"rule": "nested"}}})
        names = sorted(n for n, _ in blocks)
        check(names == ["a", "a.b"], "a nested rule block is found too", names)

        # 7. A block with no rule is not audited - the contract has prose blocks
        #    and demanding enforcement of a note would make the gate noise.
        check(rule_blocks({"note": {"text": "just prose"}}) == [],
              "a block stating no rule is not audited")

    # 8. THE REAL CONTRACT must be fully accounted for. This is the control that
    #    keeps a newly added rule from shipping unheld.
    contract = json.loads((REPO / "pipeline" / "contracts" / "chain.contract.json")
                          .read_text(encoding="utf-8"))
    rows = coverage_gate(contract, REPO)
    unheld = [r for r in rows if r["verdict"] == FAIL]
    check(not unheld, "every rule in the shipped chain contract is accounted for", unheld)
    check(len(rows) >= 7, "and there are rules to account for at all", len(rows))

    print(f"\n{'PASS' if FAILS == 0 else 'FAIL'}: {FAILS} failing check(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
