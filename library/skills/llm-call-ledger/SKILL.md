---
name: llm-call-ledger
description: Use when instrumenting or reviewing how model calls get recorded — logging each LLM/agent request and response with its model id, params, token counts, cost, latency, and timestamp to a durable, queryable ledger so runs are replayable and spend is auditable. Triggers on adding call logging or an audit trail, capturing usage/token counts per call, building a spend/metering table for COSTS.md, reconciling a provider invoice, wanting to replay or debug a past call, "log every model call", "usage ledger", "token accounting", "cost per request", "who spent what". Serves COSTS.md metering and observability. NOT for deciding which tier or budget a call should use (cost-aware-model-routing) or governing context-window token pressure (context-budget) — this only RECORDS what happened, it makes no routing or budget decisions. NOT for whether a remembered FACT was user-asserted or system-observed and is still current (memory-provenance-separation) — that governs knowledge provenance, this records calls.
---

# LLM Call Ledger

## What & why
Every model call is a billable, auditable event. Without a durable record you cannot answer
"what did this run cost", "why did the model say that", or "does the invoice reconcile". This
talent defines a per-call ledger: one row per request, written after every call, queryable by
run/user/model/day. It feeds `COSTS.md` metering and makes calls replayable. It only RECORDS —
routing and budgets belong to cost-aware-model-routing.

## When to use
- Adding or reviewing call logging, usage capture, or an audit trail around an LLM/agent call.
- Building a spend/metering view, or reconciling a provider invoice against your own numbers.
- Needing to replay, debug, or attribute a past call.

**When NOT:** deciding tier/model/budget for a call (cost-aware-model-routing); managing
context-window token pressure within a call (context-budget). Those decide; this records.

## Steps
1. **Fix the schema — one row per call.** Required fields: `id`, `timestamp` (UTC),
   `run_id`/`request_id`, `actor` (user/agent), `provider`, `model` (exact id, not alias),
   `params` (temperature, max_tokens, reasoning effort), `input_tokens`, `output_tokens`,
   `cache_read`/`cache_write_tokens`, `cost` (with currency + the price rates used),
   `latency_ms`, `status` (ok/error/refusal), and a `prompt_ref`/`response_ref`.
2. **Decide where the big blobs live.** Store prompt/response bodies content-addressed
   (hash → blob) or in a separate store; keep only the hash/ref in the ledger row so it
   stays queryable and cheap. Never inline megabyte payloads into the metering table.
3. **Write after every call — success AND failure.** Wrap the call site so the ledger entry
   is emitted in a `finally`/deferred path. A failed, refused, or timed-out call still costs
   tokens and must be logged. Capture token counts from the provider response usage, not an
   estimate, when available; mark estimated counts as such.
4. **Compute cost explicitly.** cost = input_tokens×rate_in + output_tokens×rate_out
   (+ cache tiers). Record the rate table version alongside the row so historical rows stay
   correct when prices change. Never back-fill new prices onto old rows.
5. **Make it queryable & durable.** Choose an append-only durable sink (a table or an
   append-only log), index by timestamp/run/model, and define rollups: cost per run, per day,
   per model, per user. These rollups are what `COSTS.md` reports against.
6. **Redact at write time.** Apply the project's PII/secret redaction to prompt/response refs
   before persisting. Keep a retention policy (how long bodies vs. metering rows are kept).
7. **Verify replayability.** Confirm a stored row + its prompt_ref can reconstruct the call
   inputs, and that summed ledger cost reconciles against the provider invoice within tolerance.

## Rules
- One row per call, written exactly once, on every path including errors.
- Log the exact model id and the price rates used; never mutate historical rows on a price change.
- Token counts come from provider usage when present; flag estimates as estimates.
- Ledger is append-only and durable — not an in-memory list, not best-effort.
- Metering rows and prompt/response bodies have separate stores and separate retention.
- This talent records; it makes no tier, budget, or routing decision.
