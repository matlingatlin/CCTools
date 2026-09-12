## Q1

**Decision: pilot a confidence-based auto-approve tier now, don't keep reviewing 100%.**

Numbers to work from:
- Volume: 4,000/day. Team: 6 people.
- A reviewer verifying an already-extracted invoice (not keying from scratch) can reasonably clear ~200 records/day → team capacity ≈ **1,200/day**.
- That means auto-approve **coverage must be ≥70%** just to keep the exception queue inside the team's capacity, with 75–80% giving headroom for PTO/spikes.
- Precision target on the auto-approved segment: **99%**, not 95%. A wrongly auto-posted invoice (bad amount/vendor/GL code) costs far more than one extra human glance — this is money moving, so the bar is higher than a generic 95% target.

Plan:
1. Don't threshold the raw model confidence blindly — validate it first (AUROC + decile accuracy on a few hundred labeled invoices, same check I just ran for Q2). If it's an uncalibrated softmax, use a better signal (schema/field-validator pass count, self-consistency across re-extraction, retrieval margin on vendor match).
2. Sweep coverage vs. precision on that holdout. Take the highest-coverage cut that clears 99% precision.
3. **If that cut clears 99% at ≥70% coverage** (plausible — for reference, a comparably-behaved scoring model I just validated hit 100% precision at 32% coverage and 98.8% at 40%), ship it: auto-approve above the cut, the 6-person team now only touches the ~800–1,200/day exception queue, comfortably inside their capacity.
4. **If it can't clear 99% at ≥70% coverage**, don't force it — ship a smaller auto-approve slice (whatever coverage the data actually supports at 99%) and route the rest to the team as today. That's a real finding to bring back to whoever owns the target, not something to fudge by lowering the precision bar.
5. Route the abstained slice to the AP team as a named queue, monitor abstention rate as the drift alarm, and re-validate every model/prompt change.

## Q2

Ran the sweep on the 200-row holdout. First, validated the signal: **AUROC 0.889**, and decile accuracy is monotone (20%→35%→70%→75%→80%→90%→95%→100%→100%→100% from lowest to highest score decile) — this score is real signal, safe to threshold.

**Cut: score ≥ 0.55.**
- Precision: **96.8%** (91/94 correct) — clears the 95% target with a margin (the exact boundary point, ~0.50, sits right at 94.7%, too close to the line given n=200 sampling noise; 0.55 gives room).
- Coverage: **47.0%** (94/200 records auto-approved).
- The remaining 53% (106/200) goes to the review queue.

If you want to push coverage harder and accept thinner margin, 0.51 gets you ~97% precision at ~52-53% coverage, but I wouldn't ship right at the 95.0% boundary itself — one bad batch of ~5 records flips the reported number below target.

## Q3

**No.**

"90% sure" is meaningless until you know what kind of number it is. I have both types in front of me right now:
- The calibrated model-confidence score (Q2's data): thresholding near 0.9 there is genuinely safe — deciles above ~0.67 hit 100% accuracy.
- The LLM's self-reported confidence (Q4's data): AUROC **0.48** — statistically indistinguishable from a coin flip. Its 0.90–0.93 bucket is only **55–75% accurate**, i.e. wrong roughly 1 in 3-4 times, nowhere near 90%.

So the answer depends entirely on which one "the model says it is 90% sure" refers to, and you can't assume — you have to check (decile accuracy + AUROC) before trusting any stated confidence number, self-reported ones especially.

## Q4

**No defensible cut exists on `stated_confidence` — don't ship this gate on this signal.**

Checked it the same way as Q2: **AUROC 0.482** (chance is 0.5), and accuracy is flat across score buckets — 65-85% correct whether the model claims 0.79 or 0.99 confidence. The 0.99-confidence bucket is only 60% accurate; the 0.79 bucket is 65% accurate. The number carries no information about whether the answer is right.

A threshold on this would just auto-send a random ~x% of answers, with zero precision gain over sending everything and the same error rate as chance. Per the method's rule: don't threshold an unvalidated measure — swap the signal instead.

What I'd use instead: a verifier/judge score, self-consistency across repeated generations, or retrieval margin if this is a RAG-backed answer — then re-run this same validation (holdout, deciles, AUROC) before setting a cut. Until one of those passes validation, keep routing everything to support.

## consulted
- ./scored_predictions.csv, ./selfreported_confidence.csv (read and analyzed via Bash/python3: AUROC, decile accuracy, threshold sweeps)
- The supplied Abstention Threshold Design method (steps 1–8, trap table)
- Bash tool (ls, cat, python3 for the computations above)