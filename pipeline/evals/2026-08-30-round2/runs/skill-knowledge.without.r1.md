# skill-knowledge — answers (round 2, without)

Claim-row schema used throughout (one row per atomic claim):

`id | claim (atomic, falsifiable) | source (title, URL, section/locator) | source type | date fetched | evidence strength | verdict | how it is used in the skill | open question`

Verdicts: **MEASURED** (the source reports a number/observation from an actual
measurement, and I read the passage that reports it) · **REPEATED** (the source
asserts it but is passing on someone else's or its own untested experience —
no measurement I can inspect) · **DISPUTED** (sources conflict) ·
**UNVERIFIED** (I have not seen the passage that would settle it).

---

## Q1

Added. It goes in as a **REPEATED** claim, not a measured one — "in our
experience" and "roughly in half" is a practitioner impression with no n, no
baseline, no definition of "review time". That does not make it useless; it
makes it evidence about what practitioners believe, and it must be labelled as
such so nobody downstream cites it as a number.

Row appended to the claim set:

```
id:            C-014
claim:         Adding a linting step to CI reduces code-review time, by an amount
               the source characterises as roughly half.
source:        "<engineering blog post title>", <org> engineering blog, <URL>,
               section "CI" (the sentence quoted below).
quote:         "In our experience, teams that add a linting step to CI cut review
               time roughly in half."
source type:   vendor/practitioner blog post (self-reported, not peer reviewed)
read:          in full
date fetched:  2026-08-30
evidence:      anecdotal; no sample size, no baseline, no definition of "review
               time", no control for confounders (team size, PR size, tooling
               changes shipped at the same time). Directional only.
verdict:       REPEATED
use in skill:  motivation / "why teams do this" only. MUST NOT be cited as a
               quantitative effect ("halves review time"). If the skill needs a
               number, this is not the source.
open question: is there any measured study of linting-in-CI vs review latency?
               If one is found, this row is superseded, not merged.
```

Two things I did at the same time, because they are part of "add it", not
extra credit:

1. I recorded the **verbatim sentence** and the URL. A paraphrase of a
   soft claim hardens it — six weeks from now "roughly in half" becomes "50%"
   unless the exact words are on the row.
2. I stamped the fetch date. Blog posts get edited and deleted; the row has to
   say what the page said on the day I read it.

If the claim set already contains a row on lint-in-CI, this extends that row
with a second source rather than opening a rival row.

---

## Q2

We write both failures down **now**, as claims, in the same turn we learned
them — before doing anything else with them.

The nine existing claims are from the *proposal* stage: they are what we
expected the skill would need to cover. The probe just produced something
categorically better — two **observed** failures of a real agent on a real
task. Observed failures are the highest-grade evidence this project can get,
and they are also the most perishable: they exist only in a probe transcript
that will be compacted away.

So:

**1. Two new rows, marked as observed, not proposed.**

```
id:            C-010
claim:         An agent reviewing a schema migration does not, unprompted, check
               whether the migration holds a lock for longer than the request
               timeout.
source:        probe run <run-id>, transcript <path>, turn <n>
source type:   own observation (probe)
date:          2026-08-30
evidence:      MEASURED — observed 1/1 probe runs. n=1; not yet repeated.
verdict:       MEASURED (single observation)
use in skill:  becomes a required check in the skill's procedure: "lock duration
               vs request/statement timeout" is an explicit step, not left to
               the model's judgement.
eval:          this failure is the seed for an adversarial eval scenario — a
               migration whose lock outlives the timeout; baseline must fail it.
open question: does it fail on 3/3 reruns? n=1 is a sighting, not a rate.

id:            C-011
claim:         An agent reviewing a rename does not, unprompted, identify which
               other services read the renamed table.
source:        probe run <run-id>, transcript <path>, turn <n>
source type:   own observation (probe)
date:          2026-08-30
evidence:      MEASURED — observed 1/1 probe runs. n=1; not yet repeated.
verdict:       MEASURED (single observation)
use in skill:  required step: enumerate every reader of the changed object
               (grep/graph the repo, not recall) before the change is called safe.
eval:          adversarial scenario — a renamed table with one out-of-repo reader.
open question: does it also miss writers, or only readers?
```

**2. The nine proposal-stage claims get re-graded against the probe.**
This is the part that is easy to skip. A probe does not only add claims, it
*scores the old ones*. For each of the nine, one of three outcomes:

- **corroborated** — the probe hit it, the agent failed it → promote from
  proposed to observed, and it earns a place in the procedure.
- **contradicted** — the probe hit it and the agent handled it fine → demote or
  drop. A skill that instructs the model to do what it already does reliably is
  pure token cost.
- **untouched** — the probe never exercised it → it stays *proposed*, clearly
  labelled, and it is a candidate for the next probe. It must not silently
  inherit the credibility of C-010/C-011.

**3. Provenance stays separated.** Proposed claims and observed claims live in
the same file but never lose their `source type`. The failure mode I am
guarding against is a bundle where nine speculations and two observations read
identically after a week.

**4. n=1 is stated as n=1.** I do not write "the agent misses lock duration" as
a general property from one run. If it matters, rerun the probe 3x; that is
cheap and turns a sighting into a rate.

---

## Q3

Abstract-only. That is a legitimate source, but it is a *different* source from
the paper, and the row has to say so — the abstract is the authors' summary of
their own result, with the method, the sample, the baseline and the caveats
stripped out. Effect sizes in abstracts are systematically the most favourable
framing of the result.

```
id:            C-015
claim:         <the effect, stated exactly as the abstract states it, with the
               percentage and the direction — e.g. "X reduces Y by 37%">
source:        <Authors>, "<Title>", <Venue/Journal>, <Year>. DOI <doi>.
               URL <url>.
locator:       ABSTRACT ONLY — abstract, sentence <n>. Full text paywalled;
               body, methods, tables and limitations NOT read.
quote:         "<verbatim sentence from the abstract carrying the percentage>"
source type:   peer-reviewed paper (abstract only)
date fetched:  2026-08-30
evidence:      the percentage is the authors' headline figure. NOT verified:
               sample size, population, baseline/comparator, whether the figure
               is absolute or relative, effect direction under subgroups,
               confidence interval, and whether the abstract's number matches
               the body's tables.
verdict:       UNVERIFIED (abstract-only; upgradeable to MEASURED on full-text read)
use in skill:  may be cited ONLY as "<Authors> report <figure> (abstract; full
               text not read)". MUST NOT be used as the basis for a threshold,
               a default value, or a numeric recommendation in the procedure.
next action:   attempt full text — preprint/arXiv/institutional repository,
               author copy, or library access. If obtained, re-verify the
               percentage against the results section and either upgrade this
               row or record the discrepancy.
open question: is the percentage relative or absolute? Abstracts routinely omit
               this and it changes the meaning by an order of magnitude.
```

Decisive part: **a number from an abstract does not get to set a threshold in
the skill.** It can motivate; it cannot calibrate.

---

## Q4

Do not average them. Do not pick the one that suits us. Do not quietly drop
one. 15 and 40 are not noise around 27 — a 2.7x gap almost always means the two
sources are measuring *different things*, and the interesting content is the
reason for the gap, not the midpoint.

The cleanup:

**1. Collapse to one row per claim, with the conflict on the row.** The mess is
usually caused by each source having been given its own row, so the file reads
as two facts when it holds one disputed fact.

```
id:            C-007
claim:         <the quantity>, DISPUTED. Reported as 15% by [S1] and 40% by [S2].
verdict:       DISPUTED — do not cite a single figure.
  [S1] <cite>, <locator>, fetched <date>. Figure: 15%.
       measured over: <population / window / denominator, as stated by S1>
       method: <how S1 got it>
  [S2] <cite>, <locator>, fetched <date>. Figure: 40%.
       measured over: <population / window / denominator, as stated by S2>
       method: <how S2 got it>
gap analysis:  candidate explanations, in the order I would check them —
               (a) different denominator (share of teams vs share of repos vs
                   share of PRs);
               (b) different population (all teams vs teams who already adopted
                   the practice — a selection effect);
               (c) different window or vintage (one is 2023 data, one 2026);
               (d) different definition of the thing being counted;
               (e) one is a vendor reporting on its own product.
status:        unresolved — <which of (a)-(e) I could and could not rule out
               from the sources as read>
use in skill:  cite as a RANGE with both sources ("reported between 15% and 40%,
               depending on <the axis that explains the gap>"), or omit the
               number entirely and make the claim qualitative. Never a point
               estimate. Never an average.
```

**2. Tidy the rest of the file with the same rule that produced the fix:**
one row per claim, sources nested under it; every row carries locator + fetch
date + verdict; verdicts from the same fixed vocabulary; rows sorted so the
DISPUTED and UNVERIFIED ones are visible rather than buried.

**3. Say what changed.** A short note at the top of the file: what was merged,
what was demoted, and that C-007 is now disputed — so the next reader does not
re-discover the conflict and "fix" it by averaging.

If a point estimate is genuinely needed downstream, that is a new task
(get a third, better source), not something to resolve by editing this file.

---

## Q5

Not yet — three checks first, and they take minutes.

**1. Are any verdicts UNVERIFIED?** If a claim is going into a reference file
that other work will lean on, "I checked it and could not confirm it" is a
result, not a blocker — but it must ship *labelled*, and it must not be used to
set any number or threshold. If instead the answer is "I have not got to that
one yet", it does not go in the bundle at all. Bundling is where labels get
lost, so the labels have to be right before, not after.

**2. Is each verdict backed by a locator, not a recollection?** For every row I
want the specific thing that was checked: page/section/sentence for a document,
`file:line` for code, the table for a number, the run-id for an observation.
A verdict of "verified" with no locator is an assertion about your memory of
the source, and it is exactly the kind that survives into the file and cannot
be re-checked by anyone else six weeks later.

**3. Did any verdict come back *negative* — source does not support the claim,
or supports a weaker version?** Those are the highest-value rows in the set and
the ones most likely to be quietly dropped during bundling. They stay in, with
the correction recorded, so the same claim does not get re-proposed next month.

Also, briefly: each row keeps its **source type and fetch date** through the
bundle (a reference file where a blog post, a paper abstract and an own probe
read identically is worse than no reference file), and the verdicts use one
fixed vocabulary rather than free text.

If those three come back clean — verdicts all resolved or explicitly labelled,
every one carrying a locator, negatives retained — then yes, bundle it, and the
bundle carries a one-line header saying who verified it and on what date, so
the whole file has a shelf life rather than looking permanently current.

---

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-knowledge.without.txt` (the prompt itself)
- `/home/user/skills-repo/CLAUDE.md` (loaded automatically as project instructions; not opened for this task)
- No skills were invoked and no files under `pipeline/skills/`, `pipeline/contracts/` or `pipeline/build/` were read. Answers are from my own judgement.
