# Rethink — the skill-builder, from the measurements up

**Date:** 2026-09-02. **Asked:** look at the skill-builder with everything the knowledge base
holds about agents, subagents, chains and skills, and propose a different shape that runs
faster, given the vision (`pipeline/SKILL-BUILDER-SPEC.md`), the input (a package) and the
output (a tested skill with its evals and record). **Method:** a cold position written before
reading the chain contract, the dispatcher or the three method skills (§1, verbatim); then the
measurements (§2, a new query over the five builds' cost ledgers); then the informed rethink
(§3–§5), each proposal graded build · complete · keep · park. Companion to
`REVIEW-2026-09-02-skill-builder.md`, which found the same 79-minute build and recommended
the dispatch harness that now exists; this document starts where that one stops.

## 1 · Cold position (verbatim, written first)

# Cold position — a faster skill-builder (written 2026-09-02 before reading chain.contract.json, dispatch.py or the three method skills; only the agent's posture file and STATUS/ledger rows seen so far)

What I know going in: a build takes ~40 min when nothing goes wrong, the dispatch floor alone is 28 min; every probe/arm/reader/grader is a separate `claude -p` run through dispatch.py at a fixed tier; the agent authors fields one by one against a field contract; blinding, preregistered thresholds and code gates decide.

Position:
1. The 28-minute floor is serial `claude -p` cold starts. Each run pays full context load (CLAUDE.md, skill listing, method dir) and gets no cache, because parallel runs launched at once all miss and separate processes share nothing. The fastest change is not fewer runs but *shared prefix and overlap*: warm one run, then launch; run arms concurrently up to W_MAX_AGENTS (4); author the next field while runs are in flight.
2. Half the runs are probably measurement of things that could be decided deterministically or by a cheaper reader: description trigger matrix (a listing-selection test can be simulated with a haiku reader, not an opus arm), field-length gates (code), leak checks (regex). Keep opus/fable only for the with/without arms and the blinded grader.
3. The field-by-field loop with a reader after each field is a serial chain of model round-trips. Batch: author all fields in one turn from the probe's observed failures, then one reader pass; iterate only on the fields the reader rejects.
4. The probe is the load-bearing step (a step comes only from an observed failure). Do it once, well, on 3–5 scenarios in parallel, and derive the whole skill from the failure list. Everything after is verification.
5. Expectations should be written from the baseline's observed outputs (already the rule), which means the with-arm can run *before* grading is designed — overlap them.
6. Stop rule: preregistered threshold; if the with-arm clears it on the first paired run, do not run repeats "to be safe"; repeats only when the margin is inside the noise band measured once for the tier.
7. A different shape entirely: treat the skill as a *diff against a baseline transcript*. The baseline transcript is the spec; the skill is the minimal text that turns the observed failures into passes; the measure is the same fixture replayed. That makes the build a two-run experiment plus a grader, ~3 dispatches in parallel, under 10 minutes wall clock.
Expected cost of being wrong: if the contract's phases exist for reasons I have not read (contamination, reader independence), (3) and (7) may violate them; those reasons must be checked before proposing.

## 2 · What the ledgers say — one query, five builds

`pipeline/queries/job_class_cost.py` (new, this document) aggregates every dispatched run in
`pipeline/builds/*/cost/measured.jsonl` by **job class** — the key a routing table would use —
and every coordinator turn by kind. Rows without a field are counted as absent, never zero.

All five builds (three ran before the harness existed; their rows lack tier and sometimes tokens):

```
builds: 5  (abstention-threshold-design-v2, control-seam-audit, data-contract-assertions-v2, eval-set-curation-v2, paired-comparison-blinding)
class      runs     min  %min    Mtok  %tok  max run  tools  tiers / rows without a field
arm          74   248.0    50    9.20    44     11.6    195  absent:14,opus:60 / tokens:52, tool_calls:52
reader       45   107.3    22    4.83    23      5.2     65  absent:21,sonnet:15,opus:9 / tokens:8, tool_calls:8
probe        25    64.8    13    5.02    24      6.9    123  absent:10,opus:15 / tokens:11, tool_calls:11
grader        6    32.5     7    0.32     2      8.2      0  absent:2,opus:4 / tokens:2, tool_calls:2
reviewer      4    20.6     4    1.33     6      8.3     24  absent:2,opus:2 / tokens:1, tool_calls:1
writer        7    18.6     4    0.00     0      4.7      0  sonnet:3,opus:4 / tokens:7, tool_calls:7
calibrate     1     1.8     0    0.00     0      1.8      0  opus:1 / tokens:1, tool_calls:1
trigger       4     1.3     0    0.18     1      0.4      2  absent:1,opus:2,sonnet:1 / tokens:2, tool_calls:2
total       166   494.9         20.87

coordinator turns (only builds that recorded them):
  waiting           14 turns   195.7 min  in 2 build(s)
  authoring         15 turns    47.8 min  in 2 build(s)
  planning          16 turns    27.6 min  in 2 build(s)
  reading_verdict    6 turns    20.6 min  in 2 build(s)
```

The one clean build, `eval-set-curation-v2` (79.4 min wall clock):

```
builds: 1  (eval-set-curation-v2)
class      runs     min  %min    Mtok  %tok  max run  tools  tiers / rows without a field
reader       16    37.6    38    1.02    13      4.8      1  sonnet:10,opus:6 / -
arm           8    31.9    32    4.95    61      7.3     94  opus:8 / -
probe         4    12.5    13    1.80    22      5.0     38  opus:4 / -
grader        2    12.1    12    0.19     2      6.5      0  opus:2 / -
reviewer      1     4.4     4    0.08     1      4.4      0  opus:1 / -
trigger       1     0.3     0    0.07     1      0.3      0  sonnet:1 / -
total        32    98.8          8.10

coordinator turns (only builds that recorded them):
  authoring         14 turns    44.6 min  in 1 build(s)
  planning          11 turns    16.6 min  in 1 build(s)
  reading_verdict    5 turns    10.6 min  in 1 build(s)
  waiting           12 turns     7.7 min  in 1 build(s)
```

Five readings, and they decide the shape in §3:

1. **Readers are the largest dispatched class in the clean build** — 16 runs, 37.6 of 98.8
   dispatched minutes, on one skill. They are the per-field external check of phase 4. Across
   all builds: 45 reader runs, 107 minutes, and the contract's own `convergence` block records
   a reference field going 7 rounds with round durations rising from 80 s to 313 s.
2. **Arms are the token cost, not the time cost** — 8 runs, 61% of the clean build's tokens,
   longest 7.3 min. They are the measurement; the contract's `never_routed_down` list keeps
   them on the fixed tier, and the review is right that a prompt-only arm would measure the
   wrong thing. They can only be *overlapped*, not shrunk.
3. **The coordinator's own turns are 72 of 79 minutes**: authoring 44.6, planning 16.6,
   reading verdicts 10.6, waiting 7.7. Concurrency touches only the 7.7. The chain has 21
   `model` phases; each is a coordinator turn on the top tier.
4. **Graders and the review are small in tokens and large in latency** (grader 6.5 min, review
   4.4 min, single runs): they sit on the critical path because the contract orders them
   serially — 5.2 before 6.1, 6.3 before 6.4.
5. **Across all builds, `waiting` is 195.7 minutes** — almost all of it build 3
   (`data-contract-assertions-v2`, 517 min, two rate limits, 36 arm runs for 12 valid
   observations). The harness that now exists is the fix for that build; it is not a fix for
   the clean one.

So the review's sentence holds and gets a number: the dispatch floor is 28 minutes, and the
other 51 minutes of a clean build are the coordinator writing and reading, one field at a time.

## 3 · The different shape — three fat turns and two fan-outs

The principle the cold position reached and the ledgers confirm: **the artefact is written
from the probe's failure list, so everything after the probe is verification, and verification
fans out.** Today the chain is 39 phases walked in order by one coordinator. The proposal keeps
every guarantee the contract names (fresh sessions, path not text, blinding before
expectations, calibrated grader, preregistered threshold, `never_routed_down`) and changes
*who does the writing, how many turns it takes, and what overlaps what*.

```
T0  code      admit · open record · scout (grep) · siblings          ~1 min
    dispatch  PROBES ×(tasks × 2) — launched HERE, before any reading  5 min, overlapped
T1  model     while probes run: bill of materials, eval prompts, fixtures
    code      probes back → code failures (quoted) → gap verdict → coverage
T2  model     author ALL fields in one pass, contract order, from the failure list
    code      skill_contract.py over the whole artefact (loop until green, no reader)
    dispatch  FAN-OUT A, same turn:  whole-artefact review (5.2)  ∥  description reader (4.7)
                                     ∥  arms with/without/incumbent × repeats (6.1)
T3  model     review back: if it names a CLASS-level defect in steps or description →
              rewrite once, re-run arms (one wave); else arms stand.
              blind outputs → expectations from the blinded copies
    dispatch  FAN-OUT B, same turn:  calibration specimen (6.3)  ∥  graders (6.4, ≥2)
                                     ∥  trigger matrix (6.5, sonnet, code-generated queries)
T4  code      calibration red → graders' verdict void, re-grade with a fresh grader
              decide.py · emit · deploy
```

**What changes, and the evidence for each:**

| change | replaces | evidence | outcome |
|---|---|---|---|
| **No per-field readers.** One code checker in a loop, then one whole-artefact review and the description reader — the two the contract already marks `never_batched`. | 16 reader runs / 37.6 min | reading 1; the review at 5.2 exists and "sees the artefact entire and can rule on what a field-local reader could not" (contract `convergence.on_exhaustion`); batching was already made mandatory because readers per field "did not happen" as an option | **build** |
| **Author all fields in one turn from the failure list**, in the contract's order, description last. | 9 authoring phases, 14 authoring turns, 44.6 min | reading 3; the order dependency the method states (description needs the finished body) is satisfied inside one turn; the "red field never proceeds" rule is kept by the code checker, which runs on the whole artefact | **build** |
| **Probes at T0**, before scout/siblings/planning. | probe launched 4 min after open | probes need only `representative_tasks` from the package; nothing before them feeds them | **complete** (a reordering) |
| **Review ∥ arms** (fan-out A). Arms run on the artefact as written at T2; a class-level review finding re-runs them once. | 5.2 then 6.1, serial | reading 4; the risk is one wasted arm wave (~5 Mtok, ~$25 at Opus list) when the review changes the steps materially — the ledgers do not yet say how often 5.2 changes steps; **preregister it** (§5) | **build, measured** |
| **Calibration ∥ graders** (fan-out B); a red calibration voids the grade instead of preceding it. | 6.3 then 6.4 | same shape as above; the contract's reason for 6.3-first is that a blind grader's "no findings" is uninterpretable — voiding satisfies it | **build, measured** |
| **Triggers on Sonnet with code-generated near-miss queries** | opus/sonnet mixed | `model_routing.rule`: a check that needs reading but not deep reasoning may run on a cheaper tier; the description reader itself stays on the fixed tier | **complete** |
| **Coordinator on Fable 5.1**, effort high, for T1–T3 | inherits | the writing is where the artefact is made (72 of 79 min); a stronger writer with fewer turns is the whole bet — and Scio ADR-0008 says every skill must be re-measured on Fable anyway | **build, measured** |
| Arms as prompts instead of agents | — | the review: "would measure who sounds wisest rather than who finds the unit change" | **park** (keep, with reason) |
| Cheaper tier for probe, arms, review, graders, description reader | — | `never_routed_down`: "a different experiment wearing the same name" | **keep** |
| Fewer repeats | k ≥ 2 | the threshold is preregistered per package; one run cannot tell a tie from a regression | **keep** |

**Floor of the new shape, derived from the clean build's own run lengths:** probe 5.0 (overlapped
with T1) → fan-out A max(7.3 arm, 4.4 review) = 7.3 → fan-out B max(6.5 grade, 1.8 calibrate,
0.3 trigger) = 6.5 → **≈ 19 dispatched minutes on the critical path**, against 28.3. Coordinator:
four fat turns instead of twenty-one; if a Fable authoring turn costs what an Opus one did
(3.2 min average in the clean build) that is ~15 min, against 72. **Estimate: 35–40 minutes
for a full build, DERIVED, not measured**; the honest range is 30–50 until one build runs.

Ten minutes is still not this. The review's line stands: ten minutes means measuring less.
§4 says how to get the *user* a result in ten minutes without measuring less.

## 4 · The one idea that is actually different: decouple authoring from measurement

Every current mode waits for the verdict before the artefact exists anywhere. The build that
can ship is the build the user waits 40–80 minutes for; `fast` gives a `fast_pass` that ships
nothing. A third state removes the wait without weakening the evidence:

- **`candidate`**: the artefact after T2 + fan-out A's review — code-green, reviewed whole,
  description read — is written into the library **marked `candidate`** in its frontmatter and
  in `talents.jsonl`. It is loadable by name, absent from the capability map, and cannot be
  routed to automatically. Time to `candidate`: T0–T2 plus one review ≈ **10–12 minutes**.
- **Measurement runs detached**: fan-out A's arms, fan-out B, `decide.py` — as a background
  dispatch (`dispatch_many` in a background job today; a Workflow when the run is large:
  16 concurrent agents, resumable within the session, per
  [[dynamic-workflows]]) that appends its rows to the same build record and, on `ship`, flips
  `candidate` → `adopted` and deploys; on `iterate`/`abandon`, leaves the candidate marked with
  the verdict and the report.
- **Nothing about the evidence changes.** Same arms, same repeats, same blinding, same
  threshold, same `decide.py`. What changes is *who waits*: the piano loop and the user get the
  artefact in ten minutes; the verdict arrives when the measurement is done, and until then the
  artefact says so on its face.

This is the same move the review made with `fast`, done without giving up the comparison. It
needs: a `candidate` status the loader and the capability map respect (one field, two
readers), and a detached measurement path that writes into an open record (the record is
append-only already; the missing piece is a `record.py close --from-detached` that runs the
gates when the background rows land). Both are code; neither is a new gate on the coordinator.

## 5 · How to know — preregistered, before the first v3 build

Measured on the next full build, in the v3 shape, on a package of the same kind as
`eval-set-curation-v2` (existing-artifact, shape failure kind):

| question | number | decides |
|---|---|---|
| wall clock, open → decide | **< 45 min** (baseline 79.4) | the shape |
| coordinator turns | ≤ 8 (baseline 21 model phases / 42 recorded turns) | the fat-turn claim |
| reader runs | ≤ 2 (baseline 16) | the no-per-field-reader claim |
| review changed steps or description at class level | recorded yes/no | whether fan-out A's speculation pays; if yes twice in three builds, revert to serial 5.2 → 6.1 |
| calibration red | recorded | whether fan-out B's void-and-regrade ever fires |
| verdict quality | the same threshold clause; zero regressions on correctness | the shape did not buy speed with a worse skill |
| time to `candidate` | < 15 min | §4 |

Anything that misses is reported as missed. The shape is adopted only if the first row passes
and the sixth holds; the others tune it.

## 6 · What this document did not do

- It did not change the agent file, the contract or the dispatcher. Those are the other
  session's, mid-build; the proposal is for the next contract version, not a patch.
- It did not run a build. Every minute in §3 is derived from the clean build's own rows.
- It did not read hello-world's older harness rounds (`metrics.jsonl` 2026-08-30: 24 agents,
  1,876 s, 1.64M tokens est.) beyond the row; that run predates the contract.
- The knowledge base's third-party methods were checked for a different shape and none has
  one: Anthropic's skill-creator loop is the same probe → write → eval → iterate, run by one
  author with subagent runs; superpowers' writing-skills has no measurement; the two things
  Anthropic adds that we lack are variance analysis (repeat-N, already in our threshold) and
  the description optimizer (already a talent). The different shape here comes from the ledger,
  not from a repo.

## 7 · Implemented the same day (contract 3.0.0)

On the user's go: mode `v3` in `pipeline/contracts/chain.contract.json` (skips nothing,
ship-capable, order and fan-outs declared, coordinator tier recorded), a `fanout` rule block
with its two revert rules, `record.fanout_gate()` and `--coordinator-tier`, a contract-driven
ship check in `decide.py` (a mode ships only if its contract verdicts say so; `fast` still
cannot), thirteen new controls in `selftest_build.py` (94/94), and the agent file rewritten
to the T0–T4 posture with `v3` as the default for "build X" and `full` kept for comparison.
Not done: §4's `candidate` status — the skill contract refuses non-portable frontmatter and
unplanned files, so it needs a home in `talents.jsonl` and the capability map first. Not
measured: nothing here has run a build; §5's table is what the first one is judged by.

## 8 · How much more can move into code — phase by phase (added 2026-09-02, on the question "is this all?")

v3 changed the *order*. The next lever is the *kind*: of the chain's 39 phases, 21 are
`model` — coordinator turns on the top tier — and the clean build's coordinator time was
authoring 44.6, planning 16.6, reading verdicts 10.6. This table asks, per model phase,
what a script could settle, what a script could *propose* for the model to confirm, and
what must stay a model's. "Code" here means deterministic Python with no model call, the
same standard as `decide.py`, `triggers.py`, `calibrate.py`, `extract_scripts.py`,
`expectation_power.py` and `extend_gate.py`, which already are.

| phase | today | can be | how | saves |
|---|---|---|---|---|
| 1.1 scout | model | **code proposes, model rules on the borderline only** | term-overlap and trigger-term hits over every description; `reuse` when one unit owns ≥ k of the package's trigger terms, `author` when none does, the model reads only the band between | most of 1.1 |
| 1.2 siblings | model+code | **code** | nearest N descriptions by overlap, written to `siblings.json`; the description reader gets that file | a turn |
| 2.2 code failures | model | **code for `shape`, model for `knowledge`** | a shape failure is "the artefact lacks column X / locator / verdict": the same checker the contract already names as the shape *grader* runs over probe outputs; the model quotes only what code cannot name | half the probe-coding turns |
| 2.4 eval prompts | model | **code** | the package carries `representative_tasks` with `artifact_expected` and the probe already ran them; prompts = task verbatim + fixture path, written by a template | a turn |
| 2.5 fixtures | model | **code where a generator exists** | synthetic generators per failure kind (rows with one planted unit change, a doc with one contradiction); model only for domains with no generator | varies |
| 3.1 coverage | model | **code proposes** | failures and claims both carry tags; uncovered = failure tags with no claim tag; model confirms the mapping | most |
| 3.5 reconcile | model | **code** | duplicates by quote hash; contradictions = same claim key with different verdicts, kept as rows | all |
| 4.0 bill of materials | model | **code proposes** | a BOM template per `failure_kind` × `content_kind` (shape → `references/columns.md` + `evals/`; knowledge → `references/claims.md`); model classifies the rows | half |
| 4.3 name, 4.8 frontmatter | model | **code** | the contract already decides both; the checker can emit them | two turns |
| 4.1 references | model | model, but **assembled by code** | claim rows → a reference file is a rendering; the model writes only the prose between rows | half |
| 4.4–4.6 body | model | **model** — this is the artefact | | — |
| 4.7 description | model | **code-driven search around the model** | generate N candidates, score each with `triggers.py`'s matrix on code-generated near-miss queries, pick the best: Anthropic's own "description-improver", a talent this repo already holds (`skill-description-optimizer`) | reader rounds |
| 6.2 expectations | model | **code for `shape`**, model for the rest | shape expectations are the checker's rules applied to the blinded outputs; `expectation_power.py` already prunes the inert ones | a turn |
| 7.2 triage | model | model, **code pre-sorts** | a red whose expectation is inert by `expectation_power.py` is a test bug by construction | part |
| reading verdicts (10.6 min) | model reads prose | **code** | every reader, reviewer and grader returns a JSON row against a schema (`structured-llm-extraction`), and a script folds them into the record; the coordinator reads a table, never a transcript | most of 10.6 |
| planning (16.6 min) | model | **a chain runner** | `pipeline/build/run_chain.py`: a state machine that executes every `code` phase, dispatches every `dispatch` phase, waits, runs the gates, and *calls the model only at the write points* (2.2 for knowledge, 4.1–4.7, 6.2, 7.2). The agent stops being the driver and becomes the writer | most of 16.6 |

Read across: the writing that must stay a model's is 4.4–4.6, the prose of 4.1, the
knowledge half of 2.2 and 6.2, and 7.2's judgement. Everything else is either code or code
with a model confirming a proposal. Derived, not measured: with the runner and the JSON
returns, the coordinator's 72 minutes become the authoring turns alone — 20–30 minutes of
generation — and the build lands at **25–30 minutes** with the same evidence. Below that is
the dispatched floor (19), which only `candidate` (§4) hides from the user.

Two things the package (the JSON input) should *not* absorb, and why: eval prompts and
expectations. The spec's line holds — "the package carries what a run cannot produce" —
and both are checked against the skill that actually got built. Moving them upstream
makes them unverifiable, not faster.

The order to build it, cheapest evidence first: (1) JSON returns for readers and graders
plus the folding script — it removes reading time in *every* mode and needs no new phase;
(2) `run_chain.py` over the `code` and `dispatch` phases, with the model calls as the four
write points; (3) the code-proposes phases (1.1, 3.1, 4.0) with a "model overrode the
proposal" event so the ledger says how often the proposal was wrong; (4) the description
search. Each step is measured by the same §5 table with one extra column: coordinator
turns, which should fall from ≤ 8 to ≤ 4.

## 9 · Thinking further — the levers under the floor (added 2026-09-02, on "think more")

§3 reordered, §8 moved turns into code. Both leave two things untouched: the dispatched
floor (probe 5 → arms 7.3 → graders 6.5) and the number of runs the measurement buys.
This section attacks those, then the objective itself. Each lever names its evidence in
this repository's own ledgers and what would have to be preregistered for it to count.

### 9.1 Runs that are paid for twice

- **The probe already IS the without-arm.** The spec says `representative_tasks` are
  "used by the probe AND the evals"; the probe runs them without the skill, in fresh
  sessions, fixture as a path — exactly the without-arm's definition. In the clean build
  that is 4 probe runs and 4 without-runs on the same prompts. The contract's "same turn"
  rule exists for *timing and tokens under the same load*, not for correctness. So: the
  probe outputs are the without-arm's correctness repeats; one without-run per test is
  re-dispatched in the arms' turn for the cost clauses only. Arms in the clean build:
  8 → 5. **Saves ~3 of 8 arm runs, ≈ 37% of the class that holds 61% of the tokens.**
  Preregister: correctness clause may read probe rows; cost clauses may not.
- **`k` follows the probe, as the spec's own table says.** Baseline fails on every task →
  "1 suffices"; passes unevenly or cleanly → ≥ 2. The default threshold says k ≥ 2 always,
  which contradicts the table. Derive k from 2.3's gap verdict, preregistered as a mapping,
  and half the arm waves disappear on the decisive-probe builds.
- **Fail fast where the package was wrong.** `expected_failure` was refuted **4 of 4**
  times (review, "what the measurement established"). When the probe shows a clean
  baseline *and* the package names no axis to win on, the build's best outcome is a
  measured tie at 40 minutes. Preregister: that case stops at T1 with `abandon: no axis`,
  ten minutes in, and goes back to the package author with the probe transcripts. The
  objective is minutes per *shipped* skill, and this is where iterate/abandon builds
  spend theirs.
- **Memoize dispatched runs.** Key = hash(prompt, inputs, tier, arm, model id). An
  `iterate` round re-runs the same probes and the same without-arm on the same fixture;
  only the with-arm changed. With the key, round two costs with-arms plus graders. This
  is `idempotent-action-design` applied to `dispatch.py`; the cost row records `cached:
  true` so nobody mistakes a replay for a measurement of load.

### 9.2 Latency inside a run

- **Graders per item, in parallel.** One grader over all blinded outputs took 6.5 min;
  one grader per test item is bounded by the longest item, ~1–2 min, and the contract's
  ≥ 2 graders holds per item. The whole-artefact review needs the whole artefact, so it
  stays one run — already off the critical path in v3.
- **Warm the cache, then fan out.** All arms share a prefix (bare cwd, no library, the
  fixture path, the task). A cache entry exists only after the first response begins
  (knowledge note token-economy-playbook §2.3), so eight runs launched at once all miss;
  launch one, wait for first output, launch the rest. Cuts prefill time and 90% of the
  shared prefix's cost. Preregister: the warm run's cost row is marked `warm: true`.
- **Bare startup.** Each `claude -p` pays MCP servers, settings and hooks it never uses.
  `--strict-mcp-config` with an empty config, no settings sources, `--max-turns` per class:
  seconds per run, minutes per build at 32 runs. Measure once.
- **Effort is a knob the contract does not fix.** `never_routed_down` fixes the *tier*;
  effort is per call. Preregister one effort per job class (arms high, readers medium,
  triggers low), identical across arms and builds. Not a comparability break if declared
  before and recorded on the row.
- **The fixture sets the arm's length.** A 7-minute arm run is an agent writing Python
  over 8,000 rows. The discriminating unit change is one merchant; the run time is the
  8,000. Find the smallest fixture that still separates the arms (`stage-ablation-
  attribution` on fixture size) and the arm floor drops with it.

### 9.3 Throughput, not latency

- **N builds in flight.** The piano builds one skill at a time. With the chain runner
  (§8) the probes of package B run while A authors; the dispatch queue is shared. The
  objective for the *library* is skills per hour, and that is where the cap matters:
  `W_MAX_AGENTS = 4` was measured against CPU contention on a workload that is 73% API
  wait — re-measure at 8 with the same preregistered rule, and a Workflow (16 concurrent,
  resumable) for the nightly batch.
- **The rate limiter is the biggest single number in the ledger.** Waiting is 196 of the
  495 dispatched minutes across builds, almost all build 3's two rate limits. A token-
  bucket queue in `dispatch_many` (back off on 429, spread launches) protects what
  `W_MAX_AGENTS` cannot: it guards contention, not quota.
- **Extend builds edit the delta.** `eval-set-curation-v2` was an extend of a 161-line
  incumbent; authoring rewrote the whole. With `apply-llm-edits` the with-arm is incumbent
  + diff, the writer writes the diff, and `extend_gate.py` already holds the regression
  rule. Authoring time then scales with the change, not the artefact.
- **The scout is one index query.** `knowledge/kb.py` already indexes every SKILL.md by
  section; 1.1 is `find` over the trigger terms, not a model reading 90 descriptions.

### 9.4 What all of it adds up to (DERIVED, not measured)

With 9.1's first three levers and per-item graders: dispatched critical path probe 5
(overlapped) → arms 7.3 → graders ~2 → **≈ 14–15 minutes**; with §8's runner the
coordinator is the authoring turns alone; **20–25 minutes** for a full-evidence build,
ten to a `candidate`, and an abandon at ten instead of forty on the builds that were
never going to ship. Below that the arm run itself is the floor, and only the fixture-size
lever moves it.

The order to test them, by evidence already in hand: probe-as-without-arm and k-from-probe
(spec already says both; a contract edit and one build), fail-fast at T1 (a preregistered
stop and one refuted package), per-item graders (one build), memoized dispatch (one
iterate round), the rate-limit queue (the next build that hits one). Each is one row in
the §5 table.

## 10 · §9 checked against the contracts, and what landed (same day)

- **Fail-fast at T1: KEPT as the existing rule, not built.** The skill contract's
  `acceptance.probe_never_gates` says a gap probe never terminates a build, with the reason:
  a skill that turns 18 of 20 into 19 of 20, or leaves 20 of 20 while fixing the output
  shape, is invisible before the artefact exists. §9's "abandon at ten minutes" would have
  excluded exactly those. The keep is recorded in the chain contract's `runs_paid_twice`
  block so the question does not come back.
- **Landed:** probe rows as the without-arm's correctness repeats and k from the probe's
  outcome (`acceptance.repeats_by_probe`, `decide.rows_of` / `resolve_repeats`, cost
  clauses read paired rows only); `dispatch(memo=True)` keyed on prompt, model id, arm,
  effort and every input and method byte, `cached=true` on the row; `effort` per run on
  the command and the row; `dispatch_many(stagger_s=…)` for the cache warm-up;
  rate-limit retry with recorded count and a 30 s → 8 min backoff; graders per item and
  the `kb.py` scout in the v3 posture; `job_class_cost.py` drops cached replays. Twenty-
  two new controls (103/103 build, dispatch selftest green, 13 rule blocks accounted for).
- **Not landed:** `--strict-mcp-config` / bare-startup flags (not verified against this
  CLI's help, which lists `--mcp-config` and `--effort` only), the fixture-size ablation
  (a measurement, not code), N builds in flight and the W re-measurement (a preregistered
  bench run), delta authoring for extend builds, and everything in §8 (JSON returns,
  `run_chain.py`, the code-proposes phases). Still unmeasured: every minute in §3, §8, §9.

## 11 · The first v3 build, measured (2026-09-02 22:13 → 2026-09-03 06:34)

`llm-wiki-ingest`, existing-artifact, failure_kind shape, coordinator Fable 5.1, measurement tier
Opus 5, effort medium on every dispatched run. Verdict **iterate**: no regression on T1/T2 (where
the baseline was already clean), the T3 win (no-material handling) survived both repeats, tool
calls 1.17x, tokens **1.23x against the 1.20x cap**. Against §5:

| question | preregistered | measured | holds |
|---|---|---|---|
| wall clock open → decide | < 45 min | **26.9 min active** (17.8 + 9.1 around a 7 h 54 min session suspension; raw span 500.8 min) | yes, on active time; the raw span is reported beside it |
| coordinator turns | ≤ 8 | 14 recorded turns (5 kinds); 4 authoring | no — the harness defects cost turns (see below) |
| reader runs | ≤ 2 | **2** (description reader, whole-artefact review) | yes |
| review changed steps/description at class level | recorded | **yes** — 4 CLASS findings; one rewrite; arms re-run | fan-out A's speculation did NOT pay this time: one wasted with-arm wave (6 runs, ~1.9M tokens) |
| calibration red | recorded | n/a — grader is code, 6.3 skipped with the reason | — |
| verdict quality | same clause | passed; the token clause failed on its own | the shape did not buy speed with a worse skill |
| time to `candidate` | < 15 min | not built (parked) | — |

Dispatched: 44 runs, 41.6 run-minutes, 18.5M tokens; union of windows 18.3 min. Arms 56% of
minutes, probes 30%, the review 11%. Coordinator active turns: planning 4.0, authoring 5.8,
reading verdicts 5.0, waiting 9.7 (mostly the rerun's failed wave and its reproduction), code
check ~5 (the 467-minute figure in the ledger holds the suspension; the correction event says so).

**Three harness defects found by this build, all fixed the same night:** headless runs had no
write permission (six probe runs void); six concurrent reruns failed in 2–3 s with empty stderr
(cause not established; a stagger fixed it, and dispatch.py should keep the full stderr); and
`resolve_rule` refused the threshold prose both packages of the day preregistered
(`acceptance.equivalent_prose` now registers a phrasing with its parameter mapping). Two grader
defects the review found (a regex that passed on the wrong row; the grader shipped inside the
bundle where a with-arm could read it) were fixed and the with-arm re-run.

**What the numbers say about v3.** The shape works: 26.9 active minutes for full evidence, two
reader runs, the probe as the without-arm, k from the probe. The speculative fan-out did not pay
on this build — the review was red at class level, as the preregistered revert rule anticipated;
one such build is not the two-in-three that reverts to serial. The coordinator-turn row failed
for reasons that were harness, not shape. Next build: the same package after the token
iteration (the with-arm reads a 90-line skill on every run; the 1.23x is that reading), and a
second package of a different kind.

### 11.1 The iterate rounds, and the ship (2026-09-03 08:xx)

Three repair loops after the first verdict, all on the same package, each one rewrite + one
with-arm wave (the without and incumbent rows stood):

| round | what changed | review | with-arm tokens vs without | verdict |
|---|---|---|---|---|
| 0 | first build | red, 4 CLASS | 1.23x | iterate (tokens) |
| 1 | body halved, rationale → `references/`, dispatch mounts a method VIEW without `evals/` | red, 5 CLASS + 8 INSTANCE | **1.41x** | void (class finding) |
| 2 | rules/steps contradictions, claims table, log line content, disputed scope, generality; grader strengthened, back in the bundle | red, 5 CLASS + 6 INSTANCE | 1.40x | void (class finding) |
| 3 | every branch → step 6, no-material by the value's as-of date, cascade names the neighbour's file, step 3 bounded, guards recorded as guards; pristine hashes beside the grader | not run (3-round cap; unconverged recorded) | **1.17x** | **SHIP** — tools 1.13x, no regression, T3 win on both repeats |

Two things the rounds established. First, **the token cost was the method's work, not the
reading**: halving the body and hiding the evals (round 1) made the with-arm *more* expensive,
because the runs did more of what the skill asks (hashes, history rows, cascade sentences,
open questions). What brought it under the cap in round 3 was a text that says exactly what
to do and where, so the runs stopped improvising extra work - 7-13 tool calls against
12-18 in round 1. Second, **the whole-artefact reviewer does not converge on this artefact**:
three rounds, three different sets of class-level contradictions, each real. The convergence
rule stopped the loop at three, and the record says the last text was not reviewed whole.
That is the honest state of the shipped skill, and the first thing the curator should read.

Build totals (from the cost ledger): 8 h 48 min raw span with one overnight suspension, about
55 active minutes; 65 dispatched rows (11 void: 5 on the permission defect, 6 on the transient
failure), 28.7M tokens; four triage events, three rewrite-and-rerun rounds.

## 12 · The second v3 build, measured: artifact-consistency-sweep → ABANDON (2026-09-03 07:13 → 11:40)

Origin author, failure_kind shape, coordinator Fable 5.1, measurement tier Opus 5 at effort
high (a review is the job). Verdict **abandon** at the loop cap: recall over the known
findings rose from the baseline's 0.29–0.67 to 0.64–1.00 (CLASS recall 1.0 on T1 in every
with-run), tokens 1.12x, but no test cleared every grader check on both repeats and tool
calls came in at 1.21x against 1.20x. Against §5:

| question | preregistered | measured | holds |
|---|---|---|---|
| wall clock open → decide | < 45 min | 267 min raw, no suspension; dispatched union 65 min | **no** — three review rounds and four with-arm waves |
| coordinator turns | ≤ 8 | 12 recorded | no |
| reader runs | ≤ 2 | 2 description readers + 3 reviews | reviews are the cost, not readers |
| review class finding → rerun | recorded | **three times**; the cap stopped a fourth | the revert-to-serial condition (two in three) is met across the two builds: 5 of 6 reviews red at class level |
| verdict quality | same clause | abandon on the win clause and tool calls | the shape did not buy a verdict |

**What the build established.** (1) The whole-artefact reviewer is red at class level on
every text it sees, across two builds and six reviews; the fan-out's speculation on the review
therefore never pays and the preregistered revert-to-serial condition is met — the next
contract version puts 5.2 before 6.1 again, or replaces the reviewer with the sweep it was
trying to build. (2) The harness lost this build twice: the grader-code exclusion the triage
described was not applied until after the last wave, and the arm prompt's fixed output shape
overrode the skill's own step 6, so four of six final runs failed a check the skill could not
pass. Both are in `defects.jsonl`; neither changes the verdict, both change the next build.
(3) The method works on the measure it was built for and fails the full bar it set itself —
the honest state of a candidate, kept, not routed.

Build totals from the ledger: 42 dispatched rows, 195 run-minutes, 22.6M tokens; arms 75%
of minutes, probes 19%, reviews 5%; three repair rounds.

## 13 · The third v3 build, measured: artifact-consistency-sweep-v2 → ABANDON, unconverged at review (2026-09-03 11:45 → 12:33)

The first build under contract 3.1.0 (review before arms). Same skill, iterated from the
first build's triage and field trial; the incumbent arm was the first build's final text.

| question | preregistered (§5) | measured | holds |
|---|---|---|---|
| wall clock open → decide | < 45 min | 48 min; dispatched union 27.6 min | close — and no arm ran |
| coordinator turns | ≤ 8 | 13 rebuilt from run timestamps (4 waiting, 3 authoring, 3 reading, 2 planning, 1 code check) | no |
| reader runs | ≤ 2 | 3 description readers + 3 reviews | the cap is per review round |
| review class finding → rewrite | recorded | **three times**, 7 → 9 → 11 class findings on three successive rewrites | the cap ended the build |
| verdict quality | same clause | abandon on the review cap; no measurement clause reached | the arms never ran |

Cost: 12 runs, 6.54M tokens, 51.6 run-minutes (probes 65% of tokens, reviews 21%, readers
15%) — against 22.6M and 195 run-minutes for the first build of the same skill. That is the
saving 3.1.0 was for: the four with-arm waves the first build spent on texts that were
rewritten anyway did not happen.

**What the build established.**

1. **The baseline was under-measured by its own prompt.** With the output shape no longer
   dictated, six bare runs reached recall 0.64–1.00 (0.35–0.73 with a shape); five of six
   clear the recall bars. The gap the skill has to close is the ledger, the matrix and
   precision, not recall. The first build's threshold aimed at the wrong thing.
2. **Review-before-arms works as a cost control and exposes a convergence problem.** Nine
   of nine v3 whole-artefact reviews across three builds have been red at class level. Each
   rewrite removed the previous set and the next review found a new one of comparable size.
   Either the reviewer's bar is unreachable in three rounds for a text of this kind, or the
   rewrite loop needs the sweep itself (the candidate) run on the text before the reviewer
   sees it. Both are testable; neither was tested here.
3. **Contract 3.1.1** encodes the cap: `modes.v3.max_reviews = 3`, `decide.py` returns
   abandon "unconverged at review" when the reviews stayed red and no arm ran, and the
   fan-out gate no longer flags a red review that no arm followed. 108/108 controls.
4. **Coordinator defects, two.** A rewrite script asserted the description length and wrote
   nothing while the review it dispatched ran on the old text (caught in two minutes, runs
   killed, logged as a 5.1 correction). Coordinator turns were estimated during the build
   and three had negative durations; the ledger was rebuilt from run timestamps and the
   estimated rows kept beside it. Rule from it: derive turns from run windows, never estimate.

The candidate stays kept, not routed; the r2 findings are its open set, verbatim in its
`evals.md`.

## 14 · The fourth v3 build, measured: artifact-consistency-sweep-v3 → ABANDON, unconverged at review, again (2026-09-03 12:25 → 18:35, with a 5-hour suspension)

Same skill, third build, under contract 3.1.1, with one new move: a **self-sweep** — the
candidate run on its own bundle with the build's BOM — before each reviewer round, to test
the reading from §13 that the loop needs the sweep before the reviewer sees the text.

| question | preregistered (§5) | measured | holds |
|---|---|---|---|
| wall clock open → decide | < 45 min | about 56 active minutes (span 5 h 47 min with the suspension); dispatched union 46 min | no, by the two self-sweeps (11 min each) |
| coordinator turns | ≤ 8 | 15 | no |
| reader runs | ≤ 2 | 3 readers + 3 reviews + 2 self-sweeps (+1 errored) | the cap is per round |
| review class finding → rewrite | recorded | three times: 5, 5, 6 class findings | the cap ended the build |
| verdict quality | same clause | abandon on the review cap | no arm ran |

Cost: 9 dispatched runs (one died with no output, tokens null), 4.89M tokens, 48.8
run-minutes; probes carried over from the second build and re-graded, so no probe cost.

**What the build established.**

1. **The self-sweep works as a filter and not as a cure.** It produced a complete ledger
   (242 of 242 planned pairs on its second run), 15 and 12 findings of which 11 and 11 were
   class-level, and every one of them was a real text defect. The reviewer's class findings
   per round then fell to 5, 5, 6 from the second build's 7, 9, 11. It did not reach green:
   twelve of twelve v3 reviews across four builds are red at class level.
2. **The recurring class findings are structural, not textual.** Three of the last review's
   six: the eval set is three versions of one skill, so two of the seven pair types and one
   branch of the method have no fixture; the incomplete-report branch is blessed by a rule
   and failed by a strict expectation; a step's obligation is answered by two rows with two
   vocabularies. Rewriting sentences does not remove these; new fixtures and one design
   decision do. That is the next iteration's first work, written in the skill's `evals.md`.
3. **Grader defects the self-sweep exposed.** Its output was the first ledger-carrying report
   the grader ever graded: `json.dumps` had escaped × to `\u00d7` so two of the seven pair
   types never matched, and pair ids were counted one level deep while reports nest them.
   Both were fixed before any arm could have run. A grader written against outputs that do
   not exist yet is a hypothesis; the first real output tests it.
4. **Coordinator defects, three, all recorded.** A dispatch ran on an unwritten text for the
   second time in two builds (a failed assertion in the rewrite script, the dispatch in the
   same command); it is now chained on the script's exit code. `decide.py` was called before
   its own 8.1 event and returned undecidable from the chain gate, correctly; the row it
   wrote is superseded by the next. A run died with no output and no stderr (the transient
   failure from the first build) and was re-run.

The candidate stays kept, not routed. Four builds, one skill: 22.6M + 6.5M + 4.9M tokens
(the first build's arms were 75% of its cost; the later builds spent nothing on arms). The
open question §13 posed is answered in one direction: the self-sweep lowers the count and
does not close the loop; the other reading — the reviewer's bar is unreachable in three
rounds for a reflexive text — is not refuted.

## 15 · Chain 4.0.0 and the first candidate build, measured (2026-09-03 19:04 → 19:22)

**The change.** Two modes replace v3. *Candidate*: fill from the package, code check, one probe
wave (k=1, two tasks) in parallel with authoring, one reader/review round, one rewrite, verdict
`candidate`; the artefact lives in `.claude/skills-candidates/`, which the loader never reads.
*Promote*: probes (reusable), arms with ×1 and without ×1, graders, triggers, decide, deploy by
moving the directory. The reviewer is a critic (calibration: red on 3 of 3 adopted skills, 15 of
15 reviews); the code check and the measurement decide. The package budget is enforced in
`dispatch`; a run that dies with no output is retried once; coordinator turns are derived from
the run windows; `decide` writes its own event; every dispatching phase is one script
(`run_phase.py`). 116/116 build controls, 36/36 package, dispatch and chain suites green.

**First candidate build** (artifact-consistency-sweep-v4, the third build's text plus fixtures D
and E):

| question | target (4.0.0 estimate) | measured |
|---|---|---|
| wall clock open → close | 10–15 min | 17.7 min, of which ~3 min a script crash after the runs had finished |
| dispatched runs | 4 | 4 (2 probes, reader, review), 7.7 min run windows |
| tokens | < 2M | 1.58M |
| coordinator turns | few | 2 derived (10.0 min coordinator, 7.7 waiting); nothing typed in |
| verdict | candidate | candidate: code check 0 errors after one rewrite; review red (7 CLASS) read once, fixed once |

Against the four earlier builds of the same skill (22.6M, 6.5M, 4.9M tokens; 267, 48, 56 active
minutes) the candidate path is one tenth of the cheapest and measures nothing - by design. The
measurement is now a separate, budgeted decision.

**Two defects on the first run.** `run_phase.py review` crashed while logging (no `phase` key
on the dispatch result); the runs were complete, the events were logged from their outputs, the
script gained `--log-only`. The rewrite went through two code-check rounds (a pointer at a file
the bundle lacks; nested SKILL.md rows in the BOM). Both cost coordinator minutes, not runs.
