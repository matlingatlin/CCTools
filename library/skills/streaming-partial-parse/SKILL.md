---
name: streaming-partial-parse
description: Use when a structured LLM response (a JSON object, a typed schema, Instructor's Partial[Model], a Pydantic/Zod model) should render field-by-field AS IT STREAMS instead of blocking on the full completion — a form, card, table row, or dashboard whose fields pop in progressively. Covers accumulating a token stream, repairing the truncated-JSON prefix at each chunk, coercing it to a partial object with unfilled fields left null/absent, and yielding successive snapshots to the UI. Triggers on "stream partial object", "show fields as they arrive", "progressive/streaming structured output", "partial JSON parse", "Instructor Partial", perceived-latency cuts on structured generation, or typewriter-style rendering of a schema. NOT for parsing existing structured records at volume (see hybrid-parse-escalation), plain text token streaming with no schema, or choosing a model tier (see cost-aware-model-routing).
---

# Streaming Partial Parse

## What & why
A structured completion normally forces the UI to wait for the closing brace before
anything renders — dead time that scales with object size. This talent accumulates the
token stream, repairs the incomplete-JSON prefix after each chunk, and yields a partial
object where present fields hold their value and absent ones stay null. The user watches
fields fill in instead of a spinner; perceived latency drops to first-field time.

## When to use
- A structured/typed response (JSON, Pydantic, Zod, `Partial[Model]`) drives UI that can render incrementally.
- Objects large enough that full-completion wait is a felt delay.
- You want a stream of successive partial snapshots, not one final parse.

**When NOT:** parsing many existing records cheaply (`hybrid-parse-escalation`); plain
prose streaming with no schema (raw token append is enough); model-tier selection
(`cost-aware-model-routing`); when the consumer needs only the final validated object.

## Steps
1. **Define the shape twice.** Keep the strict schema for the final value; derive a
   partial view where every field is optional/nullable. Never validate mid-stream against the strict schema.
2. **Request a streaming completion** in JSON/structured mode. Get an async iterator of text deltas.
3. **Accumulate.** Append each delta to a running buffer; do not parse deltas in isolation.
4. **Close the prefix.** Before parsing, balance the buffer: close open strings, arrays,
   and objects, drop a trailing comma or dangling key, so the prefix is valid JSON.
5. **Parse tolerantly.** Parse the repaired prefix. On failure, skip this chunk and wait
   for more tokens — do not throw. Prefer a partial/tolerant parser over hand-rolled repair when available.
6. **Coerce to the partial view.** Map the parsed prefix onto the partial schema; leave
   still-absent or half-written fields null/absent rather than emitting garbage.
7. **Yield a snapshot** each time the partial object changes; the consumer diffs and re-renders.
8. **Finalize.** On stream end, parse the complete buffer against the STRICT schema and
   yield the validated object; surface any validation error now, not mid-stream.

## Rules
- Buffer is the source of truth — always parse the full accumulated prefix, never a lone delta.
- Mid-stream parses are best-effort and non-throwing; the only hard validation is the final one.
- Unfilled fields are null/absent, never fabricated, defaulted, or partially-typed leaks.
- Emit immutable snapshots; never hand the consumer a buffer you keep mutating.
- Partial values are display-only — gate side effects (writes, API calls) on the final validated object.
- Yield only on change to avoid re-render churn; coalesce bursts of deltas if needed.
- Keep the two schemas in sync; the partial view is strictly the strict one with fields relaxed.
