---
name: hybrid-parse-escalation
description: Use when extracting fields from structured or semi-structured text at volume — logs, receipts, invoices, emails, addresses, dates, CSV-ish or key-value dumps, scraped HTML — and want to avoid paying an LLM per record. Runs a DETERMINISTIC parser (regex/grammar/format rules) first, scores each record's parse confidence, and escalates ONLY the low-confidence rejects to a cheap LLM, keeping the deterministic wins. Triggers on bulk field extraction, "parse these N records", regex-vs-LLM tradeoffs, cutting extraction cost, handling messy edge cases in an otherwise regular format, or a parser that mostly works but chokes on outliers. Not for one-off parses, free-form prose with no structure, or picking a model tier (see cost-aware-model-routing).
---

# Hybrid Parse Escalation

## What & why
Most records in a structured feed are regular and parse perfectly with regex or a
grammar — the cost and error live in a small tail of malformed, ambiguous, or novel
edge cases. Sending every record to an LLM pays top price for work a parser does for
free; using only regex silently drops the tail. This talent parses deterministically,
measures confidence per record, and spends the LLM budget ONLY on the tail — cheapest
correct path for the bulk, model judgment for the hard few. Feeds `COSTS.md`.

## When to use
- Bulk extraction from a mostly-regular format (logs, receipts, invoices, addresses, dates, key-value or CSV-ish dumps, scraped fields).
- A parser that handles the common case but chokes on outliers.
- Any per-record LLM cost you want to cut without losing edge cases.
- NOT for: a single one-off parse; genuinely free-form prose with no exploitable structure; deciding WHICH model tier to use (that is cost-aware-model-routing).

## Steps
1. **Sample & characterize.** Pull a representative sample; identify the dominant format(s) and the shapes of the outliers. Note the target schema (fields + types) up front.
2. **Write the deterministic parser.** Regex, a grammar, or format rules covering the dominant case. Aim for high precision, not full coverage — it is fine to reject the tail.
3. **Define a confidence signal.** Score each record: all required fields matched, types/ranges valid, no leftover unparsed residue, format anchors present. Low score = escalate. Pick a threshold from the sample.
4. **Run the split.** Parse all records; accept high-confidence results as-is. Route only the low-confidence rejects to a cheap LLM with the schema and the raw record, asking for the same structured output.
5. **Normalize & merge.** Coerce both paths into one schema (same field names, types, null handling). Merge deterministic + LLM results into a single output stream, tagging each record with its source.
6. **Measure & tune.** Track escalation rate, per-path accuracy on a labeled slice, and cost. If escalation rate is high, widen the parser to absorb a recurring outlier (cheaper than escalating it forever). If LLM catches parser errors, tighten the confidence signal.

## Rules
- **Deterministic first, always.** The LLM is the fallback for the tail, never the default path.
- **Confidence gates escalation** — escalate on a measured signal, not a guess. A record with unparsed residue or a failed type check is a reject, not a pass.
- **One schema, two paths.** Both parser and LLM emit the identical target schema; normalize before merging so downstream code cannot tell which produced a record (except the source tag).
- **Fold recurring outliers back into the parser.** A pattern that escalates repeatedly is a parser gap — absorbing it is a permanent cost cut; escalating it is a recurring tax.
- **Never silently drop.** Every record ends up parsed, escalated, or explicitly quarantined for review — no gaps.
- **Escalation rate is the health metric.** Rising rate means the format drifted or the parser is stale; watch it.
- Method only — no network calls, no CLI invocations, no auto-run hooks. You define the parser and the gate; the caller runs them.
