# gstack's tests, read properly

*Written 2026-08-26. `garrytan/gstack`, cloned at `ad84005` ("v1.69.0.0 fix: the silent-failure
wave"), MIT. Target: the **374 files in `test/` — 87,380 lines of TypeScript**. The repo carries 554
test files in total; the other 180 live in `browse/test` (140), `design/test` (11),
`ios-qa/daemon/test` (10) and `make-pdf/test` (10) and are outside this brief.*

*This is Pass 2. Pass 1 (`OTHERS-MINED.md` §1) read 8 of these 374 and produced twelve findings from
2% of the corpus. Everything §1 names is out of scope and is not restated here — the catalog budget,
`datamark()`, the question registry, the provider contract, `context-bill`'s divisors, the
`e2e-gate` tier split, carve-guards, and the three preamble refusals. Where a finding below touches a
file §1 also touched, it is because §1 stopped short of something inside it.*

---

## Coverage — what I read, skimmed and skipped

**Method, stated so it can be checked.** 374 files cannot be read line-by-line with attention in one
pass. So: mechanical scan first, cluster, then read.

1. **Five repo-wide mechanical scans** over all 374 files: numeric constant declarations
   (`const [A-Z_]+ = <number>`), the strings `ratchet` / `same commit`, negation density
   (`not.toContain` / `never` / `MUST NOT` per file), `fail-open|fail-closed`, and `toMatchSnapshot`.
2. **Every file's doc-comment header read** — all 374. gstack writes a 5–30 line purpose block at the
   top of nearly every test file, naming the defect class, the issue number and often the observed
   numbers. That header is the cheapest high-signal artefact in the repo and reading all of them is
   what made targeting possible.
3. **Cluster, then read in full** the clusters touching Layers A–G.
4. **Sampling rule for the rest:** a file was opened if its header named a number, a defect class, an
   invariant, or a refusal. A file was skipped if its header described platform portability
   (Windows/BSD path handling), installer plumbing, or a rename migration with no transferable
   mechanism. 76 files (20%) are static text-greps over source or prose; those were sampled at both
   ends — the best (`no-suicide-exit`, `egress-receipt-wiring`) and the worst (`jargon-list`).

| Cluster | Files | Read in full | Read in part | Header only | Why |
|---|---:|---:|---:|---:|---|
| Budgets, catalog, parity, context-bill | 13 | 8 | 3 | 2 | The brief's stated gap. Layer D + E. |
| Redaction / secrets / secret-sink | 11 | 6 | 2 | 3 | Layer A gate, Layer G. Highest §3 density. |
| Egress receipts + code-intelligence consent | 5 | 1 | 3 | 1 | Layer E relay + spend. |
| Evidence, strict-output, exit-propagation, suicide-exit | 5 | 3 | 2 | 0 | Layer C/E acceptance. Best single find. |
| Questions / preferences / one-way doors / session-kind | 9 | 4 | 3 | 2 | Layer A intake. |
| Test-infra invariants (tier alignment, hermetic, harness audit, shards) | 12 | 4 | 4 | 4 | Our build process. |
| `skill-e2e-*` behavioural evals | 70 | 3 | 3 | 64 | Paid, model-behaviour. Sampled the ones with numbers. |
| `gbrain-*` / `brain-*` / memory | 32 | 1 | 3 | 28 | Coupled to their hosted brain. Sampled for mechanism only. |
| `gstack-*` core libs | 38 | 3 | 5 | 30 | Mixed. Sampled by header. |
| `setup-*` installer | 17 | 0 | 1 | 16 | Installer plumbing. Nothing transferable. |
| `codex-*` provider dispatch | 10 | 0 | 1 | 9 | Provider-CLI specifics. |
| `regression-*` / `migrations-*` / `upgrade-*` | 10 | 1 | 1 | 8 | Mostly shell portability. One kept. |
| `model-overlay-*` | 5 | 0 | 0 | 5 | Per-model prose nudges. Taste, not mechanism. |
| `ios-*` | 4 | 0 | 0 | 4 | Out of domain. |
| Everything else | 133 | 6 | 8 | 119 | Sampled per the rule above. |
| **Total** | **374** | **~40** | **~39** | **~295** | |

**Honest accounting: roughly 9,000 of 87,380 lines (~10%) were read as source; 374 of 374 headers
were read; five mechanical scans covered 100% of the corpus.** That is 5× Pass 1's reach on source
and 47× on headers, and it is not completeness. The `gbrain`, `setup` and `codex` clusters — 59 files
— are genuinely under-read, and the 70 `skill-e2e-*` files are represented by three. If a later pass
wants a target, `gbrain-*` is the largest unread block and the one most likely to carry a memory
mechanism worth Layer D.

**Where the numbers came from.** Every figure below is quoted from the file that asserts it. Where a
comment supplies the derivation or the history of a constant, that is quoted too, because the history
is the finding — a number with no story behind it is a guess someone typed.

---

## 1 · Budgets, caps and ratchets

### 1.1 Every budget here has a floor as well as a ceiling — Layer D

`test/skill-size-budget.test.ts` runs four assertions against a frozen baseline
(`test/fixtures/parity-baseline-v1.47.0.0.json`) and only two are ceilings:

- **Per-skill growth ceiling ×1.50**, with the ratio's whole history in the comment: *"Adjusted
  v1.52.0.0 from 1.05 → 1.50: a 5% ratio tripped on legitimate feature additions (plan-tune cathedral
  T13 grew SKILL.md ×1.24 adding load-bearing Dream cycle + Audit unmarked + Recent auto-decisions
  surfaces). **Real bloat is 2-3×; this catches that while not tripping on normal feature scope.**"*
- **Corpus-total ceiling**, same ×1.50 against `totalCorpusBytes`.
- **Per-skill shrink FLOOR ×0.80** — *"A skill that was 100 KB at v1.47.0.0 and shrinks to 250 bytes
  passes [the 200-byte noise floor] despite losing 99.75% of content."* The failure message names the
  diagnosis: *"accidental body strip (a resolver returning empty, a template losing a section)."*
- **Catalog token estimate ≤ 7,000**, measured against the **committed** tree, not the live one —
  because parallel workers regenerate files mid-run and the live estimate was *"4177 solo, 8356 and
  8041 in two parallel runs."*

`test/catalog-budget.test.ts` — the file Pass 1 found — does the same and Pass 1 missed its third
test: beside the 1,150 token-equivalent aggregate and the 260-byte per-entry cap sits **`every skill
has a non-empty description`**. Cap and floor, again.

**Layer D's catalog problem has a second half nobody has written down.** A component whose `Contract`
summary silently empties still passes an under-budget check, and the matcher then never selects it.
A ceiling alone cannot tell "we trimmed it well" from "we deleted it." **Take both directions or
neither.**

### 1.2 The override is a reason string that lands in an audit log — Layer E

No budget here is overridden by a boolean: `GSTACK_SIZE_BUDGET_OVERRIDE_REASON="why this is OK"`,
`EVALS_BUDGET_OVERRIDE_REASON="…"`. `test/helpers/budget-override.ts` argues it in full:

> *"a hard cap with no escape valve becomes operationally hostile (legit price changes, longer
> transcripts, new required evals can all blow the cap). An escape valve with no audit becomes
> 'everyone overrides everything and we lose the gate.' This module is the audit half."*

The JSONL record at `~/.gstack/analytics/spend-overrides.jsonl` carries `timestamp, scope, reason,
details` **plus provenance** — `ci`, `runner`, `branch`, `commit` (8 chars) — and the write is
best-effort: *"don't fail the test on audit-write errors."*

**Layer E's spend ceiling should be this shape and is not.** A ceiling a founder cannot raise at 2am
is one they disable in code; a ceiling raised silently is not a ceiling. Reason + branch + commit is
the third option.

### 1.3 Two instruments, not one: a ratio-regression *and* an absolute cap — Layer E

`test/skill-budget-regression.test.ts` runs both over the same eval runs:

- **Relative** — no test may exceed **2× prior tool calls or turns**, with a **noise floor of 5 tool
  calls / 3 turns**. Two metrics, each with a diagnosis: *"a regression that adds tool calls usually
  reflects an inefficient skill prompt; a regression that adds turns reflects a skill that is
  hesitating or losing track."*
- **Absolute** — hard dollar cap per run per tier: **$200 gate, $500 periodic, $300 umbrella**.
  History: *"$25 → $200 gate, $70 → $500 periodic. Prior defaults tripped on normal-scope expansion;
  **new ceilings are 8× the historical worst-case eval run**."*

And the cap's purpose, stated so the number can be argued with: *"to catch runaway evals (infinite
retry, model price change, prompt-blowup bug), **NOT to gate legitimate scope growth**. Set high
enough that real growth never trips it — only obvious-bug territory does."*

Two disciplines in the same file. **First-run grace** — no prior run passes vacuously, because *"the
purpose is to catch a SECOND-run regression."* **Branch alignment** — skipped twice over, if the
latest eval came from a different branch than the checkout and if the prior run did: *"Pre-existing
eval history from other branches is not our regression to fix."*

### 1.4 Where theirs is worse than ours must be: the cost table fails open

`test/helpers/pricing.ts` is a per-model table with an `as_of: YYYY-MM` **per row** (Opus 4.7
$15/$75, Sonnet 4.6 $3/$15, Haiku 4.5 $1/$5, gpt-5.4 $2.50/$10, o3 $15/$60, gemini-2.5-pro
$1.25/$5), cache reads billed at **10%** of input, and an explicit note that cached and uncached
input tokens are **disjoint fields — do not subtract.** Then: *"When a model isn't in the table,
`estimateCost` returns **0** with a console warning."*

**That is a fail-open in the spend ceiling.** The $200/$500 cap reads `total_cost_usd`; an unpriced
model costs $0 and the cap can never fire — in exactly the condition ("model price change", a new
model id) the cap says it exists for. **Layer E must treat an unpriced model as a refusal or a
pessimistic upper bound, never zero.** Take the `as_of` stamp and the warn-once; leave the `return 0`.

### 1.5 A floor on a timeout, derived from a live census — Layer E

`test/eval-detach-timeout-floor.test.ts`: the watchdog wrapping the sharded paid runner must be
**≥ `ceil(shards / jobs) × shardTimeout × 1.05`**, computed from the live shard census, with the 5%
margin itemised (*"detach setup, lock wait, aggregation"*). The near-miss is the finding: *"That
nearly shipped once (**a review pass proposed 10800s against a 19,800s gate worst case**), so the
bound is enforced against the LIVE shard census instead of a comment snapshot that goes stale every
time a paid test file is added."* A watchdog at 55% of worst case *"kills a healthy run mid-flight
and the tail shards report never-started: **paid truncation by configuration**."* The failure message
offers two honest remedies — raise the timeout, or reduce the tier's worst case — and no suppression
flag.

**Layer E's build timeout must be `f(build plan)`; chosen rather than derived, growth in Layer C turns
silently into truncated builds that look like failures.**

### 1.6 The ratchet protocol, in full, because it is the part everyone skips

Printed inside the failure message:

> *"Adding a skill? Re-measure with `bun test test/catalog-budget.test.ts` (the failure prints the new
> total). Update `CATALOG_BUDGET_TOKEN_EQUIVALENTS` **AND the derivation comment (ref/date/value/which
> skill moved it) in the SAME commit.** Growing an existing description? Trim it instead — the catalog
> is what every host loads at discovery, every session."*

Above the constant sits a `method` block that lets anyone reproduce the measurement: the enumerator
(`skillCensus().authoredSkills`, symlink-deduped, root router excluded), what is summed
(`byteLength(name) + byteLength(description)`), the conversion (`ceil(bytes / 4)`), the result
(**53 skills = 4,371 bytes / 1,093 TE, + root router alias 49 bytes = 4,420 bytes / 1,105 TE, measured
2026-08-12**), the ceiling (1,150 TE = 4,600 bytes), the headroom (**180 bytes, ~4%**), the dominant
entry (**design-consultation, 229 bytes**). Header: *"Budget derivation (re-derive it, do not trust
the number)."*

---

## 2 · Invariants worth stealing

### 2.1 Exit 0 is not evidence — Layer C, Layer E

Three files, one argument, and after the catalog budget it is the strongest thing here.

`test/no-suicide-exit.test.ts` statically scans every `*.test.ts` for `setTimeout(() =>
process.exit(...))`, and says why with the number:

> *"`bun test` runs EVERY test file in one process. The pattern of arming a 500ms timer in `afterAll`
> whose callback calls `process.exit(0)` assumes each file gets its own process. It doesn't: the armed
> timer fires 500ms later, mid-way through a LATER test file, and kills the entire suite with exit
> code 0 and no summary. The truncated run silently masks every downstream failure (**observed: only
> ~16 of 434 files ran, shell exit 0**)."*

**96% of a suite skipped, green.** `test/exit-propagation.test.ts` is the fault-injection companion —
it builds real fixture suites, runs `bun test` on them, and proves *"the truncated run is
indistinguishable from a green one by exit code alone."*

`scripts/test-strict-output.ts` (pinned by `test/strict-output.test.ts`) is the fix.
`strictTestExitCode` **refuses a zero exit** when (1) failure lines were printed, (2) **fewer files
ran than were planned** — "invisible non-execution", or (3) an unhandled error fired between tests.
And a parsing detail with teeth: stdout and stderr are independent pipes, so the classifier keeps
**per-origin buffers** — *"a single shared buffer glues the fragments into garbled lines: a sheared
`(fail)` line goes uncounted (defeating the exit-0-with-failures backstop) and a sheared summary reads
as truncation."* Two tests drive exactly that interleaving.

**Layer E's gates report "the tests passed", and that claim is currently an exit code.** It must be:
the lanes I declared ran, the executed-unit count matched the planned count, and no failure line was
printed — all three.

The same file adds a fourth: *"Installing any SIGINT/SIGTERM listener suppresses Node's default
terminate-on-signal. Pre-fix, the forwarder killed the current child and **the parent LIVED ON — the
paid worker pool kept launching API-burning shards after Ctrl-C**."* `isTerminationRequested()` is
exposed so launch loops stop taking new work. **Cancellation must terminate the run, not the current
child** — a ceiling that only kills the in-flight job is not a ceiling.

### 2.2 The evidence ledger — a claim bound to a hash of the tree it was made about — Layer C, E

`bin/gstack-evidence`, 409 test lines. `run --label X -- <cmd>` records; `check --label X` grades
**FRESH / STALE / MISSING** and exits 0/1. The record: `label · command · cmd_sha256 · exit ·
duration_s · commit(40 hex) · tree(40 hex) · wtree(40 hex) · dirty · log_path`.

`wtree` fingerprints the **working tree**, and that is the design. The test named KEYSTONE: *"evidence
recorded on a dirty tree stays FRESH after committing the exact tested content"* — tests run at
`/ship` Step 5 on uncommitted code, Step 15 commits it, HEAD's tree changes, the content does not.
Everything else follows from binding to content rather than to a commit:

- **TOCTOU guard** — if the command mutates the tree mid-run (`wtreeBefore ≠ wtreeAfter`) the
  fingerprint is **omitted**, `check` prints *"no content fingerprint"* and grades STALE. *"Never
  certifies unseen content."*
- **Gitignored churn does not invalidate; a new untracked source file does** — `scratch.txt` FRESH,
  `brand-new.ts` STALE.
- **`--allow-paths CHANGELOG.md,VERSION,package.json`**, with the negative pinned in the same test:
  *"A source change is NOT rescued by the allow-list."*
- **`--expect-cmd` binds the label to the exact command** via `cmd_sha256` → `cmd_sha256 mismatch`.
  This is what stops "I ran the test lane" meaning something narrower.
- **A recorded FAILING run is never FRESH. A fabricated fingerprint degrades to STALE, never crashes.
  Outside a git repo, STALE. `--max-age 24` expires**, and a non-numeric `--max-age` is *"a usage
  error (exit 2), never a silent fail-open."*
- **`a green lane never masks a red sibling: every named label must be FRESH`**, and **`MISSING` for a
  label that never ran** — *"explicit labels prove expected lanes."*
- **A HIGH credential in the command is stored redacted, but `cmd_sha256` binds to the ORIGINAL exact
  string.** Hash the truth, store the redaction.
- **`TRANSPARENCY: ledger failure never breaks the command`** — an unwritable `GSTACK_HOME` yields
  exit 0, real output, and a warning. An observability layer must not be able to fail what it observes.

**Layer C writes acceptance criteria; Layer E reports them met. Nothing today binds "met" to the bytes
it was met against.** This is that binding, in one 40-line record.

The same file carries a second finding. `bin/gstack-evidence` has a bun shebang, so bun auto-loads
`.env` into `process.env` and every spawned child inherits it. Two harms are named and the **worse one
identified**: not the credential leak but *"it changes the behaviour of the command being certified —
**the ledger would vouch for a run that differs from the one CI performs**."* The scrub warns naming
the key, never the value, and a CONTROL test proves a var the shell legitimately exported **survives**.

### 2.3 Three-state completion — Layer C

`test/ship-plan-completion-invariants.test.ts` (VAS-449). Plan items are **DONE / NOT DONE /
UNVERIFIABLE**:

- **Path concreteness rule** — an item naming a concrete filesystem path *"MUST be classified DONE or
  NOT DONE based on `[ -f …]`"*, not on the agent's belief.
- **Validator detection** — a project's `package.json` `validate-*` scripts auto-run, and *"a passing
  validator promotes the item from UNVERIFIABLE to DONE."* A documented promotion path out of the
  middle state.
- **Per-item confirmation is mandatory** — *"Do NOT use a single AskUserQuestion to blanket-confirm."*
- **Subagent failure is fail-closed**, and the old permissive sentence is pinned deleted (§3.5).

**Ours is binary and theirs is better.** Layer C will contain criteria no gate can check; today those
get marked done on an agent's say-so, or block the build.

### 2.4 The inert declaration — the defect class Layer B will hit

`test/e2e-tier-alignment.test.ts`. A registry (`E2E_TIERS`) says a test is `periodic`; the file itself
self-gates on `EVALS_TIER === 'gate'`. They disagreed:

> *"the #2077 demotion of the plan-mode/finding-floor smokes to 'periodic' was **inert for months**
> because the files still gated on 'gate' and ran in the blocking lane on every gate run."*

Months of paying for tests they believed demoted. The fix cross-checks a declaration against its
enforcement, with two refinements worth copying verbatim. **The invariant's own regex is fail-open, so
it enumerates shapes and reports zero-match files**: *"Both quote styles — a mechanical refactor to
double quotes must not silently drop a file from the invariant (fail-open is the defect class this
test exists to kill)."* And **"reported, not asserted"** — files the invariant can *see* but not
*arbitrate* are `console.warn`ed as a list; only unambiguous misalignments fail. *"Never silently
skipped."* A third channel between fail and ignore.

**Layer B's `Playbook` is declared in one place and enforced in a build prompt elsewhere; Layer C's
acceptance criteria are declared in a package and checked by a gate.** Both are this defect class.

### 2.5 A catalog entry is a lead sentence; the rest moves to a body section — Layer D

Pass 1 took the 260-byte cap without asking how anyone stays under it. `test/catalog-trim.test.ts` is
the answer: `applyCatalogTrim` **splits every description in two** — the lead sentence stays in
frontmatter (always loaded, always paid for), the routing prose moves to a body section headed
`## When to invoke this skill` (loaded only when the skill is).

Two invariants around it matter as much as the split:

- **Idempotency** — *"calling on already-trimmed output returns the same parts"*; re-splitting keeps
  `lead` identical and `routingProse` empty. A generator that runs every build must be a fixed point
  after the first pass.
- **The opt-out is tested, not just the default** — `test/catalog-mode-full.test.ts` runs
  `--catalog-mode=full` for real, asserts the legacy block returns and *"`## When to invoke this
  skill` should NOT be present"*, restores in a `finally`, and prints `CRITICAL: failed to restore` if
  the restore itself fails. Invalid values throw.

**And the ordering rule that makes a two-tier catalog safe.** `test/cso-preserved.test.ts` states two
guarantees for any split: **PRESERVATION** — content survives somewhere in the skeleton+sections union,
*"a carve relocates, it never drops"* — and **ALWAYS-LOADED CONTRACT** — dispatch stays in the
skeleton and **mode dispatch must precede any STOP-Read**: *"a directive that decides which sections to
read can't sit behind the STOP that reads them."* Asserted on **earliest position of use, not loose
substring presence.**

That second rule is the one Layer D will get wrong: **everything needed to decide whether to load a
component's `Contract` body must be in its lead**, with a test that the decision logic is not in the
half you only read after deciding. `auq-format-always-loaded.test.ts` guards the same for the question
format.

### 2.6 Receipt before send, and a polarity table you cannot add to by accident — Layer E, G

`test/egress-receipt-wiring.test.ts` opens with a scoping statement most security controls never get:
*"THREAT MODEL: the egress ledger is forensic observability — it records ATTEMPTED egress so accidents
are auditable; **it is not an exfiltration control.**"*

- **Receipt strictly before send, asserted structurally** by source offsets:
  `expect(src.indexOf('writeReceipt(')).toBeLessThan(src.indexOf('ctx.fetchImpl('))`. Crude, free, and
  it catches the reordering.
- **The receipt hashes the exact bytes that go out.** `test/egress-lib.test.ts` runs the shell helper
  against a real local listener and asserts `receipts[0].sha256 === sha256Hex(received[0])` — *"same
  file is hashed and handed to curl via `--data-binary @file`."* Pass 1 §1.1's scan-at-sink rule,
  verified against what **arrived**.
- **A POLARITY table pinned as data** — 7 fail-closed, 6 fail-open, each list asserted with an exact
  `toEqual` on the sorted array so a new sink forces a deliberate choice. The rule is written:
  fail-closed when *"gstack state leaving the machine unrecorded is worse than the operation failing"*;
  fail-open for *"user-facing operations that must not die over an audit-log hiccup."*
- **A NEW-SINK SCANNER with no `KNOWN_UNWIRED` bucket** sweeping `bin/ lib/ scripts/ design/src
  browse/src`: every outbound op must be wired **or** carry a written reason in `SCANNER_EXEMPT`.
  *"An unexplained network op anywhere in the swept tree fails the scanner — add real sinks to the
  wired lists above, not here."*
- **The refusal message shape is itself the assertion.** Four `toContain`s: **problem** (`lib-test NOT
  sent`), **cause** (the typed error `EGRESS_RECEIPT_FAILED` quoted verbatim), **fix** (`Fix: chmod -R
  u+w`), **what this is** (`ATTEMPTS to send off-machine`). Copy this into the `Playbook` as the
  required shape of every refusal Scio emits.
- **Brittle by design** — stated in two separate tripwire files: *"renaming a helper must force the
  author to look here."* An unusual thing to declare out loud, and correct.

### 2.7 Four smaller invariants, each one line of Scio design

- **A command declared in a repo file is untrusted until a human trusts it.**
  `test/verify-gate.test.ts`: a project `CLAUDE.md` may declare `<!-- gstack:verify: <cmd> -->`, and it
  **never runs** until recorded via `--trust`; trusted-and-failing exits 2 so the turn cannot end;
  nothing declared exits 0 — *"Absence never blocks."* Plus *"`./setup` never registers the gate."*
  **Layer E runs builds shaped by generated repos; anything in one that could cause execution needs
  this exact per-repo, per-command trust step.**
- **Never render a missing value as a good value.** `test/security-dashboard-fallback.test.ts` (#1947):
  a backend, network or `jq` failure used to render **"0 attacks"** — *"indistinguishable from a
  genuinely healthy reading on a security-signaling surface."* The contract is four-state: error →
  `unknown`; `jq` missing → `unknown — install jq`; 200 with `status:"ok"` → **trusted**; 200 without
  the marker → shown **+ `unverified`**. Every meter Scio ships has this failure mode; a zero from a
  broken pipe reads as good news.
- **Know whether anyone is there to answer.** `test/gstack-session-kind.test.ts` classifies before
  asking: `spawned` → **auto-choose**, `headless` → **BLOCK on question failure**, `interactive` →
  **prose fallback**. Precedence is tested (`OPENCLAW_SESSION` wins over headless and Conductor
  markers), and the test runs with a **scrubbed env** because *"the test process itself runs inside
  Conductor, so `CONDUCTOR_*` / `CLAUDE_CODE_*` would leak in and contaminate the classification."*
  **Layer A's gate must not record a defaulted answer as user-provided.**
- **Preference provenance is an allowlist with its own exit code.**
  `test/gstack-question-preference.test.ts` calls the user-origin gate *"THE critical safety
  contract"*: missing `source` → non-zero; `source: 'inline-tool-output'` → rejected *"with explicit
  poisoning message"*; `source: 'anonymous'` → **rejected, not silently permitted**; and **exit 2 =
  user-origin rejection, exit 1 = validation error**, so a caller can tell "refused on provenance"
  from "malformed". **This is the enforcement half of Layer A's per-field provenance.**

### 2.8 Two rules for the `Playbook`, both learned the expensive way — Layer B

**Prefer an explicit setting to a prohibition.** `test/run-in-background-guidance.test.ts` (#2440,
which itself regressed the fix for #497):

> *"Claude Code v2.1.198 made subagents run in the BACKGROUND by default. Guidance written before that
> (**'do NOT use run_in_background'**) stopped producing a foreground run — the review army and
> autoplan dual-voice steps **silently launched specialists in the background and merged before they
> completed**. The only guidance that works post-2.1.198 is an explicit `run_in_background: false`."*

A rule phrased as a prohibition inverted itself when a host default flipped, and nothing failed. The
tripwire scans **every** generated skill file *"so the regression can't migrate to another skill
unnoticed."*

**Every path interpolated into a prompt must be absolute and host-resolved.**
`test/question-tuning-registry-path.test.ts` (#2489): the preamble pointed at a **relative**
`scripts/question-registry.ts`, which never resolves from a user's project cwd, so *"the lookup
silently failed and agents fabricated ids via the `{skill}-{slug}` fallback (**one observed
`/plan-eng-review` session: 21/21 unregistered**)."* **The failure mode of a broken path in a prompt
is not an error — it is fabrication.** The test asserts the correct path per host, that **no host
renders the bare relative shape**, and that the interpolated path points at a file that exists.

### 2.9 One enumerator, not two — Layer D

`test/helpers/skill-census.ts` exists because two test files had **two different hand-rolled directory
walks** and diverged. The comment where the duplicate used to be: *"they were duplicated here with a
DIFFERENT hand-rolled directory walk, which is **the divergence class `skill-census.ts` exists to
kill.**"*

The census returns **three counts that deliberately differ**, and `test/skill-census.test.ts` pins the
relationships rather than the totals (*"No hardcoded totals here — the catalog-budget test owns the
ratchet"*): `physicalSkillFiles` (every file on disk, root router and symlink dups included),
`authoredSkills` (symlink-deduped, router excluded), `registryEntries` (unique frontmatter names +
root alias) — with `registryEntries.length ≤ physicalSkillFiles.length` because *"it can only collapse
entries relative to physical, **never invent them**"*, and *"every registry entry a host would see
resolves back to a physical SKILL.md."*

**Layer D will have the same three counts** — component files, distinct components, catalog-addressable
`Contract`s — and they will not be equal. One module must produce all three. The rule recurs twice
more: `gbrain-exec-invariant` (every `gbrain` CLI call routes through one module) and
`hermetic-wiring` (every E2E runner builds its child env through `hermeticChildEnv()`, no
`...process.env` spread — *"local evals silently re-contaminate and nothing fails until a human
notices weird results again, **which took three burned suites last time**"*).

### 2.10 Confidence that starts uncertain and decays — Layer F

`test/taste-engine.test.ts`, the design-preference profile: **Laplace-smoothed confidence** =
`approved / (approved + rejected + 1)`, so one approval → **0.5** and five → **5/6 ≈ 0.833** — a single
yes never reads as certainty. **5%/week decay applied at read time**, not by a background job:
`0.95^weeks`, four weeks → ×0.815, three years ≈ 156 weeks → `0.95^156 ≈ 0.00036`, with a test that it
**never goes below zero**. The stored number stays raw evidence; decay is a view. **Session log capped
at the last 50, FIFO.** **Taste-drift detection** warns on stderr, naming the value, when an approved
value carries a strong opposite signal (confidence > 0.6 **and** count ≥ 3); one rejection does not
warn.

The moment Layer F remembers anything across builds it needs all four — especially decay-at-read and
the drift warning, because a user's taste in month six contradicts month one and that is not a bug.

---

## 3 · Tests that assert an absence

### 3.1 The law that makes every other absence test worth running

Stated in `test/helpers/secret-sink-harness.ts`, then obeyed five more times across the repo:

> ***"Positive-control discipline: every test suite using this harness should include one test that
> deliberately leaks a seed and asserts the harness catches it. A harness that silently under-reports
> is worse than no harness."***

**A `not.toContain` passes when the detector is broken, when the feature is deleted, and when the
fixture never established its precondition.** Every serious absence test here is paired with a control
that proves it can fail:

| Absence test | Its control |
|---|---|
| secret-sink harness finds no leak | **six** deliberate leaks — stdout, stderr, file, telemetry, base64, 12-char prefix — each asserted caught |
| no pattern has a catastrophic-backtracking shape | *"a planted catastrophic pattern WOULD be caught by the linter"* — `expect(NESTED_QUANTIFIER.test("(a+)+")).toBe(true)` |
| carved skills pass the carve guards | `carve-guards-negative.test.ts` — *"Proves the guards actually BITE… these prove a BROKEN carve fails."* |
| `gstack-memory-ingest` never calls `put_page` | a second test that it **does** call `put` or `import` — *"guards against accidentally removing all gbrain calls and having the negative test above pass for the wrong reason"* |
| a `.env` value never reaches the child | every leak test **asserts the scrub warning fired**, because the first version *"passed for exactly that wrong reason"* (bun skips `.env.local` under `NODE_ENV=test`, so the fixture proved nothing) |
| no test file schedules a delayed `process.exit` | `exit-propagation.test.ts` runs a real truncated suite and shows `bun test` exits 0 |

That fifth row is the sharpest: **they found their own fixture had never established its
precondition, and fixed it by asserting the mechanism ran rather than that the outcome looked right.**
The same file goes further — an unreadable-`.env` test *probes whether `chmod 000` could even create
unreadability* (it cannot for root / `CAP_DAC_OVERRIDE`) and **skips rather than asserting a condition
its fixture could not create.**

**This is the most transferable thing in 87,380 lines.** Layer A's gate, Layer E's sandbox isolation
and Layer G's tenancy boundary will all be tested by asserting something is absent. Every one of those
needs a twin that proves it can fail.

The harness itself is worth taking: **four channels** — stdout, stderr, every file written under a
per-run `mkdtemp` `$HOME` walked post-mortem, and `.gstack/analytics/*.jsonl` broken out separately
*"for clearer test failures"* — × **four match rules**: exact, **URL-decoded** (percent-encoded
passwords in DSNs), **first-12-char prefix** for seeds ≥16 chars (*"the 'I only logged a portion'
pattern"*), and **base64** for seeds ≥12 chars (auth headers). Both length thresholds exist to bound
false positives, and both are stated. **Its blind spots are published**: subprocess env dump
(*"portable /proc reading is non-trivial"*) and the user's real shell history, each with a reason. And
the best assertion in the file shows the right observable: `expect(r.stdout).toContain('len=43')` —
the length of the secret is visible, the value is not.

### 3.2 "The query never left the machine" — three ways to prove it

`test/code-intelligence.test.ts`, on an unconsented search against a non-loopback provider:

```ts
expect(calls).toBe(0);                      // spy fetch counter — refused BEFORE the network call
expect(ledgerLines()).toEqual([]);          // nothing sent → nothing receipted
expect(fs.existsSync(marker)).toBe(false);  // fake CLI touches a marker; subprocess never ran
```

Three proofs of "before", for three kinds of sink: a counted spy for HTTP, an empty ledger for the
audit trail, a filesystem marker for a subprocess. **A test that only checks the error code cannot
distinguish "refused" from "sent, then errored."**

The receipt is held to a **truthfulness** invariant, not a presence one. A liveness probe is allowed
without consent, and its receipt must say `consent=unchecked` and **must not** say `consented=true`:

```ts
expect(String(lines[0].consent)).toContain("consent=unchecked");
expect(String(lines[0].consent)).not.toContain("consented=true");
```

**An audit record that overclaims is worse than none.** Each receipt carries a typed `payload_class`
(`liveness-probe`, `code-search-request`, `code-search-query`, `brain-export-request`) and, for a
query, `sha256` and `bytes` **of the query text**, because the query is repo-derived content. Loopback
search is exempt and *"writes no receipt (no egress)"* — the exemption is by destination, and tested.
Two more: **default op class is write, so *"a caller that doesn't say gets fail-closed"***, and
**deny beats consent for both op classes.**

### 3.3 Absences that are the whole point of the record

- **The audit log never contains the body.** `test/redact-audit-log.test.ts` logs a review of *"Bob
  Smith is incompetent and customer ACME is churning"* and asserts `not.toContain("Bob Smith")`,
  `not.toContain("ACME")`, `toContain(sha256(secret))`. **Mode 0600**, append-not-overwrite, and the
  CLI takes the body as a **file path** so it never transits `argv`.
- **The diagnostic must not become the leak it prevents** — the `.env` scrub warning names the key and
  is asserted `not.toContain('s3cret-value')` on both streams.
- **Non-preflight skills emit exactly zero bytes** — `totalBrainBytes(skill) === 0` for `ship, qa,
  investigate, retro, design-review`, `> 0` for every registered one. A complete bipartition; cost
  isolation proved in both directions.
- **No tier promotion on a public repo.** A named block, `no visibility-based tier promotion`: an
  email stays MEDIUM on public, `repoVisibility: "public"` is recorded *"for sterner wording"*, and
  `expect(pub.severity).toBe("MEDIUM"); // NOT promoted to HIGH`. **Severity and presentation-severity
  are separated on purpose, and the separation is the test.**
- **Masking fails closed to `null`, never to raw passthrough.** *"The contract is null → caller drops
  the whole payload. **The one thing that must never happen is the secret surviving in the output.**"*
  The test accepts either legal outcome and forbids the illegal one — the right shape when the
  implementation may improve. Two hard cases: **marker-only patterns** (PEM headers, GCP
  service-account JSON) capture only the header, so splicing *"would redact the marker and forward the
  key body"* → return `null`; and **overlapping spans** (a Bearer token that is also a JWT) must
  coalesce into one well-formed marker, asserted `/^Authorization: Bearer <REDACTED-[a-z._+]+>$/`,
  because *"independent splices apply stale offsets and can leave trailing secret bytes."*
- **Suppression is the exception and must be total.** *"UUID suppression requires TOTAL containment"* —
  a real card next to a UUID still reports. **Placeholder suppression is per-span, not per-line**: *"a
  real secret on a line that ALSO contains EXAMPLE still flags."* And the calibration argument with its
  number: *"Observed live: **14 of 21 MEDIUM findings** on one ordinary branch were exactly this, all
  from test files — the volume that makes people stop reading MEDIUM output at all."*

### 3.4 Three layers for one privacy promise

`test/telemetry-repo-strip.test.ts` enforces a sentence in the consent copy — *your repo name is
recorded locally only and stripped before any upload* — three ways:

1. **Coverage** — every repo/branch field the two producers emit is in every strip list. The discovery
   rule is `/repo|branch/i` applied to the producers, so a *future* field named `..repo..` is caught.
2. **Behaviour** — run the **actual** `jq del()` filter and the **actual** `sed` expressions, extracted
   verbatim from the shipped script, over a sample line. *"Catches a broken/edited filter, not just a
   missing line."* Both strip paths (jq primary, sed fallback) are covered, and the jq leg pins that
   *"a line jq can't parse is dropped, never forwarded unstripped."*
3. **Floor** — `repo`, `_repo_slug`, `_branch` are always in the stripped set, *"so deleting a strip
   rule fails CI even if a producer also stops emitting it."*

**Any sentence Scio puts in front of a user about what does not leave their machine needs all three.**
Coverage alone drifts, behaviour alone misses new fields, the floor alone misses the filter breaking.

### 3.5 Absences that pin a deletion

- **A deleted artefact stays deleted, with the condition for reviving it.**
  `expect(existsSync('scripts/proactive-suggestions.json')).toBe(false)` — *"removed (no consumer ever
  read it). If someone re-adds the emitter, this pins the decision to delete it — **reintroduce only
  with an actual consumer**, and restore the determinism tests (sorted keys, root keyed as 'gstack',
  no timestamp fields) that lived here before."*
- **A deleted binary stays deleted, checked with `lstat` not `existsSync`** *"so a dangling symlink
  also fails"* — two dead egress sinks.
- **A deleted *sentence of prompt prose* stays deleted.**
  `expect(skill).not.toMatch(/Never block \/ship on subagent failure\.\s*$/m)`, with the replacement
  asserted present: *"Silent fail-open is the failure shape that VAS-449 surfaced."*

That last has no analogue in normal software testing and is exactly what Layer B needs. **A `Playbook`
rule that was wrong and got removed will be re-suggested by the next person who hits the symptom it
appeared to solve.** Pin the removal.

---

## 4 · Fixtures that encode a decision

### 4.1 One canonical bad input per reviewer — Layer B

`test/fixtures/forcing-finding-seeds.ts`, 178 lines, four seeds, each *"pre-loaded with one obvious
finding the matching skill cannot honestly miss"*:

- **ENG** — *"We'll roll a custom UUIDv7 generator inline in each service rather than use Node's
  `crypto.randomUUID()`… we want full control over the entropy source for 'future flexibility' — no
  concrete reason yet."*
- **CEO** — Goal: *"Increase developer adoption."* Metric: *"More signups."* Premise: *"We haven't
  talked to any developers about whether the current pricing is actually a barrier. The team agreed it
  'feels like' it should be cheaper."*
- **DESIGN** — *"All headings, taglines, and body copy will be center-aligned for a 'clean modern
  look.' The hero h1 sits 8px above the subhead with no breathing room; the CTA button is the same
  visual weight as a secondary 'Learn more' link directly beside it."*
- **DEVEX** — four-step manual onboarding: clone, install bun manually, copy `.env.example` and fill
  **8 environment variables**, run migrations against local Postgres.

**Each fixture is the operational definition of what its reviewer is for.** The origin is named: the
May 2026 transcript bug where *"`/plan-eng-review` reviewed a real PR diff, wrote a multi-section
review plan to `~/.claude/plans/` and called `ExitPlanMode` **without ever firing AskUserQuestion**."*
The failure mode is silent completion — the work got done, the interaction got skipped.

**Layer B ships a `Playbook` of house rules; each needs one of these**, or "does the Playbook work" is
an opinion. Ours has rules and no seeds.

### 4.2 The shape of a question, graded — Layer A

`test/llm-judge-recommendation.test.ts` wraps every fixture in a full `AskUserQuestion` brief, and the
brief *is* the decision:

```
D1 — Where should the retrieval smarts live?
ELI10: <plain-language framing>
Stakes if we pick wrong: <both branches, one sentence>
Recommendation: Choose C because <option-specific reason>
Note: options differ in kind, not coverage — no completeness score.
Pros / cons:  A) … ✅ … ❌ …   B) … (recommended)   C) …
Net: <the tradeoff in one line>
```

Four graded properties — `present`, `commits`, `has_because`, `reason_substance` — with the production
threshold **`reason_substance >= 4`**, earned only by *"an option-specific reason that contrasts an
alternative."* A generic because-clause scores lower. **Cost published: ~$0.04/run, 4 Haiku calls + 3
deterministic fixtures.** **Touchfile-gated to `test/helpers/llm-judge.ts`** *"so it fires on rubric
tweaks but not every test run"* — the judge's own rubric has a regression test that runs when the
rubric changes. It replaced *"the original 'manually inject bad text into a captured file and revert
the SKILL template' sabotage step with deterministic negative coverage."*

### 4.3 A frozen baseline as the unit of measure, and four smaller fixtures

`test/fixtures/parity-baseline-v1.47.0.0.json` is the denominator of every ratio in §1.1, captured
*"before any Phase A work landed."* **Rebasing is an event with a reason** (v1.44.1 → v1.47.0.0
because a merge *"pushed the v1.44.1 anchor past the 5% ratchet"*) and the superseded baselines are
**retained**, not deleted. **The baseline has its own integrity test**, because it is *"the source of
every 'v1 was X bytes' claim."* **Exemptions carry per-entry reasons** — `spec` shrank because *"the
baseline measured a template bug: prose at Phase 5 mentioned `{{PREAMBLE}}` literally, so the
generator expanded the ENTIRE preamble a second time mid-sentence (~47 KB of duplication)"*; six others
because *"the baseline measured these at the silent tier-4 default (a missing `preamble-tier`
frontmatter fell through `?? 4`)."* And **`SECTIONS_EXTRACTED` is derived, not parallel**:
`new Set(CARVED_SKILLS)`, annotated *"EQ1: derived from the canonical CARVE_GUARDS registry — no
parallel list."*

- **A curated set, looped rather than copied.** `for (const word of URL_PASSWORD_PLACEHOLDER_WORDS)` —
  *"the fix replaced a shape rule with a hand-curated EXACT set, so a typo or a dropped entry
  (`CHANGEME` → `CHANGME`) would silently start blocking a legit doc placeholder with zero failure
  elsewhere. Loop the real exported set so the test can't drift from the source list."* Plus
  `size >= 8` to catch an accidental clear, and a real secret merely *containing* a placeholder word
  still blocking.
- **Six adversarial ReDoS inputs**, one per pattern family: `"a"×5000 + "!"`, `"AKIA" + "A"×5000`,
  `"eyJ" + "a"×2000 + "." + "b"×2000`, `"x@" + "a"×3000`, `"/Users/" + "a"×4000`,
  `("1"×19 + " ")×200`. Budget **< 1000 ms**, *"generous… a catastrophic pattern would blow past this."*
- **Fixtures that must not trip the repo's own guards.** Credential-shaped literals are **assembled at
  runtime** — `"hun" + "ter2"` — *"so this file's own diff never contains a credential-shaped literal
  (the prepush guard scans exact pushed bytes)."* And suicide-exit fixtures live as `.txt`, copied to
  `.test.ts` names in a temp dir at runtime, so `no-suicide-exit` does not flag them. **Two guards in
  one repo, and the conflict is resolved by fixture naming rather than by exempting one.**
- **The POLARITY table** (§2.6) is a fixture encoding thirteen security decisions and forcing a
  fourteenth to be made deliberately.

---

## 5 · What is worthless, so nobody re-reads it

**First, to their credit: not one `toMatchSnapshot` in 374 files, and no mock-asserting-itself pattern
in anything I read.** The floor is higher than most repos this size.

- **`test/jargon-list.test.ts` (61 lines) — the weakest file I found.** *"contains ~50 terms (±20
  tolerance)"* asserts `30 ≤ n ≤ 80`, a band that detects an empty file and a runaway generator and
  nothing between. `expect(typeof t).toBe('string')` on checked-in JSON is asserting TypeScript. Only
  the duplicate check could ever fire.
- **`test/model-overlay-*.test.ts` (5 files) — taste asserted as prose.** Regexes over per-model "nudge"
  strings. They pin that someone's phrasing survives regeneration; they cannot tell whether it works.
  `OTHERS-MINED` §1.7's verdict on the `plan-*-review` family applies unchanged.
- **The prose-regex template invariants are half-worth-it, and it should be said plainly.**
  `spec-template-invariants.test.ts` consolidates 13 checks as regexes over `spec/SKILL.md.tmpl`
  (`expect(TMPL).toMatch(/HARD GATE.*Do NOT produce an issue after the first message/i)`). They catch
  **deletion and drift**, which is real — §2.8's `run_in_background` bug is this class and §3.5's
  deleted-sentence pin is the technique used well. They catch nothing about whether the prose
  **works**; that needs §4.1's forcing fixtures. **76 of 374 files (20%) are this shape.** Free, worth
  keeping, never behavioural coverage.
- **`test/e2e-harness-audit.test.ts` has the bug its own repo built `skill-census.ts` to kill.** It
  enumerates from a **hardcoded `SKILL_GLOBS` array of 39 names**, so a new `interactive: true` skill
  nobody adds is invisible to the audit that exists to prove interactive skills have interactive tests.
  Compare `static-no-legacy-writes.test.ts`, which walks **everything** except an explicit `SKIP_DIRS`
  list, stated as a property: *"any skill dir, migration script, resolver, or new top-level dir gets
  covered automatically as the repo grows."* **Default-in with a skip list, never default-out with an
  include list.** The same repo does both; one is right.
- **`test/readme-throughput.test.ts` (113 lines)** — correct, thorough, and about substituting one
  number into marketing copy.
- **`test/helpers/pricing.ts`'s `return 0`** (§1.4) — not worthless; actively wrong for a spend ceiling.

---

## 6 · Verdict table

Layer key: **A** intake · **B** understanding/Playbook · **C** build plan · **D** library · **E** build
& execution · **F** design window · **G** cross-cutting · **BP** our build process.

| # | Item | Layer | Verdict | What must be true for it to work here |
|---:|---|:---:|---|---|
| 1 | Positive control paired to every absence test (§3.1) | A E G BP | **Take, as a rule** | Written into the review checklist: a `not.toContain` without a twin that proves it can fail is not a test. Costs one extra test each time. |
| 2 | Budget floor as well as ceiling (§1.1) — ×0.80 shrink floor beside the ×1.50 growth cap | D | **Take** | Layer D's catalog needs a per-entry non-empty floor and a corpus shrink floor, or "we trimmed it" is indistinguishable from "we deleted it". |
| 3 | Two-tier catalog entry: lead in the always-loaded index, `Contract` body loaded on selection (§2.5) | D | **Take** | Requires an idempotent splitter and a test that the *decision* logic lives in the lead, never behind the load. This is the mechanism that makes a 260-byte cap survivable. |
| 4 | Exit 0 is not evidence: declared lanes + executed-unit count + no failure lines (§2.1) | C E BP | **Take** | Layer E's gate must know how many units it planned to run. Without a plan count, "invisible non-execution" is undetectable. |
| 5 | Evidence ledger: FRESH/STALE/MISSING bound to a working-tree hash, TOCTOU-omitted on mid-run mutation (§2.2) | C E | **Take** | Needs a content fingerprint of the generated app, an `--expect-cmd` binding, and multi-label AND so a green lane cannot mask a red one. |
| 6 | Three-state completion DONE / NOT DONE / UNVERIFIABLE with a mechanical promotion path (§2.3) | C | **Take — theirs is better than ours** | Per-item human confirmation, blanket-confirm forbidden. Our binary acceptance criteria force a lie in the middle case. |
| 7 | Override = reason string + audited JSONL with branch and commit (§1.2) | E | **Take** | Layer E's spend ceiling. Boolean overrides get set once and never unset; a reason string in a log gets read at review. |
| 8 | Relative-ratio regression **and** absolute hard cap, both present, purposes stated (§1.3) | E BP | **Take** | With first-run grace, a noise floor, and same-branch-only comparison. Two instruments; neither substitutes. |
| 9 | Timeout derived from the plan's worst case × margin, from a live census (§1.5) | E | **Take** | Layer E's build timeout must be `f(build plan)`, not a constant. Otherwise Layer C growth silently truncates builds. |
| 10 | The inert-declaration cross-check (§2.4), with "reported, not asserted" for the unarbitrable | B C BP | **Take** | Any fact declared in a registry and enforced elsewhere needs this. Applies to the `Playbook` and to acceptance criteria. |
| 11 | Receipt-before-send + fail-open/fail-closed polarity table asserted with exact `toEqual` (§2.6) | E G | **Take** | Requires enumerating every place bytes leave, a scanner with no `KNOWN_UNWIRED` bucket, and per-exemption written reasons. |
| 12 | Refusal message shape: problem · cause · fix · what-this-is, each asserted (§2.6) | B | **Take, into the Playbook** | Four `toContain`s per refusal. Cheap, and it is the difference between a gate and a wall. |
| 13 | Never render a missing value as a good value: trusted / unverified / unknown / error (§2.7) | G E | **Take** | Every meter — spend, tokens, tests passing, components reused. A zero from a broken pipe reads as good news. |
| 14 | Session-kind classification before asking: spawned auto-chooses, headless BLOCKS, interactive falls back to prose (§2.7) | A | **Take** | Layer A's gate must not record a defaulted answer as a user-provided one when nobody was there. |
| 15 | Preference provenance allowlist, unknown source rejected, exit 2 ≠ exit 1 (§2.7) | A F | **Take** | The enforcement half of per-field provenance. Distinct exit codes so callers can tell refusal from malformation. |
| 16 | Exemptions pinned in both directions; evidence-based, never shape-based (§3, parcel-ID) | B A | **Take, as a rule** | Every exemption added to one of Layer B's 11 validation rules needs a test that the rule still fires just outside it. |
| 17 | Canonical violating fixture per house rule (§4.1) | B | **Take** | Four seeds, one per rule family, is the minimum. Without them "does the Playbook work" is an opinion. |
| 18 | Graded question brief: ELI10 · stakes · committed recommendation with an option-specific because · pros/cons · net (§4.2) | A | **Take** | Plus a cheap LLM-judge anchored on hand-graded fixtures, gated to fire when the rubric changes. |
| 19 | Split, don't drop, when a UI cap meets a real decision (below) | A F | **Take** | Floor **and** ceiling on the behavioural count, because floor catches dropping and ceiling catches question-spam. |
| 20 | Explicit setting over prohibition in prompt prose; absolute host-resolved paths (§2.8) | B | **Take, into the Playbook** | Both failure modes are silent: an inverted prohibition, and a path that makes the model fabricate (21/21 observed). |
| 21 | One enumerator for "how many components are there", returning three deliberately-different counts (§2.9) | D | **Take** | Files on disk ≠ distinct components ≠ catalog-addressable `Contract`s. One module, monotonicity asserted. |
| 22 | Secret-sink harness: 4 channels × 4 match rules, per-run `$HOME` walked post-mortem (§3.1) | A E G | **Adapt** | Take the match rules (exact, URL-decoded, 12-char prefix ≥16, base64 ≥12) and the published blind spots. Our channels differ: sandbox FS, relay, preview, logs. |
| 23 | Laplace smoothing + 5%/week decay applied at read + FIFO 50 + drift warning (§2.10) | F | **Adapt** | Only if Layer F remembers taste across builds. The decay-at-read choice removes the need for a background job. |
| 24 | Three-layer privacy-promise enforcement: coverage · behaviour-of-the-actual-filter · floor (§3.4) | G | **Take** | For every sentence we put in front of a user about what does not leave their machine. |
| 25 | Pin the deletion — of a file, a binary (`lstat`), and a sentence of prompt prose (§3.5) | B D | **Take** | The removed `Playbook` rule will be re-suggested by whoever next hits the symptom it seemed to fix. |
| 26 | Trust store for commands declared in repo files (§2.7) | E | **Take** | Per-repo, per-command, recorded by a human. `absence never blocks`. Layer E runs builds shaped by generated repos. |
| 27 | ReDoS: static nested-quantifier lint + runtime budget + **oversize fails closed before the patterns run** (§4.4) | A | **Take** | The size cap before the scanner is the real backstop. And a malformed cap value must fall back to the default, never disable the guard (`NaN`, `≤0`). |
| 28 | Hermetic child env: no `...process.env` spread into a build child (§2.9) | E | **Take** | A sandbox that inherits the host env produces a build that works on one machine. *"Three burned suites last time."* |
| 29 | Prose-regex invariants over prompt templates (§5) | B | **Adapt, narrowly** | Free, catches deletion and drift. Never count them as behavioural coverage. 20% of their suite is this. |
| 30 | Hardcoded enumeration lists in guards (§5, `SKILL_GLOBS`) | — | **Leave** | Default-in with a skip list. Their own repo shows both patterns; copy the other one. |
| 31 | `estimateCost` returning 0 for an unpriced model (§1.4) | E | **Leave — invert it** | An unpriced model must be a refusal or a pessimistic bound. As written it disables the hard cap in exactly the case the cap exists for. |
| 32 | `jargon-list`, `model-overlay-*`, `readme-throughput` (§5) | — | **Leave** | Read so nobody has to again. |

**Row 19, at length, because the transcript is the argument.**
`test/skill-e2e-plan-ceo-split-overflow.test.ts` quotes a real agent transcript verbatim:

> *"I'm hitting Conductor's limit of 4 options in the AUQ, so I need to cut one. E4 is the largest
> lift and probably beyond scope… Trimming: E4. **Moving to TODOs without asking.** Re-firing with
> 4."*

A **UI cap silently became a product decision.** The model reasoned from an interface constraint to
dropping one of the user's five real options, and recorded it as a TODO without asking. The fix is a
split-don't-drop rule tested with N=5 seeded options, a floor of **N−1 = 4** review-phase questions
and a ceiling of **N+3**; tier `periodic`, *"~25 min, ~$0.30–$5.00/run"*, with `QUESTION_TUNING:
'false'` so the test measures the skill and not accumulated preferences.

**Layer A converts a conversation into a structured spec through a question UI. Every cap in that UI
— options per question, questions per turn, characters per label — is a cap on the spec unless
something forbids the model from resolving the constraint by discarding user intent.** That is a
Playbook refusal we do not have, and a floor-and-ceiling behavioural test we would not have thought
to write.
