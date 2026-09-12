# Piano status log

One line per wave: date · wave · job · outcome · next. Updated by `/piano`.

| Date | Wave | Job | Outcome | Next |
| --- | --- | --- | --- | --- |
| 2026-08-27 | setup | bootstrap | 34 talents adopted; catalog (469) triaged; ECC fit=3 swept; descriptions curated; CLAUDE.md + ROUTING + SPEC + BUILD written | Author brain-talents (research-scout first) or run harvest waves over remaining catalog |
| 2026-08-27 | 1 | author+run research-scout | authored research-scout talent; generated 22 search terms, 24 entities, queued 10 sources for the harvester | wave 2: harvest a queued source (e.g. anthropics/skills or a 'top 10' list) |
| 2026-08-27 | 2 | harvest top-N web lists | dedup: nothing new to factory (all vertical/covered); queued 5 new sources incl. rohitg00/awesome-claude-code-toolkit; library candidates + MCP leads → intake/wave2-top-n.md | wave 3: harvest rohitg00/awesome-claude-code-toolkit (agents/skills/commands) |
| 2026-08-27 | 3 | harvest rohitg00/awesome-claude-code-toolkit | 40 skills/138 agents/262 commands inventoried; gates routed 277 vertical/utility items to LIBRARY; 0 adopted; 4 flagged for later eval (manage-skills, claude-memory-kit, deep-dive, analyze-prompt) → intake/wave3-rohitg00.md | wave 4: harvest hesreallyhim/awesome-claude-code, or eval the 4 flagged |
| 2026-08-27 | graphify pilot | test all Graphify features | installed graphifyy 0.9.50; built ECC code graph (11,915 nodes, 0 LLM); exercised query/explain/path + graphml/obsidian/wiki/callflow exports — all work free; ADOPTED as factory step; wiki export flagged as KB input | resume harvest waves (hesreallyhim/awesome-claude-code) |
| 2026-08-27 | graphify wiring | make Graphify a runnable talent | authored `graphify-harvest` talent (install graphifyy → extract --code-only → query/explain/path → commit GRAPH_REPORT.md); wired into CLAUDE.md capability map + ROUTING.md "Harvest a GitHub repo" chain; now actually invoked, not just documented | resume harvest waves (hesreallyhim/awesome-claude-code) |
| 2026-08-27 | graphify full-surface audit | re-check ALL graphify commands | dumped full `graphify 0.9.50 --help`; found + wired missed high-value cmds (god-nodes, affected, global cross-repo graph, benchmark, --postgres); documented every deliberate skip w/ reason (auto-run hooks/installers=security, label/add/--mode deep=LLM cost) | build the cross-repo global graph over harvested repos |
| 2026-08-27 | ECC re-audit | close description-only triage gap | 4 parallel reviewers deep-read fit2=100 + fit1=30 spotcheck + adapt=27; fit1 triage 97% sound (no full re-read needed); **10 validated new talents** deduped; security items rejected w/ reasons; catalog decisions updated → intake/ecc-reaudit.md | build the 10 validated talents (cross-cutting first) |
| 2026-08-27 | build wave | build 5 cross-cutting talents | 5 parallel authors (dogfood writing-skills) built + reviewed: `prompt-refinement`, `agent-surface-security-audit` (safe read-only reimpl), `cost-aware-model-routing`, `decision-council`, `agent-blast-radius-guard` (method not hook); wired into CLAUDE.md map + ROUTING; catalog sources marked adapted_into | build the 5 domain talents on-demand (spec-mining, opt-loop, style-inheritance, hybrid-parse, mlops-review) when a matching task arrives |
| 2026-08-27 | loop infra | self-improve + deploy + templates | completion-chained waves (send_later, no cron); `wave-reflect` self-improve loop (metrics.jsonl → LESSONS.md → read-back at wave step 1; source-yield/prune/sharpen); `talent-deploy` (wire + `register_repo_root` reload so added talents go live); `templates/` scaffolds (technique/orchestrator/agent/command); all wired into piano + ROUTING + CLAUDE.md | start wave 1 (`anthropics/skills`) — chain self-advances |
| 2026-08-27 | 5 | harvest anthropics/skills (official) | 19 skills: all vertical/library (docx/pdf/design/comms) or covered (mcp-builder↔mcp-server-patterns); 0 factory talents adopted (correct); extracted skill-creator method → knowledge note + build-candidate `skill-description-optimizer` + eval-harness variance upgrade; wave-reflect logged, LESSONS updated (vendor-repo lesson) | wave 6: harvest `modelcontextprotocol/servers` (next in queue) |
| 2026-08-27 | 6 | harvest modelcontextprotocol/servers | reference MCP server code — 0 talent surfaces (no SKILL/agents/hooks); recorded 7 official servers (filesystem/git/fetch/memory/sequentialthinking/time/everything) to MCP shelf in mcp.md; covered by mcp-server-patterns; **loop reordered its own queue per LESSONS** — awesome-lists sunk, primary repos raised | wave 7: harvest `getzep/graphiti` (primary domain repo, promoted by lessons) |
| 2026-08-27 | 7 | harvest getzep/graphiti | temporal-KG agent-memory framework — 0 talent surfaces; knowledge note (bi-temporal facts, provenance, incremental updates, hybrid retrieval); NOT adoptable infra (needs DB server, like Zep — our model is git-native); MCP server noted w/ backend caveat; informs unified-memory | wave 8: papers (arxiv cs.AI agentic workflows/memory/tool-use) |
| 2026-08-27 | 8 | **PARALLEL build+scout wave** | 13 agents via Workflow: built 6 talents (skill-description-optimizer, behavioral-spec-mining, measured-optimization-loop, style-inheritance, hybrid-parse-escalation, mlops-production-review) — all verified safe+quality, verdict ship; scout emitted 6 high-yield sources (dspy/outlines/simonw-llm/pydantic-ai/hamelsmu/arxiv-self-improve); wired into CLAUDE.md+ROUTING; catalog sources→built; yield 1.0; piano upgraded to parallel fan-out model | harvest the new practitioner/framework sources in parallel, or build more candidates |
| 2026-08-27 | 9+10 | **TWO factory loops at once** | ran 2 factory workflows concurrently (queue split 3+3: dspy/outlines/simonw ∥ pydantic-ai/hamelsmu/outlines); coordinator-merged both; practitioner repos yielded 10 candidate methods → **7 build-worthy queued** (llm-judge-calibration, error-analysis-taxonomy, synthetic-eval-data-generation, llm-call-ledger, external-domain-audit, integration-contract-completeness, metric-driven-prompt-optimization); security-flagged installers kept out (npx skills / llm plugins). Concurrency finding: two loops SHARED W=2 → no throughput gain (cap is global) → intake/wave9-two-loops.md | build the 7 queued candidates (parallel build wave) |
| 2026-08-27 | 11 | **TEST wave (retroactive)** | ran the new mandatory TEST loop step on the 11 talents built without functional eval: each got SPECIFIC scenarios (representative + planted-defect/pressure) + baseline-vs-with, persisted as `.claude/skills/<name>/evals.md`. **8 passed, 3 fixed** — agent-surface-security-audit (prose-vs-code token precision), decision-council (red-team-the-rubric before fan-out), agent-blast-radius-guard (user-instruction=approval + unattended hard-disable/queue). Quality-verify had passed all 11 → proves the test step earns its place | resume harvest/build waves (now test-gated before commit) |
| 2026-08-27 | 12 | **full loop: build→TEST→commit (7 candidates)** | first end-to-end test-gated wave: built the 7 queued eval/review candidates (llm-judge-calibration, error-analysis-taxonomy, synthetic-eval-data-generation, llm-call-ledger, external-domain-audit, integration-contract-completeness, metric-driven-prompt-optimization) → TEST step authored clever baseline-vs-with scenarios → **all 7 PASSED**, evals.md persisted; wired into CLAUDE.md map; catalog build queue cleared | run first library-curator pass (write evals for the ~37 untested, sharpen descriptions, health scorecard) |
| 2026-08-27 | 14 | **loop verification (full chain)** | ran one full loop wave on promptfoo/promptfoo: harvest → 4 gates (security kept out promptfoo's auto-run hooks + remote attack service) → auto-build fed by harvest → TEST → commit. 2 talents built (llm-eval-harness, llm-redteam-scan) both PASSED 6/6 blended evals; llm-eval-harness's negative-trigger confirmed it hands off to eval-harness (no overlap). Loop verified end-to-end | trust the schedule — piano 00:03, curator 23:05 |
| 2026-08-27 | 15 | piano wave (concurrent w/ curator) — FINISH | ran a full loop wave (harvest jxnl/instructor → gate → auto-build → TEST → commit) CONCURRENTLY with a curator batch (both parallel, proving simultaneous loops). 2 built + PASSED: structured-llm-extraction (schema+reask), streaming-partial-parse; instructor network/creds kept out. Piano stops here per user (no new waves) | curator finishes its 3×10 backlog, then both stop |
| 2026-08-27 | 16 | CURATION pass 2 (10) | 10 untested talents curated, all passed + improved; caught a real ACCURACY defect — graphify-harvest's `--obsidian` vault claim is FALSE (0.9.50 silently ignores it, re-verified vs binary), fixed in SKILL.md + knowledge note; 5 dead-refs repaired, learn-eval missing `name:` added, eval-harness invented slash-commands reframed; 0 drops. 4 new CURATION-LESSONS (verify tool claims, hunt invented cmds, check name:) | final curator batch → 100% tested, then stop |
| 2026-08-27 | 17 | piano wave (one more) — Aider | harvest Aider-AI/aider → gate (installer/scrape/telemetry kept out) → auto-build → TEST → commit. 2 built + PASSED 6/6: repo-map (PageRank token-budget context selection), apply-llm-edits (fuzzy edit application). test-wave now applies CURATION-LESSONS structural pre-checks — shared brain confirmed working | final curator batch → 100% tested, then stop |
| 2026-08-27 | 18 | CURATION pass 3 (3×10 done) | final manual curator batch: 10 method talents curated, all passed + improved (blended evals, sharpened descriptions, dead-ref/namespace fixes); 1 human-gate proposal surfaced (systematic-debugging: remove 4 legacy test-*.md, format-drift). The user's 3×10 backlog is cleared; MANUAL runs stop here. Schedule takes over: piano + curator both 3h/4h (cron 0 0,4,8,12,16,20), curator now new-first-then-deepen-old | schedule runs autonomously from 00:03/00:05 UTC |

- **2026-08-28 wave 20 (piano, scout)** — Cron fired INTO the persistent session (00:03), confirming
  the scheduled path works where four spawned runs failed (private repo, credential-less containers).
  Weekly quota at warning → throttled per the new window-length rule: 1 agent, no harvest (1% yield).
  Build queue was empty → refilled with **6 validated candidates** (stage-ablation-attribution,
  eval-set-curation, abstention-threshold-design, agent-fault-injection, idempotent-action-design,
  data-contract-assertions); **5 rejected as duplicates** with per-candidate reason codes. Coordinator
  verified the scout's dedup claims rather than trusting them. Nothing built — build is wave 21's job.

- **2026-08-28 wave 21 (curator)** — Cron fired into the persistent session (00:10). Throttled to
  2 agents (weekly quota warning). **Prioritized by USAGE, not alphabet**: the two most-used
  untested talents. Both carried LOAD-BEARING defects. `skill-scout` (12 waves) searched only
  `~/.claude/skills`, never project-scoped `.claude/skills/` — the dedup gate ran blind (measured:
  0 hits vs 4). `factory` (8 waves) documented `W` as per-run when STATUS:21 records it is GLOBAL —
  a caller would start a 2nd loop for zero gain. Both fixed, plus 2 dead cross-refs, nproc
  portability, mid-fan-out failure behaviour, unnamed drivers. Coverage 57→59/65. 1 convention
  question to the human gate (disable-model-invocation vs caller wording, 3 talents).

- **2026-08-28 wave 22 (piano BUILD + curator, both in-session)** — Cadence restored to 4h on the
  user's call (the 8h throttle had cost an overnight build wave). **The TEST gate earned its place
  twice**: independent testers — never the author — failed BOTH talents on first run; both triaged
  skill-bug; both fixed with the tests left unchanged. `stage-ablation-attribution` (new, shipped)
  gave two incompatible denominators for one column; its tidy 100% was the symptom of dividing by
  Σ headroom and hid the non-additivity it elsewhere insists on → now 82/18/29 = 129% with the
  denominator in the header. `writing-skills` — which authors ALL our talents — had **zero**
  awareness of the library it writes into (0 mentions of skill-scout/dedup) → mandatory Step 0
  added. It also taught 4 `superpowers:`-prefixed refs as ✅ examples, making it a plausible ORIGIN
  of namespace drift library-wide. Coverage 59→61/66. 1 proposal raised (its 3730 words vs the
  <500 it prescribes).

- **2026-08-28 wave 23 (piano BUILD x2 + list triage)** — Shipped `eval-set-curation` and
  `abstention-threshold-design`, both tested by agents that did NOT author them.
  `eval-set-curation` FAILED first (10/11, skill-bug): the floor set in step 4 was silently
  eroded by steps 5–6 with no re-check, and the worked example cut a cluster 121→12 against a
  floor of 30 in the same sentence. The tester's insight is the durable part — **dedup AFTER
  sampling undercounts variety**: draw 30 from a 10,400-row cell and dedup to 4 and you measured
  your draw, not the cell. Fixed with step 6a; the example now demonstrates the rule instead of
  breaking it. `abstention-threshold-design` passed 11/11 with its arithmetic control-counted.
  **List triage:** ~50 items across 5 blog lists + a ranked top-100 → **2 survivors (4%)**, same
  order as harvest's 1%. 15 rejections recorded per-candidate; directive written to LESSONS.
  The Medium list returned 403 and was NOT read — recorded as unread, not summarized.

- **2026-08-28 wave 24 (piano BUILD x2)** — Shipped `agent-fault-injection` and
  `idempotent-action-design`, complements built in parallel (one *detects* a missing idempotency
  key, the other *constructs* the guarantee). `agent-fault-injection` FAILED first (12/13): its
  A–E grading ladder was **unidirectional** — every class defined by the agent over-claiming, none
  for under-claiming. The tester built the case from the skill's OWN matrix row: write commits →
  timeout → 2 correct retries → "no ticket exists, file manually", ledger holding three. It fell
  through all five classes, so the claim-vs-ledger diff fired with no grade to emit. Fixed: E split
  into E1/E2 (both ship-blockers), C and D widened, assignment rules added.
  `idempotent-action-design` passed 11/11. **Meta-finding:** that tester refused a bad instruction
  of MINE — mandating "PASS. Beats baseline." on every line, which is false on normals. Template
  and CURATION-LESSONS fixed; the agent was right.

- **2026-08-28 wave 25 (piano BUILD + curator on wave-reflect)** — Build queue **emptied**:
  `data-contract-assertions` shipped (13/13). `wave-reflect` FAILED (14/15) — it asserted
  determinism twice while three of four rules left the deciding parameter unrecorded, and rule 4
  rested on a term no schema field could answer. Fixed with a pinned CONFIG block and an honest
  restatement (*same data + same recorded config → same lessons*).
  **Then the fix uncovered the biggest finding of the series:** recomputing under the pinned config
  made `github-practitioner` compute to *deprioritize* — contradicting a CONFIRMED lesson those
  same waves produced. `yield_rate = adopted/seen` was scoring a PRODUCER by a CONSUMER's outcome;
  harvest hands candidates to a later build wave, so it read 0.00 for work that produced 10
  candidate methods, 7 build-worthy. An automated rule was one pass from deprioritizing the
  library's best source type on a metric that measured the wrong stage. Fixed in method and
  instance. Standing directive: **when a computed verdict contradicts a lesson you trust, suspect
  the metric before obeying the rule.**

- **2026-08-28 wave 26 (harvest, 2 practitioner repos)** — 61 skills examined → **4 candidates
  queued, 1 deferred, 13 rejected** per-candidate. First wave scored as a **PRODUCER** after the
  measurement fix: 4/61 = 6.6%, which would have read **0.00** under the old `adopted/seen`
  formula. **Convergent discovery:** expand-contract sequencing was named independently by both
  sources. The two highest-value items are **not new talents** — `diagnosing-bugs` Phase 1 folds
  into `systematic-debugging`, expand-contract sequencing folds into `writing-plans`; both
  harvesting agents refused to make them talents because they collide on TRIGGER. 4 security
  rejections incl. an auto-running PreToolUse hook writing to `.claude/settings.json`.
  **signals.py fixed for stock-vs-flow:** live blend reads 45% BALANCED (was masked as 33% SKEWED
  by 341 backfilled scenarios), rejections report the live per-candidate distribution, and
  measurement coverage counts only instrumented waves.

## 2026-08-28 12:03 UTC — piano-cron uppskjuten (medvetet)
Cronen fyrade mitt i baseline-kalibreringen. Kördes INTE: W=2 var mättad av kalibreringens
baselineagenter, och en parallell harvest-våg hade skrivit git samtidigt som pågaende arbete.
Byggkön är tom sedan wave 27, så vagen hade blivit en skord med ~1%% utbyte. Tas efter
kalibreringen. Detta ar ett medvetet uppskov, inte ett missat trigger-fyrande.

## 2026-08-28 wave 29 (build) — two talents shipped, three defects that were mine

**Shipped:** `semantic-duplicate-sweep` (12/12, four skill-bugs) and `budget-cut-triage`
(12/12, one skill-bug). Both were caught by an independent tester failing *their own worked
example*: the duplicate sweeper's in-repo instance broke its own two rules, and the cut-triage
talent forbade at step 7 the exact action its own trigger admits. Two talents in one wave whose
showcase contradicted their rules is not coincidence — **a worked example is a test the author
never runs, so it is where an author's blind spot lands.** Standing directive: when authoring,
run the skill against its own example before shipping it.

**Three defects this wave were the coordinator's, not a talent's.** Recording them because a
loop that only counts talent defects will report itself healthy while its operator drifts.

1. **Frontmatter damage, third occurrence.** The edit that closed boundaries for the two new
   talents dropped every key that *followed* `description` in five files — four lost
   `metadata.origin`, and `graphify-harvest` lost `disable-model-invocation: true`, which is a
   **security gate**: that talent drives an external CLI and was deliberately not
   model-invocable. Silent, and caught only by reading the staged diff. Answered with
   `pipeline/queries/preflight.py`, which diffs each changed file's frontmatter key set against
   HEAD and fails on any key that vanished undeclared. It has positive controls for all three
   damage shapes actually seen here (dropped key, swallowed closing fence, over-cap
   description), because a check that only ever reports green *is* the silent defect.

2. **Three agents against a cap of two.** `W_MAX_AGENTS` was 2 at the time, labelled `measured`
   and recorded at STATUS:21 after 3-agent loops contended (**the cap is 4 since 2026-09-01, and
   that basis did not survive measurement — this entry is the history, not the current value**) — and I exceeded it in the same session that built
   CONSTANTS.md to prevent exactly this, minutes after reading the file. The cap was not
   forgotten; it was **never checked at dispatch time**. There is no gate between deciding to
   fan out and fanning out. Third agent stopped before it wrote anything.

3. **An n=1 claim left standing in the record.** `RESULT.md` still read "pressure, discipline,
   and library-specific routing" as what discriminates, with no pointer to `RESULT-pressure.md`,
   where the *pressure* leg of that same sentence was preregistered and refuted 2/12 against a
   >=4 threshold. Anyone reading RESULT.md alone still read a refuted claim as established.
   Corrected in place. The *routing* leg is still n=1 and is now labelled what it is — an
   **untested structural argument** (a baseline cannot name a private library's talents, an
   information asymmetry rather than an empirical regularity), never a measured discriminator.
   The `capability-routing-table` brief was rewritten to match, so its author cannot inherit the
   overstatement.

**The shape common to all three:** a value I had already written down, believed, and could
recite did not translate into a *check at the moment of acting*. Writing a constant down does
not enforce it. Only a gate does.

### Wave 29 addendum — the boundary rule is eating the budget that makes boundaries work

Measured while reviewing an author's neighbour edits: **28 of 82 descriptions are at or over the
1024 spec cap, and 12 more sit within 60 characters of it.** This is not a backlog of sloppy
writing. It is structural: this library requires every new talent to add a reciprocal NOT-clause
to each contested neighbour, so **each arrival spends headroom in K existing descriptions.** The
mechanism that keeps routing correct consumes the budget that makes routing possible.

Two escape hatches are closed, and one of them is closed on *mechanism*, which is the useful part:

- **Move NOT-clauses to the body.** No. The body is not loaded until the skill activates, so a
  body NOT-clause cannot prevent a wrong activation. It would read as a fix and silently do
  nothing — the exact silent-defect shape this library keeps finding in other people's work.
- **Move them to `when_to_use`.** No. Verified 2026-08-28 against `agentskills.io/specification`:
  the spec's entire frontmatter surface is `name`, `description`, `license`, `compatibility`,
  `metadata`, `allowed-tools`. **`when_to_use` is not in it.** It is a Claude-Code extension, so
  routing-critical text placed there does not travel — the exact trade `DESCRIPTION_CAP_CHARS`
  refused. Recorded as `WHEN_TO_USE_IS_PORTABLE = no`. (The same fetch re-verified 1024 against
  the primary source: "Must be 1-1024 characters".)

Left as an open human gate with a recommendation, not decided: treat the cap as a **forcing
function**. A talent needing more than ~5 boundary clauses is evidence of a contested region that
should be *consolidated*, not disambiguated further. This library has no prune trigger by design —
disuse is never grounds for removal, because it is cross-project — so nothing currently pushes back
on sprawl. The wall can be that thing.

## 2026-08-30 · Intake: all agent + skill material from hello-world and Scio

Coordinator pass, no agents dispatched, no wave. Gathered every unit that could become a
talent from both sibling repos into `intake/2026-08-30-agent-and-skill-material/`:
**416 files, each verified byte-identical to its source** by sha256 (0 mismatches).

The find that made this urgent: **9 of the 10 agents in this corpus, plus 24 skills, 6
hooks and a 15-file validation harness, existed only on an unmerged hello-world feature
branch** (`claude/multi-agent-system-architecture-nmn1pc`, 41 commits ahead of master,
newest 2026-08-29). An earlier inventory of the same repos missed all of it because it
read only the checked-out branch. Two further branches carry an A/B experiment's output
and the earlier versions of 17 shared files.

Nothing is adopted. It sits under `intake/`, not `.claude/`, for two mechanical reasons:
57 skills and 10 agents would join the startup listing immediately (agent descriptions
share a hard 15,000-token roster budget), and 28 executables came with the material while
the security gate has not run. Directories were renamed `.claude` to `_claude` and all
executables `chmod a-x`; file contents are untouched and the mapping is 1:1.

**No `metrics.jsonl` row was written.** This was not a wave and the wall clock was not
measured at the start — recording an estimate would violate the never-fake-a-measurement
rule in `DATA.md`. The record is this entry and the intake MANIFEST.

Next: the four gates have not run on any of it. See the MANIFEST's "known problems"
section — chiefly that the three agent-building skills' own ablation returned **null**,
and that 4 of 24 branch skills (and 0 of 27 Scio skills) carry evals.

---

## 2026-08-30 · Step 3 — the package admission gate

`pipeline/contracts/package.contract.json` + `pipeline/validate/package_contract.py`:
what the skill-builder must receive before it may start. 26 code rules, 6 agent checks.
Same three verdicts as the skill checker, and the third carries the same weight — an
**INDETERMINATE is a check that could not run, never a pass**.

The contract's authority is `house`, not Anthropic — Anthropic documents nothing about a
build package — so every rule carries a **reason** in place of a citation, and the reason
is always the same shape: *which step of the chain would otherwise improvise*.

Its governing line: **the package carries inputs, never outputs.** No field of the finished
skill arrives pre-written. The line is not formatted-versus-raw; it is *what a run cannot
produce* versus *what only a run can settle*.

One rule is a **refusal, not a defect report**. `pkg.failure_kind.not_discipline` rejects
any package whose skill would teach discipline under pressure: two preregistered rounds in
this repo found no scenario class that discriminates for it (technique traps 1 of 12,
pressure 2 of 12). The package may be perfect; we still could not show the skill works, and
a green suite would ship an unmeasured claim. Lift it when a discriminating test exists.

**Tested — 28 positive controls** (`pipeline/validate/selftest_package.py`), all green.
One clean fixture, broken one field at a time; each case asserts the owning rule turns red
**and that no other rule changes verdict unless the case declared it**. That third assertion
is the one that finds over-reach — it is the planted-defect analogue of what caught the
skill checker's three over-strict rules against Anthropic's corpus.

Three gates, each demonstrated failing rather than assumed:
- engine coverage — a contract rule with no implementation aborts the run (exit 2);
- control coverage — an implemented rule with no positive control aborts the selftest (exit 2);
- the selftest's own teeth — gutting `pkg.claims.quote` so it always passes was **detected**.

Also fixed a live wrong claim in `SKILL-BUILDER-SPEC.md`: running the checker over
Anthropic's own skills was written up as a positive control on the contract. It is not.
Those skills failing does not convict the contract — our 84 predate the documentation, and
Anthropic may be sloppy in their own repos. A rate gap only says *look here*; the
disposition is then rule by rule against the documentation, and only "the contract misread
the source" means the contract is wrong.

**No `metrics.jsonl` row.** Coordinator pass, no agents dispatched, wall clock not measured
at the start. `DATA.md` forbids the estimate.

Next: step 4, the v1 chain (phases 0, 1, 2, 4, 5, 6.1/6.2/6.4, 7.2, 8, 9). Standing gap
carried into it: the skill checker shipped without positive controls of its own.

## 2026-08-30 · The skill checker's missing controls

Closed the gap the step-3 entry names. `pipeline/validate/selftest_skill.py`: one clean
fixture skill (`fixtures/skills/migration-review/`, synthetic, says so in its own body),
broken one thing at a time, **44 controls covering all 43 code rules**, all green.

Why it mattered. The checker's earlier corrections came from running it over Anthropic's
38 shipped skills — a **negative corpus**, which finds rules that fire when they should
not. It cannot find the opposite defect: a rule that stays green on an artefact that
really is broken. Only a planted defect finds that, and writing the controls found one
immediately.

**`body.critical-first` could not fail on its own canonical case.** Its step-section
pattern matched the singular `step` but not `Steps` — the commonest heading name for a
step section — so a skill with Important placed after `## Steps` scored PASS. Widening it
exposed a second fault in the same rule: a heading naming both, like *"Important — read
before the steps"*, counted on both sides, making the rule fail on exactly the shape it
exists to reward. Both fixed; contract to **v1.2.0** with the correction recorded.

The fix costs nothing measurable: 0 additional skills flagged across our 84 and the 57 in
`intake/`, and the corpus totals are unchanged at 27 errors / 77 warnings. **Anthropic's
38 were not re-run** — that corpus was not kept on disk, so the 0-additional figure is
over 141 in-house skills only.

Both selftests were themselves tested by gutting a rule so it always passes
(`pkg.claims.quote`, `ref.dated`): **both detected it**. Both also abort rather than run
when a declared rule has no control.

Library state is unchanged and still awaiting the user's rebuild-through-the-builder pass:
84 skills, 27 errors, dominated by `desc.max`.

## 2026-08-30 · Step 4 — the v1 chain

**Code (`pipeline/build/`, 28 controls, all green).** `record.py` is phase 0.2 and the
spine every later phase appends to: `record.json` written once, `events.jsonl`
append-only. A phase cannot quietly revise what an earlier phase found — both rows stay
in the file and the disagreement is visible. It opens a record only for an admitted
package, running the gate itself rather than trusting the caller.

Three things a successful run has no reason to write down, each recorded because it is
unrecoverable later: a **skip carries its reason** (and a reasonless skip is refused —
"skipped because covered" and "never reached" are the same absence otherwise);
**`not_checked`**, because a record listing only what was verified reads as though
everything else was fine; and **null is not zero**, everywhere.

`decide.py` is phase 8.1 — the verdict as code, against the preregistered threshold.
Where the prose is not the contract's default and no structured rule was supplied it
returns UNDECIDABLE and says why, rather than interpreting a rule after seeing the
numbers. It will not treat a missing measurement as a pass, will not read a measured
zero as missing, and will not let one repeat decide.

The suite was tested by weakening the verdict two plausible ways — dropping the cost
axes, and letting one repeat decide. Both detected.

**Method (staged, NOT shipped).** `skill-contract` (phase 4), `skill-measure` (2/6/8),
`skill-knowledge` (3), and the `skill-builder` agent. All three skills pass the checker
at **0 errors, 0 warnings** — better than any of our 84, and a much weaker claim than it
sounds: well-formed is not the same as works.

They sit in `pipeline/skills/` and `pipeline/agents/`, not `.claude/`, because nothing
ships before its own evals have been **run**. Their `evals.json` carry prompts and
expectations; **no paired baseline-vs-with run has happened.** `README-STAGING.txt`
records that on disk.

**New ledgers:** `builds.jsonl` (one row per build, whatever the verdict — an abandoned
build is a row, not a silence) and `fields.jsonl` (one row per field per build, which is
what makes the builder measurable on itself).

Next: run the paired evals for the three staged skills through the chain itself — the
first real dogfood, and the acceptance test for the whole thing. Then v2 (phase 3's
fetch, 6.3 calibration, 6.5 triggers, 7.1 scripts, the `extend` branch).

## 2026-08-30 · The acceptance run, and the deploy

**24 agents, 1,876 s measured wall clock.** 20 arm-runs, 10 graders, two rounds. All three
of the builder's own skills pass every clause of the contract's default rule, **cost
included**, with no correctness regression across 48 paired question-repeats.

| | wins surviving both repeats | tokens | tool calls |
| --- | --- | --- | --- |
| `skill-knowledge` | Q3, Q4, Q5 — **Q5 discounted** for vocabulary coupling | 1.05× | **0.80×** |
| `skill-contract` | Q1 | 1.08× | 1.00× |
| `skill-measure` | Q4 only | 1.03× | 1.00× |

**Deployed:** moved from `pipeline/` staging into `.claude/skills/` and `.claude/agents/`,
added to the capability map, four `deployed` events logged. `skill-builder` is an agent and
was **not independently evaluated** — it orchestrates three skills that were, and that
distinction is in its ledger row.

### Three things this run established that the table does not show

**A skill's demonstrated contribution is usually one clause, not the file.**
`skill-measure` separated the arms on exactly one question — calibrating the grader against
a planted defect. The baseline already had every other measurement discipline tested.
Whether the undifferentiated sections are redundant or merely untested is **not settled**:
several shared passes sit on expectations the graders call near-unfailable.

**The expectations were the weakest part of the system, twice, and the graders found it
both times.** Round 1's set was recitable; it was **discarded as a verdict rather than
adjusted**, and re-run. Round 2's set is far better — the baseline falls from 1/5 to 0/4 on
`skill-contract` — and still has named defects. The instruction telling each grader to
attack the expectation set earned more than any other single line in this harness.

**Three harness bugs, one of which nearly inverted a result.** The section parser split on
the answer's own headings; fence-awareness did not fix it because the winning answer wrote
its file unfenced; and the code grader punished the more complete answer for bundling a file
the checker could not see. Before the fixes it scored a complete, contract-clean SKILL.md as
*nothing*. `selftest_score.py` exists to prevent exactly this and passed throughout — the
inversion was one stage upstream of what it watches. **A control proves the thing it watches
and nothing else.** Caught only by checking a surprising result against the raw file.

### Standing, unacted-on

The sharpest criticism of the whole run, and round 3's first job: *"none of them scores the
artefact against the failure the probe documented … none asks whether the produced file
would have caught the miss."* The question supplies two observed failures and never checks
the artefact against them.

Not checked: grader calibration (6.3), trigger firing (6.5), and how much of each token
delta is the method text the `with` arm was handed rather than work it chose to do.

Next: v2 — phase 3's fetch, 6.3, 6.5, 7.1 scripts, the `extend` branch. And the agent-builder,
which was always downstream of this.

## 2026-09-02 · The skill-builder fix — one harness, two modes, a shorter agent

Follows `pipeline/REVIEW-2026-09-02-skill-builder.md` (builds good skills; too slowly, and
unstably, with the instability concentrated in a dispatch harness that did not exist).

**Added, once: `pipeline/build/dispatch.py`.** The only way a probe, arm, reader, reviewer or
grader is now run. Fresh hashed directory per run with no arm string, method mounted for
`with` only and refused otherwise, reader inputs copied in, usage payload written to the cost
row, `arm_leak` flag on output that names its own arm. `selftest_dispatch.py` reconstructs the
three build-3 contaminations as positive controls (16 checks). `cost_gate` now fails a row
with no tokens, because it returned clean for a build in which every arm run had none.

**Added: modes** (chain contract 2.0.0). `full` ships; `fast` cannot — ceiling `fast_pass`,
with-arm only, one grader, fourteen phases skipped *at open* by `record.py` with a reason
naming the mode, so a skipped phase is never a forgotten one. `decide.py` refuses ship in
fast mode whatever the rows say; 14 new controls, both mutations (ship in fast; no skips at
open) caught at 79/81.

**Cut: the agent file**, 149 → 109 lines. Rule text the contract already carries is now read
from the contract once at phase 0 instead of every turn. New in it: the one-door rule for
dispatch, "do not idle on a run", and the mode choice.

**Not done, and said so:** the contract did not shrink — 39 phases, now ten top-level rule blocks. The
phase count is not what costs time (the agent file is what is read every turn), and merging
phases would renumber what three skills cite. The fast estimate (25–30 min) is DERIVED and
stands in the contract until a measured fast build replaces it. The full chain's floor is
28.3 minutes; the ten-minute build the user asked for is not a full build.

Next: one fast build, timed, to replace the estimate; then a full build on the same package
to see whether the harness holds under the three-arm measurement.

## 2026-09-02 · Eight videos and two images, claims verified, KB extended

Transcribed locally (faster-whisper `small`, int8, 114 s for 8 clips) and frame-sampled
every 4 s; every checkable claim taken to a primary source the same day. Seven notes
touched — four new (`loop-engineering-and-fable-prompting`, `model-agnostic-agent-harnesses`,
`prompt-patterns-kernel`, `learning-resources-agents`, `production-site-checklist`), three
extended (`temporal-kg-agent-memory` +gbrain, `agent-builder-prior-art` +addyosmani/agent-skills,
`long-text-comprehension` +the "five secret codes"), neighbours back-linked.

Headline verdicts: LOOPS.md's attribution to Karpathy is UNVERIFIED (searched, absent from
every primary); the "6 rules from Anthropic's docs" are MEASURED verbatim against the Fable 5
prompting page; Goose's "writes 90% of Block's code" is one engineer's own lines, not Block's;
"no logins" holds only for local models; the five "secret Claude Code codes" are not commands
(docs' built-in list checked) and the video was not even in Claude Code; addyosmani/agent-skills
(91.6k stars, 25 skills) is a harvest source with ≥9 collisions against our library; the
vibe-coded-site checklist is a ready `shape` fixture and a candidate definition-of-done for
generated sites in hello-world/Scio. Not verified: the "9 GitHub repos that replace $2,122"
carousel — only its cover slide was supplied.

Three things the Fable 5 page says that change our work, filed as actions in the note: skills
written for prior models "can degrade output quality" on Fable (measure, then cut); "show your
reasoning" instructions can trip a refusal and fall back to Opus 4.8 (audit skills); effort is
not fixed per run in `dispatch.py` (fix before comparing builds across tiers).

## 2026-09-02 · Second batch: six videos, two duplicates, four verified

Two were byte-identical re-uploads (Stanford CS329A, gbrain — md5 match, skipped). Four
new: **BASE** (ChristopherKahler/base — Rust hook binary that injects domain rules and a
tree-sitter graph at four hook points; PolyForm *Noncommercial*, 131 stars; the video's
"90% more consistent" is unsupported and its "MCP" is not in the README) → extended
`claude-md-and-memory`. **find-skills / skills.sh** (Vercel; 1.29M+ installs, vetting =
installs + stars + org whitelist; the "700,000 skills" is the creator's graphic) → extended
`agent-builder-prior-art`; it is a *source* for reuse-first, not a replacement for the four
gates. **Nemotron 3 Ultra** (550B/55B active MoE, 1M ctx, free on OpenRouter and OpenCode
Zen with logging + trial terms + an account; "killed Claude Code" is hype) and **the
260-free-APIs list** (mnfst/awesome-free-llm-apis, CC0, 7.3k stars; "260" unverified) →
extended `model-agnostic-agent-harnesses`. Same two images re-sent; already covered.

## 2026-09-02 · Third batch: eight videos, all new, verified

Two new notes and four extended. **`claude-code-ecosystem-plugins`** grades the plugin
stack two videos sell (OmniRoute MIT 60k★, claude-mem Apache 93k★ — *syncs memories to
cmem.ai by default*, Headroom Apache 68k★ — honest about where it saves little, Anthropic's
`claude-code-setup` — read-only, does NOT build skills or remove fluff as claimed,
task-observer — does NOT edit skills automatically as claimed, unlazy MIT 3k★ — gates file +
blocking Stop hook, the same mechanism as our stop hook; Graft — the 4×/3× is best-case, the
controlled figure is +42% tokens over 162 runs and SWE-bench 33/50 vs 27/50; codebase-memory-mcp
MIT 42k★; agency-agents MIT 150k★ personas without evals; OpenMontage **AGPL** 55k★ on paid
APIs). **`local-finetuning-layer-streaming`** (Soup, Apache, 8B on a 4 GB laptop GPU
measured bit-exact; a public *retraction* of its own v1 bottleneck claim — the practice
CONSTANTS.md asks for). Extended: `mcp` +AXI (ten CLI principles; 490-run and 425-run
benchmarks with the agent model as judge), `claude-md-and-memory` +ICM (arXiv 2603.16021;
the paper states no token number, the video's "1/5–1/6" is one person's plan usage),
`model-agnostic-agent-harnesses` +Pi/Herdr/OmniRoute, `research-methodology` +the quant
validation ladder (out of core domain, kept for the one-to-one map onto our own gates).

## 2026-09-02 · Fourth batch: eight videos, one duplicate, one silent

Nemotron clip byte-identical to batch 2 (skipped); one clip had no audio track (frames
only). New note **`harness-over-model-prime-agent`**: Prime Agent (MIT, 19.6k★, RLM +
`/refine` self-editing harness state with snapshots) — Opus 5 from ARC Prize's verified 30.2
to **95.5 on ARC-AGI-3 per Prime Intellect's own post**, three runs 95.0/95.2/95.5, 183/183
levels, with an official ARC scorecard linked but no independent replication; Ruflo (ex
claude-flow, MIT, 70k★ — video said 55k) swarm-with-consensus, the opposite bet to
Anthropic's few-agents guidance, no quality measurement either side. Extended
`production-site-checklist` with the 20-item security twin (Supabase-shaped: anon key, RLS,
server-side auth), the "$21/month startup stack" two creators repeat verbatim (Claude,
Supabase, Vercel, Clerk, Stripe, Resend, PostHog, Sentry, Upstash, Pinecone — nearly
hello-world's own stack, recorded as market default not recommendation), and the "slop"
trio (UI UX Pro Max MIT **124k★**, no network, no benchmark — the most-starred skill seen so
far; CodeRabbit and 21st.dev are products). Second Soup video: same press-kit lines, same
unsourced 85,000, noted as one source not two.

### Addendum from a second session, same day — cross-check and md5 ledger

The same seven clips were transcribed independently in a second session (faster-whisper
`small`, int8, 112 s; frames every 2 s) before the fourth-batch commit was seen. Findings
matched; the rival notes it had drafted were discarded and only three verified additions
were merged: the startup stack priced from ten vendor pages (Vercel Hobby is non-commercial
by its FAQ, so the startup floor is ~$41/mo, not $21), two verbatim Prime Agent quotes
(rollback by ID; "no model has been trained around Prime Agent"), and the gradability
split of the security twin (17 code-gradable, 3 need a definition). md5 of the seven, so
the next dedup is a lookup rather than a memory: startup-stack 7568fa1c07ec9816bdf9ee4849ff33e8
(9 s) and 7363536c7d595cb2bb03445a29a96a1a (8 s, no audio); Ruflo
e291d7c023b4163d439da41b347ad412; Prime Agent 3280be5ebe1c30c7d44b0782929f049e; security
twin 77d4297d51ee8a39f7557d44378ab9f7; Nemotron 54878cc09b851a258058f0745bf9902c (batch 2
clip); find-skills 352293dad521b56454fa3ba1785c7ae3 (batch 2 clip).
## 2026-09-02 · Fifth batch: four clips, three covers

New note **`llm-wiki-pattern`** — Karpathy's gist (his own account, 2026-04-04, 5k+ stars):
raw/ immutable, wiki/ LLM-compiled, schema; ingest/query/lint. Our `knowledge/notes/` is the
wiki layer with no raw layer and no lint; a `knowledge/lint.py` is the named follow-up. The
"agentic OS in three steps" video (domains→skills→automations, Obsidian, dashboard) corroborates
our `agentic-os` skill and names one gap: a button surface over skills for non-CLI users
(→ `claude-code-extension-layer`). "/dream self-healing": Anthropic's memory page, re-read in
full today, carries the 200-line/25 KB index limit and the `modified` stamp and **no dream
feature at all**; the community `dream-skill` (MIT, 136★) documents no snapshot or approval
step; the graphic's numbers are illustration (→ `claude-md-and-memory`). "Claude Code free
forever, 51k stars" and the 11-second "unlimited usage" clip both resolve to OmniRoute's
free-tier pool (→ `claude-code-ecosystem-plugins`). Two carousel covers ("1.5 GB model
challenging Claude", "10 repos / 1.8M stars / $40k") carry no content and were not chased.

### Addendum from the second session — four images, one correction, one new model

Four images (md5 a8e2b2a5…, 8ca9ec1b…, 5a6bcbc7…, 4b59e388…). **Correction to the fifth
batch:** the "Claude Code free forever, 51k stars" cover was resolved to OmniRoute as
UNCONFIRMED; its slide 2/4, supplied here, names the repo — `Alishahryar1/free-claude-code`,
MIT, 52.8k★, a separate project of the same shape (50 providers, "1.3B+ free tokens", Gemma
via OpenRouter inside Claude Code's `/model` picker). Graded in
`model-agnostic-agent-harnesses`; "free forever" is the Claude Code CLI on non-Claude free
models, with the subscription unused. **New:** Ornith-1.5 (DeepReinforce, 397B/35B/9B, MIT
REPEATED, HF card 401 to the fetcher) — "built to improve itself" is a *training-time*
task-proposal → scaffold → rollout loop, not a deployed behaviour; the blog's table beats
Opus **4.8** on four benchmarks and loses four, Frontier-Bench by a third; filed beside
Nemotron as a non-Claude-arm candidate. The "10 repos / 1.8M stars / $40k" cover (a8e2b2a5…)
carries no content, as the fifth batch already said; md5 recorded so it is not chased twice.

## 2026-09-02 · The knowledge of three repositories merged here, with one index

Asked to gather "all knowledge" from every repository and branch into one place. Inventoried
by **content hash** over Scio (2 branches), hello-world (7) and skills-repo (2): the
2026-08-30 intake already held everything but **52 files** — Scio's 20 documents of today
(ADR-0002…0013, the fresh-eyes review, the talent and data-store documents), hello-world's
three root review documents, six per-app CLAUDE/README files, six spike findings and four
library seed entries the intake had skipped, and the older docs revisions on two 2026-08
branches. Imported byte-identical under `knowledge/raw/<repo>@<branch>@<sha>/` with a
per-file sha256 manifest — the `raw/` layer `llm-wiki-pattern` named as missing. Nothing
deleted at any source; `.py` not treated as knowledge.

**`knowledge/kb.py`** is the single index: 569 documents, 6,798 sections, 7.4M chars, built
in 0.5 s with no model call; `find` quotes every token so punctuation cannot be a syntax
error (scio.db's crash on `WHICH/HOW`); `stale` lists verified notes whose newest fetch is
older than N days; `links` reports 6 dangling wikilinks and 31 one-way links today, the
first third of the `lint` the wiki note asks for; `selftest` plants a miss that must miss.
Not done: the rebuild-on-commit hook (one line, unwired), and the dangling links themselves.

## 2026-09-02 · The repository as an Obsidian vault

Question 1, does graphify have an Obsidian mode: **yes**, MEASURED on the installed 0.9.53 —
`graphify export obsidian [--graph] [--labels] [--dir]`; a 23-node test graph became 29
notes with frontmatter, `## Connections` wikilinks tagged by edge type, `_COMMUNITY_` notes,
a `graph.canvas` and a `.obsidian/graph.json`. The flag `extract --obsidian` is ignored (the
correction chain in `graphify-assessment` stands). Question 2, an Obsidian vault of the
knowledge base: the repo root is now the vault — `.obsidian/` committed (wikilinks, shortest
link resolution, ignore filters for builds/fixtures/ledgers, graph colours per layer),
per-machine state gitignored, `knowledge/VAULT.md` explains it and gives the on-demand
command for a separate code-graph vault of hello-world's 5,173 nodes. Not run through
Obsidian itself here (no desktop in this session): the JSON validates, 709 of 914 markdown files are
visible (the rest sit under the ignore filters), and `kb.py links` names the 6 unresolved nodes the graph view will show.
## 2026-09-02 · codebase-memory-mcp looked up on request

Full grading in `graphify-assessment` (the note that owns code graphs). MIT, 41.9k★, pure C,
SQLite, 162 vendored tree-sitter grammars, 15 MCP tools with an openCypher subset, real source
(6,768 tests). Installer: curl|bash, SHA-256 from the same release channel, writes MCP client
configs, strips macOS quarantine and ad-hoc signs. Same-day open issues: unbounded RSS growth,
11.5 GB on a 14k-file monorepo, `search_code` inventing paths and line numbers. "99% fewer
tokens" is one grep-strawman comparison. **Verdict SANDBOX**: throwaway container, harvested
code repos only, when a harvest outgrows Graphify; read the daemon and install code first.

## 2026-09-02 · Conclusions between nodes — what the index can and cannot draw

Asked whether conclusions can now be drawn between nodes. Four deterministic graph commands
added to `knowledge/kb.py`: `path a b` (shortest wikilink path, with the sentence each hop
sits in), `explain <note>` (in- and out-neighbours with their sentences), `shared <note>`
(notes citing the same source URL — related by evidence rather than by link), and
`cooccur "a" "b"` (sections anywhere in raw, intake and talents that mention both terms,
because those layers carry no wikilinks). Each edge now records whether it is **argued in
the body** or **asserted only in a `related:` line**; `links` reports the count.

What that showed on first use: the path from `harness-over-model-prime-agent` to
`production-site-checklist` is two hops through `claude-code-ecosystem-plugins` and both hops
are frontmatter-only — the connection is asserted, not argued. That is the honest state of
the graph: 36 notes, most edges in `related:` lines, a handful with a sentence behind them.
`cooccur` reaches the other 530 documents by co-mention, which is a weaker relation than an
edge and is labelled as such.

What the index does not do: draw the conclusion. It hands a session the path, the sentences
and the co-mentioning sections; the synthesis is the `query` operation of the LLM-wiki
pattern and stays a session's job, written back as a note when it is worth keeping. The
next deterministic step is the one that note already names: `lint` for contradictions —
two notes asserting different values for the same named fact — which needs facts to be
extracted as rows first (the `claims` ledger is the seed).

## 2026-09-02 · The third-party landscape, summarised as one page

Asked for a summary of everything the knowledge base holds about third-party skills, agents,
plugins, tools, tips and tricks. Compiled from all 36 notes, the ten mined documents' verdict
tables (~250 rows), the 469-entry catalog, the wave intakes and LESSONS into
`knowledge/notes/third-party-landscape.md`: ~80 named projects in a source table with yield and
pointer, the 44 adopted talents and the three the security gate stopped, ~200 taken mechanisms
grouped under eight themes, ten recurring reasons for rejection with instances, and six measured
lessons about harvesting. Nothing new was verified for it; it is the `query` operation of the
LLM-wiki pattern written back as a page, and it names its own limits.
## 2026-09-02 · GLM-5.3 looked up on request

New note `glm-5.3-local`. Two models under one name: GLM-5.3 (744B/40B active per GitHub,
753B per HF — Z.ai's own sources disagree; custom licence with a $10B MaaS clause) and
GLM-5.3-Flash (320B/18B, MIT). Search snippets conflate them. Local: flagship 2-bit needs
245 GB RAM+VRAM (a 256 GB Mac Studio is the floor, at 1–2-bit quality); Flash 3-bit fits
128 GB; llama.cpp support is fork-only; no tok/s published. Claude Code path is Z.ai's
Anthropic-compatible endpoint (three env vars; opus/sonnet→glm-5.3, haiku→flash) at
$1.40/$4.40 and $0.075/$0.25 per MTok — the cheapest possible non-Claude arm for
`dispatch.py`, pending a read of Z.ai's data terms. Release dates and Coding Plan prices
not retrievable from primary pages; marked as such.

## 2026-09-02 · Best local LLM, looked up on request

New note `best-local-llm-2026-09`, by memory tier, every number from a model card or
Unsloth's tables. Ceiling: Kimi K3 and GLM-5.3 score 60 on Artificial Analysis vs Fable 5.1's
66 — but Kimi K3 is 2.8T parameters and not a local model in any owned sense. One consumer
GPU: **Qwen3.8-27B** (Apache-2.0, 2026-08-14, Q4–Q6 = 16.5–22 GB; SWE-bench Pro 61.7 vs Opus
4.6's 53.4 on its own card). 128 GB floor for near-frontier at home: GLM-5.3-Flash 3-bit (MIT).
16 GB: Qwen3.6-35B-A3B or Gemma 4 26B-A4B, per NVIDIA's own controlled table, where Nemotron
3.5 Lightning loses every row. Dated on purpose.

## 2026-09-02 · Mac Studio M5 Max / Ultra for local LLMs, on request

Extended `best-local-llm-2026-09`: Apple's specs from the user's screenshot (128 GB / 614
GB/s vs 512 GB / 1.2 TB/s; ships 22 Sep, 512 GB late Oct; from 72 995 kr), MLX measurements
on an M5 Max 128 GB (MoE ~10B active 55–90 tok/s, dense 27B 15–24, prefill 800–2,700 t/s),
nothing measured yet on an Ultra — its numbers are DERIVED at ~2× from bandwidth. Verdict:
Max = strong up to ~120B-A10B MoEs and 27B dense at Q8; Ultra 512 GB = the one consumer box
that holds GLM-5.3-Flash 4-bit with headroom.

## 2026-09-02 · What to buy for local LLMs at normal prices, on request

Extended `best-local-llm-2026-09` with a Swedish price table (search results, not quotes):
used RTX 3090 24 GB ~12 200 kr is the tok/s-per-krona winner; Mac mini M5 Pro 64 GB from
22 495 kr and Strix Halo 128 GB ~27 000 kr for "what fits" and 24/7; Mac Studio M5 Max 128 GB
~70 700 kr is the first box both large and fast; new RTX 5090 at 50 000+ kr (up 35% since
launch) is the worst LLM value on the list; DGX Spark $4 699 = Strix Halo memory at 2× price.

## 2026-09-02 · Token economy and free/local routing, on request

Two policy notes. `token-economy-playbook`: the knowledge base's measured numbers on where
tokens go, in one ranked list — output tokens first (5× input on every card; one repair
round's output costs more than a build's contract text), untouched files second (77% of a
directed change's input; −51% with a dependency-complete set), prompt caching third (Scio's
constants are under the floor, sent as a string, and ordered last; the ledger would
over-report), Batch fourth, retrieval fifth (graphify 79.6× independent but for code only,
Graft +42% when forced, and a full Scio session that queried the graph zero times), then
every-turn overhead, tier routing with the non-monotonic floor in mind, and counting tokens
before pricing. Platform docs re-read today: Fable 5.1 cache reads are 0.025×, an entry
exists only after the first response begins. `model-routing-free-and-local`: four arms,
what each silently loses (Ollama: no caching, no count_tokens, no tool_choice, no Batch —
MEASURED from its docs), OpenRouter's 20/min and 50-or-1,000/day, and the arithmetic that
closes the product question: one build is 29–79 relay calls, so a free tier cannot carry a
customer path. A jobs × arm matrix and seven rules for routed runs. Ten neighbours name
both pages back; no rival notes — the model tables stay in the local-LLM and GLM notes.

## 2026-09-02 · The routing brain, in one section

Appended §7 to `model-routing-free-and-local`: the two published forms (FrugalGPT cascade
2023, RouteLLM learned router 2024, abstracts fetched and quoted) and a cold position — in
a builder whose jobs are already typed, the brain is a lookup table on job × posture ×
budget with the pipeline's own gates as the cascade's scorer; a model chooses only at
intake, where the job type is unknown.

## 2026-09-02 · The routing brain for building, not the app

§8 of `model-routing-free-and-local`: three levels — agent `model:` fields (supported;
our `skill-builder` sets none and inherits Fable), the dispatcher's per-run tier table
(supported for Claude tiers, the only place a non-Claude arm belongs), and in-session
provider mixing through a router (unsupported; with a credential active the subscription
is bypassed and every Claude call goes to list price). Corrected twice the same day: `pipeline/metrics.jsonl` exists with 29 wave/job rows and
per-run tokens are captured per build by dispatch.py and record.py; the missing piece is an
aggregation by job class over existing rows, not instrumentation.

## 2026-09-02 · Skill-builder rethink, from the ledgers up

`pipeline/REVIEW-2026-09-02-skill-builder-rethink.md`: a cold position written before reading
the contract, then a new query `pipeline/queries/job_class_cost.py` over all five builds'
cost ledgers by job class (readers 38% of the clean build's dispatched minutes across 16 runs;
arms 61% of its tokens; coordinator 72 of 79 minutes), then the shape: three fat coordinator
turns and two fan-outs — probes at T0, all fields authored in one turn from the failure list,
no per-field readers (code checker in a loop, then the whole-artefact review and the
description reader), review ∥ arms and calibration ∥ graders with preregistered revert rules,
triggers on Sonnet, coordinator on Fable. Derived floor 19 dispatched minutes and 35–40 total
against 79, unmeasured. The one different idea: a `candidate` status so the artefact lands in
ten minutes and the measurement runs detached and promotes it. Preregistered numbers for the
first v3 build. Nothing in the agent, contract or dispatcher was changed.

## 2026-09-02 · Sixth batch: eight clips, three byte-identical duplicates, two re-cuts

Duplicates skipped by md5 (self-healing, agentic OS, four plugins). Re-cuts already graded
(Prime Agent 30→95: see `harness-over-model-prime-agent`; agentic-OS four parts: see
`claude-code-extension-layer`). New: **Unlimited OCR** (Baidu, 2026-06-22, 3B MoE / 500M
active, R-SWA with a constant m+n KV queue, OmniDocBench 93.92 reported, MIT; primary card
not fetched — REPEATED) → new note `long-document-ocr`, a candidate to remove the chunking seam
in our `pdf`→`deep-reading` path. **Orbit** (Fraima; hosted shared memory via one MCP command;
ratified facts, provenance receipts, conflict flagging = our `memory-provenance-separation`
as SaaS; no prices, no source, no self-host) → `temporal-kg-agent-memory`. **Agent TARS /
UI-TARS-desktop** (ByteDance, Apache-2.0, 38.8k★, VLM key required; a computer-use agent, not
a skill) → `model-agnostic-agent-harnesses`.

## 2026-09-02 · v3 build mode landed (chain contract 3.0.0)

Same evidence, different order: probes at open, one authoring turn, no per-field readers,
two fan-outs with revert rules audited by `record.fanout_gate()`, coordinator tier recorded
at open, ship reachable and contract-driven (`decide.py` no longer keys on a mode's name).
`full` kept for A/B on the same package. Agent file rewritten to the T0–T4 posture; 94/94
build controls, chain-contract validator 12/12 rules accounted for. Unmeasured until the
first v3 build; `candidate` status parked with its reason in the contract.

## 2026-09-02 · Seventh batch: nine clips, all new

New note `system-prompt-transparency`: Anthropic publishes the claude.ai system prompt for
every model incl. Fable 5.1 (dated 2026-09-01; read in full), so the "270,000-character leak"
is at most the unpublished tool layer, unverified; "blueprint of the model" is wrong. Extended
`agent-builder-prior-art` with mattpocock/skills (MIT, 245k★, 23 skills; "OG at Vercel"
unsupported), google/skills (Apache-2.0, 19.3k★, ~150 vendor-doc skills incl. Ads MCP and
Analytics), shanraisshan/claude-code-best-practice (63k★ curation with a workflow table and a
multi-model section), and **HKUDS/OpenSpace** (MIT, 7.5k★; FIX/DERIVED/CAPTURED; Terminal-Bench
2.1 65.2→78.7 cold→warm) — the closest external analogue to our library-curator loop, with a
CAPTURED rule stricter than our talent-worthiness gate. Ruflo's second video misses on all
three numbers it gives (no 75% in the README, 100+ agents not 60, 70k★ not 14k). Orbit and the
LLM-wiki second-brain clips corroborate existing notes. Not filed: a "$1 → $400,000 Solana
arbitrage student" clip — real Solana arbitrage events exist with other figures, the student
story is an unsourced repost; out of domain.

## 2026-09-02 · Rethink §8: what else moves into code

Per model phase: 1.2, 2.4, 3.5, 4.3, 4.8 are code; 1.1, 3.1, 4.0 code-proposes; 2.2 and
6.2 code for shape; 4.7 a code-driven search around the model; reading verdicts becomes
JSON returns folded by a script; planning becomes a chain runner that calls the model only
at the write points. Derived 25–30 minutes with the same evidence. Build order stated,
measured by the §5 table plus a coordinator-turn column.

## 2026-09-02 · Sixteen carousel slides, four sources

New note **`adversarial-plan-review-claudex`** (chaseai-yt/claudex-loop, MIT, 1.6k★): recon →
interrogate → Codex attacks the plan read-only in the same session, MAX_ROUNDS 5, 26→15→12→2→0
on one real run → rival grades the build. Three design decisions it puts to our skill-builder
(same-session reviewer vs fresh reader; cross-provider grading; convergence-to-zero vs cap 3)
are written up as questions with the cheap test for each. **Switchyard** (NVIDIA-NeMo, Rust,
Apache-2.0, ~2k★; LangChain's 145-task eval: 74% cheaper with 7% escalated to Opus 4.8 — the
slide misattributes the eval to NVIDIA) → `model-agnostic-agent-harnesses`. **Context Mode**
(ELv2, ~20k★), **Token Optimizer** (PolyForm NC, 2.1k★) and **code-review-graph** (MIT, 31k★)
→ `claude-code-ecosystem-plugins`, each number traced to its single example. BASE's "70× tokens /
90× output" added to its section as unsupported; its relay's verify-before-trust line noted.

## 2026-09-02 · Rethink §9: under the floor

Levers below the dispatched floor, each with its ledger evidence: the probe is the
without-arm (8 → 5 arm runs), k from the probe's verdict as the spec's table already says,
fail-fast at T1 on the refuted-package case (4 of 4 refuted), memoized dispatch for
iterate rounds, per-item graders (6.5 → ~2 min), cache warm-up before fan-out, bare
startup, preregistered effort per class, fixture-size ablation, N builds in flight with
W re-measured at 8, a rate-limit queue (196 of 495 dispatched minutes were waiting),
delta authoring for extend builds, kb.py as the scout. Derived 20–25 minutes.

## 2026-09-02 · §9 levers landed in code; fail-fast kept as the existing rule

decide.py: probe rows count for correctness (never cost), k from the probe's outcome as the
spec's table says. dispatch.py: memo keyed on every input byte, effort on command and row,
stagger for cache warm-up, 429 retry with recorded count. Contracts: `runs_paid_twice`
block, `acceptance.repeats_by_probe` and `probe_rows_for_correctness`. Fail-fast at T1
checked against `probe_never_gates` and KEPT out. 22 new controls, all green. Not landed
and said so: bare-startup flags, fixture ablation, W re-measure, delta authoring, §8.

## 2026-09-02 · LLM-wiki ingest skill, kb-curator agent, kb.py lint — and the curator's first pass

Two talents and one command, from Karpathy's LLM Wiki pattern and three implementations read
today (llm-wiki-pattern note extended with the comparison). `llm-wiki-ingest`: the seven-step
ingest every source goes through (raw kept, triage new/update/disputed/no-material, quote
before write, schema, cascade with a sentence, register, lint). `kb-curator` (agent): lint
first, safe tier only, judgement findings as data, merges and deletions as proposals.
`kb.py lint [--json]`: schema, dangling, one-way, orphan, unlisted-in-INDEX, stale, related-only,
shared-source pairs; exit 1 on errors. First pass by hand: 9 errors → 0 (6 dangling links
retargeted or made text; two compiled/video notes given a sources block); 17 notes added to
INDEX §0d with their own titles; 33 one-way links left for the curator's judgement tier
with the reason (a back-edge without a sentence is the defect, not the fix). Both talents
are **candidate**: eval suites authored (6 scenarios each, blend + negative trigger), the
baseline-vs-with run not yet done.

## 2026-09-03 · First v3 build: llm-wiki-ingest → ITERATE (tokens 1.23x vs 1.20x; every quality clause passed)

Full chain, three arms, k=2, code grader, blinded, preregistered rule, coordinator Fable 5.1.
26.9 active minutes open-to-decide around an overnight session suspension (raw span 8 h 21 min,
corrected in the record); 44 dispatched runs, 18.5M tokens; 2 reader runs; the whole-artefact
review was red at class level (4 findings), the skill was rewritten once and the with-arms
re-run per the fan-out rule. The skill fixes the one observed baseline failure (no material →
page untouched, log and source-log rows) with no regression where the baseline is clean; it
costs 1.23x tokens. Field trial on a copy of this knowledge base: correct update triage, a
manifest for the raw, and it caught two README quotes this KB attributed to the SKILL.md
(fixed in llm-wiki-pattern). Three harness defects found and fixed (write permission,
transient rerun failures, threshold phrasing). Extend gate CLEAR (fixed 1, regressed 0).
Trigger matrix PASS (11/12, 0/4, 4/4). Status stays candidate; next: the token iteration.

## 2026-09-03 · llm-wiki-ingest SHIPPED after three iterate rounds (tokens 1.17x, tools 1.13x, no regression, T3 win)

Rounds: 1.23x → 1.41x → 1.40x → 1.17x. The cost was the method's work, not the reading of
the skill; the text that ships says exactly what to do and where, and the with-arm stopped
improvising. Reviews red at class level three times with real findings each time; the
convergence cap stopped a fourth, so the shipped text is marked unconverged-at-review in the
record. Deployed: CLAUDE.md marker, talents.jsonl adopted row, evals.md verdict. Build
totals from the ledger: 65 dispatched rows (11 void), 28.7M tokens, three rewrite-and-rerun rounds.
Next for the curator: a whole-artefact read of the shipped text; for the builder: the
reviewer's non-convergence is the first thing to study before a second package.

## 2026-09-03 · Second v3 build: artifact-consistency-sweep → ABANDON at the loop cap (recall up, full bar not cleared)

Baseline recall 0.29–0.67 against the union of three independent reviews per fixture; with
the skill 0.64–1.00, CLASS recall 1.0 on T1 in every run, tokens 1.12x. Not shipped: no test
cleared every grader check on both repeats (ledger, precision proxy, CLASS bar on one repeat
each), tool calls 1.21x against 1.20x, three reviews red at class level, loop cap reached.
Two harness defects cost the build: the grader-code exclusion was applied late (corrected in
the record) and the arm prompt's fixed output shape overrode the skill's step 6 so the ledger
check could not pass. Trigger matrix PASS 12/13, 0/4, 4/4. Field trial on skill-measure:
a complete 24/24 ledger, 7 findings, and four gaps the run named itself. The artefact stays a
candidate, not routed. Across both builds 5 of 6 whole-artefact reviews were red at class
level: the fan-out's revert-to-serial condition is met.


## 2026-09-04 · Ingest: a forwarded graphify → Obsidian carousel, checked against the source

Disposition **update** (no new page; three notes and `knowledge/VAULT.md` extended, no rival
created). Source: an Instagram carousel by @divyannshisharma, 16 of 20 slides received as
screenshots, plus `README.md` fetched from graphify branches `v8` and `main` (2026-09-04). Raw
kept at `knowledge/raw/instagram-graphify-obsidian-2026-09-04/` (frame text + both READMEs;
images not stored, md5 per frame recorded), MANIFEST and SOURCES rows added.

What it yielded. **The `--obsidian` correction chain is closed** on its third pass: graphify
has two command surfaces and each flag belongs to one — `/graphify … --obsidian` is a skill
flag (documented, v8 l.678), `graphify export obsidian` is the CLI subcommand (measured here
2026-09-02), `extract --obsidian` is neither. Two of that chain's three errors were surface or
branch errors, not feature errors. **A branch trap worth knowing:** the default branch serves a
v1-era 7 KB README with no exports, no MCP and no Obsidian mode; this repository's feature page
is written against v8's 62 KB one. **A keep:** the carousel independently arrives at the vault
policy already in place here — build the generated vault separately, then move it in as one
deletable folder — so the policy stands with its reason now written down. **A correction to the
source, not from it:** the carousel's "bare notes" complaint matches our own 2026-09-02
measurement exactly, but its numbers are REPEATED and one of its screenshots (1,252 nodes) is
the creator's own vault, not the graphify build; the ingest says so rather than absorbing it.

Lint 0 errors before the commit; `kb.py build` 586 documents.

### 2026-09-04 · The vault's on-demand command, run rather than quoted

`knowledge/VAULT.md` carried an `export obsidian` command written 2026-09-02 and never
executed. Run today against the 5,173-node as-built graph: graphify 0.9.53 installs in 2.1 s,
the export takes 2.4 s and 0 LLM tokens, and produces 5,401 notes (5,173 node + 228 community)
plus `graph.canvas`, 24 MB, gitignored. Node notes median 42 words, 4,815 of 5,173 under 100 —
the bare-stub shape reproduced on our own artefact instead of a screenshot. Of 380 distinct
`source_file` paths, 377 resolve in the hello-world repository and **1 in skills-repo where the
vault sits**, which turns "regenerate it beside the source" from an argument into a
measurement. Not measured: rendering in the Obsidian desktop app.

### 2026-09-04 · Reconciliation: the talent that runs graphify, against the verified surface

The correction landed in the knowledge base first; the talent that actually issues the commands
had not been read against it. Four claims reconciled: `third-party-landscape`'s lesson said
"`graphify --obsidian` is ignored", which the v8 README makes false (it is a skill flag);
`graphify-harvest/SKILL.md` was right but incomplete, so a future curator would have flipped it
back — it now says why the flag looks valid in the docs and dies on `extract`;
`graphify-harvest/evals.md`'s "non-existent flag" got a dated correction appended rather than a
rewrite; `CURATION-LESSONS` gained the sharpened three-question check (feature · syntax ·
surface-and-branch). Frozen records left alone: the 2026-08-27 STATUS rows and the
`pipeline/builds/**/runs/` artefacts are history, not claims.

**And a new defect found by running it.** `graphify export wiki --dir X` accepts `--dir`,
returns no error, ignores it, and writes `wiki/` (238 articles) beside the file `--graph` points
at — which here is the immutable `intake/` import, untracked but **not** gitignored, one
`git add -A` from a commit. Removed, `intake/` verified clean. Third instance of the
accepted-then-silently-ignored flag class and the first with a blast radius; `export obsidian`
does honour `--dir`, so the two exports are not symmetrical. Recorded in the talent, the feature
note, VAULT.md and the lessons file.

### 2026-09-04 · KB tidy pass 1: the graphify/obsidian material made to agree with itself

Three values contradicted across pages, all settled against primary source and all **dated**
rather than deleted, because two of the three were right when they were written:
**licence** — the notes said both MIT and Apache-2.0; `LICENSE` on v3/v4/v6/v7 is MIT, on v8 is
Apache, and PyPI 0.9.53 metadata says Apache-2.0, so the licence *changed* under the note;
**canonical repository** — the feature page had the mirror relationship backwards, PyPI's
Homepage and Repository both point at `Graphify-Labs`; **version** — 0.9.50 in the header
against 0.9.53 measured on the installed binary and on PyPI. Frontmatter `sources` on both
graphify pages now carry the 2026-09-04 fetches, `VAULT.md`'s fetch date follows its new
measurement, and `INDEX.md` gained a 0e section listing what this source settled and where, in
the 0d convention. Lint 0 errors; the shared-source pair count rose 18 → 19 because the two
graphify pages now cite the same re-fetch, which is the curator's signal working as intended.

### 2026-09-04 · KB tidy pass 2: the curator's report, acted on

The kb-curator's deterministic tier closed 29 of 30 one-way links by editing the neighbour
with a real sentence (verified before commit: the related-only info counts did not move, so no
warning was traded for an unargued edge). Its judgement findings, worked here:

**Contradiction settled at the source.** Two notes said the Anthropic skills guide is 33 pp,
one said 30 pp, same URL, one day apart. Fresh download 2026-09-04: **33 pages** (pypdf, and 33
`/Type /Page` objects in the raw file). The obvious excuse — three blank pages a text
extractor would drop — was tested and refuted: all 33 carry extractable text. The file's own
`ModDate` is 2026-01-26, months before either read, so it did not change under us. 30 was
simply wrong, and is corrected in place with the reason.

**Two claims their own paragraph had already outlived** (`llm-wiki-pattern`): the video
transcripts do not "live in a scratch directory that will not survive the session" — they are
committed; and "contradictions and stale claims are not checked by anything" — stale is
checked by `kb.py stale` and the 90-day rule, so only contradictions are unchecked.

**The source log's own claim was false.** It said "every source consulted"; measured, the
notes' frontmatter carries 130 distinct source URLs and 112 are named nowhere in it. Not
backfilled: 112 rows needing Type/Status/Feeds-into is authoring, and it would create a second
register to keep in sync. The file now says what it is — the hand-written batch record — and
points at the register that cannot drift, `kb.py sql "SELECT note, url, fetched FROM source"`
(146 rows, command verified before it was written down).

**Two wording defects** in `anthropic-skill-authoring-contract`: a heading counting three
numbers over a four-row table (three numbers, four sources — said so), and a cell claiming
"stated four times" while naming three sources, against `skill-anatomy`'s three.

Lint: 0 errors, 0 warnings, 43 info, 19 shared-source pairs. **Not done, and recommended
next:** re-fetch the six Claude Code mechanics notes (`skill-anatomy`, `subagents`, `mcp`,
`hooks`, `plugins-and-marketplaces`, `claude-code-extension-layer`), all fetched 2026-08-27 and
all carrying version-tied values. None is stale by the 90-day rule; the licence that changed
under a note this week is the argument for going early.

### 2026-09-04 · The Claude Code mechanics set, re-fetched — nothing rotted, four things were missing

The curator's last open recommendation, run. All eight `code.claude.com` pages behind the six
mechanics notes re-fetched and kept as raw (900 KB; the `.md` twin of each page is ~a tenth of
the HTML). Two checks: every version-tied value in the notes read against the fresh text, and a
deterministic sweep of every identifier the notes name (env vars, settings keys, commands)
against it.

**Result: no rot.** 15,000-token description budget, depth 3, 20 concurrent, 5,000/25,000 at
compaction, `/subtask` v2.1.212+, MCP v2 runtime on v2.1.232+ — all still stated. Every
identifier resolves; the one apparent miss (`skill.md` in `skill-anatomy`) was the checker's
false positive, since the note names it as a *rejected* filename.

**But one claim inverted and four details were missing**, all in `subagents`: "total subagents
over a session's lifetime" was on that note's *explicitly NOT documented* list, and the page now
states there is no limit — a documented absence, which is not the same thing. Added: ultracode
sessions are exempt from the concurrency limit; the depth default has a version history
(five layers unchangeable through v2.1.216, one on v2.1.217–218, three from v2.1.219); a fork
at the depth limit keeps `Agent` and gets an error where a subagent has the tool withheld; and
`/subtask` was `/fork` on v2.1.161–v2.1.211 and is unavailable with agent view off.

The honest lesson for the stale rule: eight days bought no wrong values, and it bought four
additions and one inverted claim. Freshness of a *value* and completeness of a *page* are
different things, and only the first is what `kb.py stale` measures.

### 2026-09-04 · `kb.py contradictions` — the lint's missing third, written and tested

All three value conflicts settled today (licence, version, page count) were found by hand or by
an agent reading pairs. `llm-wiki-pattern` had named this check as the outstanding follow-up
since 2026-09-02. Written now, in the house style, no model call.

**What it does.** Compares TYPED values — licence, version, pages, tokens, words, lines, price —
stated about a SHARED subject. A note pair qualifies by citing the same source URL (the pairs the
lint already emits); the subject anchors are the tags they share plus that URL's path words, and
both sentences must name the SAME anchor.

**Three quieting rules, each earned by a false positive it produced first** (the first pass
returned 9 hits, all false):
- A stated LIMIT is never compared with a MEASURED value — judged on the words *around the
  number*, not the sentence, because reading the sentence made "the licence changed **under**
  this note" a cap.
- An anchor equal to the value's own unit is circular and dropped: "tokens" beside a token count
  is not a subject, and it was dragging every number in a frontmatter block together.
- A note naming BOTH values is a dated range ("MIT through v7, Apache-2.0 from v8"), not a
  conflict.

Also: markdown table rows and whole `- url:` frontmatter blocks are read as single units, because
a source's page count sits on its `note:` line while the document it names sits on the `url:`
line above, and split apart neither anchors the other. That fix is what made the 33-vs-30 case
catchable at all.

**Tested, in `kb.py selftest`:** a planted licence conflict must be caught; a dated range must
not be flagged; a limit-vs-measured pair must not be flagged. All three pass. Over the corrected
knowledge base the check reports **0**; over a copy with the page count put back to 30 it reports
the pair, deduplicated to one row per note pair rather than one per matching anchor.

**Honest limit.** It reads values, not prose. A contradiction carried in wording rather than in a
typed value is invisible to it, and a note that states both sides of a range is silent by design —
which is correct, and also means two of today's three conflicts would no longer fire now that
they carry their ranges.

### 2026-09-04 · The data contract, honoured late — and the new check wired into the procedures

Two debts from the day, both paid.

**The telemetry the contract requires was not written when the pass ran.** `DATA.md` says a
curation pass ticks `metrics.jsonl` and the proposal ledger, live, because wall-clock and lineage
cannot be reconstructed later. The KB curation pass ran hours ago with no row. Written now from
the run's own numbers: `wall_clock_s: 791` and `agents: 1` MEASURED, `tokens_est: 204885` marked
honestly as the harness-reported **subagent** total that EXCLUDES the coordinator and therefore
understates the pass, `spend_measured: null` because there is still no metered path. Five rows in
`ledgers/proposals.jsonl` — the curator's five judgement findings with what was actually decided,
`decided_by` the coordinator, and the note that the SOURCES.md demote-instead-of-backfill call is
reversible and was surfaced to the user. Late is worse than live: the numbers survived only
because the task notification still carried them.

**And `kb.py contradictions` is now called by the procedures that should call it.** A check
nobody's runbook runs is a check that never runs. `kb-curator` step 1 now runs it straight after
the lint, with the honest framing that a hit is a candidate and a **silence is not a clearance**
— it reads values, not prose, so the shared-source pairs still go through the agent's own step 4.
`llm-wiki-ingest` step 7 names it too, as the feed for its `disputed` branch.

Final state of the day: lint 0 errors, 0 warnings; contradictions 0; selftest PASS on all three
new fixtures.

### 2026-09-04 · BRAIN.md updated — and it had not been told the knowledge base exists

The standing rule is that both loops read `BRAIN.md` at the start of a run and update it at the
end. Today's session did neither until now, and reading it exposed something bigger than the
missed update: **the control tower models two loops, and there are three.** The knowledge base —
`knowledge/notes/`, the raw layer, `kb.py`, the `kb-curator` agent, `llm-wiki-ingest` — has had
its own lint, its own curator and its own failure modes since 2026-09-02, and none of it was
written in the file that is supposed to stop the loops colliding. Now it is, with ownership
stated: kb-curator owns link and schema repair in the notes, the coordinator owns INDEX, VAULT
and the source log, and nobody edits `raw/`.

Its stale STATE line is left standing and **labelled** rather than rewritten: it was written
2026-08-28 and is not a report on the week since. Overwriting it with today's would have made
the file look current while quietly losing the fact that a week of sessions never updated it.

Two links written both ways. KB → build: verify the SURFACE and the doc BRANCH, not just the
syntax; and a silently-ignored flag is a write somewhere you did not choose. Build → KB:
`kb.py contradictions` was built the way a talent is, each quieting rule earned by a false
positive it produced first.

Two OPTIMIZE directives, both from today's own misses: write telemetry in the turn the pass
ends (this one survived only because the completion notification still carried the numbers), and
a check nobody's runbook runs is a check that never runs.

### 2026-09-04 · The KB's ROUTINES reviewed (not its content) — three findings, two decisions open

Full review at `pipeline/KB-ROUTINES-REVIEW-2026-09-04.md`.

**1. Every routine is a convention and nothing fires it.** Measured: no CI, no active git hooks,
no cron touching `kb.py`. The lint exits 1 on errors and nothing calls it. `CLAUDE.md` already
names this class as "the weakest defence in this repo"; today produced three fresh instances —
telemetry written hours late, `BRAIN.md` a week past its own contract, the base unlinted between
sessions.

**2. A note and its raw share no join key — found by failing to measure it.** Three defensible
methods for raw coverage returned 11%, 61% and 0%. The spread IS the finding: frontmatter carries
`url` and `fetched` but never the raw path, so the "keep the raw" rule cannot be checked, the raw
cannot be found from the note, and no coverage claim can be defended. This morning's own lesson,
written about someone else's export, applies to us: a page whose source cannot be opened from the
page is a stub with a footnote.

**3. The freshness clock is the wrong clock.** 0 notes past the 90-day bar and 35 of 44
un-refetched in three days, so `stale` says nothing for three months — while eight days produced
one inverted claim and four missing details with no value changing. A release invalidates a note;
the calendar cannot see one.

Nothing was changed in the base by this review. Two decisions put to the user: how routines get
fired (CI vs the convention, against the repo's security gate on auto-run hooks), and what the
freshness signal should be. A third, cheap and uncontroversial, waits on the first: fold
build/lint/contradictions/selftest into one `kb.py check` with one exit code.

### 2026-09-04 · Both decisions from the routines review, built

**The trigger exists now.** `.github/workflows/kb-check.yml` runs `kb.py check` on every push and
PR touching `knowledge/`. Deliberately CI and not a git hook: the fourth gate is explicit about
auto-run hooks, and a hook binds only the machine it is installed on. The job needs no
dependencies — `kb.py` is standard library only — so it has no lockfile, no cache and no network.

**`kb.py check` is the routine as ONE command**: build → lint → contradictions → selftest, one
exit code. A routine you have to remember in four parts is four chances to skip one, and today I
skipped `contradictions` after edits until I remembered it existed. `llm-wiki-ingest` step 7,
`kb-curator` and `ROUTING.md` now name it instead of the parts.

**Proved it can fail, twice.** A gate that cannot fail is theatre: on a copy, a planted dangling
link exits 1, and a deleted `raw:` key exits 1. Both print FAIL.

**The raw join key exists now**, and Finding 2 is measurable instead of unmeasurable. Every
verified note citing a source carries a `raw:` key: 12 name a real path under `knowledge/raw/`,
31 say `none - fetched before the raw layer existed (2026-09-02)`. The lint requires the key to
be PRESENT, not non-empty — an honest "none" is a valid answer and a silent absence is not — and
it errors if a named path does not exist. The three-way spread of 11% / 61% / 0% is replaced by
one number a script recomputes: **12 of 43**.

One correction while filling: the first pass counted source ENTRIES, so a note citing the same
URL twice (an original fetch and today's re-fetch) was written up as "partial: 1 of 2". Counting
distinct URLs fixed five notes.

### 2026-09-04b · Finding 3 closed with a different design, and the docs moved twice in one day

The routines review proposed a release clock for freshness. **Measured before building it:** 18
notes cite a watchable source and exactly 2 pin a version to compare against, both the same
package. A version clock would have had no surface, so the proposal was dropped for the more
general signal — **have the bytes we read changed?** — which needs no version, covers any URL,
and uses the raw layer as its baseline, so Finding 3 rests on Finding 2's join key.

`knowledge/watch.py` + `knowledge/raw/WATCH.tsv` (raw path · url · fetched · sha256). Deliberately
NOT part of `kb.py check`: that runs offline in CI on every push and must stay network-free.

**Its first run found 5 of 10 changed, hours after the morning fetch.** Checked before believed —
the diffs are real content, not a nondeterministic header. Material, and now in the notes:
nested `.claude/skills/` do NOT load at startup (they load when Claude first reads or edits a file
in that subdirectory; `/add-dir` loads them early, v2.1.257+); **`/skill-doctor`** reports what each
skill costs in context and how often it is used, and flags never-invoked skills; a file form of the
subagent system-prompt flag at **v2.1.261**, twenty-nine releases above the highest version this
base cites; removing a remote MCP server also deletes its stored OAuth tokens. The fifth was a
Discord invite link, material to nothing — which is the watcher's honest shape: it detects that
bytes moved, never that a claim did.

Two notes on the machinery. The morning's raw is NOT overwritten: the changed pages got a second
dated directory (`claude-code-docs-2026-09-04b/`) and the two together are the evidence the docs
moved twice in a day. And the new gate caught its author within minutes: `kb.py check` failed on a
dangling `[[skill-description-optimizer]]` in the very edit that recorded `/skill-doctor` — a
talent is not a page, and the lint knew it before I did.

`/skill-doctor` also lands against a standing rule: it measures "never invoked", and this repo
drops a talent ONLY for failing its tests. Both stay true — the rule is now a deliberate choice
against a measurement rather than the absence of one.

### 2026-09-04b · Watch coverage 10 → 23, and the rule for what is worth watching at all

Backfilled a baseline for the notes that had no raw copy. Three things worth keeping from it.

**A principle, not a chore: watch what can move.** Of 127 unwatched source URLs, **33 are on
`doi.org`, `arxiv.org` or `usenix.org` and are deliberately never watched** — a published paper
does not change under its own identifier, so change detection over it can only ever return "same",
and a wall of green would imply the whole base is watched when it is not. Coverage is now stated
as watched / *watchable*, which is a number that means something.

**A baseline is not provenance, and the directory says so at the top.** These are today's bytes
for pages the notes were written against a week ago — they can tell us from now on that a page
moved, and they can verify nothing that is already written. The citing notes' `raw:` keys still
say no bytes were kept and name the baseline separately, because conflating the two would
manufacture provenance, which is worse than admitting we have none.

**Two of my own bugs, caught by checking rather than by trusting the count.** The first pass
reported 127 unwatched URLs including pages that ARE watched — `WATCH.tsv` holds the `.md` twin
(`…/skills.md`) while the notes cite the HTML URL, so a naive set difference lies. And the glob
that built the new rows swallowed the directory's own `README.md` as if it were a fetched source.
Both were visible only because the watcher was run and its output read: 23 watched, 22 unchanged,
1 unreachable — and the unreachable one was a trailing slash my URL reconstruction had dropped,
not a dead site.

### 2026-09-04b · Watch coverage 23 → 75, and a bug in the watcher found by its own false alarm

**The rule this batch established: watch the form that carries the claim.** A GitHub repo page
changes on every star and every "last commit" timestamp, so 19 repo URLs are watched as their
README; 11 Hugging Face model pages as their model card; 7 blob links as the raw file. Watching
the pages themselves would have built a false-positive machine.

**47 sources are never watched, each with a reason.** 39 immutable (DOI, arXiv, USENIX, PDFs — a
published work does not change under its identifier, so the check can only return "same"), 7
volatile by design (social posts, a leaderboard, gists — bytes change without the claim changing),
1 issue thread whose state, not whose page, is what a note cites.

**Three of my own defects, each caught by running the thing rather than trusting it.**

1. **The watcher read HTTP error pages as content.** `curl -sS` without `-f` exits 0 on a 429 and
   hands back the error body, which the watcher hashed and reported as "the source changed". Two
   rows cried change minutes after their baseline; a clean double-fetch showed both were stable.
   Fixed with `-fL`, and the two now report **unreachable**, which is the truth. A watcher that
   cries change on a rate limit is a watcher nobody reads.
2. **`curl` globs `{}`.** A `url:` field written this morning as a brace shorthand for five branch
   LICENSE files is not a URL — curl expanded it and the fetcher stored v8's file under a
   fabricated address. The note now cites one real URL and says in its own note field what the
   earlier entry did. `-g` added to the watcher so a malformed URL fails instead of fetching
   something else.
3. **Four HTML baselines were byte-unstable** across two fetches seconds apart and were dropped
   from the watch list. Their limit is recorded with them: one double-fetch proves instability and
   never proves stability — one page failed the sweep after its sibling had passed the same test
   minutes earlier.

State: `kb.py check` PASS, `watch.py` 73 unchanged · 0 changed · 2 unreachable · 75 watched.

### 2026-09-04b · The watcher gets the trigger the lint got — and why it lacked one for an afternoon

`kb-watch.yml`, weekly on Mondays, plus manual dispatch. A failing run means a source moved and
the citing notes are owed a re-read; unreachable rows do not fail it, because a rate limit is not
evidence.

Worth recording as a lesson rather than a chore: **this session diagnosed "a check nobody's
runbook runs never runs" in the morning, built CI to cure it, and then recreated the same defect
in the afternoon** by writing `watch.py` and deliberately excluding it from that CI job — for a
good reason (the check job is offline and must stay network-free) that nonetheless left the
watcher a convention. A fix for "nothing runs this" does not generalise to the next thing you
build the same day; each new check needs its trigger named at the moment it is written.

**Honest caveat, in the workflow's own comment and in the review:** GitHub runs `schedule:` only
on the default branch, so this fires nothing until the branch merges. Until then the watcher is
still a convention — and believing otherwise, because a file describing a trigger has been
committed, is precisely the failure this review exists to name.

### 2026-09-04b · The machinery put to work: a false absolute found in the base's weakest note

With the routines built, the base's own honesty markers were used to pick the target: all 44
notes are `status: verified`, but `best-local-llm-2026-09` carried **6 REPEATED against 1
MEASURED**, the weakest ratio in the base — and its sources are Hugging Face model cards that the
afternoon's baseline batch had just stored locally. So the claims were read back against the
cards instead of against memory.

**Found: an absolute that is false.** The note said Nemotron 3.5 Lightning "loses to
Qwen3.6-35B-A3B on **every row** of NVIDIA's own table". Checked row by row: **13 of 14
comparable rows lose, and one wins — IFBench (loose), 71.88 against 63.71.** Corrected in place
with the number and the row. The note's actual argument ("the throughput pick, not the quality
pick") survives; the absolute does not.

**Confirmed, and worth recording because the check nearly went the other way:** `SWE-bench
Verified Qwen3.6-35B-A3B 70.1` is `70.12` in the card AND sits under the column header
`Qwen 3.6 35B A3B` — a number without its header is not evidence, and reading the header is what
turned this from "the figure appears somewhere on the page" into an attribution. Two model
designations I first flagged as absent from the sources are the card's own column headers; my
grep had missed them on hyphenation, so the note was right and the check was wrong.

**The caveat that bounds all of it:** these are the cards as of 2026-09-04, not the bytes the note
was written from. This verifies the claims against the CURRENT cards; it cannot verify what was
read at the time. That distinction is the same one the baseline directory's README makes, and it
is why the baselines were never filed as the notes' `raw:`.

Lesson, recorded because it generalises past this note: an **absolute** is the cheapest claim to
write and the cheapest to refute — a fourteen-row table offers fourteen chances to be wrong.

### 2026-09-04b · The base's oldest named contradiction, settled from primary data

`llm-wiki-pattern` had carried GLM-5.3's **744B-vs-753B** since 2026-09-02 as the example of what
a value-comparing check would catch. Both halves are now closed: the check exists and is tested,
and the pair itself is resolved — not by re-reading either page's prose, but from the weights'
own `config.json`.

**It was never a contradiction.** An independent count from the shipped configuration (78 layers,
3 dense, 257 experts of 3×6144×2048, 64 heads at head_dim 192, untied 154,880-vocab embeddings)
lands at **≈754 B**: one billion from the 753 B figure and ten from the vendor's `744B-A40B`
label. The economical reading is a **rounded product label against a weight count**, which is
exactly why neither source was ever going to correct the other, and why a contradiction checker
can only ever hand such a pair to a human.

**Two honest limits, both recorded in the note.** The current HF card states no parameter count
at all, so the claim "the HF card says 753B" cannot be checked — the bytes that would settle
whether the card dropped it or the note misattributed it were never kept, because the note
predates the raw layer. This base demonstrated its own documented failure mode on itself. And a
rough active-parameter derivation lands near **50 B** against the label's **A40B**; that gap is
recorded as open, because a derivation that reproduces one number and not its sibling has not
earned the second.

### 2026-09-04b · goose verified against its README — and the same ownership move, twice in one day

Continued the verification pass on the note with the most unconfirmed claims
(`model-agnostic-agent-harnesses`, 9 REPEATED). Two claims upgraded to MEASURED against the
README stored this afternoon: **"70+ extensions"** is verbatim, and so is **"goose is part of the
Agentic AI Foundation (AAIF) at the Linux Foundation"**. The *December 2025* contribution date is
not in the README and stays REPEATED.

**Worth more than either: the repository moved and the note cites the old path.** Every GitHub
link inside goose's own README points at `github.com/aaif-goose/goose`; the note's source is
`github.com/block/goose`. Measured: both paths serve a **byte-identical README** — same sha256,
same 3,449 bytes — because GitHub follows a repository transfer. The citation resolves and is no
longer the home.

That is the **second instance in one day**, after graphify's `safishamsi` → `Graphify-Labs`, so it
is recorded in both notes as a pattern rather than a coincidence: **a project that changes hands
keeps its old URL working, which is exactly why the citation goes stale silently.** Nothing
breaks, no fetch fails, and no freshness check can see it — the watcher compares bytes, and the
bytes are identical by design.

Two of my three suspicions dissolved on a closer read: the note already quoted the AAIF sentence
correctly, and already had the Apache-2.0 licence as MEASURED. Recorded because a verification
pass that only reports its hits is not a verification pass.

### 2026-09-04b · `kb.py owners` — closing the blind spot the byte-watcher cannot see

Yesterday's pattern, made checkable the same day it was named. An ownership move keeps the old URL
alive: GitHub follows the transfer and serves **byte-identical** content, so no fetch fails, no
hash changes, and `watch.py` is structurally blind to it. Two instances turned up by hand within
hours of each other, which is what made it worth automating.

**The signal needs no API.** The session's GitHub API access is scoped to its own repositories and
returns 403 for third-party ones — checked, not assumed. But a project's own README names its
home: badges, CI links and install lines start pointing at the new org. `kb.py owners` reads the
READMEs already in the raw layer and reports where those self-links disagree with the owner we
cite. Offline, no network, so it belongs in `kb.py check`, which it now runs as a report (exit 0 —
a hit is a candidate for a human, like a contradiction row, not a defect).

**It found both known cases, and corrected one of my own claims from this morning.** `block/goose`
→ its README names `aaif-goose/goose` in **4 of 4** self-links. And `Graphify-Labs/graphify` → its
README names `safishamsi/graphify` in **1 of 1** — the opposite direction to the line I wrote this
morning, which called Graphify-Labs canonical on the strength of PyPI metadata alone. The note now
says the two homes disagree, that either resolves, and that **which one is the home is not settled
by the evidence we hold.** That is a smaller claim than the one it replaces, and it is the one the
evidence supports.

The strength of a hit is in the ratio: 4-of-4 self-links is evidence of a move, 1-of-1 is a
mention. The check prints both numbers rather than a verdict.

### 2026-09-04b · The verification queue: three notes done, the method written down, the bound stated

Three notes read back against sources actually held, and every one returned something: a false
absolute in the base's weakest note, its oldest named contradiction settled from primary data, and
an ownership move that became a check. The method is now in the routines review — read the claim
against the raw rather than memory, read the column header before trusting a number, and test
every absolute, because one counterexample ends it.

**The bound, measured: 55 REPEATED claims remain, and at least 8 are permanently unverifiable** —
sourced to a search result, a video, a review or a press mention, none retrievable then or now.
`temporal-kg-agent-memory` was opened and closed unverified on exactly that ground: its
unconfirmed claims belong to a product whose sources we never held. **Not checkable is a result.**
Manufacturing a check for it would be worse than leaving the verdict where it stands.

The remaining tail is `kb-curator`'s, one note at a time, ordered by most-REPEATED-first and only
where a source is held. That ordering is written down so the next pass does not have to rediscover
it.

### 2026-09-04b · REPEATED was doing two jobs — the queue's own ordering rule was wrong on first use

Following yesterday's ordering rule (most REPEATED first, only where a source is held) put
`subagents` at the top with three claims. **None of them was a reading job.** All three are our own
paired measurements at n=3, marked REPEATED to mean "small sample, treat with care".

`pipeline/contracts/claims.contract.json` settles it: the verdicts record **provenance, not
confidence** — MEASURED is "the source reports a number it measured itself", REPEATED is "the
source restates a finding measured by someone else", and the contract says outright that the two
"are not strong and weak". Three verdicts corrected in `subagents`; the uncertainty now lives where
it belongs, in the stated **n**.

**Measured across the base: of 55 REPEATED claims, 18 are the provenance sense, 4 the confidence
sense, and 33 cannot be told apart from the line alone.** So a queue ranked on the raw count ranks
on a mixture of two things and sends the reader after work that does not exist. The rule in the
routines review is corrected to the provenance sense only.

One more note on method: the "is a source held" column read zero for every note until `WATCH.tsv`'s
URL-to-path map was used as the authority. **Three separate crude string-matches lied about held
sources today** (11/61/0% coverage, the unwatched-URL count, and this) before each was replaced by
the real mapping. A join key exists precisely so that guessing is not necessary; every time it was
skipped, the number was wrong.

### 2026-09-04b · The verdict misuse made checkable, and the fourth case closed

All four confidence-sense uses of REPEATED are now corrected (`subagents` ×3,
`testing-skills-methodology` ×1), and the class has a check rather than a paragraph.

**The rule is contract-grounded, not a heuristic about wording.** REPEATED means "the source
restates a finding measured by someone else", so a REPEATED line that gives a sample size ought to
name whose finding it restates. The lint flags a REPEATED line carrying `n=`, batches, occurrences,
runs or trials with **no attribution word** anywhere on it — which is exactly what a first-person
measurement wearing a provenance label looks like, and which spares a source's own sample ("the
paper reports n=400").

**Tested, permanently, and the test is why the predicate exists as a function.** A file-level plant
proved inconclusive: my own correction text contains the word "source", so the exemption fired and
suppressed the plant. Rather than fight the fixture, the predicate was lifted out of the lint and
is now exercised by `kb.py selftest` on four strings — two of our own measurements that must flag,
two source-attributed lines that must not. All four pass, and the rule and its test run the same
code.

Base state: lint 0 errors, 0 warnings.

### 2026-09-04b · The day's method lessons moved to where they are read

`STATUS.md` is a chronological log; nobody opens it at the start of a run. `CURATION-LESSONS.md`
is read by the curator before every pass. *(Those five lessons are operating lessons and stayed in
`CURATION-LESSONS.md` when it was split on 2026-09-12; the test-authoring directives moved to
`pipeline/TEST-AUTHORING-LESSONS.md`.)* Five lessons from today were written there, each one
naming the concrete error it cost:

1. **A number without its column header is not evidence** — `70.12` was found in seconds in a
   six-column table; only the header row made it an attribution.
2. **Test every absolute** — "loses on every row" was 13 of 14; one counterexample ends it.
3. **A verdict records provenance, not confidence** — four REPEATED claims that were our own
   measurements, and a queue that ranked on the mixture.
4. **A join key exists so guessing is unnecessary** — three crude string-matches lied in one day
   (11/61/0% coverage, a bad unwatched-URL count, an all-zero "is it held" column).
5. **An ownership move keeps the old URL alive** — two projects moved under their notes with
   byte-identical content, invisible to a content-watcher by construction.

Deliberately NOT added: the `curl -f` and `curl -g` findings, which are tooling detail and live
where the tool does. A file read at the start of every run earns its lines or costs everyone
tokens forever — four checks were built today, and adding a fifth was the wrong reflex; writing
down what the four taught was the right one.

### 2026-09-04b · The corrected queue's first target: everything held up

`loop-engineering-and-fable-prompting`, top of the queue under the corrected rule (provenance
sense, source held). Both Anthropic pages are baselined, so its claims were re-read rather than
trusted.

**All five quotes the note calls verbatim are verbatim** — whitespace-normalised against the
stored bytes: the progress-grounding instruction, the effort default, the two unrequested-action
examples, the give-the-reason template, and "nearly eliminated fabricated status reports". The
moving values hold too: June 9 2026, $10/$50 per MTok, 1M context, 128K max output, and the
overview still calls Fable 5 legacy against 5.1 current.

**A negative result worth as much as the positives: the REPEATED verdict on the nine rules is
correct and stays.** Upgrading it was tempting — a primary Anthropic page is now held — but that
page is about longer turns, effort levels and grounded progress claims, while the nine rules are
Karpathy's loop-engineering list and appear nowhere in it. **Holding a primary source for one half
of a note is not evidence for the other half.** The queue ranks notes; verdicts belong to claims,
and the gap between those two is where a verification pass can talk itself into an upgrade it has
not earned.

### 2026-09-04b · End-of-day verification, and the watcher earning its place on the day's own claim

**Every number claimed today was recomputed rather than restated.** 75 watched sources: 75. Notes
carrying a real raw path: 12 of the 43 that carry the key. Both CI workflows point at files that
exist. `kb.py check` PASS with all six fixtures green. Tree clean, nothing unpushed.

**Then the watcher found three changes — and one of them is the day's own opening claim.**
`graphify` on PyPI read **0.9.53 in the morning** (installed binary and API agreeing), **0.9.55**
in the afternoon baseline, and **0.9.56** in the evening run. Three releases in one day. Both
graphify notes now carry the evening figure with the whole sequence, because the lesson is larger
than the number: **a version in a note is a reading, not a fact about the project** — carry the
timestamp or do not carry the number. No calendar-based staleness rule could have caught this;
`kb.py stale` would stay silent on it for ninety days.

**A watch-list rule fell out of it:** the rendered `pypi.org/project/graphifyy/` page was dropped
and the **JSON API kept**. Same fact, and the page adds download counters that move without the
version moving. Watch the API, not the rendering — the same rule that made a repo's README the
watched form rather than its star-counting page. 75 → 74 sources, and the one dropped was the
noisy twin of one we keep.

**Third change, and it is movement on a verdict:** `codebase-memory-mcp`'s README now says its
Codex install "keeps only a tiny managed activation pointer" instead of a full managed block in
`AGENTS.md`. That is less written into a file the user owns than the SANDBOX verdict was written
against. It does not overturn the verdict — daemon, config writes and quarantine-stripping
installer are untouched — but it is recorded rather than left for the next reader to rediscover.

### 2026-09-04b · Re-measuring today's own finding on today's third release — and nearly reporting a version I never ran

The version drift raised a fair question about the day's own measurements: `export wiki` ignoring
`--dir` was measured on **0.9.53**, and PyPI is now on **0.9.56**. A measurement carries the
version it was made on, so it was re-run.

**Result: unchanged on 0.9.56.** `export wiki --dir X` still writes beside the graph, and
`export obsidian --dir` still honours it. The talent's warning and the feature note now say
"measured 0.9.53 and re-measured on 0.9.56", which is a stronger claim than either alone.

**The near-miss is the part worth keeping.** The first attempt ran `uv tool install graphifyy`,
which reported success and left the **already-installed 0.9.53 in place** — `uv` does not upgrade
an existing tool on `install`. `graphify --version` said 0.9.53 while the terminal above it said
"Installed 2 executables", and one line of output away was a report that the finding "still holds
on 0.9.56" about a binary that was never run. `uv tool upgrade` was the actual command.

The general form, and it is the day's own lesson pointed at itself: **a success message is not a
state check.** The install succeeded; the upgrade never happened. Read the version, not the exit
code — the same discipline as reading the column header rather than finding the number.

### 2026-09-04b · The watcher was manufacturing its own "unreachable" rows

Runs reported one to three sources unreachable. Every one of them answered **HTTP 200** when
fetched individually seconds later: a run of ~75 fetches hits a handful of hosts and
**rate-limits itself**. That is worse than a missing check, because a reader who learns to
discount "unreachable" will discount the real dead citation when it appears.

Fixed with a 0.35 s pause between fetches — about 25 seconds added to a weekly job. A clean run
now reports **74 unchanged · 0 changed · 0 unreachable · 74 watched**.

Two of my own bugs surfaced diagnosing it and are worth the same honesty as the finding: a shell
extraction that fed three lines to `curl` as one URL, and a `grep -l` with an empty pattern that
duly "found" the citation in all 44 notes. Both were visible only because the outputs were read
rather than skimmed — the same reason the rate-limiting was found at all.

### 2026-09-04b · PR optimisation: the objection I raised was 4.7x too large

Before cutting anything, the cost was measured. **Git packs the raw baselines from 9.1 MB on disk
to 1.93 MB (21%)** — so the "8.9 MB" objection stated in chat was the working-tree number and
overstated what the repository actually pays by 4.7x. Measure before optimising, including when
the thing being measured is your own complaint.

**What was actually optimised.** First, CI was verified rather than assumed: both workflows parse
as YAML with the right triggers, `kb.py` and `watch.py` import **standard library only**
(hashlib, pathlib, re, signal, sqlite3, subprocess, sys, time), and `kb.py check` PASSES in a
**clean shallow clone** with no `kb.db` and no artifacts. A red check on the PR would cost more
than any megabyte.

**Then dead weight, and only dead weight: five baselines, 0.8 MB, cited by nothing and watched by
nothing.** The four that returned different bytes on two fetches seconds apart, plus the rendered
PyPI page dropped in favour of its JSON API. A baseline that is not watched performs no change
detection, and a baseline is never provenance, so these carried neither job. The removal is
documented in the directory's own README rather than left as a silent diff — the raw layer's
no-deletion rule protects sources the wiki cites, and these were cited by nothing within hours of
being fetched.

### 2026-09-04b · "Unreachable" now means the source, not us

The 0.35 s pause was not enough: about 30 watched rows are `raw.githubusercontent.com`, so a
single pass still hammers a handful of hosts, and repeated runs made it worse — one reported
**9 unreachable**, every one of which answered 200 individually. Fixed properly with **one retry
after a 3 s pause** before a row is called unreachable. A clean run now reports **74 unchanged ·
0 changed · 0 unreachable · 74 watched**.

This is the second fix to the same signal in one evening, and the reason it was worth doing twice
is the failure mode it prevents: a watcher that cries unreachable teaches the reader to discount
the row that is finally real. The check's value is entirely in its rows being believable.

Also handled: `ruvnet/claude-flow`'s README gained a 14-chapter documentation guide. Read, judged
immaterial to any claim we hold, baseline advanced. Recorded because a changed row that is not
acted on and not explained is indistinguishable from one that was missed.
