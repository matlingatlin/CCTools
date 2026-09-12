# Layers D, F and G — mining triage

*2026-08-26. Every row in `docs/mined/` that names Layer D (the component library),
Layer F (the design window) or Layer G (cross-cutting), triaged to one of four
destinations. Nothing here changes behaviour; the ADR rows are proposals, not decisions.*

---

## 1 · How this was scoped, and where the index undercounts

`scripts/findings-index.py` reports **D 23 · F 8 · G 5**, plus the `D/E`, `D/G`, `E/F`,
`E/G`, `F/A` and `G/B` pairs. Its own footer says to treat counts as a floor. They are.

Re-extracting by looking for a table cell that *is* a layer tag — rather than by regex over
the whole row — finds **78 rows** touching D, F or G. The difference is parse artifacts, and
they are worth naming because each one is a finding nobody would have read:

| Row | Index put it in | Actually |
|---|---|---|
| `PASS2-ECC-SKILLS.md:659` — statuses carry a TTL and decay to a truthful terminal state | **A** | `F, G` — the item cell was longer than the finding cell, and the tie-break picked *"**A** crashed agent decays…"* |
| `PASS2-GSTACK-SKILLS.md:709`, `:710` — the AI-slop rubric dimension, the baseline→final score delta | **A** | `F` |
| `PASS2-GSTACK-SKILLS.md:691` — provenance on library entries + a canary component | *(unlisted)* | `D` |
| `PASS2-ECC-RULES-COMMANDS.md:660`, `:685`, `:692`, `:693`, `:694` | *(unlisted)* | `F`, `D`, `F`, `F`, `G` |
| `PASS2-GSTACK-TESTS.md:706`, `:718` | *(unlisted)* | `G, E` · `B, D` |

`PASS2-ECC-SKILLS.md:666` and `:667` — the two rows the brief calls out as unusually
strong — are tagged `B, G` and `B, C, E`, so neither lands in a bucket named in the brief.
Both are triaged here.

**76 rows are triaged below.** The remaining rows touch D, F or G but are owned by Layer A,
B or C; they are listed in §7 rather than judged here.

## 2 · The four verdicts

- **SKILL** — a decision procedure: what exists in a domain plus how to choose among it, or a
  rule for a recurring situation. Destination: a `.claude/skills/<name>/SKILL.md`, new or amended.
- **ADR** — a decision about *what to build*. Destination: `docs/decisions/` later.
  `docs/next/SKILLS.md`: *a skill that quietly decides what we do is an architecture decision
  hiding in a markdown file.*
- **FIX** — a specific defect with a specific repair.
- **DROP** — with the reason. "Already carried" is the most common one and it is a real result.

---

## 3 · Layer D — the component library

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| D1 | Repository pattern, API response envelope | `ECC-RULES.md:512` | **DROP** | already left in the mining pass — architectural taste, and `Contract` fixes the shapes the library cares about |
| D2 | RTL query priority, MSW, `userEvent` over `fireEvent`, coverage-by-layer | `ECC-RULES.md:514` | **DROP** | already left — belongs in the scaffold's `test-utils.tsx`; `testing` §6 already owns the level boundaries |
| D3 | Layer D must distinguish *matched nothing* from *could not look* | `ECC-SKILLS.md:662` | **SKILL** | `contract-retrieval` — new §3.5, with D9 |
| D4 | Entries carry the `Playbook` version they were built under; a contract match is not a recency match | `ECC-SKILLS.md:663` | **ADR** | adds a field to `CatalogEntry` and a staleness policy — same schema decision as D25 and G-4 |
| D5 | Memory→policy promotion barrier: *"team memory is not trusted merely because it is committed"* | `ECC-SKILLS.md:665` | **ADR** | it reverses ADR-0016's provisional-but-offerable. Cannot be adopted in a skill |
| D6 | `search-first` as a workflow | `ECC-SKILLS.md:675` | **DROP** | already left — outward retrieval; ours is inward and typed |
| D7 | `api-connector-builder`'s conform-to-two-examples | `ECC-SKILLS.md:680` | **DROP** | already left — a typed `Contract` is strictly stronger |
| D8 | Catalog token budget + 260-byte per-entry cap + same-commit ratchet | `OTHERS-MINED.md:726` | **SKILL** | **`catalog-budget`** (new) §1–§3 |
| D9 | `null` (did not run) vs `[]` (ran, found nothing); never search unscoped | `OTHERS-MINED.md:729` | **SKILL** | `contract-retrieval` — new §3.5 |
| D10 | Recall-then-verify: cheap recall → top-k → exact `Contract` verification | `OTHERS-MINED.md:762` | **DROP** | already carried — `contract-retrieval` §3.3 is this decomposition |
| D11 | Vector similarity on the matching path | `OTHERS-MINED.md:763` | **DROP** | already carried — `contract-retrieval` §2 and Limits |
| D12 | Content-hash staleness test keyed by absolute path | `OTHERS-MINED.md:764` | **ADR** | superseded in part by D16–D18; a requirement of the Contract-index decision, not a rule that stands alone |
| D13 | Signature-only view of a corpus is the artefact; concatenating it is the mistake | `OTHERS-MINED.md:770` | **DROP** | the observation is the layer's premise — a `Contract` *is* a signature with no body (`identity.py:140`) |
| D14 | **Absorb** as a fourth library verdict, with an overlap check before any new entry | `PASS2-ECC-RULES-COMMANDS.md:685` | **ADR** | changes the contribute verdict set (`contribute.py:9-15`) |
| D15 | All of ECC clusters D and E as content | `PASS2-ECC-SKILLS.md:687` | **DROP** | already left after sampling all 48 files |
| D16 | Content hash + persisted snapshot + three-way `{added, removed, modified}` diff | `PASS2-FOUR-REPOS.md:638` | **ADR** | requirement of the Contract-index decision that `contract-retrieval` §3.4 defers |
| D17 | The staleness snapshot is keyed by the artefact's identity, not its filesystem path | `PASS2-FOUR-REPOS.md:639` | **ADR** | same decision |
| D18 | The snapshot is written **after** the artefact is durable, and only from the set that **succeeded** | `PASS2-FOUR-REPOS.md:640` | **ADR** | same decision — and it is the half claude-context got wrong in its own code |
| D19 | A vector index anywhere on the deciding path | `PASS2-FOUR-REPOS.md:643` | **DROP** | already carried — reaffirmed leave; `satisfied_by` stays two subsets and an equality |
| D20 | How to cite claude-context's headline number | `PASS2-FOUR-REPOS.md:644` | **SKILL** | `contract-retrieval` §4 Limits — the F1 is *end-to-end edit-localisation*, not retrieval quality |
| D21 | Signature extraction dedups twice — containment, then content identity | `PASS2-FOUR-REPOS.md:652` | **DROP** | Scio's `Contract` is derived from the file plan and operation list (`identity.py:152`), never extracted by a parser. There is no extraction step to dedup |
| D22 | Cut a signature at the parse tree's own child ranges, never by `indexOf` | `PASS2-FOUR-REPOS.md:656` | **DROP** | same reason as D21 |
| D23 | Iron contract: stage → test → approve → atomic rename | `PASS2-GSTACK-SKILLS.md:689` | **ADR** | the *approve* step is ADR-0016 reversed; the stage/rename half is already `contribute.py`'s re-verify-and-discard |
| D24 | Three-condition confident match; ambiguity falls through to generation | `PASS2-GSTACK-SKILLS.md:690` | **DROP** | already built, and asserted — `matcher.py:217` and `test_two_equal_entries_with_no_judgment_generate_rather_than_guess` |
| D25 | Provenance on entries (`trusted`/`source`/`version`) + a designated canary component | `PASS2-GSTACK-SKILLS.md:691` | **ADR** | the same missing columns as `LAYER-D` §3.1 and `LAYER-G` §3.2 — `library_entry` has eight columns and none of them is an origin |
| D26 | Budget floor as well as ceiling — ×0.80 shrink floor beside the ×1.50 growth cap | `PASS2-GSTACK-TESTS.md:695` | **SKILL** | `catalog-budget` §2 |
| D27 | Two-tier catalog entry: lead in the always-loaded index, body loaded on selection | `PASS2-GSTACK-TESTS.md:696` | **SKILL** | `catalog-budget` §3 — the mechanism that makes a byte cap survivable |
| D28 | One enumerator returning three deliberately-different counts | `PASS2-GSTACK-TESTS.md:714` | **SKILL** | `catalog-budget` §4 — you cannot ratchet a budget without one census |

**D: 7 SKILL · 9 ADR · 0 FIX · 12 DROP.**

---

## 4 · Layer F — the design window

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| F1 | Visual mode offered just-in-time, as its own message; per-question show-vs-tell test | `OTHERS-MINED.md:746` | **ADR** | when the design window shows rather than asks is product behaviour. The ideation half is already `brainstorm` |
| F2 | *"Every changed line should trace directly to the user's request"* | `OTHERS-MINED.md:771` | **SKILL** | `change-impact-analysis` — new §2.6, the *explained* criterion |
| F3 | Animate `transform`/`opacity` only | `PASS2-ECC-RULES-COMMANDS.md:660` | **SKILL** | `app-design` §3 and §5 — the mined row already says *merge into `app-design`* |
| F4 | Second builds: dry-run by default · diff above a threshold · `AUTO-GENERATED` markers | `PASS2-ECC-RULES-COMMANDS.md:692` | **DROP** | premature: no path exists by which a user's hand edits re-enter a build. `ShipPage.tsx:104-122` names download and push as not built. Revisit if export lands |
| F5 | Gate the promoted repo on `next build`, not `tsc --noEmit` — they fail differently | `PASS2-ECC-RULES-COMMANDS.md:693` | **FIX** | `compiles` is answered by `builder/typecheck.py` after a change (`change.py:330`) and after a restore (`restore.py:104`). A promoted repo that typechecks can still fail `next build` |
| F6 | Undelivered-feedback backstop that refuses to end the turn | `PASS2-ECC-SKILLS.md:660` | **FIX** | the layer computes honest data that reaches nobody: `PackageChange.cost_usd` is dropped at `design.service.ts:426-433`, and `checks_passed` is transmitted and appears in no `.tsx` (`LAYER-F` §1.1(g), §3.2) |
| F7 | Closed three-word status vocabulary — Latest · Superseded · Forgotten — with an optional reason | `PASS2-FOUR-REPOS.md:648` | **ADR** | which statuses a design version has is a product decision. **The rule is already carried** by `provenance-record` (superseded rather than deleted, mutable status fields); what remains is ours to decide |
| F8 | Branching in a version chain is forbidden at write or represented, never silently linearised | `PASS2-FOUR-REPOS.md:650` | **ADR** | two directed changes from one spec version is the normal case; the design version `ref` is a JSON blob today (`design.service.ts:169-183`) with no parent pointer. Rule already carried by `provenance-record` (*when a version chain can branch*) |
| F9 | Ten-dimension rubric with an AI-slop dimension and a score<7 escalation | `PASS2-GSTACK-SKILLS.md:709` | **DROP** | the weighted-composite half was already refused twice (`ECC-SKILLS.md:677`, `PASS2-ECC-SKILLS.md:686`); the AI-slop cluster is already `app-design` §3, verbatim |
| F10 | Baseline→final score delta with a regression warning | `PASS2-GSTACK-SKILLS.md:710` | **ADR** | requires Layer F to score a preview at all, which nothing does — `LAYER-F` §3.6 |
| F11 | Laplace smoothing + 5%/week decay at read + FIFO 50 + drift warning | `PASS2-GSTACK-TESTS.md:716` | **ADR** | conditional on a decision nobody has taken: does Layer F remember taste across builds. Rule already carried by `provenance-record` (*when a decay or half-life stops surfacing something*); the decision is not |
| F12 | Statuses carry a TTL and decay to a truthful terminal state | `PASS2-ECC-SKILLS.md:659` | **ADR** | our honest-status vocabulary names values, not what the UI shows when the reporter dies. Adding a value is an ADR; `gate-verdicts` and `provenance-record` between them already carry the rule |

**F: 2 SKILL · 6 ADR · 2 FIX · 2 DROP.**

---

## 5 · Layer G — cross-cutting

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| G1 | Closed relation ontology, three values wide — enumerate ours | `OTHERS-MINED.md:768` | **FIX** | `Permission.scope: str` with the enumeration in a comment (`architecture.py:83`) → `Literal["own","all","none"]`; `row_level_security: bool = True` → a per-table decision carrying its reason |
| G2 | Store the producing model id beside a derived value | `OTHERS-MINED.md:769` | **ADR** | sharpened by G4 into *in the key, not beside the value*; adopting either is a schema decision |
| G3 | Append-only ledgers declare a reduction key **including the tenant**; the consumer reduces | `PASS2-ECC-RULES-COMMANDS.md:694` | **SKILL** | `tenant-isolation` §5. The reduce-in-the-database half is a one-line **FIX**: `usage.service.ts:62-68` reduces in Node, and `aggregate` is already in `READ_OPERATIONS` (`workspace-scope.ts:33`) |
| G4 | Cache keys are `(content hash, producer identity, format version)` — producer **in** the key | `PASS2-FOUR-REPOS.md:657` | **ADR** | with G2 and D16–D18 |
| G5 | LLM Output Trust Boundary as a review category | `PASS2-GSTACK-SKILLS.md:697` | **ADR** | format-validated outputs, shape-checked tool results, allowlisted fetch targets, sanitised retrieval writes — a `Playbook` addition, so Layer B's decision |
| G6 | Three-layer privacy-promise enforcement: coverage · behaviour-of-the-actual-filter · floor | `PASS2-GSTACK-TESTS.md:717` | **SKILL** | `tenant-isolation` §6 — the discipline that makes an isolation claim provable rather than asserted |

**G: 2 SKILL · 3 ADR · 1 FIX · 0 DROP.**

---

## 6 · The pairs

### D/E

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| P1 | `mkdir`-as-mutex, owner token, 10-min stale reclaim, skip the cycle rather than queue | `PASS2-FOUR-REPOS.md:641` | **ADR** | requirement of the Contract-index decision (with D16–D18); no periodic rebuild exists to guard yet |
| P2 | **Predicted vs Actual** recorded per package after every build | `PASS2-ECC-RULES-COMMANDS.md:684` | **ADR** | this is `LAYER-D` §3.2's match-and-miss ledger. A prerequisite decision, and `reuse-classification` §2.3 already carries the four numbers it would report |

### D/G

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| P3 | Optional-provider contract: required/optional capabilities, ops classed read/write, fail-closed default, `local` as a provider property, consent covers *search* | `OTHERS-MINED.md:728` | **ADR** | the mined row already defers it — *"take when the library outgrows a file"*. The consent-covers-search clause is evidence for the consent ADR (`LAYER-G` §9 G-4), because the query text is repo-derived content |
| P4 | Identifiers derived from user text are query **parameters**, never interpolated | `PASS2-FOUR-REPOS.md:642` | **SKILL** | `tenant-isolation` §5 — the same boundary drawn for queries and paths |

### E/F

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| P5 | Content-hash cache keys instead of identity keys; key on the composed prompt's hash | `ECC-SKILLS.md:664` | **FIX** | contract-first ordering plus a content-hash key, per `LAYER-F` §2.2 and §7.3. Today nothing in the change path is cacheable |
| P6 | `gan-style-harness` four-criterion weighted rubric | `ECC-SKILLS.md:677` | **DROP** | already left — unvalidated weights; `app-design` §5's deterministic checks are the better instrument |
| P7 | Rulings not stalls: closed 4-item stop list + `Ruling: what — why — cost if wrong` | `OTHERS-MINED.md:748` | **ADR** | with P11 — one proposal, the autonomy rule for a directed change |
| P8 | Six click-path bug patterns + side-effect-map-first ordering | `PASS2-ECC-SKILLS.md:654` | **ADR** | adding a gate is a decision about what to build; the mined row's own value is that Scio can derive the side-effect map from the architecture graph |
| P9 | Score **caps**: deterministic conditions set a ceiling a judgement score may not exceed | `PASS2-ECC-SKILLS.md:657` | **DROP** | Layer E owns the scoring arithmetic (`LAYER-E` §1) and Scio has no judgement score to cap. `app-design` §5 supplies the conditions when it does |
| P10 | *"Omit principles you checked but did not change"* | `PASS2-ECC-SKILLS.md:680` | **DROP** | already carried — `gate-verdicts`, written in a parallel pass, fires on *"a report pads itself with things it checked but did not change"* |
| P11 | Fix-First heuristic: mechanicality decides autonomy, severity biases toward asking | `PASS2-GSTACK-SKILLS.md:692` | **ADR** | with P7. Deciding that Layer F auto-applies mechanical edits is a product decision, not a skill |
| P12 | Every gate declares whether it is the enforcement point and names the real one if not; every destructive action ships a non-scope list and an undo | `PASS2-GSTACK-SKILLS.md:686` | **SKILL** | **`gate-verdicts`**, which a parallel pass wrote around exactly this rule. `tenant-isolation` §6.1 carries only the tenancy instance and points there — positive: `ci.yml` (*"a hermeticity check, not a security check, and it does not claim to be"*); negative: `tenant-discipline.spec.ts` |
| P13 | Adversarial prompt: authorization preamble, fixture summary-mode, format-graded `Recommendation:` line | `PASS2-GSTACK-SKILLS.md:704` | **DROP** | Layer E's adversarial pass owns it; the Layer F half (promotion ends with one line naming a specific finding) is F10's ADR, not a second home |
| P14 | `gan-style-harness` weighted rubric — second argument for leaving it | `PASS2-ECC-SKILLS.md:686` | **DROP** | already left, reinforced |
| P15 | Repair loop: one change, verified, `git checkout --` on failure, skip the item; SAFE/CAUTION/DANGER tiers | `PASS2-ECC-RULES-COMMANDS.md:689` | **DROP** | already built and better — `change.py:290-322`, one rejected package never stops the others, and a change that loses a `data-scio-id` is rolled back |
| P16 | Use a score only where a gradient is needed; a verdict + checklist for decisions | `PASS2-ECC-RULES-COMMANDS.md:697` | **DROP** | one sentence, and it is already the operative rule — `app-design` §5 is a checklist of deterministic verdicts, and P6/P14 refused the composite on this ground |

### E/G

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| P17 | Unindexed-foreign-key detection over the generated migration set | `PASS2-ECC-SKILLS.md:649` | **ADR** | a new deterministic gate, and where it sits in `loop.py`'s ordering is Layer E's decision |
| P18 | Spend limits enforced outside the model; audit-log refused and halted runs, not only successful ones | `PASS2-ECC-SKILLS.md:669` | **FIX** | `AuditLog` exists, is workspace-scoped and has never been written to; four of eight `UsageKind` values have no writer (`LAYER-G` §1.8, §3.5). Metering that counts only completed builds cannot answer a disputed bill |
| P19 | `transition: all` and `will-change: all` as quality-pattern greps | `PASS2-ECC-SKILLS.md:672` | **SKILL** | `app-design` §3 and §5, with F3 — the mined row's own argument is that a linter should guarantee them |
| P20 | Two confidence gates (8/10 daily, 2/10 + `TENTATIVE`) + a 5-band display policy | `PASS2-GSTACK-SKILLS.md:699` | **DROP** | Layer E's gate ordering; there is no G-side surface it attaches to, and the demote-never-delete rule is already `honest_status`'s shape |
| P21 | Receipt before send + a fail-open/fail-closed polarity table asserted with exact `toEqual` | `PASS2-GSTACK-TESTS.md:704` | **ADR** | an egress ledger is a new control; Scio has no enumeration of the places bytes leave |
| P22 | Never render a missing value as a good value: trusted / unverified / unknown / error | `PASS2-GSTACK-TESTS.md:706` | **FIX** | instantiated at `Quality.better_than`: every contributed entry carries `scores_measured=False` and **zeros** in `accessibility_score` and `lighthouse_score`, and a Pareto comparison reads the zeros as measurements (`LAYER-D` §2.3). Refuse to compare when `scores_measured` differs |

### F/A

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| P23 | `forgetAfter` + `forgetReason` + `isForgotten`; superseded is shown dimmed, not deleted | `OTHERS-MINED.md:767` | **ADR** | with F7 — one proposal for the design-version lifecycle |
| P24 | Their forgetting has no engine: `forgetAfter` is read by exactly one place | `PASS2-FOUR-REPOS.md:646` | **ADR** | same proposal, and it is the warning attached to it — a lifecycle field with no reader is decoration |

### G/B

| # | Finding | Source · line | Verdict | Destination |
|---|---|---|---|---|
| P25 | Contradictory safety-relevant flags error; detection sets priority, not scope | `PASS2-GSTACK-SKILLS.md:711` | **ADR** | never silently resolve contradictory user input — a Layer B intake decision |
| P26 | `COMMENT ON COLUMN … IS 'PII: …'` — sensitivity labels that survive into the generated database | `PASS2-ECC-SKILLS.md:666` | **SKILL** | `tenant-isolation` §4. Layer B already types every field and nothing carries the classification downstream |
| P27 | A cross-tenant read returning zero rows, generated beside every RLS policy | `PASS2-ECC-SKILLS.md:667` | **SKILL** | `tenant-isolation` §4 — the evidence half of `LAYER-B` §3.5, and the assertion `verification/client.ts` is already built to run |
| P28 | *"No mutable module-level state in RSC/SSR — module state is shared across all requests"* | `PASS2-ECC-SKILLS.md:645` | **SKILL** | `tenant-isolation` §4 — a cross-tenant leak in a generated app that lints, typechecks and builds |
| P29 | Pin the deletion — of a file, a binary (`lstat`), and a sentence of prompt prose | `PASS2-GSTACK-TESTS.md:718` | **DROP** | already carried — `testing` §5's `negative_fixture` route is the assertion discipline this needs; which `Playbook` sentence to pin is Layer B's |
| P30 | Positive control paired to every absence test | `PASS2-GSTACK-TESTS.md:694` | **DROP** | already carried — `testing` §3 Q1 (*can this test fail?*) and §5's promotion routes are exactly this rule |

**Pairs: 6 SKILL · 11 ADR · 3 FIX · 10 DROP.**

---

## 7 · Rows that touch D, F or G and are owned elsewhere

Listed, not judged. Each names a layer ahead of D, F or G, and the owner of that layer
should triage it.

| Source · line | Tag | Note |
|---|---|---|
| `ECC-SKILLS.md:648` | B · Playbook, E, F | — |
| `ECC-SKILLS.md:656` | C, E, G | — |
| `OTHERS-MINED.md:720` | A, F, B | `datamark()` at the render boundary |
| `OTHERS-MINED.md:730` | A, G | event-sourced decisions; *active* computed, never a mutable status field — bears on F7/P23 |
| `OTHERS-MINED.md:759` | A, F | user-owned fields absent from the model's output schema |
| `PASS2-ECC-RULES-COMMANDS.md:659` | B/F | *"an operation that fails tells the user what failed and what to do next"* — its own instruction is *merge into `app-design` §4*, and §4's Error row already says it. Nothing to do |
| `PASS2-FOUR-REPOS.md:647` | A, D | tri-state *active* predicate that fails open to visible |
| `PASS2-FOUR-REPOS.md:649` | A, G | a violation is findable; the renderer is not where invariants live |
| `PASS2-FOUR-REPOS.md:653` | C, D | every discarded body leaves a visible elision sentinel |
| `PASS2-GSTACK-SKILLS.md:705` | A, G | user-origin gate on preference writes |
| `PASS2-GSTACK-SKILLS.md:707` | A, D | search the library before asking. **The second half — *or say explicitly that nothing matched* — is landed in `contract-retrieval` §3.5 with D3 and D9** |
| `PASS2-GSTACK-TESTS.md:708` | A, F | preference provenance allowlist, unknown source rejected |
| `PASS2-GSTACK-TESTS.md:712` | A, F | split, don't drop, when a UI cap meets a real decision |
| `PASS2-GSTACK-TESTS.md:715` | A, E, G | secret-sink harness, 4 channels × 4 match rules |

---

## 8 · What became a skill — and what was refused one

**Two new skills, three amended, one deferred to a parallel pass.** Seventeen rows became
skill content; they consolidate, because a skill with one rule in it is not a skill.

| Skill | State | Rows |
|---|---|---|
| **`catalog-budget`** | **new** | D8, D26, D27, D28 |
| **`tenant-isolation`** | **new** | G3, G6, P4, P26, P27, P28 |
| `gate-verdicts` | written by the parallel Layer E pass; cross-referenced, not duplicated | P12 |
| `contract-retrieval` | amended — §3.5 and one Limits row | D3, D9, D20 |
| `change-impact-analysis` | amended — §2.6 and E8 | F2 |
| `app-design` | amended — §3 and two §5 rows | F3, P19, and finding 75 (`PASS2-ECC-SKILLS.md:679`) |

### Refused a skill, deliberately

- **No `accessibility-gate`.** `LAYER-F` §5 proposes one, and its substance would come almost
  entirely from §3.8's research rather than from any mined finding — while `app-design` §5
  already owns the deterministic design gate, contrast included. The one finding that is
  genuinely a rule (`PASS2-ECC-SKILLS.md:679` — *`data-testid` is Layer F's anchor, not Layer
  E's selector; a component with no queryable role is the a11y gate failing, and a testid
  hides it*) is a row in that table. A second skill would compete with `app-design` for the
  same request and carry one rule of its own.
- **No `derived-artefact-staleness`.** D12, D16, D17, D18, P1, G2 and G4 are coherent and
  well-sourced, and every one of them is a **requirement of an artefact that does not exist** —
  the derived `Contract` index that `contract-retrieval` §3.4 explicitly defers until the
  catalog crosses ~10³ entries. Requirements for a thing not yet decided are the ADR, not the
  skill. The two rules that generalise past it — the producer belongs *in* the cache key, and
  a snapshot is written only after the artefact is durable and only from the set that
  succeeded — are recorded in `contract-retrieval` §3.4 in one sentence each.
- **No amendment to `testing`.** Three rows aimed at it (P29, P30, and the stricter-double
  case from `LAYER-G` §1.4) and all three are already there: §1(a) *is* the `FakeScope`
  case, §3 Q1 is the positive-control rule, §5's `negative_fixture` is the absence-test
  discipline. Three findings arriving at a skill that already holds them is the strongest
  evidence in this pass that the skill was written correctly.
- **No skill for the unsandboxed preview iframes** (`LAYER-F` §3.0). It is a defect with a
  repair and then a decision: `sandbox="allow-scripts"` is only safe once previews are served
  from a separate origin, which is a Layer G decision about how `previewUrl` is issued. **FIX
  then ADR**, and it is outside the mined corpus — recorded here so it is not lost.

---

## 9 · Counts

| Bucket | D | F | G | Pairs | **Total** |
|---|---:|---:|---:|---:|---:|
| **SKILL** | 7 | 2 | 2 | 6 | **17** |
| **ADR** | 9 | 6 | 3 | 11 | **29** |
| **FIX** | 0 | 2 | 1 | 3 | **6** |
| **DROP** | 12 | 2 | 0 | 10 | **24** |
| | 28 | 12 | 6 | 30 | **76** |

Plus 14 rows in §7, owned elsewhere.

**22% became skill content, and it collapsed into six files — five of them already existing.**
Of the 24 drops, **12 are
"already carried"** — the corpus and the existing skills agreeing, which is a result rather
than a loss. **29 are ADR proposals**, which is the honest shape of a mining pass: most of
what other people built is a decision we have not taken, not a procedure we can adopt.

---

## 10 · Written against a moving skills directory

This pass began with 17 skills and ended with 27: parallel passes over Layers A, B, C and E
were writing at the same time. Four of theirs landed on rows triaged here, and the triage above
is corrected for it rather than written as though they did not exist:

| Their skill | Takes | Rows affected |
|---|---|---|
| `gate-verdicts` (E) | a gate declaring whether it is the enforcement point; a report padding with no-ops | P10 → DROP, P12 → destination changed |
| `provenance-record` (A) | superseded-not-deleted, decay, branching version chains, mutable status fields | F7, F8, F11, F12, P23, P24 — the rule is theirs; the decision stays ours |
| `validation-evidence` (B, C) | empty versus missing versus error, typed three ways | `contract-retrieval` §3.5 defers the general rule and keeps only the retrieval instance |
| `untrusted-text-boundary` (A) | the prompt-injection boundary | `tenant-isolation` §3.3 defers the prompt side and keeps the query side |

**Two things this produced that no single pass would have.** First, three independent readers
arriving at *empty is not missing* — from a matcher, a validator and an impact walk — which is
stronger evidence that the rule is real than any one of them. Second, a measurement: the
always-loaded skills catalog went from **9,275 bytes to 18,212 bytes in one day** (`catalog-budget`
§6 E1), and `testing`'s description crossed the spec's own 1,024-character limit at 1,046 while
nothing was watching. The skill written from D8 caught it on its first run.
