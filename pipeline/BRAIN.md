# BRAIN — the living control tower for both loops (read at start, update at end)

The single shared brain BOTH agents feed and follow: `/piano` (the build/harvest loop) and
`library-curator` (the db2 maintenance loop). Each **reads this at the start of a run** and
**updates it at the end**. It does four jobs: **connect** their learnings, **sync** their work,
**plan** what each does next, and **optimize** the whole. The detailed stores stay where they
are; this is the coherent top layer over them.

Stores this brain sits over: `LESSONS.md` (harvest source-yield) · `TEST-AUTHORING-LESSONS.md`
(the directives both loops apply before writing tests) · `CURATION-LESSONS.md`
(shared test-authoring brain) · `metrics.jsonl` (raw per-wave data) · `ledgers/*.jsonl`
(talents lineage · per-scenario evals · categorized rejections · human-gate proposals) ·
`frontier.json` (queues + schedules + seen) · `catalog.json` (469 labelled components) ·
`STATUS.md` (log). **What each store holds, who writes it, when: `DATA.md` (the contract).**

## 0. LEARN & IMPROVE — the #1 job (everything else serves this)
The brain's primary purpose is that **each cycle makes the next one better.** Connect / sync /
plan / optimize below are only the machinery for it. Non-negotiable, every run, both loops:
- **Apply prior lessons FIRST.** Before doing work, read the relevant lessons (LESSONS /
  TEST-AUTHORING-LESSONS / CURATION-LESSONS / the LINKS here) and act on them. A lesson nobody reads back improves nothing.
- **Record at least one lesson.** Every run must leave a concrete learning — a new directive, a
  sharpened rule, a link, or "confirmed X still holds." No run ends without feeding the brain.
- **Prove improvement, don't assume it.** Learning is real only if outcomes trend better. Track
  the **improvement signals** below each cycle; if a signal is flat or worse, that itself is the
  next thing to fix (the meta-lesson: our learning on that axis isn't working).

### The objective (what "optimize" means here — ranked)
The loop optimizes this small, ranked target set — not a vague "get better":
1. **Test quality** — coverage → 100% AND blend ~50:50 normal:clever (a suite that's all traps
   misses the everyday job; all happy-path misses where it breaks). The #1 target: a library
   we can trust only if its tests discriminate.
2. **Library health** — rot/dead-refs found per curation pass trending **down** (once the
   backlog is cleared); 0 test-failed-unfixable drops (fix, don't drop).
3. **Harvest efficiency** — yield (kept/seen) per source_type up; bias to the shapes that pay.
4. **Cost/time** — measured `wall_clock_s` per wave down for equal output (needs the metric
   live, cost still estimated until a metered path).
A signal flat or worse IS the next thing to fix — that axis's learning isn't working.

### Improvement signals — AUTO-COMPUTED from the ledgers (do not hand-edit)
Run `python3 pipeline/queries/signals.py --write` at every reflect/record step; it reads
`metrics.jsonl` + `ledgers/*.jsonl` and rewrites the block below. This is what CLOSES the
optimization loop — read-back is data-driven, not from memory. (Manual edits are overwritten.)
<!-- SIGNALS:auto (computed by pipeline/queries/signals.py --write) -->
| Signal | Direction wanted | Reading (from ledgers) |
| --- | --- | --- |
| Test coverage (tested / total) | **up → 100%** | 85/85 = 100% |
| Test verdict pass-rate | **stay high** | 85 passed · 0 failed of 85 |
| Test blend · LIVE (scenarios written since instrumentation) | **~50 : 50** | normal 44% · clever 35% · neg 9% of 241 — BALANCED |
| Test blend · backfilled history (context only, cannot be changed) | n/a | normal 28% · clever 55% of 341 — the aggregate's skew lives here |
| Talents dropped (test-failed, unfixable) | **~0 (fix, don't drop)** | 0 |
| Gate rejections by reason · LIVE (per-candidate) | learn the waste shapes | tool-not-method=9; already-in-library=6; duplicate-of-existing=5; dedup=5; aggregate-list-not-a-source=4; outside-core-scope=4; unsafe-surface(hook/network/creds/installer)=4; talent-worthiness=3; reuse-first=2; too-thin=1; talent-worthiness + source-shape=1; dedup + talent-worthiness=1; source-shape=1; source-shape + talent-worthiness=1 (47 total) |
| Gate rejections · seed rows (aggregate, no per-candidate reason) | context only | 300 across 10 aggregate rows — excluded from the distribution above |
| Pass output · build (NOT a yield — rule 1 does not apply) | context only | 18/71 — see the note below |
| Pass output · curate (NOT a yield — rule 1 does not apply) | context only | 0/36 — see the note below |
| Harvest yield · github | **up** | 6/437 kept = 1% |
| Harvest yield · github-practitioner | **up** | 4/67 kept = 6% |
| Harvest yield · github-primary | **up** | 0/1 kept = 0% |
| Harvest yield · github-vendor | **up** | 0/19 kept = 0% |
| Harvest yield · github-vendor-refcode | **up** | 0/7 kept = 0% |
| Pass output · scout (NOT a yield — rule 1 does not apply) | context only | 11/11 — see the note below |
| Pass output · test (NOT a yield — rule 1 does not apply) | context only | 8/11 — see the note below |
| Harvest yield · web-top-n | **up** | 0/12 kept = 0% |
| Work types outside the harvest grouping | listed, never scored | build, curate, scout, test — shown so a new source_type cannot vanish silently |
| Measurement coverage · instrumented waves (>=19) | **100%** | 10/10 — waves 1-18 predate instrumentation and can never be filled |
| Human-gate proposals (resolved / open) | track hit-rate | 6 resolved · 3 open |
| Deploy gap (shipped but never reloaded) | **0 — routing is findable, deploy is LIVE** | 0 — every shipped talent has a deployed event |
| Defect families (where to look next) | learn the recurring shapes | missing-guard=19; asymmetric-rule=16; wrong-scope=11; open-loop=9; routing-contradiction=8; mismeasurement=7; dead-reference=4; factual-error=3; quality=2; nondeterminism=1 |
| Defects that fail SILENTLY (absence looks like success) | **down** | 67/80 = 84% — these need a positive control, not a reading |
| Independent-agent claim precision | **high, and MEASURED** | 43/52 = 83% confirmed · 4 partial (right finding, wrong mechanism) · 5 refuted |
| Descriptions over the pinned cap (1024) | **0** | 15 of 84 — abstention-threshold-design, agent-fault-injection, data-contract-assertions, eval-set-curation… |
| Time-to-detect (waves a defect lived before an independent test caught it) | **down** | median 0 of 58 measurable · 22 more existed since inception (untested until now) |
| Library composition (every talent category) | all categories managed | agent=1; skill=84 — non-skill units: rag-pipeline-reviewer |
| Routing coverage (findable when needed) | **100% (else can't be selected)** | 85/85 in map/ROUTING — all wired |
| Meta/loop-talent usage (used in a wave) | **most should fire** | 12/16 of the loop's own talents |
| Domain talents used in-loop | n/a — cross-project, no in-loop signal | 3/69 (disuse in-loop is BY DESIGN, never a prune trigger) |

Derived directives (recomputed):
- Test blend is HEALTHY on live work (44% normal of 241 scenarios). The library aggregate still reads 27% because 341 backfilled scenarios dominate it — that is history, not a defect to fix. Do NOT add normal scenarios to correct the aggregate.
- 15 description(s) exceed CONSTANTS.md's pinned cap of 1024. That number is corroborated by measurement (44 shipped skills on this machine: max 982, none above 1024), so the library is over the WALL, not a guideline. Trimming a description changes routing -- treat each as an edit with a trigger check, never a mechanical truncation.
- Most common defect family is missing-guard (19 of 80) -> when auditing, look for THAT shape first; a ranked taxonomy is a search order, not a tally.
- 84% of defects fail SILENTLY (absence looks identical to success). Reading a file cannot find these: every audit must RUN the method's own search/enumeration and confirm a known-present item comes back (a positive control).
<!-- /SIGNALS:auto -->
> Meta-rule: if "rot found per pass" does NOT trend down after the backlog is cleared, the
> lesson isn't reaching the BUILD step — strengthen the curator→piano LINK, don't just log it.

## 1. STATE — sync (avoid double-work / collisions)
Both loops run bounded passes, concurrently, one coordinator commits. **Cadence: `0 0,4,8,12,16,20`
(every 4h).** History worth keeping: throttled to every 8h on 2026-08-27 when the 7-day window hit
warning (a long window calls for throttling, not pausing) — **restored 2026-08-28 08:10 on the
user's call** once the binding window was back to `five_hour`/`allowed`. The throttle cost a real
overnight build wave (an 8h gap with no 04:00 fire), so the tradeoff is not free: throttle only
while a LONG window is actually warning, and restore as soon as it clears. Ownership so they
never fight over the same file:
- **piano owns:** NEW talent dirs (`.claude/skills/<new>/`), harvest, build, `frontier.json` queues.
- **curator owns:** EXISTING talents' `evals.md` + `SKILL.md` fixes, `CURATION-LESSONS.md`
  (its operating journal). `TEST-AUTHORING-LESSONS.md` is shared — both loops write it.
- **both:** append-only to `metrics.jsonl`; the coordinator serializes commits (pull → commit
  own files → push); never force-push. A talent being built (piano) is NOT curated the same
  cycle. Record in-flight claims below so nothing is double-assigned.
- **In-flight now:** _(nothing in flight. **This STATE line was written 2026-08-28 and is not
  a report on the week since** — the 2026-09-02/03 sessions and the 2026-09-04 knowledge-base
  work did not update it. Read `pipeline/STATUS.md` for what actually happened; do not treat
  the wave numbers above as current.)_
- **`[2026-09-04]` A THIRD maintenance surface exists, and this brain did not model it.** The
  brain says it is the control tower over two loops. Since 2026-09-02 there is a third:
  the **knowledge base** (`knowledge/notes/` + `raw/` + `kb.py` + the `kb-curator` agent +
  `llm-wiki-ingest`). It has its own lint, its own curator, its own raw layer and its own
  failure modes, and none of it was written here. Ownership so the three do not collide:
  **kb-curator owns** `knowledge/notes/` link and schema repair; **the coordinator owns**
  `knowledge/INDEX.md`, `VAULT.md`, `sources/SOURCES.md` and anything a curator is told to
  leave alone; **nobody edits `knowledge/raw/`** — it is immutable by rule. A KB pass and a
  talent pass do not touch the same files, so they may run concurrently.
- **`[2026-08-27 22:30]` OPERATIONAL LESSON — WHERE the loops must run.** Four spawned runs
  produced not one commit. Root cause: `skills-repo` is a **private** repo, and a
  `fire_trigger` run spawns a FRESH container (`origin: force_run_trigger`) with **no git
  sources and no credentials** — it cannot clone, so it correctly stops. The persistent session
  the triggers are self-bound to already HAS the repo + credentials, so the **scheduled** cron
  fire — which resumes that session — is the path that works.
  **`[2026-08-28] CORRECTION — the mechanism was NOT "no credentials".`** A controlled probe
  (a fresh `create_session` told only to call `add_repo` and report verbatim) settled it: the
  spawned session hit a **SECURITY GATE** — `status: need_input`, "needs user confirmation for
  private repo access", `SESSION_STATUS_BUCKET_BLOCKED`, and `sources` still empty. It did not
  lack access; it was **waiting for a human who was never there.** That explains the otherwise
  puzzling attempt-3 evidence: the run burned 13.7k tokens (real work) and then stopped with no
  commit and no scheduled resume — it reached the gate and waited.
  Rules learned:
  (1) **An unattended session cannot pass a human-confirmation gate.** Any step needing consent
  is a deadlock in autonomous work, not an error — it produces silence, not a failure message.
  Route private-repo (and any consent-gated) work to a session that ALREADY holds the resource.
  (2) Don't `fire_trigger` a routine whose work needs a private repo; use the scheduled path,
  which resumes the session that already has it attached.
  (3) Never probe a private repo with `curl`/`gh`/`git ls-remote` — misleading 404; never `find`.
  (4) Diagnose the RIGHT failure: no commit AND no scheduled resume means the run STOPPED, not
  that it was throttled. Ask what it was waiting for before "fixing" the wrong thing — the first
  diagnosis here (missing credentials) was plausible, fit 3 of 4 cases, and was still wrong.
  A controlled probe that could only produce one answer settled in 40 seconds what four
  production runs could not.

## 2. LINKS — connect (a learning by one becomes an action for the other)
The cross-agent wiring. Keep this current; it is the point of a shared brain.
- **curator → piano (build):** the curator's structural lessons must fire at BUILD time too,
  not only in curation — before piano commits a new talent, check: no dead cross-references,
  no invented slash-commands, tool claims verified by invocation form, `name:` present, tests
  in `evals.md`. (Source: `TEST-AUTHORING-LESSONS` directives — apply them in the build TEST step.)
- **piano → curator:** source-yield + build outcomes tell the curator which talents are fresh
  (just built, watch closely) vs battle-tested; a source class piano's security gate rejected
  (auto-run hooks, remote calls) tells the curator to watch for that pattern drifting into the library.
- **`[2026-09-04]` knowledge base → piano (build) and curator:** the KB's verification failures
  are the build loop's too, and two landed in `CURATION-LESSONS` the same day. (a) **Verify the
  SURFACE, not just the syntax** — a flag can be real on one command surface and silently
  ignored on another (`/graphify … --obsidian` is a skill flag; `graphify extract … --obsidian`
  is nothing), and the doc BRANCH matters as much: this repo's notes are written against a
  branch README while the project's default branch serves a year-old one. Three passes were
  spent on that single question. (b) **A silently-ignored flag is not just a wrong answer, it is
  a write somewhere you did not choose** — `graphify export wiki --dir X` ignores `--dir` and
  wrote 238 files into the immutable `intake/` import, untracked but not gitignored, one
  `git add -A` from a commit. Any talent that shells out to a third-party tool inherits both.
- **`[2026-09-04]` piano/curator → knowledge base:** the same discipline runs the other way. The
  KB's new `kb.py contradictions` was built the way a talent is: a first pass returned 9 hits,
  all false, and each of the three rules that quiet it is a named false positive it produced
  first — which is `measured-optimization-loop`'s method applied to a lint, not to a prompt.
- **shared brain (already live):** `TEST-AUTHORING-LESSONS.md` is read AND written by both — a
  test-writing lesson from either improves the other's tests. This is the model for every link above.

## 3. PLAN — what each loop does next (derived from the stores)
Recomputed each cycle from LESSONS + TEST-AUTHORING-LESSONS + CURATION-LESSONS + frontier + metrics:
- **piano next:** pick by source-yield (practitioner/framework repos > vendor-refs > lists,
  which are deprioritized); build queued `build_candidates` first (highest yield); scout when
  the source queue runs low.
- **knowledge base next `[2026-09-04]`:** lint is 0 errors / 0 warnings and `contradictions` is
  0, so the deterministic tier is clean and the next pass is judgement, not repair. Two things
  are queued and neither is urgent: the `agentskills.io/specification` source whose fetch date is
  `null` and unrecoverable (re-fetch or leave it honestly null), and the six Claude Code mechanics
  notes, re-fetched 2026-09-04 with no rot found — so the interval that matters for them is
  longer than eight days, and the next re-fetch should be driven by a release, not a calendar.
- **knowledge base next `[2026-09-08]`, replacing the line above for the link/verdict work:**
  the deterministic tier is still clean (lint 0/0, contradictions 0) and two of the three items
  queued on 2026-09-04 are now closed. The 67 note pairs that named each other without arguing
  it are all argued, and both standing `owners` candidates are settled — goose re-cited to
  `aaif-goose/goose`, graphify's `Graphify-Labs` confirmed right. **Still open, and now the
  whole of it:** the REPEATED tail. Ornith-1.5 came off it entirely on 2026-09-08 by trying the
  `/raw/main/` surface after a 401, so the queue should be worked **by whether a surface exists
  that was not tried**, not by count — and `best-local-llm-2026-09` is the honest floor, its
  remaining REPEATED rows being third-party Elo, one hardware review and retail prices, none
  reproducible from here. Also still open and unchanged: the `agentskills.io/specification`
  source whose fetch date is `null` and unrecoverable.
- **knowledge base next `[2026-09-08, second entry today]`:** the REPEATED tail was worked by
  the rule the earlier entry proposed — *does the note name a surface nobody opened?* — and six
  of six such notes answered, so **that queue is now empty of self-declared untried surfaces**.
  What is left divides cleanly and should not be worked as one list: (a) claims with **no
  surface at all from here** — `best-local-llm-2026-09`'s third-party Elo, one hardware review
  and retail prices; the two-week GLM safety hold; VirusTotal scanning of graphify releases —
  these are permanent and should stop being counted as a queue; (b) claims whose surface is a
  **paywalled or unlinked secondary** (the vectorize.io review, the "312 attempts" figure in
  `requirements-discovery` already traced to fabrication); (c) claims needing a **run, not a
  fetch** — Unlimited-OCR against our own `pdf` path is now the single highest-value item in
  the base, and it is a measurement, not a re-read.
- **the watcher is now a signal rather than an alarm `[2026-09-08b]`.** Its second batch reported
  8 CHANGED, of which **4 carried zero words** (Webflow republish stamps, a Vercel deploy id, two
  GitBook pages), and annotating them KNOWN-NOISY had not reduced what the reader has to do. The
  tool now asks the second question itself: bytes differ **and** the stored copy is HTML **and**
  its visible text is unchanged → `noise`, which does not fail. Byte comparison and `TAMPERED`
  are untouched; markdown stays strict. So a failing `watch.py` run again means what it says, and
  **the next batch's triage cost is the real test** — the first batch cost roughly an hour of
  hand-diffing for one true finding, this one about twenty minutes for four. Record that number
  next time; if it does not keep falling, the classifier is not earning its blind spot.
- **the one open item in the KB is still a RUN, not a fetch** (Unlimited-OCR against our own `pdf`
  path, above). Nothing in this batch changed that, and the batch is not a substitute for it.
- **SUPERSEDED `[2026-09-11]`: that item is not category (c) at all — it is BLOCKED, and the block
  is in the BASELINE arm.** Measured in this container: 0 PDFs in the repo; 7 of the 8 scripts in
  the public `pdf` skill fail at import; `pdftotext` and every other PDF CLI absent; no GPU, no
  `torch`. So the comparison has no document, no baseline and no candidate. It had stood as "the
  single highest-value open item, and it is a measurement" for three days *without anyone checking
  whether it could execute* — the check cost four commands. Full evidence and the unblock order are
  in `knowledge/notes/long-document-ocr.md`. Every unblock is a package install, which the fourth
  gate governs, so this moves from a queue the loop works to **a question standing for the human**.
  **REFINED `[2026-09-12]`: the count was 4 parts poison and 3 parts genuinely missing.** Re-run in a
  virtualenv holding nothing but `pypdf`, **5 of the 8 scripts pass** — isolation alone, no install,
  takes the skill from 1 of 8 to 5 of 8. The four recovered are all form-filling scripts, so what
  isolation buys is the half of the skill our routing line does not want; the reading half still
  needs `pdfplumber` or poppler. The conclusion holds and its size was overstated, by the same
  confusion that produced the block: **an import that raises is not evidence that a package is
  absent.**
  Two things follow for the loop. Category (c) "needs a run" must be split: a run whose arms are
  known to exist, and a run nobody has costed — only the first is work. And **a capability map
  cannot carry this**: `CLAUDE.md` routes PDF work through a skill that does not execute here, and
  no amount of listing what exists would ever have shown it. **Addendum, same day:** it is two
  skills, not one — `pdf-reading` sits beside `pdf` on the same path and fails identically (all five
  poppler tools absent). Our own executable surface was probed at the same time and is CLEAN: six
  shell scripts, six interpreters present, every external command they call present. The dead route
  is one we point at and do not own.
- **the PDF block is now HALF a block `[2026-09-11, third entry]`.** Acting on the finding above: the
  three PDFs four notes cited and nobody held are now held (`knowledge/raw/pdf-sources-2026-09-11/`,
  the raw layer's first binaries), and a stdlib-only reader with a coverage guard ships as
  `knowledge/pdftext.py` (25 fixtures, 12 mutations, no survivors, wired into CI). Measured: the two
  academic PDFs read at **100.0%** and the Anthropic guide at **17.6%**. So `requirements-discovery`'s
  sources became fully re-verifiable here at zero install cost, while the three notes resting on the
  guide did not. **The next action follows from that split, and it is cheap:** `requirements-discovery`
  now has held, readable primaries and open claims (the "312 attempts" figure already traced to
  fabrication) — verifying it against its own PDFs is a job this loop can do unaided, today, and it is
  the first KB item in a week that needs neither a fetch nor a human. The guide-backed contradiction in
  `skill-anatomy` stays blocked and stays the human's question, now with a number attached to it.
- **that next action is DONE, same day `[2026-09-11, fourth entry]`.** `requirements-discovery` was
  verified against its two held PDFs: **5 claims checked, 5 confirmed verbatim**, stamped in the note
  with the quote per row. The page needed no correction. Two by-products matter more than the result.
  The reader had a NameError on its primary output path through two commits while its 40-fixture suite
  stayed green — the predicates were tested and the entry point that joins them was not, and stderr was
  being discarded by the caller. And one row was **nearly recorded as a fabricated quotation** on the
  strength of a near-miss match elsewhere in the paper; the exact string was there, twice. Both lessons
  are in CURATION-LESSONS. **Next for this loop:** the same treatment is now possible for any note whose
  primary is a text-layer PDF, and impossible for the three resting on the Anthropic guide — which is
  the split the human's toolchain question decides.
- **second verification pass done, and one new finding outranks it `[2026-09-11, fifth entry]`.**
  `llm-idea-generation` checked against its two readable primaries: **7 claims, 7 confirmed
  verbatim**, plus one precision (GPT-4 on HotpotQA is a TIE at round 1, 49.0 → 49.0, before falling
  to 43.0 — the universal "every model, every benchmark drops" survives but the cell is recorded) and
  two figures marked **unverifiable HERE** rather than left silent. The watcher's fourth pass then
  returned `plugin-evals.md` changed again, an hour after the last re-baseline, and it carries the
  finding of the evening: **an `llm` grader sees only the first 12 and last 12 messages of a run.**
  Past 24 messages the judge is blind to the middle and says nothing about it — which lands directly
  on the measurement this library requires of every talent, since an effect that shows up mid-run is
  invisible to the grader meant to detect it. A `regex` grader is the one that sees everything. Also:
  the cost formula, spelled out, is **double** a one-armed reading (`cases × runs` with the plugin
  *and as many again* for the baseline). Both belong beside the plugin-packaging decision, which is
  the user's. **Next for this loop:** four observations now say `code.claude.com` moves several times
  a day against weekly READMEs, and three of three re-reads carried substantive diffs — the change to
  propose is a per-host interval, not a faster global schedule, and it needs the substantive-diff
  rate recorded for one more pass before it is proposed at all.
- **that pass came back empty, and it changes the reading `[2026-09-12]`.** `86 unchanged · 0 changed
  · 10 noise · 0 tampered`. Three changes clustered in one evening is a **burst**, not the hourly rate
  the run of positives suggested, and a per-host interval derived from the burst would over-fetch
  every quiet hour. The proposal stays unmade; what it now needs is a spread of quiet AND busy passes.
  Recorded because a quiet pass is the denominator nobody writes down.
- **open in the KB, found by the 2026-09-08 walk-through and NOT closed by it:** (a)
  `third-party-landscape` is a compiled page whose five inputs have all moved since it was
  written; the lint now says so on every run (2 standing warnings, not errors). Recompiling a
  29 KB synthesis over 44 notes is a real job and a wholesale rewrite of a summary page, so it is
  a proposal, not a curator's fix. (b) `status:` has cardinality ONE across all 44 notes — every
  page is `verified`. Deciding what the other values mean and re-grading against them is a
  judgement about the base's standard. Both are for the human, and both are cheap to check again:
  `kb.py lint` reports the first, and the second is one query.
- **OPEN QUEUE, 2026-09-11: 27 watch rows are CHANGED and deliberately unread.** The third batch
  moved 40 of 96 rows over three days. Seven were triaged and re-baselined; the rest stay red
  because re-baselining a row without reading its notes converts an honest backlog into a silent
  one. Ten of them are `code.claude.com` docs this base cites heavily and they are the real job:
  **`skills.md` moved 2,130 words, `hooks.md` 1,090, `model-config.md` 1,051, `sub-agents.md` 499,
  `mcp.md` 464, `workflows.md` 405**, plus `plugins`, `plugin-marketplaces`, `memory` and
  `llm-gateway-protocol`. That is an ingest pass (`llm-wiki-ingest`, update branch), not a triage.
  Do it before the next batch lands on top of it. `workflows.md` is doubly owed: it has not been
  re-read since 2026-08-27 and its held baseline already carries a concurrency qualifier
  `dynamic-workflows` does not.
- **triage cost, as this file asked: it fell.** ~1 h for 4 rows (batch 1), ~20 min for 8 (batch 2),
  ~15 min to classify 34 and settle 7 (batch 3). The gain came from ORDER, not effort — rank the
  queue by size of prose diff, smallest first, and the one-word rows resolve at a glance. Keep
  measuring it; if it stops falling, the classifier has stopped earning its blind spot.
- **curator next:** NEW/stale talents first (no `evals.md` or changed since last eval); when
  none, DEEPEN old (fresh adversarial scenarios for the weakest/oldest-tested suites).
- **current plan `[2026-08-28 09:0x]`:** piano → BUILD the 3 remaining queued candidates (agent-fault-injection — SPECIFY AGAINST A STUBBED TOOL LAYER per its security note — then idempotent-action-design, data-contract-assertions); then the 8 practitioner sources queued from the top-100 + blog triage (addyosmani/agent-skills and mattpocock/skills first; agenthatch for build-time SKILL.md validation). curator → the 5 untested (research-scout, skill-stocktake, talent-deploy, wave-reflect, writing-plans), then deepen trap-heavy suites with NORMAL scenarios (blend 31% vs 50% target).
  candidates, wave 20; build yield ~1.0 vs harvest 1% — do NOT harvest while the queue has
  items). Order: stage-ablation-attribution → eval-set-curation → abstention-threshold-design
  → agent-fault-injection → idempotent-action-design → data-contract-assertions. NB
  `agent-fault-injection` must be specified against a STUBBED tool layer (security gate note).
  curator → the 8 orchestrator talents still untested, then deepen the trap-heavy suites with
  NORMAL scenarios (blend is 29% normal vs the 50% target).

## 4. OPTIMIZE — efficiency directives (cross-cutting)
- **Concurrency is ~2 (min(16, cpus-2)) and shared** — running both loops at once does not add
  throughput on a 4-core box; the lever is more CPU cores. Don't fan out wider than useful.
- **Bias to build over harvest** while `build_candidates` is non-empty (build yield ≈1.0 vs
  harvest ≈0 for picked-over sources).
- **Measure, don't estimate** (now LIVE for time; partial for cost): every wave/pass records
  MEASURED `wall_clock_s` + `agents` (bash `date` delta + spawn count) to `metrics.jsonl`, and
  ticks the per-talent/eval/rejection/proposal ledgers (`DATA.md`) live — because cost, time,
  and lineage can't be reconstructed later. Real token `spend_measured` stays `null` until a
  wave routes through a metered path (never faked). The data-science ANALYSIS layer is still
  deferred until volume exists — rule-based reflection is right until then; but the COLLECTION
  runs now so the record is analysis-ready when we want it.
- **`[2026-09-04]` Write the telemetry IN the turn the pass ends, not the turn you remember it.**
  The KB curation pass ran with no `metrics.jsonl` row; it was written hours later and survived
  only because the completion notification still carried `wall_clock_s` and the agent count. One
  compaction later and a MEASURED number becomes an estimate forever. "Live" in `DATA.md` means
  the same turn, and this is the first recorded near-miss of that rule.
- **`[2026-09-04]` A check nobody's runbook runs is a check that never runs.** Shipping
  `kb.py contradictions` was not done when it passed its tests; it was done when `kb-curator`
  step 1 and `llm-wiki-ingest` step 7 called it by name. Treat the wiring as part of the build,
  the way `talent-deploy` treats routing — and state the honest limit where it is called, so a
  silence is not read as a clearance.
- **`[2026-09-08]` Split a check's population before you rank its output.** Twice in four
  days a signal was reported as one queue when it was two: REPEATED mixing provenance with
  confidence, then the related-edge rule counting 212 items when 134 were the debt and 76 were
  a shape this repo's own reciprocity rule *creates*. Both were found the same way — by asking
  "what would a hit look like if the system were working correctly?" and discovering that a
  large share of the hits looked exactly like that. Ask that of every check before trusting its
  ordering, and lift the predicate into a tested function while you are there: the third such
  fix in this base, and the one whose predicate stayed inline is the one that was contaminated
  by its own fixture.
- **`[2026-09-08]` A refusal is a property of the surface, not of the source.** A 401 from a
  rendered page left five claims REPEATED for six days; the same content answered at a raw path,
  refuted the claim two secondaries agreed on, and turned up a fact (three models are
  vision-language) that no source had stated. Before recording UNREACHABLE, try the other
  surface — raw over rendered, API over HTML, the artefact over the page about it.
- **`[2026-09-08]` Point the scepticism at the summary, not at the source.** Three times in one
  pass the unread primary was *more* careful than our note about it: a benchmark author
  disowning his own headline baseline, a paper naming its own failure mode and labelling its
  speed table theoretical, a second paper scoping cross-model evaluation out as future work.
  The lossy layer is the carousel, the video and the write-up. A verdict that treats "we have
  not read it" as a reason for suspicion of the *source* has the arrow backwards.
- **`[2026-09-12]` A reason for NOT monitoring something is a claim about the world, and it can be
  wrong in exactly the way the monitoring would have caught.** Five arXiv PDFs were excluded from
  the watcher on the stated ground that *"arXiv version ids are immutable, so the URL cannot change
  under us."* An id is immutable; `arxiv.org/pdf/<id>` **without** a version suffix resolves to the
  LATEST version, and that is the form all five were stored under. One of them had already been
  revised: 64 pages became 93, and four figures a note cites changed — twelve interventions to
  thirteen, 45 conditions to 73, 62 baseline comparisons to none stated, seven models to ten. The
  note was **right about v1**; the source moved under it, silently, behind an exclusion whose
  justification was the very thing that failed. The sweep the finding demanded — all five held
  arXiv PDFs re-fetched at `<id>v1` and compared by hash — found **two of five are not v1**, and
  the two differ in *direction*: one revision changed figures already recorded, the other ADDED a
  row a note now cites and v1 does not contain. So "is our copy current?" and "is our copy the one
  we read?" are two questions, and neither answers the other. Two operational rules follow. **Pin the version in
  the citation** when a claim rests on one reading, and **hold the pinned copy**, or the pin names a
  document the repo cannot produce. And when writing an exclusion: state the reason as a testable
  claim, then ask what would falsify it — this one survived a day only because nothing read the
  file it excused.
- **`[2026-09-12]` A control that isolates the claimed cause, or the cause is still a story.** The
  "pypdf is broken here" blocker was retired by running pypdf in a virtualenv — at a NEWER version
  than the system's, which left the version as an untested confound. The control is the SAME version
  isolated: 6.17.0 in a clean venv reads what 6.17.0 system-wide panics on. One extra command turned
  a plausible diagnosis into a demonstrated one, and the pattern generalises to every "it works over
  here" claim this repo makes.
- **`[2026-09-12]` An extraction defect that yields VALID output in the target language is invisible
  to every guard we have.** Reading the Anthropic guide found `##` extracting as `-#` and `###` as
  `--#` inside its code blocks — a programming-ligature font whose placeholder glyphs carry no
  `/ToUnicode`. A dropped `fi` reads as a typo; **a heading level rewritten as a hyphen reads as
  valid markdown of the wrong depth.** Coverage measured 100% for the missing spaces, 100% for the
  dropped ligatures, and would measure 100% here: the quantity a guard measures cannot see a defect
  whose output is well-formed. Only knowing what the source said catches it, which is the argument
  for quoting against a held copy rather than trusting an extraction.
- **`[2026-09-12]` A table absorbs any number you put in it.** Two rows in `skill-anatomy`'s
  frontmatter-constraints table — the 5,000-word body figure and the 20-50 enabled-skills figure —
  are not constraints at all: in the guide they sit under one `Solutions:` heading in the
  troubleshooting chapter, remedies for a skill already diagnosed as slow. Nothing rejects a
  6,000-word body. They had been read as bars for two weeks because every row around them is one,
  and the same figure was carried into a four-source "unreconciled contradiction" where it was
  comparing a rule with a repair. **Check what KIND of statement a quote is, not only whether it is
  accurate** — a correctly transcribed sentence in the wrong table is still a false claim.
- **`[2026-09-12]` Second recorded near-miss on the live-telemetry rule, and this one was caught by
  arithmetic.** A pass's `wall_clock_s` was computed from a *remembered* start time and came out
  **negative**. Nothing verified it; a start guessed two minutes late instead of five would have
  landed a plausible wrong number in `metrics.jsonl` forever. Recovered honestly from the mtime of
  the pass's first artefact. The rule in `DATA.md` says capture time LIVE; the practical form is
  **stamp the start before the first command, because a duration reconstructed at the end is a
  guess wearing a number's clothes** — and only sometimes does it have the decency to come out
  negative.
- **Soft-stop always** — finish the in-flight unit/batch, commit, leave a consistent state.

## How to use (both agents)
1. **Start:** read this file + `TEST-AUTHORING-LESSONS` (shared, before any test authoring) +
   your own store (piano→LESSONS, curator→CURATION-LESSONS) +
   the last ~10 `metrics.jsonl` rows. Apply STATE ownership + the PLAN.
2. **End:** update STATE (in-flight → done), add any new LINK you discovered, refresh the PLAN
   line for your loop, append your `metrics.jsonl` row, and commit. The next run — either loop —
   reads the brain you left.
