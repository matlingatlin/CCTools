---
title: Anthropic's skill authoring contract — body, bundled files, evals, baseline
sources:
  - url: https://code.claude.com/docs/en/skills
    note: "Read in full (96.9 KB). Body guidance, lifecycle, frontmatter, evaluate-and-iterate."
    fetched: 2026-08-30
  - url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
    note: "The substantive authoring document, linked from the Claude Code page. Progressive disclosure, reference depth, workflow/checklist pattern, EDD ordering."
    fetched: 2026-08-30
  - url: https://agentskills.io/specification
    note: "The open standard. Body: 'There are no format restrictions.' Directory contract for scripts/ references/ assets/."
    fetched: 2026-08-30
  - url: https://agentskills.io/skill-creation/evaluating-skills
    note: "Eval workspace layout, grading principles, derived JSON artefacts."
    fetched: 2026-08-30
  - url: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
    note: "33 pp (CORRECTED 2026-09-04: this entry said 30. Measured on a fresh download with pypdf — 33 pages, all 33 carrying extractable text, so the obvious excuse that three pages were blank is refuted; the file's own ModDate is 2026-01-26, months before either read, so it did not change under us and 30 was simply wrong). Downloaded and text-extracted with pdfminer.six. TWO-COLUMN layout — p.12's body template was recovered by column-ordered element sorting; heading levels there are INFERRED from extractor artefacts, not read directly."
    fetched: 2026-08-30
  - url: "local: /mnt/skills/ (37 shipped Anthropic skills) and claude-plugins-official marketplace (plugin-dev/skill-development, skill-creator)"
    note: "Read and measured directly. Evidence of PRACTICE, not of stated rules."
    fetched: 2026-08-30
verified_by: "Dedicated research pass 2026-08-30, sources fetched that day; unreached sources listed at the foot of this note. Not independently re-verified by a second party."
tags: [skills, authoring, anthropic, evals, baseline, progressive-disclosure]
related: ["[[skill-anatomy]]", "[[skill-authoring-best-practices]]", "[[skill-authoring-eval-methodology]]", "[[testing-skills-methodology]]", "[[agent-design-template]]", "[[agent-builder-prior-art]]"]
raw:
  - knowledge/raw/claude-code-docs-2026-09-04/skills@2026-09-04.md
  - knowledge/raw/pdf-sources-2026-09-11/resources.anthropic.com_hubfs_The-Complete-Guide-to-Building-Skill-for-Claude.pdf
  - "the guide is HELD but only 17.6% EXTRACTABLE here (hex-coded CID text); knowledge/pdftext.py refuses it, so rows read from it cannot be re-verified in this environment - see pipeline/decisions/2026-09-11-stdlib-pdf-text.md"
  - "partial: 2 of 6 distinct source URLs kept as raw; the rest predate the raw layer (2026-09-02)"
---

# Anthropic's skill authoring contract

What Anthropic **states** about writing and evaluating a skill, separated from what
Anthropic **does**. Written after a decision to treat Anthropic as the authority,
because they own the runtime the skills execute in.

[[skill-anatomy]] holds the frontmatter fields, the loading mechanics and the
hard rules. This note holds the body, the bundled files, the evals and the
baseline — and marks where Anthropic says nothing.

Three sibling notes cover the same subject from different evidence, and the split is
the point. [[skill-authoring-best-practices]] records only what three independent
sources AGREE on, so a rule there is corroborated where a rule here is merely
*stated*. [[skill-authoring-eval-methodology]] reads Anthropic's shipped
`skill-creator` — the authoring→eval loop as code rather than as prose. **The claim that it
"confirmed" this contract's ordering was FALSE and is retracted (2026-09-12); see the section
below.** [[testing-skills-methodology]] holds
what **we** measured running that loop, and is therefore the note to read when the
stated contract and an observed result disagree; several of its sections exist because
they did.

**Read the practice table before trusting any "recommended" item here.** Three of
the most-quoted recommendations are followed by none of Anthropic's own skills.

## The body — no required structure

The spec disclaims it outright:

> "The Markdown body after the frontmatter contains the skill instructions.
> **There are no format restrictions.** Write whatever helps agents perform the
> task effectively. Recommended sections: Step-by-step instructions · Examples of
> inputs and outputs · Common edge cases"

`code.claude.com/docs/en/skills` prescribes nothing structural either. Its only
body-level rules are two:

> "Keep the body itself concise. Once a skill loads, its content stays in context
> across turns, so every line is a recurring token cost. **State what to do rather
> than narrating how or why.**"

> "Claude Code does not re-read the skill file on later turns, so **write guidance
> that should apply throughout a task as standing instructions rather than one-time
> steps.**"

### The one published skeleton, and nobody uses it

PDF guide p.12, "Writing the main instructions", labelled *"Adapt this template"*:

`# Title` → `## Instructions` (numbered steps, each with an example command and
an *expected output* line) → `## Examples` (user-says / actions / result triples)
→ `## Troubleshooting` (error / cause / solution triples).

**Zero of the 11 shipped skills measured follow it.** Treat it as one option, not
as the shape.

**Read rather than inferred, 2026-09-12.** The 2026-09-04 pass marked this template's heading
levels *"inferred, not read"* because the guide is two-column and the columns had to be re-sorted.
The document is now readable directly, and the inference **holds**: a three-level hierarchy under a
single `#` title, with `Step 1: [First Major Step]` as a heading rather than a list item, and both
the *"Expected output: [describe what success looks like]"* line and the user-says / actions /
result and error / cause / solution triples present verbatim. One thing the summary above omits:
the template block **includes the frontmatter**, so it is a whole-file skeleton, not a body one.

**A PDF artefact worth knowing, because it silently rewrites markdown.** Inside the guide's code
blocks, `##` extracts as `-#` and `###` as `--#` — consistently, at every depth, in every template
in the document (`-# Instructions`, `--# Step 1`, `-# Workflow: Onboarding`, `--# Phase 1: Design`).
It is not that hashes fail to extract: `# Your Skill Name`, `# Bad` and `# Good` come out correctly
in the same blocks, and the *prose* sentence `Use ## Important or ## Critical headers` extracts with
both hashes intact. In a run of N hashes the **last** survives and the first N-1 become hyphens,
which is the signature of a **programming-ligature font**: the ligature is drawn as N-1 placeholder
glyphs plus one composite, and the placeholders carry no useful `/ToUnicode` entry. The same class
of defect `pdftext.py` documents for `fi`/`fl`/`ff`, in a different reader on a different glyph, and
with a worse consequence — a dropped ligature looks like a typo, whereas **a heading level rewritten
as a hyphen looks like valid markdown of the wrong depth.** Read the `-#` forms as `##`; a reader
who did not would copy this template out one heading level flat.

### The one ordering rule Anthropic gives

PDF p.25, under "Instructions not followed":

> "2. Instructions buried – **Put critical instructions at the top** – **Use
> `## Important` or `## Critical` headers** – Repeat key points if needed"

That is the entire published guidance on what comes first.

### What the body must ANSWER — Anthropic's own three questions

From `plugin-dev/skills/skill-development/SKILL.md` (Anthropic's official
marketplace), and repeated verbatim in `references/skill-creator-original.md`:

> "To complete SKILL.md body, answer the following questions:
> 1. What is the purpose of the skill, in a few sentences?
> 2. When should the skill be used? (Include this in frontmatter description with
>    specific triggers)
> 3. In practice, how should Claude use the skill? All reusable skill contents
>    developed above should be referenced so that Claude knows how to use them."

**This is the usable contract.** It governs what must be answerable, not which
headings appear — which is the only form compatible with a spec that forbids
format restrictions.

### Step shape, when the task is multi-step

best-practices, "Use workflows for complex tasks":

> "Break complex operations into clear, sequential steps. **For particularly
> complex workflows, provide a checklist that Claude can copy into its response
> and check off as it progresses.**"

Their worked example: a fenced `Task Progress:` checklist block, then
`**Step N: <name>**` headers, each carrying the command to run and what it
produces, plus an explicit loop-back ("If verification fails, return to Step 2").

### Body length — three incompatible numbers across four sources, unreconciled

| Source | Value |
|---|---|
| best-practices · Claude Code docs · spec checklist | **"under 500 lines"** (stated in the three sources named at left; [[skill-anatomy]] counts the same three. An earlier "four times" here matched no list and was corrected 2026-09-04) |
| agentskills.io spec, progressive-disclosure table | **"< 5000 tokens recommended"** |
| `plugin-dev/skill-development` | **"<5k words"**, target **1,500–2,000 words**, soft cap 3,000 |
| PDF guide | "Keep SKILL.md under 5,000 words" — **a remedy, not a cap; see below** |

**The fourth row is not the same kind of statement as the other three — read 2026-09-12.** In the
guide the sentence sits under *"Solutions:"*, in the troubleshooting chapter, answering the symptom
*"content too large"*: `1. Optimize SKILL.md size - Move detailed docs to references/ - Link to
references instead of inline - Keep SKILL.md under 5,000 words`. It is what to do about a skill
already diagnosed as oversized, not a bar every skill is authored against. So three sources give
prescriptive caps and the fourth gives a remediation step, and the table above was comparing a rule
with a repair. **That shrinks the contradiction rather than settling it** — the three prescriptive
numbers still disagree with each other — but it removes the widest of the four from the dispute, and
it is the one this page previously called authoritative.

**No Anthropic source reconciles the remaining three.** [[skill-anatomy]] previously called
5,000 words "authoritative"; that was one source among four and the 500-line
figure is the more frequently stated. Corrected there 2026-08-30.

Measured practice: 11 skills range **211 → 5,166 words** and **32 → 485 lines**.
None exceeds 500 lines.

**And our own 89, measured 2026-09-08** (`python3 pipeline/queries/context_surface.py`) — the
half this table never had:

| bar | our skills over it |
|---|---|
| **"under 500 lines"** (the most frequently stated) | **2 of 89 — 2.2%** |
| "< 5,000 tokens recommended" (spec) | 2 of 89 |
| "<5k words" (plugin-dev, PDF guide) | **0** |
| 3,000-word soft cap (plugin-dev) | 3 of 89 |
| 1,500–2,000-word target, upper end | 15 of 89 — 16.9% |

Distribution: **median 117 lines / 879 words / ~1,429 tokens**, p90 249 lines, max 563. So the
library sits comfortably inside every *hard* bar — the median is under a quarter of the
most-stated one — and the disagreement between the four sources has never bitten us, because we
are nowhere near where they disagree. That is worth stating plainly: **the unreconciled numbers
are not a live problem for this library**, and treating them as one would be optimising a
constraint nobody is close to.

The two over the 500-line bar are `subagent-driven-development` and `writing-skills`, both at
**exactly 563 lines**. Neither is trimmed here: shortening a body changes behaviour, so it is a
`skill-measure` job against a baseline, not a curation edit — the same reasoning that keeps the
13 over-cap descriptions untouched. Recorded so the next person knows which two, and why they
were left.

## Bundled files — the most thoroughly specified area

Spec directory contract:

> "`scripts/` — executable code that agents can run... `references/` — additional
> documentation that agents can read when needed... **Keep individual reference
> files focused. Agents load these on demand, so smaller files mean less use of
> context.** `assets/` — static resources: templates, images, data files."

`plugin-dev/skill-development` draws the load/execute/use distinction:

> "**Scripts** ... **may be executed without loading into context** ...
> **References** — intended to be **loaded as needed into context** ...
> **Best practice: If files are large (>10k words), include grep search patterns
> in SKILL.md.** **Avoid duplication: Information should live in either SKILL.md
> or references files, not both.**
> **Assets** — **Files not intended to be loaded into context**, but used within
> the output Claude produces."

### Reference depth — a hard rule with its failure mode stated

> "**Claude may partially read files when they're referenced from other referenced
> files. When encountering nested references, Claude might use commands like
> `head -100` to preview content rather than reading entire files, resulting in
> incomplete information.** **Keep references one level deep from SKILL.md.**"

This is the strongest rule Anthropic gives about bundled files, and it appears as
a checklist item. Nesting produces **silently incomplete** reads, not errors.

### How the body must point at a bundled file

> "Reference supporting files from SKILL.md **so Claude knows what each file
> contains and when to load it**."

> "**Make execution intent clear:** 'Run `analyze_form.py` to extract fields'
> (execute) · 'See `analyze_form.py` for the extraction algorithm' (read as
> reference)."

Naming: *"Use names that indicate content: `form_validation_rules.md`, not
`doc2.md`"*. Organise by domain so an unrelated domain's file is never loaded.
Table of contents threshold is given as **100 lines** (best-practices) and
**300 lines** (skill-creator) — unreconciled.

### When a script should exist at all

skill-creator, and it is an observation rule rather than a judgement:

> "**Look for repeated work across test cases.** ... **If all 3 test cases
> resulted in the subagent writing a `create_docx.py` or a `build_chart.py`,
> that's a strong signal the skill should bundle that script.**"

And pruning, from best-practices: a bundled file Claude never opens is
unnecessary or badly signalled; a file Claude opens every time belongs in
SKILL.md.

## Baseline — documented, and operationally defined

`code.claude.com/docs/en/skills`, "Evaluate and iterate on a skill":

> "**The check for both is a baseline comparison. Collect a few realistic prompts,
> run each one in a fresh session with the skill available and again with it
> disabled, and compare the results. A fresh session matters because leftover
> context from authoring the skill will mask gaps in the written instructions.**"

Two baseline variants, from skill-creator:

- **New skill** → no skill at all, same prompt.
- **Improving an existing skill** → snapshot the old version first and point the
  baseline run at the snapshot.

The timing rule that makes it controlled:

> "For each test case, spawn two subagents in the same turn — one with the skill,
> one without. **This is important: don't spawn the with-skill runs first and then
> come back for baselines later.**"

EDD ordering, from best-practices — evaluations come **before** the writing:

> "**Create evaluations BEFORE writing extensive documentation.** ... 1. Identify
> gaps: Run Claude on representative tasks without a Skill ... 3. Establish
> baseline ... 4. Write minimal instructions ... 5. Iterate"

### Whether evals come before writing — the contradiction resolved 2026-09-12

Recorded for four days as *"the contract asserts the eval note confirmed its ordering; the step list
is the opposite order"*. Read side by side, **they are not opposite orderings of the same steps —
they differ on whether a baseline is taken before anything is written at all.**

| | this contract (best-practices) | `skill-creator`'s shipped loop |
|---|---|---|
| 1 | *"Identify gaps: Run Claude on representative tasks **without a Skill**"* | Decide what the skill does |
| 2 | *"Establish **baseline**"* | **Write a draft** |
| 3 | *"Write **minimal** instructions"* | Write test prompts; run Claude-with-the-skill |
| 4 | *"Iterate"* | Evaluate, rewrite, repeat |

The rule *"Create evaluations BEFORE writing extensive documentation"* is consistent with its own
step 3 writing something: what comes first is the **without-skill baseline**, and what is deferred is
*extensive* documentation. `skill-creator`'s loop has **no without-skill step at all** — it opens at
"write a draft" and every later measurement is with-skill.

**So the "confirmed" claim could not have been true.** A loop that omits a step cannot confirm an
ordering whose first step it omits; it confirms a *different* loop. Retracted above.

**And this library follows THIS contract rather than the shipped loop, which is worth knowing
explicitly.** `skill-measure`'s own words: *"The measurement is not the last step. It is the first
one: the baseline probe runs"* before anything is written. `skill-authoring-eval-methodology` says so
from its side too — *"Our `writing-skills` covers authoring and `eval-harness` covers
baseline-vs-with"* — i.e. the baseline arm is **our addition, sitting outside `skill-creator`'s
loop**. Two documents that looked contradictory turn out to describe a real gap in the shipped tool,
and this library had already filled it without recording that it was doing so.

### What counts as a failure

> "**Require concrete evidence for a PASS. Don't give the benefit of the doubt.**
> If an assertion says 'includes a summary' and the output has a section titled
> 'Summary' with one vague sentence, **that's a FAIL — the label is there but the
> substance isn't.**"

### What Anthropic refuses to set

No pass threshold, no failure budget, no significance test. Stated plainly:

> "**These are aspirational targets — rough benchmarks rather than precise
> thresholds. Aim for rigor but accept that there will be an element of
> vibes-based assessment. We are actively developing more robust measurement
> guidance and tooling.**"

The delta is framed as cost/benefit, not a bar: *"A skill that adds 13 seconds but
improves pass rate by 50 percentage points is probably worth it. A skill that
doubles token usage for a 2-point improvement might not be."*

## Eval artefacts — a prescribed file, path and schema

**Location, stated identically in two sources:** `evals/evals.json`, **inside the
skill directory**.

```json
{
  "skill_name": "example-skill",
  "evals": [
    { "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": ["The output includes X", "The skill used script Y"] }
  ]
}
```

Derived artefacts, produced not authored: `grading.json` (fields **must** be
`text` / `passed` / `evidence` — "the viewer depends on these exact field names"),
`timing.json` (`total_tokens`, `duration_ms` — *"the only opportunity to capture
this data"*), `benchmark.json` (`with_skill` / `without_skill`, each `pass_rate`,
`time_seconds`, `tokens` as `{mean, stddev}`, plus a `delta`).

Workspace layout: a **sibling** directory `<skill-name>-workspace/` containing
`iteration-N/`, containing per-eval directories named descriptively, each with
`with_skill/` and `without_skill/`.

**A second, incompatible schema** exists on the best-practices page —
`skills` / `query` / `files` / `expected_behavior` — carrying its own caveat:
*"There is not currently a built-in way to run these evaluations. Users can create

> **A built-in runner now exists — and the caveat above is STILL TRUE, which is the finding
> (re-read 2026-09-11).** `claude plugin eval` shipped (docs at `/docs/en/plugin-evals`, which
> names **v2.1.269**): it runs a suite, scores with judge graders, **compares against a no-plugin
> baseline** — its own words are "the with-arm and the without-arm" — and gates CI on the score.
> `claude plugin eval init` will even propose the cases and write the files.
>
> **It does not read either `evals.json` schema.** The page says so itself: *"Its case format is
> separate from the `evals/evals.json` file the skill-creator plugin uses."* A suite is a
> directory tree — `evals/` with **one subdirectory per case**, each holding a prompt and one or
> more graders. So Anthropic now ships **three** eval formats for skills, a runner for exactly one
> of them, and the sentence quoted above remains accurate about the other two.
>
> Two things follow for us. The runner does baseline-vs-with the same way `skill-measure` and
> `eval-harness` specify it, so it is a first-party instrument for the measurement this library
> already requires — but only for a talent **shipped inside a plugin**, which ours are not. And it
> **spends real money**: *"Eval runs, judge-scored graders, and `claude plugin eval init` call the
> model with your credentials, so they count against your plan's usage limits or your API bill."*
> Adopting it is a measured decision, not a free upgrade.
>
> **Re-read again 2026-09-11 (evening); the page moved within hours and two changes are
> substantive.** Most of the diff is editorial ("by hand" → "manually", anchors renamed), but:
>
> **The cost is now stated as a formula, and it is DOUBLE what a one-armed reading suggests.**
> The page previously said *"cases × runs × arms agent runs"*, leaving `arms` undefined; it now
> spells it out — *"a suite makes roughly cases × runs agent runs with the plugin **and as many
> again for the no-plugin baseline**, plus three short judge calls per `llm` or `baseline` grader
> per run."* So the baseline arm that makes the instrument worth having is also what doubles its
> bill. With the default 3 runs, a 10-case suite is ~60 agent runs plus judge calls. That number
> belongs beside the open decision about packaging this library as a plugin.
>
> **An `llm` judge does NOT see the whole transcript.** New, in the grader-evidence table:
> *"A `regex` grader sees every message; an `llm` judge sees the first 12 and the last 12."* So on
> any run longer than 24 messages the judge is blind to the middle, and nothing in its verdict says
> so. This is the same shape this base keeps finding and has a name for — **the failure is not that
> it errors, it is that it parses** — and it lands squarely on the measurement this library
> requires: a talent whose effect shows up in the middle of a long agent run is invisible to the
> grader that is supposed to detect it. A `regex` grader is the instrument that sees everything.
>
> Smaller, recorded so a later diff is not re-read from scratch: `schema_version` `"1.1"` appeared
> as a case field; `type: agent` mocks now answer via `--judge-model`, so **changing the judge
> changes the mocks**; the replay path is `mocks/.replay/`, not `.replay/`; and an unusable evals
> directory behaves two ways — as a flag it is an error, as a manifest value it prints a `Warning:`
> and **silently falls back to `evals/`**.
their own evaluation system."* And an internal inconsistency: `schemas.md` calls
the field `expectations`; SKILL.md and agentskills.io call it `assertions`.

Count: "2-3 test cases" (agentskills.io) vs "at least three" (best-practices
checklist). Description triggering is a **separate** artefact — 20 queries,
8–10 positive and 8–10 negative, where *"the most valuable ones are the
near-misses"*.

## Who runs the test, and who writes the assertions

**Running must be independent, and the reason is stated:** leftover authoring
context masks gaps in the written instructions. Subagents give this for free; a
separate session otherwise.

Anthropic names author-runs-own-test as a rigour deficiency, in the Claude.ai
fallback path: *"**This is less rigorous than independent subagents (you wrote the
skill and you're also running it, so you have full context)**, but it's a useful
sanity check — and the human review step compensates."*

Grading is delegated, and the grader also audits the assertions:

> "**You have two jobs: grade the outputs, and critique the evals themselves. A
> passing grade on a weak assertion is worse than useless — it creates false
> confidence.**"

Version comparison must be **blind** — the judge is not told which output came
from which version.

**Nobody says the author may not write the assertions.** Every documented workflow
has the author (or "Claude A") drafting them, and the circularity is never named.

## Skill types — two taxonomies, neither is technique/reference/workflow

**By invocation** (Claude Code docs): *reference content* runs inline alongside
conversation context; *task content* is step-by-step and often
`disable-model-invocation: true`. The consequence is frontmatter, not body shape.

**By use case** (PDF guide): Document & Asset Creation · Workflow Automation ·
MCP Enhancement, each with different "key techniques".

**Type does change testing**, from skill-creator:

> "**Skills with objectively verifiable outputs (file transforms, data extraction,
> code generation, fixed workflow steps) benefit from test cases. Skills with
> subjective outputs (writing style, art) often don't need them.**"

## Triggering and collisions

Only one cross-skill disambiguation example is published — a negative trigger
naming the sibling by name:

> `description: Advanced data analysis for CSV files... Do NOT use for simple data
> exploration (use data-viz skill instead).`

Anthropic notes the failure runs the *other* way by default: *"currently Claude has
a tendency to 'undertrigger' skills... **make the skill descriptions a little bit
'pushy'.**"*

And a triggering mechanic that explains a whole class of apparent mis-fires:

> "**Claude only consults skills for tasks it can't easily handle on its own —
> simple, one-step queries like 'read this PDF' may not trigger a skill even if the
> description matches perfectly**, because Claude can handle them directly."

## PRACTICE — 11 shipped skills, measured 2026-08-30

Evidence of what Anthropic does. It deviates from the above freely.

| Skill | Words | Lines | Desc chars | Bundled dirs | Fetches at runtime? |
|---|---|---|---|---|---|
| `public/pdf` | 1,007 | 314 | 437 | `scripts/` + `FORMS.md`/`REFERENCE.md` **at root** | no |
| `public/docx` | 956 | 91 | 837 | `scripts/` | no |
| `public/pptx` | 3,184 | 241 | 962 | `scripts/` | no |
| `public/xlsx` | 1,279 | 99 | 952 | `scripts/` | no |
| `examples/skill-creator` | 5,166 | 485 | 319 | `agents/ assets/ eval-viewer/ references/ scripts/` | no |
| `examples/mcp-builder` | 1,141 | 236 | 277 | **`reference/`** (singular) `scripts/` | **yes** |
| `examples/deep-research` | 1,420 | 135 | 570 | `references/` | no |
| `examples/algorithmic-art` | 2,746 | 404 | 324 | **`templates/`** | no |
| `examples/web-artifacts-builder` | 439 | 73 | 288 | `scripts/` | no |
| `examples/brand-guidelines` | 329 | 73 | 236 | none | no |
| `examples/internal-comms` | 211 | 32 | 329 | `examples/` | no |

Findings:

1. **Eleven skills, eleven different heading sets.** No shared skeleton. None uses
   the PDF template.
2. **Body length varies 25×** (211 → 5,166 words). None exceeds 500 lines.
3. **Description length varies 4×** (236 → 962 chars). All inside 1,024.
4. **Directory names are not standardised.** Across all 37: `scripts`,
   `references`, `reference`, `templates`, `assets`, `examples`, `agents`,
   `eval-viewer`, `core`, `themes`, `canvas-fonts`, `paintkit`. `pdf` puts the
   spec's own `REFERENCE.md` filename at the skill *root*.
5. **Runtime fetching is rare but real** — only `mcp-builder`, which WebFetches
   `modelcontextprotocol.io/sitemap.xml` and a GitHub README as part of its
   workflow. Everything else is self-contained. **This is the measured answer to
   "does a skill fetch its own domain knowledge": almost never — it is bundled at
   authoring time.**
6. **Zero of 37 skills ship `evals/evals.json`** — including skill-creator, which
   defines the schema. Verified by `find /mnt/skills -name "evals.json"` → empty,
   and against the public repo listing.
7. **Anthropic breaks its own tone rules.** `algorithmic-art` uses all-caps
   headings and emoji; `xlsx` uses "mandatory"; `pptx` uses "QA (Required)" —
   against skill-creator's own warning that all-caps ALWAYS/NEVER "is a yellow flag".

## What Anthropic does not say

Confirmed gaps, not assumed ones:

1. No required body headings, sections or ordering. One recommended template,
   followed by none of their own skills.
2. No rule for what comes first beyond "critical instructions at the top".
3. No technique/reference/workflow trichotomy; the two published taxonomies do not
   map onto it.
4. No procedure for differentiating two skills that both legitimately claim a
   request, and nothing on auditing a library for collisions.
5. No pass threshold, failure budget or significance test — stated as deliberate.
6. No statement that the author may not write the assertions.
7. No built-in runner for the best-practices eval format — stated explicitly.
8. Two eval schemas that do not reconcile, plus an `expectations`/`assertions`
   field-name inconsistency inside Anthropic's own material.
9. No maximum reference-file size, no cap on bundled file count. TOC threshold
   given as both 100 and 300 lines.
10. No guidance on runtime network fetching from inside a skill — whether it is
    acceptable, how to handle failure, when to prefer bundling. `mcp-builder`
    does it; nothing documents it.
11. No versioning or deprecation story for a skill whose bundled references go
    stale.
12. Conflicting body-length targets (see above), unreconciled.
13. Conflicting voice guidance: `plugin-dev` mandates imperative and forbids
    second person; current `skill-creator` warns against "heavy-handed musty
    MUSTs" and prefers explaining why. Neither acknowledges the other.

## What could not be reached

- `pdftotext`/`pdftoppm` absent on this machine; the system `cryptography` module
  is broken (`pyo3_runtime.PanicException`), which killed `pypdf` and
  system-python `pdfminer`. Extraction used `pdfminer.six` in a venv. The guide is
  **two-column**, so p.12's template was recovered by column-ordered element
  sorting and its **heading levels are inferred**, not read.
- `github.com/anthropics/skills` is not attached to this session (MCP: "repository
  not configured"). The skill-creator listing was verified via WebFetch of the
  GitHub HTML page and matches the local copy; the repo was not enumerated
  through the API.
- The `claude.com/blog` skill-creator post returned as a tool-generated summary,
  not verbatim. Nothing load-bearing rests on it.
- `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` was not
  fetched separately. best-practices reproduces its frontmatter constraints
  inline, but the overview may carry structure language not seen here.
- No Anthropic *engineering* blog post about skills was located. Not claiming one
  does or does not exist.

## This page is where the guide gets graded, and one more page defers to it

[[agent-builder-prior-art]] cites the same 33-page guide and, as of 2026-09-12, labels it
**FIRST-PARTY** rather than AUTHORITATIVE, deferring the per-item verdicts to this page. That is the
right split and worth stating from this end too: *first-party* is a fact about the publisher and
needs no grading; *authoritative* is a claim about the contents, and this page is the only place
where the contents were checked claim by claim — which is how the guide's body template came to be
recorded as followed by **0 of 11** shipped skills, and its 5,000-word cap retracted. A page that
cites a first-party document should point at whoever graded it rather than grade it again in
passing.

## The extraction that produced this page IS repeatable — and nothing needs installing

The source entry above records the guide as *"Downloaded and text-extracted with pdfminer.six"*,
with the page count re-measured *"on a fresh download with pypdf"*, on 2026-09-04. A probe on
2026-09-12 found neither working in this container, and this section originally read *"cannot be
repeated here"* on that evidence. **That heading was wrong within the day.**

**The cause was one poisoned dependency, not a missing toolchain.** The system `pypdf` is **6.17.0**
— present and current. What is broken is the *system* `cryptography`, whose Rust binding needs an
absent `_cffi_backend`; `pypdf` reaches it on import and the failure arrives as a Rust
`PanicException` rather than an `ImportError`, so its own fallback never fires. In a virtualenv with
`include-system-site-packages = false` there is nothing poisoned to reach, and the guide reads:
**33 pages, 35,733 characters** concatenated (35,765 if the pages are newline-joined — the same
number, stated with its convention, after the first write-up gave it without one).

**And the version was not the variable either.** The first demonstration used `pypdf` 6.18.1, which
left a version bump as an untested confound. The control is the *same* version isolated: **6.17.0 —
the system's own — reads what 6.17.0 system-wide panics on.** Same version, two outcomes, one
variable.

**So the question this section used to leave standing for the human is WITHDRAWN.** It read *"should
we restore a PDF toolchain this base's own provenance depends on"*. There is nothing to restore and
nothing to install; the fourth gate has nothing to weigh. What the capability cost was one command.

What it bought, immediately: this page's own claims re-checked against the document (below), the
`skill-anatomy` contradiction settled (the guide's `/CreationDate` is 2026-01-26 and `pass_rate`
appears nowhere in it: **stale, not false**), and the p.12 template read rather than inferred.

`knowledge/pdftext.py` is not retired by any of this. It gets **17.6%** of this guide out with the
standard library alone and refuses to hand that back as a document, and it is what CI runs, because
it needs neither virtualenv nor wheel. See `pipeline/decisions/2026-09-11-stdlib-pdf-text.md`.

## Re-verified against the guide itself, 2026-09-12

Every string this page quotes from the PDF was matched against the extracted text. **All present
verbatim** — *"Keep SKILL.md under 5,000 words"*, *"Instructions not followed"*, *"Writing the main
instructions"*, *"critical instructions at the top"*, and the p.25 block quoted above including
*"Use `## Important` or `## Critical` headers"*. Two claims changed shape rather than truth value,
and both are recorded at the sections that make them.
