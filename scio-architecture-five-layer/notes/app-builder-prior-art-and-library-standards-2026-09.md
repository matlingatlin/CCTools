---
title: AI app builder prior art and library standards, 2026-09 — what competitors ship, and the two shapes a library should adopt (shadcn registry-item, DTCG 2025.10)
sources:
  - url: https://ui.shadcn.com/schema/registry-item.json
    note: "The JSON Schema itself, read in full by script (required fields, property list, type enum). Raw: knowledge/raw/web-2026-09-08-app-builder-prior-art/shadcn-schema-registry-item.json"
    fetched: 2026-09-08
  - url: https://ui.shadcn.com/docs/registry/registry-item-json
    note: "The docs page for the item shape; property descriptions and the type table. Raw: shadcn-registry-item-json.html"
    fetched: 2026-09-08
  - url: https://ui.shadcn.com/docs/changelog/2026-05-registry-include
    note: "The May 2026 changelog entry: registry include (composition) and registry validate. Raw: shadcn-changelog-2026-05-registry-include.html"
    fetched: 2026-09-08
  - url: https://www.w3.org/community/design-tokens/category/status-updates/
    note: "The DTCG status-update feed; the 2025-10-28 post announcing the first stable specification 2025.10. Raw: dtcg-status-updates.html"
    fetched: 2026-09-08
  - url: https://lovable.dev/guides/bolt-vs-replit-vs-lovable
    note: "Vendor comparison page (Lovable's own); the Replit Agent 4 feature list (parallel tasks, Design Mode, checkpoint rollback) appears here and in trade press. Search-result excerpt only; not fetched raw. Secondary."
    fetched: 2026-09-08
  - url: https://blog.replit.com/agent-4
    note: "404 'Page not found' on 2026-09-08 through the session proxy; no primary source for the Agent 4 claims was reached."
    fetched: 2026-09-08
status: verified
tags: [app-builder, prior-art, competitors, lovable, replit, v0, shadcn, registry, design-tokens, dtcg, library, standards]
related: ["[[third-party-landscape]]", "[[build-evidence-tooling-2026]]", "[[evidence-artefact-schemas-2026-09]]", "[[production-site-checklist]]"]
---

# AI app builder prior art and library standards, 2026-09

**Why this note exists.** Scio's 2026-09-08 brainstorm ran its prior-art gate over three domain
words — *AI app builder*, *continuous delivery / incremental preview*, *component library /
design tokens*. The gate found two shapes worth adopting outright and a competitor field that
differs from Scio on evidence rather than on features. The measured parts are below with a
verdict per claim; the competitor part is what secondary sources repeat, graded as such.

## 1 · The library item shape: shadcn `registry-item.json` — MEASURED

Read from the schema file itself, 2026-09-08.

1. **Only `name` and `type` are required.** `"required": ["name", "type"]`. — MEASURED
2. **The item's properties** (22): `$schema`-less in the schema object; `author`, `baseColor`,
   `categories`, `css`, `cssVars`, `dependencies`, `description`, `devDependencies`, `docs`,
   `envVars`, `extends`, `files`, `font`, `iconLibrary`, `meta`, `name`, `registryDependencies`,
   `style`, `tailwind`, `theme`, `title`, `type`. The docs page additionally lists `$schema`
   with the value `https://ui.shadcn.com/schema/registry-item.json`. — MEASURED
3. **`type` enum** (12): `registry:lib`, `registry:block`, `registry:component`, `registry:ui`,
   `registry:hook`, `registry:theme`, `registry:page`, `registry:file`, `registry:style`,
   `registry:base`, `registry:font`, `registry:item`. — MEASURED
4. **Each file** is `{ path, content?, target?, type }`, and the per-file `type` enum is the same
   list minus `registry:font` (11 values). — MEASURED
5. **Composition and validation exist since May 2026:** a root `registry.json` may `include`
   other registry files; `shadcn build` "resolves included registries and writes a flattened
   registry.json without include"; `shadcn registry validate` checks "the root registry.json,
   included registry files, item schema errors, duplicate item names, include rules, and local
   item file paths" in one run. — MEASURED (changelog page, quoted)
6. **Private GitHub registries** are supported as of August 2026 and items are reachable by
   agents through an MCP server. — REPEATED (search-result excerpt; the changelog page for
   August was not fetched)

**What it means for a library of feature parts.** A Scio library part can be a
`registry:block` with `files[]`, `dependencies`, `registryDependencies` and `cssVars`, and a
whole tenant or Scio-curated library can be a composed registry validated by a command that
already exists. The *Contract* Scio matches parts by (predecessor ADR-0013) is not in this shape
and would live in `meta` or beside it — the shape carries files and dependencies, not
acceptance.

## 2 · The token shape: W3C DTCG Design Tokens Format Module 2025.10 — MEASURED

7. **First stable version 2025.10, announced 2025-10-28.** Quoted from the status feed: "The
   Design Tokens Community Group today announced the first stable version of the Design Tokens
   Specification (2025.10), marking a milestone for design systems teams". Post timestamp
   `2025-10-28T17:04:52+00:00`. — MEASURED
8. **Shape** `$value` / `$type` per token and references by path; tool support (Figma, Penpot,
   Style Dictionary, Terrazzo, Tokens Studio). — REPEATED (from practitioner posts in the
   search results; the specification text itself was not re-fetched on 2026-09-08 — the
   2026-08-26 brainstorm skill source scan already adopted it)

## 3 · The competitor field — REPEATED, dated 2026-09-08

9. **Replit Agent 4** (trade press dates it March 2026): parallel task execution, a "Design Mode"
   for interactive mockups, checkpoint-based rollback; Replit combines the agent with a full
   IDE. — REPEATED (Lovable's comparison page and three trade-press roundups agree; Replit's
   own page 404'd)
10. **Lovable**: conversational refinement loop, GitHub sync, deployable apps with auth and
    database. **Bolt**: fastest prompt-to-preview, browser-only. **v0 / Vercel JSON Render**:
    a catalog of allowed components bound to a registry, with UI streamed from the model. —
    REPEATED
11. **No standard** exists for per-checkpoint preview of a generated app; the closest are the
    Continuous Delivery principle, CD products adding human checkpoints per stage, and the
    Vercel AI SDK's `streamObject` partial-object rendering. — REPEATED (absence of evidence
    from two searches; not proof of absence)
12. **Quality is judged from outside**: 2026 roundups score builders on "AI generation quality"
    and "real-app output"; none of the roundups or vendors describe per-build evidence handed to
    the buyer. — REPEATED

**Verdicts used by the gate.** AI app builder → *differs* (evidence per build, priced reuse,
developer-class gates are absent everywhere found; "a design mode", "checkpoints" and "stream
the UI" alone reinvent). Continuous delivery → *extend*. Library / tokens → *adopt* (rows 1–7).

## 4 · Facet prior art from the same brainstorm — REPEATED, search-summary level, dated 2026-09-08

Twenty-two facet searches ran after pooling (one per distinct facet claimed by an idea). None of
these pages was fetched; each row is what a search summary said, kept so the next run does not
search again from zero. Every row is REPEATED.

13. Per-feature LLM cost attribution is 2026 practice: Braintrust's playbook, Helicone, Langfuse,
    OpenMeter, Portkey, Vantage; "tokens per feature" as an R&D metric.
14. Elicitation with LLMs: LLMREI (arXiv:2507.02564, LLM-run interviews), Elicitron (simulated
    user agents), GUIDE (arXiv:2502.21068, GUI prototyping); a prototype's usage trace as the
    elicitation answer itself was not found.
15. Content-addressed build caches (Gradle/Bazel keys from task class + inputs); a spec-driven
    codegen study (arXiv:2601.03878) stores artefacts by content hash.
16. Spec-driven development is mainstream in 2026 (Kiro, GitHub Spec Kit, BMAD); "spec is the
    source of truth, code is derived".
17. IEEE 828-2012 defines baselines, change control, status accounting, audits.
18. FAA AC 20-148 (2004) is the reusable-software-component certification model: certify once,
    conformity per use.
19. Evidence provenance for agents: a survey of evidence tracing in LLM agents (arXiv:2606.04990);
    attesting LLM pipelines (arXiv:2603.28988); promotion gates verifying Sigstore + in-toto.
20. Bandit compute allocation across LLM trajectories: BaSE (arXiv:2605.29268, +12.3% mean
    fitness over the strongest island baseline, as summarised); cost-aware MAB LLM selection
    (arXiv:2505.13355); test-time compute bandits (arXiv:2506.12721).
21. Pact consumer-driven contracts + can-i-deploy as the pre-adoption compatibility check.
22. Best-of-N code selection: Top Pass (arXiv:2408.05715), CodeT, DOCE (arXiv:2408.13745); "Beyond
    pass@k" (arXiv:2608.14711) on reliability and security of agentic generation.
23. Agentic pentest in 2026: XBOW topped HackerOne's US leaderboard in 2025; Wiz Red Agent in
    public preview from 2026-04-22; FireCompass.
24. Synthetic users: Agent A/B (CHI 2026), PerceptUI (arXiv:2606.05697), UXAgent, SimUser; the
    documented caveat that synthetic users are too agreeable.
25. Gartner's LCAP definition: model-driven tools + prebuilt component catalogs + GenAI - the
    thing a "never generate code" idea reinvents.
26. Single-pass generation: Compiled AI (arXiv:2604.05150), Self-Spec (disambiguate before
    generating), Sonar's "loop engineering without verification is automation".
27. LLM Gherkin generation (arXiv:2607.01980, SEET 2026): JSON-constrained output, 100% structural
    validity, 94.3% semantic coverage on PURE SRS documents, as summarised.
28. Requirements ambiguity detection with LLMs, industrial study (ICSME 2025): +20.2% with ten
    in-context demonstrations; multiple independent readers as a stop rule was not found.
29. Visual regression baselines (Percy, Chromatic) and token-aware VRT; a lock file of approved
    elements in the owned repo was not found.
30. Clean-room rebuilds: Buildkite cleanroom, RepoLaunch (arXiv:2603.05026), Maven reproducible
    builds guidance.

**Neighbours.** The evidence side of the same build — CTRF, SARIF, in-toto — is measured in
[[evidence-artefact-schemas-2026-09]] and surveyed in [[build-evidence-tooling-2026]]; the wider
field of registries and token tools is tabulated in [[third-party-landscape]]; what a shipped site
must satisfy is in [[production-site-checklist]].

## What this note does not know
- Whether Replit's Design Mode produces artefacts a build consumes, or only pictures.
- Pricing of any competitor (not searched; prices are looked up when a decision needs them).
- Whether a `registry:block` can carry a test file that the shadcn CLI installs (the `files`
  type enum has no test kind; `registry:file` is the likely carrier — untested).
