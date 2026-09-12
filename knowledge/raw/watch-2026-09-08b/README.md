# The watcher's second batch, 2026-09-08 — and the question it finally asked right

Eight rows reported `CHANGED`. **Four carried no words at all.** The first batch's ratio was
1 real in 4; this one is 4 in 8, but the interesting half is the noise, because it is where the
tool changed.

## Triage, row by row

| source | what actually changed | verdict |
|---|---|---|
| `code.claude.com/docs/en/model-config.md` | pinned third-party models now display the model's **name** when Claude Code recognises the id, not the raw id; `availableModels` wording split; `ANTHROPIC_DEFAULT_*_MODEL_NAME` default restated | **REAL.** `model-routing-free-and-local` §9 |
| `code.claude.com/docs/en/llm-gateway-protocol.md` | same theme: a discovered entry uses `display_name` only when it *differs from the id*, else the recognised model name | **REAL.** same section |
| `code.claude.com/docs/en/skills.md` | one sentence added to the `/skill-doctor` report: *"start with the ones that have the highest context cost"* | **REAL.** `skill-anatomy` |
| `code.claude.com/docs/en/hooks.md` | one **link target** moved: `/docs/en/settings#available-settings` → `/docs/en/settings-reference#wslinheritswindowssettings` | true change, **no claim touched** — checked, not assumed: no note in this base cites `/docs/en/settings` |
| `claude.com/customers/block` | Webflow republish: `Last Published` timestamp + two CSS bundle hashes. **Byte length identical.** | **noise**, 0 words |
| `augmentcode.com/.../graphify-…` | Vercel `?dpl=` deploy id, 297 occurrences. **Byte length identical.** | **noise**, 0 words |
| `unsloth.ai/docs/models/glm-5.3` (+ `-flash`) | GitBook deploy id, asset hashes, chunk numbers | **noise**, 0 words — same two rows as the first batch |

A fifth noise row (`goose-docs.ai/.../providers/`) appeared between two runs minutes apart: a
single Docusaurus `runtime~main.<hash>.js` filename. It is the first row the new mechanism
classified with nobody looking, and it was verified by hand afterwards — correctly.

## Why no normaliser can fix this, proven rather than argued

The first batch wrote a narrow normaliser for the unsloth deploy id and deleted it when asset
hashes and chunk numbers turned out to churn too. This batch found the harder reason, on the
graphify page:

- Neutralising every occurrence of the literal deploy id left the page **unequal**.
- The residue is the *same* id, **split across a `<script>` boundary** by the Next.js RSC
  stream — a head like `dpl_ER3bSZGveTFG36zRe` closing one chunk and a tail like
  `YSGaVCMyiVsggS9bc` opening the next, neither carrying the `dpl_` prefix a regex matches on.
- Equality needed scrubbing every **prefix and suffix** of the id, ≥8 chars, both sides. That
  normaliser needs the answer in order to produce it. It is not a normaliser.

## So the question changed

Not *"can the noise be normalised away"* but *"is the noise even in the part we cite"*. It is
not. Measured over the four pages, **the visible text is 0.7–4.4% of the bytes** and all four
are byte-identical under it. `watch.py` now reports such a row as `noise`, and `noise` does not
fail the run.

The relaxation is scoped and the blind spot is measured, not hoped for:

- The byte comparison and the `TAMPERED` check are **unchanged** and never relaxed. The text
  question is asked *only* after bytes differ, *only* for a stored copy that is HTML, and *only*
  when that copy verifies against its recorded sha — a tampered baseline is not evidence that
  today's page says the same thing.
- Markdown keeps the strict byte comparison. `Custom model (<model-id>)` is real content in
  `model-config.md`, and a tag-stripper eats it. That is a selftest fixture, not a caveat.
- 16 mutations across the four live pages, 4 each: a changed prose word fires, a deleted
  paragraph fires, a changed **link target does not**, a changed script payload does not. The
  link-target blindness is asserted as a fixture named `KNOWN BLIND SPOT` so that the day it
  becomes unacceptable, the decision is revisited where it was made.
- `watch.py --selftest` is offline, runs in CI next to `kb.py check`, and 5 mutations of the
  predicate were each caught by it.

## What this batch retired

The two `KNOWN-NOISY` comment blocks in `WATCH.tsv` (ten lines for two rows) told the reader to
triage the diff before believing the row. The tool now does that itself, so the annotation had
become a stale instruction. They are gone; the header says what a `noise` verdict is instead. A
newly-noisy page now earns the verdict **without an edit** — which is how the goose row was
classified before anyone knew it was noisy.

## One more thing the batch exposed: the list itself was never checked

The watcher validated the sources and nothing validated the LIST of sources. Measured the same
day: the same URL (getzep/graphiti README) sat in WATCH.tsv **twice**, at two paths holding
byte-identical copies — a wasted fetch and a doubled report on every run since 2026-09-08. The
duplicate row is gone (both files stay; nothing in the raw layer is deleted), and the class is
now closed by `watch.py --offline`, which runs on **every push** because none of it needs a
network: four fields and a well-formed sha per row, no duplicate path or URL, every named file
present **and still matching its recorded sha**, and every stored raw file accounted for as
watched, superseded, pinned at a commit, or declared unwatchable.

That moves the TAMPER check from a weekly network job to every push — it compares our bytes to
our own record and never needed the internet — and turns `198 raw files: 91 watched, 107
accounted for, 0 unexplained` from an inspection into an invariant.

Nothing here was edited after fetching; every file is stored as received. The 2026-09-04 copies
are kept, because they are the provenance of the rows these four superseded.
