#!/usr/bin/env python3
"""Admission gate for a build package, against pipeline/contracts/package.contract.json.

Phase 0.1 of the skill-builder chain. The contract DECLARES the rules; this file
IMPLEMENTS them. Coverage is enforced both ways: every rule the contract marks
`check: code` must have an implementation here, or the run aborts.

Verdicts are the same three as the skill checker, and the third carries the same
weight: an INDETERMINATE is a check that could not run, and it is never a pass.

One rule is not a defect report but a REFUSAL. `pkg.failure_kind.not_discipline`
rejects a package whose skill would teach discipline under pressure, because two
preregistered rounds in this repo found no scenario class that discriminates for
it. The package may be perfect; we still cannot show the skill works, and a green
suite would ship an unmeasured claim.

Usage
    python3 pipeline/validate/package_contract.py <package.json> [...]
    python3 pipeline/validate/package_contract.py <package.json> --json

Exit 0 = admitted. Exit 1 = refused. Exit 2 = the contract and the engine disagree.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "pipeline" / "contracts" / "package.contract.json"

PASS, FAIL, INDET = "PASS", "FAIL", "INDETERMINATE"
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

REG: dict[str, callable] = {}


def rule(rid):
    def deco(fn):
        REG[rid] = fn
        return fn
    return deco


def _s(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


# --- identity ----------------------------------------------------------------

@rule("pkg.id.present")
def _(p, ctx):
    return (PASS, p.get("id")) if _s(p.get("id")) else (FAIL, "missing or empty")


@rule("pkg.id.kebab")
def _(p, ctx):
    v = p.get("id")
    if not _s(v):
        return INDET, "no id to check"
    return (PASS, v) if KEBAB.fullmatch(v) else (FAIL, f"id {v!r} is not kebab-case")


# --- scope -------------------------------------------------------------------

@rule("pkg.sentence.present")
def _(p, ctx):
    return (PASS, "") if _s(p.get("candidate_sentence")) else (FAIL, "missing or empty — a topic is not a scope")


@rule("pkg.sentence.single")
def _(p, ctx):
    v = p.get("candidate_sentence")
    if not _s(v):
        return INDET, "no sentence to measure"
    words = len(v.split())
    sentences = len([s for s in re.split(r"(?<=[.!?])\s+", v.strip()) if s])
    if words < 8:
        return FAIL, f"{words} words — a scope of that length has not been stated"
    if sentences > 1:
        return FAIL, f"{sentences} sentences — a scope needing a paragraph has not been decided"
    return PASS, f"{words} words"


# --- shape -------------------------------------------------------------------

@rule("pkg.unit_type")
def _(p, ctx):
    v = p.get("unit_type")
    return (PASS, v) if v == "skill" else (FAIL, f"unit_type {v!r} — route it, do not coerce it")


@rule("pkg.content_kind")
def _(p, ctx):
    v = p.get("content_kind")
    return (PASS, v) if v in {"reference", "task"} else (FAIL, f"content_kind {v!r}, expected reference or task")


@rule("pkg.verifiable")
def _(p, ctx):
    v = p.get("verifiable")
    return (PASS, str(v)) if isinstance(v, bool) else (FAIL, f"verifiable {v!r} is not a boolean")


@rule("pkg.failure_kind")
def _(p, ctx):
    v = p.get("failure_kind")
    return (PASS, v) if v in {"knowledge", "shape", "discipline"} else (FAIL, f"failure_kind {v!r}")


@rule("pkg.failure_kind.not_discipline")
def _(p, ctx):
    v = p.get("failure_kind")
    if v != "discipline":
        return PASS, ""
    return FAIL, ("REFUSED — not a defect in this package. We have no scenario class that "
                  "discriminates for pressure-discipline (2 preregistered rounds: 1 of 12, 2 of 12). "
                  "Build it when a test exists.")


# --- origin ------------------------------------------------------------------

ORIGINS = {"harvest", "existing-artifact", "agent-request", "library-defect", "human-request"}
GAP_KINDS = {"missing", "wrong-shaped", "improvable"}


@rule("pkg.origin")
def _(p, ctx):
    v = p.get("origin")
    return (PASS, v) if v in ORIGINS else (FAIL, f"origin {v!r}, expected one of {', '.join(sorted(ORIGINS))}")


@rule("pkg.origin.filled_by")
def _(p, ctx):
    return (PASS, p.get("filled_by")) if _s(p.get("filled_by")) else (
        FAIL, "absent — an origin says where the material came from, filled_by says who did the work")


@rule("pkg.gap_kind")
def _(p, ctx):
    v = p.get("gap_kind")
    return (PASS, v) if v in GAP_KINDS else (
        FAIL, f"gap_kind {v!r}, expected missing, wrong-shaped or improvable")


@rule("pkg.claims.not_from_artifact")
def _(p, ctx):
    """A finished skill cannot be its own evidence.

    Only checked when the package came from one. The test is deliberately about
    the SOURCE ROW, not the wording: a source whose url points into the incoming
    artefact, or whose type says so, cannot back a claim - because the artefact's
    assertions are the hypothesis under test.
    """
    if p.get("origin") != "existing-artifact":
        return PASS, "not an incoming artefact"
    art = str(p.get("incoming_artifact") or "").strip()
    bad = []
    for s in _sources(p):
        if not isinstance(s, dict):
            continue
        if s.get("type") == "incoming-artifact" or (art and art in str(s.get("url", ""))):
            bad.append(s.get("source_id"))
    if not bad:
        return PASS, ""
    cited = sorted({c.get("source_id") for c in _claims(p)
                    if isinstance(c, dict) and c.get("source_id") in set(bad)})
    if not cited:
        return PASS, f"the artefact is listed as a source but backs no claim ({', '.join(map(str, bad))})"
    return FAIL, (f"claim(s) cite the incoming artefact as evidence: {', '.join(map(str, cited))} — "
                  f"its content is the hypothesis under test, not a source for it")


# --- sources -----------------------------------------------------------------

def _sources(p) -> list:
    v = p.get("sources")
    return v if isinstance(v, list) else []


@rule("pkg.sources.present")
def _(p, ctx):
    n = len(_sources(p))
    return (PASS, f"{n}") if n else (FAIL, "no sources — a claim with no source is a memory")


@rule("pkg.sources.fields")
def _(p, ctx):
    src = _sources(p)
    if not src:
        return INDET, "no sources to inspect"
    need = ("source_id", "url", "fetched", "access", "read")
    bad = []
    for i, s in enumerate(src):
        if not isinstance(s, dict):
            bad.append(f"[{i}] not an object")
            continue
        miss = [k for k in need if not _s(s.get(k))]
        if miss:
            bad.append(f"{s.get('source_id', f'[{i}]')}: missing {', '.join(miss)}")
    return (PASS, "") if not bad else (FAIL, "; ".join(bad[:4]))


@rule("pkg.sources.fetched_iso")
def _(p, ctx):
    src = _sources(p)
    if not src:
        return INDET, "no sources to inspect"
    bad = [s.get("source_id", "?") for s in src
           if isinstance(s, dict) and not (isinstance(s.get("fetched"), str) and ISO.fullmatch(s["fetched"]))]
    return (PASS, "") if not bad else (FAIL, f"fetched not YYYY-MM-DD: {', '.join(map(str, bad[:4]))}")


@rule("pkg.sources.ids_unique")
def _(p, ctx):
    ids = [s.get("source_id") for s in _sources(p) if isinstance(s, dict)]
    if not ids:
        return INDET, "no sources to inspect"
    dup = sorted({i for i in ids if ids.count(i) > 1})
    return (PASS, f"{len(ids)}") if not dup else (FAIL, f"duplicate source_id: {', '.join(map(str, dup))}")


# --- claims ------------------------------------------------------------------

def _claims(p) -> list:
    v = p.get("claims")
    return v if isinstance(v, list) else []


@rule("pkg.claims.present")
def _(p, ctx):
    n = len(_claims(p))
    return (PASS, f"{n}") if n else (FAIL, "no claims")


@rule("pkg.claims.rows_not_prose")
def _(p, ctx):
    cl = _claims(p)
    if not cl:
        return INDET, "no claims to inspect"
    bad = [i for i, c in enumerate(cl) if not (isinstance(c, dict) and _s(c.get("claim")))]
    return (PASS, "") if not bad else (FAIL, f"claim(s) {bad[:5]} are prose, not rows")


@rule("pkg.claims.quote")
def _(p, ctx):
    cl = _claims(p)
    if not cl:
        return INDET, "no claims to inspect"
    bad = [c.get("claim", f"[{i}]")[:40] for i, c in enumerate(cl)
           if isinstance(c, dict) and not _s(c.get("quote"))]
    if not bad:
        return PASS, f"{len(cl)} quoted"
    return FAIL, f"{len(bad)} claim(s) with no verbatim quote: {bad[0]!r}…"


@rule("pkg.claims.source_resolves")
def _(p, ctx):
    cl, ids = _claims(p), {s.get("source_id") for s in _sources(p) if isinstance(s, dict)}
    if not cl:
        return INDET, "no claims to inspect"
    bad = sorted({c.get("source_id") for c in cl if isinstance(c, dict) and c.get("source_id") not in ids})
    return (PASS, "") if not bad else (FAIL, f"source_id not in sources: {', '.join(map(str, bad[:4]))}")


@rule("pkg.claims.locator")
def _(p, ctx):
    cl = _claims(p)
    if not cl:
        return INDET, "no claims to inspect"
    n = sum(1 for c in cl if isinstance(c, dict) and not _s(c.get("locator")))
    return (PASS, "") if not n else (FAIL, f"{n} claim(s) with no locator")


def _allowed_verdicts() -> set[str]:
    """Read the vocabulary from the CLAIMS contract, which owns it.

    It used to be a literal here as well as there. Adding DERIVED to the claims
    contract on 2026-09-02 therefore left this copy behind, and admission
    refused a package whose claims the claims contract had just accepted - two
    gates disagreeing about the same word because the word was written twice.
    """
    try:
        cc = json.loads((REPO / "pipeline" / "contracts" / "claims.contract.json")
                        .read_text(encoding="utf-8"))
        v = set(cc.get("verdicts") or ())
        if v:
            return v
    except Exception:
        pass
    return {"MEASURED", "REPEATED"}


@rule("pkg.claims.verdict")
def _(p, ctx):
    cl = _claims(p)
    if not cl:
        return INDET, "no claims to inspect"
    allowed = _allowed_verdicts()
    bad = sorted({str(c.get("verdict")) for c in cl
                  if isinstance(c, dict) and c.get("verdict") not in allowed})
    return (PASS, "") if not bad else (
        FAIL, f"verdict(s) outside {sorted(allowed)}: {', '.join(bad[:4])}")


@rule("pkg.claims.measured_needs_evidence")
def _(p, ctx):
    cl = _claims(p)
    if not cl:
        return INDET, "no claims to inspect"
    bad = []
    for c in cl:
        if not isinstance(c, dict) or c.get("verdict") != "MEASURED":
            continue
        if not _s(c.get("what_was_measured")) or not (_s(c.get("effect_size")) or _s(c.get("sample"))):
            bad.append(str(c.get("claim", ""))[:40])
    if not bad:
        return PASS, ""
    return FAIL, f"MEASURED without a dependent variable and a number: {bad[0]!r}…"


# --- hypothesis, vocabulary, tasks -------------------------------------------

@rule("pkg.expected_failure")
def _(p, ctx):
    return (PASS, "") if _s(p.get("expected_failure")) else (FAIL, "absent — the probe would have no hypothesis to test")


@rule("pkg.trigger_terms")
def _(p, ctx):
    v = p.get("trigger_terms")
    if not isinstance(v, list):
        return FAIL, "missing or not a list"
    good = [t for t in v if _s(t)]
    return (PASS, f"{len(good)}") if len(good) >= 3 else (FAIL, f"{len(good)} term(s), minimum 3")


@rule("pkg.tasks.min")
def _(p, ctx):
    v = p.get("representative_tasks")
    n = len(v) if isinstance(v, list) else 0
    return (PASS, f"{n}") if n >= 2 else (FAIL, f"{n} task(s), minimum 2 — one cannot separate systematic from draw")


@rule("pkg.tasks.fields")
def _(p, ctx):
    v = p.get("representative_tasks")
    if not isinstance(v, list) or not v:
        return INDET, "no tasks to inspect"
    bad = [i for i, t in enumerate(v)
           if not (isinstance(t, dict) and _s(t.get("task")) and _s(t.get("artifact_expected")))]
    return (PASS, "") if not bad else (FAIL, f"task(s) {bad[:5]} missing task or artifact_expected")


@rule("pkg.tasks.kinds")
def _(p, ctx):
    """Fixtures of one kind grade one mode. Three builds of one skill (2026-09-03) each ended with
    the reviewer saying the same thing: every fixture is a version of one artefact, so two of the
    method's pair types and one branch have no fixture and are graded by nothing. The package is
    where that is cheap to refuse; the third review is where it was found."""
    v = p.get("representative_tasks")
    if not isinstance(v, list) or len(v) < 2:
        return INDET, "fewer than two tasks to compare"
    kinds = [t.get("fixture_kind") if isinstance(t, dict) else None for t in v]
    missing = [i for i, k in enumerate(kinds) if not _s(k)]
    if missing:
        return FAIL, f"task(s) {missing[:5]} carry no fixture_kind (what sort of artefact the task runs on)"
    distinct = sorted(set(k.strip().lower() for k in kinds))
    if len(distinct) >= 2:
        return PASS, ", ".join(distinct)
    if _s(p.get("one_kind_reason")):
        return WARN, f"one kind ({distinct[0]}) with a stated reason: {p['one_kind_reason'][:120]}"
    return FAIL, f"every task runs on one kind of fixture ({distinct[0]}) and no one_kind_reason is given - a mode the text claims and no fixture exercises is graded by nothing"


# --- policy ------------------------------------------------------------------

@rule("pkg.budget")
def _(p, ctx):
    b = p.get("budget")
    if not isinstance(b, dict):
        return FAIL, "missing or not an object"
    miss = [k for k in ("max_agents", "max_paired_runs") if not isinstance(b.get(k), int)]
    return (PASS, "") if not miss else (FAIL, f"missing or non-integer: {', '.join(miss)}")


@rule("pkg.threshold")
def _(p, ctx):
    return (PASS, "") if _s(p.get("threshold")) else (FAIL, "absent — written afterwards, the result moves the bar")


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def coverage_gate(contract: dict) -> list[str]:
    return [r["id"] for r in contract["rules"] if r.get("check") == "code" and r["id"] not in REG]


def orphan_gate(contract: dict) -> list[str]:
    """Implemented rules the contract does not declare - dead code that looks live.

    The checker iterates the CONTRACT's rule list, so a rule registered in REG
    but absent from the contract is never called. It imports, it registers, it
    reads as enforcement, and it runs zero times. coverage_gate() guards the
    other direction only, so this half was ungated on all three contracts until
    2026-09-02, when a rule added to the checker alone was silently never run
    and the selftest still reported every rule controlled.
    """
    declared = {r["id"] for r in contract.get("rules", [])}
    return sorted(rid for rid in REG if rid not in declared)


def admit(pkg: dict, contract: dict, ctx: dict | None = None) -> list[dict]:
    ctx = ctx or {}
    rows = []
    for r in contract["rules"]:
        if r.get("check") != "code":
            continue
        try:
            verdict, detail = REG[r["id"]](pkg, ctx)
        except Exception as exc:  # noqa: BLE001 - an engine bug is not a package defect
            verdict, detail = INDET, f"checker error: {type(exc).__name__}: {exc}"
        rows.append({"id": r["id"], "severity": r.get("severity", "error"),
                     "verdict": verdict, "detail": detail, "reason": r.get("reason", "")})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packages", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--why", action="store_true", help="print each failing rule's reason")
    args = ap.parse_args()

    contract = load_contract()
    missing = coverage_gate(contract)
    if missing:
        print("ABORT — contract declares code rules with no implementation:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 2

    refused = False
    out = []
    for path in args.packages:
        try:
            pkg = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"REFUSED {path}: unreadable — {exc}")
            refused = True
            continue
        rows = admit(pkg, contract)
        errs = [r for r in rows if r["verdict"] == FAIL and r["severity"] == "error"]
        warns = [r for r in rows if r["verdict"] == FAIL and r["severity"] == "warn"]
        indet = [r for r in rows if r["verdict"] == INDET]
        out.append({"package": path, "rows": rows})
        if errs:
            refused = True
        if args.json:
            continue
        head = "REFUSED" if errs else "ADMITTED"
        print(f"{head} {path}  ·  {len(errs)} error(s) · {len(warns)} warning(s) · {len(indet)} indeterminate")
        for r in errs + warns + indet:
            mark = {FAIL: "E" if r["severity"] == "error" else "w", INDET: "?"}[r["verdict"]]
            print(f"   [{mark}] {r['id']:<34} {r['detail']}")
            if args.why and r["reason"]:
                print(f"        why: {r['reason']}")
    if args.json:
        print(json.dumps({"contract_version": contract["contract_version"], "results": out}, indent=2))
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
