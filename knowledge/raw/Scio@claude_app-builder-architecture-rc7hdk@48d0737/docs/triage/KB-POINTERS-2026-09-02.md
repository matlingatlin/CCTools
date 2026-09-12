# Pointers into the knowledge base — skills-repo notes that bear on Scio

**Date:** 2026-09-02. **Status:** pointers, not copies. Per `docs/PIPELINE.md` §1, a document is not
resolved into two repos by copying it; that is the drift hazard `SKILLS-LIBRARY.md` records. Each row
names where the note lives and what Scio does with it. `scio-db.py build` indexes these once it
takes three repo roots (ADR-0012, level 1); until then this file is the index.

**Location:** `matlingatlin/skills-repo`, branch `claude/hej-f7k1d2`, directory `knowledge/notes/`.
Three rounds landed there today — commits `74f191b`, `f5a3d02`, `1ff8bce` — each with a row in
`pipeline/STATUS.md`. Nothing went to `main`; a merge or PR is needed for that, and that is the
user's call. 34 notes on the branch as of `1ff8bce`.

| Note (commit) | What it establishes | Bears on | Route in Scio |
|---|---|---|---|
| `production-site-checklist.md` (`74f191b`) | 19 code-gradable facts a real site has that a generated one usually lacks (404, meta per page, OG image, favicon, robots, sitemap, alt text, breakpoints, sticky mobile CTA, loading and form-error states, thank-you page, privacy, terms, cookie banner, analytics, real contact address); items 15–17 jurisdiction-dependent; item 20 unknown | Layer C · Build gates; level 3 `evals/` | **Not the Playbook.** `playbook-admission`'s prior question sends anything a script can check to a gate. Eighteen items become deterministic checks in the build's validation set (`validation-evidence` rows, `gate-verdicts` vocabulary); 15–17 become a `needs_look` with the jurisdiction from intake (ADR-0010); the whole list is a `shape` fixture shipped in the app's `evals/` (ADR-0008 level 3). Filed as a finding for the gate list, not copied |
| `loop-engineering-and-fable-prompting.md` (`74f191b`) | how to prompt and bound a loop on this model family | Layer C · the five loops (`TALENTS-CRITICAL-SET` §1) | read before writing the `stop-rule` and `spend-ceiling` hooks; cite, do not paste |
| `model-agnostic-agent-harnesses.md` (`74f191b`, extended twice) | the harness landscape beside the Agent SDK, incl. free endpoints with logging and trial terms | ADR-0004 | the "how we will know it was wrong" row for ADR-0004; the free endpoints are excluded from any build that stores data (ADR-0010) |
| `prompt-patterns-kernel.md` (`74f191b`) | a small set of prompt patterns | Layer B/C prompts | candidate `playbook-admission` input; each pattern pays the four-part test and the token ledger |
| `claude-code-ecosystem-plugins.md` (`1ff8bce`) | the plugin stack graded: claude-mem syncs memories to a vendor by default; `claude-code-setup` is read-only; task-observer does not edit skills; Graft's controlled figure is +42% tokens; OpenMontage AGPL | Level 1 tooling; ADR-0011 | confirms ADR-0011's "no cross-tenant memory": a memory plugin that syncs by default is a tenant leak by design. Nothing adopted |
| `claude-md-and-memory.md` (extended `f5a3d02`, `1ff8bce`) | BASE (PolyForm Noncommercial, unsupported 90% claim); ICM paper states no token number | Level 1; ADR-0011 | reference; BASE's licence excludes it from anything a buyer receives |
| `subagents.md` (extended `74f191b`) | documented limits (15,000-token shared description budget, depth 3, 20 concurrent) and what is undocumented | ADR-0008 subagent design; `catalog-budget` | the description budget bounds how many level-2 subagents can coexist; count before adding one |
| `mcp.md` (extended `1ff8bce`, +AXI) | ten CLI principles for agent-facing tools, two benchmarks judged by the agent model | ADR-0013 (shadcn MCP), ADR-0008 (`mcpServers` per subagent) | reference for how the build's MCP surface is shaped |
| `local-finetuning-layer-streaming.md` (`1ff8bce`) | out of Scio's domain; kept in skills-repo for its public retraction practice | — | none |
| `agent-builder-prior-art.md` (extended `74f191b`, `f5a3d02`) | `addyosmani/agent-skills` (MIT, 25 skills, 91.6k stars, nine name collisions with ours); skills.sh (1.29M installs, vetting = installs + stars + whitelist) | ADR-0013, ADR-0008 §2.3 | reuse-first sources for Playbook entries, through the four gates; `shipping-and-launch` is the engineering twin of the site checklist |
| `research-methodology.md` (extended `1ff8bce`) | the out-of-sample validation ladder: parameter stability, resample every set, cluster the sweep, walk-forward | `testing`, `eval-set-curation` | reference for the intake replay harness's holdout |
| `subagents.md` (extended `74f191b`: the dispatch-harness faults) | four measured faults in an ad hoc harness: shared working directory, arm name in the path, method mounted for every arm, usage never captured (`tokens=None` read as clean) | ADR-0004 (one sandbox per build), ADR-0012 (ledgers: zero = did not report) | both ADRs amended |
| `learning-resources-agents.md` (`74f191b`) | Stanford CS329A, nine public lectures, parts 3 (verification) and 7 (self-improvement) | `literature-review` inputs for the critic and the intake replay | reference |
| `prompt-patterns-kernel.md` (`74f191b`) | KERNEL is a mnemonic with unsupported numbers; its "strip context" conflicts with Fable's "give the reason" and reconciles as strip vagueness, keep purpose | Layer B/C prompts | nothing to adopt; `prompt-refinement` covers it |

**Amendments made to Scio from these notes, same day:** ADR-0004 (Goose as the named alternative;
gateways unsupported; effort fixed per role), ADR-0008 (re-measure every skill on Fable; gates-file
stop rule; scaffolding expiry), ADR-0011 (wikilink edges in the index; zero means did not report;
Graft's controlled figure as the caution), ADR-0013 (skill registries under the same allow-list rule),
`REVIEW-FRESH-EYES` §7 (the premise, tested).

**What this file is not.** It is not a copy of any note and it carries none of their claims as
facts; each claim's source, fetch date and verdict live in the note. When `scio.db` indexes the
branch, this file becomes redundant and should be deleted in the same commit.
