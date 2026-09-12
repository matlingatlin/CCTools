#!/usr/bin/env python3
"""Refuse to hand a reader an incomplete bundle.

Phase 4 dispatches independent readers over a copy of the artefact. On
2026-09-01 a steps reader was given SKILL.md copied ALONE into a scratch
directory and correctly reported that references/ and assets/ did not exist --
a true finding about the harness, not the skill. The round cost a full reader
and every other finding in it had to be discarded, because they were made
against a partial artefact.

The chain contract's `preflight` block states the rule. This is the gate: the
same rule, enforced, because a convention nobody runs is the weakest defence
in this repo and it has already failed once for exactly that reason.

Checks, against the directory the reader will actually be given:
  1. Every input the phase DECLARED exists and is non-empty.
  2. Nothing is present that the phase did NOT declare.
  3. The artefact checker runs clean of ERRORS on that directory.

Both directions matter and only the first was checked at first. Requiring the
whole bill of materials for every reader fixed the truncated-bundle defect and
created its mirror: a reader ruling on the name and frontmatter was handed the
references, the assets, the evals and two CSV fixtures it had no use for. For
one phase the excess is not merely wasteful - the grader at 6.4 must see NO
artefact at all, because a grader that can see the skill can tell which arm
wrote which answer, and the blinding is the measurement.

Without --phase the check falls back to the whole bill of materials, which is
the old behaviour and is right only for the phases that genuinely need it.

Exit codes:  0 = safe to dispatch · 1 = do not dispatch · 2 = could not check
(2 is never a pass. A preflight that could not run has not run.)

    reader_preflight.py <reader-dir> <bom.json> [--skip-contract]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CHAIN = REPO / "pipeline" / "contracts" / "chain.contract.json"
IGNORED_NAMES = {".DS_Store", "__pycache__", ".git"}

# An input token to the paths it covers inside the reader's directory.
# bom and siblings are passed alongside rather than inside it, so they place no
# requirement on the directory's contents.
DIR_INPUTS = {"skill_md": ("SKILL.md",), "references": ("references/",),
              "assets": ("assets/",), "evals": ("evals/",)}
OUTSIDE_DIR = {"bom", "siblings"}


def phase_inputs(phase_id: str, chain_path: Path | None = None) -> tuple[list[str], str] | None:
    """What the chain contract says this phase's reader may see."""
    try:
        chain = json.loads((chain_path or CHAIN).read_text(encoding="utf-8"))
    except Exception:
        return None
    for ph in chain.get("phases", []):
        if str(ph.get("id")) == str(phase_id) and "inputs" in ph:
            return list(ph["inputs"]), ph.get("inputs_why", "")
    return None


def covers(rel: str, tokens: list[str]) -> bool:
    for tok in tokens:
        for pat in DIR_INPUTS.get(tok, ()):
            if rel == pat or rel.startswith(pat):
                return True
    return False


def contract_errors(reader_dir: Path) -> tuple[list[str], str | None]:
    """Run the artefact checker on the reader's directory. Returns (errors, indeterminate_reason)."""
    script = HERE / "skill_contract.py"
    if not script.exists():
        return [], f"checker not found at {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(script), str(reader_dir)],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return [], "checker timed out"
    # The checker marks errors [E], warnings [w] and indeterminates [?]. This
    # looked for [x], which it never emits, so the third of the three checks
    # this gate advertises had never fired once: it returned SAFE_TO_DISPATCH
    # on a directory the checker gave six errors. Found by a build, not by me,
    # and it is the same marker mistake I made earlier the same evening in a
    # one-off sweep and caught there only because a summary line disagreed.
    errs = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip().startswith("[E]")]
    return errs, None


def preflight(reader_dir: Path, bom_path: Path, skip_contract: bool = False,
              phase: str | None = None, chain_path: Path | None = None) -> dict:
    problems: list[str] = []
    indeterminate: list[str] = []
    waived_notes: list[str] = []

    if not reader_dir.is_dir():
        return {"verdict": "INDETERMINATE",
                "indeterminate": [f"{reader_dir} is not a directory"], "problems": []}
    try:
        bom = json.loads(bom_path.read_text())
    except Exception as exc:
        return {"verdict": "INDETERMINATE",
                "indeterminate": [f"cannot read BOM {bom_path}: {exc}"], "problems": []}

    # What this phase asked for. Falls back to the whole BOM when no phase is
    # named, which is the old behaviour: complete, and for most readers too much.
    spec = phase_inputs(phase, chain_path) if phase else None
    tokens = spec[0] if spec else None
    if phase and spec is None:
        indeterminate.append(f"phase {phase} declares no inputs in the chain contract")

    if tokens is not None and "skill_md" not in tokens:
        pass
    elif not (reader_dir / "SKILL.md").is_file():
        problems.append("SKILL.md is missing from the directory the reader will see")

    declared: set[str] = set()
    for entry in bom.get("bill_of_materials", []):
        rel = entry.get("file")
        if not rel:
            indeterminate.append(f"a BOM entry has no file field: {entry!r}")
            continue
        declared.add(rel)
        if tokens is not None and not covers(rel, tokens):
            continue          # this phase's reader does not need it
        target = reader_dir / rel
        if not target.is_file():
            # THE defect this gate exists for.
            problems.append(f"declared in the BOM but absent from the reader's directory: {rel}")
        elif target.stat().st_size == 0:
            problems.append(f"present but empty, so the reader cannot judge it: {rel}")

    # The other direction. A stray file is a different artefact than the BOM
    # describes; a file this phase did not ask for is context it pays for on a
    # judgement it was not asked to make.
    for path in sorted(reader_dir.rglob("*")):
        if path.is_dir() or any(part in IGNORED_NAMES for part in path.parts):
            continue
        rel = str(path.relative_to(reader_dir))
        if tokens is not None:
            if not covers(rel, tokens):
                problems.append(f"present but phase {phase} did not ask for it: {rel}"
                                + (f" — {spec[1][:80]}" if spec and spec[1] else ""))
        elif rel not in declared and rel != "SKILL.md":
            problems.append(f"in the reader's directory but declared nowhere: {rel}")

    # The checker can only rule on a directory that HAS the skill file. A phase
    # whose declared inputs are a subset of the bundle - 4.0 gets only the bill
    # of materials, 6.4 gets nothing at all - cannot satisfy it by construction,
    # and running it there would fail every such phase forever. Repairing the
    # marker above without this would have done exactly that, which is why the
    # build that found the marker bug reported the conflict in the same breath.
    needs_checker = tokens is None or "skill_md" in tokens
    if skip_contract:
        indeterminate.append("artefact checker skipped by flag")
    elif not needs_checker:
        indeterminate.append(
            f"artefact checker not applicable: phase {phase} declares inputs {tokens} and so is "
            f"given no SKILL.md - the checker has nothing to rule on")
    else:
        errs, why = contract_errors(reader_dir)
        if why:
            indeterminate.append(f"artefact checker did not run: {why}")
        # An error naming a file this phase deliberately WITHHELD is not a defect
        # in the artefact - it is the two rules meeting. SKILL.md points at the
        # whole bundle by ptr.every-file, so any phase given a proper subset that
        # still contains SKILL.md fails ptr.resolves and body.files-exist on a
        # directory that is correct by reader_inputs. The first carve-out covered
        # only phases with NO SKILL.md and left five of seven readers unable to
        # pass. Found by a build that refused to patch the gate for itself and
        # recorded the conflict instead.
        withheld = sorted(d for d in declared if tokens is not None and not covers(d, tokens))
        kept, waived = [], []
        for e in errs:
            if withheld and any(w in e for w in withheld):
                waived.append(e)
            else:
                kept.append(e)
        problems.extend(f"contract error on the reader's copy: {e}" for e in kept)
        # WAIVED, not INDETERMINATE. An indeterminate means a check could not
        # run; here it ran, produced a finding, and the finding was excluded by
        # a stated rule. Filing it as indeterminate would block every subset
        # phase forever, which is the same wrong answer as failing them.
        waived_notes.extend(
            f"waived, names a file phase {phase} withheld by design: {e}" for e in waived)

    if problems:
        verdict = "DO_NOT_DISPATCH"
    elif indeterminate:
        verdict = "INDETERMINATE"
    else:
        verdict = "SAFE_TO_DISPATCH"
    return {"verdict": verdict, "problems": problems, "indeterminate": indeterminate,
            "waived": waived_notes,
            "reader_dir": str(reader_dir), "declared": sorted(declared),
            "phase": phase, "inputs": tokens,
            "inputs_outside_the_directory": sorted(set(tokens or []) & OUTSIDE_DIR)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reader_dir", type=Path)
    ap.add_argument("bom", type=Path)
    ap.add_argument("--skip-contract", action="store_true")
    ap.add_argument("--phase", default=None,
                    help="check against what THIS phase declared it needs, not the whole bundle")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = preflight(a.reader_dir, a.bom, a.skip_contract, phase=a.phase)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(r["verdict"])
        for p in r["problems"]:
            print(f"  [x] {p}")
        for i in r["indeterminate"]:
            print(f"  [?] {i}")
        for w in r.get("waived", []):
            print(f"  [-] {w}")
    return {"SAFE_TO_DISPATCH": 0, "DO_NOT_DISPATCH": 1, "INDETERMINATE": 2}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
