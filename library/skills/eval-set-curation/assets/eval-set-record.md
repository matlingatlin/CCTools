# Eval set record — <set name>, cut <date>

Fill every field. A field you cannot fill is filled with the word **UNKNOWN** and the reason, never
left blank — a blank reads as "fine" and an UNKNOWN reads as what it is.

**Three sections enforce, and the rest is context.** Sections **3, 5 and 6** exist because a
measured baseline got each of them wrong; they carry stop clauses and their fields are shaped so
that skipping the step leaves a visible empty entry. Sections **1, 2, 4 and 7** record behaviours
that the same baseline already did reliably — they are here so the enforced sections can be read at
all (a cluster count means nothing without a population), and they carry no stop clause. Nothing
else is here. Sections for the decision the set serves and for the refresh cadence were dropped:
they are reasonable record-keeping and no observed failure needs them.

---

## 1. Population — *context*

| | |
|---|---|
| Source | <system, table, date range> |
| Rows in the population | <n> |
| Query used | <paste it; the set must be rebuildable> |

## 2. Slices — *context*

A slice is a subpopulation you would **act on differently** if it scored badly. Slices you would
not act on are deleted from this table, not carried.

| Slice | Population n | Population share | Would act on it? |
|---|---|---|---|

## 3. Near-duplicates — **ENFORCED. Two numbers, not one.**

**Stop clause.** *Distinct strings* and *distinct clusters* are different numbers and the second is
the one that matters. Collapsing 120 rows to 60 distinct strings and calling the result deduplicated
leaves a paraphrase family standing. Both rows below are required, **and the normalisation list is
read against them**: two equal numbers after normalising whitespace is a real finding, two equal
numbers after normalising the varying slot of a templated family is the family collapsing in the
wrong step and the failure surviving intact. That is the one route by which this section is
silently defeated, so the list is a field and not a sentence.

| | |
|---|---|
| **What was normalised before exact match** | <list every slot: case, whitespace, IDs, timestamps, order numbers, dates, names...> |
| Detector | <exact / normalised-exact / MinHash at threshold t / embedding cosine at t / LLM> |
| Threshold, and the labelled pairs it came from | <n pairs labelled, and the flip point — OR "no clean flip point", see below> |
| If the labels did not flip cleanly | <the band, what was collapsed inside its confident end, how many pairs went to a person> |
| Rows in | <n, and whether contamination was removed first> |
| Distinct **strings** after exact match on normalised text | <n> |
| Distinct **clusters** after near-duplicate collapse | <n> |
| Largest cluster | <size, and one example> |
| Rows kept | <n, one representative per cluster> |

**What the detector cannot see.** Name the paraphrase class you are not catching:

> <e.g. "normalised exact match plus 5-shingle Jaccard at 0.7 catches the templated head; the
> detector was never evaluated on paraphrase across languages, and that class is assumed absent —
> untested">

## 4. Contamination — *context* (removed BEFORE section 3 runs)

Contaminated examples are removed, not down-weighted, and the check is re-run after any change to
prompts, few-shots, training data or the index.

| Artifact checked against | Method | Rows found | Rows removed |
|---|---|---|---|
| system prompt / few-shots | | | |
| fine-tune or training data | | | |
| retrieval index | | | |
| public benchmark the model may have trained on | | | |
| traces someone debugged and hard-fixed | | | |

| | |
|---|---|
| Checked on | <date> |
| Re-check trigger | <what change forces this to be re-run> |

## 5. Per-slice sizing — **ENFORCED. The tolerance comes first.**

**Stop clause.** The floor is the arithmetic output of a tolerance, and the tolerance is the
arithmetic consequence of a decision. Fill the block below **top to bottom**; every row in it is
checkable by someone other than you, which is what the first draft of this section was missing.
A floor with a citation but no tolerance is still an invention — an interval reports the width *at*
an n, it does not select one.

**What this section can and cannot do.** It can force the tolerance to be a written, dated, owned
decision with a stated consequence, and all four of those are facts someone can check against what
you actually did. It **cannot** make the tolerance well chosen, and no template can. Two records
that both pass this section may hold floors three-fold apart; that divergence is legitimate and is
not what this section is for.

| | |
|---|---|
| **1. The decision this floor gates** | <what happens below the floor, and what happens above it — e.g. "below: this slice does not block a release; above: it does"> |
| **2. Tolerance**, in one of two forms | <largest half-width I can act on> OR <difference the gate must detect, at what power> |
| Inputs the inversion needed | <p used, and why that p> · <variance assumption, and where it came from> |
| **When p was fixed** | <at the same time as the tolerance> OR <after scoring, from this score: ___> |
| Is the interval cluster-adjusted? | <yes, by what> / <no — naive Bernoulli or Wilson> / <not checked> |
| **3. Owned by** | <one name is enough> |
| Fixed on | <date> — before or after the first score was seen? <say which> |
| Written down where | <the document, ticket or commit that carries it, dated> |

| Slice | n pre-collapse | n post-collapse | Interval at the post-collapse n | Floor from the inversion | Working shown |
|---|---|---|---|---|---|

**Slices that cannot support a per-slice claim at all.** Report the raw fraction, never a percentage:

| Slice | n | Raw fraction reported | Why it cannot support a percentage |
|---|---|---|---|

**If a cited floor is used, its verdict travels with it.** The widely-quoted floor of roughly 1,000
questions is DERIVED — computed from variance parameters its own author calls fictional in the same
sentence. It may inform a default; it may not be cited as evidence that 1,000 holds, and it is not
a tolerance.

## 6. Holdout — **ENFORCED. Sealed or UNSEALED, and a log either way.**

**Stop clause.** A pool that "can also be used as a dev set" is not a holdout. If nothing seals it,
write **UNSEALED** in the Sealed field — do not leave the table blank and call the pool a holdout.

| | |
|---|---|
| Dev n | |
| Holdout n | |
| Sealed by what mechanism | <stored where, who can open it, what enforces it — or **UNSEALED**> |
| Look budget | <n looks per period> |
| The budget is a **policy**, owned by | <name, date> |

The look budget is not an evidence-based number and this record does not present it as one. The
strongest result on holdout reuse is a synthetic worst case that gives no safe reuse count; the
results on the other side are observational, differ from each other, and neither transfers cleanly
to an internal set scored on every commit.

**Look log.** One row per look. An empty table with a mechanism in the Sealed field means no look
yet; an empty table with UNSEALED means there is no holdout.

| Date | Who | Reason | Decision it confirmed |
|---|---|---|---|

## 7. Reporting — *context*

| | |
|---|---|
| Primary output | per-slice scores |
| Headline, if one is required | <reweighted by the section 2 population shares, labelled an estimate> |
| Raw mean of this set | <n> — **not** production reality; state it only to show the gap |
| Effective N | <post-cluster-collapse, from section 3> |
