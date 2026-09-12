---
name: apply-llm-edits
description: Use when applying model-produced code edits to source files and an exact string match fails or is risky — SEARCH/REPLACE editblocks, unified diffs (@@ hunks), or fenced before/after pairs that drift on whitespace, indentation, or stale surrounding context. Covers reconciling an LLM patch against a file that moved, choosing a diff format to emit, resolving fuzzy-match ambiguity, and verifying a patch landed. Not for writing new files from scratch, not for git merge-conflict resolution, and not for reviewing edits for correctness (see code-review).
---

Robustly apply model-produced edits to source when exact-match patching fails, because LLM patches routinely drift on whitespace, indentation, and stale context.

## When to use
- A model emitted an edit (editblock, unified diff, or before/after pair) and the anchor text no longer matches the file byte-for-byte.
- You must pick a diff format to emit for a downstream applier.
- A patch applied to the wrong location or silently no-op'd and you need to reconcile it.

Do NOT use for: authoring brand-new files, git merge-conflict markers, or judging whether an edit is *correct* (that is code-review / simplify).

## Format shapes
- **Editblock** — a search body between `<<<<<<< SEARCH` and `=======`, and a replace body between `=======` and `>>>>>>> REPLACE`. One file may carry several, applied top to bottom.
- **Unified diff** — one or more `@@ -a,b +c,d @@` hunks; ` ` context lines, `-` removed, `+` added. Line numbers in the header are hints only — never trust them over content.
- **Before/after pair** — two adjacent fenced blocks (or a "replace X with Y" instruction); treat the first as search, the second as replace.

## Steps
1. **Read the target file** in full so every match runs against current bytes, not the model's assumption of the file.
2. **Identify the format.** SEARCH/REPLACE block (`<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE`), unified diff (`@@ … @@` with `-`/`+` lines), or a fenced before→after pair. Parse into ordered (search, replace) pairs; for unified diffs reconstruct the search text from context+`-` lines and the replace text from context+`+` lines. An empty search text means insert-only — resolve its position from the surrounding context lines.
3. **Try exact match first.** Search the file for the verbatim search text. If exactly one match, apply and go to step 7. If zero or many, continue.
4. **Whitespace-tolerant match.** Compare lines with leading/trailing whitespace stripped and runs of internal whitespace collapsed. Track the original indentation of the matched region so the replacement can be re-indented to it.
5. **Anchored fuzzy match.** If still unmatched, match on the most distinctive interior lines (ignore blank and pure-context lines), then expand outward to confirm neighbors. Compute a similarity ratio over the candidate window; accept only above a high threshold (e.g. ~0.85). If a block is large, try matching its first and last few lines as anchors and treat the interior as the region to replace.
6. **Resolve ambiguity.** More than one acceptable location = STOP and report the candidates with line numbers; do not guess. Prefer the candidate whose surrounding context lines also match. When blocks are ordered, prefer the earliest still-unconsumed match so later blocks don't collide with earlier ones.
7. **Re-indent and splice.** Apply the replacement using the matched region's indentation, not the patch's. Preserve the file's existing line-ending and final-newline convention.
8. **Verify.** Re-read the spliced region; confirm the replace text is present and the search text is gone. Re-check that no unrelated line count shifted. Report each block as applied / ambiguous / not-found with line numbers.

## Rules
- Method only: no shell patch tools, no network, no auto-run hooks — reason over file text you have Read.
- Never apply on an ambiguous or below-threshold match; report and stop instead.
- One block failing does not roll back blocks already cleanly applied; report per-block status.
- Match on content, re-indent to the target; never let patch indentation overwrite the file's.
- Preserve original line endings, encoding, and trailing-newline state.
- Emitting edits: choose SEARCH/REPLACE for localized changes with a unique anchor; unified diff for multi-hunk or line-addressed changes. Always include enough unique context to disambiguate.
- Do not reformat, resort imports, or touch lines outside the patched region.
