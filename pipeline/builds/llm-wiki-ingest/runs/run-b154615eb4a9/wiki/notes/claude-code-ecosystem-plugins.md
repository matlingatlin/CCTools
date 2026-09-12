---
title: The Claude Code plugin stack the videos sell — what each one actually is
sources:
  - url: https://github.com/diegosouzapw/OmniRoute
    fetched: 2026-09-02
  - url: https://github.com/thedotmack/claude-mem
    fetched: 2026-09-02
  - url: https://github.com/headroomlabs-ai/headroom
    fetched: 2026-09-02
  - url: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-code-setup/README.md
    fetched: 2026-09-02
  - url: https://github.com/iamneilroberts/claude-skills/blob/main/skills/task-observer/SKILL.md
    note: "A mirror of Eoghan Henn's (rebelytics) task-observer; CC BY 4.0."
    fetched: 2026-09-02
  - url: https://github.com/Leonxlnx/unlazy
    fetched: 2026-09-02
  - url: https://github.com/NanoNets/Graft
    fetched: 2026-09-02
  - url: https://github.com/msitarzewski/agency-agents
    fetched: 2026-09-02
  - url: https://github.com/DeusData/codebase-memory-mcp
    fetched: 2026-09-02
  - note: "Four short videos ('5 plugins', 'token limit mid-task', 'unlazy', '4 repos'), transcribed locally 2026-09-02. Claims graded per tool."
status: verified
tags: [claude-code, plugins, memory, compression, routing, tokens, claims-graded]
related: ["[[claude-code-extension-layer]]", "[[claude-md-and-memory]]", "[[model-agnostic-agent-harnesses]]", "[[hooks]]", "[[mcp]]", "[[agent-builder-prior-art]]", "[[testing-skills-methodology]]", "[[harness-over-model-prime-agent]]", "[[graphify-assessment]]", "[[third-party-landscape]]", "[[glm-5.3-local]]", "[[model-routing-free-and-local]]", "[[system-prompt-transparency]]"]
---

# The plugin stack

Two videos sell the same four-to-five tools as "don't use Claude Code without these". Each
is real. Each is described wrongly in at least one respect, and two carry a cost the videos
never mention. MEASURED from the README unless marked.

| tool | what it is | licence · stars | the sentence the video got wrong |
|---|---|---|---|
| **OmniRoute** | MIT gateway: one endpoint, 352 providers (152 free), ~1,312 models; Claude Code via base URL `http://localhost:20128/v1` or `omniroute run claude --model …`; quota-aware fallback; RTK+Caveman compression "15–95%" | MIT · 60.1k | "1.6 billion free tokens a month" — README says "~1.51B free tokens / month" pooled across 38 free-tier keys, "~2.13B in the first month with signup credits". Close, and it is a *pool of other people's free tiers*, each with its own terms |
| **claude-mem** | five lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) capture tool use, compress it "with AI" via the Agent SDK, store in SQLite + Chroma, inject via MCP in layers (~50–100 tokens per hit, 500–1,000 for detail) | Apache-2.0 · 93.0k | "memory across sessions" — true. Not said: the compression spends model calls, and **cloud sync backs memories up to cmem.ai** ("the worker syncs on write"); `<private>` tags are the opt-out |
| **Headroom** | local proxy/wrapper; reversible compression of tool outputs, logs, JSON (originals cached locally, `headroom_retrieve` on demand); `headroom wrap claude` | Apache-2.0 · 68.4k | "same results with way fewer tokens" — README: 20% for coding agents, 60–95% for JSON; "prose and dense output compress minimally". Accuracy benchmarks at **N=100** per category (GSM8K, TruthfulQA, SQuAD v2, BFCL) |
| **claude-code-setup** | Anthropic's official plugin: scans the project, recommends MCP servers, skills, hooks, subagents, slash commands; **"read-only — it analyzes but doesn't modify files"** | Anthropic | "builds AI skills for the tasks you keep repeating", "watches how you work", "removes the fluff" — **none of this is in the README**. It recommends; it does not write or delete |
| **task-observer** | one SKILL.md that appends numbered observations to `skill-observations/log.md` during any multi-step task; updated skills are written to `skill-updates/<date>/` for the user to replace by hand | CC BY 4.0 | "constantly improves your other skills in the background, entirely automatically" — the SKILL.md says the opposite: "does NOT automatically edit other skills", review is manual and weekly |
| **unlazy** | Depth Tree: split a task N layers deep, every leaf gets the whole time budget; per-task gates file (CHECK command, EXPECT marker, EVIDENCE line; "pending" = unmet); a Stop hook returns `decision: "block"` while gates are unmet | MIT · 3.0k | "OpenAI and Anthropic *design* their models to be lazy and lie" — the repo cites research on laziness (arXiv 2512.20662, 2501.18585, 2604.10739, 2508.13141, SlopCodeBench 2603.24755; REPEATED, not read); none says "designed to". "Partial compliance" is a real term from that literature |
| **Graft** | tree-sitter code graph + markdown concept nodes, `.claude/` hooks and statusline; structural refresh is deterministic, "$0", 0.18–0.74 s | MIT · 5.4k | "4× cheaper, 3× faster" — README: those are the *biggest single-task wins* from a sweep; the controlled figure is +42% tokens, +46% tool calls, +60% time over 162 runs on two codebases; SWE-bench Verified **33/50 vs 27/50** |
| **codebase-memory-mcp** | graded in full in [[graphify-assessment]] (SANDBOX). Single static binary, no runtime, no API key; indexes a repo into a queryable graph (functions, classes, packages; calls / imports / type-use edges), 158–162 languages; Cypher queries <1 ms, name search <10 ms; Linux kernel (28M LOC) indexed in 3 min; 45 client surfaces | MIT · 41.8k | "99% fewer tokens" — README's basis: five structural queries at ~3,400 tokens vs ~412,000 by file-by-file grep, 99.2%; a real but hand-picked comparison (nobody greps 412k tokens on purpose) |
| **OpenMontage** | 12 video pipelines, 100+ tools, 700+ skill/knowledge files that turn a coding agent into a video studio; needs third-party generation APIs (Kling, Runway, Veo, ElevenLabs …) or local models; plugs into Claude Code, Cursor, Copilot, Codex, Windsurf | **AGPL-3.0** · 55.5k | "makes any coding agent shoot, cut and export video" — the agent orchestrates; the shooting is paid APIs the video never mentions, and the licence is copyleft |
| **Ruflo** (ex Claude Flow) | graded in full in [[harness-over-model-prime-agent]] — MIT, 70.2k★, swarm-with-consensus over Claude Code, AgentDB shared vector memory | MIT · 70.2k | see that note |
| **agency-agents** | 230+ agent prompt files in 16+ divisions (engineering, design, paid media, …); each has identity, workflow, deliverables, success metrics, rules; installer with `--tool`, `--division`; OpenCode "registers only ~119 agents and silently drops the rest" | MIT · 150k | "a full AI agency" — it is a persona library: prompts with a voice, no tooling, no evals |

## What travels

- **Two tools ship a Stop hook that blocks the turn on unmet evidence** (unlazy) or on
  unrecorded work (this repo's own stop hook). Same mechanism, independently arrived at:
  a gate the model cannot talk its way past is worth more than an instruction to be
  thorough. unlazy's *gates file* — command, expected output, evidence line, and
  "a ticked box with pending evidence is worse than an empty box, because the agent
  graded its own work" — is `verification-before-completion` in file form and a better
  shape than ours (ours is prose).
- **task-observer is `learn-eval` + `wave-reflect` in one file**, and its discipline
  (append to a log, never edit the target until review) matches "human gate ∝ autonomy".
  Nothing to adopt; a corroboration.
- **Memory that phones home.** claude-mem's cloud sync is the fourth gate's textbook
  case: a memory layer that copies every session summary to a third party by default.
  Not adopted. Headroom stays local and is the honest one of the two "token" tools —
  and it says in its own README where its savings are small.
- **Compression changes the instrument.** Headroom or OmniRoute's Caveman in front of a
  measured run would alter what the model sees; a build's cost row through either is a
  different experiment. Never in `dispatch.py`'s path.
- **Graft's SWE-bench claim is n=50.** Six more solved out of fifty is consistent with
  the effect being real and with noise; the +42% token figure over 162 runs is the
  stronger number and the one to cite. The graph refresh being LLM-free is the design
  point that matters (compare `graphify-harvest`).
- **Ruflo's shared memory, read as a product component rather than a developer tool:** a
  memory every agent reads and writes and that persists across runs is what the Agent SDK's
  hosting page disables for multi-tenant work; fine in one developer's repo, a leak by design
  inside a product that builds other people's apps. The grading of Ruflo itself is in
  [[harness-over-model-prime-agent]]; this line is the only thing added here.
- **agency-agents at 150k stars** is the market saying personas sell. Our `templates/`
  has an agent scaffold; the roster is a reuse-first source for *names of jobs*, not
  for methods — none of the 230 files carries an eval.

## Re-sightings (2026-09-02, later the same day)

- The "four plugins" script arrived a second time from the same creator as a re-cut
  (different file, same claims, "Clod" for Claude in the audio). Nothing new; the
  grading above stands, including that `claude-code-setup` is read-only.
- An 11-second clip ("run Claude Code for FREE with unlimited usage with this one repo")
  shows OmniRoute's README on screen — the `~1.51B` free-tier budget dashboard is
  visible. "Unlimited" is the video's word; the README's is "~1.51B free tokens /
  month", pooled across 38 free-tier keys.
- A carousel cover "someone dropped a GitHub repo that lets you use Claude Code for free
  forever, already has 51k stars" shows Claude Code's `/model` picker listing
  `open_router/google/gemma-3-12b-it:free` … `gemma-4-26b…:free` and a base URL under
  `anthropic/open_router/…`. **Resolved 2026-09-02 by the carousel's slide 2/4**, supplied
  later the same day from a second session: the repo is **`Alishahryar1/free-claude-code`**,
  not OmniRoute — a separate project with the same shape. MIT, **52.8k stars** on
  2026-09-02 (the cover's 51k was two days stale). Graded in
  [[model-agnostic-agent-harnesses]] § free-claude-code. What stands from the earlier
  reading: every Claude Code-for-free post seen this week resolves to a gateway in front of
  other providers' free tiers, and Anthropic's gateway page says routing to non-Claude
  models is unsupported.

The routers listed here are arm C in [[model-routing-free-and-local]], which sets the per-day arithmetic and the rules for any routed run (added 2026-09-02).

## Three context-window tools from one carousel (added 2026-09-02; REPEATED — READMEs not fetched)

Source: seven-slide carousel by @godofprompt, plus search-result snippets from each repo.

| tool | what it does | licence · stars | the claim, and its basis |
|---|---|---|---|
| **Context Mode** (`mksglu/context-mode`) | MCP server + hooks that sandbox tool output — raw data stays out of the window, a summary goes in; session events in SQLite/FTS5, BM25 retrieval on compaction; 17 platforms | **ELv2** (source-available, no competing SaaS) · ~20k | "98% reduction on logs and repetitive tool calls" — one example: 315 KB → 5.4 KB. The slide's "30-minute session stretched to 3 hours" is arithmetic on that example. The "used across teams at Microsoft, Google, Meta…" badge is self-reported logos |
| **Token Optimizer** (`alexgreensh/token-optimizer`) | audits the setup for "ghost tokens" (bloated configs, stale docs); blocks a re-Read of a file already seen and substitutes a structural skeleton (a 720 KB / 180k-token file → 250 tokens); checkpoint + restore across compaction; live dashboard | **PolyForm Noncommercial** · 2.1k | "5–15% context recovery from cleanup, 25%+ with smarter compaction" — targets, not measurements; runs local, "telemetry none". Same licence problem as BASE ([[claude-md-and-memory]]) |
| **code-review-graph** (`tirth8205/code-review-graph`) | tree-sitter graph of functions/classes/imports with calls, inheritance and test-coverage edges; on a change, traces the blast radius and hands only that to the agent via MCP; GitHub Trending #1 | **MIT** · 31k, 1.7M PyPI downloads | "6.8× fewer tokens on reviews, up to 49× on daily coding tasks" — the author's benchmark ("Reproducing the benchmarks" is a README link); same family as Graft, Graphify and codebase-memory-mcp in [[graphify-assessment]] |

The pattern across all three: the number is one author-chosen example, and the mechanism
is the honest part. Context Mode's mechanism (tool output to a local store, summary to the
window) is the one that would change our cost rows most and is exactly why none of them may
sit in front of a measured run — see "Compression changes the instrument" above.
