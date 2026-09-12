---
name: error-analysis-taxonomy
description: "Use when you have a batch of AI/LLM output traces, generations, transcripts, or eval failures and need to know WHAT is actually going wrong and in what proportion — the 'look at your data' error-analysis practice. Reads a sample of real outputs, open-codes each failure with a short verbatim note, groups the notes into axial failure-mode categories, then frequency-ranks them into a prioritized improvement backlog. Triggers: 'look at the data', 'what are the failure modes', 'categorize/cluster these errors', 'error analysis', 'annotate traces', 'taxonomy of failures', 'why is the model getting these wrong', 'which bug to fix first'. Turns raw traces into ranked, actionable categories. NOT for building a repeatable eval/scorer (use eval-harness), capturing session lessons (use learn-eval), per-iteration loop metrics (use wave-reflect), or debugging one run (use agent-introspection-debugging)."
---

# Error Analysis Taxonomy

Open- and axial-code a batch of AI output traces into a frequency-ranked taxonomy of
failure modes, so improvement effort goes to the errors that actually dominate — not the
ones that feel salient. From the "look at your data" eval discipline.

## When to use
- You have ≥1 batch of real AI outputs (generations, agent transcripts, RAG answers, eval
  rows) and want a grounded map of what fails and how often.
- Before writing scorers or metrics — you don't yet know which axes to measure.
- When picking which failure to fix first and needing evidence, not intuition.

## When NOT to use
- Building a reusable eval harness/scorer → `eval-harness`.
- Harvesting reusable session lessons → `learn-eval`.
- Per-iteration loop yield metrics → `wave-reflect`.
- Root-causing a single failing run → `agent-introspection-debugging`.

## Steps
1. **Frame.** State the one question the traces must answer (e.g. "why do support replies
   get rejected?"). Locate the trace source and note total volume.
2. **Sample.** Pull a review set — take all rows if few, else a random sample (start ~30-50)
   plus every known failure. Record how you sampled; note over-sampling of failures.
3. **Open-code (first pass).** Read each trace end to end. Write ONE short free-text note
   naming the single most important thing wrong (or "OK"). Quote the offending span. Do not
   invent categories yet — stay concrete and verbatim. One line per trace.
4. **Axial-code (merge).** Cluster the open notes into a handful of distinct failure-mode
   categories. Give each a crisp name + one-sentence definition + 1-2 real quoted examples.
   Split any category that hides two mechanisms; merge near-duplicates.
5. **Second pass / label.** Re-read the sample and tag each trace with exactly one category
   (add "other" sparingly). Adjust definitions until every trace fits cleanly.
6. **Frequency-rank.** Count traces per category. Sort descending. Show count and % of
   sample; flag that raw counts are skewed if you over-sampled failures.
7. **Prioritize backlog.** For each top category estimate impact (frequency × severity) and
   rough fix effort. Emit an ordered backlog: category → hypothesis of cause → proposed fix
   or eval to add → owner/next step.
8. **Report.** Return the taxonomy table (category, definition, example, count, %), the
   ranked backlog, and the sampling caveats. Point the top 1-2 categories at `eval-harness`
   to become permanent scorers.

## Rules
- Look at raw outputs yourself before theorizing — no failure mode is real until quoted.
- One primary failure per trace in the first pass; multi-label only if forced, and say so.
- Categories are mutually exclusive and mechanism-based, not symptom-synonyms.
- Report the denominator and sampling method with every percentage; never imply the sample
  rate equals the production rate when failures were over-sampled.
- Taxonomy is a snapshot — re-run on a fresh sample after fixes; do not reuse stale counts.
- Method only. No network calls, no CLIs, no auto-run hooks — you read and code the data.
