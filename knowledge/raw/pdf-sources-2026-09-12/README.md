# One PDF held because a citation was pinned, 2026-09-12

| file | cited by | bytes | sha256 |
|---|---|---|---|
| `arxiv.org_pdf_2605.17193v1.pdf` | `llm-idea-generation` | 4,076,663 | `edde49ce22de86ac25ad4d676f9003afec5c11513bee35438ca8db965322abe7` |

## Why a second copy of a paper this layer already holds

It is not a second copy. `knowledge/raw/pdf-sources-2026-09-11/arxiv.org_pdf_2605.17193.pdf` was
fetched from the **unpinned** URL and is therefore whatever arXiv served that day — which turned
out to be a revision titled *"(NMI Revision)"*, 93 pages. The claims in
`knowledge/notes/llm-idea-generation.md` were taken from **v1**, 64 pages, and match it exactly:
twelve interventions, 45 tested conditions, 62 baseline comparisons, seven foundation models. The
revision says thirteen, 73, "all baseline comparisons" with the count removed, and 10.

So the note's source URL was pinned to `…/2605.17193v1`, and pinning a citation this repo cannot
produce would have been the emptier half of the fix. This file is the other half: **the document
the claims actually rest on.**

Both copies stay. The 09-11 file is the current paper, correctly fetched; this one is the cited
reading. A page whose figures differ between them now has both in front of it, which is the only
arrangement under which the difference is checkable rather than merely asserted.

## Not watched

`arxiv.org/pdf/<id>v1` **is** immutable — that is the whole reason for pinning it. Unlike the
unpinned sibling, the original justification is true of this URL.

The prefix is declared in `watch.py`'s `NEVER_WATCHED` so the offline accounting sees it.

## Provenance

Fetched 2026-09-12 with `curl -sSL https://arxiv.org/pdf/2605.17193v1` (HTTP 200, 4,076,663
bytes), verified to start with `%PDF-`, sha256 above. Read with `pypdf` in an isolated virtualenv:
64 pages, 146,614 characters, `/Title` *"Multi-LLM Systems Exhibit Robust Semantic Collapse"* with
no revision marker. Never edited, in keeping with the raw layer's rule.

## The sweep the finding demanded — all five held arXiv PDFs against their v1

One revised paper is an anecdote. Every held arXiv PDF was therefore re-fetched at `<id>v1` and
compared by sha256 on the same day.

| held file | vs `<id>v1` | what the difference is |
|---|---|---|
| `2106.09482` | **identical** | — |
| `2402.01727` | **identical** | — |
| `2606.12071` | **identical** | — |
| `2310.01798` | **differs** | 19 pp → 17 pp. The revision **added** evidence: v1 contains neither `62.0` nor `36.5`, the Llama-2 GSM8K figures `llm-idea-generation` cites |
| `2605.17193` | **differs** | 64 pp → 93 pp, *"(NMI Revision)"*. The revision **changed** four figures that note cites |

**Two of five held copies are not the v1 their unpinned URL once served — 40% of the sample.** The
exposure is not a quirk of one preprint.

And the two differ in *direction*, which is the part worth keeping. Kong et al. changed figures a
note had already recorded; Huang et al. added a row a note now cites, which means the note's claim
is true of the held copy and **not** of v1. Drift runs both ways, so "is our copy current?" and "is
our copy the one we read?" are two questions and neither answers the other.

Nothing else needs a pin. `2310.01798`'s claims were re-verified against the **held** copy on
2026-09-11 and match it; the held copy is the current paper, and that is the correct thing to cite.
Only `2605.17193` had a note resting on a reading its URL no longer serves, which is why it is the
only one pinned and the only v1 held here.
