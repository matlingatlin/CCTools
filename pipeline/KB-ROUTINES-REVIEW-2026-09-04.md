---
title: The knowledge base's routines, thought through
date: 2026-09-04
status: review — findings measured, two decisions open
---

# The knowledge base's routines, thought through

A review of the PROCEDURES that govern `knowledge/`, not of its content. The content was
cleaned earlier today (lint 0/0, contradictions 0). This asks the different question: **when do
these routines run, what checks them, and what have we actually seen fail?**

## The routines as they exist

| Routine | Defined in | What triggers it | What checks it | Enforced |
|---|---|---|---|---|
| Ingest a source | `llm-wiki-ingest` (7 steps) | someone noticing a verified fact | `kb.py lint` at step 7 | no |
| Clean the base | `kb-curator` agent | someone asking | `lint --json`, now `contradictions` | no |
| Register | INDEX · SOURCES · MANIFEST · frontmatter | ingest step 6 | lint (unlisted, orphan, schema) | partly |
| Freshness | `kb.py stale` | nothing | 90-day bar | no |
| Contradictions | `kb.py contradictions` | curator step 1 (as of today) | 3 fixtures in `selftest` | no |
| Telemetry | `DATA.md` | pass end | nothing | no |
| Carry lessons | `BRAIN.md` | loop start/end | nothing | no |

## Finding 1 — every routine is a convention, and nothing fires it

**Measured 2026-09-04:** no CI workflows in the repo, no active git hooks (`.git/hooks` holds
only samples), and no cron or trigger that runs `kb.py`. The lint exits 1 on errors and
**nothing calls it.** The talent loops have a schedule; the knowledge base has a human.

This is not a new class of defect here. `CLAUDE.md` says of the agent cap: *"This is a
convention, not a gate: no code enforces it... It is therefore the weakest defence in this repo,
and the one most likely to fail again."* Every KB routine sits in that same position, and today
produced three fresh instances of the prediction coming true: the curation pass wrote no
`metrics.jsonl` row until hours later, `BRAIN.md` went a week without the update its own contract
requires, and the base sat unlinted between sessions. None of these were forgotten rules — they
were rules nobody was asked to run.

## Finding 2 — a note and its raw are not connected by anything a machine can follow

This one was found by **failing to measure it.** Three defensible methods for "how much of what
the notes cite is kept in the raw layer" gave:

| Method | Answer |
|---|---|
| source URL appears in a raw file's text | **11%** |
| URL or its last path segment appears in raw paths, MANIFEST, or SOURCES | **61%** |
| URL named in the raw layer's own provenance (MANIFEST / raw READMEs) only | **0%** |

Sixty-one points of spread, because **there is no join key.** A note's frontmatter carries
`url` and `fetched`; nothing carries the path of the raw copy. `llm-wiki-ingest` step 1 says to
keep the raw and record provenance "in the directory's manifest rather than inside the immutable
file" — so the link exists only as prose, in a different file, in whatever words that day's
writer chose.

Consequences, in order of seriousness: the rule **cannot be checked** (no lint can say a note
kept its raw); the raw **cannot be found** from the note that needs it; and a claim of coverage
cannot be defended, as the table above demonstrates against itself.

The knowledge base wrote the lesson for this defect this morning, about someone else's tool:
*"a page whose source cannot be opened from the page is a stub with a footnote."* The same
sentence is true one level up, about these notes and their raw.

## Finding 3 — the freshness clock is the wrong clock

**Measured:** 0 notes are past the lint's 90-day bar; 35 of 44 verified notes have no fetch
newer than three days. So `stale` will report nothing for roughly three more months.

Also measured, today: eight days produced **no wrong value** in the six Claude Code mechanics
notes — and one **inverted claim** (a limit the note called undocumented had become documented)
plus four missing details. Age did not predict any of it. What invalidates a note is an upstream
**release**, and the calendar cannot see one. A green `stale` is currently evidence of nothing.

## What follows

Cheap and clearly right (not done here — it touches 44 notes' schema, so it is a decision):
a `raw:` field in note frontmatter, and a lint rule that a verified note citing a URL either
names its raw path or says in one clause why none exists. That converts Finding 2 from
unmeasurable to a lint line.

Also cheap: fold `build → lint → contradictions → selftest` into one `kb.py check` with one exit
code. A routine you have to remember in four parts is four chances to skip one, and today I
skipped `contradictions` after edits until I remembered it existed.

**All three findings were closed the same day.** Findings 1 and 2 as proposed: CI
(`.github/workflows/kb-check.yml`) runs `kb.py check` on every push touching `knowledge/`, and
every verified note now carries a `raw:` key the lint requires, which turned the unmeasurable
11/61/0% spread into 12 of 43.

**Finding 3 was closed with a different design than this file proposed, and the measurement is
why.** The proposal was a release clock: record per source what would invalidate it. Measured
first: 18 notes cite a watchable source and exactly **2 pin a version** to compare against, both
for the same package. A version clock would have had almost no surface.

So the signal became the more general one — **have the bytes we read changed?** — which needs no
version, works for any URL, and uses the raw layer as its baseline, connecting Finding 3 to
Finding 2's join key. `knowledge/watch.py` re-fetches every source in `knowledge/raw/WATCH.tsv`
and compares sha256 against the bytes we hold.

**Its first run, hours after the morning fetch, found 5 of 10 sources changed** — checked before
believed, and the diffs were real content, not a nondeterministic header: nested `.claude/skills/`
do not load at startup, `/skill-doctor` now measures per-skill context cost and invocation count,
`--append-subagent-system-prompt-file` at v2.1.261 (29 releases above the highest version this
base cites), and removing a remote MCP server deletes its OAuth tokens. Three notes were updated.
One of the five was a Discord invite link and material to nothing, which is the watcher's honest
shape: it detects that bytes moved, never that a claim did.

`kb.py stale` is left in place and left alone. It answers a question — how old is this fetch —
that is worth knowing and is not the same question.

## Postscript — the review's own Finding 1, recreated by the review's own fix

`kb.py check` got CI the same day, for the reason Finding 1 gives: a routine nothing fires is a
convention. Then `watch.py` was written and **deliberately excluded** from that job, because the
job is offline and must stay network-free — which quietly left the watcher exactly where the lint
had been that morning: a good check nobody runs.

It now has `.github/workflows/kb-watch.yml`, weekly. A failing run is not a defect in the
repository; it means a source moved and the citing notes are owed a re-read. Unreachable rows do
not fail the job, because a rate limit is not evidence of anything.

**The honest caveat: GitHub runs `schedule:` only on the default branch, so this fires nothing
until the work merges.** Until then the watcher is still a convention, and saying so is the
point — the failure mode this file documents is believing a trigger exists because a file
describing one has been committed.

The general form is worth keeping, because it took one afternoon to reproduce: **a fix for
"nothing runs this" does not generalise to the next thing you build the same day.** Each new
check needs its own trigger named at the moment it is written, or it inherits the defect its
sibling was just cured of.

## The verification queue, and where it stands

With the routines built, three notes were read back against sources actually held. What the pass
found is the argument for repeating it:

| Note | Found |
|---|---|
| `best-local-llm-2026-09` (6 REPEATED, weakest ratio) | a **false absolute** — "loses on every row" is 13 of 14; one row wins |
| `glm-5.3-local` | the base's **oldest named contradiction settled** from `config.json`: 744B is a product label, ~754B the weight count |
| `model-agnostic-agent-harnesses` (9 REPEATED, most) | two claims upgraded to MEASURED; an **ownership move** the note had not seen, which became `kb.py owners` |

**The method that worked**, in the order the steps mattered: read the claim back against the raw
we hold, not against memory; **read the column header**, because a number found on the page is not
yet attributed; and **test every absolute**, because one counterexample ends it and a table offers
as many chances as it has rows. Two of the three passes also dissolved suspicions of mine on
closer reading, which is recorded in the notes — a verification pass that reports only its hits is
not one.

**Where it stands: 55 REPEATED claims across the base.** A crude scan puts at least 8 beyond
reach — their source is a search result, a video, a review or a press mention, none of which was
ever retrievable and none of which is retrievable now. `temporal-kg-agent-memory` was opened and
closed unverified for exactly this reason: its unconfirmed claims are about a product whose
sources we never held, and the one README we do hold belongs to a different project. **Not
checkable is a result, and manufacturing a check for it would be worse than leaving the verdict
REPEATED.**

The remaining ~47 are a long tail rather than a task. It is `kb-curator`'s to continue, one note
at a time, not one session's to grind through.

**The ordering rule was wrong on its first use, and the fix matters more than the queue.** Ranking
by REPEATED count put `subagents` at the top with three claims — and none of them was a reading
job. All three are our own paired measurements at n=3, marked REPEATED to signal *"small sample,
treat with care"*. But `pipeline/contracts/claims.contract.json` defines the verdicts by
**provenance, not confidence**: MEASURED is "the source reports a number it measured itself",
REPEATED is "the source restates a finding measured by someone else", and the contract states
outright that the two "are not strong and weak". Borrowing a provenance label for a confidence job
cost something concrete: it queued work that cannot be done, because there is no source to re-read.

Measured across the base: of 55 REPEATED claims, **18 are the provenance sense**, **4 are the
confidence sense** (our own low-n measurements, three of them corrected here), and **33 cannot be
told apart from the line alone**. So the queue orders by the provenance sense only, and where a
source is actually held — `WATCH.tsv`'s URL-to-path map is the authority for "held", because three
separate crude string-matches lied about it today before that was used.

---

## Postscript, 2026-09-08 — what four days of running produced

**Finding 1 (nothing fires the routines) is still only half-closed, and for one reason: the branch
is unmerged.** GitHub runs `schedule:` on the default branch only, so `kb-watch.yml` has never
fired on a timer and `kb-check.yml` guards only this branch's own pushes. Two CI runs have passed,
both in 8–9 seconds. Until the merge, the routines remain a convention with a workflow file
describing them — which is precisely what this review was written about.

**Finding 2 (a note and its raw shared no join key) held up under use.** `WATCH.tsv` was the
authority for every "is a source held" question asked since, and no third answer appeared. It grew
74 → 79 rows; the watcher has reported **0 changed and 0 unreachable** on every run.

**Finding 3 (the freshness clock was the wrong clock) got its strongest confirmation yet, from a
source that could not change.** The goose and Ornith-1.5 findings below were both invisible to a
byte-watcher *by construction*: a transferred repository serves byte-identical content at both
addresses, and a model card that 401s never yields bytes at all. Neither a calendar nor a content
hash could have raised either. What raised them was a check reading the *shape* of what was
already stored — which is the argument this review made and now has two instances of.

### Two new findings the running produced

**4. A check that reports two populations as one ranks the wrong work — and the review's own
verdict lesson recurred, one layer up.** The related-edge rule reported 212 unargued edges. Split:
**76** are the reciprocal half of an edge argued at the other end, which this repo's
neighbours-name-back rule *creates*; **2** are argued in a source's `note:` field; **134** are the
debt, and they are exactly **67 symmetric pairs** — two notes naming each other, neither saying
why. All 67 are now argued in the note that owns the relation. The general rule, added to
`BRAIN.md`: before trusting a check's ordering, ask what a hit would look like if the system were
working correctly, and see how many hits look like that.

**5. The ordering rule for the REPEATED tail needs a second axis: has an untried surface been
tried?** Ranking by count was already corrected here to rank by provenance sense. Ornith-1.5 came
off the tail entirely on 2026-09-08 not because it was high in any queue but because a **401 from
a rendered page** had been recorded as if it were an answer about the source. The same model card
answers at `/raw/main/`, and the re-read **refuted** the claim two secondary write-ups agreed on
(weights under `deepreinforce-ai`; the HF API returns zero models for that org), upgraded five
others to MEASURED, and surfaced a fact no source had stated — all three models are
vision-language, not text.

The honest floor is unchanged: `best-local-llm-2026-09`'s remaining REPEATED rows are third-party
Elo scores, one hardware review and retail prices. No surface exists for those from here, and
manufacturing one would be worse than the verdict.
