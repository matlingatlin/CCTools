I read the file, computed the distribution, ran the dedup and contamination checks, and built the set. Everything below comes from the actual 2000 rows.

**Population facts the four answers rest on:**

| slice | rows | share | accuracy |
|---|---|---|---|
| simple_lookup | 1647 | 82.35% | 94.72% |
| multi_hop | 264 | 13.20% | 67.05% |
| ambiguous | 67 | 3.35% | 46.27% |
| adversarial | 22 | 1.10% | 31.82% |

37 rows carry `in_fewshot_prompt=1`. And a text check finds the file is far less varied than 2000 rows suggests: only **120 rows contain real natural-language queries** (all of them in `simple_lookup`), and those 120 are 60 exact-duplicate pairs — which are themselves only **6 intent templates** (`cancel_subscription`, `password_reset`, `balance_check`, `refund_eta`, `billing_address`, `warranty_check`) × 10 plan-name slot-fills. The other 1880 rows are opaque placeholders of the form `<slice> case <N> <hex>` with no distinguishing text at all.

# Q1

**The decision the set serves:** ship/no-ship on a prompt or model change, with a per-slice gate — because the three tail slices are where the failures are and they are invisible in any pooled number.

**Order of operations:** slice → count population → allocate floors → sample within cell → dedup → decontaminate → re-check floors and re-draw (this is what makes it honest) → split.

**Allocation of the 200** (floor 30 per acted-on slice, remainder pushed toward high error-variance slices, not toward traffic share):

| slice | n | pop share | acc in set | 95% CI | pop acc |
|---|---|---|---|---|---|
| simple_lookup | 58 | 82.35% | 93.1% | ±6.5pp | 94.7% |
| multi_hop | 72 | 13.20% | 70.8% | ±10.5pp | 67.0% |
| ambiguous | 48 | 3.35% | 47.9% | ±14.1pp | 46.3% |
| adversarial | 22 | 1.10% | 31.8% | ±19.5pp | 31.8% |
| **total** | **200** | | | | |

**How each cell was actually drawn:**

- **simple_lookup = 58, and 58 is a ceiling, not a choice.** 1647 rows collapse to 60 distinct natural phrasings; removing the contaminated ones and their exact twins leaves **58**. I took all 58 distinct forms rather than 58 random rows — a random draw of 58 from 1647 would have handed back mostly opaque placeholders and roughly a dozen distinct real queries. This is step 6a doing its job: I sampled to a post-dedup target, so I know the cell has 58 variants rather than merely having drawn 58.
- **multi_hop = 72.** 264 rows, 3 removed as contaminated (q0698, q1197, q1217), random draw of 72 from the remaining 261 under seed 20260902. Given the extra budget over floor because it is 13% of traffic *and* runs a 33% error rate — the largest absolute pool of real failures in the file.
- **ambiguous = 48.** 67 rows, 1 removed (q0164), 48 drawn from 66. Above floor because its error variance is the highest of any slice (p≈.46).
- **adversarial = 22 — the entire slice, and it still misses the floor.** All 22: q0128 q0260 q0281 q0326 q0399 q0425 q0726 q0819 q0870 q0948 q1138 q1167 q1198 q1286 q1344 q1499 q1672 q1687 q1772 q1886 q1938 q1961. None are contaminated. This cell is **genuinely exhausted** — no re-draw can reach 30, because the population is 22. That is a finding about your logging, not a defect in the sample.

**Split:** 200 = **120 dev / 80 frozen holdout**, stratified within each slice (simple_lookup 35/23, multi_hop 43/29, ambiguous 29/19, adversarial 13/9). Holdout stored separately, opened once per release, each look logged with date and reason.

**What the choice costs — concretely:**

1. **You cannot report the set's own mean.** The raw stratified mean of these 200 rows is **67.5%**. That number is meaningless as product quality — it is an artifact of deliberately over-sampling the tail. The reportable headline is the reweighted estimate: **88.0% ± 5.6pp (estimate)**.
2. **Adversarial stays anecdote-grade forever, at 22.** Its CI is ±19.5pp. You can distinguish "roughly a third" from "nearly all" and nothing finer. A drop from 32% to 20% will not register. The fix is not sampling — it is logging more adversarial traffic, or manufacturing cases (`synthetic-eval-data-generation`) to fill the cell.
3. **simple_lookup is capped at 6 real intents.** 82% of your traffic is measured by six question shapes. The 58 rows give a ±6.5pp CI, but the deeper limit is variety, not count: any failure mode outside those six intents is undetectable, and no amount of extra sampling from this file fixes it, because the variety is not in the file.
4. **The three tail slices are textually unauditable.** Their rows are opaque placeholders, so I could not dedup them by text. Their effective N could be far below 72/48/22 if the underlying traffic is templated the way simple_lookup is. I sampled them as if every row were distinct, which is the optimistic assumption — treat their CIs as lower bounds on the true uncertainty until raw query text is available.
5. **You lose 1800 rows.** That is the correct trade. They were near-duplicates and placeholders contributing confidence without signal.

# Q2

**No. Don't ship on it.** It is arithmetically correct — 1775/2000 = 88.75% exactly — and that is the whole problem: it is the pooled raw mean, which is the one number that hides everything you need to see.

**1. It is one number covering a 63-point spread.** 94.7% / 67.1% / 46.3% / 31.8%. "88.75%" describes no slice in the file. On your worst slice the assistant fails two times in three.

**2. It is inert — it is a traffic-share report, not a quality report.** Because simple_lookup is 82% of rows:

- adversarial collapsing to **0% accuracy** moves the headline by **0.35pp** (88.75 → 88.40)
- ambiguous collapsing to 0% moves it **1.55pp**
- a 10pp regression in adversarial moves it **0.11pp** — invisible against release noise

Anything that ships and destroys your hardest slices will pass this gate. Conversely the number will move 8.2pp on a 10pp change in password-reset boilerplate. It tracks the easy path and almost nothing else.

**3. It is contaminated upward.** The 37 few-shot rows score **36/37 = 97.3%**, against **88.59%** for the other 1963. Those rows are testing whether the model can echo its own prompt. The aggregate inflation is small (+0.16pp) only because they are few; the point is that the contaminated rows are concentrated in the slice already driving the headline (33 of 37 are simple_lookup), so they harden exactly the cell that most needs honest measurement.

**4. Its effective N is nothing like 2000.** The whole file reduces to **64 distinct normalized query forms**. The natural-language portion is 6 intent templates. Reporting 2000 as the sample size implies a ±1.4pp precision the data cannot support — a cluster of paraphrases is one observation, not forty.

**What to report instead:** per-slice scores as the primary output — `simple_lookup 94.7% (n=58, ±6.5pp) · multi_hop 67.0% (n=72, ±10.5) · ambiguous 46.3% (n=48, ±14.1) · adversarial 31.8% (n=22, ±19.5, below floor — indicative only)` — and only then, if a single number is demanded, **≈88% (population-weighted estimate)** with the label attached. Never let it stand in for "88.75% of user traffic succeeds."

# Q3

Four categories, **39 rows removed outright** before anything else:

**1. Contaminated few-shot examples — 37 rows (`in_fewshot_prompt=1`).** Removed, not down-weighted. These appear in the system prompt; scoring them measures recall of the prompt, not capability. Breakdown: 33 simple_lookup, 3 multi_hop (q0698, q1197, q1217), 1 ambiguous (q0164), 0 adversarial.

**2. Two rows the contamination flag misses — q0067 and q0011.** These have `in_fewshot_prompt=0` but their query text is an **exact match** for a flagged few-shot row (q0077 `reset the password for the legacy`, q0001 `what is the basic balance on my account`). The flag marks the specific logged trace, not the text. Contamination travels with the *content*, so the twins must go too. This is the reason the flag column alone is not sufficient and you must diff the candidate set against the prompt by text — near-match, not just exact — rather than trusting a boolean someone set at logging time.

**3. Near-duplicates — the 60 exact-duplicate pairs in simple_lookup.** Keep one representative per cluster, record cluster size as provenance. Without this, paraphrase clusters silently dominate and inflate confidence.

**4. Opaque placeholder rows — a decision you have to make explicitly.** 1880 rows are `<slice> case <N> <hex>` with no query content. Either they are redaction artifacts, in which case **you cannot freeze this file at all** until you recover the real text (there is nothing to evaluate a model against), or they are genuinely templated traffic, in which case they collapse to one cluster per slice and your effective N in the tail slices is near-zero. Resolve this before freezing — it is the largest open question in the file, and it is the difference between a 200-row eval set and a 64-row one.

**Two things that must happen after removal, not before:**

- **Re-check the floor and re-draw.** Removals shrink cells after the floors were set. simple_lookup went 60 → 58 distinct forms from contamination removal alone; ambiguous lost 1, multi_hop 3. Every cell that drops below floor gets topped up from that cell's untouched population, then re-deduped and re-decontaminated. Repeat until every cell clears floor or is provably exhausted. Adversarial (22) is exhausted — record it as a finding.
- **Re-run the contamination diff on every prompt edit.** These 39 rows are clean *against today's prompt*. Change the few-shots next sprint and this set is contaminated again. Wire the check into the same CI job that runs the eval.

**Also before freezing:** redact PII from the real query text (`reset the password for…` rows are exactly where account identifiers land), and record provenance per row — source id, slice, cluster size, why included — so the set is rebuildable. Sampling seed here: 20260902.

# Q4

**Floor: 30 per slice, and treat anything under 10 as an anecdote.** But 30 is the minimum to say anything at all, not the number that makes a gate work. The honest answer is that the number depends on the slice's base rate and on how large a regression you need to catch. From this file:

| n | simple_lookup (p≈.95) | multi_hop (p≈.67) | ambiguous (p≈.46) | adversarial (p≈.32) |
|---|---|---|---|---|
| 10 | ±13.9pp | ±29.1pp | ±30.9pp | ±28.9pp |
| 22 | ±9.3pp | ±19.6pp | ±20.8pp | ±19.5pp |
| **30** | ±8.0pp | ±16.8pp | ±17.8pp | ±16.7pp |
| 50 | ±6.2pp | ±13.0pp | ±13.8pp | ±12.9pp |
| 100 | ±4.4pp | ±9.2pp | ±9.8pp | ±9.1pp |
| 200 | ±3.1pp | ±6.5pp | ±6.9pp | ±6.5pp |

Read it as detection power. At **n=30**, a mid-range slice detects only a **~24pp** regression at 80% power. At **n=100** that improves to **~13pp**. To catch a **5pp** regression on a coin-flip slice you need roughly **380 examples in that cell**.

**The practical rule for your four slices:**

- **n < 10** — anecdote. Report the raw count ("3 of 8 passed"), never a percentage. A percentage on n=8 invites people to compare it across releases, and it will swing 25pp on noise alone.
- **n = 30** — the floor. Enough to tell a broken slice from a working one (32% vs 70% is detectable). Not enough to gate a release on movement between runs.
- **n = 100** — a real gate for a tail slice. ~±9pp, catches a 13pp regression.
- **n = 300+** — needed only where a few points matter commercially.

**Applied here:** multi_hop (72) and ambiguous (48) clear the floor and give usable directional numbers — they detect a break, not a drift. simple_lookup at 58 is fine on count (±6.5pp, high base rate needs fewer) but is limited by *variety* at 6 intents, not by n. **adversarial at 22 cannot clear the floor from this population at any sample size**, because 22 is the population. Its ±19.5pp means it should be reported as a raw fraction (`7/22`) with an explicit "below floor, indicative only" label, and it should not be a release gate until you have logged or generated more adversarial traffic.

One caveat on all of the above: these intervals assume the examples within a cell are independent. Where near-dups survive, the effective n is lower than the nominal n and the true intervals are wider — which is the whole reason dedup comes before the floor check, and why the tail slices' numbers here are best-case.