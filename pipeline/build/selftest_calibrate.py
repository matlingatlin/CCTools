#!/usr/bin/env python3
"""Controls for the grader calibration.

The thing being built here is an instrument for distrusting an instrument, so it
needs its own. Two failure modes matter and they pull in opposite directions:

  a planter that changes nothing, so every grader "passes" and the calibration is
  theatre; and

  a scorer that credits a grader for finding SOMETHING, so a grader blind to the
  planted class passes on an unrelated finding.

    python3 selftest_calibrate.py [-v]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calibrate as cal  # noqa: E402

R: list[tuple[bool, str]] = []


def check(ok, label, detail=""):
    R.append((ok, f"{label}{'  — ' + detail if detail and not ok else ''}"))


SPECIMEN = '''---
name: example-skill
description: "Use when reviewing a thing. Emits one VERDICT: GO or NO-GO line. NOT for authoring."
---

# Example

Fetched 2026-08-30 from the source below.

> The measured conflict rate reached 46.3% across the sampled judge pairs in our study.

The effect is around 46.3% in the worst pair.
'''


def _transcript_cases():
    """The answer-transcript catalogue, added because none of the five artefact
    kinds applies to an answer and a build had to plant its class by hand."""
    from calibrate import (plant, choose, catalogue_for, NotPlantable,
                           TRANSCRIPT_CATALOGUE, ARTEFACT_CATALOGUE)

    TRANSCRIPT = (
        "**Cut: score >= 0.506.** That's the highest-coverage cut that clears 95% "
        "precision: 55.5% of records (111/200) auto-approve at 95.5% precision.\n\n"
        "Check the confidence score actually separates right from wrong (bucket by "
        "decile, compute AUROC) before trusting it for anything.\n\n"
        "No reviewer-capacity target was given, so I can't price that against headcount. "
        "The signal probably behaves the same way on your data.\n"
    )
    ARTEFACT = '---\nname: x\ndescription: "Use when: a thing. NOT for: another thing."\n---\n\n# X\n'

    # 1. The sniff routes material to the right catalogue, and does not guess.
    check(catalogue_for(TRANSCRIPT) is TRANSCRIPT_CATALOGUE, "a transcript gets the transcript kinds")
    check(catalogue_for(ARTEFACT) is ARTEFACT_CATALOGUE, "frontmatter gets the artefact kinds")
    check(catalogue_for(TRANSCRIPT, "artefact") is ARTEFACT_CATALOGUE,
          "an explicit kind set overrides the sniff")

    # 2. Every transcript kind plants on representative prose. A catalogue entry
    #    that cannot plant anywhere is a kind the grader is never tested on.
    for k in TRANSCRIPT_CATALOGUE:
        try:
            d = plant(TRANSCRIPT, k, "transcript")
            check(d["specimen"] != TRANSCRIPT, f"{k} changes the text")
            check(bool(d["class"]), f"{k} names a class the grader must say")
        except NotPlantable as exc:
            check(False, f"{k} plants on representative prose", str(exc))

    # 3. THE ONE THAT MATTERS. The recommendation moves while the sentence around
    #    it still argues for the original - this is the defect a build planted by
    #    hand on 2026-09-01 because the catalogue could not.
    d = plant(TRANSCRIPT, "shifted-recommendation", "transcript")
    check("0.506" not in d["specimen"].split(".**")[0], "the recommended value actually moved")
    check("111/200" in d["specimen"] and "55.5%" in d["specimen"],
          "and the reasoning supporting the original is left intact")

    # 4. Plausibility, exercised on the PERCENTAGE path specifically. A mutation
    #    to an impossible figure tests whether a grader can see nonsense, which
    #    is a far lower bar than the real defect. The decimal fixture above never
    #    reaches this branch, so it needs prose whose recommendation IS a percent
    #    near the ceiling - without this case the guard cannot fail and the
    #    control is decoration.
    import re as _re
    HIGH = ("Recommended threshold: 96% precision on the answered set. "
            "That clears the bar with 40% coverage.\n")
    try:
        h = plant(HIGH, "shifted-recommendation", "transcript")
        pcts = [float(x) for x in _re.findall(r"(\d+(?:\.\d+)?)%", h["specimen"])]
        check(all(v <= 100 for v in pcts),
              "a percentage recommendation is moved to a possible value",
              f"got {pcts}")
        check(h["specimen"] != HIGH, "and it did move")
    except NotPlantable as exc:
        # NOT acceptable here. This fixture is built so a correct implementation
        # CAN plant it: 96% must move DOWN to 89%, not up into impossibility.
        # Treating a refusal as success let a broken arithmetic path through a
        # mutation test - the guard absorbed the bug instead of exposing it.
        check(False, "a 96% recommendation moves down to a possible value", str(exc))

    for pct in _re.findall(r"(\d+(?:\.\d+)?)%", d["specimen"]):
        check(float(pct) <= 100, f"planted figure {pct}% stays possible")

    # 5. An artefact kind must not be plantable in a transcript, and vice versa.
    try:
        plant(TRANSCRIPT, "unparseable-frontmatter", "transcript")
        check(False, "an artefact kind is refused on a transcript")
    except NotPlantable:
        check(True, "an artefact kind is refused on a transcript")

    # 6. choose() finds a workable kind rather than failing on the first miss.
    picked = choose(TRANSCRIPT, seed=3, kind_set="transcript")
    check(picked["kind"] in TRANSCRIPT_CATALOGUE, "choose picks from the right catalogue")
    check(picked["specimen"] != TRANSCRIPT, "choose returns a real mutation")

    # 7. NEGATIVE CONTROL: prose with nothing to break refuses, never invents.
    try:
        choose("Nothing here at all.\n", seed=1, kind_set="transcript")
        check(False, "unplantable prose refuses rather than inventing a defect")
    except NotPlantable:
        check(True, "unplantable prose refuses rather than inventing a defect")


def main() -> int:
    _transcript_cases()
    # every catalogue entry actually changes the text
    for kind in cal.CATALOGUE:
        try:
            d = cal.plant(SPECIMEN, kind)
        except cal.NotPlantable as exc:
            check(False, f"{kind} can be planted in a realistic specimen", str(exc)); continue
        check(d["specimen"] != SPECIMEN, f"{kind} actually changes the specimen")
        check(len(d["specimen"]) != len(SPECIMEN) or d["specimen"] != SPECIMEN,
              f"{kind} leaves a difference to find")

    # exactly one place changed, for the two that must be surgical
    import difflib
    for kind in ("undated-source", "overstated-figure"):
        d = cal.plant(SPECIMEN, kind)
        diff = [l for l in difflib.unified_diff(SPECIMEN.split("\n"), d["specimen"].split("\n"), n=0)
                if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
        check(len(diff) <= 2, f"{kind} touches one line, not several", f"{len(diff)} changed lines")

    # a specimen with nothing to break says so instead of silently passing
    try:
        cal.plant("just some prose with no frontmatter, no quote, no date, no percent.", "undated-source")
        check(False, "an unplantable specimen is refused", "it was accepted")
    except cal.NotPlantable:
        check(True, "an unplantable specimen is refused")

    # choose() picks among what fits, and is not always the same one
    seeds = {cal.choose(SPECIMEN, s)["kind"] for s in range(12)}
    check(len(seeds) > 1, "the planted class VARIES across runs — a fixed order tests one class "
                          "forever and a grader blind to the rest keeps passing", f"got {seeds}")

    # --- scoring ------------------------------------------------------------
    d = cal.plant(SPECIMEN, "undated-source")
    check(cal.score(d, "The claim lost its fetch date; nothing says when it was fetched.")["verdict"] == cal.CAUGHT,
          "naming the class counts as caught")
    r = cal.score(d, "I found a problem: the tone of the second paragraph is inconsistent.")
    check(r["verdict"] == cal.MISSED,
          "a grader that finds SOMETHING ELSE has missed it", r["detail"])
    check(cal.score(d, "No findings. The document looks correct.")["verdict"] == cal.MISSED,
          "a clean report on a planted specimen is a miss")
    r = cal.score(d, "Something about the date line reads oddly.")
    check(r["verdict"] in (cal.PARTIAL, cal.MISSED),
          "gesturing at the area without naming the class is not a catch", r["verdict"])

    # the consequence must be INDETERMINATE, never FAIL
    r = cal.score(d, "No findings.")
    check("INDETERMINATE" in r["consequence"] and "not failed" in r["consequence"],
          "a blind grader makes the grading indeterminate, not failed")

    bad = [m for ok, m in R if not ok]
    for ok, m in R:
        if "-v" in sys.argv or not ok:
            print(f"{'ok   ' if ok else 'FAIL '} {m}")
    print(f"\n{len(R) - len(bad)}/{len(R)} controls behaved")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
