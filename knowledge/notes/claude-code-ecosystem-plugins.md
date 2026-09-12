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
tags: [claude-code, plugins, memory, compression, routing, tokens, claims-graded]
related: ["[[claude-code-extension-layer]]", "[[claude-md-and-memory]]", "[[model-agnostic-agent-harnesses]]", "[[hooks]]", "[[mcp]]", "[[agent-builder-prior-art]]", "[[testing-skills-methodology]]", "[[harness-over-model-prime-agent]]", "[[graphify-assessment]]", "[[token-economy-playbook]]", "[[third-party-landscape]]", "[[glm-5.3-local]]", "[[model-routing-free-and-local]]", "[[system-prompt-transparency]]", "[[production-site-checklist]]", "[[temporal-kg-agent-memory]]"]
raw: "none - fetched before the raw layer existed (2026-09-02); url + fetched are the only provenance"
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

## Which page each of these actually lands on

This page grades the *sales pitch*. The mechanism each tool reaches for is documented
elsewhere, and the pairing is what makes a row usable:

- **The slot each tool is competing for** is in [[claude-code-extension-layer]], the hub note
  that answers which built-in feature covers which job. Every row above is a third-party
  substitute for one of those slots, so the hub is the page that decides whether the cost is
  worth paying at all.
- **Lifecycle mechanics** — claude-mem's five hooks and unlazy's blocking `Stop` — are
  specified in [[hooks]]. That two unrelated projects and this repo independently arrived at
  a Stop hook that blocks on unmet evidence is the strongest field evidence that page has.
- **The injection path** for claude-mem and codebase-memory-mcp is [[mcp]], which also holds
  the security section that matters before running any of them, and the two memory servers
  this base has actually graded.
- **OmniRoute's pool of other people's free tiers** is a routing arm, and the model such an
  arm would reach is specified in [[glm-5.3-local]] — including which of the two models
  sharing that name you would actually get.
- **task-observer's claim to improve your skills automatically** is answered by
  [[testing-skills-methodology]]: measuring one skill against a baseline is the expensive
  part, and no tool above does it. Its own SKILL.md agrees — review is manual and weekly.
- **agency-agents, 230+ persona files with no tooling and no evals**, is the persona-library
  genre graded in [[agent-builder-prior-art]], where the same distinction decides the
  reuse-first gate: a prompt with a voice is not an agent builder.
- **The method itself** is shared with [[system-prompt-transparency]]: a video's sentence set
  beside the primary it claims to summarise. Both pages find the same shape of error — the
  primary says something narrower, and the video's version is the one that travels.

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
- **Where Graft's +42% is used as a rule.** [[token-economy-playbook]] takes this row as its
  standing prohibition against injecting graph context into every call — the only controlled,
  rival-tool measurement in this base that a token policy could be built on, which is why the
  number matters more than Graft itself does. A reader crossing from there arrives here for the
  n=50 caveat below; a reader crossing the other way gets the policy the figure justifies.
- **Graft's SWE-bench claim is n=50, and the README has since stopped showing the counts
  (re-read 2026-09-11).** The controlled figures survive verbatim — 42% fewer tokens, 46% fewer
  tool calls, 60% less time, 162 runs — but the raw pair this note cites is gone as a pair, and
  the *same six instances* now appear in two larger-sounding forms: **"66% (+12 pts)"** in a
  table, and **"+22% more SWE-bench instances resolved"** in the badge. All three are 33 against
  27 out of 50: +6 absolute, +12 percentage points, +22% relative. Nothing was falsified and no
  number contradicts another — **the denominator simply stopped being shown**, and the framing
  that travels is the one where six looks biggest. That makes the caveat below more valuable than
  when it was written, not less, which is the argument for recording a sample size at the moment
  you read it. Six more solved out of fifty is consistent with
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

## Three context-window tools from one carousel (added 2026-09-02; **READMEs fetched 2026-09-08**)

Source: seven-slide carousel by @godofprompt, plus search-result snippets from each repo. The
section header said REPEATED because nobody had opened the three repositories. All three answer,
and the correction below is the one worth reading first — **on two of the three, the README is
more careful than the note was.**

| tool | what it does | licence · stars | the claim, and its basis |
|---|---|---|---|
| **Context Mode** (`mksglu/context-mode`) | MCP server + hooks that sandbox tool output — raw data stays out of the window, a summary goes in; session events in SQLite/FTS5, BM25 retrieval on compaction; 17 platforms | **ELv2** (source-available, no competing SaaS) · ~20k | "98% reduction on logs and repetitive tool calls" — one example: 315 KB → 5.4 KB. The slide's "30-minute session stretched to 3 hours" is arithmetic on that example. The "used across teams at Microsoft, Google, Meta…" badge is self-reported logos |
| **Token Optimizer** (`alexgreensh/token-optimizer`) | audits the setup for "ghost tokens" (bloated configs, stale docs); blocks a re-Read of a file already seen and substitutes a structural skeleton (a 720 KB / 180k-token file → 250 tokens); checkpoint + restore across compaction; live dashboard | **PolyForm Noncommercial** · 2.1k | "5–15% context recovery from cleanup, 25%+ with smarter compaction" — targets, not measurements; runs local, "telemetry none". Same licence problem as BASE ([[claude-md-and-memory]]) |
| **code-review-graph** (`tirth8205/code-review-graph`) | tree-sitter graph of functions/classes/imports with calls, inheritance and test-coverage edges; on a change, traces the blast radius and hands only that to the agent via MCP; GitHub Trending #1 | **MIT** · 31k, 1.7M PyPI downloads | "6.8× fewer tokens on reviews, up to 49× on daily coding tasks" — the author's benchmark ("Reproducing the benchmarks" is a README link); same family as Graft, Graphify and codebase-memory-mcp in [[graphify-assessment]] |

### Read against the READMEs, 2026-09-08

**code-review-graph's numbers in the row above are wrong, and the real ones are bigger and
weaker at the same time.** "6.8× fewer tokens on reviews, up to 49× on daily coding tasks"
appears nowhere in the README. The current headline is **~65× median per-question reduction
across 6 repositories, range 36×–376×**, and the author states plainly that "376× is the best
case (fastapi, the largest corpus), **not the headline**". Three things came with it that no
carousel would have carried:

- **The baseline is one the author disowns in the same paragraph:** "the whole-corpus baseline
  above is an upper bound no real agent pays — a competent agent greps for identifiers and reads
  only the best-matching files." A separate `agent_baseline` eval measures the realistic one.
- **The formal `token_efficiency.py` benchmark "reports ratios below 1 for small commits."** The
  tool can cost more than it saves, and the README says so.
- **The numbers were re-captured on 2026-08-02 and went DOWN**, with the reason given (richer
  node embedding text grew the graph response). Same retraction practice as Soup's in
  [[local-finetuning-layer-streaming]], done unprompted.

Its accuracy table is graded the same way: 0.693 average F1 over 13 commits, and a recall of
1.000 labelled by the author as "a circular upper bound, not '100% recall'" because the ground
truth is derived from the graph being tested.

**Context Mode is better evidenced than "one example".** The README carries an **8-scenario
table** — Playwright snapshot 99%, GitHub issues 98%, access log 100%, Context7 docs 96%,
analytics CSV 100%, git log 99%, test output 95%, subagent repo research 94% — and links a
21-scenario benchmark. "315 KB → 5.4 KB, ~30 minutes to ~3 hours" is the README's own
whole-session summary, not the slide's arithmetic on a single figure. What is still missing is
the only thing that matters for us: no comparison against a run without it, so it remains a
compression ratio and not a result. **ELv2** confirmed.

**Token Optimizer has changed what it claims.** The "5–15% / 25%+ context recovery" framing is
gone; the README now headlines **dollars** from one user's 684 sessions over 30 days (snapshot
ending 2026-06-15): "**counted**" ~$313/mo logged action by action, and "**big picture**"
~$1,877/mo (~18%) as a counterfactual against a frozen ~95%-Opus baseline. It insists the two
"are never summed" and that "your number is your own" — careful language around what is still
an n=1 self-report priced against a baseline the author chose. **PolyForm Noncommercial**
confirmed, and the licence note above needs softening: personal, research and non-commercial use
needs no purchase, **small teams get a no-cost commercial licence automatically**, and there is
a built-in 32-day grace period after written notice. That is a materially gentler licence than
BASE's ([[claude-md-and-memory]]).

**And one project in the neighbourhood does it properly, which sets the bar.**
[[temporal-kg-agent-memory]] records gbrain shipping `gbrain eval longmemeval` against a *public*
benchmark, reporting the **strict** `recall_all@5` rather than the loose any-hit variant, and
saying in the same paragraph that 300 of the 470 questions need two or more sessions — the reason
the two metrics diverge. That is the missing half of every row above: not a bigger number, a
named metric with the reason its stricter form matters. It is still one run on the author's own
harness, so it is n=1 by our bar too.

**The pattern this batch actually shows** is the opposite of the one the section was written to
illustrate. The carousel's numbers were wrong or stale on all three; the repositories' own
READMEs disown their best figures, publish the scenario that makes the tool look bad, and record
a re-measurement that went the wrong way. The unread source was more honest than the summary of
it — which is an argument for the fetch, not for the scepticism.

The same video genre sells tools for the *generated site* rather than for the harness, and
[[production-site-checklist]] grades that batch on the same terms — UI UX Pro Max at 124.1k
stars with no benchmark of any kind, CodeRabbit and 21st.dev as commercial products rather
than talents. Read the two tables together and the rule is one rule: the tool is usually
real, and the sentence the video says about it is usually not the tool.

The pattern across all three, **as revised on 2026-09-08**: the mechanism is the honest part,
and so, it turns out, is most of the documentation — what was one author-chosen example is the
carousel's reading of it. Context Mode's mechanism (tool output to a local store, summary to the
window) is the one that would change our cost rows most and is exactly why none of them may
sit in front of a measured run — see "Compression changes the instrument" above.


---

*Queue triage, 2026-09-11 — **eight rows, one material change, and the seven negatives are the
useful part.** Each was checked against what this note actually cites rather than against what the
diff happened to touch:*

- ***claude-mem*** *is at **13.24.23** (was 13.24.1) and has added an "Awareness push pilot".
  **The five-hook claim survives**: SessionStart, UserPromptSubmit, PostToolUse, Stop and
  SessionEnd are all present in the new README, verified one by one. Nothing here is re-dated.*
- ***OmniRoute***: *the two counters that moved — an i18n language count 42 → 51 and migrations
  171 → 173 — are **not cited by this base**, which is the same finding as the first watcher batch.
  The numbers this note does cite all survive: **352 providers, 152 free, 1,312 models** (the last
  appears unformatted as `1312`, a rendering difference rather than a value change).*
- ***agency-agents***: *new rows added to the table (a China Network Engineer, a Focus Music
  Architect). The claim here is **"230+ agent prompt files in 16+ divisions"** — a floor, and the
  README still says "230+ agents", so additions cannot falsify it. **This is what a floor claim is
  for**, and it is worth noticing that the one phrasing in this table that cannot rot is the one
  written with a `+`.*
- ***OpenMAIC***: *a new `ASSET_QUOTA_BYTES` (10 GiB default) storage limit. This base carries no
  storage or quota claim about it — checked, not assumed.*
- ***graphify v8 README***: *a logo filename and its height.*
- ***claude.com/customers/block*** *and the **the-decoder** article: only their "Customer story"
  and "Top Stories" carousels moved — headlines for **other** pages. The chrome class this base
  has now seen four times and deliberately does **not** normalise.*
