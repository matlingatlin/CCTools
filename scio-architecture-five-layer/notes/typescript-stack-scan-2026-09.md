---
title: TypeScript stack scan, 2026-09-03 — versions as measured, the TypeScript 7 / NestJS friction, ORM and framework positions, sandbox prices
sources:
  - path: knowledge/raw/web-2026-09-03-sdk-and-stack/npm-view-versions-2026-09-03.txt
    note: "npm view <pkg> version against registry.npmjs.org, 2026-09-03; typescript dist-tags."
    fetched: 2026-09-03
  - url: https://nodejs.org/dist/index.json
    note: "Release index; LTS codenames. Raw: nodejs-dist-index.json"
    fetched: 2026-09-03
  - url: https://fernforge.github.io/devnotes/nestjs-typescript-7/
    note: "Secondary (a developer's notes): tsgo emits decorator metadata (microsoft/typescript-go#2343, merged 2025-12-12); TS 7.0 ships no programmatic compiler API, which nest build depends on. Raw: nestjs-typescript-7-devnotes.html"
    fetched: 2026-09-03
  - url: https://github.com/nestjs/nest-cli/issues/3479
    note: "Returned a 378-byte shell; the issue's existence is from a search result only. Raw: nest-cli-issue-3479.html"
    fetched: 2026-09-03
  - url: https://northflank.com/blog/ai-sandbox-pricing
    note: "Vendor comparison table (secondary): E2B $0.0504/vCPU-hr + $0.0162/GiB-hr; Vercel Sandbox $0.128/vCPU-hr active CPU + $0.0212/GB-hr provisioned. Raw: northflank-ai-sandbox-pricing.html"
    fetched: 2026-09-03
  - note: "Search-summary-only (not fetched): Encore's Drizzle-vs-Prisma and NestJS-vs-Fastify-vs-Hono comparisons; Drizzle's RLS docs page; MarkTechPost sandbox comparison (2026-08-27). Cloudflare Sandboxes' per-vCPU-second figure appeared only in a summary and was not found in the raw table."
status: verified
tags: [typescript, node, versions, nestjs, prisma, drizzle, fastify, hono, vitest, biome, dependency-cruiser, turborepo, sandbox, pricing, scan, scio]
related: ["[[claude-agent-sdk-hosting-and-limits-2026-09]]", "[[build-evidence-tooling-2026]]", "[[third-party-landscape]]"]
---

# TypeScript stack scan, 2026-09-03

The dated scan Scio ADR-0003 requires before any framework choice inside TypeScript. Versions
are **measured** (the registry answered); everything about what those versions do is the
vendor's or a third party's word, graded as such.

## Claims

| # | Claim | Value | Verdict |
|---|---|---|---|
| 1 | Latest published versions, registry.npmjs.org, 2026-09-03 | `@anthropic-ai/claude-agent-sdk` 0.3.259 · `@anthropic-ai/sdk` 0.123.0 · `typescript` 7.0.2 (dist-tag `latest`; `beta` 6.0.0-beta; latest 6.x **6.0.3**, latest 5.x 5.9.3) · `@nestjs/core` 12.0.1 · `fastify` 5.12.1 · `hono` 4.13.5 · `prisma` 8.0.0-rc.12 / `@prisma/client` 7.10.0 · `drizzle-orm` 0.45.2 · `vitest` 5.0.0 · `@biomejs/biome` 2.5.12 · `dependency-cruiser` 18.2.0 · `turbo` 2.10.12 · `zod` 4.5.4 · `@playwright/test` 1.62.1 · `next` 16.3.4 | MEASURED |
| 2 | Node release lines | 24.x is LTS "Krypton" (24.20.0, 2026-08-26); 22.x LTS "Jod" (22.23.2); 26.8.1 current, not LTS | MEASURED (release index) |
| 3 | TypeScript 7's native compiler emits decorator metadata | "The Go compiler does handle `experimentalDecorators` and `emitDecoratorMetadata`, so the `design:paramtypes` metadata Nest's injector reads at boot is still emitted" — landed in microsoft/typescript-go#2343, merged 2025-12-12 | REPEATED (secondary; the PR itself not fetched) |
| 4 | TypeScript 7 ships no programmatic compiler API, so `nest build` cannot run on it | "7.0 ships no programmatic compiler API, and `nest build` is a program that imports `typescript` and calls `createProgram()`" | REPEATED (secondary); the nest-cli issue page was a shell |
| 5 | Sandbox prices, per the Northflank table | E2B $0.0504/vCPU-hr + $0.0162/GiB-hr, per second; Vercel Sandbox $0.128/vCPU-hr active CPU only + $0.0212/GB-hr provisioned + $0.023/GB-month snapshots; Northflank itself $0.01667/vCPU-hr + $0.00833/GB-hr | REPEATED (a vendor's comparison table; CPU-only for all three named) |
| 6 | Framework positions | NestJS: enforced module/controller/provider structure for large teams; Fastify: JSON-schema validation driving serialisation, Node-native speed; Hono: edge runtimes, lightest ceremony, "does not enforce structure" | REPEATED (search summaries of Encore's comparison) |
| 7 | ORM positions on row-level security | Drizzle "SQL-first… RLS integration natural" with an RLS docs page; Prisma "supports RLS via session variables but has historically been weaker here" | REPEATED (search summary) |
| 8 | NestJS 12 boots when compiled by TypeScript 7.0.2's native compiler with `emitDecoratorMetadata` | Scio spike 2026-09-06 (`apps/api/src/spike/nest-under-tsgo.ts`, Node 22.22.2, `@nestjs/core` 12.0.1): `design:paramtypes on Greeter: Clock` and `injected: yes`; the `typescript@7.0.2` package ships the native compiler as `tsc` | MEASURED (one module, one injected provider; not a full application) |
| 9 | `dependency-cruiser` 18.2.0 cannot read TypeScript sources through `typescript@7` | its own warning, 2026-09-06: "not a compatible TypeScript compiler (typescript: >=2.0.0 <7.0.0)… Support for typescript@>=7 will follow when its API is published and stable" — with 7 installed it cruised 0 modules; with 6.0.3 at the workspace root it cruised the sources and caught planted violations | MEASURED |
| 10 | NestJS 12's Express adapter, and what it pulls in | `@nestjs/platform-express` 12.0.1 (registry, 2026-09-09; `time.modified` 2026-08-27); its `package.json` depends on `express` 5.2.1; `@nestjs/platform-fastify` is also at 12.0.1 | MEASURED (registry read + the installed package's manifest) |
| 11 | A full NestJS 12 HTTP application boots under TypeScript 7.0.2's native compiler, parameter injection included | Scio `apps/api/src/http/server.ts`, 2026-09-09: `@Controller` with `@Inject`, `@Headers`, `@Param`, `@Body` parameter decorators, `NestFactory.create` + `listen(0)`, a global exception filter; 23 tests over HTTP on Node 22.22.2 | MEASURED (extends claim 8 from one module to an application) |
| 12 | Biome 2.5.12 refuses parameter decorators unless told | `pnpm lint` failed with "Decorators are not valid here" on every `@Inject`/`@Headers`/`@Param`/`@Body` (23 errors) and passed after `javascript.parser.unsafeParameterDecoratorsEnabled: true` in `biome.json`; class and method decorators never needed it | MEASURED |
| 13 | Vitest runs test files in parallel by default, and files that share one Postgres database collide | Scio, twice: `packages/platform` (2026-09-09, four suites on one database) and `apps/api` (2026-09-09, three suites dropping and recreating the same tables: five failures that vanished with `--no-file-parallelism`); the root runs packages with `turbo run test --concurrency=1` for the same reason | MEASURED (same symptom, same fix, two packages) |
| 14 | Postgres folds an unquoted identifier to lower case; a catalogue string comparison does not | Scio `render.test.ts` 2026-09-09: `CREATE SCHEMA spine_signedIn` created `spine_signedin`, and `pg_tables WHERE schemaname = 'spine_signedIn'` returned no rows until the name was lower-cased | MEASURED |
| 15 | A JavaScript `Date` round-trips a Postgres `timestamptz` at millisecond precision, so an optimistic guard on `updated_at` never matches; an integer version column does | Scio `apps/api/src/app/app.ts`, 2026-09-09: `WHERE updated_at = $n::timestamptz` with the ISO string read back through `new Date(...)` refused every guarded UPDATE (five suites red); a `version integer` bumped per UPDATE and compared exactly made them green | MEASURED |
| 16 | Under Vitest's jsdom environment `import.meta.url` carries an http scheme, so `new URL(file, import.meta.url)` cannot be read with `fs` | Scio `apps/web/src/design/tokens.test.ts`, 2026-09-09: `TypeError: The URL must be of scheme file`; reading from `process.cwd()` (the package root under Vitest) works | MEASURED |
| 17 | Vitest 5's `--dir` flag and a config `include` glob are relative to different roots | Scio `apps/web`, 2026-09-09: `vitest run --dir src` with `include: ["src/**/*.test.ts"]` found no test files; dropping `--dir` found both | MEASURED |
| 18 | dependency-cruiser 18 resolving through a NodeNext tsconfig cannot resolve an ESM-only Vite plugin from `vite.config.ts` | Scio 2026-09-09: `not-to-unresolvable: apps/web/vite.config.ts -> @vitejs/plugin-react`; excluding the Vite and Playwright config files from the cruise (they resolve through the bundler) cleared it with no other change | MEASURED |
| 19 | Playwright 1.63.0 drives the pre-installed Chromium through `launchOptions.executablePath` without a browser download | Scio 2026-09-09: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`, `executablePath: /opt/pw-browsers/chromium`; a `webServer` entry started the api (`node dist/root/cli.js`) against the test database and the fourteen-turn journey passed in 4.0 s on the stand-in model | MEASURED |
| 20 | A `style-src 'self'` CSP forbids React inline `style={{...}}` attributes as well as `<style>` injection; a native `<progress>` element and width classes need none | Scio `apps/web` 2026-09-09: the runtime-injected token stylesheet and two inline styles were replaced by a build-emitted `tokens.css` (a test refuses a stale file), a `progress` element and five width classes; the headers test asserts the CSP on `/` and `/api` and the journey still passes | MEASURED |
| 21 | An express app's static handler and a raw route registered on the instance run before NestJS mounts its router at `listen()`, so an SPA fallback must exclude the api prefix by regex | Scio `apps/api/src/http/server.ts` 2026-09-09: `get(/^(?!\/api(\/|$))(?!\/assets\/).*/)` on the express instance; `/apix` is the app, `/api/x` is the api's 404, a missing asset is a 404 | MEASURED (tested) |
| 22 | Biome 2.5 formats `.css` and lower-cases hex colours, which breaks a byte-equality test on a generated stylesheet | Scio 2026-09-09: `tokens.css` emitted with `#F6F8F5` came back `#f6f8f5` after `biome check --write`; excluding the generated file (`!**/tokens.css`) restored the byte-equality test | MEASURED |
| 23 | `jose` and the WebCrypto alternative for JWT verification | `jose` 6.2.12, MIT (registry, 2026-09-09). Node 22.22.2's `crypto.subtle.importKey("jwk", ...)` imports RSA and P-256/P-384 public keys and `crypto.subtle.verify` checks RS256/384/512 and ES256/384; Scio's verifier (`packages/platform/src/identity/jwks.ts`) needs no dependency and passes seven tests with a locally generated key pair and a local JWKS socket | MEASURED (the verifier); the library's scope REPEATED from the registry only |
| 24 | Under TypeScript 7 with the DOM lib, `new Uint8Array(buffer)` is `Uint8Array<ArrayBufferLike>` and is not a `BufferSource` for WebCrypto; `Uint8Array.from(buffer)` is `Uint8Array<ArrayBuffer>` and is | Scio 2026-09-09: `TS2345 ... not assignable to parameter of type 'BufferSource'` on `crypto.subtle.verify`; `Uint8Array.from(Buffer.from(part, "base64url"))` typechecks | MEASURED |
| 25 | A verifier that tolerates clock skew makes an "expired one second ago" test pass as valid | Scio 2026-09-09: `exp: now - 1` under a thirty-second leeway was accepted; the test must sit outside the leeway (`now - 60`) or it tests nothing | MEASURED |
| 26 | Git commit ids are content-addressed over tree, parents, author and committer lines: fixing `GIT_AUTHOR_*`, `GIT_COMMITTER_*` and both `_DATE` variables makes the same files with the same message commit to the same id, so a retried push is a no-op | Scio `packages/ship/src/repository/repository.ts` 2026-09-09 on git 2.43.0: two pushes of the same file map return the same 40-hex commit and the second push changes nothing (repository.test.ts, the git-host conformance suite) | MEASURED |
| 27 | `git init --bare -b main <path>` creates a bare repository with `main` as its initial branch without any global config, and `git push <path> main:main` from a working clone lands there; the api can host buyers' repositories with the git binary alone | Scio `packages/platform/src/adapters/local-git-host.ts` 2026-09-09 on git 2.43.0: create, push, clone-back and rev-parse HEAD equal to the pushed commit pass in the app journey test | MEASURED |
| 28 | Claim 26's idempotency holds only for IDENTICAL content. A build pipeline that re-inits a fresh working tree per push produces a parentless commit each time, so a SECOND build with different files shares no ancestor with the first and the remote refuses it | Measured 2026-09-11 on git 2.43.0: two single-commit histories pushed to one bare repository give `! [rejected] main -> main (fetch first)`, git exit code 1, and the bare repository still points at the first commit. Scio review 21 finding 3: the failure surfaces as a build the buyer paid for and is told failed | MEASURED |

## What it means here

- **The TypeScript 7 split (claims 3–4) is the one fact that changes a choice.** A NestJS
  service today either builds with `tsc` 6.0.3 / 5.9.3 and checks with 7, or compiles with `tsgo`
  directly and bypasses `nest build`. A Fastify or Hono service has no decorator metadata and no
  such seam. Scio's predecessor is NestJS 10 + Prisma 5 + Vitest 2 (`apps/api/package.json` on
  hello-world master), which is the measured cost of switching frameworks: 37 files, 1,984 lines
  and 135 API tests that carry forward as-is under NestJS and are rewritten under anything else.
- **Prices (claim 5) answer one of ADR-0004's five numbers** (cost per session-hour) at
  vendor-table precision; the other four — prewarm latency, concurrency limit, Playwright inside
  the boundary, regions — are still unmeasured and no page read today states them.
- **`dependency-cruiser` 18 and `@biomejs/biome` 2** are the fitness-function and lint tooling
  Scio ADR-0014 names; versions are pinned from this scan.

## What is open

- The Cloudflare Sandboxes price, the browser-inside-sandbox question, regions, prewarm latency.
- Whether NestJS 12 under TypeScript 7 holds for a Scio-sized application: the spike (claim 8) covered one module.
- Vitest 5 and NestJS 12 compatibility: not checked.
- A hosted git adapter (claims 26-27 are the local binary only): which provider, and whether its API can create a repository under a per-buyer owner at push time.
- What a REBUILD means when the buyer owns the repository (claim 28): commit on top of the existing history, or a per-build branch fast-forwarded into the default one. Undecided, and it blocks the second build.
