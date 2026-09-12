---
title: Build-evidence tooling, 2026 — the standards and tools that exist for what a verified build must show
sources:
  - url: https://ctrf.io/
    note: "'An Open Standard for JSON Test Reports.' Raw: knowledge/raw/web-2026-09-03-harness-and-evidence/ctrf-io.html"
    fetched: 2026-09-03
  - url: https://pythonspeed.com/articles/verified-fakes/
    note: "'Running the same tests against both implementations ensures both versions behave the same way'. Raw: pythonspeed-verified-fakes.html"
    fetched: 2026-09-03
  - url: https://arxiv.org/abs/2503.24260
    note: "MaintainCoder: Maintainable Code Generation Under Dynamic Requirements — submitted 31 Mar 2025, v3 29 Sep 2025. Title and dates verified; the benchmark name and task count come from a search summary only. Raw: arxiv-2503.24260-abs.html"
    fetched: 2026-09-03
  - url: https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds
    note: "Fetched as a navigation shell (no article body); existence and the OIDC-per-provider pages verified, the Sigstore/SLSA mechanics not. Raw: github-artifact-attestations.html"
    fetched: 2026-09-03
  - url: https://atlasgo.io/blog/2025/10/v038-analyzers-pii-and-migration-hooks
    note: "Fetched as a navigation shell; the 'migrate lint is Pro-only from v0.38' claim is from a search summary and unverified. Raw: atlas-v038-blog.html"
    fetched: 2026-09-03
  - note: "Search-summary-only sources (not fetched raw, listed so the gap is visible): SARIF 2.x (OASIS), in-toto attestation + SLSA provenance, Turborepo/Nx caching docs, OpenVEX spec, Infracost, cruft, dependency-cruiser and ArchUnitTS, GitHub Spec Kit, Neon+Atlas branch rehearsal, agentic pentest tools (Escape, XBOW), risk-exception-with-expiry (GRC), BYOC (Nuon, Northflank), SWE-EVO 2512.18470, SWE-CI 2603.03823. Each is named in Scio's brainstorm run file docs/next/ideas/2026-09-03-product-improvement.md with its link."
status: verified
tags: [evidence, testing, attestation, provenance, ctrf, sarif, slsa, in-toto, caching, migrations, fakes, benchmarks, app-builder]
related: ["[[agent-harness-principles-2026]]", "[[architecture-evidence]]", "[[agent-builder-prior-art]]", "[[production-site-checklist]]", "[[typescript-stack-scan-2026-09]]", "[[evidence-artefact-schemas-2026-09]]", "[[app-builder-prior-art-and-library-standards-2026-09]]"]
---

# Build-evidence tooling, 2026

Written 2026-09-03 from the prior-art gate of Scio's first brainstorm run (`docs/next/ideas/
2026-09-03-product-improvement.md` in Scio, 20 facet searches). The question the run kept
asking was *does a standard or a tool already exist for this?* — because this project has
twice invented what existed (a coverage percentage where ISO 29148 was; a token shape where
W3C DTCG was). This note is the answer per facet, graded by how much of it was actually read.

## Claims

| # | Facet | What exists | Verdict on the claim | How read |
|---|---|---|---|---|
| 1 | Test results as a machine-readable artefact | CTRF — "An Open Standard for JSON Test Reports" | REPEATED (site's own description) | raw, landing page |
| 2 | Static-check results as an artefact | SARIF 2.x (OASIS) | REPEATED | search summary only |
| 3 | Provenance of a build | in-toto attestation carrying a SLSA provenance predicate; GitHub artifact attestations sign them with a Sigstore certificate obtained via the workflow's OIDC token, verified with `gh attestation verify` | REPEATED; the GitHub page fetched was a shell — mechanics unverified today, though Scio's `docs/next` LAYER-E/F already adopt in-toto/SLSA from an earlier fetch | shell + summary |
| 4 | A fake that cannot lie about production | verified fakes / contract tests: "Running the same tests against both implementations ensures both versions behave the same way" | REPEATED (a practice, argued not measured) | raw |
| 5 | Replaying an unchanged check instead of re-running it | Turborepo and Nx task caching key on an input hash and replay the cached output and logs | REPEATED | summary |
| 6 | Maintainability of generated code under changing requirements | MaintainCoder (arXiv 2503.24260) — an offline benchmark of models, not a per-build gate; SWE-EVO and SWE-CI likewise | REPEATED; title and dates verified, the "500+ tasks" figure not | raw abstract page (title, dates) |
| 7 | Destructive schema changes caught before production | Atlas migrate lint analyzers; rehearsal on a Neon branch from production; shadow database from a snapshot | REPEATED; the Pro-only-from-v0.38 licensing claim unverified | shell + summary |
| 8 | Recall of a shipped component to downstream consumers | OpenVEX status statements (affected / not_affected / fixed / under_investigation) beside an SBOM | REPEATED | summary |
| 9 | Cost printed before deploy | Infracost, from IaC in pull requests | REPEATED | summary |
| 10 | Template drift in generated projects | cruft check / update (stored template hash, exit 1 in CI, three-way update) | REPEATED | summary |
| 11 | Import-boundary fitness functions in TypeScript | dependency-cruiser; ArchUnitTS | REPEATED | summary |
| 12 | Regenerate from an edited spec | GitHub Spec Kit (MIT) | REPEATED | summary |
| 13 | Authorization attacks as a PR gate | agentic pentest tools that do IDOR/BOLA (Escape, XBOW, Snipe) | REPEATED | summary |
| 14 | Accepting a known gap for a bounded time | GRC risk-exception pattern: owner, justification, compensating control, expiry, closure | REPEATED | summary |

## What it means here

- **Adopt, do not author:** an evidence report whose gate artefacts are CTRF and SARIF, whose
  provenance is an in-toto/SLSA statement, and whose replay is a Turborepo-shaped input-hash
  cache. A bespoke schema for any of the three would be the third reinvention in this project.
- **The per-build gap is real (claim 6):** every maintainability benchmark judges a model
  offline; nothing found runs a requirement-change test on the buyer's own app as a gate.
  That is the facet Scio's "week three inside the build" idea occupies.
- **Claim 4 is the mechanism behind the predecessor's habit-2 fix** (a test double stricter
  than production hid a cross-tenant read): run the generated suite against the double and
  against the real database with RLS, diff per test, cull the double that disagrees.
- **Fourteen facets, two raw pages, two shells, ten summaries.** Anything here that drives a
  decision must be read in full first; this note records what exists, not that it works.

## What is open

- SARIF, OpenVEX, Turborepo, cruft, dependency-cruiser, Spec Kit, Infracost: not fetched raw.
- The Atlas licensing change (claim 7) and the GitHub attestation mechanics (claim 3): the
  fetched pages were navigation shells; re-fetch with a browser or the docs' raw source.
- MaintainCoder's task count and change taxonomy: PDF not read.

## Added 2026-09-03 (later the same day)
The versions of `dependency-cruiser`, Biome, Vitest and Turborepo this note's facets would be pinned to, measured against the registry, are in [[typescript-stack-scan-2026-09]].

## Added 2026-09-06
Claims 1, 2 and 3 were REPEATED here; what each format REQUIRES was then read from the schema
files themselves (ctrf@0.3.0's bundled schema, SchemaStore's SARIF 2.1.0, the in-toto Statement
v1 spec, the SLSA Provenance v1 page) and recorded per field, MEASURED, in
[[evidence-artefact-schemas-2026-09]]. The SARIF "summary only" and the "GitHub page was a shell"
gaps in *What is open* are half closed: SARIF's required fields and enums are now measured; the
GitHub signing mechanics are still unread.

## Added 2026-09-08
The library-side counterpart — the registry item shape a feature part can take and the token format it should use — is measured in [[app-builder-prior-art-and-library-standards-2026-09]].
