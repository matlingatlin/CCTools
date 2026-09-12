# skill-knowledge — with-method run r1

## Q1

Added as one claim row plus its source row. It goes in as **repeated**, not measured: "roughly
in half" is a number inside an assertion ("in our experience"), not a measurement. There is no
dependent variable, no sample, no baseline and no window, so nothing can be recorded in the
measured fields. A figure does not promote a row.

### Claim row

| Field | Value |
| --- | --- |
| claim | Adding a linting step to CI approximately halves code review time. |
| source id | S-lint-ci-blog |
| locator | Whole document (read in full); the sentence sits in the body's "in our experience" paragraph |
| quote | "In our experience, teams that add a linting step to CI cut review time roughly in half." |
| what was measured | — nothing. "Review time" is never defined or instrumented in the source. |
| effect and sample | — none given. No n, no teams counted, no before/after window, no baseline. |
| limits | The source frames it as the authors' own experience and states no method, no population and no measurement procedure. |
| verdict | repeated |
| verified by | *(empty — I gathered it, so I do not rule on it; goes to an independent verifier with the row and the source only)* |
| expires if | the post is updated to publish or link an underlying measurement (then re-file as measured), or the CI/lint tooling it describes is superseded |

### Source row

| Field | Value |
| --- | --- |
| source id | S-lint-ci-blog |
| kind | engineering blog post (vendor/practitioner, not peer reviewed) |
| how reached | *(fill: the link/search/referral that led here — this field is not the next one)* |
| how much read | read in full |
| date fetched | 2026-08-30 |

Two things I deliberately did not do: I did not write "cuts review time ~50%" as a headline
number anywhere without the quote beside it, and I did not upgrade the verdict because the claim
is plausible and commonly said. Being asserted more often is not promotion.

## Q2

Coverage check first — and the answer gets logged either way, including the skips. The nine
proposal-stage claims answer a different question (what made the idea worth building); the
observed failures are the second question, and it can only be asked now. So:

### Step 1 — coverage table (fill against the nine, one row per observed failure)

| Failure | Do the 9 claims in hand cover it? | Decision | Reason logged |
| --- | --- | --- | --- |
| F1: agent did not check whether the migration held a lock past the request timeout | claim ids that speak to lock duration / statement timeouts / blocking DDL → *(list or "none")* | fetch / **skip** | if skipped: "covered by C-n, which already states the lock-hold check and its threshold" |
| F2: agent did not name which service read the renamed table | claim ids that speak to identifying readers/consumers before a rename → *(list or "none")* | fetch / **skip** | if skipped: "covered by C-n" |

A skipped fetch and a fetch nobody thought of leave the same trace unless the skip is written
down. Both rows land in the record regardless of outcome.

### Step 2 — bound the questions before searching (only for failures that came back "not covered")

Questions:
- Q-a. How long can a schema migration hold a lock, and what makes it exceed a request timeout — which DDL forms block, and what lock-timeout / statement-timeout settings bound it?
- Q-b. What is the check that establishes lock hold time *before* the migration runs (dry-run, lock_timeout probe, transaction inspection)?
- Q-c. How does one enumerate the readers of a table before renaming it — code search, query logs, catalog/dependency views, service-to-table maps?
- Q-d. What evidence counts as "the readers are named" — i.e. what would have made the agent's answer pass?

Out of scope, with a reason each:
- Migration *rollback* strategy — no observed failure touched it; interesting, not evidenced.
- Expand/contract or dual-write sequencing — that is the fix pattern, not the missing knowledge; the probe failed at *checking*, not at sequencing.
- Connection-pool sizing and general DB performance tuning — adjacent to timeouts, not implicated by either failure.
- Which specific database engine is best — a product choice, not a claim the probe asked for.
- Anything about the agent's prompt wording — a build change, not knowledge.

Without the second list every adjacent finding will look like it belongs, and the claim set
doubles with material no failure asked for.

### Step 3 — gather as rows, not prose

Every finding for Q-a…Q-d enters as a claim row (claim / source id / locator / quote / measured
fields / limits / verdict / verified by), with each source carrying its fetch date and each claim
its expiry condition. No verbatim line → not a finding, it does not enter. Verification goes to
someone who did not gather it.

## Q3

The row can be written, but not as **measured**, and it cannot be closed with what you have.

An abstract read through a paywall and a paper read in full are both "found" — only the second
can support a measured claim. The abstract gives the effect but not what was measured (the
operational definition), not the sample, and not the limits the paper states about itself. Those
are exactly the fields a measured verdict is made of.

### Claim row

| Field | Value |
| --- | --- |
| claim | *(one sentence, the finding as the abstract states it)* |
| source id | S-paper-01 |
| locator | Abstract |
| quote | **REQUIRED — paste the verbatim sentence from the abstract. Without it this row does not enter the set.** |
| what was measured | unknown from the abstract — the dependent variable and its operationalisation are in the methods section, which was not read |
| effect and sample | effect: the percentage as stated in the abstract, verbatim. sample: **not available** — no n, no population, no design from the abstract alone |
| limits | not available; the paper's own statement of what it does not establish is not in the abstract |
| verdict | **repeated** |
| verified by | *(empty — independent verifier, handed this row and the source only)* |
| expires if | the full text is obtained (then re-verdict: measured if methods and sample check out, or not supported if they do not), or a correction/retraction is issued |

### Source row

| Field | Value |
| --- | --- |
| source id | S-paper-01 |
| how reached | found via search / citation *(fill exactly)* |
| how much read | **abstract only — paywalled, full text not obtained** |
| date fetched | 2026-08-30 |

The honest options if this claim has to carry weight: get the full text (institutional access,
preprint/author copy, request from the author) and re-verdict, or leave it repeated and do not
let it be quoted with the number as if it were established. Do not write the percentage into the
skill's prose as a measured figure; a number lifted from an abstract reads identically to one
lifted from a read paper, and that is precisely the difference this record exists to keep.

## Q4

The contradiction stays. Cleaning up means merging true duplicates and sorting by verdict — it
does not mean picking a side, averaging to ~27%, or writing "15–40%". Collapsing a contradiction
is the one edit nobody can detect afterwards, because the losing row is simply gone.

Reconciled file, contradiction kept as two rows and flagged as a pair:

| # | claim | source id | locator | quote | what was measured | effect and sample | verdict | verified by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | *(the 15% finding, as its source states it)* — **contradiction pair X, see #2** | S-a | *(section/table)* | *(verbatim)* | *(dependent variable — likely NOT the same as #2; check first)* | 15%, n=… | measured | *(independent verifier)* |
| 2 | *(the 40% finding, as its source states it)* — **contradiction pair X, see #1** | S-b | *(section/table)* | *(verbatim)* | *(dependent variable)* | 40%, n=… | measured | *(independent verifier)* |
| 3… | *(remaining rows)* | | | | | | measured, then repeated | |

Rules applied:
- **Duplicates merged** only where claim + source + locator are genuinely the same row entered twice; keep the fuller quote and both source ids if two ids point at one source.
- **Contradiction kept as its own two rows**, cross-referenced by a pair tag, so a reader meets both.
- **Sorted by verdict**: measured rows first, repeated after, so what was measured is read before what is merely asserted.
- **Each row keeps its fetch date and expiry condition**; a contradiction pair's expiry is "resolved when a source is found that measures both under the same definition".

Before anything else, check the cheap explanation: compare the "what was measured" fields. Two
numbers for "the same thing" are very often two different dependent variables, populations or
windows — if so it is not a contradiction at all and both rows stand with their scopes made
explicit in the claim sentence. If they really do measure the same thing the same way, the
disagreement is the finding, and the skill should carry it as a range with both sources named,
not as a single number.

## Q5

Not ready. You gathered these, so your pass over them is not verification — it is the gatherer
checking their own gathering, which is the one thing the step exists to prevent. Your verdicts
are useful as a pre-pass (they catch your own typos and mis-locators); they do not close a row.

What happens next:

1. **Verified-by stays empty** on every row until someone else rules. Your verdicts go in a
   separate "gatherer's pre-pass" column, or are discarded — they must not silently become the
   verified column.
2. **Hand the verifier the claim row and the source. Nothing else.** Not your reasoning, not the
   skill the claims were gathered for, not which way you expect it to go, not the failure the
   claim is meant to answer. Any of those tells them which answer is wanted.
3. **They return one of five per row:** supported · not supported · not in the source · source
   unreachable · not checkable. The last two are results and get recorded as results — do not
   send the row back around until it comes up "supported".
4. **Partial outcomes get their own note** — e.g. the finding holds but the mechanism the row
   states is not what the source says. Both halves matter: the claim earned its keep, and
   quoting it as written would have propagated an error.

Pre-flight I would run before handing the batch over, since it costs a minute and saves a round:
- every row has a verbatim quote (no quote, no finding — drop or fetch);
- every source has a fetch date, and "how reached" and "how much read" are filled separately;
- measured rows actually carry what was measured, the effect and the sample — otherwise they are repeated;
- every claim has an expiry condition;
- contradictions are still present as separate rows.

Once verdicts come back from the verifier, reconcile into one set (merge duplicates, keep
contradictions, sort by verdict) and *then* bundle into the reference file — and the verified
findings land in the notes in that same turn, not when someone next asks for them.

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-knowledge.with.txt` — the method and the bundled `references/claim-rows.md` supplied in the prompt.
- Repo standing rules already in context (`/home/user/skills-repo/CLAUDE.md`): the MEASURED/REPEATED verdict rule and "a verified fact lands in the notes in the same turn it is verified".
- No other files opened, no tools or web fetches used.
