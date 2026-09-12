# Why each step exists — the observed failures behind llm-wiki-ingest

Open this when a step seems optional. Every rule in SKILL.md is here with the run or the
source it came from; a rule with nothing behind it does not belong in the body.

- **The trigger is "I now know something and I verified it", not "the task is finished".**
  A finding that lives only in a conversation is lost at the next compaction, silently. Seen
  twice in one session in the host repository's history (its steering file's "a verified fact
  lands the same turn" rule was written after those two).
- **Raw kept, never edited.** A page whose raw is gone cannot be re-derived when the URL rots.
  Karpathy's LLM Wiki names `raw/` as the immutable layer; the field trial of 2026-09-03 added
  a `raw/MANIFEST.md` (source, fetch date, hash, size, which note it feeds) because provenance
  cannot live inside a file that must stay byte-identical.
- **One page owns a topic; extend, never rival.** Two pages on one topic are the lint error
  a whole-wiki clean-up pass spends the most time on (duplicate findings).
- **No material means no page is touched.** Observed 2026-09-02 in the first build's probes:
  on a blog post restating two multipliers a note already held, every baseline run (2 of 2)
  still edited the owning page - a "corroborating" source entry plus a claims row. A page's
  source list says what the page was *derived from*, not what agrees with it. The
  implementation that names the disposition says the same: "No material — adds no knowledge
  beyond what the wiki already holds. Keep the raw file, log it (see Post-Ingest), and stop.
  Do not force an article out of a thin source." (Astro-Han karpathy-llm-wiki SKILL.md,
  fetched 2026-09-02, verified by an external reader). The source-log row still happens - the
  source *was* consulted - and so does the operation-log line.
- **Disputed: both values kept as dated rows, the page marked.** A GUARD, not an observed
  failure: in the first build's probes the bare baseline already kept both values on every
  run (T2, 2 of 2), so this rule has no delta behind it. It stays because the failure it
  guards - one value silently overwriting the other - is the one a wiki cannot detect after
  the fact, and the case is the one the LLM Wiki gist names for its lint ("contradictions").
  It is graded by code so it costs no judgement. Marked guard so the next build can decide
  whether a guard with no delta earns its lines.
- **The status vocabulary and the as-of date on values.** Also guards, from the whole-
  artefact reviews of 2026-09-02/03 rather than a run: a page whose status is undefined
  cannot be linted, and a value without an as-of date cannot be judged no-material later.
- **Quote before write; MEASURED / REPEATED / DERIVED.** Without a verbatim line a claim is
  indistinguishable from a reconstruction, and reconstructions drift toward the argument they
  were recalled for. A claim is not promoted by being repeated more often. DERIVED exists
  because a claim-gatherer once hit a figure computed from parameters its own author called
  fictional and had only two labels to choose from.
- **Cascade with a sentence, not an edge.** Parallel authoring produces one-way links
  structurally; a `related:` entry alone is an edge nobody argued. The first lint over the host
  repository's 44 notes found 33 one-way links and 6 dangling ones.
- **Register: map of contents by hand, search index generated.** They are different things;
  the first draft of this skill conflated them and the whole-artefact review caught it.
- **Lint in the same commit.** A verified fact and its lint pass land together; otherwise the
  lint runs when someone asks, which is never.

**Before and after, no material:** a blog post restates two multipliers a note already
carries with a dated source. *Before:* the note gains the blog as a "corroborating" source and
a claims row. *After:* the note is untouched; the log says `no material: <url> restates
prompt-caching's 0.1x / 1.25x, no new claim`; the raw is kept; the source log gains a row.

*In this repo (one instance):* the host repository above is `matlingatlin/skills-repo`; the clean-up pass is its `kb-curator` agent; the steering file is its `CLAUDE.md`.
