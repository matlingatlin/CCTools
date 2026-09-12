#!/usr/bin/env python3
"""Build a BLINDED grading prompt from two arms' outputs, and keep the key apart.

Phase 6.4. The grader must not be able to tell which answers came from the arm
that had the method. If it can, it is not grading the answers - it is grading the
label, and every ambiguous call will land on the side it expects to win.

So the two arms are relabelled A and B by a coin flip seeded per scenario, the
mapping is written to a key file the grader is never given, and the grader is
asked to rule per expectation with a quoted line as evidence.

It is also asked to attack the expectations themselves. Whoever wrote them cannot
rule on whether they were the right ones, and an expectation that both arms
satisfy trivially is a measurement that was never going to discriminate.

    python3 blind.py <run-dir> <skill> <repeat>   # writes prompt + key
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2] / "skills"
RUN_DIR = Path(".")


def coin(skill: str, repeat: int, qid: int) -> bool:
    """Deterministic per (skill, repeat, question) - reproducible, not guessable."""
    h = hashlib.sha256(f"{skill}|{repeat}|{qid}".encode()).hexdigest()
    return int(h[:8], 16) % 2 == 0


def sections(path: Path) -> dict[int, str]:
    """Split an answer file on the harness's OWN markers, and nothing else.

    Only `## Qn` and `## consulted` end a section. Every other line is content,
    fenced or not.

    The first version broke on any `## ` heading. An answer that produces a
    SKILL.md contains `## Steps` inside it, so the parser cut the artefact in
    half and the artefact check reported "no file produced" for the answer that
    produced the better file. Making it fence-aware was not enough: the winning
    answer had written the file UNFENCED, as an indented walkthrough, which is a
    presentation choice and not a failure.

    So the rule is inverted. The harness recognises its own markers; it does not
    try to recognise the answer's. An answer cannot collide with a marker it was
    told to write. Found 2026-08-30, by checking a surprising result against the
    raw file before reporting it - a per-question loss that was a parser bug.
    """
    out, cur, buf = {}, None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip().lower()
        is_q = s.startswith("## q") and s[4:].split()[0].rstrip(".").isdigit() if len(s) > 4 else False
        if is_q or s == "## consulted":
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur = int(line.strip()[4:].split()[0].rstrip(".")) if is_q else None
            buf = []
            continue
        if cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def build(skill: str, repeat: int) -> tuple[Path, Path]:
    ev = json.loads((SKILLS / skill / "evals" / "evals.json").read_text(encoding="utf-8"))
    runs = RUN_DIR / "runs"
    with_s = sections(runs / f"{skill}.with.r{repeat}.md")
    without_s = sections(runs / f"{skill}.without.r{repeat}.md")

    key, out = {}, []
    out.append(
        "You are grading two anonymised answers to each question below. You do not know how "
        "either was produced, and you must not speculate about it.\n\n"
        "IMPORTANT: the labels A and B are re-randomised FOR EVERY QUESTION. Answer A in "
        "question 1 and answer A in question 2 are not the same source. Do not write anything "
        "that treats A or B as a consistent identity across questions - a cross-question "
        "narrative about 'A' has no basis and will be discarded.\n\n"
        "For EACH question, for EACH listed expectation, rule on answer A and answer B "
        "independently: met / not met / unclear. Every ruling must quote the line from that "
        "answer that decides it. If nothing in the answer decides it, the ruling is 'not met' "
        "and you say what you looked for.\n\n"
        "Then, for each question, answer one more thing: **is this expectation set any good?** "
        "Name any expectation that both answers satisfy trivially, or that could be satisfied "
        "by an answer that misses the point. An expectation nothing could fail is not a "
        "measurement.\n\n"
        "Return strict JSON and nothing else:\n"
        '{"per_question": [{"id": 1, "rulings": [{"expectation": "...", "A": "met|not met|unclear", '
        '"A_evidence": "quoted line", "B": "...", "B_evidence": "..."}], '
        '"expectation_critique": "..."}], "overall": "..."}\n')

    for e in ev["evals"]:
        qid = e["id"]
        flip = coin(skill, repeat, qid)
        a_arm, b_arm = ("with", "without") if flip else ("without", "with")
        key[str(qid)] = {"A": a_arm, "B": b_arm}
        a_txt = (with_s if a_arm == "with" else without_s).get(qid, "(no answer given)")
        b_txt = (with_s if b_arm == "with" else without_s).get(qid, "(no answer given)")
        out.append(f"\n{'=' * 70}\nQUESTION {qid}\n{e['prompt']}\n")
        out.append("EXPECTATIONS:\n" + "\n".join(f"  - {x}" for x in e["expectations"]))
        out.append(f"\n--- ANSWER A ---\n{a_txt}\n\n--- ANSWER B ---\n{b_txt}\n")

    p = RUN_DIR / "runs" / f"{skill}.grade.r{repeat}.prompt.txt"
    k = RUN_DIR / "runs" / f"{skill}.key.r{repeat}.json"
    p.write_text("\n".join(out), encoding="utf-8")
    k.write_text(json.dumps(key, indent=2), encoding="utf-8")
    return p, k


if __name__ == "__main__":
    RUN_DIR = Path(sys.argv[1])
    prompt, key = build(sys.argv[2], int(sys.argv[3]))
    print(f"prompt: {prompt}\nkey (do NOT give to the grader): {key}")
