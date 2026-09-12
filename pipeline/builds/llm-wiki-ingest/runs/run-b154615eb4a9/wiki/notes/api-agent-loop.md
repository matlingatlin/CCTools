---
title: The API agent loop — building a tool-using agent against the Messages API
sources:
  - url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent
    note: "Anthropic tutorial, five 'rings'. Rings 1-3 read and quoted. Rings 4-5 could NOT be retrieved — the page truncates mid-ring-3 on fetch, twice. Everything below attributed to the tutorial is from rings 1-3."
    fetched: 2026-08-29
  - url: "bundled skill: claude-api (Claude Code 2.1.250)"
    note: "Source for the Tool Runner section only, clearly marked. Not from the tutorial page."
    fetched: 2026-08-29
status: verified
tags: [api, agents, tool-use, sdk, mechanics]
related: ["[[agent-design-template]]", "[[agent-builder-prior-art]]", "[[subagents]]", "[[effective-agents-anthropic]]", "[[managed-agents-architecture]]", "[[loop-engineering-and-fable-prompting]]"]
---

# The API agent loop

A different craft from [[agent-design-template]], which is about Claude Code
subagents. This is about writing agent *code* against the Messages API. Recorded
because a third-party package we were sent ([[agent-builder-prior-art]]) teaches
this domain, and we had nothing authoritative to check it against.

## The loop, from the tutorial

```
1. messages = [the user request]
2. call the API with tools=[...]
3. WHILE response.stop_reason == "tool_use":
     a. for EVERY tool_use block in response.content:
          extract name, input, id  →  execute  →  collect result
     b. append {role: "assistant", content: response.content}
        append {role: "user", content: [ all the tool_result blocks ]}
     c. call again
4. stop_reason becomes "end_turn"  →  extract text blocks, return
```

Two `stop_reason` values drive it: **`"tool_use"`** continues, **`"end_turn"`**
exits. `tool_use_id` is what pairs a result to its call.

## Parallel tool use — the rule that catches people

> *"A single response can contain multiple `tool_use` blocks. Process all of them
> and return all results together in one user message."*

Iterate the whole `content` array, execute everything, and send **one** user
message carrying **all** the `tool_result` blocks. Not one message per tool.

To force one tool at a time: `tool_choice: {"type": "auto",
"disable_parallel_tool_use": true}`. The tutorial uses it in ring 1 for teaching
and drops it from ring 2 onward without comment.

## Two defensive practices it repeats

**Never index by position.** `next(block for block in response.content if
block.type == "text")` — scan the array; do not assume `content[0]` is text. A
response mixes block types.

**Keep the full history.** *"Keep the full conversation history in a list so each
turn sees prior context."* Every turn resends everything, so **token cost grows
linearly with conversation length** and the tutorial offers no summarisation or
pagination. That is the cost model to design around, not a detail.

## Tool schemas

`input_schema` is full JSON Schema, and the tutorial deliberately shows a
non-trivial one — nested objects, arrays with `"format": "email"`, enums,
`"minimum": 1`, and `required` listing only a subset so the rest are optional.
The stated reason: it is *"closer to real-world tools than a flat string
argument."*

## What the tutorial does NOT cover — read this before treating it as a guide

Checked deliberately, because the gaps matter more than the content for anyone
shipping:

| Absent | Consequence |
|---|---|
| **Error handling** | No guidance on signalling a tool failure back to Claude. The examples return `{"error": "Unknown tool: …"}` as data, and every `run_tool` returns hardcoded mock results |
| **Streaming** | Not mentioned |
| **Token budgets** | `max_tokens: 1024` hardcoded throughout; nothing on budget exhaustion |
| **Thinking** | Not mentioned |
| **Testing or evaluation** | Not mentioned at all |
| **Safety, permissions, human approval** | Not mentioned at all |
| **When NOT to build an agent** | Not mentioned |

It is a **tutorial, not a production guide**, and it says so in its own comments:
*"In a real system this would call your calendar API. Here the result is hardcoded
to keep the example self-contained."*

Anyone building from it alone ships an agent with no error contract, no budget
control and no approval gate. That is precisely the shape of the third-party
package in [[agent-builder-prior-art]], which adds `subprocess.run(..., shell=True)`
on top and nothing that the tutorial omits.

## Tool Runner — NOT from the tutorial page

**Provenance: the bundled `claude-api` skill, not the page above.** Rings 4–5,
where the tutorial reportedly replaces the hand-written loop with the SDK
abstraction, could not be retrieved — the page truncates mid-ring-3 on fetch, and
a second targeted attempt failed the same way. Verify against the SDK docs before
relying on any signature here.

`client.beta.messages.tool_runner` runs the request → execute → loop cycle over
tools you define. Per language: Python `@beta_tool`; TypeScript `betaZodTool` with
Zod; Java annotated classes; Go `BetaToolRunner` in the `toolrunner` package; Ruby
`BaseTool` + `tool_runner`; C# `BetaToolRunner` with raw JSON schema; PHP
`BetaRunnableTool` + `toolRunner()`.

Its **per-turn hooks** are the part worth knowing, because they are where the
tutorial's missing safety story lives: approval gates, logging, error
interception, result modification (adding `cache_control`, for instance), retries,
streaming and compaction.

**Do not confuse it with the Claude Agent SDK.** The Tool Runner is a thin helper
over `POST /v1/messages` that loops over tools *you* define — no built-in tools, no
filesystem, no sandbox. The Agent SDK is Claude Code packaged as a library, with
built-in Read/Write/Edit/Bash and the full harness. Both are harness-only: you
host and deploy either one.

## When this is the wrong tier

Anthropic's own decision table, from the same bundled skill: a single call for
classification, extraction or Q&A; a code-controlled workflow for multi-step
pipelines; this loop only when the task is genuinely open-ended and model-driven.
The four questions to clear first are complexity, value, viability, and **cost of
error** — can a mistake be caught and rolled back. A "no" on any of them means
stay at a simpler tier.
