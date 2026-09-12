---
title: Inter-rater agreement with kappa - the interpretation bands and the n-rater variant, as fetched 2026-09-09
sources:
  - url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3900052/
    note: "McHugh ML. Interrater reliability: the kappa statistic. Biochemia Medica 2012;22(3):276-282. Read for the bands and the n-rater statistic; the Landis & Koch 1977 bands were NOT in this article."
    fetched: 2026-09-09
status: verified
tags: [statistics, inter-rater, kappa, agreement, evaluation, scio, intake]
related: ["[[architecture-evidence]]"]
---
# Inter-rater agreement with kappa

Why this note exists: Scio's ADR-0018 stops intake when three blind derivations of the spec
agree "above a threshold written down before the first run". The threshold has to come from a
published band, cited, and the statistic has to be the one for three raters. Both were looked
up on 2026-09-09; neither is from memory.

## Claims

| # | Claim | Source | Verbatim / value | Verdict |
|---|---|---|---|---|
| 1 | Cohen's interpretation bands for kappa | McHugh 2012 | "values ≤ 0 as indicating no agreement and 0.01–0.20 as none to slight, 0.21–0.40 as fair, 0.41–0.60 as moderate, 0.61–0.80 as substantial, and 0.81–1.00 as almost perfect agreement" | MEASURED (fetched 2026-09-09) |
| 2 | McHugh's stricter bands (her Table 3) | McHugh 2012 | 0–.20 none · .21–.39 minimal · .40–.59 weak · .60–.79 moderate · .80–.90 strong · above .90 almost perfect | MEASURED (fetched 2026-09-09) |
| 3 | Kappa for more than two raters | McHugh 2012 | "the Fleiss kappa (adaptation of Cohen's kappa for 3 or more raters)" - named, not derived, in the article | MEASURED (the naming); the formula is not in this source |
| 4 | Landis & Koch 1977 bands | not found | The bands usually attributed to Landis & Koch (Biometrics 33:159-174) were not in the fetched article and have not been read from the paper itself | UNVERIFIED - do not cite as read |

## What it means here

Scio preregisters **kappa ≥ 0.80** as the convergence threshold (`packages/intake/src/convergence`):
the lower edge of McHugh's "strong" band and one hundredth under Cohen's "almost perfect". The
statistic over three raters is Fleiss' kappa over present/absent judgements per slot; the
pairwise Cohen table is reported beside it as the explanation a person can read ("rater B alone
had the staff role"). The formula for Fleiss' kappa used in code is the standard one (per-item
agreement P_i, mean P̄, expected P̄_e from category proportions, κ = (P̄ − P̄_e)/(1 − P̄_e)) and is
covered by a test against a hand-computed example rather than by a citation, because claim 3's
source names the statistic without stating it. Neighbours: [[architecture-evidence]] reports a
kappa of .82 between raters in the SEI mission-thread study, the one other place this base uses
the statistic.
