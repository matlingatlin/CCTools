# The PDFs four notes cited and nobody held, 2026-09-11

`agent-builder-prior-art`, `anthropic-skill-authoring-contract`, `skill-anatomy` and
`requirements-discovery` all rest on PDF sources. **Not one was held.** They were read
2026-08-29, before the raw layer existed, and nothing was kept — so four pages cited documents
this repo could not produce. All three URLs still answered on 2026-09-11 (HTTP 206 to a range
request), which made holding them a five-minute job that had been outstanding for two weeks.

| file | cited by | bytes |
|---|---|---|
| `resources.anthropic.com_hubfs_The-Complete-Guide-to-Building-Skill-for-Claude.pdf` | `skill-anatomy`, `anthropic-skill-authoring-contract`, `agent-builder-prior-art` | 561,652 |
| `www.cs.umd.edu_basili_publications_journals_J81.pdf` | `requirements-discovery` | 123,121 |
| `www.microsoft.com_kim-tse-2014.pdf` | `requirements-discovery` | 1,386,731 |

## Five more, added the same day — every PDF this base cites is now held

The three above closed the gap for notes citing `.pdf` URLs directly. A second sweep for arXiv
`/pdf/` forms found **five more cited primaries, none held**, under two notes.

| file | cited by | verdict from `pdftext.py` |
|---|---|---|
| `arxiv.org_pdf_2106.09482.pdf` | `requirements-discovery` | READABLE, 100.0% |
| `arxiv.org_pdf_2310.01798.pdf` | `llm-idea-generation` | READABLE, 100.0% |
| `arxiv.org_pdf_2402.01727.pdf` | `llm-idea-generation` | REFUSED, 0.0% |
| `arxiv.org_pdf_2605.17193.pdf` | `llm-idea-generation` | REFUSED, 0.0% |
| `arxiv.org_pdf_2606.12071.pdf` | `llm-idea-generation` | READABLE, 100.0% |

Two refuse at **0.0%** — every glyph hex-coded, not a single literal string — which is a cleaner
result than the guide's partial 17.6% and means the same thing: not readable **by `pdftext.py`**
without a real PDF library. Five of eight held PDFs are fully readable by it; three are not, and
which is which is decided by a typesetting choice made years before this repo existed.

**Updated 2026-09-12: all eight are readable by a real PDF library after all**, and the library was
present the whole time. `pypdf` fails on import system-wide only because the *system*
`cryptography` reaches an absent Rust binding; in an isolated virtualenv the **same version**
imports and reads every one of these files, including the three `pdftext.py` refuses. That does not
retire `pdftext.py` — a stdlib reader with a coverage guard is still what CI can run with no
dependency — but it does retire the *blocker*, and the three refused documents have now been read.
Full measurement in `pipeline/decisions/2026-09-11-stdlib-pdf-text.md`, third postscript. The reader
itself is `knowledge/pdfread.py` - run `python3 knowledge/pdfread.py --report` to read every file
listed here.

Not watched. The reason first recorded here and in `watch.py` — *arXiv version ids are immutable,
so a change to `arxiv.org/pdf/<id>` is not a thing that happens* — **was wrong, and was measured
wrong on 2026-09-12 by one of these five files.** See the section at the end of this file.

These are the **first binaries in the raw layer**. Everything else here is HTML, markdown, JSON
or TSV. Nothing about the layer's accounting changes — a file is accounted for by being named in
a README like this one — but the *watcher's* assumptions do not survive the jump, which is why
none of these three is in `WATCH.tsv`. See below.

## Held but deliberately NOT watched

A watch row earns its place by producing diffs someone can triage. For these, nobody can.

`watch.py` compares bytes, and falls back to comparing **visible text** when the bytes differ and
the stored copy is HTML — that fallback is the whole reason the `noise` verdict works. A PDF has
no such fallback: its bytes move whenever the producer re-stamps a timestamp or reorders an object,
and the only way to ask "did the *words* change?" is to extract them. `knowledge/pdftext.py`
extracts what it can and measures how much that is, and for the document that matters most it is
**17.6%** — refused. So a PDF row would report CHANGED on a byte shuffle with no way to tell that
from a revision, which is precisely the cry-wolf failure the `noise` verdict was built to end.

The two academic papers read at **100%** and could be watched honestly — with the caveat that 100%
coverage is not 100% fidelity: the reader drops `fi`/`fl`/`ff` ligatures silently, so quotes taken
from them must be matched loosely. It also had to learn that PDF word spaces are kerning numbers and
not characters; before that fix the Kim paper extracted with one space in 74,422 letters while still
reporting full coverage. They are left out anyway,
for the reason recorded on 2026-09-11 about a different row: *watch a source for what its future
changes could still tell you.* A 1981 journal article and a 2014 conference paper are finished
documents; a new version would be a new URL, not an edit to this one.

**Re-entry condition**, so this is recoverable rather than merely decided: if the Anthropic guide
ever reads above `pdftext.COVERAGE_FLOOR`, it becomes watchable on the same terms as any HTML page
and should be added. That is one command to check and needs no judgement.

## Provenance

Fetched 2026-09-11 with `curl -sSL`; all three verified to start with `%PDF-`. Never edited, in
keeping with the raw layer's rule. `pdftext.py` opens them read-only.

## An unpinned preprint URL is a moving source — measured 2026-09-12

`arxiv.org/pdf/2605.17193` is stored here under that name, with no version suffix. **That form
resolves to the latest version**, and the paper has been revised since the note citing it was
written.

| | v1 | the copy held here |
|---|---|---|
| `/Title` | *Multi-LLM Systems Exhibit Robust Semantic Collapse* | *Multi-LLM Systems Exhibit Robust Semantic Collapse (**NMI Revision**)* |
| pages | 64 | 93 |
| bytes | 4,076,663 | 8,681,381 |
| interventions tested | twelve | thirteen |
| conditions | 45 | 73 |
| baseline comparisons | 62 | count removed |
| foundation models | seven | 10 |

`knowledge/notes/llm-idea-generation.md` cited **12 / 45 / 62 / 7** — every one of them correct
against v1. The note was not stale; the source moved under it, and nothing in this repo could
have noticed, because the row was deliberately excluded from watching on the ground that *"arXiv
version ids are immutable."* An id is. **An unpinned URL is not**, and that distinction was the
whole load-bearing part of the exclusion.

What changed, and what deliberately did not:

- `watch.py`'s reason for excluding these five is corrected. The **exclusion stands** — a PDF has
  no visible-text fallback, so a watch row could only report CHANGED with no way to triage it,
  which is the cry-wolf failure the noise verdict exists to end.
- The fix is at the **citation**, not the watcher: cite `arxiv.org/pdf/<id>v1` when a claim rests
  on a specific reading. A version-pinned URL is genuinely immutable, which makes the original
  reasoning true of the form it should have been using all along.
- The held copy is kept as-is. The raw layer is never edited, and a revision is not corruption —
  it is the current document, correctly fetched on 2026-09-11.

The general lesson, which is not about arXiv: **a justification for not monitoring something is a
claim about the world, and it can be wrong in exactly the way the thing it excuses would have
caught.** This one survived a day because nothing tested it. What tested it was reading the file.
