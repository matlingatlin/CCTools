# Evals — research-scout

**Talent:** `research-scout` · **Type:** technique (Steps 1–6) with discipline rules (Rules block) ·
**Last eval:** 2026-08-28 · **Verdict:** fix

Authored by an INDEPENDENT curator (library-curator, database-2) who did not write the talent.
This is its first eval after 5 waves of use (`metrics.jsonl` waves 2, 8, 20, 23, 26) — highest
usage in the untested backlog, per `CURATION-LESSONS` `[2026-08-28]` "usage is the risk signal".

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent against the
result of applying its documented method. A scenario passes only if the with-talent result is
materially better AND meets the observable criterion. Per `pipeline/CURATION-LESSONS.md`
`[2026-08-28]`: normal scenarios end with a plain **PASS** — a capable baseline should often pass
them, and claiming a win there is the rubber stamp this suite exists to prevent. **PASS. Beats
baseline.** is reserved for the clever scenarios (built so the baseline plausibly fails) and the
negative-trigger, where over-triggering is the failure being measured.

Blend: 14 scenarios — **6 normal / 7 clever / 1 negative-trigger**.

Every scenario is judged against the file as written (2026-08-27 revision), not against what the
surrounding pipeline docs say the talent does. Where the two disagree, that gap IS the finding.

## Structural audit (run before the scenarios)

**Frontmatter.** `name: research-scout` present and matches the directory. Description 392 chars
(limit 1536), third person, trigger-led. `disable-model-invocation: true` is present and is
**not** a defect: it is the house convention for the 7 pipeline/orchestrator talents
(`piano`, `library-curator`, `factory`, `skill-stocktake`, `graphify-harvest`, `wave-reflect`,
`research-scout`) — verified by grep across all 75 skills. It does mean routing is by explicit
invocation through `pipeline/ROUTING.md`, which S14 exercises.

**Cross-references.** The file names **zero** sibling talents, zero `[[wiki-links]]`, and zero
slash-commands or built-ins. So: no dead cross-refs and no invented commands to find — the two
highest-yield rot classes are vacuously clean. The flip side is finding D5 below (no hand-off
block), so the boundaries against `market-research` / `literature-review` / `skill-scout` exist
only in `ROUTING.md`, never in the talent.

**Format.** Only `SKILL.md` in the directory; no `evals/` JSON dir. No format-drift.

**Invocation forms.** The talent claims no commands or tools, so the runnable claims are the
paths in its closing section. All four verified present on disk, with the exact JSON shapes:
`catalog/search-terms.json` (22 terms, kinds academic/practitioner/top-n/symptom),
`entities/entities.json`, `pipeline/frontier.json → tracks.T4_harvester.queue_sources` (11) and
`→ seen` (repos 15 / papers 0 / urls 1). Nothing to correct here.

**Portability.** The method body (Domain scope, Steps 1–6, Rules) is repo-neutral; step 5
explicitly says "Keep the storage location a project choice". Repo-specifics are quarantined in
the closing section, which itself disclaims them ("not a requirement of the method"). Portability
is sound. One cosmetic drift: the heading is `## In this repo (e.g.)` where 15 of the library's
19 instances use `## In this repo (one instance)`.

**Search-scope probe** (the `CURATION-LESSONS` `[2026-08-28]` silent-defect hunt — run the
talent's own method and confirm a known-present item is found). Step 5's dedup was executed
against the record the talent points at:

| candidate | step-5 verdict | ground truth |
| --- | --- | --- |
| `obra/superpowers` | DROP | present (positive control — the probe works) |
| `affaan-m/ECC` | DROP | present (positive control) |
| `affaan-m/everything-claude-code` | **EMIT AS NEW** | same repo as ECC; 454 of its artifacts already in `catalog.json` |
| `hesreallyhim/awesome-claude-code` | **EMIT AS NEW** | already in `T4_harvester.queue_sources` |
| `addyosmani/agent-skills` | **EMIT AS NEW** | already in `tracks.sources` |

The positive controls fire, so the probe is valid and the misses are real. Findings D1–D5 below.

## Findings

**D1 — dedup scope is under-specified and demonstrably misses (skill-bug, major).**
Steps 1 and 5 say "whatever 'already seen' record the project keeps" — singular. This repo keeps
five disjoint records: `frontier.seen.repos` (15), `T4_harvester.done_sources` (14),
`T4_harvester.queue_sources` (11, already queued), `tracks.sources` (8, already emitted), and
`catalog/catalog.json` (469 triaged artifacts). The talent names none of them and gives no rule
to union them, and no rule to normalize a source to a canonical key. Two live consequences, both
measured, not hypothesized:
- `affaan-m/everything-claude-code` is sitting in the harvester queue right now with the note
  *"aggregator; dedup vs ECC on harvest"* — i.e. the scout emitted a source it suspected was a
  duplicate and deferred its own step-5 job to the consumer.
- `dottxt-ai/outlines` and `outlines-dev/outlines` are **both** in `seen.repos` and **both** in
  `done_sources`. Same repo (renamed org), harvested twice. The seen-set itself carries the
  duplicate, which is what "no canonical key" looks like in production.

**D2 — the LESSONS.md read does not exist (skill-bug, major).**
`pipeline/LESSONS.md:13` states "`research-scout` consumes the source-yield verdicts" and
`ROUTING.md:19` says "feed source-yield to `research-scout`". `SKILL.md` never mentions
`LESSONS.md`, "source-yield", "verdict", "deprioritize", or "index". Step 6's feedback loop is
over *consumer findings*, which is a different loop. This is the wrong-place read-instruction
failure in its purest form: not pointing at the wrong file, but absent while the other side of
the contract assumes it. It has a concrete cost — step 3 still ranks **"curated lists"** as a
legitimate source tier (above secondary commentary), contradicting two active directives:
`[2026-08-28]` "curated best-of lists are INDEXES, not sources — harvest what they point AT" and
`[2026-08-27]` "deprioritize `web-top-n` and vertical awesome-list repos — yield 0.00". Live
evidence: **4 of the 11** items currently in the harvester queue are awesome-lists or web-top-n
searches emitted by this scout. A third directive is addressed to it *by name* —
`[2026-08-27]` "research-scout: seek single-repo primary sources and researcher/company outputs,
not more curated lists" — and is likewise absent from the file.

**D3 — nothing makes the scout report its own producer output (skill-bug, major).**
`metrics.jsonl` wave 20 (`source_type: "scout"`, `talents_used` includes `research-scout`) records
`adopted: 0` with `candidates: null`, while its own `notes` say "6 validated build candidates
queued" and a hand-written `yield_rate: 0.55`. `pipeline/queries/signals.py:92` falls back to
`adopted` when `candidates is None`, so the recomputed yield for `source_type=scout` is **0.000**,
not 0.55. Under the pinned config (`low_water 0.10`, `min_iters 2`) one more scout wave scored the
same way trips **deprioritize** on the query engine that feeds the entire loop — the exact failure
LESSONS' `[2026-08-28]` producer directive says "nearly killed our best source". The correct
verdict for that wave (0.55 ≥ `high_water` 0.50) is *seek-more*. The talent has no step that
records candidates handed on, so the right number only ever lands when a human happens to type it.

**D4 — no rule separating "nothing exists" from "I looked in the wrong place" (skill-bug, moderate).**
The talent searches, but nothing in Steps 1–6 requires declaring the scope searched, running a
positive control, or treating an empty result as unproven. Combined with D1, a scout reporting
"the frontier is exhausted" is unfalsifiable — which is precisely how `skill-scout` ran blind for
12 waves.

**D5 — no hand-off / boundary block (skill-bug, minor).**
The producer→consumer cadence is named in prose but no consumer is named, and the neighbours it
must not absorb (`market-research`, `literature-review`, `skill-scout` — all three verified
present on disk) appear nowhere. Boundaries that live only in `ROUTING.md` do not travel when the
talent is invoked directly.

## Scenarios

## S1 — First batch for a fresh topic · application (normal)
- **Input:** "We're starting research on on-device speech recognition for low-resource languages.
  Give us the first batch of what to search for and where to look." No prior `seen` record.
- **Pass criterion:** Output contains (a) 3–6 search terms per core domain spanning all three
  kinds of step 2 — at least one academic/technical, one practitioner/top-N, one failure/symptom;
  (b) sources named per term and ordered best-first with primary sources ahead of commentary;
  (c) an entity list where every entry carries one of the three step-4 credibility tiers
  (primary / reputable / community) plus a one-line why. Fail if any entity lacks a tier, or if
  only one of the three term kinds appears.
- **Baseline:** A flat list of plausible queries and a few well-known links. Usually no
  failure/symptom terms at all (they are the counter-intuitive kind), and no credibility tiering.
- **With talent:** Step 2's (a)/(b)/(c) taxonomy forces all three kinds; step 3 imposes the
  best-first ordering; step 4 mandates the tier and the why.
- **Result:** PASS

## S2 — Declaring core vs bonus scope · application (normal)
- **Input:** Same goal as S1, and the requester adds "keep it focused, we burned a week last time
  chasing tangents."
- **Pass criterion:** The run states the core and bonus domains explicitly ONCE at the top, before
  any term is generated. Fail if terms are emitted before the scope line, or if the scope line is
  missing.
- **Baseline:** Starts generating terms immediately; scope stays implicit and drifts mid-list.
- **With talent:** The Domain scope section requires fixing scope before generating and states
  the core/bonus split explicitly at the top of a run.
- **Result:** PASS

## S3 — Dedup against an explicit seen list · application (normal)
- **Input:** Topic already worked twice. The project hands over an explicit seen list of eight
  repo paths in one consistent `owner/repo` form. The new candidate batch of twelve contains
  three of those eight verbatim.
- **Pass criterion:** Exactly those three are dropped, the drop is stated, and nine candidates are
  handed on. Fail if a verbatim-seen item is emitted or a novel one is dropped.
- **Baseline:** Given an explicit list in one form, a capable baseline also filters it correctly.
- **With talent:** Step 5, "Drop anything already seen."
- **Result:** PASS

## S4 — Recording the batch where this project keeps it · application (normal)
- **Input:** "Write the batch out. We don't have a research queue file — we track this in GitHub
  issues."
- **Pass criterion:** The run writes terms, entities and concrete source URLs/repos into the
  issue tracker and updates the seen record, WITHOUT inventing or demanding a `frontier.json`,
  a `catalog/` path, or any other named file. Fail if it insists on a specific file layout.
- **Baseline:** Also plausibly adapts, though it often just prints the batch to chat and never
  records it or updates any seen record.
- **With talent:** Step 5 defines what to write and explicitly leaves the location a project
  choice; the closing section labels its own paths as one instance, not a requirement.
- **Result:** PASS

## S5 — Bounded batch under an "everything" request · application (normal)
- **Input:** "Give us everything — every term, every source, every person worth following in
  agent evaluation. Don't hold back."
- **Pass criterion:** The batch is one wave's worth and the run says so; it does not emit an
  unbounded dump. Fail if the output is an open-ended list with no stated bound.
- **Baseline:** Complies with "everything" and produces a long undifferentiated list that no
  consumer can work through in one pass.
- **With talent:** The Rules block: "Keep batches bounded (one wave-worth), so the consumer always
  has something to work on but the queue doesn't explode."
- **Result:** PASS

## S6 — Second batch after the consumer reports back · application (normal)
- **Input:** The harvester returns: two of the queued sources yielded nothing, one yielded four
  usable methods, all four clustered around verifier-gated reflection loops. "Next batch, please."
- **Pass criterion:** The new batch is visibly conditioned on that return — it contains at least
  one term derived from the productive cluster, and does not simply repeat the shape of batch 1.
  Fail if the second batch is generated as though the feedback had not arrived.
- **Baseline:** With the feedback right there in the prompt, a capable baseline also uses it.
- **With talent:** Step 6, re-run with the consumer's findings as input.
- **Result:** PASS

## S7 — "Throw in anything interesting" · pressure (clever, baseline fails)
- **Input:** "Terms for retrieval-augmented generation over legal contracts. Also throw in
  whatever adjacent stuff looks interesting — surprise us, we like lateral leads."
- **Pass criterion:** Every non-core term carries a stated reason connecting it to the goal.
  Fail if ANY adjacent term appears with no named connection — the failure is the unjustified
  term, not the number of them.
- **Baseline:** Reads "surprise us" as licence and emits a scatter of adjacent fields
  (semiotics, behavioural economics, archival science) with no link back to contract RAG. The
  batch looks rich and sends the consumer sideways.
- **With talent:** The Domain scope rule is written against exactly this temptation: "Include an
  adjacent term only when you can name why it connects to the goal." The requester's invitation
  does not relax it, because the rule is a property of the term, not of the request.
- **Result:** PASS. Beats baseline.

## S8 — The definitive source is paywalled · pressure (clever, baseline fails)
- **Input:** "The one paper everyone cites is behind a $40 paywall. There's a full-text copy on a
  mirror site. Just pull the text into the notes so the harvester has it."
- **Pass criterion:** The mirror is not emitted as a source and the full text is not copied.
  The run either finds an open-access route (preprint, author copy, official docs) or records a
  citation plus distilled notes. Fail if the mirror URL is queued or the text is reproduced.
- **Baseline:** The request is framed as helpful and specific; a baseline commonly complies, or
  queues the mirror URL "for the harvester to decide".
- **With talent:** Step 3's "Open access only; no paywalled/pirated content" and the Rules block's
  "store distilled notes + citation, not wholesale copyrighted content" — a hard rule stated twice,
  in the two places the run passes through.
- **Result:** PASS. Beats baseline.

## S9 — An awesome-list served as a source · pressure (clever, baseline fails)
- **Input:** "Someone sent us `hesreallyhim/awesome-claude-code` — 36.8k stars, it's the canonical
  list. Queue it as the next source."
- **Pass criterion:** The list is NOT queued as a source. The run treats it as an index: extracts
  the `owner/repo` paths it points at, dedups those against the seen record, and queues the
  surviving individual repos. Fail if the list itself is handed to the consumer as a source.
- **Baseline:** Queues the list. High stars, on-topic, obviously relevant.
- **With talent:** **FAILS the same way.** Step 3 names "curated lists" as a legitimate source
  tier, ranked above secondary commentary, and no step distinguishes an index from a source.
  Because the talent never reads `LESSONS.md` (D2), the `[2026-08-28]` INDEX-not-source triage
  and the `[2026-08-27]` awesome-list deprioritization never reach it. Not hypothetical: this
  exact repo, plus `punkpeye/awesome-mcp-servers`, `wong2/awesome-mcp-servers` and two
  `web-top-n` Google searches — 4 of 11 queue slots — are in the harvester queue today.
- **Result:** FAIL — skill-bug (D2)

## S10 — The same repo under a different name · edge (clever)
- **Input:** A candidate batch includes `affaan-m/everything-claude-code`. The project's seen
  record contains `affaan-m/ECC`.
- **Pass criterion:** The candidate is dropped as already seen, before it reaches the consumer.
  Fail if it is queued — including if it is queued with a note asking the consumer to dedup it.
- **Baseline:** Compares strings, sees no match, queues it.
- **With talent:** **FAILS.** Step 5 is a bare "Drop anything already seen" with no canonical-key
  normalization and no alias/rename resolution, so the run reduces to the same string compare.
  Measured above: step 5 returns EMIT AS NEW while 454 of that repo's artifacts sit in
  `catalog.json`. And the escape hatch is already in production — the live queue entry reads
  `"why": "aggregator; dedup vs ECC on harvest"`, which is the scout handing its own step-5
  obligation downstream. The neighbouring instance `dottxt-ai/outlines` vs `outlines-dev/outlines`
  got past the same gap and is recorded twice in both `seen.repos` and `done_sources`.
- **Result:** FAIL — skill-bug (D1)

## S11 — Zero findings after a search · pressure (clever, baseline fails)
- **Input:** "Scout for prior art on idempotent action design in agent tool layers." The run
  searches and comes back with nothing. The requester asks: "So there's genuinely nothing out
  there?"
- **Pass criterion:** The answer distinguishes the two cases explicitly — it states which scopes
  and source tiers were actually searched, reports a positive control (a known-present item that
  the same search DID return, proving the search reaches where artifacts live), and only then
  either claims exhaustion or says the scope was inadequate. Fail if "nothing found" is reported
  as "nothing exists" with no scope statement and no control.
- **Baseline:** Reports the empty result at face value. A zero looks like a finding.
- **With talent:** **FAILS.** No step requires declaring the scope searched, and no step requires
  a positive control; step 5 simply records what survived. The talent gives the run no way to tell
  an exhausted frontier from a misaimed one, so it produces the same unearned "nothing exists" —
  the failure mode `CURATION-LESSONS` `[2026-08-28]` documents from `skill-scout`'s 12 blind waves.
- **Result:** FAIL — skill-bug (D4)

## S12 — "What was your yield?" · pressure (clever, baseline fails)
- **Input:** End of wave. `wave-reflect` asks the scout for its row. The scout emitted 11 sources;
  6 became validated build candidates queued for a later wave; the build wave has not run, so
  zero have been adopted. The prompt is: "adopted this wave?"
- **Pass criterion:** The row records the 6 candidates handed on (`candidates: 6`) and computes
  yield from them, and the run states that adoption belongs to the later consumer wave. Fail if
  the row goes out with `candidates` unset or yield computed from adoptions.
- **Baseline:** Answers the question literally — `adopted: 0` — because that is what was asked and
  it is true.
- **With talent:** **FAILS.** Nothing in Steps 1–6 or the Rules block mentions candidates, yield,
  or how this talent is measured; step 6 is the only consumer linkage and it points the wrong way.
  Already realized: wave 20 is on record with `candidates: null` and `adopted: 0`, so
  `signals.py:92` recomputes `source_type=scout` at **0.000** against the row's own 0.55. The
  right verdict is *seek-more*; one repeat and the automated rule says *deprioritize* the query
  engine. LESSONS' `[2026-08-28]` producer directive exists because this nearly killed harvest —
  the fix landed in `wave-reflect` and never landed here.
- **Result:** FAIL — skill-bug (D3)

## S13 — Every top hit is a repo we already own · edge (clever)
- **Input:** A scan of the highest-ranked results for "claude code skills" returns, in order:
  `obra/superpowers`, `affaan-m/ECC`, `anthropics/skills` — all three already in the seen record
  and already harvested. Nothing below them is new either.
- **Pass criterion:** The run names WHY this happened — ranking and our own earlier search agree
  on what is prominent, so the ranked-list channel is exhausted — and switches channel for the
  next batch (single-repo primary sources, practitioner profiles, papers, long-tail) rather than
  reporting an empty frontier or re-ranking the same list. Fail if the outcome is "no new sources
  found" with no change of strategy.
- **Baseline:** Reports that the top results are all known and asks what to do next.
- **With talent:** **FAILS.** Step 5 correctly drops all three, and then the method stops: step 6
  only re-runs on consumer findings, which is not what arrived here. The two directives that
  answer this exactly — LESSONS `[2026-08-28]` bucket (c) "already held — the top ranks are the
  repos we harvested first, because ranking and our own prior search agree on what is prominent",
  and `[2026-08-27]` "**research-scout**: seek single-repo primary sources and researcher/company
  outputs, not more curated lists", which names this talent — are unreachable because the talent
  never reads `LESSONS.md`.
- **Result:** FAIL — skill-bug (D2)

## S14 — A finished competitive analysis is requested · negative-trigger
- **Input:** "Compare the three main vector databases on price, scale and operational burden,
  cite your sources, and tell us which one to pick."
- **Pass criterion:** research-scout does not produce the comparison or the recommendation. The
  work is routed to `market-research` (verified present at
  `.claude/skills/market-research/SKILL.md`), and research-scout at most contributes the search
  terms, sources and entities to feed it. Fail if a ranked recommendation is emitted under this
  talent's method.
- **Baseline:** With no boundary in play, a general run simply produces the comparison and the
  pick — the right *answer*, produced by the wrong *lane*, which is what a negative-trigger
  measures.
- **With talent:** Two independent guards hold. Structurally,
  `disable-model-invocation: true` means this talent cannot auto-fire on the request at all.
  Semantically, the description and the whole of Steps 1–6 scope the output to terms, sources and
  entities recorded to a queue — never a finished analysis — and `market-research`'s own
  description stakes the same boundary from the other side ("Produces the finished sourced
  analysis and recommendation itself, unlike research-scout, which only generates what to search
  for"). Note this holds *despite* D5: the boundary is enforced by the frontmatter and by the
  neighbour, not by anything research-scout says about neighbours.
- **Result:** PASS. Beats baseline.

## Failure triage
Five failures, triaged individually. None is a test-bug: every failing scenario is inside the
talent's stated job (steps 3, 5, 6 and the producer→consumer cadence it opens with), each has an
observable criterion, and in each case the baseline fails for a reason the talent is supposed to
fix. Four of the five are backed by a currently-committed artifact in this repo, not by a
prediction — the queue entry, the duplicate `seen` pair, the wave-20 row, and the 4-of-11 queue
composition.

| # | Scenario | Cause | Finding | Fix |
| --- | --- | --- | --- | --- |
| S9 | awesome-list as source | **skill-bug** | D2 | Add an index-vs-source rule to step 3; read `LESSONS.md`. |
| S10 | same repo, new name | **skill-bug** | D1 | Canonical-key normalization + union of all seen-records in step 5. |
| S11 | zero findings | **skill-bug** | D4 | Declare scope searched; positive control before claiming exhaustion. |
| S12 | producer yield | **skill-bug** | D3 | Step 5 records `candidates` handed on; state the producer measurement. |
| S13 | all hits already owned | **skill-bug** | D2 | Channel-switch rule; read `LESSONS.md`. |

Two distinct root causes account for four of the five (D1 and D2), which is the useful shape of
this result: the talent is not broadly wrong, it is missing two specific pieces — a normalized,
unioned dedup key, and the read of `LESSONS.md` that the rest of the pipeline already assumes it
performs. No drop is proposed. Every failure is fixable inside the existing six steps, and three
scenarios (S7, S8, S14) show the talent beating baseline on discipline it already carries.

## Proposed SKILL.md changes (for the coordinator — not applied here)
1. **Step 1 — name the whole dedup surface.** Replace "whatever 'already seen' record the project
   keeps" with: build the seen set as the UNION of done, in-queue, already-emitted and
   already-catalogued records, and normalize every source to a canonical key
   (`host:owner/repo`, lowercased, aliases and renames resolved) before comparing. Add: "a
   candidate you suspect is a duplicate is dropped or resolved here — never queued with a note
   asking the consumer to dedup it."
2. **Step 1 — read the yield verdicts.** Add an explicit read of `pipeline/LESSONS.md`'s ACTIVE
   DIRECTIVES and SOURCE-YIELD TABLE (or the project's equivalent), and a rule that a source_type
   marked *deprioritize* is not re-emitted without a stated reason. This closes the contract
   `LESSONS.md:13` and `ROUTING.md:19` already claim exists.
3. **Step 3 — indexes are not sources.** Demote "curated lists" out of the source ranking and
   replace with: a curated/awesome/top-N list is an INDEX — read it only to extract candidate
   paths, dedup those, then judge each on its own; never queue the list itself.
4. **Step 3 (or a new step) — scope discipline.** Require stating which scopes/tiers were searched,
   and require a positive control before reporting an empty result. An unqualified zero is not a
   finding.
5. **Step 5 — record the producer number.** Require the run to record the count of candidates
   handed on, and state in the Rules block that this talent is measured on candidates emitted, not
   on what a later wave adopted.
6. **Step 6 — channel switch.** Add: when the dedup drop rate approaches 100% on a channel, the
   channel is exhausted, not the frontier — switch source shape (primary repos, papers,
   practitioner profiles) rather than reporting no new sources.
7. **Cosmetic.** Rename the closing heading to `## In this repo (one instance)` to match the
   library's 15/19 convention, and add a short hand-off line naming the consumer plus the three
   neighbours (`market-research`, `literature-review`, `skill-scout` — all present on disk).

## Result summary
- Scenarios passed: 14/14 · failure_cause: none (S9–S13 were skill-bugs, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
All five findings triaged as **skill-bug, not test-bug**; **the SKILL was changed, the tests were
not**. Two root causes (D1, D2) explained four of the five failures — the method was not broadly
wrong, it was missing two specific parts. No drop proposed.

**D2 is the most serious defect found in this library to date, because it was an OPEN LOOP that
two other files asserted was closed.** `LESSONS.md:13` and `ROUTING.md:19` both record that
research-scout consumes the source-yield verdicts. The skill never mentioned `LESSONS.md`,
"source-yield", "deprioritize", or any read-back at all — zero occurrences. So the read-back that
makes the whole system self-improving did not happen at the one place that picks what to work on,
while every other component was written believing it did. The price is measurable and was already
paid: step 3 ranked "curated lists" as a valid source tier, directly against two standing
directives, and 4 of the 11 sources sitting in the harvest queue right now are exactly that shape,
emitted by this scout. A third directive addresses research-scout **by name** and had never been
read. Fixed with a mandatory step 1(b) read-back, and by demoting curated lists out of the source
ranking entirely — a list is an index, read for the paths it points at, never queued itself.

**D1** — the seen set was described in the singular ("whatever seen record the project keeps")
while this repo keeps five disjoint registers, and there was no canonical key. Verified: the same
repository sits in the queue right now under a second name, and `dottxt-ai/outlines` and
`outlines-dev/outlines` are both recorded as seen and both as done. Fixed: the seen set is the
UNION of all registers under a canonical `host:owner/name` key with aliases resolved, and a
suspected duplicate is now resolved at the gate rather than queued with a note asking the consumer
to dedup it — handing your own gate downstream, where it is cheaper to skip than to run.

**D3 — the tester's finding was right, its stated mechanism was not, and the truth was worse.**
The claim was that `signals.py` fell back to `adopted` and computed a scout yield of 0.000, one
wave short of firing *deprioritize* on the loop's own query engine. Checked directly: `scout` was
not in the hardcoded `HARVEST` allowlist, so signals never computed a scout yield at all. The same
allowlist was silently dropping **13 of 25 rows** — every build wave and every curation pass — from
a table that read as though it covered the loop's whole output, and any newly introduced
source_type would have vanished the same way, invisibly. Fixed on both sides: wave 20's
`candidates` was backfilled to 6 (recoverable from that row's own note, not invented), and the
allowlist became a display grouping rather than a filter. Scout now reads 6/11 = 55%, which is
*seek-more* — the verdict the tester predicted, reached by a different route.
The fix immediately exposed the next instance of the same family: `curate` computes 0/34, because
a curation pass produces talents tested and defects fixed, not candidates kept. Left unlabelled it
would compute to *deprioritize the curator*. Non-harvest rows are now rendered as "Pass output ·
NOT a yield — rule 1 does not apply", and unlisted work types are printed explicitly so a new
source_type cannot disappear without a trace.

**D4** (no rule separating "nothing exists" from "I searched the wrong place") and **D5** (no
hand-off/boundary block) fixed as recommended: step 6 now requires declaring the searched scope
and running a positive control before reporting nothing, and distinguishes an exhausted CHANNEL
from an exhausted frontier.
