# Evals — llm-wiki-ingest

**Talent:** `llm-wiki-ingest` · **Type:** technique (with one discipline pressure) · **Last eval:** 2026-09-02/03, the first v3 build (`pipeline/builds/llm-wiki-ingest`, three arms, k=2, code grader, blinded, preregistered rule) · **Verdict:** SHIP after iterate round 1 (2026-09-03): every clause of the preregistered rule holds - every clause of the preregistered rule holds (the preregistered prose is a phrasing the contract registers as equivalent to the default rule: the default rule with identical parameters: min_repeats 2, cost_tolerance 0.20 on tokens and tool_calls, require_win wit; k=2 from probe outcome 'refuted') — note: 6 dispatched run(s) logged no duration, so this build cannot be compared on wall clock. Adopted.

## Method
Baseline-vs-with per scenario; PASS on normal scenarios, "PASS. Beats baseline." only where the baseline plausibly fails. The observable criterion for every scenario is the state of the files, checked by `python3 knowledge/kb.py lint --json` and by reading the note.

## Scenarios

### S1 — a new pricing fact from a fetched page · application (normal) — EXECUTED as T1: with 2/2, without 1/1, probe 2/2, incumbent 2/2 (the baseline is clean here)
- **Input:** a fetched vendor pricing page with three per-MTok prices; the wiki has a note that owns model prices.
- **Pass criterion:** the owning note gains a dated row with the verbatim line and MEASURED; no new note is created; lint reports 0 errors; INDEX unchanged, SOURCES +1 row.
- **Baseline:** states the prices in chat, or writes a new "pricing-2026-09" note beside the owner.
- **With talent:** triage says update; the owner is extended.
- **Result:** PASS (no delta; baseline clean)

### S2 — a source that contradicts a page · trap — EXECUTED as T2: with 2/2, without 1/1, probe 2/2, incumbent 2/2 (the baseline is clean here too)
- **Input:** a model card says 753B parameters; the wiki's note says 744B from the vendor's README.
- **Pass criterion:** both values kept as separate rows with their sources and dates; the note marked disputed at that line; neither value silently overwritten.
- **Baseline:** overwrites with the newer number, or averages, or ignores the conflict.
- **With talent:** disputed triage; two rows.
- **Result:** PASS (no delta; baseline clean)

### S3 — a video transcript with no retrievable URL · edge
- **Input:** an 8-second clip's on-screen text, creator unidentified.
- **Pass criterion:** the transcript text is saved as the raw; the note's source is a `note:` entry stating that; lint reports the note-only source as INFO, not ERROR; claims from it are REPEATED, not MEASURED.
- **Baseline:** cites "a video" with no raw and grades the on-screen numbers MEASURED.
- **Result:** pending

### S4 — the cascade under time pressure · pressure
- **Input:** the new page names four neighbours; the user says "just commit it, we'll link later".
- **Pass criterion:** each neighbour gains a sentence naming the new page back before the commit, or the commit message states which neighbours were left one-way and why; lint's one-way count for the new page is 0 or explained.
- **Baseline:** commits with four one-way links and no note of it.
- **With talent:** step 5 or an explicit deferral in the log.
- **Result:** pending

### S5 — no material · normal — EXECUTED as T3 in every round: with 2/2 (rounds 0-3), without 0/1, probe 0/2, incumbent 0/2 — the one measured win; step 2 was rewritten for it twice (page untouched; then the value's as-of date, not the fetch date)
- **Input:** a blog post restating three facts the wiki already holds with the same sources.
- **Pass criterion:** no page changed; an operation-log entry says "no material" with the URL and date.
- **Baseline:** writes a thin note anyway.
- **Result:** PASS. Beats baseline (0/5 baseline runs vs 2/2 with)

### S6 — a claim to bundle into a skill · negative-trigger
- **Input:** "gather the evidence for the eval-set-curation skill's references file".
- **Pass criterion:** this talent does not fire; `skill-knowledge` does (the destination is a skill bundle, not a wiki page).
- **Result:** pending

## Not executed in the first build
S3 (transcript with no URL), S4 (cascade under pressure) and S6 (negative trigger) have no executable eval yet; S6's claim is carried by the trigger matrix instead (recall 11/12, mis-fire 0/4, sibling reached 4/4). The whole-artefact review named this gap; closing it is the next iteration's 2.4.

## Failure triage
test-bug → fix the test and record it in `pipeline/CURATION-LESSONS.md`; skill-bug → fix the step named; a step that cannot be fixed → drop only then.
