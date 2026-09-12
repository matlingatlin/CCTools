# Third arm · what the mining added over our own analysis

**Date:** 2026-08-26. Four skills: `gate-verdicts`, `tenant-isolation`, `testing`, `run`.
This is the second of the third-arm files; `THIRD-ARM-1.md` covers a different four.

Twenty-six two-arm ablations were run today — *skill* against *no skill*. Eighteen changed an
outcome. None of them can answer the question this file exists for:

> **Did reading eight external repositories add anything, over what we already knew from
> analysing our own predecessor system?**

Several winning skills mix two origins. `testing` is built from **our own** three confirmed cases
of tests passing for the wrong reason, and its exit-code and planned-count rules are **mined**.
`tenant-isolation` carries a CVE we found ourselves, an ordering rule verified in our own
`build.service.ts`, and a rows-versus-columns section that came out of ECC's Ruby and PHP
directories. A two-arm test shows only that the mixture beats nothing.

So: three arms, the same question each ablation already used.

| Arm | Directory | What loads |
|---|---|---|
| **A · control** | `…/scratchpad/baseline` | `CLAUDE.md` + `docs/as-built/`, no project skills |
| **B · ours-only** | `…/scratchpad/oursonly-2` | same, plus all 27 skills — with the four under test **stripped of every mined rule** |
| **C · full** | `/home/user/scio` | the skills as written, in the live repo |

---

## Method, and how origin was decided

### The arms, verified

`baseline/` and `oursonly-2/` carry a byte-identical `CLAUDE.md` — identical also to
`/home/user/scio/CLAUDE.md` — and a `docs/as-built/` that differs in **exactly one line** of
`ARCHITECTURE-AS-BUILT.md`: `baseline` predates a correction and says *"`validate_plan` — nine
rules, every build"* where `oursonly-2` and `scio` say *"nine rule identifiers from seven check
functions"*. Nothing in any of the four questions touches `validate_plan`. It is recorded because
an unstated difference between arms is how a measurement stops being one.

`oursonly-2/` additionally carries all 27 skills. Before stripping, `diff -rq` against
`/home/user/scio/.claude/skills/<name>` reported **identical** for all four skills under test. The
other 23 were left untouched.

Nothing under `/home/user/scio/.claude/skills/` was modified. All stripping happened inside
`oursonly-2`. Nothing was committed or pushed.

### How a rule's origin was decided

By evidence, in this order:

1. **The skill's own `## 1 · Source` section**, which in three of these four names the file and
   often the line in `docs/mined/` that each mechanism came from. `gate-verdicts` has an
   eleven-row table doing exactly this; it made the strip nearly mechanical.
2. **A grep of the rule's distinctive phrase across `docs/mined/`, `docs/as-built/` and
   `docs/next/`.** In `docs/mined/` and nowhere in the other two → mined. In `docs/as-built/` or
   `docs/next/` with a `file:line` in `/home/user/hello-world` → ours.
3. **Where both, keep it and say so.** Two cases below are marked as such.

**Published papers are not "mined".** `testing` rests on Lin et al. (ISSTA 2026), Inozemtseva &
Holmes, Papadakis et al., Zhao et al., Luo et al., the pytest documentation, axe-core's README;
`tenant-isolation` rests on the Zanzibar paper, CVE-2025-48757, PlanetScale, Atlas and pgTAP. None
of those is one of the eight repositories, and none appears in `docs/mined/`. They stayed in arm B.
The question under test is what *reading eight repositories* bought, not what reading anything
outside the repo bought. Where that boundary matters to a result, it is said again below.

### What a strip is allowed to touch

Whole rules and their headings were deleted. Where deletion left a dangling reference — a heading
that promised "five decisions" when one survived, a lettered `(d)` with no `(a)`, a limits bullet
about a section no longer present — the reference was repaired, and every repair is listed with its
before and after alongside the removals. **Skill descriptions were stripped too**, of the trigger
clauses that name a mined-only mechanism, because a description clause is a rule about when to
fire. The full verbatim removal records are at
`…/scratchpad/thirdarm2/removed-{gate-verdicts,tenant-isolation,testing}.md`.

### Running

```bash
cd <arm directory> && timeout 300 claude -p "<question>"
```

One run per arm per skill; twelve in total. The question for each skill is the one its existing
ablation file already used, so arm C is comparable to what was measured this morning. For
`testing` that is the **second** question — the first was recorded as no difference.

### Confounds, stated once

- **`graphify` loads at account level in all three arms**, along with `session-start-hook`. It is
  not controlled for anywhere in this series.
- **Arm C is the live repo.** It carries `docs/next/`, `docs/mined/`, `docs/decisions/`,
  `docs/triage/`, `scripts/` and `scio.db`; A and B carry only `CLAUDE.md` and `docs/as-built/`.
  So a C answer that cites a number from `docs/next/` may be citing the corpus rather than the
  skill. Where that happens it is marked.
- **n = 1 per cell**, unblinded, graded by the person who did the stripping.

---

## `gate-verdicts` — what was stripped, verbatim

This is the most heavily mined of the four, and its own `§1 · Source` says so: *"Not a paper.
Twenty-five findings mined from eight external repositories on **2026-08-26** … plus this
repository's own verified defects."* Eleven mechanisms are listed with the `docs/mined/` file and
line each was read at. **Four of the five decisions came out whole.** The file went from 12,056
characters to 3,926 — a 67% cut — and three of its four `references/` files were deleted outright.

### Removed, with origin

| Unit | Lines | Origin |
|---|---|---|
| §1's mined source table, all 11 rows | 23–39 | `docs/mined/` — the table names them |
| **D1 · Is PASS reachable, and only through the last check?** | 51–66 | `PASS2-GSTACK-SKILLS.md:83` (`codex`), `:108` (`freeze`) |
| D2's second paragraph — path-concreteness and the honesty rule | 74–77 | `PASS2-GSTACK-SKILLS.md:199` (`review`) |
| **D3 · A number, or a verdict?** and the score cap | 78–88 | `PASS2-ECC-SKILLS.md:369`, `PASS2-ECC-RULES-COMMANDS.md:697` |
| **D4 · What evidence must travel with the verdict?**, all six bullets | 89–102 | gstack `review` (quote gate, confidence bands, missing voice), `OTHERS-MINED.md:752` (superpowers), `:68` (scan-at-sink), `PASS2-ECC-SKILLS.md:669` |
| **D5 · What does the gate say about itself?**, all four declarations plus the two report rules | 103–120 | `PASS2-GSTACK-SKILLS.md:129`, `:693`, `:238`; `PASS2-ECC-SKILLS.md:443`, `:680`; `PASS2-FOUR-REPOS.md:545` |
| Two limits rows and one ADR item (pruning on measured hit rate) | 127–128, 130, 140 | all about the mined corpus |
| The honesty-rule paragraph | 143–146 | describes the shape D1/D3/D4 impose |
| Evals E1, E2, E4, E5, E7, E8, E9 | 153–159, 163–170, 175–184 | each asserts a removed rule |
| `references/fail-closed.md`, `references/scores-and-caps.md`, `references/gate-self-declaration.md` | whole files | D1, D3, D5 |
| `references/outcomes.md` — everything except its `## Ours` section | | gstack `review`'s five states, `loop.service.ts`, path-concreteness, the ECC status column |

The load-bearing sentences, verbatim as they stood:

> Write the checks as an **ordered list where the first match wins, with no default branch**. PASS is
> the last entry and nothing falls through to it.

> *"No `[P1]` substring and no critical findings are different claims — never infer PASS from an
> untagged body."*

> The same polarity governs boundaries: a payload the check cannot parse is DENIED. **A boundary
> that fails open is not a boundary.**

> **Use a score only where a gradient is needed — convergence, ranking, "is this getting better".
> Use a verdict plus a checklist for a decision.**

> Where a score does exist beside deterministic checks, the deterministic checks set a **cap** the
> judgement may not exceed. Binary conditions establish a ceiling; the score may only move below it.

> - **A finding quotes the line that caused it** — file, line, and the verbatim text. If it cannot,
>   the finding is unverified and is suppressed or demoted.
> - **An agent's success report is not evidence.**
> - **A check runs on the bytes that travel**, not on an earlier copy of them.
> - **Low confidence is labelled and demoted, never deleted.**
> - **A missing voice is N/A, never agreement.**
> - **The status carries a *what must be true to say this* column.**

> 1. **Enforcement point or not.** … 2. **Non-scope.** … 3. **Its error contract** … 4. **A
> suppression list** … And two rules about the report itself: **omit principles you checked but did
> not change** … and **a degraded run carries its own disclosure into its output**.

### Kept, and why

- **§1's "Our own instances, verified at source"** — `check_tests_present` matching the substring
  `test` so `app/latest/page.tsx` satisfies it (`validation.py:132`); `checks_passed` computed,
  typed, transmitted and shown nowhere; the two interaction gates opt-in behind `SCIO_VERIFY_DATA`
  with 0 `interaction` criteria. All three trace to `docs/next/LAYER-E-BUILD.md` §1.1, §2.4.
- **D2's first paragraph — the outcome vocabulary.** *"This repository already has the vocabulary
  in types — `passed / needs_look / failed / blocked`, `Remainder`, `unjudged` — and the rule is
  that `unjudged` never rounds up."* **Both, independently:** the boolean-is-not-enough framing is
  in the mined `review` set as well, but our own vocabulary is in *types*, and two invariants are
  already enforced and tested — *an unreadable verdict is a failure, never a pass* (`critique.py:134`)
  and *nobody looked ≠ it passed* (`loop.py:696`). It survives the strip on our evidence alone.
- **E3** (a boolean cannot carry *could not run*) and **E6** (the substring test — `validation.py:132`
  as an eval).
- The ADR list's first two items and §5's routing.

### Repairs

`This skill is the five decisions…` → `the decision`; `## 2 · The five decisions` → `## 2 · The
decision`; the `→ references/outcomes.md` pointer moved out of the deleted D2 paragraph into the
kept one; *"Written 2026-08-26 from `docs/mined/` read at source"* deleted from the footer; the
three-item ADR list renumbered. Description clauses naming a mined mechanism removed: *"and when a
pass is reachable at all"*, *"when a tool returns empty or untagged output"*, *"when a number is
about to be attached to a judgement"*, *"when deciding whether a gate is the real enforcement
point"*, *"when a report pads itself with things it checked but did not change"*, *"when a reviewer
is about to be handed the whole build transcript"*, *"when an absent reviewer is about to be counted
as agreement"*, *"when a finding is emitted without quoting the line that caused it"*.

---

## `tenant-isolation` — what was stripped, verbatim

The cleanest split of the four, as expected. The CVE, the Zanzibar comparison, the ordering rule,
the four RLS traps and the zero-rows assertion are ours or published; the sensitivity labels, the
leak vectors, the SQL-injection instance and **§4b in its entirety** are mined. 24,090 characters
to 17,518 — a 27% cut.

### Removed, with origin

| Unit | Lines | Origin |
|---|---|---|
| §1's `**Mined:**` paragraph | 54–58 | names its own sources |
| §3.3 · Identifiers derived from user text are query parameters | 119–127 | `PASS2-FOUR-REPOS.md` P2-17 — claude-context `context.ts:504-521`, a live defect in *their* repo |
| §4.2 · Sensitivity labels that survive into the database | 158–177 | ECC `healthcare-phi-compliance`, `PASS2-ECC-SKILLS.md` rows 41, 62, 63 |
| §4.3's `CREATE POLICY "facility_isolation"` illustration | 180–185 | the same ECC skill; the rule around it is ours and was kept |
| §4.4 · Leak vectors that lint, typecheck and build cleanly | 195–203 | ECC `react-performance`; gstack's refuse-rather-than-widen |
| **§4b · RLS decides which rows, never which columns**, entire | 205–243 | `PASS2-ECC-RULES-COMMANDS.md` §2.1 — `ruby/security.md` and `php/security.md` |
| §6.1's rule statement and its gstack egress-test quote | | gstack, via `gate-verdicts` D5 — itself mined |
| §6.1's companion non-scope-list rule | 305–306 | `gate-verdicts` D5 |
| §6.3's three layers for one privacy promise | 319–327 | gstack |
| §7's limits bullet on the sensitivity-label mechanism | 350–352 | about the removed §4.2 |
| E7 · A labelled column in a leaky place | 396–400 | asserts the removed §4.2 |

§4b verbatim, because it is the one this experiment was built to isolate:

> ## 4b · RLS decides which rows, never which columns
>
> A row-level policy answers *may this user touch this row*. It has no opinion about **which fields
> of that row they may set**. So a handler that writes a payload straight into an update lets a user
> change their own row's `role`, `owner_id` or `workspace_id` — and every policy passes, because the
> row was always theirs.
>
> That is **mass assignment**, and it is the same failure as the CVE at a different granularity: the
> CVE is *no policy*; this is *a correct policy asked the wrong question*.
>
> **Two mechanisms, and you need both.**
>
> 1. **An explicit writable-column allowlist per operation**, derived from the architecture rather
>    than hand-maintained. A field absent from the allowlist is dropped, not rejected — rejecting
>    tells an attacker the field exists.
> 2. **`WITH CHECK` on every write policy, not only `USING`.** This is the trap: `USING` filters
>    *which rows are visible*, and a policy with `USING` alone will happily let a user `UPDATE` a row
>    **out of their own tenant and into another**. The row passed the read check on the way in;
>    nothing checked it on the way out. `WITH CHECK` is what validates the *resulting* row.
>
> **The assertion that catches it**, beside the zero-rows cross-tenant test in §4:
>
> > As tenant A, update your own row setting `workspace_id` to tenant B's. **The write must fail**,
> > and a subsequent read as tenant B must return zero rows.

**A judgement call, stated so it can be disputed.** The `WITH CHECK` half of §4b is not in
`docs/mined/` — ECC's two lines say only *"use strong parameters or typed boundary objects before
mass assignment"* and *"whitelist writable fields"*. `WITH CHECK` is our own elaboration. But §4b
exists **only because** the mined finding named the gap — the phrase *"column-level twin of
CVE-2025-48757"* is `PASS2-ECC-RULES-COMMANDS.md:135`, written by the miner, and the section's own
dateline says it was added after an ablation found the skill *"cites CVE-2025-48757 three times and
never names its column-level twin"*. Origin is the seed, not the elaboration, so the whole section
went. Reading it the other way would credit arm B with a rule that would not have been written.

### Kept, and why

- **The whole of §3** minus §3.3 — the load-bearing count (`WORKSPACE_SCOPED_MODELS` is six of
  fourteen models; seven more protected by a convention at 26 call sites), the ordering rule and
  the F-03 replay defect verified at `build.service.ts:517-525`, the ledger reduction key, and
  404-not-403 at `project.service.ts:30`.
- **§4.1** — `row_level_security: bool = True` with no code path that sets it false, and
  `scope: str` with the enumeration in a comment. Ours, at `architecture.py:49`, `:83`, `:144`.
- **§4.2 (renumbered from 4.3) · the zero-rows assertion.** Ours plus published: `LAYER-B` §3.5
  holds the deterministic half, and the second canonical assertion — the plan still uses a
  tenant-leading index — is pgTAP and Atlas, not one of the eight repos.
- **§5 and §5.1** — Zanzibar (paper), the enforcement-point table, and the four traps, three of
  which are quoted from our own `library/verification/client.ts:18-23`.
- **§6.1's two instances** (`ci.yml` passes, `tenant-discipline.spec.ts` fails), **§6.2** (`FakeScope`
  versus `applyWorkspaceScope`), **§6.3's instrument** (`verification/client.ts` runs only under
  `SCIO_VERIFY_DATA=1`), and evals **E1–E6, E8**.
- **CVE-2025-48757 and its two scores.** Ours — found in our own scan, not in `docs/mined/`.

### Repairs

§6.1's opening rewritten to drop the gstack attribution and stand on our two instances; §6.3
retitled *"The strongest check in the system is off by default"* and its *"layer 1 at best"* tail
rewritten to *"a claim, not a control"*, since the layer numbering it referred to was gstack's;
§4.3 renumbered to §4.2. Description clauses removed: *"sensitivity labels that survive into the
generated database"* and *"and the leak vectors that lint, typecheck and build cleanly"*.

---

## `testing` — what was stripped, verbatim

The brief's description holds exactly. §1's three confirmed cases of tests passing for the wrong
reason are ours, verified at `file:line` in `/home/user/hello-world`. §5's asymmetric rule is ours,
carried from `docs/next/LAYER-E-BUILD.md` §3.1. §7's skipped-test rules are ours — *"27 passed, 9
skipped"* is our own `test_interaction_channel.py`. **The exit-code rule and the planned-count rule
are mined**, and they are the two halves of §9.5(a). 51,684 characters to 34,779 — a 33% cut.

### Removed, with origin

| Unit | Lines | Origin |
|---|---|---|
| §2's two mined-source paragraphs | 103–113 | gstack's test suite; claude-task-master's `TestResultValidator`; `pass@k`/`pass^k`; the test-naming rule |
| Q3's second paragraph — **the planned count** | 153–158 | gstack, via §9.5(a) |
| **§3.5 · If it asserts an absence, where is its permanent positive control?** | 167–217 | `PASS2-GSTACK-TESTS.md` §3.1 (`secret-sink-harness.ts`) and #16 |
| §6's browser rules (auto-waiting locators, traces on failure) | | `ECC-SKILLS.md:673` |
| §6's test-naming rule | | `PASS2-ECC-SKILLS.md:653` |
| **§6a · Two rules for a test the build plan asked for** — the naming rule, the regression iron rule, the ★/★★/★★★ levels | 326–384 | `PASS2-ECC-SKILLS.md:653`; `PASS2-GSTACK-SKILLS.md` §5.5 |
| §8's `pass@k` versus `pass^k` paragraph | 435–439 | `ECC-SKILLS.md:671` |
| §9's rule 6 and the guarantee-table rendering | 476–484 | claude-task-master; `ECC-SKILLS.md:669` |
| **§9.5's intro and (a), (b), (c)** | 489–565 | gstack exit-0 truncation; claude-task-master's six arithmetic checks; gstack's evidence ledger |
| §9.5(d)'s gstack quote only | 570–572 | gstack `PASS2-GSTACK-TESTS.md` §2.9 |
| §11's limits bullets on §6a and on §9.5 | | about removed sections |
| Evals E10–E15 | 713–745 | each asserts a removed section |

The two that decide this skill's result, verbatim:

> **And a fourth number: how many units were *planned*.** A zero exit code is not the answer to this
> question, and §9.5 is why — a truncated run is indistinguishable from a green one by exit code
> alone. A claim that "the tests passed" is three claims, and all three must be checked: the lanes
> that were declared ran, the executed-unit count matched the planned count, and no failure line was
> printed.

> ### (a) Exit 0 is not evidence
>
> From `gstack`… Their runner ran every test file in one process; a `setTimeout` armed in an
> `afterAll` fired mid-way through a *later* file and killed the suite:
>
> > *"the armed timer fires 500ms later, mid-way through a LATER test file, and kills the entire suite
> > with exit code 0 and no summary. The truncated run silently masks every downstream failure
> > (**observed: only ~16 of 434 files ran, shell exit 0**)."*
>
> **96% of a suite skipped, green.** … The fix refuses a zero exit when any of three hold: failure
> lines were printed; **fewer files ran than were planned** — *invisible non-execution*; or an
> unhandled error fired between tests. Which means **the harness must know how many units it planned
> to run.**

And §9.5(b), which is the other candidate for what the mining bought here:

> | `passed + failed + skipped == total` | a fabricated summary usually gets this wrong |
> | a red phase must have `failed >= 1` | tests written first that already pass are not testing the new behaviour |
> | a red phase must have `total >= 1` | *"I wrote tests"*, with zero tests |
> | a green phase must have `failed == 0` | — |
> | a green phase must have `passed >= 1` | zero failures is trivially true of an empty suite |
> | `total < previous_total` ⇒ flagged | tests deleted to make the suite pass |
>
> **Four integers make the two cheapest ways to fake a green build — write no tests, delete the
> failing ones — detectable without reading a line of code.**

§3.5's law, removed whole:

> ***"Positive-control discipline: every test suite using this harness should include one test that
> deliberately leaks a seed and asserts the harness catches it. A harness that silently
> under-reports is worse than no harness."***

### Kept, and why

- **§1, all four failures**, at `file:line` in `/home/user/hello-world`.
- **§2's papers.** Lin et al., Inozemtseva & Holmes, Papadakis et al., Zhao et al., Luo et al., the
  pytest docs, axe-core's README, Testcontainers, Pact, verified fakes. None is one of the eight
  repositories; see the method note above.
- **§3 Q1, Q2, Q4** and Q3's first paragraph — *"Three numbers, always: ran / passed / skipped"*,
  which is §7 and is ours.
- **§4 · the double-versus-production rule.** §11 already says it is ours: *"I found no paper
  measuring the stricter direction… §4's symmetric requirement is therefore ours, argued from
  `FakeScope` and `test_sandbox_conformance`'s own docstring."*
- **§5 · the asymmetric rule**, with its three promotion routes and the Lin et al. citation.
- **§7 · skipped tests**, all six rules.
- **§8 · flakiness**, minus the `pass@k` paragraph — B105 and the 8-green-runs bound are ours.
- **§9's contract and rules 1–5.**
- **§9.5(d)** — *"the harness does not inherit the machine"*. **Both, independently:** the gstack
  quote went, and the rule stands on our own instance — *"the child was once started with
  `**os.environ` while it held the platform's API key, and a conformance suite proves it for every
  provider (`sandbox.py:105`)."*
- **§10, §11, §12's E1–E9 and E16, §13.**

### Repairs

§3's heading lost *"and a fifth for absence tests"* and its intro lost the §3.5 pointer; §9.5's
mined four-ways intro replaced with one sentence and `### (d)` de-lettered; E16's *"§9.5(d) and
§3.5"* → *"§9.5"*; §11's two bullets about removed sections deleted; §9.5(d)'s trailing *"Their
comment on why it is one"* clause trimmed. Description clauses removed: *"when naming a test"*,
*"when a regression is found"*, *"when a build plan demands one"*, *"when a test asserts that
something is absent or never happens"*, *"when a rule gains an exemption"*, *"when a run exits zero
and someone calls that evidence"*, *"when a model or an agent reports test counts"*.

---

## `run` — nothing was stripped, and that is the finding

**Arm B equals arm C for this skill.** `diff -rq` reports the two files identical, deliberately.

The brief asked whether *anything* in `run` is mined. The answer is no, and the evidence is that
the mining documents themselves treat `run`'s rules as **pre-existing ours** and argue against or
around them. Every mention of `run` in `docs/mined/` is one of these:

| `docs/mined/ECC-AGENTS.md` | What it says |
|---|---|
| `:156` | *"writing partial results to disk" from `run/SKILL.md` §5 — implemented, in an agent, by them* |
| `:333` | *"`run/SKILL.md` §5 says 'budget before parallel work…'"* — quoting us to compare |
| `:353` | *"**Our** §5 rule *budget before parallel work* is the direct contradiction, and ours is right"* |
| `:377` | ECC's per-batch budget is *"'budget before parallel work' in eleven lines"* |
| `:635` | ECC's *"ALWAYS use parallel Task execution"* — **leave, actively.** *"Directly contradicts `run/SKILL.md` §5. Ours is right"* |

There is exactly one proposal to put mined content *into* `run` — item 22 of `ECC-AGENTS.md`'s
verdict table, the **Delegation Completion Contract** (*"if you delegate, you own collection"*,
*"depth is an outcome, not a plan"*), earmarked for §5 *"which covers dispatch and not collection"*.
**It has not landed.** `grep -i "delegat\|collection\|depth is an outcome" run/SKILL.md` returns
nothing. The proposal is still a proposal.

Everything the question reaches is ours: the three repos and which is writable, the store-query
section with its measured numbers (1,274 characters against 20,397; 348 tokens against 3,153; 26×
on the graph), the order of work (brainstorm once, architecture twice, then per-layer), the five
State verdicts, the two forbidden moves, and §4's five rules. `run` is a bootstrap written from our
own system, and the mining found nothing to add to it that survived triage.

So `run`'s row in the results table is a **null by construction**, and it is the strongest kind: no
strip was possible, so no difference between B and C is possible. The two runs below are reported
anyway, as a check that the arms behave.

---

## `gate-verdicts` — three answers, compared

**The question** (from `gate-verdicts-ablation.md`):

> Our code review step prints its findings into a text blob with severity tags like [P1]. We're
> wiring it into CI so it can block a merge. What should the pass rule be? Be specific, four
> bullets maximum.

### A · control

> - **Block on any [P1]** present in the output — zero tolerance, no count threshold needed.
> - **Count [P2] findings; block if count exceeds a fixed threshold** (e.g. >3) — a couple of medium issues shouldn't halt merges, but a pile of them signals a rushed diff.
> - **Never block on [P3]/informational tags** — surface them in the PR comment for visibility, but they're advisory only.
> - **Fail closed on parse failure** — if the blob doesn't parse into recognizable severity tags (empty output, malformed run, tool crash), treat it as a block, not a pass, so a broken reviewer can't silently wave everything through.

### B · ours-only

> Given the pass rule for a text blob tagged `[P1]`/`[P2]`/etc: the rule has to be a strict parse against a known vocabulary, not a substring match, and it must fail closed on anything it can't parse — never round an unreadable or empty result up to "passed."
>
> - **Parse, don't grep.** Match tags against an exact enum (`[P0]`, `[P1]`, `[P2]`, …) at line start or a fixed delimiter — not `"P1" in output`, which a comment or code snippet can satisfy lexically without meaning it.
> - **Block on presence, not count.** Any `[P0]`/`[P1]` finding blocks the merge; the threshold is severity-based, not a count threshold, since one real blocker matters regardless of how many low-severity notes accompany it.
> - **A parse failure is a fail, not a pass.** Empty output, a timeout, a crash, or a body that doesn't match the expected tag format must resolve to `blocked`/`failed` — never silently pass the merge because "no `[P1]` was found" is indistinguishable from "the reviewer never ran."
> - **Record `unjudged` explicitly.** If the review step didn't cover certain files (diff too large, tool skipped a path), that's a distinct outcome from "reviewed and clean" — don't let CI report green when large parts of the diff were never looked at.
>
> The underlying failure mode this guards against (from `gate-verdicts`): a gate that can't verify something and says PASS anyway becomes evidence downstream that nothing was wrong.

### C · full

> Applying the D1/D2 rules to this specific gate:
>
> - **Fail on any P1, no default branch.** Grep the blob for `[P1]`; a match blocks. No other condition reaches PASS — PASS is the last check, not the default.
> - **No `[P1]` substring is not the same claim as "the review ran cleanly."** Treat non-zero exit, empty/whitespace output, or output missing *all* severity tags (no `[P1]`/`[P2]`/`[P3]` anywhere) as a separate FAIL state — "verification failed," not "0 findings" — since an untagged or empty blob means the reviewer didn't run, not that it found nothing.
> - **P2/P3 don't block.** Keep the gate binary on P1 only; use P2/P3 as visible-but-non-blocking annotations (e.g., posted as PR comments) rather than folding them into a score, since a merge gate needs a verdict, not an aggregate nobody can audit.
> - **A P1 finding must carry a `file:line` and quoted text to count.** A tagged `[P1]` line with no location/quote is unverifiable — demote it to non-blocking rather than let it block merges (or fail closed and treat it as a gate malfunction, but don't silently drop it or silently let it pass).

### Comparison, on mechanism

| Mechanism | A | B | C | Origin of the rule |
|---|---|---|---|---|
| Any P1 blocks | yes | yes | yes | instinct |
| Fail closed on empty / crashed / untagged output | **yes** | yes | yes | instinct — A has it unprompted |
| Untagged is reported as *verification failed*, not "0 findings" | no — A blocks but does not separate the claims | **yes** — *"'no [P1] was found' is indistinguishable from 'the reviewer never ran'"* | **yes**, stated as a separate FAIL state | mined (gstack `codex`), but B reaches it from `unjudged` |
| No count threshold on lower severities | **no — A proposes `>3`** | yes | yes | D3 is mined; B gets there without it |
| PASS is the last check, no default branch | no | implied by "fail closed on anything it can't parse" | **yes, named** | mined (D1) |
| A distinct value for *nobody looked* | no | **yes — `unjudged` for files the review never covered** | no | **ours** (D2, kept in B) |
| **Parse against an enum, not a substring** | no | **yes, and it leads the answer** | **no — C says "Grep the blob for `[P1]`"** | **ours** — `check_tests_present`/E6 |
| A finding must quote `file:line` to count | no | no | **yes** | **mined** (gstack `review`'s pre-emit quote gate) |

**Reading: A weak, B ≈ C, and they are strong in different places.**

Three of the mined D1 conclusions — fail closed on the unverifiable states, no default pass, no
arithmetic on a decision — appear in arm B without a single mined rule present. B reaches the
untagged-body distinction from a rule that is ours: `unjudged` never rounds up. Having a name for
*nobody looked* is apparently enough to make the model refuse to score an unreadable body, which is
what D1 exists to enforce.

**The mining bought one mechanism here: the quote gate.** Only C requires a `[P1]` to carry
`file:line` and verbatim text before it may block a merge, and that is `PASS2-GSTACK-SKILLS.md:221`.
It is a real addition and neither other arm has it at any strength.

**And it cost one.** B leads with *parse against an exact enum, not `"P1" in output`* — the
generalisation of our own `check_tests_present` substring bug, which is E6 and survives in arm B.
C, holding the same E6, does not produce it: it says *"Grep the blob for `[P1]`"* and spends its
untagged-output bullet on the mined framing instead. The stripped skill applied our own strongest
finding to the question; the full skill, with eleven more mechanisms competing for four bullets,
did not.

---

## `tenant-isolation` — three answers, compared

**The question** (from `tenant-isolation-ablation.md`):

> We've turned on Postgres row-level security so each customer only sees their own rows. I want a
> test in CI that proves the isolation actually holds. What should the test do? Four bullets max.

### A · control

> - Seed two (or more) tenant accounts with rows of the same shape, then connect **as each non-superuser tenant role** (RLS is bypassed by table owners/superusers, so the connection identity is the crux of the test) and assert `SELECT` returns only that tenant's rows, never the others'.
> - Attempt cross-tenant `UPDATE`/`DELETE`/`INSERT`-with-foreign-tenant-id from tenant A's connection and assert zero rows affected (not an error swallowed silently) rather than checking only reads.
> - Include a negative control: temporarily run the same queries as a bypass-RLS role (or with RLS disabled) to confirm the seeded data really is cross-tenant and the isolation you're seeing isn't just an empty-table artifact.
> - Run it against a real Postgres in CI (testcontainers/service container), not a mock/sqlite — RLS policies are engine-specific and only enforced by the actual planner.

### B · ours-only

> Based on §6.5/E5-E7 in the tenant-isolation skill, here's the test:
>
> - **Connect as the app's actual runtime role** (not superuser — a superuser bypasses RLS entirely and the test would pass for the wrong reason), set the tenant claim via `SET LOCAL` inside a transaction (outside a transaction it's a silent no-op), and run each tenant-scoped table's real application query as customer A while the session is scoped to customer B — assert **zero rows**, for every table, not a sample.
> - Also try the inverse: as customer A, attempt to **write/update a row that belongs to customer B** (by primary key, bypassing the app's own WHERE clause) — assert it affects 0 rows / is rejected, since a tight `GRANT` can look like isolation while the real work is done by the `POLICY`.
> - **`EXPLAIN` the query plan** for the scoped read and assert it hits a tenant-leading index, not a sequential scan — an RLS policy that forces a full scan is one that gets disabled under load, silently removing the isolation.
> - **Fail the test itself if it can't reproduce known-bad states** — e.g. temporarily run one assertion outside a transaction, or as a superuser, and confirm the suite fails; if it can't be made to fail, it isn't testing anything (this is the same trap the skill found in `tenant-discipline.spec.ts`, which names the right failure but greps the wrong client and never catches it).

### C · full

> Four bullets, grounded in the tenant-isolation skill's assertions (§4.3, §4b, E5/E6):
>
> - **Connect as the real restricted role, never as a superuser**, and set the tenant claim with `SET LOCAL` *inside a transaction* (not a bare `SET`) — both are the classic false-pass traps: a superuser bypasses RLS entirely, and `SET LOCAL` outside a transaction is a silent no-op, so either one makes a broken policy look like it's working.
> - **For every tenant-scoped table, read as tenant A while impersonating tenant B's session and assert zero rows returned** — not "fewer rows," exactly zero. This is the actual assertion CVE-2025-48757 (Lovable) was missing, and it must run against the app's real query paths, not hand-written test SQL.
> - **Attempt a cross-tenant write, not just a read**: as tenant A, `UPDATE` your own row to set its tenant/workspace column to tenant B — the write must fail, and a follow-up read as tenant B must still return zero rows. `USING` alone filters visible rows but won't stop a row being written *out* of its own tenant; only `WITH CHECK` catches that, so the test has to exercise it specifically.
> - **`EXPLAIN` the cross-tenant query and assert it hits a tenant-leading index**, not a sequential scan — a policy that's correct but unindexed is one someone disables under load, so make that regression visible in CI too.

### Comparison, on mechanism

| Mechanism | A | B | C | Origin |
|---|---|---|---|---|
| Do not connect as a superuser | **yes** | yes | yes | ours (`client.ts:18-23`) — and A holds it too |
| `SET LOCAL` must be inside a transaction | no | **yes** | **yes** | **ours** (`client.ts:18-23`) |
| The `POLICY` decides, not the `GRANT` | no | **yes**, in the write bullet | no | **ours** (`client.ts:76-83`) |
| Zero rows, every tenant-scoped table, not a sample | partial — "returns only that tenant's rows" | **yes, exactly zero, every table** | **yes, exactly zero, every table** | ours + pgTAP/Atlas |
| Drive the **app's own queries**, not SQL written for the test | no — "run against a real Postgres" | **yes** | **yes** | **ours** (`verification/client.ts`) |
| `EXPLAIN` shows a tenant-leading index | no | **yes** | **yes** | published (pgTAP, Atlas) |
| The test must be shown capable of failing | **yes** — the bypass-RLS negative control | **yes**, and named as our own `tenant-discipline.spec.ts` failure | no | ours |
| Cross-tenant write attempted | yes — write to *another tenant's* row | yes — write to *another tenant's* row | **yes — update your OWN row into another tenant** | — |
| **`USING` versus `WITH CHECK`; a row written *out* of its tenant** | **no** | **no** | **yes, with the mechanism named** | **mined** (ECC `ruby/`, `php/` → §4b) |

**Reading: A weak, B strong, C stronger — and the increment is exactly the stripped section.**

B recovers everything the ablation credited to the skill except one thing. It has the two false-pass
traps quoted from our own `client.ts`, the exactly-zero-rows assertion over every table, driving the
application's real query paths, and — the sharpest move in any of the twelve answers — a bullet
saying *fail the test itself if it can't reproduce known-bad states*, tied to our own
`tenant-discipline.spec.ts`. That bullet is arm B's alone; neither A nor C states it.

C's third bullet is §4b, reproduced faithfully: *"as tenant A, `UPDATE` your own row to set its
tenant/workspace column to tenant B — the write must fail… `USING` alone filters visible rows but
won't stop a row being written out of its own tenant; only `WITH CHECK` catches that."* **No other
arm has it.** A and B both propose a cross-tenant write, but both write at *another tenant's* row,
which any `USING` policy already stops. The distinction between a row you may not touch and a row
you may touch and may not move is present in C only.

This is the one unambiguous positive result in the file. Two lines of Ruby and PHP security prose in
a repository with no syntactic bearing on our stack produced the only rule here that neither general
instinct nor our own predecessor analysis reached. The elaboration into `WITH CHECK` is ours; it was
not written until the mined finding named the gap.

**Cost, recorded:** C dropped the capability-to-fail bullet that both A and B carry. Same pattern as
`gate-verdicts` — the fuller skill spends its four bullets on more mechanisms and loses one the
thinner arms keep.

---

## `testing` — three answers, compared

**The question** — the **second** from `testing-ablation.md`; the first was recorded as no
difference and the file says so:

> We want a done-bar for each generated package's tests: coverage over 80% and no failures. Is that
> a good bar, and what would you change? Four bullets maximum.

### A · control

> Reasonable floor, not sufficient on its own — the two metrics catch different failure modes than what matters for AI-generated code, where the tests are also generated and can't be trusted to reflect real intent.
>
> - **Coverage % without assertion quality is gameable**: a generated test can execute a line with no meaningful assertion and still count toward 80%. Pair the threshold with mutation testing (or at minimum assert-per-test linting) or the bar rewards test *presence*, not test *validity*.
> - **"No failures" only tells you the tests that exist pass** — it says nothing about missing tests for cases the generator didn't think of (error paths, boundary inputs, concurrent access). Add a check that error-handling branches specifically are covered, not just aggregate line/branch %.
> - **80% flat across a package is the wrong grain** — generated CRUD/plumbing code should be near 100% (cheap, mechanical to test), while business-logic branches deserve higher scrutiny than a blended average enforces. Consider per-file or per-module floors instead of one package-wide number.
> - **Add a build/typecheck-clean gate before coverage is even measured** — for a non-technical user's app, a package that type-checks and lints clean but has 79% coverage is closer to "done" than one at 81% with type errors suppressed to pass tests.

### B · ours-only

> No — coverage percentage as a gate is directly named as the failure mode in §10 and E8.
>
> - **Drop the 80% coverage threshold** — it's marketing, not evidence (Inozemtseva & Holmes 2014; Zhao et al. 2026 found coverage measured on buggy code is "not informative of whether tests detect that bug"). Replace it with a coverage *map* of what's untouched, not a pass/fail number.
> - **"No failures" isn't a bar either — a green suite is `unjudged` until shown capable of failing** (§5): promote it via `tdd` (red-before-fix), `mutant` (incremental Stryker-style on changed lines), or `negative_fixture`. Otherwise a passing generated-app test proves nothing — Lin et al. found 81–100% of Fail→Fail cases pass agent-run validation anyway.
> - **Gate on three numbers, not one**: ran/passed/skipped, from the machine-readable report (`--reporter=json`), never a human summary — skips are capability gaps that belong in `unjudged`, not a denominator (§7).
> - **Add the checks percentage can't catch**: doubles verified against production in one shared conformance suite (§4), fixtures traced to a real producer (Q4), and prefer a schema-derived invariant over any fixture-based test wherever one exists — it's the strongest and cheapest check in the document.

### C · full

> Not a good bar — §8 and §10 in `testing` say directly: coverage-percentage gates are contradicted by evidence (Inozemtseva & Holmes 2014; Zhao et al. 2026 found coverage on buggy code is "not informative of whether the generated tests detect that bug"), and "no failures" for a model-generated suite is `unjudged`, not passing, per Lin et al. (81–100% of failed cases pass agent-run validation).
>
> - **Drop the 80% threshold as a gate**; report coverage as a map of what's untouched, and use incremental mutation testing on changed files as the mechanical answer to "can this test fail" instead.
> - **Never let a generated package's own green suite satisfy the done-bar.** A passing test a model wrote is `unjudged` until promoted via `tdd`/`mutant`/`negative_fixture` (§5); a failing one is a `Remainder` and goes to repair — that asymmetry, not "no failures," is the real bar.
> - **Gate on the three/four numbers, not the pass count**: `ran/passed/skipped` plus planned-unit count, with skips landing in `unjudged` and never in a denominator (§7, §9.5a) — a truncated or skip-heavy run currently looks identical to a clean one.
> - **Require the double-vs-production and fixture-provenance checks (§4, Q4)** before any of this counts: a doubled seam with no conformance suite, or a hand-built fixture the real producer can't emit, invalidates whatever the coverage number says.

### Comparison, on mechanism

| Mechanism | A | B | C | Origin |
|---|---|---|---|---|
| Coverage % is a weak bar | **yes** | yes | yes | instinct; papers sharpen it |
| **Drop coverage as a gate entirely**, report it as a map | no — A keeps it and adds per-file floors | **yes** | **yes** | published (Inozemtseva, Zhao) |
| Mutation testing | **yes**, as a pairing | yes, as a promotion route | yes, as the mechanical answer to Q1 | published (Papadakis) |
| **Green is `unjudged` until shown capable of failing**; `tdd` / `mutant` / `negative_fixture` | no | **yes** | **yes** | **ours** — `docs/next/LAYER-E-BUILD.md` §3.1 |
| A model-written test never promotes | no | yes | **yes**, with `Remainder` → repair | ours + Lin et al. |
| `ran / passed / skipped` from the machine-readable report; skips never in a denominator | no | **yes** | **yes** | **ours** — §7, our own 27/9 |
| **Planned-unit count; a truncated run looks identical to a clean one** | no | **no** | **yes** | **mined** — gstack §9.5(a) |
| Double-versus-production conformance; fixture provenance | no | **yes** | **yes** | **ours** — §4, Q4 |
| Schema-derived invariants preferred over fixtures | no | **yes** | no | ours |
| Type-check / build must pass first | **yes, and only A** | no | no | instinct — displaced in both skill arms |

**Reading: A weak, B ≈ C, minus one clause.**

The two-arm ablation this morning credited `testing` with two mechanisms the control lacked:
*green is `unjudged` until the test is shown capable of failing*, and *a zero exit code does not
establish that the planned units ran, with skips excluded from the denominator*. **The third arm
splits them.** The first is ours and arrives in B in full — B states the rule, all three promotion
routes, and the Lin et al. scope. The second splits down the middle: the skip half is ours (§7) and
is in B; the **planned-count half is mined and is in C only.** C's third bullet reads *"ran/passed/skipped
plus planned-unit count… a truncated or skip-heavy run currently looks identical to a clean one"* —
the second clause is `PASS2-GSTACK-TESTS.md` §2.1, the 16-of-434 incident, and B has no trace of it.

So the mining bought one clause of one bullet. That clause is not decorative — invisible
non-execution is undetectable without a plan count, and no amount of parsing the summary recovers
it — but it is one clause, against a bullet-for-bullet match on everything else.

**B is better than C on one axis**, again: B closes with *"prefer a schema-derived invariant over
any fixture-based test wherever one exists — it's the strongest and cheapest check in the
document"*, which is §6's own row and is ours. C spends that space on the mined truncation clause.
Both arms drop the type-check-first point that only the control makes; that displacement was
recorded in the original ablation and reproduces here.

---

## `run` — three answers, compared

**The question** (from `run-ablation.md`):

> I am starting the rebuild tomorrow and want to get the sequence right. There are seven layers.
> Should I just take each layer one at a time — think through the ideas, design it, build it, test
> it — or is there something that has to happen across the whole system first? Four bullets max.

**Arms B and C load byte-identical skill files.** This pair is a control on the apparatus, not a
test of the mining.

### A · control

> - Read `docs/as-built/00-INDEX.md` and `01-DECISIONS.md` in full before touching any layer — the layers share cross-cutting decisions (data model, auth, tenancy) that no single layer's doc will surface, and building layer-by-layer without that map means re-deciding the same thing seven times.
> - Write ADRs for the stack choices CLAUDE.md flags as open (framework, DB, auth, hosting) before the first layer's build step, since every layer will silently inherit whatever the first one picks otherwise.
> - Beyond that, yes — take layers one at a time (position → design → build → test) rather than doing all seven designs before any build; each layer's "State" judgement (solid/wrong-shaped/missing/obsolete) is cheap to get wrong in the abstract and expensive to get wrong seven times over.
> - Pick the layer with the fewest unresolved cross-layer dependencies to go first — check the graph (`graph.json`) for what has the least fan-in from other layers, so its ADRs aren't retrofitted later.

### B · ours-only

> - Two whole-system passes happen **once**, before any layer: `brainstorm` (fed from `scripts/scio-db.py layers`/`sql`, not free-association) to surface options against the 249 already-triaged findings, then `architecture` to fix the system's overall shape — including whether it's even seven layers — as ADRs in `docs/decisions/`. Nothing gets built until those ADRs exist.
> - Only then does each layer run its own loop: read that layer's `LAYER-*.md` State verdict (solid/deliberate/wrong-shaped/missing/obsolete) and decide part-by-part, then run `architecture` a *second* time — now scoped to that layer's internal design — before writing any code.
> - Don't skip that second architecture pass per layer thinking the system-level one covers it; that's exactly where the predecessor's shape quietly stopped being true. Also don't re-brainstorm per layer — a layer needing new ideas mid-build means an ADR from step 1 was wrong, so reopen it rather than improvise.
> - Practically: query `scio.db` (`find`/`read`/`layers`/`skill`) instead of opening the as-built docs directly — an average lookup is ~16x cheaper — and treat step 5 (`testing`) and step 6 (ADRs + `/checkpoint`) as part of every layer's loop, not cleanup at the end.
>
> So the answer to "one layer at a time" is: yes, but only after the two whole-system passes, and each layer gets its own architecture pass too, not just a build pass.

### C · full

> No, don't go layer-by-layer from the start — two passes have to happen once, across the whole system, before any layer is touched:
>
> - **Brainstorm once, not per layer** — against the 249 findings already triaged in the store (73 are undecided ADRs), so you don't reinvent a decision that's already sitting there.
> - **Architecture, once, for the whole shape** — this fixes the stack and the layer count itself (the predecessor's seven is evidence, not a spec — could be six, could be ten). Nothing gets built until this lands as ADRs in `docs/decisions/`.
> - Only then does the per-layer loop start, and it's five steps per layer, not three: read the predecessor's verdict for that layer (solid/deliberate/wrong-shaped/missing/obsolete) → **architecture again, this time for the layer's internals** (a second, different question from step 1, not a repeat of it) → build → test (green is a claim, not proof, until shown capable of failing) → record/commit.
> - The two failure modes to guard against explicitly: building before the system-wide ADRs exist (how the predecessor sprawled to 23K lines), and re-running brainstorm per layer instead of reopening the step-1 ADR when a layer seems to need new ideas.

### Comparison, on mechanism

| Mechanism | A | B | C |
|---|---|---|---|
| Brainstorm **once**, over the whole system | no | **yes** | **yes** |
| Feed it from the 249 triaged findings | no | **yes** | **yes**, and names the 73 undecided ADRs |
| Architecture runs **twice** — whole system, then per layer | **no — A says design per layer** | **yes** | **yes** |
| The layer **count** is itself a step-1 decision, not a given | no — A accepts seven | **yes** | **yes** |
| The five State verdicts, by name | partial — four of five, "solid/wrong-shaped/missing/obsolete" | **all five** | **all five** |
| Both forbidden moves named | no | **yes** | **yes** |
| Query the store rather than opening documents | partial — A queries the graph | **yes** | implied |
| Answers the question's premise **wrongly** | **yes — "Beyond that, yes — take layers one at a time"** | no | no |

**Reading: A wrong in the predicted way; B and C indistinguishable on mechanism.**

Every rule the skill exists to install is in both B and C, and the arms differ only in emphasis — B
spends its fourth bullet on the store-query discipline, C on the two forbidden moves. A does what
the question baits it into doing: it front-loads reading and the stack ADRs, then endorses the
per-layer loop *including ideation*, and treats seven layers as given.

Since B and C load the same bytes, this pair measures only that the harness is not introducing a
difference of its own. It is not.

**One artefact worth recording:** B tells the reader to query `scio.db` via `scripts/scio-db.py`,
and arm B's directory contains neither. The skill is being followed, not the filesystem. This is a
general hazard for arms A and B, which carry `docs/as-built/` and nothing else.

---

## Verdict per skill

| Skill | Pattern | What the mining added | What it cost |
|---|---|---|---|
| **`gate-verdicts`** | A weak, **B ≈ C** | **one mechanism** — a finding must quote `file:line` and verbatim text before it may block a merge (gstack `review`) | C lost the *parse-against-an-enum, not a substring* move that B leads with, which is our own `check_tests_present` finding |
| **`tenant-isolation`** | A weak, **B strong, C stronger** | **one rule, decisive** — §4b's `USING` versus `WITH CHECK`, and the write that moves a row *out* of its own tenant (ECC `ruby/security.md`, `php/security.md`) | C lost the *make the test prove it can fail* bullet that both A and B carry |
| **`testing`** | A weak, **B ≈ C**, minus one clause | **one clause** — the planned-unit count, so invisible non-execution is detectable (gstack, the 16-of-434 incident) | C lost the schema-derived-invariant preference that B closes with |
| **`run`** | A wrong, **B = C by construction** | **nothing.** No mined rule is in the file; the one proposal to add any (the Delegation Completion Contract) has not landed | — |

### Rule-by-rule, for the two that split

`tenant-isolation`, what carried the answer:

| Rule | Arm that has it | Origin |
|---|---|---|
| superuser bypasses RLS | A, B, C | ours (`client.ts:18-23`), and instinct has it too |
| `SET LOCAL` outside a transaction is a silent no-op | B, C | **ours** |
| the `POLICY` decides, not the `GRANT` | B | **ours** |
| zero rows, every table, driven through the app's own queries | B, C | **ours** + published |
| the plan still uses a tenant-leading index | B, C | published (pgTAP, Atlas) |
| the test must be shown capable of failing | A, B | ours |
| **`WITH CHECK`, and a row written out of its tenant** | **C only** | **mined** |

`testing`, the two mechanisms the two-arm ablation credited, now split:

| Mechanism | Arm | Origin |
|---|---|---|
| green is `unjudged` until shown capable of failing; `tdd` / `mutant` / `negative_fixture` | B **and** C | **ours** (`docs/next/LAYER-E-BUILD.md` §3.1) |
| `ran / passed / skipped`, skips never in a denominator | B **and** C | **ours** (§7, our own 27 passed / 9 skipped) |
| **planned-unit count; a truncated run is indistinguishable from a green one** | **C only** | **mined** (gstack §9.5(a)) |

---

## What this says about the mining as a whole

**On these four skills, most of the value came from analysing our own system.** That was the
hypothesis, and it is the result. Of the mechanisms that appeared in a C answer and not in the
control, arm B produced all but three.

The three the mining bought are worth naming precisely, because they are more interesting than the
count suggests:

1. **`WITH CHECK` versus `USING`** — a real defect class, in the exact stack ADR-0011 fixes, that
   neither instinct nor 23,000 lines of our own predecessor put in front of us. It came from Ruby
   and PHP files with, as the miner wrote, *"zero syntactic relevance to us."* This one justifies a
   mining pass on its own terms.
2. **The planned-unit count** — invisible non-execution, undetectable without it. It came from
   someone else's incident: 16 of 434 files ran, shell exit 0.
3. **The pre-emit quote gate** — a finding that cannot quote its line is demoted. Smaller than the
   other two, and closest to being a convention we would have reached.

All three share a shape: **each is a specific failure someone else actually hit and wrote down.**
Not one of the three is a framework, a taxonomy, a vocabulary or a checklist. The mined material
that *did not* survive contact with these four questions is overwhelmingly of the other kind — five
outcome states, four verification modes, score caps and ceilings, ★/★★/★★★ levels, three layers for
a privacy promise, four self-declarations per gate, six arithmetic checks. Those are the bulk of
what was removed, and their absence changed no answer in any of the twelve runs.

**A second finding, which was not what was being tested and is more uncomfortable.** In three of the
four skills, **arm B produced a mechanism arm C did not** — parse-against-an-enum, the
capability-to-fail assertion, the schema-derived invariant. In every case the missing mechanism is
**ours**, present in both files, and displaced in C by mined content competing for the same four
bullets. The dilution is not hypothetical and it is not confined to one skill. `gate-verdicts` is
the clearest case: four-fifths of that file is mined, and the stripped version answered the question
with our own strongest finding while the full version did not.

That does not argue for deleting the mined rules. It argues that a skill has a bullet budget the
same way a context window does, and that mined material is currently being ordered ahead of material
we verified at `file:line` in our own code. `gate-verdicts` §1 lists eleven mined mechanisms above
three of our own defects. Reversing that order is a one-line edit with, on this evidence, a
measurable effect.

### Limits of this measurement

- **n = 1 per cell.** Twelve runs, one per arm per skill. No repetition, no blinding; I wrote the
  strip, ran the arms and graded them.
- **Four questions, chosen this morning for a different experiment.** Each was written to
  discriminate skill-versus-no-skill, not ours-versus-mined. A question that happens not to reach a
  mined rule reports a null that a different question might not. `gate-verdicts` in particular has
  D3 and D5 entirely unprobed by this question.
- **`graphify` loads in all three arms** and is not controlled for.
- **Arm C is the live repo**, carrying `docs/next/`, `docs/mined/`, `docs/triage/`, `scripts/` and
  `scio.db`, which A and B do not. Every C answer could in principle be reading the corpus rather
  than the skill. C's `run` answer cites the 73 undecided ADRs, which is in the skill; C's
  `tenant-isolation` answer cites §4b, which is in the skill; no C answer here demonstrably needed
  the extra corpus, but the arms are not equal on this axis and no result should be read as though
  they were.
- **Arms A and B differ by one line** of `docs/as-built/ARCHITECTURE-AS-BUILT.md` — the
  `validate_plan` correction. It is not near any of the four questions.
- **The ours/mined boundary was drawn by me, on rules whose origins are sometimes genuinely
  entangled.** §4b is the case where a reader might reasonably disagree; the argument for the call
  is written out above so it can be checked. Two rules were kept as *both, independently* and are
  marked as such.
- **Nothing here measures whether a build done either way contains fewer defects.** It measures what
  a model says when asked one question, three ways.
