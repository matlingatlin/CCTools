# Reviewer calibration — result, 2026-09-03

Three adopted, in-use skills, same reviewer prompt as phase 5.2, opus, effort high, a BOM generated from each bundle.

| skill | verdict | findings | CLASS |
|---|---|---|---|
| abstention-threshold-design (shipped v2 build) | red | 11 | 5 |
| eval-set-curation (shipped v2 build) | red | 11 | 7 |
| skill-measure (shipped) | red | 9 | 5 |

| run | tokens | duration |
|---|---|---|
| eval-set-curation | 690658 | 267 s |
| skill-measure | 390997 | 127 s |
| abstention-threshold-design | 606422 | 233 s |

**3 of 3 red at class level.** Per PREREGISTERED.md this is the second branch: the bar as applied is not
reachable by working skills, so the review cannot be the gate that ends a build. The findings are not
noise - eval-set-curation ships with every expectation list empty, skill-measure's baseline table has an
unreachable row - so the reviewer is a good critic. It is a bad gate. Fifteen of fifteen reviews red.

Outputs: calib.review.*.md beside this file.
