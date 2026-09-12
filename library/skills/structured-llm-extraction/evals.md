# Evals — structured-llm-extraction

Functional regression test for the `structured-llm-extraction` talent. This is a
**technique** talent: bind a declared output schema to an LLM call so generation is
shaped by it, then validate the raw response against the schema and, on failure, feed the
*exact validator error* back as a correction turn and reask — bounded by a retry budget —
returning a validated typed object or a typed failure, never unvalidated data. Its
sharpest, most-differentiated behaviors are (a) putting every constraint in schema
validators rather than downstream code, (b) validating *every* attempt including the
first, (c) reasking with the verbatim validator error rather than a generic "try again",
(d) bounding the loop and failing loudly instead of returning partial/None, and (e)
declining when a deterministic parser or a different sibling talent is the right tool.

**Talent:** `structured-llm-extraction` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, reason the likely output WITHOUT the talent (baseline
Claude) against the output WITH the talent's method applied, and judge whether the
with-talent result is materially better and meets the observable pass criterion. Adversarial,
not a rubber stamp. The suite blends normal/representative application cases with clever
traps that tempt a plausible-but-wrong implementation, plus a negative-trigger that should
make the talent decline. Model: claude-opus-4-8.

---

## Scenario 1 — Extract typed fields from a document (application, core target)
- **Input:** "Given a raw invoice email body, extract into `Invoice{vendor: str, invoice_no:
  str, date: date, total: Decimal, currency: 3-letter code, line_items: list[Item]}`. Our
  downstream code consumes the object directly. Make the extraction return a validated object."
- **Pass criterion (observable):** Deliverable (a) declares the schema with tight field types
  (Decimal for money, ISO date, currency constrained to a 3-letter enum/pattern), (b) binds
  it to the call as a response_model / structured-output format (not a prose "return JSON"
  prompt), (c) validates the deserialized response against the schema, and (d) returns the
  validated typed instance. All four must be present.
- **Baseline (without talent):** Typically writes a prompt like "return the invoice as JSON
  with these keys", then `json.loads(resp)` and hands the dict downstream. `total` stays a
  string, `currency` unconstrained, `date` an arbitrary string; no validation step, so a
  missing key or a `"N/A"` total surfaces as a runtime crash deep in consumer code.
- **With talent:** Steps 1-2 encode the constraints in the schema and bind it so the shape
  is injected into the request; step 3 deserializes and validates; step 6 returns the typed
  `Invoice`. Money is Decimal, currency is checked, the object is guaranteed to satisfy the
  contract before any consumer sees it.
- **Result:** pass

---

## Scenario 2 — Enum + field-validator constraints the model must satisfy (application)
- **Input:** "Classify each support ticket into `Triage{category: enum[billing, bug,
  feature, other], severity: int 1-5, confidence: float 0..1, needs_human: bool}`. The
  category must be one of those four and confidence must be a probability."
- **Pass criterion (observable):** The constraints (category ∈ 4-value enum, severity in
  1-5, confidence in [0,1]) are expressed *as schema validators/enums* and enforced by
  validating the response — NOT left as free-text keys with the checks done (or skipped) in
  downstream code. An out-of-set category or `confidence: 1.7` must be caught by validation.
- **Baseline (without talent):** Often prompts "reply with category, severity, confidence"
  and trusts the reply. The model may return `category: "billing_issue"` or
  `confidence: 95` (a percentage), which passes `json.loads` and flows downstream as a
  silent semantic bug — the enum drift and the 0-100 vs 0-1 confusion are exactly the
  failures a plain-JSON approach does not catch.
- **With talent:** Rule "the schema is the single source of truth for shape AND constraints
  — put every check in validators." `category` is an enum, `severity` a bounded int,
  `confidence` a validated 0..1 float; `category: "billing_issue"` and `confidence: 95`
  both fail validation and trigger a reask.
- **Result:** pass

---

## Scenario 3 — The generic-retry trap (adversarial: reask must carry the real error)
- **Input:** "Our extractor sometimes returns bad JSON, so we already retry: on any failure
  we re-call the same prompt up to 3 times, then give up. It still fails a lot on the same
  inputs. What's wrong?"
- **Pass criterion (observable):** Identifies that re-calling the *same* prompt is a blind
  retry that carries no repair signal, and prescribes appending the model's bad output PLUS
  the **verbatim validator error** (which field, which rule, what value) as a correction
  turn before re-calling. Answering "add more retries", "raise temperature", or "the model
  is just bad" without the error-feedback loop = fail.
- **Baseline (without talent):** A plausible baseline response is "increase the retry count",
  "lower temperature for determinism", or "try a bigger model" — all of which leave the loop
  blind. Nothing tells the model *why* the last attempt was rejected, so a systematically
  off-schema input keeps failing the identical way until the budget is exhausted. This is
  the trap: the baseline treats the symptom (flakiness) not the cause (no feedback).
- **With talent:** Step 4 is exactly this fix — "append the model's bad output plus the
  validator error as a correction turn ('field X failed rule Y; return valid data') and
  re-call. The error text is the repair signal — pass it verbatim." Turns a blind retry
  into a guided repair; the reask now converges instead of repeating the same mistake.
- **Result:** pass

---

## Scenario 4 — Well-formed-looking response used unchecked (adversarial: validate every attempt)
- **Input:** "We bind a Pydantic response_model and the SDK gives us back parsed JSON, so we
  use the first response directly and only wrap the call in a try/except for JSON decode
  errors. Any problem with skipping the validation step when the JSON already parses?"
- **Pass criterion (observable):** Flags that *syntactically valid JSON is not schema-valid
  data* — a response can deserialize cleanly yet violate a field validator (enum out of
  set, number out of range, cross-field rule, wrong type coerced to string) — and insists
  on validating **every** attempt including the first, before returning. Endorsing "if it
  parses, use it" = fail.
- **Baseline (without talent):** The framing is seductive: "the JSON parsed, the SDK typed
  it, ship it." A baseline may agree that a decode-error try/except is enough, missing that
  a `severity: 9` (out of 1-5) or `currency: "US"` (2 letters) deserializes fine and passes
  straight through — a silent off-schema record that corrupts downstream state.
- **With talent:** Rule "Validate every attempt, including the first — never trust a
  well-formed-looking response unchecked," plus step 3's explicit deserialize-then-validate.
  The first response is run through the full validator; constraint violations are caught and
  reasked rather than accepted. Materially safer than the baseline's decode-only guard.
- **Result:** pass

---

## Scenario 5 — Bulk regular feed (negative-trigger: should decline / defer to sibling)
- **Input:** "We have 4 million access-log lines a day in a fixed `ip - - [ts] "METHOD path
  HTTP/1.1" status bytes` format. Pull `ip`, `ts`, `method`, `path`, `status`, `bytes` into
  a typed record for each line, cheaply."
- **Pass criterion (observable):** Does NOT propose wrapping every line in a schema-bound,
  validate-and-reask LLM call. Recognizes that a fixed-format feed parses deterministically
  and defers the bulk to a regex/grammar parser — naming `hybrid-parse-escalation` (parse
  deterministically first, escalate only the reject tail) as the right tool. Proposing an
  LLM extraction call per line = fail (over-triggering).
- **Baseline (without talent):** A naive baseline might reach for "structured output per
  line with a Pydantic model" because the ask says "typed record" — paying an LLM call for
  4M/day lines a single regex nails 99.9%+ of the time.
- **With talent:** "When NOT to use — Bulk field extraction where most records parse
  deterministically — run a regex/grammar parser first and escalate only rejects
  (`hybrid-parse-escalation`)." The talent declines to build a per-line reask loop and hands
  off. Correctly NOT firing is the win here.
- **Result:** pass

---

## Failure triage (if any scenario failed)
No scenarios failed. Triage rules retained for future runs:
- **test-bug** — scenario unfair/out-of-scope/subjective criterion, or baseline fails for
  reasons unrelated to the talent → fix the TEST, re-run, record the flaw in CURATION-LESSONS.
- **skill-bug** — talent fails a fair clever test → fix the talent; `drop` only if it cannot
  be made to beat baseline.

## Result summary
- Scenarios passed: **5/5** · failure_cause: **none** · verdict: **passed**
- Cross-references checked: `hybrid-parse-escalation`, `cost-aware-model-routing`,
  `llm-call-ledger`, `llm-judge-calibration` all resolve to existing talents — no dead-ref rot.
- Discriminating scenarios (S3, S4, S5) each have a plausible baseline failure the talent's
  method fixes; representative scenarios (S1, S2) confirm the everyday extraction job.
