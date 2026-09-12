# `CURATION-LESSONS.md` has been diluted — measured 2026-09-12, and the filename invited it

**APPLIED 2026-09-12, option 1.** The measurement and the triage below stand as written; what
follows the options section records what was actually done.

## The measurement

| | |
|---|---|
| file | `pipeline/CURATION-LESSONS.md`, **1,198 lines / 109 KB** |
| its stated purpose | *"The ONE shared store of **'how to write good tests'** for the WHOLE system"* |
| its stated readers | `library-curator` **and** the loop's TEST step, *"before authoring tests"* |
| top-level entries by date | 08-27: 6 · 08-28: 22 · 09-04: 5 · **09-08: 27** · **09-11: 31** · **09-12: 22** |
| of 2026-09-12's 22 entries, how many touch test or verification discipline | **3** |

So **19 of 22 entries added on 2026-09-12 are not about authoring tests** — they are about watcher
cadence, a PDF toolchain regression, a graph being a forest, re-baselining discipline, PageRank's
teleport term, a vendor's installer wording. Good content; wrong reader. The same pattern holds for
the 09-08 and 09-11 batches, so the dilution is roughly **80 entries deep, not 22**.

**What it costs.** A test author — human or agent — is instructed to read this file *before* writing
tests. They now read a session journal to find the three directives addressed to them. That is the
`steering-doc-pruning` failure exactly: a document with a named reader, diluted until the reader pays
for content addressed to someone else.

## The root cause is the filename, and it predates this session

The header says **`# TEST-AUTHORING LESSONS`** and then explains: *"(File name kept as
`CURATION-LESSONS.md` for stable references.)"* So the file is named for one job and headed for
another. **A writer looking for where curation lessons go greps the filename and lands here**, reads a
header about tests, and appends anyway because the name says this is the place. That is not a careless
reader; it is a name that misroutes one.

Worth stating plainly because this repo has a talent for exactly this — `capability-routing-table`
exists to find *"units that cannot be invoked at all, units that fell out of the table"* — and the same
question applied to files rather than skills would have caught it: **which file owns "a lesson about
running the knowledge base"?** Today the answer is "the one named for it, which is about something
else."

## Three options, and the cost of each

1. **Rename the file to `TEST-AUTHORING-LESSONS.md` and create `CURATION-LESSONS.md` for what its name
   promises.** Fixes the cause. Breaks every existing reference — and the header says references are
   exactly why the name was kept. Needs a sweep of `.claude/skills/**`, `pipeline/**` and the notes.
2. **Keep the name, split the content**: leave test directives here, move the ~80 journal entries to
   `pipeline/OPERATING-JOURNAL.md`, and put a routing line at the top of each. Cheapest for readers,
   and leaves the misrouting name in place to catch the next writer.
3. **Keep one file, add an index and section it** — test directives first, journal below a fold. No
   moves, no broken references, but a 109 KB file that a test author still loads in full.

**Recommendation: 1, with 2 as the fallback if the reference sweep is judged too wide.** The name is
the cause, and options 2 and 3 both leave it armed.

## What was done — option 1, applied the same day

The user's instruction was to fix the open items, which closed the human gate this proposal was
waiting on.

1. **`git mv pipeline/CURATION-LESSONS.md pipeline/TEST-AUTHORING-LESSONS.md`.** The name now
   matches the header, and the parenthetical that kept the old name *"for stable references"* is
   gone along with the warning block that admitted the disagreement.
2. **Split at the structural seam, not by hand-classifying 120 bullets.** The file already had one:
   lines 1-330 were the header, the 33 `ACTIVE DIRECTIVES` bullets (all five `seed` plus every
   `2026-08-27` and `2026-08-28` entry) and the SIGNALS and HEALTH SCORECARD tables; from the
   `## 2026-08-28 · Curator-batch` heading onward were 872 lines holding all 87 journal bullets.
   **The `ACTIVE DIRECTIVES` section was never diluted** — that is worth recording, because the
   measurement above counted `[date]`-tagged entries across the whole file and the dilution was
   entirely below the seam. Directives above it, journal below, and the cut needed no judgement
   call per entry.
3. **Nine journal entries promoted into the directives**, restated for a test author and each
   citing its date in the journal: mutation survivors as questions, a frozen rather than live-
   computed threshold, the oracle-weakening check, testing the wiring and not only the predicates,
   asserting the primary output path with stdout *and* stderr *and* the exit code, asking what a
   defect scoring 100% would look like, testing every absolute, preferring a property test to an
   enumeration, and asserting the post-state of a string edit. This is the part a pure move would
   have lost: those nine were addressed to a test author and were sitting where no test author
   reads.
4. **Both files got a routing header** naming the other and stating which reader each serves, so
   the next writer is told where their entry goes before they append.
5. **17 live references swept** across `.claude/skills/piano/SKILL.md`,
   `.claude/skills/library-curator/SKILL.md`, `pipeline/BRAIN.md`, `pipeline/DATA.md`,
   `pipeline/STATUS.md`, `templates/EVALS.template.md`, `templates/README.md` and both
   `pipeline/workflows/*.js`. Each was judged rather than substituted: a reference meaning *"the
   directives to apply before writing tests"* now points at `TEST-AUTHORING-LESSONS.md`, and one
   meaning *"the curator's own store"* still points at `CURATION-LESSONS.md` — which the split made
   **more** accurate, not less, since the curator's operating journal is exactly what that file now
   holds.
6. **Deliberately not rewritten:** `.claude/skills/*/evals.md` records, the contract fixtures under
   `pipeline/packages/fixtures/`, the build artefacts under `pipeline/builds/`,
   `pipeline/metrics.jsonl`, and the historical log lines in `STATUS.md` and
   `pipeline/decisions/2026-09-11-stdlib-pdf-text.md`. Each is a record of what a run actually saw,
   and **a fixture asserting specific content is the one thing a rename must not chase** — editing
   one to match would weaken the test it exists to be. They name the old path because the old path
   is what was true then. Both new files say so at the top.

**The concern the proposal raised was the reference sweep's width, and it was 17 lines in 9 files** —
narrower than the header's *"stable references"* worry implied, because most of the 40-odd matches
were in records rather than instructions.
