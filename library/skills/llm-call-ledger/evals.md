# Evals — llm-call-ledger

Functional regression test for the `llm-call-ledger` talent. This is primarily a
**technique** talent (it defines a per-call ledger schema and a write method) with a
strong **discipline** spine (write-on-every-path, append-only, never mutate historical
rows, provider-usage over estimates, separate stores for bodies vs. metering). So the
scenarios below mix *application* cases (a real logging task it should improve) with
*pressure/trap* cases that tempt a plausible-but-wrong implementation, plus one
*boundary* case where it should decline and defer to a sibling talent.

Method: for each scenario, reason the likely output WITHOUT the talent (baseline)
against the output WITH the talent's method applied, and judge whether the talent
produces a materially better, criterion-meeting result. Adversarial, not a rubber stamp.

Date run: 2026-08-27 · Model: claude-opus-4-8

---

## Scenario 1 — Representative: "add logging around our model calls" (application)

**Input.** "We call the LLM in a few places and have no visibility. Add logging around
the model calls so we can see what's happening and later report spend in COSTS.md."

**Pass criterion.** Produces a *structured, per-call ledger row* with (at least) exact
model id, params, input/output token counts, computed cost with the rate table used,
latency, status, timestamp, and a run/request id — plus a prompt/response *ref* rather
than an unstructured log line. Explicitly ties rollups to COSTS.md.

**Baseline (no talent).** Adds a `logger.info(f"called {model}: {response}")` at the
call site, maybe wrapping timing. Logs prose, not a schema. No token counts, no cost,
model may be an alias, nothing queryable, error path unlogged. "Reporting spend in
COSTS.md later" is impossible because nothing numeric was captured per call.

**With talent.** Step 1 fixes the schema (id, timestamp, run_id, actor, provider, exact
model, params, input/output/cache tokens, cost + rate version, latency, status,
prompt_ref/response_ref). Step 4 computes cost explicitly; step 5 defines run/day/model
rollups that COSTS.md reports against. The deliverable is a queryable metering table,
not scrollback.

**Verdict: PASS.** Materially better — turns unstructured logs into an auditable,
queryable ledger that actually feeds COSTS.md.

---

## Scenario 2 — Trap: only the success path gets logged (error/refusal path)

**Input.** "Here's my call wrapper — it logs the row after `response = client.call(...)`
returns. Looks complete, right?" (The ledger write sits *after* the call, on the happy
path only.)

**Pass criterion.** Flags that failed, refused, and timed-out calls still burn tokens
and must be logged; moves the ledger write into a `finally`/deferred path with a
`status` of ok/error/refusal. Does NOT bless the happy-path-only wrapper.

**Baseline (no talent).** "Looks good" — the code compiles and logs on success, which
is the visible case. Silent gap: every error/refusal/timeout is invisible, so spend is
under-counted and the invoice will never reconcile. Exactly the case people forget.

**With talent.** Rule "One row per call, written exactly once, on every path including
errors" + Step 3 force the write into `finally` and require a `status` field. Refusals
and errors become first-class rows.

**Verdict: PASS.** The talent catches the single most common ledger bug; baseline
rubber-stamps it.

---

## Scenario 3 — Trap: back-fill new prices onto old rows (historical mutation)

**Input.** "Our provider raised prices yesterday. Run an UPDATE to set the `cost`
column across the whole ledger to the new rates so the numbers are consistent."

**Pass criterion.** Refuses to mutate historical rows; keeps each row's cost at the
rates in effect when the call happened, recorded with a rate-table version. New rates
apply only to new rows. Explains that overwriting breaks reconciliation with past
invoices.

**Baseline (no talent).** Complies — writes the UPDATE. Now historical cost no longer
matches what was actually billed; past-invoice reconciliation is destroyed and the
"consistency" is a fiction. Plausible-sounding instruction, silently corrupting.

**With talent.** Rules "never mutate historical rows on a price change" and "Record the
rate table version alongside the row" (Step 4) directly forbid this and give the correct
alternative (version the rate table, apply forward only).

**Verdict: PASS.** Talent blocks an irreversible data-integrity error the baseline
would execute on request.

---

## Scenario 4 — Trap: inline full prompt/response bodies into the metering table

**Input.** "Just add `prompt_text` and `response_text` columns to the metering table and
store the full strings there — simplest thing that works. Some prompts include the
user's uploaded document."

**Pass criterion.** Separates bodies from metering: content-address (hash → blob) or a
separate store, keep only the ref in the row; applies redaction at write time for the
uploaded-document PII; sets separate retention for bodies vs. rows. Does NOT inline
megabyte payloads or raw PII into the queryable table.

**Baseline (no talent).** Adds the two text columns as asked. Metering table balloons,
queries slow, and raw user-document PII lands in the spend table with the same retention
as cost rows — a privacy and cost problem shipped as "the simple thing."

**With talent.** Step 2 (bodies content-addressed, only hash/ref in the row), Step 6
(redact at write time, retention policy), and the rule "Metering rows and bodies have
separate stores and separate retention" all fire together.

**Verdict: PASS.** Talent prevents a table-bloat + PII-leak design the baseline accepts
verbatim.

---

## Scenario 5 — Trap: estimate tokens instead of reading provider usage

**Input.** "The response object has a `usage` field but it's easier to just estimate
tokens as `len(prompt)//4` for both input and output. Good enough for the ledger?"

**Pass criterion.** Insists on taking token counts from the provider `usage` when
present; only falls back to estimates when usage is unavailable, and then marks the row
as estimated. Rejects blanket estimation when real counts are in hand.

**Baseline (no talent).** "Sure, `len//4` is a fine approximation." The ledger then
disagrees with the invoice (estimates ignore tokenizer, cache tiers, system prompt,
reasoning tokens), and nobody can tell estimated rows from measured ones.

**With talent.** Rule "Token counts come from provider usage when present; flag
estimates as estimates" + Step 3 force reading `usage` and marking any estimate.

**Verdict: PASS.** Talent preserves invoice reconciliation; baseline quietly poisons it.

---

## Scenario 6 — Boundary: it should NOT fire (routing/budget decision)

**Input.** "This batch job is getting expensive. Pick a cheaper model tier for the easy
items and cap the run at $20 so we don't blow the budget."

**Pass criterion.** Recognizes this as a routing/budget *decision*, not a recording
task; defers to `cost-aware-model-routing` (and/or `context-budget`). It may note that
whatever runs should still be logged to the ledger, but it does not itself pick tiers or
set budget ceilings.

**Baseline (no talent).** A generic assistant would just start proposing tiers and a
budget cap — reasonable, but it means this talent, if it over-triggered, would be doing
another talent's job and muddying the boundary.

**With talent.** The description's explicit NOT clause ("NOT for deciding which tier or
budget a call should use … this only RECORDS") and the "makes no tier, budget, or
routing decision" rule keep it in its lane and hand off cleanly.

**Verdict: PASS (correct decline).** Clean boundary; the talent records, it does not
route.

---

## Summary

| # | Type | Criterion met with talent? | Beats baseline? |
|---|------|----------------------------|-----------------|
| 1 | Application — structured ledger | Yes | Yes (unstructured logs → queryable ledger) |
| 2 | Trap — error-path logging | Yes | Yes (catches the top ledger bug) |
| 3 | Trap — historical price mutation | Yes | Yes (blocks data corruption) |
| 4 | Trap — inline bodies + PII | Yes | Yes (prevents bloat + PII leak) |
| 5 | Trap — estimate vs provider usage | Yes | Yes (preserves reconciliation) |
| 6 | Boundary — routing/budget decline | Yes | Yes (clean hand-off, stays in lane) |

**Scenarios passed: 6 / 6.**

**Verdict: PASSED.** On every scenario the talent produces a materially better,
criterion-meeting result than baseline, and it declines correctly on the out-of-scope
case. The schema (Step 1) and the four load-bearing rules (write-on-every-path,
no-historical-mutation + rate versioning, provider-usage-over-estimates, separate
stores + redaction) are each what turn a plausible-but-wrong baseline into a correct
implementation.

**Minor note (not blocking).** The talent asserts "written exactly once … on every path"
but gives no *mechanism* for idempotency under retries — a `finally` write inside a retry
loop can emit duplicate rows for one logical call. The invariant is stated; an
implementation hint (idempotency key = request_id, upsert/dedup) would close the last
gap. Enhancement, not a defect that costs it the eval.
