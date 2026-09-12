---
title: Agent-builder prior art — three third-party builders, read and compared
sources:
  - url: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
    note: "Anthropic, The Complete Guide to Building Skills for Claude, 33pp. Re-checked against the held PDF 2026-09-12 (readable via pypdf in an isolated virtualenv): the one string this page quotes from it, 'Prove the skill improves results vs. baseline', is present verbatim. FIRST-PARTY; corroborated or refuted PER ITEM in [[anthropic-skill-authoring-contract]] — the word AUTHORITATIVE was retracted 2026-09-12. It was written 2026-08-29 and the pass one day later found its body template followed by 0 of 11 shipped skills, and retracted the same word for its 5,000-word cap. First-party is a fact about the publisher; authoritative is a claim about the contents, and this guide has not earned the second."
    fetched: 2026-08-29
  - url: https://github.com/keysersoose/claude-agent-builder
    note: "MIT. Claude Code primitives; 6-phase workflow; README read via fetch, repo files not cloned."
    fetched: 2026-08-29
  - url: https://github.com/FrancyJGLisboa/agent-skill-creator
    note: "MIT, v6.1.0, 179 commits, 2.3k stars. SME-to-skill pipeline with marketplace governance. README read via fetch; GATES.md NOT read."
    fetched: 2026-08-29
  - url: "local upload: agentbuilder-1.0.0.tar.gz (mcpmarket-version 1.0.0)"
    note: "6 files, extracted and read in full including all Python."
    fetched: 2026-08-29
tags: [agents, skills, prior-art, evidence, measured-vs-repeated]
related: ["[[agent-design-template]]", "[[skill-anatomy]]", "[[subagents]]", "[[llm-idea-generation]]", "[[api-agent-loop]]", "[[effective-agents-anthropic]]", "[[managed-agents-architecture]]", "[[model-agnostic-agent-harnesses]]", "[[production-site-checklist]]", "[[claude-code-ecosystem-plugins]]", "[[third-party-landscape]]", "[[adversarial-plan-review-claudex]]"]
raw:
  - knowledge/raw/pdf-sources-2026-09-11/resources.anthropic.com_hubfs_The-Complete-Guide-to-Building-Skill-for-Claude.pdf
  - "the guide is HELD but only 17.6% EXTRACTABLE here (hex-coded CID text); knowledge/pdftext.py refuses it, so rows read from it cannot be re-verified in this environment - see pipeline/decisions/2026-09-11-stdlib-pdf-text.md"
  - "held 2026-09-11; the rest of this page's sources predate the raw layer (2026-09-02)"
---

# Agent-builder prior art

Three third-party builders read in full on 2026-08-29, against Anthropic's own
guide and against what this library has measured. Recorded because the reuse-first
gate is only satisfiable if you can say what you looked at.

**The single most useful finding: they solve three different problems that share
one name.** Anyone reaching for "an agent builder" should first say which.

| | Builds | Artefact |
|---|---|---|
| `agentbuilder 1.0.0` (upload) | **API-level agents** | Python: a `messages.create` loop, tool defs, a scaffold script |
| `keysersoose/claude-agent-builder` | **Claude Code primitives** | agents, skills, hooks, commands, MCP configs |
| `FrancyJGLisboa/agent-skill-creator` | **skills, plus their lifecycle** | packaged skills + a governed marketplace |
| ours (`hello-world`) | **Claude Code subagents** | agent + ≤3 procedures + a wall + delegated evals |

A name collision is not academic: skill precedence is enterprise > personal >
project, so installing a same-named builder at personal scope **silently shadows a
project one**. Rename on install, or package as a plugin to get namespacing.

**The row you are in decides which page to read next.** For the API-level row,
[[api-agent-loop]] holds the loop those scaffolds generate, and the *model* is a parameter
there — which is the axis [[model-agnostic-agent-harnesses]] owns, along with Anthropic's
statement that the Claude Code equivalent (pointing the harness at a non-Claude model) is
unsupported. That asymmetry is the sharpest reason the three tools are not substitutes: an
API-level builder is portable by construction, a Claude Code builder is not. For the
primitives and skills rows, [[skill-anatomy]] is the contract whatever they emit has to
satisfy — the fields, the directory, what loads when — so it is also the cheapest way to
grade a generator: run it, then check its output against that page.

## What none of them has

**Not one cites a study, a benchmark, a measurement or a source.** Every claim in
all three is assertion. That is not a slur — it is the state of the field, and it
is what this library looked like before it started measuring. It is also why
several of their claims run directly against findings recorded in
[[llm-idea-generation]] and [[agent-design-template]].

The sharpest example, from the upload's SKILL.md: *"Trust the model. Don't
over-engineer. Don't pre-specify workflows."* Measured against that: a structured
second pass beat free generation (similarity 0.43 → 0.28), and letting the model
choose among its own outputs agrees with experts **22–40%** of the time where
expert-to-expert agreement is 60%. "Trust the model" is exactly wrong for
selection and unmeasured for generation.

**None of them tests against a baseline.** `keysersoose` ships `validate_agents.py`
(a linter) and a self-check phase; `agent-skill-creator` advertises evals and
security gates but its README specifies no methodology and `GATES.md` was not read.
Anthropic's own guide, by contrast, names baseline comparison explicitly:
*"Prove the skill improves results vs. baseline"* — while conceding *"there will
be an element of vibes-based assessment."*

**None separates the author from the tester.** In this library that separation
found **81 defects**, and an independent tester failed our own builder twice
before it was fit to use.

## What each one has that is worth taking

**`agent-skill-creator` — governance, and it is a real gap in ours.** Versioning,
rollback, **quarantine**, approval gates, and an explicit split between the subject
expert who owns business meaning and the operator who owns distribution policy.
That is separation of duties applied to *authority*, which is the same mechanism as
author-is-not-tester applied to *verification*. We have the second and not the
first: nothing in our design says who may approve an agent, how a bad one is
withdrawn, or what version anyone is running.

**`keysersoose` — the primitives decision tree**, i.e. given a need, which of the
seven Claude Code primitives it maps to. Our `agent-shape` decides how many agents
and what each may do; it does not ask whether the answer is an agent at all rather
than a hook, a command or an MCP server. A missing branch.

**The upload — API-level scaffolding**, a domain ours does not touch at all. If we
ever build agents against the SDK rather than the harness, `subagent-pattern.py`
and `tool-templates.py` are a starting point. Two cautions: every generated tool
runs `subprocess.run(command, shell=True)` with a 60-second timeout and no gate —
its own `safe_path()` guards file paths and the shell tool walks past it — and the
default model string is pinned to a 2025 Sonnet.

## Where they and our measurements agree

Worth noting, because agreement across independent sources is weak evidence but
not none:

- **Load knowledge on demand, not upfront.** All four say it. Anthropic's guide
  makes it the core design principle; the upload states it as *"Make knowledge
  available, not mandatory."* This is the tier model in [[agent-design-template]].
- **Start with a handful of capabilities.** The upload says 3–5 tools; SkillsBench
  measured 1–3 *modules* at +19.0pp against +10.1pp for 4 or more. Different unit,
  same direction.
- **Isolate noisy subtasks.** All name context isolation as the reason for
  subagents, which matches the measured finding that isolation *is* the mechanism.

## ECC — 68 agents, swept mechanically

`affaan-m/ECC/agents` (cloned locally). The largest agent library available to
compare against, and the sweep is more informative than any of the READMEs.

| | Result |
|---|---|
| Agents | 68, **all load** (line-anchored frontmatter) |
| Frontmatter keys used | `name`, `description`, `model`, `tools` (68/68); `color` (5) |
| **`tools:` set explicitly** | **68 / 68. Zero omit it** |
| **`skills:` used** | **0 / 68** |
| **`hooks:` used** | **0 / 68** |
| Descriptions over the 1024 spec | 0 |
| All descriptions combined | 14,110 chars ≈ **3,527 tokens — 23% of the 15,000 shared budget** |
| Body length | median **742 words**; longest 2,103; none over 5,000 |

**68/68 explicit `tools:` is external corroboration that the rule is right and
achievable at scale.** That default — omitting it inherits everything — is the one
this library calls the most dangerous line you can fail to write, and a
68-agent library gets it right every time.

**0/68 using `skills:`, against 0/34 in Anthropic's own agents, is the
uncomfortable number.** Nobody in either library preloads skills into an agent.
Our design does, and our own ablation found no advantage from the three we
preloaded.

**Do not over-read it.** An earlier draft of this note offered two readings — that
we found something both libraries missed, or that both tried it and dropped it —
and that was a false choice. At least four explanations fit the same number, and
only one of them is evidence against the field:

1. **Nobody considered it.** The likeliest, and the one that carries no
   information at all about whether it works.
2. **The field postdates the libraries.** If `skills:` did not exist when those
   agents were written, 0 of 68 says precisely nothing. **Unchecked** — worth five
   minutes against the changelog before anyone cites this row again.
3. Their agents are single-procedure, so there is nothing to preload. Median body
   742 words supports this.
4. They tried it and it did not help.

**Absence of use is not absence of value; it is absence of evidence.** The row
belongs in the "things to test" column and nowhere else. Our own ablation is the
one real datum here, and its confounds are stated where it lives.

**0/68 using `hooks:` is where we are ahead — and their own file shows why it
matters.** `agent-evaluator` grants `Bash` and then constrains it *in prose*: an
allowlist (`grep`, `cat`, `ls`, `find`, `head`, `tail`, `wc`), a denylist (`rm`,
`git push`, `curl … | sh`), and a genuinely sharp hardening note — always pass
`--no-pager`, prefer `-c core.pager=cat`, because a repo-local `.git/config` can
turn a pager into code execution. **They identified a real attack and chose a
mechanism that cannot enforce it.** A `PreToolUse` hook would; a paragraph asks.
This is the clearest specimen in the whole survey of the gap between naming a
risk and closing it.

**Median body 742 words** is roughly half of what this repo's architect skills
carried before their evidence moved to reference files.

Two design choices worth stealing, both from `agent-evaluator`: *"DO NOT
re-perform the original task"* — the evaluator is fenced off from becoming the
doer — and *"every score below 5 MUST cite specific evidence."* Its step 2 also
names the check that caught our own ablation: **verify that files the agent claims
to have created actually exist.**

One to leave: it ends with *"Self-check: Would the user agree with this
assessment?"* — self-evaluation, which is measured weak (22–40% agreement with
experts where expert-to-expert is 60%).

## The practitioner genre, and how to read it

Two practitioner pieces were submitted alongside the builders. One was readable
and is worth recording as a **specimen**, not as a source.

**dev.to, "I built 5 AI agents with Claude's new builder tool"** (author profile
created March 2026; no affiliation disclosed). It states results as measurements
and sources none of them: *"After one month, it resolved 73% of tickets
automatically"*, *"accurate enough for 90% of developer questions"*, *"Pro
accounts get 100 agent conversations per day"*. No screenshots, no logs, no
method, no code. It never names an actual Anthropic feature — "Claude's agent
builder" is used throughout without a product it maps to — and its pricing and
quota claims do not match Anthropic's own documentation. The author has published
a series of similarly-shaped comparison pieces about competing products.

That is the same failure mode already recorded in [[ideation-and-idea-selection]],
where an article attributed to Diehl & Stroebe a finding absent from their paper
and reversed Mullen's conclusion. **A percentage with no method behind it is
decoration.** The rule that follows: a practitioner post is evidence that someone
*tried* something, and nothing more. Read them for failure reports and surprises —
what broke is harder to fabricate than what worked — and never carry a number out
of one.

**Two could not be read at all.** A Medium post on agent coordination returned
HTTP 403, and a Reddit thread is not fetchable from this environment. Neither is
summarised here, because neither was read.

## addyosmani/agent-skills — the largest general-purpose skill library seen so far (added 2026-09-02)

Source: `https://github.com/addyosmani/agent-skills` fetched 2026-09-02; author profile
`https://github.com/addyosmani` fetched the same day; a 50-second video whose claims are
graded. MEASURED unless marked.

- "Production-grade engineering skills for AI coding agents." MIT. **91.6k stars.**
- **25 skills** (using-agent-skills, interview-me, idea-refine, spec-driven-development,
  constraint-driven-development, planning-and-task-breakdown, incremental-implementation,
  test-driven-development, context-engineering, source-driven-development,
  doubt-driven-development, frontend-ui-engineering, api-and-interface-design,
  browser-testing-with-devtools, debugging-and-error-recovery, code-review-and-quality,
  code-simplification, security-and-hardening, performance-optimization,
  git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration,
  documentation-and-adrs, observability-and-instrumentation, shipping-and-launch)
  **+ 4 personas + 8 slash commands**, in three composable layers.
- Install: `npx skills add addyosmani/agent-skills [--skill <name>]`. Targets Claude Code,
  Cursor, Codex, Copilot, Cline, Gemini CLI, Windsurf, OpenCode, Kiro and others.
- Author: profile bio reads "Former Director at Google working on Gemini and Google
  Cloud" — the video's "former director at Google who worked on Gemini" is accurate.
- Video claim "gives your AI the same coding workflows senior developers use at Google":
  marketing; the repo says "workflows... senior engineers use", not Google's. Not checkable.

**What it means for us.** Reuse-first: at least nine of its 25 names collide with talents we
already carry (test-driven-development, code-review, debugging, security, performance,
documentation/ADRs, planning, context engineering, shipping). Before any of ours is
rebuilt on the same topic, `skill-scout` reads the corresponding SKILL.md there. It is the
obvious next harvest source for `/piano`, with the four gates applied per skill: the
install is an `npx` fetch and the security gate reads the code first. Its
`shipping-and-launch` is the engineering-side twin of [[production-site-checklist]].

## skills.sh and `find-skills` — Vercel's registry, and the skill that searches it (added 2026-09-02)

Sources: `https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md` and
`https://www.skills.sh/` fetched 2026-09-02; a 41-second video whose claims are graded.

- **skills.sh** is "The Open Agent Skills Ecosystem", run by Vercel (`vercel-labs/skills`),
  installed with `npx skills add <owner/repo>`. Leaderboard shows **1.29M+ total installs**;
  ranked by installs (all-time, 24h, hot); an "Official" section and a security-audits
  page. No package count on the page (MEASURED). The video's "700,000 skills" and its
  frames showing 641,678 and 703,412 are the creator's graphics — UNVERIFIED; the page
  itself gives no number.
- **`find-skills`** (MEASURED from SKILL.md): triggers on "how do I do X" / "find a skill
  for X"; runs `npx skills find [query]`, `npx skills add <package>`, `npx skills update`;
  installs globally with `-g`. Its vetting is three heuristics: prefer 1K+ installs and be
  cautious under 100; prefer official sources (vercel-labs, anthropics, microsoft); be
  sceptical of repos under 100 stars.
- Video claims graded: "an engineer from the Vercel team" — the repo is the vercel-labs
  org; fine. "Filters out anything sketchy and only surfaces genuinely trusted skills" —
  OVERSTATED: the filter is installs + stars + a whitelist of orgs, which is the "star
  count and a guess" the video says it replaces, made explicit. "One command, handles
  everything" — accurate for install; nothing is vetted beyond the three numbers.

**For us.** skills.sh is the largest external supply of the thing this repo manufactures,
and `find-skills` is a two-line `skill-scout`. Our four gates are strictly stronger than
its three heuristics (we read the code; it reads the install count), so the right use is
as a *source*: `research-scout` queues skills.sh categories, `skill-scout` reads the
candidate's SKILL.md, the gates decide. Reuse-first now has a bigger haystack — good for
reuse, more work for the dedup gate.

## Four more libraries, one evolution engine (added 2026-09-02, evening batch)

All MEASURED from the README fetched 2026-09-02 unless marked; video claims graded inline.

- **mattpocock/skills** — "Skills for Real Engineers. Straight from my .agents directory."
  MIT, **245.1k stars**, 23 skills (13 engineering, 10 productivity: caveman, grill-me,
  handoff, write-a-skill, …), `npx skills@latest add mattpocock/skills`; skills.sh shows
  1.0M total installs across its 34 listed entries. The video's "an OG at Vercel" — the README
  says nothing of Vercel; Matt Pocock is known for Total TypeScript and now sells a "Claude
  Code for Real Engineers" cohort (visible in the frames). UNVERIFIED and probably wrong
  attribution. "caveman cuts token usage ~75%" is the skill's own one-line claim, no
  measurement. Reuse-first collisions with ours: grill-me ≈ `brainstorming`/`clarifying-
  questions`, handoff ≈ `unified-memory`, write-a-skill ≈ `writing-skills`.
- **google/skills** — "Agent Skills for Google products and technologies, including Google
  Cloud." Apache-2.0, **19.3k stars**, ~150 skills (Cloud, AI/ML, databases, security,
  Advertising incl. "Google Ads API MCP Server Installation", two Google Analytics API
  skills, Android, Flutter), "under active development"; `npx skills add google/skills` or
  `claude plugin marketplace add google/skills`. Video's "over 100 skills, 18,000 stars" —
  consistent. Nature: vendor documentation as skills — useful when building *on* Google;
  none is a method. Relevant to Scio's stack decision only as evidence that vendors now ship
  their docs in SKILL.md form.
- **shanraisshan/claude-code-best-practice** — "from vibe coding to agentic engineering —
  practice makes claude perfect". 63k stars in the frame (updated 2026-07-21), GitHub Trending
  #1 in March 2026 (REPEATED), 69 tips in 11 categories with input from Boris Cherny. What
  the frames show that the search does not: a **workflow table** (Superpowers at 258k stars,
  RPI, Ralph Wiggum Loop, Karpathy's, Steinberger's, Cherny's and Thariq's workflows) and a
  **multi-model section** (Claude Code together with Gemini, Kimi, DeepSeek, local models via
  another model's CLI as a tool). The video's three points ("ready-made instructions,
  shortcuts that chain steps, a daily-updated list of what top builders do") are accurate
  and generic. A curation, not a method — the same genre as `awesome-claude-code-toolkit`
  harvested in wave 3, with a stronger workflow taxonomy worth one `research-scout` pass.
- **HKUDS/OpenSpace** — "The Skill Management Layer for AI Agents". MIT, 7.5k stars.
  Three evolution modes: **FIX** (repair a broken or outdated skill), **DERIVED** (a
  specialised version from an existing one), **CAPTURED** (save a reusable sub-workflow only
  when the trace shows both its execution *and* a separate validation of the claimed
  postcondition). README benchmark: Terminal-Bench 2.1 **65.2% cold → 78.7% warm** on the same
  backbone. The "46% fewer tokens" and "$11K earned in 6 hours" badges are in the frames and
  in secondary write-ups (GDPVal-style set, 220 tasks / 44 jobs, Qwen 3.5+, quality 40.8 →
  70.8) but were NOT in the README content fetched — REPEATED. Cloud (open-space.cloud) is
  opt-in via explicit key provisioning; local works without it. Hosts: Claude Code, Codex,
  OpenClaw, nanobot, MCP hosts.

**OpenSpace is the one to read closely.** It is this repository's `library-curator` loop
with a trace-driven trigger instead of a schedule, and its CAPTURED rule — *a workflow becomes
a skill only when the trace contains both the execution and an independent validation of the
outcome* — is a sharper admission gate than our talent-worthiness gate, which asks whether a
function is lacking, not whether it was seen to work. The warm-vs-cold Terminal-Bench number
is the kind of measurement our skill-builder produces per skill; theirs is per library. Two
things to check before any of it is copied: whether "warm" was scored by the same model that
wrote the skills (see [[harness-over-model-prime-agent]] on self-grading), and what FIX does
to a skill that is failing because the *test* is wrong — our triage step, which their loop
does not appear to have.

## Verification note

The Anthropic guide was extracted from PDF and read page by page. The upload was
extracted and read in full, code included. The two GitHub repositories were read
**via their READMEs only** — not cloned, and `GATES.md`, `agent-patterns.md` and
`primitives-guide.md` were not read. Claims about their internals are therefore
what their authors say about themselves, not what was verified. Anyone acting on
the governance model in `agent-skill-creator` should read `GATES.md` first.
