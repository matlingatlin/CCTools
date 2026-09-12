# LESSONS — what the loop has learned (read at the start of every wave)


```
CONFIG (pinned 2026-08-28)
high_water: 0.50     # yield >= this -> seek-more
low_water:  0.10     # yield < this, over >= min_iters -> deprioritize
min_iters:  2        # a verdict needs at least this many iterations of that source_type
window_N:   10       # exact usage window for the capability-health rule
```

Deterministic, recomputed from `pipeline/metrics.jsonl` by `wave-reflect` at the end of each
wave. `/piano` step 1 reads the ACTIVE DIRECTIVES before picking a job; `research-scout`
consumes the source-yield verdicts. Related: [[testing-skills-methodology]], [[research-methodology]].

## ACTIVE DIRECTIVES (apply before choosing the next job)
- `[2026-08-28]` **An allowlist in an analysis script is a silent filter — derive the groups from
  the data.** `signals.py` grouped yield by a hardcoded set of six harvest source types. Thirteen
  of twenty-five metrics rows — every build wave and every curation pass — were dropped from a
  table that read as though it covered the loop's entire output, and any newly introduced
  source_type would have vanished the same way, with nothing in the output to show it. Fixed by
  making the set a DISPLAY grouping and printing unlisted types explicitly. The fix immediately
  exposed the next instance of the producer-vs-consumer error: `curate` computes 0/34 kept,
  because a curation pass produces talents tested and defects fixed, not candidates kept — left
  unlabelled it would have computed to *deprioritize the curator*. Non-harvest rows are now marked
  "NOT a yield — rule 1 does not apply". **Standing rule: before a rule fires on a group, check
  that "kept out of seen" is what that group actually produces. And never let an analysis script
  silently exclude rows it does not recognise — print them.**

- `[2026-08-28]` **Zero is a measurement; truthiness deletes it.** `signals.py` computed
  time-to-detect with `if d.get('lived_waves')`, which is false for `0`. A defect caught in the
  same wave the talent was born — the FASTEST detection possible — was therefore filed in the
  "existed since inception" bucket, i.e. the worst-case one. The best outcome was being scored as
  the worst, and the reading looked plausible either way. It fired the first time we actually
  achieved 0 (source-grounded-implementation, wave 27); before that no row could expose it. Fixed
  to `is not None`; median moved 12 → 10 and the schema header stopped being counted as a defect.
  **Standing rule for every metric we compute: a count, a duration, and a rate all have a
  meaningful 0. Test `is not None`, never truthiness — and make sure the sentinel for "not
  measured" is `null`, distinct from a measured zero.** Third measurement bug in the same file
  after producer-vs-consumer and stock-vs-flow: the analysis layer needs the same adversarial
  testing the talents get, because a wrong number reads exactly like a right one.

- `[2026-08-28]` **A producer's yield is its CANDIDATES, not the consumer's adoptions — this
  nearly killed our best source.** `yield_rate = adopted/seen` scores harvest at 0.00, because
  adoption happens in a LATER build wave. Waves 9/10 over practitioner repos produced 10 candidate
  methods (7 build-worthy) and were recorded `adopted: 0`, which computes to *deprioritize* under
  the pinned config — the exact opposite of the CONFIRMED lesson those same waves produced. The
  rows' own notes said "candidates queued for build"; the number did not. Fixed in `wave-reflect`
  (a `candidates` field, and the rule to measure each pass by its own output). **Standing rule:
  when a computed verdict contradicts a lesson you trust, suspect the metric before obeying it —
  an automated rule executing on a mismeasured stage is confident and wrong.**

- `[2026-08-28]` **Curated "best-of" lists are INDEXES, not sources — harvest what they point AT.**
  Five hand-picked blog lists (ayautomate, codetocloud, dev.to, composio, + a ranked top-100)
  were run through the gates. Result: **~50 named items, 2 method-shaped candidates.** The rest
  split into three predictable buckets, now the standing triage for any list:
  (a) **aggregator lists** pointing at other lists (awesome-*) → skip, they add a hop not a method;
  (b) **tools/integrations** (LSP plugins, MCP connectors, doc mirrors, packers) → fail
      talent-worthiness: we adopt METHODS, not libraries. "We already use it" is not "adopt it";
  (c) **already held** — the top ranks are the repos we harvested first (superpowers, ECC,
      anthropics/skills), because ranking and our own prior search agree on what is prominent.
  The 2 survivors were both *methods with a gap we could name*. Rule: read a list only to extract
  owner/repo paths, dedup against `seen`, then judge each repo on its own — never harvest "the list".

- `[2026-08-27]` **BUILD in the loop, in parallel — highest yield by far.** Wave 8 (parallel)
  built 6 talents (yield 1.0) vs harvest waves' ~0. The rich talent seam is BUILDING the
  validated `build_candidates`, not harvesting more repos. Interleave: every wave should
  fan out build-agents over the build queue alongside harvest, coordinator commits.
- `[2026-08-27]` **Practitioner/framework repos > lists/vendor-refs — CONFIRMED.** Wave 9/10
  (two loops over dspy/outlines/simonw/pydantic-ai/hamelsmu) yielded **10 candidate methods,
  7 build-worthy** (vs 0 from vendor/reference repos). Harvest the *methods* practitioners
  encode; the frameworks themselves are libraries (not adopted). Eval methods are the
  richest seam (hamelsmu: judge-calibration, error-taxonomy, synthetic-eval-data).
- `[2026-08-27]` **Two loops ≠ more throughput on a small box.** Two 3-agent loops shared the
  global W=2 cap and finished in ~one-6-agent-loop's time. Prefer ONE loop with more items
  for speed; add CPU cores to widen W. Use multiple loops only to separate concerns.
- `[2026-08-27]` **Deprioritize `source_type=web-top-n` and vertical "awesome-list" repos** —
  yield 0.00 over 2 waves (wave 2, wave 3). They are library/utility, not factory talents.
  Prefer deep-reading a single **primary** source (one focused repo, a paper, a profile).
- `[2026-08-27]` **Official-vendor repos (anthropics/skills) = high-quality LIBRARY +
  occasional METHODOLOGY** — wave 5: 19 polished vertical skills, 0 factory talents, but 1
  knowledge note + 1 method-gap (`skill-description-optimizer`). Harvest vendor repos for
  **knowledge/method**, not talent count; don't expect adopts.
- `[2026-08-27]` **research-scout: seek single-repo primary sources and researcher/company
  outputs**, not more curated lists — those are the higher-yield shape so far.
- `[2026-08-27]` **Deep re-read beats description-only triage** — a curate/re-audit wave
  (wave 4) yielded 10 validated talents where surface triage had found 0. When a large
  source was triaged fast, schedule a deep pass on its high-value tier.

## SOURCE-YIELD TABLE (adopted+adapted / seen, by source_type)
| source_type | waves | seen | yield | verdict |
| --- | --- | --- | --- | --- |
| web-top-n | 1 | 12 | 0.00 | _no verdict — 1 iter < min_iters 2_ |
| github (awesome-list shape) | 1 | 277 | 0.00 | deprioritize |
| github-vendor (official, e.g. anthropics) | 1 | 19 | 0.00 talents / high knowledge | harvest for method+knowledge |
| github (deep re-read of primary) | 1 | 157 | 0.06 | seek-more |
| build (parallel build of candidates) | 1 | 6 | 1.00 | **do more — highest yield** |

## LIBRARY HEALTH
- **Review-for-prune (adopted but unused in last 10 waves):** _(none yet — needs more waves
  of `talents_used` data before pruning is meaningful.)_
- **Descriptions to sharpen (overlap / mis-trigger risk):** _(run `skill-stocktake`; none
  flagged yet.)_

## DIMINISHING RETURNS
- Not triggered. (Rule: 2 consecutive waves with adopted=0 AND no new sources → pause + ask.)
