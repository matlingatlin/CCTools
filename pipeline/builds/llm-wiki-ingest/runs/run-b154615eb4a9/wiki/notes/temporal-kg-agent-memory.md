---
title: Temporal knowledge-graph agent memory (Graphiti/Zep)
sources:
  - url: https://github.com/getzep/graphiti
    fetched: 2026-08-27
status: verified
tags: [memory, knowledge-graph, temporal, agents, architecture]
related: ["[[graphify-assessment]]", "[[mcp]]", "[[llm-wiki-pattern]]", "[[third-party-landscape]]"]
---

# Temporal knowledge-graph agent memory — Graphiti

Harvested wave 7. Graphiti (`getzep/graphiti`, the engine behind Zep) is a framework for
**temporal** context graphs for AI agents. 0 talent surfaces (Python framework, not a
skill/agent/hook) → not adopted; captured as a memory-architecture reference.

## The idea worth knowing
Unlike a static KG, a temporal context graph tracks **how facts change over time**:
- **Bi-temporal model** — every fact carries both when it was true in the world and when
  the system learned it; queries can ask "what is true now" and "what was true then".
- **Provenance** — facts link back to the source data that asserted them.
- **Incremental updates** — new interactions update the graph **without recomputing** the
  whole thing (contrast batch re-embedding of a vector store).
- **Hybrid retrieval** — semantic + keyword + graph traversal combined, not chunk-similarity alone.
- **Ontology** — supports both prescribed and learned structure.

## Honest fit for us
- **Not adoptable as our infra:** Graphiti needs a running **graph DB backend** (Neo4j /
  FalkorDB, via Docker) + an LLM for extraction — the same "needs a live datastore an
  ephemeral container reclaims" problem we flagged for Zep in [[graphify-assessment]].
  Our model is git-native. So this is a **reference**, not a talent or our datastore.
- **It ships an MCP server** (`mcp_server/`) exposing the memory over MCP — an MCP-shelf
  candidate **if** a future project can host the DB backend. Note the backend caveat.
- **What we take:** the *concepts* (bi-temporal facts, provenance, incremental-update,
  hybrid retrieval) inform how `unified-memory` structures durable handoffs — e.g. record
  when a decision was made vs when it was superseded, and keep provenance to the commit.

## Contrast (memory tooling seen so far)
- **Graphify** — code → KG, on-device, git-committable, no server. Our pick for code maps.
- **Graphiti/Zep** — evolving *fact* memory, DB-backed, temporal. Powerful, but a server.
- **Our KB** — markdown + wikilinks in git; hand-curated, deterministic, persistent.
Pick by need: code navigation → Graphify; our knowledge → wikilinks; temporal fact memory
at scale with a hostable DB → Graphiti.

## gbrain — Garry Tan's agent brain (added 2026-09-02)

Source: `https://github.com/garrytan/gbrain` README, fetched 2026-09-02, plus a 74-second
video whose claims are graded here. MEASURED from the README unless marked.

- **What it is:** a "brain layer" for agents — "synthesis, graph traversal, and gap
  analysis" over your own markdown, not keyword search. MIT. Open-sourced April 2026
  (REPEATED; search results), by Garry Tan, President and CEO of Y Combinator (the video's
  "CEO of Y Combinator" is right).
- **Storage:** git repo of markdown is the system of record; PGLite (Postgres 17 in WASM,
  zero config, ~50K pages) by default; Postgres + pgvector for shared or large deployments.
- **Auto-linking — the video's "every note gets auto-linked to the people and projects it
  touches":** MEASURED. "Every page write extracts entity refs and creates typed edges
  (`attended`, `works_at`, `invested_in`, `founded`, `advises`) with zero LLM calls."
- **"Every night it cleans itself up and fills in its own gaps":** MEASURED. A "dream
  cycle" of nightly cron jobs to "ingest, enrich, and consolidate" — dedup, citation
  fixes, salience scoring.
- **"Reads all the notes and writes back one clear answer with sources":** MEASURED.
  `gbrain search` is raw retrieval; `gbrain think` is "synthesized answer across the
  results with explicit citations" plus gap analysis.
- **"Connect it to any agent — Claude, Codex, Hermes, OpenClaw":** MEASURED. Claude Code,
  Codex, OpenClaw, Hermes, and any MCP client (Claude Desktop, Cursor, Perplexity,
  ChatGPT); 100+ operations exposed as MCP tools (REPEATED). Install is agent-driven:
  paste `BOOTSTRAP_FOR_AGENTS.md` (Codex/Claude Code) or `INSTALL_FOR_AGENTS.md`
  (OpenClaw/Hermes) into the agent.
- **"Obsidian brains are a graveyard / pointless":** opinion, not a claim. The honest
  contrast is below.
- **Maturity (REPEATED, vectorize.io review):** v0.30 with frequent breaking changes.

**Contrast, extended:** gbrain sits between Graphiti and our KB. Like ours, git-markdown is
the record; unlike ours, it adds a local DB, embeddings, a synthesis command and a nightly
consolidation pass — the pieces `unified-memory` stores by hand and
`memory-provenance-separation` reasons about by hand. Its typed-edge extraction with zero
LLM calls is the one mechanism worth copying into our wikilink KB: neighbours named both
ways, structurally, rather than by the "make each neighbour name back" rule that this repo
enforces by convention. Not adopted: it is an install (DB, cron, MCP server) and our fourth
gate keeps auto-running installers out; a method note, not a talent.

## Orbit — a hosted memory layer with ratified facts and conflict flagging (added 2026-09-02)

Sources: `https://orbitagents.xyz/` fetched 2026-09-02; search results; a 2m29s video
("Obsidian vs Orbit agents") by one of the founders, transcribed 2026-09-02. Graded.

- **What (MEASURED from the site):** "a shared memory layer for AI agents"; "one dashboard
  for all your AI agents"; connects to Claude, Codex, ChatGPT, Cursor, Gemini via **one MCP
  command**; "Orbit Cloud" stores "agents, memory & data". Maker: Fraima (contact
  jonatan@fraima.com). "Free to start"; **no prices on the site**; "$8/mo" is a third-party
  review's figure (REPEATED). **No open-source component or GitHub link.** Self-hosting not
  mentioned.
- **The three mechanisms, verbatim:** "Facts you ratify are the ground truth. No agent can
  quietly overwrite them." · "Every fact carries its receipts — Source, agent, confidence,
  reasoning — attached to every entry." · "When two agents contradict each other, Orbit
  flags it for you to resolve."
- **Video claims graded.** "Obsidian treats all knowledge equally" — category error:
  Obsidian is a markdown browser with a graph view, not a memory system, so it "treats"
  nothing; the honest comparison is with gbrain (above) or claude-mem. "Saving tokens more
  than Obsidian" — no measurement. "24/7 continuously syncing … every conclusion the AI
  makes in all your chats" — that is the product's design, and it is also the fourth gate's
  concern: every session's conclusions copied to a third-party cloud by default, with no
  self-host option shown.

**What is worth taking.** The three mechanisms are, one-to-one, the
`memory-provenance-separation` skill: user-asserted (ratified) outranks system-observed
(agent-filed); every row stamped with origin, confidence and as-of; a contradiction is
surfaced, not merged. Orbit is that skill sold as a SaaS with a dashboard. Not adopted:
hosted, closed, memory leaves the machine. The design validation is real; the tool is not for
us.
A second Orbit video the same day adds "a beautiful 3D knowledge graph", "pre-built agents
with tools" and "a full company where you are the CEO" — feature marketing, nothing
checkable beyond the site's own list; "Obsidian is trash" is the same category error.

**Related talent (a skill, not a note):** `unified-memory` stores and retrieves durable agent state; this note is about temporal knowledge graphs as memory.
