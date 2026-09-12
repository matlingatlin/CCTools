# Operation log

One entry per operation: what was ingested, the triage, what it changed (or why nothing did).

## [2026-09-03] ingest | update: llm-wiki-pattern
- Disposition: Update (one page already owns the topic; extended, not rivalled)
- Source: SKILL.md of github.com/Astro-Han/karpathy-llm-wiki, fetched 2026-09-02
- Raw: `raw/2026-09-02-astro-han-karpathy-llm-wiki-SKILL.md` (md5 60184773c75ed3693ce45a30c7227645);
  `raw/MANIFEST.md` created — the raw layer had no manifest and a byte-identical copy cannot
  carry its own provenance
- Changed: `notes/llm-wiki-pattern.md` — new section "The Astro-Han SKILL.md read in full",
  six mechanisms the earlier README-based table row missed, all graded REPEATED (the file
  measures nothing); raw added to frontmatter sources; one quote in the comparison table
  corrected to the raw's exact wording ("(grep or read)" had been elided); two quotes in that
  row identified as README claims absent from this file
- Updated: `notes/research-methodology.md` — step 6 now names [[llm-wiki-pattern]] in prose
  with the parallel-search/serial-compile rule; the link existed in `related:` only
- Registered: `SOURCES.md` re-read row
- Not touched: `INDEX.md` (no new page; the existing row still describes the note)
- Lint: by hand — this wiki carries no lint script (see the ingest report)
