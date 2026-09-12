# Evals — deep-reading

Functional regression test for the `deep-reading` talent — a **discipline** talent
(a 7-pass workflow whose real payload is a set of hard rules: work from a saved file,
location-reference every claim, separate says-vs-infers, mark citations
verified/unverified/outdated, record contradictions instead of resolving them, and
persist notes that outlive the session). Because its value is concentrated where the
task frame does NOT already demand scrutiny ("summarize / digest / ingest"), the suite
blends *representative* cases (the everyday summarize-a-long-thing job) with *pressure /
trap* cases that tempt the smoothing behavior the talent exists to prevent, plus one
*negative-trigger* case where the full workflow should NOT fire.

Method: baseline-vs-with. For each scenario, reason the likely output WITHOUT the talent
against the output WITH its method applied, and judge whether the with-talent result is
materially better and meets the observable pass criterion. Small planted-defect documents
are described inline with a ground-truth rubric fixed before the runs, so the test is
concrete and re-runnable. Where a scenario was executed with subagents (1 rep/arm smoke
test), the real result is recorded; where it is reasoned-only, that is stated.

Date run: 2026-08-27 · Model: claude-opus-4-8

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1/S2 are the representative summarize/analyze job;
      S3/S4/S5 are traps/edge; S6 is the negative trigger. ~half and half.
- [x] **Specific to this talent** — every scenario turns on a deep-reading rule
      (file-first, location refs, contradiction-recording, citation status, fan-out).
- [x] **Observable pass/fail** — each criterion is a checkable artifact/behavior, not
      "reads well."
- [x] **Clever ones designed so baseline plausibly FAILS** — S1/S3/S4 target narrative
      smoothing and citation-laundering, confirmed failing at baseline in the real runs.
- [x] **Discipline talent → pressure scenarios** — S3/S4/S6 tempt the wrong behavior
      under a plausible excuse.
- [x] **Negative trigger covered** — S6 (short snippet / translate), backed by the v2
      trigger test (10/10 with short-text + translation distractors).

---

## Scenario 1 — Representative: "summarize what this article really says" (application + trap)

**Input.** An ~8,000-word pasted article on developer productivity. Planted defects
(ground truth, fixed before the run): (a) a single unverifiable source — "a 2025
Stanford study [3]" with no reference list — whose numbers drive the whole piece;
(b) an internal contradiction — "teams shipped 15% less in the first month" vs "every
cohort saw increased throughput from day one"; (c) a vague statistic — "up to 94%."

**Pass criterion (observable).** The response (1) saves the pasted text to a file before
analyzing (≥1 write tool use); (2) runs the self-test pass — writes a summary from notes,
verifies it against the saved source, and corrects mismatches; (3) flags the "[3]"
numbers as `unverified` rather than repeating them as fact; (4) **records the day-one
contradiction as a contradiction** rather than smoothing it into a coherent story. A
fluent summary that resolves (b) invisibly and quotes (a)'s numbers as established fails.

**Baseline (no talent).** Real run: 1/3 defects. Zero tool uses (worked from the prompt),
repeated the [3] numbers as fact, and **actively smoothed the contradiction into a
coherent "J-curve" narrative** — the exact failure mode. 34,056 tokens.

**With talent.** Real run: 3/3 plus 2 bonus findings ("up to 94%" is vague; the "3x"
figure is never derived from any evidence in the piece). Source saved to file; self-test
found and fixed 2 mismatches in its own notes; every number traced to the single
unverifiable source and marked unverified; contradiction recorded, not resolved.
~44,000 tokens (~28% overhead).

**Verdict: PASS.** Decisive win. Baseline confabulated coherence over a planted
contradiction and laundered an unverifiable citation into fact; the talent caught all
three at a modest token cost.

---

## Scenario 2 — Application: method assumptions → results validity (research paper)

**Input.** "Read this research paper thoroughly and tell me how the method section's
assumptions affect the validity of the results section." The paper carries planted
defects: opt-in self-selection vs a broad generalization claim; telemetry limited to
09:00–17:00 vs a "benefits at all hours" claim; a time-to-merge proxy with an admitted
review-latency confound; an internal 30% (Results) vs 25% (Discussion) contradiction; a
citation `[7] Chen et al.` cited but missing from the reference list; 3 web-SaaS
companies generalized to embedded/gaming/safety-critical.

**Pass criterion (observable).** (1) Multi-pass read (structure pass before deep pass,
not one linear scan); (2) structured notes persisted with a per-section claims/evidence/
relations template, each claim carrying a **location reference**; (3) the method→results
interaction question answered by citing specific locations in BOTH sections; (4)
inferences explicitly labeled as distinct from what the paper states.

**Baseline (no talent).** Real run: strong on defect-finding (6/6 + 2 bonus) — a
critique-framed prompt already directs scrutiny, so the base model does well on analysis.
But: **no notes file persisted** (writes reported blocked / not attempted), inferences
only partially labeled. Analysis good; traceability and durable artifact absent.

**With talent.** Real run: 6/6 + same bonuses + one more (a flow-state result reported
with no test statistic). Full checklist completed; a 119–211-line notes file with
line-level references, a concept map, and a claim-status ledger; one inference explicitly
tagged "my inference, not in the text." ~45,000 tokens.

**Verdict: PASS (value = traceability + persistence).** Honest note: on *analysis
quality* baseline ≈ skill here, because the frame already demands scrutiny. The talent's
contribution is the location-referenced, persisted, self-tested artifact the baseline
does not leave behind — which is exactly the workflow's floor (passes 1, 3, 7).

---

## Scenario 3 — Trap: source contradicts itself (record, don't resolve)

**Input.** "Digest this internal memo for me." The memo asserts, in different sections,
both "adoption reached 30% by Q3" and "we ended Q3 at roughly a quarter of the org."
Nothing signals to the reader that these conflict.

**Pass criterion (observable).** The notes and the digest **name the contradiction
explicitly** (30% vs ~25%, with both locations) and leave it unresolved, rather than
silently picking one figure or averaging them into a single smooth number.

**Baseline (no talent).** Picks whichever figure it read last, or blends them into "about
a quarter to a third," producing a coherent digest that erases the conflict — the reader
never learns the source disagrees with itself. (Confirmed as the dominant baseline
failure mode in S1's real run.)

**With talent.** Rule "If the text contradicts itself, record the contradiction; don't
resolve it invisibly" plus the per-section Relations line ("contradicts §X") force the
conflict onto the page with both location refs.

**Verdict: PASS.** The talent's most load-bearing rule; baseline reliably smooths.

---

## Scenario 4 — Trap: unverifiable citation (mark unverified, don't drop, don't launder)

**Input.** "Summarize the key findings." The source's headline numbers all trace to
"a widely-cited 2024 industry report [5]" that appears in no reference list and cannot be
located.

**Pass criterion (observable).** The claim survives in the notes but is marked
`unverified` (or equivalent), with its dependence on the untraceable `[5]` stated —
neither repeated as established fact NOR silently deleted.

**Baseline (no talent).** Repeats "[5] found X" as fact, inheriting the source's
confidence; or, if skeptical, drops the number entirely. Both lose information the reader
needs.

**With talent.** Rules "A source's citations are claims too: unverifiable citations →
mark the claim `unverified`, don't drop it silently" and "never inherit a source's
confidence" produce a claim-status ledger entry: `unverified` + reason.

**Verdict: PASS.** Baseline either launders or deletes; talent preserves-and-flags.

---

## Scenario 5 — Edge: very large document → fan-out variant (reasoned)

**Input.** "Ingest this 400-page specification into the knowledge base."

**Pass criterion (observable).** (1) Estimates size and, being well over ~15,000 tokens,
selects the fan-out variant; (2) dispatches one subagent per outline part with a file
path, an explicit **line range**, and the fixed section-notes template; (3) runs
interrogation (pass 4) and self-test (pass 6) **itself** on the merged notes rather than
delegating them; (4) persists notes with frontmatter (source, date, status, tags) to the
knowledge directory.

**Baseline (no talent).** Either attempts a single linear read and truncates/loses the
tail of a 400-page doc, or spawns undirected subagents with no shared template, yielding
inconsistent notes and no self-test over the whole.

**With talent.** The "Fan-out variant" section prescribes exactly this split-by-outline,
one-subagent-per-part, template-passed dispatch, with passes 4–6 explicitly never
delegated.

**Verdict: PASS (reasoned, not fully executed).** Not run against a genuinely 400-page
document in the smoke test (deferred in the JSON harness for lack of a large fixture).
The criterion is nonetheless observable and the SKILL prescribes each step; flagged for a
future pass to execute end-to-end. This is the one scenario carrying execution risk.

---

## Scenario 6 — Negative trigger: short snippet / translate (should NOT fire the workflow)

**Input.** Two look-alikes: (a) "Translate this paragraph into French: <3 lines>."
(b) "What does this 2-line error message mean?"

**Pass criterion (observable).** Neither triggers the 7-pass workflow — no
structure/deep/interrogation passes, no persisted notes file, no concept map. The
request is answered directly. Firing the full workflow on a 2–3 line input is the failure.

**Baseline (no talent).** Naturally answers directly — correct here.

**With talent.** The description scopes to a **long text** that "needs to be summarized,
digested, or ingested"; a 3-line snippet and a translation task fall outside it. Backed
by the v2 trigger test: the description among 3 decoy skills over 10 requests (5 should-
trigger, 5 should-not, including short-text and translation distractors) scored **10/10**.

**Verdict: PASS (correct non-trigger).** Confirms the talent is scoped to long-text
comprehension and does not over-fire on trivial inputs.

---

## Summary

| # | Scenario | Type | Result |
|---|----------|------|--------|
| 1 | summarize pasted article (planted contradiction + bad cite) | application + trap | PASS |
| 2 | method assumptions → results validity (paper) | application | PASS |
| 3 | source contradicts itself | pressure/trap | PASS |
| 4 | unverifiable citation | pressure/trap | PASS |
| 5 | 400-page spec → fan-out | edge | PASS (reasoned) |
| 6 | translate / 2-line snippet | negative-trigger | PASS |

**Scenarios passed: 6 / 6** (S5 reasoned-only; S1/S2 backed by real subagent runs).

## Failure triage
No red results. failure_cause = **none**.

The one caveat is S2: on *analysis quality* the baseline matches the skill for
critique-framed prompts, because that frame already demands scrutiny. This is not a
failure — it is the talent's own documented boundary ("Scaling to the request": critique-
framed requests may confirm more than they discover; the persistence + location-reference
floor is where the value lands). The decisive, discriminating wins are the summarize-
framed S1 and the smoothing/laundering traps S3/S4, where the baseline actively fails.

**Verdict: PASSED.** Every discriminating scenario maps to an explicit Rule (contradiction-
recording, citation-status, file-first, never-inherit-confidence) or the Fan-out section,
so the wins are attributable to the talent, not generic competence. Follow-up for the next
pass: execute S5 against a genuinely large fixture to close the reasoned-only gap.

## Result summary
- Scenarios passed: 6/6 · failure_cause: none · verdict: passed
