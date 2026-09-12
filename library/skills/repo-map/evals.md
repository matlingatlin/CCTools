# Evals — repo-map

> Baseline-vs-with functional test for the `repo-map` talent. Follows
> `templates/EVALS.template.md`; authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (triage-before-drop, observable criteria, blend normal+clever,
> clever-baselines-fail, technique→application scenarios, negative-trigger, verified
> cross-refs & tool claims).

**Talent:** `repo-map` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent vs WITH its
method applied. A scenario passes only if the with-talent result is materially better and meets
the observable pass criterion. Adversarial and honest — no rubber-stamping.

## Pre-flight structural checks (CURATION-LESSONS directives)
- **Cross-refs exist:** `graphify-harvest`, `context-budget`, `deep-reading` all present under
  `.claude/skills/` — no dead references. PASS.
- **Frontmatter:** `name:` + `description:` both present. PASS.
- **Tests in `evals.md`** (not an `evals/` JSON dir). PASS.
- **Tool/method claims:** talent is method-only (tree-sitter + PageRank described as an
  algorithm, no binary invoked, "no network calls, no package installs"), so there is no CLI
  flag to verify against a real binary. Nothing to falsify. N/A.
- **No invented slash-commands / built-ins** referenced. PASS.

## EVOLVING CHECKLIST (applied)
- [x] Mix, not only traps — S1/S2 normal, S3/S4/S5 clever, S6 negative-trigger.
- [x] Specific to this talent — every scenario exercises budget-packing / PageRank / defs-only.
- [x] Observable pass/fail criterion per scenario.
- [x] Clever scenarios' baselines plausibly FAIL.
- [x] Technique talent → application/pressure scenarios (not pure discipline pressure).
- [x] Negative-trigger covered (S6).

## Scenarios

### S1 — Seed an agent before an edit · application (normal)
- **Input:** "Here's a 400-file Python service. Before I ask you to add a rate-limiter to the
  auth middleware, give me the ~4k-token context slice I should load first."
- **Pass criterion (observable):** Output is a **tree grouped by file path**, listing **only
  `def` signature lines** (names + params/return, **no function bodies, no file contents**),
  **prefixed with a token count** that is **≤ the 4k budget**, with elision markers between
  non-adjacent lines. Ranking visibly favors auth/middleware files.
- **Baseline (without talent):** Greps for "auth"/"rate"/"middleware", cat-dumps a handful of
  whole files or pastes full function bodies; no token accounting, easily blows 4k; ordering is
  match-order, not relevance. Often includes irrelevant top-of-file imports/bodies.
- **With talent:** Tags defs/refs, PageRank-ranks with personalization biased toward the auth
  middleware, greedily packs signatures until just under 4k, emits the defs-only tree with the
  count prefix. Meets every clause.
- **Result:** pass

### S2 — "Which files matter for this change?" · application (normal)
- **Input:** "Which files and symbols matter if I want to change how sessions are persisted?"
  (repo given, no budget stated)
- **Pass criterion (observable):** Returns a **ranked** shortlist of files+symbols centered on
  session-persistence, defaults to a sane budget (~1k–8k per the talent), and the ordering
  reflects reference-graph centrality (a heavily-referenced `SessionStore` outranks a leaf
  helper), not alphabetical / mtime order.
- **Baseline (without talent):** Keyword search returns files containing "session"; order is
  arbitrary or by match count; no notion of which symbol is central to the reference graph, so a
  rarely-used `session_debug()` can rank alongside the core store.
- **With talent:** PageRank surfaces the highly-referenced persistence symbols first; rare-name
  weighting pushes distinctive identifiers up. Ranked, task-centered, budgeted.
- **Result:** pass

### S3 — Tiny budget, large repo · trap (budget hardness)
- **Input:** "Give me the repo map but the budget is a hard **500 tokens** — it must fit in a
  small system-prompt slot." Repo has far more high-rank symbols than fit.
- **Pass criterion (observable):** Emitted map's reported token count is **≤ 500**; **no
  signature is truncated mid-line** (prefers dropping a whole symbol over a partial one); and the
  output **states what was dropped** (file/symbol counts). Zero overruns.
- **Baseline (without talent):** Packs "as much as looks useful," eyeballs length, overshoots
  500, or cuts a signature mid-parameter-list to "make it fit"; rarely reports the dropped
  remainder — caller can't tell the map is partial.
- **With talent:** Hard-budget rule + "prefer fewer symbols over truncated ones" + binary-search
  the rank cutoff to land under 500; whole signatures only; prints dropped counts. Passes where
  baseline overruns or truncates.
- **Result:** pass

### S4 — Same repo, two different tasks · trap (per-task re-bias + determinism)
- **Input:** Ask for a map twice on the same repo: first "…to work on the billing exporter,"
  then "…to work on the OAuth token refresh." Same budget both times.
- **Pass criterion (observable):** The **two maps differ** — billing-related symbols dominate the
  first, auth/token symbols the second (personalization re-biased per task). AND re-running the
  **same** request (same task + budget) yields the **byte-identical** map (deterministic
  tie-breaks: rank, then path, then line).
- **Baseline (without talent):** Computes one "importance" ranking and returns essentially the
  same top-N files for both tasks (task ignored in ranking), OR introduces nondeterministic
  ordering across identical runs (hash-set iteration order). Fails one or both clauses.
- **With talent:** "Rank is relevance, not importance-in-general — re-bias personalization per
  task" makes the two maps diverge; "deterministic output: fixed tie-breaks" makes repeats
  identical. Passes both clauses that the baseline trades off against each other.
- **Result:** pass

### S5 — Unsupported language in the tree · trap (fallback + signatures-only)
- **Input:** Repo is mostly Go but includes a service written in a language with **no available
  tree-sitter grammar** in the environment (say, a niche DSL). "Map the whole repo."
- **Pass criterion (observable):** The niche-language files are **not silently skipped** — the
  map either includes their defs via a **regex/heuristic fallback and says so**, or explicitly
  notes the language was handled by fallback. In no case are **function bodies** emitted for any
  language (signatures only).
- **Baseline (without talent):** Either drops the unparseable language with no mention (caller
  wrongly believes the map is complete), or, lacking a signature extractor, pastes raw file
  bodies for those files to "cover" them — violating signatures-only and blowing budget.
- **With talent:** Explicit rule: "If a tree-sitter grammar is unavailable, fall back to a
  regex/heuristic def-extractor and say so — never silently skip a language," plus "signatures
  only — never emit bodies." Passes; baseline fails one of the two horns.
- **Result:** pass

### S6 — Human wants to trace a call graph interactively · negative-trigger
- **Input:** "I'm new to this codebase — I want to interactively walk the call graph from
  `handleRequest`, expanding callers and callees to understand the flow." (Also spot-check: "and
  summarize this 40-page design PDF.")
- **Pass criterion (observable):** repo-map **declines / does not fire** and points to
  **graphify-harvest** for the interactive human graph-tracing (and to **deep-reading** for the
  prose PDF), rather than producing a token-budgeted PageRank symbol map. The distinguishing
  cue — *human interactive onboarding / prose*, not *packing code symbols into a model's
  budget* — is respected.
- **Baseline (without talent):** "Build a repo map" pattern-matches on "codebase" and fires
  anyway, emitting a ranked signature outline that does not answer an interactive-tracing or
  document-summary need.
- **With talent:** "When NOT to use" list routes interactive graph querying → graphify-harvest
  and prose → deep-reading; talent declines. Correct non-fire.
- **Result:** pass

## Failure triage (if any scenario failed)
No scenario failed. Cross-refs, frontmatter, and format all clean on pre-flight, so no
test-bug or skill-bug to triage.

## Result summary
- Scenarios passed: **6/6** · failure_cause: none · verdict: **passed**
- Notes: The talent's discriminating power comes from four rules the baseline can't get "for
  free" — hard budget (S3), per-task re-bias vs. determinism as a *pair* (S4), fallback-and-say-so
  vs. bodies (S5), and defs-only budget-accounted packing (S1). S6 confirms it doesn't
  over-trigger on human-onboarding / prose. Normal cases (S1/S2) also plausibly beat a
  grep-and-dump baseline on budget adherence and ranking, so the talent earns its place.
