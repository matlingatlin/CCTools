---
title: Raw layer — immutable imports from the other repos and branches, with provenance
imported: 2026-09-02
by: a second session (single writer for this commit)
status: RAW — sources are never edited here; the wiki layer (knowledge/notes/) cites them
---

# knowledge/raw — the raw layer

`knowledge/notes/llm-wiki-pattern.md` names what this knowledge base lacked: a `raw/` layer of
immutable sources the wiki compiles from. This directory is that layer for the project's own
repositories. The first raw import is `intake/2026-08-30-agent-and-skill-material/` (416
files, sha256-verified, `.claude/` renamed to `_claude/`); it is left where it is and this
directory holds only what that import did not: files whose **content hash** was absent from
this branch on 2026-09-02, measured over every branch of all three repositories.

**Rule.** Nothing here is edited, and nothing was deleted at its source. A file is
`<repo>@<branch>@<short-sha>/<original path>`, byte-identical. When a source moves on, a new
directory with the new sha is added; the old one stays, because notes cite it.

**What the inventory found.** By content hash, skills-repo's KB branch already held every
knowledge-bearing file of Scio `main` and of hello-world's seven branches except the ones
below. skills-repo `main` holds only older revisions of files this branch has moved on from;
they are history in git, not imported. Source code (`.py`) was not treated as knowledge and
was not imported; the four library `entry.json` seeds were, because the as-built record argues
about them.

| Repo | Branch | Commit | Files | Bytes |
|---|---|---|---|---|
| Scio | `claude/app-builder-architecture-rc7hdk` | `48d0737` | 20 | 141,965 |
| hello-world | `master` | `bd4f6d7` | 19 | 191,955 |
| hello-world | `claude/kor-den-dxz34c` | `d076a67` | 5 | 19,710 |
| hello-world | `claude/las-och-utfor-otg0qr` | `a4ce143` | 8 | 12,765 |
| **total** | | | **52** | **366,395** |

## Per file

| Source (`repo@branch:path`) | Raw path | sha256 (16) | Bytes |
|---|---|---|---|
| `Scio@claude/app-builder-architecture-rc7hdk:docs/DATA-STORES-THREE-LEVELS-2026-09-02.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/DATA-STORES-THREE-LEVELS-2026-09-02.md` | `fc5e8147671bfa82` | 10,198 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/LIBRARY-SOURCES-2026-09-02.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/LIBRARY-SOURCES-2026-09-02.md` | `828d55c3963bccc0` | 9,996 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/REVIEW-FRESH-EYES-2026-09-02.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/REVIEW-FRESH-EYES-2026-09-02.md` | `6d966850cd86c510` | 27,265 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/TALENTS-CRITICAL-SET-2026-09-02.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/TALENTS-CRITICAL-SET-2026-09-02.md` | `9ecdc3ec01fa26ed` | 16,319 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/TALENTS-THREE-LEVELS-2026-09-02.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/TALENTS-THREE-LEVELS-2026-09-02.md` | `28d9608a6f854632` | 12,846 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0002-two-customers-one-artefact.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0002-two-customers-one-artefact.md` | `269bbd197a480c5b` | 3,558 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0003-one-language.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0003-one-language.md` | `0e898bcd2a23314d` | 2,956 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0004-buy-the-harness.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0004-buy-the-harness.md` | `57f02f2e4e32c740` | 5,238 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0005-five-layers.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0005-five-layers.md` | `36cabd2d07641120` | 3,201 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0006-vertical-slice-first.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0006-vertical-slice-first.md` | `7e93b4c0d32d4213` | 3,531 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0007-evidence-is-the-surface.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0007-evidence-is-the-surface.md` | `dfd2c5e2daf37a2e` | 3,352 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0008-talents-at-three-levels.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0008-talents-at-three-levels.md` | `3c1861f83c791875` | 6,731 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0009-hosted-by-default-buy-out-on-demand.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0009-hosted-by-default-buy-out-on-demand.md` | `bc91ecfa9b0696d9` | 3,343 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0010-data-posture-asked-at-intake.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0010-data-posture-asked-at-intake.md` | `ecfc57452c902e24` | 3,156 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0011-three-stores-not-one-smart-database.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0011-three-stores-not-one-smart-database.md` | `6d125dd52ad128c5` | 5,690 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0012-data-stores-per-level.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0012-data-stores-per-level.md` | `febbacf975dfeaa0` | 5,467 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/0013-commodity-by-reference-asset-by-contract.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/0013-commodity-by-reference-asset-by-contract.md` | `79948bf2c9d92019` | 5,600 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/decisions/README.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/decisions/README.md` | `cafb667a125c738f` | 2,942 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/positions/2026-09-02-cold-position-fable.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/positions/2026-09-02-cold-position-fable.md` | `c963f18d3c3815d9` | 4,538 |
| `Scio@claude/app-builder-architecture-rc7hdk:docs/triage/KB-POINTERS-2026-09-02.md` | `knowledge/raw/Scio@claude_app-builder-architecture-rc7hdk@48d0737/docs/triage/KB-POINTERS-2026-09-02.md` | `2b3ba6893033511b` | 6,038 |
| `hello-world@master:PRODUCTION_READINESS_DIFF.md` | `knowledge/raw/hello-world@master@bd4f6d7/PRODUCTION_READINESS_DIFF.md` | `3af43665c5385ec4` | 21,916 |
| `hello-world@master:PRODUCTION_READINESS_REVIEW.GPT.md` | `knowledge/raw/hello-world@master@bd4f6d7/PRODUCTION_READINESS_REVIEW.GPT.md` | `86ad755d4da57c0e` | 57,316 |
| `hello-world@master:PRODUCTION_READINESS_REVIEW_CLAUDE.md` | `knowledge/raw/hello-world@master@bd4f6d7/PRODUCTION_READINESS_REVIEW_CLAUDE.md` | `c9bfe757c7682248` | 60,014 |
| `hello-world@master:apps/api/CLAUDE.md` | `knowledge/raw/hello-world@master@bd4f6d7/apps/api/CLAUDE.md` | `82614168da59c5a3` | 2,611 |
| `hello-world@master:apps/api/README.md` | `knowledge/raw/hello-world@master@bd4f6d7/apps/api/README.md` | `95975ddce73dc68a` | 2,166 |
| `hello-world@master:apps/app/CLAUDE.md` | `knowledge/raw/hello-world@master@bd4f6d7/apps/app/CLAUDE.md` | `b1d37fbfae89fe2f` | 2,067 |
| `hello-world@master:apps/app/README.md` | `knowledge/raw/hello-world@master@bd4f6d7/apps/app/README.md` | `7733744bed6db325` | 1,277 |
| `hello-world@master:apps/engine/CLAUDE.md` | `knowledge/raw/hello-world@master@bd4f6d7/apps/engine/CLAUDE.md` | `15d1032933f38a41` | 2,935 |
| `hello-world@master:apps/engine/README.md` | `knowledge/raw/hello-world@master@bd4f6d7/apps/engine/README.md` | `203ab00e8d0d1605` | 9,996 |
| `hello-world@master:spikes/design-marking/FINDINGS.md` | `knowledge/raw/hello-world@master@bd4f6d7/spikes/design-marking/FINDINGS.md` | `961a568855eb3cd4` | 8,687 |
| `hello-world@master:spikes/design-marking/README.md` | `knowledge/raw/hello-world@master@bd4f6d7/spikes/design-marking/README.md` | `51267406003ffc6e` | 2,536 |
| `hello-world@master:spikes/local-data/FINDINGS.md` | `knowledge/raw/hello-world@master@bd4f6d7/spikes/local-data/FINDINGS.md` | `1c765ba1b49903cb` | 6,313 |
| `hello-world@master:spikes/local-data/README.md` | `knowledge/raw/hello-world@master@bd4f6d7/spikes/local-data/README.md` | `95e48055501f3db3` | 326 |
| `hello-world@master:spikes/sandbox-marking/FINDINGS.md` | `knowledge/raw/hello-world@master@bd4f6d7/spikes/sandbox-marking/FINDINGS.md` | `e49f8a16eb0c76f8` | 7,840 |
| `hello-world@master:spikes/sandbox-marking/README.md` | `knowledge/raw/hello-world@master@bd4f6d7/spikes/sandbox-marking/README.md` | `e854fcc4125f576b` | 1,583 |
| `hello-world@master:apps/engine/src/scio_engine/library/catalog/booking-feature/entry.json` | `knowledge/raw/hello-world@master@bd4f6d7/apps/engine/src/scio_engine/library/catalog/booking-feature/entry.json` | `6800d6bedf82a81d` | 2,147 |
| `hello-world@master:apps/engine/src/scio_engine/library/catalog/ui-button/entry.json` | `knowledge/raw/hello-world@master@bd4f6d7/apps/engine/src/scio_engine/library/catalog/ui-button/entry.json` | `a40cc3cbf89fe805` | 752 |
| `hello-world@master:apps/engine/src/scio_engine/library/catalog/ui-empty-state/entry.json` | `knowledge/raw/hello-world@master@bd4f6d7/apps/engine/src/scio_engine/library/catalog/ui-empty-state/entry.json` | `8a8c7160741df04e` | 723 |
| `hello-world@master:apps/engine/src/scio_engine/library/catalog/ui-field/entry.json` | `knowledge/raw/hello-world@master@bd4f6d7/apps/engine/src/scio_engine/library/catalog/ui-field/entry.json` | `54a3aa8050a03f0d` | 750 |
| `hello-world@claude/kor-den-dxz34c:README.md` | `knowledge/raw/hello-world@claude_kor-den-dxz34c@d076a67/README.md` | `5b5321a952f18c21` | 59 |
| `hello-world@claude/kor-den-dxz34c:docs/BACKLOG.md` | `knowledge/raw/hello-world@claude_kor-den-dxz34c@d076a67/docs/BACKLOG.md` | `c9a51adc4a4adeed` | 757 |
| `hello-world@claude/kor-den-dxz34c:docs/CHANGELOG.md` | `knowledge/raw/hello-world@claude_kor-den-dxz34c@d076a67/docs/CHANGELOG.md` | `8d772a481ea8f10f` | 207 |
| `hello-world@claude/kor-den-dxz34c:docs/PROJECT-PLAN.md` | `knowledge/raw/hello-world@claude_kor-den-dxz34c@d076a67/docs/PROJECT-PLAN.md` | `a242dda7be6d810b` | 18,501 |
| `hello-world@claude/kor-den-dxz34c:docs/ROADMAP.md` | `knowledge/raw/hello-world@claude_kor-den-dxz34c@d076a67/docs/ROADMAP.md` | `de5db0b225b0eace` | 186 |
| `hello-world@claude/las-och-utfor-otg0qr:CLAUDE.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/CLAUDE.md` | `45734f7b0299a540` | 2,187 |
| `hello-world@claude/las-och-utfor-otg0qr:README.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/README.md` | `fddde0cdbdec3c12` | 714 |
| `hello-world@claude/las-och-utfor-otg0qr:docs/ARCHITECTURE.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/docs/ARCHITECTURE.md` | `48fe9ed028dbaf98` | 1,127 |
| `hello-world@claude/las-och-utfor-otg0qr:docs/BACKLOG.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/docs/BACKLOG.md` | `2a5a4caee862654e` | 721 |
| `hello-world@claude/las-och-utfor-otg0qr:docs/PRD.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/docs/PRD.md` | `e1173d38acfc6098` | 5,128 |
| `hello-world@claude/las-och-utfor-otg0qr:docs/ROADMAP.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/docs/ROADMAP.md` | `6d1b41b2b5346308` | 1,790 |
| `hello-world@claude/las-och-utfor-otg0qr:docs/SECURITY.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/docs/SECURITY.md` | `43a7fef5794941f1` | 644 |
| `hello-world@claude/las-och-utfor-otg0qr:docs/decisions/README.md` | `knowledge/raw/hello-world@claude_las-och-utfor-otg0qr@a4ce143/docs/decisions/README.md` | `15d1ae8319ee472c` | 454 |

## Reproducing this

```
sha256(git -C <repo> show origin/<branch>:<path>)  ==  sha256(<raw path>)
```

## What is deliberately not here

- Scio's `docs/as-built/graph/graph.json` (5.5 MB) — already under `intake/…/scio/`, and it
  regenerates from the predecessor's source with `graphify` at zero model cost.
- `scio.db` — an index rebuilt from files, never a source; `knowledge/kb.py` is its
  successor here and indexes this whole repository.
- hello-world application source. The as-built documents under `intake/…/scio/docs/as-built/`
  were written so that the source need not be opened.

## Added 2026-09-04 — `instagram-graphify-obsidian-2026-09-04/`

A third kind of raw: a social-media carousel received as screenshots, plus the pages fetched to
check it. Directory `README.md` carries the provenance and the honest limits; `slides.md` is the
on-screen text of the 16 frames received (of 20 slides), each headed with the md5 of the
screenshot it was read from, so a re-send is recognised as a duplicate. The screenshots
themselves are not stored — same rule as `video-transcripts-2026-09-02/`: they are session
uploads and the creator's, and the text is what the notes cite.

| Source | Raw path | sha256 (16) | Bytes |
|---|---|---|---|
| `https://raw.githubusercontent.com/safishamsi/graphify/v8/README.md` (fetched 2026-09-04) | `knowledge/raw/instagram-graphify-obsidian-2026-09-04/graphify-README@v8@2026-09-04.md` | `0fb868544a527dff` | 62,662 |
| `https://raw.githubusercontent.com/safishamsi/graphify/main/README.md` (fetched 2026-09-04) | `knowledge/raw/instagram-graphify-obsidian-2026-09-04/graphify-README@main@2026-09-04.md` | `86382f46b8ebc269` | 7,106 |
| 16 Instagram screenshots, @divyannshisharma, received 2026-09-04 | `knowledge/raw/instagram-graphify-obsidian-2026-09-04/slides.md` (frame text; images not stored) | — | 11,550 |

Feeds: [[graphify-features]] (command surfaces, branch trap), `knowledge/VAULT.md` (the
separate-vault route, the bare-stub finding), [[graphify-assessment]] (correction chain
closed), [[llm-wiki-pattern]] (reachable provenance).

## Added 2026-09-04 — `claude-code-docs-2026-09-04/`

The eight `code.claude.com` pages the six Claude Code mechanics notes are built on, re-fetched
in one batch (the notes had carried `fetched: 2026-08-27` for eight days and every value in
them is version-tied). Markdown form — each page serves a `.md` twin that is roughly a tenth
the size of the HTML — stored byte-identical, 900 KB total.

| Page | Raw path | sha256 (16) |
|---|---|---|
| `/docs/en/skills` | `knowledge/raw/claude-code-docs-2026-09-04/skills@2026-09-04.md` | `b7a030ad40a8e613` |
| `/docs/en/sub-agents` | `…/sub-agents@2026-09-04.md` | `fb6189075b5811bc` |
| `/docs/en/mcp` | `…/mcp@2026-09-04.md` | `6fcd70146a05d0ca` |
| `/docs/en/hooks-guide` | `…/hooks-guide@2026-09-04.md` | `72a1eed90101d210` |
| `/docs/en/hooks` | `…/hooks@2026-09-04.md` | `1c1b1218cb523825` |
| `/docs/en/plugins` | `…/plugins@2026-09-04.md` | `d64f8d772d4cf378` |
| `/docs/en/plugin-marketplaces` | `…/plugin-marketplaces@2026-09-04.md` | `ed1d6ff6bd440957` |
| `/docs/en/features-overview` | `…/features-overview@2026-09-04.md` | `f02145dc806e3f21` |

Feeds: [[subagents]] (the only note that changed), and the `sources` frontmatter of
[[skill-anatomy]], [[mcp]], [[hooks]], [[plugins-and-marketplaces]],
[[claude-code-extension-layer]].

## Added 2026-09-04 — `claude-code-docs-2026-09-04b/` and `WATCH.tsv`

A second dated fetch of four pages, hours after the first, because `knowledge/watch.py` reported
they had changed. The morning's directory is NOT overwritten — a source that moves on gets a new
dated directory and the old one stays, which is how the two together became the evidence that the
docs moved twice in one day. Provenance and the per-page diff summary are in that directory's
`README.md`.

`WATCH.tsv` is the freshness baseline: raw path · url · fetched · sha256 of the bytes we read.
`watch.py` re-fetches and compares. It is the answer to "has the source changed since we read
it", which measurement showed is the question the calendar-based `kb.py stale` cannot ask.

## Added 2026-09-04 — `baseline-2026-09-04/`

Fifteen still-fetchable sources stored as a change-detection **baseline** for notes that had no
raw copy at all. Read that directory's `README.md` before citing anything in it: these are
today's bytes, **not** the bytes the citing notes were written from, and the notes' `raw:` keys
say so in as many words. Watch coverage went 10 → 23 sources.

**Deliberately not baselined: 33 URLs on `doi.org`, `arxiv.org` and `usenix.org`.** A published
paper does not change under its own identifier, so watching one is a check that can only return
"same" — and a wall of green would imply the whole base is watched when it is not. The watch list
is every source that CAN move. GitHub pages and Hugging Face model cards can move and are the
next batch.

## Extended 2026-09-04 — `baseline-2026-09-04/` second batch, and what a source is watched AS

Fifty-seven more sources baselined; watch coverage 23 → 75. The rule the batch established is in
that directory's `README.md`: **watch the form that carries the claim, not the URL as written.**
A GitHub repo page changes on every star; its README does not. A Hugging Face model page carries
download counters; its model card does not. Forty-seven sources are never watched, each with a
stated reason — 39 immutable (DOI, arXiv, USENIX, PDFs), 7 volatile by design (social posts, a
leaderboard, gists), 1 issue thread.

Four baselines were fetched and then dropped from the watch list for returning different bytes on
two fetches seconds apart. The test's own limit is recorded with them: one double-fetch can prove
instability and can never prove stability.

## Added 2026-09-08 — `ownership-2026-09-08/`

One file, fetched to settle a candidate `kb.py owners` had been reporting since 2026-09-04.

| Source | Stored as | sha256 (16) | Bytes |
|---|---|---|---|
| `https://raw.githubusercontent.com/aaif-goose/goose/HEAD/README.md` (fetched 2026-09-08) | `knowledge/raw/ownership-2026-09-08/raw.githubusercontent.com_aaif-goose_goose_HEAD_README.md.md` | `0f1df85a0c457caf` | 3,449 |

**Byte-identical to the `block/goose` baseline taken four days earlier** — the same sha256, not
merely the same length. That is what a repository transfer looks like from outside: both paths
answer 200 with the same bytes, so no watcher, no fetch and no hash could ever have raised it.
What settled it was the KIND of self-link the README carries, not how many: see that directory's
own README, and `kb.py owners`, which now reports the live-link count.

WATCH.tsv is 75 rows.

## Added 2026-09-08 — `untried-surfaces-2026-09-08/`

Eleven files. The selection rule was not "which claim is weakest" but **"which note names a
surface nobody opened"** — every source here was named as unfetched, unread or unrenderable in
the note that needed it. All of them answered. Full per-file accounting, and what each settled,
is in that directory's own README.

Two are deliberately **outside** WATCH.tsv and the README says why: the arXiv papers (a
published work does not change under its identifier) and the Hugging Face org listing (its
payload carries download counters, so it would report CHANGED every day and teach the reader to
ignore the column).

WATCH.tsv is 88 rows.

## Added 2026-09-08b — `watch-2026-09-08b/`, and the count went DOWN

Four files: the `code.claude.com` pages the watcher's second batch found carrying real content
changes (`model-config`, `llm-gateway-protocol`, `skills`, `hooks`). Their 2026-09-04 copies stay
where they are — they are the provenance of the rows those four superseded. Per-file accounting,
the triage of all eight CHANGED rows, and the measurement behind the new `noise` verdict are in
that directory's own README.

**WATCH.tsv is 91 rows, one FEWER than before, and that is the finding.** The same URL
(`getzep/graphiti`'s README) was watched twice, at two paths holding byte-identical copies — so
every run fetched it twice, paused twice, and reported the same source to the reader twice. It
had been that way since the re-fetch on 2026-09-08 stored a second copy instead of recognising
unchanged bytes. Nothing was deleted: the duplicate **row** was removed and both files remain.

**What that duplicate really exposed is that this file's own shape was never checked.** The
watcher validated the sources; nothing validated the list of sources. `watch.py --offline` now
runs on every push — no network, because none of it ever needed one:

- every row has four fields and a well-formed sha256;
- no path and no URL appears twice;
- every stored file named by a row exists, **and still matches its recorded sha** — the TAMPER
  check, which compares our bytes to our own record and was running only once a week in the
  network job for no reason;
- every stored raw file is accounted for: watched, superseded by a newer copy of the same page,
  pinned at a commit (`name@ref@sha`, immutable by construction), or named in `NEVER_WATCHED`
  with the reason it cannot be watched.

That last check is what turns the coverage number from an inspection into an invariant.
**198 raw files: 91 watched, 107 accounted for without being watched, 0 unexplained.** The 107
are 44 video transcripts, 42 pinned repo snapshots, 4 carousel screenshots, 3 arXiv captures,
1 Hugging Face listing with download counters in its payload, and 13 superseded baselines. Before
today that breakdown was true and unchecked; the next ingest is what unchecked does not survive.

## Added 2026-09-08c — `watch-2026-09-08c/`, five sources RECOVERED

Nothing new was found. Five pages this base already cited were being watched by nobody, and four
of them had been **deliberately dropped** on 2026-09-04 for returning different bytes on two
fetches seconds apart. That was the right call while the watcher could only compare bytes.

The `noise` verdict made them watchable. Re-tested: all four are byte-different and visible-text
**identical** (prose 1.5%–37.3% of the page), so they were never unstable in the part any note
cites. `anthropic.com/engineering/managed-agents` came back byte-*stable*, which is precisely the
case that drop note's own caveat warned about — it was dropped on an intermittent property. The
fifth, `docs.z.ai/guides/overview/pricing`, was never dropped and never watched: a pricing page
cited for its numbers, which is the last kind of source that should be unwatched.

**Two rows this batch tried to add and could not.** The Hugging Face `LICENSE` files for
`zai-org/GLM-5.3` and `moonshotai/Kimi-K3` were already watched from `baseline-2026-09-04`, and
the duplicate-URL check added hours earlier caught it in the same minute — stopping its own author
rather than a hypothetical future editor. The copies made minutes before were removed unbuilt;
nothing that had ever been provenance was touched.

**WATCH.tsv is 96 rows.** Live run: 87 unchanged · 0 changed · 9 noise · 0 unreachable ·
0 tampered.

**Coverage from the notes' side, measured for the first time** (`watch.py --coverage`, a report
and never a gate): **135 cited URLs — 85 watched, 40 immutable by kind, 10 to check by hand.** All
ten were checked and all ten fall in the volatile-by-design class this file already declares: two
gists, two social posts, a leaderboard, a playlist, a store listing, an issue thread, a licence
pinned at a tag, a news article. That check's first answer was 84, and it was wrong — naive URL
equality does not know the rule this file states two sections above, *watch the form that carries
the claim*. Mapped forms took it to 22; two of those were still artifacts. Hence: report, not gate.
