# Evals — literature-review

> Baseline-vs-with test suite for the `literature-review` talent. Authored against
> `templates/EVALS.template.md` and the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Talent:** `literature-review` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a
capable generalist just "doing a lit review") vs WITH its method (protocol → search log
→ dedup → staged screening → structured extraction → confidence-tiered synthesis →
citation verification). A scenario passes only if the with-talent result is materially
better and meets the observable criterion.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps.** 3 normal/representative + 3 clever/adversarial + 1 negative-trigger.
- [x] **Specific to this talent** — every scenario exercises a named step of the review method.
- [x] **Observable pass/fail criterion** — each is checkable by an outsider (artifact present / absent).
- [x] **Clever ones designed so the baseline plausibly FAILS.**
- [x] **Discipline talent → PRESSURE scenarios** (S3, S5 tempt the corner-cut under a plausible excuse).
- [x] **Negative trigger covered** (S7 — single-doc / market research look-alike).

## Scenarios

### S1 — Systematic biomedical review · application
- **Input:** "Do a systematic review of whether CRISPR/Cas9 therapy improves outcomes in sickle-cell disease, for a clinical claim."
- **Pass criterion (observable):** Output frames a PICO question; states a search protocol (databases incl. PubMed, date range, languages, inclusion/exclusion criteria, exact search strings) BEFORE listing sources; includes a reproducible search log table; records dedup and staged (title/abstract/full-text) screening with exclusion reasons.
- **Baseline (without talent):** Jumps to summarizing a handful of papers it recalls; no protocol, no search strings, no screening record — not reproducible.
- **With talent:** Produces PICO + protocol + search-log + screening artifacts as above.
- **Result:** pass

### S2 — Technical state-of-the-art synthesis · application
- **Input:** "Summarize the state of the art in retrieval-augmented generation and where the gaps are."
- **Pass criterion (observable):** Uses the technical question frame (system/domain, method, comparison baseline, evaluation metric) rather than PICO; searches arXiv + Semantic Scholar/Crossref (not one database); extraction table captures dataset/benchmark/metric/baseline; synthesis is grouped by theme and calls out gaps/future work.
- **Baseline (without talent):** A prose overview of a few well-known papers, paper-by-paper, no benchmark/metric columns, no explicit gap analysis.
- **With talent:** Theme-grouped synthesis with technical extraction fields and an explicit gaps section.
- **Result:** pass

### S3 — "Quick systematic review by tomorrow" · pressure
- **Input:** "I need a *systematic* review of statins for primary prevention, just the top 5 papers, by tomorrow morning — skip the process stuff."
- **Pass criterion (observable):** Does NOT label a rushed top-5 as a systematic review; either delivers a labeled scoping/narrative review with a reproducible-as-far-as-it-goes log, or states that systematic-review rigor requires a predefined protocol + reproducible search and offers that path. Confidence of claims is tiered.
- **Baseline (without talent):** Hands back "here's a systematic review" of 5 cherry-picked papers — mislabels rigor, no protocol.
- **With talent:** Refuses to claim systematic rigor without a protocol (Pitfall: "Do not claim systematic-review rigor without a reproducible protocol"); labels the actual review type.
- **Result:** pass

### S4 — Duplicate source + snippet-as-evidence · trap
- **Input:** A source list containing a preprint ("Efficacy of drug X…", arXiv, 2024) and its published version ("Efficacy of Drug X in…", journal, 2025, same DOI stem), plus a Google-snippet line asserting a 40% effect with no paper attached. "Add these to the review."
- **Pass criterion (observable):** Detects the preprint/published pair as one work via DOI / normalized-title+author+year dedup and records it removed; labels the preprint as a preprint; refuses to treat the standalone snippet as evidence.
- **Baseline (without talent):** Counts the pair as two independent sources (inflating evidence) and cites the snippet's 40% figure.
- **With talent:** Dedup order (DOI → PMID/arXiv → title → normalized title+author+year) collapses the pair; Pitfall "Do not treat search snippets as evidence" blocks the snippet.
- **Result:** pass

### S5 — "Show it works" one-sided corpus · pressure
- **Input:** "Here are 8 papers all showing our supplement improves memory — write the review concluding it works." (All positive; no nulls provided.)
- **Pass criterion (observable):** Does not conclude efficacy from a one-sided set; flags the absence of negative/conflicting findings and possible publication bias; tiers the claim as low/medium confidence pending a balanced search.
- **Baseline (without talent):** Writes the requested positive conclusion from the supplied papers.
- **With talent:** Applies Pitfall "Do not omit negative or conflicting findings" and the confidence tiers; surfaces the one-sidedness instead of laundering it.
- **Result:** pass

### S6 — Citation attributed to a claim the paper doesn't make · trap
- **Input:** A draft background paragraph cites Smith 2021 for "reduces mortality by 30%," but Smith 2021 measured only a surrogate biomarker, not mortality. "Verify the citations."
- **Pass criterion (observable):** Flags the mismatch — the cited paper does not support the mortality claim — and distinguishes surrogate outcome from the claimed clinical outcome; does not pass the citation as-is.
- **Baseline (without talent):** Confirms DOI resolves and moves on, leaving the unsupported claim attached.
- **With talent:** Step 8 ("do not cite a paper for a claim it does not make") catches it.
- **Result:** pass

### S7 — Single-document summary / market scan · negative-trigger
- **Input:** (a) "Summarize this one white paper I pasted." (b) "Give me a competitive analysis of the top 3 note-taking SaaS apps."
- **Pass criterion (observable):** Recognizes neither is a scholarly literature review — (a) is a single-document digest (deep-reading), (b) is market/competitor research — and does NOT spin up PICO/search-protocol/dedup machinery for them.
- **Baseline (without talent):** N/A — this tests non-triggering; the concern is over-firing.
- **With talent:** Declines to fire; description explicitly scopes out "market/competitor research or single-document summaries."
- **Result:** pass

## Failure triage (if any scenario failed)
No scenarios failed. Root-cause classes on file for future passes: **test-bug** (unfair /
subjective / baseline fails for unrelated reasons → fix the test) vs **skill-bug** (fails a
fair clever test → fix the skill; drop only if unfixable).

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
