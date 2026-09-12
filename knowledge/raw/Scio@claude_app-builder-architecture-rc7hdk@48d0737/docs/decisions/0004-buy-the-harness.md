# ADR-0004 · Buy the harness: Claude Agent SDK, self-hosted, one sandbox per build

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** E (build and execution)
**Supersedes / relates to:** replaces predecessor ADR-0005 (ACA dynamic sessions) and the hand-built relay/provider machinery of ADR-0006

## Context

The predecessor built its own model relay, provider abstraction, untrusted-text fence, reply
chunking, sandbox interface and job model. Its production sandbox was never run:
`choose_sandbox()` never returns `AcaSandbox`, whose `start` does not match its own interface and
which is excluded from the conformance suite (`docs/as-built/LAYER-E-BUILD.md` §6). Docker with
`CONTAINER_LIMITS` is a resource boundary, not a security boundary. The ceiling is checked after
the call it should stop, and the build that hits it is under-reported.

Fetched 2026-09-02 from Anthropic's documentation:

- **Claude Agent SDK** (`code.claude.com/docs/en/agent-sdk/hosting`): one `claude` subprocess per
  session; multi-tenant isolation via `settingSources: []`, per-tenant `CLAUDE_CONFIG_DIR`,
  per-session `cwd`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; `SessionStore` adapters for S3, Redis,
  Postgres; OpenTelemetry via environment; `maxTurns` as the built-in stop; a hosting cookbook
  for Docker, Modal and Kubernetes. Anthropic states token cost dominates container cost by an
  order of magnitude.
- **Claude Managed Agents** (`platform.claude.com/docs/en/managed-agents/overview`): hosted
  harness in beta (`managed-agents-2026-04-01`), cloud or self-hosted sandbox, durable event log;
  not eligible for Zero Data Retention or a HIPAA BAA; browser-in-sandbox not stated.
- Isolation primitives scanned 2026-08-26 (`docs/next/LAYER-E-BUILD.md` §3.3): Firecracker
  (E2B, Vercel Sandbox), gVisor (Modal), Cloudflare Sandboxes GA April 2026, ACA custom-container
  sessions still in preview.

## Decision

Scio's build loop runs on the Claude Agent SDK, self-hosted, with one isolated sandbox per build
and the tenant-isolation settings above applied on every `query()`. Scio owns what the harness
does not: the spec and contracts, the gates, the evidence report, a spend ceiling checked before
each call with the overshoot recorded, the untrusted-text boundary at the render edge, and the
stop rule from `build-loop-stops`. Model *and effort* are fixed per role in the routing table (E-28): Anthropic's
Fable 5 page names effort as the primary control (`high` default, `xhigh` for capability-sensitive work),
so two runs on the same model at different effort are different measurements. The `SandboxProvider` interface and its conformance suite are
carried forward; the provider behind it is chosen by five measured numbers before Slice 1 ships —
prewarm latency, concurrency limit, cost per session-hour, whether Playwright runs inside the
isolation boundary, and which regions it can place a build in (ADR-0010) — and the measurement is
attached to this ADR when taken.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Keep the hand-built relay and provider machinery (do nothing) | Rebuilds what the vendor now maintains, and it is the part of the predecessor with the ceiling and sandbox defects |
| Managed Agents now | Beta, no ZDR/BAA, and the browser-inside-sandbox question is unanswered; re-test when it leaves beta |
| Azure ACA dynamic sessions (predecessor ADR-0005) | Still in preview; never run; the four numbers were requested in 2026 and never produced |
| Docker on shared hosts | One kernel between tenants running model-generated code; the field consensus scanned 2026-08-26 is that this is not enough |
| **Goose** (Block; Apache-2.0, Agentic AI Foundation at the Linux Foundation, 60+ providers, per-session model switch, can drive Claude Code over ACP) — skills-repo note `model-agnostic-agent-harnesses`, verified 2026-09-02 | The right harness if "any model per task" were a requirement; it is not one for Slice 1, and Goose carries no documented multi-tenant isolation contract of the kind the Agent SDK's hosting page gives. Returns as the alternative if ADR-0004's "how we will know it was wrong" fires |
| Route the SDK to non-Claude models through a gateway (`ANTHROPIC_BASE_URL`) | Anthropic's own page states it "doesn't support routing Claude Code to non-Claude models through any gateway" (same note); and a gateway's `usage` payload makes cost rows non-comparable |

## Consequences

**What this buys.** Tool loop, subagents, skills, hooks, session persistence and telemetry
maintained by the vendor. Scio's own code shrinks to the parts that are the product.

**What it costs.** A dependency pinned to SDK versions (`source-grounded-implementation` applies to
every call). A sandbox provider bill per build. A migration when Managed Agents becomes eligible.

**What it forecloses.** Little; the SDK is a library and the provider sits behind an interface.

## How we will know it was wrong

A Slice 1 build needs a capability the SDK cannot expose (a gate that must run inside the
subprocess), the per-build sandbox cost exceeds the model cost of the same build, or the SDK's
`maxTurns` proves insufficient as a stop and the wrapper has to reimplement the loop anyway.
