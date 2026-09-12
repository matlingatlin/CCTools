---
title: OpenTelemetry GenAI semantic conventions - where they live, their status, the names for spans, metrics, events and cache tokens, as fetched 2026-09-09
sources:
  - url: https://opentelemetry.io/docs/specs/semconv/gen-ai/
    note: "Every page under it now reads 'Moved: Generative AI semantic conventions'; no attribute is defined there any more."
    fetched: 2026-09-09
  - url: https://github.com/open-telemetry/semantic-conventions-genai
    note: "The dedicated repository: docs/gen-ai/{README,anthropic,aws-bedrock,azure-ai-inference,gen-ai-agent-spans,gen-ai-events,gen-ai-exceptions,gen-ai-metrics,gen-ai-spans,mcp,openai}.md and docs/registry/. Releases page: 'There aren't any releases here'."
    fetched: 2026-09-09
  - url: https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md
    note: "Status Development; span name rule; inference span attributes with requirement levels; allowed values of gen_ai.operation.name and gen_ai.provider.name."
    fetched: 2026-09-09
  - url: https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md
    note: "Status Development; the twelve metric names with instrument and unit; gen_ai.token.type values; bucket boundaries."
    fetched: 2026-09-09
  - url: https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-events.md
    note: "Status Development; the two events; the evaluation event's attributes; content capture is Opt-In with a PII warning."
    fetched: 2026-09-09
  - url: https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/anthropic.md
    note: "Status Development; provider name 'anthropic'; the two cache attributes; the sum rule for input tokens."
    fetched: 2026-09-09
status: verified
tags: [opentelemetry, otel, gen-ai, semantic-conventions, observability, tokens, prompt-caching, evaluation, scio]
related: ["[[token-economy-playbook]]", "[[claude-agent-sdk-hosting-and-limits-2026-09]]"]
---
# OpenTelemetry GenAI semantic conventions, as of 2026-09-09

Why this note exists: Scio's ADR-0026 adopts the GenAI *names* for its spans, ledger rows and
gate verdicts. The predecessor read the state in July 2026 through a blog post; this note reads
the repository itself, dated, so the ADR pins what was actually there.

## Claims

| # | Claim | Source | Verbatim / value | Verdict |
|---|---|---|---|---|
| 1 | The conventions no longer live in the main semantic-conventions repository or on the opentelemetry.io spec pages | opentelemetry.io gen-ai pages; main repo docs/gen-ai/README.md | every page: "Moved: Generative AI semantic conventions"; "GenAI semantic conventions have moved to the OpenTelemetry GenAI semantic conventions repository" | MEASURED (fetched 2026-09-09) |
| 2 | The dedicated repository has no tagged release | github.com/open-telemetry/semantic-conventions-genai/releases | "There aren't any releases here" | MEASURED (fetched 2026-09-09) - pin a commit, not a version |
| 3 | Every document is in Development | gen-ai-spans.md, gen-ai-metrics.md, gen-ai-events.md, anthropic.md | "Status: Development" on each | MEASURED |
| 4 | Span name rule | gen-ai-spans.md | "Span name SHOULD be `{gen_ai.operation.name} {gen_ai.request.model}`" | MEASURED |
| 5 | Inference span attributes and levels | gen-ai-spans.md | `gen_ai.operation.name` Required · `gen_ai.provider.name` Required · `gen_ai.request.model` Conditionally Required · `gen_ai.response.model` Recommended · `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` Recommended · `gen_ai.conversation.id` Conditionally Required · `error.type` Conditionally Required · `server.address` Recommended · `gen_ai.usage.cache_read.input_tokens` / `gen_ai.usage.cache_write.input_tokens` Recommended when applicable | MEASURED |
| 6 | Allowed values include what Scio needs | gen-ai-spans.md | `gen_ai.operation.name`: chat, generate_content, text_completion, embeddings, retrieval, execute_tool, fetch_response, create_agent, invoke_agent, …; `gen_ai.provider.name` lists `anthropic` | MEASURED |
| 7 | Anthropic's input-token sum rule | anthropic.md | "Anthropic `input_tokens` excludes cached tokens. Compute: `gen_ai.usage.input_tokens = input_tokens + cache_read_input_tokens + cache_write_input_tokens`"; `gen_ai.provider.name` MUST be `"anthropic"` | MEASURED |
| 8 | The client metrics | gen-ai-metrics.md | `gen_ai.client.token.usage` Histogram `{token}` · `gen_ai.client.operation.duration` Histogram `s` · `gen_ai.client.operation.time_to_first_chunk` `s` · `gen_ai.client.operation.time_per_output_chunk` `s`; agent/workflow: `gen_ai.invoke_workflow.duration`, `gen_ai.invoke_agent.duration`, `gen_ai.invoke_agent.inference_calls` `{inference_call}`, `gen_ai.invoke_agent.tool_calls` `{tool_call}`, `gen_ai.execute_tool.duration`; server: `gen_ai.server.request.duration`, `gen_ai.server.time_per_output_token`, `gen_ai.server.time_to_first_token` | MEASURED |
| 9 | `gen_ai.token.type` has only `input` and `output` - no cache value on the metric | gen-ai-metrics.md | allowed values `input`, `output` | MEASURED - cache tokens are span attributes (claim 5), not a metric dimension |
| 10 | Token-usage bucket boundaries | gen-ai-metrics.md | [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 16777216, 67108864]; operation duration [0.01 … 81.92] doubling | MEASURED |
| 11 | The two events | gen-ai-events.md | `gen_ai.client.inference.operation.details`; `gen_ai.evaluation.result` with `gen_ai.evaluation.name` Required, `gen_ai.evaluation.score.label` and `gen_ai.evaluation.score.value` Conditionally Required, `gen_ai.evaluation.explanation` Recommended, `gen_ai.response.id` Recommended, `error.type` Conditionally Required; label examples `pass`; `fail` | MEASURED |
| 12 | Content capture is Opt-In and flagged | gen-ai-events.md | "GenAI instrumentations MAY capture user inputs … as events"; `gen_ai.input.messages` / `gen_ai.output.messages` Opt-In, "likely to contain sensitive information including user/PII data" | MEASURED |
| 13 | The commit the names were read at | github.com/open-telemetry/semantic-conventions-genai/commits/main (fetched 2026-09-09) | newest commit `b5d8440`, "Lock file maintenance (#504)", 2026-09-08 - the pin Scio records in place of a release | MEASURED |

## What it means here

- **Pin a commit and a date, not a version** (claims 2 and 13: `b5d8440`, read 2026-09-09); re-read on a cadence, because
  Development means renames without notice (the predecessor already saw `gen_ai.system` become
  `gen_ai.provider.name`).
- **The ledger's four token classes map exactly** (claims 5, 7): Scio's `ModelUsage.inputTokens`
  is the provider's uncached count, so the OTel `gen_ai.usage.input_tokens` is the sum of the
  three; the cache classes are span attributes. The metric's `gen_ai.token.type` cannot carry a
  cache dimension (claim 9), so per-class cost is derived from spans and the ledger, not the
  histogram - the ledger of [[token-economy-playbook]] §3.3 stays the priced record.
- **A gate verdict is `gen_ai.evaluation.result`** (claim 11): `evaluation.name` = the gate id,
  `score.label` = passed / failed / unjudged, `explanation` = the reason - the predecessor's
  reading holds a year on. OTel names no build id; that stays a Scio attribute.
- **Content capture stays off** (claim 12), which is what Scio's ADR-0022 step 5 decided for the
  transcripts; the SDK note [[claude-agent-sdk-hosting-and-limits-2026-09]] carries the `modelUsage`
  fields the span reads from.

The boundary whose content telemetry must never carry is described in [[preview-and-sandbox-egress-boundary-2026-09]].
