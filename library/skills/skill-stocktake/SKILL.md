---
name: skill-stocktake
description: "Use to take a periodic INVENTORY of a library of capability units (skills, commands, and similar) and grade each on quality: what exists, what overlaps, what is stale, what is untested, what has broken cross-references. Produces a per-unit verdict table (Keep/Improve/Update/Retire/Merge). Supports Quick Scan (changed units only) and Full Stocktake (everything). Triggers: 'audit our skills', 'what is in our library', 'which skills overlap', 'stocktake', 'inventory the skills'. Removal verdicts are test-validated proposals to a human, never actions; disuse is never grounds. NOT deriving the library-wide job-to-owner routing table or proving boundaries with negative triggers (capability-routing-table): this reports THAT units overlap; that decides who OWNS each job. NOT the continuous test-and-fix pass over an adopted library (library-curator), NOT authoring or editing a unit (writing-skills), NOT prior-art search before building (skill-scout). NOT duplicate functions in code (semantic-duplicate-sweep)."
metadata:
  origin: ECC
---

# skill-stocktake

Audits a library of capability units against a quality checklist plus holistic judgment. Two
modes: **Quick Scan** (only units changed since the last run) and **Full Stocktake** (everything).
Invoke it by name or by asking for the audit — this ships as a skill, not as a registered
slash command, so do not rely on a `/`-prefixed invocation existing.

## Scope

The command targets the following paths **relative to the directory where it is invoked**:

| Path | Description |
|------|-------------|
| `~/.claude/skills/` | Global units (all projects) |
| `{cwd}/.claude/skills/` | Project-level units (if the directory exists) |

**Enumerate every capability CATEGORY, not just the one with the tidiest layout.** Units do not
all share a shape: a skill may be a directory with a definition file inside, an agent a single
file, a command something else again. Enumerate each category's own path and report the counts
per category. A category nobody scans is a category nobody maintains, and the coverage number
reads 100% either way — which is exactly how one goes missing.

Where a category is genuinely out of scope for this pass, say so in the report by name and count.
Never let "N units audited" imply the whole library was seen.

**At the start of Phase 1, the command explicitly lists which paths were found and scanned.**

### Targeting a specific project

To include project-level units, invoke this skill with that project's root as the working
directory — the project path is derived from `$PWD`, so running it from elsewhere silently
audits a different library than you meant.

If the project has no `.claude/skills/` directory, only global units are evaluated — and the
report must SAY so. A scan that found nothing where the units actually live is indistinguishable
from a library that is empty; Phase 1's path listing exists precisely to tell those apart, so
never report a result without it.

## Modes

| Mode | Trigger | Duration |
|------|---------|---------|
| Quick Scan | `results.json` exists (default) | 5–10 min |
| Full Stocktake | `results.json` absent, or asking explicitly for a full stocktake | 20–30 min |

**Results cache:** `<this skill's dir>/results.json`

## Quick Scan Flow

Re-evaluate only skills that have changed since the last run (5–10 min).

1. Read `<this skill's dir>/results.json`
2. Run: `bash <this skill's dir>/scripts/quick-diff.sh \
         <this skill's dir>/results.json`
   (Project dir is auto-detected from `$PWD/.claude/skills`; pass it explicitly only if needed)
3. If output is `[]`: report "No changes since last run." and stop
4. Re-evaluate only those changed files using the same Phase 2 criteria
5. Carry forward unchanged skills from previous results
6. Output only the diff
7. **Any Retire or Merge verdict produced here goes through Phase 4's consolidation gate,
   exactly as in a Full Stocktake.** Quick Scan applies the same evaluation criteria, so it
   can reach the same removal verdicts; running it without the gate would let the short mode
   do what the long mode is not allowed to do unreviewed. The gate belongs to the verdict,
   not to the mode that produced it.
8. Run the save-results script against the results cache.

## Full Stocktake Flow

### Phase 1 — Inventory

Run: `bash <this skill's dir>/scripts/scan.sh`

The script enumerates skill files, extracts frontmatter, and collects UTC mtimes.
Project dir is auto-detected from `$PWD/.claude/skills`; pass it explicitly only if needed.
Present the scan summary and inventory table from the script output:

```
Scanning:
  ✓ ~/.claude/skills/         (17 files)
  ✗ {cwd}/.claude/skills/    (not found — global skills only)
```

| Skill | 7d use | 30d use | Description |
|-------|--------|---------|-------------|

### Phase 2 — Quality Evaluation

Launch a general-purpose subagent with the full inventory and checklist, using whatever
delegation tool the harness provides. **Pseudocode** — the tool name and argument names differ
between harnesses; check yours rather than copying this literally:

```text
Delegate(
  subagent_type="general-purpose",
  prompt="
Evaluate the following skill inventory against the checklist.

[INVENTORY]

[CHECKLIST]

Return JSON for each skill:
{ \"verdict\": \"Keep\"|\"Improve\"|\"Update\"|\"Retire\"|\"Merge into [X]\", \"reason\": \"...\" }
"
)
```

The subagent reads each skill, applies the checklist, and returns per-skill JSON:

`{ "verdict": "Keep"|"Improve"|"Update"|"Retire"|"Merge into [X]", "reason": "..." }`

**Chunk guidance:** Process ~20 skills per subagent invocation to keep context manageable. Save intermediate results to `results.json` (`status: "in_progress"`) after each chunk.

After all skills are evaluated: set `status: "completed"`, proceed to Phase 3.

**Resume detection:** If `status: "in_progress"` is found on startup, resume from the first unevaluated skill.

Each skill is evaluated against this checklist:

```
- [ ] Content overlap with other units checked
- [ ] Overlap with the project's always-loaded steering docs checked
- [ ] Freshness of technical references verified (use WebSearch if tool names / CLI flags / APIs are present)
- [ ] Cross-references resolve — every sibling unit named actually exists
- [ ] TEST COVERAGE recorded: does this unit have a test suite, and did it pass?
```

**Usage frequency is deliberately NOT on this checklist.** It is reported as context in the
inventory and is never an input to a verdict — see the removal rule below.

Verdict criteria:

| Verdict | Meaning |
|---------|---------|
| Keep | Useful and current |
| Improve | Worth keeping, but specific improvements needed |
| Update | Referenced technology is outdated (verify with WebSearch) |
| Retire | **Test-validated failure only:** the unit does not beat baseline on its own tests and cannot be fixed. Cite the failing scenario. |
| Merge into [X] | Substantial overlap with another unit; name the merge target AND the concrete task whose correct handler is ambiguous between them |

### The removal rule (read before writing any Retire or Merge verdict)

**Never propose removing a unit for being unused, niche, rarely triggered, old, or "low value".**
A library like this is used across projects and over time; a method nobody needed this month may
be exactly what next month's task needs. The ONLY removal criterion is a unit that fails its own
tests and cannot be repaired.

Write this rule against the OUTCOME, not one verb. A unit leaves the library whether you call it
delete, archive, retire, merge away, move out, demote to a reference doc, or "consolidate" — all
of them need the same test evidence. A Merge is a removal of one of the two units.

**Missing usage telemetry reads as UNKNOWN, never as zero.** If the usage source is absent or
unreadable, every unit reports no activity, and a rule keyed on usage would then nominate the
entire library at once. Treat an absent counter as no information: print `n/a`, not `0`. (A count
has a meaningful zero; the sentinel for "not measured" must be distinct from it.)

**Size is not a defect.** "The library has N units, trim it to M" is not a finding. There is no
target count, and no verdict may be justified by the library's total size.

Evaluation is **holistic AI judgment** — not a numeric rubric. Guiding dimensions:
- **Actionability**: code examples, commands, or steps that let you act immediately
- **Scope fit**: name, trigger, and content are aligned; not too broad or narrow
- **Uniqueness**: value not replaceable by the project's steering docs or another unit
- **Currency**: technical references work in the current environment
- **Verification**: the unit has a test suite, and it passes. An untested unit is an
  INVENTORY finding ("untested — needs a suite"), never a removal finding.

**Reason quality requirements** — the `reason` field must be self-contained and decision-enabling:
- Do NOT write "unchanged" alone — always restate the core evidence
- For **Retire**: state (1) what specific defect was found, (2) what covers the same need instead
  - Bad: `"Superseded"`
  - Good: `"disable-model-invocation: true already set; superseded by continuous-learning-v2 which covers all the same patterns plus confidence scoring. No unique content remains."`
- For **Merge**: name the target and describe what content to integrate
  - Bad: `"Overlaps with X"`
  - Good: `"42-line thin content; Step 4 of chatlog-to-article already covers the same workflow. Integrate the 'article angle' tip as a note in that skill."`
- For **Improve**: describe the specific change needed (what section, what action, target size if relevant)
  - Bad: `"Too long"`
  - Good: `"276 lines; Section 'Framework Comparison' (L80–140) duplicates ai-era-architecture-principles; delete it to reach ~150 lines."`
- For **Keep** (mtime-only change in Quick Scan): restate the original verdict rationale, do not write "unchanged"
  - Bad: `"Unchanged"`
  - Good: `"mtime updated but content unchanged. Unique Python reference explicitly imported by rules/python/; no overlap found."`

### Phase 3 — Summary Table

| Skill | 7d use | Verdict | Reason |
|-------|--------|---------|--------|

### Phase 4 — Consolidation

1. **Retire / Merge**: present detailed justification per file before confirming with user:
   - What specific problem was found (overlap, staleness, broken references, etc.)
   - What alternative covers the same functionality (for Retire: which existing skill/rule; for Merge: the target file and what content to integrate)
   - Impact of removal (any dependent units, steering-doc references, or workflows affected)
2. **Improve**: present specific improvement suggestions with rationale:
   - What to change and why (e.g., "trim 430→200 lines because sections X/Y duplicate python-patterns")
   - User decides whether to act
3. **Update**: present updated content with sources checked
4. **Every removal outcome is a PROPOSAL to a human, never an action** — delete, archive, merge
   away, move out of the library, and demote to a reference doc all count. Cite the failing test
   scenario in each. Sharpening a description is reversible and may be applied directly.

## Results File Schema

`<this skill's dir>/results.json`:

**`evaluated_at`**: Must be set to the actual UTC time of evaluation completion.
Obtain via Bash: `date -u +%Y-%m-%dT%H:%M:%SZ`. Never use a date-only approximation like `T00:00:00Z`.

```json
{
  "evaluated_at": "2026-02-21T10:00:00Z",
  "mode": "full",
  "batch_progress": {
    "total": 80,
    "evaluated": 80,
    "status": "completed"
  },
  "skills": {
    "skill-name": {
      "path": "~/.claude/skills/skill-name/SKILL.md",
      "verdict": "Keep",
      "reason": "Concrete, actionable, unique value for X workflow",
      "mtime": "2026-01-15T08:30:00Z"
    }
  }
}
```

## Notes

- Evaluation is blind: the same checklist applies to all skills regardless of origin (ECC, self-authored, auto-extracted)
- Anything that removes a unit from the library requires explicit user confirmation, whatever
  it is called: archive, delete, retire, merge away, move out, or demote to a reference doc
- No verdict branching by skill origin

## In this repo (one instance of the general method)
- Units are "talents" (skills, agents, commands) under `.claude/skills/`; the scan sees the
  skill directories, and `.claude/agents/` is outside it — report that gap rather than implying
  full coverage.
- The removal rule above is the repo's standing rule in `CLAUDE.md`: drop ONLY what fails its
  tests; never prune for disuse, niche-ness, or rare triggering.
- Test coverage per unit is `.claude/skills/<name>/evals.md`; an absent suite is an inventory
  finding for the curation backlog, not a removal finding.
- Removal proposals go to the human gate and are logged in `pipeline/ledgers/proposals.jsonl`.
- Deciding who OWNS each contested job, and proving it with negative triggers, belongs to
  `capability-routing-table`; this pass reports THAT units overlap and hands it that input.
- Continuous maintenance (testing and fixing the adopted library) belongs to `library-curator`;
  this method takes the periodic INVENTORY that tells the curator what to work on.
