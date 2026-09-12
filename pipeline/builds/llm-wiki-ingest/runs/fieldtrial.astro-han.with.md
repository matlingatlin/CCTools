Done. Lint (by hand) is clean: 0 dangling wikilinks, 0 unlisted notes, 0 orphans, the raw reference resolves, and every quote in the new text is verbatim in the raw except the two I explicitly flag as README-not-SKILL.md.

## Files changed

| File | Change |
|---|---|
| `wiki/raw/2026-09-02-astro-han-karpathy-llm-wiki-SKILL.md` | **new** — byte-identical copy of the source (md5 `60184773c75ed3693ce45a30c7227645`, 14342 B, 233 lines) |
| `wiki/raw/MANIFEST.md` | **new** — raw/ was empty and had no manifest; provenance row (source, fetch date, hash, size, which note it feeds) |
| `wiki/notes/llm-wiki-pattern.md` | raw added to frontmatter `sources`; new section *"The Astro-Han SKILL.md read in full — six mechanisms the summary above missed"*; one existing quote corrected to the raw's exact wording |
| `wiki/notes/research-methodology.md` | cascade — step 6 now names `[[llm-wiki-pattern]]` in prose with the parallel-search/serial-compile rule |
| `wiki/SOURCES.md` | re-read row under the existing Astro-Han entry, with hash and what it fed |
| `wiki/LOG.md` | operation entry (the file held only its heading) |
| `wiki/INDEX.md` | **untouched** — an update, not a new page; the existing row still describes the note |

## Triage: **update**, and why it wasn't "no material"

`llm-wiki-pattern` already owns this topic *and already cites this exact URL* — `SOURCES.md` said "and its SKILL.md … fetched 2026-09-02", and the comparison table has an Astro-Han row. That is the shape of a no-material ingest, so I checked claim by claim instead of assuming either way. The earlier row was written from the README plus a partial read, and the full file carries six load-bearing mechanisms the note does not hold: the **Grounding Invariant** with its owner per phase and the argument that immutability is what makes the checker stateless; fidelity of *written form* ("if the source says 42K, write 42K, not 42,000", derived values must show greppable components) — stricter than our DERIVED verdict; the no-material log heading as a **machine-readable inventory key** that suppresses the unreferenced-raw report; parallel search / serial compile; cascade must not trust the index; and the archive-never-cascades and one-level-depth carve-outs. New claims from a fuller read of the same document is not corroboration, so `update` — extend the owning page, no rival page.

Two things fell out of the check worth having: the note's "50K–100K tokens … grep and read are more reliable" and "no source hashes / vector search / MCP" quotes are **not in this file** (grep confirms) — they're README claims, now marked as such; and its quote of the fidelity rule had silently elided "(grep or read)", now exact. Everything I added is graded **REPEATED** — the file is a method document with no benchmark, sample or before-and-after anywhere in it.

## What the skill did not tell me how to handle

- **No lint script.** Step 7 says "run the wiki's deterministic lint", but this wiki has no `kb.py` or equivalent — only `INDEX.md`, `SOURCES.md`, `LOG.md`, `notes/`, `raw/`. I wrote a throwaway checker in the scratchpad (dangling links, unlisted, orphans, one-way, raw-ref resolution, quote-in-raw) rather than skip the step. The skill should say what to do when the lint doesn't exist — hand-check and say so, or build one.
- **Provenance vs. an unedited raw.** The skill wants URL, fetch date and hash kept with the raw, *and* the raw never edited. Those conflict for a byte-identical copy. I resolved it with a `MANIFEST.md` alongside; the skill names `MANIFEST.md` only in its "In this repo" section, so it reads as project-specific rather than as the general answer.
- **The log row has no format.** `LOG.md` was one heading, and the skill just says "one entry saying what was ingested and what it changed". I invented a shape. Notably the ingested source itself specifies an exact machine-readable heading for the no-material case — that's a spec the skill would benefit from adopting, and the note now says so.
- **`SOURCES.md` has no row for re-reading a source already logged.** Its table is `| Date | Source | Type | Status | Feeds into |` with a free-text "Added 2026-09-02" tail; I nested the re-read under the existing entry rather than adding a duplicate row, since the skill's "one row per consulted source" doesn't cover a second, deeper read of the same one.
- **Pre-existing finding, not fixed:** `research-methodology` → `testing-skills-methodology` is a one-way link. It predates this ingest and isn't a neighbour my new material names, so per the skill's scope it belongs to `kb-curator`, not here.