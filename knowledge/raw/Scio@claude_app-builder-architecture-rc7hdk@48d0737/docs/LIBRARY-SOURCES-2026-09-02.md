# Ready-made libraries — what Scio can jack into, and what it must never copy in

**Date:** 2026-09-02. **Status:** proposal; the decision is ADR-0013. This answers the user's
question about filling the component library from existing code and design libraries. The
forward view for Layer D (`docs/next/LAYER-D-LIBRARY.md` §4, written 2026-08-26) already worked
the question through against the predecessor's own gate functions; this document carries that
answer forward, adds today's scan, and names the sources.

---

## 1 · The finding that decides everything: an imported block is not a matchable entry

Layer D's forward view walked a shadcn `registry:block` — the richest third-party format there
is — through the fourteen things the predecessor's gate requires of an entry. Eleven can be
filled mechanically or with work. **Three cannot be filled without a judgement call**, and the
library is designed never to make one:

| What matching needs | Why a block cannot supply it |
|---|---|
| `operations` — what the part *does* to the app's data | a block declares none, because it is not a feature; it is a view |
| `files` equal to the package's file plan | the file plan is derived from the app's architecture; a block's tree is never that set |
| the entity, as `__ENTITY__` in paths and bodies | a block is not *about* anything |

Conclusion, verbatim from the forward view: *importing a visual block collection would not add
one matchable entry.* It adds `ui`-layer inventory of the kind that already sits in the catalog
unreachable (three of four seed entries), and it buys the half of the problem the reviews say is
explicitly not the differentiator: Lovable already ships design systems, a private registry,
cross-project referencing and templates.

Twelve of fourteen rows also expose what a copy would cost forever: a shipping test file,
`security_reviewed = True`, an accessibility score, no leaked avatar URLs, a licence and a
provenance chain. Every copied file is a maintenance and licence liability the library owns.

## 2 · The rule: commodity by reference, asset by contract

This is D-7 in the forward view and it becomes ADR-0013:

- **`ui` and `pattern` parts are commodity. Reference them.** An entry says *this app uses
  `@shadcn/button`* and the build installs it from the registry at build time, through the
  registry's own CLI or MCP. Scio never carries a `button.tsx`. That removes the maintenance,
  the licence question and the gate problem in one move.
- **`feature` parts are the asset. Copy them, and only with a `Contract`.** A feature entry
  carries operations, an entity, a file plan, a test, a security review and provenance. It comes
  from a build that passed the gates, generalised and re-verified against an unseen entity. **No
  external source can produce one**, which is exactly why the library is worth having.
- **Design is a token file, not a component set.** The system is derived from the spec and
  emitted as W3C DTCG (stable v2025.10, backed by Adobe, Figma, Google, Microsoft and others);
  Style Dictionary v4 turns it into CSS variables and Tailwind config. The component set is then
  *themed*, never *chosen*, from a token file the user owns.

The trade-off is named in the forward view and accepted: a reference means Scio does not control
the code, cannot instrument it until install time, and inherits upstream breakage. For commodity
parts that is the right side of the line.

## 3 · What exists to jack into, checked 2026-09-02

### 3.1 The registry ecosystem — the reference layer

| Source | What it is | Verified today | Verdict |
|---|---|---|---|
| **shadcn registry format** (`registry-item.json`) | the published schema: files, targets, deps, `registryDependencies`, `cssVars`, `envVars`, namespaces, `include` (May 2026) | the format Layer D already adopts as interchange | **adopt** as the `ui` interchange format and as the *export* format for Scio's own feature entries (with `Contract` in `meta`) |
| **shadcn MCP server** | browse, search, install across registries; namespaced, private and authenticated registries via `components.json`; config is `npx shadcn@latest mcp` | docs fetched | **adopt as the build-time mechanism** — the `package-builder` subagent's `mcpServers` row (ADR-0008). The registries it may reach are an allow-list Scio controls, not the model's choice |
| **shadcn Registry Directory** | community registries added with `npx shadcn add @<registry>/<component>`; the page's own caveat: *"maintained by third-party developers. Always review code on installation"* | fetched | the discovery surface; **no registry is allowed until it has a licence row and a review** (§4) |
| **registry.directory** | index of **82 public registries**, machine-readable `items.json`, `directory.json`, an OpenAPI 3.1 spec; licences *not* shown systematically | fetched | **use its index to build Scio's allow-list**, never as the allow-list |
| **Supabase UI Library** | shadcn-compatible: password auth (sign-up, sign-in, reset, forgot), social auth, file dropzone, realtime chat, realtime cursors, avatar stack, current-user avatar, client init; Next.js, React Router, TanStack Start, React | blog fetched; licence not stated on the pages read — **verify in the repo before use** | **the one source that is feature-shaped.** Auth and storage are operations the contract vocabulary already has. Candidate for the first *referenced feature*: matched by contract, installed by reference, gated at install |
| **Magic UI** | animated components, `registry.json` present | MIT, 22.1k stars | allowed `ui` registry, after review |
| **Origin UI → coss.com/ui** | now Cal.com's design system on Base UI; **licence is mixed: MIT for two directories, AGPLv3 elsewhere** | fetched | **the licence hazard D-1 warns about, live.** Allowed only by directory, with the SPDX expression recorded per item |
| Aceternity, Kibo, and the rest of the 82 | animation and block registries | not licence-checked today | each enters the allow-list one at a time, per §4 |

### 3.2 Design — the token layer

| Source | Verdict |
|---|---|
| **W3C DTCG format** v2025.10 | **adopt** (already argued in `app-design` §1 and Layer D's means table); the ownership promise applied to design |
| **Style Dictionary v4** (v5 for full 2025.10) | **adopt**; pin and verify, do not write transforms |
| **Figma MCP** (`get_variable_defs`, `get_design_context`) | **later** — earns its place when a buyer brings an existing Figma system |
| theme generators for shadcn (tweakcn and similar) | not verified today; at most a reference for how a token file becomes a `cssVars` block, which Style Dictionary already does |

### 3.3 What is *not* jacked into

- **Template and starter collections** (full apps). A template is a build someone else made
  without Scio's spec, gates or evidence; importing one is importing an unverified build. The
  right form of a template in Scio is a *reference architecture* per app kind (Layer B's
  forward view §4.1), which compounds once per app and cannot be bought.
- **Marketplaces of prompts or "components" without code.** Nothing to gate.
- **Anything without a licence expression.** SPDX or it does not enter.

## 4 · The admission gate for an external registry

An external registry is admitted to the build-time allow-list by a row in a table that is itself
committed, and the row is the gate:

| Field | Rule |
|---|---|
| namespace and URL | exact, pinned |
| licence | an SPDX expression per registry, and per item where the registry mixes licences (coss.com/ui); parsed with `license-expression`, compared against what a buyer may receive on buy-out (ADR-0009) |
| review | who read the code, when, at which commit; the `security-reviewer` subagent's row plus a person for the first admission |
| install gate | every install is a `PostToolUse` event: the secret sink, the leak patterns (demo avatar URLs fail as shipped), the instrumentation stamp applied after install |
| provenance | recorded in the app's SBOM (CycloneDX or SPDX) and in the evidence report: *this app contains these referenced parts from these registries under these licences* |

A registry with no row is not reachable from the MCP server. The model does not choose registries.

## 5 · What the library's own growth is, then

Not imports. Three sources, in the order Layer D's forward view fixes:

1. **The match-and-miss ledger first (D-2).** Every package that matched, every one that missed
   and why. Without it, nothing about the library is decidable, and "fill the library" has no
   measure of whether filling helped.
2. **Contribution from Scio's own builds (ADR-0006 Slice 3)**, including promotions, with consent,
   licence and origin recorded before the first entry (D-1). This is the only source of
   `feature` entries, and it is the one nobody else can import.
3. **Evidence as the product (D-8).** Each entry's `Quality` becomes a signed attestation
   (in-toto/SLSA shape) binding it to the build that made it. *Anybody can import a registry;
   nobody can import the evidence that our builds produced.*

If the ledger shows contracts scattering rather than converging, the forward view's §4.4 stands:
freeze the catalog at hand-written seeds and move the investment to reference architectures.

## Sources

- `docs/next/LAYER-D-LIBRARY.md` §4.1–4.4, §5, §9 (D-1, D-2, D-7, D-8), 2026-08-26; `docs/as-built/REVIEWS-WHAT-WE-MISSED.md` §4; `.claude/skills/app-design` §1, §6b
- [shadcn Registry Directory](https://ui.shadcn.com/docs/directory), [shadcn MCP](https://ui.shadcn.com/docs/mcp), [registry.directory](https://registry.directory/), [Supabase UI Library](https://supabase.com/blog/supabase-ui-library), [Magic UI](https://github.com/magicuidesign/magicui), [coss.com/ui (Origin UI)](https://github.com/origin-space/originui), [W3C DTCG](https://www.designtokens.org/), [Style Dictionary DTCG](https://styledictionary.com/info/dtcg/) — all fetched 2026-09-02
