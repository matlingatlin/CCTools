#!/usr/bin/env python3
"""Grade an artefact answer with code instead of a judge.

Some round-2 questions ask for a real file, not a description of one. Where the
answer contains an actual SKILL.md, no judging agent is needed and none should be
used: the contract checker already rules on it, it cannot be blind, and it cannot
be talked round.

This pulls the first fenced block that looks like a SKILL.md out of an answer,
writes it into a throwaway skill directory, and runs the real checker on it.

Two verdicts that are not the same, and the difference is the whole point:

  NO ARTEFACT   the answer described a file instead of producing one. This is a
                FAIL on the question, not a missing measurement - the question
                asked for the file.
  produced      the checker's own error and warning counts, whatever they are.

    python3 artifact_check.py <answer.md> <question-id>
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CHECKER = REPO / "pipeline" / "validate" / "skill_contract.py"

FENCE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.S)

# Rules a lone SKILL.md cannot settle. The answer is one file; a skill that
# correctly bundles an asset and points at it will fail every one of these for a
# reason that is the CHECKER'S CONTEXT, not a defect in the artefact. Counting
# them would punish the better answer for being more complete - which is exactly
# what happened before this set existed.
#
# They are reported as not-decidable-here, never silently dropped: an excluded
# check is a check that could not run, and this file uses the same rule as the
# rest of the system for that.
NOT_DECIDABLE_ALONE = {
    "body.files-exist", "ptr.resolves", "ptr.every-file", "ptr.one-level",
    "whole.bom", "whole.no-orphans", "dir.bundled-known",
    "eval.exists", "eval.schema", "eval.min", "eval.files-resolve", "eval.name-matches",
    "ref.descriptive-name", "ref.toc-warn", "ref.toc-error", "ref.grep-patterns",
    "ref.no-duplication", "ref.dated", "asset.has-fields",
    "script.documented-constants", "script.no-network", "script.no-credentials",
    "script.no-installs", "name.matches-dir",
}


def sections(path: Path) -> dict[int, str]:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import blind
    return blind.sections(path)


def extract(text: str) -> str | None:
    """The first SKILL.md in the answer, fenced or not.

    Two forms both count, because both are the file: a fenced block whose first
    line is `---`, and a bare `---` … `---` frontmatter block written straight
    into the prose or indented as a walkthrough. Insisting on a fence would
    score a presentation choice as a missing deliverable - which this checker
    did, to the better of two answers, before the second form was added.

    Anchored on lines, never on the string `---`: a block that merely contains a
    rule of dashes is not frontmatter, and matching loosely is how an
    unterminated file gets reported as valid.
    """
    for m in FENCE.finditer(text):
        block = m.group(1)
        lines = block.split("\n")
        if lines and lines[0].strip() == "---" and any(l.strip() == "---" for l in lines[1:]):
            return _dedent(block)

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.strip() != "---":
            continue
        for j in range(i + 1, len(lines)):
            if lines[j].strip() == "---":
                block = "\n".join(lines[i:j + 1] + lines[j + 1:])
                body = "\n".join(lines[i + 1:j])
                if re.search(r"^\s*name:", body, re.M):
                    return _dedent(block)
                break
    return None


def _dedent(block: str) -> str:
    """Strip a uniform leading indent, so an indented walkthrough parses."""
    lines = [l for l in block.split("\n")]
    pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return "\n".join(l[pad:] if len(l) >= pad else l for l in lines)


def check(answer: Path, qid: int) -> dict:
    body = sections(answer).get(qid, "")
    art = extract(body)
    if art is None:
        return {"question": qid, "artifact": False,
                "verdict": "fail",
                "detail": "no SKILL.md produced — the answer described a file instead of "
                          "writing one, and the question asked for the file"}
    with tempfile.TemporaryDirectory() as t:
        name = "produced-skill"
        m = re.search(r"^name:\s*(\S+)\s*$", art, re.M)
        if m:
            name = m.group(1).strip().strip("'\"")
        d = Path(t) / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(art if art.endswith("\n") else art + "\n", encoding="utf-8")
        r = subprocess.run([sys.executable, str(CHECKER), str(d), "--json"],
                           capture_output=True, text=True)
        try:
            data = json.loads(r.stdout)
        except json.JSONDecodeError:
            return {"question": qid, "artifact": True, "verdict": "indeterminate",
                    "detail": f"the checker did not return JSON: {r.stdout[:120]}{r.stderr[:120]}"}
    rows = data["results"][0]["rows"] if data.get("results") else []
    errs = [x["id"] for x in rows if x["verdict"] == "FAIL" and x["severity"] == "error"
            and x["id"] not in NOT_DECIDABLE_ALONE]
    warns = [x["id"] for x in rows if x["verdict"] == "FAIL" and x["severity"] == "warn"
             and x["id"] not in NOT_DECIDABLE_ALONE]
    excluded = sorted({x["id"] for x in rows if x["verdict"] == "FAIL"
                       and x["id"] in NOT_DECIDABLE_ALONE})
    return {"question": qid, "artifact": True,
            "verdict": "pass" if not errs else "fail",
            "errors": errs, "warnings": warns,
            "not_decidable_here": excluded,
            "detail": f"{len(errs)} error(s), {len(warns)} warning(s)"
                      + (f" — {', '.join(errs[:5])}" if errs else "")
                      + (f" · excluded (needs the bundle): {', '.join(excluded)}" if excluded else "")}


if __name__ == "__main__":
    print(json.dumps(check(Path(sys.argv[1]), int(sys.argv[2])), indent=2))
