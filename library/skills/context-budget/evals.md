# Evals — context-budget

> Follows `templates/EVALS.template.md`. Authored against the ACTIVE DIRECTIVES in
> `pipeline/CURATION-LESSONS.md` (blend normal + clever, observable criteria, design clever
> baselines to fail, match scenario type, cover a negative trigger).

**Talent:** `context-budget` · **Type:** technique (audit method, with a discipline edge on
what to protect) · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (baseline
Claude eyeballing the setup) vs WITH its inventory → classify → detect → rank method applied.
A scenario passes only if the with-talent result is materially better and meets the stated
observable criterion. Adversarial, not a rubber stamp. The talent's sharpest,
most-differentiated moves are: (a) ranking cuts by **actual token weight** (MCP tool schemas
≈ 500 tok/tool) rather than by visible **count**; (b) not double-counting duplicated skill
copies; (c) pricing the **always-loaded** cost of agent-description frontmatter; and (d)
**protecting** components that are actually needed instead of cutting the biggest thing.

---

## S1 — Basic audit, produce ranked report · application (core, normal)
- **Input:** "My context fills up fast lately. Here's my setup: 16 agents, 28 skills, 14 MCP
  servers (~87 tools total), 2 CLAUDE.md files. What's eating my context and what should I
  cut first?"
- **Pass criterion (observable):** Produces a per-bucket token breakdown (agents/skills/
  rules/MCP/CLAUDE.md) with numbers, and a **ranked** top-N cut list ordered by estimated
  token savings — with MCP tool schemas identified as the largest bucket (≈87 × ~500 ≈ 43K).
- **Baseline (without talent):** Plausibly gives generic advice ("remove skills you don't
  use, trim CLAUDE.md") with no quantification and no ranking, and may not realize MCP tools
  dominate. Unranked, unquantified.
- **With talent:** Phase 1 inventories each bucket with `words×1.3` / ~500-per-tool; Phase 4
  ranks cuts by savings, top-3 first. MCP surfaces as the biggest lever.
- **Result:** pass — quantified + ranked beats hand-waving; the everyday job done well.

## S2 — Pre-expansion headroom check · application (normal)
- **Input:** "I want to add 5 more MCP servers (~50 tools). Do I have room, or will it hurt?"
- **Pass criterion (observable):** Estimates the delta (~50 × ~500 ≈ 25K tokens), expresses
  it as a change in % of window used (before → after), and gives a go / trim-first
  recommendation tied to that number — not a bare yes/no.
- **Baseline (without talent):** "Probably fine" or "might slow things down" with no figure.
- **With talent:** Computes current overhead, adds the projected ~25K, reports the new %,
  and if it crosses a threshold recommends removing CLI-replaceable servers first.
- **Result:** pass — a checkable number and a conditional recommendation vs a guess.

## S3 — Blame the wrong lever · trap (clever, baseline fails)
- **Input:** "I have 40 skills — that's got to be why my context is full. Help me cut skills."
  (Hidden fact in the setup: those 40 skills are ~5K tokens total; one MCP server exposes 60
  tools ≈ 30K tokens.)
- **Pass criterion (observable):** Ranks by **token weight**, not item count — identifies the
  60-tool MCP server (~30K) as the dominant cost and recommends it FIRST, explicitly noting
  that the 40 skills are cheap by comparison. Recommending a skill purge as the primary fix =
  fail.
- **Baseline (without talent):** Follows the user's framing — 40 is a big, visible number —
  and starts pruning skills, chasing ~5K while ignoring the ~30K driver. High count ≠ high cost.
- **With talent:** Phase 1's per-tool ~500-token estimate makes the 60-tool server outweigh
  all 40 skills combined; the Best-Practices "MCP is the biggest lever" rule and the ranked
  Phase-4 output put the server at the top. Corrects the user's wrong premise with numbers.
- **Result:** pass — resisting the count-based framing is the talent's signature move.

## S4 — Duplicated skill copies · trap / edge (clever, baseline fails)
- **Input:** "Audit my context. Note: my skills exist both in `skills/` and are copied
  verbatim into `.agents/skills/` for the subagents."
- **Pass criterion (observable):** Counts each identical skill **once** for the loaded budget
  (dedupes the `.agents/skills/` copies) rather than reporting 2× the skill token total; may
  note the copies as a separate maintenance concern but must not inflate the live budget.
- **Baseline (without talent):** Globs all `*/SKILL.md`, sums everything, and double-counts —
  reporting a skills bucket roughly twice its true loaded size, which then mis-ranks the cuts.
- **With talent:** Phase 1 explicitly says "skip identical copies in `.agents/skills/` to
  avoid double-counting." Dedupe yields the true figure.
- **Result:** pass — the de-dup rule is a specific, easily-missed correctness point.

## S5 — Protect the needed component under cut pressure · pressure (clever, baseline fails)
- **Input:** "Just tell me the single biggest thing to delete to free the most context." (In
  the setup the heaviest single file is a 220-line planner agent that is referenced by name in
  CLAUDE.md and backs the active `/plan` command; the next heaviest removable items are three
  rarely-matched, unreferenced language-rule files.)
- **Pass criterion (observable):** Does NOT recommend deleting the CLAUDE.md-referenced,
  command-backing planner just because it's the largest; classifies it "Always needed / keep"
  and instead ranks the removable (unreferenced, overlapping, no project match) items as the
  cuts — or proposes lazy-loading the heavy-but-needed one rather than deleting it. Naming the
  planner as "the single biggest thing to delete" = fail.
- **Baseline (without talent):** Takes "biggest to delete" literally, sorts by size, and
  names the planner — breaking an active command to chase a number.
- **With talent:** Phase 2's bucket table gates on "referenced in CLAUDE.md / backs an active
  command" → Always needed → Keep; savings are ranked only among Sometimes/Rarely-needed
  items. Size alone never authorizes a cut.
- **Result:** pass — separating "heaviest" from "removable" is the discipline edge; baseline
  conflates them under the user's pressure.

## S6 — Cheap-looking agents, expensive frontmatter · edge (clever)
- **Input:** "My 20 agents are all short (30–50 lines each), so agents can't be my problem,
  right? Skip them." (Each agent carries a ~45-word `description`.)
- **Pass criterion (observable):** Flags the **always-loaded** cost of the agent-description
  frontmatter — every agent's `description` is present in every Task-tool invocation
  regardless of body length — and recommends trimming the 20 bloated descriptions even though
  the bodies are small. Accepting "bodies are short, skip agents" = fail.
- **Baseline (without talent):** Agrees the agents are small and moves on, missing that 20
  always-on 45-word descriptions are a real, recurring per-spawn tax.
- **With talent:** Phase 3 "Bloated agent descriptions" and the Best-Practices "descriptions
  are loaded always" catch exactly this; it prices the frontmatter separately from the body.
- **Result:** pass — the load-model (always-on vs on-demand) is knowledge baseline lacks.

## S7 — Look-alike, wrong talent · negative-trigger
- **Input:** "Audit my skills for quality — find the low-value, duplicated, or poorly-written
  ones and tell me which to rewrite." (Or: "Which model tier should this batch job run on to
  save money?")
- **Pass criterion (observable):** context-budget should DECLINE / hand off — the first is a
  **quality** audit (skill-stocktake), the second is **runtime dollar / tier** routing
  (cost-aware-model-routing). A pass names the right talent and does not launch a token-weight
  context inventory. Producing a context-budget report here = over-trigger = fail.
- **Baseline (without talent):** N/A (no talent to mis-fire) — this scenario checks the
  talent's own boundary, which the sharpened description now states explicitly.
- **With talent:** Description's "NOT quality-auditing skills… NOT runtime dollar spend or
  model-tier choice" boundary redirects to skill-stocktake / cost-aware-model-routing.
- **Result:** pass — declines cleanly; not over-scoped.

## Failure triage (if any scenario failed)
No scenario failed. failure_cause = none. (S3–S6 are designed so the baseline plausibly
fails and the talent's specific rules — token-weight ranking, de-dup, keep-if-referenced,
always-loaded frontmatter — are what flip the result; each has an outsider-checkable
criterion, not a subjective one.)

## Result summary
- Scenarios passed: 7/7 · failure_cause: none · verdict: passed
- Blend: S1–S2 normal/representative, S3–S6 clever/adversarial (trap/edge/pressure), S7
  negative-trigger. The clever four each corner a distinct signature behavior of the talent.
