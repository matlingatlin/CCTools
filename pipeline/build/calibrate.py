#!/usr/bin/env python3
"""Phase 6.3 - check the grader before believing the grader.

A grader reporting "no findings" has said one of two things and you cannot tell
which: the artefact is clean, or the grader is blind. This hands it a specimen
carrying exactly ONE planted defect, without saying so, and asks whether it comes
back.

Three rules the design turns on:

  ONE defect, never several. With several you learn only that the grader found
  something. With one you learn whether it finds THAT class - and a class is what
  you are trusting it on.

  The defect is planted in a REAL output, not a fixture. A grader that behaves
  differently on obviously-synthetic text has told you nothing about the run.

  A grader that misses its planted class does not make the grading FAIL. It makes
  it INDETERMINATE - the same verdict the rest of this system gives a check that
  could not run. The skill may be fine; the instrument is unproven, and those are
  different states.

    python3 calibrate.py plant <file> <kind> [--out FILE]
    python3 calibrate.py score <planted.json> <grader-report.json>
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

CAUGHT, MISSED, PARTIAL = "caught", "missed", "partial"


class NotPlantable(Exception):
    """The specimen has nothing of that kind to break - itself a finding."""


# --- the defect catalogue ----------------------------------------------------
# Each entry: what it breaks, and the class a grader must NAME to have caught it.
# The class matters more than the location: a grader that says "something is off
# around line 40" has not demonstrated it can find unsourced claims.

def _unquote_yaml_description(text: str) -> tuple[str, str]:
    """Make the frontmatter unparseable by removing the quotes around a value
    that contains a bare colon-space. Silent, and the skill will not load."""
    m = re.search(r'^(description:\s*)"(.*)"\s*$', text, re.M)
    if not m or ": " not in m.group(2):
        raise NotPlantable("no quoted description containing a bare colon-space")
    return text[:m.start()] + m.group(1) + m.group(2) + text[m.end():], "frontmatter does not parse"


def _drop_a_source_date(text: str) -> tuple[str, str]:
    m = re.search(r"\b(19|20)\d{2}-\d{2}-\d{2}\b", text)
    if not m:
        raise NotPlantable("no fetch date to remove")
    return text[:m.start()] + "recently" + text[m.end():], "a claim lost its fetch date"


def _strip_a_quote(text: str) -> tuple[str, str]:
    """Turn a verbatim quote into a paraphrase - the claim survives, its warrant
    does not, and nothing about the page looks wrong."""
    m = re.search(r"^> (.+)$", text, re.M)
    if not m:
        raise NotPlantable("no block quote to paraphrase")
    words = m.group(1).split()
    if len(words) < 8:
        raise NotPlantable("the quote is too short to paraphrase detectably")
    para = "In substance, " + " ".join(words[:6]).lower() + " and so on."
    return text[:m.start()] + "> " + para + text[m.end():], "a claim is no longer verbatim"


def _overstate_a_number(text: str) -> tuple[str, str]:
    m = re.search(r"\b(\d{1,3})(\.\d+)?%", text)
    if not m:
        raise NotPlantable("no percentage to overstate")
    val = int(m.group(1))
    return text[:m.start()] + f"{min(99, val * 3)}%" + text[m.end():], "a figure contradicts its source"


def _remove_a_negative_boundary(text: str) -> tuple[str, str]:
    """Delete the sentence saying what the unit is NOT for. The description still
    reads well and now collides with its neighbour."""
    m = re.search(r"[^.]*\b(NOT for|not for|never for)\b[^.]*\.", text)
    if not m:
        raise NotPlantable("no negative boundary to remove")
    return text[:m.start()] + text[m.end():], "the boundary against a sibling is gone"


CATALOGUE = {
    "unparseable-frontmatter": _unquote_yaml_description,
    "undated-source": _drop_a_source_date,
    "paraphrased-quote": _strip_a_quote,
    "overstated-figure": _overstate_a_number,
    "missing-boundary": _remove_a_negative_boundary,
}


# --- the answer-transcript catalogue ----------------------------------------
# The five kinds above all mutate a SKILL ARTEFACT: frontmatter, sources,
# quotes, figures, boundaries. On 2026-09-01 a build needed to calibrate a
# grader reading ANSWER TRANSCRIPTS - the outputs of the measured arms - and
# none of the five applied, so the class was planted by hand and the deviation
# recorded. These are the same instrument for that material, and they are
# written domain-agnostically: none of them knows what the answer is about.

def _shift_the_recommendation(text: str) -> tuple[str, str]:
    """Move a RECOMMENDED numeric value off the one the reasoning argues for,
    leaving every supporting sentence intact. The answer still reads well and
    the recommendation no longer follows from it.

    Two constraints learned from a bad plant: the verb must actually be a
    recommendation - a bare "use" caught a precision target the asker had
    GIVEN, which is not the answer's own recommendation - and the moved value
    must stay plausible. A mutation to 102% precision does not calibrate a
    grader on subtle defects; it tests whether it can see nonsense, which is a
    far lower bar and passes graders that would miss the real thing.
    """
    pat = (r"(recommend\w*|\bcuts?\b|\bthresholds?\b)"
           r"[^\d\n]{0,28}?(\d+\.\d+|\d+(?:\.\d+)?%|\d+)")
    for m in re.finditer(pat, text, re.I):
        raw = m.group(2)
        if raw.endswith("%"):
            val = float(raw[:-1])
            moved_v = val - 7 if val > 50 else val + 7
            if not 0 < moved_v < 100:
                continue
            moved = f"{moved_v:g}%"
        elif "." in raw:
            val = float(raw)
            moved_v = val + 0.05 if val + 0.05 < 1 or val > 1 else val - 0.05
            if moved_v <= 0:
                continue
            moved = f"{moved_v:.3f}".rstrip("0").rstrip(".")
        else:
            val = int(raw)
            if val <= 1:
                continue
            moved = str(val + max(1, val // 10))
        s, e = m.span(2)
        return (text[:s] + moved + text[e:],
                "the recommendation does not follow from its own reasoning")
    raise NotPlantable("no recommended numeric value to move")


def _strip_a_hedge(text: str) -> tuple[str, str]:
    """Delete the qualifier from a tentative claim so it reads as established.
    Nothing else changes, and the sentence is now more confident than the
    evidence behind it."""
    m = re.search(r"\b(probably|likely|roughly|approximately|about|may |might |appears to |"
                  r"suggests that |on this evidence )", text)
    if not m:
        raise NotPlantable("no hedge to strip")
    return text[:m.start()] + text[m.end():], "a tentative claim is stated as established"


def _drop_a_prerequisite_check(text: str) -> tuple[str, str]:
    """Remove the sentence that says something must be verified BEFORE acting,
    leaving the action. The answer still recommends the same thing, now with no
    gate in front of it."""
    gate = r"\b(?:before|first|until)\b"
    verb = r"\b(?:check|verify|confirm|test|validate|measure|separat\w+)\b"
    for pat in (rf"[^.\n]*{gate}[^.\n]*{verb}[^.\n]*\.",
                rf"[^.\n]*{verb}[^.\n]*{gate}[^.\n]*\."):
        m = re.search(pat, text, re.I)
        if m and len(m.group(0).strip()) > 20:
            return (text[:m.start()] + text[m.end():],
                    "a stated prerequisite check has been dropped")
    raise NotPlantable("no prerequisite check to drop")


def _invert_a_refusal(text: str) -> tuple[str, str]:
    """Turn a refusal into an assent. The reasoning still explains why the
    answer should be no, and the answer is now yes."""
    for pat, rep in ((r"\bcan(?:not| not|'t)\b", "can"),
                     (r"\bshould(?:n't| not)\b", "should"),
                     (r"\bdoes(?:n't| not)\b", "does"),
                     (r"\bdo(?:n't| not)\b", "do"),
                     (r"\bis(?:n't| not)\b", "is"),
                     (r"\bwo(?:n't)\b|\bwill not\b", "will"),
                     (r"\bnot defensible\b", "defensible")):
        m = re.search(pat, text, re.I)
        if m:
            return (text[:m.start()] + rep + text[m.end():],
                    "the conclusion contradicts the reasoning that precedes it")
    raise NotPlantable("no refusal to invert")


TRANSCRIPT_CATALOGUE = {
    "shifted-recommendation": _shift_the_recommendation,
    "stripped-hedge": _strip_a_hedge,
    "dropped-prerequisite-check": _drop_a_prerequisite_check,
    "inverted-refusal": _invert_a_refusal,
}

ARTEFACT_CATALOGUE = CATALOGUE
ALL_CATALOGUES = {"artefact": ARTEFACT_CATALOGUE, "transcript": TRANSCRIPT_CATALOGUE}


def catalogue_for(text: str, kind_set: str | None = None) -> dict:
    """Which catalogue applies. Frontmatter means a skill artefact; anything
    else is treated as a transcript. An explicit kind_set overrides the sniff,
    because a guess about material is not something to make silently."""
    if kind_set:
        if kind_set not in ALL_CATALOGUES:
            raise NotPlantable(f"unknown kind set {kind_set!r}; "
                               f"have {', '.join(sorted(ALL_CATALOGUES))}")
        return ALL_CATALOGUES[kind_set]
    return ARTEFACT_CATALOGUE if re.match(r"^---\s*$", text.split("\n")[0] or "") \
        else TRANSCRIPT_CATALOGUE


def plant(text: str, kind: str, kind_set: str | None = None) -> dict:
    cat = catalogue_for(text, kind_set)
    if kind not in cat:
        raise NotPlantable(f"unknown defect kind {kind!r}; have {', '.join(sorted(cat))}")
    mutated, cls = cat[kind](text)
    if mutated == text:
        raise NotPlantable(f"{kind} changed nothing - the specimen has no such thing to break")
    return {"kind": kind, "class": cls, "specimen": mutated,
            "note": "exactly one change; the grader is not told a defect exists"}


def choose(text: str, seed: int | None = None, kind_set: str | None = None) -> dict:
    """Whichever defect this specimen can actually carry, chosen at random.

    Not the first that works: a fixed order means the same class is tested every
    time, and a grader blind to everything else keeps passing.
    """
    kinds = list(catalogue_for(text, kind_set))
    random.Random(seed).shuffle(kinds)
    problems = []
    for k in kinds:
        try:
            return plant(text, k, kind_set)
        except NotPlantable as exc:
            problems.append(f"{k}: {exc}")
    raise NotPlantable("nothing plantable in this specimen — " + "; ".join(problems))


# --- scoring -----------------------------------------------------------------

def score(planted: dict, report: str) -> dict:
    """Did the grader name the planted CLASS, not merely find something?"""
    text = report.lower()
    cls = planted["class"].lower()
    key = [w for w in re.findall(r"[a-z]{4,}", cls) if w not in {"lost", "does", "with", "from"}]
    hits = [w for w in key if w in text]
    found_anything = bool(re.search(r"\b(finding|defect|problem|issue|wrong|missing|broken|fails?)\b", text))

    if len(hits) >= max(2, len(key) - 1):
        verdict, detail = CAUGHT, f"named the class ({', '.join(hits)})"
    elif hits:
        verdict, detail = PARTIAL, (f"touched the area ({', '.join(hits)}) without naming the class - "
                                    f"a grader that says something is off near the defect has not "
                                    f"shown it can find that class")
    elif found_anything:
        verdict, detail = MISSED, "reported findings, none of them the planted one"
    else:
        verdict, detail = MISSED, "reported nothing"

    return {"planted": planted["kind"], "class": planted["class"], "verdict": verdict,
            "detail": detail,
            "consequence": ("the grading may be believed" if verdict == CAUGHT else
                            "the GRADING IS INDETERMINATE, not failed - the artefact may be fine "
                            "and the instrument is unproven, and those are different states")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plant"); p.add_argument("file"); p.add_argument("kind", nargs="?")
    p.add_argument("--kind-set", default=None, choices=sorted(ALL_CATALOGUES),
                   help="artefact (a SKILL.md) or transcript (an answer). "
                        "Sniffed from frontmatter when omitted.")
    p.add_argument("--out"); p.add_argument("--seed", type=int)
    s = sub.add_parser("score"); s.add_argument("planted"); s.add_argument("report")
    a = ap.parse_args()

    if a.cmd == "plant":
        text = Path(a.file).read_text(encoding="utf-8")
        try:
            d = (plant(text, a.kind, a.kind_set) if a.kind
                 else choose(text, a.seed, a.kind_set))
        except NotPlantable as exc:
            print(f"CANNOT PLANT: {exc}", file=sys.stderr)
            return 2
        out = Path(a.out) if a.out else Path(a.file).with_suffix(".planted.md")
        out.write_text(d["specimen"], encoding="utf-8")
        meta = out.with_suffix(".meta.json")
        meta.write_text(json.dumps({k: v for k, v in d.items() if k != "specimen"}, indent=2))
        print(f"specimen: {out}\nkey (do NOT give the grader): {meta}\nplanted: {d['kind']} — {d['class']}")
        return 0

    planted = json.loads(Path(a.planted).read_text(encoding="utf-8"))
    r = score(planted, Path(a.report).read_text(encoding="utf-8"))
    print(json.dumps(r, indent=2))
    return 0 if r["verdict"] == CAUGHT else 1


if __name__ == "__main__":
    sys.exit(main())
