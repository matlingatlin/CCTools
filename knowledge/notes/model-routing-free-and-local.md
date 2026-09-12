---
title: Routing to free and local models — mechanics, limits, and which jobs may leave Claude
sources:
  - url: https://docs.ollama.com/api/anthropic-compatibility
    note: "Endpoint /v1/messages; ANTHROPIC_BASE_URL=http://localhost:11434, ANTHROPIC_AUTH_TOKEN=ollama; 'ollama launch claude'; unsupported: count_tokens, tool_choice, metadata, prompt caching, batches, citations, PDF blocks, streaming error events; budget_tokens accepted but not enforced; URL images unsupported."
    fetched: 2026-09-02
  - url: https://openrouter.ai/docs/api-reference/limits
    note: "Free models: 20 requests/minute; 50 requests/day with no credits ever bought; 1,000/day once $10 of credits has been purchased all-time. The page says nothing about logging."
    fetched: 2026-09-02
  - url: https://code.claude.com/docs/en/llm-gateway
    note: "'Anthropic doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway.' Subscription not used while a gateway credential is active; base URL alone keeps the subscription login active."
    fetched: 2026-09-02
  - url: https://code.claude.com/docs/en/llm-gateway-protocol
    note: "Gateway must forward cache_control and the anthropic-beta capabilities; CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY keeps model ids containing 'claude' or 'anthropic'; attribution block stable since v2.1.181. Read 2026-09-02; the relevant sentences are quoted in [[model-agnostic-agent-harnesses]]. RE-READ 2026-09-08 after watch.py reported the page changed: the cited filter is unchanged and now stated more precisely -- 'keeps an entry when its id contains claude or anthropic anywhere in the string, matched case-insensitively', with provider-prefixed ids such as vertex_ai/claude-sonnet-4-6 passing, and 'before v2.1.223, Claude Code kept an entry only when its id BEGAN with claude or anthropic, which hid provider-prefixed IDs'. What changed is the PICKER LABEL, not the filter."
    fetched: 2026-09-11
  - url: https://platform.claude.com/docs/en/about-claude/pricing
    fetched: 2026-09-02
  - url: https://code.claude.com/docs/en/model-config
    note: "ANTHROPIC_DEFAULT_{FABLE,OPUS,SONNET,HAIKU}_MODEL accept 'full model name or provider identifier'; HAIKU also drives background functionality; CLAUDE_CODE_SUBAGENT_MODEL; CLAUDE_CODE_EFFORT_LEVEL. RE-READ 2026-09-08: the pinned-model DISPLAY rules changed, see section 9."
    fetched: 2026-09-11
  - url: https://code.claude.com/docs/en/sub-agents
    note: "Subagent model field: sonnet/opus/haiku/fable, a full id, or inherit; resolution order per-invocation → frontmatter → CLAUDE_CODE_SUBAGENT_MODEL → main model; CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1. No per-subagent base URL is documented."
    fetched: 2026-09-02
  - url: https://arxiv.org/abs/2305.05176
    note: "FrugalGPT (Chen, Zaharia, Zou, 2023): the LLM cascade. Abstract only, fetched 2026-09-02."
    fetched: 2026-09-02
  - url: https://arxiv.org/abs/2406.18665
    note: "RouteLLM (Ong et al., 2024): a learned router from preference data. Abstract only, fetched 2026-09-02."
    fetched: 2026-09-02
  - note: "Model figures (Qwen3.8-27B, GLM-5.3/Flash, Kimi K3, memory tiers, Z.ai's Anthropic-compatible endpoint) are in [[best-local-llm-2026-09]] and [[glm-5.3-local]]; free-tier routers (free-claude-code, OmniRoute, claude-code-router, the '260 free APIs' list) in [[model-agnostic-agent-harnesses]] and [[claude-code-ecosystem-plugins]]. This note does not repeat them; it decides."
tags: [routing, local-inference, free-tier, ollama, gateway, openrouter, cost, policy, data-posture]
related: ["[[model-agnostic-agent-harnesses]]", "[[subagents]]", "[[best-local-llm-2026-09]]", "[[glm-5.3-local]]", "[[claude-code-ecosystem-plugins]]", "[[token-economy-playbook]]", "[[local-finetuning-layer-streaming]]", "[[third-party-landscape]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/sub-agents@2026-09-04.md
  - knowledge/raw/watch-2026-09-11/code.claude.com_docs_en_llm-gateway-protocol.md
  - knowledge/raw/watch-2026-09-11/code.claude.com_docs_en_model-config.md
  - "the watch-2026-09-08b copies are kept: they are the provenance of section 9's rows" 
  - "partial: 3 of 9 distinct source URLs kept as raw; the rest predate the raw layer (2026-09-02)"
---

# Routing to free and local models

Written 2026-09-02 to answer: *explore routing to free LLMs, or local ones.* The landscape
notes already say what exists and what it scores. This note says how each path is wired,
what silently breaks on it, what the free tiers actually allow per day, and — the part
nobody else writes down — which of *our* jobs may go there and which may not.

## 1. Four arms, one variable

Everything that runs Claude Code or the Agent SDK against another model goes through
`ANTHROPIC_BASE_URL` plus a credential. Four arms, in increasing distance from the
supported path:

| arm | wiring | what it costs | what silently breaks |
|---|---|---|---|
| **A · Claude, native** | nothing | list price ([[token-economy-playbook]] §2.4) | nothing; the only supported path |
| **B · hosted non-Claude, Anthropic-compatible endpoint** (Z.ai GLM-5.3 / Flash) | `ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`, `ANTHROPIC_AUTH_TOKEN`, `API_TIMEOUT_MS` | GLM-5.3 $1.40 / $4.40; Flash **$0.15 / $0.50** per MTok — **doubled on 2026-09-09**, when Z.ai's 50% launch discount expired exactly as its own page said it would (*"The promotion ends at 24:00 on September 9, 2026"*). This cell read $0.075 / $0.25 until 2026-09-11 and was a PROMOTIONAL price quoted as a standing one; the watcher caught the expiry two days after it happened | the `usage` payload is whatever Z.ai returns; caching multipliers are Z.ai's; data-use terms unread; Anthropic: unsupported |
| **C · free tiers through a router/gateway** (OpenRouter `:free`, free-claude-code, OmniRoute, claude-code-router, LiteLLM) | `ANTHROPIC_BASE_URL=http://localhost:<port>` + the router's token; `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` to list its models | $0 per token; **20 req/min, 50 req/day** unfunded, 1,000/day after $10 bought (OpenRouter) | rate limits; provider logging/training clauses per endpoint; caching only if the router forwards `cache_control`; model discovery keeps only ids containing "claude"/"anthropic", so non-Claude ids need the router's own picker; each Claude Code release can break a router that does not forward the new headers; router software itself is fourth-gate material |
| **D · local, Ollama** | `ANTHROPIC_BASE_URL=http://localhost:11434`, `ANTHROPIC_AUTH_TOKEN=ollama`, or `ollama launch claude` | electricity and a machine ([[best-local-llm-2026-09]]: 24 GB GPU → Qwen3.8-27B; 128 GB → GLM-5.3-Flash 3-bit) | **no prompt caching, no `count_tokens`, no `tool_choice`, no Batch, no PDF blocks, no citations, no streaming error events; `budget_tokens` accepted but not enforced; URL images unsupported** (MEASURED, Ollama docs 2026-09-02) |

Two facts from Anthropic's gateway page settle the frame (MEASURED): the mechanism is
documented and *"Anthropic doesn't … support routing Claude Code to non-Claude models
through any gateway"*; and while a gateway credential is active *"a developer's claude.ai
subscription isn't used"*. So arm C and D are not "Claude Code for free" — they are the
CLI driving a different model, with the subscription idle.

## 2. The decisive number: a free tier cannot run the product

Scio's own measurement ([[token-economy-playbook]] §2.2): one build is **29 relay calls**
if every package passes first time and **79** if every package needs three attempts. An
unfunded OpenRouter free tier allows **50 requests a day** across all free models; funded,
1,000. One customer build can exhaust the unfunded tier before its first repair round, and
twenty builds exhaust the funded one. Free tiers are for **experiments and offline
batches**, never for a customer-facing path. That is the whole routing question for the
product, answered by arithmetic.

Local (arm D) has no request limit but loses the three things Scio's cost model depends
on: prompt caching (the ≈$0.41-per-build fix does not exist there), `count_tokens` (no
pricing without it), and the Batch API. It also has no Anthropic data-processing terms to
point a customer at; what it has is *no network at all*, which is the one thing a customer
with "store: no, sensitivity: high" may value more.

## 3. Which jobs may leave Claude — the matrix

"May" means: allowed under our rules, with the cost row marked non-comparable and the
result never counted as a measurement of the talent. "Must stay" means the product's or
the pipeline's promise rests on the model the skills were measured on.

### 3.1 Building Scio (our own work, skills-repo and Scio)

| job | arm | why |
|---|---|---|
| `dispatch.py` with-arm and baseline arm (talent measurement) | **A only** | the talent is graded on Fable/Opus; a result on another model is a different experiment (Scio ADR-0008: re-measure every skill per model) |
| "does this skill help a non-Claude model too?" | B, then C/D | a *third* arm, own `TIERS` entry, `usage` checked first, never in the measured path ([[model-agnostic-agent-harnesses]]) |
| harvest grading, rejection categorisation, description drafts, summarising raw intake | B or D, Batch on A otherwise | high volume, low stakes, reviewed before landing; on A use Batch (50%) |
| anything touching a private repository, a customer fixture, or a credential | **A or D** | a free endpoint may log; a local model cannot exfiltrate |
| knowledge-base search, section retrieval, graph queries | none | no model call at all (`kb.py`, graphify code-only) |

### 3.2 Inside Scio (the product's own calls)

| call | arm | why |
|---|---|---|
| intake classification, `advise_grouping`, yes/no judgements at temperature 0 | A on Haiku 4.5 / Sonnet 5 low effort; **candidate for D** once a hosted local box exists | constrained output, cheap to verify, no caching expected under Haiku's 4,096 floor anyway |
| architecture derivation, validation rules, deterministic edits | none | rules, not a model (Layer B is "close to free"; Layer F §4.1 −100%) |
| codegen, repair, critique, the whole | **A** | the promise is developer-grade output; every skill in the loop was measured on Claude; caching, Batch and `count_tokens` are load-bearing |
| a customer who answered *store: yes, sensitivity: high, region: EU* (ADR-0010) | A in an EU-served configuration; **never C**; D only if Scio hosts the box | a free endpoint's logging clause is a data-processing decision the customer did not make |
| a customer who answered *store: no* | A with zero-retention where offered; D is the only arm that is offline by construction | see the hosting/ZDR discussion in Scio's review |

### 3.3 Apps that Scio generates

The customer owns the app (ADR-0009 buy-out as key transfer). The generated app reads its
provider from environment: default Claude; the same base-URL variable lets the customer
point it at B, C or D after buy-out. Scio's generator must not hard-code a feature that
arm D lacks (PDF blocks, citations, `tool_choice`) without a fallback, or the app breaks
the day the customer goes local. That is a codegen rule, not a routing rule, and belongs in
the contract's house rules.

## 4. Rules for any routed run (all four arms except A)

1. **Own tier, marked non-comparable.** A routed run gets its own `TIERS` entry; its cost
   row is never averaged with native runs.
2. **Check `usage` before trusting tokens.** The payload is whatever the endpoint reports;
   Ollama reports no cache fields at all.
3. **Read the data-use terms before the first request**, per endpoint, and record the
   date. OpenRouter's limits page says nothing about logging; the per-provider pages do,
   and some free endpoints train on prompts (REPEATED across [[model-agnostic-agent-harnesses]]
   and [[claude-code-ecosystem-plugins]]; each endpoint's own page is the source).
4. **Re-measure before claiming.** A skill helps *a model*, not models. Nothing routed
   counts as evidence for the talent's grade.
5. **Prefer an Anthropic-compatible endpoint over router software.** Z.ai and Ollama need
   three environment variables and no third-party binary; free-claude-code, OmniRoute and
   claude-code-router are software with their own update cadence and get the four gates.
6. **Never set the base URL globally.** Per run, in the dispatcher's environment, so a
   forgotten variable cannot route a customer build or a talent measurement elsewhere.
7. **Expect features to vanish silently.** Caching under the floor, caching through a
   router that drops `cache_control`, `budget_tokens` on Ollama — none of these error.
   Assert on `usage` and on effort actually applied.

## 5. What this repository can and cannot do today

This box: 4 cores, 15 GB RAM, no GPU — arm D is not runnable here at any useful size
([[best-local-llm-2026-09]] §For this repo). Arm B (Z.ai) is the cheapest real non-Claude
arm and needs only the three variables and a terms read. Arm C is usable for a public
fixture experiment at 50 requests a day. The first hardware that changes the answer is a
24 GB GPU (Qwen3.8-27B, Apache-2.0) for cheap classification arms, and the first that
makes a near-frontier local arm honest is 128 GB (GLM-5.3-Flash, MIT).

## 6. Open

- Z.ai's data-use terms: not yet read (the GLM note says so). Blocks arm B on anything
  private until done.
- An EU-served Claude configuration for the ADR-0010 "region: EU" answer: the pricing and
  platform pages do not decide it; the gateway page names Bedrock, Google Cloud's Agent
  Platform and Microsoft Foundry as billed upstreams, which is where a region is chosen.
- Whether Haiku-tier classification calls in Scio are worth moving to D at all: the
  measured Layer B/C model calls are "a few hundred tokens" and fire rarely
  (`advise_grouping` only when `pkg_feature_general` exists). The saving may be zero.

## 7. A routing brain — the published form, and the shape that fits here (added 2026-09-02)

The idea raised in conversation: *one brain that splits the work and sends each piece to
the right model.* Two published forms, both read at abstract level only today:

- **The cascade** — FrugalGPT (Chen, Zaharia, Zou, 2023): *"LLM cascade which learns which
  combinations of LLMs to use for different queries in order to reduce cost and improve
  accuracy"*; reported *"match the performance of the best individual LLM (e.g. GPT-4) with
  up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost."*
  Cheap model first, a scorer decides whether to accept or escalate. MEASURED as a quote;
  the 98% is on their 2023 benchmarks and their scorer, not transferable.
- **The learned router** — RouteLLM (Ong et al., 2024): a router trained on human preference
  data that picks the model *before* the call; *"significantly reduces costs — by over 2
  times in certain cases — without compromising the quality of responses."* Needs training
  data of the exact task distribution; that is the cost.

Both are already in the landscape as products: claude-code-router's per-request-type rules,
OpenRouter's auto-router, LiteLLM's fallbacks ([[model-agnostic-agent-harnesses]]), and in
miniature Scio's own `matrix.yaml`, which ranks models per job.

**The shape that fits a builder (position, cold, 2026-09-02):** the brain is a *table*, not
a model. Scio's work is already typed by the pipeline — intake classification, rule-based
derivation, codegen, repair, critique, directed change — so the route is a lookup on
(job type × data posture × remaining budget), decided deterministically and logged. The
only place a model must choose is where the job type is unknown, which is intake: one cheap
classification call, then tables. Escalation is a cascade with the pipeline's *own gates*
as the scorer: deterministic edit → local/cheap tier → Sonnet 5 → Opus 5 → Fable 5.1, each
step accepted or rejected by the same typecheck, tests and contract checks
(`build-loop-stops`, `hybrid-parse-escalation` are the same pattern at smaller scale). That
avoids the two costs a model-brain carries: a model call per routing decision, and a
decision nobody can replay. Three constraints stay fixed under any brain: the data posture
filter (§3.2) runs before cost; a routed arm forfeits caching, `count_tokens` and Batch
(§1); and a skill is measured per model, so a route change is a re-measurement, not a
config edit.

## 8. The brain for *building*, not for the app (added 2026-09-02)

The question, sharpened: when *we* build — Claude Code sessions, `/piano` waves, the
curator, evals — can one brain split the work and send each piece to Claude, a cheap tier,
a free endpoint or a local model? Three levels exist, and only the first two are supported.

**Level 1 — inside a session, Claude tiers only (supported, zero new software).** The
routing table already has a place to live: the `model` field of each agent definition
(`sonnet`, `opus`, `haiku`, `fable`, a full id, or `inherit`), resolved per-invocation →
frontmatter → `CLAUDE_CODE_SUBAGENT_MODEL` → the main model (MEASURED, sub-agents page).

**[[subagents]] owns that field and the order it resolves in, and this note depends on both
being right.** The dependency is not decorative: if omitting `model:` meant `inherit` — as that
note said until 2026-09-08, when the held bytes corrected it — then `CLAUDE_CODE_SUBAGENT_MODEL`
could never take effect and the whole level-1 routing table above would be inert. A reader
crossing from here gets the field list, the version-tied caveat that **before v2.1.251 the
environment variable came first** and overrode both the per-invocation parameter and the
frontmatter, and the measured limits on what a subagent can actually do once running; a reader
crossing the other way gets the policy those fields exist to serve.

Background functionality already runs on the `haiku` alias (MEASURED, model-config page),
and `CLAUDE_CODE_EFFORT_LEVEL` sets effort. The coordinator decomposes; the agent files
route. Inventory of this repository on 2026-09-02: two agents, one sets `model: sonnet`
(`rag-pipeline-reviewer`), `skill-builder` sets nothing and therefore inherits the
coordinator's model. Read closer (2026-09-02, correcting an earlier draft of this
paragraph): the agent's own turns are authoring — writing skill fields against the field
contract — and every probe, arm, reader and grader it runs goes through `dispatch.py` on
the tier `pipeline/contracts/chain.contract.json` names ("cheaper there is a different
experiment wearing the same name"). So its `model:` field governs only the authoring
turns, and changing it is a re-measurement of the skills it produces, not a one-line
saving. Not changed.

**Level 2 — outside the session, the dispatcher (supported for Claude tiers).**
`pipeline/build/dispatch.py` already carries `TIERS = {opus, sonnet, haiku}` and runs
`claude -p` per work item with the tier fixed per run; `factory` asks for "a model tier
per stage" and `cost-aware-model-routing` has the task-class → tier table. A non-Claude
arm is the same mechanism with `ANTHROPIC_BASE_URL` and the credential set *for that run's
process only* (rule 6 in §4) — unsupported by Anthropic, but mechanically the same
per-run fixing the harness was built for, and the only place a free or local arm should
ever be wired. This is the brain: a table on job type (harvest grading, intake
summarising, description drafts, eval baseline, authoring, review, architecture) → tier or
arm, read by the dispatcher, logged per run.

**Level 3 — one session, several providers (unsupported, and it changes the bill).** A
Claude Code process has one base URL; no per-subagent base URL is documented. Mixing
providers inside one session therefore needs a router process that receives every call
and forwards by model name (claude-code-router, LiteLLM — [[model-agnostic-agent-harnesses]]).
Two documented facts decide whether that is worth it (MEASURED, gateway page): while a
gateway *credential* is active the claude.ai subscription is not used and every Claude
call is billed per token to the credential; with the base URL alone and no credential,
the saved login stays active and the gateway must forward the OAuth capability header.
So a "send the haiku jobs to a free model" router that carries a credential can cost more
than it saves — every Fable and Opus call in the session moves from the subscription to
list price. Whether a mixing router meets the subscription's terms is not on the page;
read the terms before trying it.

**The number that is missing — corrected twice on 2026-09-02.** First draft: "metrics.jsonl
has zero rows". Second: "it does not exist". Both looked in `pipeline/ledgers/`; the file is
`pipeline/metrics.jsonl`, 29 rows (MEASURED), one per wave or job, with `wall_clock_s`,
`agents` and, on the skill-builder rows, `tokens_est` summed from per-run subagent token
reports (e.g. 2026-08-30: 24 agents, 1,876 s, ~1.64M tokens). Per-run capture also exists:
the harness the other session built on 2026-09-01/02 (`pipeline/build/dispatch.py`,
"the only thing that captures tokens"; `record.py` writes a per-build `events.jsonl`;
`builds.jsonl` rows carry ratios such as "Tokens 1.84x … against a 1.20x cap"). So tokens
per run and per wave are on disk. What no file holds is the aggregation by *job class*
(probe, arm, reader, grader, author) across builds that a routing table would read. That
is a script over existing rows, not new instrumentation — and the lesson of this
paragraph is that a claim about a ledger is checked with `find`, not with one path.

**The script now exists** — `pipeline/queries/job_class_cost.py` (2026-09-02), run over the
five builds (MEASURED): 166 dispatched runs, 495 minutes, 20.9M tokens. By class: arms 74
runs / 50% of minutes / 44% of tokens (Opus, fixed by contract); readers 45 runs / 22% /
23% (15 on Sonnet, 9 on Opus, 21 pre-harness rows without a tier); probes 25 / 13% / 24%;
graders 6 / 7% / 2%. In the one clean build readers were the largest dispatched class (16
runs, 38% of dispatched minutes) and arms the token cost (61%). So the only job class with
volume *and* permission to move is the reader class — and the rethink in
`pipeline/REVIEW-2026-09-02-skill-builder-rethink.md` removes most of it rather than routing
it. Coordinator turns, recorded in two builds: waiting 196 min (almost all build 3's rate
limits), authoring 48, planning 28, reading verdicts 21.

**Position (cold, 2026-09-02):** for our own build the brain is (a) `model:` on every
agent file, set down not up, (b) the dispatcher's table for anything fanned out, (c) no
in-session provider mixing until the ledger shows a job class worth it and the terms are
read. Free arms stay on public fixtures at 50 requests a day; a local arm waits for a
24 GB GPU ([[best-local-llm-2026-09]]).


## 9. Re-read 2026-09-08 — the picker now names the model, and only the label moved

`watch.py` reported four `code.claude.com` pages changed under rows this note cites. Both of
this note's pages changed on **one** theme, and the theme is display, not routing.

| claim | before (read 2026-09-04) | now (2026-09-08) | verdict |
|---|---|---|---|
| discovery's id filter | ids containing `claude`/`anthropic` are kept | unchanged, stated more precisely, and dated: *"Before v2.1.223, Claude Code kept an entry only when its `id` began with `claude` or `anthropic`, which hid provider-prefixed IDs"* | **survives**, and the note's §4 wording stays |
| a discovered entry's name | `display_name`, else the raw `id` | `display_name` when it **differs from the id**; otherwise the model's name if Claude Code *recognises* the id, and the id when it does not | **superseded** |
| a pinned third-party model's row | *"the provider-specific ID appears as-is in the `/model` picker"* | the model's name when the pinned id is recognised, the raw id otherwise | **superseded** |
| `ANTHROPIC_DEFAULT_*_MODEL_NAME` unset | *"Defaults to the model ID when not set"* | shows the model's name if the id is recognised, the id otherwise | **superseded** |

**These four rows settled a cross-note contradiction, 2026-09-12.** [[model-agnostic-agent-harnesses]]
records a vendor screenshot of Claude Code v2.1.126's `/model` picker listing
`open_router/google/gemma-3-4b-it:free` — an id that **cannot pass** the discovery filter in the row
above. The third row resolves it: a **pinned** model's row shows the raw id when Claude Code does not
recognise it, and pinning does not go through discovery at all. The filter governs what is
*discovered*; it says nothing about what is *pinned*. Recorded at both ends because each note alone
held half of it, and the halves read as a conflict for four days.

**What "recognised" means, verbatim:** *"the exact ID of a model Claude Code knows, such as its
Anthropic API ID or your provider's or gateway's form of it, with or without the `[1m]` suffix.
Pin `us.anthropic.claude-sonnet-4-5-20250929-v1:0` and the row reads `Sonnet 4.5`."* And the one
provider where it never fires: *"On Microsoft Foundry, deployment names are user-defined, so
Claude Code never recognizes a pinned ID there, mapped or not."*

**Why it matters to a routed run, which is the only reason it is here.** The picker row is now
*evidence of what Claude Code believes it is talking to*, not just a string the operator typed.
A gateway id like `my-gateway-claude-sonnet-4-6` displaying as `Sonnet 4.6` means the mapping is
recognised; the raw id still showing means it is not, and the capability flags this note's §4
depends on (`..._SUPPORTED_CAPABILITIES`) are the operator's assertion rather than something the
client inferred. So the label is a cheap, free pre-flight check on a routed setup — and one that
reads the *opposite* way on Foundry, where a raw-looking row proves nothing.

**One removal in the same diff, and it cuts toward us:** the `availableModels` allowlist section
dropped *"list the same provider-form ID the picker shows"* in favour of *"list its full
provider-form ID"* — sensible, because with recognition on, the picker may no longer show the id
at all. A note that had cited the picker as the way to discover the string to allowlist would now
be wrong. This one did not, which is luck rather than method, and the method is the re-read.

*Re-read against `knowledge/raw/watch-2026-09-08b/` (both pages stored as received). The
2026-09-04 copies are kept: they are the provenance for the superseded rows above.*


## 10. Re-read 2026-09-11 — what the second doc pass added

§9 is untouched: neither the discovery id filter nor the picker-recognition rules changed (the
diffs have no hunk in those sections). What is new sits beside them.

**A behaviour change nobody in this base had recorded either side of: the token-counting
fallback.** Held bytes said a gateway without `count_tokens` meant Claude Code *"falls back to
counting context usage through the inference endpoint"*, with the remedy *"Expose the endpoint so
token counts don't consume inference requests."* It now says it *"falls back to a **character-based
estimate** of context usage"*, and the remedy became *"Expose the endpoint for exact token
counts."* Three independent signals agree it is a change and not a rewording: the mechanism, the
cost, and the remedy text rewritten to match. **Nothing here was falsified** — no note stated the
fallback in either form — but it changes what a routed arm without `count_tokens` costs (no longer
extra inference requests) *and* what its numbers mean: `/context` is now an estimate. That is the
same chars÷4 substitution [[token-economy-playbook]] already carries a ±15% caveat for, now
happening inside the client.

**Retry-on-rejection, which this base carried nothing about.** A rejected `thinking` field,
mid-conversation system message or `cache_control` marker disables that capability for the rest of
the conversation. A rejected **thinking signature** now behaves differently: Claude Code retries
without the conversation's earlier thinking blocks and keeps them out of later requests, *"New
responses still include thinking"*. For a routed arm that is the difference between "thinking is
off for the session" and "history truncated, thinking continues" — two token profiles. Unchanged:
context-management and tool-schema rejections are **not** retried and reach the developer as 400s.

**The `fable` alias resolves differently behind a gateway** — to Fable 5.1 direct, but to Fable 5
in Claude apps gateway sessions — and *"A gateway that isn't configured to serve
`claude-fable-5-1` rejects requests for that model."* First documented case in this base of an
alias meaning two things depending on the path, and a hard failure rather than a silent
degradation.

**Effort is now enforceable, where it was not.** The held page said `effortLevel` in managed
settings is *"a starting default, not enforcement"*; that sentence is **gone**, replaced by
`maxEffortLevel`, which caps effort on the client *"on any plan and any provider"* and takes the
lower of it and any organisation cap. A subagent's `effort:` frontmatter is no longer the last
word — which is why §4's rule to assert on effort *actually applied* was right.

**Doc-side version instability, recorded as a standing caveat.** The same three facts about Fable
5.1 moved from "requires v2.1.255" to "requires v2.1.257" across three days, and *"Fable 5 requires
v2.1.170 or later"* was deleted outright. No note cited v2.1.255, so nothing is false — but a
version read off this page is not a stable value and must always be quoted with its fetch date.
