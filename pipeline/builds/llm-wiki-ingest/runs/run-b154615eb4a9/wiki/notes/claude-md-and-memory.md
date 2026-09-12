---
title: CLAUDE.md, rules, and auto memory
sources:
  - url: https://code.claude.com/docs/en/memory
    fetched: 2026-09-02
    note: "Re-read in full 2026-09-02; the auto-memory limits and the absence of any dream/consolidation section are from that read."
status: verified
tags: [claude-code, memory, claude-md, rules, mechanics]
related: ["[[skill-anatomy]]", "[[claude-code-extension-layer]]", "[[agent-design-template]]", "[[graphify-assessment]]", "[[hooks]]", "[[model-agnostic-agent-harnesses]]", "[[claude-code-ecosystem-plugins]]", "[[llm-wiki-pattern]]", "[[third-party-landscape]]"]
---

# CLAUDE.md, rules, and auto memory

Two memory systems, both loaded at the start of every session, both **context not
enforcement** (to hard-block, use a PreToolUse hook): CLAUDE.md (you write) and
auto memory (Claude writes).

## CLAUDE.md locations (load order, broad → specific; concatenated, not overriding)

1. **Managed policy** (org-wide, cannot be excluded): macOS
   `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL
   `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md`.
2. **User:** `~/.claude/CLAUDE.md` (all projects).
3. **Project:** `./CLAUDE.md` OR `./.claude/CLAUDE.md` (source-controlled).
4. **Local:** `./CLAUDE.local.md` (personal, gitignore it).

Loaded from working dir up to filesystem root; root-down ordering means the file
closest to the launch dir is read **last**. `CLAUDE.local.md` appended after
`CLAUDE.md` at each level. Subdirectory CLAUDE.md files load on demand when Claude
reads files there, not at launch. Verify what actually loaded with `/context` →
Memory files. Block-level HTML comments are stripped before injection.

## Size and structure

- Target **under 200 lines** per file; hard ceiling 4 MiB (larger files skipped
  entirely). Longer files reduce adherence.
- Growing too large → move to path-scoped rules (loads only for matching files)
  or skills (loads on demand). `@path` imports help organization but NOT context
  (imported files still load at launch).
- Be concrete and verifiable ("Use 2-space indentation", "Run `npm test` before
  committing"). Contradictory rules → arbitrary choice.

## Imports (`@path`)

Relative (resolved against the importing file) or absolute; recurse to **4 hops**;
skipped inside code spans/blocks (`` `@README` `` stays literal). An import
resolving outside the working dir in a project file triggers a one-time approval
dialog; user-scope imports are trusted (except Cowork desktop). AGENTS.md is not
read directly — bridge via `@AGENTS.md`, a symlink, or `/import` (v2.1.213+).

## `.claude/rules/`

Topic files (`.md`, discovered recursively). Rules **without** `paths` frontmatter
load at launch with the same priority as `.claude/CLAUDE.md`. **Path-specific
rules** use `paths:` (YAML list of globs) and load only when Claude reads matching
files:

```
---
paths:
  - "src/api/**/*.ts"
---
```

Globs support brace expansion (`src/**/*.{ts,tsx}`); the whole `paths` list shares
a 1,000-expanded-pattern / 4 MiB budget. `~/.claude/rules/` apply to all projects
and load before project rules (so project rules win). For task-specific content
that shouldn't always sit in context, prefer a skill over a rule.

## Auto memory (Claude-written)

On by default. Per-repository, shared across worktrees; stored at
`~/.claude/projects/<project>/memory/`. `MEMORY.md` is an index loaded every
session (first **200 lines or 25KB**, whichever first); one topic file per memory,
read on demand. `type` frontmatter: `user` / `feedback` / `project` / `reference`.
Skips anything derivable from code or already in CLAUDE.md. Toggle via `/memory`,
`autoMemoryEnabled: false`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. **Not loaded
into subagents** (except a fork); a subagent's own auto memory is a separate dir.

## Enterprise

Managed org-wide CLAUDE.md at the policy paths (cannot be excluded); or inline via
the `claudeMd` key in managed-settings.json (honored only in managed settings).
Split: technical enforcement → managed settings (`permissions.deny`,
`sandbox.enabled`); behavioral guidance → managed CLAUDE.md. `claudeMdExcludes`
(glob, absolute paths, arrays merge across layers) skips ancestor files;
managed policy CLAUDE.md cannot be excluded.

## "Self-healing" and /dream — what is official and what is not (added 2026-09-02)

Sources: `code.claude.com/docs/en/memory` re-fetched 2026-09-02 in full;
`github.com/grandamenium/dream-skill` (MIT, 136 stars) fetched the same day; search
results for the community coverage; a 14-second silent graphic ("make your Claude Code
self-healing", "111 sessions", "10 repeats → 15 fixed", "comment DREAM for the skill").

- **What the official memory page says (MEASURED):** auto memory writes four kinds of
  note (`user`, `feedback`, `project`, `reference`) into `~/.claude/projects/<project>/memory/`;
  `MEMORY.md` is the index, **first 200 lines or 25 KB loaded every session**, the rest
  dropped; Claude Code nags to shorten it near the limit and errors past it; a
  `modified` ISO timestamp is stamped into frontmatter on write (v2.1.214+); `/memory`
  toggles and opens it; memory files are excluded from the transcript retention sweep.
  **The page does not mention "dream", "Auto Dream" or consolidation at all.**
- **Auto Dream (REPEATED, third-party only):** several sites describe a background
  sub-agent that merges recent transcripts into `MEMORY.md` and topic files, deletes
  contradicted notes, converts relative dates, trims the index under 200 lines, and
  runs after 24 h and ≥5 sessions or via `/dream`; one calls it a Research Preview
  primitive in the Managed Agents API rolling out behind a server-side flag. None of
  this is on Anthropic's memory page as fetched. Treat as UNVERIFIED-official until the
  docs carry it; the `/dream` command was not in the built-in command list checked
  earlier today either.
- **`dream-skill` (MEASURED from its README):** four phases — orient, gather signal
  (greps recent JSONL transcripts for corrections, preferences, decisions, patterns),
  consolidate (merge, absolute dates, resolve contradictions, drop stale), prune and
  index (rebuild `MEMORY.md` under 200 lines). A Stop hook flags the next session to run
  `/dream` after 24 h. Its claim that it "replicates Anthropic's unreleased auto-dream
  feature" cites nothing. **No snapshot, backup or approval step is documented**; a fork
  (`timoncool/dream-skill`, not read) advertises "read-only dream pass, checkbox gate,
  snapshot + one-command rollback, no rm ever", which is what the video's "it proposes,
  you approve, nothing is overwritten" would require.
- **The graphic's numbers** ("111 sessions", "10 repeats", "15 fixed", per-session
  seconds) are the creator's illustration; no run is cited. The *idea* it illustrates —
  each session repeats a mistake because "each session thinks it is the first time", and
  a nightly pass over all sessions writes one rule ("read the file before you write it")
  — is exactly `wave-reflect` and `learn-eval` run on a schedule, and is the kind of rule
  that belongs in `feedback`-type auto memory by the docs' own taxonomy.

**For us.** Anything that rewrites memory from transcripts automatically is on the far
side of "human gate ∝ autonomy": a consolidation pass that *proposes* a diff is fine, one
that *applies* it without a snapshot is the memory equivalent of an unaudited hook. The
official mechanism we can rely on today is the 200-line index plus the `modified` stamp;
the `memory-provenance-separation` skill is what says what to do with the stamp.

## Rules that go stale — BASE, a graph-injected alternative to a static CLAUDE.md (added 2026-09-02)

Source: `https://github.com/ChristopherKahler/base` README fetched 2026-09-02; a 97-second
video by Charlie Automates whose claims are graded; the resource list at
`charlieautomates.com/free-resources`. MEASURED from the README unless marked.

- **The problem it names is real and is this note's subject:** everything in CLAUDE.md is
  loaded every session whether or not it applies, and nothing updates it. BASE's answer:
  "Turn Claude Code from a per-session tool into a workspace that remembers, maintains
  itself, and never goes stale."
- **What it is:** a single Rust binary (~20 MB, embedded dashboard). Tree-sitter AST graph
  over 35+ languages; on top of it *domains* (projects with milestones, tasks, rules),
  *rules* that fire by keyword trigger, star commands (`*handoff`, `*fork`, `*base`,
  `*end`), and a local "relay" between sessions with no external calls mentioned.
- **How it injects:** four hook points — session start (projects, handoffs, signals), at
  the prompt (domain rules, prior decisions), before a tool runs (file shape, entities,
  dependents), after it returns (call chains). The video's frames show a
  `<!-- BASE-MANAGED -->` block inside CLAUDE.md, `~/.base-gl/base.toml`, `base domain get
  DEV`, `base rule add --domain DEV`, and a graph of 218 nodes / 250 edges.
- **Licence — the part the video omits:** PolyForm Noncommercial 1.0.0. Commercial use
  needs the author's individual approval. 131 stars on 2026-09-02. Charlie Automates'
  own resource page lists it as "Free + paid tier".
- **Video claims graded:** "hook and MCP that base comes pre-installed with" — hooks
  MEASURED, MCP not found in the README (UNVERIFIED); "consistent behavior and output
  increased by 90%" — no source anywhere, UNSUPPORTED; "Graphify gives unlimited memory"
  — Graphify builds a code graph ([[graphify-assessment]]), memory is the video's word.

- **A seven-slide carousel the same evening (Charlie Automates)** adds three claims: "saving
  70× on tokens while 90×'ing output" and "90% better output" — no source, no run, and
  the two numbers do not agree with each other; and a **relay** feature: `*task` sends work
  to another running Claude Code session by codeword, with the receiving session told to
  read "the full message and verify its claims independently rather than taking them at
  face value" — a real mechanism (the README's relay, above), and the verify-before-trust
  line is the one thing in the carousel worth copying into any inter-session handoff.

**For us.** The mechanism worth having is *conditional loading of rules by trigger*, and
Claude Code already ships it without a binary: `.claude/rules/` with path-scoped rules
(above), and skills that load by description. BASE adds keyword triggers at the prompt
and a groomed graph of decisions; we get the first from skill descriptions and the second
from `knowledge/notes/` in git. Not adopted: noncommercial licence fails the portability
requirement of every talent, and the fourth gate keeps a self-injecting hook binary out
until its code is read. The *idea* — "a rule that nobody triggered this session costs
context for nothing" — is `steering-doc-pruning`'s no-op test, and this note should be
read with it.

## ICM — folder structure as the context architecture (added 2026-09-02)

Source: arXiv 2603.16021, "Interpretable Context Methodology: Folder Structure as Agentic
Architecture", Jake Van Clief and David McDermott, submitted 2026-03-17 (abstract page
fetched 2026-09-02; the 28-page paper not read); reference repo
`RinDig/Interpretable-Context-Methodology` (MIT). Surfaced by a 72-second video ("how I
stopped burning my Claude limits"), whose author calls it "Jay Van Cleef's ICM".

- **The claim (MEASURED from the abstract):** replace framework-level orchestration with
  filesystem structure — numbered folders are workflow stages, plain markdown carries
  prompts and context, local scripts do the mechanical work "that does not need AI at
  all". A layered read: CLAUDE.md always (~800 tokens), a root CONTEXT.md on entry
  (~300), a stage CONTEXT.md per task (~200–500), reference material on demand
  (REPEATED — the layer figures come from secondary write-ups, not the abstract).
- **What the paper does not claim:** any token-reduction number. Abstract: 28 pages, 5
  figures, 2 tables, 54 references, no experimental comparison stated.
- **Video claims graded:** "token cost reduction like a fifth or a sixth" — one person's
  before/after on a $200/month plan, no measurement, UNVERIFIED; the mechanism he
  describes (Claude finds the exact file instead of pulling in everything) is the
  paper's argument and is plausible; the paper itself offers no number.

This is the same principle as this note's "size and structure" section and
`steering-doc-pruning`'s progressive exposure, with a filesystem discipline attached.
Our `knowledge/notes/` + `pipeline/` layout already is a weak ICM; the numbered-stage
convention is the part we do not have.

## For this project

CLAUDE.md is a request, not a guarantee — the factory's security gate and any
"must never" rules belong in a **hook**, not in CLAUDE.md or a skill. `/init`
(with `CLAUDE_CODE_NEW_INIT=1`) can scaffold CLAUDE.md, skills, and hooks together.
