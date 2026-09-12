# Tooling scan — what to adopt, and where it attaches

**Scanned 2026-08-26.** Every claim below was checked at its own source on that date — the
official documentation at `code.claude.com/docs`, the GitHub API for stars, last push, licence
and archived status, PyPI for package versions, and the official MCP registry. Nothing here is
answered from memory. Where a source could not be reached or a claim could not be confirmed, it
says so.

The organising question is not "is this good" but **"which stage of `PIPELINE.md` or which layer
of `docs/next/` does it attach to."** A candidate with no attachment point is inventory, and
gets a `skip` — most of them do.

---

## What I scanned, and what I found dead or recycled

**The method, as instructed.** Ten links were supplied and treated as two tiers. The six primary
sources were read properly. The four listicles were read **only as pointers**: every repository
and tool name they list was extracted and then verified at its own GitHub repository or official
documentation — stars, last commit, licence, archived flag, and whether the thing does what the
article claims. Two claims failed that check outright and are recorded below. After the ten, I
searched the official marketplaces and the MCP registry directly.

**Nothing was dead.** All ten URLs resolved. One, KDnuggets, returned `403 Forbidden` to the
fetch tool and was retrieved with a normal browser user-agent instead; its content is real and is
used. Nothing was paywalled — the Substack article is fully readable.

**The four listicles are not one recycled list, but their top is.** Across the four, `obra/superpowers`
appears in three, `hesreallyhim/awesome-claude-code` in three, `affaan-m/ECC` in three (twice under
a repo slug that does not exist), and `anthropics/skills` in two; below that they diverge into
four largely disjoint tails, several of them self-promotional. That is one sentence's worth of
finding and no more.

**Two verifiable errors in the secondary tier.** ayautomate names `affaan-m/everything-claude-code`;
that repository does not exist — the real one is `affaan-m/ECC`, and the same article states
superpowers has "94,000+ GitHub stars" when the repository reports **277,967**. KDnuggets
recommends `gsd-build/get-shit-done`, which GitHub reports as **archived**. ayautomate's own
`walidboulanouar/Ay-Skills` is placed first in its list and has **86 stars**. The listicles were
useful as a name-harvest and useless as evidence, which is exactly the tier they were assigned.

**Volume is confirmed, and confirms nothing.** The official marketplace
`anthropics/claude-plugins-official` carries **289 plugins**; the community marketplace
`anthropics/claude-plugins-community` carries **2,282**. `docs/next/SKILLS.md` already made the
call — volume is not the gap.

---

## 1 · The candidates

| Name | What it is | Where it attaches | Verdict | Why |
|---|---|---|---|---|
| **Plugin + marketplace mechanism** | Claude Code's own distribution format: one repo publishes `.claude-plugin/marketplace.json`, another consumes it via settings | Stage 0, then every stage — it is how the build repo reads `scio` | **adopt now** | Answers the open question in `OPERATING-MODEL.md` §1 outright. See §3 |
| **`skill-creator`** (official plugin, Anthropic) | Writes skills; runs per-skill evals in isolated subagents; benchmarks with/without; A/B two versions; tunes descriptions | Stage 0 — it is the `eval` leg of the four-part contract | **adopt now** | The only verified mechanism that actually runs an eval. See §3 |
| **`plugin-dev`** (official plugin, Anthropic) | 7 skills + `plugin-validator`, `skill-reviewer`, `agent-creator` subagents for building plugins | Stage 0 only, while `scio` is being turned into a marketplace | **adopt now, then remove** | Scaffolding. Keeping it after the marketplace exists is a context tax |
| **`obra/superpowers` → `writing-skills`** | MIT, v6.3.0, 277,967★, pushed 2026-08-19. 14 skills. `writing-skills` is 679 lines of TDD-for-skills | Stage 0 | **adopt the method, not the plugin** | Its central rule is better than ours. See §4 |
| **`/doctor`** (bundled skill) | Setup checkup: flags unused skills, MCP servers and plugins *against their context cost*, and flags slow hooks | Stage 0, recurring | **adopt now** | Free, already installed, and it measures the exact thing our token-economy sections care about |
| **graphify `--mcp`** | The installed `graphifyy` package can serve the graph as an MCP stdio server | Stage 1 and Stage 5 retrieval; Layer B | **adopt later** | Right answer *if* the graph turns out to be the main thing the build repo reads. Decide after Stage 3 |
| **`github` / `github/github-mcp-server`** | MIT, 32,524★, GitHub's official MCP server; also packaged as the `github` plugin | Stage 7 (review), Stage 5 (PRs) | **later** | Earns it when the build repo has PRs. Nothing to read today |
| **`code-review`, `pr-review-toolkit`** (official) | Multi-agent PR review with confidence scoring; six specialised reviewer agents | Stage 6 / Stage 7 | **later** | Overlaps `testing` on evidence, not on review. Revisit when code exists |
| **`claude-md-management`** (official) | Audits `CLAUDE.md`, captures session learnings, keeps project memory current | Cross-cutting | **later** | Small and real, but `CLAUDE.md` here is 3.3 KB and healthy. No problem to solve yet |
| **`security-guidance` / `claude-security`** (official) | Pattern warnings on edit, LLM diff review on `Stop`, agentic commit reviewer | Layer G | **later** | Layer G already holds the tenancy and auth work. Adopt when there is code to scan |
| **`frontend-design`** (official) | Frontend/UI implementation quality | Layer F / `app-design` | **skip for now** | Overlaps `app-design` §1–§4, which is sourced and token-contracted. Ours is more specific |
| **`context7`** (official, Upstash) | Hosted MCP for up-to-date library documentation | Stage 5 | **later** | Useful only once the stack is chosen. Stage 3's output decides |
| **`hookify`** (official) | Generates hooks from markdown rule files instead of `hooks.json` | Stage 0 | **skip** | Our hook need is one narrow, deliberate rule (§2). A rule generator is the wrong shape for it |
| **`affaan-m/ECC`** | MIT, 243,420★, pushed 2026-08-25. "Agent harness performance optimization system" — skills, instincts, memory, security | — | **skip** | A whole competing harness. Adopting it means adopting its opinions wholesale, which is the opposite of the ADR discipline |
| **`garrytan/gstack`** | MIT. **Not** 23 persona tools — a substantial TypeScript codebase with **554 test files** | Layer D, Layer A | **skip as a dependency; mine it** | The verdict holds (competing harness); **the stated reason was false** — it described the README, not the repo. Its `test/catalog-budget.test.ts` already solves Layer D's catalog-loaded-whole problem. See `docs/mined/OTHERS-MINED.md` §1 · *corrected 2026-08-26* |
| **`gsd-build/get-shit-done`** | 64,637★, **archived** | — | **skip** | Archived, and it is a competing pipeline to `PIPELINE.md` |
| **`yamadashy/repomix`** | MIT, 28,069★. Packs an entire repository into one AI-friendly file | — | **skip, instructively** | It is packing. `docs/next/` names retrieval-versus-packing as a cross-cutting axis. This is the anti-pattern with a CLI |
| **`zilliztech/claude-context`** | MIT, 12,445★, pushed 2026-07-14. Semantic code search MCP over a vector DB | Stage 5 retrieval | **skip** | Duplicates what graphify already gives us, and adds a vector database. Revisit only if graphify's retrieval measurably fails |
| **`eyaltoledano/claude-task-master`** | 28,022★. AI task management dropped into an editor. **Licence is MIT + Commons Clause** — verified in its `LICENSE`, which is why the API reports `NOASSERTION` | Stage 4, Layer C | **skip** | Wrong granularity, and now also a licence question: **Commons Clause withholds the right to sell.** That is material for a commercial builder and disqualifies vendoring any of it · *corrected 2026-08-26* |
| **`supermemoryai/supermemory`** (29,080★) · **`steipete/claude-code-mcp`** (1,315★, **archived**) | Hosted memory engine; Claude-Code-as-an-MCP-server | — | **skip** | Our memory is a git repo with ADRs; the second is archived |
| **`multica-ai/andrej-karpathy-skills`** | 207,611★ for a single skill. **No `LICENSE` file at all**, and not authored by the person named | — | **skip** | Star count is not evidence. One opinionated file, no source, no limits, no eval — and nothing granting the right to use it · *corrected 2026-08-26* |
| **awesome-lists** (`hesreallyhim`, `ComposioHQ`, `travisvn`, `rohitg00`, `VoltAgent`) | Curated directories, 2.5k–73k★ | — | **skip as adoptions; keep one as a search index** | Unfiltered directories. `hesreallyhim/awesome-claude-code` (pushed today) is the one worth searching when a specific need appears |
| **`Piebald-AI/claude-code-system-prompts`** | MIT, 12,462★, pushed 2026-08-26. Claude Code's system prompt and 27 tool descriptions, per version | — | **skip as a tool, bookmark as evidence** | Not something to install. It is the only place to check harness behaviour we would otherwise assume |
| **`EvanLi/Github-Ranking`** | MIT, 11,997★, auto-updated daily | — | **skip** | A generic stars-and-forks leaderboard for all of GitHub. Contains nothing Claude-specific. Its only use here is as a reminder that stars rank popularity, not fitness |
| **MCP registry: knowledge/memory servers** | `ai.brainattic/knowledge-base`, `ai.justonce/memory`, `co.dijin/memory`, `com.aiakiv/memory` and ~dozens more | — | **skip** | All hosted third-party services. Every one puts our knowledge base on someone else's server to solve a problem a local file already solves |

### The five that actually matter

**The plugin mechanism is the finding.** `OPERATING-MODEL.md` §1 lists four ways the build repo
could read `scio` and calls it "a decision, not a preference". The documentation settles it, and
§3 below gives the exact configuration. This is not a candidate to evaluate — it is the mechanism
that makes every other candidate installable, and it carries the version pin the drift hazard
demands.

**`skill-creator` is the only verified eval runner.** `docs/next/SKILLS.md` requires four things
of every research skill, and the fourth — *runnable cases with expected outcomes* — has had no
mechanism behind it. It does now, and it is more than the note assumed: test cases in
`evals/evals.json`, one **isolated subagent per case** so context from authoring cannot leak in,
grading with evidence into `grading.json`, aggregation into `benchmark.json` with pass rate,
tokens and time as **mean ± stddev** for with-skill versus without-skill, blind A/B between two
versions of a skill, and a description tuner that generates should-trigger and should-not-trigger
prompts and measures the hit rate. That last part is aimed directly at a defect we already have:
`graphify`'s description says only what it does, never when to use it, so it will not fire.

**`superpowers/writing-skills` beats our plan on one point.** Its core rule is *"If you didn't
watch an agent fail without the skill, you don't know if the skill teaches the right thing"* —
baseline-first, RED before GREEN. `OPERATING-MODEL.md` §2.2 proposes a `skill-writer` that refuses
to emit a skill when the Limits section is empty. Both refusals are right and they are different
refusals. Take both. Do **not** install the superpowers plugin: it ships 14 skills, of which
`brainstorming`, `test-driven-development` and `writing-plans` collide head-on with `brainstorm`,
`testing` and Stage 4, and installing it to get one skill imports three conflicts.

**graphify is already the MCP answer, if we need one.** `OPERATING-MODEL.md` §1 asks whether an
MCP server in front of the graph is the right mechanism. It does not need to be built —
`/graphify <path> --mcp` starts an MCP stdio server over the existing graph. That collapses the
question to a cheap one: point the build repo at it and measure. Do it after Stage 3, because
until the stack is chosen we do not know what the build sessions will actually query.

**The registries confirmed the parked idea in `SKILLS.md`.** 289 official plugins, 2,282
community plugins, and an MCP registry whose "knowledge" and "memory" categories are wall-to-wall
hosted vendors — several listed two and three times over. Not one of them carries a source, a
limits section, or a published eval. `SKILLS.md` called provenance and evals the gap; the scan
did not find a counterexample.

---

## 2 · Automation — the mechanics, and one proposal

The ask is specific: **on every commit, refresh the code graph, update the documentation
intelligently, and commit the result.** `CLAUDE.md` already mandates the checkpoint protocol and
notes that a hook or CI check *could* enforce it. So the first job is to establish what a hook
actually is, from the reference rather than from memory.

### 2.1 The hook surface, in full

Claude Code fires hooks on **Claude's actions**, in-session. There are 25 events. All matching
hooks for an event run in parallel; hooks from every settings file merge rather than replace.

| Event | Fires when | Matcher on | Can block? |
|---|---|---|---|
| `SessionStart` | session begins or resumes | `startup·resume·clear·compact·fork` | no |
| `Setup` | `--init-only`, or `--init`/`--maintenance` in `-p` | `init·maintenance` | no |
| `SessionEnd` | session terminates | `clear·resume·logout·prompt_input_exit·other` | no |
| `UserPromptSubmit` | prompt submitted, before Claude sees it | — | **yes** |
| `UserPromptExpansion` | a typed command expands into a prompt | command name | **yes** |
| `Stop` | Claude finishes responding | — | **yes** |
| `StopFailure` | turn ends on an API error | error type | no |
| `PreToolUse` | before a tool call | tool name | **yes** |
| `PermissionRequest` | a call needs a permission decision | tool name | via JSON only |
| `PermissionDenied` | auto mode denies a call | tool name | no (can offer `retry`) |
| `PostToolUse` | **after** a tool call succeeds | tool name | **no — it already ran** |
| `PostToolUseFailure` | after a tool call fails | tool name | no |
| `PostToolBatch` | after a parallel batch resolves | — | **yes** |
| `SubagentStart` / `SubagentStop` | subagent spawned / finished | agent type | start no, stop **yes** |
| `TaskCreated` / `TaskCompleted` | task created / marked done | — | **yes** |
| `TeammateIdle` | an agent-team teammate is about to idle | — | **yes** |
| `FileChanged` | a watched file changes on disk | **literal filenames**, not regex | no |
| `CwdChanged` | working directory changes | — | no |
| `DirectoryAdded` | `/add-dir` or `register_repo_root` | `slash_command·register_repo_root` | no |
| `ConfigChange` | a settings file changes mid-session | config source | yes (not `policy_settings`) |
| `InstructionsLoaded` | a `CLAUDE.md` or `.claude/rules/*.md` loads | load reason | no |
| `WorktreeCreate` / `WorktreeRemove` | worktree created / removed | — | create: **any** non-zero exit aborts |
| `PreCompact` / `PostCompact` | around context compaction | `manual·auto` | pre yes, post no |
| `Elicitation` / `ElicitationResult` | MCP server asks the user for input | server name | **yes** |
| `Notification` / `MessageDisplay` | a notification / streaming assistant text | type / — | no |

Every hook receives JSON on stdin carrying at least `session_id`, `transcript_path`, `cwd` and
`hook_event_name`, plus event-specific fields (`tool_name`, `tool_input`, `tool_output`,
`last_assistant_message`, and so on). Five handler types exist: `command`, `http`, `mcp_tool`,
and the experimental `prompt` and `agent` types — **the last two call a model**, at 30 s and 60 s
default timeouts respectively.

**The limits that decide the design.** Exit 0 succeeds; **exit 2 blocks** on the events that
support it and sends stderr as the reason; other codes are non-blocking errors. Default timeout
is 600 s for `command`/`http`/`mcp_tool` (30 s for `UserPromptSubmit`, 10 s for `MessageDisplay`,
and all `SessionEnd` hooks share a 1.5 s budget). A timed-out hook does **not** block. Tool events
accept an `if` field in permission-rule syntax — `Bash(git commit *)`, `Edit(*.ts)`. Hooks in
project `.claude/settings.json` require **workspace trust**, and `disableAllHooks: true` switches
off every user/project/local hook at once. Command hooks run without a controlling terminal, so
they cannot prompt.

### 2.2 There is no "after a commit" event, and that is the whole point

**No Claude Code hook fires on a git commit.** The nearest thing is `PostToolUse` with
`matcher: "Bash"` and `if: "Bash(git commit *)"` — which fires only when *Claude* runs the commit,
in a Claude Code session, and only after the commit already exists. It cannot block, because the
commit has happened. A commit you make yourself in another terminal fires nothing at all.

A **git `post-commit` hook** is a different mechanism with a different guarantee: it fires on
every commit in that clone regardless of who made it, has no access to the session, cannot block
either (it runs after the commit object exists), and has no model unless it pays to start one.
`graph-guard` already says this in its own words and already reaches for `graphify hook install`,
which appends to any existing `post-commit` hook.

So the split is not a preference:

- **Deterministic, must fire on every commit including human ones → git `post-commit`.**
- **Anything needing the session, the transcript, or Claude's judgement → a Claude Code hook,
  and only `PostToolUse`/`Stop` are in the right place in the loop.**
- **Anything that must actually block bad work → CI on push, or `pre-push`. Never `pre-commit`.**

### 2.3 One proposal for the auto-documentation loop

**Mechanism: two hooks, neither of which calls a model.**

**(a) The graph, in git `post-commit`.** Exactly what `graph-guard` already specifies: cheap exit
first (`git diff --name-only HEAD~1 HEAD | grep -E '\.(py|ts|tsx|sql)$' || exit 0` — most commits
stop here), incremental tree-sitter re-extraction of only the changed files, a diff against the
previous graph, the layer-boundary check, one appended line in `docs/graph-log.md`. **Cost: zero
tokens, zero dollars, sub-second on the common path.** It never commits `graph.json` — 5.5 MB of
derived data per commit is half a gigabyte of history for something rebuildable in seconds.
Install `graphifyy[sql]`, pinned, or the twelve migrations are silently invisible to the graph.

**(b) The documentation, as a `Stop` gate — not a generator.** A `PostToolUse` handler scoped
with `if: "Bash(git commit *)"` writes a sentinel recording the commit sha and the paths it
touched. A `Stop` handler reads the sentinel and asks one deterministic question: *did this
session commit a change to `docs/`, `.claude/skills/` or `docs/decisions/` without appending to
`docs/CHANGELOG.md`?* If yes, exit 2 with the missing item named. Exit 2 on `Stop` prevents Claude
from stopping and continues the turn — so the documentation is written **by the session that is
already open, with the context already loaded**, and the follow-up commit is part of the same turn.
Both handlers are shell scripts reading `git show --name-only`. **Cost per commit: zero tokens
when the check passes; when it fires, the tokens the session was going to spend anyway.**

**What it must never do.**

- **Never call a model in the hook.** The `prompt` and `agent` handler types exist and are exactly
  the wrong tool here. A hook that spends money on every commit is a tax, and a tax gets removed —
  `disableAllHooks: true` is one line, and the person who writes it will not tell anyone.
- **Never regenerate a document per commit.** `graph-guard` already argues this: a file that
  changes constantly is never read. Append-only log, or nothing.
- **Never block `pre-commit`.** Blocking every commit on a graph rebuild is the canonical way a
  guard gets uninstalled.
- **Never let the `Stop` gate loop.** Exit 2 prevents stopping; if the condition cannot be
  satisfied the session cannot end. The sentinel must be cleared on the first re-fire and the gate
  must fire **at most once per commit**, with an escape hatch (`SCIO_SKIP_DOC_GATE=1`) that is
  visible in the terminal when used.
- **Never make it the only enforcement.** A `Stop` hook is trivially bypassed by committing from
  another terminal. The authoritative check is CI on push, where a missing CHANGELOG entry fails
  the build. The hook exists to make the CI failure rare, not to replace it.

**The named failure mode.** The version of this that dies within a week is the tempting one: a
`Stop` or `post-commit` hook that runs `claude -p "update the docs for this commit"`. It costs a
model call on every commit, it produces plausible prose nobody asked for, it will occasionally
commit something wrong on its own authority, and its cost is invisible until the bill arrives.
The proposal above deliberately keeps every model token inside a session a human is already
watching.

**One tension to record, not to paper over.** `graph-guard`'s stated design is *"it guards; it
does not document."* The ask is that documentation be updated on every commit. These are only
compatible under the reading above — the hook **detects and demands**, the session **writes**.
If someone later wants the hook itself to write documentation, that is a reversal of graph-guard's
design and belongs in an ADR, not in a script.

---

## 3 · What the official documentation settles that we had open

### 3.1 How one repo distributes skills to another — settled

`OPERATING-MODEL.md` §1 lists four candidate mechanisms and asks which wins. The documentation
answers it: **plugins, distributed through a marketplace, with a commit SHA pin.** The other three
lose on stated grounds — a submodule carries no namespacing and no version semantics, an MCP
server is the wrong shape for shipping *instructions* (see §3.3), and clone-on-demand has no pin
at all.

**`scio` becomes a marketplace** by adding `.claude-plugin/marketplace.json` at its root, listing
one or more plugins with `name`, `source`, `description` and `version`. **A plugin** is a directory
with an optional `.claude-plugin/plugin.json` manifest and, at the plugin *root* (never inside
`.claude-plugin/`): `skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`,
`monitors/monitors.json`, `bin/`, `settings.json`, and `commands/` for the legacy flat form. One
repo can therefore ship skills, subagents, hooks and MCP configuration **in a single install** —
which is precisely the shape `PIPELINE.md` §5 says the run document actually describes.

**The build repo consumes it** with two keys in its `.claude/settings.json`, which register the
marketplace and enable the plugin automatically once the folder is trusted:

```json
{
  "extraKnownMarketplaces": {
    "scio": { "source": { "source": "github", "repo": "<owner>/scio" } }
  },
  "enabledPlugins": { "scio-build@scio": true }
}
```

**The drift hazard has a documented answer.** Sources take a `sha`, and the resolved commit SHA is
itself a version source when no `version` field is set — so a plugin entry can be pinned to an
exact commit. `renames` migrates users when a plugin is renamed or withdrawn without breaking
installs. `claude plugin validate ./plugin --strict` checks `plugin.json`, `hooks/hooks.json` and
the frontmatter of every skill, agent and command, and treats warnings as errors. That is the
"fails loudly when the pin is stale" that `OPERATING-MODEL.md` asked for — but note the honest
limit: **validation checks schema, not truth.** It will not notice that a vendored skill calls a
function whose signature changed. Version-pinning the package is still the only defence there.

Two further facts worth having. Plugin skills are **namespaced** (`/scio:brainstorm`), so they
cannot collide with a project's own; project and user `.claude/agents/` definitions **override**
same-named plugin agents, so a local override is possible without forking. And `--plugin-dir ./path`
loads a plugin for one session without installing it, which is how to test `scio` as a marketplace
before publishing anything.

### 3.2 How a skill gets an eval — settled, and it is more than we assumed

`docs/next/SKILLS.md` demands *"runnable cases with expected outcomes"* and notes only that
"`skill-creator` supports evals and variance analysis". Verified at the source, the loop is:

1. **Test cases** — prompts, input files and expected behaviour in `evals/evals.json` **inside the
   skill directory**, so the eval travels with the skill and ships in the plugin.
2. **Isolated runs** — one subagent per case, clean context, token count and duration recorded.
   This matters: `skills.md` warns that leftover context from authoring a skill masks gaps in it.
3. **Grading** — each assertion checked against the output, pass/fail **with evidence**, into
   `grading.json`.
4. **Benchmark** — `benchmark.json` aggregating pass rate, time and tokens for *with-skill* versus
   *without-skill*, as **mean ± stddev** with the delta. That is the variance analysis.
5. **Version comparison** — a blind A/B between two versions of a skill.
6. **Description tuning** — 20 generated should-trigger / should-not-trigger prompts, hit rate
   measured, description edits proposed.

**`claude plugin eval` does exist, and it is the better answer — but we cannot run it yet.**
*(Corrected twice on 2026-08-26. First: this section originally said there was no such subcommand;
it exists, verified via `--help`. Second: **invoking it returns `plugin eval is currently in early
access`** on this account. The capability described below is real and documented by the CLI's own
help; none of it is available to us today. `skill-creator` is the fallback that works now.)*

It runs eval cases — `<eval dir>/**/case.yaml`, or `prompt.md` plus `graders/*.md`, defaulting to
`evals/` — against a plugin and reports scored results. The target may be a path, a plugin name, or
a `plugin@marketplace` id; installed plugins and skills-dir plugins both resolve.

The feature that makes it the right tool for our four-part contract is `--ablation`, which defaults
to **`with-without`**: it runs a no-plugin baseline arm alongside the real one and reports the score
delta. That is precisely the measurement `docs/next/SKILLS.md` demands and cannot currently make —
*does this skill change the outcome, or does the model do it anyway?* Graders marked `with-only`
(including `tool_used: Skill`) count as a plugin-fired indicator rather than as score, so the run
also tells you whether the skill **triggered at all** — which is the failure our `graphify`
description has.

Also present: `--case <glob>` to filter, `--eval-dir` to relocate the directory, and
`--allow-tools` as an operator grant for gated tools (`Bash`, `Write`, `Edit`, `WebFetch`, `mcp__*`)
with `Tool(pattern:*)` syntax. `claude plugin details <name>` reports a plugin's component
inventory **and its projected token cost**, and `claude plugin init` scaffolds one that auto-loads
next session.

**The consequence for us:** the eval half of our four-part contract has a destination — a command,
ablation-controlled — but not yet a road. Until early access opens, the same measurement has to be
made two other ways: `skill-creator`, which runs isolated per-case subagents and reports
with-versus-without as mean ± stddev; and by hand, which is what `obra/superpowers`'
`writing-skills` already prescribes — **watch an agent fail without the skill before writing it.**
Neither is blocked. Nothing excuses seventeen skills with no evidence that any of them changes an
outcome.

`skill-creator` remains useful and is not superseded — it *authors* evals and tunes descriptions;
`claude plugin eval` *runs* them with a baseline. Use both.

**Still not found:** `/skill-doctor`. The nearest bundled thing is **`/doctor`** (alias `/checkup`),
which does something adjacent and useful: it finds unused skills, MCP servers and plugins **weighed
against their context cost**, and flags slow hooks.

### 3.3 MCP servers versus connectors — settled, and it decides the knowledge-base question

They are not two competing designs. **A connector is an MCP server you added in claude.ai**, at
`claude.ai/customize/connectors`; when Claude Code is authenticated with a claude.ai subscription
login it picks those up automatically. Connectors are therefore **account-scoped and remote** —
admin-controlled on Team and Enterprise, subject to per-tool organisation controls, invisible when
you authenticate by API key, and switchable off with `disableClaudeAiConnectors`. An MCP server
configured in the repo is **project-scoped and local**: `.mcp.json` at project scope is checked in
and shared with the team, with `local` and `user` scopes above and below it, and plugins can ship
their own `.mcp.json`.

For distributing **our** knowledge base to a build session, the connector route is wrong on both
counts — it would require hosting `scio` as a remote service and would attach it to an account
rather than to a repository. The repo-scoped options are the real ones: files shipped by a plugin
(§3.1) for the skills, and, if the graph turns out to be what sessions actually query, a
project-scope stdio MCP server — which `graphify --mcp` already provides.

### 3.4 Subagents — settled

`PIPELINE.md` is a chain of eight stages; the documentation confirms a stage can be a subagent and
gives the exact contract. A subagent is a markdown file with YAML frontmatter in `.claude/agents/`
(project), `~/.claude/agents/` (user) or a plugin's `agents/`, in that precedence order under
managed settings and `--agents`. Only `name` and `description` are required. The optional fields
that matter for a pipeline: `tools` / `disallowedTools`, `model`, `permissionMode`, `maxTurns`,
**`skills:` to preload named skills**, `mcpServers`, `memory`, `isolation: worktree`, and `hooks`.

The property that makes the chain work is **context isolation**: a non-fork subagent starts with
its own system prompt, the task message, `CLAUDE.md`, a git-status snapshot and its preloaded
skills — and gets **none** of the conversation history, previously invoked skills, or files the
parent already read. That is the enforcement mechanism for `PIPELINE.md`'s stage contracts:
Stage 3 receives *only* what Stage 2 hands it, structurally, not by good intentions. The limits:
nesting depth 3 below the main thread, 20 concurrent subagents, both env-var configurable. And
`skills: [...]` is the direct answer to the bootstrap problem in `PIPELINE.md` §5 — a stage
preloads the two or three skills it needs, instead of a run document loading fifteen.

---

## 4 · What we already have that is better, and what of ours is worse

**Ours is better on provenance, and it is not close.** Thirteen of our sixteen skills open with a
`## 1 · Source` heading naming authors, venue and date, and carry an explicit Limits section
separating what a paper shows from what we are assuming. Across 289 official plugins and 2,282
community plugins, the scan found none that does this. `ontoagent-elicitation` states the exact
scope of OntoAgent's +33%; `architecture` carries fourteen patterns *with what disqualifies each*
rather than a persona; `testing` is built from three named, file-and-line-verified failures in
`hello-world`. Every overlapping candidate — `frontend-design` against `app-design`, `code-review`
against `testing`, `gstack` against `architecture` — is more generic than what we have.
**Do not replace any of them.**

**Ours is worse on four specific, checkable things.**

1. **No skill has an eval.** Sixteen skills, zero `evals/` directories. The four-part contract's
   fourth leg is unbuilt everywhere. §3.2 is the fix and it can start with one skill.
2. **No skill uses progressive disclosure.** Every one is a single `SKILL.md`, and `graphify`'s is
   **1,204 lines** — it all loads when invoked. `skill-creator` splits into `references/`,
   `scripts/`, `agents/` and `assets/` and loads only what a given path needs. Our
   `architecture` (395), `brainstorm` (465) and `testing` (465) are candidates for the same
   treatment, and this is a token-economy item, not a tidiness one.
3. **`graphify` has three defects the others do not.** Its description (109 chars) says only what
   the skill does and never when to use it, which by `SKILLS.md`'s own rule means it will not fire
   from context; it carries a `trigger:` key that is not in the frontmatter reference and is not
   part of the Agent Skills spec's six fields; and it remains the vendored copy that drifts from
   the installed package. `graphifyy` on PyPI is at **0.9.50**, uploaded 2026-08-25 — so the
   version named in `SKILLS.md` is current today, which makes this exactly the right moment to pin
   it and re-fetch the vendored file deliberately.
4. **`superpowers/writing-skills` has a rule we do not.** *Watch an agent fail without the skill
   before you write it.* Our contract checks that a skill is honest about its source; that rule
   checks that the skill changes behaviour at all. They are complementary, and the `skill-writer`
   proposed in `OPERATING-MODEL.md` §2.2 should carry both — baseline first, then the four-part
   shape, then the eval. Adopt the rule and cite it; do not install the plugin.

**One thing that is neither.** `hesreallyhim/awesome-claude-code` (53,024★, pushed today) and the
other directories are worse than our skills in every respect and more useful than any of them for
one job: finding out whether something already exists before we write it. That is the standing
rule in `OPERATING-MODEL.md` §2.1, and a bookmark is the right form for it.

---

## 5 · Sources

All fetched and verified **2026-08-26**. `P` = primary, `S` = secondary.

**Primary — the ten, tier one**

- `P` [code.claude.com/docs](https://code.claude.com/docs) — and specifically `/en/hooks`,
  `/en/plugins`, `/en/plugin-marketplaces`, `/en/plugins-reference`, `/en/skills`,
  `/en/sub-agents`, `/en/mcp`, `/en/commands`, `/en/cli-reference`. Live.
- `P` [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
  — Apache-2.0, 34,297★, pushed 2026-08-26. **289 plugins** in `marketplace.json`.
- `P` [github.com/anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community)
  — Apache-2.0, 2,112★, pushed 2026-08-25. **2,282 plugins**. Read-only mirror.
- `P` [github.com/EvanLi/Github-Ranking](https://github.com/EvanLi/Github-Ranking) — MIT, 11,997★,
  auto-updated 2026-08-26T04:07Z. Generic GitHub stars/forks leaderboard; **no Claude-specific content**.
- `P` [gist.github.com/hqman/e29cb6386c539d795767e8c3fd2c959b](https://gist.github.com/hqman/e29cb6386c539d795767e8c3fd2c959b)
  — "Boris Cherny's CLAUDE.md", created 2026-02-23. Live. A short workflow file (plan mode,
  subagents, `tasks/todo.md`, `tasks/lessons.md`, self-improvement loop). **Attribution unverified** —
  a third-party gist, not a repository under Cherny's own account.
- `P` [getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually](https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually)
  — John Kim, 2026-02-21. Live, **not paywalled**. Corroborates the mechanisms above from practice:
  team `CLAUDE.md` in git, slash commands in `.claude/commands/` in git, MCP config in git,
  `/permissions` in `.claude/settings.json` rather than skipping checks, post-tool-use hooks for
  formatting, feedback loops for verification. Its claims about parallel-session counts and a
  "2–3x quality" figure are **reported, not measured**, and are not used as evidence here.

**Secondary — pointers only, every name verified independently**

- `S` [blockchain-council.org/claude-ai/top-50-claude-skills-and-github-repos](https://www.blockchain-council.org/claude-ai/top-50-claude-skills-and-github-repos/)
  — 2026-03-23, updated 2026-08-03. Live. Names 4 repos + a tool. Promotional for its own certification.
- `S` [codetocloud.io/blog/claude-code-repos-engineering-team](https://codetocloud.io/blog/claude-code-repos-engineering-team/)
  — 2026-05-21. Live. Names 10 repos.
- `S` [ayautomate.com/blog/best-claude-code-github-repos](https://www.ayautomate.com/blog/best-claude-code-github-repos)
  — 2026-03-29. Live. Names 10 repos; **one slug does not exist** and one star count is off by ~184,000.
- `S` [kdnuggets.com/10-github-repositories-to-master-claude-code](https://www.kdnuggets.com/10-github-repositories-to-master-claude-code)
  — Live, but returns **403** to automated fetch; retrieved with a browser user-agent. Names 10
  repos; **one is archived**.

**Beyond the ten**

- `P` Official MCP registry, `registry.modelcontextprotocol.io/v0/servers` — queried for `graph`,
  `knowledge`, `memory`, `docs`. Results are overwhelmingly hosted third-party services, with
  duplicate entries for the same server. Nothing fits a repo-scoped knowledge base.
- `P` PyPI `graphifyy` — **0.9.50**, uploaded 2026-08-25, 218 releases, **no licence declared** in
  package metadata.
- `P` [github.com/obra/superpowers](https://github.com/obra/superpowers) — MIT, v6.3.0, 277,967★,
  pushed 2026-08-19. 14 skills, inspected.
- `P` [github.com/anthropics/skills](https://github.com/anthropics/skills) — 171,772★, pushed
  2026-08-21. **No repo-level LICENSE file**; the README states most skills are Apache-2.0 and the
  document skills (`docx`, `pdf`, `pptx`, `xlsx`) are **source-available, not open source**.
  Installable as a marketplace: `/plugin marketplace add anthropics/skills`.
Stars, last push, licence and archived flag for every candidate in §1 were read from the GitHub
API on 2026-08-26.

**Stated limits of this scan.** I did not install or run any candidate; verdicts rest on
documentation, source inspection and repository metadata, not on measured behaviour. I did not
read all 289 official or 2,282 community plugin manifests — I filtered both marketplaces by
keyword against our stated needs and inspected the matches. The `code.claude.com` pages were read
via their published Markdown; version-gated behaviour ("requires v2.1.x or later") is reported as
the docs state it and was not checked against an installed CLI. Star counts are a popularity
signal and are reported, never used as a reason to adopt.

*Written 2026-08-26. Proposals only. Per `CLAUDE.md`: every adoption above becomes an ADR before
it becomes a fact.*


---

## Corrections from the deep pass, 2026-08-26

`docs/mined/` holds four documents that read what this scan only listed. Three rows above were
wrong and are corrected in place; the pattern behind all three is worth stating once.

**Every wrong row was wrong in the same way: it described the repository's own marketing copy.**
gstack was called "23 tools cast as personas" because its README says so; the repo is a large
TypeScript codebase with 554 test files, and the single most useful artefact found across all eight
repositories sits in one of its test files. Licences were taken from the GitHub API's summary rather
than from the `LICENSE` file, so a Commons Clause that withholds the right to sell was recorded as
plain MIT, and a repository with no licence at all was recorded as having one.

The verdicts survived. The reasons did not. A `skip` reached by reading a README is not a skip you
can defend later, and the four `docs/mined/` documents exist because of it.
