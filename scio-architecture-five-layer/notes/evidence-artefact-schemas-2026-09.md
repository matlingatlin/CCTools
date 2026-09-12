---
title: Evidence artefact schemas, 2026-09 — what CTRF, SARIF, in-toto and SLSA actually require
sources:
  - url: https://registry.npmjs.org/ctrf/-/ctrf-0.3.0.tgz
    note: "ctrf@0.3.0 (MIT), the reference package; dist/ctrf-schema-0.0.json and dist/index.d.ts read in full. Raw: knowledge/raw/web-2026-09-06-evidence-schemas/ctrf-npm/"
    fetched: 2026-09-06
  - url: https://ctrf.io/docs/specification/overview
    note: "A JS shell; only the example report and the sentence 'Just three essential properties required for each test - name, duration, and status' are in the served HTML. Raw: ctrf-spec-overview.html"
    fetched: 2026-09-06
  - url: https://json.schemastore.org/sarif-2.1.0.json
    note: "The OASIS SARIF 2.1.0 JSON Schema as mirrored by SchemaStore ($id points at oasis-tcs/sarif-spec). Raw: sarif-2.1.0.json"
    fetched: 2026-09-06
  - url: https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md
    note: "The Statement layer spec, read in full. Raw: in-toto-statement-v1.md"
    fetched: 2026-09-06
  - url: https://slsa.dev/spec/v1.0/provenance
    note: "SLSA Provenance v1.0 page, HTML; the predicate schema block and the model paragraphs read. v1.1 page fetched beside it. Raw: slsa-provenance-v1.0.html, slsa-provenance-v1.1.html"
    fetched: 2026-09-06
status: verified
tags: [evidence, ctrf, sarif, in-toto, slsa, attestation, provenance, schema, testing, app-builder]
related: ["[[build-evidence-tooling-2026]]", "[[architecture-evidence]]", "[[agent-harness-principles-2026]]", "[[app-builder-prior-art-and-library-standards-2026-09]]"]
---

# Evidence artefact schemas, 2026-09

Written 2026-09-06 while Scio's Build layer needed fixtures that validate against the two
formats ADR-0015 chose (CTRF for anything that runs tests or flows, SARIF for anything that
scans) and the statement that binds them to a commit. [[build-evidence-tooling-2026]] recorded
that these standards *exist* (its claims 1–3, all REPEATED from summaries); this note records
what each one *requires*, read from the schema files themselves. Every claim below is MEASURED
against the raw file named, unless marked otherwise.

## Claims

| # | Claim | Verdict | Source |
|---|---|---|---|
| 1 | The current CTRF reference package on npm is `ctrf@0.3.0` (MIT); it ships `dist/ctrf-schema-0.0.json`, exports `validate`, `isValid`, `validateStrict`, `parse`, `stringify`, `merge`, `calculateSummary`, `schema`, and the constants `REPORT_FORMAT = "CTRF"`, `CURRENT_SPEC_VERSION = "0.0.0"`, `SUPPORTED_SPEC_VERSIONS = ["0.0.0"]` | MEASURED (npm view; index.d.ts lines 504–1295) | ctrf-npm/ |
| 2 | A CTRF report's top level requires `results`, `reportFormat`, `specVersion`; optional `reportId`, `runId`, `timestamp`, `generatedBy`, `insights`, `baseline`, `extra` | MEASURED (schema `required`) | ctrf-schema-0.0.json |
| 3 | `results` requires `tool` (`name` required; `version` optional), `summary` (requires `tests`, `passed`, `failed`, `skipped`, `pending`, `other`, `start`, `stop`; optional `duration`, `suites`, `flaky`), `tests[]`; optional `environment` (`appName`, `buildId`, `buildName`, `buildNumber`, `commit`, `branchName`, `repositoryUrl`, `testEnvironment`, …) | MEASURED | ctrf-schema-0.0.json |
| 4 | Each test requires `name`, `status`, `duration`; `status` is the closed enum `passed | failed | skipped | pending | other` (the same enum on `retryAttempts[].status` and `steps[].status`); optional `message`, `trace`, `filePath`, `suite`, `tags`, `attachments[]` (`name`, `contentType`, `path` required), `steps[]` (`name`, `status` required), `start`, `stop`, `retries`, `flaky` | MEASURED | ctrf-schema-0.0.json |
| 5 | SARIF 2.1.0's top level requires `version` (enum: exactly `"2.1.0"`) and `runs[]`; a `run` requires `tool`; `tool` requires `driver`; a `toolComponent` requires `name`; a `result` requires `message`; a `reportingDescriptor` (rule) requires `id`; an `invocation` requires `executionSuccessful` | MEASURED (schema `required`) | sarif-2.1.0.json |
| 6 | `result.level` is the enum `none | note | warning | error`; `result.kind` is `notApplicable | pass | fail | review | open | informational`; `location`, `physicalLocation`, `artifactLocation`, `region`, `message` have no required fields (`message.text` and `artifactLocation.uri` are the usual carriers) | MEASURED | sarif-2.1.0.json |
| 7 | An in-toto Statement v1 is `{ "_type": "https://in-toto.io/Statement/v1", "subject": [ {name, digest:{alg:hex}} … ], "predicateType": URI, "predicate": {...} }`; `_type`, `subject`, `predicateType` are required, `predicate` optional; every subject MUST carry `digest`; subjects are matched by digest only | MEASURED (spec text) | in-toto-statement-v1.md |
| 8 | SLSA Provenance v1's `predicateType` is the string `https://slsa.dev/provenance/v1` (the spec says to use exactly that string, not the URL bar; the v1.1 page says the same); the predicate is `buildDefinition { buildType, externalParameters, internalParameters, resolvedDependencies[] }` and `runDetails { builder { id, builderDependencies[], version }, metadata { invocationId, startedOn, finishedOn }, byproducts[] }`; `externalParameters` are untrusted and MUST be recorded and verified downstream, `internalParameters` are trusted and optional | MEASURED (page text) | slsa-provenance-v1.0.html, v1.1 |
| 9 | A JSON Schema validator is available in this workspace without a new dependency: `ajv@8.20.0` (MIT) is already in Scio's pnpm store as a transitive dependency | MEASURED (`ls node_modules/.pnpm`, `npm view ajv license`) | this session |

## What it means here

- **A CTRF fixture is small:** `reportFormat: "CTRF"`, `specVersion: "0.0.0"`, `results.tool.name`,
  a full `summary` with all eight counters and `start`/`stop`, and tests with `name`/`status`/`duration`.
  Scio's gates that run things (the app's suite, the interaction scripts, the cross-tenant
  zero-rows test) emit this and nothing bespoke. `ctrf`'s own `validate()` is the check.
- **A SARIF fixture is a `run` with a `tool.driver.name`, `rules[]` with ids, and `results[]` each
  carrying `ruleId`, `level`, `message.text` and a `locations[0].physicalLocation.artifactLocation.uri`.**
  Scio's gates that scan (secret sink, plan conformance, placeholder and type honesty, security
  review) emit this. `ajv` over the SchemaStore file is the check.
- **The attestation is one Statement** whose `subject` is the built commit (`digest: {sha1: …}` or the
  bundle's `sha256`) and whose predicate is SLSA provenance v1 with the gate artefacts as
  `byproducts` and the spec, plan and skill plugin SHA as `externalParameters` — the untrusted
  inputs the judge must verify.
- **The predecessor's "missing artefact = unjudged" rule maps cleanly:** a gate with no CTRF or SARIF
  file is absent from `byproducts`, and the renderer has nothing to read.

## Neighbours

[[architecture-evidence]] argues that structural claims need artefacts a reader can check; this note is the artefact half of that argument. [[agent-harness-principles-2026]] carries the rule that a gate emits one standard file and a hook that did not fire is a missing row; the schemas here are what that file must contain.

## What is open

- The CTRF spec site is a JS application; the prose spec was not readable from the served HTML.
  The schema in the npm package is the source used. Whether the site's "spec version" wording
  differs from `0.0.0` is unread.
- SARIF was read as a schema, not as the OASIS prose; property semantics beyond `required` and
  enums (for example `baselineState`, `fingerprints`) are unread.
- The GitHub artifact-attestation mechanics named in [[build-evidence-tooling-2026]] claim 3 remain
  a shell; signing is not covered here.

## Added 2026-09-08
The registry item schema a library part would be validated against (a sibling to these evidence schemas, on the library side) is in [[app-builder-prior-art-and-library-standards-2026-09]].
