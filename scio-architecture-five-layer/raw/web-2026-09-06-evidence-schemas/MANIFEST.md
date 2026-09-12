---
title: Raw layer — the evidence artefact schemas (CTRF, SARIF, in-toto, SLSA), fetched 2026-09-06
imported: 2026-09-06
by: the Scio build session (single writer for this commit)
status: RAW — never edited; HTML as served through the session proxy; the ctrf npm tarball unpacked with only its schema, types, package.json, README and LICENSE kept (the compiled JS was dropped for size, the dropped files are named below)
---

# web-2026-09-06-evidence-schemas

| File | URL / command | Fetched | sha256[:12] | Bytes | Feeds |
| --- | --- | --- | --- | ---: | --- |
| `ctrf-npm/package/dist/ctrf-schema-0.0.json` | https://registry.npmjs.org/ctrf/-/ctrf-0.3.0.tgz (npm view ctrf version → 0.3.0) | 2026-09-06 | `742dee4cffda` | 26,288 | evidence-artefact-schemas-2026-09 |
| `ctrf-npm/package/dist/index.d.ts` | same tarball | 2026-09-06 | `d418b7d6f264` | 33,260 | evidence-artefact-schemas-2026-09 |
| `ctrf-npm/package/package.json` | same tarball | 2026-09-06 | `beda86232765` | 2,453 | evidence-artefact-schemas-2026-09 |
| `ctrf-npm/package/LICENSE`, `README.md` | same tarball (MIT) | 2026-09-06 | — | — | licence check |
| `ctrf-spec-overview.html` | https://ctrf.io/docs/specification/overview | 2026-09-06 | `8604c3838d38` | 30,449 | evidence-artefact-schemas-2026-09 (the example report only; the page is a JS shell) |
| `ctrf-readme.md` | https://raw.githubusercontent.com/ctrf-io/ctrf/main/README.md | 2026-09-06 | `2b6008b146b5` | 3,208 | evidence-artefact-schemas-2026-09 |
| `sarif-2.1.0.json` | https://json.schemastore.org/sarif-2.1.0.json | 2026-09-06 | `7c9688f0a1c4` | 111,720 | evidence-artefact-schemas-2026-09 |
| `in-toto-statement-v1.md` | https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md | 2026-09-06 | `cbe684a18b81` | 2,492 | evidence-artefact-schemas-2026-09 |
| `slsa-provenance-v1.0.html` | https://slsa.dev/spec/v1.0/provenance | 2026-09-06 | `a5d8066c3a29` | 61,049 | evidence-artefact-schemas-2026-09 |
| `slsa-provenance-v1.1.html` | https://slsa.dev/spec/v1.1/provenance | 2026-09-06 | `d6f9509b9921` | 62,138 | evidence-artefact-schemas-2026-09 |

Dropped from the tarball after unpacking: `dist/cli/*`, `dist/index.js`, `dist/index.cjs`, `dist/index.d.cts`, `src/*`.
Four URLs returned 404 and were not kept: `raw.githubusercontent.com/ctrf-io/ctrf/main/schema.json`, `.../ctrf-schema.json`, `raw.githubusercontent.com/slsa-framework/slsa/main/docs/spec/v1.0/provenance.md`, `.../docs/provenance/v1.md`. `ctrf.io/docs/specification/root` served the same bytes as `overview` and was deleted.

Added 2026-09-06, later: `claude-agent-sdk-0.3.259-sdk.d.ts` — the installed package's type declarations, copied from Scio's pnpm store (`node_modules/.pnpm/@anthropic-ai+claude-agent-sdk@0.3.259/.../sdk.d.ts`), sha256[:12] `f76aa847ddf4`, 426,240 bytes; feeds claude-agent-sdk-hosting-and-limits-2026-09 claim 15.
