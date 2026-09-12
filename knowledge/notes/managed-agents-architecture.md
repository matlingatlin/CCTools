---
title: Managed Agents — the architecture, and two lessons that transfer
sources:
  - url: https://www.anthropic.com/engineering/managed-agents
    note: "Anthropic engineering blog. An ARCHITECTURE post, not API documentation — no endpoints, schemas, quotas or pricing. The API reference it points to (platform.claude.com/docs/en/managed-agents/overview) was NOT read."
    fetched: 2026-08-29
tags: [agents, architecture, isolation, credentials, mechanics]
related: ["[[agent-design-template]]", "[[api-agent-loop]]", "[[effective-agents-anthropic]]", "[[subagents]]", "[[agent-builder-prior-art]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
---

# Managed Agents — architecture

A hosted service that *"runs long-horizon agents on your behalf through a small
set of interfaces meant to outlast any particular implementation."*

## The decoupling that is the whole idea

Three virtualised components, each able to fail or be replaced independently:

| | What it is |
|---|---|
| **brain** | Claude plus the harness — *"the loop that calls Claude and routes Claude's tool calls"* — the loop written out in full in [[api-agent-loop]]; this service's whole claim is that you should stop maintaining it |
| **hands** | sandboxes and tools — *"an execution environment where Claude can run code and edit files"* |
| **session** | *"an append-only log of everything that happened"* |

The harness is deliberately ignorant of what it is driving: *"it doesn't know
whether the sandbox is a container, a phone, or a Pokémon emulator."* Everything
is a tool with the signature `execute(name, input) → string`.

Containers are cattle: *"if a container died, the harness caught the failure as a
tool-call error."* Sessions outlive them. Operations named in the post: `wake`,
`getSession`, `emitEvent`, `getEvents`, `execute`, `provision`.

Anthropic operates the harness, the session log, container provisioning, the
credential vaults and the MCP proxies. The developer operates custom tool
implementations, resource configuration and VPC connectivity.

## Lesson one — the credential pattern, and it is our wall in another form

**The secret is never inside the thing that runs the code.**

> *"The tokens are never reachable from the sandbox where Claude's generated code
> runs."*

OAuth tokens sit in a vault; Claude calls MCP tools through a proxy that holds the
token and makes the outbound call. Git access tokens are wired into the local
remote at initialisation, so `push` and `pull` work **without the token being
present** for code to read.

That is architecturally the same move as [[agent-design-template]]'s rule that a
must-never is an absent tool rather than an instruction. Here the capability is
fully available and the *credential* is out of reach. Worth stealing whenever an
agent needs to act on a system it must not be able to exfiltrate from.

The same decoupling *"solved one of our earliest customer complaints"* — previously
reaching resources in a customer VPC required peering their network with
Anthropic's.

## Lesson two — harness assumptions go stale, and they have a measured example

Claude Sonnet 4.5 exhibited **"context anxiety"** — wrapping up tasks prematurely
— and the harness mitigated it with context resets. **Claude Opus 4.5 did not
exhibit the behaviour**, which made the mitigation unnecessary and its assumption
false.

This is a concrete instance of a workaround outliving its cause, from the people
who wrote the workaround. It is the argument for recording an **expiry condition**
beside every mitigation rather than only the mitigation. This library has the same
debt: pinned constants measured under conditions that have since moved, and
2026-workaround rows whose expiry conditions are already met.

## The one number

> *"our p50 TTFT dropped roughly 60% and p95 dropped over 90%."*

A real before/after on the decoupling, though the post gives no baseline figures,
no SLA and no method. Treat the direction as reported, the magnitude as unaudited.

## Debugging, and why the coupled design failed at it

Before decoupling, *"an engineer had to open a shell inside the container, but
because that container often also held user data, that approach essentially meant
we lacked the ability to debug."* The event stream alone *"couldn't tell us
**where** failures arose."*

The session log is now the observability surface, read by positional slices of the
event stream via `getEvents()`. **The lesson generalises: if the only way to
inspect a running agent is to enter the place where user data lives, you cannot
inspect it.** Our subagents have the same property — the transcript is the log,
and there is no other window.

## What the post does NOT contain

No endpoints, no request/response schemas, no event schema, no session state
machine, no error-handling contract, no quotas, no rate limits, no pricing, no
SLA, and no explicit comparison against the Claude API with your own loop or the
Claude Agent SDK. Nothing on scheduling or triggers. Nothing on evaluation, safety
gates or guardrails. Skills appear only in footer navigation.

For any of that, the API reference at
`platform.claude.com/docs/en/managed-agents/overview` is where to look — **it was
not read for this note.**

**And nothing about lifecycle governance**, which is the layer that sits above this
architecture rather than inside it. [[agent-builder-prior-art]] names it from the
third-party side — versioning, rollback, quarantine, approval gates, and a split between
the expert who owns business meaning and the operator who owns distribution — found in one
builder of three and absent from ours. Nothing in this post says who may approve an agent
or how a bad one is withdrawn either, so brain/hands/session decoupling does not supply it.
