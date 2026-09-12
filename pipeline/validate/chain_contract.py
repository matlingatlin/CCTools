#!/usr/bin/env python3
"""Coverage gate for the chain contract: every rule declares how it is held.

The package, skill and claims contracts each abort when a contract rule has no
implementation behind it. The chain contract had no such gate, and on
2026-09-01 six rules were added to it in one evening - convergence, preflight,
batching, model routing, blinding order, sweep-the-class - with nothing
checking that any of them was enforced, or even that anyone had decided how.

This does NOT require every rule to be code. Some rules cannot be: dispatch has
no script hook, so "count before you fan out" is a convention and always will
be. What it requires is that the rule SAY which it is. A convention that knows
it is a convention can be defended - it can be repeated, put in the steering
doc, checked in review. A convention that everyone assumes is a gate is the
weakest defence in a repository, and this one has already failed that way once.

Each rule block must carry either:

  enforced_by : a path, relative to the repo, that exists and implements it
  convention  : true, plus why_no_gate saying WHY code cannot hold this one

Exit 0 = every rule accounted for · 1 = a rule is unaccounted for
Exit 2 = the contract could not be read (never a pass)

    chain_contract.py [--contract PATH] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "pipeline" / "contracts" / "chain.contract.json"

PASS, FAIL, INDET = "pass", "fail", "indeterminate"


def rule_blocks(contract: dict, prefix: str = "") -> list[tuple[str, dict]]:
    """Every block stating a rule, including nested ones."""
    out = []
    for key, val in contract.items():
        if not isinstance(val, dict):
            continue
        name = f"{prefix}{key}"
        if "rule" in val:
            out.append((name, val))
        out.extend(rule_blocks(val, prefix=f"{name}."))
    return out


def check_block(name: str, block: dict, repo: Path) -> dict:
    enforced = block.get("enforced_by")
    convention = block.get("convention")
    why = (block.get("why_no_gate") or "").strip()

    if enforced and convention:
        return {"rule": name, "verdict": FAIL,
                "detail": "declares both enforced_by and convention - pick one; a rule held by "
                          "code is not a convention"}
    if enforced:
        paths = enforced if isinstance(enforced, list) else [enforced]
        missing = [p for p in paths if not (repo / p).exists()]
        if missing:
            return {"rule": name, "verdict": FAIL,
                    "detail": f"enforced_by names a path that does not exist: {', '.join(missing)}"}
        return {"rule": name, "verdict": PASS, "detail": f"enforced by {', '.join(paths)}"}
    if convention is True:
        if not why:
            return {"rule": name, "verdict": FAIL,
                    "detail": "convention with no why_no_gate. An unexplained convention is "
                              "indistinguishable from a rule nobody got round to enforcing"}
        return {"rule": name, "verdict": PASS, "detail": f"convention: {why[:70]}"}
    return {"rule": name, "verdict": FAIL,
            "detail": "states a rule but says nothing about how it is held - neither "
                      "enforced_by nor convention. This is the gap the gate exists for"}


def coverage_gate(contract: dict, repo: Path | None = None) -> list[dict]:
    return [check_block(n, b, repo or REPO) for n, b in rule_blocks(contract)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--contract", type=Path, default=CONTRACT)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        contract = json.loads(a.contract.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"INDETERMINATE - cannot read {a.contract}: {exc}", file=sys.stderr)
        return 2

    rows = coverage_gate(contract, REPO)
    if a.json:
        print(json.dumps(rows, indent=2))
    else:
        bad = [r for r in rows if r["verdict"] == FAIL]
        for r in rows:
            mark = "ok " if r["verdict"] == PASS else "[E]"
            print(f"{mark} {r['rule']:<28} {r['detail']}")
        print(f"\n{len(rows)} rule(s) · {len(bad)} unaccounted for")
        if bad:
            print("A rule with no stated means of enforcement is not a rule. Either name the "
                  "code that\nholds it, or say it is a convention and why code cannot.")
    return 1 if any(r["verdict"] == FAIL for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
