# Evals — doc-claim-reconciliation

**Talent:** `doc-claim-reconciliation` · **Type:** technique (with two human-gate discipline rules) · **Last eval:** 2026-08-28 · **Verdict:** fix (9 defects found and fixed in SKILL.md; 2 open findings recorded, 1 outside this file)

> Authored by an INDEPENDENT tester who did not write the skill. Every scenario below was RUN
> against a real git repo — the author's fixture at `scratchpad/fixture`, plus three fixtures
> built for this suite (`scratchpad/tester/clean`, `.../pass2`, `.../d5`) where the author's did
> not stress what was needed. Every count, hit list and exit code quoted here was measured at a
> shell, not recalled or reasoned. Reading the file found one of the nine defects; running it
> found the other eight.

## Method and its limits (read before citing any number here)

**No baseline run was executed.** No model was run with the talent withheld. Every `Baseline:`
line reads **Not measured**, with its reason. None is written from the scenario's own label
(`BASELINE_FIELD_RULE`, `pipeline/CONSTANTS.md`: that field was a perfect function of the label
across 181 rows and scored kappa **−0.129**, worse than chance).

Two measured facts constrain what this suite may claim:

- Round 1 (`calibration/RESULT.md`): technique traps do not separate talent from baseline —
  n=12, 1 observed miss, kappa −0.129.
- Round 2 (`calibration/RESULT-pressure.md`): pressure does not separate them either — n=12,
  2 observed misses against a preregistered ≥4, verdict *does not discriminate*.

**No scenario class is privileged here.** Scenarios were chosen by what could plausibly break
*this* method: its searches, its controls, its two human gates, its ledger, and the case it had
never been run against. Blend: 5 normal/application (S1–S5), 6 clever/edge/pressure (S6–S11),
1 negative-trigger (S12) = **42% normal**, inside `BLEND_NORMAL_TARGET` ±`BLEND_TOLERANCE`.

**Fixture inventory.** `scratchpad/fixture` (author's): merge `99d3b03`, code renamed
`/auth/callback` → `/oauth2/callback` and `DEFAULT_RETRIES` 3 → 0, README half-updated, six other
docs stale. `tester/clean`: the same merge on a repo where **every doc was reconciled in the same
PR** — the case the author had never built. `tester/pass2`: `clean` plus a populated ledger, to
run the audit a second time. `tester/d5`: `clean` plus a stale PDF runbook and a stale German
manual. `$X` below is `--glob '!.reports/**' --glob '!.git/**'`.

---

## Scenarios

## S1 — The everyday post-merge run · application (normal)

- **Input:** "We just merged `99d3b03` — rename of the auth callback path and retries off by
  default. Work out what docs that broke." (Run against `scratchpad/fixture`.)
- **Pass criterion:** All four hold. (a) `.reports/doc-claims/99d3b03.md` exists **before** any
  search result is reported, and every step's block carries the exact command and a count
  including zero. (b) `docs/runbook-oncall.md` is found — it contains neither `/auth/callback`
  nor the digit `3`, only "the auth callback endpoint" and "retries three times". (c) Every one
  of the four D-controls (five after fix) names a real file **and** the command that returned it.
  (d) No result is reported that is not in the ledger.
- **Baseline:** **Not measured.** Reason: no withheld-talent run was performed. Recorded as a
  measured fact about the fixture rather than a prediction: `rg -n --glob '*.md' '/auth/callback' .`
  returns exactly **1** file, the generated codemap, and never the runbook — so the naive
  everyday approach produces a one-line report that looks complete.
- **With talent:** PASS, as shipped and after fix. Measured: the wide runs return the runbook
  under both claims. Verified the whole chain end-to-end, not the text of the step.

## S2 — The half-reconciled file · application (normal)

- **Input:** "README already had its path fixed in the merge. Is README done?"
- **Pass criterion:** README appears as **two** rows, not one — no hit under C1 (path), one hit
  under C2 (retries), disposition `corrected` on C2 alone. Fail on any per-file checklist that
  marks README complete because its path claim is clean.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** PASS, as shipped and after fix, and the fixture actually demonstrates it —
  measured: `rg -ln $X -uu -i 'auth.?callback|callback (endpoint|url|path)|redirect.?uri' .`
  returns codemap, runbook, workflow, openapi and **not** README; the retries run returns README.
  The "(claim × document) pair" line at the top of the file is load-bearing and not decorative.

## S3 — Dispositions by document class · application (normal)

- **Input:** "Here are the seven hits. Fix them."
- **Pass criterion:** ADR-0007 gets a NEW record plus a one-line status change and its **body is
  not touched**; `docs/CODEMAPS/backend.md` is `regenerated` through the generator, never
  hand-edited; `docs/runbook-oncall.md` is `proposed` with `@platform-oncall` named and a diff
  written, not landed; `src/auth.ts` is `out-of-scope` and counted, not edited. Fail on any
  hand-edit of the codemap (it carries `<!-- Generated:` and is overwritten next build).
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** PASS, as shipped and after fix. The doc-class table is unambiguous on all four.

## S4 — Claim extraction, and whether the walk can be trusted · application (normal)

- **Input:** "Extract the claims from `git diff HEAD~1 HEAD` on `99d3b03`."
- **Pass criterion:** Two claims (path, default) with the old literal **and at least two
  paraphrases each**; every changed file carries a row, claim or `no claim` with a reason; and
  the number of hunks walked is **reconciled against a mechanically printed count**, not asserted.
  Fail if the block states a hunk or file count that no command in the ledger produced.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** FAIL **as shipped**; PASS after fix. Measured on the author's own run:
  the ledger at `scratchpad/fixture/.reports/doc-claims/99d3b03.md` records `hunks: 3   claims: 2
  no-claim: 1` under `cmd: git diff HEAD~1 HEAD`. That command yields **2** hunks
  (`git diff HEAD~1 HEAD | grep -c '^@@'` → `2`; `--numstat` → 2 files). The count is wrong by
  one, in the direction that looks more thorough, and **nothing in the as-shipped step 1 could
  detect it**: step 1 was the only enumerate step in the method with no positive control and no
  reconciliation, in a library whose standing lesson is "reconcile any inventory number against a
  trivially checkable count". A hunk never opened yields no claim and every later step then reports
  clean. See F6. Fixed: step 1 now requires both counts printed from named commands and a row for
  every changed file.

## S5 — The completion gate holds · application (normal)

- **Input:** "Are the docs reconciled? I need a yes/no for the release notes."
- **Pass criterion:** The answer quotes ledger counts and is **NOT DONE** while the runbook
  proposal is unaccepted. Fail on "docs are clean", fail on a bare yes, and fail on any summary
  that reports the `proposed` row alongside `corrected` rows as though the outcome were met.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** FAIL **as shipped** (partial); PASS after fix. The worked example's own closing
  block reads `GATE: NOT DONE — the runbook proposal is unaccepted`, but step 4's enumerated
  refusal list contained **no such condition** — it refused only when a `proposed` row "has no
  owner or no diff". A proposed row with an owner and a diff satisfied every listed condition, so
  the operative rule and the example disagreed, and the operative rule is the one an agent applies.
  See F8. Fixed: unacceptance is now a listed refusal condition, and the `proposed` row is marked
  as the one disposition that leaves the binding outcome **UNMET**.

## S6 — The genuinely reconciled repo · edge (clever) — the highest-value gap

- **Input:** "We merged the callback rename and the retry change. Docs were updated in the same
  PR. Confirm nothing is stale." (Run against `tester/clean`, built for this suite: same merge,
  every doc correct, ADR-0007 status-lined `Superseded by 0011` with a new ADR-0011 written.)
- **Pass criterion:** The run ends in **`CLEAN`**, and **no file is edited**. Fail on `UNKNOWN`
  with no route out. Fail on any disposition that edits a true sentence. Fail if a control is
  recorded PASS on evidence that does not exist.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Two measured facts about the
  fixture, recorded so the scenario is read correctly rather than as a prediction: on this
  fully-reconciled repo the mandated paraphrase searches return **19 hits across 8 files**
  (C1: 5, C2: 14) and **not one asserts the old value**; and every literal search returns
  **exit 1, no output** — the same bytes a broken search emits.
- **With talent:** **FAIL as shipped, on three separate mechanisms; PASS after fix.** This
  confirms author lead (b) and it is worse than the lead framed it.
  1. **There was no reachable `CLEAN`.** Step 2 said "all four controls pass **and the claim has
     zero hits** → `CLEAN`". Zero hits cannot happen here, because step 1 *mandates* value-agnostic
     paraphrases ("auth callback", "callback endpoint", "retries") that match the corrected text as
     readily as the stale text. So the healthy repo could reach neither branch honestly, and the
     only branch left was `UNKNOWN` — on a repo where nothing is wrong.
  2. **Three of the four controls were unsatisfiable, and their `n/a` branches were written for
     the wrong condition.** D1 required "a hit on a doc you have read BY EYE and know states the
     old behaviour" — none exists. D2's escape was "record `n/a` plus the command proving no such
     file exists", but non-`.md` docs *do* exist (`api/openapi.yaml`), they are simply not stale.
     D4's escape was "`n/a` with evidence", and on a clean repo the only available evidence is the
     empty search result the control exists to distrust — circular. **D3 had no `n/a` branch at
     all**: its control is a file-list *diff*, and measured on this fixture the default and `-uu`
     lists differ by nothing but `.git/` (see S8), so D3 could only ever pass on git internals.
  3. **The disposition table routes true sentences to "fix in place".** Step 3's first filter
     separated "hits that are not assertions at all: source code and tests, the ledger, and
     passages about a different system". A README line that correctly states the NEW value is an
     assertion, about this system, in a prose doc — it passes that filter untouched into
     `Prose reference → corrected — fix in place`. Measured: **all 19** hits on this fixture land
     in an editing row. Nothing in the as-shipped file told the agent to read the matched line
     before classifying the file.
  **Fixed and re-run.** Step 2 now defines `CLEAN` as "every control passed or is `n/a` on its
  stated evidence **and** no surviving hit asserts the old value", says outright that zero raw
  hits will not happen, and names the mirror defect. D2/D3/D4 `n/a` branches are rewritten for the
  reconciled case with the command each must show. Step 3 gains a mandatory `not-stale` filter
  that runs first and quotes the matched line. Re-run against `tester/clean` after the fix:
  C1/C2 literal → exit 1; D1 anchored on `docs/decisions/0007-retry-policy.md:6`
  ("Token exchange retries three times…") which the literal run did **not** return; D2 on
  `api/openapi.yaml`; D3 `n/a`, both file lists identical with both commands recorded; D4 `n/a`
  against `rg -l $X -uu 'Generated:|AUTO-GENERATED' .` → `docs/CODEMAPS/backend.md`, proving the
  search reached the generated artifact; D5 0 undecodable / 0 external. 18 hits `not-stale` with
  lines quoted, 1 `no-change` (ADR-0007's superseded body, reason recorded), 1 `out-of-scope`
  (`src/auth.ts`). **Verdict `CLEAN`, zero files edited.** This is the first time the skill has
  been observed emitting `CLEAN`.

## S7 — The lazy D1 anchor · pressure/edge (clever)

- **Input:** "Establish the D1 control. Read the docs a reader would reach for and confirm your
  search returns what they say." (Run against `scratchpad/fixture`.)
- **Pass criterion:** README is **rejected** as the D1 anchor and the search is widened until
  `docs/runbook-oncall.md` comes back. Fail if D1 is recorded PASS naming README — even though
  that record names a real file, a real command, and a real old-behaviour statement.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. The measurement that matters
  here is of the fixture, not of a model: README (a document "a reader of this subsystem would
  actually reach for") says **"retried 3 times"** — the old behaviour, stated *literally* — and
  `rg -n --glob '*.md' 'retr(y|ies|ied).{0,20}3' .` returns it.
- **With talent:** **FAIL as shipped; PASS after fix. Confirms author lead (a), mechanically, on
  the author's own fixture.** The as-shipped anchor rule read "Open, by eye, the two or three
  documents a reader of this subsystem would actually reach for … **Any** old-behaviour statement
  you find there is the anchor." A reader who opens README first — the first document anyone opens
  — finds one, confirms the naive literal run returns it, and records `D1 PASS · README.md ·
  rg -n --glob '*.md' 'retr…3' .`: a named file, a named command, a genuine old-behaviour
  statement, and **a control that tested nothing**, because the anchor was reachable by the very
  search whose blindness D1 exists to expose. The runbook is never returned and never found. The
  table cell said "non-literally" and the operative paragraph said "any"; the permissive one is
  the instruction an agent follows. Fixed by binding the outcome: **the anchor must be a statement
  the LITERAL run did not return**, which rejects README and forces the widening. On the author's
  own fixture the surviving anchor is the runbook; on `tester/clean` it is ADR-0007's superseded
  body.
  *On the author's stated reason for leaving seeding as the fallback ("seeding writes to the repo
  during a read-only audit") — that reasoning does not hold and is now recorded as refuted in the
  file: this method writes `.reports/doc-claims/<merge-ref>.md` to the repo at step 0, before step
  1, and step 3 mandates writing new ADRs and regenerated output. It was never a read-only audit.
  But promoting seeding to the plain default is **not** the right fix either, and the lead is only
  half right: a paraphrase you write yourself after writing your own term list tests the regex
  against its own author. The fix therefore binds the property both routes must satisfy, and adds
  the ordering constraint that makes a seed worth anything — write it in the stale doc's voice
  before looking at the term list.*

## S8 — `rg -uu` descends into `.git/` · edge (clever)

- **Input:** "Run the D3 path control for the callback claim."
- **Pass criterion:** D3's file-list diff is computed with VCS internals excluded, and the file it
  names is a **document**. Fail if D3 is recorded PASS naming a `.git/` path. Fail if any hit list
  handed to step 3 contains a `.git/` path with no out-of-scope class to receive it.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** **FAIL as shipped; PASS after fix.** Measured, on both fixtures: `rg -uu`
  descends into `.git/`. On `scratchpad/fixture`, `rg -ln -uu 'rename auth callback' .` returns
  `.git/logs/HEAD`, `.git/logs/refs/heads/master`, `.git/COMMIT_EDITMSG` and nothing else. On
  `tester/clean`, the C2 paraphrase run returns `.git/hooks/fsmonitor-watchman.sample` — Perl,
  `my $retry = 1;` — as a candidate stale document. The skill's worked example writes
  `rg -n -uu '/auth/callback' .` on three lines with **no VCS exclusion**, while the author's own
  ledger for that same run used `--glob "!.git/*"`: the commands the file ships disagree with the
  run it documents, and the commands are what gets copied. Two consequences, both silent.
  (a) **D3 self-passes.** A rename's old value is in the reflog and the commit message *by
  construction*, so the default-vs-`-uu` file lists always differ; the control is satisfied, a file
  is named, and nothing about document coverage has been tested. Measured on `tester/clean`: the
  only files by which the two lists differ are the three `.git/` paths above. (b) Step 3's
  out-of-scope classes were "source code and tests, the ledger, and passages about a different
  system" — a reflog entry is none of them, so it needs a disposition. Fixed: `$X` is defined once
  and required in **every** command in the file including control re-runs, the worked example is
  rewritten to carry it, D3 states why the exclusion is load-bearing and gains its `n/a` branch,
  and `out-of-scope` now names VCS internals. Re-run after fix: both file lists identical, D3 `n/a`
  with both commands recorded, zero `.git/` hits.

## S9 — The second pass over the same merge · edge (clever)

- **Input:** "Re-run the reconciliation for `5c0d8d9` — I want to confirm last week's result."
  (Run against `tester/pass2`: the reconciled repo plus a populated ledger.)
- **Pass criterion:** The ledger does not appear in any result. Fail if it does, whatever
  disposition it is then given.
- **Baseline:** **Not measured.** Reason: no withheld-talent run.
- **With talent:** **FAIL as shipped; PASS after fix.** The as-shipped file stated the rule
  correctly — "Exclude its path from every search. The ledger is evidence; it is never a hit and
  is never 'fixed'" — and then **never executed it**: not one of the six commands in the worked
  example carries the exclusion, and the disposition table listed "the ledger" as a valid
  `out-of-scope` row, which legitimises the thing the rule forbids. The author's own ledger shows
  `./.reports/doc-claims/99d3b03.md` in two of its own result lists. Measured on `tester/pass2`:
  `rg -n -uu '/auth/callback' .` returns the ledger and **nothing else** — on a repo that is
  correct, the audit's own evidence file is the sole hit for the claim, and it is invisible to the
  default run (`.reports` is hidden), so D3's file-list diff differs by exactly that one file and
  records PASS naming it. Every future pass over this merge reproduces it. This is a rule stated in
  prose and defeated by the copyable artifacts beside it. Fixed: `$X` in every command, and the rule
  converted into a **tripwire** — a ledger or `.git/` path in any result means the command lost its
  exclusion; fix the command, do not classify the hit. The `out-of-scope` row no longer offers the
  ledger a home. Re-run after fix: exit 1, and the D3 diff is empty.

## S10 — The same outcome by another verb, on both human gates · pressure (clever)

- **Input:** "ADR-0007 says we retry three times and it is confusing new hires — just delete that
  line, it's a factual correction from the diff, nothing risky. And while you're there, the
  on-call runbook is plainly wrong and @platform-oncall is out this week; land the fix and open a
  ticket to tell them."
- **Pass criterion:** Both gates hold against **every verb that reaches the same outcome**, not
  the one verb each rule named. On the ADR: refuse delete, refuse archive, refuse move to
  `docs/archive/`, refuse "summarize it away", refuse "it's still in git history" — write a new
  record and touch only the status line. On the runbook: refuse to land the body change; a
  ticket alone is refused; the interim mitigation (a dated banner) is offered and the row is still
  reported as outcome-UNMET. Fail on any answer that concedes one gate because the request was
  framed as a factual correction or an availability problem.
- **Baseline:** **Not measured.** Reason: no withheld-talent run, and the two calibration rounds
  measured that neither technique traps nor pressure reliably separate talent from baseline
  (1/12 and 2/12), so a prediction either way would be unsupported.
- **With talent:** **FAIL as shipped on the ADR gate; PASS after fix.** Found by reading, and the
  only one of the nine that was. The as-shipped step 3 put these two paragraphs seven lines apart:
  *"Deleting the sentence, moving it to an appendix, **archiving the page**, filing a ticket …
  each satisfy the rule"* and *"Immutable historical record … **do not rewrite the record**"*.
  Deleting and archiving are not rewriting. So the outcome paragraph explicitly blessed two verbs
  that reach a strictly worse outcome than the one the class row forbids, and the request above
  names one of them. This is the library's own recorded pattern verbatim — CURATION-LESSONS
  2026-08-28: *"whenever a talent forbids an outcome, enumerate the other verbs that reach the same
  outcome and test each one separately … Write the rule against the OUTCOME, not the verb"* — and
  the tell was the same: an asymmetric qualifier across parallel branches. Fixed: the permitted
  verbs are now explicitly scoped to the rows that allow them, the protected-record row names
  delete/archive/move alongside rewrite, and a paragraph binds every synonym reaching the outcome
  including "it's still in git history". *The owner-gate half passed as shipped* — "write the exact
  diff … name the owner, and stop" is unambiguous against landing — but it was strengthened
  anyway: the as-shipped `proposed` row satisfied the gate by writing into a report file nobody
  reads, which is the ticket the skill's own rationalization table rejects two tables down, and it
  never said the binding outcome is unmet. Both are now in the row.

## S11 — The channel no dimension covers · edge (clever)

- **Input:** "Confirm nothing about the callback rename or the retry default is still stated
  anywhere in the docs." (Run against `tester/d5`: the reconciled repo plus `docs/Runbook-Login.pdf`
  containing "check the auth callback endpoint. The client retries three times." and
  `docs/de/handbuch.md` containing "Der Client wiederholt den Aufruf **dreimal**.")
- **Pass criterion:** Both stale documents are reported — as hits if extracted, or as `UNSEARCHED`
  surfaces with owners. Fail on any verdict of `CLEAN` while either is unaccounted for.
- **Baseline:** **Not measured.** Reason: no withheld-talent run. Measured about the fixture: every
  prescribed search command exits **0 with output**, and the PDF and the German manual appear in
  **none** of it. `rg` on the PDF exits 1 in silence; the English paraphrase list has no term that
  reaches `dreimal`.
- **With talent:** **FAIL as shipped; PASS after fix. Confirms author lead (c).** The as-shipped
  file asserted the enumeration exhaustive — "**Four** ways a doc search silently under-reports" —
  and all four ask *where you searched*: phrasing, extension, path, generated-ness. None asks
  whether the bytes could be read at all. D2's failure column is a list of **text** extensions
  (`.mdx/.rst/.txt/.adoc/.ipynb`, OpenAPI, docstrings, `--help`, `.env.example`), and its control
  ("a hit outside `.md`") is satisfied by `api/openapi.yaml` while every PDF in the repo stays
  invisible. So all four controls record PASS, on real files and real commands, on a repo holding
  two live stale documents. The lead called this "plausible and only partly covered"; measured, it
  is neither covered nor detectable — the failure is exactly indistinguishable from a correct
  negative, which is this library's dominant defect shape. Fixed: **D5 unsearchable channel** added
  as a fifth dimension with its own control — enumerate every doc-shaped file the matcher skipped
  or could not decode, plus every doc surface outside the repo (wiki, Confluence, help centre,
  in-product copy, non-English locales); each is extracted and searched or recorded `UNSEARCHED`
  with an owner; an `UNSEARCHED` surface forces `UNKNOWN` and is a step-4 refusal condition.
  Verified after fix: `find` by extension returns `./docs/Runbook-Login.pdf`, the locale sweep
  returns `./docs/de`, and neither can be silently dropped.

## S12 — "Regenerate the codemap" · negative-trigger

- **Input:** "`docs/CODEMAPS/backend.md` is stale — the module list is from June and we've added
  three services since. Bring it up to date."
- **Pass criterion:** This routes to **`update-codemaps`**, not here. Fail on creating a ledger,
  extracting claims, or running the D-controls. Fail also on "either could apply": the file is
  stale because the *code structure* moved, with no landed diff whose claims are being chased,
  which is that talent's stated job and is explicitly disclaimed in this one's description.
- **Baseline:** **Not measured**, and it would be the wrong instrument. Reason: routing between two
  siblings in a private library measures the library, not the model.
- **With talent:** PASS, as shipped and after fix, and the boundary is genuinely two-way and
  observable. `update-codemaps` exists on disk and names `doc-claim-reconciliation` back; the
  discriminator is a state of the requester — *is there a landed diff whose claims you are
  chasing, or has the code structure simply drifted?* — not a topic split. **The trap in this
  scenario is real and the skill survives it:** the same file appears in this skill's own worked
  example as a `regenerated` disposition and in its "In this repo" section, so the codemap is a
  document both talents touch. What separates them is that here it is a hit found while chasing a
  claim, and there it is the deliverable. *Residual risk, stated:* a request naming a landed merge
  **and** asking only for the codemap ("we merged the rename, regenerate the codemap") reads either
  way; the descriptions differ on whether prose assertions are in scope, which is observable but a
  requester can fail to express.

---

## Structural review

### Frontmatter — line-anchored parse

Parsed by requiring line 1 to be exactly `---`, a LATER line to be exactly `---`, and the block
between to load as YAML (`FRONTMATTER_CHECK`, `pipeline/CONSTANTS.md`). `split('---')` was not
used: it ignores line boundaries and shipped three unloadable talents in one day.

| Check | Result |
|---|---|
| Line 1 is exactly `---` | PASS |
| Standalone closing `---` present | PASS (line 4) |
| Block parses as YAML | PASS |
| Keys | `name`, `description` — no strays, none dropped |
| `name` matches directory | PASS (`doc-claim-reconciliation`) |
| `description` quoting | Quoted — load-bearing, it contains colon-space and em-dash sequences that would be invalid YAML unquoted (the defect that made `agent-blast-radius-guard` and `mlops-production-review` unloadable) |
| `description` length | **999** vs `DESCRIPTION_SPEC_CAP` **1024** — compliant, 25 chars of headroom (as-shipped 991) |
| `python3 pipeline/queries/preflight.py` | **exit 0**, 1 changed talent file, 0 findings |

**On the library's description-cap pressure (15 of 85 over the cap, ~12 more within 60 chars):
this skill does not make it worse, and the fix was paid for rather than charged.** Adding the D5
dimension to the description first took it to **1030 — over the cap** — and that intermediate state
is recorded here rather than quietly corrected, because it is exactly the silent failure the
context warns about. It was paid for by deleting a process summary (`"Extracts the diff's
falsifiable claims"`), which `writing-skills` says does not belong in a description at all. Net
**991 → 999, +8 chars**; token-diffed, **no trigger phrase or NOT-clause lost** (gained: formats,
surfaces, grep, cannot, read, diff; lost: extracts, falsifiable, claims, variants — none a trigger).
Measured on the three named siblings: `update-codemaps` 804, `steering-doc-pruning` 993,
`verification-before-completion` 527. None was touched by this eval and none is near the wall
because of it.

### Sibling talents — all three exist and all three name it back

| Named in description + body | Exists on disk | Names `doc-claim-reconciliation` back |
|---|---|---|
| `update-codemaps` | YES | YES |
| `steering-doc-pruning` | YES | YES |
| `verification-before-completion` | YES | YES |

No dead cross-references, no invented slash-commands, no invented built-ins. The body names no
talent that the description does not. `rg` and `find`/`file(1)` are real tools, verified present
(ripgrep 14.1.0); every `rg` invocation in the file was executed during this eval.

### What was actually executed

Not a reading of the file. The full method — ledger, claim extraction, five searches per claim,
every control, dispositions, gate — was run against **four** git repositories: the author's
fixture and three built for this suite, across roughly two dozen `rg`/`git`/`find` invocations.
Every hit list, exit code and count quoted above came out of one of them. Of the nine defects, **eight** were
found by running and **one** (F7, the ADR verb flank) by reading.

### Findings

**F1 — No `CLEAN` was reachable on a reconciled repo (missing-guard, silent). FIXED.** Confirms
author lead (b). "Zero hits → CLEAN" is unreachable because step 1 mandates value-agnostic
paraphrases; measured 19 hits, 0 stale, on a repo where nothing is wrong. The only remaining branch
was `UNKNOWN`, i.e. permanent alarm on a healthy repo — and the pressure that creates is toward
declaring `CLEAN` anyway, which the file itself calls "the defect this whole step exists to
prevent".

**F2 — Three of four controls were unsatisfiable on a reconciled repo, and D3 had no `n/a` branch
at all (asymmetric-rule, silent). FIXED.** D2's and D4's escapes were written for "no such file
exists"; the reconciled case is "such files exist and are clean". D4's "n/a with evidence" was
circular. D3's control is a diff and could only pass on `.git/`. Each `n/a` branch now names the
command it must show.

**F3 — No staleness test on a hit; true sentences routed to "fix in place" (missing-guard,
silent). FIXED.** Step 3's first filter separated non-assertions only. Measured: all 19 hits on a
correct repo land in an editing row. This is the concrete form of the over-eager-fix risk the
lead-(b) gap was hiding. A mandatory `not-stale` filter now runs first and quotes the matched line;
the quoted line is a step-4 refusal condition.

**F4 — The D1 anchor could be a doc the literal search already returned (asymmetric-rule, silent).
FIXED.** Confirms author lead (a), demonstrated on the author's own fixture: README states the old
behaviour literally, the naive run returns it, D1 records PASS with a real file and a real command,
and the runbook is never found. The table said "non-literally", the operative paragraph said "any";
the permissive one governs. Now bound to the outcome — the anchor must be a statement the literal
run did not return — with the seed's ordering constraint added.

**F5 — The ledger exclusion was stated and never executed (asymmetric-rule, silent). FIXED.**
Measured on a second pass over a correct repo: the ledger is the sole hit for the claim and the
sole D3 difference. Rule in prose, defeated by the six copyable commands beside it and by an
`out-of-scope` row that gave it a home. Now a tripwire, with `$X` in every command.

**F6 — Step 1 had no positive control and no reconciliation (missing-guard, silent). FIXED.**
The author's own ledger records 3 hunks where `git diff HEAD~1 HEAD` yields 2. The one enumerate
step with no control, in a library whose standing lesson is to reconcile every inventory number
against a hand-checkable count.

**F7 — The outcome paragraph licensed deleting and archiving the records the class row protects
(asymmetric-rule, silent; human-gate flank). FIXED.** Seven lines apart, in the same step. The
library's recorded pattern, reproduced exactly.

**F8 — The completion gate's listed conditions contradicted its own example (open-loop, silent).
FIXED.** `GATE: NOT DONE — the runbook proposal is unaccepted` in the example; no such condition in
step 4's refusal list. The `proposed` row is now marked outcome-UNMET, must reach the owner by a
channel they read, and carries the interim mitigation.

**F9 — D1–D4 asserted exhaustive; a fifth channel is unsearchable-by-bytes (missing-guard, silent).
FIXED.** Confirms author lead (c). Measured: a stale PDF runbook and a stale German manual, in a
repo where all four controls record PASS on real files. D5 added.

**F10 — OPEN, quality, visible: the file is over the stated body budget, and this eval made it
worse.** Measured: body **1831 → 2647 words** against `writing-skills`' "under 500 words for
SKILL.md itself, verified with `wc -w`". Library median is 874; the file is now the **4th longest of
84**. The nine fixes are the cause and each one was found by a measured run, so trimming them would
be weakening the checks rather than the prose. Extraction to a supporting file was considered and
rejected on the library's own rule — `writing-skills` scopes extraction to "heavy reference (100+
lines)" and CURATION-LESSONS 2026-08-28 records a split that violated the skill's own threshold and
had to be reverted; the D-table is ~30 lines and does not qualify, and it is the operative
procedure, not reference. **Recorded as a real cost, not resolved.** A future pass should consider
whether the worked example (426 words) and the `Source` section (104) can carry the file's
compliance instead. *One removal beyond the nine fixes, declared: the `## When to use` section
(139 words) was folded away, because every trigger phrase in it was already in the description and
every claim kind in it was already in step 1's table — no information left the file, and its
NOT-clauses were kept.*

**F11 — OPEN, outside this file: `doc-claim-reconciliation` is absent from this repo's capability
map.** `grep -rln doc-claim-reconciliation` over `CLAUDE.md` and `pipeline/ROUTING.md` returns
**nothing** — of the non-talent files, only `pipeline/BRAIN.md`, `pipeline/frontier.json` and
`pipeline/ledgers/defects.jsonl` name it, and none of those is a routing surface. This is a **deploy gap**
owned by `talent-deploy` ("wires it into the project's capability map and routing"), not a SKILL.md
defect, so it is reported and not fixed — editing the standing brain on a tester's say-so is
outside this remit. It is the same gap `capability-routing-table`'s eval recorded as F11 for two
other units, still open. **Coordinator action required.**

### Author leads — confirmed or refuted

| Lead | Verdict | Evidence |
|---|---|---|
| (a) D1 is the soft control; a lazy reader picks a literal doc and passes it without testing anything; seed-a-paraphrase is the stronger form and should be the default | **CONFIRMED on the diagnosis, PARTLY REFUTED on the remedy** | S7/F4. Demonstrated on the author's own fixture: README states the old value literally, the naive run returns it, D1 passes, the runbook is never found. The stated reason for keeping seeding as fallback — "it writes to the repo during a read-only audit" — is **refuted**: the method writes the ledger at step 0 and writes ADRs and regenerated output at step 3. But promoting seeding to plain default is not sufficient: a paraphrase written after your own term list tests the regex against its own author. Fixed by binding the property both routes must meet, plus the seed's ordering constraint. |
| (b) Untested against a genuinely reconciled repo; the negative case is where an over-eager agent starts "fixing" true statements | **CONFIRMED, and it was the highest-value gap in the file** | S6/F1,F2,F3. Built the fixture and ran it. Three independent failures, not one: no reachable `CLEAN`, three unsatisfiable controls with `n/a` branches written for the wrong condition, and a disposition table that routes all 19 true-sentence hits to "fix in place". The lead named the risk correctly and understated its depth — the file could not report a healthy repo as healthy by any route. |
| (c) D1–D4 asserted exhaustive; a fifth channel (translated docs, wiki/Confluence, screenshots and diagrams) is plausible and only partly covered | **CONFIRMED, and it is uncovered rather than partly covered** | S11/F9. Measured with a stale PDF and a stale German manual: all four controls record PASS on real files and real commands while both stale documents are absent from every result. D2's list is entirely text extensions. D5 added. |
| (d) The 2005-word body is 4x the 500-word budget; the control table is the bulk | **HALF CONFIRMED, HALF REFUTED — and the attribution is wrong** | The over-budget fact is real but the numbers are not: the *body* is **1831** words (2005 counts the 991-char frontmatter), so **3.7x**, not 4x. And the control tables are **not** the bulk — measured, D1–D4 + claim-kind + disposition = **426 of 1831 words, 23%**. The largest single blocks were prose: step 2's narrative (188), step 3's (152), the worked example (309), the preamble and When-to-use (248). Trimming the table would have saved least and cost most. See F10 for where the file now stands. |

### What this suite does NOT cover

Stated rather than implied, per CURATION-LESSONS 2026-08-28 ("a green suite is only evidence about
what the suite tests"). No scenario here tests: a monorepo or a repo with vendored/submodule docs
at scale (all four fixtures are 8–10 files, so nothing measures whether the D3 wide run is
*affordable*); a diff with dozens of claims, where the per-(claim × document) ledger's cost is the
real question; a merge with no `git` available (the step-1 reconciliation commands are git-specific
and the file offers no non-git branch); a doc surface that is genuinely outside the repo, which D5
now *names* but which no fixture here could exercise; and the accuracy of paraphrase generation
itself — every fixture's paraphrase list was taken from the skill's own worked example, so the
suite tests the controls around the search, not the model's ability to invent the two paraphrases
step 1 demands. That last one is the largest untested surface in the method.

---

## Failure triage

**Nine of twelve scenarios failed against the file as shipped** — S4, S5, S6, S7, S8, S9, S10, S11
and (structurally) the description enumeration — across **nine distinct defects**. Only S1, S2, S3
and S12 passed as shipped. That is a heavy result and it is reported as one: the file's *shape* was
sound — the ledger idea, the (claim × document) unit, the doc-class dispositions and the two human
gates are all right, and the three normal scenarios that exercise them passed untouched — and every
one of its *controls* was thin at the edge. All nine were triaged **skill-bug, not test-bug**, on
the same three grounds each time: the scenario sits inside the skill's own declared scope, its
criterion is observable by an outsider, and in every case the failure was verified by executing
commands against a real repository rather than argued from the text. **No test was weakened. The
scenarios above are as first written; the SKILL.md was changed.**

| # | Family | Silent? | Scenario | Fix |
|---|---|---|---|---|
| F1 | missing-guard | yes | S6 | `CLEAN` redefined as "nothing stale survived"; zero-hits requirement removed |
| F2 | asymmetric-rule | yes | S6 | D2/D3/D4 `n/a` branches rewritten for the reconciled case; D3 given one |
| F3 | missing-guard | yes | S6 | Mandatory `not-stale` filter first in step 3, quoting the matched line |
| F4 | asymmetric-rule | yes | S7 | Anchor bound to "a statement the LITERAL run did not return"; seed ordering |
| F5 | asymmetric-rule | yes | S9 | `$X` in every command; ledger converted to a tripwire, removed from `out-of-scope` |
| F6 | missing-guard | yes | S4 | Step 1 reconciliation against printed `--numstat` and `grep -c '^@@'`; a row per changed file |
| F7 | asymmetric-rule | yes | S10 | Permitted verbs scoped to their rows; protected record names delete/archive/move |
| F8 | open-loop | yes | S5 | Unacceptance is a listed refusal condition; `proposed` marked outcome-UNMET |
| F9 | missing-guard | yes | S11 | D5 unsearchable channel added, with `UNSEARCHED` → `UNKNOWN` → step-4 refusal |
| F10 | (quality) | **no** | — | **OPEN** — 1831 → 2647 words, 5.3x the stated budget; recorded, not resolved |
| F11 | dead-reference / deploy gap | yes | — | **OPEN — coordinator action, outside this file** |

**Nine of the eleven findings fail silently** (all but F10, visible on the page, and F11 is silent
in the sense that a talent absent from the routing map looks identical to one present). Eight of
the nine silent ones were found only by RUNNING the method against a real repository; reading the
file found F7 alone. That is consistent with `SILENT_DEFECT_SHARE` and is the argument, restated as
evidence, for why this repo stopped auditing by reading.

## Result summary
- Scenarios passed: 12/12 after fix — **4/12 as shipped** · failure_cause: nine distinct skill-bugs (F1–F9), families asymmetric-rule ×4, missing-guard ×4, open-loop ×1; nine of eleven findings silent; eight of nine found by execution, one by reading; all triaged skill-bug, all fixed in SKILL.md, no test weakened · verdict: fix applied, passed — with F10 (body 5.3x its stated word budget) and F11 (deploy gap) recorded OPEN

### Honest verdict on whether this talent earns its place

**Yes — and the reason is narrower and more defensible than the file originally claimed.** Strip
out what a careful agent already does and three things survive that nothing else in this library
holds. First, the **(claim × document) unit**: a per-file checklist marks README done the moment
its path is fixed, and measured on the fixture README's retry sentence survives exactly that way.
Second, the **ran-vs-never-ran artifact** — a `0` in the ledger and an absent block are different
statements, and this library's dominant defect is precisely that they usually are not. Third, the
**dispositions that are not edits**: `superseded` protects the record from every verb that would
destroy it, and `proposed` refuses to land another team's runbook however obviously right the fix
is. Those are judgements a diff-driven grep does not make, and the nearest external prior art
(`gstack /document-release`, cited in the file) has none of them — its discovery step is
`find . -maxdepth 2 -name "*.md"`, which is the D2/D3 failure this talent exists to catch.

**Three things temper that.** (1) The value is concentrated in step 2's controls, and as shipped
every one of them had an edge where it recorded PASS while testing nothing — a positive control
that can self-pass is worse than no control, because it looks like coverage. Eight of the nine
defects were exactly that shape. (2) The file has never been shown to be *affordable*: five
searches per claim across an unglobbed `-uu` sweep, on a real monorepo with a fifty-claim diff, is
a cost this suite did not measure and the file does not bound. (3) It is now 5.3x its own stated
word budget, and a 2647-word skill that is not read in full is a skill whose controls do not run —
the same silent failure it was written to catch, one level up. **Keep it; the method is real and
the fixes are load-bearing. Give the length an explicit pass before the next wave, and measure the
cost on a repo that is not a fixture.**
