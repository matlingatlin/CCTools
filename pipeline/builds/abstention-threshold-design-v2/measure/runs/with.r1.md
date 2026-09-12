## Q1

No holdout is attached to this question — just a rate ("wrong on ~1 in 20") and headcount. Per the method, when there's no named, scored, labelled holdout, the answer is not a cut or a coverage band; it's what to pull and who has to agree the target. Four bad answers to this exact kind of question all invented a coverage number ("~40-55%") anyway — I'm not doing that.

**Good news: you already have the holdout, you just haven't pulled it as one.** Every record is reviewed today, so your AP team's correction log *is* model-prediction vs. human-verified-outcome for every one of ~4,000 records/day. Pull the last 4-6 weeks (~80-120k records) as the labelled set, stratified across vendor and document type, and attach the model's per-record confidence score (not a stated "I'm sure" — the actual score/logit it currently produces).

**Fix these before looking at the data, and get them signed, not asserted by me:**
- **Precision target on the auto-approved segment** — proposing 99.5% (invoice errors are money out the door; this needs an AP/Finance controller sign-off, not mine).
- **Coverage floor** — the minimum auto-approve rate for this to be worth shipping. Proposing ≥40%: at 4,000/day and a 6-person team (667/head/day today), anything below that isn't meaningfully changing headcount math. *Both numbers above are proposed by me, unagreed — needs an owner and a date before they're binding.*

**Before trusting the confidence score at all, test it (this is the gate, not a formality):** bucket the pulled holdout by score decile and check accuracy rises with score, and compute AUROC against the human-corrected label. Don't assume it passes — Q3/Q4 below show a model's own stated confidence is frequently close to useless as a ranking signal even though it looks fine in isolation. If the score doesn't separate, no cut on it is defensible at any coverage, and the fix is a better signal (line-item/vendor/PO reconciliation match, schema/validator pass, cross-check against historical vendor amounts), not a lower bar.

**Then**: sweep the cut, take the highest-coverage row that clears 99.5%, check it against the 40% floor, and price anything stricter in coverage points. Everything below the cut keeps going to the same 6-person queue — that queue is the existing, already-sized owner, so this ships as review-load relief, not a new unowned path.

## Q2

Ran it. Signal separates well: **AUROC 0.889**, and decile accuracy rises cleanly from 20% (bottom decile) to 100% (top three deciles) — this score is worth thresholding on.

Swept score-by-score (not a coarse grid) on the full 200-row holdout (`./scored_predictions.csv`, n=200, no locator/date/sampling info beyond the file itself — treat that as a gap if this feeds a real decision):

**Cut = 0.506** is the highest-coverage cut that clears 95% precision.
- Coverage: **55.5%** (111/200 answered)
- Precision on the answered segment: **95.5%** (106/111 correct)
- 95% Wilson CI on that precision: **[89.9%, 98.1%]** — this is the honest caveat: n=111 is thin for a 95%-precision claim, the interval straddles the target. Treat 0.506 as a starting cut with that stated uncertainty, not a constant, until it's re-validated on more traffic.

What a stricter cut costs, for comparison: pushing to 0.602 buys precision 98.8% (CI [93.3%, 99.8%]) but coverage drops to 40% (80/200) — you'd surrender 15.5 points of coverage for 3.3 points of precision you didn't ask for. Nothing below 0.506 is on the table; every row below it dips under 95% at some point on the sweep.

No baseline volume was given for this system, so I can't convert 55.5% into cases/day — if you tell me the daily volume I'll do that arithmetic, and someone needs to own the 44.5% that falls below the cut.

## Q3

**No.**

"90% confident" is the model's *stated* confidence — exactly the signal the method says is a candidate, never a default, until it's tested against real outcomes (step 4 gate). I have real evidence sitting right here that this distrust is warranted: the self-reported confidence data in Q4 (different system, same failure shape) has AUROC **0.482** — indistinguishable from chance — despite every value sitting between 0.79 and 0.99 ("sure" to "very sure"). One decile centered at 0.91-0.93 stated confidence was only 55% accurate; a noisier one at 0.95 hit 85%. The stated number and the actual correctness are not tracking each other.

So "auto-approve at 90% stated confidence" isn't a conservative choice, it's an untested one — it could be filtering nothing, or filtering close to randomly. Before committing to any cut on a model's self-reported number: pull a labelled holdout, bucket by that confidence value, and check accuracy actually rises with it. If it doesn't (as in Q4), don't ship the cut — find a different signal.

## Q4

Ran the same procedure. This signal fails the gate: **AUROC 0.482** (chance), and decile accuracy is flat/non-monotonic — 65%, 75%, 70%, 65%, 75%, 55%, 60%, 85%, 65%, 60% across rising stated_confidence deciles, no trend. Values only span 0.79-0.99, clustered at 0.90 (122/200 rows), so there's barely any spread to threshold on even setting aside that it doesn't separate. Overall accuracy is 67.5%.

Swept it anyway for completeness: **no cut on this signal reaches 95% precision at any coverage.** The best any row achieves is a noisy 85% in one decile that doesn't hold at neighboring cuts — that's the artefact case in the method, not a usable crossing.

**Cut recommendation: none.** Don't ship "auto-send above X stated confidence" on this data — it would silently discard roughly a random subset of answers with respect to correctness, buying zero precision for whatever coverage you lose. Two ways forward, and this needs an owner to pick: (1) find a different signal for this system — self-consistency across resampled answers, a separate verifier/judge score, or retrieval margin if it's RAG-backed — and rerun the step-4 check before proposing any cut; (2) until a signal passes, everything routes to support, which is already the correctly-owned path for 100% of volume today, so nothing about routing changes — the LLM's own confidence just isn't the lever to pull.

## consulted
- `./scored_predictions.csv`, `./selfreported_confidence.csv` — read and processed via Bash/Python (AUROC, decile accuracy buckets, precision/coverage sweep, Wilson confidence intervals).
- `ls` on `./skill/` to confirm the bundled assets/references/evals existed — did not open `skill/SKILL.md`, `assets/threshold-decision-record.md`, or `references/uncertainty-signal-evidence.md`, since the method was already provided inline and the steps run here (0-6) didn't require them per the method's own "not needed to run the steps" note.