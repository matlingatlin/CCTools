# skill-knowledge — round 2 (with method)

## Q1

Added as a **repeated** row, not a measured one. "In our experience" plus "roughly in half"
is an assertion with no study, no dependent variable, no sample — the verdict is not decided
by how confident the sentence sounds. It still earns a row: repeated is a verdict, not a
rejection.

**Claim row**

| Field | Value |
| --- | --- |
| claim | Adding a linting step to CI roughly halves code review time. |
| source id | S-01 (engineering blog post — fill title + URL; must be unique in the source list) |
| locator | Whole document — post was read in full; the sentence was not recorded to a section. Locator stays "whole document" rather than being invented. |
| quote | "In our experience, teams that add a linting step to CI cut review time roughly in half." |
| what was measured | — (not a measured row; "review time" is never defined in the source: wall-clock to approval? reviewer minutes? rounds?) |
| effect and sample | — (no n, no teams counted, no before/after baseline; "roughly in half" is the whole of it) |
| limits | The source states none. The phrase "in our experience" is the author's own scope marker: one org's practice, not a study. |
| verdict | repeated |
| verified by | *(empty — I gathered it, so I do not rule on it)* |

**Source row**

| Field | Value |
| --- | --- |
| source id | S-01 |
| reached how | supplied by colleague / opened directly (not a search result) |
| read how much | read in full |
| date fetched | 2026-08-30 |

**Expiry condition:** wrong the moment a controlled before/after measurement of review time
with lint-in-CI turns up — that finding would supersede this row, not sit beside it. Also
wrong if the post is edited or withdrawn.

One caveat on the verdict word: "repeated" means asserted-without-measurement. This is
currently **one** assertion, not a widely-repeated one. It does not get promoted by finding
four more blog posts saying the same thing.

## Q2

**Coverage check first — and the answer is logged either way.**

The nine claims we hold were gathered at proposal stage: they are what made the artefact
worth building. That is a different question from what the probe's failures show is missing,
and it could not have been asked until now. So each failure is checked against the nine
before anything is fetched.

**Coverage log** (this is the artefact; both rows are written even though one is a skip)

| # | Observed failure | Covered by the nine? | Decision | Reason (recorded) |
| --- | --- | --- | --- | --- |
| F1 | Agent did not check whether the migration held a lock past the request timeout | No — the proposal-stage claims argue *that* online migrations are risky; none of them carries a lock-acquisition or timeout figure the agent could have checked against | **Fetch**, bounded | The gap is a missing fact (what lock a given DDL takes, and how lock waits interact with statement/request timeouts), and no claim in hand supplies it |
| F2 | Agent did not name which service read the renamed table | Yes, in the sense that matters — this is not a knowledge gap at all | **Skip fetch** | Nothing external could have told the agent which of *our* services read that table. The failure is a missing **step** in the method (enumerate readers before renaming, from the codebase/grants/query logs), not a missing claim. Fetching here would produce adjacent-interesting rows that answer nothing observed. |

Recording F2's skip is the point: a skipped fetch and a fetch nobody thought of leave the
same trace in a log that only records what happened.

**Bounded question list (F1 only)**

1. Which lock does the DDL in question acquire, and does it block reads, writes, or both?
2. Does a blocked DDL waiting on a lock also queue every subsequent statement on that table?
3. What setting bounds the wait (lock timeout / statement timeout), what is its default,
   and how does that default compare with our request timeout?
4. Is there a documented lock-free or concurrent variant of this operation?

**Out of scope, with a reason each**

- General migration-tooling comparisons (Flyway vs Liquibase vs bespoke) — no observed
  failure is about tooling choice.
- Replication lag and failover behaviour — adjacent and interesting; the probe did not fail
  on it.
- Zero-downtime deploy patterns in general (expand/contract) — already owned elsewhere in the
  library; not a knowledge gap.
- Benchmarks of migration duration — the failure was about lock *hold* vs timeout, not speed.
- Anything about F2 (dependency discovery) — closed above as a method gap, not a fetch.

Then: rows not prose, quote-or-it-isn't-a-finding, verdicts measured/repeated, someone other
than the gatherer verifies, dates and expiry conditions on every row. Nine existing claims
are re-sorted by verdict when the new rows merge in; duplicates merged, contradictions kept.

## Q3

The abstract states the effect. It does not make the row **measured**. "Found through a search
engine" and "read in full" are different fields for exactly this case: an abstract can tell me
a number was reported, but it cannot tell me what was measured, on what sample, or what the
paper says it does not establish. So the row goes in as **repeated**, with the percentage
quoted verbatim, and an explicit expiry that flips it to measured once someone reads the
full text.

**Claim row**

| Field | Value |
| --- | --- |
| claim | *(the effect exactly as the abstract states it — one sentence, no rounding, no rephrasing of the direction)* |
| source id | S-02 (paper; DOI + title — DOI is the join key, it is stable and the URL is not) |
| locator | Abstract |
| quote | *(verbatim sentence from the abstract, including the percentage as written)* |
| what was measured | **Unknown from the abstract** — the dependent variable, its operationalisation and the comparison condition are in the methods section, which is paywalled. Left empty, not guessed. |
| effect and sample | Effect as stated in the abstract: *(the percentage, verbatim)*. Sample: **not available** — no n, no population, no design visible. |
| limits | Not available: an abstract does not carry the authors' own statement of what the study does not establish. Recorded as unavailable, not as "none". |
| verdict | **repeated** — the abstract asserts a measurement; nobody in this process has read one. |
| verified by | *(empty)* |

**Source row**

| Field | Value |
| --- | --- |
| source id | S-02 |
| reached how | search result / database listing |
| read how much | **abstract only — full text paywalled** |
| date fetched | 2026-08-30 |

**Expiry condition:** promote to `measured` when the full text is obtained (institutional
access, preprint, author copy, interlibrary request) and the methods section is read — at
which point `what was measured`, `effect and sample` and `limits` get filled and the row is
re-verified. Also wrong if the paper is retracted or corrected. Until then, no downstream
document may cite this as a measured effect.

If a verifier can only reach the abstract too, the honest return is **not checkable** for the
measured half — that is a result, not a hole in the process.

## Q4

I am not cleaning that up, because the mess is the finding. Two sources disagreeing 15 vs 40
is the most load-bearing thing in the file, and picking one, averaging them, or writing "15–40
percent" is the one edit nobody can detect afterwards — the reference stops recording that a
disagreement exists.

What I do:

1. **Both rows stay, as separate rows**, each with its own source id, locator, quote, verdict,
   and fetch date. Neither is deleted, merged, or softened.
2. **Mark the contradiction explicitly** so a reader cannot miss it — a `contradicts` field on
   each row naming the other's source id, or a short "Contradictions" block at the top listing
   the pair. It is stated, not resolved.
3. **Ask whether they are even the same quantity** before calling it a contradiction. Different
   denominator, different population, different time window, or different definition of the
   thing being measured turns "15 vs 40" into two compatible claims about two different
   quantities — in which case the fix is a sharper `claim` sentence on each row, and they still
   both stay.
4. **Merge only true duplicates** — the same claim from the same source reached twice.
5. **Sort by verdict**, measured before repeated, so a reader sees what was measured first.
   If one of the two is measured and the other repeated, the ordering already tells the reader
   which one carries weight — without either being deleted.
6. **Date each source and give each claim its expiry condition.** For this pair the natural
   expiry is: "resolved if a source is found that measures both populations on the same
   definition."

Shape of the cleaned section:

```
## Contradictions
- C1: effect size for <X>. S-03 reports 15%; S-07 reports 40%. Unresolved as of 2026-08-30.
      Same definition? not established. Do not cite a single figure for <X>.

## Claims — measured
| claim | source | locator | quote | measured | effect & sample | limits | verdict | verified by |
| <X> is 15% ... | S-03 | Table 2 | "..." | ... | 15%, n=... | ... | measured | R. |
## Claims — repeated
| <X> is 40% ... | S-07 | §4 | "..." | — | 40%, no n | — | repeated | R. |
```

The only thing that actually gets tidied is formatting and duplicate rows. The disagreement
survives the cleanup by design.

## Q5

Not ready — one blocker, and it is structural rather than a comment on your work.

**You cannot verify your own gathering.** The verdicts you produced are the gatherer's
proposed verdicts. They go in the file as proposals with `verified by` still empty. Verification
means someone else is handed the claim row and the source — and *only* those. Not your
reasoning, not what the skill is for, not which way the claim needs to come out; anything that
signals the wanted answer stops it being a check.

So the sequence before bundling:

1. Keep your verdicts, relabelled as proposed. Nothing is discarded.
2. Hand each row + its source to someone who did not gather it.
3. They return exactly one of: **supported** · **not supported** · **not in the source** ·
   **source unreachable** · **not checkable**. `source unreachable` and `not checkable` are
   results — they get recorded as verdicts, they are not retried until they turn into
   something nicer.
4. Partial outcomes get their own note: the finding held but the mechanism as stated was wrong
   is a real and common result, and both halves are worth writing — the claim earned its keep,
   and quoting it as stated would have shipped an error.
5. Anything without a verbatim quote does not proceed at all. No quote, no finding — a
   verifier handed a row with no quote can only re-do the gathering.
6. Then reconcile: merge duplicates, keep contradictions as their own rows, sort measured
   before repeated, confirm every source carries its fetch date and every claim its expiry
   condition.

Two things to check on your own pass while that is happening, since they are cheap: that no
row's verdict is `measured` unless someone actually read the study (an abstract does not
qualify), and that the coverage-check log records the fetches that were *skipped*, not only
the ones that happened.

Send me the rows and the sources and I will verify them — I did not gather them.

**In this repo:** rows and their verification outcomes append to `pipeline/ledgers/claims.jsonl`;
the verified findings land in `knowledge/notes/` in the same turn they are verified. (Not
written here — this run was told to write only this file.)

## consulted

- `/home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-knowledge.with.txt` (the prompt, its embedded method, and the bundled `references/claim-rows.md`)
- `/home/user/skills-repo/CLAUDE.md` (already in context; ledger and `knowledge/notes/` paths used in Q5)
- No skills invoked, no other files or tools opened, no network fetches.
