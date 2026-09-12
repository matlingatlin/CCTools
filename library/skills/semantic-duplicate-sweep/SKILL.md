---
name: semantic-duplicate-sweep
description: "Use when a codebase has grown functions that do the SAME JOB under different names and different implementations — formatCurrency, toMoneyString, priceLabel, renderAmount — typically after weeks of agent-written or many-authored PRs that were each small and locally correct, so review never saw the overlap. Triggers on 'clean up the utils', 'is this already implemented somewhere', 'why are there four of these', duplicated helpers, look-alike helpers whose rounding/validation/error behavior has quietly diverged, a bug fixed in one copy but not its twins, or a pre-refactor audit. Grep and clone detectors miss these: the names share no tokens and the bodies differ. NOT ranking or budget-packing files for LLM context (use repo-map), NOT building a structural code graph to navigate (use graphify-harvest), NOT searching for an existing SKILL before authoring one (use skill-scout)."
---

# Semantic Duplicate Sweep

Find functions that serve the same **intent** under different names and different code, then
consolidate onto one survivor with every call site redirected — without silently changing
behavior at any of them. Language-neutral.

## When to use
- Weeks of small PRs (human or agent) have piled up helpers nobody compared to each other.
- You suspect a helper already exists but cannot find it, because you do not know its name.
- Two look-alike helpers disagree on an edge case — rounding, negatives, nulls, empty input.
- A bug was fixed in one place and the same bug is still live in its unnamed twins.
- Before a refactor or an API change, to know how many copies of the rule you must edit.

**When NOT to use:** selecting the highest-signal files/symbols to fit an LLM context budget
(`repo-map`); building a navigable structural graph of a repo (`graphify-harvest`); checking
whether a SKILL already exists before authoring (`skill-scout`); genuine copy-paste blocks with
shared text — an ordinary clone detector is cheaper and finds those; a codebase small enough
that one person can read every function in a sitting (just read it — see Scaling).

## Why the usual tools miss this
| Tool | What it matches | Why it fails here |
|---|---|---|
| grep / symbol search | shared tokens in names | `formatCurrency` and `renderAmount` share none. You cannot grep for a word you do not know. |
| textual clone detection (type-1/2) | identical or renamed text | Independently written implementations share no text. |
| AST / structural comparison (type-3) | similar trees | Three different rounding strategies produce three different trees. Structural distance is large; intent distance is zero. |
| type signatures | same types | `(number) => string` matches hundreds of unrelated functions, and misses the twin taking `{amount, currency}`. |

The signal is **contract plus caller purpose**, not text, tree, or type. Everything below is
built on that.

## Steps

1. **Extract a function catalog — deterministically, no model calls.** Every function/method
   in scope with: name, file, line, arity, parameter and return types if the language has
   them, docstring/comment first line, LOC. Use the language's own tooling (ctags, tree-sitter,
   `go doc`, `inspect`, an LSP symbol dump) or a regex over definition lines. This step is
   cheap and must stay cheap — it runs over the whole repo.

2. **Bucket by DOMAIN, not by name.** Group the catalog by what the code is *about*: money
   formatting, date arithmetic, path handling, HTTP retry, string casing, validation. Use
   directory, module, imports, and the vocabulary in names and doc lines. **Only functions in
   the same bucket are ever compared** — this is what keeps the sweep from being quadratic
   over the whole repo. **A bucket of one is dropped. A bucket of TWO is kept and compared** — a pair is the
   commonest real case (the bug fixed in one copy and not its twin), and dropping pairs would
   discard the exact situation this method advertises. What a pair does NOT get is the automatic
   benefit of the doubt: with no third sibling there is no pattern to argue from, so a pair needs
   the step-3 tests to come back clean on their own merits, and a pair at `low` confidence goes
   to a human rather than into a consolidation. Split any bucket over ~40 functions
   further (by sub-domain or directory) before comparing.

   **Prove the extraction found things before trusting that it found everything.** A regex or
   parser over definition lines misses whole shapes silently — arrow consts, methods, decorated
   or generated definitions, re-exports — and a bucket emptied by a missed shape produces a report
   byte-identical to a genuinely clean one. Before comparing anything: pick two or three functions
   you KNOW exist in the target area, and confirm the extraction returned them. If it did not, fix
   the extraction; a sweep that reports "no duplicates" after searching the wrong shape is the
   worst output this method can produce, because it closes the question.

3. **Decide intent-equivalence by CONTRACT and CALL SITES, never by the body.** For each
   candidate, written *before* looking at the others:
   - **Contract triple.** IN: accepted input domain, including which inputs it rejects.
     OUT: type and shape of the result. EFFECTS: mutation, I/O, logging, throws, allocation.
   - **Caller purpose.** For 2–3 real call sites, write the one-line job the caller wanted,
     from the surrounding code and the name it assigns the result to — "show a price in the
     cart UI" vs "serialize an amount into an API payload". These are different intents even
     when both return a string.
   Then apply, in order:
   - **Substitution test.** At each call site of A, could B be called instead — allowing a
     trivial adapter, disallowing a rewrite — and still serve that caller's purpose?
   - **Co-change test (the decisive one).** Name a plausible requirement change in the domain
     ("crypto amounts now show 8 decimals"). Would **both** have to change? Both → same intent.
     Only one → different intents; they answer to different rules and different owners.
   - **Falsify before you conclude.** Hunt for one call site where B genuinely cannot stand in
     *for a reason* — a different input domain, a different effect class, a different owner.
     A mere difference in output value is **not** a difference of intent; it is divergence, and
     divergence is step 4's job, not an excuse to declare them unrelated.
   Record each group with a confidence: **high** (contracts match, co-change yes, substitution
   clean), **medium** (one adapter needed or one call site unclear), **low** (a hunch). Low
   confidence never proceeds to consolidation without a human saying so.

4. **Map the divergences BEFORE choosing a survivor.** Do not read the sources and reason about
   what they probably do — **run them** on a shared probe set and record observed outputs in a
   matrix (probe inputs × functions). Probes must include the ugly inputs: zero, negatives,
   nulls/undefined, empty, very large, non-finite, boundary rounding (`.005`, `.015`),
   locale/precision variants, and the wrong-typed input each one is passed anywhere in the repo.
   Classify **every** difference as exactly one of:
   - **BUG** — violates the contract or the domain rule (a formatter that prints `-$1.00` as
     `$-1.00`). Fix it **in its own change, with its own test, before any consolidation.**
   - **INTENTIONAL** — a caller genuinely needs it; name that caller. Intentional variation is
     not merged away: it becomes an explicit parameter, or those functions stay separate.
   - **UNSPECIFIED** — nobody ever decided. This is NOT the soft option: whichever way you
     decide, some call site's observable behavior changes, which is the same outcome as shipping
     an unfixed BUG. So it carries the same requirement — **its own change, its own test, landed
     before any consolidation** — and the decision is written down. If you cannot get the decision
     made, the group does not consolidate; it waits. Decide now, write the decision down, and treat the
     chosen behavior as new contract; anything that changes for a caller is a behavior change.
   **Only then** pick the survivor — the one whose contract is widest and whose behavior is
   correct after the bug fixes, not the one with the most call sites or the nicest name.
   Two independent INTENTIONAL variations that do not co-vary mean this was never one
   function; a survivor carrying a boolean flag per variation is a merge that should not happen.
   *A consolidation that quietly changes rounding on negative amounts is worse than the
   duplicates were: the duplicates were visible, the change is not.*

5. **Prove the survivor before deleting anything.** The survivor must pass the **union** of
   tests: every existing test of every function in the group, **retargeted at the survivor**
   (retarget them — never delete a function's tests along with the function, which is how
   coverage silently drops); plus one case per row of the step-4 matrix; plus the cases each
   call site depends on, **including behavior only the doomed function ever covered**. If a
   retargeted test fails, that is an unfixed bug or an intentional divergence you merged away
   — go back to step 4. Never loosen, skip, or re-record the test to get green (that is
   `oracle-weakening-audit`'s failure mode).

6. **Redirect, verify, then delete — in that order, one group per commit.** Point every call
   site at the survivor; run the full suite; search the whole repo for remaining references
   including strings, dynamic dispatch, re-exports, config, and docs; then delete. The
   consolidation commit should be observably a no-op at every call site — the bug fixes
   already landed separately in step 4.

7. **Report and gate.** Emit one table: group, member functions, evidence for equivalence,
   confidence, divergences with their classification, proposed survivor, call-site count (blast
   radius). **A human approves each group before deletion.** Consolidation is hard to reverse
   and the cost of a wrong merge lands months later, at a call site nobody was looking at.

## Scaling
The bucket boundary in step 2 is the whole scaling story: comparisons are within-bucket, so
cost grows with the largest bucket, not the repo. On thousands of functions, bucket first by
directory/module, then by domain, cap buckets at a few dozen, and process the highest-yield
buckets first — `utils/`, `helpers/`, `common/`, and any directory with many authors and many
short functions. Cheap prefilters inside a bucket (arity, return kind, shared vocabulary in
names/doc lines) cut the pair count further before any careful comparison.

**This is overkill when:** the codebase is small enough to read in one sitting; the suspected
duplicates are one-line wrappers where consolidation buys nothing; or the code is about to be
deleted or rewritten anyway. Read it and move on.

## Example
**Before:** Six weeks of agent-written PRs leave `formatCurrency`, `toMoneyString`,
`priceLabel`, `renderAmount`. No shared tokens, four different bodies; every PR was small and
locally correct, so review never saw them together. "Clean up the utils" consolidates none of
them, because nothing links the names.

**After:** The money bucket has 4 members (≥3, so it is swept). Contracts all read
"amount → human-readable currency string, no effects"; the co-change test on "crypto shows 8
decimals" says all four would change. The probe matrix shows **three** rounding behaviors
(half-up, half-even, truncate) and one wrong sign placement on negatives. The negative-amount
bug ships first as its own fix with its own test. Half-even is chosen and recorded as the
contract; truncate turns out to be intentional for one CSV export caller, which keeps its own
function. `formatCurrency` becomes the survivor, passes the retargeted union suite, the other
two call sites are redirected, and the deletions land in a commit that changes no output.

## Rules
- Equivalence is judged on contract and caller purpose. Body similarity is neither necessary
  nor sufficient — never conclude from a diff.
- Map divergences before choosing a survivor. Choosing first turns the map into a justification.
- Bugs are fixed in a separate change from the consolidation. Always.
- Never delete a function until the survivor is green on the union of all their tests.
- Intentional variation is preserved, not averaged away.
- A human approves each group before any step that changes what production runs — **redirecting
  call sites counts, not only deleting**. Redirect-now-delete-later satisfies a deletion-worded
  gate while performing the change the gate exists to review; the gate is on the OUTCOME (a call
  site starts running different code), never on the verb.
- Method only: no vendored scripts, no auto-run hooks, no installs. Model-assisted judgement is
  optional and belongs only inside step 3 for a single bucket at a time — extraction and
  bucketing stay deterministic and free, so a per-bucket fan-out is a spend you opt into, not a
  default. Fanning subagents across every category by reflex costs real money for buckets that
  a prefilter would have emptied.

## In this repo (one instance) — and why it is currently the WRONG instance

Honest answer first: **this repo does not need this method today.** `pipeline/` holds 8 functions
across 4 files. That is small enough to read in one pass, which is this skill's own overkill
branch, and it is the illustration worth keeping — an audit method that cannot say "not here"
is a method that manufactures work.

What would change that: the talent library is 80+ units and growing, and if `pipeline/` grows into
per-wave scripts with their own formatting, path and ledger helpers, the twins will appear there
first — written in different waves, by different agents, with no shared vocabulary in their names,
which is exactly the shape grep and clone detection miss. Bucket by pipeline stage (metrics,
ledger writes, frontmatter checks, report rendering) when that happens.

Two repo-specific bindings when it does apply: the human gate is the standing "anything
irreversible asks the user first" rule and it fires on the REDIRECT, not just the delete; and the
survivor decision, its contract, and the classified divergences go in an ADR plus a `CHANGELOG`
entry, with the bug fixes committed ahead of the consolidation.

Duplication among *skills* is a different job — `skill-stocktake` for the library,
`skill-scout` before authoring.
