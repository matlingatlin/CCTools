# Reviewer calibration — preregistered 2026-09-03, before any run

**Question.** The v3 whole-artefact reviewer (phase 5.2: opus, effort high, the same prompt
every build uses) has returned a class-level finding on 12 of 12 reviews across four builds.
Is that the texts, or the reviewer's bar?

**Method.** The same prompt, unchanged, on three skills that are adopted and used in this
library and that this reviewer has never seen: `eval-set-curation` (shipped v2 build),
`skill-measure` (shipped), `abstention-threshold-design` (shipped v2 build). Each gets a
bom.json generated from its bundle listing (kind by directory), as a build would supply.

**Decision rule, fixed now.**
- 0 or 1 of 3 red at class level: the bar is reachable; the sweep's texts were the problem.
  No contract change.
- 2 or 3 of 3 red at class level: the bar as applied is not reachable by working skills in
  three rounds. Then the contract narrows what counts as CLASS for the review cap: a
  finding is cap-relevant only if it makes a step unexecutable as written, or makes an
  expectation grade the opposite of a rule, or makes the description promise a mode the
  body has no path for. Other class findings still force one rewrite but do not count
  toward the abandon cap. The narrowing is written into chain 3.2.0 and decide.py reads it.

**Not decided by this.** Whether the reviewer's findings are wrong. Every finding so far
has quoted real lines; the question is only whether the bar ends builds that should ship.
