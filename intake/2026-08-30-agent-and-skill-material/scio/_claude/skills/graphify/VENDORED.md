# Vendored from graphifyy

**Package:** `graphifyy` **0.9.50**
**Refreshed:** 2026-08-26, via `graphify install --platform claude`
**Contents:** `SKILL.md` (713 lines) + `references/` (8 files, ~44 KB)

## Why this file exists

The previous vendored copy was **1,208 lines and wrong**. It called
`check_semantic_cache(all_files)` and unpacked three return values; the package returns **four**
(`cached_nodes, cached_edges, cached_hyperedges, uncached`) and takes `root=` and `prompt_file=`.
1,153 lines differed.

Two conclusions in this repo were wrong because of it, and both are corrected here:

- `docs/REVIEW-WHOLE.md` records that the vendored file's sha matched its pin, so upstream had
  drifted from the package and **re-fetching could not fix it**. Re-fetching fixed it. The stale
  copy predated the package.
- The same review found *"zero use of progressive disclosure"* across our sixteen skills and named
  graphify's 1,204 lines as the example. **Upstream uses progressive disclosure**: `SKILL.md` loads
  a `references/*.md` only when its step is reached — *"Load it only here… a pure-code corpus has
  skipped Part B and never reads it."* We vendored a monolithic older version and then criticised
  it for being monolithic.

A local frontmatter fix was also applied to the old copy, adding a when-clause because its
description could never fire from context. **Upstream's description already has one**, so that
patch is dropped rather than carried.

## Refreshing

```bash
pip show graphifyy                       # confirm the version first
graphify install --platform claude       # writes ~/.claude/skills/graphify/
```

Then copy `SKILL.md` and `references/` here and update the version above.

**Side effect worth knowing:** `graphify install` also creates `~/.claude/CLAUDE.md` if absent —
it writes outside the project.

## The standing rule this cost us

Pin the package version and re-fetch **deliberately**. A vendored skill that drifts is worse than
no skill, because it is trusted. Check the signature of anything it tells you to call against the
installed package before believing it.
