# Layer B and Layer C findings — triage

*Written 2026-08-26. Fifty-six findings from `docs/mined/`, sorted into four buckets.*

Every row carries its source file and line so the original wording can be re-read. Nothing here
is a decision: an **ADR** row is a decision *to be proposed*, not one taken.

---

## How the buckets were decided

| Bucket | Test |
|---|---|
| **SKILL** | a decision procedure — what exists in a domain plus how to choose — or a rule for a recurring situation. It must not settle *what Scio builds* |
| **ADR** | a decision about what to build. Playbook text, a new validation rule identifier, a new model field, a new package state. Goes to `docs/decisions/` later |
| **FIX** | a specific defect with a specific repair, at a named file and line |
| **DROP** | with the reason stated, not implied |

**The governing line, from `docs/next/SKILLS.md`:** *"a skill that quietly decides what we do is an
architecture decision hiding in a markdown file."* This is why the Playbook findings — the largest
single group — are almost all **ADR**. The Playbook is the house rules every generated app
inherits; adding a line to it decides what gets built, in every app, forever. What *is* a skill is
the procedure that decides whether a line may be added at all.

**"SKILL" here means "a rule that lands in a skill", not "a new skill".** Twenty-three findings
become sections or single lines across seven skills. **Two of the seven are new; five already
existed and were amended**, which is the ratio the brief asked for and the overlap gate enforces.

---

## Counts

| Verdict | Count |
|---|---:|
| **ADR** | 21 |
| **SKILL** | 23 |
| **DROP** | 8 |
| **FIX** | 4 |
| **Total** | **56** |

Fifty-one rows come from the index's `B`, `C`, `B/C`, `B/E`, `B/G`, `C/D` and `C/E` buckets. Five
more were recovered by hand:

- **`ECC-SKILLS.md:644`** — the `rules-distill` admission criteria, the single most load-bearing
  finding here. `scripts/findings-index.py` files it under **A**, because its `LAYER` regex is
  case-insensitive and matched the *"a"* in *"promoting a principle to a rule"*. The script's own
  closing note applies: *"Treat counts as a floor, never a total."*
- **`OTHERS-MINED.md:733, 734, 745, 772`** — filed under `— none —` because their layer column
  reads `Playbook` rather than `B`. The Playbook is Layer B's third artifact, so they are Layer B
  findings.

### Two counts corrected while verifying

Verified against `/home/user/hello-world` (read-only) on 2026-08-26:

- **Layer B: eleven rule identifiers from *six* check functions**, not seven.
  `layerb/validate.py:238-249` calls exactly six `_check_*` functions; the seventh name is
  `validate_architecture` itself, which composes them. Seven is **Layer C's** count.
- **Layer C: nine rule identifiers from seven check functions** — confirmed,
  `layerc/validate.py:225-235`.

### Three measurements re-run rather than quoted

| Claim | Measured |
|---|---|
| the rendered Playbook is 668 tokens | **668** — `len(default_playbook().as_prompt_section()) == 2671` chars ÷ 4 |
| `playbook.py:118` passes the whole architecture graph, indented | **confirmed** — `architecture=architecture.model_dump_json(indent=2)` |
| the docstring at `:83` concedes it | **confirmed** — *"for now it assembles the whole architecture."* |

---

## 1 · SKILL — 23 findings, into 7 skills

Two are new. Five were amended in preference to writing more, per the brief and per
`skills-index.py`'s overlap gate. One finding (row 11) turned out to be already carried by a skill
another layer's triage wrote concurrently, and was **not** written a second time.

| # | Finding | Source | Destination |
|---|---|---|---|
| 1 | `rules-distill`'s four admission criteria for promoting a principle to a rule | `ECC-SKILLS.md:644` | **`playbook-admission`** §2 — the skill's spine, taken verbatim |
| 2 | Explicit setting over prohibition; every interpolated path absolute and host-resolved | `PASS2-GSTACK-TESTS.md:713` | `playbook-admission` §4. Both failure modes are silent, and the second's failure mode is *fabrication* (21/21 observed) |
| 3 | A rules document declares its own trade-off and its own success criterion | `OTHERS-MINED.md:772` | `playbook-admission` §6 |
| 4 | Canonical violating fixture per house rule | `PASS2-GSTACK-TESTS.md:710` | `playbook-admission` §5 — *"without them 'does the Playbook work' is an opinion"* |
| 5 | The inert-declaration cross-check, with *"reported, not asserted"* for the unarbitrable | `PASS2-GSTACK-TESTS.md:703` | `playbook-admission` §5. The Playbook is declared in `playbook.yaml` and enforced in a prompt elsewhere — exactly the defect class |
| 6 | Exemptions pinned in both directions; evidence-based, never shape-based | `PASS2-GSTACK-TESTS.md:709` | `playbook-admission` §5 |
| 7 | Prose-regex invariants over prompt templates | `PASS2-GSTACK-TESTS.md:722` | `playbook-admission` §5, with the mined caveat kept: free, catches deletion and drift, **never behavioural coverage** |
| 8 | Validators emit an evidence table, one row per checked pair; no rows = not a scan | `OTHERS-MINED.md:751` | **`validation-evidence`** §2 — the new skill's founding sentence |
| 9 | *"No envelope"* ≠ *"zero results"* — a failed pipeline is not an empty one | `OTHERS-MINED.md:734` | `validation-evidence` §2 |
| 10 | Exit 0 is not evidence: declared lanes + executed-unit count + no failure lines | `PASS2-GSTACK-TESTS.md:697` | `validation-evidence` §2. The planned-count half is what `testing` §3 Q3's three numbers lack |
| 11 | Five outcome states + path-concreteness rule + honesty rule | `PASS2-GSTACK-SKILLS.md:682` | **`gate-verdicts` D2 — already carried.** Written concurrently for Layer E from the same source line. `validation-evidence` calls it and does not restate it; the Layer C half of the finding (*"every acceptance criterion carries how it can be checked"*) is `observed_by` (`criteria.py:67`) and already exists |
| 12 | Claimed limitations need evidence: verbatim error, documented statement, or a live probe | `OTHERS-MINED.md:733` | `validation-evidence` §2.4 — the input side of `gate-verdicts` D2's *"'I don't want to check' is not unreachable"* |
| 13 | TDD Evidence Report table (guarantee · test · type · result · evidence command) | `ECC-SKILLS.md:669` | `validation-evidence` §3 — links a Layer C criterion to a Layer E gate result in something a person can read |
| 14 | Every discarded body leaves a visible elision sentinel; adjacent signatures merged | `PASS2-FOUR-REPOS.md:653` | `validation-evidence` §4. `PackageInterface` (`plan.py:47`) is a signature view with no marker |
| 15 | A package boundary no gate could independently reject is not a boundary | `OTHERS-MINED.md:738` | `design-rule-hierarchy` §2(f) — as a *criterion*, and it conflicts with §2(c) by design. The mined verdict *"take as a validation rule"* would need an ADR of its own, which this triage does not open |
| 16 | Score-then-expand; the scorer may return "do not decompose" | `OTHERS-MINED.md:756` | `design-rule-hierarchy` §2(e) — the declining rule only. The scoring mechanism is `docs/next/LAYER-C-BUILD-PLAN.md` §3.2 |
| 17 | The count is computed by code; the model fills the content | `PASS2-FOUR-REPOS.md:631` | `architecture` §4 — a fourth boundary test, sharper than the three there. None of task-master's constants taken |
| 18 | The seven security triggers (authn/authz, user input, DB query, FS path, external call, crypto, secrets) | `ECC-SKILLS.md:656` | `architecture` §5a. Verbatim; computable from a package's architecture slice |
| 19 | Preservation is an **allowlist** — unknown statuses are preserved | `PASS2-FOUR-REPOS.md:632` | `change-impact-analysis` §2.6 |
| 20 | A delta that changes nothing is a no-op with a distinguishable return | `PASS2-FOUR-REPOS.md:633` | `change-impact-analysis` §2.6 |
| 21 | Name generated tests after the failure they prevent, not the function they cover | `PASS2-ECC-SKILLS.md:653` | `testing` §6a |
| 22 | Regression iron rule + ★/★★/★★★ test quality | `PASS2-GSTACK-SKILLS.md:695` | `testing` §6a — ★ smoke tests do not satisfy a contract |
| 23 | Motion admission test (guide attention / communicate state / preserve continuity, else remove) | `PASS2-ECC-SKILLS.md:676` | `app-design` §4a. A four-way admission test, which is decision-procedure shaped |

**One finding sits next door and is deliberately not in this table.** *"Minimum-substance guards
belong in the type, not only in the prose"* (`OTHERS-MINED.md:760`) is **ADR A16** — it changes a
Layer C contract type. Its *principle* is already the prior question in `playbook-admission` §3
route 2, where it appears as a worked example. Citing a finding inside a skill is not the same as
promoting it, and the counts above treat only the second as a SKILL verdict.

### The skills

| Skill | New or amended | Layer |
|---|---|---|
| `playbook-admission` | **new** | B |
| `validation-evidence` | **new** | B, C |
| `architecture` | amended — §4 fourth boundary test, §5a security triggers | B, build-process |
| `design-rule-hierarchy` | amended — §2(d) write-surface test, §2(e) declining splitter, §2(f) review boundary | C |
| `change-impact-analysis` | amended — §2.6 applying the delta; `layer` widened to C | C, F |
| `testing` | amended — §6a two rules for a plan-demanded test; `layer` widened to C | C, E, build-process |
| `app-design` | amended — §4a motion admission test | B, F |
| `gate-verdicts` | **not modified** — already carried row 11 from the same source line | E |

`design-rule-hierarchy` §2(d) is the general form of **FIX F4**: the write-surface test is what
makes `parallelizable` computable rather than asserted. The rule lives in the skill; the repair
lives in `decompose.py`.

---

## 2 · ADR — 21 findings

All of these decide what gets built. **None was written into a skill.** Each needs an ADR in
`docs/decisions/`, and every Playbook row must first clear `playbook-admission` and be priced.

### 2.1 Playbook content — 11 findings

The Playbook is **668 tokens today**, is byte-identical for a restaurant booking app and a B2B
tender platform (`docs/as-built/LAYER-B-UNDERSTANDING.md` §3 marks it `constant`), and enters
**every package prompt on every build**. A prior proposal took it to 961 against a ~1,200 cap
(`PASS2-ECC-RULES-COMMANDS.md:662`). These eleven cannot all land.

| # | Finding | Source | Note |
|---|---|---|---|
| A1 | *"No mutable module-level state in RSC/SSR"* (~22 tok) | `PASS2-ECC-SKILLS.md:645` | **Strongest of the eleven.** A cross-tenant leak that lints, typechecks, builds and passes `_UNSAFE_PATTERNS` — so no linter can take it |
| A2 | `USING ((SELECT auth.uid()) = user_id)` — evaluate the auth call once, not per row (~30 tok) | `PASS2-ECC-SKILLS.md:647` | Attaches to `secure_by_default`; same upstream `LAYER-B` §525 already marks *adopt* |
| A3 | Idempotent write/job/webhook retries; verify the webhook signature before parsing (~34 tok) | `PASS2-ECC-SKILLS.md:658` | Absent from `secure_by_default`. Required the moment a generated app takes payments |
| A4 | Request schemas **reject** unknown keys rather than stripping them (~20 tok) | `PASS2-ECC-SKILLS.md:677` | Mass assignment. One flag apart from the permissive default every framework ships (`.strict()` in a Zod stack) |
| A5 | `font-variant-numeric: tabular-nums` on counters, timers, prices, tables (~18 tok) | `PASS2-ECC-SKILLS.md:674` | **Replaces**, does not extend: it supersedes the vaguer "stable responsive dimensions" line from `ECC-SKILLS.md:649`. Net cost ≈ 0 |
| A6 | 40×40px minimum hit target, 44×44 preferred (~26 tok) | `PASS2-ECC-SKILLS.md:673` | Near-computable against Tailwind output. Should be a seventh `app-design` §5 gate check *before* it is a Playbook sentence |
| A7 | `react-patterns` decision trees (state location, data fetching, hooks defaults, RSC boundaries) | `ECC-SKILLS.md:645` | Largest of the eleven and the least priced. The source names no React version |
| A8 | `frontend-design-direction`'s three lines (usable-experience-first, no cards-in-cards, stable responsive dimensions) | `ECC-SKILLS.md:649` | One of the three is superseded by A5 before it lands |
| A9 | Refusal message shape: problem · cause · fix · what-this-is | `PASS2-GSTACK-TESTS.md:705` | **Decide once.** The same shape answers `docs/next/LAYER-C-BUILD-PLAN.md` §3.1's open question about what a user sees when a plan is invalid |
| A10 | Hydration family as one Playbook line (module-scope `window`/`navigator`, server/client render parity) | `PASS2-ECC-SKILLS.md:675` | The *grep* half of this finding is FIX 2. Only the residue that no grep catches is Playbook text |
| A11 | The hydration line's companion — `onUnhandledRequest: "error"` in generated test setup (~16 tok) | `PASS2-ECC-SKILLS.md:678` | **Should not be prompt text at all.** It is config the scaffold writes once, at zero prompt tokens — blocked on the foundation package actually owning a test runner (`decompose.py:73` advertises one it does not build) |

### 2.2 Architecture and emitter — 4 findings

| # | Finding | Source | Note |
|---|---|---|---|
| A12 | Schema types: `bigint` ids · `text` not `varchar(n)` · `timestamptz` · `numeric` for money | `PASS2-ECC-SKILLS.md:648` | **The cleanest instance of the prior question in the corpus.** Layer B types the schema in `derive.py` before any prompt exists; prompt text here would be a rule a generator could have guaranteed |
| A13 | `COMMENT ON COLUMN … IS 'PII: …'` — sensitivity labels surviving into the generated database | `PASS2-ECC-SKILLS.md:666` | Turns four leak-vector name heuristics into decidable checks. Layer B has the classification and nothing carries it downstream |
| A14 | Cross-tenant read returning zero rows, generated beside every RLS policy | `PASS2-ECC-SKILLS.md:667` | The evidence half of `docs/next/LAYER-B-UNDERSTANDING.md` §3.5 (CVE-2025-48757). **Blocked on FIX 3** — `isolation_script` (`scripts.py:189`) exists and never arms |
| A15 | `data-testid` on every interactive and list element, derived from `PackageInterface` | `ECC-SKILLS.md:648` | The *principle* (a derivable identifier is never model-chosen) went to `architecture` §4. The decision to emit one, and its collision with RTL's query priority (`PASS2-ECC-SKILLS.md` §1.8), is the ADR |

### 2.3 Plan model and validation — 4 findings

| # | Finding | Source | Note |
|---|---|---|---|
| A16 | `No Placeholders` rejection list + minimum-substance constraints in the contract type | `OTHERS-MINED.md:739`, `:760` | Two halves of one decision: the list extends `contract_complete`, the constraints go in the type. Both mechanically checkable |
| A17 | `Consumes`/`Produces` bipartite completeness check as a new rule identifier | `OTHERS-MINED.md:735` | The block itself already exists — `PackageInterface` + `depends_on`. The **check** is new, and it is what `contract.py:160`'s import-boundary section was written from |
| A18 | `Must not:` as an eighth field on an acceptance criterion | `ECC-SKILLS.md:660` | The authoring rule is already `ears-requirements` §6 (the `IF … THEN` unwanted-behaviour pattern, *"the half hand-written criteria omit"*). The **field** is the decision, and it must be derivable by Layer B, not authored by a model |
| A19 | *"Already satisfied"* as a first-class outcome at both ends — C may emit a no-build package, E may close one without change | `PASS2-FOUR-REPOS.md:630` | Layer D's assembly match and this outcome are one state, currently modelled twice |

### 2.4 Build process — 2 findings

| # | Finding | Source | Note |
|---|---|---|---|
| A20 | Size classifier → gate mask; three signals, highest wins, user-overridable, tier stated aloud | `ECC-SKILLS.md:655` | Whether gates become skippable by size is a cost decision. Its **principle** — *"a model may not set ceremony any more than it may set membership"* — went to `architecture` §4 |
| A21 | Per-stack ordered gate pipeline with stop-on-fail | `ECC-SKILLS.md:647` | Shape only; all four source texts are for repos we did not write. Pairs with `docs/next/LAYER-C-BUILD-PLAN.md` §3.1's VAL result: *the first failing rule is the message* |

---

## 3 · FIX — 4 findings

| # | Finding | Source | Repair |
|---|---|---|---|
| F1 | Leak vectors as greps: no identifiers in URLs, browser storage, logs or client errors; no `service_role` key client-side | `PASS2-ECC-SKILLS.md:668` | **Not Playbook text**, despite the mined verdict *"take the text (~40 tok)"*. `ECC-RULES.md` §4 item 2 already names the repair: regex lines in `builder/validation.py`'s `_SECRET_PATTERNS` / `_UNSAFE_PATTERNS`, in a file that already has severity semantics, the fix-instruction loop and tests |
| F2 | Module-scope `window`/`navigator` — the grep half of the hydration family | `PASS2-ECC-SKILLS.md:675` | One multiline regex in `_UNSAFE_PATTERNS`. Four rules, three files, no file named "hydration": `rules-distill` criterion 1 satisfied and never acted on |
| F3 | `criterion_vague` over a term blacklist, warning severity | `ECC-SKILLS.md:661` | ~20 lines in `layerc/validate.py`. A real hole: *"works correctly and is secure"* passes `criterion_observable` today |
| F4 | `parallelizable` is a claim, not a computation | `PASS2-ECC-SKILLS.md:665` | `decompose.py:442` documents *"packages that share no dependency path with a sibling of the same kind"* and implements `len(group) > 1` — internal drift item 4 in `docs/as-built/LAYER-C-BUILD-PLAN.md`. The repair is a reachability query over `plan.graph` **plus** the mined test: two packages may build in parallel exactly when their file plans are disjoint. The general rule went to `design-rule-hierarchy` §2(d) |

---

## 4 · DROP — 8 findings

| # | Finding | Source | Reason |
|---|---|---|---|
| D1 | The 39 `-patterns`, 12 `-testing`, 7 `-security` snippet libraries as Playbook content | `ECC-SKILLS.md:674` | Already **leave** in the source. Cookbooks at 80–88% code fence; taking one takes a stack decision `CLAUDE.md` forbids |
| D2 | The sixteen-skill cluster B (`iterative-retrieval`, `blueprint`, `token-budget-advisor`, …) | `PASS2-ECC-SKILLS.md:685` | Already **leave**. Personas with checklists, or ECC's own installer surface |
| D3 | `regex-vs-llm-structured-text` deterministic-first, escalate on low confidence | `ECC-SKILLS.md:678` | Already **leave**. Scio does it better and states it: *"never fails the plan: any error, and the deterministic grouping stands"* (`judgment.py:74`). The source's 95–98% is unsourced |
| D4 | `## Global Constraints` — spec-wide requirements copied verbatim into every package prompt | `OTHERS-MINED.md:736` | Split and both halves already placed. The **constant** half ships today — scope guard, vocabulary and Playbook travel into every package, asserted by `test_the_scope_guard_travels_into_every_package`. The **requirements** half is blocked on requirement objects existing at all, which is `docs/next/LAYER-B-UNDERSTANDING.md` §3.3 and already an open proposal. Nothing left to record |
| D5 | Monotone dependency ordering in the prompt **and** a cycle check that doesn't trust it | `OTHERS-MINED.md:757` | Both halves exist and neither involves a prompt. Kahn with id tie-break (`decompose.py:418`), `acyclic` (`validate.py:63`), `order_respects_dependencies` (`:191`). Scio's order is never model-emitted, so there is nothing to distrust |
| D6 | At least one package with an empty `Consumes`, or the plan is deadlocked | `OTHERS-MINED.md:758` | Mathematically subsumed. In a finite directed graph where every node has at least one out-edge there is a cycle, so `_check_acyclic` already fires on exactly this condition. A second rule id would report the same defect twice |
| D7 | Four-part agent brief: scope · goal · explicit constraints · specified output shape | `OTHERS-MINED.md:755` | The mined note says *"ours carry two of four"*; `contract_prompt` (`contract.py:142-199`) carries all four and five more — goal, architecture slice, dependency interfaces, import boundary, why, vocabulary, scope guard, done-when, house rules. The one weak part, the output shape, is already recorded as documentation drift item 5: `contract.py:168` promises a file list that only `codegen.build_prompt` (`builder/codegen.py:149`) appends |
| D8 | Red-flag / rationalization tables — excuses paired with rebuttals, not rules | `OTHERS-MINED.md:745` | A presentation form, not a decision procedure. Its function is already carried: `architecture`'s **disqualified when** column and `testing` §3's *"automatic fails, greppable"* list are both this shape, arrived at independently |

---

## 5 · What this triage deliberately did not do

- **It did not add a single line to the Playbook.** Eleven candidates are recorded as ADR rows with
  a token price each; the skill that governs admission was written first, on purpose.
- **It did not promote the Playbook findings that a linter, a type, a config file or the generator
  could guarantee.** Four moved to FIX or to the emitter instead. `ECC-RULES.md` §4's count stands
  behind that: fifteen ECC rules are lint config typed into prose and eleven more are *already*
  checks in `builder/validation.py`.
- **It did not open the question of whether Layer C's validation should gate.** Nine good rule
  identifiers, and `docs/as-built/LAYER-C-BUILD-PLAN.md` verified that no runtime caller reads the
  result while ADR-0013 says a plan is *"validated … before building"*. That is `docs/next/LAYER-C-BUILD-PLAN.md`
  §3.1's ADR-C-1, it is a product decision about what a user sees, and it is not a finding's to
  settle. `validation-evidence` gives it a reporting vocabulary; it does not decide it.
