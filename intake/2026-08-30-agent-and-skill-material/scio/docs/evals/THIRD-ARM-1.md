# Third arm · what the mining added over our own analysis

**Date:** 2026-08-26. Four skills: `validation-evidence`, `spend-ceilings`, `build-loop-stops`,
`playbook-admission`.

Twenty-six two-arm ablations were run today — *skill* against *no skill*. Eighteen changed an
outcome. None of them can answer the question this file exists for:

> **Did reading eight external repositories add anything, over what we already knew from
> analysing our own predecessor system?**

Several winning skills mix two origins. A two-arm test shows only that the mixture beats nothing.
So: three arms, the same question each ablation already used.

| Arm | Directory | What loads |
|---|---|---|
| **A · control** | `…/scratchpad/baseline` | `CLAUDE.md` + `docs/as-built/`, no project skills |
| **B · ours-only** | `…/scratchpad/oursonly-1` | same, plus all 27 skills — with the four under test **stripped of every mined rule** |
| **C · full** | `/home/user/scio` | the skills as written, in the live repo |

---

## Method, and how origin was decided

### The arms, verified

`baseline/` and `oursonly-1/` carry a byte-identical `CLAUDE.md` and a byte-identical
`docs/as-built/` (15 files + the graph directory), checked with `diff` before any run. `oursonly-1/`
additionally carries all 27 skills; before stripping, `diff -rq` against
`/home/user/scio/.claude/skills/<name>` reported **identical** for all four skills under test. The
other 23 skills were left untouched in both directions.

Nothing under `/home/user/scio/.claude/skills/` was modified. All stripping happened inside
`oursonly-1`. Nothing was committed or pushed.

### How a rule's origin was decided

By evidence, in this order:

1. **The skill's own `## 1 · Source` section**, which names a file and often a line in
   `docs/mined/` or in `docs/as-built/` / `docs/next/`. These skills are unusually well cited; most
   rules declare their own origin.
2. **A grep of the rule's distinctive phrase** across `docs/mined/` versus `docs/as-built/` and
   `docs/next/`. Present only in `docs/mined/` ⇒ **mined, removed**. Present in `as-built/` or
   `next/` ⇒ **ours, kept**.
3. **`docs/triage/`** was treated as a mapping document, not as an origin: its rows carry a
   `Where it was read` column pointing at `docs/mined/`, and where they do, the row is mined.
   Triage row BC-8, for example, names `OTHERS-MINED.md:751` as *"the new skill's founding
   sentence"* for `validation-evidence` — that is the mining declaring authorship of the rule.
4. **Both, independently** ⇒ kept, and flagged. Two cases arose and both are recorded below.

A rule was **not** treated as ours merely because the skill applies it to our code. Most mined
rules in these four skills are stated abstractly and then instantiated against
`/home/user/hello-world`. The instantiation is ours; the rule is not. Where the *observation* about
our system survives without the imported rule, the observation was kept and the rule removed —
and where it does not (the elision marker is the clean case: *"Scio has two signature views and
neither marks anything"* has no content without repomix's rule), the whole block went.

### Coherence

Stripped files were re-read end to end. Headings whose entire body was mined were deleted with the
body; section cross-references (`§2.3`, `→ references/…`) were repointed or removed; eval tables
were pruned to the cases whose rule survived. No stripped file refers to a section it no longer
contains.

### Confounds, stated before any result

- **`graphify` loads at account level in all three arms.** So does `session-start-hook`. No arm is
  skill-free.
- **Arm C runs in the live repo.** It sees `docs/next/`, `docs/mined/`, `docs/triage/`,
  `docs/decisions/`, `graphify-out/`, `scio.db` and `hooks/`. Arms A and B see only `CLAUDE.md` and
  `docs/as-built/`. **This confound favours C in a way that has nothing to do with the mining** —
  and it cuts both ways for interpretation: a C-only mechanism may have come from the mined skill
  text *or* from `docs/next/` being on disk.
- **Much of the "ours" content in these skills is `docs/next/`, which neither A nor B carries as a
  document.** So arm B's kept rules are not redundant with arm A's docs — the stripped skill is
  the only carrier of those findings in arm B. `docs/as-built/`, which both A and B carry, does
  already state some of them.
- n=1 per arm per skill, unblinded. I chose the strip and graded the answers.

---

## `validation-evidence` — what was stripped, verbatim

**Result of the strip:** 254 lines → 152. Four of the skill's six rules removed outright.

### Kept, and why

| Kept | Evidence it is ours |
|---|---|
| Eleven Layer B rule identifiers / nine Layer C; identifiers are the keying unit; the seven-vs-nine correction | `docs/as-built/LAYER-B-UNDERSTANDING.md` §4; `docs/next/LAYER-C-BUILD-PLAN.md` §1.1 |
| `validate_architecture` records the finding and nothing about what it walked; `_check_something_to_build` exists | `layerb/validate.py`; as-built §4 lists the rule as *"an architecture that is empty"* |
| **Nobody looked ≠ it passed** — `unjudged` as a first-class value, `passed / needs_look / failed / blocked` | `docs/as-built/LAYER-E-BUILD.md` §4 (`loop.py:696`, `typecheck.py:64`, two named tests); `ARCHITECTURE-AS-BUILT.md` §2 |
| `scripts.py`'s refusal discipline → `Observability.unsupported`; unsupported criteria kept, never deleted | `docs/as-built/LAYER-C-BUILD-PLAN.md` §6 |
| Nothing renders the Layer C → Layer E join; `produced_by` × `observed_by` | `layerc/criteria.py:67`; `docs/as-built/LAYER-C-BUILD-PLAN.md` §6 |
| **8 of 27 criteria unsupported, zero observed by interaction** | `docs/next/LAYER-C-BUILD-PLAN.md` §1.1; re-confirmed at `docs/next/LAYER-E-BUILD.md` §1.1b |
| Layer C's nine rules run and **nothing reads the result** | `docs/as-built/LAYER-C-BUILD-PLAN.md` §6 (*"Validation is a report, nothing consumes it"*); `docs/next/…` §3.1 |
| Deterministic in-process validation costs memory, not tokens | reading of `layerb/`, `layerc/` |

### Removed — mined

**1 · The founding quote and its framing.** `docs/mined/OTHERS-MINED.md` §2.3 / `:751`
(superpowers `subagent-driven-development`). Our own `docs/triage/LAYER-BC-TRIAGE.md` row 8 names
this source and calls it *"the new skill's founding sentence"*.

> **An empty list is the same object whether nothing was wrong or nothing was checked.** That is the
> subject of this skill, and it is why the mined corpus's best single sentence is a sentence about
> tables:
>
> > *"The scan's output is a table, not a verdict. One row for every pair … 'The scan is clean'
> > without those rows is not a scan you ran."*
> > — `docs/mined/OTHERS-MINED.md` §2.3, verdicted *"best single sentence in the eight repos"*

**2 · The whole `## 1 · Source` block except the last paragraph** — seven citations, six of them to
`docs/mined/`:

> **The evidence table.** superpowers `subagent-driven-development`, read and verdicted in
> `docs/mined/OTHERS-MINED.md` §2.3 and row 32 (`:751`), 2026-08-26.
>
> **Exit 0 is not evidence.** `docs/mined/PASS2-GSTACK-TESTS.md` §2.1 — three test files and one
> observed number: **only ~16 of 434 files ran, shell exit 0.** 96% of a suite skipped, green. The
> companion file *"proves the truncated run is indistinguishable from a green one by exit code
> alone."*
>
> **Empty is not failed.** gstack `spec` 1b, `docs/mined/OTHERS-MINED.md:734` — *"'no envelope' ≠
> 'zero results': a failed pipeline is not an empty one."* The same rule arrived at independently in
> task-master (`docs/mined/PASS2-FOUR-REPOS.md` §1.4): *a delta that changes nothing returns a
> distinguishable no-op, not an empty regeneration.*
>
> **Claimed limitations need evidence.** gstack preamble, `docs/mined/OTHERS-MINED.md:733`.
>
> **The evidence report shape.** ECC's TDD Evidence Report, `docs/mined/ECC-SKILLS.md:669`.
>
> **The elision marker.** repomix `parseFile.ts:36, :108, :180-213`, read in
> `docs/mined/PASS2-FOUR-REPOS.md` §4.2 and row P2-28 (`:653`).

**3 · §2.1's evidence-table rule** — the table shape, and the teeth. Mined, per source note 1 above.

> A checker's output is a **table**: one row per thing it looked at, carrying what it compared
> against what, and what it found. The verdict is *derived from* the table; it is not the output.
>
> … A model required to emit one row per interface pair **cannot**. The table is what converts a
> claim into work that either happened or visibly did not
>
> The addition is a shape, not an algorithm: alongside `violations`, a
> `checked: list[Checked{rule, subject, compared_against, outcome}]`, and —
>
> > **no rows for a rule that declares itself applicable is a failure, not a pass.**

**4 · §2.2 in full — the planned count.** `docs/mined/PASS2-GSTACK-TESTS.md` §2.1. This is the
mechanism the parent brief names as the mined half of this skill, and it is the whole section.

> ### 2.2 Three numbers, and one of them must be a plan
>
> `.claude/skills/testing` §3 Q3 already requires **ran / passed / skipped**, parsed from a
> machine-readable report rather than a human summary. The mined finding adds the number those three
> cannot supply:
>
> > A gate must know **how many units it planned to run**. Without a plan count, *"invisible
> > non-execution"* is undetectable.
>
> The reference implementation refuses a zero exit when (1) failure lines were printed, (2) **fewer
> units ran than were planned**, or (3) an unhandled error fired between units — and it keeps
> **per-origin buffers** for stdout and stderr, because a shared buffer shears a `(fail)` line into
> fragments that go uncounted, *"defeating the exit-0-with-failures backstop."*
>
> **Declared lanes, executed-unit count against a planned count, no failure lines. All three.** This
> is the parsing half of the same idea as §2.1: a count of subjects, known in advance, is the cheapest
> possible evidence table.

**5 · §2.3's three-way typing table.** gstack `spec` 1b (`OTHERS-MINED.md:734`) and task-master
(`PASS2-FOUR-REPOS.md` §1.4). Our own `docs/triage/LAYER-DFG-TRIAGE.md` row D9 books the same rule
to `OTHERS-MINED.md:729`. Not in `as-built/` or `next/`.

> Three outcomes that must be distinguishable **in the return type**, never collapsed:
>
> | Outcome | Means | Never rendered as |
> |---|---|---|
> | **a result with zero items** | the check ran and found nothing | a failure |
> | **no result** | the check did not run, could not run, or produced nothing parseable | zero items |
> | **an error** | the check ran and broke | either of the above |
>
> `null` versus `[]` is the whole mechanism and it is free. Two independent repos in the mined corpus
> state it: *"'no envelope' ≠ 'zero results'"*, and *a delta that changes nothing is a no-op with a
> distinguishable return.*

**6 · §2.4 in full — a claimed limitation carries its evidence.** gstack preamble,
`OTHERS-MINED.md:733`.

> When a check reports that it *could not* do something, one of three things is attached or the claim
> is an assertion wearing a result's clothes:
>
> 1. the **verbatim error**, quoted;
> 2. a **documented statement** that the thing is impossible, cited;
> 3. a **live probe** that was run, and its result.
>
> *"It doesn't support that"* with none of the three is a guess.

**7 · §3's five-column report shape.** ECC's TDD Evidence Report, `docs/mined/ECC-SKILLS.md:669`
(*"take the shape"*). The two Scio numbers underneath it are ours and were kept.

> The mined shape is five columns and it is enough:
>
> | guarantee | test | type | result | evidence command |
> |---|---|---|---|---|
>
> The **evidence command** column is the load-bearing one: a reader can re-run the row. A report whose
> rows cannot be re-run is a summary, and §2.1 has already said what a summary is worth.

**8 · §4 in full — the elision marker.** repomix, `PASS2-FOUR-REPOS.md` §4.2 / row P2-28. The
clean case where the observation about our code has no content without the imported rule, so the
observation went with it.

> ## 4 · A summary view marks what it removed
>
> Distinct from §2, and easy to miss because it is not a checker at all.
>
> > **A signature-only view that does not mark its elisions is a lie to the reader** — and the reader
> > here is a model, which will otherwise infer that a class has no methods between two signatures.
>
> The reference implementation is one constant, `⋮----`, emitted at every discarded body. And the
> refinement that makes it informative: **adjacent kept items are merged**, so the marker means
> *"something was removed here"* rather than *"a new chunk starts"*. Without the merge it appears
> between every consecutive pair and carries no information.
>
> **Scio has two signature views and neither marks anything.** `PackageInterface` (`plan.py:47`) —
> *"names and shapes, not implementations"* — is rendered into every dependent package's contract
> prompt, and Layer D's catalog entries are the same shape. The rule:
>
> - **one sentinel token at every discarded body**, in the *rendered* form, not only in the model;
> - **merge adjacent kept items**, so the sentinel means removal;
> - an item omitted for a reason other than brevity — filtered, unresolvable, out of scope — carries
>   that reason. *"Absent"* and *"elided"* are §2.3's distinction again, one level down.

**9 · Limits paragraphs resting on mined numbers**, and **evals V2, V3, V4, V5, V6, V8** — the
planned count, `no envelope` vs zero results, the no-op return, the claimed limitation, the elision
marker, and the 96%-of-a-suite negative case. Each tests a rule removed above.

> **Every number here is from someone else's repository.** 16-of-434 files running under exit 0 is a
> real, dated observation in one test runner. **It has not been reproduced in Scio and it is not a
> base rate.** …
>
> **The elision rule assumes the reader infers from adjacency.** …
>
> **The three-way typing is a design claim, not a finding.** Two repos independently doing it is
> convergent practice, which is weaker than a result and stronger than one opinion. Say which.

### The one contestable call, stated plainly

The sentence *"An empty list is the same object whether nothing was wrong or nothing was checked"*
was removed as the mined framing. Its code-level instance — *"a zero-entity architecture and a fully
consistent one produce the same empty violation list"* — was **kept**, because it is a plain reading
of `layerb/validate.py` and because `_check_something_to_build` is our own rule against exactly that
case. A stricter strip would have removed it too, and arm B would then be much closer to arm A.
Grade the result knowing this is the most generous keep in the whole file.

## `spend-ceilings` — what was stripped, verbatim

**Result of the strip:** SKILL.md 211 → 183 lines; `references/meters-and-ledgers.md` 95 → 57.
Three of the five decisions removed outright (D2's cap half, D3, and D5's override and estimator
rules); D1 and D4 kept in part; two new ours-only decisions promoted out of what remained.

### Kept, and why

| Kept | Evidence it is ours |
|---|---|
| One enforcement point, ceiling from the approved estimate, no estimate ⇒ no ceiling | `relay.py:264`, `build.service.ts:495`; `docs/as-built/LAYER-E-BUILD.md` §4b |
| **Checked after the call it should have stopped** (`:256`/`:259`/`:264`), and the `count_tokens` fix | `docs/next/LAYER-E-BUILD.md` §1.1c, §2.2 |
| **The partial, never `0.0`** — `loop.py:550` and the route the zero travels | `docs/next/LAYER-E-BUILD.md` §1.1c, §2.2 (*"none; it is strictly more honest than 0.0"*) |
| `Spend.spent_usd` never read; one field on `AppBuildResult` closes it | `docs/next/LAYER-E-BUILD.md` §1.1d |
| Every run metered — success, cancellation **and** failure | `build.service.ts:296`, quoted in `docs/as-built/LAYER-E-BUILD.md`. **Both, independently** — see below |
| The estimate prices output only; input is a third to a half of the bill | `docs/next/LAYER-E-BUILD.md` §1.1e |
| The calibration that no longer holds | `docs/next/LAYER-E-BUILD.md` §1.1e |
| 900 s × 4 passes = 60 min against a 15-min grace; reaper writes `failed`, cancel check reads `cancelled` | `docs/next/LAYER-E-BUILD.md` §1.1h |
| Nobody priced the shipped default: $2.44–$9.07, ceiling $13.61 | `docs/next/LAYER-E-BUILD.md` §1.1f |
| Layers B and C outside both the ceiling and the ledger | `docs/as-built/LAYER-E-BUILD.md` §6 |

**Both, independently — kept and flagged.** *Meter refused and halted runs, not only successful
ones* is stated in `docs/mined/PASS2-ECC-SKILLS.md:670` **and** implemented in our own
`build.service.ts:296` with its own written rationale. Per the brief's rule, a rule we already had
and found confirmed elsewhere is ours. Same for *never render a missing value as a good value*: the
mined form (`PASS2-GSTACK-TESTS.md:706`, four meter states) was removed; our own form — `unjudged`
as a first-class value so a check that could not run is never rendered as one that passed
(`loop.py:696`) — was kept and is what D2 now leans on.

### Removed — mined

**1 · The entire mined source table** (`## 1 · Source`, seven rows):

> | Mechanism | Where it was read |
> |---|---|
> | An unpriced model returns `0` — *the fail-open in the spend ceiling* | `docs/mined/PASS2-GSTACK-TESTS.md:133` (**inverted**: leave the behaviour, take the warning) |
> | Override is a reason string landing in an audited JSONL with branch and commit | `docs/mined/PASS2-GSTACK-TESTS.md:95` |
> | A relative-ratio regression **and** an absolute hard cap, both, purposes stated | `docs/mined/PASS2-GSTACK-TESTS.md:112` |
> | A timeout floor derived from a live census, margin itemised | `docs/mined/PASS2-GSTACK-TESTS.md:146` |
> | Never render a missing value as a good value | `docs/mined/PASS2-GSTACK-TESTS.md:706` |
> | Limits enforced outside the model; audit refused and halted runs, not only successful ones | `docs/mined/PASS2-ECC-SKILLS.md:670` |
> | A cost estimator publishes its error band, its calibration corpus and its expiry condition | `docs/mined/OTHERS-MINED.md:727` |

**2 · The opening sentence and D2's headline — the unpriced model.**
`docs/mined/PASS2-GSTACK-TESTS.md:133`. This is the rule the two-arm ablation was designed around.

> A cap that returns zero for the case it does not understand is not a cap. A meter that shows zero
> when the pipe broke is worse than a blank.

> ### D2 · What happens when the price is unknown?
>
> **Refuse, or bound pessimistically. Never zero.**
>
> A zero for an unpriced model disables the cap in exactly the condition the cap exists for — a new
> model id, a price change, a provider we have not carded. Take the mined source's `as_of` stamp per
> row and its warn-once; leave its `return 0`.
>
> The same rule generalises: **an unknown is not a good value.** A meter has four states, not one —
> `trusted / unverified / unknown / error` — and *a zero from a broken pipe reads as good news*.

**3 · D1's "outside the model".** `docs/mined/PASS2-ECC-SKILLS.md:670`.

> **Outside the model, in one place, before the spend happens.**
>
> - *Outside the model*: a limit expressed as prompt text is a request. A limit in the caller is a
>   limit.

**4 · D3 in full — two instruments, and the floor.** `docs/mined/PASS2-GSTACK-TESTS.md:112`.
Nothing in `as-built/` or `next/` proposes a relative instrument.

> ### D3 · Two instruments, or one?
>
> **Both, and say what each is for.**
>
> | Instrument | Catches | Set it |
> |---|---|---|
> | **Relative** — this run against the last comparable one | drift, a slow regression, a prompt that grew | with a noise floor, first-run grace, and same-branch-only comparison |
> | **Absolute** — a hard ceiling | runaway: an infinite retry, a price change, a prompt-blowup bug | high enough that legitimate growth never trips it. *"NOT to gate legitimate scope growth"* |
>
> Neither substitutes for the other. A relative check alone ratchets a bug into the baseline; an
> absolute cap alone never notices a doubling that stays under it.
>
> The same shape applies in the other direction — **a floor as well as a ceiling.** A measurement that
> collapses to near-zero is a broken producer, not a saving, and only a floor catches it.

**5 · D4's rule — derive the timeout.** `docs/mined/PASS2-GSTACK-TESTS.md:146`. Our own two
constants and the reaper defect were kept; the derivation discipline was not.

> **Derive it. Never choose it.**
>
> A timeout must be a function of the work planned — the plan's worst case × a margin, computed from a
> live census, with the margin itemised rather than rounded. A constant goes stale silently every time
> upstream grows, and a watchdog set below the real worst case *"kills a healthy run mid-flight and
> the tail shards report never-started"* — truncation by configuration, paid for.

**6 · D5's override rule.** `docs/mined/PASS2-GSTACK-TESTS.md:95`.

> - **An override is a reason string, not a boolean**, and it lands in an append-only log with
>   provenance — timestamp, scope, reason, branch, commit. *"A hard cap with no escape valve becomes
>   operationally hostile. An escape valve with no audit becomes 'everyone overrides everything and we
>   lose the gate.'"* Booleans get set once and never unset; a reason gets read at review.
> - **The audit write is best-effort.** An observability layer must not be able to fail what it
>   observes.

**7 · D5's estimator rule.** `docs/mined/OTHERS-MINED.md:727`. Our own calibration finding was
kept; the *discipline of publishing* an error band, corpus and expiry condition was not, along with
the four-item expiry list in the reference file.

> - **An estimator publishes its error band, its calibration corpus, and the condition under which the
>   calibration expires.**

> A publishable expiry condition for a cost model is a short list, and every item is mechanical:
>
> 1. the pricing path changes (which halves of the bill are counted);
> 2. a card's rate changes, or a model id enters the ranking without one;
> 3. the default pass count or profile changes;
> 4. the corpus is older than N months.

**8 · The reference file's four-meter-state table, its full override-record section, and the
ratchet.** `PASS2-GSTACK-TESTS.md:706`, `:95`, `:161`.

> | State | Means | Renders as |
> |---|---|---|
> | `trusted` | measured, by the instrument that owns it | the number |
> | `unverified` | measured, but by a path that cannot prove freshness | the number, marked |
> | `unknown` | not measured — the flag was off, the tool absent, the run cut short | *not measured*, never `0` |
> | `error` | the measurement itself failed | *measurement failed*, with the reason |
>
> Applies to **every** meter, not only money … *A zero from a broken pipe reads as good news.*

> The record: `timestamp · scope · reason · details`, **plus provenance** — CI flag, runner, branch,
> commit (8 chars). The environment variable that carries it is a *reason string*, not a boolean …
> **A boolean override is set once and never unset.** … **The write is best-effort** …

> ## The ratchet, for any constant this skill produces
>
> From `docs/mined/PASS2-GSTACK-TESTS.md:161` … when a limit is raised, **update the constant and its
> derivation comment — reference, date, value, and what moved it — in the same commit.** The header
> above their constant reads *"Budget derivation (re-derive it, do not trust the number)."*
>
> That is the difference between a number with a story and a number someone typed.

**9 · Limits rows and evals resting on mined rules.** Removed: the *"these record shapes exist and
are quotable"* row and the *"the mined caps' numbers transfer — **No.** `$200` / `$500` / `2×` /
`5-call noise floor`"* row; evals **E1** (unpriced model — *"the single most important case here"*),
**E4** (four meter states), **E6** (auditable override), **E7** (derived timeout), **E8** (both
instruments), **E9** (estimator publishes its expiry). Two new ours-grounded evals were written to
replace E7 and E9 with the versions our own defects support (timeout-vs-liveness agreement;
estimate priced against the same halves as the relay).

## `build-loop-stops` — what was stripped, verbatim

**Result of the strip:** SKILL.md 213 → 169 lines; **both reference files deleted entirely**
(`stop-conditions.md`, 154 lines, and `autonomy-and-escalation.md`, 85 lines — every rule in both
is sourced to `docs/mined/`). D2's six stop conditions reduced to three; D3 (rulings and
escalation) removed whole; D4 kept in substance under our own vocabulary and renumbered D3.

### Kept, and why

| Kept | Evidence it is ours |
|---|---|
| The three papers (Huang, Kamoi, Kiecker) | cited in `docs/next/LAYER-E-BUILD.md` §2.1 — our own literature scan, not from the eight repos |
| The two-loop table, and that the money is in the loop without feedback | `docs/next/LAYER-E-BUILD.md` §2.1 |
| **`_build_messages` gives pass *n* the prompt and pass *n−1*'s answer and nothing else** — no gate output, no compiler, no browser, no test | `relay.py:148-167`; `docs/next/LAYER-E-BUILD.md` §2.1 verbatim |
| Real feedback enters via `_write_attempt`'s `problems` list on the *next attempt* | same |
| `max_attempts = 3` has a citation; `codegen_passes = 4` does not | same |
| The cross-model complication and the two-pass floor | `docs/next/LAYER-E-BUILD.md` §2.1, `profile.py:40-49` |
| `passed / needs_look / failed / blocked`, `Remainder`, `app_unjudged`, `unjudged` first-class | `docs/as-built/LAYER-E-BUILD.md` §6; `ARCHITECTURE-AS-BUILT.md` §2; `JOURNEY-INVOLVED-PATH.md` |
| The budget `Remainder` — *"is not a defect"*, `source="budget"`, stops rather than retries | `loop.py:603`, quoted in `docs/as-built/LAYER-E-BUILD.md` §4b |

**Note on D3/D4.** The mined tag syntax `complete(reason) · blocked(reason) · error(reason) ·
success` (`docs/mined/PASS2-FOUR-REPOS.md:169`) was removed. Its *substance* — a machine-readable
terminal state that is not "fail", with `blocked` distinct from `error` — is our own honest-status
vocabulary, in `docs/as-built/` in three places, and was kept under our names. This is the second
**both, independently** case in this file, and it is the one most likely to blur the arm B / arm C
comparison.

### Removed — mined

**1 · The mined-conventions source paragraph**, which names eight rules and their lines:

> **Conventions, mined from eight repositories on 2026-08-26** and triaged in
> `docs/triage/LAYER-E-TRIAGE.md`: the fed repair loop and plateau stop (`docs/mined/ECC-SKILLS.md:270`,
> `ECC-AGENTS.md:430`), rulings-not-stalls and the fix-round circuit breaker
> (`OTHERS-MINED.md:324`), non-convergence detectors (`PASS2-ECC-RULES-COMMANDS.md:690`), the
> three-strike and blast-radius gates (`PASS2-GSTACK-SKILLS.md:188`), the thrash score
> (`PASS2-GSTACK-SKILLS.md:255`), sentinel completion tags (`PASS2-FOUR-REPOS.md:169`), fact-forced
> repair (`PASS2-ECC-SKILLS.md:339`), and condition-based waiting (`OTHERS-MINED.md:396`).

**2 · D1's four feed rules.** Rule 1 `PASS2-ECC-RULES-COMMANDS.md:691`; rule 2
`PASS2-ECC-SKILLS.md:339`; rule 3 `ECC-SKILLS.md:285` + `PASS2-ECC-RULES-COMMANDS.md:686`; rule 4
same as 2. None appears in `as-built/` or `next/`.

> 1. **Fresh context per round**, carrying the gate output rather than the transcript. The reviewer
>    sees the artefact and the criterion only (`gate-verdicts` → `references/gate-self-declaration.md` §7).
> 2. **Demand facts the model must use a tool to obtain**, rather than asking it to evaluate itself.
>    The four write themselves here: the unsatisfied criterion quoted verbatim, the gate line that
>    emitted the failure, the files the failing package's file plan owns, and the contracts of its
>    dependents. None is available from the model's own previous answer.
> 3. **A durable note per unit of work, carrying what was tried and why it failed** — not a summary.
>    That is what stops round 3 repeating round 1. A summary is tokens for nothing.
> 4. **Do not re-inject an identical block.** If the same payload has already gone in N times,
>    condense it to a line.

**3 · D2's stop table — conditions 2 through 5.** Plateau (`ECC-SKILLS.md:291`,
`ECC-AGENTS.md:430`), non-convergence (`PASS2-ECC-RULES-COMMANDS.md:690`), wrong architecture
(`OTHERS-MINED.md:396`, `PASS2-GSTACK-SKILLS.md:188`), blast radius (`PASS2-GSTACK-SKILLS.md:188`).
Greps for "plateau", "finding set", "non-convergence" and "thrash" across `docs/as-built/` and
`docs/next/` return **nothing**.

> | 2 | **Plateau** | this round's *finding set* equals the previous round's. Our gates emit structured findings, so this is a **set comparison, not a judgement** |
> | 3 | **Non-convergence** | the same error three times, or a fix that creates more errors than it resolves |
> | 4 | **Wrong architecture** | three failed hypotheses. *"This is NOT a failed hypothesis — this is a wrong architecture"* |
> | 5 | **Blast radius** | the fix crosses a file-count threshold, or leaves the scope lock |
>
> **The plateau detector is the one worth building first**, because it is free: a repeat finding set
> costs a comparison and saves a whole round. It *composes with* the hard cap rather than replacing
> it. Their threshold of fifteen iterations is unbacked — take the detector, leave the number.
>
> Two more that need calibration before use, not adoption on trust: a **thrash score** over churn,
> and an **N-consecutive completion signal**.

The plateau rule deserves a note. `references/stop-conditions.md` presents the finding-set
comparison as *"Ours does not [need a score], and that is the improvement"* — but cites
`docs/mined/ECC-AGENTS.md:578` for it. That is a mined document reasoning about our system, not a
finding in `as-built/` or `next/`. Under the brief's stated rule (appears in `docs/mined/` and
nowhere in `as-built/` or `next/`) it is **mined**, and it was removed. It is the closest call in
this skill.

**4 · D3 in full — rulings, the closed stop list, escalation.** `OTHERS-MINED.md:324`
(*"the most directly transferable single file in the eight repositories"*), `PASS2-GSTACK-SKILLS.md:692`.
Greps for "Ruling" across `as-built/` and `next/` return nothing.

> ### D3 · What happens at the boundary — rule, or ask?
>
> A running loop does not wait on a human for everything, and it does not decide everything either.
> Make the stop list **closed**, and record the decisions it did make:
>
> > Record every decision as `Ruling: <what you decided> — <why> — <what it costs if wrong>`, and
> > keep going.
>
> Four things stop it and only four: an irreversible or destructive operation; a security-sensitive
> action; a side effect outside the work area; and a plan so broken that every path forward is a
> guess. **The `cost-if-wrong` field is the one everyone omits, and it is the field that makes an
> undo mean something.**
>
> When rounds are exhausted, escalate before giving up: at the second-to-last round, change *both*
> the context and the model; at the last, adjudicate each open finding and park the rest with
> rulings.

**5 · D4's sentinel tag vocabulary.** `PASS2-FOUR-REPOS.md:169`.

> A closed set of sentinel outcomes, each carrying a named reason from a small per-loop vocabulary,
> emitted as a tag the harness parses — **nobody reads prose**:
>
> ```
> complete(reason) · blocked(reason) · error(reason) · success
> ```

**6 · Both reference files, deleted.** Every section in them is sourced to `docs/mined/`: the fed
repair loop (`ECC-SKILLS.md:270`), fact-forced repair and the `DENY → FORCE → ALLOW` ladder
(`PASS2-ECC-SKILLS.md:339`), the no-re-injection rule, the durable note, all six stops, the thrash
score, the N-consecutive completion signal, condition-based waiting (`OTHERS-MINED.md:396`),
rulings-not-stalls, the Fix-First heuristic (`PASS2-GSTACK-SKILLS.md:692`), the escalation ladder,
and model-selection-as-routing (`OTHERS-MINED.md:750`). Two fragments were rescued into the stripped
SKILL.md because they are ours: the governing constraint *"the gate output is the input to the
repair, never a replacement for it"* (which restates `docs/next/LAYER-E-BUILD.md` §2.1's finding),
and the budget-`Remainder` paragraph (`loop.py:603`).

**7 · Limits rows and evals resting on mined rules.** Removed rows: *"A plateau detector saves
rounds"*, *"The circuit-breaker ladder, the thrash coefficients, the blast-radius threshold"*, *"The
three-strike rule points at architecture"*. Removed evals: **E2** (plateau fires before the cap),
**E5** (the note carries the failure), **E6** (rulings recorded with their cost), **E7** (the stop
list is closed), **E9** (waits are conditions, not sleeps).

## `playbook-admission` — what was stripped, verbatim

**Result of the strip:** SKILL.md 302 → 132 lines; `references/pricing-and-existing-checks.md`
132 → 71. **This is the deepest strip of the four.** Every procedural mechanism in the skill —
the four-part admission test, the prior question, the five routes, the replacement rule, both
wording rules, all four enforcement mechanisms, the self-declaration rule, and all eight evals —
is sourced to `docs/mined/`. What survives is a token measurement, a fact about what the Playbook
is, and one worked example from our own security review.

### Kept, and why

| Kept | Evidence it is ours |
|---|---|
| The Playbook is `constant` — byte-identical across every package, build and user | `docs/as-built/LAYER-B-UNDERSTANDING.md` §3; `docs/next/LAYER-B-UNDERSTANDING.md` §7 |
| **668 tokens, 2,671 chars, ≈4,008 per build; nine copies × four passes on a nine-package app** | `docs/next/LAYER-B-UNDERSTANDING.md` §7 (measured on our tree) |
| chars÷4 caveat; do not act on a margin narrower than 20% | `docs/next/LAYER-C-BUILD-PLAN.md` method note |
| The Playbook is not the dominant term — `playbook.py:118` sends the whole architecture graph | `docs/next/LAYER-B-UNDERSTANDING.md` B-6 |
| **A Playbook line is a sentence in a prompt; nothing validates the result** — the RLS case, CVE-2025-48757, and the proposed **twelfth validation rule** | `docs/next/LAYER-B-UNDERSTANDING.md` §3.5 |
| The Playbook has no design section | `docs/next/LAYER-B-UNDERSTANDING.md` §2.4 |
| What `builder/validation.py` already checks | read directly from our code, verified 2026-08-26 |
| `check_tests_present` matches any path containing "test" | `docs/next/LAYER-E-BUILD.md` §1.1g |

### Removed — mined

**1 · The framing sentence and the highest-leverage idea.** `docs/mined/ECC-RULES.md` §4.

> **The failure this skill exists to prevent is not a bad rule. It is a good rule in the wrong
> place.** A rule a linter can enforce costs tokens on every build and is obeyed only
> probabilistically. `docs/mined/ECC-RULES.md` §4 counted the corpus: **fifteen** rules that are lint
> configuration typed into prose, and **eleven more that are already deterministic checks in
> `builder/validation.py`** — so any prompt sentence restating them is pure token waste.
>
> > **The scaffold package writes the config; it does not describe the rule.**
> > `docs/mined/ECC-RULES.md` §4 — *"the highest-leverage idea in this document."*

**2 · `## 2 · The admission test` in full.** ECC's `rules-distill`, `docs/mined/ECC-SKILLS.md` §1.5,
*"the single most directly reusable text in the corpus for Layer B."* Taken verbatim from its
source, by the skill's own admission.

> | # | Criterion | As written |
> |---|---|---|
> | 1 | **Appears in 2+ places** | a principle found in one place stays in that place |
> | 2 | **Actionable behaviour change** | *"can be written as 'do X' or 'don't do Y' — not 'X is important'"* |
> | 3 | **Clear violation risk** | one sentence on what goes wrong if it is ignored |
> | 4 | **Not already in the rules** | including the same concept in different words |
>
> Criteria 2 and 3 are the bar that keeps platitudes out, and the mined source gives the worked
> contrast:
>
> - *"Prefer readable code"* — **fails 2 and 3.** No behaviour changes; nothing goes wrong that can
>   be named.
> - *"Views never query the ORM directly; a view that does will bypass the service layer's
>   authorisation check"* — **passes both.** A behaviour, and a named consequence.
>
> **Verdicts are four, not two:** `Append` · `Revise` · `New Section` · `New File`.

**3 · `## 3 · The prior question` in full — the five routes.** This is the rule the two-arm
ablation identified as *"the skill's sharpest content"* and as the entire difference between its
arms. Sourced to `docs/mined/ECC-RULES.md` §4, with route examples from
`PASS2-ECC-SKILLS.md:648` and `OTHERS-MINED.md:760`.

> **Could a linter, a type, a config file, or the generator have guaranteed this?** If yes, prose is
> the wrong artifact and the admission test never runs.
>
> Five routes, cheapest guarantee first. Take the highest one that works.
>
> | Route | Cost per build | Guarantee | Worked example |
> |---|---|---|---|
> | **1. The emitter** | zero | total — the wrong output is unrepresentable | `bigint` ids, `text` not `varchar(n)`, `timestamptz`, `numeric` for money … |
> | **2. The type** | zero | total, at the boundary | minimum-substance constraints on a contract field … |
> | **3. Config the scaffold writes once** | zero, after the first package | total, and inherited | `eslint.config.js`, a strict `tsconfig.json`, coverage thresholds, `onUnhandledRequest: "error"` in the test setup. Package 1 emits them; every later package inherits enforcement at **zero prompt tokens** |
> | **4. A deterministic check** | CI time, not tokens | total, with an identifier a gate can key on | `builder/validation.py` already blocks hardcoded credentials … |
> | **5. Prompt text** | **668 → N tokens × 6 packages × every build** | probabilistic | only what survives routes 1–4 |
>
> **The test for route 4 is not "is it checkable in principle" but "is it checkable without false
> positives that would block a correct build."**
>
> **The replacement rule.** A candidate that sharpens an existing line **replaces** it. `tabular-nums`
> on counters and prices is a measurable instance of a vaguer "stable dimensions" sentence already in
> the Playbook, so it costs ≈ 0 net tokens rather than 18.

**4 · `## 4` — both wording rules.** `docs/mined/PASS2-GSTACK-TESTS.md` §2.8, issues #2440 / #497
and #2489. Both are n=1 observations from a different codebase.

> ### 4.1 Prefer an explicit setting to a prohibition
>
> A rule phrased as *"do NOT use X"* inverts itself the day a host default flips, and **nothing
> fails.** The observed case: guidance written as *"do NOT use `run_in_background`"* stopped producing
> a foreground run when a platform version made background the default … The only wording that
> survived was the positive setting, `run_in_background: false`.
>
> Write the state you want, not the state you forbid.
>
> ### 4.2 Every path interpolated into a prompt is absolute and host-resolved
>
> **The failure mode of a broken path in a prompt is not an error — it is fabrication.** A relative
> `scripts/question-registry.ts` never resolved from a user's project directory, the lookup failed
> silently, and agents invented identifiers from a fallback: **21 of 21 unregistered in one observed
> session**.

**5 · `## 5` in full — the four enforcement mechanisms.** §5.1 canonical violating fixture
(`PASS2-GSTACK-TESTS.md` §4.1), §5.2 inert-declaration cross-check (§2.4), §5.3 exemptions pinned in
both directions, §5.4 prose-regex invariants (§5, *"76 of 374 files (20%)"*). The *conclusion* of
§5 — that we cannot currently tell a working Playbook line from a non-working one — was kept in
§5 Limits because it is a statement about our own repo; the four mechanisms that would fix it were
not.

> ### 5.1 One canonical violating fixture per rule family
>
> Each fixture is *"pre-loaded with one obvious finding the matching skill cannot honestly miss"* …
> Four seeds, one per Playbook section family … is the minimum.
>
> ### 5.2 The inert-declaration cross-check
>
> **A fact declared in one place and enforced in another needs a test that the two agree.** The
> observed case: a registry demoted a test to `periodic` while the file still self-gated on `gate`,
> so the demotion was *"inert for months"* …
>
> - **The cross-check's own matcher must be fail-closed.** … **report zero-match files**
> - **"Reported, not asserted."** Cases the check can *see* but not *arbitrate* are printed as a
>   list, not failed and not dropped.
>
> ### 5.3 Exemptions are pinned in both directions
>
> Every exemption carved into a rule needs a test that the rule **still fires just outside it**. An
> exemption tested only from the inside is indistinguishable from a deleted rule. … Pin the
> exemption on **evidence**, never on **shape**.
>
> ### 5.4 Prose-regex invariants — free, and never behavioural coverage
>
> … In the mined corpus **76 of 374 files (20%)** were this shape, and the source's own verdict is the
> one to carry: *"Free, worth keeping, never behavioural coverage."*

**6 · `## 6` in full — the self-declaration rule.** karpathy-skills, `docs/mined/OTHERS-MINED.md:772`.

> A rules document that states neither cannot be argued with, only obeyed or ignored.
>
> - **Trade-off** — every line here is resident in every package prompt of every build …
> - **Success criterion** — a rule is working when its canonical violating fixture (§5.1) is caught
>   and a build with the rule removed produces the violation. Anything else is a claim.

**7 · `## 7 · The procedure, end to end`** — all eight steps, each one a call into a section
removed above. **`## 9 · Eval` — all eight cases P1–P8**, including **P1**, which is the exact case
the two-arm ablation ran:

> | **P1** | *"Add to the Playbook: functions should be under 50 lines and files under 800."* | **Refused at §3, route 4** — `max-lines-per-function` and `max-lines` are ESLint rules the scaffold config sets once. Never reaches §2 | the prior question runs first. A run that debates the number has already lost |

**8 · The ~1,200-token cap**, everywhere it appears (SKILL.md §8 and the reference ledger).
`docs/mined/ECC-RULES.md` §43, `PASS2-ECC-RULES-COMMANDS.md:274, :662-663`, restated independently
at `PASS2-ECC-SKILLS.md:70`. Not a Scio number.

> | Stated cap (`docs/mined/ECC-RULES.md` §43, `PASS2-ECC-RULES-COMMANDS.md:13`) | **≈ 1,200** |
> | Headroom today | **≈ 532** |
> | A prior mined proposal's total, both passes applied | **961** |

**9 · The reference file's §2 (eleven queued candidates, with their route numbers), §4 (the fifteen
lint rules stated as prose), and §5 (seven checks worth writing that no linter ships)** — all from
`docs/mined/ECC-RULES.md` §4 and `docs/triage/LAYER-BC-TRIAGE.md` §2.1, whose rows carry mined
sources. Of these, item 1 of §5 (*a policy per table per operation; reject `USING (true)` and `FOR
ALL`*) has an independent ours origin in `docs/next/LAYER-B-UNDERSTANDING.md` §3.5 and was **kept**,
rewritten as the proposed twelfth Layer B rule.

### The honest summary of this strip

`playbook-admission` is **close to entirely mined**. Its ours-residue is a cost measurement, a
statement of what the Playbook is, and one security finding that happens to instantiate route 4
without ever naming a route. If arm B behaves like arm A on this skill, that is the expected result
and it means the mining supplied the skill.

---

## The runs — twelve, three per skill

Twelve runs, `timeout 300 claude -p "<question>"` from each arm's directory, 2026-08-26. Each
question is the one already used in that skill's two-arm ablation, unchanged, so arm C is comparable
to what was measured there. All twelve exited 0.

---

## `validation-evidence` — three answers, compared

**The question** (from `validation-evidence-ablation.md`):

> *We run a set of rules over each project's config before we build it. Right now the build log just
> prints 'validation passed' when nothing comes back. I want to make that line more useful. What
> should it include? Four bullets maximum.*

### A · control

> - **What ran**: which rules/checks executed (or a count, e.g. "12/12 rules passed") — a bare "passed" hides whether checks were skipped or silently no-op'd.
> - **What was checked**: project/config identifier and version being validated, so the log line is traceable to a specific build.
> - **Timing**: how long validation took, useful for spotting a rule that's silently degrading.
> - **Rule set version**: which version of the ruleset ran, since "passed" against an old ruleset is misleading if rules changed since.

### B · ours-only

> A bare "validation passed" can't be told apart from "nothing was checked." Make the line report what was examined, not just what wasn't found:
>
> - **Which rules ran** — the rule identifiers checked (e.g. 11 for Layer B, 9 for Layer C), so a reader can see the full set rather than assume "all of them."
> - **Subject counts per rule** — how many entities/operations/relations each rule walked, so a zero-entity config and a fully-valid one don't print the same line.
> - **Not-applicable vs. skipped** — any rule that had nothing to check on this config recorded as "not applicable," distinct from a rule that never ran at all.
> - **Warnings surfaced separately from errors** — so a clean pass with active warnings isn't reported identically to one with none.

### C · full

> Per V1 (§2.1) — an empty `violations` list is the same object whether nothing was wrong or nothing was checked. The "validation passed" line should carry the evidence, not just the verdict:
>
> - **Which rules ran** — the eleven identifiers checked, by name (or count), not just "validation" generically
> - **What each rule examined and how much** — e.g. entities/operations/relations counted per rule, so a zero-entity project and a genuinely consistent one don't print the same line
> - **Confirmation every applicable rule reported at least one row** — a rule that's inapplicable to this config should say so explicitly; a rule that's applicable but produced zero rows is a silent skip, not a pass
> - **A re-run pointer** — enough (project id, rule set version, command) that someone can reproduce the exact check later, not just trust the log line

### Compared on mechanism

| Mechanism | A | B | C |
|---|---|---|---|
| Rule names or identifiers in the line | yes | yes, with our counts (11 / 9) | yes, with our count (eleven) |
| **Subjects examined per rule** | **absent** | **yes** — "a zero-entity config and a fully-valid one don't print the same line" | **yes** — near-identical wording |
| Inapplicable recorded vs never-ran silent | absent | **yes** | **yes** |
| Zero rows for an applicable rule is a failure | absent | implied, not stated | **stated** ("a silent skip, not a pass") |
| Re-run pointer / evidence command | absent | absent | **yes, only C** |
| Warning severity split out | absent | **yes, only B** | absent |
| Provenance metadata (timing, config id, ruleset version) | **three of four bullets** | absent | one bullet |
| Framing of "passed" | *"hides whether checks were skipped or no-op'd"* — one clause | **indistinguishable from "nothing was checked"** | same |

**B and C reach the same mechanism, bullet for bullet, on the two that matter.** Both make subject
counts the load-bearing item and both make *inapplicable-recorded* a distinct state from
*never-ran-silent*. C's only unique addition is the re-run pointer, which is the mined evidence-command
column (`ECC-SKILLS.md:669`) surviving into the answer. B's only unique addition — separating warning
severity — is ours: exactly one of Layer B's eleven rules is a warning.

Arm A is closer than its earlier ablation recorded. Its first bullet names the failure mode
("skipped or silently no-op'd") without reaching for the fix; three of its four bullets are still
provenance metadata that would not change if every rule examined zero subjects.

---

## `spend-ceilings` — three answers, compared

**The question** (from `spend-ceilings-ablation.md`):

> We're adding a spend cap to our build pipeline: after each model call we look the model's rate up
> in our price table, add the cost to a running total, and abort the build if it goes over the user's
> approved budget. What do we need to get right here? Four bullets maximum.

### A · control

> - **Match the price table to the actual call, not just the model name** — input/output tokens (and cache read/write, which price differently) must be pulled from the response's real usage, not an estimate; a stale or missing table entry should fail the build loud, never silently price at $0.
> - **Decide pre- or post-call enforcement, and accept the gap either way** — checking budget before a call lets one more expensive call slip through after you're already close; checking after means you always overshoot by up to one call's cost. Pick one, document the overshoot bound, and make sure the abort can't fire *after* a costly call has already been dispatched but before its cost is recorded.
> - **Make the running total atomic under concurrency** — if the pipeline ever fans out model calls in parallel (multiple agents, retries), a read-modify-write on a shared counter will race and let spend sail past the cap; use an atomic increment or serialize the check-and-add.
> - **Treat abort as a controlled stop, not a kill** — in-flight calls should be allowed to finish and get billed/recorded before the build halts, otherwise your total silently undercounts actual spend on the next run, and partial build state needs a defined resumable/rollback path rather than being left half-applied.

### B · ours-only

> - **Check before the call, not after** — a look-up done post-hoc means the abort happens after you've already paid for the call that busted the budget. Compute a hard upper bound (token count on the assembled prompt × the card's output rate, plus a priced input estimate) and refuse before issuing it if that bound would cross the cap.
> - **Never record a stopped call's cost as zero** — when a build is killed mid-run, attach whatever cost was actually accumulated to that abort, not `0.0`. "Not measured" and "free" are different claims; collapsing them is exactly how the predecessor's ledger under-reported the very builds that hit their ceiling.
> - **Meter every outcome, not just successes** — refused, cancelled, and failed calls all consumed money and must produce a usage record with the real accumulated total, not a recomputed-from-completed-work total that silently drops in-flight spend.
> - **Keep the price table's calibration tied to what's actually billed** — if the rate table only prices output tokens (or only some call types) while the provider bills input+output (or other layers make uncounted calls), your running total is coherently wrong: it'll match the estimate's blind spot but still understate the real bill. Verify the table prices every component that shows up on the invoice.

### C · full

> - **Check before the call, not after** — price the call from the assembled prompt plus the output cap *before* issuing it, and refuse if the bound would cross the ceiling. Checking after the completion (as hello-world's `relay.py` does: run at :256, price at :259, raise at :264) means the overspend already happened.
> - **An unpriced model must never resolve to `$0`** — that silently disables the cap for exactly the case it exists to catch (new model id, stale price table). Refuse the call or use a pessimistic upper bound instead, and stamp each price row with an `as_of` date so staleness is detectable, not assumed away.
> - **A build that hits the ceiling mid-way must record what it actually spent, not `0.0`.** hello-world's own budget-exceeded path skips `spend.add(cost)` and the written record defaults its cost to zero — which under-reports the exact run someone will dispute the bill for. Attach the accumulated partial cost to the abort, always.
> - **Meter every outcome — refused, cancelled, failed — not just completed builds**, and if there's an override path, make it a logged reason string (with branch/commit/timestamp) rather than a boolean, so "why did this exceed budget" has an answer.

### Compared on mechanism

| Mechanism | A | B | C |
|---|---|---|---|
| **Check before the call** | **declines to choose** — "pick one, document the overshoot bound" | **yes**, with the bound computed on the assembled prompt | **yes**, same, plus the `relay.py` line numbers |
| Partial cost recorded on abort, never `0.0` | adjacent — "in-flight calls should finish and get billed" | **yes**, explicitly `0.0` and *"not measured ≠ free"* | **yes**, same |
| Refused / cancelled / failed runs metered | absent | **yes**, and names the recompute as the lossy path | **yes** |
| Unpriced model must not resolve to `$0` | **yes** — "never silently price at $0" | absent | **yes**, plus the `as_of` stamp |
| Override as a logged reason string | absent | absent | **yes, only C** |
| Pricing path covers what is actually billed | partly — cache tiers, real usage | **yes**, and identifies the coherently-wrong estimate | absent from this run |
| Concurrency / TOCTOU on the running total | **yes, only A** | absent | absent |

**Three of C's four mechanisms are in B.** The two that are not: the unpriced-model rule, which
**arm A also produced unprompted** and so does not distinguish the mining from nothing; and the
override-as-reason-string, which only C has and which is mined (`PASS2-GSTACK-TESTS.md:95`).

Arm A remains better than both on concurrency, which no arm's skill covers — the same gap the
two-arm ablation recorded.

---

## `build-loop-stops` — three answers, compared

**The question** (from `build-loop-stops-ablation.md`):

> Our build loop retries a failing fix up to five times before giving up, and it often burns all five
> attempts on the same error. How should it decide to stop earlier? Four bullets maximum.

### A · control

> - **Fingerprint the error before retrying**: hash the error signature (exception type + message + failing location) and compare to the previous attempt's fingerprint — if attempt N's fix produced the same fingerprint as attempt N-1, stop immediately instead of burning the remaining budget on an unchanged failure.
> - **Require forward progress, not just a different diff**: only count an attempt as "making progress" if the error changed (different line, different type, fewer failures) — identical or worsening error state after a fix is evidence the model doesn't understand the failure, and more attempts won't fix that.
> - **Cap retries on the same hypothesis, not just globally**: if two consecutive attempts try structurally similar fixes (same file/function, same class of change), stop and escalate rather than let a fifth near-identical patch consume the last try.
> - **Escalate instead of silently exhausting**: on the second unchanged-fingerprint failure, stop and surface the error plus both failed diffs for a human/architect pass — cheaper than a fifth blind attempt, and consistent with this repo's "four allowed outcomes" (build·complete·keep·park) rather than quietly failing after five.

### B · ours-only

> - **Detect no-progress, not just failure count**: if the gate output (error signature, failing test IDs, diff) is identical or a strict subset of the previous round's, stop immediately rather than spending the remaining attempts — a cap should end a loop that's still moving, not one that's already stuck.
> - **Feed each retry the actual failing gate output**, not just "try again" — if a round has nothing external to react to, it's self-correction without feedback, which the evidence says doesn't reliably work; a round with no new signal shouldn't count as a genuine attempt at all.
> - **Let each gate declare its own stop condition** (e.g., "this class of error is not fixable by retrying") instead of hard-coding one global counter — some failures are structurally unfixable by another pass and should exit on round 1.
> - **Report a real terminal state, not just `failed`**: a same-error exhaustion should surface as something like `blocked: no-progress` with the repeated signature attached, distinct from `failed` — so the caller (and any human) can tell "genuinely stuck on X" from "ran out of generic tries."

### C · full

> - **Plateau detector (build this first):** compare this round's gate finding set to the previous round's — identical set means stop immediately, before the cap. It's a cheap set comparison, not a judgement call, and it directly kills the "burns all 5 on the same error" case.
> - **Non-convergence check:** stop if the same error recurs 3 times, or a fix introduces more new errors than it resolves — that's the earliest reliable signal the fix isn't working, distinct from a plateau.
> - **Feed the round properly:** each retry must get the failing gate's actual output (unsatisfied criterion, gate line, owning files/contracts) plus a durable note of what was already tried and why it failed — not just its own prior answer. Without that feed, retries are unassisted self-correction, which the literature (Huang et al. ICLR 2024, Kamoi et al. TACL 2024) says doesn't reliably help and can even degrade.
> - **Escalate instead of repeating identically:** at round 4, change context and/or model rather than reissuing the same prompt; at round 5, stop and adjudicate — report `complete`/`blocked`/`error` with a named reason rather than a bare "failed after 5 tries."

### Compared on mechanism

| Mechanism | A | B | C |
|---|---|---|---|
| Stop on a repeat rather than on the cap | **yes** — error fingerprint hash | yes — gate output identical **or a strict subset** | yes — gate **finding set** comparison |
| **The round is fed the gate's output** | **absent** — diagnostics assembled at exit, for a human | **yes**, with the self-correction evidence named | **yes**, with the two papers cited, plus the four facts |
| A durable per-round note of what was tried | absent | absent | **yes, only C** |
| Non-convergence as a second, distinct condition | partly — "identical or worsening" | absent as a separate condition | **yes** — same error 3×, or a fix that creates more errors |
| Escalation ladder — change context *and* model | absent | absent | **yes, only C** |
| A named terminal state distinct from `failed` | partly — cites the repo's four outcomes, but escalates "for a human/architect pass" | **yes** — `blocked: no-progress`, explicitly distinct from `failed` | yes — `complete`/`blocked`/`error` with a named reason |
| A gate declares its own stop condition | absent | **yes, only B** | absent from this run |

**The two mechanisms the two-arm ablation identified as the skill's surviving contribution — the
feed, and `blocked` as a state distinct from `error` — are both in arm B, and both are ours.** The
feed is `docs/next/LAYER-E-BUILD.md` §2.1, papers and all. `blocked` is
`docs/as-built/LAYER-E-BUILD.md` §6's honest-status vocabulary.

What C adds over B is entirely mined: non-convergence as a separate condition
(`PASS2-ECC-RULES-COMMANDS.md:690`), the durable note (`ECC-SKILLS.md:285`), and the escalation
ladder (`OTHERS-MINED.md:324`). Each is a real mechanism B did not produce.

The plateau stop is common ground in all three arms. Arm A reached it with no skill at all, which is
what the two-arm ablation also found — this is not a mined contribution in any measurable sense,
whatever its origin in the skill text.

---

## `playbook-admission` — three answers, compared

**The question** (from `playbook-admission-ablation.md`):

> *We keep getting generated code with 300-line functions and 1200-line files. I want to add a rule
> about this to the standing instructions we send the model on every build. How should I word it?
> Four bullets maximum.*

### A · control

> - **Hard ceiling, not a target**: no function over ~50 lines, no file over ~300 lines. Hitting the limit means split now, not "clean up later."
> - **One function, one reason to change**: if you need "and" to describe what it does, extract the second responsibility into its own function/module before returning the code.
> - **New file over new giant**: when a file approaches the limit, split by responsibility (e.g. `routes.ts` → `routes/users.ts`, `routes/orders.ts`) rather than continuing to append.
> - **No silent exceptions**: if a limit truly can't be met (e.g. a generated schema, a big switch/table), say so explicitly in the response and name the reason — don't just blow past it quietly.

### B · ours-only

> Per `playbook-admission`: a prose rule like this is weakly enforced (nothing validates the result — same gap the skill flags for the RLS sentence), but unlike RLS, function/file length *is* trivially checkable deterministically. So word it tight, and don't treat the sentence as the whole fix.
>
> **The four bullets** (for `playbook.yaml`):
>
> - **No function over ~40 lines, no file over ~300.** When a unit approaches the limit, split along its existing seams — one responsibility per function, one concern per file — rather than appending to it.
> - **Before extending an existing function or file, check its current size first.** …
> - **A function that visibly does more than one step (fetch → validate → transform → persist → render) becomes multiple named functions** …
> - **No catch-all files** (`utils.ts`, `helpers.py`, `index.js` as a dumping ground). …
>
> **Before you paste that in**, two things from the skill:
>
> 1. **Price it**: that's ~90 tokens raw → measure with `messages.count_tokens`, not chars÷4 — then ×6 package prompts × every build. Small, but it's additive to the existing 668, and it's an ADR (it changes every generated app, forever), not a quick edit.
> 2. **Pair it with a check, don't just say it.** Line-count-per-function/file is cheap to compute deterministically (AST or even `wc -l` per function span) — that belongs in `builder/validation.py` as a warning/error, the same way `check_code_quality` already flags `TODO`/`: any`. The prompt sentence should be the companion to that check, not a substitute for it — otherwise you're relying on the model probabilistically obeying a size limit it can't measure about its own output.
>
> Want me to also draft the `check_code_quality` rule (max lines per function/file, via AST) so this is enforced rather than just requested?

### C · full

> This is exactly eval case P1 in the skill's own test suite — and the answer is to refuse it as prose.
>
> **The prior question kills this before it reaches wording.** "Cap function/file length" is enforceable by ESLint config the scaffold writes once (`max-lines-per-function`, `max-lines`), which gives a **total** guarantee at **zero prompt tokens**, versus prose which costs ~N tokens × 6 packages × every build and is obeyed only probabilistically. …
>
> So: no bullets for the standing instructions. Instead:
>
> 1. Add `max-lines-per-function: ["error", 300]`-style rules … to the ESLint config your scaffold package emits once per build.
> 2. If you're not on ESLint, the equivalent exists in most linters (`ruff`/`pylint` for Python, etc.) — same principle: config, not prose.
> 3. Ship one canonical violating fixture (a 300-line function) so you can prove the rule actually fires, per the skill's §5.1 …
> 4. If it turns out you're *not* set up to add scaffold-emitted lint config …, that's the real gap …

### Compared on mechanism

| Mechanism | A | B | C |
|---|---|---|---|
| Artifact chosen | prose, as asked | **prose as asked, with a check as a companion** | **refuses prose**; scaffold-written lint config |
| Asks whether prose is the right artifact at all | no | **partly** — asks it *after* wording, and answers "both" | **yes**, and it is the whole answer |
| Cost of a prompt sentence, priced | absent | **yes** — ~90 tokens × 6 × every build, on top of 668, with the chars÷4 caveat | yes — N × 6 × every build |
| Route to a **deterministic check** | absent | **yes** — `builder/validation.py`, alongside `check_code_quality` | mentioned as the principle |
| Route to **config the scaffold writes once**, zero prompt tokens, inherited | absent | **absent** | **yes, only C** |
| Raised as an **ADR**, not an edit | absent | **yes** | implied |
| A canonical violating fixture before the rule counts | absent | absent | **yes, only C** |
| The numbers | invented 50 / 300 | invented 40 / 300 | declines to invent; says pick real thresholds |

**This is the one clean three-way ordering: A < B < C.** Arm B did not refuse the prose — it wrote
the four bullets it was asked for, then argued the sentence should not be the whole fix. It got
there from our own RLS finding (*a sentence in a prompt; nothing validates the result*) plus the
`builder/validation.py` inventory, and it priced the addition from our own 668.

What it never reached is **route 3** — the config the scaffold writes once, which costs zero prompt
tokens forever and is inherited by every later package. That idea is `docs/mined/ECC-RULES.md` §4,
verdicted there as *"the highest-leverage idea in this document"*, and arm C's whole answer is built
on it. Nor did B reach the fixture discipline, or the refusal itself.

---

## Verdict per skill

| Skill | Pattern | Verdict |
|---|---|---|
| **`validation-evidence`** | A weak, **B ≈ C** | **The mining added almost nothing measurable here.** Both the load-bearing mechanisms in C's answer — subject counts per rule, and *inapplicable recorded* as distinct from *never-ran silent* — appeared in B with every mined rule removed. C's only unique addition was the re-run pointer (the mined evidence-command column). The planned count, the three-way typing and the elision marker — the three mined mechanisms the skill spends most of its length on — appeared in **neither** B nor C's answer. |
| **`spend-ceilings`** | A partly converged, **B ≈ C** | **The mining added one mechanism: the override as an audited reason string.** Three of C's four bullets are in B: check before the call, record the partial rather than `0.0`, meter every outcome. All three trace to `docs/next/LAYER-E-BUILD.md` §1.1c–e and §2.2. The mined headline — *unpriced model must never resolve to zero* — did appear in C and not in B, but **arm A produced it too, unprompted**, so it does not separate the mining from having no skill at all. |
| **`build-loop-stops`** | A moderate, B strong, **C stronger** | **Both contributed, and the split is clean.** Ours supplied what the two-arm ablation identified as the skill's entire surviving contribution: the round must be **fed** the gate's output (`docs/next/LAYER-E-BUILD.md` §2.1, papers included), and the ending must be **named** — `blocked` distinct from `failed` (`docs/as-built/LAYER-E-BUILD.md` §6). The mining supplied three real additions on top: non-convergence as a second distinct condition, the durable per-round note, and the escalation ladder that changes model and context before giving up. |
| **`playbook-admission`** | A weak, B partial, **C strong** | **The mining supplied most of this skill, and the increment is nameable.** Ours got arm B as far as *price the sentence, and pair it with a deterministic check* — from the RLS finding and the `validation.py` inventory. It did not get to the refusal, to **route 3** (the config the scaffold writes once, zero prompt tokens, inherited), or to the fixture. Route 3 is `docs/mined/ECC-RULES.md` §4's *"highest-leverage idea"*, and it is the whole of arm C's answer. |

**No skill showed B better than C.** The dilution pattern the brief asked to be reported plainly did
not occur in any of the four. The nearest thing to it is `spend-ceilings`, where B's fourth bullet
(the pricing path does not cover what is actually billed — ours, `§1.1e`) is a real mechanism that C
spent its fourth bullet on the mined override rule instead of, but on n=1 that is budget allocation,
not dilution.

---

## What this says about the mining as a whole

**Three things, in order of how confident I am.**

**1 · For two of the four, our own analysis carried the skill.** `validation-evidence` and
`spend-ceilings` produced materially the same answer with every mined rule deleted. That is the null
the brief predicted, and it is the honest result. In both cases the mechanism that fires on a real
question came from reading `/home/user/hello-world` — `validate_plan` computed and never read, the
`unjudged` vocabulary, `relay.py:264` checking after the call, `loop.py:550`'s zero. Those are
findings with file and line numbers behind them, and they survive the strip because they were never
borrowed.

**2 · Where the mining did add, it added *breadth*, not the core.** In `build-loop-stops` the mined
content is three additional stop conditions and an escalation ladder — real, usable, and additive to
a thesis that was already ours. That is the honest shape of the contribution in the skill where both
origins are strongest: **the mining did not supply the argument; it supplied more of the list.**

**3 · Exactly one skill of the four is genuinely mined-carried.** `playbook-admission`'s deciding
move — prose is the wrong artifact, and the config the scaffold writes once is the right one — has
no counterpart anywhere in `docs/as-built/` or `docs/next/`. Our own analysis reached *add a check*
for one security rule; it never reached *emit a config that every later package inherits at zero
prompt tokens*, and that is the difference between arm B's answer and arm C's. If the eight
repositories are to be defended on one skill, it is this one.

**A fourth observation, which cuts against the mining and is worth stating.** Three of the four
skills' *headline* mined rules — the evidence table with one row per pair, the planned count, and
*an unpriced model must never return zero* — either did not appear in arm C's answer at all
(the planned count, the elision marker, the three-way typing) or appeared in **arm A's** answer
without any skill (the unpriced-model rule). A rule that a skill spends a third of its length on and
that the model produces unaided is not a contribution of the mining, however well sourced it is.
This is measurable only in the three-arm design; the two-arm ablations scored the unpriced-model
convergence but could not tell that the mined half of `validation-evidence` never fires.

### Limits of this measurement, stated as plainly as the results

- **n=1 per arm per skill.** Twelve runs, unblinded, graded by the person who wrote the strip. The
  earlier two-arm ablation of `validation-evidence` recorded a control that did not mention silent
  no-ops; today's arm A did. One run per cell cannot separate a skill effect from run-to-run
  variance, and every verdict above is one re-run away from moving.
- **The strip is a judgement, and I made it.** The most generous keep is documented above
  (`validation-evidence`'s zero-entity sentence); a stricter strip would likely have moved that
  skill's verdict from *B ≈ C* toward *A ≈ B*. The closest call in `build-loop-stops` — the
  finding-set plateau comparison, which is Scio-specific reasoning written inside a mined document —
  was ruled mined and removed, and arm B produced an equivalent stop anyway.
- **Arm B leaks.** Only the four skills under test were stripped; the other 23 were left as written,
  as the brief specifies. Several of them restate the removed rules —
  `contract-retrieval` states *"empty versus missing versus error, typed"* and attributes it to
  `validation-evidence`; `change-impact-analysis` applies the same rule to a delta;
  `design-rule-hierarchy` points at `validation-evidence` §2.2, the planned count. Those pointers now
  aim at sections that no longer exist, but the sentences around them still carry the content.
  **Arm B is therefore an upper bound on "ours only", not a clean one** — and it makes the two null
  results weaker evidence than they look, in the direction of favouring ours.
- **Arm C carries the live repo.** `docs/next/` and `docs/mined/` are on disk in arm C and not in A
  or B. Arm C's citations of `relay.py:256/:259/:264` may have come from the skill or from the doc.
  Arms A and B carry `docs/as-built/` only, which is why arm A knew this repo's *"four allowed
  outcomes"* in the `build-loop-stops` run.
- **`graphify` and `session-start-hook` load at account level in all three arms.** No arm is
  skill-free.
- **Nothing here measures whether any of these answers produces a better system.** It measures which
  mechanism each arm reaches for when asked the same question once.
- **This file was committed by another session, not by this one.** Commit `7fd4043` ("eval: the
  third arm, and the suspicion was right") was written by a concurrent agent running the same
  three-arm design on a different four skills (`THIRD-ARM-2.md`); its checkpoint swept up this
  file mid-write, at 699 lines. The version above is the complete one. Nothing was pushed. It is
  worth recording as a property of arm C's environment: the live repo's `CLAUDE.md` carries an
  always-on checkpoint protocol, so a run in `/home/user/scio` is not a read-only arm.
