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
    note: "30 pp. Downloaded and text-extracted with pdfminer.six. TWO-COLUMN layout — p.12's body template was recovered by column-ordered element sorting; heading levels there are INFERRED from extractor artefacts, not read directly."
    fetched: 2026-08-30
  - url: "local: /mnt/skills/ (37 shipped Anthropic skills) and claude-plugins-official marketplace (plugin-dev/skill-development, skill-creator)"
    note: "Read and measured directly. Evidence of PRACTICE, not of stated rules."
    fetched: 2026-08-30
status: verified
verified_by: "Dedicated research pass 2026-08-30, sources fetched that day; unreached sources listed at the foot of this note. Not independently re-verified by a second party."
tags: [skills, authoring, anthropic, evals, baseline, progressive-disclosure]
related: ["[[skill-anatomy]]", "[[skill-authoring-best-practices]]", "[[skill-authoring-eval-methodology]]", "[[testing-skills-methodology]]", "[[agent-design-template]]"]
---

# Anthropic's skill authoring contract

What Anthropic **states** about writing and evaluating a skill, separated from what
Anthropic **does**. Written after a decision to treat Anthropic as the authority,
because they own the runtime the skills execute in.

[[skill-anatomy]] holds the frontmatter fields, the loading mechanics and the
hard rules. This note holds the body, the bundled files, the evals and the
baseline — and marks where Anthropic says nothing.

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

### Body length — three incompatible numbers, unreconciled

| Source | Value |
|---|---|
| best-practices · Claude Code docs · spec checklist | **"under 500 lines"** (stated four times across sources) |
| agentskills.io spec, progressive-disclosure table | **"< 5000 tokens recommended"** |
| `plugin-dev/skill-development` | **"<5k words"**, target **1,500–2,000 words**, soft cap 3,000 |
| PDF guide | "Keep SKILL.md under 5,000 words" |

**No Anthropic source reconciles these.** [[skill-anatomy]] previously called
5,000 words "authoritative"; that was one source among four and the 500-line
figure is the more frequently stated. Corrected there 2026-08-30.

Measured practice: 11 skills range **211 → 5,166 words** and **32 → 485 lines**.
None exceeds 500 lines.

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
