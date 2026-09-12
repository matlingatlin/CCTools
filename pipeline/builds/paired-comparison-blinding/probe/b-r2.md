## T1

Scoring two sets of outputs over the same 12 tickets is a paired comparison. Set it up so the
score measures the prompt and not the grader's expectations.

**Set-up (do this before any grading happens)**

1. Pair by ticket: 12 pairs, each = {old output, new output} for the same input.
2. Blind and randomise per pair. For each ticket, coin-flip which output is shown as **A** and
   which as **B**, and record the assignment in a key file the grader never sees. Strip anything
   that leaks the version: file names, headers, "v2", trailing whitespace/formatting quirks that
   differ systematically between runs, model-name mentions inside the text.
3. Fix the decision rule in writing NOW: primary metric = share of pairs where the new prompt
   wins, ties counted as half. Pre-declare what result means "adopt the new prompt". With 12
   pairs the honest bar is high — see the power note below.
4. Grade each pair twice with the presentation order flipped (24 judgements). Disagreement between
   the two orders on the same ticket = position bias / genuine tie, and both are useful to know.
5. Unblind only after all judgements are written down.

**Grading prompt (usable as-is, one call per pair)**

```
You are comparing two candidate summaries of the same customer support ticket.
You do not know which system produced which; do not speculate.

TICKET
<<<{ticket_text}>>>

SUMMARY A
<<<{a_text}>>>

SUMMARY B
<<<{b_text}>>>

Judge on these criteria, in this priority order:
1. Factual faithfulness — every claim is supported by the ticket; no invented details.
2. Completeness — the customer's actual problem, what was tried, and the current state.
3. Actionability — a colleague could pick up the ticket from the summary alone.
4. Concision — no filler, no restating the ticket verbatim.

Do not reward length, formatting, or confident tone for their own sake.

Output JSON only:
{"faithfulness": "A"|"B"|"tie",
 "completeness": "A"|"B"|"tie",
 "actionability": "A"|"B"|"tie",
 "concision": "A"|"B"|"tie",
 "overall": "A"|"B"|"tie",
 "reason": "<=40 words, cite the specific difference that decided it",
 "unsupported_claims_A": ["..."],
 "unsupported_claims_B": ["..."]}
```

**Who grades.** A human on 12 pairs is affordable (~30-45 min) and is the reference. If a model
grades, calibrate it first: have a human do 4-5 pairs blind, check the model agrees on those,
and report that agreement rate alongside the result. An uncalibrated judge score is not evidence.

**Tally.** Wins/losses/ties, plus a two-sided sign test on the non-tied pairs. Flag it up front:
12 pairs is small. 9-3 gives p≈0.15; even 10-2 is p≈0.04 — one flipped ticket changes the verdict.
So expect the outcome to be "adopt / keep / need more tickets", and if it lands near the middle
the answer is to grade more tickets, not to argue about the twelve.

**Also report:** per-criterion breakdown (a new prompt that wins on concision and loses on
faithfulness is not better), the order-flip disagreement count, and every ticket where a judge
flagged an unsupported claim — those are worth reading individually regardless of the tally.

## T2

Two things to settle before writing anything: was the comparison blind and order-randomised, and
who/what was the reviewer. If the reviewer knew which side was the new prompt, the write-up has to
say so, because that result cannot be separated from expectation.

5 of 6 with a single reviewer is a weak signal, and the write-up should say that plainly. Two-sided
sign test on 6 pairs: 5-1 gives p = 0.22. That is the kind of split you get from a coin about one
run in five. It is not a null result and it is not a green light; it is a reason to run more pairs.

**Draft for the team:**

> **Summariser prompt comparison — interim result**
>
> **What we did.** One reviewer compared 6 pairs of outputs, one pair per ticket, same input to both
> versions. [Blinding: labels randomised per pair, reviewer did not know which version produced
> which / NOT blinded — state which.] Criteria: faithfulness, completeness, actionability, concision.
>
> **Result.** Answer B — [version name] — was preferred in 5 of the 6 pairs.
>
> **What that supports.** B is plausibly better, and nothing suggests it is worse. That is the whole
> of it. With 6 pairs, a 5-1 split has a two-sided p of 0.22: if the two versions were actually
> equivalent, we would see a split this lopsided about 22% of the time. One reviewer also means no
> read on whether a second person would agree.
>
> **What it does not support.** "B is better" as a settled fact, a percentage improvement, or a
> ship decision on its own.
>
> **Recommendation.** Extend to ~25-30 pairs (blind, order-randomised) before deciding; that gets a
> real result out of the same 5:1 rate. If we need to decide this week, ship B provisionally — the
> evidence leans that way and the downside is low — and label it provisional in the changelog.
>
> **Worth reading anyway:** the one pair where A won, and the reviewer's stated reason on each pair.
> Six comments are cheap to read and often more informative than the count.

If the reviewer was not blinded, add a line: "Reviewer knew which version was which, so preference
may partly reflect expectation; the re-run should be blinded."

## T3

This script performs the unblinding. If it is wrong, every number downstream is wrong and nothing
downstream looks broken — the tally will be confidently reversed. So the tests are mostly about
loud failure and about not losing or duplicating rows.

**Core correctness**

1. Happy path: a 3-item map, 3 scored labels → each score lands on the right version.
2. Round-trip: blind(unblind(x)) == x for a generated mapping; and unblind is the exact inverse of
   the blinding step's own output (feed the blinder's real output, not a hand-written fixture).
3. Count conservation: rows out == rows in. No score is dropped, none is duplicated.
4. Order independence: shuffle the input rows, get the same mapping (compare as sets/sorted).
5. Idempotence guard: running the mapper on already-unblinded output either errors or is a no-op —
   never maps twice.

**The failure modes that silently corrupt results**

6. Unknown label in the scores (typo, extra row) → raises/exits non-zero. Must NOT skip the row.
7. Label in the map with no score → raises or is reported explicitly as missing, not silently absent.
8. Duplicate label in the map file → error. A non-bijective map is the single worst bug here.
9. Two labels mapping to the same version *within one pair* (both A and B marked "new") → error.
10. Wrong map file for this run: the map carries a run id / input hash; a mismatch aborts. This
    catches the classic "reused yesterday's key" and it is the test most worth having.
11. Off-by-one/positional assumption: give the map and the scores in different orders — if the code
    joins by position instead of by label the test must fail. Construct the fixture so a positional
    join produces a *plausible but wrong* answer, not a crash.

**Input hygiene**

12. Label normalisation: whitespace, case, BOM, quoted CSV fields — decide the policy and test it,
    including that "a " and "A" do not silently collide if the policy is case-sensitive.
13. Ties / blank / non-numeric scores pass through unchanged rather than being coerced to a winner.
14. Empty input → empty output plus a warning, not a crash and not a silent success.
15. Malformed map file (missing column, bad JSON/CSV) → clear error naming the file and line.

**Property test worth the ten minutes**

For a random permutation mapping over N pairs and random scores: unblinding then re-tallying by
version equals tallying the pre-blinded ground truth. Run it over many random seeds; this catches
the whole class of "correct on the fixture, wrong on a different permutation" bugs, including the
symmetric case where a bug that swaps every label looks fine on a 1-item fixture.

**Sanity assertion to build into the script itself, not just the tests:** if every single pair
resolves to the same version winning, print a warning — that is more often an inverted or constant
map than a landslide.
