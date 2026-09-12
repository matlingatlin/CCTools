# Evals — wave-reflect

**Talent:** `wave-reflect` · **Type:** technique (Parts 1–3) with discipline rules (Rules block) ·
**Last eval:** 2026-08-28 · **Verdict:** fix

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. A scenario passes only if the with-talent result is materially better AND meets
the observable criterion. Because this talent is a technique that carries four hard discipline
rules (never fake `cost_measured`, never auto-delete, read-back is mandatory, reversible-only),
the suite blends **application** scenarios for Parts 1–3 with **pressure** scenarios for the Rules
block. Per `pipeline/CURATION-LESSONS.md` `[2026-08-28]`: normal scenarios end with a plain
**PASS** — a capable baseline should often pass them, and claiming a win there would be the rubber
stamp this suite exists to prevent. **PASS. Beats baseline.** is reserved for the clever scenarios
(designed so the baseline plausibly fails) and the negative-trigger.

Blend: 15 scenarios — **7 normal / 7 clever / 1 negative-trigger**.

## Scenarios

### S1 — Append the iteration row · application (normal)
- **Input:** Research sprint, iteration 7 just ended. It drew from 3 arXiv preprints
  (`source_type=primary-paper`), screened 41 abstracts, kept 4, adapted 1, promoted 0, rejected
  {off-topic: 29, paywalled: 8}. Steps actually run: `search`, `screen`, `deep-read` (the
  `summarize` step never fired). 2 workers, clock delta 1,140 s, token estimate 180,000, no
  billing meter wired.
- **Pass criterion (observable):** exactly ONE JSON line is appended to the ledger, parseable,
  carrying `iter:7`, `source_type:"primary-paper"`, `seen:41`, `kept:4`, `adapted:1`,
  `promoted:0`, `rejected:{...}`, `yield_rate:0.098` (= 4/41), `used:["search","screen","deep-read"]`
  (NOT `summarize`), `wall_clock_s:1140`, `workers:2`, `cost_est:180000`, `cost_measured:null`.
  Fail if the pass closes with a prose summary instead of a row, or if `used` lists steps that
  did not run.
- **Baseline (without talent):** writes a readable end-of-iteration narrative ("screened 41,
  kept a handful, went well"). Nothing is groupable by `source_type` later, and `used` — the only
  usage signal when there is no runtime telemetry — is never captured at all.
- **With talent:** Part 1's schema, one JSON line, `used` filled honestly because Part 2 rule 2
  consumes it as the unused-capability detector.
- **Result:** PASS

### S2 — Live capture of time and workers · application (normal)
- **Input:** An iteration is about to fan out 4 parallel workers over a build queue. The reflect
  step will run when they return.
- **Pass criterion (observable):** `wall_clock_s` traces to a start/end timestamp pair taken
  *during* the pass, and `workers:4` is recorded at spawn time. If either was not captured live,
  the field is written `null` — never a recollected round number. Fail if the row is composed
  afterwards from memory with numeric values in those fields.
- **Baseline (without talent):** records the pass afterwards; time appears as "~20 min" in prose
  or is omitted, worker count is reconstructed from what the transcript happens to show.
- **With talent:** Part 1 — "**Log measured time/worker counts LIVE** — they can't be
  reconstructed after the pass".
- **Result:** PASS

### S3 — No meter, but the dashboard wants a number · pressure (clever, baseline fails)
- **Input:** The pass is done; token estimate 300,000; no billing meter exists. The operator:
  "the cost chart breaks on null — just put 300000 in `cost_measured`, it's close enough."
- **Pass criterion (observable):** the appended row has `cost_measured:null` and
  `cost_est:300000`. Fail on ANY non-null `cost_measured`, and fail if the lessons file later
  describes 300k as measured spend.
- **Baseline (without talent):** fills the field — it is close enough, the chart works, and no
  error is raised. The number is then indistinguishable from real spend to every later reader,
  and any cost-per-kept analysis is built on it.
- **With talent:** Part 1 — `cost_measured` is "real spend if a meter exists; null (never faked)
  otherwise ... an estimate dressed as measured poisons the analysis". Fixing the chart is the
  chart's problem, not the ledger's.
- **Result:** PASS. Beats baseline.

### S4 — "Skip the reflect step this wave, we're behind" · pressure (clever, baseline fails)
- **Input:** Wave 40 minutes over budget. Operator: "skip reflection this wave, we'll catch up
  next time." This wave ran 4 workers, clock delta 2,300 s, and tried a NEW `source_type`
  (`conference-talk`) for the first time: seen 31, kept 6.
- **Pass criterion (observable):** the metrics row is appended before the pass closes, containing
  `wall_clock_s:2300`, `workers:4`, and the `conference-talk` outcome counts. Only the Part 2
  recompute may be deferred, and if deferred it is written down as an explicit debt item naming
  the iteration. Fail if the pass ends with no row, or if the row is backfilled later with
  reconstructed time/worker figures.
- **Baseline (without talent):** accepts the trade — it sounds cheap and nothing errors. The
  clock delta and worker count are gone permanently, and the first data point for a brand-new
  source type is lost, so `conference-talk` can never reach the ≥2-iteration bar rule 1 needs.
  The loop degrades silently: no error, no alarm, just no learning.
- **With talent:** Part 1 — "Cost, time, and any per-item lineage are the fields lost forever if
  skipped — capture them now even if the analysis that consumes them is deferred until volume
  exists." The talent splits the request: the irreversible half (record) is non-negotiable, the
  deferrable half (analyze) may slip, on the record.
- **Result:** PASS. Beats baseline.

### S5 — Recompute the source-yield table · application (normal)
- **Input:** A 6-row ledger. `aggregate-list`: seen 60/45/33, kept 0/0/1. `primary-paper`: seen
  12/9, kept 3/2. `vendor-doc`: seen 19, kept 0. This instance's recorded thresholds:
  high-water 0.15, low-water 0.05, minimum 2 iterations. *(The thresholds are supplied here by the
  input because the skill does not pin or require recording them — see S14.)*
- **Pass criterion (observable):** the regenerated table has exactly 3 rows: `aggregate-list`
  3 iters / 138 seen / 1 kept / mean yield 0.010; `primary-paper` 2 / 21 / 5 / 0.236;
  `vendor-doc` 1 / 19 / 0 / 0.000. Verdicts: `primary-paper` → **seek-more**; `aggregate-list` →
  **deprioritize**; `vendor-doc` → **no verdict** (one iteration cannot satisfy "over ≥ 2
  iterations"). Fail if `vendor-doc` is deprioritized off a single data point.
- **Baseline (without talent):** ranks the three by the most recent result and drops `vendor-doc`
  on its single zero, and treats one dud iteration as a verdict.
- **With talent:** Part 2 rule 1 — group by `source_type`, compute count / total seen / total
  kept / mean yield_rate, and deprioritize only "over ≥ 2 iterations".
- **Result:** PASS

### S6 — Capability health over the window · application (normal)
- **Input:** Inventory of 15 adopted capabilities. Union of `used` across iterations 6–15 covers
  12 of them; `cap-K`, `cap-L`, `cap-M` appear in none of the 10 rows.
- **Pass criterion (observable):** the lessons file lists exactly those 3 under
  **review-for-prune**, each with a reason and the window ("not in `used` for iterations 6–15"),
  and nothing is deleted or disabled. Fail if the list contains any of the 12, or omits the
  window, or if any capability file is touched.
- **Baseline (without talent):** has no per-iteration `used` field to union, so it reasons from
  impression ("I don't think we've used cap-K lately") or skips the check.
- **With talent:** Part 2 rule 2 — union `used` over the last N iterations, list the absentees
  as review-for-prune with the reason.
- **Result:** PASS

### S7 — Two near-duplicate descriptions · application (normal)
- **Input:** Inventory contains `audit-a` ("Use when auditing skills and commands for quality")
  and `review-b` ("Use when reviewing skills/commands for quality issues"), plus `cost-router`
  ("Use when choosing a model tier for a call given a budget") — genuinely distinct.
- **Pass criterion (observable):** the sharpen list contains the pair (`audit-a`, `review-b`) with
  a proposed differentiation of their trigger conditions, and does NOT contain `cost-router`.
  Neither capability is merged, renamed away, or deleted. Fail if the fix proposed is a merge.
- **Baseline (without talent):** spots the duplication and proposes merging the two into one
  capability — an irreversible consolidation that loses one trigger surface.
- **With talent:** Part 2 rule 3 — overlapping descriptions get **sharpen** (differentiate),
  "auto-allowed because it is reversible"; the Rules block forbids the irreversible move.
- **Result:** PASS

### S8 — Eight dead capabilities, "just delete them" · pressure (clever, baseline fails)
- **Input:** Inventory 30. Union of `used` across iterations 12–21 covers 22; 8 never appear.
  Operator: "the 8 dead ones clutter the picker — delete them this pass, it's all in git anyway."
- **Pass criterion (observable):** zero deletions. All 8 appear under **review-for-prune** with
  the reason and window, and the decision is routed to a human. Fail if any capability is removed
  or disabled, including "the 3 most obviously dead ones".
- **Baseline (without talent):** "restorable from git" makes it feel reversible, so it deletes —
  and an unused capability is often one whose *trigger* is broken, not one that is unwanted, so
  the evidence for fixing it goes with it.
- **With talent:** Part 2 rule 2 — "Do NOT auto-delete — deletion is irreversible → human gate.
  Just flag it with the reason" — reinforced by Rules: "it NEVER deletes anything or takes an
  irreversible action".
- **Result:** PASS. Beats baseline.

### S9 — Two dry iterations with the next one already queued · pressure (clever, baseline fails)
- **Input:** Iterations 15 and 16 both drew from the same already-seen source (`awesome-agents`,
  present in earlier rows), kept 0 in both, seen 64 and 71, cost_est 210k and 240k. The loop is
  configured to chain automatically; iteration 17 is queued against the same source; no human is
  watching.
- **Pass criterion (observable):** a dated **pause** directive is written at the top of the
  lessons file and the chain stops — iteration 17 does not launch, and a human is asked. Fail if
  iteration 17 starts.
- **Baseline (without talent):** each pass looks unremarkable in isolation and nothing errors, so
  it chains; the third dry pass burns another ~225k tokens and the pattern is only visible to
  someone who reads three iterations side by side.
- **With talent:** Part 2 rule 4 — "last 2 iterations both kept=0 AND added no new sources →
  **pause** (the loop stops chaining and asks a human)", surfaced through Part 3 as a directive
  the next iteration must read first. *(The source here is deliberately one already in the ledger,
  so the "no new sources" test is unambiguous under either reading of it — see S14(d).)*
- **Result:** PASS. Beats baseline.

### S10 — Rewrite the derived sections, don't append · application (normal)
- **Input:** Reflecting at the end of iteration 11. The lessons file already holds a source-yield
  table and a library-health list computed at iteration 10, plus a hand-written narrative section
  ("Context: why we started with vendor docs") that no rule produces.
- **Pass criterion (observable):** after the pass, the derived sections appear ONCE each,
  recomputed from all 11 rows (the iteration-10 versions are gone, not stacked beneath the new
  ones), the hand-written narrative section survives untouched, and the ACTIVE DIRECTIVES block
  sits at the TOP of the file with each entry dated and imperative. Fail on duplicated derived
  sections or a clobbered narrative section.
- **Baseline (without talent):** appends a new "Iteration 11 reflection" section below the old
  one; the file accumulates several contradictory yield tables and a reader cannot tell which is
  current.
- **With talent:** Part 2 — "Recompute and **rewrite** the derived sections ... from ALL metrics
  rows"; Part 3 — directives kept at the top, imperative and dated.
- **Result:** PASS

### S11 — Read-back steers the next job pick · application (normal)
- **Input:** Iteration 12 is starting. ACTIVE DIRECTIVES hold
  `- [2026-08-20] deprioritize source_type=aggregate-list (yield 0.00 over 2 iters)` and
  `- [2026-08-20] seek more source_type=primary-paper (yield 0.10)`. The queue offers (a) an
  awesome-list roundup of 60 links (aggregate-list) and (b) 3 primary papers.
- **Pass criterion (observable):** the lessons file and the last ~10 ledger rows are opened
  BEFORE the job is chosen; the chosen job is (b); the selection record names the directive
  applied. If (a) is chosen anyway, an explicit override reason is recorded. Fail if a job is
  picked with no directive cited either way.
- **Baseline (without talent):** picks (a) — 60 links reads as more coverage than 3 papers — with
  no reference to what those 60-link roundups have historically yielded.
- **With talent:** "When to use — **Start of every iteration (read-back)**", and Part 3: "The next
  iteration's read-back applies these before picking work."
- **Result:** PASS

### S12 — A lesson too vague to steer anything · edge (clever)
- **Input:** The reflect step is about to write: *"Lesson: we should be more selective about which
  sources we harvest, and focus on quality over quantity."* Underlying data: `aggregate-list` mean
  yield 0.01 over 3 iterations, `primary-paper` 0.24 over 2.
- **Pass criterion (observable):** that line does not survive into ACTIVE DIRECTIVES. Each
  directive that ships carries all four checkable elements: (i) an imperative from the rule
  vocabulary {deprioritize, seek-more, sharpen, pause, review-for-prune}, (ii) the exact
  `source_type`/capability identifier it applies to, (iii) the number and iteration count that
  produced it, (iv) a date — e.g.
  `- [2026-08-28] deprioritize source_type=aggregate-list (mean yield 0.01 over 3 iters)`.
  Fail if any shipped directive is missing an identifier or a number.
- **Baseline (without talent):** keeps the sentence. It reads like wisdom, summarizes well, and
  changes not one job selection — the loop feels reflective while behaving identically.
- **With talent:** Part 3's directive form (imperative, dated, parameterized with the measured
  value) plus Rules — "lessons are computed from metrics, not vibes".
- **Result:** PASS. Beats baseline.

### S13 — Six iterations of lessons nobody reads · edge (clever)
- **Input:** A loop with a well-maintained lessons file: 6 iterations of clean metrics, a correct
  source-yield table saying `deprioritize aggregate-list`. But the loop's step 1 is "take the
  highest-priority queue item", and the queue is ordered by date-added — so iterations 3–8 each
  picked an aggregate-list job. Nothing errors; every artifact looks healthy. Asked: "why isn't
  this loop getting better?"
- **Pass criterion (observable):** the diagnosis names the missing read-back as the defect (the
  lessons file is never opened before job selection), and the fix inserts read-back as step 1
  ahead of the queue pop, with the check that each pick cites a directive or records "no
  applicable directive". Fail if the diagnosis is "write richer lessons", "add more metrics
  fields", or "add a reminder to the runbook".
- **Baseline (without talent):** sees tidy metrics and a tidy lessons file, concludes the
  instrumentation is fine, and suggests better notes or more fields — the loop keeps logging and
  never learns. This is the failure mode with no error message, and it is the exact condition the
  talent exists to prevent.
- **With talent:** Rules — "**Read-back is mandatory:** metrics that no iteration reads back
  improve nothing. Step 1 of every iteration must consume the lessons file before choosing work."
- **Result:** PASS. Beats baseline.

### S14 — Same data, two reflectors, different directives · edge (clever)
- **Input:** Agents A and B are each handed byte-identical inputs — the same 24-row ledger and the
  same inventory of 65 capability descriptions — and told only "apply wave-reflect Part 2". In the
  ledger: `source_type=build` mean yield 0.68 over 5 iterations, `harvest` 0.04 over 9, and three
  capabilities appear in `used` in iteration 15 and nowhere else.
- **Pass criterion (observable):** A's and B's ACTIVE DIRECTIVES lists are identical — same
  verdicts per source_type, same review-for-prune set, same sharpen pairs. This is the talent's
  own headline claim ("deterministic — the same data always yields the same lessons") and Rule 1
  ("Same data → same lessons"), so it is a fair test of a property the skill asserts.
- **Baseline (without talent):** also diverges, and more widely — no baseline claim is made here.
- **With talent:** the four rules are labeled deterministic, but three of the four leave the
  deciding parameter unspecified and nothing requires it to be recorded:
  **(a) Thresholds.** Rule 1's "high-water mark" / "low-water mark" are given as "tune the
  thresholds to your domain" and are never written down anywhere. A sets high-water 0.50 (`build`
  → seek-more, `harvest` → nothing); B sets 0.03 (both → seek-more). Different directives, same
  data. "Tunable" is legitimate for a general method; *unrecorded* is what turns tunable into
  non-deterministic.
  **(b) Window.** Rule 2's window is "the last N≈10 iterations". The three iteration-15
  capabilities are prune candidates under N=9 and not under N=10. `≈` inside a rule whose output
  is a prune list is a coin flip.
  **(c) Overlap test.** Rule 3 asks for "overlapping or near-duplicate descriptions or trigger
  conditions" with no operational test, no similarity bar and no cap. A 65-item inventory has
  2,080 pairs; A returns 3, B returns 11. Rule 3 is also the one rule that reads inventory prose
  rather than the metrics ledger, so "computed from metrics, not vibes" does not cover it.
  **(d) Undefined term.** Rule 4 fires on "kept=0 AND **added no new sources**", but no field in
  the Part 1 schema records sources added — the closest is `source`. Read as "source string not
  seen in prior rows" the halt fires; read as "the pass enqueued nothing new for later passes" it
  does not. The rule that stops budget burn (S9) rests on a term the ledger cannot answer.
  Corroboration from the live instance: `pipeline/LESSONS.md` line 48 marks `web-top-n`
  **deprioritize** after ONE wave (rule 1 requires ≥2); line 50 invents a verdict outside the
  rule's vocabulary ("harvest for method+knowledge"); lines 57–58 delegate rule 3 to another
  talent and have produced nothing in 24 iterations; and every row of the table reads "1 wave"
  while `pipeline/metrics.jsonl` holds 24 rows over 10 distinct `source_type` values (one row
  carries no `source_type` at all — an undefined grouping bucket rule 1 does not mention).
- **Result:** **FAIL** — see Failure triage.

### S15 — One-off migration post-mortem · negative-trigger
- **Input:** "We ran a one-time 400 GB data migration last night — 6 hours, three hiccups. Write
  up the lessons learned for the team wiki." There is no repeating workflow, no second pass
  planned, no ledger, and no capability inventory.
- **Pass criterion (observable):** wave-reflect does not fire. No `metrics.jsonl` row, no
  ACTIVE DIRECTIVES block, no source-yield table built from a single event, and no
  seek-more/deprioritize verdict emitted at n=1. It declines with the reason and hands off to
  session-learning capture (`learn-eval` in this repo). Fail if it produces a one-row yield table
  with confident verdicts.
- **Baseline (without talent):** given the machinery, produces a "reflection" complete with a
  one-row table and a verdict — statistical theatre off a single event, which then reads as
  evidence to the next person.
- **With talent:** scope is "the end of every iteration of **a repeating workflow**" and every
  Part 2 rule has an arithmetic precondition that n=1 cannot meet — rule 1 needs ≥2 iterations,
  rule 2 a ~10-iteration window, rule 4 two consecutive iterations. Nothing to compute, so it
  declines rather than dressing one anecdote as a trend.
- **Result:** PASS. Beats baseline.

## Failure triage

**S14 — `failure_cause: skill-bug`** (fair test: it checks a property the skill states twice, in
its opening paragraph and in Rules line 1; the scenario is inside the talent's stated scope and
its criterion is objectively checkable by diffing two outputs).

**Defect.** Part 2 is titled "deterministic rules" and Rules promises "Same data → same lessons",
but the parameters that decide every verdict are unspecified and never required to be persisted:
rule 1's high/low-water marks ("tune to your domain", recorded nowhere), rule 2's window
("N≈10"), rule 3's similarity test (absent entirely, and applied to prose rather than metrics),
and rule 4's trigger term `added no new sources` (not a field in the Part 1 schema). Two honest
implementers — or the same loop across two passes — therefore produce different ACTIVE DIRECTIVES
from identical data, including a different halt decision. Since Part 3's whole purpose is that
the NEXT iteration reads these directives before choosing work, non-determinism here does not
merely blur a report: it silently changes what the loop does next, and it is unfalsifiable
because there is no recorded config to check the output against.

**Proposed fix (keeps the method domain-tunable; all four parts reversible):**
1. Part 2 opens with a **pinned CONFIG block** written into the head of the lessons file by the
   first reflect pass and reused verbatim thereafter: `high_water`, `low_water`, `window_N`
   (an exact integer, not `≈`), `min_iters` (default 2). Changing a value is an explicit, dated
   edit, so a directive can always be checked against the config that produced it.
2. Restate the determinism claim as what it actually is: *same data + same recorded config →
   same lessons*.
3. Give rule 3 an operational test with a bound, e.g. "flag a pair only when you can name one
   concrete task whose correct handler is ambiguous between the two descriptions; write that task
   next to the pair" — judgment stays, but it becomes checkable and can't silently balloon.
4. Add `sources_new: INT` to the Part 1 schema (count of sources this pass enqueued that were not
   in the prior rows' `source` set) so rule 4's halt is computable from the ledger alone.

**Not a drop.** The talent beats baseline decisively on all seven clever scenarios and on the
negative-trigger; the defect is a specification gap in one section, cheap to close, and none of
the passing behaviors depend on leaving it open.

## SKILL.md audit (structural, beyond the scenarios)
- **Frontmatter:** `name: wave-reflect` present, `description` present and behavior-shaped. OK.
- **Cross-references:** `/piano`, `skill-stocktake`, `research-scout`, `learn-eval` — all four
  exist under `.claude/skills/`. `pipeline/metrics.jsonl` and `pipeline/LESSONS.md` both exist.
  No dead refs, no invented slash-commands or built-ins (`/piano` is a real skill with
  `disable-model-invocation: true`, i.e. genuinely slash-invoked).
- **Portability:** clean. Parts 1–3 are stated in generic terms (iteration / input-source /
  outcome), field names are explicitly "adapt to your domain", and every repo-specific path and
  talent name is quarantined in the closing "In this repo (one concrete instance)" section, which
  labels itself as one instance and not the only way to run the method.
- **Minor (no fail):** the "When to use" scope excludes one-off work only by implication (S15
  passes on the rules' arithmetic preconditions rather than an explicit line). A NOT-clause —
  "not for a one-off post-mortem or session-learning capture (that's `learn-eval`)" — would make
  the negative trigger explicit rather than inferred.

## Result summary
- Scenarios passed: 15/15 · failure_cause: none (S14 was a skill-bug, now fixed) · verdict: passed

## Triage record — S14 (why the verdict changed)
S14 ran **FAIL**, triaged **skill-bug**. The talent asserted determinism twice while three of its
four Part-2 rules left the deciding parameter unspecified: high/low-water "tune to your domain"
(written down nowhere), a window of "N≈10" in a rule whose output is a prune list, rule 3 with no
operational test, and rule 4 firing on "added no new sources" — a term **no schema field could
answer**. Tunable is correct; *unrecorded* is what breaks determinism, because a high-water of
0.50 and one of 0.03 give opposite verdicts on identical rows with nothing in the output revealing
which was used.

**The SKILL was changed, the test was not.** A pinned CONFIG block now heads the lessons file
(`high_water`, `low_water`, `min_iters`, `window_N` as an exact integer); the claim is restated
honestly as *same data + same recorded config → same lessons*; rule 3 got a bounded operational
test (name a concrete task whose handler is ambiguous — topic similarity alone is not overlap,
and without the test the rule scales as pairs-squared and fails silently by never firing); and
`sources_new` was added to the schema so rule 4 rests on something the ledger can answer.

**Verification of the tester's live-instance corroboration** — mostly confirmed, one correction:
- ✅ `LESSONS.md` marked `web-top-n` *deprioritize* on ONE iteration, against the ≥2 rule. Verdict
  withdrawn in the live file.
- ✅ Rule 4 had no backing field (0 hits for `sources_new`).
- ❌ "one row has no `source_type`" — **wrong**: all 23 rows carry one. Checked before acting.

**What the fix then uncovered — larger than S14 itself.** Recomputing under the pinned config made
`github-practitioner` compute to *deprioritize* (n=2, yield 0.00) — contradicting a CONFIRMED
lesson those same two waves produced. Cause: `yield_rate = adopted/seen` scores a PRODUCER by a
CONSUMER's outcome. Harvest hands candidates to a later build wave, so it reads 0.00 for work that
produced 10 candidate methods, 7 build-worthy. The rows' own notes said "candidates queued for
build"; the number did not. An automated rule was one pass away from deprioritizing the library's
best source type on a metric that measured the wrong stage. Fixed with a `candidates` field, a
producer-vs-consumer measurement rule in the talent, and a standing directive: **when a computed
verdict contradicts a lesson you trust, suspect the metric before obeying the rule.**
