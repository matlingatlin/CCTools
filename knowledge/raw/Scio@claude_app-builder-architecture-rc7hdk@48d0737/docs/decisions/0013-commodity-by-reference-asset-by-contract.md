# ADR-0013 · Commodity by reference, asset by contract: external libraries are referenced through an allow-listed registry, never copied into the library

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** C (build; the library is a step inside it per ADR-0005), B (design tokens)
**Supersedes / relates to:** adopts Layer D forward proposals D-7 and D-1; relates to predecessor ADR-0014 and ADR-0016 (library matches by contract, grows from real builds); ADR-0006 (Slice 3), ADR-0008 (MCP servers per subagent), ADR-0009 (what a buyer receives)

## Context

The user wants to fill the component library from existing code and design libraries. Layer D's
forward view (2026-08-26) walked a shadcn `registry:block` through the fourteen requirements of the
predecessor's own admission gate and found three that only a judgement call could fill —
operations, the file plan, the entity — which the library is designed never to make. *Importing a
visual block collection would not add one matchable entry.* The reviews record that Lovable
already ships design systems, a private registry and cross-project referencing, so inventory is
not a differentiator; evidence is.

Checked 2026-09-02: the shadcn registry format is the published interchange schema with
namespaces and an MCP server that browses, searches and installs across allow-listed registries;
registry.directory indexes 82 public registries with a machine-readable index and no systematic
licence display; Origin UI has become Cal.com's design system with a **mixed MIT/AGPLv3 licence**
by directory; the Supabase UI Library offers shadcn-compatible auth, storage and realtime blocks
whose operations the contract vocabulary already names; W3C DTCG v2025.10 is stable with Style
Dictionary v4 support.

## Decision

`ui` and `pattern` parts are **commodity and are referenced**: an entry names a registry item,
and the build installs it at build time through the shadcn MCP server from a registry on Scio's
committed allow-list. Scio carries no copy. `feature` parts are **the asset and are copied only
with a `Contract`**, and their only source is Scio's own builds, with consent, licence and origin
recorded before the first entry. Design is a **DTCG token file** derived from the spec and
transformed by Style Dictionary; components are themed from it, never chosen from a collection.

A registry enters the allow-list by a committed row: pinned namespace and URL, an SPDX licence
expression per registry and per item where licences mix, a recorded code review at a commit, and
its items pass the same install-time hooks as generated code (secret sink, leak patterns,
instrumentation stamp). A registry without a row is unreachable; the model never chooses one.
Every referenced part is recorded in the app's SBOM and in the evidence report, and its licence is
checked against what the buyer receives on buy-out. Templates and full starter apps are not
imported; the equivalent in Scio is a reference architecture per app kind. The same rule governs
*skill* registries: skills.sh (Vercel; 1.29M installs; vetting is installs, stars and an org whitelist)
and `addyosmani/agent-skills` (MIT, 25 skills, 91.6k stars; at least nine names collide with talents
we carry) are reuse-first *sources* for level-2 Playbook entries (ADR-0008), each candidate read in
full through the four gates and `playbook-admission`, then re-measured on Fable — never installed by
`npx` into a build (skills-repo notes `agent-builder-prior-art`, verified 2026-09-02).

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Import a large block collection into the catalog | Zero matchable entries; permanent maintenance and licence liability; buys the non-differentiator (`next/LAYER-D` §4.1) |
| Derive `operations` and the entity for imported blocks with a model | Puts a judgement call on the deciding path the library exists to keep decidable (predecessor ADR-0014, ADR-0016 rejected this in so many words) |
| Copy `ui` parts too, for control | Owns upstream's code, tests, security review and licence forever, for commodity parts whose value is that they are commodity |
| Let the build agent browse any public registry | 82 registries with unchecked licences and unreviewed code reaching a buyer's repository; the directory's own page says to review on install |
| Fill design from theme collections | A theme is a token set nobody derived from the spec; DTCG plus Style Dictionary gives the user a file they own instead |

## Consequences

**What this buys.** The `ui` gap closes without a catalog to maintain. The library's real
entries stay decidable. Licence exposure is a table, not a discovery. The evidence report can say
what an app contains and under which terms.

**What it costs.** A language-server-free but network-dependent install step per build; upstream
breakage inherited by reference; the allow-list as a maintained artefact with a review per
registry; an SBOM per app.

**What it forecloses.** Selling "thousands of components" as a feature. Offline builds for apps
that reference registries, unless the allow-listed items are mirrored — which is a later decision
with a cost, not this one.

## How we will know it was wrong

The match-and-miss ledger (D-2) shows `ui`-layer misses dominating build cost, which would mean
reference installs are not cheap enough and mirroring returns; a referenced item breaks delivered
apps at a rate that makes pinning per item necessary; or a licence in the allow-list survives into
a buy-out it should have blocked, which means the SPDX check is not on the transfer path.
