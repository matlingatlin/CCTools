---
title: Raw layer — BASELINE bytes for change detection, not evidence of what was read
imported: 2026-09-04
status: RAW — never edited. Read the warning below before citing anything here as provenance.
---

# What this directory is, and the one thing it is NOT

These are the bytes of fifteen still-fetchable sources **as of 2026-09-04**. They exist so
`knowledge/watch.py` can answer "has this page changed since?" for notes that had no raw copy at
all — 31 of 43 sourced notes, because the raw layer only began on 2026-09-02.

**They are NOT the bytes the citing notes were written from.** Those notes were written on
2026-08-27 and 2026-08-30 against pages that have had a week to move, and today's evidence says
that is not hypothetical: four Claude Code doc pages changed within *hours* of a morning fetch.
So a baseline here:

- **can** tell us from now on that a page moved and a note is owed a re-read;
- **cannot** verify a single existing claim, and must never be cited as though it were the
  source the note quoted.

That is why the citing notes' `raw:` keys still say no bytes were kept, and name this directory
separately as a baseline. Conflating the two would manufacture provenance, which is a worse
failure than admitting we have none.

## What is deliberately NOT baselined

**33 source URLs on `doi.org`, `arxiv.org` and `usenix.org` are not watched, on purpose.** A
published paper with a DOI or an arXiv identifier does not change under its own identifier; a
new version gets a new one. Change detection over an immutable object is a check that can only
ever return "same", which is worse than no check, because a wall of green implies the whole base
is watched. The watch list is *every source that can move*, not every source.

GitHub repository pages and Hugging Face model cards (about 36 URLs) can move and are not
baselined yet — the next batch, not a decision against them.

## The second batch (2026-09-04, same day): what a source is watched AS

Fifty-seven more sources baselined. The rule that matters is not "fetch the URL" but **watch the
form that carries the claim**:

| Source shape | Watched as | Why |
|---|---|---|
| a GitHub repo page (19) | `raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md` | the repo page changes on every star and every "last commit" timestamp; the README is what the notes quote |
| a GitHub `blob` link (7) | the same file's raw URL | same reason, one file deep |
| a Hugging Face model page (11) | `…/raw/main/README.md`, the model card | the model page carries download counters |
| a plain article or vendor doc (19) | the page itself | no raw form exists, and a blog does not churn like a repo page |

## Never watched, and why — 47 sources

**39 are immutable**: `doi.org`, `arxiv.org`, `usenix.org`, university and vendor PDFs, and the
Anthropic skills guide PDF (its own `ModDate` is 2026-01-26 and has not moved). A published work
does not change under its identifier; watching one can only ever return "same".

**7 are volatile by design**: `x.com`, Threads, a YouTube playlist, the Chrome Web Store, an
`artificialanalysis.ai` leaderboard, and two gists. Their bytes change without their claim
changing, which is the definition of a signal that cannot be read.

**1 is an issue thread**: it changes with every comment, and the note cites a state of the
discussion rather than the page.

## Four baselines were fetched and then DROPPED from the watch list

`openrouter.ai/docs/api-reference/limits`, `stevescargall.com/blog/…graphify-memmachine…`,
`the-decoder.com/…unlimited-ocr…` and `anthropic.com/engineering/managed-agents` returned
**different bytes on two fetches seconds apart**. A baseline that reports CHANGED every run is
worse than no baseline: it trains the reader to ignore the watcher. Their bytes are kept here as
a dated snapshot; they are simply not watched.

**The honest limit of that test.** One double-fetch can PROVE instability and can never prove
stability — `anthropic.com/engineering/managed-agents` came out unstable in the full sweep while
its sibling page had passed the same test minutes earlier, so the property is intermittent.
Four more pages could not be re-fetched during the sweep at all (the rapid double request appears
to have tripped rate limits, minutes after they fetched cleanly), so they are untested rather
than unstable, and stay watched. The remaining rows are "not shown to be unstable", which is
weaker than stable. The first weeks of running `watch.py` are the real test: a row that reports
CHANGED with no content difference gets dropped then, for the same reason these four were.

> **Superseded 2026-09-08.** All four are watched again, and no row was dropped to get there.
> `watch.py` now separates a byte change from a CONTENT change, so a page whose bytes move while
> its visible text does not reports `noise` instead of `CHANGED` and does not fail the run. Re-
> tested that day: all four are byte-different and visible-text identical (prose 1.5%–37.3% of the
> page), so they were never unstable in the part any note cites. `anthropic.com/engineering/
> managed-agents` came back byte-*stable*, which is the case this section's own next paragraph
> warned about — it was dropped on an intermittent property. The paragraph above is kept as
> written because it was the right call on the evidence then; the prediction it makes in its last
> sentence is the one thing that did not happen. See `knowledge/raw/watch-2026-09-08c/`.

## Five baselines removed the same day, and why that is not a raw-layer deletion

The raw layer's rule is that nothing here is edited or deleted, because notes cite it. These five
files were cited by nothing and watched by nothing, and both facts were true within hours of their
being fetched:

- `openrouter.ai/docs/api-reference/limits`, `anthropic.com/engineering/managed-agents`,
  `the-decoder.com/…unlimited-ocr…` and `stevescargall.com/…graphify-memmachine…` — the four that
  returned **different bytes on two fetches seconds apart** and were dropped from the watch list.
- `pypi.org/project/graphifyy/` — the rendered page, dropped in favour of the JSON API, which
  carries the same fact without download counters that move when the version does not.

A baseline that is not watched performs no change detection, and a baseline is never provenance -
it is today's bytes for a page a note was written against earlier. So these carried neither job.
0.8 MB on disk, and the decision is written here instead of the files sitting
unexplained. The rows that replaced them - the four dropped from `WATCH.tsv`, and the PyPI JSON -
are recorded above with their reasons.
