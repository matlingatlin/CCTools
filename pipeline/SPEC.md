# The Self-Playing Piano — master spec

The complete system: a self-improving talent factory. **Talents** = skills, hooks,
subagents, agents, commands. The **brain** decides the next step and grows as new
useful talents are found. This is the authoritative description of every part,
function, and step.

## Ground principles (everywhere)
- All state in git (survives ephemeral container reclaim) + a heartbeat that
  re-wakes the piano if the session goes idle.
- The coordinator commits; track-agents only produce (no parallel git conflicts).
- Security gate always on: nothing third-party installed without review; auto-run
  / unaudited hooks, obfuscated code, external CLI installs are stopped.
- Human gate ∝ autonomy: the more self-running, the stricter the human
  confirmation before irreversible steps (`loop-design-check` principle).

## Part 1 — Knowledge (the starting point)
1. Read official Claude Code docs (skills, hooks, subagents, MCP, plugins,
   workflows, memory).
2. Distill into knowledge notes with source + date + status.
3. This is the brain's reference for how to build, test, and run talents.

## Part 2 — Query engine (`research-scout`)
4. From the knowledge, derive dynamic search terms (academic + "top 10" + practitioner).
5. Derive sources: universities, researchers, tech companies, known profiles
   (e.g. Boris Cherny), GitHub orgs.
6. Derive entities: people/companies/institutes/universities, with a credibility tier.
7. Domain scope: **core (default, always filled in)** = AI, ML, LLMs, agents,
   software engineering, data, IT/infra, tooling, developer workflows, NLP, prompt
   engineering. **Bonus / connected (only when it yields a real talent)** =
   psychology, cognition, linguistics, design, decision science.
8. Output feeds the frontier queue and is itself a reusable talent.

## Part 3 — Ingestion per source type (source-methods)
9. GitHub repo → clone, walk, (Graphify code-only for big repos), sort per type.
10. Research/PDF → arXiv/Semantic Scholar/ACL/OpenReview (open access), `pdf` skill,
    read in order: abstract → method → results → limitations.
11. Profiles → repo / site / clip / post, fetch in the form presented.
12. "Top 10" sites → google the term, walk the hits, fetch, sort.
13. Documents → `docx`/`pptx`/`xlsx` per format; web → WebFetch/Playwright.
14. Each source type has a fixed method + note template + credibility/recency
    filter (cross-reference, prefer last 12 months, flag single-source).

## Part 4 — Two-tier database
15. Tier 1 — Intake (raw): Classify → Deduplicate → Store → Index per source type
    (`knowledge-ops` pattern).
16. Tier 2 — Talent library (tested): only finished, tested talents
    (`.claude/skills`, `.claude/agents`).
17. Promotion gate raw → talent via `unified-memory` format (scope,
    `trust:unreviewed`, recall-before-write).

## Part 5 — The gates (four judgments before anything becomes a talent)
18. Dedup guardian — prospective: new candidate compared against the whole library
    (name + description + function). Near match → merge/reject/flag.
19. Reuse-first: search our own catalog + talents for existing help (code/architecture)
    before building new.
20. Talent-worthiness: "does this fill a function we do NOT already have?" No → stays
    a knowledge note, becomes no talent.
21. Security: read the code; no network/credential calls, no auto-run unaudited hooks.
    Unsafe → sandbox or skip.

## Part 6 — The factory (build/adopt/test)
22. Pipeline engine (`orch-pipeline` pattern): gated harvest → build/adopt → test →
    store, with two commit gates.
23. Two production modes: (a) adopt an existing talent from a repo; (b) author a new
    talent from a research insight.
24. Talent routing (`plan-orchestrate` pattern): for job X, pick talent Y (a routing
    table that grows).
25. Test: baseline-vs-with-talent on a planted-defect scenario; discipline talents
    pressure-tested.
26. Quality loop (`gan-style-harness` + `santa-method`): generator builds, ruthless
    evaluator fails it until a threshold is met.
27. Parallel fan-out (`parallel-execution-optimizer`): build many talents at once
    without write-surface collisions.
28. Adopt winners into tier 2; log the verdict in the catalog.

## Part 7 — The librarian (curator of database 2)
29. Inventory + deep-read each talent (`deep-reading`) — understand what it really does.
30. Re-test (`eval-harness`/`santa-method`) — does it do what it claims? Flag
    broken/stale.
31. Announce better — sharpen the description (`writing-skills`: triggers only, right
    keywords, within the listing budget pinned in `pipeline/CONSTANTS.md`) so the right talent triggers.
32. Check the ones lying close together — similarity clustering; overlapping
    descriptions → differentiate or merge so triggering is unambiguous
    (ties to `context-budget` listing budget).
33. Sort by conclusions/search-terms — group per function/domain; update the routing
    table + `INDEX.md`.
34. Dedup guardian — retroactive: pairwise scan the whole library, cluster
    near-duplicates, propose keep/merge/differentiate (never auto-delete).

## Part 8 — The brain / orchestrator (autonomous operation)
35. Orchestrator reads the frontier + DB state and decides the next action (which
    source, which talent to build, which search term).
36. Loop safety (`loop-design-check`): decidable stop-condition, anti-spin damping,
    Goodhart boundary, human switch.
37. Recovery (`continuous-agent-loop` pattern): freeze → audit → narrow scope → replay.
38. Producer→consumer cadence: run one, feed, run next — always something to consume
    (T3 feeds T4 feeds the factory).
39. Runs until you say stop; heartbeat + git-state make it survivable.

## Part 9 — Self-improvement (feedback loops)
40. T4's findings sharpen T3's next search terms.
41. The piano eats its own dog food: runs adopted talents (deep-reading,
    research-methodology, skill-scout, eval-harness, santa-method, context-budget…)
    on its own work.
42. A new useful talent → wired into the routing table → the brain gets better at
    running itself.
43. A proven harness solution → promoted to a permanent talent (skill extraction).

## Part 10 — Control & observability
44. `STATUS.md` the brain updates each wave — so "is anything happening?" is one line.
45. Human gates: auto-sharpen descriptions (low risk, allowed) but ask you before
    merge/delete/irreversible (high risk).
46. Everything commits continuously to `skills-repo`; nothing lives only in a session.

## The chain, in one line
knowledge → query engine (terms/sources/profiles) → ingestion per source type →
intake DB → four gates (dedup, reuse-first, talent-worthiness, security) → factory
(build/adopt/test) → talent library → librarian (test/understand/announce/cluster/
dedup) → orchestrator runs it all in a safe loop → everything feeds back and makes
the brain sharper.
