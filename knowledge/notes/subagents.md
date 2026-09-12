---
title: Subagents
sources:
  - url: https://code.claude.com/docs/en/sub-agents
    fetched: 2026-08-27
  - url: https://code.claude.com/docs/en/sub-agents
    fetched: 2026-09-04
    note: re-fetch; raw at knowledge/raw/claude-code-docs-2026-09-04/sub-agents@2026-09-04.md
tags: [claude-code, subagents, context, mechanics]
related: ["[[skill-anatomy]]", "[[dynamic-workflows]]", "[[hooks]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]", "[[api-agent-loop]]", "[[effective-agents-anthropic]]", "[[managed-agents-architecture]]", "[[testing-skills-methodology]]", "[[loop-engineering-and-fable-prompting]]", "[[model-agnostic-agent-harnesses]]", "[[harness-over-model-prime-agent]]", "[[architecture-evidence]]", "[[llm-idea-generation]]", "[[plugins-and-marketplaces]]", "[[third-party-landscape]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/sub-agents@2026-09-04.md
---

# Subagents

Specialized assistants that run in an **isolated context window** and return only a
summary — keeping verbose work (searches, logs, file contents) out of the main
thread. Each has a custom system prompt, restricted tools, and its own context.

Two measurements elsewhere in this base bound what that isolation is worth.
[[architecture-evidence]] credits the mechanism rather than the costume: removing agent
roles from a SWE-bench pipeline *lowered* the resolve rate, and what it credits is a
separate context plus a restricted tool surface — the two properties this page documents,
not the persona in the prompt. [[llm-idea-generation]] bounds the claim from the other
side: no multi-agent result there carries a matched single-model baseline, so fanning out
is a context device, not evidence that more agents produce better answers.

**The same isolation, built four other ways.** [[api-agent-loop]] is this mechanism by hand:
a fresh message list per sub-task, on the API, with none of the loading rules below.
[[managed-agents-architecture]] is it hosted — the isolation is the same, the machine and the
lifecycle are someone else's. [[harness-over-model-prime-agent]] records the sharpest
alternative: Prime Agent's RLM makes a sub-agent a *function call inside a persistent REPL*,
so context is a variable rather than a boundary. And [[model-agnostic-agent-harnesses]] holds
the harness fixed and swaps the model underneath, which is the one variation Anthropic states
is unsupported. [[effective-agents-anthropic]] names the pattern all four instantiate
(orchestrator–worker) and is the page to read for when it is worth it at all.

**What sits above and beside this page.** [[dynamic-workflows]] is the layer above — a
JavaScript script dispatching subagents at scale, where the concurrency measured below becomes
a parameter someone sets. [[hooks]] is the layer beside it and the one that answers what
crosses the boundary: a subagent's `hooks:` block lasts only while it runs, and a `Stop`
arrives as `SubagentStop` — the same reach question the `.claude/rules/` measurement below
answers negatively. [[testing-skills-methodology]] uses subagents as the instrument rather
than the subject: a fresh-context reviewer is the only reviewer that has nothing to defend.
[[agent-builder-prior-art]] is the reuse-first record for anyone about to generate these
definitions rather than write them, and its central finding is that "agent builder" names
three different artefacts — ours being precisely the subagent this page specifies.

## Locations & precedence (highest → lowest)

1. Managed settings → 2. `--agents` CLI flag → 3. `.claude/agents/` (project) →
4. `~/.claude/agents/` (user) → 5. plugin `agents/`. Name conflicts: highest
priority wins; closest-to-cwd wins among project dirs.

Plugin agents sit last because a standalone project or user agent **overrides** a
same-named plugin agent — [[plugins-and-marketplaces]] holds that rule, and the packaging
contract that produces the `agents/` directory at a plugin's root in the first place.

## What loads into a (non-fork) subagent at startup

Custom system prompt + env details (NOT the full Claude Code prompt); the task
message Claude writes; **the whole CLAUDE.md hierarchy**; git status snapshot;
full content of skills named in `skills:`; sibling roster for `SendMessage`.
**Does NOT get:** main conversation history, main auto-memory, previously invoked
skills, prior tool results. **Exception:** built-in Explore and Plan skip CLAUDE.md
and git status (that is why they stay small).

## Frontmatter fields

`name`, `description` (required — drives delegation). Optional: `tools`
(allowlist; **omitted = inherit ALL**), `disallowedTools` (**a specifier does NOT narrow it — `Bash(git push *)` removes Bash
entirely from the subagent**, added 2026-09-11; to keep Bash and block commands, the deny rule
goes in `permissions.deny`, which binds the main conversation too, so the fix has a wider blast
radius than the trap. This is the same shape as the `tools:`-omitted-inherits-ALL default
[[agent-design-template]] calls the most dangerous one here: the author believes they restricted
something and has instead deleted a capability), `model` (`sonnet`/`opus`/`haiku`/
`fable`/full-id/`inherit`; **omitting it is NOT the same as `inherit`** — corrected 2026-09-08
against the held bytes, `knowledge/raw/claude-code-docs-2026-09-04/sub-agents@2026-09-04.md:296`:
*"When you omit it, Claude Code picks the model in the subagent model order"*, i.e.
per-invocation → frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → the main model. This line
previously read "default `inherit`", which would have made `CLAUDE_CODE_SUBAGENT_MODEL` inert
and [[model-routing-free-and-local]]'s whole level-1 routing table with it. Version-tied caveat
the same bytes carry and neither note did: **before v2.1.251 the env var came FIRST** and
overrode both the per-invocation parameter and the frontmatter, `model: inherit` included),
`permissionMode` (**the main conversation's mode decides whether yours is
used at all, and as of v2.1.267 a subagent can no longer escalate itself** — added 2026-09-11:
under a `bypassPermissions`, `acceptEdits` or auto-mode parent the subagent runs in the parent's
mode and yours is ignored; under a `default`, `dontAsk` or `plan` parent yours applies *except*
`bypassPermissions`, which is refused and the parent's mode kept. `manual` is an alias for
`default`. This base carried neither the old rule nor the new one, and it sits directly beside
[[agent-design-template]]'s argument that a PreToolUse hook is the only real wall — that argument
now has a second, weaker guarantee next to it), `maxTurns`,
`skills` (preload full content), `mcpServers`, `hooks`, `memory`
(`user`/`project`/`local`), `background`, `effort`, `isolation: worktree`, `color`.

## Skills relationship (the key inversion)

The subagent `skills:` field is the **inverse** of a skill's `context: fork`. With
`skills:`, the subagent owns its system prompt and pulls skill content in; with
`context: fork`, a skill's content is injected into a chosen agent. A subagent can
still discover other skills via the Skill tool (unless `Skill` is removed from
`tools`); can't preload `disable-model-invocation: true` skills.

## Foreground vs background

Foreground blocks the main thread, passes permission prompts through, gets the
**full** tool set. Background runs concurrently, surfaces prompts in the main
session, and gets a **restricted** built-in tool set (Read/Grep/Glob/Bash/Edit/
Write/WebFetch/WebSearch/Skill/SendMessage/… — most others removed; MCP inherited).

**The tool pool is not purely subtractive — corrected 2026-09-11 (evening).** The page had been
read, here and upstream, as inheritance narrowed by two filters. It gained a sentence saying a
subagent can also be **given** tools the main conversation does not have: *"On macOS, Linux, and
WSL, a subagent can also receive the Glob and Grep tools when the main conversation doesn't have
them."* Platform-conditional, and in the widening direction. Worth holding because every mental
model built from "inherit, then remove" predicts the wrong tool list here, and because a
capability that appears only on three of the platforms is invisible to anyone testing on the
fourth.
In interactive sessions fork mode is on by default → spawns run in background.

## Fork

Inherits the ENTIRE conversation (system prompt, tools, model, full history) but
isolates tool calls. Use when a fresh subagent would need too much background, or
to try approaches in parallel. `/subtask <task>` (v2.1.212+). Forks reuse the
parent prompt cache (cheaper) and cannot nest.

## MEASURED: `.claude/rules/` does NOT reach a subagent

Tested 2026-08-28 with a canary probe (a rule file containing a unique phrase, a
subagent asked to report any canary in its context **before** touching any tool).

- **Result: the canary was absent.** The subagent correctly answered "no canary in
  context" rather than guessing, then read the file and confirmed the miss.
- **Only `CLAUDE.md` was injected** as a project instruction file. Also present:
  the `userEmail`/`currentDate` blocks, deferred-tool names, MCP server
  instructions, and skill **descriptions only** (names + one-liners, not bodies).
- Both an unconditioned rule and a `paths:`-scoped rule were planted; neither
  appeared.

**Design consequence: an agent's rules cannot live in `.claude/rules/`.** They must
go where a subagent actually loads from — `CLAUDE.md` (repo-wide, so every agent
gets every rule), the agent body itself (tier 0, which is what a system prompt is
for), a preloaded skill (tier 1), or a reference file the procedure opens (tier 3).

**Scope limit, stated by the probe itself:** this tests the *subagent* path only.
Whether the main session loads `.claude/rules/` is NOT established here — the probe
file was created mid-session, and rules load at session start, so the parent's
failure to see it proves nothing. Do not generalise this to the main session.

## Documented limits (re-verified 2026-08-28, re-fetched 2026-09-04)

| Limit | Value |
|---|---|
| **Combined descriptions of all non-built-in subagents** | **15,000 tokens.** Claude Code shows a startup warning with the total when exceeded. A **shared** budget across the whole roster — it bites as the roster grows, not per agent |
| Nesting depth | **3** (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` disables nesting). At the depth limit Claude Code **withholds the `Agent` tool from every subagent except a fork** |
| Concurrent subagents | **20** (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) |
| `MEMORY.md` in the subagent system prompt | first **200 lines or 25 KB**, whichever comes first |
| Transcript retention | `cleanupPeriodDays`, default 30 |
| `maxTurns` | field exists; **no default or maximum documented** |

**Explicitly NOT documented:** maximum size of the agent definition file; maximum
system-prompt length; context window (inherits from the model); truncation behaviour for
oversized inputs. (*Total subagents over a session's lifetime* left this list on 2026-09-04:
the page now states it outright — "There's no limit on the total number of subagents Claude
can spawn over a session." The absence is documented, which is not the same as undocumented.)

## Re-fetched 2026-09-04 — every value held, four details were missing

All four limits above were re-read against `code.claude.com/docs/en/sub-agents` fetched
2026-09-04 (raw: `knowledge/raw/claude-code-docs-2026-09-04/`). **Nothing had rotted** — 15,000,
3, 20 and the two env-var names are all still stated. What the page had gained:

- **The concurrency limit is not universal.** Sessions with **ultracode** active are exempt and
  the limit is not enforced there. The limit itself requires v2.1.217+.
- **The depth default has a history**, which matters when reading an older transcript:
  v2.1.172–v2.1.216 nested five layers deep and the limit could not be changed; v2.1.217–
  v2.1.218 defaulted to **one**, so a subagent could not spawn at all; v2.1.219 raised it to
  three.
- **A fork at the depth limit behaves differently from a subagent at it.** The subagent has
  `Agent` withheld; the fork *keeps* `Agent` in its inherited tool list and the tool returns an
  error instead of spawning. Same wall, two different failure shapes.
- **A file form of the system-prompt flag** (added by the page's second revision of the day,
  raw `…-2026-09-04b/sub-agents@2026-09-04b.md`): "If your text is too long to pass on the command
  line, save it to a file and pass the path with `--append-subagent-system-prompt-file` instead.
  The file flag requires Claude Code v2.1.261 or later." **The gap that used to be stated here is deleted rather than updated, and the deletion is the
point (2026-09-11).** The sentence has now gone stale three times: "29 releases above the highest
this base cites", corrected to "4 releases, the highest is v2.1.257", and then falsified again
within days by a single doc re-read that brought in v2.1.259, v2.1.260, v2.1.265 and **v2.1.267** —
which puts v2.1.261 *below* the ceiling rather than above it. Two readers working on disjoint
documents flagged it independently, which is what showed it to be a property of the base rather
than of any page. A statement whose truth depends on the state of the whole corpus cannot be
repaired by updating it; it has to stop being a stored value. So: **compute it, do not read it
here** — `grep -rho "v2\.1\.[0-9]\+" knowledge/notes/ | sort -uV | tail -1`. What remains fixed
is the flag's own requirement, which is a property of the flag: it was 29 releases above
  the highest this knowledge base cites, which is the freshness finding in one number.
- **`/subtask` has a rename behind it.** It requires v2.1.212+; on v2.1.161 through v2.1.211 the
  command is `/fork`. With agent view turned off, `/subtask` is unavailable and `/fork` starts
  the forked subagent instead.

So **there is no size cap on an agent body.** Against Opus 5's 1M-token context an
agent file is a rounding error. Keeping it short is a *quality* argument — the body
becomes the system prompt and shapes every turn — not a mechanical one. Say it that
way; do not dress it as a limit.

## Limits & gotchas

Transcripts at
`~/.claude/projects/{project}/{sessionId}/subagents/agent-{id}.jsonl`, survive
compaction, deleted after `cleanupPeriodDays` (30). Explore/Plan can't be resumed
(one-shot). Easy to get wrong: `tools` omitted inherits all (not none); background
silently drops non-listed built-ins.

## For this project

Subagents are the fan-out engine behind `deep-reading` ingestion and the eval
harness. Note for the factory: a normal subagent DOES load this repo's CLAUDE.md
(so doc-driven rules apply), but Explore/Plan do not — pick `general-purpose` when
the rules must hold.

---

## A subagent has no Task tool here — MEASURED 2026-09-01

Running the `skill-builder` agent unaided on a full build surfaced a limit nothing in
our design had accounted for: **the agent could not dispatch subagents.** No `Task` tool
was available to it.

**The vendor documents two fan-out paths this measurement never tried (re-read 2026-09-11), and
neither needs an `Agent` tool.** (a) *"When Claude sends a completed subagent a message with the
`SendMessage` tool, the subagent resumes in the background without a new `Agent` invocation"* —
and *"A subagent that has the `SendMessage` tool can send that message too"*, with the resumed
agent reporting back **to the subagent that resumed it, not to the main conversation**. (b) The
resume section speaks of *"background subagents of its own"*, so a subagent spawning subagents is
a documented arrangement. The measurement above is **not** contradicted: it found no `Task` tool,
and the docs never name one — they name `Agent`. But the design conclusion drawn from it needs
this beside it, because `SendMessage` **is** in the background tool set this note already records,
and it is a fan-out path the workaround never tested.

It worked around this by driving the headless CLI — `claude -p` — from fresh scratch
directories outside the repo, so none of the library's 88 skills loaded into the runs it
started. Never more than two concurrent. It captured cost per run.

**Verdict MEASURED**, n=1 agent, one environment. What it establishes is that the
capability cannot be *assumed*; it does not establish the rule for every host.

**Why it matters beyond the workaround.** Every orchestrating talent we own — `factory`,
`dispatching-parallel-agents`, `subagent-driven-development`, the `skill-builder` agent
itself — is written as though an agent can fan out. One level down, in this environment,
it cannot. An orchestrator that assumes it will either stop or improvise, and improvising
is what happened here.

Two consequences worth carrying:

- **A dispatching talent should state what it needs and check for it**, rather than
  discovering the absence mid-run.
- **The workaround is better than it looks.** Fresh scratch directories mean the runs
  loaded no skills at all, which is a *cleaner* baseline than our own harness produces —
  ours runs the without-arm inside a repo where 88 descriptions are in the listing. Worth
  copying deliberately rather than inheriting by accident.

## What a dispatched chain actually costs — MEASURED 2026-09-01

One agent, one full 38-phase build, 55 minutes wall clock. The distribution is not where
I predicted, and the prediction is worth recording alongside the number because it was
wrong in an instructive way.

| | |
| --- | --- |
| total wall clock | 55 min |
| logged run time | 15 min, 18 dispatched runs |
| **coordinator's own turns** | **roughly half the wall clock** |
| total tokens | 3.58M |
| **share in 6 probe/arm runs** | **82%**, at 420–570k each |

**The first diagnosis was wrong.** From my own earlier build I concluded the wall clock
was the cold sessions. It was not: in that build I was the coordinator and my turns never
appeared in any measurement. When the coordinator is an agent, its turns become visible
and they are half the cost. A cost model built from a run where you were the orchestrator
will systematically under-count orchestration.

**Why the six runs dominate the tokens:** each pasted the same fixture and the same method
body inline. Four runs over one fixture pay for it four times, and text that shifts
position in every prompt cannot be served from the prompt cache. Hand a run a PATH to
anything it can look up; paste only what it must not be able to find.

**And 12 of the 18 runs logged no duration at all** — only tokens. Two thirds of the run
was invisible to anyone trying to make it faster. Same class of loss as an unrecorded
spend: available at the moment, unrecoverable afterwards.

## The headless run's observable surface — MEASURED 2026-09-01

Measured directly by running `claude -p "<prompt>" --output-format json` from a fresh scratch
directory on this box (CLI 2.1.257), n=3 runs. Recorded because a benchmark that reads this
payload wrongly produces a **wrong number, not an error** — and did, twice, before it was fixed
(`pipeline/bench/`, prereg amendment 2).

**Top-level keys of the JSON result** (verbatim from a run):
`api_error_status`, `duration_api_ms`, `duration_ms`, `fast_mode_disabled_reason`,
`fast_mode_state`, `is_error`, `modelUsage`, `num_turns`, `permission_denials`,
`queued_turn_count`, `result`, `session_id`, `stop_reason`, `subagent_stats`, `subtype`,
`terminal_reason`, `time_origin_ms`, `time_to_request_from_spawn_ms`, `time_to_request_ms`,
`total_cost_usd`, `ttft_ms`, `type`, `usage`, `uuid`, `warm_spare_claimed`.

Three findings, each of which cost a defect to learn:

1. **A headless run cannot read outside its own working directory.** Given an absolute path into
   another tree it does not error — it *declines*, in prose, in about 6 seconds, and exits 0 with
   a well-formed JSON result. Any harness that times such runs is timing a refusal. Copy the
   inputs into the run's cwd. **MEASURED**, n=1, reproduced by the fix.
2. **`modelUsage` has MORE THAN ONE key.** A run pinned with `--model claude-sonnet-5` reported
   `['claude-haiku-4-5-20251001', 'claude-sonnet-5']` — the requested model plus an auxiliary the
   CLI uses internally. Reading `list(modelUsage)[0]` therefore reports the *auxiliary* model for
   a correctly-served run. Check membership, never position. **MEASURED here, n=3** (all three runs; corrected 2026-09-04 from REPEATED - `pipeline/contracts/claims.contract.json` defines REPEATED as *the source restates a finding measured by someone else*, and we measured this ourselves. The small sample is the honest caveat and belongs in the number, not in the verdict).
3. **`--model` does take effect** in a headless run; the apparent mismatch in (2) was entirely the
   reader's. **MEASURED here, n=3** (same correction).

**`duration_api_ms` vs `duration_ms` splits waiting-on-the-API from local work** — the quantity
that decides whether a dispatch cap is protecting against real contention. It varies sharply by
model on the same box and the same prompt:

| Model | `duration_api_ms` / `duration_ms` | Share NOT spent waiting on the API |
|---|---|---|
| `claude-sonnet-5` | 5079 / 10786 | ~47% local |
| `claude-opus-5` | 11917 / 15177 | ~22% local |

**Weak: n=1 each, both taken under load with a build running**, which inflates the local share in
both rows. Directional only. What it does establish is that **"is this workload network-bound?"
has no model-independent answer** — the heavier model spends proportionally more of its wall clock
waiting, so a dispatch cap tuned on one model is not evidence about another. A benchmark of
concurrency must therefore pin the model it is answering for. The clean version is the registered
benchmark at `pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md`, pinned to Opus 5, which has not
run.

## Dispatch concurrency 2 vs 4 on a 4-core box — MEASURED 2026-09-01

Preregistered before any number existed (`pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md`),
rows in `pipeline/bench/runs/`. 56 headless `claude -p` runs on `claude-opus-5`, 8 per batch,
3 valid batches per arm, arms alternated, $9.18.

| | concurrency 2 | concurrency 4 |
|---|---|---|
| Batch wall clock, median of 3 | 59.0s | **32.8s** |
| Per-run duration, median | 13.6s | 15.1s |
| Failed runs | 0 | 0 |

**Ratio 0.556** against a threshold of 0.70 fixed in advance. Per-run cost of the higher
concurrency is **1.11x**, well inside the 1.5x guardrail. **MEASURED here, 3 batches per arm** (same correction: our own paired runs, not a restatement of someone else's finding).

**The thing worth carrying to another project:** the prior value came from `min(16, cores-2)`,
a formula that models **CPU** contention. The median run here spent **73% of its wall clock
waiting on the API** (`duration_api_ms` over `duration_ms`, 56 runs). A core-count formula does
not describe a workload that is three-quarters network wait, and four agents fitted comfortably
where it predicted two would not. Before accepting a concurrency cap derived from cores, measure
the API-wait share of one run — it is one field in `--output-format json` and it decides whether
the formula applies at all.

**Bounds, stated because a measurement widens quietly otherwise:** this licenses 4, not 8 or 16,
which were not run. It is silent on write collisions between parallel agents, which is a
correctness constraint no wall-clock number can speak to. It is one box, one model, one date.

**One instrument fault, recorded before the verdict and unresolved by it.** A concurrency-4 batch
leaves the box at loadavg ~1.84 and a concurrency-2 batch at ~0.94, while the driver only waited
for 0.50 — so only the first batch ever started cold, and no concurrency-4 batch did. Cold and
warm batches of identical work differed ~10%. Two post-hoc checks (dropping the cold batch;
counting the voided one) moved the ratio to 0.554 and 0.578, so the win survives either way, but
both are **exploratory**. A cleaner design waits to a fixed low load before *every* batch and
randomises arm order rather than alternating.

## Three ways an ad hoc dispatch script poisons a paired comparison — MEASURED 2026-09-02

Source: build `data-contract-assertions-v2` (`pipeline/builds/data-contract-assertions-v2/`,
36 arm runs for 12 valid observations), read from the run outputs, not from any gate. All
three faults were in shell written for that build and none was visible to a check.

- **A shared working directory.** MEASURED: a later run in the same directory read the
  earlier run's answer file and continued from it. Fix that generalises: one fresh directory
  per run, created `exist_ok=False`, named by a hash of label plus nonce.
- **The arm name in the path.** MEASURED: six of twelve answers wrote their own working
  directory into their text ("artefacts are in `.../with-arm/`"), so a grader handed the
  relabelled files could still read the arm off the prose. Blinding by label does not blind
  by content. Fix: the path carries no arm string, and every output is regex-scanned for the
  arm vocabulary before it reaches a grader (`arm_leak`).
- **The method mounted for every arm.** MEASURED: `--add-dir <skill>` was passed to all three
  arms, so the bare baseline cited the skill's own reference material. Fix: the mount is a
  parameter that raises for any arm but `with`.
- **The usage payload was never captured.** MEASURED: every cost row of that build had
  `tokens=None`, and the cost gate returned clean, so the cost clauses of the verdict had
  nothing to judge. `--output-format json` carries `usage` and `modelUsage`; sum the
  `*_tokens` fields and treat a zero as a run that did not report, not as a cheap run.

The generalisable lesson: the harness is part of the instrument, and a harness rewritten per
experiment cannot be trusted by the experiment that uses it. In this repo the four fixes are
`pipeline/build/dispatch.py`, with each fault reconstructed as a positive control in
`selftest_dispatch.py`. Neighbour: `testing-skills-methodology.md` (mutation-testing the
controls that guard this). These four faults are also carried as rows in
[[third-party-landscape]], which compiles what the whole harvest taught and files them
beside the third-party defects they rhyme with — an unpriced model reported as $0, a zero
from a broken pipe read as good news.

**Why three verdicts moved on 2026-09-04.** A verification pass ranked this note high because it
carried three REPEATED claims — then found none of them was a reading job. All three are our own
paired measurements at n=3. Under the claims contract that is **MEASURED**: the verdict records
**who did the measuring**, not how confident anyone is, and the contract says outright that the
two "are not strong and weak". Using REPEATED to mean "small sample, treat with care" borrows a
provenance label for a confidence job, and the cost is concrete: it put this note at the top of a
queue for work that cannot be done, because no source exists to re-read. The uncertainty is real
and is now carried where it belongs — in the stated **n**.
