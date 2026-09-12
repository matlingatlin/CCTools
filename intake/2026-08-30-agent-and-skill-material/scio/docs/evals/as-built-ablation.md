# Ablation · `as-built`

**Date:** 2026-08-26. Control: same CLAUDE.md and as-built docs, no project skills.

This is the **re-run** demanded by `as-built-ablation-01.md`, where the skill made an answer *worse*: it
obeyed its own do-not-open-the-old-repo rule while `00-INDEX` and `LAYER-C-BUILD-PLAN` disagreed, resolved
the conflict from the graph, and answered seven where the answer was nine. Since then the documents were
repaired and the skill gained an escape hatch — *"When two documents disagree, stop and go to the code."*
**Two** questions were run here: one to discriminate on the standing facts, one to test whether the
amendment holds.

**Confound:** `graphify` is installed at **account level** and loads in **both** arms. **Second confound:**
the treatment directory carries `docs/next/`, `docs/mined/`, `docs/decisions/`, `scripts/` and `scio.db`
that the control does not; `CLAUDE.md` and `docs/as-built/` are identical between arms. **Third:** the
predecessor source really is on disk at `/home/user/hello-world`, reachable by absolute path from **both**
arms — so the escape hatch was genuinely available to control and treatment alike.

## The discriminating rule, and why the obvious answer is wrong

Two rules were targeted.

**Q1 — the standing facts contradict the sources a reader would trust.** The skill's *Standing facts*
list says the predecessor's own `STRATEGY.md` is stale (it claims the intake agent was never built; it
was, and has run for real), and — separately — that *"the baseline below is one observation, not proof of
stability: `design.test.tsx` is recorded as flaky (B105)."* The obvious answer to "the docs say X and the
tests are green" is to believe both. One of those is a documentation-drift trap; the other is a
green-is-a-claim trap.

**Q2 — a units trap.** *"How many validation rules"* has two true answers in this repo: **nine rule
identifiers** emitted by **seven check functions** (`layerc/validate.py`, counted at source below). The
obvious answer is to report whichever number the first document offers, without the unit. This is
ablation-01's question, re-asked against the repaired documents.

**Ground truth, counted at source on 2026-08-26:**
```
grep -o 'rule="[a-z_]*"' layerc/validate.py | sort -u | wc -l   → 9
grep -c '^def _check'    layerc/validate.py                     → 7
```
And `validate_plan` is imported only by `layerc/service.py:22,85` — nothing downstream reads the result.

## The questions

**Q1** — *The old repo docs say the intake agent was never built, and its test suite is green. Before I
plan the rebuild around that, is that the real picture — what is actually safe to carry over and what is
not? Four bullets max.*

**Q2** — *How many validation rules does the build-plan step run before a build, and does anything
actually read the result? Two bullets.*

Neither names a skill, a file in `.claude/`, or a term unique to the skill. Q1 asserts both traps as fact.

## Control answer

**Q1** (trimmed — the two carry-over bullets are near-identical to the treatment's and elided):

> Checked `docs/as-built/LAYER-A-INTAKE.md` against `01-DECISIONS.md`, `00-INDEX.md`, and both
> review-synthesis docs. The premise needs correcting on one point and caveating on another:
>
> - **"Never built" is stale, not current.** That line is a quote from `docs/STRATEGY.md` (untouched since
>   2026-08-19), and Layer A explicitly flags it as documentation drift: the agent shipped and ran for
>   real, cited to `extraction.py:317`, `questions.py::write_question`, `service.py::run_intake_step`,
>   commits dated 2026-08-19/22. Plan around it being built.
> - **"Green" needs a caveat before you lean on it.** The 67 intake tests are part of a single clean-
>   container run on 2026-08-26 (`00-INDEX.md`). `REVIEWS-WHAT-WE-MISSED.md` §6 catches our own team
>   writing down one green run as a "verified baseline" elsewhere in this same pass, when a known flaky
>   test (`design.test.tsx`, per the consultant review) had failed on other runs. One pass isn't proof of
>   stability — treat it as one observation, not a guarantee, especially since I haven't re-run the suite
>   or the cited file:lines myself […]
> - **Safe to carry over (Layer A's own "Solid" list):** […] `FieldMeta{value, source, confidence,
>   provenance}` […] `is_buildable()` gate […] `StandInIntakeProvider` no-API-key path […]
> - **Not safe to carry over as-is:** the boolean shape of `is_buildable()` […] the fixed-order question
>   sequence and lack of app-kind detection, and the total absence of a feedback loop or replay metric […]

**Q2:**

> Confirmed against `docs/as-built/LAYER-C-BUILD-PLAN.md`:
>
> - `validate_plan` (`validate.py`) runs **seven check functions** before a build (e.g. `_check_coverage`
>   at `validate.py:43`).
> - Nothing reads the result: `builder/pipeline.py:214-227` calls `run_layer_c` and proceeds straight to
>   `save_plan`/build without touching `layer_c.validation`, the `EnginePlanResponse` type doesn't even
>   model a `validation` field, and a repo-wide grep for `.validation` outside `layerc` and its tests
>   turns up nothing — despite ADR-0013 and `LAYER-C.md` claiming the plan is validated before building
>   (doc:code mismatch, `LAYER-C-BUILD-PLAN.md:204-325`).

## Treatment answer

**Q1** (trimmed the same way):

> Verified against `LAYER-A-INTAKE.md` (§6, §Documentation drift, all sourced to `file:line`).
>
> - **"Never built" is stale, not current.** `docs/STRATEGY.md` §A line 12 says "Designed; NOT built" but
>   that file was last touched 2026-08-19 — the code moved past it with real relay calls
>   (`extraction.py:317` […]), commit dated 2026-08-19/22. The agent has run for real. **Green tests are
>   real evidence here, not a false signal — 67/67 passing, verified 2026-08-26.**
> - **Safe to carry over as-is:** the provenance model […] enforced in code at `intake/extraction.py:160`/
>   `:64`/`:142`, not just prompted […] These are marked *Solid* — rebuilding them loses work and reopens
>   closed bugs.
> - **Safe to carry over only with an explicit ADR, not silently:** the fixed WHICH/HOW question order
>   (deterministic gate picks the field, model only words it) — reopening this to make selection adaptive
>   trades away a stated guarantee, per ADR-0010's own reasoning, not a free win.
> - **Not safe to inherit as-is — real gaps, not documentation drift:** `is_buildable()` being a plain
>   boolean with no scored coverage view, no app-kind detection […] and no replay harness/metric at all
>   […] Plan the rebuild's evaluation story before touching the schema.

**Q2:**

> - `validate_plan` (`validate.py`) runs **seven check functions** before a build — coverage, cycles,
>   contract validity, etc.
> - Nothing consumes the result: `builder/pipeline.py:214-227` calls `run_layer_c` and proceeds straight
>   to `save_plan`/build without reading `layer_c.validation`, the `/plan` API response type doesn't even
>   model the `validation` field, and a repo-wide grep for `.validation` outside `layerc` and its tests
>   turns up nothing — it's an advisory report nobody reads, despite ADR-0013 and `LAYER-C.md` both
>   claiming a validated-before-building plan.

## Comparison

| Mechanism | Control | Treatment |
|---|---|---|
| Q1 · `STRATEGY.md` is stale, agent is built | **yes**, with `file:line` | **yes**, with `file:line` — same citations |
| Q1 · **green is one observation, not stability** | **yes** — names `design.test.tsx` flaky, and that the team made this exact error once already | **no — asserts the opposite**: *"Green tests are real evidence here, not a false signal"* |
| Q1 · carry-over "Solid" list | same six items | same six items |
| Q1 · **third verdict — *deliberate*, change only via ADR** | **no** — binary safe / not-safe | **yes** — the WHICH/HOW question order, tied to ADR-0010's stated reason |
| Q1 · states its own epistemic limit | **yes** — "I haven't re-run the suite … myself" | no |
| Q2 · rule count | seven check functions | seven check functions — **identical** |
| Q2 · **unit attached (nine identifiers / seven functions)** | **no** | **no** |
| Q2 · nothing reads the result | yes, with the same `pipeline.py:214-227` evidence | yes, near-verbatim the same |
| Q2 · noticed `ARCHITECTURE-AS-BUILT.md:70` still says "nine rules" | no | no |

Q2's two answers are close to verbatim identical. Both went to `LAYER-C-BUILD-PLAN.md` and stopped there.

## Verdict

**No difference — and inside the null, one regression.**

**Does the amendment hold?** *Untested, and for an instructive reason.* The escape hatch fires only when
two documents disagree, and the document repair removed the disagreement the reader would hit:
`00-INDEX:120` now states both numbers with their units and `LAYER-C-BUILD-PLAN:204` says seven check
functions. Neither arm encountered a conflict, so neither arm needed the hatch. **Both arms then answered
a question about *rules* with a count of *functions*** — the same class of error as ablation-01, now
committed by control and treatment alike, and no longer detectable as a contradiction. The repair fixed
the contradiction and, in doing so, removed the thing that made a reader stop and attach the unit.
`ARCHITECTURE-AS-BUILT.md:70` still carries a bare *"nine rules"*; neither arm read it. **That is a
finding about the documents, not the skill.**

**The regression on Q1 is the skill's own.** `as-built` carries the standing fact *"the baseline below is
one observation, not proof of stability: `design.test.tsx` is recorded as flaky (B105)."* The treatment
arm, with that sentence loaded, wrote *"Green tests are real evidence here, not a false signal."* The
control, without it, reconstructed the caveat from `REVIEWS-WHAT-WE-MISSED.md` and stated it more
strongly than the skill does. A skill firing is not a skill being applied.

**What the treatment did add:** the third State verdict — *deliberate, easy to break by accident* — and
what it obliges (change it only by arguing against ADR-0010 in an ADR). The control collapsed the
five-verdict vocabulary into safe/not-safe and lost that middle category entirely. That is a real
mechanism the skill supplied, and it is the one thing on the table that changes what someone would *do*.

Net: one mechanism gained, one caveat lost, and the routing measured as no better than the documents'
own. Ablation-01's finding — *the document did the routing; the skill was not needed to find it* — repeats.

## Limits of this measurement

n=1 per arm, two questions, unblinded, single grader who wrote the questions after reading the skill. The
treatment arm carries the rest of the `scio` corpus as well as the skills. Q1's regression is one sample:
a rerun might not reproduce it, and I did not rerun it. Nothing here shows the skill is net-negative —
it shows that on these two questions it did not beat the documents it routes to, and that on the one
question where it held a directly applicable standing fact, it did not apply it.
