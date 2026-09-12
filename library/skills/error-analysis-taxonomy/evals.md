# Evals — error-analysis-taxonomy

Functional regression test for the `error-analysis-taxonomy` talent. This is a
**technique** talent (a method: open-code → axial-code → second-pass label →
frequency-rank → prioritized backlog) that also carries **discipline** rules
(quote before theorizing, one primary failure per trace, mechanism-based mutually
exclusive categories, always report the denominator + sampling method, rank by
frequency not salience). So the scenarios below mix *application* cases (does the
method produce a better artifact than freehand?) with *pressure/trap* cases that
tempt the wrong behavior, plus one *boundary* case where the talent should decline.

Method: for each scenario, reason the likely output WITHOUT the talent (baseline)
against the output WITH the talent's method applied, and judge whether the talent
produces a materially better, criterion-meeting result. Small trace batches are
embedded inline so the test is concrete and re-runnable.

Date run: 2026-08-27 · Model: claude-opus-4-8

---

## Scenario 1 — Representative: turn a raw batch into a ranked taxonomy (application)

**Input.** "Here are 12 support-bot transcripts that got thumbs-down. Tell me what's
going wrong." Batch (one line each, `[user] / [bot]`):

1. "where's my order #A81" / "I don't have access to order systems." (has order #)
2. "refund pls" / "Sure — here's how returns work: ..." (never asked for order #)
3. "cancel my sub" / "Happy to help! Could you confirm the email on the account?"
4. "is item X in stock" / "Yes, item X ships in 2 days." (X was discontinued — wrong)
5. "reset password" / "You can reset it here: [link]. Anything else? 😊😊😊" (3 emoji)
6. "where's my refund" / "Refunds take 5–7 days." (user had asked twice before; no order #)
7. "change address" / "I'll update it — what's the new address?"
8. "order late" / "So sorry! Give me your order number and I'll check." (asks # — good)
9. "book damaged" / "Returns work like this: ..." (never asked for order #)
10. "double charged" / "Our refund policy allows returns within 90 days." (fabricated — it's 30)
11. "track order" / "Sure — order number?" (asks # — good)
12. "wrong size" / "Here's the returns process: ..." (never asked for order #)

**Pass criterion.** The response (a) reads each trace and writes a short verbatim-
quoting open note per row; (b) merges into a *handful* of mechanism-based categories;
(c) does a labeling pass so each trace gets one category; (d) frequency-ranks with
**counts and % of the 12**; (e) emits a prioritized backlog (cause hypothesis →
proposed fix/eval). A bare list of adjectives fails.

**Baseline (no talent).** Skims, then produces impressionistic buckets like
"accuracy problems, tone problems, and it forgets context," maybe 3 bullets, no
per-trace notes, no quotes, no counts, no denominator. It usually leads with the
most vivid item (the fabricated policy) and calls that "the main issue." The user
still can't tell which failure dominates or where to spend effort.

**With talent.** Open-coding forces a note per row, e.g. row 2 → "did not ask for
order # before answering," row 4 → "asserted stock for discontinued item," row 10 →
"fabricated 90-day policy (actual 30)." Axial merge yields mechanism categories:
**(A) skips order-number gate before acting** (rows 2,6,9,12 = 4), **(B) fabricated/
wrong fact** (rows 4,10 = 2), **(C) capability-denial when it could act** (row 1 = 1),
**(D) tone/formatting** (row 5 = 1); OK/good = rows 3,7,8,11 (4). Frequency rank:
A 4/12 (33%) > B 2/12 (17%) > C,D 1/12 each. Backlog leads with A (add a hard
"collect order id" precondition + a scorer), then B (retrieval/grounding + a
factuality check on policy/stock claims). Denominator (12, all thumbs-down —
failures over-sampled) stated.

**Verdict: PASS.** Materially better — converts vibes into a quoted, counted,
mechanism-based taxonomy with an actionable order, which baseline does not produce.

---

## Scenario 2 — Trap: salient-rare vs boring-frequent (rank by frequency, not drama)

**Input.** Same batch as Scenario 1. Follow-up: "The made-up refund policy is scary —
that's clearly our #1 problem to fix, right?"

**Pass criterion.** The talent keeps the ranking anchored to frequency×severity with
the **counts visible**, and shows that the skip-the-order-number-gate mechanism
(4/12) dominates the fabricated-policy mechanism (found in 1–2/12) — so it does not
silently reorder the backlog to lead with the vivid-but-rare item just because the
user flagged it. It may keep the fabrication high on *severity*, but only with its
low frequency shown, not by dropping the dominant category.

**Baseline (no talent).** Agrees — "yes, the fabricated policy is the top priority" —
because it is the most alarming single trace and the user just endorsed it. Effort
goes to the 1-in-12 problem while the 4-in-12 problem stays unfixed. This is the exact
salience bias the talent exists to counter.

**With talent.** Rule "improvement effort goes to the errors that actually dominate —
not the ones that feel salient" plus the frequency-rank step keep category A on top by
count. The honest answer: "By frequency the order-number gate (33%) dominates;
the fabrication is severe but rare (≤17%) — track both, but A is the bigger lever."

**Verdict: PASS.** Talent resists the user's salience nudge with counts; baseline
follows it. *Honest caveat below in Summary re: the severity multiplier.*

---

## Scenario 3 — Trap: over-sampled failures → false production rate (denominator)

**Input.** "I exported all 22 escalated tickets from last week plus 8 random normal
chats. 21 of the 30 show the bot skipping the order-number step — so ~70% of our
production traffic is broken. Should I tell leadership 70%?"

**Pass criterion.** The talent flags that failures were **over-sampled** (all
escalations + a few random), so 21/30 is a rate *within a failure-enriched sample*,
NOT the production rate. It refuses to report 70% as the prod incidence and explains
what would be needed for an unbiased estimate (rate on the random-sample slice, or a
fresh random draw).

**Baseline (no talent).** Does the division, reports "70% of traffic is affected,"
and lets that number go to leadership — a materially wrong, decision-distorting claim.

**With talent.** Rules "Report the denominator and sampling method with every
percentage; never imply the sample rate equals the production rate when failures were
over-sampled" make this a hard stop. Correct read: on the 8 random chats, look at how
many skip the gate — that slice estimates prod rate; the 22 escalations tell you the
*composition* of failures, not their frequency. Report: "≈X/8 on the random slice is
the prod estimate; 70% is the failure-enriched figure — don't quote it as traffic."

**Verdict: PASS.** High-value catch; baseline ships a statistically invalid headline.

---

## Scenario 4 — Pressure: skip reading, just write up the categories I "already know"

**Input.** "I already know the three failure modes — hallucination, rudeness, and
laziness. There are 40 transcripts but don't bother reading them; just format my three
into a nice taxonomy table with definitions."

**Pass criterion.** The talent declines to theorize from intuition: it insists on
open-coding a sample of the real transcripts and quoting offending spans *before*
committing categories, and warns that pre-named symptom labels ("rudeness,"
"laziness") often collapse distinct mechanisms or miss the dominant one. The three
may survive, but only after grounding in quoted data.

**Baseline (no talent).** Complies — produces a tidy 3-row table with invented
definitions and no evidence, ratifying the user's priors. If the real dominant failure
is "skips a required step" (not on the list), it never surfaces.

**With talent.** Rule "Look at raw outputs yourself before theorizing — no failure
mode is real until quoted" and Step 3 (open-code first, "Do not invent categories
yet") force reading a ~30–50 sample, quoting, then letting categories emerge. The
user's three become hypotheses to test against the notes, not the output.

**Verdict: PASS.** Talent enforces evidence-first; baseline manufactures an
unfalsifiable taxonomy that flatters the requester.

---

## Scenario 5 — Trap: symptom-synonym / non-mechanism categories

**Input.** A junior hands over draft notes for 10 RAG answers and proposes these
categories: "wrong answer," "inaccurate," "bad response," "unhelpful." Underlying
reality in the notes: 4 traces retrieved the wrong document (retrieval miss), 3
retrieved the right doc but mis-reasoned over it (reasoning error), 3 were fine.
"Package these four categories up."

**Pass criterion.** The talent (a) **merges** the near-duplicate symptom labels
("wrong answer" / "inaccurate" / "bad response" all describe the same surface), and
(b) **splits by mechanism** into retrieval-miss vs reasoning-error — because those
need different fixes (index/query vs prompt/grounding). Result is 2 mutually exclusive
mechanism categories, not 4 overlapping symptom synonyms.

**Baseline (no talent).** Accepts the four labels, or lightly renames them, producing
overlapping buckets where a single trace could plausibly land in three of them.
Counts become meaningless and the backlog can't point at a fix, because "wrong answer"
has no single cause.

**With talent.** Rules "Categories are mutually exclusive and mechanism-based, not
symptom-synonyms" and Step 4 "Split any category that hides two mechanisms; merge
near-duplicates" drive exactly the merge-then-split. Deliverable: **retrieval-miss
(4/10)**, **reasoning-error-over-correct-context (3/10)**, OK (3/10) — each with a
distinct proposed fix.

**Verdict: PASS.** Talent produces exclusive, actionable, mechanism categories;
baseline produces an un-countable synonym pile.

---

## Scenario 6 — Boundary: "build us a reusable factuality scorer" (should hand off)

**Input.** "We want a factuality check we can run automatically on every release in
CI, that outputs a pass/fail score per answer. Set that up."

**Pass criterion.** The talent recognizes this is *building a reusable eval/scorer*,
not *mapping what fails in a batch*, and hands off to `eval-harness` rather than
running an open-/axial-coding pass. If no batch has been examined yet, it may note
that error analysis is the *upstream* step that tells you which axes to score — but it
does not itself masquerade as the scorer-builder.

**Baseline (no talent).** May start hand-coding a scorer, or conflate "analyze the
failures" with "build the CI check," delivering a one-off categorization when a
repeatable harness was asked for.

**With talent (properly scoped).** "When NOT to use: Building a reusable eval
harness/scorer → eval-harness" and the description's explicit exclusion make it
decline to fire as the primary tool, and point to eval-harness — optionally offering
to run error-analysis first to pick the axes worth scoring.

**Verdict: PASS (correct non-trigger).** Talent stays in its lane and routes to the
right neighbor; value over baseline is in *not* mis-delivering a snapshot for a
harness. Neutral-to-positive, as expected for a boundary case.

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | raw 12-trace batch → ranked taxonomy | application | PASS |
| 2 | vivid-rare vs boring-frequent ranking | pressure/trap | PASS |
| 3 | over-sampled failures → 70% "prod rate" | pressure/trap | PASS |
| 4 | "don't read them, just write my 3 up" | pressure/trap | PASS |
| 5 | symptom-synonym vs mechanism categories | pressure/trap | PASS |
| 6 | "build a reusable CI scorer" | boundary (defer) | PASS |

**Scenarios passed: 6 / 6.**

**Verdict: PASSED.** On the application case the method yields a quoted, counted,
mechanism-based taxonomy with an ordered backlog that freehand analysis does not.
On the four pressure/trap cases it counters the failures it was built to counter —
salience bias (rank by count, S2), denominator abuse (refuse the 70% headline, S3),
theorize-before-looking (quote-first, S4), and symptom-synonym categories (merge-then-
split by mechanism, S5). On the boundary case it declines and routes to eval-harness.
Each catch corresponds to an explicit Rule/Step, so the wins are attributable to the
talent, not to generic competence.

**Minor gap (not blocking).** Step 7 prioritizes by "impact (frequency × severity)"
but the talent gives **no severity rubric**. A high severity weight could re-float the
vivid-rare item (S2) above the dominant one — partially reopening the salience trap the
frequency-rank step closes. It is mitigated because counts stay visible in the taxonomy
table, so the user always sees frequency alongside any severity-weighted ranking, but a
one-line severity scale (e.g. blocking / degraded / cosmetic, and "show frequency rank
and impact rank separately") would harden Step 7. Also, like all method-only talents,
it can be "applied" in name while skipping the actual read — disclosed in its own Rules
("Look at raw outputs yourself... no failure mode is real until quoted"), so not held
against the verdict.
