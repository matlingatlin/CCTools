# skill-builder — specification

The agent that turns an admitted idea into a tested skill. Written 2026-08-30.

**Authority: Anthropic.** They own the runtime the skills execute in. Where Anthropic
states a rule it binds; where Anthropic states advice it is the default and a
measurement may override it with the reason recorded; where Anthropic says nothing
we decide and mark it `house`. Every field rule lives in
`pipeline/contracts/skill.contract.json` — **the one source, read by both the code
validator and this agent.** Nothing here restates a rule from there.

Evidence behind the contract: `knowledge/notes/anthropic-skill-authoring-contract.md`.

---

## 1 · The package — what arrives

The upstream evaluator has already ruled `go` and already decided this is a skill.
The package carries **inputs, never outputs**: no field of the finished skill arrives
pre-written.

**Why not pre-written.** The line is not "formatted versus raw". It is:

> The package carries what a run cannot produce. The builder writes what only a run
> can settle.

`description` needs the finished body's scope and a sibling scan. The steps need
*observed* failures, and observation is a run. Assertions are written after the first
outputs are seen. Written upstream, none of these can be checked against the skill
that actually got built.

```jsonc
{
  "id": "...",                    // one id; every downstream artefact shares it

  "candidate_sentence": "...",    // ONE sentence: what it does AND what it emits.
                                  // This is the scope. A topic is not a scope.

  "unit_type": "skill",
  "content_kind": "reference|task",   // Anthropic's taxonomy → invocation policy
  "verifiable": true,                 // objectively verifiable output? → are evals authored
  "failure_kind": "knowledge|shape|discipline",   // → which test form applies

  "sources": [
    { "source_id": "S1", "url": "...", "type": "paper|docs|repo|page",
      "title": "...", "authors": "...", "year": 2026,
      "fetched": "YYYY-MM-DD", "access": "open|paywalled|local", "read": "full|partial" }
  ],

  "claims": [                     // rows, never prose — prose cannot be verified
    { "claim": "...", "source_id": "S1", "locator": "§4.2, Table 3",
      "quote": "...",             // VERBATIM. No quote → not MEASURED.
      "what_was_measured": "...", "effect_size": "...", "sample": "...",
      "limits": "...",            // what the source itself says it does not establish
      "verdict": "MEASURED|REPEATED",
      "verified_by": "path or null" }
  ],

  "expected_failure": "...",      // HYPOTHESIS: what Claude gets wrong today without this
  "trigger_terms": ["..."],       // the words a user types. From the source, not invented.
  "representative_tasks": [       // 2–3 realistic tasks. Used by the probe AND the evals.
    { "task": "...", "artifact_expected": "..." }
  ],

  "budget":    { "max_agents": 2, "max_paired_runs": 20 },
  "threshold": "..."              // the decision rule, written BEFORE any measurement
}
```

**Each field exists because a step would otherwise improvise:**

| Field | The step that improvises without it |
|---|---|
| `candidate_sentence` | all of them |
| `claims[].quote` | the reference file — a finding becomes indistinguishable from a memory |
| `expected_failure` | the gap probe has no hypothesis to test |
| `trigger_terms` | `description`, written from imagination |
| `representative_tasks` | the probe **and** the evals; invented tasks flatter |
| `content_kind` | frontmatter policy, and whether evals are authored at all |
| `failure_kind` | which test form applies — and whether we can test it at all |
| `threshold` | the verdict. Written afterwards, the result moves the bar. |

**`failure_kind: discipline` is refused at admission.** Two preregistered rounds in
this repo found no scenario class that discriminates (technique traps 1 of 12,
pressure 2 of 12). Until one exists, a discipline skill cannot be shown to work, and
shipping one on a green suite would be shipping an unmeasured claim.

---

## 2 · The chain

**[K]** code · **[M]** the builder's own model · **[X]** external agent — cannot see
how the thing was produced · **[D]** dispatch

External means one thing precisely: *it cannot see the reasoning that produced what
it judges.* A model critiquing its own output with no external signal measures worse
on every model and every benchmark tested.

### Phase 0 · Arrival

| # | Function | Out | | v |
|---|---|---|---|---|
| 0.1 | `admit_package` | pass, or a rejection naming the missing field | **[K]** | 1 |

**Built:** `pipeline/validate/package_contract.py` against `pipeline/contracts/package.contract.json` — 26 code rules, 6 agent checks. Two gates run before any package is judged: the engine aborts if the contract declares a `check: code` rule it does not implement, and `selftest_package.py` aborts if a declared rule has no positive control. Exit 0 admitted · 1 refused · 2 the contract and the engine disagree.

| 0.2 | `open_build_record` | the build record; everything downstream appends here | **[K]** | 1 |

Refuses: no `candidate_sentence` · claims without `quote` · no
`representative_tasks` · no `expected_failure` · no `threshold` ·
`failure_kind: discipline`.

### Phase 1 · Orientation

| # | Function | Out | | v |
|---|---|---|---|---|
| 1.1 | `scout_library` | `reuse` / `extend` / `author` **+ the queries run** | **[M]** | 1 |
| 1.2 | `read_siblings` | adjacent skills' descriptions, held for 4.7 | **[K][M]** | 1 |

`reuse` stops the build. `extend` is a different job — the existing skill's evals must
still pass afterwards (**v2**).

### Phase 2 · Observation

The hypothesis meets reality. Nothing is written before this.

| # | Function | Out | | v |
|---|---|---|---|---|
| 2.1 | `probe_gap` | N runs of `representative_tasks` **without** the skill, fresh sessions | **[D]** | 1 |
| 2.2 | `code_failures` | failure list: what they did (quoted), the consequence, did all runs do it | **[M]** | 1 |
| 2.3 | `gap_verdict` | what the skill must prove — see below | **[K]** | 1 |
| 2.4 | `write_eval_prompts` | `evals/evals.json` — **prompts only, no expectations** | **[M]** | 1 |
| 2.5 | `write_eval_fixtures` | `evals/files/*` — the inputs the prompts reference | **[M]** | 1 |

**A passing baseline does not stop the build. It raises the bar.**

| Probe shows | What the skill must prove | Runs |
|---|---|---|
| baseline **fails** | it fixes the observed failure | 1 suffices |
| baseline passes **unevenly** | it makes the outcome consistent | ≥2, or variance is invisible |
| baseline passes **cleanly** | it wins on a **named** axis — tool calls, tokens, completeness, shape — **and does not regress** | ≥2 |

The third row is where the danger lives: ~15% of tasks measurably *regress* under a
skill, concentrated exactly where the base model was already competent. So the clean
cases are not neutral, and one run cannot tell a tie from a small regression.

### Phase 3 · Knowledge

Runs only when the package's seed does not cover the observed gap. **Upstream fetched
what made the idea worth building; the builder fetches what the observed gap shows is
missing.** The second question cannot be asked before the probe.

| # | Function | Out | | v |
|---|---|---|---|---|
| 3.1 | `coverage_check` | per observed failure: covered by `claims` or not | **[M]** | 1 |
| 3.2 | `ask` | a bounded question list **+ an out-of-scope list with reasons** | **[M]** | 2 |
| 3.3 | `gather` | claim rows from primary sources | **[D]** | 2 |
| 3.4 | `verify_claims` | per row: supported / not-supported / not-in-source / source-unreachable / not-checkable | **[X]** | 2 |
| 3.5 | `reconcile` | one claim set: duplicates merged, **contradictions kept as their own rows**, sorted by verdict | **[M]** | 2 |

Skipped when 3.1 says covered — **and the skip is logged**. 3.4 is external because
whoever gathered may not rule on their own gathering.

### Phase 4 · Writing

Each field: write → **[K]** → **[X]**. A red field never proceeds. Code first — there
is no point asking a model whether a 1,400-character description is well phrased.

| # | Field | | v |
|---|---|---|---|
| 4.0 | `plan_bundle` — the bill of materials. One row per planned file: kind, why it is needed, `exists` / `needed` / `not needed because…`. **No row may be blank.** | **[M]** | 1 |
| 4.1 | `references/*` | **[M]** | 2 |
| 4.2 | `assets/*` | **[M]** | 2 |
| 4.3 | `name` | **[M]** | 1 |
| 4.4 | body Q1 + Q2 | **[M]** | 1 |
| 4.5 | body Q3 steps | **[M]** | 1 |
| 4.6 | pointers | **[M]** | 1 |
| 4.7 | `description` | **[M]** | 1 |
| 4.8 | frontmatter policy | **[M]** | 1 |

The rules and the per-field agent question are in the contract file.

**4.7 is last** — it needs the finished body's scope, the trigger terms, and 1.2's
sibling scan. **4.5 may use only observed failures** — a rule with no row behind it is
an opinion. **Nothing proceeds from 4.0 with an unclassified row**: a gap found there
is a task; the same gap found mid-writing is an improvisation.

### Phase 5 · The whole

Section checks cannot see contradictions *between* fields.

| # | Function | | v |
|---|---|---|---|
| 5.1 | `validate_artifact` — cross-field mechanical, incl. the bill of materials in **both** directions | **[K]** | 1 |
| 5.2 | `review_artifact` — the questions that need the whole artefact | **[X]** | 1 |

### Phase 6 · Measurement

| # | Function | | v |
|---|---|---|---|
| 6.1 | `run_paired` — with and without, **same turn**, fresh sessions, + timing and tool counts | **[D]** | 1 |
| 6.2 | `write_expectations` — from the observed outputs, not before | **[M]** | 1 |
| 6.3 | `calibrate_judge` — hand the grader a specimen carrying **one planted defect**, without saying so | **[D]** | 2 |
| 6.4 | `grade` — pass/fail per expectation **with evidence**, plus a critique of the expectations | **[X]** | 1 |
| 6.5 | `test_triggers` — 20 queries, 8–10 positive, 8–10 near-miss negatives | **[D]** | 2 |

**6.3 before 6.4.** A grader reporting "no findings" has said one of two things and
you cannot tell which: the skill is clean, or the grader is blind. A grader that
misses its own planted class is not reporting on the skill you pointed it at.

**For `failure_kind: shape` the grader is code, not an agent** — count the columns,
check every row carries its locator, check the verdict is not buried. Cheapest
category to measure, and the only one whose judge cannot be blind.

**Every [D] goes through `pipeline/build/dispatch.py`** (chain contract 2.0.0, `dispatch`).
Until 2026-09-02 each build dispatched from shell written that day, and build 3 lost a
full wave of arm runs to three faults that shell made easy: a working directory shared
between runs, the arm's name in the run's path, the method mounted for every arm. The
module makes each inexpressible - fresh hashed directory per run, `method_dir` refused for
any arm but `with`, inputs copied in - and writes tokens, tier and window to the cost row
on every run, which no ad hoc script ever did.

### Phase 7 · Feedback

| # | Function | Triggered by | Goes to | | v |
|---|---|---|---|---|---|
| 7.1 | `extract_scripts` | did every run write the same helper? | **→ 4.5, 4.6** | **[M]** | 2 |
| 7.1b | `write_script` | 7.1 found one | | **[M]** | 2 |
| 7.1c | `audit_script` | a bundled script is executable code that ships | | **[X]** | 2 |
| 7.2 | `triage_failure` | 6.4 or 6.5 red | **→ 4.x** skill-bug · **→ 2.4** test-bug | **[M]** | 1 |

**7.2 is not optional.** Without it the skill is always repaired, even when the test
was wrong.

### Phase 8 · Verdict

| # | Function | | v |
|---|---|---|---|
| 8.1 | `decide` — the delta against the package's `threshold` | **[K]** | 1 |
| 8.2 | `emit` — the skill, its evals, and the build record | **[K]** | 1 |

The build record carries: which claims were used, which were dropped and why, what
the probe showed, whether phase 3 ran or was skipped, the measurement, the grader's
calibration, and **what was not checked**.

### Phase 9 · Deploy

| # | Function | | v |
|---|---|---|---|
| 9.1 | `deploy` — capability map, routing, commit, **reload**, deploy event in the ledger | **[K]** | 1 |

---

## 3 · The chain in one view

```
package
 └─0.1 admit ── 0.2 record
     └─1.1 scout ── 1.2 siblings
         └─2.1 probe ── 2.2 code ── 2.3 verdict ── 2.4 prompts ── 2.5 fixtures
             └─3.1 coverage ──┬── covered → skip phase 3 (logged)
                              └─3.2 ask ─ 3.3 gather ─ 3.4 verify[X] ─ 3.5 reconcile
                 └─4.0 bill of materials
                     └─4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → 4.7 → 4.8
                        [K] then [X] after each
                         └─5.1 validate ── 5.2 review[X]
                             └─6.1 paired ─ 6.2 expectations ─ 6.3 calibrate ─ 6.4 grade[X] ─ 6.5 triggers
                                 ├─7.1 scripts ─ 7.1b write ─ 7.1c audit[X] ──▶ back to 4.5
                                 ├─7.2 triage ────────────────▶ 4.x or 2.4
                                 └─8.1 decide ── 8.2 emit ── 9.1 deploy
```

---

## 4 · The agent's shape

34 functions, but functions are not skills. The cap is three preloaded skills.

| | Contents |
|---|---|
| **skill 1 · `skill-contract`** | 4.0–4.8 — what each field requires and how it is written. Reads the contract file. |
| **skill 2 · `skill-knowledge`** | 3.1–3.5 — what is missing, where it is fetched, how sources are reconciled |
| **skill 3 · `skill-measure`** | 2.1–2.5, 6.1–6.5, 8.1 — how you see that it works |
| **scripts** | `admit_package`, `validate_artifact` — zero context, cannot be argued past |
| **external agents** | `verify_claims`, `review_artifact`, `grade`, `audit_script` |

**Two modes** (chain contract 2.0.0, `modes`). `full` is the chain above and the only
mode that can ship. `fast` - opened with `record.py open --mode fast` - skips the probe,
phase 3, calibration, scripts and deploy at open (each with a skip event naming the mode),
writes the fields with the code checker only and reads the artefact once, whole, at 5.2,
runs the with-arm only, and grades with one grader. Its ceiling is `fast_pass`: passed its
own checks and tests, beat nothing. `decide.py` never returns ship for it. The full chain's
dispatch floor is 28.3 minutes at infinite agents; fast is DERIVED at 25-30 minutes and
unmeasured until the first fast build replaces that line in the contract.

External cost per skill: **6 light field checks** (single-shot, field + contract only)
**+ 3 heavy** (review, calibrate, grade) **+ 1 per source** (claim verification). At
`W_MAX_AGENTS = 4` (raised from 2 on 2026-09-01, measured) this is the dominant cost of the chain — and it is there because
every one of those points is a place the builder would otherwise grade its own work.

---

## 5 · Acceptance

The rule is preregistered per build in the package. The default shape and its staging
are in the contract file under `acceptance`. In outline:

> Across k ≥ 2 repeats: **zero regressions on correctness**, no more than 20% worse on
> tokens or tool calls, and **at least one test where the skill wins with the win
> surviving the repeat**.

Staged: 3–5 tests × 2 arms × 2 repeats always; expand to 20 tests only when stage 1 is
borderline. Anthropic: *"Start with 2-3 test cases. Don't over-invest before you've
seen your first round of results."*

---

## 6 · Build order

| | What | Why first |
|---|---|---|
| **1** | `validate_artifact` (the code checker) | pure code, no open questions, and **testable against the 84 skills we already have**. **Done:** `pipeline/validate/skill_contract.py`. |
| **2** | Run it over our 84 **and over Anthropic's own 38** | a *negative corpus*, not a positive control. Their skills failing does not by itself convict the contract — the 84 predate the documentation, and Anthropic may be sloppy in their own repos too. A gap between the two rates only says **look here**, and the disposition is then rule by rule against the documentation: the contract misread the source · the source disagrees with their practice · the rule is stricter than the source. Only the first means the contract is wrong. **Done:** 3 rules overturned, 2 demoted from error to warn. |
| **3** | `admit_package` | the package schema as a validator. Also pure code. **Done:** `pipeline/contracts/package.contract.json` + `pipeline/validate/package_contract.py`, 28 positive controls in `selftest_package.py`. |
| **4** | The v1 chain — phases 0, 1, 2, 4 (writers), 5, 6.1/6.2/6.4, 7.2, 8, 9 | the narrow path, end to end. **Built:** `pipeline/build/record.py` (0.2, the append-only spine) + `pipeline/build/decide.py` (8.1) with 28 controls; the three methods and the agent staged in `pipeline/skills/` and `pipeline/agents/`. **Not yet run:** the paired evals that would let them ship. |
| **5** | v2 — phase 3 (knowledge), 6.3, 6.5, 7.1 (scripts), the `extend` branch | added once the narrow path carries |

**Why v1/v2 and not all 34 at once.** This repo's own ablation of a three-skill
preload measured **null**. Building 34 functions and assuming they earn their place
would be the same error at larger scale. The v1 path is the smallest thing that can
produce a tested skill; each v2 function is added when the data says the v1 path
needs it.

---

## 7 · Data — captured live, because it cannot be reconstructed

Timing and token counts are gone the moment the run notification passes. Anthropic
says the same of their own `timing.json`: *"This is the only opportunity to capture
this data."*

**A measured zero is not the same as not-measured.** `null` for not-measured, `0` for
a measured zero, always — a truthiness test once filed the fastest possible detection
in the worst bucket.

| Phase | Row | The question it opens |
|---|---|---|
| 0 | source type · claim count · verified share · was a threshold set | which source type yields skills that survive |
| 2 | **per task:** baseline pass/fail/uneven · n runs · tool calls · tokens | **does the probe predict the outcome** |
| 3 | fetch run or skipped · questions · sources reached/unreachable · claims per verdict | what share of fetched claims survives verification |
| 4 | **per field:** red code checks · red agent checks · which rule failed | **which contract field costs the most rework** |
| 6 | with/without: pass rate, tool calls, tokens, duration · per expectation · **did the grader catch its planted defect** · the trigger matrix | the delta distribution; how often is the grader blind |
| 7 | triage verdict test-bug/skill-bug · loops to green | **is the builder getting better** |
| 8 | ship / iterate / abandon + reason | the abandon rate and its shapes |

Existing ledgers take most of it: `talents.jsonl`, `evals.jsonl` (one row per
scenario), `rejections.jsonl`, `claims.jsonl`, `defects.jsonl`. **Two are new:**
`builds.jsonl` (one row per build) and `fields.jsonl` (one row per field per build).

`fields.jsonl` is what makes the builder measurable on itself. Without it we learn
only that a skill came out good or bad; with it we learn **where in the chain** it
did.

---

## 8 · What Anthropic does not settle, and what we chose

| Question | Anthropic | Ours |
|---|---|---|
| Body structure | *"There are no format restrictions."* One template (guide p.12), followed by none of their own skills | Not enforced. The contract governs what must be **answerable**, not which headings appear |
| Body length | four unreconciled values | 500 lines and 5,000 words enforced as **warnings**, not errors — every carrier hedges, and skill-creator says feel free to go longer if needed. Demoted 2026-08-30; conflict recorded |
| Two skills claiming one job | one example of a negative trigger naming a sibling | the sibling scan at 1.2 and the `description` agent check |
| Pass threshold | *"aspirational targets… an element of vibes-based assessment"* | preregistered per build; default in the contract |
| Who writes the expectations | the author, circularity never named | the builder writes them; the **grader critiques them** |
| Independent running | required, with the reason stated | adopted unchanged |
| Stale bundled knowledge | nothing | every source dated, every row carries an expiry condition |
| Skill types | two taxonomies, neither is technique/reference/workflow | `failure_kind` decides the test form; `discipline` is refused |

---

## 9 · v3 — the same evidence in a different order (chain contract 3.0.0, 2026-09-02)

The clean build measured 79.4 minutes with 72 of them the coordinator's own turns and 16
reader runs on one skill (`pipeline/queries/job_class_cost.py`). v3 keeps every phase, every
arm, the blinding, the calibrated grader and the preregistered threshold, and changes the
order: probes dispatched at open; one authoring turn for 4.1–4.8 with the code checker in a
loop and no per-field reader; fan-out A = description reader ∥ whole-artefact review ∥ arms;
fan-out B = calibration ∥ graders ∥ triggers. Two revert rules (`fanout` block) are audited
by `record.fanout_gate()`: a class-level review finding must be followed by a `rerun=true`
arm wave, a `caught=false` calibration by a `fresh_grader=true` grade; otherwise
`decide.py` returns undecidable. The coordinator's tier is recorded at open. `full` is kept
as the previous shape so both can run on the same package. Derived floor 19 dispatched
minutes, 35–40 total — unmeasured; the numbers the first v3 build must meet are in
`pipeline/REVIEW-2026-09-02-skill-builder-rethink.md` §5. Parked: the `candidate` status
(rethink §4), because this contract's frontmatter and bill-of-materials rules leave it no
home yet.

