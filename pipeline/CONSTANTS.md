# CONSTANTS — pinned values the loops READ and never WRITE

**Nothing auto-writes this file.** `signals.py --write` rewrites BRAIN §0; `wave-reflect`
rewrites LESSONS' derived sections; both loops rewrite STATUS and the ledgers. None of them
touch this file, by design. A value here changes only by a human decision recorded as an ADR or
a resolved proposal, and the change carries a new date and a new source line.

Why this file exists: today a scheduled prompt carried an instruction the measurement had already
refuted, two of our own documents disagreed on a cap, and three talents shipped unloadable because
an automated edit rewrote a line nobody re-checked. The pattern is the same each time — a value
that matters got restated in a second place and the two drifted. This is the one place, and every
other place should point here rather than repeat the number.

Every constant carries **how we know it**. `measured` beats `cited` beats `decided`; a `decided`
value is a judgement we are free to revisit, a `measured` one needs new measurement to move.

---

## Description length

**Two real limits, governing different things.** They were treated as competing claims about one
number for a full session; they are not, and the confusion cost a wrong resolution before our own
knowledge base settled it.

| Constant | Value | How we know it |
|---|---|---|
| `DESCRIPTION_SPEC_CAP` | **1024** | `cited` — the field limit in the **agentskills.io open standard**, which is what a portable skill must satisfy. Cited in `writing-skills`. **Re-verified 2026-08-28 against the primary source** (`agentskills.io/specification`): "Must be 1-1024 characters". The spec's full frontmatter surface is `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` — nothing else. |
| `DESCRIPTION_LISTING_TRUNCATION` | **1536** | `cited` — where **Claude Code truncates `description` + `when_to_use` COMBINED** in the listing shown to the model. From `knowledge/notes/skill-anatomy.md` (`status: verified`, sourced to `code.claude.com/docs/en/skills`, fetched 2026-08-27). This is a host behaviour, not an authoring allowance — and it is a SHARED budget, so a long description eats the `when_to_use` room. |
| `DESCRIPTION_HEADROOM_TARGET` | **1230** | `measured` 2026-09-08 — the length above which a description has no room left for one more NOT-clause. `DESCRIPTION_LISTING_TRUNCATION` (1536) minus **306**, the p75 of the **69** NOT-clauses this library actually writes across 62 of 92 descriptions (min 41, median 189, mean 219, p90 405, max 537). Rule fixed before any candidate was read: `pipeline/decisions/2026-09-08-description-headroom.md`. **FROZEN on purpose.** The gate first recomputed p75 live and the number moved from 1230 to 1231 *during a test that lengthened a description* — a threshold derived from the population it judges can be raised by the very edit it should refuse. `desc_headroom.py --gate` reads this cell; the report still prints today's p75 beside it, so drift is visible without being automatic. Re-deriving it is a new measurement, not a side effect. |
| `DESCRIPTION_CAP_CHARS` | **1024** | **`sourced` 2026-09-12** — upgraded from `decided`. The Agent Skills spec states it as a hard limit, verbatim: *"The required `description` field: Must be **1-1024 characters**"* (`knowledge/raw/baseline-2026-09-04/agentskills.io_specification.html`, held since 2026-09-04 — the answer sat in the raw layer for eight days while two notes recorded the question as unresolvable). So this was never only a house style: it is the spec's maximum, it is the stricter of the two limits, and it is the only one that travels. **13 units currently exceed it**, 1,037 to 1,446 characters; `desc_headroom --gate` sees only 5 of those, because its frozen target of 1,230 answers the host's silent 1,536 truncation wall instead. Both numbers are real and they are different constraints. Trimming changes routing, which this library's own rule says must be proven against a baseline, so the 13 are a standing item for the human. |
| `DESCRIPTION_TARGET_CHARS` | **~350** | `measured` 2026-08-28 — 44 shipped Anthropic skills on this machine (`/mnt/skills`, `~/.claude/skills`): median 308, max 982, none above 1024. Consistent with authoring to the spec limit. Our own median is 709, roughly double. |
| `WHEN_TO_USE_IS_PORTABLE` | **no** | `cited` 2026-08-28 — **`when_to_use` is NOT a field in the agentskills.io spec** (see the full field list above); it is a Claude-Code extension. So it cannot hold routing-critical text in a library that means to travel. This closes the obvious escape hatch for the description-headroom problem: moving NOT-clauses into `when_to_use` would weld the library to one host, which is the exact trade `DESCRIPTION_CAP_CHARS` refused. **0 of 85 talents use the field** — corrected 2026-08-28; an earlier note here said 2 of 82, which came from grepping the string rather than parsing frontmatter and matched graphviz labels and prose. So the 1536 budget is not being under-used through neglect of a field we rely on: we do not use that field at all, and should not. |

**Correction on the record.** An earlier version of this file said the measurement "corroborates
1024 and refutes 1536". That was wrong. The measurement is consistent with authoring to 1024, but
it cannot refute 1536, because 1536 is a truncation point for a different (larger, shared)
quantity. The error came from calling 1536 "uncited" when its citation was sitting in our own
`knowledge/` store, verified and dated — I measured the outside world and never searched inside.
That is the wrong-scope family, which is the most common defect in this library, committed by the
coordinator while writing the file meant to prevent exactly this.

**Known violation, open — for the CURRENT count run `python3 pipeline/queries/preflight.py`, never
this line.** Some descriptions exceed 1024. They are spec-non-compliant; none is truncated by
Claude Code today, which is why nothing visibly broke. Trimming changes routing, so each is an
edit with a trigger check, never a mechanical truncation.

**How much room is actually left — MEASURED 2026-09-08.** "None is truncated today" is true and
was hiding how close it is. `when_to_use` is used by **0 of 92** units, so the whole 1,536 belongs
to `description`, and the largest is **1,446 — 90 characters of headroom**; three are within 100.
The failure mode is specific: truncation takes the **tail**, and this library's house style puts
the NOT-clauses at the tail, so the first clarifying clause someone adds to one of those three is
the clause that silently disappears from the listing the model routes on. `preflight.py` now reads
`DESCRIPTION_LISTING_TRUNCATION` from this table and reports crossing it as a **distinct, harder
finding** than the 1024 style finding, plus a warning inside 100 characters. Both were proven to
fire before shipping. The 1,536 itself was re-verified the same day against held bytes
(`knowledge/raw/claude-code-docs-2026-09-04b/skills@2026-09-04b.md`): unchanged.

This line previously read "19 of 79", which was 15 of 85 by the time an independent tester flagged
it. That is the **second** running statistic in this file pinned as if it were a fixed value (see
`SILENT_DEFECT_SHARE`). The lesson generalises and is now a rule for this file: **a value that
moves on its own must be recorded as a finding plus a pointer to its live computation, never as a
number.** A pinned number that drifts is worse than no number, because it is cited with the
authority of this file. What is fixed here is the standard (1024) and the consequence (trim only
with a trigger check); the count belongs to `preflight.py`.

## Concurrency

| Constant | Value | How we know it |
|---|---|---|
| `W_MAX_AGENTS` | **4** | `measured` — 2026-09-01, against a threshold fixed before any number existed: `pipeline/prereg/2026-09-01-w-max-agents-2-vs-4.md`, rows in `pipeline/bench/runs/`. 56 runs, 3 valid batches per arm, alternated. Batch wall clock **32.8s at 4 against 59.0s at 2 (ratio 0.556)**, per-run **1.11x**, **0 failures**. Supersedes the previous value of 2, which was labelled `measured` from `min(16, cores-2)` and whose citation (STATUS:21) does not resolve — a formula modelling CPU contention, over a workload measured at **73% API wait**. **Licenses 4 and nothing above it:** 8 and 16 were not measured. **GLOBAL and shared** across loops, unchanged. Says nothing about write collisions — that is held by *coordinator commits, agents produce*, not by this number. |

**A vendor qualifier found 2026-09-08, which neither refutes nor licenses a change.** The
workflows page states its concurrency cap as *"Up to 16 concurrent agents, **fewer when Claude
Code has fewer CPUs available, including inside a CPU-limited container**"* (held bytes,
`knowledge/raw/baseline-2026-09-04/code.claude.com_docs_en_workflows.md:349`). So the host does
bound concurrency by CPU — the mechanism this table rejected when it retired the old value of 2,
which came from `min(16, cores-2)` over a workload measured at 73% API wait. The rejection still
stands and for the same reason: a formula is not a measurement, and **4 was measured on this box
against a threshold fixed beforehand**. What the qualifier changes is the confidence that 4 will
travel — on a larger machine the measured number may be higher, and on a smaller one the host may
already be cutting below it. Do not move the constant on this; re-measure, or leave it.
[[dynamic-workflows]] carries the same finding on the note side, and that page has not been
re-read since 2026-08-27.

## Test-suite shape

| Constant | Value | How we know it |
|---|---|---|
| `BLEND_NORMAL_TARGET` | **~50%** | `decided` — half representative, half clever, plus at least one negative-trigger. |
| `BLEND_TOLERANCE` | **±15pp** | `decided` — the band `signals.py` calls BALANCED. |
| `ADVERSARIAL_SHAPE` | **pressure, not technique** | `measured` 2026-08-28 — see `calibration/RESULT.md`. Of 12 adversarial scenarios claiming a baseline failure, **one** actually failed, and it was a social-pressure case. Technique traps do not separate talent from baseline at this model tier. |
| `BASELINE_FIELD_RULE` | **observation or `null`** | `measured` — never written from the scenario's own label. The field was a perfect function of that label across 181 rows and scored kappa **−0.129**, worse than chance. |

## Source yield (drives what harvest is worth running)

| Constant | Value | How we know it |
|---|---|---|
| `YIELD_HIGH_WATER` | **0.50** | `decided` — at or above → seek-more. |
| `YIELD_LOW_WATER` | **0.10** | `decided` — below, over ≥ `MIN_ITERS` → deprioritize. |
| `MIN_ITERS_FOR_VERDICT` | **2** | `decided` — one iteration never earns a verdict, however extreme. |
| `PRODUCER_MEASURE` | **`candidates`, never `adopted`** | `measured` — a harvest or scout pass hands work to a later stage; scoring it by the consumer's adoptions reads 0.00 for excellent work and computes to deprioritize the best source we have. |

## Detection

| Constant | Value | How we know it |
|---|---|---|
| `SILENT_DEFECT_SHARE` | **>=70%, and rising — read the live figure, never this one** | `measured`, but it is a RUNNING STATISTIC and was wrongly pinned as a fixed value. First recorded at 20/28 = ~70%; at 48 defects it is 39/48 = 81%. A number that moves every wave goes stale between readings, so citing the pinned figure is itself a mismeasurement — the failure this row exists to warn about. **What is pinned here is the finding and its consequence, which do not move:** the majority of this library's defects fail silently, meaning absence of a result is indistinguishable from a correct negative, so an audit must RUN the method's own search and confirm a known-present item comes back. Reading cannot find these. For the current share, run `python3 pipeline/queries/signals.py`, which computes it from the ledger. Restructured 2026-08-28 by the coordinator after an independent tester flagged the pinned number stale and correctly declined to edit it. |
| `FRONTMATTER_CHECK` | **line-anchored** | `measured` — line 1 is exactly `---`, a later line is exactly `---`, and the block between parses with `name` and `description`. A `split('---')` check ignores line boundaries and reports green on an unterminated file; it passed three unloadable talents in one day. |

---

## Rules for this file
- **Read it; never write it from a loop.** If a value needs to change, that is a human decision.
- **Point here instead of repeating.** A number restated in a second document is a number that will
  drift, and the drift is silent because both copies look authoritative.
- **Every value carries its source.** A constant without one is a guess with a table around it.
- **`measured` values name their measurement** so anyone can re-run it and disagree with evidence.
