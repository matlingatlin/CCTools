#!/usr/bin/env python3
"""The SHAPE axis, graded by CODE. The contract: 'the output conforms where the
baseline's does not ... Graded by CODE, so this axis has no blind judge.'

The shape this skill's steps require, and the one the probe showed the baseline
reaches only sometimes: every difference assigned to exactly one of two sides,
with the two sides reported as TWO SEPARATE COUNTS. A single failure tally with
the benign rows filed inside it is the observed failure (OBS-2).
"""
import re, sys, json
def shape_ok(text: str) -> tuple[bool, str]:
    t = text.lower()
    # both side-words present as labels
    has_block = bool(re.search(r"\bblock(?:s|ed|ing)?\b|\bstop the batch\b|\bhard breach", t))
    has_widen = bool(re.search(r"\bwiden\b|\bratif", t))
    if not (has_block and has_widen):
        return False, "the two sides are not both named as sides"
    # two counts, side by side
    m = re.search(r"block[^.\n]{0,20}?(\d+)[^.\n]{0,40}?widen[^.\n]{0,20}?(\d+)", t)
    m2 = re.search(r"widen[^.\n]{0,20}?(\d+)[^.\n]{0,40}?block[^.\n]{0,20}?(\d+)", t)
    if not (m or m2):
        return False, "both sides are named but no pair of counts is reported"
    return True, f"two counts reported: {(m or m2).group(0)[:60]!r}"
if __name__ == "__main__":
    for p in sys.argv[1:]:
        ok, why = shape_ok(open(p).read())
        print(json.dumps({"file": p.split("/")[-1], "shape_ok": ok, "why": why}))
