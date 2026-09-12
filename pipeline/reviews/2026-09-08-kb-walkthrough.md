# Walking the whole knowledge base, 2026-09-08

A full curation pass over `knowledge/` — the deterministic tier first, then the judgement tier
that no script can do. Four read-only judges over the 23 candidate pairs (every pair sharing a
source, plus every pair sharing three or more tags), coordinator applying every change.

## The deterministic tier had nothing left to do

`kb.py check` PASS · lint 0 errors 0 warnings · `contradictions` 0 · `links` 0 pairs argued at
neither end · `watch.py --offline` 96 rows, 203 raw files, 0 unexplained. **The safe tier of the
curator's method was empty before the pass started** — which is the point of having built it.
Everything below came from reading.

## Applied — verified against primary source or against the base itself

| # | What | Evidence |
|---|---|---|
| 1 | **A percentage that was a factor.** `graphify-assessment` quoted *"79% token reduction"* as the source's claim. The held bytes read verbatim **"Reduction: 79.6x fewer tokens per query"** and *"We're seeing 79x token reductions"* — a factor, never a percent. 496k → 6.2k is **80×, a 98.8% cut**; "79%" understates the source by a factor of eighty, *inside quotation marks*. The origin is the URL slug `…-79-token-reduction`, which carries no unit. **The correct figure was already three sections above on the same page.** | `knowledge/raw/watch-2026-09-08c/stevescargall.com_graphify-memmachine.html` |
| 2 | **A citation pointing at a page that never mentions its subject.** `token-economy-playbook` attributed Graft's controlled +42%/+46% figure to `[[graphify-assessment]]` **twice**, including in a standing rule. That page contains **zero** occurrences of "Graft". The owner is `claude-code-ecosystem-plugins`. Retargeted, with the edge argued at both ends per the reciprocity rule. | grep over `knowledge/notes/` |
| 3 | **A benchmark contradiction inside one page.** `model-agnostic-agent-harnesses` reports Opus 4.8 on Terminal-Bench 2.1 as **85.0** (vendor blog, "who ran the Opus 4.8 numbers is not stated") and as **76.0%** (NVIDIA's own README, MEASURED). Nine points, same benchmark version, same model. Marked disputed at **both** sites; neither value picked. **A pairwise contradiction check cannot see this — both values live on one page.** | the note's own two tables |
| 4 | **Two Anthropic eval schemas for one filename.** `skill-authoring-best-practices` presented one as "the Official version" without the caveat the contract had already recovered: *"There is not currently a built-in way to run these evaluations."* Additive cross-reference; no value changed. | `anthropic-skill-authoring-contract` |
| 5 | **A compiled page with no freshness mechanism** — see below. | `kb.py lint` |
| 6 | **A wrong default in a frontmatter field list.** `subagents` said `model` has **"default `inherit`"**. The held bytes say the opposite: *"When you omit it, Claude Code picks the model in the subagent model order"*. Omitting is **not** `inherit` — if it were, `CLAUDE_CODE_SUBAGENT_MODEL` could never take effect and `model-routing-free-and-local`'s entire level-1 routing table would be inert. Corrected, with the version-tied caveat neither note carried: **before v2.1.251 the env var came first**, overriding the per-invocation parameter and the frontmatter, `model: inherit` included. | `knowledge/raw/claude-code-docs-2026-09-04/sub-agents@2026-09-04.md:296`, `:356` |
| 7 | **A self-measurement that went stale when its neighbour was refreshed.** `subagents` said a cited version was *"29 releases above the highest this knowledge base cites"*. Re-swept: the highest cited elsewhere is **v2.1.257**, so the gap is **4**. The sentence was measuring the base, and a later refresh of `skill-anatomy` moved the thing it measured — the failure it was itself describing. | sweep of every `v2.1.x` in `knowledge/notes/` |
| 8 | **Three more pinned running statistics.** `agent-design-template`: *"all 84 skills in this library are ~176,000 tokens — 18% of the window"*, undated, in a page that does not own the measured surface. Today: **89 bodies, ~167,597 tokens, 16.8%**. Replaced by a pointer to the script, which itself prints *"Do not copy one into a document as a constant."* | `pipeline/queries/context_surface.py` |
| 9 | **A vendor qualifier that bears on this repo's own concurrency constant.** The workflows page states its cap as *"Up to 16 concurrent agents, **fewer when Claude Code has fewer CPUs available, including inside a CPU-limited container**"* — a qualifier `dynamic-workflows` never carried, and that page has not been re-read since 2026-08-27. Recorded in the note **and** in `CONSTANTS.md` beside `W_MAX_AGENTS`. It does **not** move the constant: 4 was measured on this box against a threshold fixed beforehand, and a formula is still not a measurement. What it changes is the confidence that 4 travels. | `knowledge/raw/baseline-2026-09-04/code.claude.com_docs_en_workflows.md:349` |

## The structural finding: a page built from the base had no watcher

`third-party-landscape` is the base's one *compiled* page — a summary written back as a note,
whose sources are `path:` entries pointing at five other notes. It declares `fetched:
2026-09-02`; **all five inputs had been rewritten since**, two of them now declaring later
fetches. Nothing could have said so: `watch.py` watches external URLs, the lint checks schema
and links, `contradictions` compares values across pairs. **A page whose inputs are other pages
has no watcher, because its sources never move on the network.**

Fixed with a join key of the kind the raw layer already uses: `compiled_from:` records each
input's declared fetch at compile time, and `kb.py lint` compares it against each input's
current one. Declared dates rather than git or mtime **on purpose** — CI checks out shallow so
`git log` is empty there, and a fresh clone gives every file the same mtime. Five fixtures, five
mutations, all caught.

It also caught a pinned running statistic in that page: **"36 notes"**, undated, now 44. Dated
in place rather than updated, per this repository's own rule that a value which moves on its own
is recorded with a pointer to its live computation and never as a number.

## Four of these were APPLIED 2026-09-12 — with evidence the base already held

Marked here rather than deleted, so the count is honest: **eleven proposals, four now applied, seven
open.** None of the four needed a fetch, a run, or a human. What they needed was reading two pages at
once, which is what a review pass produces and then nobody does.

| applied | what was done |
|---|---|
| `graphify-features` **Export block** | listed exports as **flags** while the same note, 130 lines below, explained the two command surfaces correctly and named the flag form as its own lesson. Rewritten to the measured `graphify export <format>` subcommands, with `--obsidian` marked as the SKILL-surface flag it is |
| `graphify-features` **manifest.json** | the README-silence row is KEPT and the ECC pilot's runtime observation added beside it, because the two are different evidence bases and collapsing them loses which supported what. `cost.json` stays unobserved by either route |
| `agent-builder-prior-art` **label** | AUTHORITATIVE → **FIRST-PARTY, graded per item in `anthropic-skill-authoring-contract`**. First-party is a fact about the publisher; authoritative is a claim about the contents, and the pass one day later found the guide's body template followed by 0 of 11 shipped skills |
| `graphify-assessment` vs `graphify-features` **canonical repo** | the over-claiming side is now qualified at every occurrence. New evidence from `kb.py owners` 2026-09-12: the `safishamsi` self-links are **0 of 1 LIVE**, *"a leftover, not a move"* — so the evidence leans to `Graphify-Labs` without closing it, and the word is "likelier", not "canonical" |

**And one open item changed category.** The `skill-anatomy` internal contradiction needs the guide
re-extracted, which this environment cannot do — but that turns out to be a **regression**, not a
limitation: `anthropic-skill-authoring-contract` records the extraction as done with `pdfminer.six`
and `pypdf` on 2026-09-04, and both are unusable here today. See `knowledge/notes/long-document-ocr.md`.

## Status of all eleven — corrected 2026-09-12

The heading here said "the seven still open" while the table below still listed all eleven, which is the
same defect this pass exists to find. Each row now carries its own verdict, and **the count below is derived from the table rather than
written by hand** — because two later attempts to update it by hand silently matched nothing and left
a third number standing. As of 2026-09-12: **9 resolved, 2 open, 0 blocked.** Both open rows
are the human's.

| # | row | status |
|---|---|---|
| 1 | `extract --no-viz` needs a run | **RESOLVED 2026-09-12 by running it.** `--no-viz` is **respected**, not silently ignored: no `graph.html` in `graphify-out/`. The worry that the pilot "built the viz it believed it had suppressed" is refuted for 0.9.58 |
| 2 | canonical graphify repo | **RESOLVED.** Qualified at every occurrence; `kb.py owners` shows the `safishamsi` self-links 0-of-1 LIVE, *"a leftover, not a move"* — leans to Graphify-Labs without closing it |
| 3 | `skill-anatomy` internal (skill-creator's eval capability) | **RESOLVED 2026-09-12.** The blocker was a poisoned system dependency, not a missing toolchain: `pypdf` 6.18.1 in a clean venv reads the guide (33 pages, 35,765 chars). Verdict: the sentence is **stale, not false** — the guide's `/CreationDate` is 2026-01-26, `pass_rate` appears **0 times** in it, and the tool's metrics were read 2026-08-30 |
| 4 | evals-before-writing vs the canonical loop's order | **RESOLVED 2026-09-12.** Not opposite orderings: the contract runs without-skill baseline → *minimal* instructions and defers only *extensive* documentation, while `skill-creator`'s loop opens at "write a draft" with **no without-skill step at all**. The contract's "confirmed" claim is retracted — a loop cannot confirm an ordering whose first step it omits. The baseline arm is **our** addition over the vendor's loop |
| 5 | frontmatter optional vs mandatory | **RESOLVED.** The spec says *"The required `name` field"* / *"The required `description` field"*; the scope clause (spec requires, loader tolerates) is now at both ends |
| 6 | gateway discovery vs the gemma screenshot | **RESOLVED.** Two code paths: the filter governs what is *discovered*, a pinned model's row shows the raw id and never passes it |
| 7 | `manifest.json` unconfirmed | **RESOLVED, then measured directly.** The additive row landed 2026-09-12; the same day a real run wrote `graphify-out/manifest.json`, 71,711 bytes. Confirmed twice, by two evidence bases |
| 8 | Export block lists flags | **RESOLVED.** Rewritten to the measured `graphify export <format>` subcommands, `--obsidian` marked as the skill-surface flag |
| 9 | `agent-builder-prior-art` label | **RESOLVED.** AUTHORITATIVE → FIRST-PARTY, graded per item in `anthropic-skill-authoring-contract` |
| 10 | recompile `third-party-landscape` | **OPEN — the human's.** Two standing lint warnings, both true; recompiling a 29 KB synthesis over 44 notes is a wholesale rewrite |
| 11 | `status:` has cardinality one | **OPEN — the human's.** Every note is `verified`; deciding what the other values mean is a judgement about the base's standard |

The original table follows unchanged, as the record of what was proposed and why.

## The eleven as originally proposed

| Kind | Pages | The question |
|---|---|---|
| **needs a run** | `graphify-features`, `graphify-assessment` | `extract --no-viz` is named as a member of the accepted-then-silently-ignored flag class, while the same base prescribes it twice. If the flag class is right, the 11,915-node pilot built the viz it believed it had suppressed. One run of `graphify extract --no-viz` and a check for `graph.html` settles it. |
| contradiction | `graphify-assessment` vs `graphify-features` | Which GitHub repo is graphify's canonical home. `features` records "not settled by the evidence we hold" **and** that an earlier "canonical" call was corrected by `kb.py owners`; `assessment` still says canonical twice, resting on the PyPI metadata alone that `features` records as insufficient. |
| contradiction | `skill-anatomy` (internal) | Anthropic's guide: skill-creator *"does not execute automated test suites or produce quantitative evaluation results"* (PDF, 2026-08-29). The same note, ~100 lines later, describes it automating baseline-vs-skill runs and emitting `pass_rate` / `tokens {mean, stddev}` / a delta (direct read, 2026-08-30). Likeliest reading — the guide predates the shipped tooling — is **untested**: the PDF was not re-extracted. |
| contradiction | `anthropic-skill-authoring-contract` vs `skill-authoring-eval-methodology` | Where evals sit relative to writing: *"Create evaluations BEFORE writing extensive documentation"* against a canonical loop with a draft at step 2 and test prompts at step 3. The contract asserts the eval note "confirmed" its ordering; the step list is the opposite order. |
| contradiction | `skill-anatomy` vs `skill-authoring-eval-methodology` | Frontmatter `name`/`description`: "All optional" versus "mandatory". Both may hold under different governing documents (the loader tolerates omission; the spec requires them) — but neither page carries the scope clause, so `skill-anatomy` alone reads as licence to ship without either. **Not resolvable this pass:** `agentskills.io/specification` is not held as raw and its fetch date is `null`. |
| contradiction | `model-routing-free-and-local` vs `model-agnostic-agent-harnesses` | Gateway discovery keeps only ids containing `claude`/`anthropic` (re-verified 2026-09-08, raw held) — yet a vendor screenshot on v2.1.126 shows `open_router/google/gemma-3-4b-it:free` in the picker, an id that could not pass that filter. Two untested reconciliations: a **pinned** model bypasses discovery, or the screenshot is the router's own UI. |
| stale | `graphify-features` | `manifest.json` graded "unconfirmed" from README silence; the ECC pilot measured it present. Exact additive row proposed, because README-silence and a runtime observation are not the same evidence base. |
| stale | `graphify-features` | The Export block lists exports as **flags**; they were measured as **subcommands**, and `--obsidian` belongs to the `/graphify` *skill* surface — the exact invocation-form error both notes name as their own lesson. |
| label | `agent-builder-prior-art` | Calls the PDF guide "AUTHORITATIVE" (2026-08-29), one day before the pass that found its body template followed by **0 of 11** shipped skills and retracted the word for its 5,000-word cap. Proposed: "FIRST-PARTY; corroborated or refuted per item in [[anthropic-skill-authoring-contract]]". |
| recompile | `third-party-landscape` | Two standing lint warnings, both true. Recompiling a 29 KB synthesis over 44 notes is a wholesale rewrite of a summary page — a proposal, not a curator's fix. |
| schema | all 44 notes | **`status:` has cardinality one.** Every note is `verified`. Either the base has no provisional page, in which case the field costs a line per note and says nothing, or pages are marked verified on arrival — in which case the word means "written". |

## The hub verdict, since it was the reason four pairs were assigned

`agent-design-template` shares a source with five other notes, the most connected page in the
base. It is a **genuine hub**, not an absorber: it owns the six-tier layering model, the
where-a-thing-belongs table, the four-places-for-agent-rules table, the fixation trap, the
composition-pattern verdicts — and every mechanic it restates carries a pointer to its owner.
Two leaks were found and only one mattered: the compaction budget is restated without naming
`skill-anatomy` (argued reuse, not absorption), and the library-size statistic above, which was
a measurement of a surface the page does not own.

## What the pass says about the checks themselves

Five of the nine applied findings were **invisible to every existing check**, and each for a
different structural reason: one lived inside a single page (the pairwise contradiction check
compares across pairs); one was a *pointer* to a page that does not contain the subject (the
link check verifies that a target exists, never that it is the right target); one was a unit
error in a quotation (no check reads units); one was a **wrong default in a field list**, which
only the held bytes could settle; and one was a **self-measurement about the base** that a
later, unrelated refresh of a neighbour falsified. The negative worth recording: **a base can be green
on every deterministic check and still carry a figure wrong by a factor of eighty.**

The judges also produced substantial *negative* results, which are kept: the four-note
skill-authoring cluster is **not** a duplicate set — it has a stated evidence-tier boundary
(runtime / what Anthropic states / where three sources agree / a harvest verdict) and merging
any two would destroy it; `1,024` and `1,536` are two different subjects and no note in the
cluster states either for the other's; `best-local-llm-2026-09` and `glm-5.3-local` agree on
every shared figure; and `model-routing-free-and-local` borrows the playbook's cost figures by
citation rather than restating them, so there is no second value to drift.
