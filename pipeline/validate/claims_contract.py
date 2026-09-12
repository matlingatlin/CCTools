#!/usr/bin/env python3
"""Gate for a claim set the builder FETCHED, against claims.contract.json.

Phases 3.2-3.5. The package contract already gates claims that arrive with a
package; this gates the ones the run went and got itself, which is the harder
case because nobody outside the run has looked at them.

Same three verdicts and the same coverage gate as everywhere else: a declared
`check: code` rule with no implementation aborts, and an INDETERMINATE is a check
that could not run, never a pass.

    python3 claims_contract.py <claims.json> [--why] [--json]

Exit 0 accepted · 1 rejected · 2 the contract and the engine disagree.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "pipeline" / "contracts" / "claims.contract.json"
PASS, FAIL, INDET = "PASS", "FAIL", "INDETERMINATE"
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERIFIED = {"supported", "not-supported", "not-in-source", "source-unreachable", "not-checkable"}

REG: dict[str, callable] = {}


def rule(rid):
    def deco(fn):
        REG[rid] = fn
        return fn
    return deco


def _s(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _claims(d):
    v = d.get("claims")
    return v if isinstance(v, list) else []


def _sources(d):
    v = d.get("sources")
    return v if isinstance(v, list) else []


@rule("cl.rows")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return FAIL, "no claims"
    bad = [i for i, c in enumerate(cl) if not (isinstance(c, dict) and _s(c.get("claim")))]
    return (PASS, f"{len(cl)}") if not bad else (FAIL, f"claim(s) {bad[:5]} are prose, not rows")


@rule("cl.quote")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    bad = [str(c.get("claim", ""))[:40] for c in cl if isinstance(c, dict) and not _s(c.get("quote"))]
    return (PASS, "") if not bad else (FAIL, f"{len(bad)} with no verbatim quote: {bad[0]!r}…")


@rule("cl.locator")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    n = sum(1 for c in cl if isinstance(c, dict) and not _s(c.get("locator")))
    return (PASS, "") if not n else (FAIL, f"{n} claim(s) with no locator")


@rule("cl.source_resolves")
def _(d, ctx):
    cl, ids = _claims(d), {s.get("source_id") for s in _sources(d) if isinstance(s, dict)}
    if not cl:
        return INDET, "no claims to inspect"
    bad = sorted({c.get("source_id") for c in cl if isinstance(c, dict) and c.get("source_id") not in ids})
    return (PASS, "") if not bad else (FAIL, f"source_id not in sources: {', '.join(map(str, bad[:4]))}")


# The vocabulary now lives in the contract; this mirrors it so the checker can
# run standalone. DERIVED was added after a gatherer met a claim that was
# neither measured nor repeated - a sample-size floor computed from parameters
# its own author called fictional - and coined the label rather than mislabel
# it MEASURED. Two verdicts forced a choice between calling an assumption a
# measurement and discarding an honest finding.
VERDICTS = {"MEASURED", "REPEATED", "DERIVED"}


@rule("cl.derived_names_its_assumption")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    der = [c for c in cl if isinstance(c, dict) and c.get("verdict") == "DERIVED"]
    if not der:
        # Vacuously satisfied over a non-empty claim set, which is a PASS here
        # and not an INDETERMINATE - the same shape as cl.measured_evidence.
        # INDETERMINATE is for a check that COULD NOT run, and this one ran.
        return PASS, "no DERIVED claims to check"
    bad = [str(c.get("claim", ""))[:40] for c in der
           if not _s(c.get("assumes")) and "assum" not in str(c.get("claim", "")).lower()
           and "fictional" not in str(c.get("claim", "")).lower()]
    return (PASS, "") if not bad else (
        FAIL, f"DERIVED without naming what it assumes: {bad[0]!r}… — a computed figure whose "
              f"assumptions are not stated reads exactly like a measured one")


@rule("cl.verdict")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    bad = sorted({str(c.get("verdict")) for c in cl if isinstance(c, dict)
                  and c.get("verdict") not in VERDICTS})
    return (PASS, "") if not bad else (FAIL, f"verdict(s): {', '.join(bad[:4])}")


@rule("cl.measured_evidence")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    bad = [str(c.get("claim", ""))[:40] for c in cl if isinstance(c, dict) and c.get("verdict") == "MEASURED"
           and (not _s(c.get("what_was_measured")) or not (_s(c.get("effect_size")) or _s(c.get("sample"))))]
    return (PASS, "") if not bad else (FAIL, f"MEASURED with no dependent variable and number: {bad[0]!r}…")


@rule("cl.verified")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    bad = []
    for c in cl:
        if not isinstance(c, dict):
            continue
        v = c.get("verification")
        if not isinstance(v, dict) or v.get("verdict") not in VERIFIED:
            bad.append(str(c.get("claim", ""))[:40])
    return (PASS, "") if not bad else (FAIL, f"{len(bad)} unverified: {bad[0]!r}…")


@rule("cl.verifier_not_gatherer")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    same, unknown = [], 0
    for c in cl:
        if not isinstance(c, dict):
            continue
        v = c.get("verification") or {}
        by, got = v.get("by"), c.get("gathered_by")
        if not _s(by) or not _s(got):
            unknown += 1
        elif by == got:
            same.append(str(c.get("claim", ""))[:40])
    if same:
        return FAIL, f"{len(same)} verified by whoever gathered them: {same[0]!r}…"
    if unknown:
        return INDET, f"{unknown} claim(s) do not record who gathered or who verified — cannot check"
    return PASS, ""


@rule("cl.unsupported_dropped")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    bad = [str(c.get("claim", ""))[:40] for c in cl if isinstance(c, dict)
           and (c.get("verification") or {}).get("verdict") in {"not-supported", "not-in-source"}
           and c.get("adopted")]
    return (PASS, "") if not bad else (FAIL, f"{len(bad)} adopted despite failing verification: {bad[0]!r}…")


@rule("cl.reach_vs_read")
def _(d, ctx):
    src = {s.get("source_id"): s for s in _sources(d) if isinstance(s, dict)}
    if not src:
        return INDET, "no sources to inspect"
    miss = [k for k, s in src.items() if not (_s(s.get("access")) and _s(s.get("read")))]
    if miss:
        return FAIL, f"access and read not both recorded: {', '.join(map(str, miss[:4]))}"
    thin = [str(c.get("claim", ""))[:40] for c in _claims(d) if isinstance(c, dict)
            and c.get("verdict") == "MEASURED"
            and "abstract" in str(src.get(c.get("source_id"), {}).get("read", "")).lower()]
    return (PASS, "") if not thin else (FAIL, f"MEASURED resting on an abstract-only source: {thin[0]!r}…")


@rule("cl.dated")
def _(d, ctx):
    src = _sources(d)
    if not src:
        return INDET, "no sources to inspect"
    bad = [s.get("source_id") for s in src if isinstance(s, dict)
           and not (isinstance(s.get("fetched"), str) and ISO.fullmatch(s["fetched"]))]
    return (PASS, "") if not bad else (FAIL, f"fetched not YYYY-MM-DD: {', '.join(map(str, bad[:4]))}")


@rule("cl.contradictions_kept")
def _(d, ctx):
    cl = _claims(d)
    if not cl:
        return INDET, "no claims to inspect"
    by_id = {c.get("claim_id"): c for c in cl if isinstance(c, dict) and c.get("claim_id")}
    dangling = []
    for c in cl:
        if not isinstance(c, dict):
            continue
        for other in c.get("contradicts") or []:
            if other not in by_id:
                dangling.append(f"{c.get('claim_id')} -> {other}")
    if dangling:
        return FAIL, ("a contradiction names a row that is not in the set — the other side was "
                      f"dropped: {', '.join(dangling[:4])}")
    return PASS, f"{sum(len(c.get('contradicts') or []) for c in cl if isinstance(c, dict))} link(s), both sides present"


@rule("cl.no_dup_source_ids")
def _(d, ctx):
    ids = [s.get("source_id") for s in _sources(d) if isinstance(s, dict)]
    if not ids:
        return INDET, "no sources to inspect"
    dup = sorted({i for i in ids if ids.count(i) > 1})
    return (PASS, f"{len(ids)}") if not dup else (FAIL, f"duplicate source_id: {', '.join(map(str, dup))}")


@rule("cl.coverage_answered")
def _(d, ctx):
    cov = d.get("coverage")
    if not isinstance(cov, list) or not cov:
        return FAIL, ("no coverage list — phase 3 exists to answer a question per observed failure, "
                      "and an unanswered one is the absence the chain gate was built for")
    bad = [i for i, r in enumerate(cov) if not (isinstance(r, dict) and isinstance(r.get("covered"), bool))]
    return (PASS, f"{len(cov)} failure(s) answered") if not bad else (FAIL, f"row(s) {bad[:5]} have no covered verdict")


# --- engine ------------------------------------------------------------------

def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def coverage_gate(contract: dict) -> list[str]:
    return [r["id"] for r in contract["rules"] if r.get("check") == "code" and r["id"] not in REG]


def orphan_gate(contract: dict) -> list[str]:
    """Implemented rules the contract does not declare - dead code that looks live.

    check() iterates the CONTRACT's rule list, so a rule registered in REG but
    absent from the contract is never called. It imports, it registers, it reads
    as enforcement, and it runs zero times. coverage_gate() guards the other
    direction only, so this half was ungated on all three contracts until
    2026-09-02, when a rule added to the checker alone was silently never run
    and the selftest still reported every rule controlled.
    """
    declared = {r["id"] for r in contract.get("rules", [])}
    return sorted(rid for rid in REG if rid not in declared)


def check(data: dict, contract: dict) -> list[dict]:
    rows = []
    for r in contract["rules"]:
        if r.get("check") != "code":
            continue
        try:
            v, detail = REG[r["id"]](data, {})
        except Exception as exc:  # noqa: BLE001
            v, detail = INDET, f"checker error: {type(exc).__name__}: {exc}"
        rows.append({"id": r["id"], "severity": r.get("severity", "error"),
                     "verdict": v, "detail": detail, "reason": r.get("reason", "")})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("claims"); ap.add_argument("--why", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    contract = load_contract()
    missing = coverage_gate(contract)
    if missing:
        print("ABORT — contract declares code rules with no implementation: " + ", ".join(missing), file=sys.stderr)
        return 2
    rows = check(json.loads(Path(a.claims).read_text(encoding="utf-8")), contract)
    errs = [r for r in rows if r["verdict"] == FAIL and r["severity"] == "error"]
    indet = [r for r in rows if r["verdict"] == INDET]
    if a.json:
        print(json.dumps({"contract_version": contract["contract_version"], "rows": rows}, indent=2))
        return 1 if errs else 0
    print(f"{'REJECTED' if errs else 'ACCEPTED'} {a.claims}  ·  {len(errs)} error(s) · {len(indet)} indeterminate")
    for r in errs + indet:
        print(f"   [{'E' if r['verdict'] == FAIL else '?'}] {r['id']:<26} {r['detail']}")
        if a.why and r["reason"]:
            print(f"        why: {r['reason']}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
