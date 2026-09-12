---
title: Temporal knowledge-graph agent memory (Graphiti/Zep)
sources:
  - url: https://github.com/getzep/graphiti
    note: "README re-read 2026-09-08 at the raw path. Backend requirements and the structured-output caveat below are from it."
    fetched: 2026-09-08
  - url: https://pypi.org/pypi/graphiti-core/json
    note: "The release history, read 2026-09-08. 193 releases, Apache-2.0, current 0.30.1 uploaded 2026-09-01. This is the surface that settles the maturity claim, and it settles it against the review."
    fetched: 2026-09-08
tags: [memory, knowledge-graph, temporal, agents, architecture]
related: ["[[graphify-assessment]]", "[[mcp]]", "[[llm-wiki-pattern]]", "[[third-party-landscape]]"]
raw:
  - knowledge/raw/untried-surfaces-2026-09-08/pypi.org_pypi_graphiti-core_json.json
  - knowledge/raw/untried-surfaces-2026-09-08/raw.githubusercontent.com_getzep_graphiti_HEAD_README.md.md
  - knowledge/raw/untried-surfaces-2026-09-08/raw.githubusercontent.com_garrytan_gbrain_HEAD_README.md.md
  - "the Orbit section predates the raw layer (fetched 2026-09-02); url + fetched are its only provenance"
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
- **Not adoptable as our infra, and the 2026-09-08 re-read makes the case stronger, not
  weaker.** The README's Requirements section, verbatim: Python 3.10+, **Neo4j 5.26 / FalkorDB
  1.1.2 / Amazon Neptune + OpenSearch Serverless / Kuzu 0.11.2 (marked deprecated)**, and an
  **OpenAI API key** — "Graphiti defaults to OpenAI for LLM inference and embedding". So it is a
  live datastore *and* a paid third-party dependency per write, which is the "needs a datastore
  an ephemeral container reclaims" problem we flagged for Zep in [[graphify-assessment]], plus a
  second one we had not recorded. Licence **Apache-2.0** (PyPI metadata, MEASURED).
- **A constraint worth carrying even though we are not adopting it.** The README's own warning:
  Graphiti "works best with LLM services that support Structured Output … using other services
  may result in incorrect output schemas and ingestion failures. This is particularly
  problematic when using smaller models." Any future extraction step of ours that leans on a
  local or routed model inherits exactly that failure mode —
  [[model-agnostic-agent-harnesses]] holds the arms it would run on.
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
  ChatGPT); **100+ operations exposed as MCP tools — MEASURED 2026-09-08 against the README as it
  stood that day**, verbatim: "GBrain exposes nearly all of its 100+ operations as MCP tools
  (stdio and HTTP; a handful of local-only ops stay CLI-side) — or exactly the seven memory verbs
  with `--surface verbs`".

  > **That sentence no longer exists at the source (re-read 2026-09-11).** The README was
  > substantially repositioned — from "the brain layer your AI agent has been missing" and a
  > personal-agent bootstrap, to "add GBrain memory to the agent you already use" — and the
  > quoted line went with it. The current README states **no MCP tool count at all**: neither
  > "100+ operations" nor "nearly all of its" appears anywhere in it. Nearby claims survived
  > (`gbrain think`, `v0.48.4`, `longmemeval` are all still there), so this is a targeted removal
  > rather than a wholesale rewrite of the facts.
  >
  > **The claim is not refuted and it is not re-dated.** It is still verifiable, because the
  > bytes it was read from are held at
  > `knowledge/raw/untried-surfaces-2026-09-08/raw.githubusercontent.com_garrytan_gbrain_HEAD_README.md.md`
  > — which is the entire argument for keeping a raw layer: a MEASURED verbatim quote outlives
  > the page it was taken from. What changed is its *future*: a reader cannot now confirm it
  > against the live README, so it must never be cited as current capability without a re-check.
  > A vendor dropping a number is weak evidence about the number and strong evidence about the
  > vendor's positioning.

  Install is agent-driven:
  paste `BOOTSTRAP_FOR_AGENTS.md` (Codex/Claude Code) or `INSTALL_FOR_AGENTS.md`
  (OpenClaw/Hermes) into the agent.
- **"Obsidian brains are a graveyard / pointless":** opinion, not a claim. The honest
  contrast is below.
- **It now ships its own eval, and reports it more carefully than most (MEASURED 2026-09-08 from
  the README).** `gbrain eval longmemeval` runs the public LongMemEval benchmark against its
  hybrid retrieval: **93.40% (439/470)** strict `recall_all@5` with the reranker off, at
  v0.48.4.0, LongMemEval-S cleaned Sept-2025 revision, k=5, **single run**, 470 scored after the
  30 abstention questions are dropped as the official scorer does. What makes it worth citing is
  the sentence beside it: strict `recall_all@5` requires *every* gold session in the top 5, loose
  any-hit needs one, and **300 of the 470 questions need two or more sessions** — so the two
  metrics are not close, and the README says which it is reporting. Compare that with the
  benchmark practice graded in [[claude-code-ecosystem-plugins]]. Still one run and the author's
  own harness, so n=1 by our bar.
- **"Open-sourced April 2026" stays REPEATED, and now for a stated reason:** the README was read
  in full on 2026-09-08 and **carries no release date at all** (the only 2026-04 string in it is
  an example note filename). Search results remain the only source.
- **Maturity — the review's claim is filed under the wrong project, and half of it is now
  false (MEASURED 2026-09-08).** "v0.30" is **graphiti-core's** version, not gbrain's: PyPI has
  `graphiti-core` at exactly **0.30.1**, and gbrain's own README puts it at **v0.48.4**. So this
  bullet belongs to the Graphiti section above; it is left here, corrected, rather than moved
  silently, because the mis-filing is the more useful record.

  *Re-read 2026-09-11: `graphiti-core` is now **0.30.2** (PyPI release index, watched). The
  version moved and the finding did not — the argument never rested on the digit but on the two
  projects being different, which a one-patch bump cannot change. The number is updated anyway,
  because a stale figure cited as MEASURED teaches a reader to distrust the ones that matter.*

  **CORRECTED the same day, and the correction is the better lesson.** The first version of this
  line cited "gbrain ships on npm at 1.3.1" as the second half of the evidence. That is a
  **different project**: the npm package `gbrain` is `stormcolor/gbrain`, "GPU Javascript Library
  for Machine Learning", created 2018-04-02 and last published 2018-11-15. This project's own
  README carries a warning about exactly that collision — *"GBrain is NOT distributed on npm. The
  npm package named `gbrain` is an unrelated package with no connection to this project … it can
  shadow the real binary on your PATH."* A registry hit on a matching name is not an identity
  check; the conclusion survives on graphiti-core's version alone, but it was reached with one
  leg of borrowed evidence.

  And "frequent breaking changes" **is no longer true** of Graphiti:
  193 releases since 2024-08-27 across 30 minor versions is a fast history, but the cadence
  collapsed — 10 releases in January 2026, 6 in February, then **one per month**, and **two in
  the last ninety days**. A review that was accurate when written now reads as a warning about
  a project that has settled down.

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
