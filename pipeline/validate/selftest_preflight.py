#!/usr/bin/env python3
"""Positive controls for the reader preflight gate.

The load-bearing case is not synthetic: it reconstructs the 2026-09-01 defect
exactly -- SKILL.md copied alone into a scratch directory while the BOM
declares a reference and an asset. If that case does not come back
DO_NOT_DISPATCH, this gate is decoration.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reader_preflight import preflight  # noqa: E402

FAILS = 0
BOM = {
    "skill": "example-skill",
    "bill_of_materials": [
        {"file": "references/evidence.md", "kind": "reference", "why": "the verified claims"},
        {"file": "assets/record.md", "kind": "asset", "why": "the template"},
    ],
}


def check(label, got, want):
    global FAILS
    if got != want:
        FAILS += 1
    print(f"{'ok  ' if got == want else 'FAIL'} {label}: got {got}, want {want}")


def build(tmp: Path, *, whole: bool, extra: str | None = None,
          empty: str | None = None) -> tuple[Path, Path]:
    d = tmp / "reader"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text("---\nname: example-skill\n---\n\n# Example\n")
    if whole:
        for rel in ("references/evidence.md", "assets/record.md"):
            f = d / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("" if rel == empty else "content\n")
    if extra:
        f = d / extra
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("stray\n")
    bom = tmp / "bom.json"
    bom.write_text(json.dumps(BOM))
    return d, bom


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        # 1. THE defect of 2026-09-01, reconstructed. SKILL.md alone.
        d, bom = build(tmp / "a", whole=False)
        r = preflight(d, bom, skip_contract=True)
        check("SKILL.md alone -> DO_NOT_DISPATCH", r["verdict"], "DO_NOT_DISPATCH")
        check("  names both missing bundle files",
              sum("absent from the reader" in p for p in r["problems"]), 2)

        # 2. The whole bundle passes -- the gate must not block a correct copy.
        d, bom = build(tmp / "b", whole=True)
        r = preflight(d, bom, skip_contract=True)
        check("whole bundle -> INDETERMINATE only from the skipped checker",
              r["verdict"], "INDETERMINATE")
        check("  and has no problems", r["problems"], [])

        # 3. A file present but EMPTY. The reader can see it and still cannot judge it.
        d, bom = build(tmp / "c", whole=True, empty="references/evidence.md")
        r = preflight(d, bom, skip_contract=True)
        check("empty bundled file -> DO_NOT_DISPATCH", r["verdict"], "DO_NOT_DISPATCH")

        # 4. A stray file nothing declared: a different artefact than the BOM describes.
        d, bom = build(tmp / "d", whole=True, extra="references/leftover.md")
        r = preflight(d, bom, skip_contract=True)
        check("undeclared file -> DO_NOT_DISPATCH", r["verdict"], "DO_NOT_DISPATCH")

        # 5. No SKILL.md at all.
        d, bom = build(tmp / "e", whole=True)
        (d / "SKILL.md").unlink()
        r = preflight(d, bom, skip_contract=True)
        check("no SKILL.md -> DO_NOT_DISPATCH", r["verdict"], "DO_NOT_DISPATCH")

        # 6. A directory that does not exist is INDETERMINATE, never a pass.
        r = preflight(tmp / "nope", bom, skip_contract=True)
        check("missing directory -> INDETERMINATE", r["verdict"], "INDETERMINATE")

        # 7. An unreadable BOM is INDETERMINATE, never a pass by absence.
        bad = tmp / "bad.json"
        bad.write_text("{not json")
        d, _ = build(tmp / "f", whole=True)
        r = preflight(d, bad, skip_contract=True)
        check("unreadable BOM -> INDETERMINATE", r["verdict"], "INDETERMINATE")

        # 8. NEGATIVE CONTROL on the gate's own severity: an INDETERMINATE must
        #    not be reachable when a real problem exists. A missing file plus a
        #    skipped checker is still DO_NOT_DISPATCH, not INDETERMINATE.
        d, bom = build(tmp / "g", whole=False)
        r = preflight(d, bom, skip_contract=True)
        check("a problem outranks an indeterminate", r["verdict"], "DO_NOT_DISPATCH")

        # 9. The real checker runs and a valid bundle survives it end to end.
        d, bom = build(tmp / "h", whole=True)
        r = preflight(d, bom, skip_contract=False)
        check("real checker runs (verdict is not INDETERMINATE-for-not-running)",
              any("did not run" in i for i in r["indeterminate"]), False)

        # --- per-phase inputs: the OTHER direction ---------------------------
        # Requiring the whole bundle for every reader fixed the truncation and
        # created its mirror: maximum context for a reader that needs one file.
        import json as _json
        chain = tmp / "chain.json"
        chain.write_text(_json.dumps({"phases": [
            {"id": "4.3", "inputs": ["skill_md"], "inputs_why": "name is decided by the body"},
            {"id": "4.6", "inputs": ["skill_md", "references", "assets"],
             "inputs_why": "every pointer must resolve"},
            {"id": "6.4", "inputs": [], "inputs_why": "the grader sees no artefact at all"},
            {"id": "9.9", "fn": "undeclared"},
        ]}))

        chain2 = tmp / "chain2.json"
        chain2.write_text(_json.dumps({"phases": [
            {"id": "4.0", "inputs": ["bom"], "inputs_why": "plans the bundle; no SKILL.md yet"},
        ]}))

        d, bom = build(tmp / "p1", whole=True)
        r = preflight(d, bom, skip_contract=True, phase="4.3", chain_path=chain)
        check("a reader given more than its phase asked for is refused",
              r["verdict"], "DO_NOT_DISPATCH")
        check("  and every excess file is named",
              sum("did not ask for it" in p for p in r["problems"]), 2)

        d2 = tmp / "p2" / "reader"
        d2.mkdir(parents=True)
        (d2 / "SKILL.md").write_text("---\nname: example-skill\n---\n\n# Example\n")
        r = preflight(d2, bom, skip_contract=True, phase="4.3", chain_path=chain)
        check("the minimum set passes", r["verdict"], "INDETERMINATE")
        check("  with no problems", r["problems"], [])

        # The ORIGINAL defect must still be caught for a phase that needs the lot.
        r = preflight(d2, bom, skip_contract=True, phase="4.6", chain_path=chain)
        check("a phase that needs the bundle still catches truncation",
              r["verdict"], "DO_NOT_DISPATCH")

        # The blinding case: the grader must see NOTHING of the artefact.
        r = preflight(d2, bom, skip_contract=True, phase="6.4", chain_path=chain)
        check("handing the grader the skill is refused", r["verdict"], "DO_NOT_DISPATCH")
        # The general property: whatever the phase gave as its reason travels
        # with the refusal, so whoever reads it knows why the file is excluded
        # rather than only that it is.
        check("  and the phase's own reason travels with the refusal",
              any("the grader sees no artefact at all" in p for p in r["problems"]), True)

        # A phase with no declaration is INDETERMINATE, never a silent pass.
        r = preflight(d2, bom, skip_contract=True, phase="9.9", chain_path=chain)
        check("an undeclared phase is indeterminate, not assumed fine",
              any("declares no inputs" in i for i in r["indeterminate"]), True)

        # --- the marker bug, and the conflict it masked ----------------------
        # contract_errors() looked for a marker the checker never emits, so the
        # third of three advertised checks had never fired: a directory the
        # checker gave six errors came back SAFE_TO_DISPATCH.
        from reader_preflight import contract_errors
        d7 = tmp / "p7" / "reader"
        d7.mkdir(parents=True)
        (d7 / "SKILL.md").write_text("---\nname: Bad_Name\ndescription: x\n---\n\n# X\n")
        errs, why = contract_errors(d7)
        check("the checker's errors are actually read back", bool(errs) and why is None, True)
        check("  and they are the checker's own error lines",
              all(e.startswith("[E]") for e in errs), True)

        # A phase given no SKILL.md cannot satisfy the checker by construction.
        # Repairing the marker without this would fail every such phase forever.
        r = preflight(d2, bom, phase="6.4", chain_path=chain)
        check("a phase with no skill file is not failed by the checker",
              any("not applicable" in i for i in r["indeterminate"])
              or r["verdict"] == "DO_NOT_DISPATCH", True)
        empty = tmp / "p8" / "reader"
        empty.mkdir(parents=True)
        r = preflight(empty, bom, phase="4.0", chain_path=chain2)
        check("phase 4.0, whose inputs are bom only, is INDETERMINATE not a pass",
              r["verdict"], "INDETERMINATE")
        check("  and says why the checker has nothing to rule on",
              any("nothing to rule on" in i for i in r["indeterminate"]), True)

        # --- the waiver, and the line it must not cross ----------------------
        # A phase given a proper subset that still contains SKILL.md fails
        # ptr.resolves and body.files-exist on a directory that is CORRECT by
        # reader_inputs, because SKILL.md points at the whole bundle. Found by a
        # build that refused to patch the gate for its own artefact.
        chain3 = tmp / "chain3.json"
        chain3.write_text(_json.dumps({"phases": [
            {"id": "4.3", "inputs": ["skill_md"], "inputs_why": "name is decided by the body"},
            {"id": "4.6", "inputs": ["skill_md", "references", "assets"],
             "inputs_why": "every pointer must resolve"},
        ]}))
        sub = tmp / "p9" / "example-skill"
        sub.mkdir(parents=True)
        # Backticked, because the checker's path extractor reads code spans and
        # markdown links, not bare prose - a plain sentence produced no error at
        # all and the control asserted a waiver nothing could have triggered.
        (sub / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: x\n---\n\n"
            "# X\n\nSee `references/evidence.md` and `assets/record.md`.\n")
        r = preflight(sub, bom, phase="4.3", chain_path=chain3)
        check("a subset phase dispatches once the withheld files are waived",
              r["verdict"], "SAFE_TO_DISPATCH")
        check("  and the waiver is recorded, not silent", bool(r.get("waived")), True)
        check("  and it is NOT filed as an indeterminate",
              any("withheld" in i for i in r["indeterminate"]), False)

        # THE LINE, tested with an error that names NO file at all, so it can
        # only survive if the waiver is narrow. An earlier version of this
        # control used an empty bundled file, which the BOM check catches on a
        # different path - so it passed even when the waiver was made to swallow
        # everything, and a mutation walked straight through it.
        bad = tmp / "p9b" / "example-skill"
        bad.mkdir(parents=True)
        (bad / "SKILL.md").write_text(
            "---\nname: wrong-name-entirely\ndescription: x\n---\n\n"
            "# X\n\nSee `references/evidence.md`.\n")
        r = preflight(bad, bom, phase="4.3", chain_path=chain3)
        check("an error naming no withheld file survives the waiver",
              r["verdict"], "DO_NOT_DISPATCH")
        check("  and it is the name mismatch that survived",
              any("name.matches-dir" in p for p in r["problems"]), True)

        # And a phase declaring the whole bundle waives nothing.
        d, bom2 = build(tmp / "p10", whole=True)
        r = preflight(d, bom2, skip_contract=True)
        check("a whole-bundle check waives nothing", r.get("waived") or [], [])

        # NEGATIVE CONTROL: without --phase the old whole-bundle behaviour holds,
        # so nothing that depended on it silently changed meaning.
        d3, bom3 = build(tmp / "p3", whole=False)
        r = preflight(d3, bom3, skip_contract=True)
        check("with no phase named, the whole bundle is still required",
              r["verdict"], "DO_NOT_DISPATCH")

    print(f"\n{'PASS' if FAILS == 0 else 'FAIL'}: {FAILS} failing check(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
