---
name: structured-llm-extraction
description: "Use when a single LLM call must return data that conforms to a declared output schema (Pydantic model, JSON Schema, Zod, dataclass, TypedDict) and you want the model's response validated and auto-repaired instead of hand-parsing free text — the Instructor-style bind-schema-and-reask loop. Wraps the call so the schema drives generation, validates the raw response against it, and on validation failure feeds the exact validator error back to the model as a correction turn and retries until it conforms or a retry budget is hit. Triggers: 'extract structured/typed data', 'force JSON that matches this model', 'response_model / response_format', 'validate and retry the LLM output', 'Pydantic-validated extraction', 'coerce the answer into this shape', 'reask on schema error', 'stop parsing the model's prose by hand', field-level validators and enums the model must satisfy. NOT for bulk records where a deterministic regex/grammar parser should run first and only rejects hit a cheap LLM (use hybrid-parse-escalation), NOT for choosing a model tier (cost-aware-model-routing), NOT for logging calls (llm-call-ledger), NOT for grading open-ended quality with a judge (llm-judge-calibration)."
---

# Structured LLM Extraction

Bind a declared output schema to an LLM call so the response comes back typed and
validated — and when it does not, feed the validation error back and retry until it
conforms. Turns "parse the model's prose and hope" into a checked contract.

## When to use
- One (or per-item) LLM call whose result must populate a typed object your code consumes.
- You already have, or can declare, a schema: Pydantic/dataclass/TypedDict, JSON Schema,
  Zod, a struct — with field types, enums, required fields, and validators.
- You want malformed or off-schema responses repaired automatically, not silently accepted.

## When NOT to use
- Bulk field extraction where most records parse deterministically — run a regex/grammar
  parser first and escalate only rejects (`hybrid-parse-escalation`).
- Free-form prose output with no target shape, or open-ended quality grading
  (`llm-judge-calibration`). Model-tier or budget decisions (`cost-aware-model-routing`).

## Steps
1. **Declare the schema.** Define the exact target type with tight field types, enums,
   required-vs-optional, and field validators (ranges, formats, cross-field rules). The
   schema is the spec — encode every constraint you would otherwise check by hand.
2. **Bind it to the call.** Pass the schema as the response model / structured-output
   format so it is injected into the request (as a tool/function schema or JSON-Schema
   response format) and shapes generation. Keep the prompt about intent; let the schema
   carry the shape.
3. **Parse + validate the raw response.** Deserialize, then validate against the schema.
   Capture the full validator error (which field, which rule, what value) — do not discard it.
4. **Reask on failure.** If validation fails, append the model's bad output plus the
   validator error as a correction turn ("field X failed rule Y; return valid data") and
   re-call. The error text is the repair signal — pass it verbatim, do not paraphrase away detail.
5. **Bound the loop.** Retry up to a fixed budget (2–4 attempts). On exhaustion, raise a
   typed failure with the last error and attempts — never return unvalidated data.
6. **Return the typed object.** Hand back the validated instance. Optionally record
   attempts and final validity for observability.

## Rules
- The schema is the single source of truth for shape AND constraints — put every check in
  validators, not in downstream code.
- Always feed the *actual* validator error back on reask; a generic "try again" wastes turns.
- Cap retries and fail loudly. An infinite reask loop on a stubborn input burns tokens silently.
- Prefer provider-native structured output / tool-schema binding over prompt-only "return JSON";
  fall back to strict-parse-then-reask when the provider lacks it.
- Validate every attempt, including the first — never trust a well-formed-looking response unchecked.
- Keep it method-only: declare, bind, validate, reask, bound, return. No network or CLI calls here.
